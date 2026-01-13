#! /usr/bin/env python3
#
# meshcutter.core.cq_cutter - CadQuery-based Gridfinity micro-foot cutter generation
#
# Generates cutter geometry using CadQuery for proper 45-degree chamfers,
# exactly mirroring microfinity's foot construction for geometric accuracy.
#

from __future__ import annotations

import math
import os
import tempfile
from functools import lru_cache
from typing import List, Optional, Tuple

import cadquery as cq
import trimesh
from cqkit.cq_helpers import rounded_rect_sketch

from microfinity.core.constants import (
    GR_BASE_CLR,
    GR_BASE_HEIGHT,
    GR_BOX_PROFILE,
    GR_RAD,
    GR_TOL,
    GRU,
    SQRT2,
)

# -----------------------------------------------------------------------------
# CadQuery version detection for ZLEN_FIX (copied from microfinity.core.base)
# CQ versions < 2.4.0 typically require zlen correction for tapered extrusions
# -----------------------------------------------------------------------------
ZLEN_FIX = True
_r = cq.Workplane("XY").rect(2, 2).extrude(1, taper=45)
_bb = _r.vals()[0].BoundingBox()
if abs(_bb.zlen - 1.0) < 1e-3:
    ZLEN_FIX = False


# -----------------------------------------------------------------------------
# Extrude profile helper (mirrors microfinity.core.base.GridfinityObject.extrude_profile)
# -----------------------------------------------------------------------------
def extrude_profile(sketch, profile, workplane="XY", angle=None) -> cq.Workplane:
    """Extrude a sketch through a multi-segment profile with optional tapers.

    This is a standalone version of GridfinityObject.extrude_profile() to avoid
    needing to instantiate a full GridfinityObject just for profile extrusion.

    Args:
        sketch: CadQuery Sketch to extrude
        profile: Tuple of profile segments. Each segment is either:
                 - A float (straight extrusion height)
                 - A tuple (height, taper_angle) for tapered extrusion
        workplane: Workplane to start from (default "XY")
        angle: If provided, use angle-based ZLEN correction instead of SQRT2

    Returns:
        CadQuery Workplane with extruded solid
    """
    taper = profile[0][1] if isinstance(profile[0], (list, tuple)) else 0
    zlen = profile[0][0] if isinstance(profile[0], (list, tuple)) else profile[0]

    if abs(taper) > 0:
        if angle is None:
            zlen = zlen if ZLEN_FIX else zlen / SQRT2
        else:
            zlen = zlen / math.cos(math.radians(taper)) if ZLEN_FIX else zlen

    r = cq.Workplane(workplane).placeSketch(sketch).extrude(zlen, taper=taper)

    for level in profile[1:]:
        if isinstance(level, (tuple, list)):
            if angle is None:
                zlen = level[0] if ZLEN_FIX else level[0] / SQRT2
            else:
                zlen = level[0] / math.cos(math.radians(level[1])) if ZLEN_FIX else level[0]
            r = r.faces(">Z").wires().toPending().extrude(zlen, taper=level[1])
        else:
            r = r.faces(">Z").wires().toPending().extrude(level)

    return r


# -----------------------------------------------------------------------------
# Geometry constants (derived from microfinity conventions)
# -----------------------------------------------------------------------------
def get_outer_rad() -> float:
    """Get the outer corner radius used for foot solids.

    From microfinity: outer_rad = GR_RAD - GR_TOL / 2
    """
    return GR_RAD - GR_TOL / 2  # 4.0 - 0.25 = 3.75mm


def get_foot_rad() -> float:
    """Get the corner radius for foot profile extrusion.

    From microfinity: rad = outer_rad + GR_BASE_CLR
    """
    return get_outer_rad() + GR_BASE_CLR  # 3.75 + 0.25 = 4.0mm


def _top_chamfer_run() -> float:
    """Get the horizontal/vertical run of the top 45° chamfer (mm).

    The top chamfer is a 45° slope, so its horizontal run equals its vertical run.
    This is used to calculate the width needed for inter-cell channels and
    boundary fill to fully cover the chamfer seam between adjacent feet.

    Returns:
        Chamfer run in mm (~2.4mm for standard Gridfinity)
    """
    # Try to use GR_BOX_TOP_CHAMF if available (this is the vertical height)
    try:
        from microfinity.core.constants import GR_BOX_TOP_CHAMF

        return float(GR_BOX_TOP_CHAMF)
    except ImportError:
        pass

    # Fallback: compute from GR_BOX_PROFILE[0] = (diagonal_length, angle_deg)
    # The profile stores (length_along_slope, angle) where length is diagonal
    # For a 45° chamfer: vertical_run = diagonal_length * sin(45°) = diagonal / sqrt(2)
    chamfer_segment = GR_BOX_PROFILE[0]
    if isinstance(chamfer_segment, (tuple, list)) and len(chamfer_segment) >= 2:
        diagonal_len, angle_deg = chamfer_segment[0], chamfer_segment[1]
        return float(diagonal_len) * math.sin(math.radians(float(angle_deg)))

    # Ultimate fallback: use known value for standard Gridfinity
    return 2.4


# -----------------------------------------------------------------------------
# Foot generation (mirrors microfinity/parts/box.py)
# -----------------------------------------------------------------------------
def generate_1u_foot_cq(cropped: bool = True) -> cq.Workplane:
    """Generate a 1U foot solid using CadQuery.

    Mirrors microfinity box.py render_shell() for macro feet.

    In box.py, the foot is generated at GRU (42mm) then intersected with
    an outer envelope at (GRU - GR_TOL) = 41.5mm with radius (GR_RAD - GR_TOL/2).
    We replicate this by generating the raw foot then intersecting with the
    same cropping envelope.

    Args:
        cropped: If True (default), apply envelope cropping to match actual model.
                 If False, return raw 42mm foot.

    Returns:
        CadQuery Workplane with 1U foot solid
    """
    rad = get_foot_rad()  # 4.0mm

    # Generate raw foot at GRU (42mm) - same as box.py render_shell()
    foot = extrude_profile(rounded_rect_sketch(GRU, GRU, rad), GR_BOX_PROFILE)
    foot = foot.translate((0, 0, -GR_BASE_CLR))
    foot = foot.mirror(mirrorPlane="XY")

    if cropped:
        # Apply the same cropping envelope as box.py
        # rc = cq.Workplane("XY").placeSketch(rs).extrude(-GR_BASE_HEIGHT - 1).translate((*self.half_dim, 0.5))
        outer_size = GRU - GR_TOL  # 41.5mm
        outer_rad = get_outer_rad()  # 3.75mm
        crop_env = (
            cq.Workplane("XY")
            .placeSketch(rounded_rect_sketch(outer_size, outer_size, outer_rad))
            .extrude(-GR_BASE_HEIGHT - 1)
            .translate(cq.Vector(0, 0, 0.5))
        )
        foot = crop_env.intersect(foot)

    return foot


def generate_micro_foot_cq(
    micro_divisions: int = 4,
    size_reduction: float = 0.0,
) -> cq.Workplane:
    """Generate a micro foot solid using CadQuery.

    Creates a micro-foot with the correct dimensions to match microfinity output.
    The foot size is (micro_pitch - GR_TOL) to account for the 0.5mm clearance
    between adjacent feet. For div=4, this gives 10.0mm feet with 0.5mm gaps.

    Args:
        micro_divisions: Number of divisions (2 or 4)
        size_reduction: Amount to shrink the foot size (mm). Used for cutter
                       generation where smaller micro-feet create a gap that
                       allows cutting the outer wall.

    Returns:
        CadQuery Workplane with micro foot solid
    """
    outer_rad = get_outer_rad()  # 3.75mm
    rad_1u = outer_rad + GR_BASE_CLR  # 4.0mm

    micro_pitch = GRU / micro_divisions  # 10.5mm for div=4
    # Foot size = micro_pitch - GR_TOL to match actual foot dimensions
    # This gives 10.0mm feet for div=4 (10.5 - 0.5), matching microfinity output
    foot_size = micro_pitch - GR_TOL - size_reduction  # 10.0mm for div=4

    # Ensure minimum viable size
    foot_size = max(foot_size, 2.0)

    # Clamp radius to valid range (must fit in foot)
    rad = min(rad_1u, foot_size / 2 - 0.05)
    rad = max(rad, 0.2)  # Minimum to avoid degenerate geometry

    foot = extrude_profile(rounded_rect_sketch(foot_size, foot_size, rad), GR_BOX_PROFILE)
    foot = foot.translate((0, 0, -GR_BASE_CLR))
    foot = foot.mirror(mirrorPlane="XY")

    return foot


def micro_foot_offsets(micro_divisions: int, pitch: float = GRU) -> List[Tuple[float, float]]:
    """Return micro-foot center offsets relative to 1U cell center.

    This matches the microfinity reference implementation exactly:
    - Foot centers are symmetric about the origin
    - Outermost feet extend GR_TOL/2 PAST the envelope edge (then get cropped)
    - This is identical to how 1U feet (at 42mm) get cropped by the 41.5mm envelope

    For micro_divisions=4, pitch=42:
    - micro_pitch = 10.5mm
    - foot_size = 10.5mm (same as micro_pitch)
    - Centers at: ±15.75, ±5.25 (matching reference micro_grid_centres)
    - Outermost foot edge at ±21.0, cropped by envelope to ±20.75

    The key insight: feet should extend PAST the envelope by GR_TOL/2 so that
    the envelope intersection crops them, producing the correct chamfer profile
    at the boundary (same mechanism as 1U feet).

    Args:
        micro_divisions: Number of divisions (1, 2, or 4)
        pitch: 1U pitch (default 42mm)

    Returns:
        List of (x, y) offset tuples
    """
    if micro_divisions <= 1:
        return [(0.0, 0.0)]

    micro_pitch = pitch / micro_divisions  # 10.5mm for div=4

    # Simple symmetric formula matching microfinity's micro_grid_centres
    # NO inward shift - feet extend past envelope and get cropped
    #
    # For div=4: centers at (micro_pitch/2) * [-3, -1, 1, 3] = [-15.75, -5.25, 5.25, 15.75]
    # This puts outermost foot edges at ±21.0, which get cropped to ±20.75 by envelope
    offsets = []
    for i in range(micro_divisions):
        for j in range(micro_divisions):
            x = (micro_pitch / 2) * (2 * i - (micro_divisions - 1))
            y = (micro_pitch / 2) * (2 * j - (micro_divisions - 1))
            offsets.append((x, y))
    return offsets


