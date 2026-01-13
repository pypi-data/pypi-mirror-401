#! /usr/bin/env python3
#
# meshcutter.cli.meshcut - CLI entry point for microfinity-meshcut
#
# Converts standard 1U Gridfinity feet into micro-divided feet.
#
# Two approaches are available:
# 1. Replace-base (default): Replaces entire foot region with fresh micro-feet.
#    Produces EXACT geometric match with natively-generated micro boxes.
# 2. Boolean subtraction (legacy): Carves micro-feet pattern into existing feet.
#    Preserves features below z=5mm but has small geometric residuals (~50mm³).

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from meshcutter import __version__
from meshcutter.core.constants import (
    GR_BASE_HEIGHT,
    COPLANAR_EPSILON,
    MIN_COMPONENT_FACES,
    MIN_SLIVER_SIZE,
    MIN_SLIVER_VOLUME,
    GRU,
)
from meshcutter.core.detection import detect_aligned_frame
from meshcutter.core.foot_cutter import generate_microgrid_cutter, convert_to_micro_feet
from meshcutter.core.boolean import (
    boolean_difference,
    validate_boolean_inputs,
    check_manifold3d_available,
    check_pymeshlab_available,
    BooleanError,
)
from meshcutter.io.loader import load_mesh, validate_mesh, LoaderError
from meshcutter.io.exporter import export_stl, get_export_info, ExporterError


def _repair_mesh_manifold(mesh):
    """Repair mesh by passing through manifold3d.

    This eliminates floating-point artifacts and non-manifold geometry
    that can occur during boolean operations or STL export/import.

    Args:
        mesh: trimesh.Trimesh to repair

    Returns:
        Repaired trimesh.Trimesh (or original if manifold3d unavailable)
    """
    try:
        import numpy as np
        import manifold3d

        # Convert to manifold (auto-repairs)
        m = manifold3d.Manifold(
            manifold3d.Mesh(
                vert_properties=np.array(mesh.vertices, dtype=np.float32),
                tri_verts=np.array(mesh.faces, dtype=np.uint32),
            )
        )

        # Convert back to trimesh
        import trimesh

        mesh_data = m.to_mesh()
        return trimesh.Trimesh(vertices=mesh_data.vert_properties[:, :3], faces=mesh_data.tri_verts)
    except ImportError:
        return mesh  # manifold3d not available


def _is_degenerate_sliver(component, min_size=MIN_SLIVER_SIZE, min_volume=MIN_SLIVER_VOLUME):
    """Check if a component is a degenerate sliver (boolean artifact).

    A sliver is identified by:
    - All bounding box dimensions being very small (< min_size), OR
    - Having an extremely small volume (< min_volume), OR
    - Having fewer than 4 faces (can't form a valid solid)

    Args:
        component: trimesh.Trimesh component to check
        min_size: Minimum acceptable size in any dimension (mm)
        min_volume: Minimum acceptable volume (mm³)

    Returns:
        True if the component is a degenerate sliver that should be removed
    """
    import numpy as np

    # Check face count - need at least 4 faces for a tetrahedron
    if len(component.faces) < 4:
        return True

    # Check if all dimensions are tiny (nanometer-scale artifact)
    size = component.bounds[1] - component.bounds[0]
    if (size < min_size).all():
        return True

    # Check volume - if it's effectively zero, it's degenerate
    # Use absolute value since non-watertight meshes can have negative volume
    if abs(component.volume) < min_volume:
        return True

    return False


def _clean_mesh_components(mesh):
    """Remove floating/degenerate components from mesh.

    Keeps only the largest component(s) that have significant geometry.
    Small floating triangles and nanometer-scale slivers (common boolean
    artifacts) are removed.

    Args:
        mesh: trimesh.Trimesh input mesh

    Returns:
        Tuple of (cleaned mesh, number of components removed)
    """
    import trimesh

    components = mesh.split(only_watertight=False)

    if len(components) <= 1:
        return mesh, 0

    # Find the main component (largest by face count)
    main_component = max(components, key=lambda c: len(c.faces))
    main_face_count = len(main_component.faces)

    # Keep components that:
    # 1. Have at least MIN_COMPONENT_FACES faces OR 1% of main component, AND
    # 2. Are NOT degenerate slivers (size/volume check)
    threshold = max(MIN_COMPONENT_FACES, main_face_count * 0.01)
    kept = [c for c in components if len(c.faces) >= threshold and not _is_degenerate_sliver(c)]
    removed_count = len(components) - len(kept)

    if len(kept) == 1:
        return kept[0], removed_count
    elif len(kept) > 1:
        # Concatenate kept components
        return trimesh.util.concatenate(kept), removed_count
    else:
        # Shouldn't happen, but return original if no components kept
        return mesh, 0


