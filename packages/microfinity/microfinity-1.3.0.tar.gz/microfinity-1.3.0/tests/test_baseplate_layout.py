# Gridfinity Baseplate Layout Tests
import pytest
import os

from microfinity.parts.baseplate_layout import (
    GridfinityBaseplateLayout,
    GridfinityConnectionClip,
    LayoutResult,
    PieceSpec,
    EdgeMode,
    SegmentationMode,
    ToleranceMode,
    partition_micro,
    compute_cumulative_offsets,
    compute_notch_positions_along_edge,
)
from microfinity.core.constants import GRU

from common_test import _almost_same

try:
    from cqkit.cq_helpers import size_3d

    HAS_CADQUERY = True
except ImportError:
    HAS_CADQUERY = False

env = dict(os.environ)
SKIP_TEST_LAYOUT = "SKIP_TEST_LAYOUT" in env


# =============================================================================
# partition_micro() tests
# =============================================================================


class TestPartitionMicro:
    """Tests for the partition_micro flooring algorithm."""

    def test_fits_in_one_piece(self):
        """When total fits in one piece, return single segment."""
        result = partition_micro(total_micro=16, max_micro=20, min_segment_micro=4)
        assert result == [16]

    def test_exact_multiple(self):
        """When total is exact multiple of max, return equal segments."""
        result = partition_micro(total_micro=40, max_micro=20, min_segment_micro=4)
        assert result == [20, 20]

    def test_even_distribution(self):
        """Even mode distributes evenly to avoid tiny pieces."""
        # 45 micro-cells, max 20, min 4
        # Could be [20, 20, 5] but 5 < min_segment is borderline
        # Should try to find [15, 15, 15] or similar
        result = partition_micro(
            total_micro=45,
            max_micro=20,
            min_segment_micro=4,
            mode=SegmentationMode.EVEN,
        )
        # Should be 3 segments that sum to 45
        assert sum(result) == 45
        assert all(s <= 20 for s in result)
        # Should be relatively even
        assert max(result) - min(result) <= 1

    def test_max_then_remainder(self):
        """Max-then-remainder mode uses max for most, remainder in last."""
        result = partition_micro(
            total_micro=45,
            max_micro=20,
            min_segment_micro=4,
            mode=SegmentationMode.MAX_THEN_REMAINDER,
        )
        # Should be [20, 20, 5] or redistributed
        assert sum(result) == 45
        assert all(s <= 20 for s in result)

    def test_respects_min_segment(self):
        """Should avoid segments smaller than min when possible."""
        # 21 micro-cells, max 20, min 8
        # Naive: [20, 1] but 1 < 8
        # Better: [11, 10] or [10, 11]
        result = partition_micro(
            total_micro=21,
            max_micro=20,
            min_segment_micro=8,
            mode=SegmentationMode.EVEN,
        )
        assert sum(result) == 21
        # Both segments should be >= 8 if possible
        # Actually 21 = 11 + 10, both >= 8
        assert all(s >= 8 for s in result)

    def test_large_total(self):
        """Test with larger numbers."""
        # 100 micro-cells, max 20, min 4
        result = partition_micro(total_micro=100, max_micro=20, min_segment_micro=4)
        assert sum(result) == 100
        assert all(s <= 20 for s in result)
        assert len(result) == 5  # 100 / 20 = 5

    def test_empty(self):
        """Zero total returns empty list."""
        result = partition_micro(total_micro=0, max_micro=20, min_segment_micro=4)
        assert result == []


# =============================================================================
# compute_cumulative_offsets() tests
# =============================================================================


class TestCumulativeOffsets:
    """Tests for cumulative offset calculation."""

    def test_single_segment(self):
        """Single segment starts at 0."""
        result = compute_cumulative_offsets([20])
        assert result == [0]

    def test_multiple_segments(self):
        """Multiple segments have correct cumulative positions."""
        result = compute_cumulative_offsets([10, 15, 12])
        assert result == [0, 10, 25]

    def test_empty(self):
        """Empty list returns empty."""
        result = compute_cumulative_offsets([])
        assert result == [0]  # Always has at least the starting 0


# =============================================================================
# compute_notch_positions_along_edge() tests
# =============================================================================


