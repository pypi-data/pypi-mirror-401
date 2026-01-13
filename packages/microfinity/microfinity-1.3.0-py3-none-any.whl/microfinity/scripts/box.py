#! /usr/bin/env python3
"""
Command line script to make a Gridfinity box.
"""
import argparse

import microfinity
from microfinity import GridfinityBox, GR_BOT_H

title = """
  _____      _     _  __ _       _ _           ____
 / ____|    (_)   | |/ _(_)     (_) |         |  _ \\
| |  __ _ __ _  __| | |_ _ _ __  _| |_ _   _  | |_) | _____  __
| | |_ | '__| |/ _` |  _| | '_ \\| | __| | | | |  _ < / _ \\ \\/ /
| |__| | |  | | (_| | | | | | | | | |_| |_| | | |_) | (_) >  <
 \\_____|_|  |_|\\__,_|_| |_|_| |_|_|\\__|\\__, | |____/ \\___/_/\\_\\
                                        __/ |
                                       |___/
"""

DESC = """
Make a customized/parameterized Gridfinity compatible box with many optional features.

Supports fractional sizes with micro-grid (--micro):
  - micro=1: Standard 1U grid (42mm pitch)
  - micro=2: Half-grid (21mm pitch, 0.5U increments)
  - micro=4: Quarter-grid (10.5mm pitch, 0.25U increments) [default]
"""

