from itertools import combinations
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json
from mapplings.cleaners import MTCleaner, ParamCleaner

MTCleaner.global_log_toggle(1)
MTCleaner.global_tracker.log_level = 2
ParamCleaner.global_log_toggle(1)
ParamCleaner.global_tracker.log_level = 2

from_table = []
failures = []
run_time = 3600 * 0.1
debug = False

all_patterns = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
all_params = dict[str, Parameter]()
for pat in all_patterns:
    temp = list(map(str, pat))
    temp.insert(2, "-")
    all_params["".join(temp)] = Parameter.make_vincular(pat, [1])
    temp = list(map(str, pat))
    temp.insert(1, "-")
    all_params["".join(temp)] = Parameter.make_vincular(pat, [2])

cleaner = MTCleaner.make_full_cleaner("Initial Cleanup")
base = Tiling([GriddedCayleyPerm((0, 0), ((0, 0), (0, 0)))], [], (1, 1))

for key1, key2 in combinations(all_params.keys(), 2):
    p1, p2 = all_params[key1], all_params[key2]
    mappling = cleaner(MappedTiling(base, [p1, p2], [], []))
    try:
        pack = MappedTileScopePack.point_placement(mappling)
        searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=debug)
        spec = searcher.auto_search(status_update=30, max_expansion_time=run_time)
        spec.show()
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        with open(f"Av({key1})_Av({key2}).json", "w") as f:
            f.write(json_str)
        spec.get_genf()
        from_table.append(mappling)
    except Exception as e:
        print(f"Av({key1}), Av({key2}): {e}")
        failures.append(f"Av({key1}), Av({key2}): {e}")

print("Failures:")
for failure in failures:
    print(" " * 6, failure)
