# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import itertools
import logging
import math
import pathlib
from collections.abc import Iterable
from dataclasses import dataclass

import cadquery as cq
import cadquery.func
import numpy as np
import numpy.typing as npt
import scipy
from scipy.interpolate import BSpline
from scipy.optimize import brentq

from roxieinterfaces.geom.math_tools import find_nr_straight


def create_bspline(
    points: npt.NDArray[np.float64], smoothing_factor: float, bspline_degree: int
) -> tuple[scipy.interpolate.BSpline, np.ndarray]:
    weights = np.ones(points.shape[0])
    weights[0] = 1000
    weights[-1] = 1000
    bspline, u = scipy.interpolate.make_splprep(points.T, w=weights, s=smoothing_factor, k=bspline_degree)
    return bspline, u


def get_coilnr_imag(symm: int, nodes: np.ndarray) -> tuple[int, bool]:
    cable_phi = np.arctan2(nodes[0, 1], nodes[0, 0])
    if cable_phi < 0:
        cable_phi += 2 * np.pi
    coil_nr = int(cable_phi // (np.pi / symm))
    imag = cable_phi // (np.pi / symm / 2) % 2 == 1

    return coil_nr, imag


def find_u_for_z(spline: BSpline, z_target: float, u_min: float, u_max: float) -> float | None:
    """Find parameter u where spline has z coordinate = z_target.

    Args:
        spline: BSpline object
        z_target: Target z coordinate
        u_min, u_max: Parameter bounds to search within

    Returns:
        Parameter u corresponding to z_target
    """

    def z_residual(u):
        point = spline(u)  # Evaluate spline at u
        return point[2] - z_target  # z is the third component

    try:
        u_solution = brentq(z_residual, u_min, u_max, disp=True)
        return u_solution
    except ValueError:
        return None
    except RuntimeError:
        return None


@dataclass
class ModelProperties:
    """Dataclass for CAD model properties"""

    color: cq.Color


class CadProvider:
    """Base class for CAD providers
    (shared functions between different CAD backends)
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("CadProvider")
        self.model_name: str | None = None
        self.model_color: list[int] | None = None
        self.output_step_folder: pathlib.Path | None = None
        self.output_vtk_folder: pathlib.Path | None = None
        self.magnet_order: int = 0
        self.bspline_degree: int = 3
        self.smoothing_factor: float = 0.001

        self.model_properties = {
            "cables": ModelProperties(color=cq.Color(0xD5 / 0xFF, 0x75 / 0xFF, 0x0A / 0xFF)),
            "insulated_cables": ModelProperties(color=cq.Color(0x7E / 0xFF, 0x3A / 0xFF, 0x06 / 0xFF)),
            "blocks": ModelProperties(color=cq.Color(0x9E / 0xFF, 0x18 / 0xFF, 0x02 / 0xFF)),
            "insulations": ModelProperties(color=cq.Color(0x19 / 0xFF, 0x99 / 0xFF, 0x87 / 0xFF)),
            "spacers": ModelProperties(color=cq.Color(0x0C / 0xFF, 0x4F / 0xFF, 0xAB / 0xFF)),
        }
        self.assemblies: dict[str, cq.Assembly] = {}

    def get_assembly(self, top_name: str = "Model", groups: Iterable[str] | None = None) -> cq.Assembly:
        top_assembly = cq.Assembly(name=top_name)
        if groups is None:
            groups = self.assemblies.keys()
        for group in groups:
            if group in self.assemblies:
                top_assembly.add(self.assemblies[group], name=group)
        return top_assembly

    def clear_assemblies(self) -> None:
        self.assemblies.clear()

    def _add_to_assembly(
        self,
        group: str,
        id: int,
        name: str,
        solid: cq.Solid,
    ) -> None:
        if group not in self.assemblies:
            self.assemblies[group] = cq.Assembly(name=group)
        self.assemblies[group].add(solid, name=name, color=self.model_properties[group].color)

    def make_cable(
        self,
        id: int,
        name: str,
        insulated: bool,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
    ):
        solid = self._create_block(points_front_bottom, points_front_top, points_back_bottom, points_back_top)
        group = "insulated_cables" if insulated else "cables"
        self._add_to_assembly(group, id, name, solid)

    def make_block(
        self,
        id: int,
        name: str,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
    ):
        solid = self._create_block_rounded(points_front_bottom, points_front_top, points_back_bottom, points_back_top)
        self._add_to_assembly("blocks", id, name, solid)

    def make_block_simple(
        self,
        id,
        name,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
    ):
        solid = self._create_block(points_front_bottom, points_front_top, points_back_bottom, points_back_top)
        self._add_to_assembly("blocks", id, name, solid)

    def make_insulation(
        self,
        id: int,
        name: str,
        outer_points_front_bottom: npt.NDArray[np.float64],
        outer_points_front_top: npt.NDArray[np.float64],
        outer_points_back_bottom: npt.NDArray[np.float64],
        outer_points_back_top: npt.NDArray[np.float64],
        inner_points_front_bottom: npt.NDArray[np.float64],
        inner_points_front_top: npt.NDArray[np.float64],
        inner_points_back_bottom: npt.NDArray[np.float64],
        inner_points_back_top: npt.NDArray[np.float64],
    ):
        solid = self._create_hollow_block(
            outer_points_front_bottom,
            outer_points_front_top,
            outer_points_back_bottom,
            outer_points_back_top,
            inner_points_front_bottom,
            inner_points_front_top,
            inner_points_back_bottom,
            inner_points_back_top,
        )

        self._add_to_assembly("insulations", id, name, solid)

    def make_spacer(
        self,
        id: int,
        name: str,
        points_front_bottom: npt.NDArray[np.float64] | None,
        points_front_top: npt.NDArray[np.float64] | None,
        points_back_bottom: npt.NDArray[np.float64] | None,
        points_back_top: npt.NDArray[np.float64] | None,
        z_max: float | None = None,
        min_width: float | None = None,
    ) -> None:
        solid = None
        # Check that pairs of points are corret (either both none or both defined)
        if (points_front_bottom is None and points_front_top is not None) or (
            points_front_bottom is not None and points_front_top is None
        ):
            raise Exception("points_front_bottom and points_front_top must both be defined or both be None")
        if (points_back_bottom is None and points_back_top is not None) or (
            points_back_bottom is not None and points_back_top is None
        ):
            raise Exception("points_back_bottom and points_back_top must both be defined or both be None")
        if points_front_bottom is None and points_back_bottom is None:
            raise Exception("At least one set of points must be provided for spacer generation")

        if points_front_bottom is None:
            if z_max is None:
                raise Exception("z_max must be provided for headspacer generation")
            assert points_back_bottom is not None and points_back_top is not None
            z_max = math.copysign(z_max, points_back_bottom[-1, 2])
            if min_width:
                solid = self._create_headspacer_cut(points_back_bottom, points_back_top, z_max, min_width=min_width)
            else:
                solid = self._create_headspacer(points_back_bottom, points_back_top, z_max)
        elif points_back_bottom is None:
            assert points_front_top is not None and points_front_bottom is not None
            solid = self._create_inner_post(points_front_bottom, points_front_top)
        elif points_front_bottom is not None and points_back_bottom is not None:
            assert points_front_top is not None and points_back_top is not None
            if min_width:
                lower_width_e = abs(points_front_top[-1, 2] - points_back_top[-1, 2])
                upper_width_e = abs(points_front_bottom[-1, 2] - points_back_bottom[-1, 2])
                if lower_width_e < min_width or upper_width_e < min_width:
                    solid = self._create_wedge_cut(
                        points_back_top, points_front_top, points_back_bottom, points_front_bottom, min_width=min_width
                    )
                else:
                    solid = self._create_block_rounded_cut(
                        points_back_top, points_front_top, points_back_bottom, points_front_bottom, min_width=min_width
                    )
            else:
                solid = self._create_block_rounded(
                    points_back_top, points_front_top, points_back_bottom, points_front_bottom
                )
        else:
            nones = [x is None for x in [points_front_bottom, points_front_top, points_back_bottom, points_back_top]]
            raise Exception(f"Incorrect assignment of points: some are None where not expected: {nones}")
        self._add_to_assembly("spacers", id, name, solid)

    def _find_u_at_z_with_width_constraint(
        self,
        points_list: list[npt.NDArray[np.float64]],
        width_calculator,
        min_width: float | None = None,
        z_cut: float | None = None,
    ) -> tuple[list[float | None], float]:
        """Helper function: Find u parameters at z where width constraint is met.

        Args:
            points_list: List of point arrays to create BSplines from
            width_calculator: Function(targets) -> width that calculates width from evaluated points
            min_width: Target minimum width
            z_cut: Specific z coordinate to cut at

        Returns:
            List of u parameters or None if no cut needed
        """
        n_straight = find_nr_straight(points_list)
        input_bsplines: list[tuple[scipy.interpolate.BSpline | None, np.ndarray | None]] = []
        input_straights: list[npt.NDArray[np.float64]] = []
        for input_p in points_list:
            input_straights.append(input_p[n_straight])
            if len(input_p) - n_straight > 2:
                bspline, u = create_bspline(input_p[n_straight:], self.smoothing_factor, self.bspline_degree)
                input_bsplines.append((bspline, u))
            else:
                input_bsplines.append((None, None))

        def calculate_min_width_diff(z_target) -> float:
            targets = []
            for ps, (bsp, _) in zip(input_straights, input_bsplines, strict=True):
                if abs(ps[2]) >= abs(z_target):
                    targets.append(ps)
                elif bsp is not None:
                    u_res = find_u_for_z(bsp, z_target, u[0], u[-1])
                    if u_res is None:
                        targets.append(ps)
                    else:
                        targets.append(bsp(u_res))

            return width_calculator(targets) - min_width

        z_lim = min(
            [spl(u[-1])[2] if spl is not None and u is not None else math.inf for spl, u in input_bsplines], key=abs
        )
        z_min = min(
            [spl(u[0])[2] if spl is not None and u is not None else -math.inf for spl, u in input_bsplines], key=abs
        )

        z_target = z_cut or scipy.optimize.ridder(calculate_min_width_diff, z_min, z_lim)

        u_list: list[float | None] = []
        for straight_p, (spl, u1) in zip(input_straights, input_bsplines, strict=True):
            if abs(straight_p[2]) >= abs(z_target):
                u_list.append(None)
            elif spl is not None and u1 is not None:
                u_res = find_u_for_z(spl, z_target, u1[0], u1[-1])
                if u_res is None:
                    u_list.append(None)
                else:
                    u_list.append(u_res)

        return u_list, z_target

    def _calculate_u_at_min_width_fixed(
        self,
        points_front: npt.NDArray[np.float64],
        points_back: npt.NDArray[np.float64],
        p_front: npt.NDArray[np.float64],
        p_back: npt.NDArray[np.float64],
        min_width: float | None = None,
        z_cut: float | None = None,
    ) -> tuple[list[float | None] | None, float | None]:
        """Calculate u parameters where width reaches minimum (with fixed points).

        Args:
            points_front: Points for front spline
            points_back: Points for back spline
            p_front: Fixed point (x,y,z) for inner width calculation (z ignored)
            p_back: Fixed point (x,y,z) for outer width calculation (z ignored)
            min_width: Target minimum width
            z_cut: Specific z coordinate to cut at

        Returns:
            List of 2 u parameters [u_front, u_back] or None if no cut needed
        """
        if min_width is not None and z_cut is not None:
            raise Exception("Cannot specify both min_width and z_cut")
        if min_width is None and z_cut is None:
            return None, None

        if min_width is not None:
            front_width = np.linalg.norm(points_front[0, :2] - p_front[:2])
            back_width = np.linalg.norm(points_back[0, :2] - p_back[:2])
            if min(front_width, back_width) >= min_width:
                return None, None

        def width_calc(targets):
            front_width = math.sqrt((targets[0][0] - p_front[0]) ** 2 + (targets[0][1] - p_front[1]) ** 2)
            back_width = math.sqrt((targets[1][0] - p_back[0]) ** 2 + (targets[1][1] - p_back[1]) ** 2)
            return min(front_width, back_width)

        return self._find_u_at_z_with_width_constraint([points_front, points_back], width_calc, min_width, z_cut)

    def _calculate_u_at_min_width(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
        min_width: float | None = None,
        z_cut: float | None = None,
    ) -> tuple[list[float | None] | None, float | None]:
        """Calculate u parameters where width reaches minimum width (four splines).

        Args:
            points_front_bottom: Front bottom spline points
            points_front_top: Front top spline points
            points_back_bottom: Back bottom spline points
            points_back_top: Back top spline points
            min_width: Target minimum width
            z_cut: Specific z coordinate to cut at

        Returns:
            List of 4 u parameters [back_top, front_top, back_bottom, front_bottom] or None
        """
        if min_width is not None and z_cut is not None:
            raise Exception("Cannot specify both min_width and z_cut")
        if min_width is None and z_cut is None:
            return None, None

        if min_width is not None:
            lower_width = np.linalg.norm(points_front_top[0, :] - points_front_bottom[0, :])
            upper_width = np.linalg.norm(points_back_top[0, :] - points_back_bottom[0, :])
            if min(upper_width, lower_width) >= min_width:
                return None, None

        def width_calc(targets):
            # targets order: [back_top, front_top, back_bottom, front_bottom]
            lower_width = math.sqrt((targets[1][0] - targets[0][0]) ** 2 + (targets[1][1] - targets[0][1]) ** 2)
            upper_width = math.sqrt((targets[3][0] - targets[2][0]) ** 2 + (targets[3][1] - targets[2][1]) ** 2)

            return min(upper_width, lower_width)

        input_combined = [points_front_bottom, points_front_top, points_back_bottom, points_back_top]
        return self._find_u_at_z_with_width_constraint(input_combined, width_calc, min_width, z_cut)

    def _calculate_u_at_max_width(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
        max_width: float | None = None,
        z_cut: float | None = None,
    ) -> tuple[list[float | None] | None, float | None]:
        """Calculate u parameters where width reaches maximum width (four splines).

        Args:
            points_front_bottom: Front bottom spline points
            points_front_top: Front top spline points
            points_back_bottom: Back bottom spline points
            points_back_top: Back top spline points
            max_width: Target maximum width
            z_cut: Specific z coordinate to cut at

        Returns:
            List of 4 u parameters [back_top, front_top, back_bottom, front_bottom] or None
        """
        if max_width is not None and z_cut is not None:
            raise Exception("Cannot specify both min_width and z_cut")
        if max_width is None and z_cut is None:
            raise ValueError("Either min width or z_cut must be set")

        if max_width is not None:
            lower_width = np.linalg.norm(points_front_top[0, :] - points_front_bottom[0, :])
            upper_width = np.linalg.norm(points_back_top[0, :] - points_back_bottom[0, :])
            if min(upper_width, lower_width) <= max_width:
                return None, None

        def width_calc(targets):
            # targets order: [back_top, front_top, back_bottom, front_bottom]
            lower_width = math.sqrt((targets[1][0] - targets[0][0]) ** 2 + (targets[1][1] - targets[0][1]) ** 2)
            upper_width = math.sqrt((targets[3][0] - targets[2][0]) ** 2 + (targets[3][1] - targets[2][1]) ** 2)
            return min(upper_width, lower_width)

        input_combined = [points_front_bottom, points_front_top, points_back_bottom, points_back_top]
        return self._find_u_at_z_with_width_constraint(input_combined, width_calc, max_width, z_cut)

    def _calculate_bsplines_n_straight(
        self, *points: npt.NDArray[np.float64]
    ) -> tuple[list[tuple[scipy.interpolate.BSpline | None, np.ndarray | None]], int]:
        n_straight = find_nr_straight(points)
        input_bsplines: list[tuple[scipy.interpolate.BSpline | None, np.ndarray | None]] = []
        for i in range(len(points)):
            input_p = points[i]
            if len(input_p) - n_straight > 2:
                bspline, u = create_bspline(input_p[n_straight:], self.smoothing_factor, self.bspline_degree)
                input_bsplines.append((bspline, u))
            else:
                input_bsplines.append((None, None))

        return input_bsplines, n_straight

    def _interpolate_points(
        self,
        n_straight: int,
        input_bsplines: list[tuple[scipy.interpolate.BSpline | None, np.ndarray | None]],
        *points: npt.NDArray[np.float64],
    ) -> tuple[list[list[cq.Vector]], list[list[cq.Vector]]]:
        coilnr, imag = get_coilnr_imag(self.magnet_order, points[0])

        input_vectors = [[cq.Vector(*row) for row in array] for array in points]

        input_tangents = []
        for i, iv in enumerate(input_vectors):
            tangents = []
            bspline, u = input_bsplines[i]

            if bspline is not None and u is not None:
                deriv = bspline(u, nu=1).T

                tangents.extend([cq.Vector(*d) for d in deriv])

                # Last tangent extension
                mag_angle = (coilnr + 0.5) * (np.pi / self.magnet_order)
                coil_angle = mag_angle - np.pi / 2 if imag else mag_angle + np.pi / 2
                tx = math.cos(coil_angle)
                ty = math.sin(coil_angle)
                tangents[0] = iv[1] - iv[0]  # Straight section extension
                tangents[-1] = cq.Vector(tx, ty, 0)  # YZ plain extension

            input_tangents.append(tangents)

        return input_vectors, input_tangents

    def _calculate_cutting_points(
        self,
        input_bsplines: list[tuple[scipy.interpolate.BSpline | None, np.ndarray | None]],
        u_list: list[float | None],
        z_cut: float,
        points_straight_section: list[cq.Vector],
    ) -> list[tuple[int | None, cq.Vector, cq.Vector]]:
        cut_indices: list[tuple[int | None, cq.Vector, cq.Vector]] = []
        for (bspline, u), u_cut, p_s in zip(input_bsplines, u_list, points_straight_section, strict=True):
            if u_cut is None or bspline is None or u is None:
                p_c = cq.Vector(p_s)
                p_c.z = z_cut
                t_c = p_s - p_c
                cut_indices.append((None, p_c, t_c))
            else:
                idx = int(np.searchsorted(u, u_cut))
                cut_indices.append((idx, cq.Vector(*bspline(u_cut)), cq.Vector(*bspline(u_cut, nu=1))))

        return cut_indices

    def _create_block(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
    ) -> cq.Solid:
        """Create a block solid given the corner points.
        4 sets of points defining the corners of the block.

                front_top ┌──────────┐ back_top
            r ───────────►│          │
                front_bot └──────────┘ back_bot


        """
        points = [
            points_front_bottom,
            points_front_top,
            points_back_top,
            points_back_bottom,
        ]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(n_straight, input_bsplines, *points)

        input_edges = []
        input_wires = []
        input_faces = []

        for i, iv in enumerate(input_vectors):
            tangents = input_tangents[i]
            edges = []

            if len(iv) - n_straight <= 2:
                # Only straight section
                if len(iv) == n_straight:
                    edges.append(cq.Edge.makeLine(iv[0], iv[n_straight - 1]))
                else:
                    edges.append(cq.Edge.makeLine(iv[0], iv[n_straight]))
                    if len(iv) < n_straight:
                        edges.append(cq.Edge.makeLine(iv[n_straight], iv[-1]))
            else:
                # Curved section
                edges.append(cq.Edge.makeLine(iv[0], iv[n_straight]))
                for edge_i in range(n_straight + 1, len(iv)):
                    t_i = edge_i - n_straight
                    pp = [iv[edge_i - 1], iv[edge_i]]
                    tangs = (tangents[t_i - 1], tangents[t_i])
                    edges.append(cq.Edge.makeSpline(pp, tangs, scale=True))

            input_edges.append(edges)

        for ie in input_edges:
            wire = cq.Wire.assembleEdges(ie)
            input_wires.append(wire)

        # Side faces
        for i in range(len(input_wires)):
            i2 = (i + 1) % len(input_wires)
            f = cq.Face.makeRuledSurface(input_wires[i], input_wires[i2])
            input_faces.append(f)

        # Top / bottom
        wstart = cq.Wire.makePolygon([iv[0] for iv in input_vectors], close=True)
        wend = cq.Wire.makePolygon([iv[-1] for iv in input_vectors], close=True)
        fstart = cq.Face.makeFromWires(wstart)
        fend = cq.Face.makeFromWires(wend)

        input_wires.extend([wstart, wend])
        input_faces.extend([fstart, fend])

        shell = cq.Shell.makeShell(input_faces)
        solid = cq.Solid.makeSolid(shell)

        return solid

    def _create_headspacer_cut(
        self,
        points_bottom: npt.NDArray[np.float64],
        points_top: npt.NDArray[np.float64],
        z_end: float,
        min_width: float | None = None,
        z_cut: float | None = None,
    ):
        if min_width or z_cut:
            u_list, z_cut = self._calculate_u_at_min_width_fixed(
                points_bottom, points_top, points_bottom[0, :], points_top[0, :], min_width=min_width
            )
        else:
            u_list = None
        if u_list is None or z_cut is None:
            return self._create_headspacer(points_bottom, points_top, z_end)

        points = [points_bottom, points_top]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(n_straight, input_bsplines, *points)
        cut_indices = self._calculate_cutting_points(
            input_bsplines, u_list, z_cut, [cq.Vector(*p[n_straight]) for p in points]
        )

        surfaces = []
        cut_points = {}
        side_edges: dict[int, list[cq.Edge]] = {i: [] for i in range(4)}

        # Straight side, from cut to z_end
        psc_l = cq.Vector(input_vectors[0][0].x, input_vectors[0][0].y, cut_indices[0][1].z)
        psc_u = cq.Vector(input_vectors[1][0].x, input_vectors[1][0].y, cut_indices[0][1].z)
        pse_l = cq.Vector(input_vectors[0][0].x, input_vectors[0][0].y, z_end)
        pse_u = cq.Vector(input_vectors[1][0].x, input_vectors[1][0].y, z_end)

        # End points at symmetry plane
        pe_l = cq.Vector(input_vectors[0][-1].x, input_vectors[0][-1].y, z_end)
        pe_u = cq.Vector(input_vectors[1][-1].x, input_vectors[1][-1].y, z_end)

        side_edges[2].append(cq.Edge.makeLine(psc_l, pse_l))
        side_edges[3].append(cq.Edge.makeLine(psc_u, pse_u))

        # Perform cutting and restitching magic
        for i1, i2 in [(0, 1)]:
            # find the "lower index for each pair"
            ci1 = cut_indices[i1][0]
            ci2 = cut_indices[i2][0]

            if ci1 is None or ci2 is None:
                raise ValueError("Missing cutting point for conductor part, cannot converge to geometry")

            if ci1 < ci2:
                i_lower = i1
                i_upper = i2
            else:
                i_lower = i2
                i_upper = i1

            u_l = cut_indices[i_lower]
            u_u = cut_indices[i_upper]
            z_cut = u_l[1].z

            assert u_l[0] is not None
            assert u_u[0] is not None

            P_on_z, tangs = self._vertical_cut(input_vectors, cut_indices, i_lower, i_upper)

            range_cross = list(range(u_l[0], u_u[0] + 1))
            side_surfaces = []
            front_edges = []

            for i_pz, i in enumerate(range_cross):
                t_i = i - n_straight
                points_upper = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                tangs_upper = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                points_lower = (input_vectors[i_lower][i], input_vectors[i_lower][i + 1])
                tangs_lower = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])

                if i_pz == 0:  # First triangle
                    edges = [
                        cq.Edge.makeSpline(
                            [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                        ),
                        cq.Edge.makeLine(P_on_z[i_pz + 1], points_lower[1]),
                        cq.Edge.makeSpline([points_lower[1], P_on_z[i_pz]], (-tangs_lower[1], -u_l[2]), scale=True),
                    ]
                    side_edges[i_lower].append(edges[-1])
                    front_edges.append(edges[0])
                    cut_points[i_lower] = P_on_z[i_pz]
                elif i_pz == len(range_cross) - 1:  # Last Segment
                    edges = [
                        cq.Edge.makeSpline(
                            [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                        ),
                        cq.Edge.makeSpline([P_on_z[i_pz + 1], points_upper[1]], (u_u[2], tangs_upper[1]), scale=True),
                        cq.Edge.makeLine(points_upper[1], points_lower[1]),
                        cq.Edge.makeSpline(
                            [points_lower[1], points_lower[0]], (-tangs_lower[1], -tangs_lower[0]), scale=True
                        ),
                        cq.Edge.makeLine(points_lower[0], P_on_z[i_pz]),
                    ]
                    side_edges[i_upper].append(edges[1])
                    side_edges[i_lower].append(edges[3])
                    front_edges.append(edges[0])
                    cut_points[i_upper] = P_on_z[i_pz + 1]
                else:  # Middle segments
                    edges = [
                        cq.Edge.makeSpline(
                            [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                        ),
                        cq.Edge.makeLine(P_on_z[i_pz + 1], points_lower[1]),
                        cq.Edge.makeSpline(
                            [points_lower[1], points_lower[0]], (-tangs_lower[1], -tangs_lower[0]), scale=True
                        ),
                        cq.Edge.makeLine(points_lower[0], P_on_z[i_pz]),
                    ]
                    front_edges.append(edges[0])
                    side_edges[i_lower].append(edges[2])

                surf = cq.func.fill(cq.Wire.assembleEdges(edges))

                side_surfaces.append(surf)

            for i in range(u_u[0] + 1, len(input_vectors[i_upper]) - 1):
                t_i = i - n_straight
                cq_points = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                tangs = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                edge_upper = cq.Edge.makeSpline(
                    cq_points,
                    tangs,
                )
                cq_points = [input_vectors[i_lower][i], input_vectors[i_lower][i + 1]]
                tangs = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])
                edge_lower = cq.Edge.makeSpline(
                    cq_points,
                    tangs,
                )
                side_edges[i_upper].append(edge_upper)
                side_edges[i_lower].append(edge_lower)
                surf = cq.Face.makeRuledSurface(edge_lower, edge_upper)
                side_surfaces.append(surf)

            surfaces.extend(side_surfaces)

        # Surface facing symmetry plane
        symm_edges = [
            cq.Edge.makeLine(input_vectors[0][-1], input_vectors[1][-1]),
            cq.Edge.makeLine(input_vectors[1][-1], pe_u),
            cq.Edge.makeLine(pe_u, pe_l),
            cq.Edge.makeLine(pe_l, input_vectors[0][-1]),
        ]

        symm_wires = cq.Wire.assembleEdges(symm_edges)
        symm_face = cq.Face.makeFromWires(symm_wires)
        surfaces.append(symm_face)

        # Front Surface
        r_inner = (cut_points[0].x ** 2 + cut_points[0].y ** 2) ** 0.5
        r_outer = (cut_points[1].x ** 2 + cut_points[1].y ** 2) ** 0.5

        phis_s = np.array([math.atan2(ci.y, ci.x) for _, ci, _ in cut_indices])
        phis_e = np.array([math.atan2(v.y, v.x) for v in [psc_l, psc_u]])
        phis = (phis_s + phis_e) / 2
        mid = [
            cq.Vector(
                r * math.cos(phi),
                r * math.sin(phi),
                cut_points[0].z,
            )
            for r, phi in zip([r_inner, r_outer], phis, strict=False)
        ]
        edges_front = [
            *front_edges,
            cq.Edge.makeThreePointArc(cut_indices[0][1], mid[0], psc_l),
            cq.Edge.makeLine(psc_l, psc_u),
            cq.Edge.makeThreePointArc(psc_u, mid[1], cut_indices[1][1]),
        ]

        front_surface = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges_front))
        surfaces.append(front_surface)

        phis_s = np.array([math.atan2(v.y, v.x) for v in [pe_l, pe_u]])
        phis_e = np.array([math.atan2(v.y, v.x) for v in [pse_l, pse_u]])
        phis = (phis_s + phis_e) / 2
        mid = [
            cq.Vector(
                r * math.cos(phi),
                r * math.sin(phi),
                z_end,
            )
            for r, phi in zip([r_inner, r_outer], phis, strict=False)
        ]
        edges_back = [
            cq.Edge.makeThreePointArc(pe_l, mid[0], pse_l),
            cq.Edge.makeLine(pse_l, pse_u),
            cq.Edge.makeThreePointArc(pse_u, mid[1], pe_u),
            cq.Edge.makeLine(pe_u, pe_l),
        ]
        back_surface = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges_back))
        surfaces.append(back_surface)

        # Edges to the main plane
        edges_main = [cq.Edge.makeLine(psc_l, psc_u), *side_edges[3], cq.Edge.makeLine(pse_u, pse_l), *side_edges[2]]
        mainplane_surface = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges_main))
        surfaces.append(mainplane_surface)

        edges_top = [*side_edges[0], symm_edges[3], edges_back[0], *side_edges[2], edges_front[-3]]
        edges_bot = [*side_edges[1], symm_edges[1], edges_back[2], *side_edges[3], edges_front[-1]]

        surfaces.append(cq.func.fill(cq.func.wire(edges_top)))
        surfaces.append(cq.func.fill(cq.func.wire(edges_bot)))

        shell = cq.Shell.makeShell(surfaces)  # type: ignore
        solid = cq.Solid.makeSolid(shell)

        return solid

    def _create_headspacer(
        self,
        points_bottom: npt.NDArray[np.float64],
        points_top: npt.NDArray[np.float64],
        z_end: float,
    ) -> cq.Solid:
        points = [points_bottom, points_top]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(n_straight, input_bsplines, *points)

        vec_b = [cq.Vector(input_vectors[0][j].x, input_vectors[0][j].y, z_end) for j in [n_straight, -1]]
        vec_t = [cq.Vector(input_vectors[1][j].x, input_vectors[1][j].y, z_end) for j in [n_straight, -1]]

        r_inner = (vec_b[0].x ** 2 + vec_b[0].y ** 2) ** 0.5
        r_outer = (vec_t[0].x ** 2 + vec_t[0].y ** 2) ** 0.5
        phis_s = np.array([math.atan2(v[n_straight].y, v[n_straight].x) for v in input_vectors])
        phis_e = np.array([math.atan2(v[-1].y, v[-1].x) for v in input_vectors])
        phis = (phis_s + phis_e) / 2
        mid = [
            cq.Vector(
                r * math.cos(phis[0]),
                r * math.sin(phis[0]),
                z_end,
            )
            for r, phi in zip([r_inner, r_outer], phis, strict=False)
        ]

        input_edges = []
        input_wires = []
        input_faces = []

        for i, iv in enumerate(input_vectors):
            tangents = input_tangents[i]
            edges = []

            for edge_i in range(n_straight + 1, len(iv)):
                t_i = edge_i - n_straight
                cq_points = [iv[edge_i - 1], iv[edge_i]]
                tangs = (tangents[t_i - 1], tangents[t_i])
                edges.append(cq.Edge.makeSpline(cq_points, tangs, scale=True))

            input_edges.append(edges)

        input_edges.append(
            [
                cq.Edge.makeLine(vec_b[1], input_vectors[0][-1]),
                cq.Edge.makeLine(input_vectors[0][-1], input_vectors[1][-1]),
                cq.Edge.makeLine(input_vectors[1][-1], vec_t[1]),
                cq.Edge.makeLine(vec_t[1], vec_b[1]),
            ]
        )
        input_edges.append(
            [
                cq.Edge.makeThreePointArc(vec_b[0], mid[0], vec_b[1]),
                cq.Edge.makeLine(vec_b[1], vec_t[1]),
                cq.Edge.makeThreePointArc(vec_t[0], mid[1], vec_t[1]),
                cq.Edge.makeLine(vec_t[0], vec_b[0]),
            ]
        )
        input_edges.append(
            [
                cq.Edge.makeLine(vec_b[0], input_vectors[0][n_straight]),
                cq.Edge.makeLine(input_vectors[0][n_straight], input_vectors[1][n_straight]),
                cq.Edge.makeLine(input_vectors[1][n_straight], vec_t[0]),
                cq.Edge.makeLine(vec_t[0], vec_b[0]),
            ]
        )

        for ie in input_edges:
            wire = cq.Wire.assembleEdges(ie)
            input_wires.append(wire)

        # Side faces
        input_faces.extend(
            [
                cq.Face.makeRuledSurface(input_wires[0], input_wires[1]),  # Side attached to block
                cq.Face.makeFromWires(input_wires[2]),  # facing center
                cq.Face.makeFromWires(input_wires[3]),  # front face
                cq.Face.makeFromWires(input_wires[4]),  # front face
            ]
        )

        edges_top = [
            *input_edges[1],
            input_edges[2][2],
            input_edges[3][2],
            input_edges[4][2],
        ]
        edges_bot = [
            *input_edges[0],
            input_edges[2][0],
            input_edges[3][0],
            input_edges[4][0],
        ]

        input_faces.append(cq.func.fill(cq.func.wire(edges_top)))  # type: ignore
        input_faces.append(cq.func.fill(cq.func.wire(edges_bot)))  # type: ignore

        shell = cq.Shell.makeShell(input_faces)
        solid = cq.Solid.makeSolid(shell)

        return solid

    def _create_inner_post(
        self,
        points_bottom: npt.NDArray[np.float64],
        points_top: npt.NDArray[np.float64],
    ) -> cq.Solid:
        points = [points_bottom, points_top]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(
            n_straight,
            input_bsplines,
            *points,
        )

        vec_fb = cq.Vector(input_vectors[0][-1].x, input_vectors[0][-1].y, 0)
        vec_ft = cq.Vector(input_vectors[1][-1].x, input_vectors[1][-1].y, 0)

        r_inner = (input_vectors[0][0].x ** 2 + input_vectors[0][0].y ** 2) ** 0.5
        r_outer = (input_vectors[1][0].x ** 2 + input_vectors[1][0].y ** 2) ** 0.5
        phis_s = np.array([math.atan2(v[0].y, v[0].x) for v in input_vectors])
        phis_e = np.array([math.atan2(v[-1].y, v[-1].x) for v in input_vectors])
        phis = (phis_s + phis_e) / 2
        mid_1 = cq.Vector(
            r_inner * math.cos(phis[0]),
            r_inner * math.sin(phis[0]),
            0,
        )
        mid_2 = cq.Vector(r_outer * math.cos(phis[1]), r_outer * math.sin(phis[1]), 0)

        input_edges = []
        input_wires = []
        input_faces = []

        for i, iv in enumerate(input_vectors):
            tangents = input_tangents[i]
            edges = []

            # Straight section
            edges.append(cq.Edge.makeLine(iv[0], iv[n_straight]))

            # Curved section
            if len(iv) - n_straight <= 2:
                edges.append(cq.Edge.makeLine(iv[n_straight], iv[-1]))
            else:
                for edge_i in range(n_straight + 1, len(iv)):
                    t_i = edge_i - n_straight
                    cq_points = [iv[edge_i - 1], iv[edge_i]]
                    tangs = (tangents[t_i - 1], tangents[t_i])
                    edges.append(cq.Edge.makeSpline(cq_points, tangs, scale=True))

            input_edges.append(edges)

        input_edges.append(
            [
                cq.Edge.makeLine(vec_fb, input_vectors[0][-1]),
                cq.Edge.makeLine(input_vectors[0][-1], input_vectors[1][-1]),
                cq.Edge.makeLine(input_vectors[1][-1], vec_ft),
                cq.Edge.makeLine(vec_ft, vec_fb),
            ]
        )
        input_edges.append(
            [
                cq.Edge.makeThreePointArc(input_vectors[0][0], mid_1, vec_fb),
                cq.Edge.makeLine(vec_fb, vec_ft),
                cq.Edge.makeThreePointArc(vec_ft, mid_2, input_vectors[1][0]),
                cq.Edge.makeLine(input_vectors[1][0], input_vectors[0][0]),
            ]
        )

        for ie in input_edges:
            wire = cq.Wire.assembleEdges(ie)
            input_wires.append(wire)

        # Side faces
        input_faces.extend(
            [
                cq.Face.makeRuledSurface(input_wires[0], input_wires[1]),  # Side attached to block
                cq.Face.makeFromWires(input_wires[2]),  # facing center
                cq.Face.makeFromWires(input_wires[3]),  # front face
            ]
        )

        edges_top = [
            *input_edges[1],
            input_edges[2][2],
            input_edges[3][2],
        ]
        edges_bot = [
            *input_edges[0],
            input_edges[2][0],
            input_edges[3][0],
        ]

        input_faces.append(cq.func.fill(cq.func.wire(edges_top)))  # type: ignore
        input_faces.append(cq.func.fill(cq.func.wire(edges_bot)))  # type: ignore

        shell = cq.Shell.makeShell(input_faces)
        solid = cq.Solid.makeSolid(shell)

        return solid

    def _vertical_cut(
        self,
        input_vectors: list[list[cq.Vector]],
        cut_indices: list[tuple[int | None, cq.Vector, cq.Vector]],
        i_lower: int,
        i_upper: int,
    ):
        u_l = cut_indices[i_lower]
        u_u = cut_indices[i_upper]

        if u_l[0] is None or u_u[0] is None:
            raise ValueError("Missing cutting point for conductor part, cannot converge to geometry")

        z_cut = u_l[1].z

        # Find intersections between ruling lines and cut plane
        P_on_z = [u_l[1]]
        for i in range(u_l[0] + 1, u_u[0] + 1):
            P0 = input_vectors[i_lower][i]
            P1 = input_vectors[i_upper][i]
            dP = P1 - P0
            dz = z_cut - P0.z
            t = dz / dP.z
            P_cut = P0 + dP * t
            P_on_z.append(P_cut)
        P_on_z.append(u_u[1])

        # Make spline
        p_x = [p.x for p in P_on_z]
        p_y = [p.y for p in P_on_z]
        bspline = scipy.interpolate.make_interp_spline(p_y, p_x, k=3, bc_type=("natural", "natural"))
        tangs = [cq.Vector(d, 1, 0.0) for d in bspline(p_y, nu=1)]
        return P_on_z, tangs

    def _create_wedge_cut(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
        min_width: float,
        z_cut: float | None = None,
    ) -> cq.Solid:
        """
        Create a wedge between two blocks (in x,y) with tapering off to a minimum width.
        Used for conductors which wind onto the next inner layer, so don't have a spacer in yz plane.

        Basically the other end of a block_rounded_cut.
        """
        u_list, z_cut = self._calculate_u_at_max_width(
            points_front_bottom,
            points_front_top,
            points_back_bottom,
            points_back_top,
            max_width=min_width,
            z_cut=z_cut,
        )

        if u_list is None or z_cut is None:
            return self._create_block_rounded(
                points_front_bottom, points_front_top, points_back_bottom, points_back_top
            )

        points = [points_front_bottom, points_front_top, points_back_top, points_back_bottom]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)

        input_vectors, input_tangents = self._interpolate_points(n_straight, input_bsplines, *points)

        if not u_list:
            cut_indices = None
            z_ext = min([iv[n_straight].z for iv in input_vectors], key=abs)
            w_a = cq.Wire.makePolygon((iv[0] for iv in input_vectors), close=True)
            w_b = cq.Wire.makePolygon((cq.Vector(iv[0].x, iv[0].y, z_ext) for iv in input_vectors), close=True)
            solid = cq.Solid.makeLoft([w_a, w_b])
        else:
            u_list = [
                u_list[0],
                u_list[1],
                u_list[3],
                u_list[2],
            ]
            cut_indices = self._calculate_cutting_points(
                input_bsplines,
                u_list,
                z_cut,
                [cq.Vector(*p[n_straight]) for p in points],
            )

            # Start from here
            edges_back = []
            surfaces: list[cq.Shape] = []
            cut_points = {}
            side_edges: dict[int, list[cq.Edge]] = {i: [] for i in range(4)}
            # Perform cutting and restitching magic
            for i1, i2 in [(1, 2), (3, 0)]:
                ci1 = cut_indices[i1][0]
                ci2 = cut_indices[i2][0]

                if ci1 is None or ci2 is None:
                    raise ValueError("Missing cutting point for conductor part, cannot converge to geometry")

                if ci1 < ci2:
                    i_lower = i1
                    i_upper = i2
                else:
                    i_lower = i2
                    i_upper = i1

                u_l = cut_indices[i_lower]
                u_u = cut_indices[i_upper]
                z_cut = u_l[1].z

                assert u_l[0] is not None
                assert u_u[0] is not None

                P_on_z, tangs = self._vertical_cut(input_vectors, cut_indices, i_lower, i_upper)

                range_cross = list(range(u_l[0], u_u[0] + 1))
                side_surfaces = []
                back_edges = []

                for i_pz, i in enumerate(range_cross):
                    t_i = i - n_straight
                    points_upper = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                    tangs_upper = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                    points_lower = (input_vectors[i_lower][i], input_vectors[i_lower][i + 1])
                    tangs_lower = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])

                    if i_pz == 0:  # First segment
                        edges = [
                            cq.Edge.makeSpline(
                                [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                            ),
                            cq.Edge.makeLine(P_on_z[i_pz + 1], points_upper[1]),
                            cq.Edge.makeSpline(
                                [points_upper[1], points_upper[0]], (-tangs_upper[1], -tangs_upper[0]), scale=True
                            ),
                            cq.Edge.makeLine(points_upper[0], points_lower[0]),
                            cq.Edge.makeSpline([points_lower[0], P_on_z[i_pz]], (tangs_lower[0], u_l[2]), scale=True),
                        ]
                        side_edges[i_upper].append(edges[2])
                        side_edges[i_lower].append(edges[4])
                        back_edges.append(edges[0])
                        cut_points[i_upper] = P_on_z[i_pz + 1]
                    elif i_pz == len(range_cross) - 1:  # Last triangle
                        edges = [
                            cq.Edge.makeSpline(
                                [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                            ),
                            cq.Edge.makeSpline(
                                [P_on_z[i_pz + 1], points_upper[0]], (-u_u[2], -tangs_upper[0]), scale=True
                            ),
                            cq.Edge.makeLine(points_upper[0], P_on_z[i_pz]),
                        ]
                        side_edges[i_upper].append(edges[1])
                        back_edges.append(edges[0])
                        cut_points[i_lower] = P_on_z[i_pz]
                    else:  # Middle segments
                        edges = [
                            cq.Edge.makeSpline(
                                [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                            ),
                            cq.Edge.makeLine(P_on_z[i_pz + 1], points_upper[1]),
                            cq.Edge.makeSpline(
                                [points_upper[1], points_upper[0]], (-tangs_upper[1], -tangs_upper[0]), scale=True
                            ),
                            cq.Edge.makeLine(points_upper[0], P_on_z[i_pz]),
                        ]
                        back_edges.append(edges[0])
                        side_edges[i_upper].append(edges[2])

                    surf = cq.func.fill(cq.Wire.assembleEdges(edges))
                    side_surfaces.append(surf)

                for i in range(u_l[0]):
                    if i < n_straight:
                        edge_lower = cq.Edge.makeLine(input_vectors[i_lower][i], input_vectors[i_lower][i + 1])
                        edge_upper = cq.Edge.makeLine(input_vectors[i_upper][i], input_vectors[i_upper][i + 1])
                    else:
                        t_i = i - n_straight
                        cq_points = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                        tangs = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                        edge_upper = cq.Edge.makeSpline(
                            cq_points,
                            tangs,
                        )
                        cq_points = [input_vectors[i_lower][i], input_vectors[i_lower][i + 1]]
                        tangs = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])
                        edge_lower = cq.Edge.makeSpline(
                            cq_points,
                            tangs,
                        )

                    side_edges[i_upper].append(edge_upper)
                    side_edges[i_lower].append(edge_lower)
                    surf = cq.Face.makeRuledSurface(edge_lower, edge_upper)
                    side_surfaces.append(surf)

                edges_back.append(back_edges)

                surfaces.extend(side_surfaces)

            r_inner = (cut_indices[0][1].x ** 2 + cut_indices[0][1].y ** 2) ** 0.5
            r_outer = (cut_indices[2][1].x ** 2 + cut_indices[2][1].y ** 2) ** 0.5
            phis = [math.atan2(ci[1].y, ci[1].x) for ci in cut_indices]
            z_inner = z_cut
            z_outer = z_cut

            mid_2 = cq.Vector(
                r_outer * math.cos((phis[2] + phis[3]) / 2), r_outer * math.sin((phis[2] + phis[3]) / 2), z_outer
            )
            mid_1 = cq.Vector(
                r_inner * math.cos((phis[0] + phis[1]) / 2), r_inner * math.sin((phis[0] + phis[1]) / 2), z_inner
            )

            ebb = cq.Edge.makeThreePointArc(cut_indices[0][1], mid_1, cut_indices[1][1])
            ebt = cq.Edge.makeThreePointArc(cut_indices[2][1], mid_2, cut_indices[3][1])

            back_edges = [
                *edges_back[0],
                ebt,
                *edges_back[1],
                ebb,
            ]

            back_surface = cq.Face.makeFromWires(cq.Wire.assembleEdges(back_edges))

            surfaces.append(back_surface)

            r_inner = (input_vectors[0][0].x ** 2 + input_vectors[0][0].y ** 2) ** 0.5
            r_outer = (input_vectors[2][0].x ** 2 + input_vectors[2][0].y ** 2) ** 0.5
            phis = [math.atan2(v[0].y, v[0].x) for v in input_vectors]
            z_inner = (input_vectors[0][0].z + input_vectors[1][0].z) / 2
            z_outer = (input_vectors[2][0].z + input_vectors[3][0].z) / 2

            mid_1 = cq.Vector(
                r_inner * math.cos((phis[1] + phis[0]) / 2), r_inner * math.sin((phis[1] + phis[0]) / 2), z_inner
            )
            mid_2 = cq.Vector(
                r_outer * math.cos((phis[3] + phis[2]) / 2), r_outer * math.sin((phis[3] + phis[2]) / 2), z_outer
            )

            efb = cq.Edge.makeThreePointArc(input_vectors[0][0], mid_1, input_vectors[1][0])
            eft = cq.Edge.makeThreePointArc(input_vectors[2][0], mid_2, input_vectors[3][0])

            front_edges = [
                cq.Edge.makeLine(input_vectors[1][0], input_vectors[2][0]),
                eft,
                cq.Edge.makeLine(input_vectors[3][0], input_vectors[0][0]),
                efb,
            ]

            front_surface = cq.Face.makeFromWires(cq.Wire.assembleEdges(front_edges))

            surfaces.append(front_surface)

            edges_top = [
                *side_edges[2],
                eft,
                *side_edges[3],
                ebt,
            ]
            edges_bot = [
                *side_edges[0],
                efb,
                *side_edges[1],
                ebb,
            ]

            surfaces.append(cq.func.fill(cq.func.wire(edges_top)))
            surfaces.append(cq.func.fill(cq.func.wire(edges_bot)))

            shell = cq.Shell.makeShell(surfaces)  # type: ignore
            solid = cq.Solid.makeSolid(shell)

            return solid

        return solid

    def _create_block_rounded_cut(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
        min_width: float,
        z_cut: float | None = None,
    ) -> cq.Solid:
        u_list, z_cut = self._calculate_u_at_min_width(
            points_front_bottom,
            points_front_top,
            points_back_bottom,
            points_back_top,
            min_width=min_width,
            z_cut=z_cut,
        )
        if not u_list or z_cut is None:
            return self._create_block_rounded(
                points_front_bottom, points_front_top, points_back_bottom, points_back_top
            )

        u_list = [
            u_list[0],
            u_list[1],
            u_list[3],
            u_list[2],
        ]

        points = [points_front_bottom, points_front_top, points_back_top, points_back_bottom]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(n_straight, input_bsplines, *points)
        points_ss = [cq.Vector(*p[n_straight]) for p in points]
        cut_indices = self._calculate_cutting_points(
            input_bsplines,
            u_list,
            z_cut,
            points_ss,
        )

        edges_front = []
        edges_back = []
        surfaces = []
        cut_points = {}
        side_edges: dict[int, list[cq.Edge]] = {i: [] for i in range(4)}
        # Perform cutting and restitching magic
        u_l: tuple[int | None, cq.Vector, cq.Vector]
        u_u: tuple[int | None, cq.Vector, cq.Vector]
        for i1, i2 in [(1, 2), (3, 0)]:
            side_surfaces: list[cq.Shape] = []
            front_edges = []

            if cut_indices[i1][0] is None and cut_indices[i2][0] is None:
                # Cut in the straight section
                i_lower = i1
                i_upper = i2

                pcl = cq.Vector(points_ss[i_lower].x, points_ss[i_lower].y, z_cut)
                pcu = cq.Vector(points_ss[i_upper].x, points_ss[i_upper].y, z_cut)

                psl = points_ss[i_lower]
                psu = points_ss[i_upper]

                edges = [
                    cq.Edge.makeLine(pcl, psl),
                    cq.Edge.makeLine(psl, psu),
                    cq.Edge.makeLine(psu, pcu),
                    cq.Edge.makeLine(pcu, pcl),
                ]

                side_edges[i_lower].append(edges[0])
                side_edges[i_upper].append(edges[2])
                front_edges.append(edges[3])
                cut_points[i_lower] = pcl
                cut_points[i_upper] = pcu

                # update u_u and _ul
                u_l = (n_straight - 1, pcl, cq.Vector(0, 0, 1))
                u_u = (n_straight - 1, pcu, cq.Vector(0, 0, 1))

                surf = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges))
                side_surfaces.append(surf)
            elif cut_indices[i1][0] is None or cut_indices[i2][0] is None:
                raise RuntimeError("One cut index is None, not implemented yet")
            else:
                ci1 = cut_indices[i1][0]
                ci2 = cut_indices[i2][0]

                if ci1 is None or ci2 is None:
                    raise ValueError("Missing cutting point for conductor part, cannot converge to geometry")

                if ci1 < ci2:
                    i_lower = i1
                    i_upper = i2
                else:
                    i_lower = i2
                    i_upper = i1

                u_l = cut_indices[i_lower]
                u_u = cut_indices[i_upper]

                assert u_l[0] is not None
                assert u_u[0] is not None

                P_on_z, tangs = self._vertical_cut(input_vectors, cut_indices, i_lower, i_upper)

                range_cross = list(range(u_l[0], u_u[0] + 1))
                if len(range_cross) == 1:
                    i = range_cross[0]
                    t_i = i - n_straight
                    i_pz = 0
                    points_upper = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                    tangs_upper = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                    points_lower = (input_vectors[i_lower][i], input_vectors[i_lower][i + 1])
                    tangs_lower = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])

                    edges = [
                        cq.Edge.makeSpline(
                            [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                        ),
                        cq.Edge.makeSpline([P_on_z[i_pz + 1], points_upper[1]], (u_u[2], tangs_upper[1]), scale=True),
                        cq.Edge.makeLine(points_upper[1], points_lower[1]),
                        cq.Edge.makeSpline([points_lower[1], P_on_z[i_pz]], (-tangs_lower[1], -u_l[2]), scale=True),
                    ]
                    side_edges[i_upper].append(edges[1])
                    side_edges[i_lower].append(edges[3])
                    front_edges.append(edges[0])
                    cut_points[i_lower] = P_on_z[i_pz]
                    cut_points[i_upper] = P_on_z[i_pz + 1]
                    side_surfaces.append(cq.func.fill(cq.Wire.assembleEdges(edges)))  #
                else:
                    for i_pz, i in enumerate(range_cross):
                        t_i = i - n_straight
                        points_upper = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                        tangs_upper = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                        points_lower = (input_vectors[i_lower][i], input_vectors[i_lower][i + 1])
                        tangs_lower = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])

                        if i_pz == 0:  # First triangle
                            edges = [
                                cq.Edge.makeSpline(
                                    [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                                ),
                                cq.Edge.makeLine(P_on_z[i_pz + 1], points_lower[1]),
                                cq.Edge.makeSpline(
                                    [points_lower[1], P_on_z[i_pz]], (-tangs_lower[1], -u_l[2]), scale=True
                                ),
                            ]
                            side_edges[i_lower].append(edges[-1])
                            front_edges.append(edges[0])
                            cut_points[i_lower] = P_on_z[i_pz]
                        elif i_pz == len(range_cross) - 1:  # Last Segment
                            edges = [
                                cq.Edge.makeSpline(
                                    [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                                ),
                                cq.Edge.makeSpline(
                                    [P_on_z[i_pz + 1], points_upper[1]], (u_u[2], tangs_upper[1]), scale=True
                                ),
                                cq.Edge.makeLine(points_upper[1], points_lower[1]),
                                cq.Edge.makeSpline(
                                    [points_lower[1], points_lower[0]], (-tangs_lower[1], -tangs_lower[0]), scale=True
                                ),
                                cq.Edge.makeLine(points_lower[0], P_on_z[i_pz]),
                            ]
                            side_edges[i_upper].append(edges[1])
                            side_edges[i_lower].append(edges[3])
                            front_edges.append(edges[0])
                            cut_points[i_upper] = P_on_z[i_pz + 1]
                        else:  # Middle segments
                            edges = [
                                cq.Edge.makeSpline(
                                    [P_on_z[i_pz], P_on_z[i_pz + 1]], (tangs[i_pz], tangs[i_pz + 1]), scale=True
                                ),
                                cq.Edge.makeLine(P_on_z[i_pz + 1], points_lower[1]),
                                cq.Edge.makeSpline(
                                    [points_lower[1], points_lower[0]], (-tangs_lower[1], -tangs_lower[0]), scale=True
                                ),
                                cq.Edge.makeLine(points_lower[0], P_on_z[i_pz]),
                            ]
                            front_edges.append(edges[0])
                            side_edges[i_lower].append(edges[2])

                        side_surfaces.append(cq.func.fill(cq.Wire.assembleEdges(edges)))  #

            # Fill out the rest of the sides
            assert u_l[0] is not None
            assert u_u[0] is not None
            for i in range(u_u[0] + 1, len(input_vectors[i_upper]) - 1):
                t_i = i - n_straight
                cq_points = [input_vectors[i_upper][i], input_vectors[i_upper][i + 1]]
                tangs = [input_tangents[i_upper][t_i], input_tangents[i_upper][t_i + 1]]
                edge_upper = cq.Edge.makeSpline(
                    cq_points,
                    tangs,
                )
                cq_points = [input_vectors[i_lower][i], input_vectors[i_lower][i + 1]]
                tangs = (input_tangents[i_lower][t_i], input_tangents[i_lower][t_i + 1])
                edge_lower = cq.Edge.makeSpline(
                    cq_points,
                    tangs,
                )
                side_edges[i_upper].append(edge_upper)
                side_edges[i_lower].append(edge_lower)
                surf = cq.Face.makeRuledSurface(edge_lower, edge_upper)
                side_surfaces.append(surf)

            edges_back.append(cq.Edge.makeLine(input_vectors[i_lower][-1], input_vectors[i_upper][-1]))
            edges_front.append(front_edges)
            surfaces.extend(side_surfaces)

        edges_back.append(cq.Edge.makeLine(input_vectors[0][-1], input_vectors[1][-1]))
        edges_back.append(cq.Edge.makeLine(input_vectors[2][-1], input_vectors[3][-1]))

        back_wires = cq.Wire.assembleEdges(edges_back)
        try:
            back_surface: cq.Shape = cq.Face.makeFromWires(back_wires)
        except ValueError as ve:
            self.logger.warn(f"Error while creating planar surface: {ve}. Trying fill")
            back_surface = cq.func.fill(back_wires)
        surfaces.append(back_surface)

        r_inner = (cut_points[0].x ** 2 + cut_points[0].y ** 2) ** 0.5
        r_outer = (cut_points[2].x ** 2 + cut_points[2].y ** 2) ** 0.5
        phis = {i: math.atan2(v.y, v.x) for i, v in cut_points.items()}
        z_inner = z_cut
        z_outer = z_cut

        mid_1 = cq.Vector(
            r_inner * math.cos((phis[1] + phis[0]) / 2), r_inner * math.sin((phis[1] + phis[0]) / 2), z_inner
        )
        mid_2 = cq.Vector(
            r_outer * math.cos((phis[3] + phis[2]) / 2), r_outer * math.sin((phis[3] + phis[2]) / 2), z_outer
        )

        efb = cq.Edge.makeThreePointArc(cut_indices[0][1], mid_1, cut_indices[1][1])
        eft = cq.Edge.makeThreePointArc(cut_indices[2][1], mid_2, cut_indices[3][1])

        front_edges = [
            *edges_front[0],
            eft,
            *edges_front[1],
            efb,
        ]
        front_surface = cq.Face.makeFromWires(cq.Wire.assembleEdges(front_edges))
        surfaces.append(front_surface)

        edges_top = [
            *side_edges[2],
            *side_edges[3],
            eft,
            edges_back[3],
        ]
        edges_bot = [
            *side_edges[0],
            *side_edges[1],
            efb,
            edges_back[2],
        ]

        surfaces.append(cq.func.fill(cq.func.wire(edges_top)))
        surfaces.append(cq.func.fill(cq.func.wire(edges_bot)))

        shell = cq.Shell.makeShell(surfaces)  # type: ignore
        solid = cq.Solid.makeSolid(shell)

        return solid

    def _create_block_rounded(
        self,
        points_front_bottom: npt.NDArray[np.float64],
        points_front_top: npt.NDArray[np.float64],
        points_back_bottom: npt.NDArray[np.float64],
        points_back_top: npt.NDArray[np.float64],
    ) -> cq.Solid:
        points = [points_front_bottom, points_front_top, points_back_top, points_back_bottom]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(n_straight, input_bsplines, *points)

        input_edges = []
        input_wires = []
        input_faces: list[cq.Shape] = []

        edges_front: list[cq.Edge] = []
        edges_back: list[cq.Edge] = []

        for i, iv in enumerate(input_vectors):
            tangents = input_tangents[i]
            edges = []

            if len(iv) - n_straight <= 2:
                # Only straight section
                edges.append(cq.Edge.makeLine(iv[0], iv[n_straight]))
                if len(iv) < n_straight:
                    edges.append(cq.Edge.makeLine(iv[n_straight], iv[-1]))
            else:
                # Curved section
                if n_straight > 0:
                    edges.append(cq.Edge.makeLine(iv[0], iv[n_straight]))
                    first_curve_idx = n_straight + 1
                else:
                    first_curve_idx = 1
                for edge_i in range(first_curve_idx, len(iv)):
                    t_i = edge_i - n_straight
                    cq_points = [iv[edge_i - 1], iv[edge_i]]
                    tangs = (tangents[t_i - 1], tangents[t_i])
                    edges.append(cq.Edge.makeSpline(cq_points, tangs, scale=True))

            input_edges.append(edges)

        for ie in input_edges:
            wire = cq.Wire.assembleEdges(ie)
            input_wires.append(wire)

        # Side faces
        for i, i2 in [(1, 2), (3, 0)]:
            f = cq.Face.makeRuledSurface(input_wires[i], input_wires[i2])

            input_faces.append(f)
            edges_front.append(cq.Edge.makeLine(input_vectors[i][0], input_vectors[i2][0]))
            edges_back.append(cq.Edge.makeLine(input_vectors[i][-1], input_vectors[i2][-1]))

        r_inner = (input_vectors[0][0].x ** 2 + input_vectors[0][0].y ** 2) ** 0.5
        r_outer = (input_vectors[2][0].x ** 2 + input_vectors[2][0].y ** 2) ** 0.5
        phis = [math.atan2(v[0].y, v[0].x) for v in input_vectors]
        z_inner = (input_vectors[0][0].z + input_vectors[1][0].z) / 2
        z_outer = (input_vectors[2][0].z + input_vectors[3][0].z) / 2

        mid_1 = cq.Vector(
            r_inner * math.cos((phis[1] + phis[0]) / 2), r_inner * math.sin((phis[1] + phis[0]) / 2), z_inner
        )
        mid_2 = cq.Vector(
            r_outer * math.cos((phis[3] + phis[2]) / 2), r_outer * math.sin((phis[3] + phis[2]) / 2), z_outer
        )

        edges_front.append(cq.Edge.makeThreePointArc(input_vectors[0][0], mid_1, input_vectors[1][0]))
        edges_front.append(cq.Edge.makeThreePointArc(input_vectors[2][0], mid_2, input_vectors[3][0]))

        edges_back.append(cq.Edge.makeLine(input_vectors[0][-1], input_vectors[1][-1]))
        edges_back.append(cq.Edge.makeLine(input_vectors[2][-1], input_vectors[3][-1]))

        edges_top = [
            *input_edges[2],
            *input_edges[3],
            edges_front[3],
            edges_back[3],
        ]
        edges_bot = [
            *input_edges[0],
            *input_edges[1],
            edges_front[2],
            edges_back[2],
        ]
        input_faces.append(cq.Face.makeFromWires(cq.Wire.assembleEdges(edges_front)))
        try:
            face_back: cq.Shape = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges_back))
        except ValueError as ve:
            self.logger.warn(f"Error while creating planar surface: {ve}. Trying fill")
            face_back = cq.func.fill(cq.Wire.assembleEdges(edges_back))

        input_faces.append(face_back)
        input_faces.append(cq.func.fill(cq.func.wire(edges_top)))
        input_faces.append(cq.func.fill(cq.func.wire(edges_bot)))

        shell = cq.Shell.makeShell(input_faces)  # type: ignore
        solid = cq.Solid.makeSolid(shell)

        return solid

    def _create_hollow_block(
        self,
        outer_points_front_bottom: npt.NDArray[np.float64],
        outer_points_front_top: npt.NDArray[np.float64],
        outer_points_back_bottom: npt.NDArray[np.float64],
        outer_points_back_top: npt.NDArray[np.float64],
        inner_points_front_bottom: npt.NDArray[np.float64],
        inner_points_front_top: npt.NDArray[np.float64],
        inner_points_back_bottom: npt.NDArray[np.float64],
        inner_points_back_top: npt.NDArray[np.float64],
    ):
        points = [
            outer_points_front_bottom,
            outer_points_front_top,
            outer_points_back_top,
            outer_points_back_bottom,
            inner_points_front_bottom,
            inner_points_front_top,
            inner_points_back_top,
            inner_points_back_bottom,
        ]
        input_bsplines, n_straight = self._calculate_bsplines_n_straight(*points)
        input_vectors, input_tangents = self._interpolate_points(
            n_straight,
            input_bsplines,
            *points,
        )

        input_edges = []
        input_wires = []
        input_faces = []

        for i, iv in enumerate(input_vectors):
            tangents = input_tangents[i]
            edges = []

            # Straight section
            edges.append(cq.Edge.makeLine(iv[0], iv[n_straight]))

            # Curved section
            if len(iv) - n_straight <= 2:
                edges.append(cq.Edge.makeLine(iv[n_straight], iv[-1]))
            else:
                for edge_i in range(n_straight + 1, len(iv)):
                    t_i = edge_i - n_straight
                    cq_points = [iv[edge_i - 1], iv[edge_i]]
                    tangs = (tangents[t_i - 1], tangents[t_i])
                    edges.append(cq.Edge.makeSpline(cq_points, tangs, scale=True))

            input_edges.append(edges)

        for ie in input_edges:
            wire = cq.Wire.assembleEdges(ie)
            input_wires.append(wire)

        # Side faces
        for i, i2 in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4)]:
            f = cq.Face.makeRuledSurface(input_wires[i], input_wires[i2])
            input_faces.append(f)

        # Top / bottom
        wlist = []
        for idx, vs in itertools.product((0, -1), ([0, 1, 2, 3], [4, 5, 6, 7])):
            wlist.append(cq.Wire.makePolygon([input_vectors[v][idx] for v in vs], close=True))

        wso, wsi, weo, wei = wlist
        fs = cq.Face.makeFromWires(wso, [wsi])
        fe = cq.Face.makeFromWires(weo, [wei])
        shell = cq.Shell.makeShell(input_faces + [fs, fe])
        solid = cq.Solid.makeSolid(shell)

        return solid
