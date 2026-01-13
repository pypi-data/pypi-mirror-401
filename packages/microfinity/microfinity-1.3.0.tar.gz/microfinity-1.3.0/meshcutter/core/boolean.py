#! /usr/bin/env python3
#
# meshcutter.core.boolean - Tiered boolean operations with fallbacks
#

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

import numpy as np
import trimesh


class MeshCutterError(Exception):
    """Base exception for meshcutter errors."""

    pass


class BooleanError(MeshCutterError):
    """Exception raised when boolean operations fail."""

    def __init__(self, message: str, diagnostics: Optional[dict] = None):
        super().__init__(message)
        self.diagnostics = diagnostics or {}


@dataclass
class BooleanResult:
    """Result of a boolean operation with metadata."""

    mesh: trimesh.Trimesh
    engine_used: str
    repair_applied: bool
    warnings: List[str]


def check_manifold3d_available() -> bool:
    """Check if manifold3d is installed and working."""
    try:
        import manifold3d  # noqa: F401

        return True
    except ImportError:
        return False


def check_pymeshlab_available() -> bool:
    """Check if pymeshlab is installed and working."""
    try:
        import pymeshlab  # noqa: F401

        return True
    except ImportError:
        return False


def get_available_engines() -> List[str]:
    """Get list of available boolean engines."""
    engines = []
    if check_manifold3d_available():
        engines.append("manifold")
    engines.append("blender")  # trimesh's built-in fallback
    if check_pymeshlab_available():
        engines.append("pymeshlab")
    return engines


def repair_mesh(mesh: trimesh.Trimesh, aggressive: bool = False) -> trimesh.Trimesh:
    """
    Attempt basic mesh repairs.

    Repairs that can be reliably handled:
    - Duplicate vertices
    - Degenerate faces
    - Inconsistent normals
    - Small holes

    Repairs that cannot be reliably fixed (may still exist after repair):
    - Deep self-intersections
    - Non-manifold tangles

    Args:
        mesh: Input mesh (not modified in place)
        aggressive: If True, attempt more aggressive repairs

    Returns:
        Repaired mesh (new object)
    """
    # Work on a copy
    repaired = mesh.copy()

    # Merge duplicate vertices
    repaired.merge_vertices()

    # Remove degenerate faces (zero area) - API differs between trimesh versions
    try:
        # trimesh >= 4.0
        if hasattr(repaired, "remove_degenerate_faces"):
            repaired.remove_degenerate_faces()
        else:
            # Older trimesh: use nondegenerate_faces mask
            repaired.update_faces(repaired.nondegenerate_faces())
    except Exception:
        pass  # Skip if neither method works

    # Remove duplicate faces
    try:
        repaired.remove_duplicate_faces()
    except Exception:
        pass

    # Fix normals to be consistent
    repaired.fix_normals()

    if aggressive:
        # Try to fill holes
        try:
            repaired.fill_holes()
        except Exception:
            pass  # Some holes cannot be filled

        # Remove unreferenced vertices
        try:
            repaired.remove_unreferenced_vertices()
        except Exception:
            pass

    return repaired


