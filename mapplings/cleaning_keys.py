"""These give names to the cleaning_function_map keys so they show up for autocomplete
The value assigned to each dictates the order in which the associated function will be applied
Function maps are defined beneath each cleaner class"""

from typing import Callable, TypeVar

# Mappling Cleaner Keys
# Prefix with mc_
MC_KILL = 0
MC_TIDY = 1
MC_INSERT_AVOIDERS = 2
MC_BACKMAP = 4
MC_REAP = 3
MC_EMPTY = 5
MC_PARAMS = 6
MC_FACTOR_CONTAINERS = 7
MC_REDUNDANT = 8
MC_FULL = -1  # Flags a full cleanup

# Parameter Cleaner keys
# Prefix with pc_
PC_FUSION = 3
PC_EMPTY = 1
PC_BLANK = 0
PC_UNPLACEMENT = 2
PC_FULL = -1  # Flags a full cleanup

T = TypeVar("T")


def make_register(
    function_map: dict[int, Callable[[T], T]],
) -> Callable[[int], Callable[[Callable[[T], T]], Callable[[T], T]]]:
    """Makes a decorator that adds decorated functions to a function map according to an index"""

    def register(index: int) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
        def get_func(func: Callable[[T], T]) -> Callable[[T], T]:
            function_map[index] = func
            return func

        return get_func

    return register