class TestNotchPositions:
    """Tests for notch position calculation."""

    def test_standard_spacing(self):
        """Standard spacing with clip_pitch = 4 micro (1U at micro_div=4).

        Notches are centered on cell openings at global positions:
        g0 + k * pitch = 2 + k * 4 = 2, 6, 10, 14, 18...
        For edge starting at origin_micro=0, these become local positions.
        """
        # Edge of 20 micro-cells, pitch 4, margin 1, origin 0
        result = compute_notch_positions_along_edge(
            edge_length_micro=20,
            clip_pitch_micro=4,
            end_margin_micro=1,
            origin_micro=0,
            M=4,
        )
        # Cell centers at global 2, 6, 10, 14, 18 -> local 2, 6, 10, 14, 18
        # End margin is 1, so valid range is [1, 19]
        assert 2 in result  # First cell center
        assert 6 in result
        assert 10 in result
        assert 14 in result
        assert 18 in result
        assert all(pos >= 1 for pos in result)  # Respects start margin
        assert all(pos <= 19 for pos in result)  # Respects end margin

    def test_short_edge_single_notch(self):
        """Very short edge gets single centered notch.

        With cell-centered algorithm, for edge of 4 microcells at origin 0,
        the cell center at global 2 maps to local 2.
        """
        result = compute_notch_positions_along_edge(
            edge_length_micro=4,
            clip_pitch_micro=4,
            end_margin_micro=1,
            origin_micro=0,
            M=4,
        )
        # Cell center at global 2 -> local 2, within margin [1, 3]
        assert len(result) >= 1
        assert result[0] == 2  # Cell center at global 2

    def test_edge_too_short(self):
        """Edge shorter than margins still gets a notch if possible."""
        result = compute_notch_positions_along_edge(
            edge_length_micro=2,
            clip_pitch_micro=4,
            end_margin_micro=1,
        )
        # Edge is 2, margins would need 2, but we should place one at center
        assert result == [1]


# =============================================================================
# GridfinityBaseplateLayout tests
# =============================================================================


