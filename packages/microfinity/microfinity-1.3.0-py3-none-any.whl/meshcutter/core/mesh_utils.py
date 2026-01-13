#! /usr/bin/env python3
#
# meshcutter.core.mesh_utils - Mesh conversion and utility functions
#
# This module provides utilities for converting between mesh formats,
# cleaning meshes, and computing mesh diagnostics.

from __future__ import annotations

import os
import tempfile
from typing import Dict, List, Optional, Tuple

import numpy as np
import trimesh

from meshcutter.core.constants import (
    MIN_COMPONENT_FACES,
    MIN_SLIVER_SIZE,
    MIN_SLIVER_VOLUME,
)


# -----------------------------------------------------------------------------
# Mesh format conversion
# -----------------------------------------------------------------------------


def trimesh_to_manifold(mesh: trimesh.Trimesh):
    """Convert trimesh to manifold3d Manifold.

    Args:
        mesh: Input trimesh mesh

    Returns:
        manifold3d.Manifold object
    """
    import manifold3d

    return manifold3d.Manifold(
        manifold3d.Mesh(
            vert_properties=np.array(mesh.vertices, dtype=np.float32),
            tri_verts=np.array(mesh.faces, dtype=np.uint32),
        )
    )


def manifold_to_trimesh(manifold) -> trimesh.Trimesh:
    """Convert manifold3d Manifold to trimesh.

    Args:
        manifold: manifold3d.Manifold object

    Returns:
        trimesh.Trimesh object
    """
    mesh_data = manifold.to_mesh()
    return trimesh.Trimesh(
        vertices=np.array(mesh_data.vert_properties, dtype=np.float64),
        faces=np.array(mesh_data.tri_verts, dtype=np.int64),
    )


def cq_to_trimesh(cq_obj, tol: float = 0.01, ang_tol: float = 0.1) -> trimesh.Trimesh:
    """Convert CadQuery Workplane to trimesh.

    Uses CadQuery's STL export with specified tolerances, matching
    microfinity's default export settings.

    Args:
        cq_obj: CadQuery Workplane object
        tol: Linear mesh tolerance (mm)
        ang_tol: Angular mesh tolerance (radians)

    Returns:
        trimesh.Trimesh object
    """
    import cadquery as cq

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

    # Ensure we return a Trimesh, not a Scene
    if isinstance(mesh, trimesh.Scene):
        # Combine all geometries in the scene
        meshes = [g for g in mesh.geometry.values() if isinstance(g, trimesh.Trimesh)]
        if len(meshes) == 1:
            return meshes[0]
        elif len(meshes) > 1:
            return trimesh.util.concatenate(meshes)
        else:
            raise ValueError("No valid mesh geometry in CadQuery export")

    return mesh


# -----------------------------------------------------------------------------
# Mesh repair and cleaning
# -----------------------------------------------------------------------------


