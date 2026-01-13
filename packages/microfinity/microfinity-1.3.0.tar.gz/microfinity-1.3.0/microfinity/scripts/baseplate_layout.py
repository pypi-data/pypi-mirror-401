#! /usr/bin/env python3
"""
Command line script to generate segmented Gridfinity baseplate layouts for drawers.
"""
import argparse
import os

import microfinity
from microfinity import (
    GridfinityBaseplateLayout,
    GridfinityConnectionClip,
    SegmentationMode,
    ToleranceMode,
)

title = """
  _____      _     _  __ _       _ _           _                            _
 / ____|    (_)   | |/ _(_)     (_) |         | |                          | |
| |  __ _ __ _  __| | |_ _ _ __  _| |_ _   _  | |     __ _ _   _  ___  _   _| |_
| | |_ | '__| |/ _` |  _| | '_ \\| | __| | | | | |    / _` | | | |/ _ \\| | | | __|
| |__| | |  | | (_| | | | | | | | | |_| |_| | | |___| (_| | |_| | (_) | |_| | |_
 \\_____|_|  |_|\\__,_|_| |_|_| |_|_|\\__|\\__, | |______\\__,_|\\__, |\\___/ \\__,_|\\__|
                                        __/ |               __/ |
                                       |___/               |___/
"""

DESC = """
Generate segmented Gridfinity baseplate layouts for drawers.

Calculates optimal baseplate tiling given drawer dimensions and build plate constraints.
Supports fractional sizes (quarter-grid by default) and generates connection clips.

Features:
  - Automatic segmentation to fit build plate
  - Fractional edge pieces for perfect drawer fit
  - Connection clip notches on seams
  - Integrated solid fill for sub-grid gaps
"""

EPILOG = """
example usages:

  Generate layout for 450x380mm drawer with 220x220mm build plate:
  $ microfinity-baseplate-layout --drawer 450 380 --buildplate 220 220 -o ./drawer -f stl

  Same but with custom tolerance and minimum segment size:
  $ microfinity-baseplate-layout -d 450 380 -b 220 220 --tolerance 1.0 --min-segment 2.0

  Just print the layout summary without exporting:
  $ microfinity-baseplate-layout -d 450 380 -b 220 220 --summary

  Export only clips (e.g., if you already have the baseplates):
  $ microfinity-baseplate-layout -d 450 380 -b 220 220 --clips-only -o ./clips

  Skip clips entirely:
  $ microfinity-baseplate-layout -d 450 380 -b 220 220 --no-clips -o ./plates

  Export fit test strips to validate drawer fit before full prints:
  $ microfinity-baseplate-layout -d 450 380 -b 220 220 --fit-strips -o ./fit_test

  Export only fit strips (quick validation):
  $ microfinity-baseplate-layout -d 450 380 -b 220 220 --fit-strips-only -o ./fit_test
"""


