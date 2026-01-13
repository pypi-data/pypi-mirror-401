# Gridfinity tests
import pytest

# my modules
from microfinity import *
from microfinity.parts.baseplate import EdgeMode
from cqkit import FlatEdgeSelector
from cqkit.cq_helpers import size_3d
from common_test import (
    EXPORT_STEP_FILE_PATH,
    _almost_same,
    _faces_match,
    _export_files,
    SKIP_TEST_BASEPLATE,
)


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_make_baseplate():
    bp = GridfinityBaseplate(4, 3)
    r = bp.render()
    if _export_files("baseplate"):
        bp.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert bp.filename() == "gf_baseplate_4x3"
    assert _almost_same(size_3d(r), (168, 126, 4.75))
    assert _faces_match(r, ">Z", 16)
    assert _faces_match(r, "<Z", 1)
    edge_diff = abs(len(r.edges(FlatEdgeSelector(0)).vals()) - 104)
    assert edge_diff < 3


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_make_ext_baseplate():
    bp = GridfinityBaseplate(5, 4, ext_depth=5, corner_screws=True)
    r = bp.render()
    assert _almost_same(size_3d(r), (210, 168, 9.75))
    edge_diff = abs(len(r.edges(FlatEdgeSelector(0)).vals()) - 188)
    assert edge_diff < 3


# =============================================================================
# Connectable Baseplate Tests
# =============================================================================


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_baseplate_default_edge_modes():
    """Test that default edge modes are all OUTER (backward compatible)."""
    bp = GridfinityBaseplate(3, 3)
    assert bp.edge_modes["left"] == EdgeMode.OUTER
    assert bp.edge_modes["right"] == EdgeMode.OUTER
    assert bp.edge_modes["front"] == EdgeMode.OUTER
    assert bp.edge_modes["back"] == EdgeMode.OUTER
    assert not bp.has_connectors


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_baseplate_with_join_edges():
    """Test baseplate with JOIN edge modes."""
    bp = GridfinityBaseplate(
        3,
        3,
        edge_modes={
            "left": EdgeMode.OUTER,
            "right": EdgeMode.JOIN,
            "front": EdgeMode.OUTER,
            "back": EdgeMode.JOIN,
        },
    )
    assert bp.has_connectors
    assert bp.edge_modes["right"] == EdgeMode.JOIN
    assert bp.edge_modes["back"] == EdgeMode.JOIN

    # Should render without error
    r = bp.render()
    assert r is not None


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_baseplate_with_solid_fill():
    """Test baseplate with solid fill on edges."""
    bp = GridfinityBaseplate(
        2,
        2,
        solid_fill={
            "left": 0.0,
            "right": 5.5,
            "front": 0.0,
            "back": 3.2,
        },
    )
    assert bp.has_fill
    # Total dimensions should include fill
    assert _almost_same(bp.total_length, 2 * 42 + 5.5)
    assert _almost_same(bp.total_width, 2 * 42 + 3.2)

    # Should render without error
    r = bp.render()
    assert r is not None
    # Check size includes fill
    s = size_3d(r)
    assert _almost_same(s[0], 2 * 42 + 5.5, tol=0.5)
    assert _almost_same(s[1], 2 * 42 + 3.2, tol=0.5)


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_baseplate_with_notches():
    """Test baseplate with notch positions."""
    bp = GridfinityBaseplate(
        2,
        2,
        micro_divisions=4,
        edge_modes={
            "left": EdgeMode.OUTER,
            "right": EdgeMode.JOIN,
            "front": EdgeMode.OUTER,
            "back": EdgeMode.JOIN,
        },
        notch_positions={
            "left": [],
            "right": [2, 6],  # Positions in micro-cells
            "front": [],
            "back": [2, 6],
        },
    )
    assert bp.has_connectors

    # Should render without error
    r = bp.render()
    assert r is not None


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_baseplate_fractional_size():
    """Test baseplate with fractional size using micro_divisions."""
    # 1.5U x 1.25U with micro_divisions=4
    bp = GridfinityBaseplate(1.5, 1.25, micro_divisions=4)
    assert _almost_same(bp.length, 1.5 * 42)
    assert _almost_same(bp.width, 1.25 * 42)

    # Should render without error
    r = bp.render()
    assert r is not None


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_baseplate_combined_features():
    """Test baseplate with all new features combined."""
    bp = GridfinityBaseplate(
        2,
        2,
        micro_divisions=4,
        edge_modes={
            "left": EdgeMode.OUTER,
            "right": EdgeMode.JOIN,
            "front": EdgeMode.OUTER,
            "back": EdgeMode.JOIN,
        },
        solid_fill={
            "left": 0.0,
            "right": 0.0,
            "front": 0.0,
            "back": 5.0,
        },
        notch_positions={
            "left": [],
            "right": [2, 6],
            "front": [],
            "back": [2, 6],
        },
    )
    assert bp.has_connectors
    assert bp.has_fill

    # Should render without error
    r = bp.render()
    assert r is not None

    # Size should include fill
    s = size_3d(r)
    assert _almost_same(s[1], 2 * 42 + 5.0, tol=0.5)


