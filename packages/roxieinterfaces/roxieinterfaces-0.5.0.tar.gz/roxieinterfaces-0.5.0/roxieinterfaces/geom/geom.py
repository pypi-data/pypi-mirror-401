# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause
import collections
import logging
import math
from dataclasses import dataclass, field

import cadquery
import numpy as np
import pandas as pd
from roxieapi.commons.types import BlockTopology, Coil3DGeometry
from roxieapi.input.builder import RoxieInputBuilder
from roxieapi.output.parser import RoxieOutputParser
from scipy.sparse import csr_array
from scipy.sparse.csgraph import breadth_first_order
from tqdm.autonotebook import tqdm

from roxieinterfaces.geom._cadquery import CadProvider
from roxieinterfaces.geom.math_tools import (
    add_insulation_thickness,
    get_intersection_line_cylinder,
    normalize_vectors,
)


@dataclass
class BlockParams:
    """Parameters for a single block."""

    block_nr: int
    ins_r: float
    ins_phi: float
    origin_block: int
    radial_nr: int | None = None
    angular_nr: int | None = None
    z_dir: int | None = None
    part_half: int | None = None
    block_type: int | None = None
    z_idx: int | None = None  # Z index (inner to outer) within layer


@dataclass
class LayerParams:
    """Parameters for a single layer."""

    layer_nr: int
    radii: tuple[float, float]  # (inner, outer)
    blocks: list[int] = field(default_factory=list)
    quadrants: set[int] = field(default_factory=set)
    symmetry: int = 1
    max_z: float = 0.0


