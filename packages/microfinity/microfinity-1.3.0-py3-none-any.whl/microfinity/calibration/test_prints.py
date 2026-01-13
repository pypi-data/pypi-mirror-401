#
# Gridfinity Test Print Generators
#
# This module provides generators for test prints used to validate:
# - Fractional pocket fits (0.25U, 0.5U, 0.75U)
# - Clip clearance tuning (via clearance sweep)
#

"""
Test Print Generators for Gridfinity Baseplates.

This module provides functions to generate small test prints for validating:

1. Fractional Pocket Fit Tests:
   - Small baseplate sections with fractional pockets (0.25U, 0.5U, 0.75U)
   - Plus reference full-U pocket for comparison
   - Includes female connector slots for testing clip fit
   - Verify that Gridfinity items fit properly in fractional pockets

2. Clip Clearance Sweep:
   - Multiple loose clips with varying clearances
   - Test which clearance fits best for your printer
   - Female slots are static (in fractional plates), male clips vary

Design Philosophy:
   - Female slots are STATIC: Always use production notch geometry
   - Male clips VARY: Clearance sweep only on clip dimensions
   - Single source of truth: NotchSpec from gf_baseplate.py

Usage:
    from microfinity.test_prints import (
        generate_fractional_pocket_test,
        generate_clip_clearance_sweep,
        export_test_prints,
    )

    # Generate all test prints to a directory
    export_test_prints("./test_prints/")

    # Or generate individual tests
    test_025 = generate_fractional_pocket_test(0.25, include_slots=True)
    clips, clearances = generate_clip_clearance_sweep()
"""

from typing import List, Dict, Tuple, Optional, Any
import cadquery as cq

# Default clearance values for the sweep (tight to loose)
# Extended range up to 0.6mm in 0.05mm increments for thorough fit testing
DEFAULT_CLEARANCE_SWEEP = [
    -0.10,
    -0.05,
    0.00,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
]


