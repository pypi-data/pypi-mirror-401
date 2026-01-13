#! /usr/bin/env python3
#
# meshcutter.core.replace_base - Replace Base Pipeline for micro-foot conversion
#
# Instead of carving into existing geometry with booleans (which creates artifacts),
# this approach replaces the entire foot region:
#   1. Trim input mesh above z_split to keep only the top portion
#   2. Generate fresh micro-feet base directly (using microfinity construction path)
#   3. Union with overlapping sleeve interface (NOT coplanar join)
#
# This avoids the mesh boolean retessellation artifacts that caused ~50mm^3 residuals.

from __future__ import annotations

import tempfile
import os
from typing import List, Optional, Tuple, Union

import numpy as np
import trimesh
import manifold3d
import cadquery as cq
from cqkit.cq_helpers import rounded_rect_sketch, composite_from_pts
from shapely.geometry import Polygon, MultiPolygon

from microfinity.core.constants import (
    GR_BASE_CLR,
    GR_BASE_HEIGHT,
    GR_BOX_PROFILE,
    GR_RAD,
    GR_TOL,
    GRU,
    SQRT2,
)

from meshcutter.core.detection import BottomFrame

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
# Z_split is the plane where we cut between top (kept) and bottom (replaced)
# z_split = z_min + GR_BASE_HEIGHT + GR_BASE_CLR = z_min + 5.0mm
Z_SPLIT_HEIGHT = GR_BASE_HEIGHT + GR_BASE_CLR  # 4.75 + 0.25 = 5.0mm

# Sleeve height - how far the new base extends ABOVE z_split for overlap
# This is critical: overlap ensures robust union (no coplanar faces)
SLEEVE_HEIGHT = 0.5  # mm


# -----------------------------------------------------------------------------
# CadQuery version detection (from cq_cutter.py)
# -----------------------------------------------------------------------------
ZLEN_FIX = True
_r = cq.Workplane("XY").rect(2, 2).extrude(1, taper=45)
_bb = _r.vals()[0].BoundingBox()
if abs(_bb.zlen - 1.0) < 1e-3:
    ZLEN_FIX = False


def extrude_profile(sketch, profile, workplane="XY", angle=None) -> cq.Workplane:
    """Extrude a sketch through a multi-segment profile with optional tapers.

    Mirrors microfinity.core.base.GridfinityObject.extrude_profile().
    """
    import math

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
# Trimesh <-> Manifold conversion helpers
# -----------------------------------------------------------------------------
def trimesh_to_manifold(mesh: trimesh.Trimesh) -> manifold3d.Manifold:
    """Convert trimesh to manifold3d Manifold."""
    return manifold3d.Manifold(
        manifold3d.Mesh(
            vert_properties=np.array(mesh.vertices, dtype=np.float32), tri_verts=np.array(mesh.faces, dtype=np.uint32)
        )
    )


def manifold_to_trimesh(manifold: manifold3d.Manifold) -> trimesh.Trimesh:
    """Convert manifold3d Manifold to trimesh."""
    mesh_data = manifold.to_mesh()
    return trimesh.Trimesh(
        vertices=np.array(mesh_data.vert_properties, dtype=np.float64),
        faces=np.array(mesh_data.tri_verts, dtype=np.int64),
    )


def cq_to_trimesh(cq_obj: cq.Workplane, tol: float = 0.01, ang_tol: float = 0.1) -> trimesh.Trimesh:
    """Convert CadQuery Workplane to trimesh."""
    with tempfile.TemporaryDirectory() as tmpdir:
        stl_path = os.path.join(tmpdir, "temp.stl")
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
# Step 1: Trim mesh above z_split
# -----------------------------------------------------------------------------
def trim_mesh_above_z(mesh: trimesh.Trimesh, z_split: float) -> trimesh.Trimesh:
    """Trim mesh to keep only the portion above z_split.

    Uses Manifold's trimByPlane to extract the top portion of the mesh.
    The plane normal points downward (-Z) so material above z_split is kept.

    Args:
        mesh: Input mesh
        z_split: Z coordinate of the split plane

    Returns:
        Trimesh containing only geometry above z_split
    """
    manifold = trimesh_to_manifold(mesh)

    # trimByPlane keeps material in the positive half-space of the plane
    # Plane defined by normal and distance from origin along normal
    # To keep material ABOVE z_split, use normal=(0,0,-1), distance=-z_split
    # This keeps material where dot(vertex, normal) >= distance
    # i.e., -vertex.z >= -z_split => vertex.z <= z_split
    # Wait, that's wrong. Let me reconsider.
    #
    # trimByPlane(normal, originOffset): keeps vertices where dot(v, normal) >= originOffset
    # To keep v.z >= z_split: use normal=(0,0,1), originOffset=z_split
    trimmed = manifold.trim_by_plane(
        normal=(0.0, 0.0, 1.0), origin_offset=z_split  # Plane normal pointing up  # Keep material where z >= z_split
    )

    return manifold_to_trimesh(trimmed)


