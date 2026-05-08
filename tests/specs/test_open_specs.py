import json
from comb_spec_searcher import CombinatorialSpecification
from pathlib import Path

HERE = Path(__file__).parent


def test_open_4c_spec():
    """Opens an old spec and checks still loads. Then checks can find
    the correct generating function. Also checks can find the expanded
    spec from the unexpanded version."""

    with open(HERE / "Av(0-12)_Av(20-1)_point_place_expanded.json") as f:
        spec = CombinatorialSpecification.from_dict(json.load(f))
    gf = spec.get_genf()
    assert "(x - 1)/(2*x - 1)" == str(gf)

    with open(HERE / "Av(0-12)_Av(20-1)_point_place.json") as f:
        spec = CombinatorialSpecification.from_dict(json.load(f))
    gf = spec.get_genf()
    assert "(x - 1)/(2*x - 1)" == str(gf)


def test_open_5a_spec():
    """Opens an old spec and checks still loads. Then checks can find
    the correct generating function."""

    with open(HERE / "Av(1-20)_Av(21-0)_row_and_col_placement_expanded.json") as f:
        spec = CombinatorialSpecification.from_dict(json.load(f))
    gf = spec.get_genf()
    assert "(x - 1)/(2*x - 1)" == str(gf)
