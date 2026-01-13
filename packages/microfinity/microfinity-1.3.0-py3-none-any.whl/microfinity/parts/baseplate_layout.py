#! /usr/bin/env python3
#
# Copyright (C) 2023  Michael Gale
# This file is part of the cq-gridfinity python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Gridfinity Baseplate Layout System
#
# This module provides tools for calculating optimal baseplate layouts
# to fill drawers, with support for:
# - Fractional sizes (micro-divisions: 0.25U, 0.5U, 1U increments)
# - Connectable baseplates with clip notches
# - Integrated solid fill for sub-micro-unit gaps
# - Build plate constraints
# - "Flooring logic" to avoid tiny end pieces

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import warnings
import cadquery as cq

from microfinity.core.constants import GRU
from microfinity.core.export import GridfinityExporter
from microfinity.parts.baseplate import (
    EdgeMode,
    EdgeRole,
    EdgeFrameMode,
    FillInnerMode,
    NotchSpec,
    get_notch_spec,
)
from microfinity.core.helpers import union_all


# =============================================================================
# Enums (local aliases for convenience, main definitions in gf_baseplate)
# =============================================================================

# EdgeMode, EdgeRole, EdgeFrameMode, FillInnerMode are imported from gf_baseplate


class SegmentationMode(Enum):
    """Segmentation strategy for partitioning grid."""

    EVEN = "even"  # Distribute evenly (minimize tiny pieces)
    MAX_THEN_REMAINDER = "max_then_remainder"  # Use max size, remainder in last
    ALIGNED = "aligned"  # Internal seams on full-U boundaries, fractional on perimeter


class ToleranceMode(Enum):
    """How tolerance is applied to drawer dimensions."""

    CENTERED = "centered"  # Split evenly on all sides
    CORNER = "corner"  # Push grid to origin corner


# =============================================================================
# Dataclasses
# =============================================================================


@dataclass(frozen=True)
class PieceSpec:
    """Specification for a single baseplate piece.

    All grid dimensions are in integer micro-cells to prevent float drift.
    Fill dimensions are in mm (always < one micro-pitch).
    """

    # Unique identifier
    id: str

    # Grid-bearing area in micro-cells (integer)
    size_mx: int
    size_my: int

    # Integrated solid fill on outer edges (mm, always < micro_pitch)
    # Legacy: only +X/+Y (deprecated - use fill_left/right/front/back)
    fill_x_mm: float = 0.0
    fill_y_mm: float = 0.0

    # Per-edge fill amounts (mm) - preferred over fill_x_mm/fill_y_mm
    fill_left: float = 0.0
    fill_right: float = 0.0
    fill_front: float = 0.0
    fill_back: float = 0.0

    # Legacy edge modes: which edges are JOIN vs OUTER (deprecated)
    edge_left: EdgeMode = EdgeMode.OUTER
    edge_right: EdgeMode = EdgeMode.OUTER
    edge_front: EdgeMode = EdgeMode.OUTER
    edge_back: EdgeMode = EdgeMode.OUTER

    # New edge system: roles (what the edge touches)
    edge_role_left: EdgeRole = EdgeRole.OUTER
    edge_role_right: EdgeRole = EdgeRole.OUTER
    edge_role_front: EdgeRole = EdgeRole.OUTER
    edge_role_back: EdgeRole = EdgeRole.OUTER

    # New edge system: frame modes (how the edge is rendered)
    edge_frame_left: EdgeFrameMode = EdgeFrameMode.FULL_FRAME
    edge_frame_right: EdgeFrameMode = EdgeFrameMode.FULL_FRAME
    edge_frame_front: EdgeFrameMode = EdgeFrameMode.FULL_FRAME
    edge_frame_back: EdgeFrameMode = EdgeFrameMode.FULL_FRAME

    # Fill inner modes (for half-profile on grid→fill boundary)
    fill_inner_mode_x: FillInnerMode = FillInnerMode.NONE
    fill_inner_mode_y: FillInnerMode = FillInnerMode.NONE

    # Notch positions along each SEAM edge (in micro-cells from piece origin)
    # These are local coordinates relative to this piece
    notches_left: Tuple[int, ...] = field(default_factory=tuple)
    notches_right: Tuple[int, ...] = field(default_factory=tuple)
    notches_front: Tuple[int, ...] = field(default_factory=tuple)
    notches_back: Tuple[int, ...] = field(default_factory=tuple)

    # Position in drawer (mm) for preview/assembly
    origin_x_mm: float = 0.0
    origin_y_mm: float = 0.0

    # Grid indices in the layout
    grid_x: int = 0
    grid_y: int = 0

    # Cumulative micro-cell offsets (for global seam coordinate mapping)
    cumulative_mx: int = 0
    cumulative_my: int = 0

    @property
    def edge_modes(self) -> Dict[str, EdgeMode]:
        """Return legacy edge modes as a dictionary (deprecated)."""
        return {
            "left": self.edge_left,
            "right": self.edge_right,
            "front": self.edge_front,
            "back": self.edge_back,
        }

    @property
    def edge_roles(self) -> Dict[str, EdgeRole]:
        """Return edge roles as a dictionary."""
        return {
            "left": self.edge_role_left,
            "right": self.edge_role_right,
            "front": self.edge_role_front,
            "back": self.edge_role_back,
        }

    @property
    def edge_frame_modes(self) -> Dict[str, EdgeFrameMode]:
        """Return edge frame modes as a dictionary."""
        return {
            "left": self.edge_frame_left,
            "right": self.edge_frame_right,
            "front": self.edge_frame_front,
            "back": self.edge_frame_back,
        }

    @property
    def solid_fill(self) -> Dict[str, float]:
        """Return solid fill amounts as a dictionary for GridfinityBaseplate."""
        return {
            "left": self.fill_left,
            "right": self.fill_right,
            "front": self.fill_front,
            "back": self.fill_back,
        }

    @property
    def signature(self) -> tuple:
        """Signature for deduplication - pieces with same signature are identical geometry."""
        return (
            self.size_mx,
            self.size_my,
            round(self.fill_left, 3),
            round(self.fill_right, 3),
            round(self.fill_front, 3),
            round(self.fill_back, 3),
            self.edge_role_left,
            self.edge_role_right,
            self.edge_role_front,
            self.edge_role_back,
            self.edge_frame_left,
            self.edge_frame_right,
            self.edge_frame_front,
            self.edge_frame_back,
            self.fill_inner_mode_x,
            self.fill_inner_mode_y,
            self.notches_left,
            self.notches_right,
            self.notches_front,
            self.notches_back,
        )

    def size_u(self, micro_divisions: int) -> Tuple[float, float]:
        """Return size in U (grid units)."""
        return (
            self.size_mx / micro_divisions,
            self.size_my / micro_divisions,
        )

    def size_mm(self, micro_divisions: int) -> Tuple[float, float]:
        """Return grid-bearing size in mm (excluding fill)."""
        pitch = GRU / micro_divisions
        return (
            self.size_mx * pitch,
            self.size_my * pitch,
        )

    def total_size_mm(self, micro_divisions: int) -> Tuple[float, float]:
        """Return total size in mm (including fill)."""
        grid_x, grid_y = self.size_mm(micro_divisions)
        return (
            grid_x + self.fill_x_mm,
            grid_y + self.fill_y_mm,
        )


