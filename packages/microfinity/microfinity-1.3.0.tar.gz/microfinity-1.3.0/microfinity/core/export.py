"""Gridfinity Export Utilities.

Low-level export primitives for CadQuery geometry to various file formats.
This module contains ONLY the file-writing logic, not orchestration.

For batch exports of layouts, use GridfinityBaseplateLayout.export_all().
For test print exports, use calibration.test_prints.export_test_prints().
"""

from enum import Enum
from typing import List, Tuple, Optional, Dict, Any, Union
import os
import warnings

import cadquery as cq
from cadquery import exporters
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.StlAPI import StlAPI_Writer
from cqkit import export_step_file


class SVGView(Enum):
    """Preset SVG view orientations for export."""

    ISOMETRIC = "isometric"  # Classic 3/4 isometric view
    FRONT = "front"  # Front elevation (XZ plane)
    TOP = "top"  # Plan view (XY plane)
    RIGHT = "right"  # Right elevation (YZ plane)
    ISOMETRIC_FLAT = "iso_flat"  # Isometric without pre-rotation


# Type alias for objects we can export
Exportable = Union[cq.Workplane, cq.Assembly]


class GridfinityExporter:
    """Static utility class for exporting CadQuery geometry to files.

    All methods are static - no instance needed.
    All export methods return the absolute path to the created file.

    Example:
        from microfinity import GridfinityExporter, SVGView

        path = GridfinityExporter.to_step(obj, "output.step")
        path = GridfinityExporter.to_svg(obj, "preview.svg", view=SVGView.FRONT)

        # Batch export
        paths = GridfinityExporter.batch_export([
            (obj1, "file1.step"),
            (obj2, "file2.step"),
        ])
    """

    DEFAULT_SVG_OPTIONS: Dict[str, Any] = {
        "width": 600,
        "height": 400,
        "showAxes": False,
        "marginTop": 20,
        "marginLeft": 20,
        "projectionDir": (1, 1, 1),
    }

    @staticmethod
    def ensure_extension(filepath: str, ext: str) -> str:
        """Ensure filepath has the correct extension.

        Args:
            filepath: Path to file
            ext: Extension with dot (e.g., ".step")

        Returns:
            Filepath with correct extension
        """
        if not filepath.lower().endswith(ext.lower()):
            return filepath + ext
        return filepath

    @staticmethod
    def to_step(obj: Exportable, filepath: str) -> str:
        """Export CadQuery object to STEP file.

        Args:
            obj: CadQuery Workplane or Assembly to export
            filepath: Output file path

        Returns:
            Absolute path to exported file
        """
        filepath = GridfinityExporter.ensure_extension(filepath, ".step")

        if isinstance(obj, cq.Assembly):
            obj.save(filepath)
        else:
            export_step_file(obj, filepath)

        return os.path.abspath(filepath)

    @staticmethod
    def to_stl(
        obj: Exportable,
        filepath: str,
        linear_tolerance: float = 1e-2,
        angular_tolerance: float = 0.1,
    ) -> str:
        """Export CadQuery object to STL file.

        Args:
            obj: CadQuery Workplane to export
            filepath: Output file path
            linear_tolerance: Mesh linear tolerance (default 0.01mm)
            angular_tolerance: Mesh angular tolerance in radians (default 0.1)

        Returns:
            Absolute path to exported file

        Raises:
            TypeError: If obj is an Assembly (STL export not directly supported)
        """
        if isinstance(obj, cq.Assembly):
            raise TypeError(
                "STL export of Assembly not supported. " "Convert to compound first or export components separately."
            )

        filepath = GridfinityExporter.ensure_extension(filepath, ".stl")

        shape = obj.val().wrapped
        mesh = BRepMesh_IncrementalMesh(shape, linear_tolerance, True, angular_tolerance, True)
        mesh.Perform()

        writer = StlAPI_Writer()
        writer.Write(shape, filepath)

        return os.path.abspath(filepath)

    @staticmethod
    def to_svg(
        obj: Exportable,
        filepath: str,
        view: SVGView = SVGView.ISOMETRIC,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Export CadQuery object to SVG projection.

        Args:
            obj: CadQuery Workplane to export (Assembly not supported)
            filepath: Output file path
            view: Preset view orientation (default: ISOMETRIC)
            options: Override default SVG options (merged with defaults)

        Returns:
            Absolute path to exported file

        Raises:
            TypeError: If obj is an Assembly
        """
        if isinstance(obj, cq.Assembly):
            raise TypeError("SVG export of Assembly not supported. " "Convert to compound first.")

        filepath = GridfinityExporter.ensure_extension(filepath, ".svg")

        # Apply view transformation
        rotated = GridfinityExporter._apply_view_rotation(obj, view)

        # Merge options with defaults
        export_opts = {**GridfinityExporter.DEFAULT_SVG_OPTIONS}
        if options:
            export_opts.update(options)

        exporters.export(rotated, filepath, opt=export_opts)

        return os.path.abspath(filepath)

    @staticmethod
    def _apply_view_rotation(obj: cq.Workplane, view: SVGView) -> cq.Workplane:
        """Apply rotation for the specified view.

        Args:
            obj: CadQuery object to rotate
            view: Target view orientation

        Returns:
            Rotated CadQuery object
        """
        if view == SVGView.ISOMETRIC:
            # Classic 3/4 isometric (matches original save_svg_file)
            r = obj.rotate((0, 0, 0), (0, 0, 1), 75)
            return r.rotate((0, 0, 0), (1, 0, 0), -90)
        elif view == SVGView.FRONT:
            return obj.rotate((0, 0, 0), (1, 0, 0), -90)
        elif view == SVGView.TOP:
            return obj  # No rotation needed
        elif view == SVGView.RIGHT:
            r = obj.rotate((0, 0, 0), (0, 0, 1), -90)
            return r.rotate((0, 0, 0), (1, 0, 0), -90)
        elif view == SVGView.ISOMETRIC_FLAT:
            return obj
        return obj

    @staticmethod
    def batch_export(
        items: List[Tuple[Exportable, str]],
        file_format: str = "step",
        strict: bool = False,
        linear_tolerance: float = 1e-2,
        angular_tolerance: float = 0.1,
    ) -> List[str]:
        """Export multiple objects sequentially.

        Note: Parallel export is intentionally not supported because
        OCCT/CadQuery is not thread-safe. Use sequential export.

        Args:
            items: List of (cq_obj, filepath) tuples
            file_format: "step" or "stl"
            strict: If True, raise on first failure; if False, warn and continue
            linear_tolerance: STL mesh tolerance (ignored for STEP)
            angular_tolerance: STL angular tolerance (ignored for STEP)

        Returns:
            List of successfully exported file paths

        Raises:
            Exception: If strict=True and any export fails
        """
        if not items:
            return []

        exported = []

        for obj, filepath in items:
            try:
                if file_format.lower() == "step":
                    path = GridfinityExporter.to_step(obj, filepath)
                elif file_format.lower() == "stl":
                    path = GridfinityExporter.to_stl(obj, filepath, linear_tolerance, angular_tolerance)
                else:
                    raise ValueError(f"Unsupported format: {file_format}")
                exported.append(path)
            except Exception as e:
                if strict:
                    raise
                warnings.warn(f"Failed to export {filepath}: {e}")

        return exported