def repair_mesh_manifold(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Repair mesh by passing through manifold3d.

    This eliminates floating-point artifacts and non-manifold geometry
    that can occur during boolean operations or STL export/import.

    Args:
        mesh: trimesh.Trimesh to repair

    Returns:
        Repaired trimesh.Trimesh (or original if manifold3d unavailable)
    """
    try:
        import manifold3d

        # Convert to manifold (auto-repairs)
        m = manifold3d.Manifold(
            manifold3d.Mesh(
                vert_properties=np.array(mesh.vertices, dtype=np.float32),
                tri_verts=np.array(mesh.faces, dtype=np.uint32),
            )
        )

        # Convert back to trimesh
        mesh_data = m.to_mesh()
        return trimesh.Trimesh(vertices=mesh_data.vert_properties[:, :3], faces=mesh_data.tri_verts)
    except ImportError:
        return mesh  # manifold3d not available


def is_degenerate_sliver(
    component: trimesh.Trimesh,
    min_size: float = MIN_SLIVER_SIZE,
    min_volume: float = MIN_SLIVER_VOLUME,
) -> bool:
    """Check if a component is a degenerate sliver (boolean artifact).

    A sliver is identified by:
    - All bounding box dimensions being very small (< min_size), OR
    - Having an extremely small volume (< min_volume), OR
    - Having fewer than 4 faces (can't form a valid solid)

    Args:
        component: trimesh.Trimesh component to check
        min_size: Minimum acceptable size in any dimension (mm)
        min_volume: Minimum acceptable volume (mm³)

    Returns:
        True if the component is a degenerate sliver that should be removed
    """
    # Check face count - need at least 4 faces for a tetrahedron
    if len(component.faces) < 4:
        return True

    # Check if all dimensions are tiny (nanometer-scale artifact)
    size = component.bounds[1] - component.bounds[0]
    if (size < min_size).all():
        return True

    # Check volume - if it's effectively zero, it's degenerate
    # Use absolute value since non-watertight meshes can have negative volume
    if abs(component.volume) < min_volume:
        return True

    return False


def clean_mesh_components(
    mesh: trimesh.Trimesh,
    min_faces: int = MIN_COMPONENT_FACES,
) -> Tuple[trimesh.Trimesh, int]:
    """Remove floating/degenerate components from mesh.

    Keeps only the largest component(s) that have significant geometry.
    Small floating triangles and nanometer-scale slivers (common boolean
    artifacts) are removed.

    Args:
        mesh: trimesh.Trimesh input mesh
        min_faces: Minimum faces to keep a component

    Returns:
        Tuple of (cleaned mesh, number of components removed)
    """
    components = mesh.split(only_watertight=False)

    if len(components) <= 1:
        return mesh, 0

    # Find the main component (largest by face count)
    main_component = max(components, key=lambda c: len(c.faces))
    main_face_count = len(main_component.faces)

    # Keep components that:
    # 1. Have at least min_faces faces OR 1% of main component, AND
    # 2. Are NOT degenerate slivers (size/volume check)
    threshold = max(min_faces, main_face_count * 0.01)
    kept = [c for c in components if len(c.faces) >= threshold and not is_degenerate_sliver(c)]
    removed_count = len(components) - len(kept)

    if len(kept) == 1:
        return kept[0], removed_count
    elif len(kept) > 1:
        # Concatenate kept components
        return trimesh.util.concatenate(kept), removed_count
    else:
        # Shouldn't happen, but return original if no components kept
        return mesh, 0


# -----------------------------------------------------------------------------
# Mesh diagnostics
# -----------------------------------------------------------------------------


def get_mesh_diagnostics(mesh: trimesh.Trimesh) -> Dict:
    """Get diagnostic information about a mesh.

    Useful for debugging boolean failures and mesh issues.

    Args:
        mesh: Input mesh

    Returns:
        Dictionary with diagnostic info
    """
    diagnostics = {
        "is_watertight": mesh.is_watertight,
        "is_winding_consistent": mesh.is_winding_consistent,
        "euler_number": mesh.euler_number,
        "face_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "bounds_min": mesh.bounds[0].tolist(),
        "bounds_max": mesh.bounds[1].tolist(),
        "area": mesh.area,
    }

    # Volume only valid for watertight meshes
    if mesh.is_watertight:
        diagnostics["volume"] = mesh.volume
    else:
        diagnostics["volume"] = None

    # Check for non-manifold edges
    try:
        edges = mesh.edges_unique
        diagnostics["edge_count"] = len(edges)
    except Exception:
        diagnostics["edge_count"] = None

    return diagnostics


def validate_mesh_for_boolean(mesh: trimesh.Trimesh, name: str = "mesh") -> List[str]:
    """Validate a mesh is suitable for boolean operations.

    Args:
        mesh: Input mesh
        name: Name for error messages

    Returns:
        List of warning messages (empty if all OK)
    """
    warnings = []

    if not mesh.is_watertight:
        warnings.append(f"{name} is not watertight - boolean may fail")

    if not mesh.is_winding_consistent:
        warnings.append(f"{name} has inconsistent face winding")

    if len(mesh.faces) == 0:
        warnings.append(f"{name} has no faces")

    return warnings
