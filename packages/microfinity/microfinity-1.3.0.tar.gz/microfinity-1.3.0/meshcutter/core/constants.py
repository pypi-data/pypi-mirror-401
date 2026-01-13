#! /usr/bin/env python3
#
# meshcutter.core.constants - Centralized Gridfinity constants
#
# Re-exports constants from microfinity.core.constants for consistency,
# plus meshcutter-specific constants for the replace-base pipeline.

from __future__ import annotations

# Re-export Gridfinity constants from microfinity
from microfinity.core.constants import (
    GRU,  # 42.0 - 1U pitch (mm)
    GR_TOL,  # 0.5 - Clearance between feet (mm)
    GR_RAD,  # 4.0 - Nominal exterior fillet radius (mm)
    GR_BASE_HEIGHT,  # 4.75 - Foot height (mm)
    GR_BASE_CLR,  # 0.25 - Clearance above foot (mm)
    GR_BOX_PROFILE,  # Profile segments for box foot
    GR_BOX_CHAMF_H,  # 0.8 - Bottom chamfer height
    GR_STR_H,  # 1.8 - Straight section height
    SQRT2,  # sqrt(2) for 45-degree calculations
)

# -----------------------------------------------------------------------------
# Meshcutter-specific constants
# -----------------------------------------------------------------------------

# Z_SPLIT_HEIGHT is the plane where we cut between top (kept) and base (replaced)
# z_split = z_min + GR_BASE_HEIGHT + GR_BASE_CLR = z_min + 5.0mm
Z_SPLIT_HEIGHT: float = GR_BASE_HEIGHT + GR_BASE_CLR  # 4.75 + 0.25 = 5.0mm

# SLEEVE_HEIGHT - how far the new base extends ABOVE z_split for overlap
# This is critical: overlap ensures robust union (no coplanar faces)
SLEEVE_HEIGHT: float = 0.5  # mm

# COPLANAR_EPSILON - offset to avoid coplanar geometry issues in booleans
COPLANAR_EPSILON: float = 0.02  # mm

# Mesh cleanup thresholds
MIN_COMPONENT_FACES: int = 100  # Minimum faces to keep a component
MIN_SLIVER_SIZE: float = 0.001  # 1 µm - any dimension smaller is suspicious
MIN_SLIVER_VOLUME: float = 1e-12  # mm³ - volumes below this are effectively zero

# Golden test acceptance threshold
MAX_VOLUME_DIFF_MM3: float = 1.0  # Maximum acceptable difference in mm³
