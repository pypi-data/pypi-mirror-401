#!/usr/bin/env python3
"""CLI interface for generating geometries using GeometryBuilder.

This script provides a command-line interface to the GeometryBuilder API,
allowing generation of coils, blocks, and endspacers from Roxie model data.
"""

import argparse
import sys
from pathlib import Path

from cadquery.vis import show
from roxieapi.input.builder import RoxieInputBuilder
from roxieapi.output.parser import RoxieOutputParser

from roxieinterfaces.geom import StepGenerator


def create_geometry():
    """Main entry point for the geometry generation CLI."""
    parser = argparse.ArgumentParser(
        description="Generate geometries from Roxie model data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input files (required)
    parser.add_argument("data_file", type=Path, help="Path to Roxie .data file")
    parser.add_argument("xml_file", type=Path, help="Path to Roxie .xml output file")

    # Output file
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=False,
        help="Output file path (extension determines format: .step, .stl, etc.)",
    )
    parser.add_argument("-p", "--plot", action="store_true", help="Plot the generated geometry")

    # Component selection - using add_* methods
    component_group = parser.add_argument_group("Component Selection")
    component_group.add_argument(
        "--conductors",
        type=int,
        nargs="+",
        metavar="ID",
        help="Conductor IDs to include",
    )
    component_group.add_argument(
        "--blocks",
        type=int,
        nargs="+",
        metavar="ID",
        help="Block IDs to include",
    )
    component_group.add_argument(
        "--coil-section",
        nargs=5,
        metavar=("RADIAL", "ANGULAR", "Z_DIR", "HALFID", "IDX"),
        action="append",
        help="Add coil section (use None for any value). Can be specified multiple times.",
    )
    component_group.add_argument(
        "--coil",
        nargs=2,
        type=int,
        metavar=("RADIAL", "ANGULAR"),
        action="append",
        help="Add complete coil by radial and angular number. Can be specified multiple times.",
    )
    component_group.add_argument("-a", "--all", action="store_true", help="Include all components")

    # Generation targets - using with_* methods
    generation_group = parser.add_argument_group("Generation Targets")
    generation_group.add_argument(
        "--with-coils",
        action="store_true",
        help="Generate coil geometries",
    )
    generation_group.add_argument(
        "--coil-insulation",
        action="store_true",
        help="Include insulation in coil geometry (use with --with-coils)",
    )
    generation_group.add_argument(
        "--with-insulations",
        action="store_true",
        help="Generate separate insulation geometries",
    )
    generation_group.add_argument(
        "--with-blocks",
        action="store_true",
        help="Generate coil block geometries",
    )
    generation_group.add_argument(
        "--coilblock-dr",
        type=float,
        default=0.0,
        help="Radial offset for blocks (default: 0.0)",
    )
    generation_group.add_argument(
        "--with-endspacers",
        action="store_true",
        help="Generate endspacer geometries",
    )
    generation_group.add_argument(
        "--endspacer-add-z",
        type=float,
        default=0.0,
        help="Additional z extension for endspacers (default: 0.0)",
    )
    generation_group.add_argument(
        "--endspacer-zmax",
        type=float,
        help="Maximum z extension for endspacers (overrides add-z)",
    )
    generation_group.add_argument(
        "--endspacer-min-width",
        type=float,
        help="Minimum width for endspacers",
    )

    # StepGenerator configuration
    config_group = parser.add_argument_group("StepGenerator Configuration")
    config_group.add_argument(
        "--former-ins-r",
        type=float,
        default=0.0,
        help="Additional former insulation (radial) (default: 0.0)",
    )
    config_group.add_argument(
        "--former-ins-phi",
        type=float,
        default=0.0,
        help="Additional former insulation (azimuthal) (default: 0.0)",
    )
    config_group.add_argument(
        "--opt-nr",
        type=int,
        default=1,
        help="Optimization number to use from Roxie output (default: 1)",
    )

    args = parser.parse_args()

    if not args.output and not args.plot:
        print("Error: Neither plotting nor output file defined. Doing nothing.", file=sys.stderr)
        sys.exit(1)

    # Validate input files
    if not args.data_file.exists():
        print(f"Error: Data file not found: {args.data_file}", file=sys.stderr)
        sys.exit(1)
    if not args.xml_file.exists():
        print(f"Error: XML file not found: {args.xml_file}", file=sys.stderr)
        sys.exit(1)

    # Validate that at least one generation target is specified
    if not any([args.with_coils, args.with_insulations, args.with_blocks, args.with_endspacers]):
        parser.error("At least one generation target must be specified (--with-coils, --with-blocks, etc.)")

    # Validate that at least one component is selected
    if not any([args.conductors, args.blocks, args.coil_section, args.coil, args.all]):
        parser.error(
            "At least one component selection must be specified (--conductors, --blocks, --coil-section, or --coil)"
        )

    # Load Roxie data
    print(f"Loading Roxie data from {args.data_file.name}...")
    try:
        roxie_input = RoxieInputBuilder.from_datafile(args.data_file)
        roxie_output = RoxieOutputParser(args.xml_file)
    except Exception as e:
        print(f"Error loading Roxie data: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize StepGenerator
    print("Initializing StepGenerator...")
    try:
        step_gen = StepGenerator(
            roxie_input=roxie_input,
            roxie_output=roxie_output,
            opt_nr=args.opt_nr,
        )
        step_gen.set_former_insulation(args.former_ins_r, args.former_ins_phi)
    except Exception as e:
        print(f"Error initializing StepGenerator: {e}", file=sys.stderr)
        sys.exit(1)

    # Build geometry using builder API
    print("Building geometry...")
    try:
        builder = step_gen.builder()

        # Add components
        if args.conductors:
            builder.add_conductors(*args.conductors)

        if args.blocks:
            builder.add_blocks(*args.blocks, also_conductors=True)

        if args.coil_section:
            for section in args.coil_section:
                radial = None if section[0] == "None" else int(section[0])
                angular = None if section[1] == "None" else int(section[1])
                z_dir = None if section[2] == "None" else int(section[2])
                halfid = None if section[3] == "None" else int(section[3])
                idx = None if section[4] == "None" else int(section[4])
                builder.add_coil_section(radial, angular, z_dir, halfid, idx, also_conductors=True)

        if args.coil:
            for radial, angular in args.coil:
                builder.add_coil(radial, angular, also_conductors=True)

        if args.all:
            builder.add_all()

        # Configure generation targets
        if args.with_coils:
            builder.with_coils(add_insulation=args.coil_insulation)

        if args.with_insulations:
            builder.with_insulations()

        if args.with_blocks:
            builder.with_blocks(coilblock_dr=args.coilblock_dr)

        if args.with_endspacers:
            builder.with_endspacers(
                add_z=args.endspacer_add_z,
                zmax=args.endspacer_zmax,
                min_width=args.endspacer_min_width,
            )

        # Generate
        print("Generating geometries...")
        assembly = builder.generate()

    except Exception as e:
        print(f"Error generating geometries: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)

    # Optional plotting
    if args.plot:
        show(assembly)

    # Save output
    print(f"Saving to {args.output}...")
    try:
        # Create parent directory if it doesn't exist
        args.output.parent.mkdir(parents=True, exist_ok=True)
        assembly.export(str(args.output))
        print(f"Successfully saved to {args.output}")
    except Exception as e:
        print(f"Error saving output: {e}", file=sys.stderr)
        sys.exit(1)
