from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling, RowColMap
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.cleaners import MTCleaner


def test_try_to_kill_in_cleaner():
    """Doesn't contain empty gcp, check still not contained after cleaning."""
    mt = MappedTiling(
        Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),), (), (1, 1)),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                            ),
                            (),
                            (1, 1),
                        ),
                        RowColMap({0: 0}, {0: 0}),
                    )
                }
            )
        ),
        (),
        (),
    )

    cleaned = MTCleaner.full_cleanup(mt)

    for i in range(4):
        assert mt.get_terms(i)[()] == cleaned.get_terms(i)[()]
