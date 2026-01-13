#! /usr/bin/env python3
#
# meshcutter.core.validation - Placement validation and sanity checks
#
# Provides utilities to verify cutter placement against input mesh,
# catching common issues like misaligned grids or insufficient coverage.
#

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import trimesh

from microfinity.core.constants import GR_BASE_CLR, GR_BASE_HEIGHT, GR_TOL, GRU


def validate_cutter_placement(
    input_mesh: trimesh.Trimesh,
    cutter_mesh: trimesh.Trimesh,
    cell_centers: List[Tuple[float, float]],
    expected_cells: Optional[int] = None,
    margin: float = 5.0,
) -> Dict:
    """Validate cutter placement against input mesh.

    Checks:
    1. Cell count matches expected (if provided)
    2. Cutter XY bounds overlap input mesh with sufficient margin
    3. Cutter Z range covers the foot region

    Args:
        input_mesh: Original input mesh
        cutter_mesh: Generated cutter mesh
        cell_centers: List of detected (x, y) cell centers
        expected_cells: Expected number of cells (optional)
        margin: Minimum XY overlap margin in mm (default 5.0)

    Returns:
        Dict with validation results:
        - cell_count: Number of detected cells
        - expected_cells: Expected count (if provided)
        - cells_match: Whether counts match
        - xy_overlap: (overlap_x, overlap_y) in mm
        - xy_margin_ok: Whether margin is sufficient
        - z_covers_foot: Whether Z range covers foot region
        - input_bounds: Input mesh bounds
        - cutter_bounds: Cutter mesh bounds
        - issues: List of issue descriptions
    """
    input_bounds = input_mesh.bounds  # [[minx,miny,minz], [maxx,maxy,maxz]]
    cutter_bounds = cutter_mesh.bounds

    # XY overlap calculation
    xy_overlap_x = min(input_bounds[1, 0], cutter_bounds[1, 0]) - max(input_bounds[0, 0], cutter_bounds[0, 0])
    xy_overlap_y = min(input_bounds[1, 1], cutter_bounds[1, 1]) - max(input_bounds[0, 1], cutter_bounds[0, 1])

    # Z coverage check (foot region is z=0 to ~5mm)
    foot_z_min = 0.0
    foot_z_max = GR_BASE_HEIGHT + GR_BASE_CLR  # ~5.0mm
    z_covers_foot = (cutter_bounds[0, 2] <= foot_z_min) and (cutter_bounds[1, 2] >= foot_z_max)

    # Cell count check
    cells_match = True
    if expected_cells is not None:
        cells_match = len(cell_centers) == expected_cells

    # XY margin check
    xy_margin_ok = xy_overlap_x >= margin and xy_overlap_y >= margin

    # Collect issues
    issues = []
    if not cells_match:
        issues.append(f"Cell count mismatch: detected {len(cell_centers)}, expected {expected_cells}")
    if not xy_margin_ok:
        issues.append(f"Insufficient XY overlap: {xy_overlap_x:.2f}mm x {xy_overlap_y:.2f}mm (need >= {margin}mm)")
    if not z_covers_foot:
        issues.append(
            f"Cutter Z range [{cutter_bounds[0, 2]:.2f}, {cutter_bounds[1, 2]:.2f}] "
            f"doesn't cover foot region [0, {foot_z_max:.2f}]"
        )

    result = {
        "cell_count": len(cell_centers),
        "expected_cells": expected_cells,
        "cells_match": cells_match,
        "xy_overlap": (xy_overlap_x, xy_overlap_y),
        "xy_margin_ok": xy_margin_ok,
        "z_covers_foot": z_covers_foot,
        "input_bounds": input_bounds.tolist(),
        "cutter_bounds": cutter_bounds.tolist(),
        "issues": issues,
        "valid": len(issues) == 0,
    }

    return result


def print_placement_report(validation: Dict, verbose: bool = True) -> None:
    """Print human-readable placement validation report.

    Args:
        validation: Dict from validate_cutter_placement()
        verbose: If True, print full details; if False, only issues
    """
    print("=== Cutter Placement Validation ===")

    if verbose:
        print(f"Cells detected: {validation['cell_count']}", end="")
        if validation["expected_cells"] is not None:
            print(f" (expected: {validation['expected_cells']})")
        else:
            print()

        print(f"XY overlap: {validation['xy_overlap'][0]:.2f}mm x {validation['xy_overlap'][1]:.2f}mm")
        print(f"Z covers foot region: {validation['z_covers_foot']}")

        print(
            f"Input bounds: X[{validation['input_bounds'][0][0]:.2f}, {validation['input_bounds'][1][0]:.2f}] "
            f"Y[{validation['input_bounds'][0][1]:.2f}, {validation['input_bounds'][1][1]:.2f}] "
            f"Z[{validation['input_bounds'][0][2]:.2f}, {validation['input_bounds'][1][2]:.2f}]"
        )
        print(
            f"Cutter bounds: X[{validation['cutter_bounds'][0][0]:.2f}, {validation['cutter_bounds'][1][0]:.2f}] "
            f"Y[{validation['cutter_bounds'][0][1]:.2f}, {validation['cutter_bounds'][1][1]:.2f}] "
            f"Z[{validation['cutter_bounds'][0][2]:.2f}, {validation['cutter_bounds'][1][2]:.2f}]"
        )

    if validation["valid"]:
        print("Status: VALID")
    else:
        print("Status: ISSUES DETECTED")
        for issue in validation["issues"]:
            print(f"  WARNING: {issue}")


