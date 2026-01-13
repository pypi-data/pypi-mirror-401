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
# Gridfinity Baseplates

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import cadquery as cq

from microfinity.core.constants import (
    GRU,
    GRU2,
    GRU_CUT,
    GR_RAD,
    GR_WALL,
    GR_BASE_HEIGHT,
    GR_BASE_PROFILE,
    GR_STR_BASE_PROFILE,
    GR_STR_H,
    GR_BASE_TOP_CHAMF,
    EPS,
)
from microfinity.core.base import GridfinityObject
from cqkit.cq_helpers import (
    rounded_rect_sketch,
    composite_from_pts,
    rotate_x,
    recentre,
)
from cqkit import VerticalEdgeSelector, HasZCoordinateSelector
from microfinity.core.helpers import union_all


# =============================================================================
# Enums
# =============================================================================


class EdgeMode(Enum):
    """Legacy edge mode for baseplate edges (deprecated, kept for backward compatibility)."""

    OUTER = "outer"  # Edge touches drawer wall - no notches, standard rim
    JOIN = "join"  # Edge joins another baseplate - has notches, modified rim


class EdgeRole(Enum):
    """What this edge touches (semantic role)."""

    OUTER = "outer"  # Touches drawer wall
    SEAM = "seam"  # Touches adjacent piece (will have notches)
    FILL_OUTER = "fill_outer"  # Outer boundary of fill strip (flat wall)


class EdgeFrameMode(Enum):
    """How this edge is rendered geometrically."""

    FULL_FRAME = "full_frame"  # Full perimeter frame width (OUTER edges)
    HALF_FRAME = "half_frame"  # Half frame width (SEAM edges, Option B seam-disappears)
    FLAT_WALL = "flat_wall"  # Vertical wall only (FILL_OUTER edges)


class FillInnerMode(Enum):
    """How the inner edge of a fill strip is rendered (virtual edge, not piece boundary)."""

    NONE = "none"  # No fill on this axis
    HALF_PROFILE = "half_profile"  # Half baseplate profile for bin support


# =============================================================================
# Constants
# =============================================================================

# Notch geometry constants (configurable defaults)
# These define the notch pocket that accepts the clip leg
NOTCH_WIDTH_MM = 8.0  # Width along the edge (mm)
NOTCH_DEPTH_MM = 1.2  # Depth into the rim wall (mm)
NOTCH_HEIGHT_MM = 1.6  # Height of the notch pocket (mm)
NOTCH_CHAMFER_MM = 0.3  # Lead-in chamfer for clip insertion

# Notch Z placement margins within the straight (90°) wall section
# The notch must sit entirely within the straight vertical section of the
# baseplate profile, avoiding the 45° chamfers at top and bottom.
NOTCH_TOP_MARGIN_MM = 0.1  # Margin below top of straight section
NOTCH_BOT_MARGIN_MM = 0.0  # Margin above bottom of straight section

# Deprecated - kept for backward compatibility
NOTCH_KEEPOUT_TOP_MM = 0.4  # No longer used for placement; see get_straight_band_z()

# Frame geometry constants (deprecated - now using microcell system)
DEFAULT_FRAME_WIDTH_MM = 2.15  # Frame width that matches existing geometry

# Through-slot geometry constants
# The notch cuts completely through the seam wall (not a blind pocket)
NOTCH_THROUGH_OVERCUT_MM = 0.1  # Small overcut for robust boolean subtraction


def get_seam_wall_thickness_mm(frame_width_mm: float = DEFAULT_FRAME_WIDTH_MM) -> float:
    """Get the wall thickness at SEAM edges (half-frame width).

    DEPRECATED: Use get_seam_cut_depth_mm() for through-slot cutting.
    This function returns half-frame width, but the actual seam wall
    at notch Z height is full-frame width.

    Args:
        frame_width_mm: Full frame width used by the baseplate instance

    Returns:
        Seam wall thickness in mm (half of frame width)
    """
    return frame_width_mm / 2.0


def get_seam_cut_depth_mm(frame_width_mm: float = DEFAULT_FRAME_WIDTH_MM) -> float:
    """Get nominal per-side depth for seam slot at notch Z height.

    This is the depth from seam outer face to the inner mating profile.
    Used for:
    - Determining clip engagement depth (clip_length = 2 * this - axial_tolerance)
    - Computing boolean cutter depth (this + NOTCH_THROUGH_OVERCUT_MM)

    The boolean overcut is NOT included here - it's added separately when
    creating the cutter geometry for robust boolean operations.

    Args:
        frame_width_mm: Full frame width used by the baseplate instance

    Returns:
        Nominal cut depth per side in mm (full frame width)
    """
    return frame_width_mm


# Microcell pocket constants
# Overcut is applied to pocket dimensions to match full-cell behavior
POCKET_OVERCUT = GRU_CUT - GRU  # ~0.2mm total overcut


# =============================================================================
# Notch Z Placement (Profile-Derived)
# =============================================================================


def get_straight_band_z(total_height: float = GR_BASE_HEIGHT) -> Tuple[float, float]:
    """Get the Z range of the straight (90°) section of the baseplate profile.

    The baseplate outer wall profile has three sections (top to bottom):
    1. Upper 45° chamfer (GR_BASE_TOP_CHAMF vertical height)
    2. Straight 90° vertical section (GR_STR_H height) <- notch goes here
    3. Lower 45° chamfer (GR_BASE_CHAMF_H vertical height)

    The notch/clip must sit entirely within the straight section to avoid
    intersecting the 45° chamfered regions.

    Args:
        total_height: Total height of the baseplate (default: GR_BASE_HEIGHT)

    Returns:
        (z_bottom, z_top) of the straight vertical section
    """
    z_top = total_height - GR_BASE_TOP_CHAMF
    z_bot = z_top - GR_STR_H
    return (z_bot, z_top)


