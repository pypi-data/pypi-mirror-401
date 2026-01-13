"""microfinity - A python library to make Gridfinity compatible objects with CadQuery."""

import os

# fmt: off
__project__ = 'microfinity'
__version__ = '1.3.0'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

# Core components
from .core.constants import *
from .core.base import GridfinityObject
from .core.helpers import union_all, quarter_circle, chamf_cyl, chamf_rect
from .core.export import GridfinityExporter, SVGView

# Parts
from .parts.baseplate import (
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
    NOTCH_KEEPOUT_TOP_MM,  # Deprecated
    EdgeMode,
    EdgeRole,
    EdgeFrameMode,
    FillInnerMode,
)
from .parts.box import GridfinityBox, GridfinitySolidBox
from .parts.drawer import GridfinityDrawerSpacer
from .parts.baseplate_layout import (
    GridfinityBaseplateLayout,
    GridfinityConnectionClip,
    LayoutResult,
    PieceSpec,
    SegmentationMode,
    ToleranceMode,
)

# Calibration tools
from .calibration.test_prints import (
    generate_fractional_pocket_test,
    generate_fractional_pocket_test_set,
    generate_clip_clearance_sweep,
    generate_clip_test_set,
    export_test_prints,
)
