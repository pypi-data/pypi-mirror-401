#! /usr/bin/env python3
#
# meshcutter.core.cq_utils - CadQuery utilities and version compatibility
#
# This module provides CadQuery-specific utilities including version detection
# and the extrude_profile function used for generating foot geometry.

from __future__ import annotations

import math
from typing import List, Tuple, Union

import cadquery as cq

from meshcutter.core.constants import SQRT2


# -----------------------------------------------------------------------------
# CadQuery version detection
# -----------------------------------------------------------------------------
# CQ versions < 2.4.0 typically require zlen correction for tapered extrusions,
# i.e., scaling the vertical extrusion extent by 1/cos(taper).
# This is computed once at module load time.

ZLEN_FIX: bool = True
_test_result = cq.Workplane("XY").rect(2, 2).extrude(1, taper=45)
_test_bb = _test_result.vals()[0].BoundingBox()
if abs(_test_bb.zlen - 1.0) < 1e-3:
    ZLEN_FIX = False


# -----------------------------------------------------------------------------
# Profile extrusion
# -----------------------------------------------------------------------------


def extrude_profile(
    sketch,
    profile: List[Union[float, Tuple[float, float]]],
    workplane: str = "XY",
    angle: float = None,
) -> cq.Workplane:
    """Extrude a sketch through a multi-segment profile with optional tapers.

    This mirrors microfinity.core.base.GridfinityObject.extrude_profile() exactly
    to ensure geometric consistency.

    The profile is a list of segments, where each segment is either:
    - A float: straight extrusion of that height
    - A tuple (height, taper_angle): tapered extrusion

    Args:
        sketch: CadQuery sketch to extrude
        profile: List of profile segments
        workplane: Workplane orientation (default "XY")
        angle: Override angle for taper calculations

    Returns:
        CadQuery Workplane with the extruded geometry
    """
    taper = profile[0][1] if isinstance(profile[0], (list, tuple)) else 0
    zlen = profile[0][0] if isinstance(profile[0], (list, tuple)) else profile[0]

    if abs(taper) > 0:
        if angle is None:
            zlen = zlen if ZLEN_FIX else zlen / SQRT2
        else:
            zlen = zlen / math.cos(math.radians(taper)) if ZLEN_FIX else zlen

    r = cq.Workplane(workplane).placeSketch(sketch).extrude(zlen, taper=taper)

    for level in profile[1:]:
        if isinstance(level, (tuple, list)):
            if angle is None:
                zlen = level[0] if ZLEN_FIX else level[0] / SQRT2
            else:
                zlen = level[0] / math.cos(math.radians(level[1])) if ZLEN_FIX else level[0]
            r = r.faces(">Z").wires().toPending().extrude(zlen, taper=level[1])
        else:
            r = r.faces(">Z").wires().toPending().extrude(level)

    return r
