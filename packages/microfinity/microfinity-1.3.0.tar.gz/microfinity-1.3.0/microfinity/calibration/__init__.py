"""Calibration tools for Gridfinity printer fit testing.

This subpackage provides tools for generating test prints to calibrate
your 3D printer settings for optimal Gridfinity fit:

- test_prints: Generate fractional pocket tests and clip clearance sweeps
"""

from .test_prints import (
    generate_fractional_pocket_test,
    generate_fractional_pocket_test_set,
    generate_clip_clearance_sweep,
    generate_clip_test_set,
    export_test_prints,
    DEFAULT_CLEARANCE_SWEEP,
)
