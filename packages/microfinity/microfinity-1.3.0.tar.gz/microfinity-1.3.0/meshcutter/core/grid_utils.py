#! /usr/bin/env python3
#
# meshcutter.core.grid_utils - Grid and micro-foot offset calculations
#
# This module provides utilities for calculating micro-foot positions
# and detecting cell centers from footprints.

from __future__ import annotations

from typing import List, Optional, Tuple, Union

import numpy as np
from shapely.geometry import Polygon, MultiPolygon

from meshcutter.core.constants import GRU, GR_TOL


# -----------------------------------------------------------------------------
# Micro-foot offset calculations
# -----------------------------------------------------------------------------


def micro_foot_offsets_single_cell(
    micro_divisions: int = 4,
    pitch: float = GRU,
) -> List[Tuple[float, float]]:
    """Return micro-foot center offsets relative to 1U cell center.

    For micro_divisions=4, pitch=42:
    - micro_pitch = 10.5
    - offsets at: [-15.75, -5.25, 5.25, 15.75] in each axis
    - 16 micro-feet total per cell

    Args:
        micro_divisions: Number of divisions (2 or 4)
        pitch: 1U pitch (default 42mm)

    Returns:
        List of (x, y) offsets relative to cell center
    """
    if micro_divisions <= 1:
        return [(0.0, 0.0)]  # Single foot at center

    micro_pitch = pitch / micro_divisions
    offsets = []
    for i in range(micro_divisions):
        for j in range(micro_divisions):
            x = (i - (micro_divisions - 1) / 2.0) * micro_pitch
            y = (j - (micro_divisions - 1) / 2.0) * micro_pitch
            offsets.append((x, y))
    return offsets


def micro_foot_offsets_grid(
    cells_x: int,
    cells_y: int,
    micro_divisions: int = 4,
    pitch: float = GRU,
) -> List[Tuple[float, float]]:
    """Return micro-foot center offsets for a grid of cells.

    Matches microfinity's micro_grid_centres calculation exactly.
    The returned offsets are centered at (0, 0) for the grid center.

    Args:
        cells_x: Number of 1U cells in X direction
        cells_y: Number of 1U cells in Y direction
        micro_divisions: Number of divisions per 1U (2 or 4)
        pitch: 1U pitch (42mm)

    Returns:
        List of (x, y) offsets for micro-foot centers, centered at origin
    """
    if micro_divisions <= 1:
        # Standard 1U grid
        half_l = (cells_x - 1) * pitch / 2
        half_w = (cells_y - 1) * pitch / 2
        return [(x * pitch - half_l, y * pitch - half_w) for x in range(cells_x) for y in range(cells_y)]

    micro_pitch = pitch / micro_divisions
    micro_count_x = cells_x * micro_divisions
    micro_count_y = cells_y * micro_divisions

    # Half extents (distance from center to edge foot centers)
    micro_half_l = (micro_count_x - 1) * micro_pitch / 2
    micro_half_w = (micro_count_y - 1) * micro_pitch / 2

    offsets = [
        (x * micro_pitch - micro_half_l, y * micro_pitch - micro_half_w)
        for x in range(micro_count_x)
        for y in range(micro_count_y)
    ]
    return offsets


# -----------------------------------------------------------------------------
# Cell center detection
# -----------------------------------------------------------------------------


def detect_cell_centers(
    footprint: Union[Polygon, MultiPolygon],
    pitch: float = GRU,
    mesh_bounds: Optional[np.ndarray] = None,
) -> List[Tuple[float, float]]:
    """Detect 1U cell centers from footprint, optionally using mesh bounds for sizing.

    For Gridfinity models, the footprint detected at Z=0 may be smaller than
    the actual foot base due to chamfers. If mesh_bounds is provided, we use
    the XY extent of the mesh bounds for calculating the number of cells.

    The returned centers are in LOCAL FRAME coordinates (same as footprint).
    The center position comes from the footprint (which is in local coords), while
    the dimensions can come from mesh_bounds (for accurate cell count).

    Args:
        footprint: Shapely polygon of bottom footprint (LOCAL frame coordinates)
        pitch: 1U pitch (default 42mm)
        mesh_bounds: Optional mesh bounds array [[minx,miny,minz], [maxx,maxy,maxz]]
                     in WORLD coordinates. Used only for determining cell count,
                     not for center positioning.

    Returns:
        List of (x, y) cell center coordinates in LOCAL frame
    """
    # Always use footprint center (local frame coordinates)
    fp_bounds = footprint.bounds
    cx = (fp_bounds[0] + fp_bounds[2]) / 2.0
    cy = (fp_bounds[1] + fp_bounds[3]) / 2.0

    if mesh_bounds is not None:
        # Use mesh bounds for dimensions (captures full foot size)
        width = mesh_bounds[1, 0] - mesh_bounds[0, 0]
        height = mesh_bounds[1, 1] - mesh_bounds[0, 1]
    else:
        # Use footprint bounds for dimensions
        width = fp_bounds[2] - fp_bounds[0]
        height = fp_bounds[3] - fp_bounds[1]

    # Gridfinity convention: overall_dim ≈ N * pitch - GR_TOL
    cells_x = int(round((width + GR_TOL) / pitch))
    cells_y = int(round((height + GR_TOL) / pitch))

    # Ensure at least 1 cell in each dimension
    cells_x = max(1, cells_x)
    cells_y = max(1, cells_y)

    centers = []
    for i in range(cells_x):
        for j in range(cells_y):
            x = cx + (i - (cells_x - 1) / 2.0) * pitch
            y = cy + (j - (cells_y - 1) / 2.0) * pitch
            centers.append((x, y))

    return centers


def detect_grid_size(
    mesh_bounds: np.ndarray,
    pitch: float = GRU,
) -> Tuple[int, int]:
    """Detect the grid size (cells_x, cells_y) from mesh bounds.

    Args:
        mesh_bounds: Mesh bounds array [[minx,miny,minz], [maxx,maxy,maxz]]
        pitch: 1U pitch (default 42mm)

    Returns:
        Tuple of (cells_x, cells_y)
    """
    width = mesh_bounds[1, 0] - mesh_bounds[0, 0]
    height = mesh_bounds[1, 1] - mesh_bounds[0, 1]

    # Gridfinity convention: overall_dim ≈ N * pitch - GR_TOL
    cells_x = int(round((width + GR_TOL) / pitch))
    cells_y = int(round((height + GR_TOL) / pitch))

    return max(1, cells_x), max(1, cells_y)


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def quantize(v: float, precision: float = 0.1) -> float:
    """Quantize a value to a given precision.

    Useful for snapping coordinates to grid positions.

    Args:
        v: Value to quantize
        precision: Precision to round to

    Returns:
        Quantized value
    """
    return round(v / precision) * precision