# -----------------------------------------------------------------------------
# Cell cutter generation
# -----------------------------------------------------------------------------
@lru_cache(maxsize=8)
def generate_extended_foot_cq(overshoot: float = 0.0, cropped: bool = True) -> cq.Workplane:
    """Generate an extended 1U foot solid for cutter envelope.

    This creates a foot that extends beyond the normal 1U foot boundary
    by the overshoot amount on all sides. Used for generating cutters
    that extend beyond the foot boundary to cut outer walls.

    Args:
        overshoot: Extension beyond normal foot size (mm)
        cropped: If True (default), apply envelope cropping to match actual model.

    Returns:
        CadQuery Workplane with extended foot solid
    """
    rad = get_foot_rad()  # 4.0mm
    size = GRU + 2 * overshoot  # Extend in both directions from raw 42mm

    foot = extrude_profile(
        rounded_rect_sketch(size, size, rad),
        GR_BOX_PROFILE,
    )
    foot = foot.translate((0, 0, -GR_BASE_CLR))
    foot = foot.mirror(mirrorPlane="XY")

    if cropped:
        # Apply cropping envelope extended by overshoot
        outer_size = GRU - GR_TOL + 2 * overshoot  # 41.5mm + overshoot
        outer_rad = get_outer_rad()  # 3.75mm
        crop_env = (
            cq.Workplane("XY")
            .placeSketch(rounded_rect_sketch(outer_size, outer_size, outer_rad))
            .extrude(-GR_BASE_HEIGHT - 1)
            .translate(cq.Vector(0, 0, 0.5))
        )
        foot = crop_env.intersect(foot)

    return foot


@lru_cache(maxsize=32)
def generate_cell_cutter_cq(
    micro_divisions: int = 4,
    epsilon: float = 0.02,
    overshoot: float = 0.0,
    wall_cut: float = 0.0,
) -> cq.Workplane:
    """Generate cutter for a single 1U cell using CadQuery.

    The cutter is computed as: C = Envelope - union(micro_feet)
    where Envelope is the 1U foot (optionally extended) and micro_feet are smaller.

    The overshoot parameter extends the cutter beyond the normal F1 boundary,
    allowing it to cut the outer walls of edge cells where the micro-foot gaps
    should extend beyond the 1U foot profile.

    The wall_cut parameter shrinks the micro-feet used in the cutter calculation,
    creating cutter material that extends INTO the model at the outer edge. This
    allows the cutter to cut through the outer wall of the foot.

    This is done entirely in CadQuery (B-rep booleans) for stability,
    including the epsilon extension below z=0.

    Args:
        micro_divisions: Number of divisions (2 or 4)
        epsilon: Extension below z=0 to avoid coplanar issues (mm)
        overshoot: Extension beyond normal F1 size to cut outer walls (mm).
                   Default 0.0 = no extension (cutter stays within F1).
                   Typical value: 1.0-2.0mm for cutting outer walls.
        wall_cut: Amount to shrink micro-feet in cutter, creating overlap with
                  model outer wall (mm). Set to 0.5-1.0 to cut outer walls.
                  Default 0.0 = no shrinkage.

    Returns:
        CadQuery Workplane with cell cutter solid
    """
    if micro_divisions <= 1:
        raise ValueError("micro_divisions must be > 1 for cutter generation")

    # Generate the envelope (F1 foot, optionally extended)
    # Use cropped=True to match the actual model's 41.5mm cropped foot.
    # The cutter must match the model's F1 exactly so the chamfer profiles align.
    # Using uncropped (42mm) would leave 0.25mm of F1 chamfer uncut at the edges.
    if overshoot > 0:
        envelope = generate_extended_foot_cq(overshoot, cropped=True)
    else:
        envelope = generate_1u_foot_cq(cropped=True)
    envelope_solid = envelope.val()

    # Generate micro foot template (optionally shrunk for wall cutting)
    micro_foot = generate_micro_foot_cq(micro_divisions, size_reduction=wall_cut)
    micro_foot_solid = micro_foot.val()

    # Union all micro feet at their offset positions
    # Using OCC Shape operations (.fuse/.cut) for consistency
    offsets = micro_foot_offsets(micro_divisions)
    micro_feet_union = None

    for ox, oy in offsets:
        instance = micro_foot_solid.translate(cq.Vector(ox, oy, 0))
        if micro_feet_union is None:
            micro_feet_union = instance
        else:
            micro_feet_union = micro_feet_union.fuse(instance)

    # Cutter = envelope - union of micro feet
    cutter_solid = envelope_solid.cut(micro_feet_union)

    # NOTE: epsilon extension is now applied as a pure affine transform in
    # generate_grid_cutter_mesh() via apply_bottom_epsilon_preserve_top().
    # The previous approach (fusing a box) created internal coincident faces
    # that caused "stacked Z sheets" and boolean artifacts.

    return cq.Workplane("XY").newObject([cutter_solid])


# -----------------------------------------------------------------------------
# Corner plug generation for 4-cell meeting points
# -----------------------------------------------------------------------------
def detect_four_cell_intersections(
    cell_centers: List[Tuple[float, float]],
    pitch: float = GRU,
) -> List[Tuple[float, float]]:
    """Detect points where exactly 4 cells meet.

    A 4-cell intersection exists at (xb, yb) if and only if all four adjacent
    cells exist: (x_left, y_down), (x_left, y_up), (x_right, y_down), (x_right, y_up)

    This is robust for arbitrary grids including ragged/non-rectangular layouts.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        pitch: 1U pitch (default 42mm)

    Returns:
        List of (x, y) coordinates where 4 cells meet
    """
    if len(cell_centers) < 4:
        return []

    # Create a set for fast lookup (quantize to avoid float comparison issues)
    def quantize(v: float, precision: float = 0.1) -> float:
        return round(v / precision) * precision

    cell_set = {(quantize(cx), quantize(cy)) for cx, cy in cell_centers}

    # Find unique X and Y coordinates
    xs = sorted(set(quantize(cx) for cx, cy in cell_centers))
    ys = sorted(set(quantize(cy) for cx, cy in cell_centers))

    # Find all valid 4-cell intersections
    intersections = []

    for i in range(len(xs) - 1):
        x_left = xs[i]
        x_right = xs[i + 1]
        x_boundary = (x_left + x_right) / 2.0

        for j in range(len(ys) - 1):
            y_down = ys[j]
            y_up = ys[j + 1]
            y_boundary = (y_down + y_up) / 2.0

            # Check if all 4 adjacent cells exist
            has_all_four = (
                (quantize(x_left), quantize(y_down)) in cell_set
                and (quantize(x_left), quantize(y_up)) in cell_set
                and (quantize(x_right), quantize(y_down)) in cell_set
                and (quantize(x_right), quantize(y_up)) in cell_set
            )

            if has_all_four:
                intersections.append((x_boundary, y_boundary))

    return intersections


