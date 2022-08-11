"""Tests for worlds"""
import importlib.util
import os
from pathlib import Path

import pytest

from pytiled_parser import OrderedPair, world

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"
WORLD_TESTS = TEST_DATA / "world_tests"

ALL_WORLD_TESTS = [
    WORLD_TESTS / "static_defined",
    WORLD_TESTS / "pattern_matched",
    WORLD_TESTS / "both",
]


def fix_world_map(world_map):
    world_map.coordinates = OrderedPair(
        round(world_map.coordinates[0], 3), round(world_map.coordinates[1], 3)
    )


def fix_world(world):
    for world_map in world.maps:
        fix_world_map(world_map)

@pytest.mark.parametrize("world_test", ALL_WORLD_TESTS)
def test_world_integration(world_test):
    # it's a PITA to import like this, don't do it
    # https://stackoverflow.com/a/67692/1342874
    spec = importlib.util.spec_from_file_location(
        "expected", world_test / "expected.py"
    )
    expected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected)

    raw_world_path = world_test / "world.world"

    casted_world = world.parse_world(raw_world_path)
    fix_world(casted_world)

    assert casted_world == expected.EXPECTED
