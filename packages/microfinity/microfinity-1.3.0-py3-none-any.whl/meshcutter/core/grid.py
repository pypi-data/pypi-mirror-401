#! /usr/bin/env python3
#
# meshcutter.core.grid - 2D grid mask generation using Shapely
#

from __future__ import annotations

from typing import List, Tuple, Union

import numpy as np
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely.validation import make_valid


# Gridfinity standard grid unit (42mm)
GRU = 42.0

# Default slot width derived from GR_STR_H (1.8mm straight section)
DEFAULT_SLOT_WIDTH = 1.8


def compute_grid_positions(
    bbox: Tuple[float, float, float, float],
    pitch: float,
    phase_x: float = 0.0,
    phase_y: float = 0.0,
) -> Tuple[List[float], List[float]]:
    """
    Compute X and Y positions for grid cuts.

    Grid lines are defined at positions:
        x = centroid_x + phase_x + k * pitch
        y = centroid_y + phase_y + k * pitch
    for integer k covering the bounding box.

    Args:
        bbox: (x_min, y_min, x_max, y_max) of footprint
        pitch: Grid spacing in mm (e.g., 42/4 = 10.5 for quarter-grid)
        phase_x: Offset from centroid-centered grid in X (mm)
        phase_y: Offset from centroid-centered grid in Y (mm)

    Returns:
        Tuple of (x_positions, y_positions) - lists of cut centerlines
    """
    x_min, y_min, x_max, y_max = bbox

    # Compute centroid
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0

    # Reference point for grid
    ref_x = cx + phase_x
    ref_y = cy + phase_y

    # Compute X positions
    # Find the range of k values needed to cover [x_min, x_max]
    k_min_x = int(np.floor((x_min - ref_x) / pitch))
    k_max_x = int(np.ceil((x_max - ref_x) / pitch))

    x_positions = []
    for k in range(k_min_x, k_max_x + 1):
        x = ref_x + k * pitch
        # Only include if it's within or near the bbox
        if x_min - pitch < x < x_max + pitch:
            x_positions.append(x)

    # Compute Y positions
    k_min_y = int(np.floor((y_min - ref_y) / pitch))
    k_max_y = int(np.ceil((y_max - ref_y) / pitch))

    y_positions = []
    for k in range(k_min_y, k_max_y + 1):
        y = ref_y + k * pitch
        if y_min - pitch < y < y_max + pitch:
            y_positions.append(y)

    return x_positions, y_positions


