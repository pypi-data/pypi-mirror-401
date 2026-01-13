"""Tests for meshcutter.core.cq_cutter module.

Tests the CadQuery-based cutter generation for Gridfinity micro-feet.
"""

import pytest
import trimesh

from meshcutter.core.cq_cutter import (
    generate_1u_foot_cq,
    generate_micro_foot_cq,
    generate_cell_cutter_cq,
    generate_grid_cutter_mesh,
    generate_grid_cutter_meshes,
    cq_to_trimesh,
    micro_foot_offsets,
    get_cell_cutter_volume,
    get_1u_foot_volume,
    get_micro_foot_volume,
)


class TestFootGeneration:
    """Tests for foot solid generation."""

    def test_1u_foot_dimensions(self):
        """1U foot should have correct dimensions."""
        foot = generate_1u_foot_cq(cropped=False)
        bb = foot.val().BoundingBox()

        # Uncropped foot is 42mm
        assert abs(bb.xlen - 42.0) < 0.1
        assert abs(bb.ylen - 42.0) < 0.1

    def test_1u_foot_cropped_dimensions(self):
        """Cropped 1U foot should be 41.5mm (42 - 0.5 tolerance)."""
        foot = generate_1u_foot_cq(cropped=True)
        bb = foot.val().BoundingBox()

        assert abs(bb.xlen - 41.5) < 0.1
        assert abs(bb.ylen - 41.5) < 0.1

    def test_micro_foot_dimensions(self):
        """Micro foot for div=4 should be 10mm."""
        foot = generate_micro_foot_cq(micro_divisions=4)
        bb = foot.val().BoundingBox()

        # micro_pitch = 42/4 = 10.5, foot_size = 10.5 - 0.5 = 10.0
        assert abs(bb.xlen - 10.0) < 0.1
        assert abs(bb.ylen - 10.0) < 0.1

    def test_micro_foot_with_reduction(self):
        """Micro foot with size_reduction should be smaller."""
        foot_normal = generate_micro_foot_cq(micro_divisions=4, size_reduction=0.0)
        foot_reduced = generate_micro_foot_cq(micro_divisions=4, size_reduction=0.5)

        bb_normal = foot_normal.val().BoundingBox()
        bb_reduced = foot_reduced.val().BoundingBox()

        assert bb_normal.xlen - bb_reduced.xlen > 0.4  # Should be ~0.5 smaller


class TestMicroFootOffsets:
    """Tests for micro foot offset calculations."""

    def test_div1_offsets(self):
        """div=1 should return single offset at origin."""
        offsets = micro_foot_offsets(1)
        assert offsets == [(0.0, 0.0)]

    def test_div2_offsets(self):
        """div=2 should return 4 offsets."""
        offsets = micro_foot_offsets(2)
        assert len(offsets) == 4

        # Offsets should be at +/- 10.5mm
        xs = sorted(set(o[0] for o in offsets))
        assert len(xs) == 2
        assert abs(xs[0] - (-10.5)) < 0.01
        assert abs(xs[1] - 10.5) < 0.01

    def test_div4_offsets(self):
        """div=4 should return 16 offsets."""
        offsets = micro_foot_offsets(4)
        assert len(offsets) == 16

        # Offsets should be at -15.75, -5.25, 5.25, 15.75
        xs = sorted(set(o[0] for o in offsets))
        assert len(xs) == 4
        expected_xs = [-15.75, -5.25, 5.25, 15.75]
        for x, expected in zip(xs, expected_xs):
            assert abs(x - expected) < 0.01


class TestCellCutter:
    """Tests for cell cutter generation."""

    def test_cell_cutter_volume(self):
        """Cell cutter volume should be F1 - 16*Fm approximately."""
        # Clear cache to ensure fresh generation
        generate_cell_cutter_cq.cache_clear()

        f1_vol = get_1u_foot_volume()
        fm_vol = get_micro_foot_volume(4)
        cutter_vol = get_cell_cutter_volume(4)

        # Cutter = F1 - 16*Fm (approximately, feet overlap at tips)
        expected_approx = f1_vol - 16 * fm_vol

        # The actual cutter should be close but not exact due to overlap
        # Expect within 10% of the naive calculation
        assert cutter_vol > expected_approx * 0.8
        assert cutter_vol < f1_vol  # Must be less than full foot

    def test_cell_cutter_watertight(self):
        """Cell cutter mesh should be watertight."""
        generate_cell_cutter_cq.cache_clear()

        cutter = generate_cell_cutter_cq(micro_divisions=4, epsilon=0.02)
        mesh = cq_to_trimesh(cutter)

        # CadQuery-generated meshes should be watertight
        assert mesh.is_watertight

    def test_cell_cutter_div2(self):
        """Cell cutter for div=2 should work."""
        generate_cell_cutter_cq.cache_clear()

        cutter = generate_cell_cutter_cq(micro_divisions=2, epsilon=0.02)
        mesh = cq_to_trimesh(cutter)

        assert mesh.is_watertight
        # div=2 cutter should be smaller (fewer, larger micro-feet)
        vol_div2 = get_cell_cutter_volume(2)
        vol_div4 = get_cell_cutter_volume(4)
        assert vol_div2 < vol_div4


