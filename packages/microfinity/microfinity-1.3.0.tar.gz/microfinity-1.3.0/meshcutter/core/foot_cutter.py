#! /usr/bin/env python3
#
# meshcutter.core.foot_cutter - Gridfinity micro-foot complement cutter generation
#
# Generates cutters using the complement approach: Cutter = F1 - Fm
# where F1 is the 1U foot volume and Fm is the union of micro-feet.
#
# Instead of computing this via 3D booleans, we construct the geometry
# analytically as a lofted polygon-with-holes, which is faster and more stable.

from __future__ import annotations

from typing import List, Tuple, Optional, Union

import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon

from meshcutter.core.detection import BottomFrame
from meshcutter.core.geometry import sample_rounded_rect
from meshcutter.core.profile import (
    GR_BASE_HEIGHT,
    GR_BOX_CHAMF_H,
    GR_STR_H,
    GR_BASE_CLR,
)

# Gridfinity constants (from microfinity.core.constants)
GRU = 42.0  # 1U pitch (mm)
GR_TOL = 0.5  # Clearance between feet (mm)
GR_RAD = 4.0  # Nominal exterior fillet radius (mm)


def compute_foot_size(pitch: float) -> float:
    """Compute foot size from pitch: size = pitch - GR_TOL."""
    return pitch - GR_TOL


def compute_corner_radius(foot_size: float) -> float:
    """Compute corner radius for a foot, clamped to valid range.

    Uses: r = min(GR_RAD + GR_BASE_CLR, foot_size/2 - 0.05)
    """
    r = min(GR_RAD + GR_BASE_CLR, foot_size / 2.0 - 0.05)
    return max(r, 0.2)  # Minimum radius to avoid degenerate geometry


def get_profile_z_levels(epsilon: float = 0.02) -> List[float]:
    """Get the Z levels for the Gridfinity box profile.

    Only 4-5 levels needed since profile is piecewise-linear:
    - z0: -epsilon (coplanar avoidance)
    - z1: 0.0 (floor contact)
    - z2: bottom chamfer end
    - z3: straight section end
    - z4: top (full height)
    """
    z0 = -epsilon
    z1 = 0.0
    z2 = GR_BOX_CHAMF_H
    z3 = GR_BOX_CHAMF_H + GR_STR_H
    z4 = GR_BASE_HEIGHT

    return [z0, z1, z2, z3, z4]


def compute_inset_at_z(z: float) -> float:
    """Compute the profile inset at height z.

    The Gridfinity foot profile in world coordinates (z=0 at foot tip):
    - z=0: foot tip (narrow), maximum inset
    - z=GR_BASE_HEIGHT: foot base (wide), zero inset

    Profile segments (from base to tip):
    - [GR_BASE_HEIGHT - top_chamf, GR_BASE_HEIGHT]: top 45° chamfer (inset grows toward tip)
    - [GR_BOX_CHAMF_H, GR_BASE_HEIGHT - top_chamf]: straight section
    - [0, GR_BOX_CHAMF_H]: bottom 45° chamfer (inset continues to tip)

    The max inset at z=0 is: GR_BOX_CHAMF_H + (top_chamf_height)
    where top_chamf_height = GR_BASE_HEIGHT - GR_BOX_CHAMF_H - GR_STR_H
    """
    if z <= 0:
        # Below foot: use max inset
        z = 0.0
    if z >= GR_BASE_HEIGHT:
        # At or above foot base: zero inset
        return 0.0

    # Profile heights
    z_bot_chamf_end = GR_BOX_CHAMF_H  # 0.8mm
    z_str_end = GR_BOX_CHAMF_H + GR_STR_H  # 2.6mm
    z_top = GR_BASE_HEIGHT  # 4.75mm

    # Top chamfer height
    top_chamf_h = z_top - z_str_end  # 2.15mm

    if z >= z_str_end:
        # Top chamfer region: inset grows linearly from 0 at z_top to GR_BOX_CHAMF_H at z_str_end
        # But wait - this doesn't match! Let me reconsider.
        # At z=z_top (4.75): inset = 0 (foot base, full size)
        # At z=z_str_end (2.6): inset = top_chamf_h = 2.15
        return z_top - z  # Linear from 0 at top to 2.15 at z_str_end
    elif z >= z_bot_chamf_end:
        # Straight section: constant inset = top_chamf_h
        return top_chamf_h
    else:
        # Bottom chamfer: inset continues growing
        # At z=z_bot_chamf_end (0.8): inset = top_chamf_h = 2.15
        # At z=0: inset = top_chamf_h + z_bot_chamf_end = 2.15 + 0.8 = 2.95
        return top_chamf_h + (z_bot_chamf_end - z)