def main():
    """Main entry point for microfinity-meshcut CLI."""
    parser = argparse.ArgumentParser(
        prog="microfinity-meshcut",
        description=(
            "Convert standard 1U Gridfinity feet into micro-divided feet.\n\n"
            "This tool enables existing Gridfinity models to work with\n"
            "micro-divided baseplates (quarter-grid or half-grid).\n\n"
            "By default, uses the 'replace-base' approach which produces\n"
            "geometry identical to natively-generated micro boxes."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with quarter-grid divisions (default, recommended)
  microfinity-meshcut input.stl -o output.stl

  # Half-grid divisions (21mm pitch)
  microfinity-meshcut input.stl -o output.stl --micro-divisions 2

  # Legacy boolean subtraction (preserves magnet holes but has residuals)
  microfinity-meshcut input.stl -o output.stl --use-boolean --add-channels

  # No-op mode (useful for testing pipeline)
  microfinity-meshcut input.stl -o output.stl --micro-divisions 1

  # 3MF input
  microfinity-meshcut model.3mf -o output.stl

Approaches:
  Replace-base (default):
    - Replaces entire foot region (z < 5mm) with fresh micro-feet
    - Produces EXACT match with natively-generated micro boxes
    - WARNING: Removes magnet holes, screw holes, and base text
    
  Boolean subtraction (--use-boolean):
    - Carves micro-feet pattern into existing feet
    - Preserves features below z=5mm (holes, text)
    - Has small geometric residuals (~50mm³) at corners
""",
    )

    # Positional arguments
    parser.add_argument(
        "input",
        type=Path,
        help="Input STL or 3MF file (must have standard 1U Gridfinity feet)",
    )

    # Required arguments
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output STL file",
    )

    # Micro-division options
    parser.add_argument(
        "-d",
        "--micro-divisions",
        type=int,
        default=4,
        choices=[1, 2, 4],
        help=("Micro-divisions per grid unit: " "4=quarter-grid (10.5mm), 2=half (21mm), 1=no-op. " "Default: 4"),
    )

    parser.add_argument(
        "--depth",
        type=float,
        default=GR_BASE_HEIGHT,
        help=f"Cut depth in mm. Default: {GR_BASE_HEIGHT} (GR_BASE_HEIGHT)",
    )

    parser.add_argument(
        "--epsilon",
        type=float,
        default=COPLANAR_EPSILON,
        help=f"Coplanar avoidance offset in mm. Default: {COPLANAR_EPSILON}",
    )

    parser.add_argument(
        "--overshoot",
        type=float,
        default=0.0,
        help="Extend cutter beyond foot boundary to cut outer walls (mm). "
        "Set to 0.0 to keep cutter within foot boundary. Default: 0.0",
    )

    parser.add_argument(
        "--auto-overshoot",
        action="store_true",
        help="Automatically apply 0.35mm overshoot for multi-cell grids (2+ cells). "
        "This helps cut outer shell walls that intersect the foot region. "
        "Overrides --overshoot when applicable.",
    )

    parser.add_argument(
        "--wall-cut",
        type=float,
        default=0.0,
        help="Shrink micro-feet in cutter to cut outer walls (mm). "
        "Creates overlap between cutter and model edge. Default: 0.0",
    )

    parser.add_argument(
        "--add-channels",
        action="store_true",
        help="Add inter-cell channel cutters to cut material between adjacent cells. "
        "Only needed for solid-walled 1U boxes. (Only used with --use-boolean)",
    )

    # Approach selection
    parser.add_argument(
        "--use-boolean",
        action="store_true",
        help="Use legacy boolean subtraction instead of replace-base approach. "
        "Boolean subtraction preserves features below z=5mm (magnet holes, screw holes, text) "
        "but has small geometric residuals (~50mm³) at corners. "
        "Default: replace-base (exact geometry but removes base features).",
    )

    # Detection options
    parser.add_argument(
        "--force-z-up",
        action="store_true",
        help="Assume model is already Z-aligned (faster, more stable)",
    )

    parser.add_argument(
        "--z-tolerance",
        type=float,
        default=0.1,
        help="Tolerance for bottom face detection in mm. Default: 0.1",
    )

    # Boolean options
    parser.add_argument(
        "--repair",
        action="store_true",
        help="Attempt mesh repair before boolean operation",
    )

    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Disable automatic cleanup of floating/degenerate triangles in input mesh",
    )

    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip cutter geometry validation (not recommended). "
        "Validation detects internal faces that cause boolean artifacts.",
    )

    # Output options
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output with detailed progress",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    # Run the main processing
    try:
        run_meshcut(args)
    except KeyboardInterrupt:
        print("\nAborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def run_meshcut(args: argparse.Namespace) -> None:
    """Run the mesh cutting operation."""
    start_time = time.time()

    micro_pitch = GRU / args.micro_divisions
    micro_foot_size = micro_pitch - 0.5  # GR_TOL = 0.5

    # Determine which approach to use
    use_replace_base = not args.use_boolean

    if args.verbose:
        print(f"microfinity-meshcut v{__version__}")
        print(f"Input: {args.input}")
        print(f"Output: {args.output}")
        print(f"Micro-divisions: {args.micro_divisions}")
        print(f"  Micro-pitch: {micro_pitch:.1f}mm")
        print(f"  Micro-foot size: {micro_foot_size:.1f}mm")
        print(f"  Feet per 1U cell: {args.micro_divisions ** 2}")
        if use_replace_base:
            print("  Method: replace-base (exact geometry)")
        else:
            print("  Method: boolean subtraction (preserves base features)")
        print()

        # Check available engines
        engines = []
        if check_manifold3d_available():
            engines.append("manifold3d")
        if check_pymeshlab_available():
            engines.append("pymeshlab")
        if engines:
            print(f"Available boolean engines: {', '.join(engines)}")
        else:
            print("Warning: No optimized boolean engines found. Install manifold3d:")
            print("  pip install manifold3d")
        print()

    # Handle no-op case (micro_divisions=1)
    if args.micro_divisions == 1:
        if args.verbose:
            print("micro-divisions=1: no changes will be made (pass-through mode)")
            print()

        # Load and immediately export (useful for testing pipeline)
        try:
            mesh = load_mesh(args.input)
        except LoaderError as e:
            raise RuntimeError(f"Failed to load mesh: {e}")

        try:
            export_stl(mesh, args.output)
        except ExporterError as e:
            raise RuntimeError(f"Failed to export: {e}")

        elapsed = time.time() - start_time
        if args.verbose:
            print(f"Completed in {elapsed:.2f}s (no changes)")
        else:
            print(f"Wrote {args.output} (unchanged)")
        return

    # Step 1: Load mesh
    if args.verbose:
        print("Loading mesh...", end=" ", flush=True)

    try:
        mesh = load_mesh(args.input)
    except LoaderError as e:
        raise RuntimeError(f"Failed to load mesh: {e}")

    # Clean up floating/degenerate components if enabled (default)
    if not args.no_clean:
        mesh, cleaned_count = _clean_mesh_components(mesh)
        if args.verbose and cleaned_count > 0:
            print(f"(removed {cleaned_count} floating components) ", end="")

    if args.verbose:
        info = validate_mesh(mesh)
        print("done")
        print(f"  Triangles: {info['face_count']}")
        print(f"  Vertices: {info['vertex_count']}")
        print(
            f"  Dimensions: {info['dimensions'][0]:.1f} x {info['dimensions'][1]:.1f} x {info['dimensions'][2]:.1f} mm"
        )
        print(f"  Watertight: {info['is_watertight']}")
        if not info["is_watertight"]:
            print("  Warning: Mesh is not watertight. Consider using --repair")
        print()

    # =========================================================================
    # REPLACE-BASE APPROACH (default, recommended)
    # =========================================================================
    if use_replace_base:
        if args.verbose:
            print("Converting to micro-feet using replace-base approach...")
            print("  NOTE: This replaces everything below z=5mm (magnet holes, etc. will be lost)")
            print()

        try:
            result_mesh = convert_to_micro_feet(
                mesh,
                micro_divisions=args.micro_divisions,
                pitch=GRU,
                use_replace_base=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to convert to micro-feet: {e}")

        if result_mesh is None:
            raise RuntimeError("Conversion returned None")

        # Clean up floating/degenerate components from result
        if not args.no_clean:
            result_mesh, cleaned_count = _clean_mesh_components(result_mesh)
            if args.verbose and cleaned_count > 0:
                print(f"Cleaned up {cleaned_count} floating components from result")
                print()

    # =========================================================================
    # LEGACY BOOLEAN SUBTRACTION APPROACH
    # =========================================================================
    else:
        # Step 2: Detect bottom frame and extract footprint
        if args.verbose:
            mode = "force Z-up" if args.force_z_up else "auto-detect"
            print(f"Detecting bottom plane and footprint ({mode})...", end=" ", flush=True)

        try:
            frame, footprint = detect_aligned_frame(
                mesh,
                force_z_up=args.force_z_up,
                z_tolerance=args.z_tolerance,
                edge_voting=True,
            )
        except ValueError as e:
            raise RuntimeError(f"Failed to detect bottom plane: {e}")

        if args.verbose:
            import math

            yaw_deg = math.degrees(math.atan2(frame.x_axis[1], frame.x_axis[0]))
            print("done")
            print(f"  Z-min: {frame.z_min:.3f}mm")
            print(f"  Origin: ({frame.origin[0]:.2f}, {frame.origin[1]:.2f}, {frame.origin[2]:.2f})")
            print(f"  Frame yaw: {yaw_deg:.2f} degrees")
            bounds = footprint.bounds
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            print(f"  Footprint: {width:.1f} x {height:.1f} mm")

            # Infer cell count
            from meshcutter.core.foot_cutter import detect_cell_centers

            centers = detect_cell_centers(footprint, GRU)
            cells_x = int(round((width + 0.5) / GRU))
            cells_y = int(round((height + 0.5) / GRU))
            print(f"  Detected grid: {cells_x} x {cells_y} = {len(centers)} cells")
            print()

        # Determine effective overshoot
        # Auto-overshoot applies 0.35mm for multi-cell grids to cut outer shell walls
        effective_overshoot = args.overshoot
        if args.auto_overshoot:
            # Compute cell count from mesh bounds
            bounds = footprint.bounds
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            cells_x = int(round((width + 0.5) / GRU))
            cells_y = int(round((height + 0.5) / GRU))
            num_cells = cells_x * cells_y

            if num_cells >= 2:
                effective_overshoot = 0.35
                if args.verbose:
                    print(f"Auto-overshoot enabled: using {effective_overshoot}mm for {num_cells}-cell grid")
                    print()

        # Step 3: Generate micro-grid cutter
        if args.verbose:
            print(
                f"Generating micro-foot cutter ({args.micro_divisions}x{args.micro_divisions} per cell)...",
                end=" ",
                flush=True,
            )

        try:
            cutter = generate_microgrid_cutter(
                footprint=footprint,
                frame=frame,
                micro_divisions=args.micro_divisions,
                pitch=GRU,
                epsilon=args.epsilon,
                mesh_bounds=mesh.bounds,  # Use mesh bounds for accurate cell detection
                overshoot=effective_overshoot,
                wall_cut=args.wall_cut,
                add_channels=args.add_channels,
            )
        except ValueError as e:
            raise RuntimeError(f"Failed to generate cutter: {e}")

        if cutter is None:
            raise RuntimeError("Cutter generation returned None")

        if args.verbose:
            print("done")
            print(f"  Cutter triangles: {len(cutter.faces)}")
            print(f"  Cutter watertight: {cutter.is_watertight}")
            cutter_bounds = cutter.bounds
            print(
                f"  Cutter bounds: [{cutter_bounds[0, 0]:.1f}, {cutter_bounds[0, 1]:.1f}] "
                f"to [{cutter_bounds[1, 0]:.1f}, {cutter_bounds[1, 1]:.1f}]"
            )
            print()

        # Validate cutter geometry (detect internal faces / stacked sheets)
        if not args.no_validate:
            from meshcutter.core.validation import validate_cutter_geometry, CutterValidationError

            if args.verbose:
                print("Validating cutter geometry...", end=" ", flush=True)

            try:
                validation = validate_cutter_geometry(cutter, name="cutter", epsilon=args.epsilon, raise_on_error=True)
                if args.verbose:
                    print("OK")
                    if validation["warnings"]:
                        for w in validation["warnings"]:
                            print(f"  Note: {w}")
                    print()
            except CutterValidationError as e:
                raise RuntimeError(str(e))

        # Step 4: Validate inputs and check bounds intersection
        if args.verbose:
            print("Validating boolean inputs...", end=" ", flush=True)

        part_bounds = mesh.bounds
        cutter_bounds = cutter.bounds

        # Check if cutter intersects part bounds
        bounds_intersect = not (
            part_bounds[1, 0] < cutter_bounds[0, 0]
            or part_bounds[0, 0] > cutter_bounds[1, 0]
            or part_bounds[1, 1] < cutter_bounds[0, 1]
            or part_bounds[0, 1] > cutter_bounds[1, 1]
            or part_bounds[1, 2] < cutter_bounds[0, 2]
            or part_bounds[0, 2] > cutter_bounds[1, 2]
        )

        if not bounds_intersect:
            import math

            yaw_angle = math.degrees(math.atan2(frame.x_axis[1], frame.x_axis[0]))
            raise RuntimeError(
                f"Cutter does not intersect part bounds.\n"
                f"  Part bounds:   {part_bounds.tolist()}\n"
                f"  Cutter bounds: {cutter_bounds.tolist()}\n"
                f"  Frame yaw:     {yaw_angle:.2f} degrees\n"
                f"  This may indicate a detection or alignment issue."
            )

        warnings = validate_boolean_inputs(mesh, cutter)
        if args.verbose:
            if warnings:
                print()
                for w in warnings:
                    print(f"  Warning: {w}")
            else:
                print("OK")
            print()

        # Step 5: Boolean difference
        if args.verbose:
            repair_msg = " (with repair)" if args.repair else ""
            print(f"Performing boolean difference{repair_msg}...", end=" ", flush=True)

        try:
            result = boolean_difference(
                part=mesh,
                cutter=cutter,
                repair=args.repair,
            )
        except BooleanError as e:
            raise RuntimeError(str(e))

        if args.verbose:
            print("done")
            print(f"  Engine used: {result.engine_used}")
            print(f"  Repair applied: {result.repair_applied}")
            if result.warnings:
                for w in result.warnings:
                    print(f"  Note: {w}")
            print()

        # Clean up floating/degenerate components from result
        if not args.no_clean:
            result_mesh, cleaned_count = _clean_mesh_components(result.mesh)
            if args.verbose and cleaned_count > 0:
                print(f"Cleaned up {cleaned_count} floating components from result")

            # Final manifold repair to eliminate any remaining artifacts
            result_mesh = _repair_mesh_manifold(result_mesh)
            if args.verbose:
                print()
        else:
            result_mesh = result.mesh

    # Step 6: Export result
    if args.verbose:
        print(f"Exporting to {args.output}...", end=" ", flush=True)

    try:
        export_stl(result_mesh, args.output)
    except ExporterError as e:
        raise RuntimeError(f"Failed to export: {e}")

    if args.verbose:
        export_info = get_export_info(result_mesh)
        print("done")
        print(f"  Output triangles: {export_info['face_count']}")
        print(f"  Output watertight: {export_info['is_watertight']}")
        dims = export_info["dimensions"]
        print(f"  Output dimensions: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")
        print()

    elapsed = time.time() - start_time

    if args.verbose:
        print(f"Completed in {elapsed:.2f}s")
    else:
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