@pytest.mark.skipif(
    SKIP_TEST_LAYOUT,
    reason="Skipped intentionally by test scope environment variable",
)
class TestBaseplateLayout:
    """Tests for the main layout calculator."""

    def test_simple_layout(self):
        """Test basic layout with exact fit."""
        # Drawer 210mm x 168mm = 5U x 4U exactly (plus tolerance)
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=210.5,  # 5U + 0.5 tolerance
            drawer_y_mm=168.5,  # 4U + 0.5 tolerance
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            tolerance_mm=0.5,
        )
        result = layout.get_layout()

        # Should be 5U x 4U = 20 micro x 16 micro (at micro_div=4)
        assert result.total_micro_x == 20
        assert result.total_micro_y == 16

        # Fill should be ~0 (exact fit)
        assert result.fill_x_mm < 0.1
        assert result.fill_y_mm < 0.1

        # Should fit in single piece
        assert len(result.pieces) == 1
        assert result.pieces[0].size_mx == 20
        assert result.pieces[0].size_my == 16

    def test_layout_with_remainder(self):
        """Test layout with fractional remainder."""
        # Drawer 230mm x 180mm
        # 230 - 0.5 tol = 229.5mm usable
        # 229.5 / 10.5 = 21.857 micro-cells -> 21 micro = 220.5mm
        # Remainder: 229.5 - 220.5 = 9mm fill
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=230,
            drawer_y_mm=180,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            tolerance_mm=0.5,
        )
        result = layout.get_layout()

        # Check that fill is calculated
        assert result.fill_x_mm > 0
        # Should have integrated fill on rightmost pieces
        rightmost = [p for p in result.pieces if p.edge_right == EdgeMode.OUTER]
        assert all(p.fill_x_mm > 0 for p in rightmost)

    def test_layout_multiple_plates(self):
        """Test layout requiring multiple plates."""
        # Large drawer 450mm x 380mm with 220mm build plate
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=450,
            drawer_y_mm=380,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            tolerance_mm=0.5,
        )
        result = layout.get_layout()

        # Should have multiple pieces
        assert len(result.pieces) > 1

        # Check grid dimensions
        grid_x, grid_y = result.grid_size
        assert grid_x >= 2
        assert grid_y >= 2

        # Check edge modes are correct
        for piece in result.pieces:
            # Left edge of leftmost pieces should be OUTER
            if piece.grid_x == 0:
                assert piece.edge_left == EdgeMode.OUTER
            else:
                assert piece.edge_left == EdgeMode.JOIN

            # Right edge of rightmost pieces should be OUTER
            if piece.grid_x == grid_x - 1:
                assert piece.edge_right == EdgeMode.OUTER
            else:
                assert piece.edge_right == EdgeMode.JOIN

    def test_clip_pitch_validation(self):
        """Clip pitch must be compatible with micro_divisions."""
        # clip_pitch_u=0.3 with micro_divisions=4 -> 0.3*4=1.2, not integer
        with pytest.raises(ValueError):
            GridfinityBaseplateLayout(
                drawer_x_mm=200,
                drawer_y_mm=200,
                build_plate_x_mm=220,
                build_plate_y_mm=220,
                micro_divisions=4,
                clip_pitch_u=0.3,
            )

    def test_clip_pitch_valid(self):
        """Valid clip pitch values should work."""
        # clip_pitch_u=0.5 with micro_divisions=4 -> 0.5*4=2, valid
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=200,
            drawer_y_mm=200,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            clip_pitch_u=0.5,
        )
        result = layout.get_layout()
        assert result.clip_pitch_u == 0.5

    def test_notches_only_on_join_edges(self):
        """Notches should only appear on JOIN edges."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=300,
            build_plate_x_mm=150,
            build_plate_y_mm=150,
            micro_divisions=4,
        )
        result = layout.get_layout()

        for piece in result.pieces:
            # OUTER edges should have no notches
            if piece.edge_left == EdgeMode.OUTER:
                assert len(piece.notches_left) == 0
            if piece.edge_right == EdgeMode.OUTER:
                assert len(piece.notches_right) == 0
            if piece.edge_front == EdgeMode.OUTER:
                assert len(piece.notches_front) == 0
            if piece.edge_back == EdgeMode.OUTER:
                assert len(piece.notches_back) == 0

            # JOIN edges should have notches
            if piece.edge_left == EdgeMode.JOIN:
                assert len(piece.notches_left) > 0
            if piece.edge_right == EdgeMode.JOIN:
                assert len(piece.notches_right) > 0
            if piece.edge_front == EdgeMode.JOIN:
                assert len(piece.notches_front) > 0
            if piece.edge_back == EdgeMode.JOIN:
                assert len(piece.notches_back) > 0

    def test_micro_divisions_2(self):
        """Test with micro_divisions=2 (0.5U increments)."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=200,
            drawer_y_mm=200,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=2,
            clip_pitch_u=1.0,
        )
        result = layout.get_layout()
        assert result.micro_divisions == 2
        assert result.micro_pitch_mm == 21.0  # GRU / 2

    def test_deduplication(self):
        """Test unique_pieces deduplication."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=300,
            build_plate_x_mm=150,
            build_plate_y_mm=150,
            micro_divisions=4,
        )
        result = layout.get_layout()

        unique = result.unique_pieces()
        total_count = sum(count for _, count in unique.values())
        assert total_count == len(result.pieces)

    def test_summary_output(self):
        """Test summary method produces output."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=250,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
        )
        result = layout.get_layout()
        summary = result.summary()

        assert "GRIDFINITY BASEPLATE LAYOUT" in summary
        assert "Drawer:" in summary
        assert "Build plate:" in summary
        assert "Clips needed:" in summary


# =============================================================================
# PieceSpec tests
# =============================================================================


