"""Test the to_json and from_dict methods for Parameter,
ParameterList, MappedTiling and CombinatorialSpecification."""

import pytest
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies import MappedTileScopePack
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
    CombinatorialSpecification,
)
import json


@pytest.fixture
def avoiding_parameter():
    """The avoiding parameter for motzkin mappling."""
    til = Tiling.create_vincular_or_bivincular(CayleyPermutation([0, 1, 2]))
    ghost = til.delete_rows([4])
    param = Parameter(
        ghost, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(6)})
    )
    return param


@pytest.fixture
def motzkin_mappling(avoiding_parameter):
    """The mappling for the motzkin class."""
    avoiding_parameters = [avoiding_parameter]
    mappling = MappedTiling(
        Tiling(
            [
                GriddedCayleyPerm(
                    CayleyPermutation([0, 2, 1]), ((0, 0), (0, 0), (0, 0))
                ),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), [(0, 0), (0, 0)]),
            ],
            [],
            (1, 1),
        ),
        avoiding_parameters,
        [],
        [],
    )
    return mappling


@pytest.fixture
def containing_param():
    """Containing parameter for inc inc mappling."""
    param = Parameter(
        Tiling(
            [
                GriddedCayleyPerm((1, 0), ((0, 0), (0, 0))),
                GriddedCayleyPerm((1, 0), ((1, 0), (1, 0))),
            ],
            [],
            (2, 1),
        ),
        RowColMap({0: 0, 1: 0}, {0: 0}),
    )
    return param


@pytest.fixture
def inc_inc_mappling(containing_param):
    """The mappling for the inc inc grid class."""
    mappling = MappedTiling(
        Tiling([], [], (1, 1)),
        avoiding_parameters=[],
        containing_parameters=[ParameterList([containing_param])],
        enumerating_parameters=[],
    )
    return mappling


def test_classes_jsons(
    motzkin_mappling, inc_inc_mappling, containing_param, avoiding_parameter
):
    """Test json for various classes:
    - parameters
    - parameter lists
    - mapplings"""
    assert containing_param == Parameter.from_dict(
        json.loads(json.dumps(containing_param.to_jsonable()))
    )
    assert avoiding_parameter == Parameter.from_dict(
        json.loads(json.dumps(avoiding_parameter.to_jsonable()))
    )
    assert ParameterList([containing_param]) == ParameterList.from_dict(
        json.loads(json.dumps(ParameterList([containing_param]).to_jsonable()))
    )
    assert motzkin_mappling.avoiding_parameters == ParameterList.from_dict(
        json.loads(json.dumps(motzkin_mappling.avoiding_parameters.to_jsonable()))
    )
    for param_list in inc_inc_mappling.containing_parameters:
        param_to_dict = json.dumps(param_list.to_jsonable())
        assert param_list == ParameterList.from_dict(json.loads(param_to_dict))
    assert motzkin_mappling == MappedTiling.from_dict(
        json.loads(json.dumps(motzkin_mappling.to_jsonable()))
    )
    assert inc_inc_mappling == MappedTiling.from_dict(
        json.loads(json.dumps(inc_inc_mappling.to_jsonable()))
    )


def test_motzkin_spec(motzkin_mappling):
    """Test the json and counts for the motzkin spec."""
    pack = MappedTileScopePack.point_placement(motzkin_mappling)
    searcher = CombinatorialSpecificationSearcher(motzkin_mappling, pack, debug=False)
    spec = searcher.auto_search()
    spec_counts = [spec.count_objects_of_size(i) for i in range(9)]
    assert spec_counts == [1, 1, 2, 4, 9, 21, 51, 127, 323]
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    load_dict = json.loads(json_str)
    reloaded_spec = CombinatorialSpecification.from_dict(load_dict)
    assert spec == reloaded_spec
    spec_counts = [spec.count_objects_of_size(i) for i in range(9)]
    assert spec_counts == [1, 1, 2, 4, 9, 21, 51, 127, 323]


def test_inc_inc_spec(inc_inc_mappling):
    """Test the json for the inc inc grid class spec."""
    pack = MappedTileScopePack.point_placement(inc_inc_mappling)
    searcher = CombinatorialSpecificationSearcher(inc_inc_mappling, pack, debug=False)
    spec = searcher.auto_search()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    load_dict = json.loads(json_str)
    reloaded_spec = CombinatorialSpecification.from_dict(load_dict)
    assert spec == reloaded_spec
    # Now test counts and expanded spec
    expanded_spec = spec.expand_verified()
    spec_counts = [expanded_spec.count_objects_of_size(i) for i in range(10)]
    assert spec_counts == [1, 1, 3, 12, 50, 200, 764, 2816, 10120, 35744]
    spec_to_dict = json.dumps(expanded_spec.to_jsonable())
    reloaded_expanded_spec = CombinatorialSpecification.from_dict(
        json.loads(spec_to_dict)
    )
    assert expanded_spec == reloaded_expanded_spec
    spec_counts = [reloaded_expanded_spec.count_objects_of_size(i) for i in range(10)]
    assert spec_counts == [1, 1, 3, 12, 50, 200, 764, 2816, 10120, 35744]