def _cut_female_slots_on_edge(
    body: cq.Workplane,
    *,
    length_u: float,
    width_u: float,
    slot_edge: str,
    total_height: float,
    micro_divisions: int = 4,
    clip_pitch_u: float = 1.0,
) -> cq.Workplane:
    """Cut female connector slots (through-slots) into an edge of the body.

    Uses the production make_notch_cutter_outer_anchored() and compute_notch_z_band()
    to ensure slots match production baseplates exactly (same Z placement in the
    straight 90-degree wall section, same through-slot depth).

    Args:
        body: The CadQuery geometry to cut slots into
        length_u: Length of the piece in U (X dimension)
        width_u: Width of the piece in U (Y dimension)
        slot_edge: Edge to cut slots on ("left", "right", "front", "back")
        total_height: Total height of the baseplate (from GridfinityBaseplate)
        micro_divisions: Micro-divisions per U (typically 4)
        clip_pitch_u: Spacing between clips in U (typically 1.0)

    Returns:
        Body with through-slots cut into the specified edge
    """
    from microfinity.core.constants import GRU
    from microfinity.parts.baseplate import (
        get_notch_spec,
        make_notch_cutter_outer_anchored,
        get_seam_cut_depth_mm,
        DEFAULT_FRAME_WIDTH_MM,
        NOTCH_THROUGH_OVERCUT_MM,
        compute_notch_z_band,
    )

    spec = get_notch_spec()

    # Grid region extents (centered at origin)
    half_x = (length_u * GRU) / 2.0
    half_y = (width_u * GRU) / 2.0

    # Notch Z placement using profile-derived position (same as production)
    notch_bottom_z = compute_notch_z_band(total_height, spec.height)[0]

    # Boolean cut depth: nominal depth + overcut for robust cutting (true window)
    cut_depth_per_side = get_seam_cut_depth_mm(DEFAULT_FRAME_WIDTH_MM)
    boolean_cut_depth = cut_depth_per_side + NOTCH_THROUGH_OVERCUT_MM

    # Micro-cell pitch in mm
    pitch_mm = GRU / micro_divisions
    pitch_micro = int(round(clip_pitch_u * micro_divisions))

    # Edge length in micro-cells
    if slot_edge in ("left", "right"):
        edge_len_u = width_u
    else:
        edge_len_u = length_u
    edge_len_micro = int(round(edge_len_u * micro_divisions))

    # Notch positions: centers of 1U cells (at micro positions 2, 6, 10, ...)
    # For M=4: center offset is M//2 = 2
    center_offset = micro_divisions // 2
    positions_micro = []
    pos = center_offset
    while pos < edge_len_micro:
        positions_micro.append(pos)
        pos += pitch_micro

    # Cut each notch using outer-anchored through-slot cutter
    for pm in positions_micro:
        pos_mm = pm * pitch_mm

        # Create outer-anchored cutter with boolean depth (true window)
        cutter = make_notch_cutter_outer_anchored(
            width=spec.width,
            depth=boolean_cut_depth,
            height=spec.height,
            chamfer=spec.chamfer,
            overcut=0.0,  # Overcut already included in boolean_cut_depth
        ).translate((0, 0, notch_bottom_z))

        # Position cutter based on edge
        # Cutter has outer face at Y=0, extends in +Y direction
        # We rotate and place so outer face aligns with piece boundary
        if slot_edge == "right":
            # Right edge at +X, notch extends inward (-X)
            x = half_x
            y = -half_y + pos_mm
            cutter = cutter.rotate((0, 0, 0), (0, 0, 1), 90)
        elif slot_edge == "left":
            # Left edge at -X, notch extends inward (+X)
            x = -half_x
            y = -half_y + pos_mm
            cutter = cutter.rotate((0, 0, 0), (0, 0, 1), -90)
        elif slot_edge == "back":
            # Back edge at +Y, notch extends inward (-Y)
            x = -half_x + pos_mm
            y = half_y
            cutter = cutter.rotate((0, 0, 0), (0, 0, 1), 180)
        elif slot_edge == "front":
            # Front edge at -Y, notch extends inward (+Y)
            x = -half_x + pos_mm
            y = -half_y
            # No rotation needed, +Y is already inward
        else:
            raise ValueError(f"Invalid slot_edge: {slot_edge}")

        cutter = cutter.translate((x, y, 0))
        body = body.cut(cutter)

    return body


def generate_fractional_pocket_test(
    fractional_u: float = 0.25,
    reference_size_u: float = 1.0,
    micro_divisions: int = 4,
    include_slots: bool = True,
    slot_edge: str = "right",
):
    """Generate a test piece with a fractional pocket column plus reference pocket.

    Creates a minimal baseplate section with:
    - One column of fractional pockets (0.25U, 0.5U, or 0.75U wide)
    - One reference column of full-U pocket for comparison
    - Optional female connector slots on a full-U-aligned edge

    The slots use production notch geometry (via make_notch_cutter) to ensure
    test results are representative of actual baseplate fit.

    Args:
        fractional_u: The fractional size to test (0.25, 0.5, or 0.75)
        reference_size_u: Size of the reference pocket area (default 1.0U)
        micro_divisions: Grid subdivision (must be 4 for fractional support)
        include_slots: If True, add female connector slots on the specified edge
        slot_edge: Edge for female slots ("right" recommended, must be full-U aligned)

    Returns:
        CadQuery Workplane with the test piece
    """
    from microfinity.parts.baseplate import GridfinityBaseplate, EdgeRole

    # Validate fractional size
    valid_fractions = [0.25, 0.5, 0.75]
    if fractional_u not in valid_fractions:
        raise ValueError(f"fractional_u must be one of {valid_fractions}, got {fractional_u}")

    if micro_divisions != 4:
        raise ValueError("micro_divisions must be 4 for fractional pocket tests")

    if slot_edge not in ("left", "right", "front", "back"):
        raise ValueError(f"slot_edge must be left/right/front/back, got {slot_edge}")

    # Create a minimal piece: fractional + 1 full U reference
    # E.g., 0.25U test = 1.25U x 1.0U
    total_width_u = fractional_u + reference_size_u
    height_u = reference_size_u

    # All edges are OUTER - we cut slots manually
    bp = GridfinityBaseplate(
        length_u=total_width_u,
        width_u=height_u,
        micro_divisions=micro_divisions,
        edge_roles={
            "left": EdgeRole.OUTER,
            "right": EdgeRole.OUTER,
            "front": EdgeRole.OUTER,
            "back": EdgeRole.OUTER,
        },
    )

    body = bp.render()

    # Cut female slots if requested
    if include_slots:
        body = _cut_female_slots_on_edge(
            body,
            length_u=total_width_u,
            width_u=height_u,
            slot_edge=slot_edge,
            total_height=bp.total_height,  # Use actual baseplate height
            micro_divisions=micro_divisions,
            clip_pitch_u=1.0,
        )

    return body


