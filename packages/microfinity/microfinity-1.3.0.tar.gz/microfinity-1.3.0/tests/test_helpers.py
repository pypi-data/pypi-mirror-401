"""Tests for microfinity.core.helpers module."""

import pytest
import cadquery as cq
from microfinity.core.helpers import union_all, quarter_circle, chamf_cyl, chamf_rect


class TestUnionAll:
    """Tests for union_all() helper function."""

    def test_union_all_empty(self):
        """union_all([]) should return None."""
        result = union_all([])
        assert result is None

    def test_union_all_single(self):
        """union_all with single item should return that item."""
        box = cq.Workplane("XY").box(10, 10, 10)
        result = union_all([box])
        bb = result.val().BoundingBox()
        assert abs(bb.xlen - 10) < 0.01
        assert abs(bb.ylen - 10) < 0.01
        assert abs(bb.zlen - 10) < 0.01

    def test_union_all_multiple(self):
        """union_all should combine multiple workplanes."""
        boxes = [
            cq.Workplane("XY").box(10, 10, 10).translate((0, 0, 0)),
            cq.Workplane("XY").box(10, 10, 10).translate((15, 0, 0)),
            cq.Workplane("XY").box(10, 10, 10).translate((30, 0, 0)),
        ]
        result = union_all(boxes)
        bb = result.val().BoundingBox()
        # Combined BB should span all three boxes
        assert abs(bb.xlen - 40) < 0.01  # 30 + 10
        assert abs(bb.ylen - 10) < 0.01
        assert abs(bb.zlen - 10) < 0.01

    def test_union_all_overlapping(self):
        """union_all should handle overlapping geometry."""
        boxes = [
            cq.Workplane("XY").box(10, 10, 10).translate((0, 0, 0)),
            cq.Workplane("XY").box(10, 10, 10).translate((5, 0, 0)),  # Overlaps
        ]
        result = union_all(boxes)
        bb = result.val().BoundingBox()
        # Overlapping boxes should fuse
        assert abs(bb.xlen - 15) < 0.01  # 5 + 10
        assert abs(bb.ylen - 10) < 0.01


class TestQuarterCircle:
    """Tests for quarter_circle() helper function."""

    def test_quarter_circle_renders(self):
        """quarter_circle() should produce valid geometry."""
        geom = quarter_circle(outer_rad=10, inner_rad=5, height=3)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert bb.xlen > 0
        assert bb.ylen > 0
        assert abs(bb.zlen - 3) < 0.1  # Allow for chamfer

    @pytest.mark.parametrize("quad", ["tr", "tl", "br", "bl"])
    def test_quarter_circle_quadrants(self, quad):
        """quarter_circle() should work for all quadrants."""
        geom = quarter_circle(outer_rad=10, inner_rad=5, height=3, quad=quad)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert bb.zlen > 0

    def test_quarter_circle_no_chamfer(self):
        """quarter_circle(chamf=0) should have no chamfer."""
        geom = quarter_circle(outer_rad=10, inner_rad=5, height=3, chamf=0)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert abs(bb.zlen - 3) < 0.01


class TestChamfCyl:
    """Tests for chamf_cyl() helper function."""

    def test_chamf_cyl_renders(self):
        """chamf_cyl() should produce chamfered cylinder."""
        geom = chamf_cyl(rad=5, height=10, chamf=0.5)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert abs(bb.xlen - 10) < 0.1  # diameter
        assert abs(bb.ylen - 10) < 0.1
        assert abs(bb.zlen - 10) < 0.1

    def test_chamf_cyl_no_chamfer(self):
        """chamf_cyl(chamf=0) should produce plain cylinder."""
        geom = chamf_cyl(rad=5, height=10, chamf=0)
        assert geom is not None
        bb = geom.val().BoundingBox()
        assert abs(bb.zlen - 10) < 0.01


class TestChamfRect:
    """Tests for chamf_rect() helper function."""

    def test_chamf_rect_renders(self):
        """chamf_rect() should produce chamfered box."""
        geom = chamf_rect(length=10, width=8, height=5)
        assert geom is not None
        bb = geom.val().BoundingBox()
        # Note: chamf_rect adds tolerance (0.5) to dimensions
        assert bb.xlen > 10
        assert bb.ylen > 8
        assert bb.zlen > 0

    def test_chamf_rect_with_angle(self):
        """chamf_rect() should support rotation angle."""
        geom = chamf_rect(length=10, width=8, height=5, angle=45)
        assert geom is not None
        bb = geom.val().BoundingBox()
        # Rotated box should have different BB
        assert bb.xlen > 0
        assert bb.ylen > 0
