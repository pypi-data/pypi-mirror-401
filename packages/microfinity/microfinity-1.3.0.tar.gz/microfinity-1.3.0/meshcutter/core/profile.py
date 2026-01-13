#! /usr/bin/env python3
#
# meshcutter.core.profile - Gridfinity profile definitions for chamfered cutters
#

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
from math import sqrt

import numpy as np


# Gridfinity profile constants (from microfinity/core/constants.py)
SQRT2 = sqrt(2)

GR_BASE_HEIGHT = 4.75  # Total base height (mm)
GR_STR_H = 1.8  # Straight vertical section height (mm)
GR_BASE_CLR = 0.25  # Clearance above nominal base height

# Baseplate profile chamfer dimensions
GR_BASE_CHAMF_H = 0.98994949 / SQRT2  # ~0.7mm bottom chamfer vertical height
GR_BASE_TOP_CHAMF = GR_BASE_HEIGHT - GR_BASE_CHAMF_H - GR_STR_H  # ~2.25mm top chamfer

# Box/bin base profile (slightly different dimensions)
GR_BOX_CHAMF_H = 1.1313708 / SQRT2  # ~0.8mm bottom chamfer vertical height
GR_BOX_TOP_CHAMF = GR_BASE_HEIGHT - GR_BOX_CHAMF_H - GR_STR_H + GR_BASE_CLR  # ~2.4mm


@dataclass
class ProfileSegment:
    """
    A single segment of the profile (from bottom to top).

    Attributes:
        z_start: Starting Z coordinate (from bottom = 0)
        z_end: Ending Z coordinate
        inset_start: Inset from polygon at z_start (mm)
        inset_end: Inset from polygon at z_end (mm)
    """

    z_start: float
    z_end: float
    inset_start: float
    inset_end: float

    @property
    def height(self) -> float:
        return self.z_end - self.z_start

    def inset_at(self, z: float) -> float:
        """Compute inset at a given Z within this segment."""
        if self.z_end == self.z_start:
            return self.inset_start
        t = (z - self.z_start) / (self.z_end - self.z_start)
        t = max(0.0, min(1.0, t))
        return self.inset_start + t * (self.inset_end - self.inset_start)


@dataclass
class CutterProfile:
    """
    A complete cutter profile definition.

    The profile defines how the cutter polygon is inset at different Z heights.
    This allows creating chamfered/stepped cutter geometry that matches
    Gridfinity base profiles.

    The profile is defined from Z=0 (bottom plane) upward into the part.
    At each Z level, the polygon is inset (buffered inward) by the specified amount.
    A 45-degree chamfer is achieved by linearly increasing inset with height.
    """

    name: str
    segments: List[ProfileSegment]

    @property
    def total_height(self) -> float:
        """Total height of the profile."""
        if not self.segments:
            return 0.0
        return self.segments[-1].z_end

    @property
    def max_inset(self) -> float:
        """Maximum inset in the profile."""
        if not self.segments:
            return 0.0
        return max(max(s.inset_start, s.inset_end) for s in self.segments)

    def inset_at(self, z: float) -> float:
        """
        Compute the inset at a given Z height.

        Args:
            z: Height from bottom plane (0 = bottom)

        Returns:
            Inset distance in mm (how much to buffer inward)
        """
        if z <= 0:
            return self.segments[0].inset_start if self.segments else 0.0

        for seg in self.segments:
            if seg.z_start <= z <= seg.z_end:
                return seg.inset_at(z)

        # Beyond profile, use max inset
        return self.max_inset

    def sample_z_levels(self, n_slices: int = 10, epsilon: float = 0.02) -> List[float]:
        """
        Generate Z levels for slab extrusion.

        Args:
            n_slices: Approximate number of slices
            epsilon: Penetration below Z=0 for coplanar avoidance

        Returns:
            List of Z values from -epsilon to total_height
        """
        if not self.segments:
            return [-epsilon, 0.0]

        # Include segment boundaries for accurate profile representation
        z_levels = set([-epsilon])
        for seg in self.segments:
            z_levels.add(seg.z_start)
            z_levels.add(seg.z_end)

        # Add intermediate points within each segment
        for seg in self.segments:
            if seg.height > 0:
                n_intermediate = max(1, int(n_slices * seg.height / self.total_height))
                for i in range(1, n_intermediate + 1):
                    z = seg.z_start + (seg.height * i / (n_intermediate + 1))
                    z_levels.add(z)

        return sorted(z_levels)