def micro_foot_offsets(micro_divisions: int, pitch: float = GRU) -> List[Tuple[float, float]]:
    """Return micro-foot center offsets relative to 1U cell center.

    For micro_divisions=4, pitch=42:
    - micro_pitch = 10.5
    - offsets at: [-15.75, -5.25, 5.25, 15.75] in each axis
    - 16 micro-feet total
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


def cell_cutter_cross_section_shapely(
    z: float,
    pitch: float,
    micro_divisions: int,
    points_per_corner: int = 8,
) -> Union[Polygon, MultiPolygon]:
    """Compute the cutter cross-section at height z using Shapely boolean.

    The cross-section is F1 - Fm (1U foot minus micro-feet union).
    Uses Shapely for robust boolean operations that handle edge cases
    where micro-feet touch the outer boundary.

    Args:
        z: Height from bottom (mm)
        pitch: 1U pitch (default 42mm)
        micro_divisions: Number of divisions (2 or 4)
        points_per_corner: Vertices per corner arc

    Returns:
        Shapely Polygon representing the cutter cross-section
    """
    from shapely.geometry import Polygon as ShapelyPolygon
    from shapely.ops import unary_union

    inset = compute_inset_at_z(z)

    # 1U foot dimensions at this Z
    foot_1u_size = compute_foot_size(pitch)
    foot_1u_size_at_z = foot_1u_size - 2 * inset
    radius_1u = compute_corner_radius(foot_1u_size)
    radius_1u_at_z = max(radius_1u - inset, 0.0)

    # Build 1U foot polygon
    outer_verts = sample_rounded_rect(
        width=foot_1u_size_at_z,
        height=foot_1u_size_at_z,
        radius=radius_1u_at_z,
        points_per_corner=points_per_corner,
        center=(0.0, 0.0),
    )
    outer_ring = list(map(tuple, outer_verts))
    if outer_ring[0] != outer_ring[-1]:
        outer_ring.append(outer_ring[0])
    f1 = ShapelyPolygon(outer_ring)

    # Micro-foot dimensions at this Z
    # Note: Micro-feet use different sizing than 1U feet:
    # - Size: pitch - GR_TOL - 2*GR_BASE_CLR (additional clearance between micro-feet)
    # - Radius: GR_RAD - GR_BASE_CLR (smaller radius than 1U feet)
    micro_pitch = pitch / micro_divisions
    micro_foot_size = compute_foot_size(micro_pitch) - 2 * GR_BASE_CLR
    micro_foot_size_at_z = micro_foot_size - 2 * inset
    # Micro-foot radius uses GR_RAD - GR_BASE_CLR instead of GR_RAD + GR_BASE_CLR
    radius_micro_base = GR_RAD - GR_BASE_CLR  # 3.75mm
    radius_micro = min(radius_micro_base, micro_foot_size / 2.0 - 0.05)
    radius_micro = max(radius_micro, 0.2)  # Minimum radius
    radius_micro_at_z = max(radius_micro - inset, 0.0)

    # Build micro-feet polygons
    micro_feet = []
    for ox, oy in micro_foot_offsets(micro_divisions, pitch):
        if micro_foot_size_at_z > 0.1:  # Skip if foot collapsed
            verts = sample_rounded_rect(
                width=micro_foot_size_at_z,
                height=micro_foot_size_at_z,
                radius=radius_micro_at_z,
                points_per_corner=points_per_corner,
                center=(ox, oy),
            )
            ring = list(map(tuple, verts))
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            micro_feet.append(ShapelyPolygon(ring))

    # Compute F1 - Fm
    if micro_feet:
        fm = unary_union(micro_feet)
        cutter_shape = f1.difference(fm)
    else:
        cutter_shape = f1

    return cutter_shape  # type: ignore[return-value]


def generate_cell_cutter(
    pitch: float = GRU,
    micro_divisions: int = 4,
    epsilon: float = 0.02,
    points_per_corner: int = 8,
) -> Optional[trimesh.Trimesh]:
    """Generate cutter for a single 1U cell using CadQuery.

    Uses CadQuery-based generation for proper 45-degree chamfers that
    exactly match microfinity's foot geometry.

    Args:
        pitch: 1U pitch (default 42mm) - currently only 42mm is supported
        micro_divisions: Number of divisions (1, 2, or 4)
        epsilon: Coplanar avoidance offset (mm)
        points_per_corner: Ignored (kept for API compatibility)

    Returns:
        trimesh.Trimesh for the cell cutter, or None if micro_divisions=1
    """
    if micro_divisions <= 1:
        return None  # No cutting needed

    if pitch != GRU:
        raise ValueError(f"Only pitch={GRU} is supported, got {pitch}")

    from meshcutter.core.cq_cutter import generate_cell_cutter_cq, cq_to_trimesh

    cq_cutter = generate_cell_cutter_cq(micro_divisions, epsilon)
    return cq_to_trimesh(cq_cutter)


def detect_cell_centers_from_footprint(
    footprint: Union[Polygon, MultiPolygon],
    pitch: float = GRU,
) -> List[Tuple[float, float]]:
    """Detect 1U cell centers from footprint polygon.

    Uses Gridfinity convention: overall_dim ≈ N * pitch - GR_TOL
    So: N = round((dim + GR_TOL) / pitch)

    Assumes axis-aligned rectangular Gridfinity footprint.

    Args:
        footprint: Shapely polygon of bottom footprint
        pitch: 1U pitch (default 42mm)

    Returns:
        List of (x, y) cell center coordinates
    """
    bounds = footprint.bounds  # (minx, miny, maxx, maxy)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]

    # Gridfinity convention: overall_dim ≈ N * pitch - GR_TOL
    cells_x = int(round((width + GR_TOL) / pitch))
    cells_y = int(round((height + GR_TOL) / pitch))

    # Ensure at least 1 cell in each dimension
    cells_x = max(1, cells_x)
    cells_y = max(1, cells_y)

    # Centers arranged symmetrically within footprint
    cx = (bounds[0] + bounds[2]) / 2.0
    cy = (bounds[1] + bounds[3]) / 2.0

    centers = []
    for i in range(cells_x):
        for j in range(cells_y):
            x = cx + (i - (cells_x - 1) / 2.0) * pitch
            y = cy + (j - (cells_y - 1) / 2.0) * pitch
            centers.append((x, y))

    return centers


def detect_cell_centers(
    footprint: Union[Polygon, MultiPolygon],
    pitch: float = GRU,
    mesh_bounds: Optional[np.ndarray] = None,
) -> List[Tuple[float, float]]:
    """Detect 1U cell centers from footprint, optionally using mesh bounds for sizing.

    For Gridfinity models, the footprint detected at Z=0 may be smaller than
    the actual foot base due to chamfers. If mesh_bounds is provided, we use
    the XY extent of the mesh bounds for calculating the number of cells.

    IMPORTANT: The returned centers are in LOCAL FRAME coordinates (same as footprint).
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
    # This ensures cell centers are in the correct coordinate system for
    # transformation to world coordinates via frame.to_transform_matrix()
    fp_bounds = footprint.bounds
    cx = (fp_bounds[0] + fp_bounds[2]) / 2.0
    cy = (fp_bounds[1] + fp_bounds[3]) / 2.0

    if mesh_bounds is not None:
        # Use mesh bounds for dimensions (captures full foot size)
        # This gives accurate cell count even if footprint is smaller due to chamfers
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