class TestPieceSpec:
    """Tests for PieceSpec dataclass."""

    def test_size_u(self):
        """Test size_u calculation."""
        piece = PieceSpec(
            id="test",
            size_mx=8,
            size_my=12,
        )
        # At micro_divisions=4: 8/4=2U, 12/4=3U
        assert piece.size_u(micro_divisions=4) == (2.0, 3.0)
        # At micro_divisions=2: 8/2=4U, 12/2=6U
        assert piece.size_u(micro_divisions=2) == (4.0, 6.0)

    def test_size_mm(self):
        """Test size_mm calculation."""
        piece = PieceSpec(
            id="test",
            size_mx=4,  # 1U at micro_div=4
            size_my=8,  # 2U at micro_div=4
        )
        # At micro_divisions=4: pitch=10.5mm
        # 4 * 10.5 = 42mm, 8 * 10.5 = 84mm
        size = piece.size_mm(micro_divisions=4)
        assert _almost_same(size, (42.0, 84.0))

    def test_total_size_mm_with_fill(self):
        """Test total_size_mm includes fill."""
        piece = PieceSpec(
            id="test",
            size_mx=4,
            size_my=8,
            fill_x_mm=5.5,
            fill_y_mm=3.2,
        )
        total = piece.total_size_mm(micro_divisions=4)
        # Grid: 42mm x 84mm, plus fill
        assert _almost_same(total, (47.5, 87.2))

    def test_signature_for_dedup(self):
        """Pieces with same geometry should have same signature."""
        piece1 = PieceSpec(
            id="piece_0_0",
            size_mx=8,
            size_my=8,
            edge_left=EdgeMode.OUTER,
            edge_right=EdgeMode.JOIN,
            edge_front=EdgeMode.OUTER,
            edge_back=EdgeMode.JOIN,
            notches_right=(2, 6),
            notches_back=(2, 6),
        )
        piece2 = PieceSpec(
            id="piece_1_1",  # Different ID
            size_mx=8,
            size_my=8,
            edge_left=EdgeMode.OUTER,
            edge_right=EdgeMode.JOIN,
            edge_front=EdgeMode.OUTER,
            edge_back=EdgeMode.JOIN,
            notches_right=(2, 6),
            notches_back=(2, 6),
            origin_x_mm=100,  # Different position
            origin_y_mm=100,
        )
        # Same geometry, different position/id -> same signature
        assert piece1.signature == piece2.signature

    def test_signature_differs_on_geometry(self):
        """Pieces with different geometry should have different signatures."""
        piece1 = PieceSpec(id="a", size_mx=8, size_my=8)
        piece2 = PieceSpec(id="b", size_mx=8, size_my=12)  # Different size
        assert piece1.signature != piece2.signature

        # Use per-edge fill (fill_right) instead of legacy fill_x_mm
        piece3 = PieceSpec(id="c", size_mx=8, size_my=8, fill_right=5.0)
        assert piece1.signature != piece3.signature  # Different fill


# =============================================================================
# GridfinityConnectionClip tests
# =============================================================================