def compute_notch_z_band(
    total_height: float,
    notch_height: float = NOTCH_HEIGHT_MM,
    top_margin: float = NOTCH_TOP_MARGIN_MM,
    bot_margin: float = NOTCH_BOT_MARGIN_MM,
) -> Tuple[float, float]:
    """Compute the notch Z position within the straight wall section.

    Places the notch at the top of the straight section (minus margin),
    ensuring it fits entirely within the 90° vertical band.

    Args:
        total_height: Total height of the baseplate
        notch_height: Height of the notch pocket
        top_margin: Margin below top of straight section
        bot_margin: Margin above bottom of straight section

    Returns:
        (notch_bottom_z, notch_top_z)

    Raises:
        ValueError: If notch doesn't fit within the straight band
    """
    z_band_bot, z_band_top = get_straight_band_z(total_height)
    available_height = (z_band_top - top_margin) - (z_band_bot + bot_margin)

    if notch_height > available_height + 1e-6:
        raise ValueError(
            f"Notch height {notch_height}mm exceeds available {available_height:.2f}mm "
            f"in straight band (margins: top={top_margin}, bot={bot_margin})"
        )

    notch_top_z = z_band_top - top_margin
    notch_bot_z = notch_top_z - notch_height

    return (notch_bot_z, notch_top_z)


# =============================================================================
# Notch Specification (Canonical Female Geometry)
# =============================================================================


@dataclass(frozen=True)
class NotchSpec:
    """Canonical specification for connector notch (female slot) geometry.

    This is the single source of truth for notch dimensions used by both
    production baseplates and test prints. The clip (male part) derives
    its dimensions from this spec.

    Note: Z placement is now derived from the profile geometry via
    compute_notch_z_band(), not from keepout_top.

    Attributes:
        width: Width of notch along the edge (mm)
        depth: Depth of notch into the rim wall (mm)
        height: Height of notch pocket (mm)
        chamfer: Lead-in chamfer on top edges (mm)
        keepout_top: Deprecated - kept for backward compatibility
    """

    width: float
    depth: float
    height: float
    chamfer: float
    keepout_top: float  # Deprecated, not used for Z placement

    def notch_z_band(self, total_height: float) -> Tuple[float, float]:
        """Calculate the Z range of the notch within the straight wall section.

        Uses profile-derived placement to ensure notch sits in the 90° section.

        Args:
            total_height: Total height of the baseplate

        Returns:
            (notch_bottom_z, notch_top_z)
        """
        return compute_notch_z_band(total_height, self.height)

    def notch_bottom_z(self, total_height: float) -> float:
        """Calculate the Z position of the notch bottom face.

        Args:
            total_height: Total height of the baseplate

        Returns:
            Z coordinate of the notch bottom face
        """
        bot_z, _ = self.notch_z_band(total_height)
        return bot_z

    def notch_top_z(self, total_height: float) -> float:
        """Calculate the Z position of the notch top face.

        Args:
            total_height: Total height of the baseplate

        Returns:
            Z coordinate of the notch top face
        """
        _, top_z = self.notch_z_band(total_height)
        return top_z


def get_notch_spec(
    width: float = NOTCH_WIDTH_MM,
    depth: Optional[float] = None,
    height: float = NOTCH_HEIGHT_MM,
    chamfer: float = NOTCH_CHAMFER_MM,
    keepout_top: float = NOTCH_KEEPOUT_TOP_MM,
) -> NotchSpec:
    """Get the canonical notch specification.

    Returns the standard notch geometry used by production baseplates.
    Test prints and clips should use this to ensure geometry matches.

    The default depth is the nominal per-side cut depth (full frame width),
    which defines how far the clip engages per side. The boolean cutter
    adds NOTCH_THROUGH_OVERCUT_MM to this for robust cutting.

    Note: keepout_top is deprecated - Z placement is now derived from
    the profile geometry via compute_notch_z_band().

    Args:
        width: Width along edge (default: NOTCH_WIDTH_MM = 8.0)
        depth: Nominal per-side cut depth (default: ~2.15mm full frame width).
            If None, uses get_seam_cut_depth_mm(DEFAULT_FRAME_WIDTH_MM).
            This does NOT include the boolean overcut.
        height: Height of slot (default: NOTCH_HEIGHT_MM = 1.6)
        chamfer: Lead-in chamfer (default: NOTCH_CHAMFER_MM = 0.3)
        keepout_top: Deprecated, kept for backward compatibility

    Returns:
        NotchSpec with the canonical dimensions
    """
    # Default depth is nominal per-side cut depth (no overcut)
    if depth is None:
        depth = get_seam_cut_depth_mm(DEFAULT_FRAME_WIDTH_MM)

    return NotchSpec(
        width=width,
        depth=depth,
        height=height,
        chamfer=chamfer,
        keepout_top=keepout_top,
    )