@dataclass
class LayoutResult:
    """Complete layout calculation results."""

    # Input parameters (echoed)
    drawer_x_mm: float
    drawer_y_mm: float
    build_plate_x_mm: float
    build_plate_y_mm: float
    micro_divisions: int
    tolerance_mm: float
    tolerance_mode: ToleranceMode

    # Computed grid info
    total_micro_x: int  # Total micro-cells in X
    total_micro_y: int  # Total micro-cells in Y
    fill_x_mm: float  # Remainder fill in X (< micro_pitch) - total both sides
    fill_y_mm: float  # Remainder fill in Y (< micro_pitch) - total both sides

    # Segmentation info
    segments_x: List[int]  # Micro-cell counts for each segment in X
    segments_y: List[int]  # Micro-cell counts for each segment in Y
    cumulative_x: List[int]  # Cumulative micro offsets in X
    cumulative_y: List[int]  # Cumulative micro offsets in Y

    # Pieces
    pieces: List[PieceSpec]

    # Clip info
    clip_pitch_u: float
    clip_count: int
    seam_stations: Dict[str, List[int]]  # Global seam station positions

    # Per-side fill amounts (split fill)
    fill_x_left: float
    fill_x_right: float
    fill_y_front: float
    fill_y_back: float

    @property
    def micro_pitch_mm(self) -> float:
        """Micro-pitch in mm."""
        return GRU / self.micro_divisions

    @property
    def total_u(self) -> Tuple[float, float]:
        """Total grid size in U."""
        return (
            self.total_micro_x / self.micro_divisions,
            self.total_micro_y / self.micro_divisions,
        )

    @property
    def num_pieces(self) -> int:
        """Total number of pieces."""
        return len(self.pieces)

    @property
    def grid_size(self) -> Tuple[int, int]:
        """Grid dimensions (number of pieces in X, Y)."""
        return (len(self.segments_x), len(self.segments_y))

    def unique_pieces(self) -> Dict[tuple, Tuple[PieceSpec, int]]:
        """Group pieces by signature for deduplication.

        Returns dict mapping signature -> (example PieceSpec, count)
        """
        result: Dict[tuple, Tuple[PieceSpec, int]] = {}
        for piece in self.pieces:
            sig = piece.signature
            if sig in result:
                _, count = result[sig]
                result[sig] = (result[sig][0], count + 1)
            else:
                result[sig] = (piece, 1)
        return result

    def summary(self) -> str:
        """Human-readable summary of the layout."""
        lines = [
            "=" * 60,
            "GRIDFINITY BASEPLATE LAYOUT",
            "=" * 60,
            "",
            "INPUT:",
            f"  Drawer:      {self.drawer_x_mm:.1f}mm x {self.drawer_y_mm:.1f}mm",
            f"  Build plate: {self.build_plate_x_mm:.1f}mm x {self.build_plate_y_mm:.1f}mm",
            f"  Micro-div:   {self.micro_divisions} ({self.micro_pitch_mm:.2f}mm = {1/self.micro_divisions:.2f}U)",
            f"  Tolerance:   {self.tolerance_mm:.1f}mm ({self.tolerance_mode.value})",
            "",
            "GRID:",
            f"  Total grid:  {self.total_micro_x}mx x {self.total_micro_y}my",
            f"               ({self.total_u[0]:.2f}U x {self.total_u[1]:.2f}U)",
            f"  Fill:        X={self.fill_x_mm:.2f}mm, Y={self.fill_y_mm:.2f}mm",
            "",
            "SEGMENTATION:",
            f"  X segments:  {self.segments_x} (micro-cells)",
            f"  Y segments:  {self.segments_y} (micro-cells)",
            f"  Grid:        {self.grid_size[0]} x {self.grid_size[1]} pieces",
            "",
            "PIECES:",
            f"  Total:       {self.num_pieces}",
        ]

        unique = self.unique_pieces()
        lines.append(f"  Unique:      {len(unique)}")
        lines.append("")
        lines.append("  Unique piece types:")
        lines.append("    Legend: O=outer S=seam F=fill_outer .=none")
        for sig, (piece, count) in unique.items():
            size_u = piece.size_u(self.micro_divisions)
            fill_str = ""
            if piece.fill_x_mm > 0 or piece.fill_y_mm > 0:
                fill_str = f" +fill({piece.fill_x_mm:.1f}, {piece.fill_y_mm:.1f})mm"

            # Show edge roles with single-char codes
            def role_char(role: EdgeRole) -> str:
                if role == EdgeRole.OUTER:
                    return "O"
                elif role == EdgeRole.SEAM:
                    return "S"
                elif role == EdgeRole.FILL_OUTER:
                    return "F"
                return "."

            edge_str = "".join(
                [
                    f"L:{role_char(piece.edge_role_left)}",
                    f" R:{role_char(piece.edge_role_right)}",
                    f" F:{role_char(piece.edge_role_front)}",
                    f" B:{role_char(piece.edge_role_back)}",
                ]
            )
            lines.append(f"    {size_u[0]:.2f}U x {size_u[1]:.2f}U [{edge_str}]{fill_str} x{count}")

        lines.append("")
        lines.append("CONNECTORS:")
        lines.append(f"  Clip pitch:  {self.clip_pitch_u:.2f}U")
        lines.append(f"  Clips needed: {self.clip_count}")
        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


# =============================================================================
# Layout Algorithm Helpers
# =============================================================================