def generate_grid_mask(
    footprint: Union[Polygon, MultiPolygon],
    pitch: float,
    slot_width: float = DEFAULT_SLOT_WIDTH,
    clearance: float = 0.0,
    phase_x: float = 0.0,
    phase_y: float = 0.0,
    overshoot: float = 1.0,
    clip_to_footprint: bool = False,
) -> Union[Polygon, MultiPolygon]:
    """
    Generate 2D grid mask polygon for cutting.

    This function creates a 2D mask representing the grid of slots to be cut.
    By default, strips extend beyond the footprint bounding box by `overshoot`
    to ensure cuts go completely through each foot cell.

    Strategy:
        1. Compute grid positions covering footprint bbox
        2. Create X-strips (vertical) and Y-strips (horizontal) as rectangles
        3. Strips use: slot_width + 2*clearance as the effective width
        4. Union all strips (fast 2D operation via Shapely)
        5. Optionally clip to footprint (disabled by default for through-cuts)

    Args:
        footprint: Shapely Polygon/MultiPolygon of the bottom footprint
        pitch: Grid spacing in mm (42 / divisions)
        slot_width: Base width of cut slots in mm (default: 1.8)
        clearance: Additional clearance per side in mm (default: 0)
        phase_x: Grid phase offset in X (mm)
        phase_y: Grid phase offset in Y (mm)
        overshoot: How far strips extend beyond bbox (mm)
        clip_to_footprint: If True, clip mask to footprint boundary (legacy).
            If False (default), strips extend full length for through-cuts.

    Returns:
        Shapely Polygon or MultiPolygon representing the cut region

    Raises:
        ValueError: If result is empty (no intersection with footprint)
    """
    # Validate inputs
    if pitch <= 0:
        raise ValueError(f"pitch must be positive, got {pitch}")
    if slot_width <= 0:
        raise ValueError(f"slot_width must be positive, got {slot_width}")
    if clearance < 0:
        raise ValueError(f"clearance must be non-negative, got {clearance}")

    # Effective slot width includes clearance on both sides
    effective_width = slot_width + 2 * clearance

    # Get footprint bounding box
    bounds = footprint.bounds  # (minx, miny, maxx, maxy)
    x_min, y_min, x_max, y_max = bounds

    # Compute grid positions
    x_positions, y_positions = compute_grid_positions(
        bbox=bounds,
        pitch=pitch,
        phase_x=phase_x,
        phase_y=phase_y,
    )

    # Create strips
    strips = []
    half_width = effective_width / 2.0

    # X-strips (vertical, cutting in X direction)
    # These are rectangles spanning the full Y range
    for x in x_positions:
        strip = box(
            x - half_width,
            y_min - overshoot,
            x + half_width,
            y_max + overshoot,
        )
        strips.append(strip)

    # Y-strips (horizontal, cutting in Y direction)
    # These are rectangles spanning the full X range
    for y in y_positions:
        strip = box(
            x_min - overshoot,
            y - half_width,
            x_max + overshoot,
            y + half_width,
        )
        strips.append(strip)

    if not strips:
        raise ValueError(
            f"No grid strips generated. Footprint bounds: {bounds}, "
            f"pitch: {pitch}, positions: x={x_positions}, y={y_positions}"
        )

    # Union all strips (this is fast in 2D)
    grid_union = unary_union(strips)

    # Ensure validity
    if not grid_union.is_valid:
        grid_union = make_valid(grid_union)

    if clip_to_footprint:
        # Legacy behavior: clip to footprint polygon boundary
        result = footprint.intersection(grid_union)
    else:
        # Default: no clipping - strips extend full length for through-cuts
        # This ensures cuts go completely through each foot cell and past the model edge
        result = grid_union

    # Validate result
    if result.is_empty:
        raise ValueError(
            "Grid mask is empty after processing. "
            "Check that grid pitch and phase produce cuts that overlap the footprint."
        )

    # Ensure validity of result
    if not result.is_valid:
        result = make_valid(result)

    return result


def compute_pitch(divisions: int) -> float:
    """
    Compute grid pitch from number of divisions.

    Args:
        divisions: Number of divisions per grid unit (1, 2, or 4)

    Returns:
        Pitch in mm (42.0, 21.0, or 10.5)

    Raises:
        ValueError: If divisions is not 1, 2, or 4
    """
    if divisions not in (1, 2, 4):
        raise ValueError(f"divisions must be 1, 2, or 4, got {divisions}")
    return GRU / divisions


def get_grid_info(
    footprint: Union[Polygon, MultiPolygon],
    pitch: float,
    phase_x: float = 0.0,
    phase_y: float = 0.0,
) -> dict:
    """
    Get information about the grid that would be generated.

    Useful for debugging and verbose output.

    Args:
        footprint: Shapely Polygon/MultiPolygon of the bottom footprint
        pitch: Grid spacing in mm
        phase_x: Grid phase offset in X (mm)
        phase_y: Grid phase offset in Y (mm)

    Returns:
        Dictionary with grid info
    """
    bounds = footprint.bounds
    x_positions, y_positions = compute_grid_positions(
        bbox=bounds,
        pitch=pitch,
        phase_x=phase_x,
        phase_y=phase_y,
    )

    cx = (bounds[0] + bounds[2]) / 2.0
    cy = (bounds[1] + bounds[3]) / 2.0

    return {
        "footprint_bounds": bounds,
        "footprint_area": footprint.area,
        "footprint_centroid": (cx, cy),
        "pitch": pitch,
        "phase": (phase_x, phase_y),
        "grid_reference": (cx + phase_x, cy + phase_y),
        "x_cut_positions": x_positions,
        "y_cut_positions": y_positions,
        "num_x_cuts": len(x_positions),
        "num_y_cuts": len(y_positions),
        "total_cuts": len(x_positions) + len(y_positions),
    }
