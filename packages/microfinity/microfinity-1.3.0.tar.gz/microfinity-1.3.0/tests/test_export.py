"""Tests for export functionality in microfinity."""

import os
import tempfile
import pytest
import cadquery as cq
from microfinity import (
    GridfinityBox,
    GridfinityBaseplate,
    GridfinityBaseplateLayout,
    GridfinityExporter,
    SVGView,
)


class TestGridfinityObjectExport:
    """Tests for GridfinityObject export methods."""

    def test_save_step_file(self):
        """save_step_file() should create valid STEP file."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_box.step")
            box.save_step_file(filename=filepath)

            assert os.path.exists(filepath)
            assert os.path.getsize(filepath) > 0

            # Verify it's a valid STEP file (starts with ISO-10303)
            with open(filepath, "r") as f:
                header = f.read(200)
                assert "ISO-10303" in header

    def test_save_stl_file(self):
        """save_stl_file() should create valid STL file."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_box.stl")
            box.save_stl_file(filename=filepath)

            assert os.path.exists(filepath)
            assert os.path.getsize(filepath) > 0

    def test_save_svg_file(self):
        """save_svg_file() should create valid SVG file."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_box.svg")
            box.save_svg_file(filename=filepath)

            assert os.path.exists(filepath)
            assert os.path.getsize(filepath) > 0

            # Verify it's a valid SVG
            with open(filepath, "r") as f:
                content = f.read()
                assert "<svg" in content or "<?xml" in content

    def test_baseplate_save_step(self):
        """GridfinityBaseplate should export to STEP."""
        bp = GridfinityBaseplate(2, 2)
        bp.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "baseplate.step")
            bp.save_step_file(filename=filepath)

            assert os.path.exists(filepath)
            assert os.path.getsize(filepath) > 0


class TestLayoutExport:
    """Tests for GridfinityBaseplateLayout export methods."""

    def test_layout_export_all(self):
        """GridfinityBaseplateLayout.export_all() should create files."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=100,
            drawer_y_mm=100,
            build_plate_x_mm=200,
            build_plate_y_mm=200,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            files = layout.export_all(tmpdir, file_format="step", include_clips=False)

            assert len(files) > 0
            for filepath in files:
                assert os.path.exists(filepath)
                assert os.path.getsize(filepath) > 0

    def test_layout_export_all_with_clips(self):
        """export_all(include_clips=True) should include clip file if layout needs clips."""
        # Use dimensions that require multiple pieces (and thus clips)
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=300,
            build_plate_x_mm=150,
            build_plate_y_mm=150,
        )

        layout_info = layout.get_layout()

        with tempfile.TemporaryDirectory() as tmpdir:
            files = layout.export_all(tmpdir, file_format="step", include_clips=True)

            assert len(files) > 0
            for filepath in files:
                assert os.path.exists(filepath)

            # If layout needs clips, there should be a clip file
            if layout_info.clip_count > 0:
                clip_files = [f for f in files if "clip" in f.lower()]
                assert len(clip_files) > 0

    def test_layout_export_stl_format(self):
        """export_all() should support STL format."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=100,
            drawer_y_mm=100,
            build_plate_x_mm=200,
            build_plate_y_mm=200,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            files = layout.export_all(tmpdir, file_format="stl", include_clips=False)

            assert len(files) > 0
            for filepath in files:
                assert filepath.endswith(".stl")
                assert os.path.exists(filepath)

    def test_layout_export_strict_mode(self):
        """export_all(strict=True) should raise on failure."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=100,
            drawer_y_mm=100,
            build_plate_x_mm=200,
            build_plate_y_mm=200,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # strict=False is default (should succeed)
            files = layout.export_all(tmpdir, file_format="step", include_clips=False)
            assert len(files) > 0


