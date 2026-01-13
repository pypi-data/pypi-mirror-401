#! /usr/bin/env python3
#
# meshcutter.core.cutter - 2D to 3D extrusion for cutter mesh generation
#

from __future__ import annotations

from typing import List, Optional, Union

import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

from meshcutter.core.detection import BottomFrame
from meshcutter.core.profile import CutterProfile, get_profile, PROFILE_RECTANGULAR


# Penetration below the bottom plane to avoid coplanar boolean degeneracy.
# The cutter will extend from z = -epsilon up to z = +depth in local coordinates.
COPLANAR_EPSILON = 0.02  # mm


def generate_cutter(
    grid_mask: Union[Polygon, MultiPolygon],
    frame: BottomFrame,
    depth: float,
    epsilon: float = COPLANAR_EPSILON,
) -> trimesh.Trimesh:
    """
    Generate a 3D cutter mesh from a 2D grid mask polygon.

    This function extrudes the 2D grid mask upward into the part to create
    a solid mesh suitable for boolean difference operations.

    Strategy:
        1. Extrude the 2D polygon in local +Z direction into the part by `depth`
        2. Extend cutter slightly below the bottom plane by `epsilon` (coplanar avoidance)
        3. Transform from local frame to world coordinates

    The resulting cutter in world coordinates spans approximately:
        z_range = [z_min - epsilon, z_min + depth]

    Args:
        grid_mask: Shapely Polygon/MultiPolygon in local 2D coordinates
        frame: BottomFrame defining the local coordinate system
        depth: Extrusion depth in mm (positive value, extruded upward into part)
        epsilon: Penetration below bottom plane in mm (avoids coplanar faces)

    Returns:
        trimesh.Trimesh in world coordinates

    Raises:
        ValueError: If extrusion fails or produces invalid mesh
    """
    if depth <= 0:
        raise ValueError(f"depth must be positive, got {depth}")
    if epsilon < 0:
        raise ValueError(f"epsilon must be non-negative, got {epsilon}")

    # Handle MultiPolygon by creating meshes for each and combining
    if isinstance(grid_mask, MultiPolygon):
        meshes = []
        for poly in grid_mask.geoms:
            if poly.is_valid and poly.area > 1e-6:
                mesh = _extrude_polygon(poly, depth, epsilon)
                if mesh is not None:
                    meshes.append(mesh)

        if not meshes:
            raise ValueError("No valid meshes created from MultiPolygon")

        # Concatenate all meshes
        cutter_local = trimesh.util.concatenate(meshes)
    else:
        cutter_local = _extrude_polygon(grid_mask, depth, epsilon)
        if cutter_local is None:
            raise ValueError("Failed to extrude polygon")

    # Transform local cutter into world coordinates
    # Local z=0 corresponds to the bottom plane (frame.origin)
    T = frame.to_transform_matrix()

    cutter_world = cutter_local.copy()
    cutter_world.apply_transform(T)

    # Validate result
    if len(cutter_world.faces) == 0:
        raise ValueError("Cutter mesh has no faces")

    return cutter_world


def _extrude_polygon(poly: Polygon, depth: float, epsilon: float) -> Optional[trimesh.Trimesh]:
    """
    Extrude a single 2D polygon to a 3D mesh.

    The polygon is extruded from Z=-epsilon to Z=+depth in local frame.
    This creates a cutter that:
    - Penetrates slightly below the bottom plane (by epsilon)
    - Extends upward into the part (by depth)

    Args:
        poly: Shapely Polygon (can have holes)
        depth: Extrusion depth upward into part (positive value)
        epsilon: Penetration below bottom plane (>= 0)

    Returns:
        trimesh.Trimesh or None if extrusion fails
    """
    try:
        # Total height includes both the upward depth and downward penetration
        height = depth + epsilon

        # extrude_polygon extrudes in +Z direction: creates mesh from Z=0 to Z=height
        mesh = trimesh.creation.extrude_polygon(poly, height=height)

        if mesh is None or len(mesh.faces) == 0:
            return None

        # Shift so cutter spans [-epsilon, +depth] in local Z
        # Currently spans [0, height], need to shift down by epsilon
        if epsilon != 0:
            mesh.apply_translation([0, 0, -epsilon])

        return mesh

    except Exception:
        return None


