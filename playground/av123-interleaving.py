from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from mapplings import MappedTiling
from mapplings.strategies import MappedTileScopePack
from mapplings.strategies.factor import MapplingILFactorStrategy
from comb_spec_searcher import CombinatorialSpecificationSearcher
from comb_spec_searcher import AtomStrategy
from mapplings.cleaners import MTCleaner, ParamCleaner
from mapplings.tracked_tilescope import TrackedSearcher

# MTCleaner.global_debug_toggle(1)

obs = [
    GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 0), (0, 0))),
    GriddedCayleyPerm((0, 0), ((0, 0), (0, 0))),
]

mappling = MappedTiling(Tiling(obs, [], (1, 1)), [], [], [])

pack = MappedTileScopePack.point_placement(mappling)
pack = pack.add_initial(MapplingILFactorStrategy(ignore_parent=True), apply_first=True)
pack = pack.add_verification(AtomStrategy(), replace=True)

css = TrackedSearcher(mappling, pack, max_cvs=1, debug=True)
spec = css.auto_search(status_update=30)
spec.show(verbose=True)

# json_dict = {
#     "obstructions": [
#         {"pattern": {"cperm": [0]}, "positions": [[0, 0]]},
#         {"pattern": {"cperm": [0]}, "positions": [[0, 1]]},
#         {"pattern": {"cperm": [0]}, "positions": [[0, 2]]},
#         {"pattern": {"cperm": [0]}, "positions": [[1, 0]]},
#         {"pattern": {"cperm": [0]}, "positions": [[1, 2]]},
#         {"pattern": {"cperm": [0]}, "positions": [[1, 3]]},
#         {"pattern": {"cperm": [0]}, "positions": [[2, 1]]},
#         {"pattern": {"cperm": [0]}, "positions": [[2, 2]]},
#         {"pattern": {"cperm": [0]}, "positions": [[3, 0]]},
#         {"pattern": {"cperm": [0]}, "positions": [[3, 1]]},
#         {"pattern": {"cperm": [0]}, "positions": [[3, 3]]},
#         {"pattern": {"cperm": [0]}, "positions": [[4, 1]]},
#         {"pattern": {"cperm": [0]}, "positions": [[4, 2]]},
#         {"pattern": {"cperm": [0]}, "positions": [[4, 3]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[0, 3], [0, 3]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[0, 3], [2, 3]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[1, 1], [1, 1]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[2, 0], [2, 0]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[2, 0], [4, 0]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[2, 3], [2, 3]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[3, 2], [3, 2]]},
#         {"pattern": {"cperm": [0, 0]}, "positions": [[4, 0], [4, 0]]},
#         {"pattern": {"cperm": [0, 1]}, "positions": [[0, 3], [0, 3]]},
#         {"pattern": {"cperm": [0, 1]}, "positions": [[1, 1], [1, 1]]},
#         {"pattern": {"cperm": [0, 1]}, "positions": [[2, 0], [2, 0]]},
#         {"pattern": {"cperm": [0, 1]}, "positions": [[2, 3], [2, 3]]},
#         {"pattern": {"cperm": [0, 1]}, "positions": [[3, 2], [3, 2]]},
#         {"pattern": {"cperm": [1, 0]}, "positions": [[3, 2], [3, 2]]},
#         {"pattern": {"cperm": [0, 1, 2]}, "positions": [[2, 0], [4, 0], [4, 0]]},
#         {"pattern": {"cperm": [0, 1, 2]}, "positions": [[4, 0], [4, 0], [4, 0]]},
#     ],
#     "requirements": [[{"pattern": {"cperm": [0]}, "positions": [[3, 2]]}]],
#     "dimensions": [5, 4],
#     "class_module": "mapplings.mapped_tiling",
#     "comb_class": "MappedTiling",
#     "tiling": {
#         "obstructions": [
#             {"pattern": {"cperm": [0]}, "positions": [[0, 0]]},
#             {"pattern": {"cperm": [0]}, "positions": [[0, 1]]},
#             {"pattern": {"cperm": [0]}, "positions": [[0, 2]]},
#             {"pattern": {"cperm": [0]}, "positions": [[1, 0]]},
#             {"pattern": {"cperm": [0]}, "positions": [[1, 2]]},
#             {"pattern": {"cperm": [0]}, "positions": [[1, 3]]},
#             {"pattern": {"cperm": [0]}, "positions": [[2, 1]]},
#             {"pattern": {"cperm": [0]}, "positions": [[2, 2]]},
#             {"pattern": {"cperm": [0]}, "positions": [[3, 0]]},
#             {"pattern": {"cperm": [0]}, "positions": [[3, 1]]},
#             {"pattern": {"cperm": [0]}, "positions": [[3, 3]]},
#             {"pattern": {"cperm": [0]}, "positions": [[4, 1]]},
#             {"pattern": {"cperm": [0]}, "positions": [[4, 2]]},
#             {"pattern": {"cperm": [0]}, "positions": [[4, 3]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[0, 3], [0, 3]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[0, 3], [2, 3]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[1, 1], [1, 1]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[2, 0], [2, 0]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[2, 0], [4, 0]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[2, 3], [2, 3]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[3, 2], [3, 2]]},
#             {"pattern": {"cperm": [0, 0]}, "positions": [[4, 0], [4, 0]]},
#             {"pattern": {"cperm": [0, 1]}, "positions": [[0, 3], [0, 3]]},
#             {"pattern": {"cperm": [0, 1]}, "positions": [[1, 1], [1, 1]]},
#             {"pattern": {"cperm": [0, 1]}, "positions": [[2, 0], [2, 0]]},
#             {"pattern": {"cperm": [0, 1]}, "positions": [[2, 3], [2, 3]]},
#             {"pattern": {"cperm": [0, 1]}, "positions": [[3, 2], [3, 2]]},
#             {"pattern": {"cperm": [1, 0]}, "positions": [[3, 2], [3, 2]]},
#             {"pattern": {"cperm": [0, 1, 2]}, "positions": [[2, 0], [4, 0], [4, 0]]},
#             {"pattern": {"cperm": [0, 1, 2]}, "positions": [[4, 0], [4, 0], [4, 0]]},
#         ],
#         "requirements": [[{"pattern": {"cperm": [0]}, "positions": [[3, 2]]}]],
#         "dimensions": [5, 4],
#         "class_module": "gridded_cayley_permutations.tilings",
#         "comb_class": "Tiling",
#     },
#     "avoiding_parameters": [],
#     "containing_parameters": [],
#     "enumerating_parameters": [],
# }

# mappling = MappedTiling.from_dict(json_dict)
# print(mappling)


# rule = MapplingILFactorStrategy()(mappling)
# print(rule)