def generate_fractional_pocket_test_set(
    reference_size_u: float = 1.0,
    micro_divisions: int = 4,
    include_slots: bool = True,
    slot_edge: str = "right",
) -> Dict[str, Any]:
    """Generate a complete set of fractional pocket test pieces.

    Creates test pieces for 0.25U, 0.5U, and 0.75U fractional pockets,
    each with optional female connector slots for testing clip fit.

    Args:
        reference_size_u: Size of reference pocket area
        micro_divisions: Grid subdivision (must be 4)
        include_slots: If True, add female slots to each test piece
        slot_edge: Edge for female slots ("right" recommended)

    Returns:
        Dict mapping fraction name to geometry (e.g., {"0.25U": geom, ...})
    """
    results = {}
    for frac in [0.25, 0.5, 0.75]:
        name = f"{frac}U"
        results[name] = generate_fractional_pocket_test(
            fractional_u=frac,
            reference_size_u=reference_size_u,
            micro_divisions=micro_divisions,
            include_slots=include_slots,
            slot_edge=slot_edge,
        )
    return results


def generate_clip_clearance_sweep(
    clearances: Optional[List[float]] = None,
    clip_spacing_mm: float = 4.0,
) -> Tuple[cq.Workplane, List[float]]:
    """Generate a set of loose clips with varying clearances for fit testing.

    Creates multiple SEPARATE clips arranged in a row, each with a different
    clearance value. Clips are NOT fused - they are separate solids in the
    same workplane so they can be individually picked and tested.

    Design:
    - Clips sized from NotchSpec (production female slot dimensions)
    - Clearance applied to clip width and height (positive = smaller clip = looser fit)
    - Clips ordered from tight (negative clearance) to loose (positive clearance)
    - Clips are separate bodies (not unioned) so they export as distinct parts

    Args:
        clearances: List of clearance values in mm (default: [-0.10 to +0.20])
        clip_spacing_mm: Gap between clips (default 4.0mm for safe separation)

    Returns:
        Tuple of (workplane with multiple solids, list of clearance values)
    """
    from microfinity.parts.baseplate_layout import GridfinityConnectionClip

    if clearances is None:
        clearances = DEFAULT_CLEARANCE_SWEEP.copy()

    if not clearances:
        raise ValueError("clearances list cannot be empty")

    # Build clips as separate solids using .add() instead of .union()
    wp = cq.Workplane("XY")
    x = 0.0

    for clearance in clearances:
        clip = GridfinityConnectionClip(clip_clearance_mm=clearance)
        w, l, h = clip.dims

        clip_geom = clip.render_flat()
        # Translate clip so its left edge is at current x
        clip_geom = clip_geom.translate((x + w / 2.0, 0, 0))

        # Add as separate solid (not union!)
        wp = wp.add(clip_geom)

        x += w + clip_spacing_mm

    return wp, clearances