def estimate_expected_cells(mesh_bounds: np.ndarray, pitch: float = GRU) -> int:
    """Estimate expected number of 1U cells from mesh bounds.

    Uses Gridfinity convention: overall_dim ~ N * pitch - GR_TOL
    So: N = round((dim + GR_TOL) / pitch)

    Args:
        mesh_bounds: Mesh bounds [[minx,miny,minz], [maxx,maxy,maxz]]
        pitch: 1U pitch (default 42mm)

    Returns:
        Expected number of cells (cells_x * cells_y)
    """
    width = mesh_bounds[1, 0] - mesh_bounds[0, 0]
    height = mesh_bounds[1, 1] - mesh_bounds[0, 1]

    cells_x = max(1, int(round((width + GR_TOL) / pitch)))
    cells_y = max(1, int(round((height + GR_TOL) / pitch)))

    return cells_x * cells_y


def validate_mesh_quality(mesh: trimesh.Trimesh) -> Dict:
    """Validate mesh quality for boolean operations.

    Checks:
    1. Watertightness
    2. Consistent winding
    3. No degenerate faces
    4. Positive volume

    Args:
        mesh: Trimesh to validate

    Returns:
        Dict with quality metrics and issues
    """
    issues = []

    is_watertight = mesh.is_watertight
    is_winding_consistent = mesh.is_winding_consistent

    # Check for degenerate faces
    degen_mask = mesh.nondegenerate_faces(height=1e-8)
    degen_count = len(degen_mask) - np.sum(degen_mask)

    volume = mesh.volume
    has_positive_volume = volume > 0

    if not is_watertight:
        issues.append("Mesh is not watertight")
    if not is_winding_consistent:
        issues.append("Mesh winding is inconsistent")
    if degen_count > 0:
        issues.append(f"Mesh has {degen_count} degenerate faces")
    if not has_positive_volume:
        issues.append(f"Mesh has non-positive volume: {volume:.2f}")

    result = {
        "is_watertight": is_watertight,
        "is_winding_consistent": is_winding_consistent,
        "degenerate_faces": int(degen_count),
        "volume": volume,
        "face_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "issues": issues,
        "valid": len(issues) == 0,
    }

    return result


class CutterValidationError(Exception):
    """Raised when cutter validation fails with critical errors."""

    pass


def has_stacked_sheets_near_top(
    mesh: trimesh.Trimesh,
    n_samples: int = 100,
    epsilon: float = 0.02,
    band_multiplier: float = 3.0,
) -> Tuple[bool, str]:
    """Detect stacked sheets near the top plane (symptom of internal faces).

    Casts rays downward from above the mesh and checks for multiple hits
    clustered near the top plane. A valid solid should have clean enter/exit
    pairs, not multiple surfaces at nearly the same Z level.

    The specific failure this detects: internal coincident faces created by
    box-fuse operations, which triangulate into "stacked Z sheets" like
    Z hits at [4.98, 5.00, 5.02] instead of just [5.00].

    Args:
        mesh: Trimesh to check
        n_samples: Number of random XY sample points
        epsilon: Epsilon value used in cutter generation
        band_multiplier: Multiplier for epsilon to define "near top" band

    Returns:
        Tuple of (has_stacked_sheets, details_string)
    """
    bounds = mesh.bounds
    top_z = bounds[1, 2]
    band = epsilon * band_multiplier  # Detection band around top plane

    # Sample random XY points within bounds (with margin to avoid edges)
    margin = 1.0
    x_min, x_max = bounds[0, 0] + margin, bounds[1, 0] - margin
    y_min, y_max = bounds[0, 1] + margin, bounds[1, 1] - margin

    if x_max <= x_min or y_max <= y_min:
        return False, "mesh too small to sample"

    rng = np.random.default_rng(42)  # Deterministic for reproducibility
    xs = rng.uniform(x_min, x_max, n_samples)
    ys = rng.uniform(y_min, y_max, n_samples)

    stacked_count = 0
    example_hits = None

    for x, y in zip(xs, ys):
        # Cast ray downward from above
        origins = np.array([[x, y, top_z + 10]])
        directions = np.array([[0, 0, -1]])
        locs, _, _ = mesh.ray.intersects_location(origins, directions)

        if len(locs) < 2:
            continue

        z_hits = locs[:, 2]

        # Count hits near top_z (within band)
        near_top_mask = np.abs(z_hits - top_z) < band
        near_top_hits = z_hits[near_top_mask]

        # Check for 3+ total hits with at least 2 distinct near top
        # (normal solid: 2 hits for enter/exit; stacked: 3+ with clustering)
        if len(z_hits) >= 3 and len(near_top_hits) >= 2:
            unique_near = np.unique(np.round(near_top_hits, 3))
            if len(unique_near) >= 2:
                stacked_count += 1
                if example_hits is None:
                    example_hits = sorted([round(z, 3) for z in z_hits])

    if stacked_count > 0:
        details = f"{stacked_count}/{n_samples} rays found stacked sheets"
        if example_hits:
            details += f"; example Z hits: {example_hits}"
        return True, details

    return False, ""