def detect_seam_network(
    cell_centers: List[Tuple[float, float]],
    pitch: float = GRU,
    footprint_bounds: Optional[Tuple[float, float, float, float]] = None,
) -> List[Tuple[float, float, List[str]]]:
    """Detect all seam nodes in the inter-cell channel network.

    A seam node is any point where channels meet or terminate. This includes:
    - Degree 4: Internal 4-cell crossings (4 incident channels)
    - Degree 3: T-junctions at boundaries or cutouts (3 incident channels)
    - Degree 2: Edge terminations where channels meet boundary (2 incident channels)

    Each node is returned with its incident channel directions.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        pitch: 1U pitch (default 42mm)
        footprint_bounds: Optional (x_min, y_min, x_max, y_max) clipping bounds

    Returns:
        List of (node_x, node_y, incident_directions) tuples where
        incident_directions is a list of 'N', 'S', 'E', 'W' indicating
        which channel directions are present at this node.
    """
    if len(cell_centers) < 2:
        return []

    # Quantize for float comparison
    def quantize(v: float, precision: float = 0.1) -> float:
        return round(v / precision) * precision

    cell_set = {(quantize(cx), quantize(cy)) for cx, cy in cell_centers}

    # Find unique X and Y coordinates (grid lines)
    xs = sorted(set(quantize(cx) for cx, cy in cell_centers))
    ys = sorted(set(quantize(cy) for cx, cy in cell_centers))

    # Channel seam locations:
    # - Vertical seams (between X columns): at X = (xs[i] + xs[i+1]) / 2
    # - Horizontal seams (between Y rows): at Y = (ys[j] + ys[j+1]) / 2
    x_seams = [(xs[i] + xs[i + 1]) / 2.0 for i in range(len(xs) - 1)]
    y_seams = [(ys[j] + ys[j + 1]) / 2.0 for j in range(len(ys) - 1)]

    seam_nodes = []

    # Internal nodes: where vertical and horizontal seams cross
    for x_seam in x_seams:
        for y_seam in y_seams:
            # Check which cells exist around this crossing
            # A channel exists in a direction if both cells along it exist

            # Find the two X columns this seam is between
            x_left = None
            x_right = None
            for i in range(len(xs) - 1):
                if abs((xs[i] + xs[i + 1]) / 2.0 - x_seam) < 0.01:
                    x_left = xs[i]
                    x_right = xs[i + 1]
                    break

            # Find the two Y rows this seam is between
            y_down = None
            y_up = None
            for j in range(len(ys) - 1):
                if abs((ys[j] + ys[j + 1]) / 2.0 - y_seam) < 0.01:
                    y_down = ys[j]
                    y_up = ys[j + 1]
                    break

            if x_left is None or y_down is None:
                continue

            # Determine incident directions based on adjacent cell existence
            incident = []

            # North: vertical channel continues north if cells at (x_left, y_up) and (x_right, y_up) exist
            if (quantize(x_left), quantize(y_up)) in cell_set and (quantize(x_right), quantize(y_up)) in cell_set:
                incident.append("N")

            # South: vertical channel continues south if cells at (x_left, y_down) and (x_right, y_down) exist
            if (quantize(x_left), quantize(y_down)) in cell_set and (quantize(x_right), quantize(y_down)) in cell_set:
                incident.append("S")

            # East: horizontal channel continues east if cells at (x_right, y_up) and (x_right, y_down) exist
            if (quantize(x_right), quantize(y_up)) in cell_set and (quantize(x_right), quantize(y_down)) in cell_set:
                incident.append("E")

            # West: horizontal channel continues west if cells at (x_left, y_up) and (x_left, y_down) exist
            if (quantize(x_left), quantize(y_up)) in cell_set and (quantize(x_left), quantize(y_down)) in cell_set:
                incident.append("W")

            if len(incident) >= 2:  # Only nodes with at least 2 incident channels
                seam_nodes.append((x_seam, y_seam, incident))

    # Boundary nodes: where channels meet the outer edge of the footprint
    if footprint_bounds is not None:
        fb_xmin, fb_ymin, fb_xmax, fb_ymax = footprint_bounds

        # Vertical channels at X seams meeting Y boundaries
        for x_seam in x_seams:
            # Find which Y rows have cells on both sides of this X seam
            for j in range(len(ys)):
                y_row = ys[j]
                # Check if cells on both sides of x_seam at this y_row
                x_left = None
                x_right = None
                for i in range(len(xs) - 1):
                    if abs((xs[i] + xs[i + 1]) / 2.0 - x_seam) < 0.01:
                        x_left = xs[i]
                        x_right = xs[i + 1]
                        break
                if x_left is None:
                    continue

                has_left = (quantize(x_left), quantize(y_row)) in cell_set
                has_right = (quantize(x_right), quantize(y_row)) in cell_set

                if has_left and has_right:
                    # Channel exists at this x_seam, y_row
                    # Check if this is at a Y boundary
                    if j == 0:
                        # Bottom boundary
                        y_node = y_row - pitch / 2.0
                        if y_node >= fb_ymin - 1:
                            seam_nodes.append((x_seam, y_node, ["N"]))
                    if j == len(ys) - 1:
                        # Top boundary
                        y_node = y_row + pitch / 2.0
                        if y_node <= fb_ymax + 1:
                            seam_nodes.append((x_seam, y_node, ["S"]))

        # Horizontal channels at Y seams meeting X boundaries
        for y_seam in y_seams:
            # Find which X columns have cells on both sides of this Y seam
            for i in range(len(xs)):
                x_col = xs[i]
                y_down = None
                y_up = None
                for j in range(len(ys) - 1):
                    if abs((ys[j] + ys[j + 1]) / 2.0 - y_seam) < 0.01:
                        y_down = ys[j]
                        y_up = ys[j + 1]
                        break
                if y_down is None:
                    continue

                has_down = (quantize(x_col), quantize(y_down)) in cell_set
                has_up = (quantize(x_col), quantize(y_up)) in cell_set

                if has_down and has_up:
                    # Channel exists at this x_col, y_seam
                    # Check if this is at an X boundary
                    if i == 0:
                        # Left boundary
                        x_node = x_col - pitch / 2.0
                        if x_node >= fb_xmin - 1:
                            seam_nodes.append((x_node, y_seam, ["E"]))
                    if i == len(xs) - 1:
                        # Right boundary
                        x_node = x_col + pitch / 2.0
                        if x_node <= fb_xmax + 1:
                            seam_nodes.append((x_node, y_seam, ["W"]))

    return seam_nodes