def main():
    parser = argparse.ArgumentParser(
        description=DESC,
        epilog=EPILOG,
        prefix_chars="-+",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "-d",
        "--drawer",
        nargs=2,
        type=float,
        required=True,
        metavar=("X", "Y"),
        help="Drawer interior dimensions in mm (X Y)",
    )
    parser.add_argument(
        "-b",
        "--buildplate",
        nargs=2,
        type=float,
        required=True,
        metavar=("X", "Y"),
        help="Build plate dimensions in mm (X Y)",
    )

    # Optional layout parameters
    parser.add_argument(
        "-M",
        "--micro",
        type=int,
        choices=[1, 2, 4],
        default=4,
        help="Micro-grid divisions (1=standard, 2=half, 4=quarter) default=4",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.5,
        help="Drawer clearance tolerance in mm (default=0.5)",
    )
    parser.add_argument(
        "--min-segment",
        type=float,
        default=1.0,
        help="Minimum segment size in U - avoids tiny pieces (default=1.0)",
    )
    parser.add_argument(
        "--clip-pitch",
        type=float,
        default=1.0,
        help="Clip spacing in U (default=1.0)",
    )
    parser.add_argument(
        "--print-margin",
        type=float,
        default=2.0,
        help="Build plate safety margin in mm (default=2.0)",
    )
    parser.add_argument(
        "--clip-clearance",
        type=float,
        default=0.2,
        help="Clip clearance in mm for fit adjustment (default=0.2)",
    )

    # Output options
    parser.add_argument(
        "-o",
        "--output",
        default="./layout_output",
        help="Output directory (default=./layout_output)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="step",
        choices=["step", "stl"],
        help="Output file format (default=step)",
    )

    # Clip handling
    clip_group = parser.add_mutually_exclusive_group()
    clip_group.add_argument(
        "--no-clips",
        action="store_true",
        default=False,
        help="Do not export clips (baseplates only)",
    )
    clip_group.add_argument(
        "--clips-only",
        action="store_true",
        default=False,
        help="Export only clips (no baseplates)",
    )

    # Fit strips
    fit_strip_group = parser.add_mutually_exclusive_group()
    fit_strip_group.add_argument(
        "--fit-strips",
        action="store_true",
        default=False,
        help="Also export fit test strips (thin edge strips to validate drawer fit)",
    )
    fit_strip_group.add_argument(
        "--fit-strips-only",
        action="store_true",
        default=False,
        help="Export only fit test strips (no baseplates or clips)",
    )
    parser.add_argument(
        "--fit-strip-width",
        type=float,
        default=10.0,
        help="Width of fit test strips in mm (default=10.0)",
    )

    # Other options
    parser.add_argument(
        "--preview",
        action="store_true",
        default=False,
        help="Also export a preview assembly showing all pieces",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        default=False,
        help="Print layout summary only (no export)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress verbose output",
    )

    args = parser.parse_args()
    argsd = vars(args)

    drawer_x, drawer_y = argsd["drawer"]
    buildplate_x, buildplate_y = argsd["buildplate"]
    micro_divisions = argsd["micro"]
    output_dir = argsd["output"]
    file_format = argsd["format"].lower()
    quiet = argsd["quiet"]

    if not quiet:
        print(title)
        print("Version: %s" % (microfinity.__version__))
        print()

    # Create layout
    layout = GridfinityBaseplateLayout(
        drawer_x_mm=drawer_x,
        drawer_y_mm=drawer_y,
        build_plate_x_mm=buildplate_x,
        build_plate_y_mm=buildplate_y,
        micro_divisions=micro_divisions,
        tolerance_mm=argsd["tolerance"],
        min_segment_u=argsd["min_segment"],
        clip_pitch_u=argsd["clip_pitch"],
        print_margin_mm=argsd["print_margin"],
    )

    # Get layout result
    result = layout.get_layout()

    if not quiet:
        print(f"Drawer: {drawer_x:.1f} x {drawer_y:.1f} mm")
        print(f"Build plate: {buildplate_x:.1f} x {buildplate_y:.1f} mm")
        print(f"Micro divisions: {micro_divisions} (pitch = {layout.micro_pitch:.2f} mm)")
        print()
        print(result.summary())
        print()

    # Summary-only mode
    if argsd["summary"]:
        return

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    exported_files = []

    # Export baseplates
    if not argsd["clips_only"] and not argsd["fit_strips_only"]:
        if not quiet:
            print("Exporting baseplates...")

        unique_pieces = result.unique_pieces()
        for sig, (piece, count) in unique_pieces.items():
            # Generate filename
            size_u = piece.size_u(micro_divisions)
            size_str = f"{size_u[0]:g}x{size_u[1]:g}"
            fn = f"baseplate_{piece.id}_{size_str}"
            if count > 1:
                fn += f"_x{count}"

            filepath = os.path.join(output_dir, fn)

            # Render and export
            bp = layout.render_piece(piece.id)
            if file_format == "stl":
                from microfinity import GridfinityExporter

                path = GridfinityExporter.to_stl(bp, filepath)
            else:
                from microfinity import GridfinityExporter

                path = GridfinityExporter.to_step(bp, filepath)

            exported_files.append(path)
            if not quiet:
                print(f"  - {os.path.basename(path)} (x{count})")

    # Export clips
    if not argsd["no_clips"] and not argsd["fit_strips_only"] and result.clip_count > 0:
        if not quiet:
            print("Exporting clips...")

        clip = GridfinityConnectionClip(clip_clearance_mm=argsd["clip_clearance"])

        # Export as a sheet of clips
        clip_sheet = layout.render_clip_sheet()
        fn = f"clips_x{result.clip_count}"
        filepath = os.path.join(output_dir, fn)

        if file_format == "stl":
            from microfinity import GridfinityExporter

            path = GridfinityExporter.to_stl(clip_sheet, filepath)
        else:
            from microfinity import GridfinityExporter

            path = GridfinityExporter.to_step(clip_sheet, filepath)

        exported_files.append(path)
        if not quiet:
            print(f"  - {os.path.basename(path)}")

    # Export preview
    if argsd["preview"] and not argsd["fit_strips_only"]:
        if not quiet:
            print("Exporting preview assembly...")

        preview = layout.render_preview()
        filepath = os.path.join(output_dir, "preview")

        if file_format == "stl":
            from microfinity import GridfinityExporter

            path = GridfinityExporter.to_stl(preview, filepath)
        else:
            from microfinity import GridfinityExporter

            path = GridfinityExporter.to_step(preview, filepath)

        exported_files.append(path)
        if not quiet:
            print(f"  - {os.path.basename(path)}")

    # Export fit strips
    if argsd["fit_strips"] or argsd["fit_strips_only"]:
        if not quiet:
            print("Exporting fit test strips...")

        fit_strip_paths = layout.export_fit_strips(
            path=output_dir,
            strip_width_mm=argsd["fit_strip_width"],
            file_format=file_format,
        )
        exported_files.extend(fit_strip_paths)
        if not quiet:
            for path in fit_strip_paths:
                print(f"  - {os.path.basename(path)}")

    if not quiet:
        print()
        print(f"Exported {len(exported_files)} file(s) to {output_dir}/")


if __name__ == "__main__":
    main()