def validate_cutter(cutter: trimesh.Trimesh) -> dict:
    """
    Validate a cutter mesh and return diagnostic info.

    Args:
        cutter: The cutter mesh to validate

    Returns:
        Dictionary with validation results
    """
    return {
        "is_watertight": cutter.is_watertight,
        "is_winding_consistent": cutter.is_winding_consistent,
        "face_count": len(cutter.faces),
        "vertex_count": len(cutter.vertices),
        "bounds_min": cutter.bounds[0].tolist(),
        "bounds_max": cutter.bounds[1].tolist(),
        "volume": cutter.volume if cutter.is_watertight else None,
    }


def estimate_cutter_bounds(
    grid_mask: Union[Polygon, MultiPolygon],
    frame: BottomFrame,
    depth: float,
    epsilon: float = COPLANAR_EPSILON,
) -> dict:
    """
    Estimate the bounds of the cutter without actually creating it.

    Useful for validation and verbose output.

    Args:
        grid_mask: Shapely Polygon/MultiPolygon in local 2D coordinates
        frame: BottomFrame defining the local coordinate system
        depth: Extrusion depth in mm
        epsilon: Penetration below bottom plane in mm

    Returns:
        Dictionary with estimated bounds info
    """
    # Get 2D bounds
    bounds_2d = grid_mask.bounds  # (minx, miny, maxx, maxy)

    # Convert corners to 3D local coordinates
    # Cutter spans from z=-epsilon to z=+depth
    corners_local = np.array(
        [
            [bounds_2d[0], bounds_2d[1], -epsilon],
            [bounds_2d[2], bounds_2d[1], -epsilon],
            [bounds_2d[2], bounds_2d[3], -epsilon],
            [bounds_2d[0], bounds_2d[3], -epsilon],
            [bounds_2d[0], bounds_2d[1], depth],
            [bounds_2d[2], bounds_2d[1], depth],
            [bounds_2d[2], bounds_2d[3], depth],
            [bounds_2d[0], bounds_2d[3], depth],
        ]
    )

    # Transform to world
    corners_world = frame.local_to_world(corners_local)

    return {
        "local_bounds_2d": bounds_2d,
        "local_z_range": (-epsilon, depth),
        "world_min": corners_world.min(axis=0).tolist(),
        "world_max": corners_world.max(axis=0).tolist(),
        "grid_mask_area": grid_mask.area,
        "estimated_volume": grid_mask.area * (depth + epsilon),
    }


