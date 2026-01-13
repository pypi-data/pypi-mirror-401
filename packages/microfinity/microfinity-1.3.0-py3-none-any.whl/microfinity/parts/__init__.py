"""Gridfinity part generators.

This subpackage contains classes for generating Gridfinity-compatible parts:
- baseplate: GridfinityBaseplate and related utilities
- baseplate_layout: GridfinityBaseplateLayout for tiled layouts
- box: GridfinityBox and GridfinitySolidBox
- drawer: GridfinityDrawerSpacer
"""

from .baseplate import (
    GridfinityBaseplate,
    NotchSpec,
    get_notch_spec,
    make_notch_cutter,
    make_notch_cutter_outer_anchored,
    get_straight_band_z,
    compute_notch_z_band,
    get_seam_wall_thickness_mm,
    get_seam_cut_depth_mm,
    NOTCH_WIDTH_MM,
    NOTCH_DEPTH_MM,
    NOTCH_HEIGHT_MM,
    NOTCH_CHAMFER_MM,
    NOTCH_TOP_MARGIN_MM,
    NOTCH_BOT_MARGIN_MM,
    NOTCH_THROUGH_OVERCUT_MM,
    NOTCH_KEEPOUT_TOP_MM,
    EdgeMode,
    EdgeRole,
    EdgeFrameMode,
    FillInnerMode,
)
from .baseplate_layout import (
    GridfinityBaseplateLayout,
    GridfinityConnectionClip,
    LayoutResult,
    PieceSpec,
    SegmentationMode,
    ToleranceMode,
)
from .box import GridfinityBox, GridfinitySolidBox
from .drawer import GridfinityDrawerSpacer
