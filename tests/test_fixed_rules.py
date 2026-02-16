from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling, RowColMap
from cayley_permutations import CayleyPermutation
from mapplings.strategies.tilescope_strategies import (
    MapplingRequirementPlacementStrategy,
)
import pytest

mappling = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
        ),
        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),),
        (2, 3),
    ),
    ParameterList(frozenset()),
    (
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (),
                            (3, 2),
                        ),
                        RowColMap({0: 0, 1: 1, 2: 1}, {0: 1, 1: 2}),
                    )
                }
            )
        ),
    ),
    (),
)
req = (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),)
indices = (0,)
direction = 0
strategy = MapplingRequirementPlacementStrategy(req, indices, direction)
rule1 = strategy(mappling)


mappling2 = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
        ),
        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),),),
        (4, 3),
    ),
    ParameterList(frozenset()),
    (
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                                ),
                            ),
                            (),
                            (5, 3),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 1, 2: 1}),
                    )
                }
            )
        ),
    ),
    (),
)
reqs = (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),)
indices = (0,)
direction = 0

strategy = MapplingRequirementPlacementStrategy(reqs, indices, direction)
rule2 = strategy(mappling2)


rules = [rule1, rule2]


@pytest.mark.parametrize("rule", rules)
def test_rules(rule):
    print(rule)
    for i in range(5):
        assert rule.sanity_check(i)
