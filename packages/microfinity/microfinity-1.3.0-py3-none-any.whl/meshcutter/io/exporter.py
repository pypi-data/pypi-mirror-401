#! /usr/bin/env python3
#
# meshcutter.io.exporter - STL export
#

from __future__ import annotations

from pathlib import Path
from typing import Union

import trimesh


class ExporterError(Exception):
    """Exception raised when mesh export fails."""

    pass


def export_stl(
    mesh: trimesh.Trimesh,
    filepath: Union[str, Path],
    binary: bool = True,
) -> None:
    """
    Export a mesh to STL format.

    Args:
        mesh: The mesh to export
        filepath: Output file path
        binary: If True (default), export binary STL. If False, export ASCII.

    Raises:
        ExporterError: If export fails
    """
    filepath = Path(filepath)

    # Ensure parent directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        if binary:
            mesh.export(str(filepath), file_type="stl")
        else:
            # ASCII STL
            mesh.export(str(filepath), file_type="stl_ascii")

    except Exception as e:
        raise ExporterError(f"Failed to export STL to {filepath}: {e}")


def get_export_info(mesh: trimesh.Trimesh) -> dict:
    """
    Get information about what will be exported.

    Useful for verbose output before exporting.

    Args:
        mesh: The mesh to export

    Returns:
        Dictionary with export info
    """
    return {
        "face_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "bounds_min": mesh.bounds[0].tolist(),
        "bounds_max": mesh.bounds[1].tolist(),
        "dimensions": (mesh.bounds[1] - mesh.bounds[0]).tolist(),
        "is_watertight": mesh.is_watertight,
        "estimated_binary_stl_size": _estimate_stl_size(mesh, binary=True),
        "estimated_ascii_stl_size": _estimate_stl_size(mesh, binary=False),
    }


def _estimate_stl_size(mesh: trimesh.Trimesh, binary: bool = True) -> int:
    """
    Estimate the file size of an STL export.

    Args:
        mesh: The mesh
        binary: Whether binary or ASCII format

    Returns:
        Estimated size in bytes
    """
    face_count = len(mesh.faces)

    if binary:
        # Binary STL: 80 byte header + 4 byte count + 50 bytes per triangle
        return 80 + 4 + (face_count * 50)
    else:
        # ASCII STL: roughly 200-250 bytes per triangle
        return face_count * 220
