"""Testing the dunder methods of MappedTiling."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
import pytest
from mapplings import MappedTiling, ParameterList


@pytest.fixture
def all_cperms_mappling():
    all_cperms_tiling = Tiling([], [], (1, 1))
    return MappedTiling(
        all_cperms_tiling, ParameterList([]), ParameterList([]), ParameterList([])
    )


@pytest.fixture
def empty_mappling():
    return MappedTiling(
        Tiling.empty_tiling(), ParameterList([]), ParameterList([]), ParameterList([])
    )


def test_repr(all_cperms_mappling, empty_mappling):
    assert all_cperms_mappling == eval(repr(all_cperms_mappling))
    assert empty_mappling == eval(repr(empty_mappling))