# =============================================================================
# Notch Spec and Cutter Consistency Tests
# =============================================================================


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_notch_spec_matches_constants():
    """NotchSpec default values should match module constants."""
    from microfinity.parts.baseplate import (
        get_notch_spec,
        get_seam_cut_depth_mm,
        NOTCH_WIDTH_MM,
        NOTCH_HEIGHT_MM,
        NOTCH_CHAMFER_MM,
        NOTCH_KEEPOUT_TOP_MM,
        DEFAULT_FRAME_WIDTH_MM,
    )

    spec = get_notch_spec()
    assert spec.width == NOTCH_WIDTH_MM
    # Default depth is now full frame width (for through-slot cutting)
    expected_depth = get_seam_cut_depth_mm(DEFAULT_FRAME_WIDTH_MM)
    assert _almost_same(spec.depth, expected_depth, tol=0.001)
    assert spec.height == NOTCH_HEIGHT_MM
    assert spec.chamfer == NOTCH_CHAMFER_MM
    assert spec.keepout_top == NOTCH_KEEPOUT_TOP_MM


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_get_seam_wall_thickness_mm():
    """get_seam_wall_thickness_mm should return half of frame width (deprecated)."""
    from microfinity.parts.baseplate import get_seam_wall_thickness_mm, DEFAULT_FRAME_WIDTH_MM

    result = get_seam_wall_thickness_mm(DEFAULT_FRAME_WIDTH_MM)
    assert _almost_same(result, DEFAULT_FRAME_WIDTH_MM / 2, tol=0.001)

    # Test with custom frame width
    result2 = get_seam_wall_thickness_mm(4.0)
    assert _almost_same(result2, 2.0, tol=0.001)


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_get_seam_cut_depth_mm():
    """get_seam_cut_depth_mm should return full frame width for through-slots."""
    from microfinity.parts.baseplate import get_seam_cut_depth_mm, DEFAULT_FRAME_WIDTH_MM

    result = get_seam_cut_depth_mm(DEFAULT_FRAME_WIDTH_MM)
    assert _almost_same(result, DEFAULT_FRAME_WIDTH_MM, tol=0.001)

    # Test with custom frame width
    result2 = get_seam_cut_depth_mm(4.0)
    assert _almost_same(result2, 4.0, tol=0.001)


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_make_notch_cutter_outer_anchored_dimensions():
    """Outer-anchored notch cutter should have correct dimensions and position."""
    from microfinity.parts.baseplate import (
        make_notch_cutter_outer_anchored,
        get_notch_spec,
        NOTCH_THROUGH_OVERCUT_MM,
    )

    spec = get_notch_spec()
    cutter = make_notch_cutter_outer_anchored(spec=spec)
    bb = cutter.val().BoundingBox()

    expected_depth = spec.depth + NOTCH_THROUGH_OVERCUT_MM

    # Check dimensions (chamfer may reduce width/height slightly)
    assert _almost_same(bb.xlen, spec.width, tol=0.1)
    assert _almost_same(bb.ylen, expected_depth, tol=0.1)
    assert _almost_same(bb.zlen, spec.height, tol=0.1)

    # Check outer face at Y=0 (within tolerance)
    assert abs(bb.ymin) < 0.01, f"Outer face should be at Y=0, got ymin={bb.ymin}"


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_make_notch_cutter_unchanged():
    """Original make_notch_cutter should remain Y-centered (backward compatible)."""
    from microfinity.parts.baseplate import make_notch_cutter, get_notch_spec

    spec = get_notch_spec()
    cutter = make_notch_cutter(spec=spec)
    bb = cutter.val().BoundingBox()

    # Should be centered in Y (ymin approximately -depth/2)
    assert _almost_same(bb.ymin, -spec.depth / 2, tol=0.1)


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_make_notch_cutter_dimensions():
    """make_notch_cutter should produce correct bounding box."""
    from microfinity.parts.baseplate import get_notch_spec, make_notch_cutter

    spec = get_notch_spec()
    cutter = make_notch_cutter(spec)
    bb = cutter.val().BoundingBox()

    # Cutter should match spec dimensions (chamfer may reduce slightly)
    assert _almost_same(bb.xlen, spec.width, tol=0.1)
    assert _almost_same(bb.ylen, spec.depth, tol=0.1)
    assert _almost_same(bb.zlen, spec.height, tol=0.1)


@pytest.mark.skipif(
    SKIP_TEST_BASEPLATE,
    reason="Skipped intentionally by test scope environment variable",
)
def test_notch_cutter_consistency():
    """Production baseplate notches and make_notch_cutter should match.

    This ensures test prints use the same notch geometry as production.
    Note: Notch depth is now based on full frame width (through-slot),
    not the legacy NOTCH_DEPTH_MM value.
    """
    from microfinity.parts.baseplate import (
        GridfinityBaseplate,
        EdgeRole,
        get_notch_spec,
        make_notch_cutter,
        get_seam_cut_depth_mm,
    )

    # Get standalone notch cutter
    spec = get_notch_spec()
    standalone_cutter = make_notch_cutter(spec)
    standalone_bb = standalone_cutter.val().BoundingBox()

    # Create a baseplate with SEAM edge (has notches)
    bp = GridfinityBaseplate(
        length_u=2.0,
        width_u=2.0,
        micro_divisions=4,
        edge_roles={
            "left": EdgeRole.OUTER,
            "right": EdgeRole.SEAM,
            "front": EdgeRole.OUTER,
            "back": EdgeRole.OUTER,
        },
    )

    # The baseplate uses the same width/height spec
    assert bp.notch_width == spec.width
    assert bp.notch_height == spec.height
    assert bp.notch_chamfer == spec.chamfer

    # Notch depth is now full frame width (for through-slot cutting)
    seam_cut_depth = get_seam_cut_depth_mm(bp.frame_width_mm)
    assert _almost_same(spec.depth, seam_cut_depth, tol=0.01)

    # Verify dimensions match for width and height
    assert _almost_same(standalone_bb.xlen, bp.notch_width, tol=0.01)
    assert _almost_same(standalone_bb.ylen, spec.depth, tol=0.01)
    assert _almost_same(standalone_bb.zlen, bp.notch_height, tol=0.01)