def convert_to_micro_feet(
    input_mesh: trimesh.Trimesh,
    micro_divisions: int = 4,
    pitch: float = GRU,
    use_replace_base: bool = True,
) -> Optional[trimesh.Trimesh]:
    """Convert a 1U Gridfinity box to micro-divided feet.

    This is the main high-level API for converting standard Gridfinity boxes
    with 1U (42mm) feet into micro-divided versions with smaller feet.

    Two approaches are available:

    1. Replace Base (default, recommended):
       - Trims the input mesh above the foot region (z >= 5mm)
       - Generates fresh micro-feet base using microfinity's construction path
       - Unions the trimmed top with the new base
       - Produces EXACT geometric match with natively-generated micro boxes
       - Limitation: Removes everything below z=5mm (magnet holes, screw holes, etc.)

    2. Boolean Subtraction (legacy):
       - Generates a cutter shape (1U foot - micro feet union)
       - Subtracts the cutter from the input mesh
       - Preserves features below z=5mm (holes, text, etc.)
       - May have small geometric residuals (~50mm³) due to mesh boolean artifacts

    Args:
        input_mesh: Input mesh with standard 1U feet
        micro_divisions: Number of divisions per 1U (2 or 4)
        pitch: 1U pitch (42mm)
        use_replace_base: If True (default), use the replace-base approach.
                         If False, use legacy boolean subtraction.

    Returns:
        Output mesh with micro-feet, or None if conversion fails
    """
    from meshcutter.core.detection import detect_aligned_frame
    from meshcutter.core.boolean import boolean_difference

    if micro_divisions <= 1:
        return input_mesh.copy()  # No conversion needed

    if use_replace_base:
        # Use the new replace-base pipeline for exact geometric match
        from meshcutter.core.replace_base import replace_base_pipeline

        frame, footprint = detect_aligned_frame(input_mesh, force_z_up=True)

        return replace_base_pipeline(
            input_mesh=input_mesh,
            footprint=footprint,
            frame=frame,
            micro_divisions=micro_divisions,
            pitch=pitch,
            mesh_bounds=input_mesh.bounds,
        )
    else:
        # Use legacy boolean subtraction (preserves holes but has residuals)
        frame, footprint = detect_aligned_frame(input_mesh, force_z_up=True)

        cutter = generate_microgrid_cutter(
            footprint=footprint,
            frame=frame,
            micro_divisions=micro_divisions,
            pitch=pitch,
            mesh_bounds=input_mesh.bounds,
            add_channels=True,
        )

        if cutter is None:
            return input_mesh.copy()

        result = boolean_difference(part=input_mesh, cutter=cutter)
        return result.mesh