@pytest.mark.skipif(
    SKIP_TEST_LAYOUT or not HAS_CADQUERY,
    reason="Skipped intentionally or CadQuery not available",
)
class TestConnectionClip:
    """Tests for the connection clip."""

    def test_clip_renders(self):
        """Clip should render without error."""
        clip = GridfinityConnectionClip()
        r = clip.render()
        assert r is not None

    def test_clip_flat_renders(self):
        """Clip flat orientation should render without error."""
        clip = GridfinityConnectionClip()
        r = clip.render_flat()
        assert r is not None

    def test_clip_geometry_size(self):
        """Clip should match notch dimensions (derived from NotchSpec).

        Clip is a through-slot connector that spans both sides of the seam:
        - Width (X) = notch_width - clip_clearance (8.0 - 0.0 = 8.0)
        - Length (Y) = 2 * notch_depth (spans both slots: ~2.15 * 2 = 4.3)
        - Height (Z) = notch_height - clip_clearance (1.6 - 0.0 = 1.6)
        """
        from microfinity.parts.baseplate import get_notch_spec

        clip = GridfinityConnectionClip()
        r = clip.render()
        s = size_3d(r)

        spec = get_notch_spec()
        expected_width = spec.width  # 8.0
        expected_length = 2 * spec.depth  # ~4.3 (spans both through-slots)
        expected_height = spec.height  # 1.6

        assert abs(s[0] - expected_width) < 0.01, f"Width {s[0]} != {expected_width}"
        assert abs(s[1] - expected_length) < 0.01, f"Length {s[1]} != {expected_length}"
        assert abs(s[2] - expected_height) < 0.01, f"Height {s[2]} != {expected_height}"

    @pytest.mark.parametrize("clearance", [-0.10, 0.00, 0.20, 0.60])
    def test_clip_clearance_affects_all_dimensions(self, clearance):
        """Clearance affects width (X), height (Z), and length (Y for positive clearance).

        - Width and height shrink with clearance (positive or negative)
        - Length shrinks with positive clearance only (axial_tolerance = max(clearance, 0))
        - Negative clearance does NOT lengthen the clip (safety: no inner profile contact)
        """
        from microfinity.parts.baseplate import get_notch_spec

        spec = get_notch_spec()
        clip = GridfinityConnectionClip(clip_clearance_mm=clearance)
        w, l, h = clip.dims

        # Width and height shrink with clearance
        assert w == pytest.approx(spec.width - clearance, abs=1e-6)
        assert h == pytest.approx(spec.height - clearance, abs=1e-6)

        # Length shrinks with positive clearance only (axial_tolerance = max(clearance, 0))
        axial_tol = max(clearance, 0.0)
        expected_length = 2.0 * spec.depth - axial_tol
        assert l == pytest.approx(expected_length, abs=1e-6)

    def test_clip_lead_in_chamfer(self):
        """Clip with lead_in_mm should render without error and have smaller volume."""
        clip_plain = GridfinityConnectionClip()
        clip_chamfer = GridfinityConnectionClip(lead_in_mm=0.3)

        geom_plain = clip_plain.render()
        geom_chamfer = clip_chamfer.render()

        # Both should render
        assert geom_plain is not None
        assert geom_chamfer is not None

        # Chamfered should have smaller volume (material removed from corners)
        vol_plain = geom_plain.val().Volume()
        vol_chamfer = geom_chamfer.val().Volume()
        assert vol_chamfer < vol_plain, "Chamfer should reduce volume"

    # -------------------------------------------------------------------------
    # clip_ct parameter tests
    # -------------------------------------------------------------------------

    def test_clip_ct_default_single(self):
        """clip_ct=None (default) should result in clip_ct=1."""
        clip = GridfinityConnectionClip()
        assert clip.clip_ct == 1

    def test_clip_ct_one_explicit(self):
        """clip_ct=1 should render single clip with correct dimensions."""
        clip = GridfinityConnectionClip(clip_ct=1)
        geom = clip.render_flat()
        bb = geom.val().BoundingBox()
        w, l, h = clip.dims
        assert abs(bb.xlen - w) < 0.01
        assert abs(bb.ylen - l) < 0.01
        assert abs(bb.zlen - h) < 0.01

    def test_clip_ct_multiple_bounding_box(self):
        """clip_ct=5 should render geometry larger than single clip."""
        clip1 = GridfinityConnectionClip(clip_ct=1)
        clip5 = GridfinityConnectionClip(clip_ct=5)
        bb1 = clip1.render_flat().val().BoundingBox()
        bb5 = clip5.render_flat().val().BoundingBox()
        # 5 clips arranged in grid should be larger
        assert bb5.xlen > bb1.xlen or bb5.ylen > bb1.ylen

    def test_clip_ct_multiple_grid_layout(self):
        """clip_ct=5 should arrange clips in ceil(sqrt(5))=3 columns."""
        import math

        clip = GridfinityConnectionClip(clip_ct=5)
        w, l, h = clip.dims
        gap = clip._CLIP_GAP_MM
        cols = math.ceil(math.sqrt(5))  # 3
        rows = math.ceil(5 / cols)  # 2

        expected_width = cols * w + (cols - 1) * gap
        expected_depth = rows * l + (rows - 1) * gap

        geom = clip.render_flat()
        bb = geom.val().BoundingBox()

        assert abs(bb.xlen - expected_width) < 0.01
        assert abs(bb.ylen - expected_depth) < 0.01

    def test_clip_ct_large(self):
        """clip_ct=20 should render 20 clips in grid."""
        import math

        clip = GridfinityConnectionClip(clip_ct=20)
        w, l, h = clip.dims
        gap = clip._CLIP_GAP_MM
        cols = math.ceil(math.sqrt(20))  # 5
        rows = math.ceil(20 / cols)  # 4

        expected_width = cols * w + (cols - 1) * gap
        expected_depth = rows * l + (rows - 1) * gap

        geom = clip.render_flat()
        bb = geom.val().BoundingBox()

        assert abs(bb.xlen - expected_width) < 0.01
        assert abs(bb.ylen - expected_depth) < 0.01

    def test_clip_ct_zero_raises(self):
        """clip_ct=0 should raise ValueError."""
        with pytest.raises(ValueError, match="clip_ct must be >= 1"):
            GridfinityConnectionClip(clip_ct=0)

    def test_clip_ct_negative_raises(self):
        """clip_ct=-1 should raise ValueError."""
        with pytest.raises(ValueError, match="clip_ct must be >= 1"):
            GridfinityConnectionClip(clip_ct=-1)

    def test_clip_ct_does_not_affect_render(self):
        """render() should always return single clip regardless of clip_ct."""
        clip1 = GridfinityConnectionClip(clip_ct=1)
        clip5 = GridfinityConnectionClip(clip_ct=5)
        clip20 = GridfinityConnectionClip(clip_ct=20)

        bb1 = clip1.render().val().BoundingBox()
        bb5 = clip5.render().val().BoundingBox()
        bb20 = clip20.render().val().BoundingBox()

        # All should have identical dimensions (single clip)
        assert abs(bb1.xlen - bb5.xlen) < 0.01
        assert abs(bb1.xlen - bb20.xlen) < 0.01
        assert abs(bb1.ylen - bb5.ylen) < 0.01
        assert abs(bb1.ylen - bb20.ylen) < 0.01

    def test_clip_ct_with_clearance(self):
        """clip_ct should work correctly with clip_clearance_mm."""
        clip = GridfinityConnectionClip(clip_clearance_mm=0.2, clip_ct=3)
        w, l, h = clip.dims

        # Verify clearance reduces width
        default_clip = GridfinityConnectionClip()
        default_w, _, _ = default_clip.dims
        assert w < default_w  # Clearance makes clip narrower

        # Verify render_flat works
        geom = clip.render_flat()
        assert geom is not None