def make_notch_cutter(
    spec: Optional[NotchSpec] = None,
    width: Optional[float] = None,
    depth: Optional[float] = None,
    height: Optional[float] = None,
    chamfer: Optional[float] = None,
) -> cq.Workplane:
    """Create a notch cutter solid (rectangular pocket with optional chamfer).

    The cutter is centered at origin in XY, with Z from 0 to height.
    The caller is responsible for positioning and rotating it.

    This is the canonical notch cutter geometry used by production baseplates.
    Test prints should use this same function to ensure consistency.

    Args:
        spec: NotchSpec to use (if None, uses default from get_notch_spec())
        width: Override width (uses spec.width if None)
        depth: Override depth (uses spec.depth if None)
        height: Override height (uses spec.height if None)
        chamfer: Override chamfer (uses spec.chamfer if None)

    Returns:
        CadQuery Workplane with the notch cutter solid, centered at origin,
        Z from 0 to height, oriented with width along X, depth along Y.
    """
    if spec is None:
        spec = get_notch_spec()

    w = width if width is not None else spec.width
    d = depth if depth is not None else spec.depth
    h = height if height is not None else spec.height
    c = chamfer if chamfer is not None else spec.chamfer

    # Create rectangular pocket centered at origin
    notch = cq.Workplane("XY").box(w, d, h).translate((0, 0, h / 2))

    # Add lead-in chamfer on top face edges
    if c > 0:
        try:
            notch = notch.faces(">Z").edges().chamfer(c)
        except Exception:
            pass  # Skip chamfer if it fails (e.g., chamfer too large)

    return notch


def make_notch_cutter_outer_anchored(
    spec: Optional[NotchSpec] = None,
    width: Optional[float] = None,
    depth: Optional[float] = None,
    height: Optional[float] = None,
    chamfer: Optional[float] = None,
    overcut: float = NOTCH_THROUGH_OVERCUT_MM,
) -> cq.Workplane:
    """Create a notch cutter solid with outer face anchored at Y=0.

    This is the through-slot version of make_notch_cutter(). The cutter
    extends from Y=0 (seam plane) inward to Y=cut_depth, making placement
    trivial: align Y=0 with the seam plane.

    Coordinate system (outer-face anchored):
    - Centered in X (width direction)
    - Outer face at Y=0, extends to Y=cut_depth (inward)
    - Z from 0 to height

    Args:
        spec: NotchSpec to use (if None, uses default)
        width: Override width
        depth: Override depth (seam wall thickness)
        height: Override height
        chamfer: Override chamfer
        overcut: Additional depth for boolean robustness (default 0.1mm)

    Returns:
        CadQuery Workplane with the notch cutter, outer face at Y=0
    """
    if spec is None:
        spec = get_notch_spec()

    w = width if width is not None else spec.width
    d = depth if depth is not None else spec.depth
    h = height if height is not None else spec.height
    c = chamfer if chamfer is not None else spec.chamfer

    cut_depth = d + overcut

    # Create box centered in X, outer face at Y=0, Z from 0 to height
    # box() creates geometry centered at origin, so translate to anchor outer face at Y=0
    notch = cq.Workplane("XY").box(w, cut_depth, h)
    notch = notch.translate((0, cut_depth / 2, h / 2))

    # Add lead-in chamfer on top face edges
    if c > 0:
        try:
            notch = notch.faces(">Z").edges().chamfer(c)
        except Exception:
            pass  # Skip chamfer if it fails

    return notch


# =============================================================================
# Microcell Segmentation Helpers
# =============================================================================


def _segment_axis(
    origin_m: int,
    size_m: int,
    M: int = 4,
) -> List[int]:
    """Segment an axis into pocket widths (in microcells).

    Computes pocket segment widths that align with the global grid based on
    the piece's origin offset. Pockets extend to all boundaries - the pocket
    wall at each edge serves as the profile (half-profile for SEAM edges,
    full closure for OUTER edges).

    Args:
        origin_m: Global microcell offset (cumulative_mx or cumulative_my)
        size_m: Size in microcells (e.g., 14 for 3.5U)
        M: Microcells per U (always 4)

    Returns:
        List of segment widths in microcells, e.g., [2, 4, 4, 4, 2]
    """
    if size_m <= 0:
        return []

    # Compute segments that align to global grid
    o = origin_m % M  # Phase within a U cell

    # Leading partial (to align to global grid boundary)
    lead = (M - o) % M
    if lead > size_m:
        lead = size_m

    N2 = size_m - lead
    full = N2 // M  # Full 1U cells
    trail = N2 % M  # Trailing partial

    segments = []
    if lead > 0:
        segments.append(lead)
    segments.extend([M] * full)
    if trail > 0:
        segments.append(trail)

    return segments


def _micro_pitch(M: int = 4) -> float:
    """Get micro-pitch in mm for a given microcell count per U."""
    return GRU / M


# =============================================================================
# GridfinityBaseplate Class
# =============================================================================