def create_rectangular_profile(depth: float) -> CutterProfile:
    """
    Create a simple rectangular (no chamfer) profile.

    Args:
        depth: Total depth of cut (mm)

    Returns:
        CutterProfile with no chamfers (constant zero inset)
    """
    return CutterProfile(
        name="rectangular",
        segments=[
            ProfileSegment(z_start=0.0, z_end=depth, inset_start=0.0, inset_end=0.0),
        ],
    )


def create_gridfinity_baseplate_profile(depth: float = GR_BASE_HEIGHT) -> CutterProfile:
    """
    Create a Gridfinity baseplate pocket profile.

    This profile matches the cavities in a Gridfinity baseplate that receive
    the bin feet. It has 45-degree chamfers at top and bottom with a straight
    section in between.

    Profile (from bottom, Z=0, upward into baseplate):
        - Bottom chamfer: 45° inward, ~0.7mm height
        - Straight section: constant inset, 1.8mm height
        - Top chamfer: 45° inward, ~2.25mm height

    Args:
        depth: Total depth (default: GR_BASE_HEIGHT = 4.75mm)

    Returns:
        CutterProfile for baseplate pockets
    """
    # Adjust heights if depth is different from standard
    scale = depth / GR_BASE_HEIGHT if depth != GR_BASE_HEIGHT else 1.0

    bottom_chamf_h = GR_BASE_CHAMF_H * scale
    straight_h = GR_STR_H * scale
    top_chamf_h = GR_BASE_TOP_CHAMF * scale

    # For 45-degree chamfers: inset = height (1:1 ratio)
    bottom_inset = bottom_chamf_h
    top_inset = bottom_inset + top_chamf_h

    z1 = bottom_chamf_h
    z2 = z1 + straight_h
    z3 = z2 + top_chamf_h

    return CutterProfile(
        name="gridfinity_baseplate",
        segments=[
            # Bottom chamfer: inset grows from 0 to bottom_inset
            ProfileSegment(z_start=0.0, z_end=z1, inset_start=0.0, inset_end=bottom_inset),
            # Straight section: constant inset
            ProfileSegment(z_start=z1, z_end=z2, inset_start=bottom_inset, inset_end=bottom_inset),
            # Top chamfer: inset grows from bottom_inset to top_inset
            ProfileSegment(z_start=z2, z_end=z3, inset_start=bottom_inset, inset_end=top_inset),
        ],
    )


def create_gridfinity_box_profile(depth: float = GR_BASE_HEIGHT) -> CutterProfile:
    """
    Create a Gridfinity box/bin foot profile.

    This profile matches the feet on Gridfinity bins that insert into
    baseplate pockets. Slightly different chamfer dimensions than baseplate.

    Args:
        depth: Total depth (default: GR_BASE_HEIGHT = 4.75mm)

    Returns:
        CutterProfile for bin feet
    """
    scale = depth / GR_BASE_HEIGHT if depth != GR_BASE_HEIGHT else 1.0

    bottom_chamf_h = GR_BOX_CHAMF_H * scale
    straight_h = GR_STR_H * scale
    top_chamf_h = GR_BOX_TOP_CHAMF * scale

    bottom_inset = bottom_chamf_h
    top_inset = bottom_inset + top_chamf_h

    z1 = bottom_chamf_h
    z2 = z1 + straight_h
    z3 = z2 + top_chamf_h

    return CutterProfile(
        name="gridfinity_box",
        segments=[
            ProfileSegment(z_start=0.0, z_end=z1, inset_start=0.0, inset_end=bottom_inset),
            ProfileSegment(z_start=z1, z_end=z2, inset_start=bottom_inset, inset_end=bottom_inset),
            ProfileSegment(z_start=z2, z_end=z3, inset_start=bottom_inset, inset_end=top_inset),
        ],
    )


# Pre-defined profiles
PROFILE_RECTANGULAR = "rect"
PROFILE_GRIDFINITY = "gridfinity"
PROFILE_GRIDFINITY_BOX = "gridfinity_box"


def get_profile(name: str, depth: float = GR_BASE_HEIGHT) -> CutterProfile:
    """
    Get a cutter profile by name.

    Args:
        name: Profile name ("rect", "gridfinity", "gridfinity_box")
        depth: Cut depth in mm

    Returns:
        CutterProfile instance

    Raises:
        ValueError: If profile name is unknown
    """
    if name == PROFILE_RECTANGULAR:
        return create_rectangular_profile(depth)
    elif name == PROFILE_GRIDFINITY:
        return create_gridfinity_baseplate_profile(depth)
    elif name == PROFILE_GRIDFINITY_BOX:
        return create_gridfinity_box_profile(depth)
    else:
        raise ValueError(f"Unknown profile: {name}. Valid options: rect, gridfinity, gridfinity_box")