def validate_cutter_geometry(
    mesh: trimesh.Trimesh,
    name: str = "cutter",
    epsilon: float = 0.02,
    raise_on_error: bool = True,
) -> Dict:
    """Validate cutter mesh geometry for boolean operations.

    Performs comprehensive validation including:
    1. Watertightness (critical)
    2. Stacked sheet detection (critical - catches internal faces)
    3. Winding consistency
    4. Single component check

    Args:
        mesh: Trimesh to validate
        name: Name for error messages
        epsilon: Epsilon value used for coplanar avoidance
        raise_on_error: If True, raise CutterValidationError on critical failure

    Returns:
        Dict with validation results

    Raises:
        CutterValidationError: If raise_on_error=True and critical validation fails
    """
    errors = []
    warnings = []

    # Check watertight (critical)
    is_watertight = mesh.is_watertight
    if not is_watertight:
        errors.append(f"{name} is not watertight")

    # Check winding consistency (warning)
    if not mesh.is_winding_consistent:
        warnings.append(f"{name} has inconsistent winding")

    # Check for stacked sheets near top (critical)
    stacked, stacked_details = has_stacked_sheets_near_top(mesh, epsilon=epsilon)
    if stacked:
        errors.append(f"{name} has stacked sheets (internal faces): {stacked_details}")

    # Check single component (warning if multiple)
    try:
        components = mesh.split(only_watertight=False)
        if len(components) > 1:
            warnings.append(f"{name} has {len(components)} components (expected 1)")
    except Exception:
        pass

    result = {
        "is_watertight": is_watertight,
        "has_stacked_sheets": stacked,
        "stacked_details": stacked_details,
        "errors": errors,
        "warnings": warnings,
        "valid": len(errors) == 0,
    }

    if raise_on_error and errors:
        raise CutterValidationError("Cutter validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    return result


def quick_z_hit_check(
    mesh: trimesh.Trimesh,
    sample_points: Optional[List[Tuple[float, float]]] = None,
) -> Dict:
    """Quick diagnostic check of Z-hit patterns at specific points.

    This is a targeted check that can be used to verify the specific
    failure mode of stacked sheets. Returns a dict with hit information
    at each sample point.

    Args:
        mesh: Trimesh to check
        sample_points: List of (x, y) points to sample. If None, uses
                       default grid based on mesh bounds.

    Returns:
        Dict mapping (x, y) tuple to list of Z hits
    """
    bounds = mesh.bounds
    top_z = bounds[1, 2]

    if sample_points is None:
        # Default: sample at center and midpoints
        margin = 2.0
        cx = (bounds[0, 0] + bounds[1, 0]) / 2
        cy = (bounds[0, 1] + bounds[1, 1]) / 2
        x_lo = bounds[0, 0] + margin
        x_hi = bounds[1, 0] - margin
        y_lo = bounds[0, 1] + margin
        y_hi = bounds[1, 1] - margin

        sample_points = [
            (cx, cy),  # Center
            (x_lo, cy),  # Left
            (x_hi, cy),  # Right
            (cx, y_lo),  # Bottom
            (cx, y_hi),  # Top
        ]

    results = {}
    for x, y in sample_points:
        origins = np.array([[x, y, top_z + 10]])
        directions = np.array([[0, 0, -1]])
        locs, _, _ = mesh.ray.intersects_location(origins, directions)

        z_hits = sorted([round(z, 4) for z in locs[:, 2]]) if len(locs) > 0 else []
        results[(round(x, 2), round(y, 2))] = z_hits

    return results


def print_mesh_quality_report(quality: Dict, name: str = "Mesh") -> None:
    """Print mesh quality report.

    Args:
        quality: Dict from validate_mesh_quality()
        name: Name to use in report header
    """
    print(f"=== {name} Quality ===")
    print(f"Vertices: {quality['vertex_count']}, Faces: {quality['face_count']}")
    print(f"Volume: {quality['volume']:.2f} mm³")
    print(f"Watertight: {quality['is_watertight']}")
    print(f"Consistent winding: {quality['is_winding_consistent']}")

    if quality["degenerate_faces"] > 0:
        print(f"Degenerate faces: {quality['degenerate_faces']}")

    if quality["valid"]:
        print("Status: VALID")
    else:
        print("Status: ISSUES DETECTED")
        for issue in quality["issues"]:
            print(f"  WARNING: {issue}")