def get_mesh_diagnostics(mesh: trimesh.Trimesh) -> dict:
    """
    Get diagnostic information about a mesh.

    Useful for debugging boolean failures.

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

    # Check for non-manifold edges (edges shared by more than 2 faces)
    try:
        edges = mesh.edges_unique
        edge_face_count = mesh.edges_unique_length
        # This is a simplified check
        diagnostics["edge_count"] = len(edges)
    except Exception:
        diagnostics["edge_count"] = None

    return diagnostics


def _try_manifold_boolean(
    part: trimesh.Trimesh,
    cutter: trimesh.Trimesh,
) -> Optional[trimesh.Trimesh]:
    """
    Attempt boolean difference using manifold3d engine.

    Returns:
        Result mesh or None if failed
    """
    if not check_manifold3d_available():
        return None

    try:
        result = trimesh.boolean.difference([part, cutter], engine="manifold")
        if result is not None and len(result.faces) > 0:
            return result
    except Exception:
        pass

    return None


def _try_blender_boolean(
    part: trimesh.Trimesh,
    cutter: trimesh.Trimesh,
) -> Optional[trimesh.Trimesh]:
    """
    Attempt boolean difference using trimesh's blender engine.

    Note: This requires Blender to be installed and accessible.
    It's included as a fallback but not recommended for headless CI.

    Returns:
        Result mesh or None if failed
    """
    try:
        result = trimesh.boolean.difference([part, cutter], engine="blender")
        if result is not None and len(result.faces) > 0:
            return result
    except Exception:
        pass

    return None


def _try_pymeshlab_boolean(
    part: trimesh.Trimesh,
    cutter: trimesh.Trimesh,
) -> Optional[trimesh.Trimesh]:
    """
    Attempt boolean difference using PyMeshLab.

    PyMeshLab uses libigl for exact booleans, which can handle
    some cases that manifold3d cannot.

    Returns:
        Result mesh or None if failed
    """
    if not check_pymeshlab_available():
        return None

    try:
        import pymeshlab

        # Create a new MeshSet
        ms = pymeshlab.MeshSet()

        # Add the part mesh
        part_pymesh = pymeshlab.Mesh(
            vertex_matrix=part.vertices,
            face_matrix=part.faces,
        )
        ms.add_mesh(part_pymesh, "part")

        # Add the cutter mesh
        cutter_pymesh = pymeshlab.Mesh(
            vertex_matrix=cutter.vertices,
            face_matrix=cutter.faces,
        )
        ms.add_mesh(cutter_pymesh, "cutter")

        # Perform boolean difference
        # In PyMeshLab, mesh IDs are 0-indexed
        ms.generate_boolean_difference(first_mesh=0, second_mesh=1)

        # Get the result (should be the last mesh added)
        result_pymesh = ms.current_mesh()

        # Convert back to trimesh
        result = trimesh.Trimesh(
            vertices=result_pymesh.vertex_matrix(),
            faces=result_pymesh.face_matrix(),
        )

        if len(result.faces) > 0:
            return result

    except Exception:
        pass

    return None


def boolean_difference(
    part: trimesh.Trimesh,
    cutter: trimesh.Trimesh,
    repair: bool = False,
    fallback_engines: bool = True,
) -> BooleanResult:
    """
    Perform robust boolean difference with tiered fallbacks.

    Tier 1: manifold3d (if available) - fast and robust
    Tier 2: repair + retry manifold3d
    Tier 3: pymeshlab (if available) - handles some edge cases
    Tier 4: raise with diagnostic message

    Note: Blender engine is NOT used as a fallback because it requires
    Blender to be installed and is not suitable for headless CI.

    Args:
        part: The base mesh to cut from
        cutter: The mesh to subtract
        repair: If True, attempt mesh repair before boolean
        fallback_engines: If True, try alternative engines on failure

    Returns:
        BooleanResult with the result mesh and metadata

    Raises:
        BooleanError: If all boolean attempts fail
    """
    warnings: List[str] = []
    engine_used = "unknown"
    repair_applied = False

    # Optionally repair input meshes first
    if repair:
        repair_applied = True
        part = repair_mesh(part, aggressive=False)
        cutter = repair_mesh(cutter, aggressive=False)

    # Tier 1: Try manifold3d
    if check_manifold3d_available():
        result = _try_manifold_boolean(part, cutter)
        if result is not None:
            return BooleanResult(
                mesh=result,
                engine_used="manifold",
                repair_applied=repair_applied,
                warnings=warnings,
            )
        warnings.append("manifold3d boolean failed")

    # Tier 2: Repair + retry manifold3d
    if not repair_applied and check_manifold3d_available():
        part_repaired = repair_mesh(part, aggressive=True)
        cutter_repaired = repair_mesh(cutter, aggressive=True)
        repair_applied = True

        result = _try_manifold_boolean(part_repaired, cutter_repaired)
        if result is not None:
            warnings.append("Boolean succeeded after repair")
            return BooleanResult(
                mesh=result,
                engine_used="manifold",
                repair_applied=True,
                warnings=warnings,
            )
        warnings.append("manifold3d boolean failed after repair")

    # Tier 3: Try PyMeshLab
    if fallback_engines and check_pymeshlab_available():
        # Use repaired meshes if available
        part_to_use = part_repaired if repair_applied else part
        cutter_to_use = cutter_repaired if repair_applied else cutter

        result = _try_pymeshlab_boolean(part_to_use, cutter_to_use)
        if result is not None:
            warnings.append("Used PyMeshLab fallback")
            return BooleanResult(
                mesh=result,
                engine_used="pymeshlab",
                repair_applied=repair_applied,
                warnings=warnings,
            )
        warnings.append("PyMeshLab boolean failed")

    # Tier 4: Fail with diagnostics
    part_diag = get_mesh_diagnostics(part)
    cutter_diag = get_mesh_diagnostics(cutter)

    # Build helpful error message
    suggestions = []
    if not check_manifold3d_available():
        suggestions.append("Install manifold3d: pip install manifold3d")
    if not check_pymeshlab_available():
        suggestions.append("Install pymeshlab for fallback: pip install pymeshlab")
    if not part_diag["is_watertight"]:
        suggestions.append("Input mesh is not watertight - try --repair flag")
    if not cutter_diag["is_watertight"]:
        suggestions.append("Cutter mesh is not watertight (internal error)")

    suggestions.append("Check mesh for self-intersections in MeshLab or Blender")
    suggestions.append("Try simplifying the input mesh")

    error_msg = (
        "Boolean operation failed after all attempts.\n"
        f"Warnings: {warnings}\n"
        f"Suggestions:\n  - " + "\n  - ".join(suggestions)
    )

    raise BooleanError(
        error_msg,
        diagnostics={
            "part": part_diag,
            "cutter": cutter_diag,
            "warnings": warnings,
            "engines_tried": ["manifold", "pymeshlab"] if check_pymeshlab_available() else ["manifold"],
        },
    )


def validate_boolean_inputs(
    part: trimesh.Trimesh,
    cutter: trimesh.Trimesh,
) -> List[str]:
    """
    Validate inputs for boolean operation and return warnings.

    Args:
        part: The base mesh
        cutter: The cutter mesh

    Returns:
        List of warning messages (empty if all OK)
    """
    warnings = []

    if not part.is_watertight:
        warnings.append("Part mesh is not watertight - boolean may fail")

    if not cutter.is_watertight:
        warnings.append("Cutter mesh is not watertight - boolean may fail")

    if not part.is_winding_consistent:
        warnings.append("Part mesh has inconsistent face winding")

    if not cutter.is_winding_consistent:
        warnings.append("Cutter mesh has inconsistent face winding")

    # Check for reasonable mesh sizes
    if len(part.faces) == 0:
        warnings.append("Part mesh has no faces")

    if len(cutter.faces) == 0:
        warnings.append("Cutter mesh has no faces")

    # Check that meshes overlap
    part_bounds = part.bounds
    cutter_bounds = cutter.bounds

    # Check if bounding boxes intersect
    if not (
        part_bounds[0, 0] <= cutter_bounds[1, 0]
        and part_bounds[1, 0] >= cutter_bounds[0, 0]
        and part_bounds[0, 1] <= cutter_bounds[1, 1]
        and part_bounds[1, 1] >= cutter_bounds[0, 1]
        and part_bounds[0, 2] <= cutter_bounds[1, 2]
        and part_bounds[1, 2] >= cutter_bounds[0, 2]
    ):
        warnings.append("Part and cutter bounding boxes do not intersect")

    return warnings