def generate_junction_correction(
    node_x: float,
    node_y: float,
    incident_directions: List[str],
    z0: float,
    z1: float,
    z2: float,
    z3: float,
    top_chamf_vert: float,
    bot_chamf_vert: float,
    micro_pitch: float = None,
    n_arc_points: int = 12,
) -> Optional[cq.Workplane]:
    """DEPRECATED: Generate correction geometry at a seam junction node.

    WARNING: This function is DEPRECATED and NOT USED in production.

    This was an attempt to patch junction artifacts in the boolean subtraction
    approach. It fundamentally doesn't work because adding geometry still goes
    through the same mesh boolean pipeline that causes the artifacts.

    The correct solution is to use the replace_base_pipeline from
    meshcutter.core.replace_base, which generates fresh micro-feet base
    geometry instead of trying to carve it with booleans.

    See: meshcutter.core.replace_base.replace_base_pipeline()

    ---
    Original docstring preserved below for reference:
    ---

    At channel junctions, small circular-segment gaps exist between the micro-foot's
    curved inner corner arc and the straight channel edge. These gaps are not cut by
    either the cell cutter (which follows the foot arc) or the channel (which has
    straight edges).

    The gap at each micro-foot inner corner is the thin circular segment between:
    - The foot's corner arc (R=4mm at base, shrinking with Z)
    - The tangent channel edge (straight line)

    This function generates the correction geometry by building the circular segment
    at each adjacent micro-foot's inner corner.

    Args:
        node_x: X position of the junction node
        node_y: Y position of the junction node
        incident_directions: List of incident channel directions ('N', 'S', 'E', 'W')
        z0, z1, z2, z3: Z breakpoints (CQ space)
        top_chamf_vert: Vertical height of top chamfer region
        bot_chamf_vert: Vertical height of bottom chamfer region
        micro_pitch: Micro-foot pitch (default GRU/4 = 10.5mm)
        n_arc_points: Number of points for arc approximation

    Returns:
        CadQuery Workplane with correction solid, or None if no correction needed
    """
    import warnings

    warnings.warn(
        "generate_junction_correction is deprecated and does not work correctly. "
        "Use meshcutter.core.replace_base.replace_base_pipeline() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    import numpy as np

    if micro_pitch is None:
        micro_pitch = GRU / 4.0  # 10.5mm for div=4

    micro_foot_half = (micro_pitch - GR_TOL) / 2.0  # 5.0mm for div=4

    def channel_half_width_at_z(z: float) -> float:
        """Compute channel half-width at given Z level (CQ space)."""
        if z >= z3:
            return GR_TOL / 2.0
        elif z >= z2:
            return GR_TOL / 2.0 + (z3 - z)
        elif z >= z1:
            return GR_TOL / 2.0 + (z3 - z2)  # = 0.25 + bot_chamf_vert
        else:
            return GR_TOL / 2.0 + (z3 - z2) + (z1 - z)

    def foot_corner_radius_at_z(z: float) -> float:
        """Compute micro-foot corner radius at given Z level (CQ space)."""
        if z >= z3:
            return GR_RAD
        else:
            return max(0.0, GR_RAD - (z3 - z))

    # At a junction node, find the adjacent micro-feet and their inner corner positions.
    # For a 4-cell intersection at (node_x, node_y), the 4 adjacent micro-feet are at:
    # - Foot centers: (node_x ± micro_pitch/2, node_y ± micro_pitch/2)
    # - Each foot's inner corner points toward the junction

    # The gap exists between each foot's inner corner arc and the adjacent channel edge.
    # For the foot at (node_x - micro_pitch/2, node_y - micro_pitch/2) (SW quadrant):
    # - Inner corner at (node_x - GR_TOL/2, node_y - GR_TOL/2)
    # - Arc center at (node_x - GR_TOL/2 - GR_RAD + micro_foot_half + GR_TOL/2, ...)
    #   Wait, this is getting complicated. Let me work it out properly.

    # Foot at center (fx, fy) has:
    # - Outer edges at fx ± micro_foot_half, fy ± micro_foot_half
    # - Corner radius GR_RAD at base
    # - Inner corner (toward +X, +Y) at (fx + micro_foot_half, fy + micro_foot_half)
    # - Arc center for inner corner at (fx + micro_foot_half - GR_RAD, fy + micro_foot_half - GR_RAD)

    # For the SW foot (in the -X, -Y quadrant from junction):
    # - Foot center: (node_x - micro_pitch/2, node_y - micro_pitch/2)
    #              = (node_x - 5.25, node_y - 5.25)
    # - Inner corner (toward +X, +Y from foot center):
    #   (fx + micro_foot_half, fy + micro_foot_half)
    #   = (node_x - 5.25 + 5, node_y - 5.25 + 5)
    #   = (node_x - 0.25, node_y - 0.25)
    # - Arc center: (node_x - 0.25 - 4, node_y - 0.25 - 4) = (node_x - 4.25, node_y - 4.25)

    # The gap for this foot is the circular segment between:
    # - Arc (R=4 at base) centered at (node_x - 4.25, node_y - 4.25)
    # - Tangent lines: X = node_x - 0.25 (vertical channel edge) and Y = node_y - 0.25 (horizontal channel edge)

    # Generate circular segment polygons for each adjacent foot
    def segment_polygon_at_z(
        arc_center_x: float,
        arc_center_y: float,
        foot_corner_x: float,
        foot_corner_y: float,
        dx: int,
        dy: int,
        z: float,
    ) -> Optional[List[Tuple[float, float]]]:
        """Generate circular segment polygon for one micro-foot corner at given Z.

        The segment is bounded by:
        - The vertical channel edge at x = foot_corner_x
        - The horizontal channel edge at y = foot_corner_y
        - The foot's inner corner arc

        Args:
            arc_center_x, arc_center_y: Arc center (fixed, doesn't move with Z)
            foot_corner_x, foot_corner_y: Corner position at foot base (Z=z3)
            dx, dy: Direction of the quadrant (-1 for -X, +1 for +X, etc.)
            z: Current Z level

        Returns:
            Polygon points, or None if no gap at this Z
        """
        R = foot_corner_radius_at_z(z)
        if R <= 0.1:
            return None

        w = channel_half_width_at_z(z)

        # At this Z level:
        # - Foot corner has moved inward by (z3 - z) due to chamfer
        # - Channel edge has moved outward by (z3 - z) due to widening
        shrink = z3 - z
        corner_x = foot_corner_x - dx * shrink  # Corner moves inward
        corner_y = foot_corner_y - dy * shrink
        # Arc center stays FIXED (it's the center of the original arc)

        # Channel edges at this Z (relative to node):
        # For dx=-1: vertical channel edge at x = -w (moving left as channel widens)
        # For dx=+1: vertical channel edge at x = +w (moving right as channel widens)
        channel_edge_x = dx * w
        channel_edge_y = dy * w

        # The gap is bounded by:
        # - Vertical line x = channel_edge_x (from corner to where arc meets it)
        # - Arc from vertical intersection to horizontal intersection
        # - Horizontal line y = channel_edge_y (from arc to corner)

        # But the gap only exists where the channel edge is between the corner and the arc tangent.
        # At base (z=z3): channel edge is at ±0.25, foot corner is at ±0.25, so they coincide!
        # As Z decreases: channel edge moves outward, corner moves inward, creating a gap.

        # Actually wait - let me reconsider.
        # At z=z3 (foot base):
        # - Foot corner at (node_x - 0.25, node_y - 0.25) for SW foot
        # - Channel edge at X = -0.25 and Y = -0.25 relative to node
        # - These coincide! No gap at z=z3.

        # As Z decreases:
        # - Foot corner moves toward (-node_x, -node_y) direction (inward)
        # - Channel edge moves in (-dx, -dy) direction (outward)
        # - Now there's a gap between channel edge and foot corner

        # Check if there's a gap
        # Gap exists if channel edge is "outside" the corner (further from node center)
        # For dx=-1: gap if channel_edge_x < corner_x (channel moved further left)
        # For dx=+1: gap if channel_edge_x > corner_x (channel moved further right)
        gap_width_x = dx * (channel_edge_x - corner_x)  # Positive if gap exists
        gap_width_y = dy * (channel_edge_y - corner_y)  # Positive if gap exists

        if gap_width_x <= 0 and gap_width_y <= 0:
            return None  # No gap at this Z

        # Build the segment polygon
        # The segment is the region bounded by:
        # - x = corner_x to x = channel_edge_x (or the arc, whichever is closer)
        # - y = corner_y to y = channel_edge_y (or the arc, whichever is closer)
        # - The arc itself

        # Arc intersections with channel edges:
        # Vertical edge x = channel_edge_x:
        #   (channel_edge_x - arc_center_x)^2 + (y - arc_center_y)^2 = R^2
        #   y = arc_center_y ± sqrt(R^2 - (channel_edge_x - arc_center_x)^2)
        dx_edge = channel_edge_x - (arc_center_x - node_x)
        disc_v = R * R - dx_edge * dx_edge
        if disc_v < 0:
            # Arc doesn't reach vertical channel edge
            return None
        arc_y_at_vedge = (arc_center_y - node_y) + dy * np.sqrt(disc_v)

        # Horizontal edge y = channel_edge_y:
        dy_edge = channel_edge_y - (arc_center_y - node_y)
        disc_h = R * R - dy_edge * dy_edge
        if disc_h < 0:
            # Arc doesn't reach horizontal channel edge
            return None
        arc_x_at_hedge = (arc_center_x - node_x) + dx * np.sqrt(disc_h)

        # Build polygon (in local coords relative to node):
        # Start at the L-corner where channel edges meet
        pts = [(channel_edge_x, channel_edge_y)]

        # Go along horizontal edge to where arc meets it
        pts.append((arc_x_at_hedge, channel_edge_y))

        # Follow arc from horizontal intersection to vertical intersection
        # Arc center in local coords:
        local_arc_cx = arc_center_x - node_x
        local_arc_cy = arc_center_y - node_y

        # Calculate start and end angles for the arc
        start_angle = np.arctan2(channel_edge_y - local_arc_cy, arc_x_at_hedge - local_arc_cx)
        end_angle = np.arctan2(arc_y_at_vedge - local_arc_cy, channel_edge_x - local_arc_cx)

        # Ensure we go the right way around the arc
        if dx * dy > 0:
            # Same sign: arc goes counterclockwise (in standard math coords)
            if end_angle < start_angle:
                end_angle += 2 * np.pi
        else:
            # Opposite sign: arc goes clockwise
            if end_angle > start_angle:
                end_angle -= 2 * np.pi

        for i in range(1, n_arc_points - 1):
            t = i / (n_arc_points - 1)
            angle = start_angle + t * (end_angle - start_angle)
            px = local_arc_cx + R * np.cos(angle)
            py = local_arc_cy + R * np.sin(angle)
            pts.append((px, py))

        # End at vertical edge where arc meets it
        pts.append((channel_edge_x, arc_y_at_vedge))

        # Close back to start (CadQuery will handle this)

        return pts

    # Determine which quadrants have gaps based on incident directions
    # At a degree-4 node, all 4 adjacent feet have gaps
    # At a degree-2 node (boundary), only 2 adjacent feet have gaps

    has_n = "N" in incident_directions
    has_s = "S" in incident_directions
    has_e = "E" in incident_directions
    has_w = "W" in incident_directions

    # For each quadrant, check if both adjacent channel directions exist
    quadrants = []
    if has_e and has_n:  # NE quadrant
        quadrants.append((1, 1))
    if has_w and has_n:  # NW quadrant
        quadrants.append((-1, 1))
    if has_e and has_s:  # SE quadrant
        quadrants.append((1, -1))
    if has_w and has_s:  # SW quadrant
        quadrants.append((-1, -1))

    if not quadrants:
        return None

    # For each quadrant, compute the foot corner position and arc center
    foot_data = []
    for dx, dy in quadrants:
        # Foot corner at base (relative to node)
        foot_corner_x = dx * GR_TOL / 2.0
        foot_corner_y = dy * GR_TOL / 2.0
        # Arc center (relative to node)
        arc_center_x = foot_corner_x + dx * GR_RAD
        arc_center_y = foot_corner_y + dy * GR_RAD
        foot_data.append((arc_center_x, arc_center_y, foot_corner_x, foot_corner_y, dx, dy))

    # Build correction geometry at multiple Z levels
    z_levels = [z0, z1, z2, z3]
    all_segments = None

    for arc_cx, arc_cy, corner_x, corner_y, dx, dy in foot_data:
        segment_slices = []

        for z in z_levels:
            pts = segment_polygon_at_z(
                arc_center_x=arc_cx + node_x,
                arc_center_y=arc_cy + node_y,
                foot_corner_x=corner_x + node_x,
                foot_corner_y=corner_y + node_y,
                dx=dx,
                dy=dy,
                z=z,
            )
            if pts is not None and len(pts) >= 3:
                segment_slices.append((z, pts))

        if len(segment_slices) < 2:
            continue

        # Loft through the slices
        z_first, pts_first = segment_slices[0]
        wp = cq.Workplane("XY", origin=(node_x, node_y, z_first))
        wp = wp.polyline(pts_first).close()

        for z_level, pts in segment_slices[1:]:
            wp = wp.workplane(offset=(z_level - z_first))
            wp = wp.polyline(pts).close()
            z_first = z_level

        try:
            segment_solid = wp.loft()
            if all_segments is None:
                all_segments = segment_solid.val()
            else:
                all_segments = all_segments.fuse(segment_solid.val())
        except Exception:
            continue

    if all_segments is None:
        return None

    return cq.Workplane("XY").newObject([all_segments])


def generate_corner_plug(
    x_pos: float,
    y_pos: float,
    z0: float,
    z1: float,
    z2: float,
    z3: float,
    top_chamf_vert: float,
    bot_chamf_vert: float,
    straight_vert: float,
    epsilon: float = 0.02,
) -> cq.Workplane:
    """Generate a diamond-shaped corner plug at a 4-cell intersection.

    The plug fills the diagonal gap between perpendicular channels at the
    intersection point. It uses a diamond (45° rotated square) cross-section
    that follows the same taper profile as the channels.

    The diamond inradius at each Z level equals the channel half-width:
    - At z0 (tip): inradius = (GR_TOL + 2*(top_chamf + bot_chamf)) / 2
    - At z1 (after bot chamfer): inradius = (GR_TOL + 2*top_chamf) / 2
    - At z2 (same as z1, straight section)
    - At z3 (base): inradius = GR_TOL / 2

    The plug is built as three segments using loft/extrude to match the
    channel taper profile exactly.

    Args:
        x_pos: X position of the intersection
        y_pos: Y position of the intersection
        z0, z1, z2, z3: Z breakpoints (same as channel profile)
        top_chamf_vert: Vertical height of top chamfer
        bot_chamf_vert: Vertical height of bottom chamfer
        straight_vert: Vertical height of straight section
        epsilon: Small margin to add to inradius for tolerance

    Returns:
        CadQuery Workplane with diamond-shaped plug
    """
    # Calculate inradius at each Z level (with epsilon margin)
    r0 = (GR_TOL + 2.0 * (top_chamf_vert + bot_chamf_vert)) / 2.0 + epsilon  # At z0 (tip)
    r1 = (GR_TOL + 2.0 * top_chamf_vert) / 2.0 + epsilon  # At z1 (after bot chamfer)
    r2 = r1  # At z2 (same, straight section)
    r3 = GR_TOL / 2.0 + epsilon  # At z3 (base)

    def diamond_points(r: float) -> List[Tuple[float, float]]:
        """Create diamond (45° square) vertices with given inradius."""
        return [(r, 0), (0, r), (-r, 0), (0, -r)]

    # Build plug as three segments using loft/extrude
    # Segment 1: z0 to z1 (bottom chamfer - tapered)
    segment1 = (
        cq.Workplane("XY", origin=(x_pos, y_pos, z0))
        .polyline(diamond_points(r0))
        .close()
        .workplane(offset=(z1 - z0))
        .polyline(diamond_points(r1))
        .close()
        .loft()
    )

    # Segment 2: z1 to z2 (straight section - constant radius)
    segment2 = cq.Workplane("XY", origin=(x_pos, y_pos, z1)).polyline(diamond_points(r1)).close().extrude(z2 - z1)

    # Segment 3: z2 to z3 (top chamfer - tapered)
    segment3 = (
        cq.Workplane("XY", origin=(x_pos, y_pos, z2))
        .polyline(diamond_points(r2))
        .close()
        .workplane(offset=(z3 - z2))
        .polyline(diamond_points(r3))
        .close()
        .loft()
    )

    # Union all segments
    plug = segment1.union(segment2).union(segment3)

    return plug


def generate_inner_corner_fillet(
    corner_x: float,
    corner_y: float,
    arc_center_x: float,
    arc_center_y: float,
    z0: float,
    z1: float,
    z2: float,
    z3: float,
    base_radius: float = 4.0,
    n_arc_points: int = 12,
) -> cq.Workplane:
    """Generate a fillet plug to fill the gap at inner micro-foot corners.

    At 4-cell meeting points, the cell cutter has a curved boundary where the
    micro-foot's inner corner arc is. The channel has straight edges. This
    creates a "circular segment" gap between the curved cell cutter edge and
    the straight channel edge.

    This fillet fills that gap. It's shaped like a circular segment that tapers
    along Z to match the foot profile.

    The gap exists because:
    - Cell cutter boundary follows the micro-foot's 4mm corner arc
    - Channel boundary is straight (X=corner_x or Y=corner_y)
    - The arc curves AWAY from the straight lines, leaving a gap

    Args:
        corner_x: X coordinate of the corner (where channel edges meet)
        corner_y: Y coordinate of the corner
        arc_center_x: X coordinate of the micro-foot arc center
        arc_center_y: Y coordinate of the micro-foot arc center
        z0: Bottom Z (foot tip, CQ space)
        z1: After bottom chamfer
        z2: After straight section
        z3: Top Z (foot base, CQ space)
        base_radius: Arc radius at foot base (Z=z3), typically 4mm
        n_arc_points: Number of points to approximate the arc

    Returns:
        CadQuery Workplane with fillet solid
    """
    import numpy as np

    def fillet_polygon_at_z(z_level: float, z_ref: float = z3) -> List[Tuple[float, float]]:
        """Generate fillet polygon at given Z level.

        The fillet shrinks as Z decreases (toward foot tip) because:
        - The micro-foot corner radius decreases with the 45° chamfer
        - The corner position moves inward

        Args:
            z_level: Z level in CQ space
            z_ref: Reference Z (foot base, where radius = base_radius)

        Returns:
            List of (x, y) polygon vertices
        """
        # How much has the foot shrunk at this Z?
        shrink = z_ref - z_level  # Positive when z_level < z_ref

        # Current arc radius
        R = base_radius - shrink
        if R <= 0.1:  # Minimum radius to avoid degenerate geometry
            return None

        # Current corner position (moves inward with shrink)
        cx = corner_x - shrink
        cy = corner_y - shrink

        # Arc center stays fixed (property of uniform 45° taper)
        # Current arc endpoints:
        # - Arc start: (arc_center_x + R, arc_center_y) - on the X=cx line
        # - Arc end: (arc_center_x, arc_center_y + R) - on the Y=cy line

        arc_start = (arc_center_x + R, arc_center_y)
        arc_end = (arc_center_x, arc_center_y + R)

        # Build polygon: corner -> arc_start -> along arc -> arc_end -> back to corner
        pts = [(cx, cy)]
        pts.append(arc_start)

        # Arc points (from θ=0 to θ=π/2)
        for t in np.linspace(0, np.pi / 2, n_arc_points)[1:-1]:
            x = arc_center_x + R * np.cos(t)
            y = arc_center_y + R * np.sin(t)
            pts.append((x, y))

        pts.append(arc_end)

        return pts

    def make_polygon_wire(pts: List[Tuple[float, float]], z: float) -> cq.Workplane:
        """Create a CadQuery wire from polygon points at given Z."""
        wp = cq.Workplane("XY", origin=(0, 0, z))
        return wp.polyline(pts).close()

    # Generate polygons at key Z levels
    # We use the same Z breakpoints as the channel profile
    z_levels = [z0, z1, z2, z3]

    # Build the fillet as a lofted solid through multiple cross-sections
    polygons = []
    for z in z_levels:
        pts = fillet_polygon_at_z(z, z_ref=z3)
        if pts is None:
            continue
        polygons.append((z, pts))

    if len(polygons) < 2:
        # Not enough valid cross-sections
        return None

    # Create loft from bottom to top
    # Start with the bottom polygon
    z_bottom, pts_bottom = polygons[0]
    fillet = cq.Workplane("XY", origin=(0, 0, z_bottom)).polyline(pts_bottom).close()

    for z_level, pts in polygons[1:]:
        fillet = fillet.workplane(offset=(z_level - z_bottom)).polyline(pts).close()
        z_bottom = z_level

    fillet = fillet.loft()

    return fillet


def detect_inner_corner_positions(
    cell_centers: List[Tuple[float, float]],
    pitch: float = GRU,
    micro_pitch: float = None,
) -> List[Tuple[float, float, float, float]]:
    """Detect positions where inner corner fillets are needed.

    At each 4-cell meeting point, there are 4 inner micro-foot corners that
    need fillets. This function returns the corner and arc center positions
    for each fillet.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        pitch: 1U pitch (default 42mm)
        micro_pitch: Micro-foot pitch (default GRU/4 = 10.5mm)

    Returns:
        List of (corner_x, corner_y, arc_center_x, arc_center_y) tuples
    """
    if micro_pitch is None:
        micro_pitch = pitch / 4  # Default to quarter-grid

    # First find 4-cell intersection points
    intersections = detect_four_cell_intersections(cell_centers, pitch)

    fillets = []
    micro_foot_half = (micro_pitch - GR_TOL) / 2  # 5.0mm for div=4
    corner_radius = GR_RAD  # 4.0mm

    for ix, iy in intersections:
        # At each intersection, there are 4 adjacent micro-feet
        # Each has its inner corner pointing toward the intersection

        # The 4 micro-feet are at offsets (±micro_pitch/2, ±micro_pitch/2) from intersection
        # Their inner corners are at (ix + dx*0.25, iy + dy*0.25) at Z=5
        # The arc center is always (corner - 4, corner - 4) because the inner corner
        # arc curves away from the intersection

        # For dx=-1, dy=-1: corner at (ix - 0.25, iy - 0.25), arc center at (ix - 4.25, iy - 4.25)
        # For dx=+1, dy=+1: corner at (ix + 0.25, iy + 0.25), arc center at (ix - 3.75, iy - 3.75)
        # Wait, that's wrong. Each foot's arc center is at (foot_center + 5 - 4, ...) = (foot_center + 1)
        # which is (corner - 4, corner - 4) from the corner.

        # Actually: arc center is (corner_x + dx*corner_radius, corner_y + dy*corner_radius)
        # because for dx=-1: corner_x - 4 is the correct direction (toward -X)
        #          for dx=+1: corner_x + 4 is the correct direction (toward +X)
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            corner_x = ix + dx * GR_TOL / 2
            corner_y = iy + dy * GR_TOL / 2
            # Arc center is in the direction AWAY from the intersection (same sign as dx, dy)
            arc_cx = corner_x + dx * corner_radius
            arc_cy = corner_y + dy * corner_radius
            fillets.append((corner_x, corner_y, arc_cx, arc_cy))

    return fillets


def generate_intercell_channels(
    cell_centers: List[Tuple[float, float]],
    pitch: float = GRU,
    epsilon: float = 0.02,
    footprint_bounds: Optional[Tuple[float, float, float, float]] = None,
) -> Optional[cq.Workplane]:
    """Generate tapered channel cutters between adjacent 1U cells.

    When cutting micro-feet into a model with existing 1U feet, the cell
    cutters (F1 - micro_feet) don't reach the inter-cell gaps. This function
    creates TAPERED channels that match the foot profile exactly:
    - Narrow (GR_TOL) at foot base (Z=5 in world, Z=-4.75 in CQ space)
    - Wide at foot tip (Z=0 in world, Z=+0.25 in CQ space)

    The channel profile mirrors GR_BOX_PROFILE to match the foot chamfers,
    ensuring the channel cuts exactly the gap between micro-feet without
    cutting into the micro-feet themselves.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        pitch: 1U pitch (default 42mm)
        epsilon: Extension below z=0 (mm)
        footprint_bounds: Optional (x_min, y_min, x_max, y_max) to clip channels
                         to model footprint. If None, channels extend to full
                         grid extent (may clip corners of outer model).

    Returns:
        CadQuery Workplane with channel cutters, or None if no channels needed
    """
    if len(cell_centers) < 2:
        return None

    # Find unique X and Y coordinates
    xs = sorted(set(cx for cx, cy in cell_centers))
    ys = sorted(set(cy for cx, cy in cell_centers))

    # Channel profile segments (from GR_BOX_PROFILE)
    # GR_BOX_PROFILE = ((top_chamf_diag, 45), straight, (bot_chamf_diag, 45))
    # Extract vertical heights from diagonal lengths
    top_chamf_diag = GR_BOX_PROFILE[0][0]
    top_chamf_vert = top_chamf_diag / SQRT2  # ~2.4mm
    straight_vert = GR_BOX_PROFILE[1]  # 1.8mm
    bot_chamf_diag = GR_BOX_PROFILE[2][0]
    bot_chamf_vert = bot_chamf_diag / SQRT2  # ~0.8mm

    # Z levels in CQ space (before flip_z transform)
    # z0 = foot base (narrow channel), z3 = foot tip (wide channel)
    z0 = -GR_BASE_HEIGHT  # -4.75mm
    z1 = z0 + top_chamf_vert  # ~-2.35mm
    z2 = z1 + straight_vert  # ~-0.55mm
    z3 = z2 + bot_chamf_vert  # +0.25mm = GR_BASE_CLR (exact foot base, no epsilon)

    # Base channel width at foot base (narrowest point)
    # This is just the GR_TOL gap between adjacent micro-feet
    base_width = GR_TOL  # 0.5mm

    # Small XY epsilon for channel length overshoot
    eps_xy = 0.05

    channels = None

    def _create_tapered_channel(
        width: float, length: float, x_pos: float, y_pos: float, rotated: bool = False
    ) -> cq.Workplane:
        """Create a single tapered channel matching foot profile.

        The channel must be:
        - WIDE at CQ Z=+0.25 (foot BASE in CQ, but becomes foot TIP at world Z=0)
        - NARROW at CQ Z=-4.75 (foot TIP in CQ, but becomes foot BASE at world Z=5)

        In CQ space, the foot is WIDER at higher Z (base at top, tip at bottom).
        After flip_z, this gets reversed: tip at world Z=0, base at world Z=5.

        The GAP between feet is inverse of foot width:
        - At foot TIP (CQ Z=-4.75 → world Z=0): feet are narrow, gap is WIDE
        - At foot BASE (CQ Z=+0.25 → world Z=5): feet are wide, gap is NARROW

        So we build the channel starting WIDE at the bottom (CQ Z=-4.75) and
        SHRINKING as we go up (using +45 taper), matching the foot profile.

        Args:
            width: Narrow width at Z=z3 (top, foot base)
            length: Channel length (in the long direction)
            x_pos: X position of channel center
            y_pos: Y position of channel center
            rotated: If True, rotate 90° (for horizontal channels)

        Returns:
            CadQuery Workplane with tapered channel
        """
        # Calculate wide width at bottom (foot tip in CQ, becomes world Z=0)
        # Gap at foot tip = GR_TOL + 2*(top_chamf + bot_chamf) = 0.5 + 2*3.2 = 6.9mm
        wide_width = GR_TOL + 2.0 * (top_chamf_vert + bot_chamf_vert)

        # Build channel from Z=z0 (bottom, wide) upward with POSITIVE taper (shrinking)
        # The foot profile is: bot_chamf (45°) → straight → top_chamf (45°)
        # We reverse this for the channel: start wide, shrink with chamfers
        if rotated:
            # Horizontal channel: wide in Y at bottom, narrow at top
            channel = (
                cq.Workplane("XY", origin=(0, 0, z0))
                .rect(length, wide_width)
                .extrude(bot_chamf_vert, taper=45)  # Shrink during bottom chamfer
                .faces(">Z")
                .wires()
                .toPending()
                .extrude(straight_vert)  # Straight section (no taper)
                .faces(">Z")
                .wires()
                .toPending()
                .extrude(top_chamf_vert, taper=45)  # Shrink during top chamfer
            )
        else:
            # Vertical channel: wide in X at bottom, narrow at top
            channel = (
                cq.Workplane("XY", origin=(0, 0, z0))
                .rect(wide_width, length)
                .extrude(bot_chamf_vert, taper=45)  # Shrink during bottom chamfer
                .faces(">Z")
                .wires()
                .toPending()
                .extrude(straight_vert)  # Straight section (no taper)
                .faces(">Z")
                .wires()
                .toPending()
                .extrude(top_chamf_vert, taper=45)  # Shrink during top chamfer
            )

        # Translate to final position
        channel = channel.translate(cq.Vector(x_pos, y_pos, 0))
        return channel

    # Calculate wide channel width at foot tip (for corner inset calculation)
    # Gap at foot tip = GR_TOL + 2*(top_chamf + bot_chamf) = 0.5 + 2*3.2 = 6.9mm
    wide_width = GR_TOL + 2.0 * (top_chamf_vert + bot_chamf_vert)

    # Corner radius of the model (used to inset clipping bounds)
    # The model has rounded corners with radius approximately GR_RAD - GR_TOL/2
    # We need to inset the clipping bounds by the channel's half-width at the bottom
    # PLUS the corner radius to avoid extending into the rounded corner region.
    corner_radius = GR_RAD - GR_TOL / 2.0  # 3.75mm
    channel_half_width_at_tip = wide_width / 2.0  # 3.45mm at Z=0 (foot tip)
    # Total inset needed: corner region where channel would extend outside model
    corner_inset = corner_radius + channel_half_width_at_tip  # ~7.2mm

    # Create vertical channels (between X columns)
    for i in range(len(xs) - 1):
        x_mid = (xs[i] + xs[i + 1]) / 2.0
        # Find Y extent for this column pair
        ys_at_cols = [cy for cx, cy in cell_centers if cx in (xs[i], xs[i + 1])]
        if not ys_at_cols:
            continue
        y_min = min(ys_at_cols) - pitch / 2 - 1
        y_max = max(ys_at_cols) + pitch / 2 + 1

        # Clip to footprint bounds if provided, with corner inset
        if footprint_bounds is not None:
            # Standard clipping to footprint bounds
            y_min = max(y_min, footprint_bounds[1])
            y_max = min(y_max, footprint_bounds[3])

            # Additional corner inset: only apply if channel is near X boundary
            # This prevents the wide channel from extending into rounded corners
            dist_to_x_min = x_mid - footprint_bounds[0]
            dist_to_x_max = footprint_bounds[2] - x_mid
            if dist_to_x_min < corner_inset or dist_to_x_max < corner_inset:
                # Channel is near X boundary - inset Y bounds to avoid corners
                y_min = max(y_min, footprint_bounds[1] + corner_inset)
                y_max = min(y_max, footprint_bounds[3] - corner_inset)

            if y_max <= y_min:
                continue  # Channel completely outside footprint

        y_len = y_max - y_min + 2.0 * eps_xy
        y_center = (y_min + y_max) / 2.0

        channel = _create_tapered_channel(base_width, y_len, x_mid, y_center, rotated=False)

        if channels is None:
            channels = channel.val()
        else:
            channels = channels.fuse(channel.val())

    # Create horizontal channels (between Y rows)
    for j in range(len(ys) - 1):
        y_mid = (ys[j] + ys[j + 1]) / 2.0
        # Find X extent for this row pair
        xs_at_rows = [cx for cx, cy in cell_centers if cy in (ys[j], ys[j + 1])]
        if not xs_at_rows:
            continue
        x_min = min(xs_at_rows) - pitch / 2 - 1
        x_max = max(xs_at_rows) + pitch / 2 + 1

        # Clip to footprint bounds if provided, with corner inset
        if footprint_bounds is not None:
            # Standard clipping to footprint bounds
            x_min = max(x_min, footprint_bounds[0])
            x_max = min(x_max, footprint_bounds[2])

            # Additional corner inset: only apply if channel is near Y boundary
            # This prevents the wide channel from extending into rounded corners
            dist_to_y_min = y_mid - footprint_bounds[1]
            dist_to_y_max = footprint_bounds[3] - y_mid
            if dist_to_y_min < corner_inset or dist_to_y_max < corner_inset:
                # Channel is near Y boundary - inset X bounds to avoid corners
                x_min = max(x_min, footprint_bounds[0] + corner_inset)
                x_max = min(x_max, footprint_bounds[2] - corner_inset)

            if x_max <= x_min:
                continue  # Channel completely outside footprint

        x_len = x_max - x_min + 2.0 * eps_xy
        x_center = (x_min + x_max) / 2.0

        channel = _create_tapered_channel(base_width, x_len, x_center, y_mid, rotated=True)

        if channels is None:
            channels = channel.val()
        else:
            channels = channels.fuse(channel.val())

    # Add corner plugs at 4-cell intersections
    # These fill the diamond-shaped gaps where perpendicular channels don't fully overlap
    four_cell_intersections = detect_four_cell_intersections(cell_centers, pitch)

    for ix, iy in four_cell_intersections:
        plug = generate_corner_plug(
            x_pos=ix,
            y_pos=iy,
            z0=z0,
            z1=z1,
            z2=z2,
            z3=z3,
            top_chamf_vert=top_chamf_vert,
            bot_chamf_vert=bot_chamf_vert,
            straight_vert=straight_vert,
            epsilon=eps_xy,  # Use same epsilon as channels
        )

        if channels is None:
            channels = plug.val()
        else:
            channels = channels.fuse(plug.val())

    # NOTE: Inner corner fillets are disabled for now.
    # The fillet geometry needs more work to match the actual gap shape.
    # The current implementation creates fillets that are too large.
    #
    # TODO: Investigate the actual gap geometry more carefully.
    # The residual is only ~0.12mm³ per corner, but the fillet is ~4mm³.
    #
    # inner_corner_positions = detect_inner_corner_positions(cell_centers, pitch)
    # corner_radius = GR_RAD  # 4.0mm at foot base
    #
    # for corner_x, corner_y, arc_cx, arc_cy in inner_corner_positions:
    #     fillet = generate_inner_corner_fillet(
    #         corner_x=corner_x,
    #         corner_y=corner_y,
    #         arc_center_x=arc_cx,
    #         arc_center_y=arc_cy,
    #         z0=z0,
    #         z1=z1,
    #         z2=z2,
    #         z3=z3,
    #         base_radius=corner_radius,
    #         n_arc_points=12,
    #     )
    #
    #     if fillet is not None:
    #         if channels is None:
    #             channels = fillet.val()
    #         else:
    #             channels = channels.fuse(fillet.val())

    if channels is None:
        return None

    return cq.Workplane("XY").newObject([channels])


def generate_boundary_fill(
    cell_centers: List[Tuple[float, float]],
    pitch: float = GRU,
    epsilon: float = 0.02,
    footprint_bounds: Optional[Tuple[float, float, float, float]] = None,
) -> Optional[cq.Workplane]:
    """Generate boundary fill to cover outer chamfer regions of edge cells.

    The cell cutter is based on the cropped F1 envelope (41.5mm), but the input
    mesh's 1U feet have chamfers that extend slightly beyond this boundary at
    the outer perimeter. This creates thin residual strips at the outer edges.

    IMPORTANT: Unlike inter-cell channels, the boundary fill should NOT extend
    inward into the micro-feet region. At the outer perimeter:
    - The outermost micro-foot edge is at the grid boundary (cell_center ± 20.75)
    - We only need to cut the tiny sliver of 1U foot material OUTSIDE this boundary
    - This is just the GR_TOL/2 = 0.25mm that extends beyond the cropped envelope

    The boundary fill is a thin ring that extends OUTWARD from the grid boundary,
    not inward. This prevents cutting into the outer micro-feet.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        pitch: 1U pitch (default 42mm)
        epsilon: Extension below z=0 (mm)
        footprint_bounds: Optional (x_min, y_min, x_max, y_max) to constrain the
                         outer extent of the boundary fill to the model footprint.
                         If None, extends slightly beyond grid boundary.

    Returns:
        CadQuery Workplane with boundary fill, or None if not needed
    """
    if not cell_centers:
        return None

    # Find grid extents
    xs = sorted(set(cx for cx, cy in cell_centers))
    ys = sorted(set(cy for cx, cy in cell_centers))

    x_min_cell = min(xs)
    x_max_cell = max(xs)
    y_min_cell = min(ys)
    y_max_cell = max(ys)

    # Grid outer boundary (center of outer cells ± half of cropped F1 envelope)
    # This is where the outermost micro-feet edges are
    # Cropped F1 envelope = pitch - GR_TOL = 41.5mm, so half = 20.75mm
    grid_x_min = x_min_cell - (pitch - GR_TOL) / 2
    grid_x_max = x_max_cell + (pitch - GR_TOL) / 2
    grid_y_min = y_min_cell - (pitch - GR_TOL) / 2
    grid_y_max = y_max_cell + (pitch - GR_TOL) / 2

    # The boundary fill should only extend OUTWARD from the grid boundary
    # to cut the small amount of 1U material beyond the micro-feet.
    # This is approximately GR_TOL/2 = 0.25mm plus a small margin.
    eps_xy = 0.05
    outward_extend = GR_TOL / 2.0 + eps_xy  # ~0.3mm outward only

    # Z range matches the cell cutter
    z_min_foot = -GR_BASE_HEIGHT  # -4.75mm
    z_max_foot = GR_BASE_CLR  # 0.25mm exactly (no epsilon on top)
    fill_height = z_max_foot - z_min_foot
    z_center = (z_min_foot + z_max_foot) / 2.0

    # Outer boundary: extend outward from grid boundary, but clip to footprint
    outer_x_min = grid_x_min - outward_extend
    outer_x_max = grid_x_max + outward_extend
    outer_y_min = grid_y_min - outward_extend
    outer_y_max = grid_y_max + outward_extend

    # Clip outer boundary to footprint bounds if provided
    if footprint_bounds is not None:
        outer_x_min = max(outer_x_min, footprint_bounds[0])
        outer_x_max = min(outer_x_max, footprint_bounds[2])
        outer_y_min = max(outer_y_min, footprint_bounds[1])
        outer_y_max = min(outer_y_max, footprint_bounds[3])

    # Inner boundary: exactly at the grid boundary (micro-feet edge)
    # This means the ring only covers the area OUTSIDE the micro-feet
    inner_x_min = grid_x_min
    inner_x_max = grid_x_max
    inner_y_min = grid_y_min
    inner_y_max = grid_y_max

    # Grid center for positioning
    grid_center_x = (x_min_cell + x_max_cell) / 2.0
    grid_center_y = (y_min_cell + y_max_cell) / 2.0

    # Create outer box
    outer_width = outer_x_max - outer_x_min
    outer_height = outer_y_max - outer_y_min
    outer_box = (
        cq.Workplane("XY")
        .box(outer_width, outer_height, fill_height)
        .translate(cq.Vector(grid_center_x, grid_center_y, z_center))
    )

    # Create inner cutout at the grid boundary
    inner_width = inner_x_max - inner_x_min
    inner_height = inner_y_max - inner_y_min
    if inner_width > 0 and inner_height > 0:
        inner_box = (
            cq.Workplane("XY")
            .box(inner_width, inner_height, fill_height + 1)  # slightly taller for clean cut
            .translate(cq.Vector(grid_center_x, grid_center_y, z_center))
        )
        frame = outer_box.cut(inner_box)
    else:
        # Grid too small for ring, use solid rect
        frame = outer_box

    return frame


def generate_grid_cutter_cq(
    cell_centers: List[Tuple[float, float]],
    micro_divisions: int = 4,
    epsilon: float = 0.02,
    overshoot: float = 0.0,
    wall_cut: float = 0.0,
    add_channels: bool = False,
    footprint_bounds: Optional[Tuple[float, float, float, float]] = None,
) -> cq.Workplane:
    """Generate full grid cutter in CadQuery (one export, one subtract).

    Instances the cell cutter at each detected cell center and unions them
    all in CadQuery before export. This minimizes triangle boolean operations.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        micro_divisions: Number of divisions (2 or 4)
        epsilon: Extension below z=0 (mm)
        overshoot: Extension beyond F1 boundary to cut outer walls (mm)
        wall_cut: Shrink micro-feet to cut outer walls (mm)
        add_channels: If True, add inter-cell channel cutters
        footprint_bounds: Optional (x_min, y_min, x_max, y_max) to clip channels
                         and boundary fill to model footprint. Prevents corner
                         clipping artifacts when cutter extends beyond model.

    Returns:
        CadQuery Workplane with complete grid cutter solid
    """
    if not cell_centers:
        raise ValueError("No cell centers provided")

    # Get the cached cell cutter
    cell_cutter = generate_cell_cutter_cq(micro_divisions, epsilon, overshoot, wall_cut)
    cell_solid = cell_cutter.val()

    # Instance at each cell center
    grid_cutter = None
    for cx, cy in cell_centers:
        instance = cell_solid.translate(cq.Vector(cx, cy, 0))
        if grid_cutter is None:
            grid_cutter = instance
        else:
            grid_cutter = grid_cutter.fuse(instance)

    # Add inter-cell channels if requested
    if add_channels and len(cell_centers) > 1:
        channels_cq = generate_intercell_channels(cell_centers, GRU, epsilon, footprint_bounds)
        if channels_cq is not None:
            grid_cutter = grid_cutter.fuse(channels_cq.val())

    # Add boundary fill to cover outer chamfer regions
    if add_channels:
        boundary_fill = generate_boundary_fill(cell_centers, GRU, epsilon, footprint_bounds)
        if boundary_fill is not None:
            grid_cutter = grid_cutter.fuse(boundary_fill.val())

    # Z-clipping safeguard: Intersect with half-space to enforce Z <= GR_BASE_CLR
    # This catches any epsilon/rounding drift from channels or boundary fill.
    # Creates a large bounding box that ends exactly at z=GR_BASE_CLR (foot base plane).
    bb = grid_cutter.BoundingBox()
    clip_margin = 10.0  # Extra margin in XY to ensure full coverage
    clip_box = (
        cq.Workplane("XY")
        .box(
            bb.xmax - bb.xmin + 2 * clip_margin,
            bb.ymax - bb.ymin + 2 * clip_margin,
            GR_BASE_CLR - bb.zmin + clip_margin,  # From below cutter to exactly GR_BASE_CLR
        )
        .translate(
            cq.Vector(
                (bb.xmin + bb.xmax) / 2,
                (bb.ymin + bb.ymax) / 2,
                (bb.zmin - clip_margin + GR_BASE_CLR) / 2,  # Center the box vertically
            )
        )
    )
    grid_cutter = grid_cutter.intersect(clip_box.val())

    # Assert that Z max is within tolerance of GR_BASE_CLR
    final_bb = grid_cutter.BoundingBox()
    assert (
        final_bb.zmax <= GR_BASE_CLR + 1e-6
    ), f"Cutter Z max ({final_bb.zmax:.6f}) exceeds GR_BASE_CLR ({GR_BASE_CLR})"

    return cq.Workplane("XY").newObject([grid_cutter])


def generate_grid_cutter_meshes(
    cell_centers: List[Tuple[float, float]],
    micro_divisions: int = 4,
    epsilon: float = 0.02,
    tol: float = 0.01,
    ang_tol: float = 0.1,
    flip_z: bool = True,
    overshoot: float = 0.0,
    wall_cut: float = 0.0,
    add_channels: bool = False,
) -> List[trimesh.Trimesh]:
    """Generate grid cutter as list of individual cell cutter meshes.

    This approach keeps each cell cutter as a separate watertight mesh,
    which works better with manifold boolean operations that can handle
    multiple tool meshes.

    Args:
        cell_centers: List of (x, y) cell center coordinates
        micro_divisions: Number of divisions (2 or 4)
        epsilon: Extension below z=0 (mm)
        tol: STL export tolerance
        ang_tol: STL export angular tolerance
        flip_z: If True, flip Z coordinates so foot points upward (z=0 to z~5)
                matching typical STL exports. Default True.
        overshoot: Extension beyond F1 boundary to cut outer walls (mm)
        wall_cut: Shrink micro-feet to cut outer walls (mm)
        add_channels: If True, add inter-cell channel cutters to cut material
                      between adjacent cells. Only needed for solid-walled 1U
                      boxes. Default False.

    Returns:
        List of trimesh.Trimesh meshes, one per cell
    """
    if not cell_centers:
        raise ValueError("No cell centers provided")

    # Generate the template cell cutter mesh (watertight)
    cell_cutter_cq = generate_cell_cutter_cq(micro_divisions, epsilon, overshoot, wall_cut)
    cell_mesh = cq_to_trimesh(cell_cutter_cq, tol=tol, ang_tol=ang_tol)

    # Align Z if requested (default) to match typical STL orientation
    # The CQ cutter has foot tip at z≈-4.75, base at z≈0.25 (after mirror in CQ)
    # STL exports typically have foot tip at z=0, base at z≈5
    # We just need to TRANSLATE upward, NOT negate/reflect Z
    # This preserves the correct taper direction (narrow at bottom, wide at top)
    cell_z_min = None
    if flip_z:
        # Shift so the minimum Z (foot tip) is at z=-epsilon
        # This ensures the cutter extends BELOW the model's z=0 bottom plane,
        # avoiding coplanar faces that cause non-manifold edges
        cell_z_min = cell_mesh.vertices[:, 2].min()
        cell_mesh.vertices[:, 2] -= cell_z_min  # Now tip is at z=0
        cell_mesh.vertices[:, 2] -= epsilon  # Now tip is at z=-epsilon
        # No invert() needed since we didn't negate/reflect

    # Instance at each cell center
    meshes = []
    for cx, cy in cell_centers:
        instance = cell_mesh.copy()
        instance.apply_translation([cx, cy, 0])
        meshes.append(instance)

    # Add inter-cell channel cutters if requested and there are multiple cells
    # These cut away the remaining 1U foot wall material between adjacent cells
    # Only needed for solid-walled 1U boxes, not for natively-generated microfinity boxes
    if add_channels and len(cell_centers) > 1:
        channels_cq = generate_intercell_channels(cell_centers, GRU, epsilon)
        if channels_cq is not None:
            channels_mesh = cq_to_trimesh(channels_cq, tol=tol, ang_tol=ang_tol)
            if flip_z:
                # Use the SAME z_min as cell cutters for consistent Z alignment
                # This ensures channels end at the same Z level as the cell cutters
                # (i.e., at Z=5.0 in world coordinates, matching the foot base)
                if cell_z_min is not None:
                    channels_mesh.vertices[:, 2] -= cell_z_min
                    channels_mesh.vertices[:, 2] -= epsilon
            meshes.append(channels_mesh)

    return meshes


def apply_bottom_epsilon_preserve_top(mesh: trimesh.Trimesh, epsilon: float) -> None:
    """Apply coplanar avoidance by pushing bottom down while preserving top.

    Maps Z range [zmin, zmax] → [zmin - epsilon, zmax] using affine transform.
    This cannot create internal faces because it only moves vertices.

    The transform is:
        z_new = -epsilon + (z - zmin) * (h + epsilon) / h

    Where h = zmax - zmin. This keeps:
        - z=zmin → -epsilon (bottom gets pushed down)
        - z=zmax → h (top stays exactly where it was after normalization)

    Args:
        mesh: Trimesh to modify in-place
        epsilon: Amount to push bottom below Z=0
    """
    if epsilon <= 0:
        return

    zmin = float(mesh.vertices[:, 2].min())
    zmax = float(mesh.vertices[:, 2].max())
    h = zmax - zmin

    if h <= 1e-9:
        raise ValueError(f"Degenerate cutter height: h={h}")

    # Normalize so bottom is at 0, top at h
    mesh.vertices[:, 2] -= zmin

    # Affine map [0, h] -> [-epsilon, h]
    # z_new = -epsilon + z * (h + epsilon) / h
    scale = (h + epsilon) / h
    mesh.vertices[:, 2] = -epsilon + mesh.vertices[:, 2] * scale


def generate_grid_cutter_mesh(
    cell_centers: List[Tuple[float, float]],
    micro_divisions: int = 4,
    epsilon: float = 0.02,
    tol: float = 0.01,
    ang_tol: float = 0.1,
    flip_z: bool = True,
    overshoot: float = 0.0,
    wall_cut: float = 0.0,
    add_channels: bool = False,
    fast_mode: bool = False,
    footprint_bounds: Optional[Tuple[float, float, float, float]] = None,
) -> trimesh.Trimesh:
    """Generate grid cutter as a single mesh.

    ALWAYS uses CadQuery fusion for robustness (eliminates boolean slivers).
    The fast_mode option exists for debugging but is not recommended for
    production use as it may leave slivers or asymmetric artifacts.

    The top of the cutter is extended by epsilon before the Z-shift, ensuring
    the final cutter top is at exactly Z=5.0 (not truncated by epsilon).

    Args:
        cell_centers: List of (x, y) cell center coordinates
        micro_divisions: Number of divisions (2 or 4)
        epsilon: Extension below z=0 (mm)
        tol: STL export tolerance
        ang_tol: STL export angular tolerance
        flip_z: If True, flip Z so foot points upward (z=0 to z~5). Default True.
        overshoot: Extension beyond F1 boundary to cut outer walls (mm)
        wall_cut: Shrink micro-feet to cut outer walls (mm)
        add_channels: If True, add inter-cell channel cutters. Default False.
        fast_mode: If True, use mesh concatenation instead of CQ fusion (debug only).
                   WARNING: May leave slivers/asymmetry due to non-fused shells.
        footprint_bounds: Optional (x_min, y_min, x_max, y_max) to clip channels
                         and boundary fill to model footprint.

    Returns:
        trimesh.Trimesh with all cell cutters
    """
    # Fast mode: use mesh concatenation (debug only, may have slivers)
    if fast_mode:
        import warnings

        warnings.warn(
            "fast_mode=True may leave slivers/asymmetry due to non-fused shells. " "Use only for debugging.",
            UserWarning,
        )
        meshes = generate_grid_cutter_meshes(
            cell_centers, micro_divisions, epsilon, tol, ang_tol, flip_z, overshoot, wall_cut, add_channels=add_channels
        )
        if len(meshes) == 1:
            return meshes[0]
        return trimesh.util.concatenate(meshes)

    # Default: Always use CadQuery fusion for robustness
    # This eliminates boolean slivers from overlapping mesh shells
    cq_cutter = generate_grid_cutter_cq(
        cell_centers,
        micro_divisions,
        epsilon,
        overshoot,
        wall_cut,
        add_channels=add_channels,
        footprint_bounds=footprint_bounds,
    )

    # Convert to trimesh (no box-fusing operations that create internal faces)
    mesh = cq_to_trimesh(cq_cutter, tol=tol, ang_tol=ang_tol)

    if flip_z:
        # Apply coplanar avoidance as a pure affine transform.
        # This pushes the bottom down by epsilon while preserving the top,
        # WITHOUT creating internal coincident faces (which caused "stacked
        # Z sheets" artifacts like 4.98/5.00/5.02).
        apply_bottom_epsilon_preserve_top(mesh, epsilon)

    return mesh


# -----------------------------------------------------------------------------
# Conversion to trimesh
# -----------------------------------------------------------------------------
def cq_to_trimesh(
    cq_obj: cq.Workplane,
    tol: float = 0.01,
    ang_tol: float = 0.1,
) -> trimesh.Trimesh:
    """Convert CadQuery Workplane to trimesh with proper cleanup.

    Exports to STL via temp file, then loads with trimesh.
    Temp file is automatically cleaned up.

    Args:
        cq_obj: CadQuery Workplane to convert
        tol: Linear mesh tolerance (mm)
        ang_tol: Angular mesh tolerance (radians)

    Returns:
        trimesh.Trimesh mesh
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        stl_path = os.path.join(tmpdir, "cutter.stl")
        cq.exporters.export(
            cq_obj,
            stl_path,
            exportType="STL",
            tolerance=tol,
            angularTolerance=ang_tol,
        )
        mesh = trimesh.load(stl_path)

    return mesh


# -----------------------------------------------------------------------------
# Validation helpers
# -----------------------------------------------------------------------------
def get_cell_cutter_volume(micro_divisions: int = 4) -> float:
    """Get the volume of a single cell cutter from CadQuery solid.

    This is the authoritative volume (not dependent on tessellation).

    Args:
        micro_divisions: Number of divisions (2 or 4)

    Returns:
        Volume in mm³
    """
    cutter = generate_cell_cutter_cq(micro_divisions, epsilon=0)
    return cutter.val().Volume()


def get_1u_foot_volume() -> float:
    """Get the volume of a 1U foot from CadQuery solid.

    Returns:
        Volume in mm³
    """
    foot = generate_1u_foot_cq()
    return foot.val().Volume()


def get_micro_foot_volume(micro_divisions: int = 4) -> float:
    """Get the volume of a micro foot from CadQuery solid.

    Args:
        micro_divisions: Number of divisions (2 or 4)

    Returns:
        Volume in mm³
    """
    foot = generate_micro_foot_cq(micro_divisions)
    return foot.val().Volume()
