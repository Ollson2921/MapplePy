from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json
from mapplings.cleaners import MTCleaner
from datetime import timedelta

MTCleaner.global_log_toggle(2)

from playground.table1 import from_table

successes = []
data_string = ""

count = 0
for mappling in from_table:
    success = False
    count += 1
    print(f"Starting mappling {count}/{len(from_table)}")
    print(f"Successes so far: {sum(successes)}/{len(successes)}")
    try:
        pack = MappedTileScopePack.point_placement(mappling)
        searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

        spec = searcher.auto_search(
            status_update=3600, max_expansion_time=36000
        )  # 10hrs
        success = True
        time_taken = timedelta(seconds=int(sum(spec.func_times.values())))
        time_taken_str = f"\nTotal time accounted for: {time_taken}\n"
        # spec.show()
        data_string += "Mappling " + str(count) + " point placement: " + time_taken_str
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string = f"table_1_{count}_point_place"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        new_spec = spec.expand_verified()
        # new_spec.show()

        json_dict = new_spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string += "_expanded"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)
    except Exception as e:
        print(f"Failed on mappling {count}: {e}")
    try:
        pack = MappedTileScopePack.row_and_col_placement(mappling)
        searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
        spec = searcher.auto_search(status_update=3600, max_expansion_time=36000)
        success = True
        time_taken = timedelta(seconds=int(sum(spec.func_times.values())))
        time_taken_str = f"\tTotal time accounted for: {time_taken}\n"
        data_string += "Mappling " + str(count) + " point placement: " + time_taken_str
        # spec.show()
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string = f"table_1_{count}_row_and_col.json"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        new_spec = spec.expand_verified()
        # new_spec.show()
        json_dict = new_spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string += "_expanded"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)
    except Exception as e:
        print(f"Failed on mappling {count}: {e}")
    successes.append(int(success))
print("Successes:", successes)
print(data_string)
