#! /usr/bin/env python3
#
# meshcutter.io.loader - STL/3MF mesh loading
#

from __future__ import annotations

from pathlib import Path
from typing import Union, Optional
import zipfile
import tempfile
import os

import numpy as np
import trimesh


class LoaderError(Exception):
    """Exception raised when mesh loading fails."""

    pass


def load_mesh(
    filepath: Union[str, Path],
    merge_objects: bool = True,
) -> trimesh.Trimesh:
    """
    Load a mesh from an STL or 3MF file.

    For 3MF files with multiple objects:
    - If merge_objects=True (default): All objects are merged into one mesh
      with their transforms applied.
    - If merge_objects=False: Only the first object is returned.

    Args:
        filepath: Path to STL or 3MF file
        merge_objects: Whether to merge multiple objects (for 3MF)

    Returns:
        trimesh.Trimesh

    Raises:
        LoaderError: If loading fails
        FileNotFoundError: If file doesn't exist
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    suffix = filepath.suffix.lower()

    if suffix == ".stl":
        return _load_stl(filepath)
    elif suffix == ".3mf":
        return _load_3mf(filepath, merge_objects=merge_objects)
    else:
        raise LoaderError(f"Unsupported file format: {suffix}. Use .stl or .3mf")


def _load_stl(filepath: Path) -> trimesh.Trimesh:
    """Load an STL file."""
    try:
        mesh = trimesh.load(str(filepath), file_type="stl", force="mesh")

        if mesh is None:
            raise LoaderError(f"Failed to load STL: {filepath}")

        # Ensure we have a Trimesh, not a Scene
        if isinstance(mesh, trimesh.Scene):
            # Extract geometry from scene
            geometries = list(mesh.geometry.values())
            if not geometries:
                raise LoaderError(f"STL contains no geometry: {filepath}")
            mesh = trimesh.util.concatenate(geometries)

        if not isinstance(mesh, trimesh.Trimesh):
            raise LoaderError(f"Unexpected mesh type: {type(mesh)}")

        return mesh

    except Exception as e:
        if isinstance(e, LoaderError):
            raise
        raise LoaderError(f"Failed to load STL {filepath}: {e}")


def _load_3mf(filepath: Path, merge_objects: bool = True) -> trimesh.Trimesh:
    """
    Load a 3MF file.

    3MF is a ZIP archive containing XML model data. Trimesh can load it,
    but we may need special handling for multiple objects and transforms.
    """
    try:
        # Try loading with trimesh first
        loaded = trimesh.load(str(filepath), file_type="3mf")

        if loaded is None:
            raise LoaderError(f"Failed to load 3MF: {filepath}")

        # Handle different return types
        if isinstance(loaded, trimesh.Trimesh):
            return loaded

        elif isinstance(loaded, trimesh.Scene):
            geometries = list(loaded.geometry.values())
            object_count = len(geometries)

            if object_count == 0:
                raise LoaderError(f"3MF contains no geometry: {filepath}")

            if object_count == 1:
                mesh = geometries[0]
                # Apply transform if present
                if hasattr(loaded, "graph") and loaded.graph:
                    for node_name, geom_name in loaded.graph.geometry_nodes.items():
                        if geom_name == list(loaded.geometry.keys())[0]:
                            transform = loaded.graph.get(node_name)[0]
                            if transform is not None:
                                mesh = mesh.copy()
                                mesh.apply_transform(transform)
                            break
                return mesh

            # Multiple objects
            if merge_objects:
                # Get all meshes with their transforms applied
                meshes = []
                for name, geom in loaded.geometry.items():
                    mesh_copy = geom.copy()

                    # Try to find the transform for this geometry
                    if hasattr(loaded, "graph") and loaded.graph:
                        for node_name, geom_name in loaded.graph.geometry_nodes.items():
                            if geom_name == name:
                                transform = loaded.graph.get(node_name)[0]
                                if transform is not None:
                                    mesh_copy.apply_transform(transform)
                                break

                    meshes.append(mesh_copy)

                return trimesh.util.concatenate(meshes)
            else:
                # Return first geometry
                return geometries[0]

        else:
            raise LoaderError(f"Unexpected type from 3MF load: {type(loaded)}")

    except Exception as e:
        if isinstance(e, LoaderError):
            raise
        raise LoaderError(f"Failed to load 3MF {filepath}: {e}")


def get_file_info(filepath: Union[str, Path]) -> dict:
    """
    Get information about a mesh file without fully loading it.

    Args:
        filepath: Path to mesh file

    Returns:
        Dictionary with file info
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()

    info = {
        "path": str(filepath),
        "name": filepath.name,
        "format": suffix[1:] if suffix else "unknown",
        "size_bytes": filepath.stat().st_size if filepath.exists() else None,
        "exists": filepath.exists(),
    }

    if suffix == ".3mf" and filepath.exists():
        # Peek into 3MF to count objects
        try:
            with zipfile.ZipFile(filepath, "r") as zf:
                info["is_valid_3mf"] = "3D/3dmodel.model" in zf.namelist()
        except Exception:
            info["is_valid_3mf"] = False

    return info


def validate_mesh(mesh: trimesh.Trimesh) -> dict:
    """
    Validate a loaded mesh and return diagnostic info.

    Args:
        mesh: Loaded mesh

    Returns:
        Dictionary with validation results
    """
    return {
        "is_watertight": mesh.is_watertight,
        "is_winding_consistent": mesh.is_winding_consistent,
        "is_convex": mesh.is_convex,
        "euler_number": mesh.euler_number,
        "face_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "bounds_min": mesh.bounds[0].tolist(),
        "bounds_max": mesh.bounds[1].tolist(),
        "dimensions": (mesh.bounds[1] - mesh.bounds[0]).tolist(),
        "volume": mesh.volume if mesh.is_watertight else None,
        "area": mesh.area,
        "center_mass": mesh.center_mass.tolist() if mesh.is_watertight else None,
    }
