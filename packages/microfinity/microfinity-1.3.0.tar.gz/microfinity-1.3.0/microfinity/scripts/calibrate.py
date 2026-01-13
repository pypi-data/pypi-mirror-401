#! /usr/bin/env python3
"""
Command line script to generate Gridfinity calibration test prints.

Generates test prints for validating printer fit:
- Fractional pocket tests (0.25U, 0.5U, 0.75U) with female connector slots
- Clip clearance sweep for tuning clip tolerance
"""
import argparse
import os

import microfinity
from microfinity.calibration import (
    export_test_prints,
    generate_fractional_pocket_test_set,
    generate_clip_clearance_sweep,
    DEFAULT_CLEARANCE_SWEEP,
)
from microfinity.core.export import GridfinityExporter

title = """
   _____      _     _  __ _       _ _           _____      _ _ _
  / ____|    (_)   | |/ _(_)     (_) |         / ____|    | (_) |
 | |  __ _ __ _  __| | |_ _ _ __  _| |_ _   _  | |     __ _| |_| |__
 | | |_ | '__| |/ _` |  _| | '_ \\| | __| | | | | |    / _` | | | '_ \\
 | |__| | |  | | (_| | | | | | | | | |_| |_| | | |___| (_| | | | |_) |
  \\_____|_|  |_|\\__,_|_| |_|_| |_|_|\\__|\\__, |  \\_____\\__,_|_|_|_.__/
                                         __/ |
                                        |___/
"""

DESC = """
Generate calibration test prints for validating Gridfinity fit on your printer.

Test prints include:
- Fractional pocket tests (0.25U, 0.5U, 0.75U) with reference 1U pocket
  Each includes female connector slots for testing clip fit
- Clip clearance sweep with clips from -0.10mm to +0.60mm clearance
  Print these and test fit to find optimal clearance for your printer
"""

EPILOG = """
Example usages:

  Generate all test prints to ./calibration directory in STL format:
  $ microfinity-calibrate -o ./calibration -f stl

  Generate only fractional pocket tests:
  $ microfinity-calibrate --fractional -o ./test_prints

  Generate only clip clearance sweep:
  $ microfinity-calibrate --clips -o ./test_prints -f stl

Usage workflow:
  1. Print the fractional test plates (with female slots)
  2. Print the clip clearance sweep
  3. Test each clip in the slots
  4. Find the clip with the best snap-fit
  5. Use that clearance value in GridfinityConnectionClip(clip_clearance_mm=X)
"""


def main():
    parser = argparse.ArgumentParser(
        description=DESC,
        epilog=EPILOG,
        prefix_chars="-+",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="./calibration_prints",
        help="Output directory for test prints (default: ./calibration_prints)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="step",
        choices=["step", "stl"],
        help="Output file format (default: step)",
    )
    parser.add_argument(
        "--fractional",
        action="store_true",
        default=False,
        help="Generate only fractional pocket tests (with female slots)",
    )
    parser.add_argument(
        "--clips",
        action="store_true",
        default=False,
        help="Generate only clip clearance sweep",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress output messages",
    )

    args = parser.parse_args()
    argsd = vars(args)

    # If neither flag is set, generate both
    include_fractional = argsd["fractional"] or (not argsd["fractional"] and not argsd["clips"])
    include_clips = argsd["clips"] or (not argsd["fractional"] and not argsd["clips"])

    if not argsd["quiet"]:
        print(title)
        print("Version: %s" % (microfinity.__version__))
        print()

    output_dir = argsd["output"]
    file_format = argsd["format"].lower()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    exported_files = export_test_prints(
        path=output_dir,
        file_format=file_format,
        include_fractional=include_fractional,
        include_clip_sweep=include_clips,
    )

    if not argsd["quiet"]:
        print(f"Generated {len(exported_files)} file(s) in {output_dir}/:")
        for f in exported_files:
            print(f"  - {os.path.basename(f)}")
        print()

        if include_fractional:
            print("Fractional pocket tests:")
            print("  - Test pieces with 0.25U, 0.5U, and 0.75U fractional pockets")
            print("  - Each includes a reference 1U pocket")
            print("  - Female connector slots on right edge for clip testing")
            print()

        if include_clips:
            print("Clip clearance sweep:")
            print("  - Separate loose clips with varying clearances")
            print("  - Arranged left-to-right from tight to loose:")
            for i, c in enumerate(DEFAULT_CLEARANCE_SWEEP):
                sign = "+" if c >= 0 else ""
                note = ""
                if i == 0:
                    note = " (tightest)"
                elif i == len(DEFAULT_CLEARANCE_SWEEP) - 1:
                    note = " (loosest)"
                elif abs(c) < 0.001:
                    note = " (nominal)"
                print(f"    Clip {i + 1}: {sign}{c:.2f}mm{note}")
            print()

        print("How to use:")
        print("  1. Print the fractional test plates")
        print("  2. Print the clip clearance sweep")
        print("  3. Test each clip in the female slots")
        print("  4. Find the best-fitting clip")
        print("  5. Use that clearance in GridfinityConnectionClip(clip_clearance_mm=X)")


if __name__ == "__main__":
    main()
