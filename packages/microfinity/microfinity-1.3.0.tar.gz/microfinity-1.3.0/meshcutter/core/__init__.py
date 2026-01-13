#! /usr/bin/env python3
#
# meshcutter.core - Core geometry operations
#

from meshcutter.core.detection import detect_bottom_frame, extract_footprint, detect_aligned_frame
from meshcutter.core.boolean import boolean_difference, repair_mesh
from meshcutter.core.foot_cutter import (
    generate_microgrid_cutter,
    generate_cell_cutter,
    detect_cell_centers,
    GRU,
)

__all__ = [
    "detect_bottom_frame",
    "extract_footprint",
    "detect_aligned_frame",
    "generate_microgrid_cutter",
    "generate_cell_cutter",
    "detect_cell_centers",
    "boolean_difference",
    "repair_mesh",
    "GRU",
]