# -----------------------------------------------------------------------------
# Step 2: Generate micro-base with sleeve overlap
# -----------------------------------------------------------------------------
def generate_micro_foot_cq(micro_divisions: int = 4) -> cq.Workplane:
    """Generate a single micro-foot solid using CadQuery.

    Uses the same construction path as microfinity for geometric accuracy.
    """
    micro_pitch = GRU / micro_divisions  # 10.5mm for div=4
    foot_size = micro_pitch - GR_TOL  # 10.0mm for div=4

    # Corner radius - same as microfinity's micro_foot()
    outer_rad = GR_RAD - GR_TOL / 2  # 3.75mm
    rad = min(outer_rad + GR_BASE_CLR, foot_size / 2 - 0.05)
    rad = max(rad, 0.2)

    foot = extrude_profile(rounded_rect_sketch(foot_size, foot_size, rad), GR_BOX_PROFILE)
    foot = foot.translate((0, 0, -GR_BASE_CLR))
    foot = foot.mirror(mirrorPlane="XY")

    return foot


def micro_foot_offsets(
    cells_x: int, cells_y: int, micro_divisions: int = 4, pitch: float = GRU
) -> List[Tuple[float, float]]:
    """Return micro-foot center offsets for a grid of cells.

    Matches microfinity's micro_grid_centres calculation exactly.

    Args:
        cells_x: Number of 1U cells in X direction
        cells_y: Number of 1U cells in Y direction
        micro_divisions: Number of divisions per 1U (2 or 4)
        pitch: 1U pitch (42mm)

    Returns:
        List of (x, y) offsets for micro-foot centers
    """
    if micro_divisions <= 1:
        # Standard 1U grid
        return [(x * pitch, y * pitch) for x in range(cells_x) for y in range(cells_y)]

    micro_pitch = pitch / micro_divisions
    micro_count_x = cells_x * micro_divisions
    micro_count_y = cells_y * micro_divisions

    # Half extents (distance from center to edge foot centers)
    half_l = (cells_x - 1) * pitch / 2
    half_w = (cells_y - 1) * pitch / 2
    micro_half_l = (micro_count_x - 1) * micro_pitch / 2
    micro_half_w = (micro_count_y - 1) * micro_pitch / 2

    # Center the micro lattice on the cell grid center
    offsets = [
        (x * micro_pitch - micro_half_l + half_l, y * micro_pitch - micro_half_w + half_w)
        for x in range(micro_count_x)
        for y in range(micro_count_y)
    ]
    return offsets


