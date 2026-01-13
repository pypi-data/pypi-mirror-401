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
# Globally useful constants representing Gridfinity geometry

from math import sqrt

SQRT2 = sqrt(2)
EPS = 1e-5
M2_DIAM = 1.8
M2_CLR_DIAM = 2.5
M3_DIAM = 3
M3_CLR_DIAM = 3.5
M3_CB_DIAM = 5.5
M3_CB_DEPTH = 3.5

GRU = 42
GRU2 = GRU / 2
GRHU = 7


# Micro-grid support: quarter-pitch positioning (0.25U = 10.5mm)
# micro_pitch is derived at runtime based on micro_divisions parameter
# Default micro_divisions=1 means standard behavior, micro_divisions=4 means quarter-grid
def micro_pitch(micro_divisions=4):
    """Returns the micro-pitch for a given division factor."""
    return GRU / micro_divisions


GRU_CUT = 42.2  # base extrusion width
GR_WALL = 1.0  # nominal exterior wall thickness
GR_DIV_WALL = 1.2  # width of dividing walls
GR_TOL = 0.5  # nominal tolerance

GR_RAD = 4  # nominal exterior filleting radius
GR_BASE_CLR = 0.25  # clearance above the nominal base height
GR_BASE_HEIGHT = 4.75  # nominal base height

# baseplate extrusion profile
GR_BASE_CHAMF_H = 0.98994949 / SQRT2
GR_STR_H = 1.8
GR_BASE_TOP_CHAMF = GR_BASE_HEIGHT - GR_BASE_CHAMF_H - GR_STR_H
GR_BASE_PROFILE = (
    (GR_BASE_TOP_CHAMF * SQRT2, 45),
    GR_STR_H,
    (GR_BASE_CHAMF_H * SQRT2, 45),
)
GR_STR_BASE_PROFILE = (
    (GR_BASE_TOP_CHAMF * SQRT2, 45),
    GR_STR_H + GR_BASE_CHAMF_H,
)

GR_BOT_H = 7  # bin nominal floor height
GR_FILLET = 1.1  # inside filleting radius
GR_FLOOR = GR_BOT_H - GR_BASE_HEIGHT  # floor offset

# box/bin extrusion profile
GR_BOX_CHAMF_H = 1.1313708 / SQRT2
GR_BOX_TOP_CHAMF = GR_BASE_HEIGHT - GR_BOX_CHAMF_H - GR_STR_H + GR_BASE_CLR
GR_BOX_PROFILE = (
    (GR_BOX_TOP_CHAMF * SQRT2, 45),
    GR_STR_H,
    (GR_BOX_CHAMF_H * SQRT2, 45),
)

# bin mating lip extrusion profile
GR_UNDER_H = 1.6
GR_TOPSIDE_H = 1.2
GR_LIP_PROFILE = (
    (GR_UNDER_H * SQRT2, 45),
    GR_TOPSIDE_H,
    (0.7 * SQRT2, -45),
    1.8,
    (1.3 * SQRT2, -45),
)
GR_LIP_H = 0
for h in GR_LIP_PROFILE:
    if isinstance(h, tuple):
        GR_LIP_H += h[0] / SQRT2
    else:
        GR_LIP_H += h
GR_NO_PROFILE = (GR_LIP_H,)

# bottom hole nominal dimensions
GR_HOLE_D = 6.5
GR_HOLE_H = 2.4
GR_BOLT_D = 3.0
GR_BOLT_H = 3.6 + GR_HOLE_H
GR_HOLE_DIST = 26 / 2
GR_HOLE_SLICE = 0.25
