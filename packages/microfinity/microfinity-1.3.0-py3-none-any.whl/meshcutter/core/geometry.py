#! /usr/bin/env python3
#
# meshcutter.core.geometry - Geometry helpers for foot cutter generation
#
# Provides topology-stable rounded rectangle generation and polygon-with-holes
# lofting for constructing Gridfinity foot complement cutters.

from __future__ import annotations

from typing import List, Tuple, Optional

import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import triangulate


def sample_rounded_rect(
    width: float,
    height: float,
    radius: float,
    points_per_corner: int = 8,
    center: Tuple[float, float] = (0.0, 0.0),
) -> np.ndarray:
    """
    Generate CCW vertices for a rounded rectangle.

    Topology-stable:
    - Always returns same vertex count regardless of radius
    - When radius approaches 0, corner arcs collapse but vertex count unchanged
    - No duplicate closing point (open ring)
    - Guaranteed CCW ordering

    Args:
        width: Total width of rectangle (mm)
        height: Total height of rectangle (mm)
        radius: Corner radius (mm), clamped to valid range
        points_per_corner: Number of points per corner arc (default: 8)
        center: Center point (x, y)

    Returns:
        np.ndarray of shape (N, 2) with CCW-ordered vertices (open ring)
        N = 4 * points_per_corner (corners) + 4 (straight midpoints)
    """
    cx, cy = center

    # Clamp radius to valid range
    max_radius = min(width, height) / 2.0 - 1e-6
    r = max(0.0, min(radius, max_radius))

    # Half-dimensions minus radius gives corner centers
    hw = width / 2.0
    hh = height / 2.0

    # Corner centers (CCW from bottom-right)
    corners = [
        (cx + hw - r, cy - hh + r),  # bottom-right
        (cx + hw - r, cy + hh - r),  # top-right
        (cx - hw + r, cy + hh - r),  # top-left
        (cx - hw + r, cy - hh + r),  # bottom-left
    ]

    # Start angles for each corner (CCW)
    start_angles = [
        -np.pi / 2,  # bottom-right: -90° to 0°
        0,  # top-right: 0° to 90°
        np.pi / 2,  # top-left: 90° to 180°
        np.pi,  # bottom-left: 180° to 270°
    ]

    vertices = []

    for i, (corner_cx, corner_cy) in enumerate(corners):
        start_angle = start_angles[i]
        # Generate arc points for this corner
        for j in range(points_per_corner):
            t = j / points_per_corner
            angle = start_angle + t * (np.pi / 2)
            if r > 1e-9:
                x = corner_cx + r * np.cos(angle)
                y = corner_cy + r * np.sin(angle)
            else:
                # Radius is ~0, all points collapse to corner
                # Still generate same count for topology stability
                x = corner_cx
                y = corner_cy
            vertices.append((x, y))

        # Add straight edge midpoint after each corner arc
        # This helps with triangulation and edge correspondence
        if i == 0:
            # Right edge midpoint
            vertices.append((cx + hw, cy))
        elif i == 1:
            # Top edge midpoint
            vertices.append((cx, cy + hh))
        elif i == 2:
            # Left edge midpoint
            vertices.append((cx - hw, cy))
        elif i == 3:
            # Bottom edge midpoint
            vertices.append((cx, cy - hh))

    return np.array(vertices, dtype=np.float64)


def reverse_winding(vertices: np.ndarray) -> np.ndarray:
    """Reverse vertex winding order (CCW <-> CW)."""
    return vertices[::-1].copy()