def generate_micro_base_with_sleeve(
    cells_x: int,
    cells_y: int,
    micro_divisions: int = 4,
    z_base: float = 0.0,
    sleeve_height: float = SLEEVE_HEIGHT,
    pitch: float = GRU,
) -> trimesh.Trimesh:
    """Generate micro-feet base that extends above z_split by sleeve_height.

    This creates:
    1. Micro-feet at the correct positions (matching microfinity exactly)
    2. Outer envelope that crops the feet (41.5mm per cell)
    3. Wall sleeve that extends above z_split for overlap with trimmed top

    The geometry is generated in CadQuery for accuracy, then converted to trimesh.
    The final mesh is centered at origin in XY (same as microfinity output).

    Args:
        cells_x: Number of 1U cells in X direction
        cells_y: Number of 1U cells in Y direction
        micro_divisions: Number of divisions per 1U (2 or 4)
        z_base: Z coordinate of the base bottom (typically mesh z_min)
        sleeve_height: How far to extend above z_split (mm)
        pitch: 1U pitch (42mm)

    Returns:
        Trimesh of the micro-base with sleeve, centered at origin in XY
    """
    # Outer envelope dimensions (same as microfinity)
    outer_l = cells_x * pitch - GR_TOL  # 83.5mm for 2 cells
    outer_w = cells_y * pitch - GR_TOL  # 125.5mm for 3 cells
    outer_rad = GR_RAD - GR_TOL / 2  # 3.75mm

    # Half dimensions for internal grid centering (matches microfinity)
    # This is the offset from grid origin to the center of the grid
    half_l = (cells_x - 1) * pitch / 2  # 21mm for 2 cells
    half_w = (cells_y - 1) * pitch / 2  # 42mm for 3 cells

    # Generate micro-foot template
    micro_foot = generate_micro_foot_cq(micro_divisions)
    micro_foot_solid = micro_foot.val()

    # Replicate micro-feet at all positions
    # These offsets are in "internal" coordinates where grid starts at (0,0)
    offsets = micro_foot_offsets(cells_x, cells_y, micro_divisions, pitch)

    feet_union = None
    for ox, oy in offsets:
        instance = micro_foot_solid.translate(cq.Vector(ox, oy, 0))
        if feet_union is None:
            feet_union = instance
        else:
            feet_union = feet_union.fuse(instance)

    # Create outer envelope to crop feet
    # Envelope is centered at (half_l, half_w) in internal coords
    # This matches box.py: rc.translate((*self.half_dim, 0.5))
    crop_env = (
        cq.Workplane("XY")
        .placeSketch(rounded_rect_sketch(outer_l, outer_w, outer_rad))
        .extrude(-GR_BASE_HEIGHT - 1)
        .translate(cq.Vector(half_l, half_w, 0.5))
    )

    # Intersect feet with envelope
    cropped_feet = crop_env.val().intersect(feet_union)

    # Create wall sleeve that extends above the feet (if sleeve_height > 0)
    # Sleeve extends from z=GR_BASE_CLR (top of feet) to z=GR_BASE_CLR+sleeve_height
    if sleeve_height > 0.01:  # Use small threshold to avoid degenerate geometry
        sleeve = (
            cq.Workplane("XY")
            .placeSketch(rounded_rect_sketch(outer_l, outer_w, outer_rad))
            .extrude(sleeve_height)
            .translate(cq.Vector(half_l, half_w, GR_BASE_CLR))
        )
        # Union feet with sleeve
        base_solid = cropped_feet.fuse(sleeve.val())
    else:
        base_solid = cropped_feet

    # Translate to final position - center at origin in XY
    # In microfinity, render() does: translate((-self.half_l, -self.half_w, GR_BASE_HEIGHT))
    # We apply the XY centering here, and handle Z separately
    base_solid = base_solid.translate(cq.Vector(-half_l, -half_w, 0))

    base_cq = cq.Workplane("XY").newObject([base_solid])

    # Convert to trimesh
    mesh = cq_to_trimesh(base_cq, tol=0.01, ang_tol=0.1)

    # Adjust Z position
    # After the CQ operations, the mesh has:
    # - foot tip (narrow end) at z ≈ -4.75
    # - foot base + sleeve at z ≈ 0.25 + sleeve_height
    # We want foot tip at z_base
    z_min_mesh = mesh.vertices[:, 2].min()
    z_shift = z_base - z_min_mesh
    mesh.vertices[:, 2] += z_shift

    return mesh


