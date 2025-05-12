from typing import Callable, TypeVar

# These give names to the cleaning_function_map keys so they show up for autocomplete
# The value assigned to each dictates the order in which the associated function will be applied
# Function maps are defined beneath each cleaner class

# Mappling Cleaner Keys
# Prefix with mc_
mc_try_to_kill = 0
mc_tidy_containers = 1
mc_insert_avoiders = 2
mc_backmap = 4
mc_reap_contradictions = 3
mc_remove_empty = 5
mc_clean_params = 6
mc_factor_containers = 7
mc_redundancy_check = 8
mc_full = -1  # Flags a full cleanup

# Parameter Cleaner keys
# Prefix with pc_
pc_fusion = 3
pc_reduce_empty = 1
pc_remove_blank = 0
pc_unplace_points = 2
pc_full = -1  # Flags a full cleanup

T = TypeVar("T")


def make_register(
    function_map: dict[int, Callable[[T], T]],
) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
    """Makes a decorator that adds decorated functions to a function map according to an index"""

    def register(index: int) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
        def get_func(func: Callable[[T], T]) -> Callable[[T], T]:
            function_map[index] = func
            return func

        return get_func

    return register