def generate_profiled_cutter(
    grid_mask: Union[Polygon, MultiPolygon],
    frame: BottomFrame,
    profile: Union[str, CutterProfile] = PROFILE_RECTANGULAR,
    depth: Optional[float] = None,
    epsilon: float = COPLANAR_EPSILON,
    n_slices: int = 10,
    mitre_limit: float = 5.0,
    simplify_tolerance: float = 0.01,
) -> trimesh.Trimesh:
    """
    Generate a 3D cutter mesh with a chamfered/profiled sidewall.

    This function creates a cutter that matches the Gridfinity base profile
    by stacking multiple extruded slabs with progressive insets.

    Strategy:
        1. Sample Z levels from the profile
        2. For each Z level, compute the inset and buffer the polygon inward
        3. Extrude each slab between consecutive Z levels
        4. Concatenate all slabs (union if manifold3d available)
        5. Transform to world coordinates

    Args:
        grid_mask: Shapely Polygon/MultiPolygon in local 2D coordinates
        frame: BottomFrame defining the local coordinate system
        profile: Profile name ("rect", "gridfinity") or CutterProfile instance
        depth: Override depth (uses profile's depth if None)
        epsilon: Penetration below bottom plane in mm
        n_slices: Number of Z slices for profile approximation
        mitre_limit: Mitre limit for buffer operation (prevents spikes)
        simplify_tolerance: Tolerance for polygon simplification (reduces noise)

    Returns:
        trimesh.Trimesh in world coordinates

    Raises:
        ValueError: If extrusion fails or produces invalid mesh
    """
    # Get profile
    if isinstance(profile, str):
        profile_obj = get_profile(profile, depth if depth is not None else 4.75)
    else:
        profile_obj = profile

    # Use profile's total height if depth not specified
    if depth is None:
        depth = profile_obj.total_height

    if depth <= 0:
        raise ValueError(f"depth must be positive, got {depth}")
    if epsilon < 0:
        raise ValueError(f"epsilon must be non-negative, got {epsilon}")

    # Simplify the mask slightly to reduce micro-zigzags that create bad miters
    if simplify_tolerance > 0:
        simplified_mask = grid_mask.simplify(simplify_tolerance, preserve_topology=True)
        if simplified_mask.is_valid and not simplified_mask.is_empty:
            grid_mask = simplified_mask

    # Get Z levels
    z_levels = profile_obj.sample_z_levels(n_slices=n_slices, epsilon=epsilon)

    # Ensure we have the full depth
    if z_levels[-1] < depth:
        z_levels.append(depth)

    # Generate slabs
    slabs: List[trimesh.Trimesh] = []

    for i in range(len(z_levels) - 1):
        z_bottom = z_levels[i]
        z_top = z_levels[i + 1]
        slab_height = z_top - z_bottom

        if slab_height <= 0:
            continue

        # Compute inset at bottom of this slab
        # (conservative: use the larger inset to avoid boolean issues)
        inset = profile_obj.inset_at(max(0, z_bottom))

        # Buffer the polygon inward
        if inset > 0:
            buffered = grid_mask.buffer(
                -inset,
                join_style="mitre",
                mitre_limit=mitre_limit,
            )
        else:
            buffered = grid_mask

        # Skip if polygon collapsed
        if buffered.is_empty:
            continue

        # Handle invalid geometry
        if not buffered.is_valid:
            from shapely.validation import make_valid

            buffered = make_valid(buffered)
            if buffered.is_empty:
                continue

        # Extrude this slab
        slab_meshes = _extrude_geometry(buffered, slab_height)

        if not slab_meshes:
            continue

        # Translate to correct Z position
        for mesh in slab_meshes:
            mesh.apply_translation([0, 0, z_bottom])

        slabs.extend(slab_meshes)

    if not slabs:
        raise ValueError("No valid slabs created for profiled cutter")

    # Concatenate all slabs
    cutter_local = trimesh.util.concatenate(slabs)

    # Try to union/merge if manifold3d is available (cleaner result)
    cutter_local = _try_union_slabs(cutter_local)

    # Transform to world coordinates
    T = frame.to_transform_matrix()
    cutter_world = cutter_local.copy()
    cutter_world.apply_transform(T)

    if len(cutter_world.faces) == 0:
        raise ValueError("Profiled cutter mesh has no faces")

    return cutter_world


def _extrude_geometry(geom, height: float) -> List[trimesh.Trimesh]:
    """
    Extrude a Shapely geometry (Polygon or MultiPolygon) to 3D meshes.

    Args:
        geom: Shapely geometry
        height: Extrusion height

    Returns:
        List of trimesh.Trimesh objects
    """
    meshes = []

    if isinstance(geom, MultiPolygon):
        for poly in geom.geoms:
            if isinstance(poly, Polygon) and poly.is_valid and poly.area > 1e-6:
                mesh = _extrude_single_polygon(poly, height)
                if mesh is not None:
                    meshes.append(mesh)
    elif isinstance(geom, Polygon):
        if geom.is_valid and geom.area > 1e-6:
            mesh = _extrude_single_polygon(geom, height)
            if mesh is not None:
                meshes.append(mesh)
    # Handle GeometryCollection or other types
    elif hasattr(geom, "geoms"):
        for g in geom.geoms:
            meshes.extend(_extrude_geometry(g, height))

    return meshes


def _extrude_single_polygon(poly: Polygon, height: float) -> Optional[trimesh.Trimesh]:
    """Extrude a single polygon to a mesh."""
    try:
        mesh = trimesh.creation.extrude_polygon(poly, height=height)
        if mesh is not None and len(mesh.faces) > 0:
            return mesh
    except Exception:
        pass
    return None


def _try_union_slabs(cutter: trimesh.Trimesh) -> trimesh.Trimesh:
    """
    Try to union/merge the slab meshes for a cleaner result.

    Uses manifold3d if available, otherwise just merges vertices.
    """
    try:
        # Try manifold3d union
        import manifold3d

        m = manifold3d.Manifold.from_mesh(cutter.vertices, cutter.faces)
        # Self-union to clean up
        mesh_out = m.to_mesh()
        return trimesh.Trimesh(vertices=mesh_out.vert_properties, faces=mesh_out.tri_verts)
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: just merge vertices and remove degenerate faces
    try:
        cutter.merge_vertices()
        cutter.remove_degenerate_faces()
        cutter.remove_duplicate_faces()
    except Exception:
        pass

    return cutter
