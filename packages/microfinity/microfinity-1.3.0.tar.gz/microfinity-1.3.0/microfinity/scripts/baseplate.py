#! /usr/bin/env python3
"""
Command line script to make a Gridfinity baseplate.
"""
import argparse

import microfinity
from microfinity import GridfinityBaseplate

title = """
  _____      _     _  __ _       _ _           ____
 / ____|    (_)   | |/ _(_)     (_) |         |  _ \\
| |  __ _ __ _  __| | |_ _ _ __  _| |_ _   _  | |_) | __ _ ___  ___
| | |_ | '__| |/ _` |  _| | '_ \\| | __| | | | |  _ < / _` / __|/ _ \\
| |__| | |  | | (_| | | | | | | | | |_| |_| | | |_) | (_| \\__ \\  __/
 \\_____|_|  |_|\\__,_|_| |_|_| |_|_|\\__|\\__, | |____/ \\__,_|___/\\___|
                                        __/ |
                                       |___/
"""

DESC = """
Make a customized/parameterized Gridfinity compatible simple baseplate.

Supports fractional sizes with micro-grid (--micro):
  - micro=1: Standard 1U grid (42mm pitch)
  - micro=2: Half-grid (21mm pitch, 0.5U increments)
  - micro=4: Quarter-grid (10.5mm pitch, 0.25U increments) [default]

For segmented drawer layouts with multiple baseplates, use microfinity-baseplate-layout.
"""

EPILOG = """
example usages:

  6 x 3 baseplate to default STL file:
  $ microfinity-base 6 3 -f stl

  Fractional 2.5 x 3.25 baseplate using quarter-grid (default micro=4):
  $ microfinity-base 2.5 3.25 -f stl

  Standard integer-only baseplate (disable micro-grid):
  $ microfinity-base 4 3 --micro 1 -f stl

  Baseplate with corner screw mounting tabs:
  $ microfinity-base 6 4 -s -f stl
"""


def main():
    parser = argparse.ArgumentParser(
        description=DESC,
        epilog=EPILOG,
        prefix_chars="-+",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "length",
        metavar="length",
        type=float,
        help="Baseplate length in U (1U = 42 mm). Fractional values supported with --micro.",
    )
    parser.add_argument(
        "width",
        metavar="width",
        type=float,
        help="Baseplate width in U (1U = 42 mm). Fractional values supported with --micro.",
    )
    parser.add_argument(
        "-M",
        "--micro",
        type=int,
        choices=[1, 2, 4],
        default=4,
        help="Micro-grid divisions (1=standard, 2=half, 4=quarter) default=4",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="step",
        help="Output file format (STEP, STL, SVG) default=STEP",
    )
    parser.add_argument(
        "-s",
        "--screws",
        default=False,
        action="store_true",
        help="Add screw mounting tabs to the corners (adds +5 mm to depth)",
    )
    parser.add_argument(
        "-d",
        "--depth",
        default=None,
        type=float,
        action="store",
        help="Extrude extended depth under baseplate by this amount (mm)",
    )
    parser.add_argument(
        "-hd",
        "--holediam",
        default=None,
        type=float,
        action="store",
        help="Corner mounting screw hole diameter (default=5)",
    )
    parser.add_argument(
        "-hc",
        "--cskdiam",
        default=None,
        type=float,
        action="store",
        help="Corner mounting screw countersink diameter (default=10)",
    )
    parser.add_argument(
        "-ca",
        "--cskangle",
        default=None,
        type=float,
        action="store",
        help="Corner mounting screw countersink angle (deg) (default=82)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output filename (inferred output file format with extension)",
    )
    args = parser.parse_args()
    argsd = vars(args)

    length_u = argsd["length"]
    width_u = argsd["width"]
    micro_divisions = argsd["micro"]

    # Validate fractional sizes align with micro_divisions
    step = 1.0 / micro_divisions
    for name, val in [("length", length_u), ("width", width_u)]:
        if abs(val / step - round(val / step)) > 1e-6:
            parser.error(f"{name}={val} must be a multiple of {step} when --micro={micro_divisions}")

    print(title)
    print("Version: %s" % (microfinity.__version__))

    base = GridfinityBaseplate(
        length_u=length_u,
        width_u=width_u,
        micro_divisions=micro_divisions,
        ext_depth=argsd["depth"],
        corner_screws=argsd["screws"],
        csk_hole=argsd["holediam"],
        csk_diam=argsd["cskdiam"],
        csk_angle=argsd["cskangle"],
    )

    # Format size string (show decimals only if fractional)
    def fmt_u(val):
        return f"{val:g}"

    size_str = f"{fmt_u(length_u)}U x {fmt_u(width_u)}U"
    if micro_divisions > 1:
        size_str += f" (micro={micro_divisions})"

    print(
        "Gridfinity baseplate: %s (%.1f mm x %.1f mm)"
        % (
            size_str,
            base.length,
            base.width,
        )
    )

    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = base.filename()

    s = ["\nBaseplate generated and saved as"]
    if argsd["format"].lower() == "stl" or fn.lower().endswith(".stl"):
        if not fn.endswith(".stl"):
            fn = fn + ".stl"
        base.save_stl_file(filename=argsd["output"])
        s.append("%s in STL format" % (fn))
    elif argsd["format"].lower() == "svg" or fn.lower().endswith(".svg"):
        if not fn.endswith(".svg"):
            fn = fn + ".svg"
        base.save_svg_file(filename=argsd["output"])
        s.append("%s in SVG format" % (fn))
    else:
        if not fn.endswith(".step"):
            fn = fn + ".step"
        base.save_step_file(filename=argsd["output"])
        s.append("%s in STEP format" % (fn))
    print(" ".join(s))


if __name__ == "__main__":
    main()
