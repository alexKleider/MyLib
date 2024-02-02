#!/usr/bin/env python

# Wrong File Name: Mymath/Tests/test_volume_center.py

"""
This module got isolated from its "mymath" dependency
and was there for renamed pytest_volume_center.py
"""

# Must first add the parent directory of the
# currently running script to the system path:
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
# ... or alternatively set PYTHONPATH to project directory:
# export PYTHONPATH=/home/alex/Git/Mymath

import math
import pytest
import mymath

@pytest.mark.parametrize("length, d1, d2, expected", [
                        (21, 13.5, 16, 25),
                        ])
def test_volume(length, d1, d2, expected):
    assert math.isclose(mymath.volume(length, d1, d2), expected,
                        rel_tol=0.01)


@pytest.mark.parametrize("l, length, d1, d2, expected", [
                         (10, 20, 10, 12, 11)
                         ])
def test_get_diameter_at_l(l, length, d1, d2, expected):
    assert mymath.get_diameter_at_l(l, length, d1, d2) == expected


@pytest.mark.parametrize("length, d1, d2, expected", [
                        (21, 13.5, 16, 11.5),
                        ])
def test_volume_centre(length, d1, d2, expected):
    assert mymath.volume_centre(length, d1, d2) == expected