class GeometryBuilder:
    """Builder interface for collecting geometries to build and then generating different targets.

    Functions starting with add_ will add components in the list to generate.

    Example usage:
        stepGen.builder().add_blocks(1, 2, 3, 4).with_coils().with_insulations().generate()
        stepGen.builder().add_conductors(23).with_coils(add_insulation=True).generate()
    """

    def __init__(self, step_gen: "StepGenerator"):
        self._step_gen = step_gen

        self._coils: set[int] = set()
        self._blocks: set[int] = set()
        self._spacers: set[tuple[int, int, int, int, int]] = set()

        # What to generate
        self._gen_coils: bool = False
        self._gen_insulations: bool = False
        self._gen_blocks: bool = False
        self._gen_endspacers: bool = False

        # Generation options
        self._add_insulation_to_coils: bool = False
        self._endspacer_add_z: float = 0.0
        self._endspacer_zmax: float | None = None
        self._endspacer_min_width: float | None = None

    def add_conductors(self, *conductor_id: int) -> "GeometryBuilder":
        """Add one or more conductors to generate.

        :param coil_id: The coil ids to add
        :return: self for method chaining
        """
        self._coils.update(conductor_id)
        return self

    def add_blocks(self, *block_id: int, also_conductors: bool = True) -> "GeometryBuilder":
        """Add one or more blocks to generate.

        :param block_id: The block ids to add
        :also_conductors: Also add coils for the block
        :return: self for method chaining
        """
        self._blocks.update(block_id)
        if also_conductors:
            self._coils.update(self._conductors_for_blocks(*block_id))
        return self

    def add_coil_section(
        self,
        radial_nr: int | None = None,
        angular_nr: int | None = None,
        z_dir: int | None = None,
        halfid: int | None = None,
        idx: int | None = None,
        also_conductors: bool = True,
    ) -> "GeometryBuilder":
        """Add Spacers to generate.

        Adds Spacers to generate based on radial, angular, z direction, half id and index.
        Each can be set to None to include all.

        :param radial_nr: The radial number of the coil (inner to outer), or None for all
        :param angular_nr: The angular number of the coil (starting at 1, mathematical angle order), or None for all
        :param z_dir: Z direction: 1 for positive z, -1 for negative z, None for both
        :param halfid: Half ID of the block part (0 for first half, 1 for "mirrored" half), or None for all
        :param idx: Index of the block in z direction (0 for inner_post, increasing for each spacer), or None for all
        """
        spacers, blocks = self._blocks_for_part(radial_nr, angular_nr, z_dir, halfid)

        for k, v in spacers.items():
            vs = v if idx is None else [idx] if idx in v else []
            for i in vs:
                self._spacers.add((*k, i))

        if idx is not None:
            blocks_filtered = []
            for bid in blocks:
                bl = self._step_gen._blocks[bid]
                if bl.z_idx == idx - 1 or bl.z_idx == idx:
                    blocks_filtered.append(bid)
            self.add_blocks(*blocks_filtered, also_conductors=also_conductors)
        else:
            self.add_blocks(*blocks, also_conductors=also_conductors)

        return self

    def add_all(self, also_conductors: bool = True) -> "GeometryBuilder":
        """Add all coils, blocks and spacers to generate.
        :param also_conductors: Also add coils for the blocks
        :return: self for method chaining
        """
        self.add_coil_section(None, None, None, None, None, also_conductors=also_conductors)
        return self

    def add_coil(self, radial_nr: int, angular_nr: int, also_conductors: bool = True) -> "GeometryBuilder":
        """Add a whole coil to generate.

        :param radial_nr: The radial number of the coil (inner to outer)
        :param angular_nr: The angular number of the coil (starting at 1, mathematical angle order)
        :also_conductors: Also add conductors for each block (default: True)

        :return: self for method chaining

        """
        self.add_coil_section(
            radial_nr,
            angular_nr,
            None,
            None,
            None,
            also_conductors=also_conductors,
        )
        return self

    def _conductors_for_blocks(self, *block_id: int) -> set[int]:
        """For a given list of blocks, find all coils corrosponding to it"""

        coils = {cid for cid, c in self._step_gen._coils.items() if c.block_id in block_id}
        return coils

    def _blocks_for_part(
        self, radial_nr: int | None, angular_nr: int | None, z_dir: int | None, halfid: int | None
    ) -> tuple[dict[tuple[int, int, int, int], list[int]], list[int]]:
        """For a given radial, angular and z position, return all blocks.

        :param radial_nr:
        :param angular_nr:
        :param z_dir:
        :param halfid:

        :return: Set of blocks in given range
        """
        block_ids: set[int] = set()
        block_dict: dict[tuple[int, int, int, int], int] = collections.defaultdict(int)
        for bl_id, bl in self._step_gen._blocks.items():
            bl = self._step_gen._blocks[bl_id]
            if (
                (radial_nr is None or bl.radial_nr == radial_nr)
                and (angular_nr is None or bl.angular_nr == angular_nr)
                and (z_dir is None or bl.z_dir == z_dir)
                and (halfid is None or bl.part_half == halfid)
                and bl.block_type in self._step_gen._supported_block_types
            ):
                block_ids.add(bl_id)
                # Only add to dict if all required fields are non-None
                if (
                    bl.radial_nr is not None
                    and bl.angular_nr is not None
                    and bl.z_dir is not None
                    and bl.part_half is not None
                ):
                    block_dict[(bl.radial_nr, bl.angular_nr, bl.z_dir, bl.part_half)] += 1
        es_dict = {k: list(range(v + 1)) for k, v in block_dict.items()}
        return es_dict, list(block_ids)

    # Generation target methods (return self for chaining)
    def with_coils(self, add_insulation: bool = False) -> "GeometryBuilder":
        """Generate coil geometries.

        :param add_insulation: Whether to include insulation in coil geometry
        :return: self for method chaining
        """
        self._gen_coils = True
        self._add_insulation_to_coils = add_insulation
        return self

    def with_insulations(self) -> "GeometryBuilder":
        """Generate insulation geometries.

        :return: self for method chaining
        """
        self._gen_insulations = True
        return self

    def with_blocks(
        self, coilblock_dr: float = 0.0, overwrite_radii: dict[int, tuple[float, float]] | None = None
    ) -> "GeometryBuilder":
        """Generate coil block geometries.

        :return: self for method chaining
        """
        self._gen_blocks = True
        self._coilblock_dr = coilblock_dr
        self._overwrite_block_radii = overwrite_radii
        return self

    def with_endspacers(
        self, add_z: float = 0.0, zmax: float | None = None, min_width: float | None = None
    ) -> "GeometryBuilder":
        """Generate endspacer geometries.

        :param add_z: Additional z extension of endspacer
        :param zmax: Optional maximum z extension (overrides add_z and coil length)
        :param min_width: Minimum width of endspacer
        :return: self for method chaining
        """
        self._gen_endspacers = True
        self._endspacer_add_z = add_z
        self._endspacer_zmax = zmax
        self._endspacer_min_width = min_width
        return self

    def generate(self) -> cadquery.Assembly:
        """Execute the geometry generation based on accumulated filters and targets."""
        # Count total tasks for outer progress bar
        total_tasks = sum([self._gen_coils, self._gen_insulations, self._gen_blocks, self._gen_endspacers])
        #            zmax = max([np.abs(c.geometry.nodes[-1, 2]).max() for c in coils.values()])
        # Find max z
        if self._gen_endspacers and not self._endspacer_zmax:
            max_z = max(
                [
                    np.abs(c.geometry.nodes[-1, 2]).max()
                    for c in self._step_gen._coils.values()
                    if c.block_id in self._blocks
                ]
            )

            if self._endspacer_add_z:
                max_z += self._endspacer_add_z
            self._endspacer_zmax = max_z

        with tqdm(total=total_tasks, desc="Generating geometries") as outer_pbar:
            # Generate coils
            if self._gen_coils:
                outer_pbar.set_description(f"Generating {len(self._coils)} coils")
                for coil_id in tqdm(self._coils, desc="Coils", leave=False):
                    self._step_gen.get_coil_geom(coil_id, self._add_insulation_to_coils)
                outer_pbar.update(1)

            # Generate insulations
            if self._gen_insulations:
                outer_pbar.set_description(f"Generating {len(self._coils)} insulations")
                for coil_id in tqdm(self._coils, desc="Insulations", leave=False):
                    self._step_gen.get_insulation_geom(coil_id)
                outer_pbar.update(1)

            # Generate blocks
            if self._gen_blocks:
                outer_pbar.set_description(f"Generating {len(self._blocks)} blocks")
                for block_id in tqdm(self._blocks, desc="Blocks", leave=False):
                    self._step_gen.get_coil_block_geom(block_id, self._coilblock_dr, self._overwrite_block_radii)
                outer_pbar.update(1)

            # Generate endspacers
            if self._gen_endspacers:
                outer_pbar.set_description("Generating endspacers")
                for radial_nr, angular_nr, z_dir, halfid, idx in tqdm(
                    self._spacers,
                    desc="Endspacers",
                    leave=False,
                ):
                    self._step_gen.get_endspacer_geom(
                        radial_nr,
                        angular_nr,
                        z_dir,
                        halfid,
                        idx,
                        z_max=self._endspacer_zmax,
                        min_width=self._endspacer_min_width,
                    )
                outer_pbar.update(1)

        return self._step_gen.assembly()


