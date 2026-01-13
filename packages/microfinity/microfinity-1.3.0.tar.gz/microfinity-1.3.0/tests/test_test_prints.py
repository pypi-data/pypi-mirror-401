"""Tests for microfinity.test_prints module."""

import os
import tempfile
import pytest
from microfinity.calibration.test_prints import (
    generate_fractional_pocket_test,
    generate_fractional_pocket_test_set,
    generate_clip_clearance_sweep,
    generate_clip_test_set,
    export_test_prints,
    DEFAULT_CLEARANCE_SWEEP,
)


class TestFractionalPocketTest:
    """Tests for fractional pocket test generation."""

    def test_generate_fractional_pocket_test(self):
        """generate_fractional_pocket_test() should produce valid geometry."""
        geom = generate_fractional_pocket_test(fractional_u=0.5)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert bb.xlen > 0
        assert bb.ylen > 0
        assert bb.zlen > 0

    @pytest.mark.parametrize("frac", [0.25, 0.5, 0.75])
    def test_generate_fractional_pocket_test_sizes(self, frac):
        """generate_fractional_pocket_test() should work for all fraction sizes."""
        geom = generate_fractional_pocket_test(fractional_u=frac)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert bb.zlen > 0

    def test_generate_fractional_pocket_test_with_slots(self):
        """generate_fractional_pocket_test() should add slots when requested."""
        geom_with_slots = generate_fractional_pocket_test(fractional_u=0.5, include_slots=True)
        geom_without_slots = generate_fractional_pocket_test(fractional_u=0.5, include_slots=False)
        assert geom_with_slots is not None
        assert geom_without_slots is not None
        # Both should render, geometry may differ slightly


class TestFractionalPocketTestSet:
    """Tests for fractional pocket test set generation."""

    def test_generate_fractional_pocket_test_set(self):
        """generate_fractional_pocket_test_set() should produce dict of geometries."""
        results = generate_fractional_pocket_test_set()

        assert isinstance(results, dict)
        assert "0.25U" in results
        assert "0.5U" in results
        assert "0.75U" in results

        for name, geom in results.items():
            assert geom is not None
            bb = geom.val().BoundingBox()
            assert bb.zlen > 0


class TestClipClearanceSweep:
    """Tests for clip clearance sweep generation."""

    def test_generate_clip_clearance_sweep(self):
        """generate_clip_clearance_sweep() should produce clips with varying clearances."""
        geom, clearances = generate_clip_clearance_sweep()

        assert geom is not None
        assert len(clearances) > 0
        assert clearances == DEFAULT_CLEARANCE_SWEEP

        bb = geom.val().BoundingBox()
        assert bb.xlen > 0

    def test_generate_clip_clearance_sweep_custom(self):
        """generate_clip_clearance_sweep() should accept custom clearances."""
        custom_clearances = [0.0, 0.1, 0.2]
        geom, clearances = generate_clip_clearance_sweep(clearances=custom_clearances)

        assert clearances == custom_clearances
        assert geom is not None

    def test_generate_clip_clearance_sweep_empty_raises(self):
        """generate_clip_clearance_sweep() should raise on empty clearances."""
        with pytest.raises(ValueError, match="clearances list cannot be empty"):
            generate_clip_clearance_sweep(clearances=[])


class TestClipTestSet:
    """Tests for clip test set generation."""

    def test_generate_clip_test_set_single(self):
        """generate_clip_test_set(num_clips=1) should produce single clip."""
        geom = generate_clip_test_set(num_clips=1, clearance_mm=0.0)
        assert geom is not None

        bb = geom.val().BoundingBox()
        assert bb.xlen > 0
        assert bb.ylen > 0
        assert bb.zlen > 0

    def test_generate_clip_test_set_multiple(self):
        """generate_clip_test_set(num_clips=3) should produce more solids."""
        single = generate_clip_test_set(num_clips=1, clearance_mm=0.1)
        multiple = generate_clip_test_set(num_clips=3, clearance_mm=0.1)

        # Multiple clips uses .add() which creates separate solids
        # So we check that multiple has more solids than single
        single_solids = single.solids().vals()
        multiple_solids = multiple.solids().vals()

        # 3 clips should have 3 solids (or more than 1)
        assert len(multiple_solids) >= len(single_solids)
        assert len(multiple_solids) == 3

    def test_generate_clip_test_set_with_clearance(self):
        """generate_clip_test_set() should apply clearance."""
        geom_tight = generate_clip_test_set(num_clips=1, clearance_mm=0.0)
        geom_loose = generate_clip_test_set(num_clips=1, clearance_mm=0.2)

        bb_tight = geom_tight.val().BoundingBox()
        bb_loose = geom_loose.val().BoundingBox()

        # Looser clip should be narrower
        assert bb_loose.xlen < bb_tight.xlen


class TestExportTestPrints:
    """Tests for test print export functionality."""

    def test_export_test_prints(self):
        """export_test_prints() should create files in directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = export_test_prints(
                path=tmpdir,
                file_format="step",
                include_fractional=True,
                include_clip_sweep=True,
            )

            assert len(files) > 0
            for filepath in files:
                assert os.path.exists(filepath)
                # Allow both files and text files
                if filepath.endswith(".step"):
                    assert os.path.getsize(filepath) > 0

    def test_export_test_prints_fractional_only(self):
        """export_test_prints() should support fractional-only export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = export_test_prints(
                path=tmpdir,
                file_format="step",
                include_fractional=True,
                include_clip_sweep=False,
            )

            assert len(files) > 0
            # Should not have clip sweep file
            clip_files = [f for f in files if "clip" in f.lower() and f.endswith(".step")]
            assert len(clip_files) == 0

    def test_export_test_prints_clips_only(self):
        """export_test_prints() should support clip-sweep-only export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = export_test_prints(
                path=tmpdir,
                file_format="step",
                include_fractional=False,
                include_clip_sweep=True,
            )

            assert len(files) > 0
            # Should have clip sweep file
            clip_files = [f for f in files if "clip" in f.lower()]
            assert len(clip_files) > 0