def generate_clip_test_set(
    num_clips: int = 1,
    clearance_mm: float = 0.0,
) -> cq.Workplane:
    """Generate clips for testing (simple version).

    Args:
        num_clips: Number of clips to generate
        clearance_mm: Clearance to apply to all clips

    Returns:
        CadQuery Workplane with the clips arranged for printing
    """
    from microfinity.parts.baseplate_layout import GridfinityConnectionClip

    clip = GridfinityConnectionClip(clip_clearance_mm=clearance_mm)
    w, l, h = clip.dims

    if num_clips == 1:
        return clip.render_flat()

    # Arrange multiple clips in a row using .add() (not union)
    wp = cq.Workplane("XY")
    spacing = w + 4.0  # 4mm gap

    for i in range(num_clips):
        clip_geom = clip.render_flat().translate((i * spacing, 0, 0))
        wp = wp.add(clip_geom)

    return wp


def export_test_prints(
    path: str,
    file_format: str = "step",
    include_fractional: bool = True,
    include_clip_sweep: bool = True,
) -> List[str]:
    """Export all test prints to a directory.

    Exports:
    - Fractional pocket test pieces (with female slots for clip testing)
    - Clip clearance sweep (multiple loose clips with varying clearances)
    - Clearance values text file

    Args:
        path: Directory path to export files to
        file_format: File format ("step" or "stl")
        include_fractional: Include fractional pocket tests with female slots
        include_clip_sweep: Include clip clearance sweep

    Returns:
        List of exported file paths
    """
    import os
    from microfinity.core.export import GridfinityExporter

    os.makedirs(path, exist_ok=True)
    exported_files = []
    ext = ".step" if file_format.lower() == "step" else ".stl"

    # Export fractional pocket tests (with female slots)
    if include_fractional:
        fraction_tests = generate_fractional_pocket_test_set(include_slots=True)
        for name, geom in fraction_tests.items():
            filename = f"test_fractional_{name.replace('.', '_')}{ext}"
            filepath = os.path.join(path, filename)
            if file_format.lower() == "step":
                exported_files.append(GridfinityExporter.to_step(geom, filepath))
            else:
                exported_files.append(GridfinityExporter.to_stl(geom, filepath))

    # Export clip clearance sweep
    if include_clip_sweep:
        clips, clearances = generate_clip_clearance_sweep()
        filename = f"test_clips_clearance_sweep{ext}"
        filepath = os.path.join(path, filename)
        if file_format.lower() == "step":
            exported_files.append(GridfinityExporter.to_step(clips, filepath))
        else:
            exported_files.append(GridfinityExporter.to_stl(clips, filepath))

        # Write clearance values to a text file
        clearance_file = os.path.join(path, "clip_clearance_values.txt")
        _write_clearance_reference(clearance_file, clearances)
        exported_files.append(clearance_file)

    return exported_files


def _write_clearance_reference(filepath: str, clearances: List[float]) -> None:
    """Write clearance values reference file.

    Args:
        filepath: Path to output text file
        clearances: List of clearance values
    """
    with open(filepath, "w") as f:
        f.write("Clip Clearance Sweep Values\n")
        f.write("=" * 40 + "\n\n")
        f.write("Clips are SEPARATE loose pieces, arranged\n")
        f.write("in order from tight (left) to loose (right).\n\n")
        f.write("Test each clip in the female slots on the fractional\n")
        f.write("test plates to find your ideal clearance.\n\n")
        f.write("Clip order (X- to X+, left to right):\n\n")
        for i, clearance in enumerate(clearances):
            sign = "+" if clearance >= 0 else ""
            label = ""
            if i == 0:
                label = " (tightest)"
            elif i == len(clearances) - 1:
                label = " (loosest)"
            elif abs(clearance) < 0.001:
                label = " (nominal)"
            f.write(f"  Clip {i + 1}: {sign}{clearance:.2f}mm{label}\n")
        f.write("\n")
        f.write("HOW TO USE:\n")
        f.write("  1. Print the fractional test plates (with female slots)\n")
        f.write("  2. Print the clip clearance sweep\n")
        f.write("  3. Pick up each clip and test in the slots\n")
        f.write("  4. Find the clip with the best snap-fit\n")
        f.write("  5. Use that clearance value in GridfinityConnectionClip()\n")