class StepGenerator:
    """Base class for step generators

    (shared functions between classic Step generator and Step generator based only on coils)
    """

    def __init__(
        self,
        roxie_input: RoxieInputBuilder,
        roxie_output: RoxieOutputParser,
        opt_nr=1,
    ) -> None:
        self.logger = logging.getLogger("StepGenerator")

        # Configuration organized by entity
        self._blocks: dict[int, BlockParams] = {}
        self._layers: dict[int, LayerParams] = {}

        # Conductor/coil ordering parameters
        self._conductor_orders: list[list[int]] = []
        self._conductor_order_dict: dict[int, tuple[int, int]]
        self._prepend_continuity_order: bool = False

        # Global geometry configuration
        self._bspline_smoothing_factor = 0.001
        self._bspline_degree = 3
        self._add_ins_r: float | None = None
        self._add_ins_phi: float | None = None

        # Layer ordering (maps radius_order -> list of layer_nrs)
        self._layer_order: dict[int, list[int]] = {}

        # Core utilities
        self._cad = CadProvider()

        self._supported_block_types = (31, 32)

        self.fill_parameters(roxie_input, roxie_output, opt_nr)

    def builder(self) -> GeometryBuilder:
        """Create a geometry builder for fluent generation API.

        :return: A new GeometryBuilder instance for this StepGenerator
        """
        return GeometryBuilder(self)

    def assembly(self) -> cadquery.Assembly:
        """Get the generated assembly.

        :return: The generated assembly
        """
        return self._cad.get_assembly()

    def clear_assembly(self) -> None:
        """Clear the current assembly."""
        self._cad.clear_assemblies()

    def _set_cable_parameters(self, topologies: dict[int, BlockTopology]):
        self._blocks = {}
        for block_nr, bt in topologies.items():
            self._blocks[block_nr] = BlockParams(
                block_nr=block_nr,
                ins_r=bt.ins_radial,
                ins_phi=bt.ins_azimuthal,
                origin_block=bt.block_orig,
            )

    def _get_insulation(self, block_nr: int) -> tuple[float, float]:
        # Check for global default (block 0)
        if block_nr in self._blocks:
            return self._blocks[block_nr].ins_r, self._blocks[block_nr].ins_phi
        if 0 in self._blocks:
            return self._blocks[0].ins_r, self._blocks[0].ins_phi
        raise ValueError(f"No insulation thickness for block {block_nr}")

    def _get_coil_order_prefix(self, coil_nr: int) -> str:
        if self._prepend_continuity_order and coil_nr in self._conductor_order_dict:
            oidx, cidx = self._conductor_order_dict[coil_nr]
            return f"grp_{oidx:02d}_order_{cidx:03d}_"
        return ""

    def fill_parameters(
        self,
        roxie_input: RoxieInputBuilder,
        roxie_output: RoxieOutputParser,
        opt_nr=1,
    ) -> None:
        """Fill the parameters for the step generator from a roxie input and output.

        :param roxie_input: The roxie input object to get the parameters from
        :param roxie_output: The roxie output object to get the parameters from
        """
        self._set_cable_parameters(roxie_output.opt[opt_nr].blockTopologies)
        layer_order: dict[float, list[int]] = {}
        for _, row in roxie_input.layer.iterrows():
            layer_nr = row.no
            layer_symmetry = row.symm // 2
            blocks = row.blocks
            block_radii = [roxie_input.block.loc[roxie_input.block["no"] == b, "radius"].iloc[0] for b in blocks]
            std = np.std(block_radii)
            if std > 10e-3:
                self.logger.warning(
                    f"variation in radii within blocks in layer {layer_nr}:",
                    f"{[(bl, r) for bl, r in zip(blocks, block_radii, strict=False)]}. ",
                    f"Using {block_radii[0]} as radius.",
                )
            r = round(block_radii[0], 2)
            if r not in layer_order:
                layer_order[r] = []
            layer_order[r].append(layer_nr)

            # Create LayerParams for this layer
            if layer_nr not in self._layers:
                self._layers[layer_nr] = LayerParams(
                    layer_nr=layer_nr,
                    radii=(0.0, 0.0),  # Will be set below
                    blocks=blocks,
                    symmetry=layer_symmetry,
                )
            else:
                self._layers[layer_nr].blocks = blocks
                self._layers[layer_nr].symmetry = layer_symmetry

        layer_items = list(layer_order.items())
        layer_items.sort(key=lambda x: x[0])  # Sort by radius
        if len(layer_items) >= 2:
            layer_delta = layer_items[1][0] - layer_items[0][0]
            for r, layers in layer_items:
                for la in layers:
                    self._layers[la].radii = (r, r + layer_delta)
        else:
            self.logger.warning("""There is only one layer, please set coil block manually.
            stepGen.set_coil_block_radii(layer_nr,r_inner,r_outer)
            """)
        self._layer_order = {i + 1: layer_order[r] for i, r in enumerate(layer_order.keys())}
        self._coils = roxie_output.opt[opt_nr].coilGeometries3D

        self._set_block_parameters()
        self._set_block_type(roxie_input.block, roxie_input.block3d)
        self._set_block_order()
        self._fix_bugs()

    def _fix_bugs(self):
        """Apply bug fixes to problems not yet addressed upstream (roxie-api or roxie)"""
        # [Roxie Issue 105](https://gitlab.cern.ch/roxie/ROXIE/-/issues/105)
        for blid, bl in self._blocks.items():
            if bl.block_type == 90:
                for coil in self._coils.values():
                    if coil.block_id == blid:
                        nodes = coil.geometry.nodes
                        dist = sum(np.linalg.norm(nodes[i + 4, :] - nodes[i, :]) for i in range(4))
                        if dist < 1e-8:
                            # The first 2 sets of nodes have the same z coordinate, add an intermediate point into z2
                            for i in range(4):
                                z_mid = (nodes[i + 8, 2] + nodes[i, 2]) / 2
                                nodes[i + 4, 2] = z_mid

    def _set_block_type(self, blocks: pd.DataFrame, blocks_3d: pd.DataFrame) -> None:
        df_merged = blocks.merge(
            left_on="ne",
            right_on="ne",
            right=blocks_3d,
            how="left",
            suffixes=("", "_3d"),
        ).set_index("no")
        for bl in self._blocks.values():
            if bl.origin_block in df_merged.index:
                bl.block_type = df_merged.loc[bl.origin_block, "type_3d"]

    def get_coil_geom(self, coil_id: int, add_insulation: bool = False) -> None:
        coil = self._coils[coil_id]
        prefix = self._get_coil_order_prefix(coil.nr)
        model_name = f"{prefix}coil_{coil.nr:03d}"
        if add_insulation:
            if not coil.geometry.elements:
                raise ValueError("The given coil is missing its element (connectivity) information")
            ins_r, ins_phi = self._get_insulation(coil.block_id)

            nodes = add_insulation_thickness(
                coil.geometry.nodes,
                coil.geometry.elements,
                ins_r,
                ins_phi,
            )
        else:
            nodes = coil.geometry.nodes
        self._cad.magnet_order = self._layers[coil.layer_id].symmetry
        self._cad.make_cable(
            coil.nr, model_name, add_insulation, nodes[::4, :], nodes[1::4, :], nodes[3::4, :], nodes[2::4, :]
        )

    def get_insulation_geom(self, coil_id: int) -> None:
        coil = self._coils[coil_id]
        prefix = self._get_coil_order_prefix(coil.nr)
        model_name = f"{prefix}insulation_{coil.nr:03d}"
        ins_r, ins_phi = self._get_insulation(coil.block_id)
        nodes_outer = add_insulation_thickness(
            coil.geometry.nodes,
            coil.geometry.elements,
            ins_r,
            ins_phi,
        )
        nodes_inner = coil.geometry.nodes
        self._cad.magnet_order = self._layers[coil.layer_id].symmetry
        self._cad.make_insulation(
            coil.nr,
            model_name,
            nodes_outer[::4, :],
            nodes_outer[1::4, :],
            nodes_outer[3::4, :],
            nodes_outer[2::4, :],
            nodes_inner[::4, :],
            nodes_inner[1::4, :],
            nodes_inner[3::4, :],
            nodes_inner[2::4, :],
        )

    def get_zerogap_aligned_coil_geoms(self, coil_list: list[int], add_insulation: bool = True) -> None:
        node_list = []
        for c in coil_list:
            coil = self._coils[c]
            if add_insulation:
                ins_r, ins_phi = self._get_insulation(coil.block_id)
                nodes = add_insulation_thickness(
                    coil.geometry.nodes,
                    coil.geometry.elements,
                    ins_r,
                    ins_phi,
                )
            else:
                nodes = coil.geometry.nodes
            node_list.append((c, nodes))

    def get_zerogap_aligned_coil_geoms_for_block(
        self, coils: dict[int, Coil3DGeometry], coil_block: BlockTopology, add_insulation: bool = True
    ) -> None:
        self.get_zerogap_aligned_coil_geoms(
            list(range(coil_block.first_conductor, coil_block.last_conductor + 1)), add_insulation
        )

    def set_conductor_order(self) -> None:
        """Find a ordered list of connected conductors for all coil blocks.

        Stores continuity and append to name of exported conductors.

        This function iterates through all coils, finds connected conductors (via proximity of the ends
        between conductors) and generates a list of conductor groups, each group containing a list of conductors
        in order of connection. Iterating over the resulting list will lead to a continuous coil from end to end.

        :return: A list of lists, where each inner list contains the ordered conductor IDs for one continuous coil.

        """
        self._prepend_continuity_order = True
        conductor_points = {}
        for geom_id, geom in self._coils.items():
            p_s = np.mean(geom.geometry.nodes[:4], axis=0)
            p_e = np.mean(geom.geometry.nodes[-4:], axis=0)
            conductor_points[geom_id] = (p_s, p_e)

        base_cond = 2
        base_s, base_e = conductor_points[base_cond]
        nr_cond = len(conductor_points)
        threshold = 0.5

        connectivity = csr_array((nr_cond, nr_cond), dtype=int)
        for geom1, (s1, e1) in conductor_points.items():
            nr_conn = []
            for geom2, (s2, e2) in conductor_points.items():
                if geom1 == geom2:
                    continue
                dist_e1_e2 = np.linalg.norm(e2 - e1)
                dist_s1_s2 = np.linalg.norm(s2 - s1)
                if dist_e1_e2 < threshold:
                    connectivity[geom1 - 1, geom2 - 1] = 1
                    nr_conn.append(geom2)
                if dist_s1_s2 < threshold:
                    connectivity[geom1 - 1, geom2 - 1] = 1
                    nr_conn.append(geom2)
        degrees = connectivity.sum(axis=1)
        start_end_nodes = set([i for i in range(nr_cond) if degrees[i] == 1])
        all_nodes = set(range(nr_cond))
        orders = []
        while start_end_nodes:
            n = start_end_nodes.pop()
            node_list = breadth_first_order(connectivity, n, directed=False, return_predecessors=False)
            node_set = set(node_list)
            all_nodes -= node_set
            start_end_nodes -= node_set
            orders.append([c + 1 for c in node_list])
        if all_nodes:
            self.logger.warning(
                f"There are still conductors which could not be assigned to groups: {[c + 1 for c in all_nodes]}"
            )

        order_dict = {}
        for oidx, order in enumerate(orders):
            for cidx, c in enumerate(order):
                order_dict[c] = (oidx, cidx)  # Adjusting for 1-based indexing

        self._conductor_order_dict = order_dict
        self._conductor_orders = orders

    def set_layer_symmetry(self, layer_nr: int, symmetry: int):
        """
        Set the symmetry type of a layer. This is used to determine the number of blocks in a layer.

        :param layer_nr: Layer number to apply symmetry
        :type layer_nr: int
        :param symmetry:
            The symmetry of the layer. 1 = dipole, 2 = quadrupole, 3 = sextupole, ...
        """
        if layer_nr not in self._layers:
            self._layers[layer_nr] = LayerParams(
                layer_nr=layer_nr,
                radii=(0.0, 0.0),  # Will be set later
                symmetry=symmetry,
            )
        else:
            self._layers[layer_nr].symmetry = symmetry

    def set_coil_block_radii(self, layer_nr: int, inner_radius: float, outer_radius: float):
        """
        Set the inner and outer radii of the former for a given layer.

        :param layer_nr: Layer number to apply radii
        :type layer_nr: int
        :param inner_radius:
            The inner radius of the block geometry. The coil
            block can be used as a tool for the boolean operation
            to determine the endspacer, wedge and post geometry.
        :param outer_radius:
            The outer radius of the block geometry. The coil
            block can be used as a tool for the boolean operation
            to determine the endspacer, wedge and post geometry.
        """
        if layer_nr not in self._layers:
            self._layers[layer_nr] = LayerParams(
                layer_nr=layer_nr,
                radii=(inner_radius, outer_radius),
            )
        else:
            self._layers[layer_nr].radii = (inner_radius, outer_radius)

    def set_former_insulation(self, add_ins_r: float, add_ins_phi: float):
        """Add insulation to former geometry
        :param add_ins_r:
            The thickness of the insulation in r direction.
        :type add_ins_r: float

        :param add_ins_phi:
            The thickness of the insulation in phi direction.
        :type add_ins_phi: float
        """
        self._add_ins_r = add_ins_r
        self._add_ins_phi = add_ins_phi

    def _set_block_parameters(self) -> None:
        """Set max Z extend and block part numbers for all coilblocks.

        The block part number is defined as one block plus it's symmetry component.
        E.g for Dipoles, there are 2 coil block parts, for quadrupoles 4, sextupoles 6, etc.
        Coil block parts for Z<0 are negative, for Z>0 positive.


        :return: The block part number.
        :rtype: int
        """

        for _, c in self._coils.items():
            max_z = np.abs(c.geometry.nodes[:, 2]).max()
            self._layers[c.layer_id].max_z = max(
                self._layers[c.layer_id].max_z,
                max_z,
            )
            if c.block_id not in self._blocks or self._blocks[c.block_id].angular_nr is None:
                layer_nr = c.layer_id
                if layer_nr not in self._layers:
                    raise ValueError(f"Layer {layer_nr} has no symmetry set. Use set_layer_symmetry to set it")
                if c.geometry.nodes is None:
                    raise ValueError(f"Coil {c.nr} has no geometry nodes set. Cannot determine block part number")
                z_inner = c.geometry.nodes[-1, 2]
                cable_phi = np.arctan2(c.geometry.nodes[0, 1], c.geometry.nodes[0, 0])
                if cable_phi < 0:
                    cable_phi += 2 * math.pi
                if self._layers[layer_nr].symmetry == 0:
                    continue
                bpn_float = cable_phi / (math.pi / self._layers[layer_nr].symmetry)
                block_part_nr = int(bpn_float) + 1
                part_half = 0 if (bpn_float % 1) < 0.5 else 1
                block_z_dir = 1 if z_inner >= 0 else -1

                radial_nr = None
                for k, v in self._layer_order.items():
                    if layer_nr in v:
                        radial_nr = k
                        break

                if c.block_id in self._blocks:
                    self._blocks[c.block_id].angular_nr = block_part_nr
                    self._blocks[c.block_id].z_dir = block_z_dir
                    self._blocks[c.block_id].part_half = part_half
                    self._blocks[c.block_id].radial_nr = radial_nr
                else:
                    # Create block if it doesn't exist (shouldn't normally happen)
                    self._blocks[c.block_id] = BlockParams(
                        block_nr=c.block_id,
                        ins_r=0.0,
                        ins_phi=0.0,
                        origin_block=c.block_id,
                        radial_nr=radial_nr,
                        angular_nr=block_part_nr,
                        z_dir=block_z_dir,
                        part_half=part_half,
                    )

    def _set_block_order(self) -> None:
        def coil_block_max_z(block_id: int) -> float:
            cb = min([idx for idx, coil in self._coils.items() if coil.block_id == block_id])
            max_z = 0.0
            c = self._coils[cb]
            max_z = max(max_z, np.abs(c.geometry.nodes[-1, 2]).max())
            return max_z

        blockdict: dict[tuple[int, int, int, int], list[int]] = {}
        for b_v in self._blocks.values():
            if b_v.block_type not in self._supported_block_types:
                continue
            # Skip blocks with None values
            if b_v.radial_nr is None or b_v.angular_nr is None or b_v.part_half is None or b_v.z_dir is None:
                continue
            key = (b_v.radial_nr, b_v.angular_nr, b_v.z_dir, b_v.part_half)
            if key not in blockdict:
                blockdict[key] = []
            blockdict[key].append(b_v.block_nr)

        for v in blockdict.values():
            v.sort(key=coil_block_max_z)
            for z_idx, b_nr in enumerate(v):
                self._blocks[b_nr].z_idx = z_idx

    def _get_corner_order(self, layer_nr: int, nodes: np.ndarray) -> tuple[int, int, int, int, int]:
        symm = self._layers[layer_nr].symmetry
        z_inner = nodes[-1, 2]
        cable_phi = np.arctan2(nodes[0, 1], nodes[0, 0])
        imag = cable_phi / (np.pi / symm / 2) // 1 % 2 == 1

        quadrant = 2 if imag else 1
        if z_inner < 0:
            quadrant += 2

        if quadrant == 1:
            p1 = 0
            p2 = 1
            p3 = 2
            p4 = 3
        elif quadrant == 2:
            p1 = 1
            p2 = 0
            p3 = 3
            p4 = 2
        elif quadrant == 3:
            p1 = 3
            p2 = 2
            p3 = 1
            p4 = 0
        elif quadrant == 4:
            p1 = 2
            p2 = 3
            p3 = 0
            p4 = 1

        quadr = math.floor(cable_phi % (np.pi / symm / 2))

        return p1, p2, p3, p4, quadr

    #    def _calculate_endspacer_surface(self, coil: Coil3DGeometry)

    def _calculate_endspacer_surface(
        self,
        coil_id: int,
        inner: bool,
        add_ins_r: float | None = None,
        add_ins_phi: float | None = None,
        debug=False,
    ):
        """Calculate one surface of a coil extended to the mandrel radius.

        Args:
            coil_id: The coil ID to process
            inner: If True, this is the inner cable of the block (uses p2->p3 edge);
                   if False, this is the outer cable (uses p1->p4 edge)
            add_ins_r: Additional radial insulation
            add_ins_phi: Additional azimuthal insulation
            debug: Enable debug output

        Returns:
            tuple: (r_outer, r_inner) - Points extended to outer and inner radius respectively
        """
        coil = self._coils[coil_id]
        layer_nr = coil.layer_id
        if layer_nr not in self._layers:
            raise ValueError(
                f"Layer {layer_nr} has no inner and outer coil block radius set. Use set_coil_block_radii to set them"
            )
        inner_radius = self._layers[layer_nr].radii[0]
        outer_radius = self._layers[layer_nr].radii[1]

        # Get insulation
        ins_r, ins_phi = self._get_insulation(coil.block_id)
        if add_ins_r:
            ins_r += add_ins_r
        if add_ins_phi:
            ins_phi += add_ins_phi

        if coil.geometry.elements is None:
            raise ValueError("Cable geometry is lacking connectivity information")

        # Add insulation to the nodes
        p_insulated = add_insulation_thickness(coil.geometry.nodes, coil.geometry.elements, ins_r, ins_phi)

        # Get corner order
        p1, p2, p3, p4, quadr = self._get_corner_order(layer_nr, coil.geometry.nodes)
        self._layers[layer_nr].quadrants.add(quadr)

        # Select corners and direction based on whether this is inner or outer cable
        if inner:
            # Inner cable: use p2 corner and p2->p3 direction
            r_pre = p_insulated[p2::4, :]
            direction = normalize_vectors(coil.geometry.nodes[p3::4, :] - coil.geometry.nodes[p2::4, :])
        else:
            # Outer cable: use p1 corner and p1->p4 direction
            r_pre = p_insulated[p1::4, :]
            direction = normalize_vectors(coil.geometry.nodes[p4::4, :] - coil.geometry.nodes[p1::4, :])

        # Extend to outer radius
        r_outer, _ = get_intersection_line_cylinder(r_pre, direction, outer_radius, debug=debug)

        # Extend to inner radius (mandrel)
        r_inner, _ = get_intersection_line_cylinder(r_pre, direction, inner_radius, debug=debug)

        return r_outer, r_inner

    def _calculate_coil_block(
        self,
        block_number: int,
        extend=True,
        debug=False,
    ):
        coil_blocks = [idx for idx, coil in self._coils.items() if coil.block_id == block_number]
        inner_cable_number = min(coil_blocks)
        outer_cable_number = max(coil_blocks)

        # Calculate surfaces for inner cable (inner=True)
        if extend:
            r_3, r_0 = self._calculate_endspacer_surface(inner_cable_number, inner=True, debug=debug)
        else:
            inner_cable = self._coils[inner_cable_number]
            r_3 = inner_cable.geometry.nodes[::4, :]
            r_0 = inner_cable.geometry.nodes[1::4, :]

        # Calculate surfaces for outer cable (inner=False)
        if extend:
            r_2, r_1 = self._calculate_endspacer_surface(outer_cable_number, inner=False, debug=debug)
        else:
            outer_cable = self._coils[outer_cable_number]
            r_2 = outer_cable.geometry.nodes[3::4, :]
            r_1 = outer_cable.geometry.nodes[2::4, :]

        return r_3, r_2, r_0, r_1

    def get_coil_block_geom(
        self,
        block_number: int,
        block_dr: float = 0.0,
        overwrite_radii: dict[int, tuple[float, float]] | None = None,
    ) -> None:
        """Make a step file for a coil block.

        :param block_number: The block number to generate
        :param block_dr: Additional radial extension of the coil block
        :param overwrite_radii: Optional dictionary to overwrite the inner and outer radii for specific layers.

        """

        # Get layer_nr from one of the coils in this block
        coil_in_block = next(coil for coil in self._coils.values() if coil.block_id == block_number)
        layer_nr = coil_in_block.layer_id
        if overwrite_radii:
            if layer_nr not in overwrite_radii:
                raise ValueError(f"Layer {layer_nr} not found in overwrite_radii")
            r_inner, r_outer = overwrite_radii[layer_nr]
        else:
            r_inner, r_outer = self._layers[layer_nr].radii
            r_inner -= block_dr
            r_outer += block_dr

        self._cad.magnet_order = self._layers[layer_nr].symmetry

        is_cos_theta = self._blocks[block_number].block_type in self._supported_block_types
        r_ft, r_fb, r_0, r_1 = self._calculate_coil_block(block_number, extend=is_cos_theta)
        if is_cos_theta:
            self._cad.make_block(block_number, f"coilblock_{block_number:03d}", r_fb, r_ft, r_1, r_0)
        else:
            self._cad.make_block_simple(block_number, f"coilblock_{block_number:03d}", r_fb, r_ft, r_1, r_0)

    def get_all_insulation_geoms(self) -> None:
        """
        Generate the geometry of all insulations.


        :return: None
        """
        self.builder().add_conductors(*self._coils.keys()).with_insulations().generate()

    def get_all_coil_geoms(self, add_insulation: bool = False) -> None:
        """
        Generate the geometry of all coils.

        :param add_insulation: Whether to add insulation to the coils
        :type add_insulation: bool

        :return: None
        """
        self.builder().add_conductors(*self._coils.keys()).with_coils(add_insulation=add_insulation).generate()

    def get_all_coil_block_geoms(
        self,
        block_dr: float = 0.0,
        overwrite_radii: dict[int, tuple[float, float]] | None = None,
    ) -> None:
        """
        Generate the geometry of all coil blocks.

        :param block_dr: Additional radial extension of the coil block
        :param overwrite_radii: Optional dictionary to overwrite the inner and outer radii for specific layers.

        :return: None
        """
        # Extract coil blocks
        coil_blocks = {coil.block_id for coil in self._coils.values() if coil.block_id}
        self.builder().add_blocks(*coil_blocks, also_conductors=False).with_blocks(
            coilblock_dr=block_dr, overwrite_radii=overwrite_radii
        ).generate()

    def get_endspacer_geom_from_coils(
        self,
        endspacer_nr: int,
        name: str,
        coil_inner_id: int | None,
        coil_outer_id: int | None,
        z_max: float | None = None,
        min_width: float | None = None,
    ):
        if coil_inner_id is None and coil_outer_id is None:
            raise ValueError("At least one of coil_inner_id or coil_outer_id must be provided")
        if (
            coil_inner_id is not None
            and coil_outer_id is not None
            and self._coils[coil_inner_id].layer_id != self._coils[coil_outer_id].layer_id
        ):
            raise ValueError("coil_inner and coil_outer must belong to the same layer")
        if coil_inner_id is not None:
            front_bot, front_top = self._calculate_endspacer_surface(
                coil_inner_id, inner=True, add_ins_r=self._add_ins_r, add_ins_phi=self._add_ins_phi
            )
            layer_nr = self._coils[coil_inner_id].layer_id
        else:
            front_bot, front_top = None, None
        if coil_outer_id is not None:
            back_bot, back_top = self._calculate_endspacer_surface(
                coil_outer_id, inner=False, add_ins_r=self._add_ins_r, add_ins_phi=self._add_ins_phi
            )
            layer_nr = self._coils[coil_outer_id].layer_id
        else:
            back_bot, back_top = None, None
        self._cad.magnet_order = self._layers[layer_nr].symmetry
        self._cad.make_spacer(endspacer_nr, name, back_bot, back_top, front_bot, front_top, z_max, min_width=min_width)

    def get_endspacer_geom(
        self,
        radial_nr: int,
        angular_nr: int,
        z_dir: int,
        halfid: int,
        idx: int,
        z_max: float | None = None,
        min_width: float | None = None,
        force_inner_post: bool = False,
        force_headspacer: bool = False,
    ):
        """Create spacer geometry.
        :param radial_nr: The radial number of the layer to generate spacers from (inner to outer)
        :param angular_nr: The angular number of the layer to generate spacers from (math. positive direction)
                            For dipole, this is 1 or 2, for quadrupole 1, 2, 3, or 4, etc.
        :param z_dir: The z direction of the layer to generate spacers from (-1 for Z<0, 1 for Z>0)
        :param halfid: The half of the coil block (0 for first half, 1 for second half)
        :param idx: The index of the endspacer with increasing z (0 for inner_post, 1 for second block, etc.)
        :param z_max: Optional: Maximum z extension of endspacer (ignore actual length of coils)
        :param min_width: Minimum width of endspacer
        :return: None
        """
        blocks = {}
        for block_id, block in self._blocks.items():
            if (
                block.radial_nr == radial_nr
                and block.angular_nr == angular_nr
                and block.z_dir == z_dir
                and block.part_half == halfid
                and block.block_type in self._supported_block_types
            ):
                blocks[block.z_idx] = block_id

        block_inner = blocks.get(idx - 1)
        block_outer = blocks.get(idx)

        if force_inner_post:
            block_inner = None
        if force_headspacer:
            block_outer = None

        if block_inner is None and block_outer is None:
            raise ValueError("At least one of block_inner or block_outer must be present")

        coil_inner = (
            min([idx for idx, coil in self._coils.items() if coil.block_id == block_inner]) if block_inner else None
        )
        coil_outer = (
            max([idx for idx, coil in self._coils.items() if coil.block_id == block_outer]) if block_outer else None
        )

        model_name = (
            f"spacers_rp_{radial_nr}_ap_{angular_nr}_z{'pos' if z_dir > 0 else 'neg'}_h_{halfid}_id{idx + 1:02d}_"
        )
        if block_inner is None:
            model_name += "inner_post"
        elif block_outer is None:
            model_name += "headspacer"
        else:
            model_name += "spacer"

        return self.get_endspacer_geom_from_coils(
            idx,
            model_name,
            coil_inner,
            coil_outer,
            z_max,
            min_width,
        )

    def get_all_endspacer_geoms(
        self,
        add_z: float = 20.0,
        zmax: float | None = None,
        min_width: float | None = None,
    ) -> None:
        """Generate the geometry of all spacers.
        :param add_z: Additional z extension of endspacer
        :param zmax: Optional: Maximum z extension of endspacer (ignore add_z and actual length of coils)
        :param starting_angle: Optional: Offset angle at which cylinder of endspacer starts (in radians)
        :return: None
        """
        self.builder().add_all().with_endspacers(add_z=add_z, zmax=zmax, min_width=min_width).generate()