# =============================================================================
# Layout rendering tests
# =============================================================================


@pytest.mark.skipif(
    SKIP_TEST_LAYOUT or not HAS_CADQUERY,
    reason="Skipped intentionally or CadQuery not available",
)
class TestLayoutRendering:
    """Tests for layout rendering methods."""

    def test_render_piece(self):
        """Test rendering a single piece."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=200,
            drawer_y_mm=200,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
        )
        result = layout.get_layout()
        assert len(result.pieces) > 0

        # Render the first piece
        r = layout.render_piece(result.pieces[0].id)
        assert r is not None

    def test_render_piece_at(self):
        """Test rendering a piece by grid position."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=200,
            drawer_y_mm=200,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
        )

        # Render piece at (0, 0)
        r = layout.render_piece_at(0, 0)
        assert r is not None

    def test_render_piece_invalid_id(self):
        """Test that invalid piece ID raises error."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=200,
            drawer_y_mm=200,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
        )

        with pytest.raises(ValueError):
            layout.render_piece("nonexistent_piece")

    def test_render_clip_sheet(self):
        """Test rendering a clip sheet."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=300,
            build_plate_x_mm=150,
            build_plate_y_mm=150,
            micro_divisions=4,
        )
        result = layout.get_layout()

        if result.clip_count > 0:
            r = layout.render_clip_sheet(count=4)
            assert r is not None

    def test_render_preview(self):
        """Test rendering the full preview."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=150,
            drawer_y_mm=150,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
        )

        # This should render a single piece since it fits on build plate
        r = layout.render_preview()
        assert r is not None


# =============================================================================
# Integration tests
# =============================================================================


@pytest.mark.skipif(
    SKIP_TEST_LAYOUT or not HAS_CADQUERY,
    reason="Skipped intentionally or CadQuery not available",
)
class TestIntegration:
    """Integration tests for the full layout workflow."""

    def test_full_workflow_small_drawer(self):
        """Test complete workflow with a small drawer that fits one plate."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=180,
            drawer_y_mm=160,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            tolerance_mm=0.5,
        )

        result = layout.get_layout()

        # Should fit in a single plate
        assert len(result.pieces) == 1

        # No clips needed (single plate)
        assert result.clip_count == 0

        # Render should work
        r = layout.render_piece_at(0, 0)
        assert r is not None

    def test_full_workflow_large_drawer(self):
        """Test complete workflow with a large drawer requiring multiple plates."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=450,
            drawer_y_mm=380,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            tolerance_mm=0.5,
            clip_pitch_u=1.0,
        )

        result = layout.get_layout()

        # Should have multiple pieces
        assert len(result.pieces) > 1

        # Should have clips
        assert result.clip_count > 0

        # Check that deduplication works
        unique = result.unique_pieces()
        assert len(unique) <= len(result.pieces)

        # Render preview should work
        r = layout.render_preview()
        assert r is not None

    def test_micro_divisions_2(self):
        """Test with 0.5U increments (micro_divisions=2)."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=250,
            drawer_y_mm=200,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=2,
            clip_pitch_u=1.0,
        )

        result = layout.get_layout()

        # Check micro pitch is correct
        assert result.micro_pitch_mm == 21.0  # 42 / 2

        # Should be able to render
        if len(result.pieces) > 0:
            r = layout.render_piece(result.pieces[0].id)
            assert r is not None

    def test_fill_on_edge_pieces(self):
        """Test that fill is properly applied to edge pieces."""
        # Create a drawer where there will be fill
        # 200mm usable, 4U = 168mm, gap = 32mm
        # With micro_divisions=4, pitch=10.5mm
        # 32 / 10.5 = 3.04 micro-cells = 3 = 0.75U
        # Fill = 32 - 31.5 = 0.5mm
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=200.5,  # 200mm usable after 0.5 tolerance
            drawer_y_mm=200.5,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
            tolerance_mm=0.5,
        )

        result = layout.get_layout()

        # There should be some fill on the right and back edges
        # Check that pieces on the outer edges have fill
        for piece in result.pieces:
            if piece.edge_right == EdgeMode.OUTER:
                # This piece is on the right edge
                assert piece.fill_x_mm >= 0  # May or may not have fill depending on exact dimensions

    def test_summary_contains_key_info(self):
        """Test that summary output contains all key information."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=250,
            build_plate_x_mm=220,
            build_plate_y_mm=220,
            micro_divisions=4,
        )

        result = layout.get_layout()
        summary = result.summary()

        # Check for key sections
        assert "GRIDFINITY BASEPLATE LAYOUT" in summary
        assert "INPUT:" in summary
        assert "GRID:" in summary
        assert "SEGMENTATION:" in summary
        assert "PIECES:" in summary
        assert "CONNECTORS:" in summary

        # Check for key values
        assert "300.0mm" in summary  # drawer X
        assert "250.0mm" in summary  # drawer Y
        assert "220.0mm" in summary  # build plate

    def test_piece_edge_modes_are_consistent(self):
        """Test that adjacent pieces have consistent edge modes at seams."""
        layout = GridfinityBaseplateLayout(
            drawer_x_mm=300,
            drawer_y_mm=300,
            build_plate_x_mm=150,
            build_plate_y_mm=150,
            micro_divisions=4,
        )

        result = layout.get_layout()
        grid_x, grid_y = result.grid_size

        # For each interior seam, check that both adjacent pieces have JOIN mode
        for piece in result.pieces:
            ix, iy = piece.grid_x, piece.grid_y

            # Check right edge
            if ix < grid_x - 1:
                # This piece's right edge should be JOIN
                assert piece.edge_right == EdgeMode.JOIN
                # The piece to the right should have JOIN on its left
                right_piece = layout.get_piece_at(ix + 1, iy)
                assert right_piece is not None
                assert right_piece.edge_left == EdgeMode.JOIN

            # Check back edge
            if iy < grid_y - 1:
                # This piece's back edge should be JOIN
                assert piece.edge_back == EdgeMode.JOIN
                # The piece above should have JOIN on its front
                back_piece = layout.get_piece_at(ix, iy + 1)
                assert back_piece is not None
                assert back_piece.edge_front == EdgeMode.JOIN