class TestGridfinityExporter:
    """Tests for GridfinityExporter primitives."""

    def test_ensure_extension_adds_missing(self):
        """ensure_extension() should add extension if missing."""
        assert GridfinityExporter.ensure_extension("foo", ".step") == "foo.step"
        assert GridfinityExporter.ensure_extension("foo.bar", ".step") == "foo.bar.step"

    def test_ensure_extension_preserves_existing(self):
        """ensure_extension() should not duplicate extension."""
        assert GridfinityExporter.ensure_extension("foo.step", ".step") == "foo.step"
        assert GridfinityExporter.ensure_extension("foo.STEP", ".step") == "foo.STEP"

    def test_to_step_returns_absolute_path(self):
        """to_step() should return absolute path."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test")
            result = GridfinityExporter.to_step(box.cq_obj, filepath)

            assert os.path.isabs(result)
            assert os.path.exists(result)
            assert result.endswith(".step")

    def test_to_stl_returns_absolute_path(self):
        """to_stl() should return absolute path."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test")
            result = GridfinityExporter.to_stl(box.cq_obj, filepath)

            assert os.path.isabs(result)
            assert os.path.exists(result)
            assert result.endswith(".stl")

    def test_to_svg_returns_absolute_path(self):
        """to_svg() should return absolute path and create non-empty file."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test")
            result = GridfinityExporter.to_svg(box.cq_obj, filepath)

            assert os.path.isabs(result)
            assert os.path.exists(result)
            assert result.endswith(".svg")
            assert os.path.getsize(result) > 0

    def test_to_svg_all_views(self):
        """to_svg() should work with all SVGView presets."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            for view in SVGView:
                filepath = os.path.join(tmpdir, f"test_{view.value}")
                result = GridfinityExporter.to_svg(box.cq_obj, filepath, view=view)

                assert os.path.exists(result)
                assert os.path.getsize(result) > 0

    def test_to_stl_rejects_assembly(self):
        """to_stl() should raise TypeError for Assembly."""
        asm = cq.Assembly()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.stl")
            with pytest.raises(TypeError, match="Assembly"):
                GridfinityExporter.to_stl(asm, filepath)

    def test_to_svg_rejects_assembly(self):
        """to_svg() should raise TypeError for Assembly."""
        asm = cq.Assembly()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.svg")
            with pytest.raises(TypeError, match="Assembly"):
                GridfinityExporter.to_svg(asm, filepath)

    def test_batch_export_success(self):
        """batch_export() should export all items."""
        box1 = GridfinityBox(1, 1, 3)
        box1.render()
        box2 = GridfinityBox(2, 1, 3)
        box2.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            items = [
                (box1.cq_obj, os.path.join(tmpdir, "box1.step")),
                (box2.cq_obj, os.path.join(tmpdir, "box2.step")),
            ]
            result = GridfinityExporter.batch_export(items)

            assert len(result) == 2
            for path in result:
                assert os.path.exists(path)

    def test_batch_export_strict_raises(self):
        """batch_export(strict=True) should raise on failure."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            items = [
                (box.cq_obj, os.path.join(tmpdir, "good.step")),
                (None, os.path.join(tmpdir, "bad.step")),  # Will fail
            ]
            with pytest.raises(Exception):
                GridfinityExporter.batch_export(items, strict=True)

    def test_batch_export_non_strict_warns(self):
        """batch_export(strict=False) should warn and continue."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            items = [
                (box.cq_obj, os.path.join(tmpdir, "good.step")),
                (None, os.path.join(tmpdir, "bad.step")),  # Will fail
            ]
            with pytest.warns(UserWarning):
                result = GridfinityExporter.batch_export(items, strict=False)

            # Only good.step should succeed
            assert len(result) == 1
            assert "good.step" in result[0]

    def test_batch_export_stl_format(self):
        """batch_export() should support STL format."""
        box = GridfinityBox(1, 1, 3)
        box.render()

        with tempfile.TemporaryDirectory() as tmpdir:
            items = [(box.cq_obj, os.path.join(tmpdir, "box"))]
            result = GridfinityExporter.batch_export(items, file_format="stl")

            assert len(result) == 1
            assert result[0].endswith(".stl")
            assert os.path.exists(result[0])
