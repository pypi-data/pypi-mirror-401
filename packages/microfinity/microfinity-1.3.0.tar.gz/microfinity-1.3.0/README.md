# Microfinity

[![PyPI](https://img.shields.io/pypi/v/microfinity.svg)](https://pypi.org/project/microfinity/)
![python version](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=blue&style=flat&logo=python)
[![CadQuery](https://img.shields.io/static/v1?label=dependencies&message=CadQuery%202.0%2B&color=blue&style=flat)](https://github.com/CadQuery/cadquery)
![license](https://img.shields.io/badge/license-MIT-blue.svg)

**Gridfinity-compatible storage system with optional sub-grid sizing for more granular bin dimensions.**

Microfinity extends the [Gridfinity](https://gridfinity.xyz) modular storage system with support for fractional grid units (0.25U and 0.5U increments), allowing you to create bins that better fit your specific items while remaining fully compatible with standard Gridfinity baseplates and bins.

## Key Features

- **100% Gridfinity Compatible** - All bins work on standard Gridfinity baseplates
- **Fractional Sizing** - Create bins in 0.25U (10.5mm) or 0.5U (21mm) increments
- **Automatic Drawer Layouts** - Generate optimally-segmented baseplates for any drawer size
- **Multi-Piece Baseplates** - Connection clips join pieces that exceed your build plate
- **Parametric Design** - Full control over holes, scoops, labels, dividers, and more
- **Multiple Export Formats** - STEP, STL, and SVG output

## Installation

```bash
pip install microfinity
```

Or install from source:

```bash
git clone https://github.com/nullstack65/microfinity.git
cd microfinity
pip install -e .
```

### Dependencies

- [CadQuery](https://github.com/CadQuery/cadquery) (>= 2.0)
- [cq-kit](https://github.com/michaelgale/cq-kit) (>= 0.5.6)

## Quick Start

### Create a Standard Box

```python
from microfinity import GridfinityBox

# 2x3x4 box with magnets, scoops, and labels
box = GridfinityBox(2, 3, 4, holes=True, scoops=True, labels=True)
box.save_stl_file()  # Saves: gf_box_2x3x4_holes_scoops_labels.stl
```

### Create a Fractional Box

```python
from microfinity import GridfinityBox

# 1.25U x 0.5U x 3U box - fits in tighter spaces
box = GridfinityBox(1.25, 0.5, 3, micro_divisions=4)
box.save_stl_file()  # Saves: gf_box_1.25x0.50x3_micro4.stl
```

### Create a Baseplate

```python
from microfinity import GridfinityBaseplate

# 4x3 baseplate with corner mounting screws
baseplate = GridfinityBaseplate(4, 3, corner_screws=True)
baseplate.save_stl_file()
```

### Generate a Drawer Layout

```python
from microfinity import GridfinityBaseplateLayout

# Automatically segment a drawer into printable pieces
layout = GridfinityBaseplateLayout(
    drawer_x_mm=450,
    drawer_y_mm=380,
    build_plate_x_mm=220,
    build_plate_y_mm=220,
)

layout.print_summary()  # Shows piece breakdown
layout.export_all("./drawer_plates", file_format="stl")
```

## CLI Commands

Generate models directly from the command line:

```bash
# Standard 2x3x5 box with magnet holes
microfinity-box 2 3 5 -m -f stl

# Fractional 1.25x2x3 box (quarter-grid)
microfinity-box 1.25 2 3 -f stl

# 6x4 baseplate with corner screws
microfinity-base 6 4 -s -f stl

# Generate drawer layout
microfinity-baseplate-layout -d 450 380 -b 220 220 -o ./drawer -f stl

# Generate calibration test prints
microfinity-calibrate -o ./calibration -f stl
```

## The Microgrid System

Standard Gridfinity uses a 42mm grid (1U). Microfinity adds support for smaller increments:

| micro_divisions | Pitch   | Increment | Use Case |
|-----------------|---------|-----------|----------|
| 1               | 42.0mm  | 1U        | Standard Gridfinity |
| 2               | 21.0mm  | 0.5U      | Half-grid sizing |
| 4               | 10.5mm  | 0.25U     | Quarter-grid sizing |

Fractional bins use smaller "micro-feet" that still index properly on standard baseplates:

```
Standard 1U bin:          Fractional 0.5U bin:
┌────────────────┐        ┌───────┐
│                │        │       │
│   Single 42mm  │        │ 21mm  │
│      foot      │        │ foot  │
│                │        │       │
└────────────────┘        └───────┘
```

See [The Microgrid System](docs/microgrid-system.md) for details.

## Documentation

- [Getting Started](docs/getting-started.md) - Installation and first steps
- [The Microgrid System](docs/microgrid-system.md) - How fractional sizing works
- **Components:**
  - [Boxes](docs/components/boxes.md) - GridfinityBox parameters and features
  - [Baseplates](docs/components/baseplates.md) - GridfinityBaseplate options
  - [Layouts](docs/components/layouts.md) - Automatic drawer tiling system
  - [Spacers](docs/components/spacers.md) - Drawer spacer generation
- [CLI Reference](docs/cli-reference.md) - Command line tools
- [Calibration](docs/calibration.md) - Test prints for tuning fit
- [Export Options](docs/export.md) - File formats and batch export
- [Python API](docs/python-api.md) - Programmatic usage

## Examples

See the [examples/](examples/) directory for complete scripts:

- `basic_box.py` - Simple box with common features
- `fractional_bins.py` - Various fractional sizes
- `drawer_layout.py` - Complete drawer layout workflow
- `custom_baseplate.py` - Baseplate with specific options
- `batch_export.py` - Generate families of parts

## Credits

Microfinity is a fork of [cq-gridfinity](https://github.com/michaelgale/cq-gridfinity) by Michael Gale. The Gridfinity system was created by [Zack Freedman](https://www.youtube.com/c/ZackFreedman).

## License

MIT License - See [LICENSE](LICENSE) for details.
