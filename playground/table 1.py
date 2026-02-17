from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json
from mapplings.cleaners import MTCleaner, ParamCleaner

MTCleaner.global_debug_toggle(2)

run_time = 3600 * 5
debug = True

from_table = []
"""Row 1"""
## Basis 1 ##
til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_columns([4])

til2 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 0]), [])
ghost2 = til2.delete_columns([2])

avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)

try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_1.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 1 basis 1: {e}")

## Basis 2 ##

til3 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 0]), [])
ghost3 = til3.delete_columns([4])

til4 = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost4 = til4.delete_columns([2])

avoiding_parameters = [
    Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)

try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_2.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 1 basis 2: {e}")

"""Row 2"""
## Basis 1 ##
til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_columns([4])

til2 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 0]), [])
ghost2 = til2.delete_columns([4])

avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_3.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 2 basis 1: {e}")

## Basis 2 ##

til3 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 0]), [])
ghost3 = til3.delete_columns([2])

til4 = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost4 = til4.delete_columns([2])

avoiding_parameters = [
    Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_4.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
except Exception as e:
    print(f"Failed row 2 basis 2: {e}")
from_table.append(mappling)

"""Row 3"""
## Basis 1 ##
til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_columns([4])

til2 = MappedTiling.from_vincular_with_obs(CayleyPermutation([1, 2, 0]), [])
ghost2 = til2.delete_columns([4])

avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_5.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 3 basis 1: {e}")

## Basis 2 ##

til3 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 0]), [])
ghost3 = til2.delete_columns([4])

til4 = MappedTiling.from_vincular_with_obs(CayleyPermutation([1, 0, 2]), [])
ghost4 = til2.delete_columns([4])

avoiding_parameters = [
    Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_6.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 3 basis 2: {e}")

## Basis 3 ##
til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_columns([2])

til2 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 0, 1]), [])
ghost2 = til2.delete_columns([2])

avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_7.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 3 basis 3: {e}")

## Basis 4 ##

til3 = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 0]), [])
ghost3 = til3.delete_columns([2])

til4 = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 2, 1]), [])
ghost4 = til4.delete_columns([2])

avoiding_parameters = [
    Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
try:
    pack = MappedTileScopePack.point_placement(mappling)
    searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
    spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
    spec.show()
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    with open("table_1_mappling_8.json", "w") as f:
        f.write(json_str)
    spec.get_genf()
    from_table.append(mappling)
except Exception as e:
    print(f"Failed row 3 basis 4: {e}")