EPILOG = """
example usages:

  2x3x5 box with magnet holes saved to STL file with default filename:
  $ microfinity-box 2 3 5 -m -f stl

  1x3x4 box with scoops, label strip, 3 internal partitions and specified name:
  $ microfinity-box 1 3 4 -s -l -ld 3 -o MyBox.step

  Solid 3x3x3 box with 50% fill, unsupported magnet holes and no top lip:
  $ microfinity-box 3 3 3 -d -r 0.5 -u -n

  Lite style box 3x2x3 with label strip, partitions, output to default SVG file:
  $ microfinity-box 3 2 3 -e -l -ld 2 -f svg

  Fractional 1.25x2x3 box using quarter-grid (default micro=4):
  $ microfinity-box 1.25 2 3 -f stl

  Standard integer-only box (disable micro-grid):
  $ microfinity-box 2 3 5 --micro 1 -f stl
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
        help="Box length in U (1U = 42 mm). Fractional values supported with --micro.",
    )
    parser.add_argument(
        "width",
        metavar="width",
        type=float,
        help="Box width in U (1U = 42 mm). Fractional values supported with --micro.",
    )
    parser.add_argument(
        "height",
        metavar="height",
        type=int,
        help="Box height in U (1U = 7 mm)",
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
        "-m",
        "--magnetholes",
        action="store_true",
        default=False,
        help="Add bottom magnet/mounting holes",
    )
    parser.add_argument(
        "-u",
        "--unsupported",
        action="store_true",
        default=False,
        help="Add bottom magnet holes with 3D printer friendly strips without support",
    )
    parser.add_argument(
        "-n",
        "--nolip",
        action="store_true",
        default=False,
        help="Do not add mating lip to the top perimeter",
    )
    parser.add_argument(
        "-s",
        "--scoops",
        action="store_true",
        default=False,
        help="Add finger scoops against each length-wise back wall",
    )
    parser.add_argument(
        "-l",
        "--labels",
        action="store_true",
        default=False,
        help="Add label strips against each length-wise front wall",
    )
    parser.add_argument(
        "-e",
        "--ecolite",
        action="store_true",
        default=False,
        help="Make economy / lite style box with no elevated floor",
    )
    parser.add_argument(
        "-d",
        "--solid",
        action="store_true",
        default=False,
        help="Make solid (filled) box for customized storage",
    )
    parser.add_argument(
        "-r",
        "--ratio",
        action="store",
        type=float,
        default=1.0,
        help="Solid box fill ratio 0.0 = minimum, 1.0 = full height",
    )
    parser.add_argument(
        "-ld",
        "--lengthdiv",
        action="store",
        type=int,
        default=0,
        help="Split box length-wise with specified number of divider walls",
    )
    parser.add_argument(
        "-wd",
        "--widthdiv",
        action="store",
        type=int,
        default=0,
        help="Split box width-wise with specified number of divider walls",
    )
    parser.add_argument(
        "-wt",
        "--wall",
        action="store",
        type=float,
        default=1.0,
        help="Wall thickness (default=1 mm)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="step",
        help="Output file format (STEP, STL, SVG) default=STEP",
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
    height_u = argsd["height"]
    micro_divisions = argsd["micro"]
    solid_ratio = argsd["ratio"]
    length_div = argsd["lengthdiv"]
    width_div = argsd["widthdiv"]
    wall = argsd["wall"]

    # Validate fractional sizes align with micro_divisions
    step = 1.0 / micro_divisions
    for name, val in [("length", length_u), ("width", width_u)]:
        if abs(val / step - round(val / step)) > 1e-6:
            parser.error(f"{name}={val} must be a multiple of {step} when --micro={micro_divisions}")

    box = GridfinityBox(
        length_u=length_u,
        width_u=width_u,
        height_u=height_u,
        micro_divisions=micro_divisions,
        holes=argsd["magnetholes"] or argsd["unsupported"],
        unsupported_holes=argsd["unsupported"],
        no_lip=argsd["nolip"],
        scoops=argsd["scoops"],
        labels=argsd["labels"],
        lite_style=argsd["ecolite"],
        solid=argsd["solid"],
        solid_ratio=solid_ratio,
        length_div=length_div,
        width_div=width_div,
        wall_th=wall,
    )

    if argsd["ecolite"]:
        bs = "lite "
    elif argsd["solid"]:
        bs = "solid "
    else:
        bs = ""

    print(title)
    print("Version: %s" % (microfinity.__version__))

    # Format size string (show decimals only if fractional)
    def fmt_u(val):
        return f"{val:g}"

    size_str = f"{fmt_u(length_u)}U x {fmt_u(width_u)}U x {height_u}U"
    if micro_divisions > 1:
        size_str += f" (micro={micro_divisions})"

    print(
        "Gridfinity %sbox: %s (%.1f mm x %.1f mm x %.1f mm), %.2f mm walls"
        % (
            bs,
            size_str,
            box.length,
            box.width,
            box.height,
            box.wall_th,
        )
    )

    if argsd["solid"]:
        print(
            "  solid height ratio: %.2f  top height: %.2f mm / %.2f mm"
            % (solid_ratio, box.top_ref_height, box.max_height + GR_BOT_H)
        )

    s = []
    if argsd["unsupported"]:
        s.append("holes with no support")
    elif argsd["magnetholes"]:
        s.append("holes")
    if argsd["nolip"]:
        s.append("no lip")
    if argsd["scoops"]:
        s.append("scoops")
    if argsd["labels"]:
        s.append("label strips")
    if length_div:
        s.append("%d length-wise walls" % (length_div))
    if width_div:
        s.append("%d width-wise walls" % (width_div))
    if len(s):
        print("  with options: %s" % (", ".join(s)))

    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = box.filename()

    s = ["\nBox generated and saved as"]
    if argsd["format"].lower() == "stl" or fn.lower().endswith(".stl"):
        if not fn.endswith(".stl"):
            fn = fn + ".stl"
        box.save_stl_file(filename=argsd["output"])
        s.append("%s in STL format" % (fn))
    elif argsd["format"].lower() == "svg" or fn.lower().endswith(".svg"):
        if not fn.endswith(".svg"):
            fn = fn + ".svg"
        box.save_svg_file(filename=argsd["output"])
        s.append("%s in SVG format" % (fn))
    else:
        if not fn.endswith(".step"):
            fn = fn + ".step"
        box.save_step_file(filename=argsd["output"])
        s.append("%s in STEP format" % (fn))
    print(" ".join(s))


if __name__ == "__main__":
    main()