class GridfinityBaseplate(GridfinityObject):
    """Gridfinity Baseplate

    This class represents a basic Gridfinity baseplate object. This baseplate
    more or less conforms to the original simple baseplate released by
    Zach Freedman. As such, it does not include features such as mounting
    holes, magnet holes, weight slots, etc.

    Standard Parameters:
      length_u - length in U (42 mm / U), can be fractional with micro_divisions
      width_u - width in U (42 mm / U), can be fractional with micro_divisions
      ext_depth - extrude bottom face by an extra amount in mm
      straight_bottom - remove bottom chamfer and replace with straight side
      corner_screws - add countersink mounting screws to the inside corners
      corner_tab_size - size of mounting screw corner tabs
      csk_hole - mounting screw hole diameter
      csk_diam - mounting screw countersink diameter
      csk_angle - mounting screw countersink angle

    Microcell System Parameters (for fractional U support):
      micro_divisions - grid subdivision (1=1U, 2=0.5U, 4=0.25U increments)
      origin_mx - global microcell X offset (for grid alignment across pieces)
      origin_my - global microcell Y offset (for grid alignment across pieces)
      outer_fillet_radius - fillet radius for outer corners (0 for sharp)

    Edge System Parameters:
      edge_roles - dict of EdgeRole per edge: {"left": EdgeRole.OUTER, ...}
      edge_frame_modes - dict of EdgeFrameMode per edge (deprecated with microcell system)
      fill_inner_mode_x - FillInnerMode for X-axis fill inner edge
      fill_inner_mode_y - FillInnerMode for Y-axis fill inner edge

    Legacy Parameters (deprecated, for backward compatibility):
      edge_modes - dict of EdgeMode per edge: {"left": EdgeMode.OUTER, ...}
      solid_fill - dict of fill amounts: {"right": 5.2, "back": 3.1} in mm
      notch_positions - dict of notch positions per edge (in micro-cells)
      notch_width - width of notch pocket along edge (mm)
      notch_depth - depth of notch pocket into rim (mm)
      frame_width_mm - width of perimeter frame band (mm) (deprecated)

    When edge_roles are all OUTER (default), the baseplate behaves as the
    original simple baseplate with no connector features.
    """

    def __init__(self, length_u, width_u, **kwargs):
        super().__init__()
        self.length_u = length_u
        self.width_u = width_u
        self.ext_depth = 0
        self.straight_bottom = False
        self.corner_screws = False
        self.corner_tab_size = 21
        self.csk_hole = 5.0
        self.csk_diam = 10.0
        self.csk_angle = 82

        # Microcell system parameters
        # Default micro_divisions: 1 for integer sizes (backward compatible), 4 for fractional
        self._auto_micro_divisions = True  # Flag to track if user explicitly set micro_divisions
        self.micro_divisions: int = 1  # Will be auto-set in _validate_and_compute_micro if needed
        self.origin_mx: int = 0  # Global microcell X offset
        self.origin_my: int = 0  # Global microcell Y offset
        self.outer_fillet_radius: float = GR_RAD  # Fillet radius (0 for sharp corners)

        # New edge system parameters (preferred, with backward-compatible defaults)
        self.edge_roles: Dict[str, EdgeRole] = {
            "left": EdgeRole.OUTER,
            "right": EdgeRole.OUTER,
            "front": EdgeRole.OUTER,
            "back": EdgeRole.OUTER,
        }
        self.edge_frame_modes: Dict[str, EdgeFrameMode] = {
            "left": EdgeFrameMode.FULL_FRAME,
            "right": EdgeFrameMode.FULL_FRAME,
            "front": EdgeFrameMode.FULL_FRAME,
            "back": EdgeFrameMode.FULL_FRAME,
        }
        self.fill_inner_mode_x: FillInnerMode = FillInnerMode.NONE
        self.fill_inner_mode_y: FillInnerMode = FillInnerMode.NONE
        self.frame_width_mm: float = DEFAULT_FRAME_WIDTH_MM  # Deprecated

        # Legacy edge mode parameters (deprecated, kept for backward compatibility)
        self.edge_modes: Dict[str, EdgeMode] = {
            "left": EdgeMode.OUTER,
            "right": EdgeMode.OUTER,
            "front": EdgeMode.OUTER,
            "back": EdgeMode.OUTER,
        }
        self.solid_fill: Dict[str, float] = {
            "left": 0.0,
            "right": 0.0,
            "front": 0.0,
            "back": 0.0,
        }
        # Notch positions: dict mapping edge -> list of positions in micro-cells
        self.notch_positions: Dict[str, List[int]] = {
            "left": [],
            "right": [],
            "front": [],
            "back": [],
        }
        # Notch geometry (can be overridden)
        self.notch_width = NOTCH_WIDTH_MM
        self.notch_depth = NOTCH_DEPTH_MM
        self.notch_height = NOTCH_HEIGHT_MM
        self.notch_keepout_top = NOTCH_KEEPOUT_TOP_MM
        self.notch_chamfer = NOTCH_CHAMFER_MM

        for k, v in kwargs.items():
            if k in self.__dict__ and v is not None:
                self.__dict__[k] = v
                if k == "micro_divisions":
                    self._auto_micro_divisions = False  # User explicitly set it
        if self.corner_screws:
            self.ext_depth = max(self.ext_depth, 5.0)

        # Validate and compute derived microcell values
        self._validate_and_compute_micro()

    def _validate_and_compute_micro(self):
        """Validate micro parameters and compute derived values.

        Auto-detects micro_divisions if not explicitly set:
        - Integer U sizes: micro_divisions=1 (backward compatible)
        - Fractional U sizes: auto-select smallest compatible micro_divisions
        """
        # Auto-detect micro_divisions if not explicitly set
        if self._auto_micro_divisions:
            is_length_int = abs(self.length_u - round(self.length_u)) < 1e-6
            is_width_int = abs(self.width_u - round(self.width_u)) < 1e-6

            if is_length_int and is_width_int:
                # Integer sizes: use 1 for backward compatibility
                self.micro_divisions = 1
            else:
                # Fractional sizes: find smallest compatible micro_divisions
                for md in [2, 4]:
                    size_mx = round(self.length_u * md)
                    size_my = round(self.width_u * md)
                    err_x = abs(size_mx / md - self.length_u)
                    err_y = abs(size_my / md - self.width_u)
                    if err_x < 1e-6 and err_y < 1e-6:
                        self.micro_divisions = md
                        break
                else:
                    raise ValueError(
                        f"Cannot find compatible micro_divisions for length_u={self.length_u}, width_u={self.width_u}. "
                        f"Sizes must be multiples of 0.25U (quarter grid)."
                    )

        # Compute size in microcells from length_u/width_u
        self._size_mx = round(self.length_u * self.micro_divisions)
        self._size_my = round(self.width_u * self.micro_divisions)

        # Validate that float→int conversion is accurate
        expected_length_u = self._size_mx / self.micro_divisions
        expected_width_u = self._size_my / self.micro_divisions

        if abs(expected_length_u - self.length_u) > 1e-6:
            raise ValueError(
                f"length_u ({self.length_u}) is not compatible with micro_divisions ({self.micro_divisions}). "
                f"Expected {expected_length_u}"
            )
        if abs(expected_width_u - self.width_u) > 1e-6:
            raise ValueError(
                f"width_u ({self.width_u}) is not compatible with micro_divisions ({self.micro_divisions}). "
                f"Expected {expected_width_u}"
            )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def size_mx(self) -> int:
        """Size in microcells (X axis)."""
        return self._size_mx

    @property
    def size_my(self) -> int:
        """Size in microcells (Y axis)."""
        return self._size_my

    @property
    def has_connectors(self) -> bool:
        """Check if this baseplate has any connector features (SEAM edges)."""
        # Check new system first
        if any(role == EdgeRole.SEAM for role in self.edge_roles.values()):
            return True
        # Fall back to legacy check
        return any(mode == EdgeMode.JOIN for mode in self.edge_modes.values())

    @property
    def has_fill(self) -> bool:
        """Check if this baseplate has any solid fill."""
        return any(fill > 0 for fill in self.solid_fill.values())

    @property
    def total_length(self) -> float:
        """Total length including solid fill."""
        return self.length + self.solid_fill.get("left", 0) + self.solid_fill.get("right", 0)

    @property
    def total_width(self) -> float:
        """Total width including solid fill."""
        return self.width + self.solid_fill.get("front", 0) + self.solid_fill.get("back", 0)

    @property
    def fill_offset_x(self) -> float:
        """X offset to center grid within total bounds (accounts for left fill)."""
        return self.solid_fill.get("left", 0) / 2 - self.solid_fill.get("right", 0) / 2

    @property
    def fill_offset_y(self) -> float:
        """Y offset to center grid within total bounds (accounts for front fill)."""
        return self.solid_fill.get("front", 0) / 2 - self.solid_fill.get("back", 0) / 2

    @property
    def total_height(self) -> float:
        """Total height of the baseplate."""
        return GR_BASE_HEIGHT + self.ext_depth

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _corner_pts(self):
        oxy = self.corner_tab_size / 2
        return [(i * (self.length / 2 - oxy), j * (self.width / 2 - oxy), 0) for i in (-1, 1) for j in (-1, 1)]

    def _is_outer_boundary(self, role: EdgeRole) -> bool:
        """Check if an edge role represents an outer boundary of the assembled baseplate.

        OUTER and FILL_OUTER are true outer boundaries.
        SEAM edges join to adjacent pieces, so corners there should be sharp.
        """
        return role in (EdgeRole.OUTER, EdgeRole.FILL_OUTER)

    def _get_frame_width(self, edge: str) -> float:
        """Get the frame width for a specific edge based on its frame mode.

        Args:
            edge: Edge name ("left", "right", "front", "back")

        Returns:
            Frame width in mm
        """
        mode = self.edge_frame_modes.get(edge, EdgeFrameMode.FULL_FRAME)
        if mode == EdgeFrameMode.FULL_FRAME:
            return self.frame_width_mm
        elif mode == EdgeFrameMode.HALF_FRAME:
            return self.frame_width_mm / 2
        elif mode == EdgeFrameMode.FLAT_WALL:
            # Flat wall has minimal width (just the wall thickness)
            return GR_WALL
        return self.frame_width_mm

    # =========================================================================
    # Geometry Generation: Microcell Grid Interior
    # =========================================================================

    def _render_grid_interior(self) -> cq.Workplane:
        """Render the bin mating surface pattern using microcell segmentation.

        Generates pocket cutters for each (x_segment, y_segment) pair.
        Segments can be fractional (1-3 microcells = 0.25-0.75U) or full (4 = 1U).

        This approach:
        - Cuts actual fractional pockets (not solid pads)
        - Aligns to global grid using origin_mx/my
        - Pockets extend to all edges (no seam bands)
        - Pocket walls at edges form half-profiles (SEAM) or full closure (OUTER)
        - Pocket field is constrained to grid region (excludes mm fill areas)

        Returns:
            CadQuery Workplane with combined pocket cutter geometry
        """
        # Get microcell pitch
        pitch = _micro_pitch(self.micro_divisions)

        # Profile for extrusion
        profile = GR_BASE_PROFILE if not self.straight_bottom else GR_STR_BASE_PROFILE
        if self.ext_depth > 0:
            profile = [*profile, self.ext_depth]

        # Segment each axis (edge-agnostic, just aligned to global grid)
        x_segments = _segment_axis(
            origin_m=self.origin_mx,
            size_m=self._size_mx,
            M=self.micro_divisions,
        )
        y_segments = _segment_axis(
            origin_m=self.origin_my,
            size_m=self._size_my,
            M=self.micro_divisions,
        )

        if not x_segments or not y_segments:
            # No pockets to cut
            return cq.Workplane("XY").box(0.001, 0.001, 0.001)

        # Compute pocket field bounds
        # IMPORTANT: Grid region is centered at origin. Fill strips are unioned
        # OUTSIDE the grid region. Pockets must be anchored to the grid region
        # bounds, NOT the total body bounds (which would shift pockets incorrectly
        # for asymmetric fill pieces).
        grid_len_mm = self._size_mx * pitch
        grid_wid_mm = self._size_my * pitch

        # Pocket field is the grid region, centered at origin
        pocket_x_min = -grid_len_mm / 2
        pocket_y_min = -grid_wid_mm / 2

        # Generate cutters for each segment pair
        cutters = []
        x_pos = pocket_x_min

        for x_m in x_segments:
            # Nominal width in mm for this X segment
            w_nom = x_m * pitch
            y_pos = pocket_y_min

            for y_m in y_segments:
                # Nominal height in mm for this Y segment
                h_nom = y_m * pitch

                # Apply overcut (same as full cells)
                w_cut = w_nom + POCKET_OVERCUT
                h_cut = h_nom + POCKET_OVERCUT

                # Clamp corner radius to fit pocket (must be positive)
                rad = min(GR_RAD, 0.5 * w_cut - EPS, 0.5 * h_cut - EPS)
                rad = max(0.1, rad)  # Ensure positive minimum

                # Create pocket cutter
                # Note: rounded_rect_sketch accepts float radius at runtime despite type hint
                cutter = self.extrude_profile(rounded_rect_sketch(w_cut, h_cut, rad), profile)  # type: ignore[arg-type]

                # Position: rotate 180 (profile extrudes downward), translate to position
                # Center of pocket is at (x_pos + w_nom/2, y_pos + h_nom/2)
                cx = x_pos + w_nom / 2
                cy = y_pos + h_nom / 2
                cutter = rotate_x(cutter, 180).translate((cx, cy, self.total_height))

                cutters.append(cutter)
                y_pos += h_nom

            x_pos += w_nom

        # Combine all cutters using batch compound (O(1) vs O(n) sequential unions)
        result = union_all(cutters)
        if result is None:
            return cq.Workplane("XY").box(0.001, 0.001, 0.001)

        # Option B: Intersect with grid mask to prevent overcut bleeding into fill
        # This ensures cutters cannot touch fill regions, even with overcut
        if self.has_fill:
            grid_mask = (
                cq.Workplane("XY")
                .rect(grid_len_mm, grid_wid_mm)
                .extrude(self.total_height + 10)  # Tall enough to cover cutters
            )
            result = result.intersect(grid_mask)

        return result

    # =========================================================================
    # Geometry Generation: Fill Strips
    # =========================================================================

    def _render_fill_strips(self) -> Optional[cq.Workplane]:
        """Render solid fill geometry for edges.

        Fill strips extend the baseplate beyond the grid area to fill sub-grid
        gaps in drawer layouts. They are added BEFORE the grid is cut.

        Returns:
            CadQuery Workplane with fill geometry, or None if no fill
        """
        fills = []

        # Grid area half-dimensions
        grid_half_l = self.length / 2
        grid_half_w = self.width / 2

        for edge, fill_mm in self.solid_fill.items():
            if fill_mm <= 0:
                continue

            if edge == "left":
                # Fill strip on left edge (-X side)
                fill = (
                    cq.Workplane("XY")
                    .box(fill_mm, self.width, self.total_height)
                    .translate((-grid_half_l - fill_mm / 2, 0, self.total_height / 2))
                )
                fills.append(fill)

            elif edge == "right":
                # Fill strip on right edge (+X side)
                fill = (
                    cq.Workplane("XY")
                    .box(fill_mm, self.width, self.total_height)
                    .translate((grid_half_l + fill_mm / 2, 0, self.total_height / 2))
                )
                fills.append(fill)

            elif edge == "front":
                # Fill strip on front edge (-Y side)
                # Width extends to cover corner fills if present
                fill_width = self.length + self.solid_fill.get("left", 0) + self.solid_fill.get("right", 0)
                x_offset = (self.solid_fill.get("right", 0) - self.solid_fill.get("left", 0)) / 2
                fill = (
                    cq.Workplane("XY")
                    .box(fill_width, fill_mm, self.total_height)
                    .translate((x_offset, -grid_half_w - fill_mm / 2, self.total_height / 2))
                )
                fills.append(fill)

            elif edge == "back":
                # Fill strip on back edge (+Y side)
                fill_width = self.length + self.solid_fill.get("left", 0) + self.solid_fill.get("right", 0)
                x_offset = (self.solid_fill.get("right", 0) - self.solid_fill.get("left", 0)) / 2
                fill = (
                    cq.Workplane("XY")
                    .box(fill_width, fill_mm, self.total_height)
                    .translate((x_offset, grid_half_w + fill_mm / 2, self.total_height / 2))
                )
                fills.append(fill)

        if not fills:
            return None

        # Combine all fills using batch compound (O(1) vs O(n) sequential unions)
        return union_all(fills)

    # =========================================================================
    # Geometry Generation: Notch Cutters
    # =========================================================================

    def _create_notch_cutter(
        self,
        edge: str,
        position_micro: int,
        base_notch: Optional[cq.Workplane] = None,
        notch_bottom_z: Optional[float] = None,
    ) -> Optional[cq.Workplane]:
        """Create a notch cutter for a single notch position.

        The notch is a through-slot cut through the seam wall to accept a clip.
        Uses outer-face-anchored cutter for precise placement.
        Notches are only cut on SEAM edges.

        Args:
            edge: Edge name ("left", "right", "front", "back")
            position_micro: Position along edge in micro-cells from edge start
            base_notch: Pre-created base notch geometry (for caching). If None,
                creates a new one using instance frame_width_mm.
            notch_bottom_z: Pre-computed Z position for notch bottom. Required
                if base_notch is provided.

        Returns:
            CadQuery workplane with the notch cutter geometry, or None if invalid
        """
        # Only cut notches on SEAM edges
        if self.edge_roles.get(edge) != EdgeRole.SEAM:
            # Fall back to legacy check
            if self.edge_modes.get(edge) != EdgeMode.JOIN:
                return None

        # Convert micro position to mm
        pitch = _micro_pitch(self.micro_divisions)
        position_mm = position_micro * pitch

        # Use cached base notch or create new one
        if base_notch is None:
            # Compute boolean cut depth: nominal depth + overcut for robust cutting
            cut_depth_per_side = get_seam_cut_depth_mm(self.frame_width_mm)
            boolean_cut_depth = cut_depth_per_side + NOTCH_THROUGH_OVERCUT_MM

            # Create outer-anchored cutter with boolean depth (true window)
            base_notch = make_notch_cutter_outer_anchored(
                width=self.notch_width,
                depth=boolean_cut_depth,
                height=self.notch_height,
                chamfer=self.notch_chamfer,
                overcut=0.0,  # Overcut already included in boolean_cut_depth
            )
            notch_bottom_z = compute_notch_z_band(self.total_height, self.notch_height)[0]

        # Translate to correct Z position
        # notch_bottom_z is guaranteed to be set at this point (either from cache or computed above)
        assert notch_bottom_z is not None
        notch = base_notch.translate((0, 0, notch_bottom_z))

        # Position the notch based on edge
        # Cutter has outer face at Y=0, extends in +Y direction (inward)
        # We place Y=0 at the seam plane (piece boundary)
        grid_half_l = self.length / 2
        grid_half_w = self.width / 2

        if edge == "left":
            # Left edge at -X, notch extends inward (+X direction)
            x = -grid_half_l
            y = -grid_half_w + position_mm
            # Rotate so +Y (cutter inward) becomes +X
            notch = notch.rotate((0, 0, 0), (0, 0, 1), -90)
            notch = notch.translate((x, y, 0))
        elif edge == "right":
            # Right edge at +X, notch extends inward (-X direction)
            x = grid_half_l
            y = -grid_half_w + position_mm
            # Rotate so +Y (cutter inward) becomes -X
            notch = notch.rotate((0, 0, 0), (0, 0, 1), 90)
            notch = notch.translate((x, y, 0))
        elif edge == "front":
            # Front edge at -Y, notch extends inward (+Y direction)
            x = -grid_half_l + position_mm
            y = -grid_half_w
            # No rotation needed, +Y is already inward
            notch = notch.translate((x, y, 0))
        elif edge == "back":
            # Back edge at +Y, notch extends inward (-Y direction)
            x = -grid_half_l + position_mm
            y = grid_half_w
            # Rotate 180° so +Y becomes -Y
            notch = notch.rotate((0, 0, 0), (0, 0, 1), 180)
            notch = notch.translate((x, y, 0))
        else:
            return None

        return notch

    def _create_all_notch_cutters(self) -> Optional[cq.Workplane]:
        """Create combined notch cutter for all notch positions.

        Only cuts notches on SEAM edges (or legacy JOIN edges).
        Uses cached base notch geometry for efficiency.

        Returns:
            Combined CadQuery workplane with all notches, or None if no notches
        """
        # Compute boolean cut depth: nominal depth + overcut for robust cutting
        cut_depth_per_side = get_seam_cut_depth_mm(self.frame_width_mm)
        boolean_cut_depth = cut_depth_per_side + NOTCH_THROUGH_OVERCUT_MM

        # Pre-create base notch geometry once (cache for all notches)
        # Uses outer-anchored cutter with boolean depth (true window)
        base_notch = make_notch_cutter_outer_anchored(
            width=self.notch_width,
            depth=boolean_cut_depth,
            height=self.notch_height,
            chamfer=self.notch_chamfer,
            overcut=0.0,  # Overcut already included in boolean_cut_depth
        )
        notch_bottom_z = compute_notch_z_band(self.total_height, self.notch_height)[0]

        cutters = []

        for edge, positions in self.notch_positions.items():
            # Check if this edge should have notches
            is_seam = self.edge_roles.get(edge) == EdgeRole.SEAM
            is_legacy_join = self.edge_modes.get(edge) == EdgeMode.JOIN

            if not (is_seam or is_legacy_join):
                continue  # Only cut notches on SEAM/JOIN edges

            for pos in positions:
                cutter = self._create_notch_cutter(edge, pos, base_notch=base_notch, notch_bottom_z=notch_bottom_z)
                if cutter is not None:
                    cutters.append(cutter)

        if not cutters:
            return None

        # Combine all cutters using batch compound (O(1) vs O(n) sequential unions)
        return union_all(cutters)

    # =========================================================================
    # Main Render Method
    # =========================================================================

    def render(self):
        """Render the baseplate geometry.

        This method creates the full baseplate using the correct order:
        1. Create main body (solid block)
        2. Union fill strips (to establish final outer silhouette)
        3. Fillet outer vertical edges (once, on final silhouette)
        4. Cut grid interior (microcell-segmented pockets)
        5. Cut connector notches (on SEAM edges only)
        6. Apply corner screws if enabled

        The microcell segmentation in _render_grid_interior() generates actual
        fractional pockets (0.25U, 0.5U, 0.75U), not solid pads. SEAM edges
        get solid bands to ensure mechanical strength at connections.

        Returns:
            CadQuery Workplane with the complete baseplate geometry
        """
        # =====================================================================
        # Pass 1: Create main body
        # =====================================================================
        r = cq.Workplane("XY").rect(self.length, self.width).extrude(self.total_height)

        # =====================================================================
        # Pass 2: Union fill strips (before fillet!)
        # =====================================================================
        # Fill strips must be added BEFORE filleting so corners are consistent
        if self.has_fill:
            fill_geom = self._render_fill_strips()
            if fill_geom is not None:
                r = r.union(fill_geom)

        # =====================================================================
        # Pass 3: Fillet outer corners (only true outer corners of assembled plate)
        # =====================================================================
        # A corner is rounded only if BOTH adjacent edges are outer boundaries.
        # This ensures interior corners (where pieces join) remain sharp.
        if self.outer_fillet_radius > 0:
            # Compute actual corner coordinates including fill
            fill_left = self.solid_fill.get("left", 0.0)
            fill_right = self.solid_fill.get("right", 0.0)
            fill_front = self.solid_fill.get("front", 0.0)
            fill_back = self.solid_fill.get("back", 0.0)

            x_min = -self.length / 2 - fill_left
            x_max = self.length / 2 + fill_right
            y_min = -self.width / 2 - fill_front
            y_max = self.width / 2 + fill_back
            z_mid = self.ext_depth / 2

            roles = self.edge_roles
            corners_to_round = []

            # Check each corner: round only if both adjacent edges are outer boundaries
            if self._is_outer_boundary(roles["left"]) and self._is_outer_boundary(roles["front"]):
                corners_to_round.append((x_min, y_min))  # front-left
            if self._is_outer_boundary(roles["right"]) and self._is_outer_boundary(roles["front"]):
                corners_to_round.append((x_max, y_min))  # front-right
            if self._is_outer_boundary(roles["left"]) and self._is_outer_boundary(roles["back"]):
                corners_to_round.append((x_min, y_max))  # back-left
            if self._is_outer_boundary(roles["right"]) and self._is_outer_boundary(roles["back"]):
                corners_to_round.append((x_max, y_max))  # back-right

            for cx, cy in corners_to_round:
                try:
                    # Pre-filter to vertical edges, then select nearest to corner point
                    r = (
                        r.edges("|Z")
                        .edges(cq.selectors.NearestToPointSelector((cx, cy, z_mid)))
                        .fillet(self.outer_fillet_radius)
                    )
                except Exception:
                    pass  # Skip if fillet fails for this corner

        # =====================================================================
        # Pass 4: Cut grid interior (microcell pockets)
        # =====================================================================
        grid_interior = self._render_grid_interior()
        r = r.cut(grid_interior)

        # =====================================================================
        # Pass 5: Cut connector notches (SEAM edges only)
        # =====================================================================
        if self.has_connectors:
            notch_cutters = self._create_all_notch_cutters()
            if notch_cutters is not None:
                r = r.cut(notch_cutters)

        # =====================================================================
        # Pass 6: Corner screws (optional)
        # =====================================================================
        if self.corner_screws:
            rs = cq.Sketch().rect(self.corner_tab_size, self.corner_tab_size)
            rs = cq.Workplane("XY").placeSketch(rs).extrude(self.ext_depth)
            rs = rs.faces(">Z").cskHole(self.csk_hole, cskDiameter=self.csk_diam, cskAngle=self.csk_angle)
            r = r.union(recentre(composite_from_pts(rs, self._corner_pts()), "XY"))
            bs = VerticalEdgeSelector(self.ext_depth) & HasZCoordinateSelector(0)
            r = r.edges(bs).fillet(GR_RAD)

        return r

    def crop_to_strip(
        self,
        body: cq.Workplane,
        edge: str,
        strip_width_mm: float = 10.0,
    ) -> cq.Workplane:
        """Crop a rendered baseplate to a thin strip along one edge.

        This is used for fit testing - the strip preserves the exact edge profile
        including fill, fillets, and frame geometry.

        Args:
            body: The rendered baseplate geometry
            edge: Which edge to keep ("left", "right", "front", "back")
            strip_width_mm: Width of the strip to keep (default 10mm)

        Returns:
            CadQuery Workplane with only the strip remaining
        """
        # Compute actual extents including fill
        fill_left = self.solid_fill.get("left", 0.0)
        fill_right = self.solid_fill.get("right", 0.0)
        fill_front = self.solid_fill.get("front", 0.0)
        fill_back = self.solid_fill.get("back", 0.0)

        x_min = -self.length / 2 - fill_left
        x_max = self.length / 2 + fill_right
        y_min = -self.width / 2 - fill_front
        y_max = self.width / 2 + fill_back

        # Full extents for the non-cropped dimension
        full_x = x_max - x_min
        full_y = y_max - y_min
        full_z = self.total_height

        # Create mask box based on which edge we're keeping
        if edge == "front":
            # Keep y in [y_min, y_min + strip_width_mm]
            mask_x = full_x + 2  # Slightly oversized to ensure clean intersection
            mask_y = strip_width_mm
            mask_center_x = (x_min + x_max) / 2
            mask_center_y = y_min + strip_width_mm / 2
        elif edge == "back":
            # Keep y in [y_max - strip_width_mm, y_max]
            mask_x = full_x + 2
            mask_y = strip_width_mm
            mask_center_x = (x_min + x_max) / 2
            mask_center_y = y_max - strip_width_mm / 2
        elif edge == "left":
            # Keep x in [x_min, x_min + strip_width_mm]
            mask_x = strip_width_mm
            mask_y = full_y + 2
            mask_center_x = x_min + strip_width_mm / 2
            mask_center_y = (y_min + y_max) / 2
        elif edge == "right":
            # Keep x in [x_max - strip_width_mm, x_max]
            mask_x = strip_width_mm
            mask_y = full_y + 2
            mask_center_x = x_max - strip_width_mm / 2
            mask_center_y = (y_min + y_max) / 2
        else:
            raise ValueError(f"Invalid edge: {edge}. Must be 'left', 'right', 'front', or 'back'")

        # Create the mask box and intersect
        mask = (
            cq.Workplane("XY")
            .center(mask_center_x, mask_center_y)
            .rect(mask_x, mask_y)
            .extrude(full_z + 2)  # Slightly taller to ensure clean intersection
            .translate((0, 0, -1))  # Shift down to cover full Z range
        )

        return body.intersect(mask)