def triangulate_polygon_with_holes(
    outer: np.ndarray,
    holes: List[np.ndarray],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Triangulate a polygon with holes using earcut algorithm.

    Args:
        outer: CCW vertices of outer boundary (N, 2)
        holes: List of CW vertices for each hole (each is (M, 2))

    Returns:
        (vertices, faces) tuple for a 2D triangulated mesh
    """
    try:
        import mapbox_earcut as earcut
    except ImportError:
        # Fallback to trimesh's built-in earcut
        earcut = None

    # Build vertex array: outer ring followed by all holes
    all_vertices = list(outer)
    ring_ends = [len(outer)]

    for hole in holes:
        all_vertices.extend(hole)
        ring_ends.append(len(all_vertices))

    vertices = np.array(all_vertices, dtype=np.float64)

    if earcut is not None:
        # Use mapbox_earcut directly
        # ring_ends defines where each ring ends (exclusive)
        # earcut expects a 2D array of vertices and array of ring end indices
        # The last value must equal the total number of vertices
        ring_array = np.array(ring_ends, dtype=np.uint32)

        # earcut returns flat array of triangle indices
        indices = earcut.triangulate_float64(vertices, ring_array)

        faces = np.array(indices, dtype=np.int64).reshape(-1, 3)
        return vertices, faces
    else:
        # Fallback: build Shapely polygon and use trimesh
        outer_ring = list(map(tuple, outer))
        if outer_ring[0] != outer_ring[-1]:
            outer_ring = outer_ring + [outer_ring[0]]

        hole_rings = []
        for hole in holes:
            hole_ring = list(map(tuple, hole))
            if hole_ring[0] != hole_ring[-1]:
                hole_ring = hole_ring + [hole_ring[0]]
            hole_rings.append(hole_ring)

        poly = Polygon(outer_ring, hole_rings)

        if not poly.is_valid:
            # Try to fix with buffer(0)
            poly = poly.buffer(0)

        if poly.is_empty or not hasattr(poly, "exterior"):
            raise ValueError("Invalid polygon for triangulation")

        # Use trimesh's triangulation
        try:
            verts, faces = trimesh.creation.triangulate_polygon(poly, engine="earcut")
            return np.array(verts), np.array(faces)
        except Exception as e:
            raise ValueError(f"Failed to triangulate polygon: {e}")


def loft_polygon_with_holes(
    rings: List[Tuple[float, np.ndarray, List[np.ndarray]]],
) -> trimesh.Trimesh:
    """
    Loft a polygon-with-holes through multiple Z levels.

    Creates a watertight solid by:
    1. Connecting corresponding vertices between consecutive Z rings (side faces)
    2. Adding triangulated caps at top and bottom (using ring vertices)

    Args:
        rings: List of (z, outer_verts, [hole_verts, ...]) tuples
               - z: Z coordinate for this ring
               - outer_verts: CCW vertices (N, 2) for outer boundary
               - hole_verts: List of CW vertices for holes

    Returns:
        Watertight trimesh.Trimesh solid

    Raises:
        ValueError: If rings have inconsistent topology
    """
    if len(rings) < 2:
        raise ValueError("Need at least 2 rings to loft")

    # Validate topology consistency
    n_outer = len(rings[0][1])
    n_holes = len(rings[0][2])
    hole_sizes = [len(h) for h in rings[0][2]]

    for i, (z, outer, holes) in enumerate(rings):
        if len(outer) != n_outer:
            raise ValueError(f"Ring {i} has {len(outer)} outer vertices, expected {n_outer}")
        if len(holes) != n_holes:
            raise ValueError(f"Ring {i} has {len(holes)} holes, expected {n_holes}")
        for j, h in enumerate(holes):
            if len(h) != hole_sizes[j]:
                raise ValueError(f"Ring {i} hole {j} has {len(h)} vertices, expected {hole_sizes[j]}")

    all_vertices = []
    all_faces = []

    # Build 3D vertices for all rings
    ring_vertex_offsets = []
    for z, outer, holes in rings:
        offset = len(all_vertices)
        ring_vertex_offsets.append(offset)

        # Add outer boundary vertices
        for x, y in outer:
            all_vertices.append([x, y, z])

        # Add hole vertices
        for hole in holes:
            for x, y in hole:
                all_vertices.append([x, y, z])

    # Create side faces between consecutive rings
    for ring_idx in range(len(rings) - 1):
        offset_a = ring_vertex_offsets[ring_idx]
        offset_b = ring_vertex_offsets[ring_idx + 1]

        # Outer boundary side faces (CCW outer = outward normal)
        for i in range(n_outer):
            i_next = (i + 1) % n_outer
            v0 = offset_a + i
            v1 = offset_a + i_next
            v2 = offset_b + i_next
            v3 = offset_b + i
            # Outer faces: normal points outward (away from center)
            # For CCW outer ring, going up (a->b), we want CCW when viewed from outside
            all_faces.append([v0, v1, v2])
            all_faces.append([v0, v2, v3])

        # Hole boundary side faces (CW holes = inward normal toward hole center)
        hole_offset_in_ring = n_outer
        for hole_idx, hole_size in enumerate(hole_sizes):
            for i in range(hole_size):
                i_next = (i + 1) % hole_size
                v0 = offset_a + hole_offset_in_ring + i
                v1 = offset_a + hole_offset_in_ring + i_next
                v2 = offset_b + hole_offset_in_ring + i_next
                v3 = offset_b + hole_offset_in_ring + i
                # Hole faces: normal points inward (toward hole center = outward from solid)
                # For CW hole ring, going up, we want faces pointing inward
                all_faces.append([v0, v2, v1])
                all_faces.append([v0, v3, v2])
            hole_offset_in_ring += hole_size

    # Add caps using triangulation, but reuse the ring vertices
    # Bottom cap (first ring, facing -Z)
    z_bottom, outer_bottom, holes_bottom = rings[0]
    offset_bottom = ring_vertex_offsets[0]

    # Triangulate to get face indices (relative to the combined vertex list)
    cap_verts, cap_faces = triangulate_polygon_with_holes(outer_bottom, holes_bottom)

    # Map triangulation vertices to ring vertices
    # The triangulation returns vertices in same order: outer, then holes
    # We need to map these back to the ring vertex indices
    total_ring_verts = n_outer + sum(hole_sizes)

    # Bottom cap faces (facing -Z, so reverse winding)
    for face in cap_faces:
        # Indices are into the triangulation vertex array, which matches ring vertex layout
        all_faces.append(
            [
                offset_bottom + face[0],
                offset_bottom + face[2],
                offset_bottom + face[1],
            ]
        )

    # Top cap (last ring, facing +Z)
    z_top, outer_top, holes_top = rings[-1]
    offset_top = ring_vertex_offsets[-1]

    cap_verts, cap_faces = triangulate_polygon_with_holes(outer_top, holes_top)

    # Top cap faces (facing +Z, normal winding)
    for face in cap_faces:
        all_faces.append(
            [
                offset_top + face[0],
                offset_top + face[1],
                offset_top + face[2],
            ]
        )

    vertices = np.array(all_vertices, dtype=np.float64)
    faces = np.array(all_faces, dtype=np.int64)

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Clean up the mesh
    mesh.merge_vertices()
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.update_faces(mesh.unique_faces())

    # Fix winding if volume is negative
    if mesh.volume < 0:
        mesh.invert()

    return mesh
