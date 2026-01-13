#! /usr/bin/env python3
#
# meshcutter.core.detection - Bottom plane detection and footprint extraction
#

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Union

import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely.ops import unary_union
from shapely.validation import make_valid


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize a vector, handling near-zero magnitude."""
    n = np.linalg.norm(v)
    return v / (n + 1e-12)


def gram_schmidt_xy(x: np.ndarray, y: np.ndarray) -> tuple:
    """Orthonormalize X and Y vectors, computing Z = X cross Y.

    Ensures right-handed coordinate system.

    Args:
        x: Desired X axis direction
        y: Desired Y axis direction

    Returns:
        Tuple of (x, y, z) orthonormal vectors forming right-handed basis
    """
    x = normalize(x)
    y = y - np.dot(y, x) * x  # Remove component along x
    y = normalize(y)
    z = np.cross(x, y)
    z = normalize(z)

    # Enforce right-handed system
    if np.linalg.det(np.stack([x, y, z], axis=1)) < 0:
        y = -y
        z = np.cross(x, y)
        z = normalize(z)

    return x, y, z


def snap_to_cardinal(v: np.ndarray, deg: float = 5.0) -> np.ndarray:
    """Snap a vector to the nearest cardinal axis if within tolerance.

    Only snaps if the vector is within `deg` degrees of a cardinal axis.
    Otherwise returns the input vector unchanged.

    Args:
        v: Input unit vector
        deg: Tolerance in degrees (default 5.0)

    Returns:
        Snapped vector (unit cardinal) or original vector
    """
    v = normalize(v)
    axes = np.eye(3)
    dots = axes @ v  # Dot product with each cardinal axis

    # Find the cardinal axis with largest alignment
    i = int(np.argmax(np.abs(dots)))

    # Check if close enough to snap
    if np.abs(dots[i]) >= np.cos(np.deg2rad(deg)):
        out = np.zeros(3)
        out[i] = 1.0 if dots[i] >= 0 else -1.0
        return out

    return v  # Not close enough; don't snap


def stabilize_frame(
    x: np.ndarray,
    y: np.ndarray,
    snap_deg: float = 5.0,
) -> tuple:
    """Stabilize a frame by orthonormalizing and optionally snapping to cardinal axes.

    This eliminates tiny rotation drift from mesh noise that causes asymmetric
    cutting artifacts (e.g., "Y- clips on X+ row, Y+ clips on X- row").

    Process:
    1. Gram-Schmidt orthonormalize X and Y
    2. Snap X to nearest cardinal if within tolerance
    3. Snap Y to nearest cardinal if within tolerance
    4. Re-orthonormalize to ensure orthogonality after snapping

    Args:
        x: X axis vector
        y: Y axis vector
        snap_deg: Snap tolerance in degrees (default 5.0)

    Returns:
        Tuple of (x, y, z) stabilized orthonormal vectors
    """
    # First, make orthonormal
    x, y, z = gram_schmidt_xy(x, y)

    # Snap to cardinals if close
    x2 = snap_to_cardinal(x, deg=snap_deg)
    y2 = snap_to_cardinal(y, deg=snap_deg)

    # Re-orthonormalize after snapping (snapping may break orthogonality)
    x = normalize(x2)
    y = y2 - np.dot(y2, x) * x
    y = normalize(y)
    z = normalize(np.cross(x, y))

    # Ensure right-handed
    if np.linalg.det(np.stack([x, y, z], axis=1)) < 0:
        y = -y
        z = normalize(np.cross(x, y))

    return x, y, z


def compute_dominant_edge_angle(
    footprint: Union[Polygon, MultiPolygon],
    bin_size_deg: float = 0.5,
    min_dominance: float = 0.25,
) -> Optional[float]:
    """
    Compute the dominant edge direction from a footprint polygon using length-weighted voting.

    This function analyzes the exterior boundary edges of the footprint and finds
    the most common edge direction (within a tolerance). This is more robust than
    PCA or minimum rotated rectangle for parts with straight edges.

    Algorithm:
        1. Extract all exterior boundary segments
        2. For each segment, compute its angle (reduced to [0, pi) for undirected)
        3. Weight each angle by segment length
        4. Histogram the angles and find the dominant bin
        5. Compute weighted mean within winning bin neighborhood

    Args:
        footprint: Shapely Polygon or MultiPolygon
        bin_size_deg: Histogram bin size in degrees (default: 0.5)
        min_dominance: Minimum fraction of total weight in best bin to be considered
                       "dominant" (default: 0.25). If not met, returns None.

    Returns:
        Dominant angle in radians [0, pi), or None if no dominant direction found.
    """
    # Collect all edges from exterior rings
    edges: list[tuple[float, float]] = []  # List of (angle, length)

    def add_polygon_edges(poly: Polygon):
        if poly.is_empty:
            return
        coords = np.array(poly.exterior.coords)
        for i in range(len(coords) - 1):
            p1, p2 = coords[i], coords[i + 1]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            length = np.sqrt(dx * dx + dy * dy)
            if length < 1e-9:
                continue
            # Compute angle, reduce to [0, pi) for undirected edges
            angle = np.arctan2(dy, dx)
            if angle < 0:
                angle += np.pi
            if angle >= np.pi:
                angle -= np.pi
            edges.append((angle, length))

    if isinstance(footprint, MultiPolygon):
        # Use largest polygon for edge voting
        largest = max(footprint.geoms, key=lambda p: p.area)
        add_polygon_edges(largest)
    else:
        add_polygon_edges(footprint)

    if not edges:
        return None

    # Build length-weighted histogram
    edges_arr = np.array(edges)  # shape (N, 2): [angle, length]
    angles = edges_arr[:, 0]
    lengths = edges_arr[:, 1]
    total_length = lengths.sum()

    if total_length < 1e-9:
        return None

    # Create histogram bins
    bin_size_rad = np.deg2rad(bin_size_deg)
    n_bins = int(np.ceil(np.pi / bin_size_rad))
    bins = np.zeros(n_bins)

    for angle, length in zip(angles, lengths):
        bin_idx = int(angle / bin_size_rad) % n_bins
        bins[bin_idx] += length

    # Find best bin
    best_bin = np.argmax(bins)
    best_weight = bins[best_bin]

    # Check dominance threshold
    if best_weight / total_length < min_dominance:
        return None

    # Compute weighted mean angle within winning bin +/- 1 bin (to reduce quantization)
    # Handle wraparound at pi
    neighbor_bins = [(best_bin - 1) % n_bins, best_bin, (best_bin + 1) % n_bins]

    weighted_sum = 0.0
    weight_sum = 0.0

    for angle, length in zip(angles, lengths):
        bin_idx = int(angle / bin_size_rad) % n_bins
        if bin_idx in neighbor_bins:
            # Handle wraparound: if angle near 0 and best_bin near pi, adjust
            adjusted_angle = angle
            best_angle_approx = best_bin * bin_size_rad
            if best_angle_approx > np.pi * 0.75 and angle < np.pi * 0.25:
                adjusted_angle = angle + np.pi
            elif best_angle_approx < np.pi * 0.25 and angle > np.pi * 0.75:
                adjusted_angle = angle - np.pi
            weighted_sum += adjusted_angle * length
            weight_sum += length

    if weight_sum < 1e-9:
        return best_bin * bin_size_rad + bin_size_rad / 2

    dominant_angle = weighted_sum / weight_sum
    # Normalize back to [0, pi)
    while dominant_angle < 0:
        dominant_angle += np.pi
    while dominant_angle >= np.pi:
        dominant_angle -= np.pi

    return float(dominant_angle)


def apply_yaw_to_frame(frame: "BottomFrame", yaw_angle: float) -> "BottomFrame":
    """
    Apply a yaw (rotation about Z/up_normal) to align the frame's X axis.

    After rotation, the frame is stabilized by snapping near-cardinal axes
    to eliminate any remaining drift.

    Args:
        frame: The original BottomFrame
        yaw_angle: Angle in radians to rotate the X-Y plane

    Returns:
        New BottomFrame with rotated X/Y axes (same origin and up_normal)
    """
    cos_yaw = np.cos(yaw_angle)
    sin_yaw = np.sin(yaw_angle)

    # Current axes
    x_old = frame.x_axis.copy()
    y_old = frame.y_axis.copy()

    # Rotate in the X-Y plane (about up_normal)
    x_new = cos_yaw * x_old + sin_yaw * y_old
    y_new = -sin_yaw * x_old + cos_yaw * y_old

    # Stabilize by snapping near-cardinal axes (eliminates remaining drift)
    x_new, y_new, z_new = stabilize_frame(x_new, y_new, snap_deg=5.0)

    # Build new rotation matrix
    new_rotation = np.column_stack([x_new, y_new, z_new])

    return BottomFrame(
        origin=frame.origin.copy(),
        rotation=new_rotation,
        z_min=frame.z_min,
    )


@dataclass
class BottomFrame:
    """
    Represents a local coordinate frame for the bottom plane of a mesh.

    Attributes:
        origin: 3D point on the bottom plane (centroid of bottom faces)
        rotation: 3x3 rotation matrix [x_axis | y_axis | up_normal] (columns)
                  Transforms from local to world coordinates.
        z_min: The minimum Z coordinate of the bottom plane in world coords
    """

    origin: np.ndarray
    rotation: np.ndarray
    z_min: float

    @property
    def x_axis(self) -> np.ndarray:
        """Local X axis in world coordinates."""
        return self.rotation[:, 0]

    @property
    def y_axis(self) -> np.ndarray:
        """Local Y axis in world coordinates."""
        return self.rotation[:, 1]

    @property
    def up_normal(self) -> np.ndarray:
        """Up normal (into the part) in world coordinates."""
        return self.rotation[:, 2]

    def world_to_local(self, points: np.ndarray) -> np.ndarray:
        """
        Transform 3D points from world to local coordinates.

        Args:
            points: (N, 3) array of world coordinates

        Returns:
            (N, 3) array of local coordinates
        """
        points = np.atleast_2d(points)
        return (points - self.origin) @ self.rotation

    def local_to_world(self, points: np.ndarray) -> np.ndarray:
        """
        Transform 3D points from local to world coordinates.

        Args:
            points: (N, 3) array of local coordinates

        Returns:
            (N, 3) array of world coordinates
        """
        points = np.atleast_2d(points)
        return points @ self.rotation.T + self.origin

    def to_transform_matrix(self) -> np.ndarray:
        """Return 4x4 homogeneous transformation matrix (local to world)."""
        T = np.eye(4)
        T[:3, :3] = self.rotation
        T[:3, 3] = self.origin
        return T


def detect_bottom_frame(
    mesh: trimesh.Trimesh,
    force_z_up: bool = False,
    normal_threshold: float = 0.9,
    z_tolerance: float = 0.1,
) -> BottomFrame:
    """
    Detect the bottom plane and build a stable local coordinate frame.

    This function identifies the bottom-facing faces of a mesh and constructs
    a local coordinate frame suitable for grid cutting operations.

    Args:
        mesh: Input triangle mesh
        force_z_up: If True, assume mesh is already Z-aligned (faster, more stable).
                    If False, auto-detect bottom via face normals.
        normal_threshold: Threshold for face normal dot product to be considered
                          "pointing down" (0.9 = within ~25 degrees of -Z)
        z_tolerance: Tolerance in mm for faces to be considered part of bottom plane

    Returns:
        BottomFrame with origin, rotation matrix, and z_min

    Raises:
        ValueError: If no bottom faces are detected
    """
    # Get mesh bounds
    bounds = mesh.bounds
    z_min = bounds[0, 2]

    # Get face centroids and normals
    centroids = mesh.triangles_center
    normals = mesh.face_normals

    if force_z_up:
        # Assume mesh is Z-aligned: bottom faces point in -Z direction
        down_vector = np.array([0.0, 0.0, -1.0])

        # Find faces near z_min with downward normals
        near_bottom = centroids[:, 2] < z_min + z_tolerance
        pointing_down = np.dot(normals, down_vector) > normal_threshold

        bottom_mask = near_bottom & pointing_down

        if not np.any(bottom_mask):
            raise ValueError(
                f"No bottom faces detected. z_min={z_min:.3f}, "
                f"tolerance={z_tolerance:.3f}, threshold={normal_threshold:.2f}. "
                "Try increasing z_tolerance or lowering normal_threshold."
            )

        # Origin at centroid of bottom faces
        origin = centroids[bottom_mask].mean(axis=0)
        origin[2] = z_min  # Snap to actual z_min

        # Identity rotation for Z-aligned mesh (already axis-aligned)
        # Stabilization is trivially satisfied for identity
        rotation = np.eye(3)

    else:
        # Auto-detect: find the "down" direction and build frame via PCA
        # First, find the global minimum Z and candidate bottom faces
        near_bottom = centroids[:, 2] < z_min + z_tolerance

        if not np.any(near_bottom):
            raise ValueError(f"No faces near z_min={z_min:.3f} within tolerance={z_tolerance:.3f}")

        # Compute average normal of bottom-region faces
        candidate_normals = normals[near_bottom]
        avg_normal = candidate_normals.mean(axis=0)
        avg_normal_norm = np.linalg.norm(avg_normal)

        if avg_normal_norm < 1e-6:
            raise ValueError("Bottom faces have inconsistent normals")

        avg_normal = avg_normal / avg_normal_norm

        # The "down" direction is the average normal (should point down)
        # The "up" direction (into part) is the opposite
        if avg_normal[2] > 0:
            # Normals pointing up = we found top faces, flip
            avg_normal = -avg_normal

        up_normal = -avg_normal  # Points into the part

        # Refine selection: faces with normal aligned to down direction
        down_vector = -up_normal
        pointing_down = np.dot(normals, down_vector) > normal_threshold
        bottom_mask = near_bottom & pointing_down

        if not np.any(bottom_mask):
            # Fallback to just near_bottom if normal filtering is too strict
            bottom_mask = near_bottom

        # Get vertices of bottom faces for PCA
        bottom_face_indices = np.where(bottom_mask)[0]
        bottom_vertices = mesh.vertices[mesh.faces[bottom_face_indices].flatten()]

        # Project vertices onto the bottom plane and compute PCA for X/Y axes
        # Project to 2D by removing the up_normal component
        origin = centroids[bottom_mask].mean(axis=0)
        origin[2] = z_min  # Snap to actual z_min for consistent local Z=0 plane

        # Create a temporary basis to project vertices
        # Find a vector not parallel to up_normal for cross product
        if abs(up_normal[2]) < 0.9:
            temp = np.array([0.0, 0.0, 1.0])
        else:
            temp = np.array([1.0, 0.0, 0.0])

        x_temp = np.cross(up_normal, temp)
        x_temp = x_temp / np.linalg.norm(x_temp)
        y_temp = np.cross(up_normal, x_temp)

        # Project vertices to 2D
        centered = bottom_vertices - origin
        proj_2d = np.column_stack([np.dot(centered, x_temp), np.dot(centered, y_temp)])

        # PCA to find principal directions
        if len(proj_2d) > 2:
            cov = np.cov(proj_2d.T)
            eigenvalues, eigenvectors = np.linalg.eigh(cov)
            # Sort by eigenvalue descending
            order = np.argsort(eigenvalues)[::-1]
            eigenvectors = eigenvectors[:, order]

            # First principal component becomes X, second becomes Y
            x_2d = eigenvectors[:, 0]
            y_2d = eigenvectors[:, 1]

            # Convert back to 3D
            x_axis = x_2d[0] * x_temp + x_2d[1] * y_temp
            y_axis = y_2d[0] * x_temp + y_2d[1] * y_temp
        else:
            # Not enough vertices for PCA, use temp axes
            x_axis = x_temp
            y_axis = y_temp

        # Ensure right-handedness: z = x cross y should equal up_normal
        z_check = np.cross(x_axis, y_axis)
        if np.dot(z_check, up_normal) < 0:
            y_axis = -y_axis

        # Stabilize the frame by snapping near-cardinal axes
        # This eliminates tiny rotation drift from mesh noise that causes
        # asymmetric cutting artifacts (e.g., "Y- clips on X+ row")
        x_axis, y_axis, up_normal = stabilize_frame(x_axis, y_axis, snap_deg=5.0)

        # Build rotation matrix
        rotation = np.column_stack([x_axis, y_axis, up_normal])

    return BottomFrame(origin=origin, rotation=rotation, z_min=z_min)


def extract_footprint(
    mesh: trimesh.Trimesh,
    frame: BottomFrame,
    slice_delta: Optional[float] = None,
) -> Union[Polygon, MultiPolygon]:
    """
    Extract the 2D footprint polygon by slicing just above the bottom plane.

    Args:
        mesh: Input triangle mesh
        frame: Bottom frame from detect_bottom_frame()
        slice_delta: Offset above bottom plane in mm. If None, auto-computed
                     as max(0.05, min(0.2, 0.01 * bbox_diagonal))

    Returns:
        Shapely Polygon or MultiPolygon representing the bottom footprint
        in local 2D coordinates (origin-centered)

    Raises:
        ValueError: If no footprint can be extracted
    """
    # Compute slice_delta adaptively if not provided
    if slice_delta is None:
        bbox_diagonal = np.linalg.norm(mesh.bounds[1] - mesh.bounds[0])
        delta = float(max(0.05, min(0.2, 0.01 * bbox_diagonal)))
    else:
        delta = slice_delta

    # Compute slice plane in world coordinates
    slice_origin = frame.origin + delta * frame.up_normal
    slice_normal = frame.up_normal

    # Slice the mesh
    try:
        section = mesh.section(plane_origin=slice_origin, plane_normal=slice_normal)
    except Exception as e:
        raise ValueError(f"Failed to slice mesh: {e}")

    if section is None:
        # Try with different delta values
        for delta_mult in [0.5, 2.0, 0.1, 5.0]:
            alt_delta = delta * delta_mult
            alt_origin = frame.origin + alt_delta * frame.up_normal
            try:
                section = mesh.section(plane_origin=alt_origin, plane_normal=slice_normal)
                if section is not None:
                    break
            except Exception:
                continue

    if section is None:
        raise ValueError(
            f"No cross-section found at slice_delta={delta:.3f}mm. "
            "The mesh may not intersect the bottom plane or may be non-watertight."
        )

    # Convert to 2D path
    try:
        planar_path, transform = section.to_2D()
    except Exception as e:
        raise ValueError(f"Failed to convert section to 2D: {e}")

    if planar_path is None or len(planar_path.polygons_full) == 0:
        raise ValueError("Cross-section produced no valid polygons")

    # Get all polygons from the section
    polygons = []
    for poly in planar_path.polygons_full:
        if poly.is_valid and poly.area > 1e-6:
            polygons.append(poly)

    if not polygons:
        # Try polygons_closed as fallback
        for poly in planar_path.polygons_closed:
            if poly.is_valid and poly.area > 1e-6:
                polygons.append(poly)

    if not polygons:
        raise ValueError("No valid polygons in cross-section")

    # Union all polygons
    if len(polygons) == 1:
        footprint_geom = polygons[0]
    else:
        footprint_geom = unary_union(polygons)

    # Ensure validity
    if not footprint_geom.is_valid:
        footprint_geom = make_valid(footprint_geom)

    # Transform footprint to local frame coordinates
    # The planar path has its own transform; we need to account for that
    # and then apply the inverse of our frame's transform

    # First, get the 3D coordinates of the footprint boundary
    # The planar path is in some arbitrary 2D coordinate system
    # We need to convert to our local frame

    # Extract coordinates from footprint
    if isinstance(footprint_geom, MultiPolygon):
        result_polys = []
        for geom in footprint_geom.geoms:
            if not isinstance(geom, Polygon):
                continue
            local_poly = _transform_polygon_to_local_frame(geom, transform, frame)
            if local_poly is not None and local_poly.is_valid and local_poly.area > 1e-6:
                result_polys.append(local_poly)
        if len(result_polys) == 1:
            return result_polys[0]
        elif len(result_polys) > 1:
            return MultiPolygon(result_polys)
        else:
            raise ValueError("No valid polygons after transformation")
    elif isinstance(footprint_geom, Polygon):
        local_poly = _transform_polygon_to_local_frame(footprint_geom, transform, frame)
        if local_poly is None or not local_poly.is_valid:
            raise ValueError("Failed to transform footprint to local frame")
        return local_poly
    else:
        raise ValueError(f"Unexpected geometry type: {type(footprint_geom)}")


def _transform_polygon_to_local_frame(
    poly: Polygon,
    planar_transform: np.ndarray,
    frame: BottomFrame,
) -> Optional[Polygon]:
    """
    Transform a 2D polygon from planar section coordinates to local frame coordinates.

    Args:
        poly: Shapely Polygon in planar section coordinates
        planar_transform: 4x4 transform from section.to_2D()
        frame: Our target local frame

    Returns:
        Polygon in local frame coordinates (2D, XY plane)
    """
    try:
        # Get exterior coordinates (2D in planar space)
        coords_2d = np.array(poly.exterior.coords)

        # Convert to 3D by adding Z=0
        coords_3d_planar = np.column_stack([coords_2d, np.zeros(len(coords_2d))])

        # Apply planar transform to get world coordinates
        # planar_transform is typically a 4x4 matrix
        coords_3d_world = trimesh.transform_points(coords_3d_planar, planar_transform)

        # Convert to local frame coordinates
        coords_local = frame.world_to_local(coords_3d_world)

        # Extract XY for 2D polygon (Z should be near 0 in local frame)
        coords_2d_local = coords_local[:, :2]

        # Handle holes if present
        holes = []
        for interior in poly.interiors:
            hole_coords_2d = np.array(interior.coords)
            hole_coords_3d = np.column_stack([hole_coords_2d, np.zeros(len(hole_coords_2d))])
            hole_world = trimesh.transform_points(hole_coords_3d, planar_transform)
            hole_local = frame.world_to_local(hole_world)
            holes.append(hole_local[:, :2])

        return Polygon(coords_2d_local, holes=holes if holes else None)

    except Exception:
        return None


def detect_aligned_frame(
    mesh: trimesh.Trimesh,
    force_z_up: bool = False,
    z_tolerance: float = 0.1,
    normal_threshold: float = 0.9,
    edge_voting: bool = True,
) -> Tuple[BottomFrame, Union[Polygon, MultiPolygon]]:
    """
    Detect bottom frame with edge-aligned axes and extract footprint.

    This function combines frame detection, footprint extraction, and
    edge-direction voting into a single pipeline that ensures the
    frame axes are aligned with the dominant edge directions.

    Process:
        1. Detect bottom plane with provisional axes
        2. Extract footprint in provisional frame
        3. Compute dominant edge angle (if edge_voting=True)
        4. Apply yaw rotation to align X axis with dominant edge
        5. Re-extract footprint in corrected frame

    Args:
        mesh: Input triangle mesh
        force_z_up: If True, assume mesh is already Z-aligned
        z_tolerance: Tolerance for bottom face detection (mm)
        normal_threshold: Threshold for face normal alignment
        edge_voting: If True, use edge voting to align axes (recommended)

    Returns:
        Tuple of (aligned_frame, footprint_in_aligned_frame)

    Raises:
        ValueError: If detection or footprint extraction fails
    """
    # Step 1: Detect bottom plane with provisional axes
    frame = detect_bottom_frame(
        mesh,
        force_z_up=force_z_up,
        normal_threshold=normal_threshold,
        z_tolerance=z_tolerance,
    )

    # Step 2: Extract footprint in provisional frame
    footprint = extract_footprint(mesh, frame)

    if not edge_voting:
        return frame, footprint

    # Step 3: Compute dominant edge angle
    dominant_angle = compute_dominant_edge_angle(footprint)

    if dominant_angle is None:
        # No dominant edge found, use frame as-is
        return frame, footprint

    # Step 4: Compute yaw rotation needed
    # The current X axis is at angle 0 in local frame
    # We want it aligned with the dominant edge angle
    # So we rotate by -dominant_angle to bring dominant edge to X axis
    #
    # However, we also want to pick the closest 90-degree alignment
    # (since rectangles have edges at 0 and 90 degrees)
    # Snap to nearest multiple of 90 degrees if close
    angle_deg = np.degrees(dominant_angle)

    # Find the nearest 90-degree snap point
    snap_angles = [0, 90, 180]
    closest_snap = min(snap_angles, key=lambda s: min(abs(angle_deg - s), abs(angle_deg - s + 180)))

    # Use the snap if within tolerance
    if abs(angle_deg - closest_snap) < 5.0 or abs(angle_deg - closest_snap + 180) < 5.0:
        yaw = np.radians(closest_snap)
    else:
        yaw = dominant_angle

    # We want to rotate so the dominant direction aligns with X
    # Current X is at 0, dominant is at `yaw`, so rotate by -yaw
    # But since we want X to align TO the dominant edge, we rotate by -yaw
    yaw_correction = -yaw

    # Only apply rotation if it's significant
    if abs(yaw_correction) < np.radians(0.1):
        return frame, footprint

    # Step 5: Apply yaw rotation
    aligned_frame = apply_yaw_to_frame(frame, yaw_correction)

    # Step 6: Re-extract footprint in aligned frame
    aligned_footprint = extract_footprint(mesh, aligned_frame)

    return aligned_frame, aligned_footprint


def get_mesh_diagnostics(mesh: trimesh.Trimesh) -> dict:
    """
    Get diagnostic information about a mesh for debugging.

    Args:
        mesh: Input triangle mesh

    Returns:
        Dictionary with diagnostic info
    """
    bounds = mesh.bounds
    return {
        "is_watertight": mesh.is_watertight,
        "is_winding_consistent": mesh.is_winding_consistent,
        "euler_number": mesh.euler_number,
        "bounds_min": bounds[0].tolist(),
        "bounds_max": bounds[1].tolist(),
        "triangle_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "volume": mesh.volume if mesh.is_watertight else None,
        "area": mesh.area,
    }