def _build_balanced_internals(total: int, n: int, min_seg: int, max_seg: int, M: int) -> Optional[List[int]]:
    """Build n segments that sum to total, each in [min_seg, max_seg] and multiple of M.

    Args:
        total: Total microcells to distribute
        n: Number of segments
        min_seg: Minimum segment size (must be multiple of M)
        max_seg: Maximum segment size (must be multiple of M)
        M: Microcells per U (alignment unit)

    Returns:
        List of segment sizes, or None if not possible
    """
    if n <= 0:
        return [] if total == 0 else None

    if total < n * min_seg or total > n * max_seg:
        return None

    # Start with base size (multiple of M)
    base = (total // n // M) * M
    if base < min_seg:
        base = min_seg
    if base > max_seg:
        base = max_seg

    segments = [base] * n
    shortfall = total - sum(segments)

    # Distribute shortfall by adding M to segments (front to back)
    i = 0
    iterations = 0
    max_iterations = n * (max_seg - min_seg) // M + 10
    while shortfall > 0 and iterations < max_iterations:
        if segments[i] + M <= max_seg:
            segments[i] += M
            shortfall -= M
        i = (i + 1) % n
        iterations += 1

    # Distribute excess by subtracting M (if needed)
    iterations = 0
    while shortfall < 0 and iterations < max_iterations:
        if segments[i] - M >= min_seg:
            segments[i] -= M
            shortfall += M
        i = (i + 1) % n
        iterations += 1

    if sum(segments) != total:
        return None
    if any(s < min_seg or s > max_seg for s in segments):
        return None

    return segments


def _partition_micro_aligned(
    total_micro: int,
    max_micro: int,
    min_segment_micro: int,
    M: int,
) -> List[int]:
    """Partition with internal seams on full-U boundaries.

    Fractional remainder is pushed to the last segment (+ side / perimeter).
    All internal pieces are multiples of M microcells.

    Args:
        total_micro: Total micro-cells to partition
        max_micro: Maximum micro-cells per segment (build plate limit)
        min_segment_micro: Minimum acceptable segment size
        M: Microcells per U (alignment unit, typically 4)

    Returns:
        List of segment sizes in micro-cells

    Raises:
        ValueError: If no valid aligned partition exists
    """
    if total_micro <= 0:
        return []

    if total_micro <= max_micro:
        return [total_micro]  # Single piece, no seams

    # Compute aligned bounds
    max_aligned = (max_micro // M) * M  # Largest full-U that fits
    min_aligned = ((min_segment_micro + M - 1) // M) * M  # Round up to multiple of M

    if max_aligned < min_aligned:
        # Can't fit even one aligned piece - fall back to unaligned
        raise ValueError(f"Cannot align seams: max_aligned={max_aligned} < min_aligned={min_aligned}")

    # Search k from minimum upward
    k_min = math.ceil(total_micro / max_aligned)
    k_max = math.ceil(total_micro / min_segment_micro) + 1

    best_segments = None
    best_score = (float("inf"), float("inf"), float("inf"))  # (k, -rem, variance)

    for k in range(k_min, min(k_max + 1, k_min + 10)):  # Cap search
        n_internal = k - 1

        if n_internal == 0:
            # Single piece case
            if total_micro <= max_micro and total_micro >= min_segment_micro:
                return [total_micro]
            continue

        # Search remainders: prefer LARGEST valid remainder (iterate high to low)
        for rem in range(min(max_micro, total_micro), min_segment_micro - 1, -1):
            internal_total = total_micro - rem

            if internal_total % M != 0:
                continue  # Internal sum must be divisible by M

            # Check feasibility of internal split
            if internal_total < n_internal * min_aligned:
                continue
            if internal_total > n_internal * max_aligned:
                continue

            # Build balanced internal segments
            internals = _build_balanced_internals(internal_total, n_internal, min_aligned, max_aligned, M)
            if internals is None:
                continue

            # Score: prefer fewer pieces, larger remainder, lower variance
            variance = max(internals) - min(internals) if internals else 0
            score = (k, -rem, variance)

            if score < best_score:
                best_score = score
                best_segments = internals + [rem]

    if best_segments:
        return best_segments

    raise ValueError(
        f"Cannot align seams for total={total_micro}, max={max_micro}, "
        f"min={min_segment_micro}, M={M}. Try adjusting constraints."
    )


def partition_micro(
    total_micro: int,
    max_micro: int,
    min_segment_micro: int,
    mode: SegmentationMode = SegmentationMode.EVEN,
    M: int = 4,
) -> List[int]:
    """Partition a total micro-cell count into segments that fit build plate.

    Uses "flooring logic" to avoid tiny end pieces.

    Args:
        total_micro: Total micro-cells to partition
        max_micro: Maximum micro-cells per segment (build plate limit)
        min_segment_micro: Minimum acceptable segment size
        mode: Segmentation strategy
        M: Microcells per U (only used for ALIGNED mode)

    Returns:
        List of segment sizes in micro-cells
    """
    if total_micro <= 0:
        return []

    if total_micro <= max_micro:
        # Fits in one piece
        return [total_micro]

    # Handle ALIGNED mode first
    if mode == SegmentationMode.ALIGNED:
        return _partition_micro_aligned(total_micro, max_micro, min_segment_micro, M)

    if mode == SegmentationMode.MAX_THEN_REMAINDER:
        # Use max size for all but last, remainder in last
        n_full = total_micro // max_micro
        remainder = total_micro % max_micro

        if remainder == 0:
            return [max_micro] * n_full
        elif remainder >= min_segment_micro:
            return [max_micro] * n_full + [remainder]
        else:
            # Remainder too small - redistribute
            # Add remainder to last full piece if it fits
            if n_full > 0 and (max_micro + remainder) <= max_micro:
                # This shouldn't happen since remainder > 0 means it doesn't fit
                pass
            # Otherwise, reduce one full piece to make remainder larger
            if n_full > 0:
                # Take from last piece to give to remainder
                reduction = min_segment_micro - remainder
                return [max_micro] * (n_full - 1) + [max_micro - reduction, remainder + reduction]
            else:
                return [total_micro]

    # EVEN mode: find best distribution
    n_min = math.ceil(total_micro / max_micro)

    best_segments = None
    best_score = (float("inf"), float("inf"))  # (n, spread)

    # Try a range of segment counts
    for n in range(n_min, n_min + 7):
        if n <= 0:
            continue

        base = total_micro // n
        remainder = total_micro % n

        # Distribute: 'remainder' segments get (base+1), rest get 'base'
        segments = [base + 1] * remainder + [base] * (n - remainder)

        # Check constraints
        if any(s > max_micro for s in segments):
            continue
        if any(s < min_segment_micro for s in segments):
            # Only reject if we have other options
            if best_segments is not None:
                continue

        # Score: prefer fewer segments, then minimize spread
        spread = max(segments) - min(segments)
        score = (n, spread)

        if score < best_score:
            best_score = score
            best_segments = segments

    if best_segments is None:
        # Fallback: just use max_then_remainder logic
        n_full = total_micro // max_micro
        remainder = total_micro % max_micro
        if remainder == 0:
            return [max_micro] * n_full
        else:
            return [max_micro] * n_full + [remainder]

    return best_segments


def compute_cumulative_offsets(segments: List[int]) -> List[int]:
    """Compute cumulative offsets for a list of segments.

    Returns list where cumulative[i] is the start position of segment i.
    """
    cumulative = [0]
    for s in segments[:-1]:
        cumulative.append(cumulative[-1] + s)
    return cumulative


def compute_seam_stations(
    segments: List[int],
    cumulative: List[int],
    clip_pitch_micro: int,
    end_margin_micro: int,
) -> Dict[int, List[int]]:
    """Compute clip station positions along seams between segments.

    Seams are at positions cumulative[1], cumulative[2], etc. (between segments).
    Stations are placed along the seam at clip_pitch_micro intervals.

    Args:
        segments: List of segment sizes in micro-cells
        cumulative: Cumulative start positions
        clip_pitch_micro: Clip pitch in micro-cells
        end_margin_micro: Keep-out distance from corners

    Returns:
        Dict mapping seam_index -> list of global station positions (micro-cells)
        seam_index is 0-based (seam 0 is between segment 0 and 1)
    """
    if len(segments) <= 1:
        return {}

    result = {}

    for seam_idx in range(len(segments) - 1):
        # Seam is between segment[seam_idx] and segment[seam_idx + 1]
        # The seam runs along the perpendicular axis

        # For now, we need the perpendicular length to place stations
        # This function is called separately for X and Y axes
        # The caller will combine them appropriately

        # Actually, seam stations depend on the OTHER axis length
        # This needs to be handled at a higher level
        # Here we just return the seam positions (where seams exist)
        seam_position = cumulative[seam_idx + 1]
        result[seam_idx] = [seam_position]

    return result


def compute_notch_positions_along_edge(
    edge_length_micro: int,
    clip_pitch_micro: int,
    end_margin_micro: int,
    origin_micro: int = 0,
    M: int = 4,
) -> List[int]:
    """Compute notch positions along a single edge, centered on cell openings.

    Notches are placed at the center of full-U cells in global coordinates,
    then converted to local edge coordinates. Cell centers occur at:
        global_pos = (M // 2) + k * clip_pitch_micro
    For M=4, centers are at microcells 2, 6, 10, 14... (0.5U, 1.5U, 2.5U...)

    Args:
        edge_length_micro: Edge length in micro-cells
        clip_pitch_micro: Clip pitch in micro-cells (typically M for 1U pitch)
        end_margin_micro: Keep-out distance from corners (micro-cells)
        origin_micro: Global offset of this edge's start (micro-cells)
        M: Micro-divisions per U (typically 4)

    Returns:
        List of notch positions (in micro-cells from edge start)
    """
    if edge_length_micro <= 2 * end_margin_micro:
        # Edge too short for any notches with margin
        # Place one in center if there's room
        if edge_length_micro >= 2:
            return [edge_length_micro // 2]
        return []

    positions = []
    g0 = M // 2  # Cell center offset (2 for M=4, i.e., 0.5U into each cell)

    # Find the first k such that global_pos >= origin_micro + end_margin_micro
    # global_pos = g0 + k * clip_pitch_micro
    # We need: g0 + k * clip_pitch_micro >= origin_micro + end_margin_micro
    # So: k >= (origin_micro + end_margin_micro - g0) / clip_pitch_micro
    min_global = origin_micro + end_margin_micro
    max_global = origin_micro + edge_length_micro - end_margin_micro

    if clip_pitch_micro <= 0:
        return []

    # Find first valid k
    k_start = max(0, (min_global - g0 + clip_pitch_micro - 1) // clip_pitch_micro)
    if min_global <= g0:
        k_start = 0

    k = k_start
    while True:
        global_pos = g0 + k * clip_pitch_micro
        if global_pos > max_global:
            break
        local_pos = global_pos - origin_micro
        if local_pos >= end_margin_micro and local_pos <= edge_length_micro - end_margin_micro:
            positions.append(local_pos)
        k += 1

    # Fallback: if no positions found but edge is long enough, place one in center
    if not positions and edge_length_micro >= 2 * end_margin_micro:
        positions.append(edge_length_micro // 2)

    return positions


# =============================================================================
# Main Layout Class
# =============================================================================


class GridfinityBaseplateLayout:
    """Calculates optimal baseplate layout for a drawer given build plate constraints.

    All internal calculations use integer micro-cells to prevent float drift.
    """

    def __init__(
        self,
        drawer_x_mm: float,
        drawer_y_mm: float,
        build_plate_x_mm: float,
        build_plate_y_mm: float,
        micro_divisions: int = 4,
        tolerance_mm: float = 0.5,
        tolerance_mode: ToleranceMode = ToleranceMode.CENTERED,
        min_segment_u: float = 1.0,
        segmentation_mode: SegmentationMode = SegmentationMode.ALIGNED,
        print_margin_mm: float = 2.0,
        clip_pitch_u: float = 1.0,
        clip_end_margin_u: float = 0.25,
        fill_edges: Tuple[str, ...] = ("left", "right", "front", "back"),
    ):
        """Initialize the layout calculator.

        Args:
            drawer_x_mm: Drawer interior X dimension (mm)
            drawer_y_mm: Drawer interior Y dimension (mm)
            build_plate_x_mm: Build plate X dimension (mm)
            build_plate_y_mm: Build plate Y dimension (mm)
            micro_divisions: Grid subdivision (1=1U, 2=0.5U, 4=0.25U)
            tolerance_mm: Total gap tolerance for drawer clearance (mm)
            tolerance_mode: How tolerance is applied (centered or corner)
            min_segment_u: Minimum acceptable segment size in U (flooring rule)
            segmentation_mode: Strategy for partitioning (aligned, even, or max_then_remainder)
            print_margin_mm: Safety margin for build plate (mm)
            clip_pitch_u: Clip spacing in U
            clip_end_margin_u: Keep-out from corners for clips (U)
            fill_edges: Which edges get integrated fill ("left"/"right"/"front"/"back")
        """
        # Validate inputs
        if micro_divisions not in (1, 2, 4):
            raise ValueError("micro_divisions must be 1, 2, or 4")

        # Validate clip_pitch compatibility with micro_divisions
        clip_pitch_micro = clip_pitch_u * micro_divisions
        if abs(clip_pitch_micro - round(clip_pitch_micro)) > 1e-6:
            raise ValueError(
                f"clip_pitch_u ({clip_pitch_u}) * micro_divisions ({micro_divisions}) "
                f"must be an integer, got {clip_pitch_micro}"
            )

        self.drawer_x_mm = drawer_x_mm
        self.drawer_y_mm = drawer_y_mm
        self.build_plate_x_mm = build_plate_x_mm
        self.build_plate_y_mm = build_plate_y_mm
        self.micro_divisions = micro_divisions
        self.tolerance_mm = tolerance_mm
        self.tolerance_mode = tolerance_mode
        self.min_segment_u = min_segment_u
        self.segmentation_mode = segmentation_mode
        self.print_margin_mm = print_margin_mm
        self.clip_pitch_u = clip_pitch_u
        self.clip_end_margin_u = clip_end_margin_u
        self.fill_edges = fill_edges

        # Derived values
        self.micro_pitch = GRU / micro_divisions
        self.min_segment_micro = math.ceil(min_segment_u * micro_divisions)
        self.clip_pitch_micro = int(round(clip_pitch_u * micro_divisions))
        self.clip_end_margin_micro = math.ceil(clip_end_margin_u * micro_divisions)

        # Calculate layout
        self._layout: Optional[LayoutResult] = None

    def _calculate_layout(self) -> LayoutResult:
        """Perform the layout calculation."""

        # Step 1: Compute usable drawer span
        usable_x = self.drawer_x_mm - self.tolerance_mm
        usable_y = self.drawer_y_mm - self.tolerance_mm

        # Step 2: Compute total micro-cells and remainder fill
        total_micro_x = int(usable_x // self.micro_pitch)
        total_micro_y = int(usable_y // self.micro_pitch)

        fill_x_mm = usable_x - (total_micro_x * self.micro_pitch)
        fill_y_mm = usable_y - (total_micro_y * self.micro_pitch)

        # Split fill between both sides (centered in drawer)
        # If fill_edges includes both left and right, split X fill
        # If only one side, all fill goes to that side
        has_left = "left" in self.fill_edges
        has_right = "right" in self.fill_edges
        has_front = "front" in self.fill_edges
        has_back = "back" in self.fill_edges

        if has_left and has_right:
            fill_x_left = fill_x_mm / 2
            fill_x_right = fill_x_mm - fill_x_left  # Ensures exact sum
        elif has_left:
            fill_x_left = fill_x_mm
            fill_x_right = 0.0
        elif has_right:
            fill_x_left = 0.0
            fill_x_right = fill_x_mm
        else:
            fill_x_left = 0.0
            fill_x_right = 0.0

        if has_front and has_back:
            fill_y_front = fill_y_mm / 2
            fill_y_back = fill_y_mm - fill_y_front
        elif has_front:
            fill_y_front = fill_y_mm
            fill_y_back = 0.0
        elif has_back:
            fill_y_front = 0.0
            fill_y_back = fill_y_mm
        else:
            fill_y_front = 0.0
            fill_y_back = 0.0

        # Step 3: Compute max printable span in micro-cells
        max_print_x = self.build_plate_x_mm - self.print_margin_mm
        max_print_y = self.build_plate_y_mm - self.print_margin_mm

        max_micro_x = int(max_print_x // self.micro_pitch)
        max_micro_y = int(max_print_y // self.micro_pitch)

        # Step 4: Partition into segments (flooring logic)
        segments_x = partition_micro(
            total_micro_x,
            max_micro_x,
            self.min_segment_micro,
            self.segmentation_mode,
            M=self.micro_divisions,
        )
        segments_y = partition_micro(
            total_micro_y,
            max_micro_y,
            self.min_segment_micro,
            self.segmentation_mode,
            M=self.micro_divisions,
        )

        # Compute cumulative offsets for global seam coordinates
        cumulative_x = compute_cumulative_offsets(segments_x)
        cumulative_y = compute_cumulative_offsets(segments_y)

        # Step 5: Generate pieces
        pieces = []
        n_x = len(segments_x)
        n_y = len(segments_y)

        # Track clip count
        total_clips = 0
        seam_stations: Dict[str, List[int]] = {}

        for ix, seg_x in enumerate(segments_x):
            for iy, seg_y in enumerate(segments_y):
                # Determine legacy edge modes (for backward compatibility)
                edge_left = EdgeMode.OUTER if ix == 0 else EdgeMode.JOIN
                edge_right = EdgeMode.OUTER if ix == n_x - 1 else EdgeMode.JOIN
                edge_front = EdgeMode.OUTER if iy == 0 else EdgeMode.JOIN
                edge_back = EdgeMode.OUTER if iy == n_y - 1 else EdgeMode.JOIN

                # Determine new edge roles (Option B: seam-disappears half-frame)
                # OUTER edges: drawer boundary -> FULL_FRAME
                # SEAM edges: piece-to-piece -> HALF_FRAME (two halves make one full)
                # FILL_OUTER edges: fill strip boundary -> FLAT_WALL
                edge_role_left = EdgeRole.OUTER if ix == 0 else EdgeRole.SEAM
                edge_role_right = EdgeRole.OUTER if ix == n_x - 1 else EdgeRole.SEAM
                edge_role_front = EdgeRole.OUTER if iy == 0 else EdgeRole.SEAM
                edge_role_back = EdgeRole.OUTER if iy == n_y - 1 else EdgeRole.SEAM

                # Determine per-edge fill amounts (split fill goes to both sides)
                piece_fill_left = 0.0
                piece_fill_right = 0.0
                piece_fill_front = 0.0
                piece_fill_back = 0.0
                fill_inner_mode_x = FillInnerMode.NONE
                fill_inner_mode_y = FillInnerMode.NONE

                # Left edge fill (leftmost pieces only)
                if ix == 0 and fill_x_left > 0:
                    piece_fill_left = fill_x_left
                    edge_role_left = EdgeRole.FILL_OUTER
                    fill_inner_mode_x = FillInnerMode.HALF_PROFILE

                # Right edge fill (rightmost pieces only)
                if ix == n_x - 1 and fill_x_right > 0:
                    piece_fill_right = fill_x_right
                    edge_role_right = EdgeRole.FILL_OUTER
                    fill_inner_mode_x = FillInnerMode.HALF_PROFILE

                # Front edge fill (frontmost pieces only)
                if iy == 0 and fill_y_front > 0:
                    piece_fill_front = fill_y_front
                    edge_role_front = EdgeRole.FILL_OUTER
                    fill_inner_mode_y = FillInnerMode.HALF_PROFILE

                # Back edge fill (backmost pieces only)
                if iy == n_y - 1 and fill_y_back > 0:
                    piece_fill_back = fill_y_back
                    edge_role_back = EdgeRole.FILL_OUTER
                    fill_inner_mode_y = FillInnerMode.HALF_PROFILE

                # Legacy fill_x_mm / fill_y_mm for backward compatibility
                piece_fill_x = piece_fill_left + piece_fill_right
                piece_fill_y = piece_fill_front + piece_fill_back

                # Determine frame modes based on edge roles
                def role_to_frame_mode(role: EdgeRole) -> EdgeFrameMode:
                    if role == EdgeRole.OUTER:
                        return EdgeFrameMode.FULL_FRAME
                    elif role == EdgeRole.SEAM:
                        return EdgeFrameMode.HALF_FRAME
                    elif role == EdgeRole.FILL_OUTER:
                        return EdgeFrameMode.FLAT_WALL
                    return EdgeFrameMode.FULL_FRAME

                edge_frame_left = role_to_frame_mode(edge_role_left)
                edge_frame_right = role_to_frame_mode(edge_role_right)
                edge_frame_front = role_to_frame_mode(edge_role_front)
                edge_frame_back = role_to_frame_mode(edge_role_back)

                # Compute notch positions for SEAM edges
                # Notches are centered on cell openings using global coordinates
                notches_left = []
                notches_right = []
                notches_front = []
                notches_back = []

                # Left/right edges run along Y axis - use cumulative_y for origin
                origin_my = cumulative_y[iy]
                if edge_role_left == EdgeRole.SEAM:
                    notches_left = compute_notch_positions_along_edge(
                        seg_y,
                        self.clip_pitch_micro,
                        self.clip_end_margin_micro,
                        origin_micro=origin_my,
                        M=self.micro_divisions,
                    )
                if edge_role_right == EdgeRole.SEAM:
                    notches_right = compute_notch_positions_along_edge(
                        seg_y,
                        self.clip_pitch_micro,
                        self.clip_end_margin_micro,
                        origin_micro=origin_my,
                        M=self.micro_divisions,
                    )

                # Front/back edges run along X axis - use cumulative_x for origin
                origin_mx = cumulative_x[ix]
                if edge_role_front == EdgeRole.SEAM:
                    notches_front = compute_notch_positions_along_edge(
                        seg_x,
                        self.clip_pitch_micro,
                        self.clip_end_margin_micro,
                        origin_micro=origin_mx,
                        M=self.micro_divisions,
                    )
                if edge_role_back == EdgeRole.SEAM:
                    notches_back = compute_notch_positions_along_edge(
                        seg_x,
                        self.clip_pitch_micro,
                        self.clip_end_margin_micro,
                        origin_micro=origin_mx,
                        M=self.micro_divisions,
                    )

                # Compute origin position in drawer
                origin_x = cumulative_x[ix] * self.micro_pitch
                origin_y = cumulative_y[iy] * self.micro_pitch

                if self.tolerance_mode == ToleranceMode.CENTERED:
                    origin_x += self.tolerance_mm / 2
                    origin_y += self.tolerance_mm / 2

                piece_id = f"piece_{ix}_{iy}"

                piece = PieceSpec(
                    id=piece_id,
                    size_mx=seg_x,
                    size_my=seg_y,
                    fill_x_mm=piece_fill_x,
                    fill_y_mm=piece_fill_y,
                    # Per-edge fill amounts
                    fill_left=piece_fill_left,
                    fill_right=piece_fill_right,
                    fill_front=piece_fill_front,
                    fill_back=piece_fill_back,
                    # Legacy edge modes
                    edge_left=edge_left,
                    edge_right=edge_right,
                    edge_front=edge_front,
                    edge_back=edge_back,
                    # New edge system
                    edge_role_left=edge_role_left,
                    edge_role_right=edge_role_right,
                    edge_role_front=edge_role_front,
                    edge_role_back=edge_role_back,
                    edge_frame_left=edge_frame_left,
                    edge_frame_right=edge_frame_right,
                    edge_frame_front=edge_frame_front,
                    edge_frame_back=edge_frame_back,
                    fill_inner_mode_x=fill_inner_mode_x,
                    fill_inner_mode_y=fill_inner_mode_y,
                    # Notches
                    notches_left=tuple(notches_left),
                    notches_right=tuple(notches_right),
                    notches_front=tuple(notches_front),
                    notches_back=tuple(notches_back),
                    origin_x_mm=origin_x,
                    origin_y_mm=origin_y,
                    grid_x=ix,
                    grid_y=iy,
                    cumulative_mx=cumulative_x[ix],
                    cumulative_my=cumulative_y[iy],
                )
                pieces.append(piece)

        # Step 6: Count clips (each seam station needs one clip)
        # Vertical seams (between X segments) - run along Y axis
        for ix in range(n_x - 1):
            for iy in range(n_y):
                seg_y = segments_y[iy]
                origin_my = cumulative_y[iy]
                stations = compute_notch_positions_along_edge(
                    seg_y,
                    self.clip_pitch_micro,
                    self.clip_end_margin_micro,
                    origin_micro=origin_my,
                    M=self.micro_divisions,
                )
                total_clips += len(stations)
                seam_key = f"v_{ix}_{iy}"
                seam_stations[seam_key] = stations

        # Horizontal seams (between Y segments) - run along X axis
        for iy in range(n_y - 1):
            for ix in range(n_x):
                seg_x = segments_x[ix]
                origin_mx = cumulative_x[ix]
                stations = compute_notch_positions_along_edge(
                    seg_x,
                    self.clip_pitch_micro,
                    self.clip_end_margin_micro,
                    origin_micro=origin_mx,
                    M=self.micro_divisions,
                )
                total_clips += len(stations)
                seam_key = f"h_{ix}_{iy}"
                seam_stations[seam_key] = stations

        return LayoutResult(
            drawer_x_mm=self.drawer_x_mm,
            drawer_y_mm=self.drawer_y_mm,
            build_plate_x_mm=self.build_plate_x_mm,
            build_plate_y_mm=self.build_plate_y_mm,
            micro_divisions=self.micro_divisions,
            tolerance_mm=self.tolerance_mm,
            tolerance_mode=self.tolerance_mode,
            total_micro_x=total_micro_x,
            total_micro_y=total_micro_y,
            fill_x_mm=fill_x_mm,
            fill_y_mm=fill_y_mm,
            fill_x_left=fill_x_left,
            fill_x_right=fill_x_right,
            fill_y_front=fill_y_front,
            fill_y_back=fill_y_back,
            segments_x=segments_x,
            segments_y=segments_y,
            cumulative_x=cumulative_x,
            cumulative_y=cumulative_y,
            pieces=pieces,
            clip_pitch_u=self.clip_pitch_u,
            clip_count=total_clips,
            seam_stations=seam_stations,
        )

    def get_layout(self) -> LayoutResult:
        """Get the calculated layout (cached)."""
        if self._layout is None:
            self._layout = self._calculate_layout()
        return self._layout

    def print_summary(self) -> None:
        """Print human-readable layout summary."""
        print(self.get_layout().summary())

    def get_piece(self, piece_id: str) -> Optional[PieceSpec]:
        """Get a piece by ID."""
        layout = self.get_layout()
        for piece in layout.pieces:
            if piece.id == piece_id:
                return piece
        return None

    def get_piece_at(self, grid_x: int, grid_y: int) -> Optional[PieceSpec]:
        """Get a piece by grid position."""
        layout = self.get_layout()
        for piece in layout.pieces:
            if piece.grid_x == grid_x and piece.grid_y == grid_y:
                return piece
        return None

    def render_piece(self, piece_id: str, **baseplate_kwargs) -> "cq.Workplane":
        """Render a single piece by ID.

        Args:
            piece_id: The piece ID (e.g., "piece_0_0")
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            CadQuery Workplane with the rendered baseplate
        """
        piece = self.get_piece(piece_id)
        if piece is None:
            raise ValueError(f"Piece '{piece_id}' not found")
        return self._render_piece_spec(piece, **baseplate_kwargs)

    def render_piece_at(self, grid_x: int, grid_y: int, **baseplate_kwargs) -> "cq.Workplane":
        """Render a piece at a specific grid position.

        Args:
            grid_x: X grid index
            grid_y: Y grid index
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            CadQuery Workplane with the rendered baseplate
        """
        piece = self.get_piece_at(grid_x, grid_y)
        if piece is None:
            raise ValueError(f"Piece at ({grid_x}, {grid_y}) not found")
        return self._render_piece_spec(piece, **baseplate_kwargs)

    def _create_baseplate_from_spec(self, piece: PieceSpec, **baseplate_kwargs):
        """Create a GridfinityBaseplate from a PieceSpec without rendering.

        This is used by rendering methods that need access to the baseplate
        object for post-render operations like strip cropping.

        Args:
            piece: The PieceSpec to convert
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            GridfinityBaseplate instance (not yet rendered)
        """
        from microfinity.parts.baseplate import GridfinityBaseplate

        # Convert sizes from micro-cells to U
        length_u = piece.size_mx / self.micro_divisions
        width_u = piece.size_my / self.micro_divisions

        # Set up solid fill using per-edge fill amounts
        solid_fill = piece.solid_fill

        # Set up notch positions
        notch_positions = {
            "left": list(piece.notches_left),
            "right": list(piece.notches_right),
            "front": list(piece.notches_front),
            "back": list(piece.notches_back),
        }

        return GridfinityBaseplate(
            length_u=length_u,
            width_u=width_u,
            micro_divisions=self.micro_divisions,
            origin_mx=piece.cumulative_mx,
            origin_my=piece.cumulative_my,
            edge_roles=piece.edge_roles,
            edge_frame_modes=piece.edge_frame_modes,
            fill_inner_mode_x=piece.fill_inner_mode_x,
            fill_inner_mode_y=piece.fill_inner_mode_y,
            edge_modes=piece.edge_modes,
            solid_fill=solid_fill,
            notch_positions=notch_positions,
            **baseplate_kwargs,
        )

    def _render_piece_spec(self, piece: PieceSpec, **baseplate_kwargs) -> "cq.Workplane":
        """Render a PieceSpec to geometry.

        Args:
            piece: The PieceSpec to render
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            CadQuery Workplane with the rendered baseplate
        """
        bp = self._create_baseplate_from_spec(piece, **baseplate_kwargs)
        return bp.render()

    def render_preview(self, include_clips: bool = False, **baseplate_kwargs) -> "cq.Workplane":
        """Render all pieces positioned in the drawer for visualization.

        Args:
            include_clips: Whether to include clip geometries at seams
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            CadQuery Workplane with all pieces positioned
        """
        import cadquery as cq

        layout = self.get_layout()
        pieces_geom = []

        for piece in layout.pieces:
            bp = self._render_piece_spec(piece, **baseplate_kwargs)

            # Translate to drawer position
            # Account for the baseplate being centered on its grid
            size_mm = piece.size_mm(self.micro_divisions)
            x_offset = piece.origin_x_mm + size_mm[0] / 2
            y_offset = piece.origin_y_mm + size_mm[1] / 2

            bp = bp.translate((x_offset, y_offset, 0))
            pieces_geom.append(bp)

        # Combine all pieces using batch compound (O(1) vs O(n) sequential unions)
        result = union_all(pieces_geom)

        if include_clips and layout.clip_count > 0:
            clips = self.render_clips_at_seams()
            if clips is not None and result is not None:
                result = result.union(clips)

        return result

    def render_clips_at_seams(self) -> Optional["cq.Workplane"]:
        """Render clips positioned at all seam locations.

        Returns:
            CadQuery Workplane with all clips positioned, or None if no clips
        """
        import cadquery as cq

        layout = self.get_layout()
        if layout.clip_count == 0:
            return None

        clip = GridfinityConnectionClip()
        clip_geom = clip.render()
        clips_geom = []

        # Place clips at vertical seams (between X segments)
        n_x = len(layout.segments_x)
        n_y = len(layout.segments_y)

        for ix in range(n_x - 1):
            for iy in range(n_y):
                seam_key = f"v_{ix}_{iy}"
                stations = layout.seam_stations.get(seam_key, [])

                # Seam X position
                seam_x = layout.cumulative_x[ix + 1] * self.micro_pitch
                if self.tolerance_mode == ToleranceMode.CENTERED:
                    seam_x += self.tolerance_mm / 2

                # Y origin for this segment
                seg_y_start = layout.cumulative_y[iy] * self.micro_pitch
                if self.tolerance_mode == ToleranceMode.CENTERED:
                    seg_y_start += self.tolerance_mm / 2

                for station in stations:
                    station_y = seg_y_start + station * self.micro_pitch
                    c = clip_geom.rotate((0, 0, 0), (0, 0, 1), 90)  # Rotate for vertical seam
                    c = c.translate((seam_x, station_y, 0))
                    clips_geom.append(c)

        # Place clips at horizontal seams (between Y segments)
        for iy in range(n_y - 1):
            for ix in range(n_x):
                seam_key = f"h_{ix}_{iy}"
                stations = layout.seam_stations.get(seam_key, [])

                # Seam Y position
                seam_y = layout.cumulative_y[iy + 1] * self.micro_pitch
                if self.tolerance_mode == ToleranceMode.CENTERED:
                    seam_y += self.tolerance_mm / 2

                # X origin for this segment
                seg_x_start = layout.cumulative_x[ix] * self.micro_pitch
                if self.tolerance_mode == ToleranceMode.CENTERED:
                    seg_x_start += self.tolerance_mm / 2

                for station in stations:
                    station_x = seg_x_start + station * self.micro_pitch
                    c = clip_geom.translate((station_x, seam_y, 0))
                    clips_geom.append(c)

        # Combine all clips using batch compound (O(1) vs O(n) sequential unions)
        return union_all(clips_geom)

    def render_clip_sheet(
        self,
        count: Optional[int] = None,
        spacing_mm: float = 5.0,
        columns: Optional[int] = None,
    ) -> "cq.Workplane":
        """Render multiple clips arranged for batch printing.

        Args:
            count: Number of clips (defaults to layout.clip_count)
            spacing_mm: Spacing between clips
            columns: Number of columns (auto-calculated if None)

        Returns:
            CadQuery Workplane with clips arranged in a grid
        """
        import cadquery as cq

        layout = self.get_layout()
        if count is None:
            count = layout.clip_count

        if count <= 0:
            raise ValueError("No clips to render")

        clip = GridfinityConnectionClip()
        clip_geom = clip.render()

        # Get clip bounding box for spacing
        bb = clip_geom.val().BoundingBox()
        clip_width = bb.xlen + spacing_mm
        clip_depth = bb.ylen + spacing_mm

        # Auto-calculate columns to fit build plate
        if columns is None:
            columns = max(1, int((self.build_plate_x_mm - self.print_margin_mm) // clip_width))

        rows = math.ceil(count / columns)

        # Collect all clip positions
        clips_geom = []
        for i in range(count):
            col = i % columns
            row = i // columns

            x = col * clip_width
            y = row * clip_depth

            c = clip_geom.translate((x, y, 0))
            clips_geom.append(c)

        # Combine all clips using batch compound (O(1) vs O(n) sequential unions)
        return union_all(clips_geom)

    def export_all(
        self,
        path: str,
        file_format: str = "step",
        include_clips: bool = True,
        strict: bool = False,
        **baseplate_kwargs,
    ) -> List[str]:
        """Export all unique pieces as individual files.

        Uses signature-based deduplication to avoid exporting identical pieces
        multiple times. Each unique piece type is exported once with a count
        in the filename.

        Args:
            path: Directory path to export files to
            file_format: File format ("step" or "stl")
            include_clips: Whether to export a clip sheet
            strict: If True, raise on first failure; if False, warn and continue
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            List of exported file paths
        """
        import os

        os.makedirs(path, exist_ok=True)

        layout = self.get_layout()
        unique = layout.unique_pieces()
        ext = ".step" if file_format.lower() == "step" else ".stl"

        # Render all geometries and build export list
        export_items = []

        for sig, (piece, count) in unique.items():
            # Generate descriptive filename
            size_u = piece.size_u(self.micro_divisions)
            size_str = f"{size_u[0]:.2f}x{size_u[1]:.2f}U"

            # Edge mode string (for identifying piece type)
            edge_str = ""
            if piece.edge_left == EdgeMode.JOIN:
                edge_str += "L"
            if piece.edge_right == EdgeMode.JOIN:
                edge_str += "R"
            if piece.edge_front == EdgeMode.JOIN:
                edge_str += "F"
            if piece.edge_back == EdgeMode.JOIN:
                edge_str += "B"

            # Fill string
            fill_str = ""
            if piece.fill_x_mm > 0:
                fill_str += f"_fx{piece.fill_x_mm:.1f}"
            if piece.fill_y_mm > 0:
                fill_str += f"_fy{piece.fill_y_mm:.1f}"

            # Build filename
            if edge_str:
                filename = f"baseplate_{size_str}_join{edge_str}{fill_str}_x{count}"
            else:
                filename = f"baseplate_{size_str}{fill_str}_x{count}"

            filepath = os.path.join(path, filename + ext)

            # Render geometry
            geom = self._render_piece_spec(piece, **baseplate_kwargs)
            export_items.append((geom, filepath))

        # Add clips if requested
        if include_clips and layout.clip_count > 0:
            clip_filename = f"clips_x{layout.clip_count}"
            clip_filepath = os.path.join(path, clip_filename + ext)
            clip_geom = self.render_clip_sheet()
            export_items.append((clip_geom, clip_filepath))

        # Delegate to exporter (sequential - OCCT is not thread-safe)
        return GridfinityExporter.batch_export(
            export_items,
            file_format=file_format,
            strict=strict,
        )

    def export_preview(
        self,
        filepath: str,
        file_format: str = "step",
        include_clips: bool = False,
        **baseplate_kwargs,
    ) -> str:
        """Export the full preview as a single file.

        Args:
            filepath: Full path to the output file
            file_format: File format ("step" or "stl")
            include_clips: Whether to include clips at seams
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            Absolute path to exported file
        """
        geom = self.render_preview(include_clips=include_clips, **baseplate_kwargs)

        if file_format.lower() == "step":
            return GridfinityExporter.to_step(geom, filepath)
        else:
            return GridfinityExporter.to_stl(geom, filepath)

    # =========================================================================
    # Test Print Methods: Fit Strips
    # =========================================================================

    def render_fit_strip_x(
        self,
        strip_width_mm: float = 10.0,
        edge: str = "front",
        **baseplate_kwargs,
    ) -> List[Tuple[str, "cq.Workplane"]]:
        """Render fit test strips for the X dimension (tests total assembled X length).

        Returns thin strips from pieces along one horizontal edge (front or back).
        When printed and assembled, these strips span the full drawer X dimension
        for testing fit before committing to full prints.

        Args:
            strip_width_mm: Width of each strip (default 10mm)
            edge: Which edge to use ("front" or "back")
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            List of (piece_id, geometry) tuples for pieces on the selected edge
        """
        if edge not in ("front", "back"):
            raise ValueError(f"edge must be 'front' or 'back', got '{edge}'")

        layout = self.get_layout()
        n_y = len(layout.segments_y)

        # Select the row of pieces on the specified edge
        target_iy = 0 if edge == "front" else n_y - 1

        results = []
        for piece in layout.pieces:
            if piece.grid_y == target_iy:
                # Check if this piece has the correct edge as outer boundary
                edge_role = piece.edge_role_front if edge == "front" else piece.edge_role_back
                if edge_role in (EdgeRole.OUTER, EdgeRole.FILL_OUTER):
                    # Render full piece, then crop to strip
                    bp = self._create_baseplate_from_spec(piece, **baseplate_kwargs)
                    full_geom = bp.render()
                    strip_geom = bp.crop_to_strip(full_geom, edge, strip_width_mm)
                    results.append((piece.id, strip_geom))

        return results

    def render_fit_strip_y(
        self,
        strip_width_mm: float = 10.0,
        edge: str = "left",
        **baseplate_kwargs,
    ) -> List[Tuple[str, "cq.Workplane"]]:
        """Render fit test strips for the Y dimension (tests total assembled Y length).

        Returns thin strips from pieces along one vertical edge (left or right).
        When printed and assembled, these strips span the full drawer Y dimension
        for testing fit before committing to full prints.

        Args:
            strip_width_mm: Width of each strip (default 10mm)
            edge: Which edge to use ("left" or "right")
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            List of (piece_id, geometry) tuples for pieces on the selected edge
        """
        if edge not in ("left", "right"):
            raise ValueError(f"edge must be 'left' or 'right', got '{edge}'")

        layout = self.get_layout()
        n_x = len(layout.segments_x)

        # Select the column of pieces on the specified edge
        target_ix = 0 if edge == "left" else n_x - 1

        results = []
        for piece in layout.pieces:
            if piece.grid_x == target_ix:
                # Check if this piece has the correct edge as outer boundary
                edge_role = piece.edge_role_left if edge == "left" else piece.edge_role_right
                if edge_role in (EdgeRole.OUTER, EdgeRole.FILL_OUTER):
                    # Render full piece, then crop to strip
                    bp = self._create_baseplate_from_spec(piece, **baseplate_kwargs)
                    full_geom = bp.render()
                    strip_geom = bp.crop_to_strip(full_geom, edge, strip_width_mm)
                    results.append((piece.id, strip_geom))

        return results

    def export_fit_strips(
        self,
        path: str,
        strip_width_mm: float = 10.0,
        file_format: str = "step",
        strict: bool = False,
        **baseplate_kwargs,
    ) -> List[str]:
        """Export fit test strips for both X and Y dimensions.

        Creates thin edge strips that can be printed and assembled to test
        drawer fit before committing to full baseplate prints.

        Args:
            path: Directory path to export files to
            strip_width_mm: Width of each strip (default 10mm)
            file_format: File format ("step" or "stl")
            strict: If True, raise on first failure; if False, warn and continue
            **baseplate_kwargs: Additional kwargs passed to GridfinityBaseplate

        Returns:
            List of exported file paths
        """
        import os

        os.makedirs(path, exist_ok=True)
        ext = ".step" if file_format.lower() == "step" else ".stl"

        # Build list of items to export
        export_items = []

        # X-fit strips (front edge)
        x_strips = self.render_fit_strip_x(strip_width_mm, edge="front", **baseplate_kwargs)
        for piece_id, geom in x_strips:
            filename = f"fit_strip_x_{piece_id}{ext}"
            filepath = os.path.join(path, filename)
            export_items.append((geom, filepath))

        # Y-fit strips (left edge)
        y_strips = self.render_fit_strip_y(strip_width_mm, edge="left", **baseplate_kwargs)
        for piece_id, geom in y_strips:
            filename = f"fit_strip_y_{piece_id}{ext}"
            filepath = os.path.join(path, filename)
            export_items.append((geom, filepath))

        return GridfinityExporter.batch_export(
            export_items,
            file_format=file_format,
            strict=strict,
        )


# =============================================================================
# Connection Clip
# =============================================================================


class GridfinityConnectionClip:
    """Connection clip for joining baseplate pieces.

    The clip is a flat rectangular prism that spans the seam between
    two baseplates, fitting into the through-slot notches on each side.

    Dimensions are derived from the canonical NotchSpec:
    - Width (along edge): notch_width - clip_clearance_mm
    - Length (across seam): 2 * notch_depth - axial_tolerance + seam_gap_mm
    - Height: notch_height - clip_clearance_mm

    Clearance/Tolerance:
    - clip_clearance_mm: Applied to width AND height (positive = smaller clip = looser fit)
    - axial_tolerance_mm: Applied to length to prevent clip touching inner profile.
        If None, defaults to max(clip_clearance_mm, 0.0) so positive clearance
        shortens the clip, but negative clearance doesn't make it longer.
    - seam_gap_mm: Gap between adjacent pieces (default 0.0)

    Lead-in:
    - lead_in_mm: Chamfer on vertical edges to ease insertion (default 0.0)

    The clip is designed to be printed flat without supports.
    """

    # Internal constant for clip grid spacing (not a parameter)
    _CLIP_GAP_MM = 2.0

    def __init__(
        self,
        clip_clearance_mm: float = 0.0,
        seam_gap_mm: float = 0.0,
        notch_spec: Optional[NotchSpec] = None,
        clip_ct: Optional[int] = None,
        lead_in_mm: float = 0.0,
        axial_tolerance_mm: Optional[float] = None,
        # Legacy alias
        clearance_mm: Optional[float] = None,
    ):
        """Initialize the clip with geometry parameters.

        Args:
            clip_clearance_mm: Clearance applied to clip width and height
                (positive = smaller = looser fit). Default 0.0 for nominal fit.
            seam_gap_mm: Gap between adjacent baseplate pieces. Default 0.0.
            notch_spec: NotchSpec defining the female slot geometry.
                If None, uses the default from get_notch_spec().
            clip_ct: Number of clips to render in render_flat(). If None or 1,
                renders a single clip (default behavior). Only affects render_flat(),
                not render().
            lead_in_mm: Chamfer applied to all vertical edges for easier
                insertion. Default 0.0 (no chamfer).
            axial_tolerance_mm: Clearance applied to clip length to prevent
                touching inner mating profile. If None, defaults to
                max(clip_clearance_mm, 0.0). This ensures positive clearance
                shortens the clip, but negative clearance doesn't extend it.
            clearance_mm: Deprecated alias for clip_clearance_mm.
        """
        # Handle legacy clearance_mm parameter
        if clearance_mm is not None:
            warnings.warn(
                "clearance_mm is deprecated, use clip_clearance_mm instead",
                DeprecationWarning,
                stacklevel=2,
            )
            if clip_clearance_mm == 0.0:
                clip_clearance_mm = clearance_mm

        # Get notch spec (source of truth for dimensions)
        self._notch_spec = notch_spec if notch_spec is not None else get_notch_spec()
        self.clip_clearance_mm = float(clip_clearance_mm)
        self.seam_gap_mm = float(seam_gap_mm)
        self.lead_in_mm = float(lead_in_mm)

        # Axial tolerance: if not specified, derive from clearance (clamped to >= 0)
        # This ensures positive clearance shortens clip, negative doesn't lengthen it
        if axial_tolerance_mm is not None:
            self.axial_tolerance_mm = float(axial_tolerance_mm)
        else:
            self.axial_tolerance_mm = max(clip_clearance_mm, 0.0)

        # Normalize clip_ct: None -> 1, validate >= 1
        self.clip_ct = 1 if clip_ct is None else int(clip_ct)
        if self.clip_ct < 1:
            raise ValueError("clip_ct must be >= 1")

    @property
    def dims(self) -> Tuple[float, float, float]:
        """Get clip dimensions (width, length, height) in mm.

        - Width: notch_width - clip_clearance_mm
        - Length: 2 * notch_depth - axial_tolerance_mm + seam_gap_mm
        - Height: notch_height - clip_clearance_mm

        The axial_tolerance_mm ensures the clip doesn't touch the inner
        mating profile. It defaults to max(clip_clearance_mm, 0.0).
        """
        w = max(0.1, self._notch_spec.width - self.clip_clearance_mm)
        length = max(0.1, 2.0 * self._notch_spec.depth - self.axial_tolerance_mm + self.seam_gap_mm)
        h = max(0.1, self._notch_spec.height - self.clip_clearance_mm)
        return (w, length, h)

    @property
    def notch_spec(self) -> NotchSpec:
        """Get the NotchSpec used for this clip's dimensions."""
        return self._notch_spec

    def render(self) -> "cq.Workplane":
        """Render the clip geometry.

        Returns geometry centered at origin, Z centered on origin.
        If lead_in_mm > 0, applies chamfer to all vertical edges.

        Returns:
            CadQuery Workplane with the clip geometry
        """
        import cadquery as cq

        w, l, h = self.dims
        clip = cq.Workplane("XY").box(w, l, h)

        if self.lead_in_mm > 0:
            try:
                # Chamfer all vertical edges for orientation-agnostic insertion
                clip = clip.edges("|Z").chamfer(self.lead_in_mm)
            except Exception:
                pass  # Skip if chamfer fails (e.g., too large for geometry)

        return clip

    def _render_one_flat(self) -> "cq.Workplane":
        """Render a single clip oriented for flat printing (Z=0 at bottom).

        Returns:
            CadQuery Workplane with single clip positioned for printing
        """
        import cadquery as cq

        w, l, h = self.dims
        clip = cq.Workplane("XY").box(w, l, h)

        if self.lead_in_mm > 0:
            try:
                clip = clip.edges("|Z").chamfer(self.lead_in_mm)
            except Exception:
                pass

        # Position with bottom at Z=0
        return clip.translate((0, 0, h / 2.0))

    def render_flat(self) -> "cq.Workplane":
        """Render clip(s) oriented for flat printing (Z=0 at bottom).

        If clip_ct is 1 (default), returns a single clip.
        If clip_ct > 1, returns multiple clips arranged in a grid.

        Note: clip_ct only affects this method, not render(). This ensures
        layout.render_clip_sheet() (which uses render()) won't multiply.

        Returns:
            CadQuery Workplane with clip(s) positioned for printing
        """
        one = self._render_one_flat()

        if self.clip_ct == 1:
            return one

        # Arrange multiple clips in a grid
        w, l, h = self.dims
        cols = math.ceil(math.sqrt(self.clip_ct))
        dx = w + self._CLIP_GAP_MM
        dy = l + self._CLIP_GAP_MM

        # Collect all clip positions
        clips_geom = []
        for i in range(self.clip_ct):
            r = i // cols
            c = i % cols
            inst = one.translate((c * dx, r * dy, 0))
            clips_geom.append(inst)

        # Combine using batch compound (O(1) vs O(n) sequential unions)
        return union_all(clips_geom)