# -----------------------------------------------------------------------------
# Step 3: Replace base pipeline
# -----------------------------------------------------------------------------
def replace_base_pipeline(
    input_mesh: trimesh.Trimesh,
    footprint: Union[Polygon, MultiPolygon],
    frame: BottomFrame,
    micro_divisions: int = 4,
    pitch: float = GRU,
    sleeve_height: float = SLEEVE_HEIGHT,
    mesh_bounds: Optional[np.ndarray] = None,
) -> trimesh.Trimesh:
    """Replace the foot region of input mesh with fresh micro-feet.

    This is the main entry point for the replace-base approach.

    Pipeline:
    1. Detect footprint and cell count from input mesh
    2. Compute z_split = z_min + 5.0mm
    3. Trim input to get top portion (above z_split)
    4. Generate micro-base with sleeve (extends above z_split)
    5. Union trimmed top + micro-base (overlap makes this robust)
    6. Validate result

    IMPORTANT LIMITATION: This replaces EVERYTHING below z_split.
    Magnet holes, screw holes, and embossed text on the base will be lost.

    Args:
        input_mesh: Input mesh with 1U feet
        footprint: Shapely polygon of detected footprint (local coords)
        frame: BottomFrame for coordinate transform
        micro_divisions: Number of divisions per 1U (2 or 4)
        pitch: 1U pitch (42mm)
        sleeve_height: Overlap height above z_split (mm)
        mesh_bounds: Optional mesh bounds for accurate cell detection

    Returns:
        Output mesh with micro-feet

    Raises:
        ValueError: If input is invalid or result fails validation
    """
    # Get mesh bounds
    if mesh_bounds is None:
        mesh_bounds = input_mesh.bounds

    z_min = float(mesh_bounds[0, 2])
    z_split = z_min + Z_SPLIT_HEIGHT

    # Detect cell count from footprint/bounds
    fp_bounds = footprint.bounds  # (minx, miny, maxx, maxy)

    # Use mesh bounds for dimensions (full foot coverage at base)
    width = mesh_bounds[1, 0] - mesh_bounds[0, 0]
    height = mesh_bounds[1, 1] - mesh_bounds[0, 1]

    # Gridfinity convention: overall_dim = N * pitch - GR_TOL
    cells_x = int(round((width + GR_TOL) / pitch))
    cells_y = int(round((height + GR_TOL) / pitch))
    cells_x = max(1, cells_x)
    cells_y = max(1, cells_y)

    print("Replace base pipeline:")
    print(f"  Input z_min: {z_min:.3f}mm, z_split: {z_split:.3f}mm")
    print(f"  Detected grid: {cells_x}x{cells_y} cells")
    print(f"  Micro divisions: {micro_divisions}")

    # Step 1: Trim input to keep top portion
    print(f"  Trimming input above z={z_split:.3f}...")
    trimmed_top = trim_mesh_above_z(input_mesh, z_split)
    print(f"    Trimmed top: {len(trimmed_top.vertices)} vertices, {len(trimmed_top.faces)} faces")

    # Verify trimmed top has reasonable geometry
    if len(trimmed_top.faces) < 10:
        raise ValueError(
            f"Trimmed top has too few faces ({len(trimmed_top.faces)}). "
            f"Check that z_split={z_split:.3f} is correct."
        )

    # Step 2: Generate micro-base with sleeve
    print(f"  Generating micro-base with {sleeve_height:.2f}mm sleeve...")

    # The micro-base needs to be positioned correctly:
    # - X/Y centered on the mesh (not necessarily at origin)
    # - Z starts at z_min (foot tip) and extends to z_split + sleeve_height

    # Get mesh center in XY
    mesh_center_x = (mesh_bounds[0, 0] + mesh_bounds[1, 0]) / 2
    mesh_center_y = (mesh_bounds[0, 1] + mesh_bounds[1, 1]) / 2

    micro_base = generate_micro_base_with_sleeve(
        cells_x=cells_x,
        cells_y=cells_y,
        micro_divisions=micro_divisions,
        z_base=z_min,
        sleeve_height=sleeve_height,
        pitch=pitch,
    )

    # The micro_base is already centered at origin by generate_micro_base_with_sleeve.
    # We only need to shift if the input mesh is NOT centered at origin.
    # For standard microfinity meshes, both are centered at origin.
    if abs(mesh_center_x) > 0.01 or abs(mesh_center_y) > 0.01:
        micro_base.vertices[:, 0] += mesh_center_x
        micro_base.vertices[:, 1] += mesh_center_y

    print(f"    Micro-base: {len(micro_base.vertices)} vertices, {len(micro_base.faces)} faces")
    print(f"    Base z range: [{micro_base.vertices[:, 2].min():.3f}, {micro_base.vertices[:, 2].max():.3f}]")

    # Step 3: Union trimmed top + micro-base
    print("  Performing union...")

    manifold_top = trimesh_to_manifold(trimmed_top)
    manifold_base = trimesh_to_manifold(micro_base)

    result_manifold = manifold_top + manifold_base
    result = manifold_to_trimesh(result_manifold)

    print(f"    Result: {len(result.vertices)} vertices, {len(result.faces)} faces")

    # Step 4: Validate result
    print("  Validating result...")

    if not result.is_watertight:
        print("    WARNING: Result is not watertight!")

    if result.volume <= 0:
        raise ValueError("Result has non-positive volume")

    # Check for tiny disconnected components
    components = result.split(only_watertight=False)
    if len(components) > 1:
        print(f"    WARNING: Result has {len(components)} disconnected components")
        # Keep only the largest component
        largest = max(components, key=lambda m: m.volume if m.is_watertight else 0)
        if largest.volume > result.volume * 0.9:
            print(f"    Keeping largest component (volume={largest.volume:.2f}mm^3)")
            result = largest
        else:
            print(f"    WARNING: Largest component is only {largest.volume/result.volume*100:.1f}% of total")

    print(f"  Done. Output volume: {result.volume:.2f}mm^3")

    return result


# -----------------------------------------------------------------------------
# High-level API
# -----------------------------------------------------------------------------
def convert_to_micro(
    input_mesh: trimesh.Trimesh,
    micro_divisions: int = 4,
) -> trimesh.Trimesh:
    """Convert a 1U Gridfinity box to micro-divided feet.

    This is a convenience wrapper that handles footprint detection
    and calls the replace_base_pipeline.

    Args:
        input_mesh: Input mesh with standard 1U feet
        micro_divisions: Number of divisions (2 or 4)

    Returns:
        Output mesh with micro-feet
    """
    from meshcutter.core.detection import detect_aligned_frame

    frame, footprint = detect_aligned_frame(input_mesh, force_z_up=True)

    return replace_base_pipeline(
        input_mesh=input_mesh,
        footprint=footprint,
        frame=frame,
        micro_divisions=micro_divisions,
        mesh_bounds=input_mesh.bounds,
    )
