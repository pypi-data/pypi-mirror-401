#! /usr/bin/env python3
#
# meshcutter - Gridfinity mesh profile cutter
#
# Cut gridfinity micro-division profiles into existing STL/3MF models
# using mesh boolean operations.
#
# Part of the microfinity package - shares version with microfinity.
#

from microfinity import __version__

from meshcutter.core.detection import detect_bottom_frame, extract_footprint
from meshcutter.core.grid import generate_grid_mask, compute_grid_positions
from meshcutter.core.cutter import generate_cutter
from meshcutter.core.boolean import boolean_difference, repair_mesh
from meshcutter.io.loader import load_mesh
from meshcutter.io.exporter import export_stl

__all__ = [
    "__version__",
    "detect_bottom_frame",
    "extract_footprint",
    "generate_grid_mask",
    "compute_grid_positions",
    "generate_cutter",
    "boolean_difference",
    "repair_mesh",
    "load_mesh",
    "export_stl",
]
