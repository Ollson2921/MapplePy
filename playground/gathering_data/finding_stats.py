from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json
from mapplings.cleaners import MTCleaner
from datetime import timedelta
import time
import requests

MTCleaner.global_log_toggle(2)

from playground.table1 import from_table
from all_tilings import all_other_mapplings, L_classes

group_name = "from_table"
all_to_run = from_table

successes = []
data_string = ""

mappling_types = ["motzkin", "inc_inc", "hare_2_stack", "ten_point_one"]
mappling_types = ["L0", "L1", "L3", "L4", "L5", "L7"]
mappling_types = [n for n in range(1, len(all_to_run) + 1)]

webhookurl = "https://discord.com/api/webhooks/1446479214629883997/Ct682I4szno9aF4mpskSHVoeCpXA37IfWddC1SVycmI-CY"

count = 0
for mappling in all_to_run:
    success = False
    count += 1
    print(f"Starting mappling {count}/{len(all_to_run)}")
    print(f"Successes so far: {sum(successes)}/{len(successes)}")
    try:
        start_time = time.time()
        pack = MappedTileScopePack.point_placement(mappling)
        searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

        spec = searcher.auto_search(
            status_update=3600, max_expansion_time=36000
        )  # 10hrs
        success = True
        time_taken = timedelta(seconds=int(time.time() - start_time))
        print("Time taken:", time_taken)
        time_taken_str = f"\nTotal time accounted for: {time_taken}\n"
        # spec.show()
        data_string += "Mappling " + str(count) + " point placement: " + time_taken_str
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string = f"{group_name}_{count}_point_place"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        headers = {"User-Agent": "hildur", "Content-Type": "application/json"}
        message = (
            "Spec for mappling "
            + f"{mappling_types[count - 1]} with "
            + " point placement in "
            + str(time_taken)
        )
        data = json.dumps({"content": message})
        requests.post(webhookurl, headers=headers, data=data)

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
        time_taken = timedelta(seconds=int(time.time() - start_time))
        time_taken_str = f"\nTotal time accounted for: {time_taken}\n"
        print("Time taken:", time_taken)
        data_string += (
            "Mappling " + str(count) + " row and col placement: " + time_taken_str
        )
        # spec.show()
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string = f"{group_name}_{count}_row_and_col.json"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        headers = {"User-Agent": "hildur", "Content-Type": "application/json"}
        message = (
            "Spec for mappling "
            + f"{mappling_types[count - 1]} with "
            + " row and col placement in "
            + str(time_taken)
        )
        data = json.dumps({"content": message})
        requests.post(webhookurl, headers=headers, data=data)

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

print(data_string)
print("Successes:", successes)
