from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json
from mapplings.cleaners import MTCleaner
from datetime import timedelta
import time
import requests
from cayley_permutations import CayleyPermutation

MTCleaner.global_log_toggle(2)

from playground.table1 import from_table
from all_tilings import all_other_mapplings, L_classes

all_to_run = L_classes

mappling_types = ["motzkin", "inc_inc", "hare_2_stack", "ten_point_one"]
mappling_types = ["L0", "L1", "L3", "L4", "L5", "L7"]
# mappling_types = [
#     f"vincular_from_table_1,_basis_{i}" for i in range(1, len(all_to_run) + 1)
# ]

n = 6  # how far to check counts
time_to_run = 7200  # max time to run each search (in seconds)

successes = []
failures = []


count = 0
for mappling in all_to_run:
    success_pp = False
    success_rc = False
    finished_pp_checks = False
    finished_rc_checks = False
    count += 1
    message = f"mappling {mappling_types[count - 1]} \n```{str(mappling)}```"
    print(f"Starting mappling {count}/{len(all_to_run)}")
    print(f"Successes so far: {sum(successes)}/{len(successes)}")
    mappling_counts = []
    try:
        # Try find a spec with point placement
        message1 = ""
        start_time = time.time()
        pack = MappedTileScopePack.point_placement(mappling)
        searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
        spec = searcher.auto_search(
            status_update=3600, max_expansion_time=time_to_run
        )  # 10hrs

        # check time taken and mark success
        success_pp = True
        time_taken = timedelta(seconds=int(time.time() - start_time))
        # spec.show()
        message1 += f"\npack: point_placement \nTime taken: {time_taken}"

        # Save spec
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string = f"{mappling_types[count - 1]}_point_place"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        # print("Sanity checking spec...")
        # spec.sanity_check()
        # message1 += "\nSpec passes sanity check"

        # Expand verified
        to_expand = []
        for comb_class in spec.comb_classes():
            if (
                not comb_class.has_parameters()
                or comb_class.tiling.is_vertical_insertion_encodable()
                or comb_class.tiling.is_horizontal_insertion_encodable()
            ):
                to_expand.append(comb_class)
        start_time = time.time()
        pack = MappedTileScopePack.no_ver_point_placement()
        new_spec = spec.expand_comb_classes(
            to_expand,
            pack,
            continue_expanding_verified=False,
            reverse=True,
            max_expansion_time=time_to_run,
        )
        time_taken = timedelta(seconds=int(time.time() - start_time))

        # save expanded spec
        json_dict = new_spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string += "_expanded"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        message1 += f"\nFound expanded spec, took {str(time_taken)}"

        # Sanity check expanded spec
        print("Checking sanity of expanded spec...")
        new_spec.sanity_check()

        # Check counts match
        print("Checking counts...")
        spec_counts = [new_spec.count_objects_of_size(n) for n in range(n)]
        mappling_counts = [mappling.get_terms(i).total() for i in range(n)]
        # mappling_counts = []
        # for i in range(n):
        #     for cperm in CayleyPermutation.of_size(i):
        #         if mappling.tili
        print(f"Counts match up to size {n - 1}:", spec_counts == mappling_counts)
        print(spec_counts, "spec counts")
        print(mappling_counts, "mappling counts")
        if spec_counts == mappling_counts:
            checked_counts = "are the same"
            print("Same counts")
        else:
            checked_counts = "are different"
            print("Different counts")

        message1 += f"\nExpanded spec passes sanity check, counts {checked_counts} \n{str(spec_counts)} spec counts \n{str(mappling_counts)} mappling counts"

        finished_pp_checks = True

    except Exception as e:
        print(f"Failed with point placement \n{e}")

    try:
        # Try find a spec with row and col placement
        message2 = ""
        start_time = time.time()
        pack = MappedTileScopePack.row_and_col_placement(mappling)
        searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
        spec = searcher.auto_search(
            status_update=3600, max_expansion_time=time_to_run
        )  # 10hrs

        # check time taken and mark success
        success_rc = True
        time_taken = timedelta(seconds=int(time.time() - start_time))
        # spec.show()
        message2 += f"\npack: row_and_col_placement \nTime taken: {time_taken}"

        # Save spec
        json_dict = spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string = f"{mappling_types[count - 1]}_row_and_col"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        # print("Sanity checking spec...")
        # spec.sanity_check()
        # message2 += "\nSpec passes sanity check"

        # Try find an expanded spec with row_and_col_placement
        to_expand = []
        for comb_class in spec.comb_classes():
            if (
                not comb_class.has_parameters()
                or comb_class.tiling.is_vertical_insertion_encodable()
                or comb_class.tiling.is_horizontal_insertion_encodable()
            ):
                to_expand.append(comb_class)
        start_time = time.time()
        pack = MappedTileScopePack.no_ver_row_and_col_placement()
        new_spec = spec.expand_comb_classes(
            to_expand,
            pack,
            continue_expanding_verified=False,
            reverse=False,
            max_expansion_time=time_to_run,
        )
        time_taken = timedelta(seconds=int(time.time() - start_time))

        # save expanded spec
        json_dict = new_spec.to_jsonable()
        json_str = json.dumps(json_dict)
        string += "_expanded"
        with open(f"{string}.json", "w") as f:
            f.write(json_str)

        message2 += f"\nFound expanded spec, took {str(time_taken)}"

        # Sanity check expanded spec
        print("Checking sanity of expanded spec...")
        new_spec.sanity_check()

        # Check counts match
        print("Checking counts...")
        spec_counts = [new_spec.count_objects_of_size(n) for n in range(n)]
        if mappling_counts == []:
            mappling_counts = [mappling.get_terms(i).total() for i in range(n)]
        print(f"Counts match up to size {n - 1}:", spec_counts == mappling_counts)
        print(spec_counts, "spec counts")
        print(mappling_counts, "mappling counts")
        if spec_counts == mappling_counts:
            checked_counts = "are the same"
            print("Same counts")
        else:
            checked_counts = "are different"
            print("Different counts")

        message2 += f"\nExpanded spec passes sanity check, counts {checked_counts} \n{str(spec_counts)} spec counts \n{str(mappling_counts)} mappling counts"

        finished_rc_checks = True
    except Exception as e:
        print(f"Failed with row and col placement \n{e}")

    successes.append(int(success_pp) + int(success_rc))

    if success_pp or success_rc:
        # Send to discord
        webhookurl = "https://discord.com/api/webhooks/1446479214629883997/Ct682I4szno9aF4mpskSHVoeCpXA37IfWddC1SVycmI-CYbHmbrFsmQNhAxEC2yCu1mT"
        headers = {"User-Agent": "hildur", "Content-Type": "application/json"}
        message = "Spec for " + message
        if success_pp:
            if finished_pp_checks:
                message += "\nSucceeded with point placement" + message1
            else:
                message += "\nIncorrect spec found with point placement" + message1
        if success_rc:
            if finished_rc_checks:
                message += "\nSucceeded with row and col placement" + message2
            else:
                message += (
                    "\nIncorrect spec found with row and col placement" + message2
                )

        data = json.dumps({"content": message})
        requests.post(webhookurl, headers=headers, data=data)
        print(message)
    else:
        message = "No spec " + message
        print(message)
        failures.append(mappling_types[count - 1])

print("Successes:", successes)
print("Failures:", failures)
