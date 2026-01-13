"""Golden tests for geometry regression detection.

These tests compare rendered geometry against stored "golden" signatures
(bounding box + volume) to catch unintended changes.

To update baselines after intentional changes:
    UPDATE_GOLDEN=1 pytest tests/test_golden.py

Golden data is stored in tests/golden_data/*.json
"""

import pytest
import sys
from pathlib import Path

# Add tests directory to path for golden_test_utils import
sys.path.insert(0, str(Path(__file__).parent))
from golden_test_utils import assert_matches_golden

from microfinity import (
    GridfinityBox,
    GridfinitySolidBox,
    GridfinityBaseplate,
    GridfinityBaseplateLayout,
    GridfinityConnectionClip,
    GridfinityDrawerSpacer,
)


class TestGoldenBox:
    """Golden tests for GridfinityBox."""

    def test_box_1x1x3_basic(self):
        """Basic 1x1x3 box."""
        box = GridfinityBox(1, 1, 3)
        geom = box.render()
        assert_matches_golden(geom, "box_1x1x3_basic")

    def test_box_2x2x4_basic(self):
        """Basic 2x2x4 box."""
        box = GridfinityBox(2, 2, 4)
        geom = box.render()
        assert_matches_golden(geom, "box_2x2x4_basic")

    def test_box_2x2x4_lite(self):
        """2x2x4 lite style box."""
        box = GridfinityBox(2, 2, 4, lite_style=True)
        geom = box.render()
        assert_matches_golden(geom, "box_2x2x4_lite")

    def test_box_2x1x3_solid(self):
        """2x1x3 solid (no interior) box."""
        box = GridfinityBox(2, 1, 3, solid=True)
        geom = box.render()
        assert_matches_golden(geom, "box_2x1x3_solid")

    def test_box_3x3x5_with_magnets(self):
        """3x3x5 box with magnet holes."""
        box = GridfinityBox(3, 3, 5, holes=True)
        geom = box.render()
        assert_matches_golden(geom, "box_3x3x5_magnets")


class TestGoldenSolidBox:
    """Golden tests for GridfinitySolidBox."""

    def test_solidbox_1x1x3(self):
        """1x1x3 solid box."""
        box = GridfinitySolidBox(1, 1, 3)
        geom = box.render()
        assert_matches_golden(geom, "solidbox_1x1x3")

    def test_solidbox_2x2x4(self):
        """2x2x4 solid box."""
        box = GridfinitySolidBox(2, 2, 4)
        geom = box.render()
        assert_matches_golden(geom, "solidbox_2x2x4")


class TestGoldenBaseplate:
    """Golden tests for GridfinityBaseplate."""

    def test_baseplate_2x2(self):
        """2x2 baseplate."""
        bp = GridfinityBaseplate(2, 2)
        geom = bp.render()
        assert_matches_golden(geom, "baseplate_2x2")

    def test_baseplate_4x3(self):
        """4x3 baseplate."""
        bp = GridfinityBaseplate(4, 3)
        geom = bp.render()
        assert_matches_golden(geom, "baseplate_4x3")

    def test_baseplate_3x3_with_screws(self):
        """3x3 baseplate with corner screws."""
        bp = GridfinityBaseplate(3, 3, corner_screws=True)
        geom = bp.render()
        assert_matches_golden(geom, "baseplate_3x3_screws")


class TestGoldenClip:
    """Golden tests for GridfinityConnectionClip."""

    def test_clip_default(self):
        """Default clip (no clearance)."""
        clip = GridfinityConnectionClip()
        geom = clip.render()
        assert_matches_golden(geom, "clip_default")

    def test_clip_clearance_0p2(self):
        """Clip with 0.2mm clearance."""
        clip = GridfinityConnectionClip(clip_clearance_mm=0.2)
        geom = clip.render()
        assert_matches_golden(geom, "clip_clearance_0p2")

    def test_clip_flat_default(self):
        """Default clip in flat orientation."""
        clip = GridfinityConnectionClip()
        geom = clip.render_flat()
        assert_matches_golden(geom, "clip_flat_default")


class TestGoldenSpacer:
    """Golden tests for GridfinityDrawerSpacer."""

    def test_spacer_100x50(self):
        """100x50mm drawer spacer."""
        spacer = GridfinityDrawerSpacer(100, 50)
        geom = spacer.render()
        assert_matches_golden(geom, "spacer_100x50")