class TestGridCutter:
    """Tests for grid cutter generation."""

    def test_single_cell_grid(self):
        """Single cell grid should produce one mesh."""
        centers = [(0.0, 0.0)]
        meshes = generate_grid_cutter_meshes(centers, micro_divisions=4, add_channels=False)

        assert len(meshes) == 1
        assert meshes[0].is_watertight

    def test_multi_cell_grid_no_channels(self):
        """Multi-cell grid without channels should produce N meshes."""
        centers = [(-21.0, 0.0), (21.0, 0.0)]  # 2x1 grid
        meshes = generate_grid_cutter_meshes(centers, micro_divisions=4, add_channels=False)

        assert len(meshes) == 2  # One per cell, no channel

    def test_multi_cell_grid_with_channels(self):
        """Multi-cell grid with channels should include channel mesh."""
        centers = [(-21.0, 0.0), (21.0, 0.0)]  # 2x1 grid
        meshes = generate_grid_cutter_meshes(centers, micro_divisions=4, add_channels=True)

        assert len(meshes) == 3  # Two cells + one channel mesh

    def test_grid_cutter_mesh_concatenation(self):
        """generate_grid_cutter_mesh should concatenate all cells."""
        centers = [(-21.0, 0.0), (21.0, 0.0)]
        mesh = generate_grid_cutter_mesh(centers, micro_divisions=4, add_channels=False)

        # Should be a single mesh
        assert isinstance(mesh, trimesh.Trimesh)

        # Volume should be approximately 2x single cell
        single_vol = get_cell_cutter_volume(4)
        assert mesh.volume > single_vol * 1.8
        assert mesh.volume < single_vol * 2.2


class TestCutterPlacement:
    """Tests for cutter placement and Z-orientation."""

    def test_flip_z_orientation(self):
        """With flip_z=True, cutter should extend from z=-epsilon upward."""
        centers = [(0.0, 0.0)]
        meshes = generate_grid_cutter_meshes(centers, micro_divisions=4, epsilon=0.02, flip_z=True)

        mesh = meshes[0]
        z_min = mesh.vertices[:, 2].min()
        z_max = mesh.vertices[:, 2].max()

        # Should start at -epsilon
        assert abs(z_min - (-0.02)) < 0.01
        # Should extend upward ~5mm
        assert z_max > 4.5
        assert z_max < 5.5

    def test_no_flip_z(self):
        """With flip_z=False, cutter is in CadQuery's native orientation."""
        centers = [(0.0, 0.0)]
        meshes = generate_grid_cutter_meshes(centers, micro_divisions=4, epsilon=0.02, flip_z=False)

        mesh = meshes[0]
        z_min = mesh.vertices[:, 2].min()
        z_max = mesh.vertices[:, 2].max()

        # In CQ orientation, foot tip is at positive Z
        # (after mirror in generate_*_foot_cq)
        # The exact values depend on CQ internals
        assert z_max > z_min


class TestOvershotAndWallCut:
    """Tests for overshoot and wall_cut parameters."""

    def test_overshoot_increases_volume(self):
        """Overshoot should increase cutter volume."""
        generate_cell_cutter_cq.cache_clear()

        cutter_plain = generate_cell_cutter_cq(4, 0.02, overshoot=0.0, wall_cut=0.0)
        cutter_overshoot = generate_cell_cutter_cq(4, 0.02, overshoot=1.0, wall_cut=0.0)

        vol_plain = cutter_plain.val().Volume()
        vol_overshoot = cutter_overshoot.val().Volume()

        assert vol_overshoot > vol_plain

    def test_wall_cut_increases_volume(self):
        """Wall cut should increase cutter volume (smaller micro-feet)."""
        generate_cell_cutter_cq.cache_clear()

        cutter_plain = generate_cell_cutter_cq(4, 0.02, overshoot=0.0, wall_cut=0.0)
        cutter_wall = generate_cell_cutter_cq(4, 0.02, overshoot=0.0, wall_cut=0.5)

        vol_plain = cutter_plain.val().Volume()
        vol_wall = cutter_wall.val().Volume()

        assert vol_wall > vol_plain


class TestMicroFootMatchesMicrofinity:
    """Tests that meshcutter micro-feet match microfinity's output exactly."""

    def test_micro_foot_matches_microfinity(self):
        """Meshcutter micro_foot should match microfinity box.micro_foot()."""
        from microfinity.parts.box import GridfinityBox

        # Generate feet from both sources
        box = GridfinityBox(1, 1, 1, micro_divisions=4)
        mf_foot = box.micro_foot()
        mc_foot = generate_micro_foot_cq(micro_divisions=4)

        # Convert to trimesh for comparison
        mf_mesh = cq_to_trimesh(mf_foot)
        mc_mesh = cq_to_trimesh(mc_foot)

        # Bounds should match
        assert abs(mf_mesh.bounds[0][0] - mc_mesh.bounds[0][0]) < 0.01
        assert abs(mf_mesh.bounds[1][0] - mc_mesh.bounds[1][0]) < 0.01

        # Volume should match
        assert abs(mf_mesh.volume - mc_mesh.volume) < 0.1

    def test_micro_foot_width_at_straight_section(self):
        """Micro-foot should be 5.2mm wide at straight section (Z=-4.0 in CQ)."""
        foot = generate_micro_foot_cq(micro_divisions=4)
        mesh = cq_to_trimesh(foot)

        # Find vertices at Z≈-4.0 (straight section in CQ coordinates)
        z_target = -4.0
        tol = 0.15
        verts = mesh.vertices[abs(mesh.vertices[:, 2] - z_target) < tol]

        assert len(verts) > 0, "No vertices found at straight section"
        width = verts[:, 0].max() - verts[:, 0].min()

        # Should be 5.2mm (10.0mm foot at straight section with chamfer profile)
        assert abs(width - 5.2) < 0.1, f"Width {width} != 5.2mm"

    def test_micro_foot_top_width(self):
        """Micro-foot should be 10.0mm wide at top (foot_size = micro_pitch - GR_TOL)."""
        foot = generate_micro_foot_cq(micro_divisions=4)
        bb = foot.val().BoundingBox()

        # Top width should be 10.0mm
        assert abs(bb.xlen - 10.0) < 0.1
        assert abs(bb.ylen - 10.0) < 0.1