def generate_microgrid_cutter(
    footprint: Union[Polygon, MultiPolygon],
    frame: BottomFrame,
    micro_divisions: int = 4,
    pitch: float = GRU,
    epsilon: float = 0.02,
    points_per_corner: int = 8,
    mesh_bounds: Optional[np.ndarray] = None,
    overshoot: float = 0.0,
    wall_cut: float = 0.0,
    add_channels: bool = False,
) -> Optional[trimesh.Trimesh]:
    """Generate complete cutter for all 1U cells using CadQuery.

    Pipeline:
    1. Detect 1U cell centers from footprint/mesh bounds
    2. Build full grid cutter in CadQuery (one solid)
    3. Export to trimesh once
    4. Transform to world coordinates

    This approach minimizes triangle boolean operations by doing all
    unions in CadQuery (B-rep) before tessellation.

    Args:
        footprint: Shapely polygon of bottom footprint (local coords)
        frame: BottomFrame for world transform
        micro_divisions: Number of divisions (1, 2, or 4)
        pitch: 1U pitch (default 42mm)
        epsilon: Coplanar avoidance offset (mm)
        points_per_corner: Ignored (kept for API compatibility)
        mesh_bounds: Optional original mesh bounds for accurate cell detection
        overshoot: Extension beyond F1 boundary to cut outer walls (mm).
                   Set to 1.0-2.0mm to cut through outer foot walls.
        wall_cut: Shrink micro-feet to cut outer walls (mm).
                  Set to 0.5-1.0 to create cutter overlap with model edge.
        add_channels: If True, add inter-cell channel cutters to cut material
                      between adjacent cells. Only needed for solid-walled 1U
                      boxes. Default False.

    Returns:
        trimesh.Trimesh cutter in world coordinates, or None if micro_divisions=1
    """
    if micro_divisions <= 1:
        return None  # No cutting needed

    if pitch != GRU:
        raise ValueError(f"Only pitch={GRU} is supported, got {pitch}")

    # Detect cell centers (use mesh bounds if available for full foot coverage)
    centers = detect_cell_centers(footprint, pitch, mesh_bounds)

    if not centers:
        raise ValueError("No cells detected in footprint")

    from meshcutter.core.cq_cutter import generate_grid_cutter_mesh

    # Compute footprint bounds for clipping channels/boundary fill to model footprint.
    # IMPORTANT: Use mesh_bounds (full model extent at foot base) NOT footprint bounds
    # (which is at Z=0 foot tip where feet are narrower due to chamfer).
    # This prevents the cutter from extending beyond the model and clipping corners.
    if mesh_bounds is not None:
        # mesh_bounds is in world coords; footprint/centers are in local coords
        # For a Z-aligned model, the XY extent is the same in both coord systems
        footprint_bounds = (
            float(mesh_bounds[0, 0]),  # x_min
            float(mesh_bounds[0, 1]),  # y_min
            float(mesh_bounds[1, 0]),  # x_max
            float(mesh_bounds[1, 1]),  # y_max
        )
    else:
        # Fallback to footprint bounds (may cause corner clipping)
        fp_bounds = footprint.bounds  # (minx, miny, maxx, maxy)
        footprint_bounds = (fp_bounds[0], fp_bounds[1], fp_bounds[2], fp_bounds[3])

    # Build grid cutter from individual cell meshes (watertight cells)
    cutter_local = generate_grid_cutter_mesh(
        centers,
        micro_divisions,
        epsilon,
        overshoot=overshoot,
        wall_cut=wall_cut,
        add_channels=add_channels,
        footprint_bounds=footprint_bounds,
    )

    # Transform to world coordinates
    T = frame.to_transform_matrix()
    cutter_world = cutter_local.copy()
    cutter_world.apply_transform(T)

    return cutter_world
