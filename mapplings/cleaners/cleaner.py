"""Module with the generic cleaner and register classes"""

from typing import TypeVar, Callable, Generic, Iterable
from time import time
from datetime import timedelta
from tabulate import tabulate

from comb_spec_searcher.combinatorial_class import CombinatorialClass

T = TypeVar("T", bound=CombinatorialClass)
Cell = tuple[int, int]


class Register(Generic[T]):
    """Used within cleaners to register core functions.
    Initialize with a string to determine the name of the index attribute added to functions.
    Initialize with flag_name = bool to make flag_name an attribute of all registered functions.
    """

    def __init__(self, **additional_flags: bool):
        self.registered_functions: set[Callable[[T], T]] = set()
        self.map: dict[int, Callable[[T], T]] = {}
        self.flags = dict(additional_flags)

    def __call__(
        self,
        idx: int,
        update_register: bool = True,
        log_id: str | None = None,
        **flag_updates: bool,
    ) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
        """Used as the decorator to register functions.
        Setting update_register to False doesn't add the function to registered functions
        Flag updates will overwrite the register's default flag states."""

        def register_function(func: Callable[[T], T]) -> Callable[[T], T]:
            assert not hasattr(
                func, "index"
            ), f"{func.__name__} already has index attribute."
            if log_id is None:
                setattr(func, "log_id", func.__name__.replace("_", " ").title())
            else:
                setattr(func, "log_id", log_id)
            if update_register:
                self.add_to_register(func, idx)
            setattr(func, "index", idx)
            self.map[idx] = func

            return self.set_flags(func, flag_updates)

        return register_function

    def add_to_register(self, func: Callable[[T], T], idx: int) -> None:
        """Used to add functions to the register"""
        assert idx not in self.map, (
            f"Index {idx} is already assigned to {self[idx].__qualname__} "
            + f"and cannot be assigned to {func.__qualname__}"
        )
        self.registered_functions.add(func)

    def set_flags(self, func: Callable[[T], T], flag_updates: dict[str, bool]):
        """Adds all registered flags as attributes to func.
        Default flag values are overwritten by flag updates."""
        known_flags = tuple(self.flags.keys())
        adjusted_dict = self.flags.copy()
        for key, value in flag_updates.items():
            assert key in known_flags, (
                f"Unknown Flag : {key} \n."
                + f"{func.__qualname__} can be registered with the following flags : {known_flags}"
            )
            adjusted_dict[key] = value
        func.__dict__.update(adjusted_dict)
        return func

    def sorting_key(self, func: Callable[[T], T]) -> int:
        """Used to sort fuctions in cleaners"""
        assert hasattr(func, "index"), f"{func.__qualname__} has no assigned index"
        return getattr(func, "index")

    def __getitem__(self, key: int) -> Callable[[T], T]:
        return self.map[key]

    def __repr__(self):
        output = f"{self.__class__.__name__}("
        for key, value in self.flags.items():
            output += f", {key}={value}"
        return output + ")"

    def __str__(self):
        funcs = sorted(self.registered_functions, key=self.sorting_key)
        output = f"{funcs[0].__qualname__.split('.')[0]} has registered the following functions:"
        for func in funcs:
            output += f"\n{getattr(func, "index")} : {func.__name__}"
            for key, value in tuple(func.__dict__.items())[1:]:
                output += f"\n    -{key}={value}"
            output += "\n"
        return output


class GenericCleaner(Generic[T]):
    """A class for cleaning combinatorial objects.
    Core fuctions are decorated with @reg(index)
    where index is the order of cleaning
    DEBUG = 0 skips any debugging
    DEBUG = 1 checks counts and elapsed time after loop cleaning
    DEBUG = 2 checks counts and elapsed time after each function
    LOG = 0 Skips logging
    LOG = 1 Enables a global log
    LOG = 2 Enables a detailed log
    """

    DEBUG = 0
    LOG = 0
    reg = Register[T]()
    _currently_tracking = "Unspecified"
    _unnamed = 0
    log_tracker = {
        "Global Tracker": {
            getattr(func, "log_id"): {"Attempts": 0, "Successes": 0, "Time Spent": 0.0}
            for func in reg.registered_functions
        }
    }

    def __init__(
        self, todo_list: Iterable[Callable[[T], T]], tracker_id: str = "Unnamed"
    ):
        self.todo_list: tuple[Callable[[T], T], ...] = tuple(
            sorted(todo_list, key=self.__class__.reg.sorting_key)
        )
        if tracker_id == "Unnamed":
            self.id = f"Unnamed {self.__class__.__name__} {self.__class__._unnamed}"
            self.__class__._unnamed += 1
        else:
            self.id = tracker_id

        if self.__class__.LOG >= 2 and self.id not in self.__class__.log_tracker.keys():
            self.__class__.log_tracker[self.id] = {
                getattr(func, "log_id"): {
                    "Attempts": 0,
                    "Successes": 0,
                    "Time Spent": 0.0,
                }
                for func in self.todo_list
            }
        super().__init__()

    def __call__(self, cleaning_object: T) -> T:
        """Cleans the input cleaning_object according to the cleaner's todo_list"""
        self.__class__._currently_tracking = self.id
        new_object = self.__class__.loop_cleanup(cleaning_object, self.todo_list)
        self.__class__._currently_tracking = "Unspecified"
        return new_object

    def __repr__(self):
        return self.__class__.__name__ + f"({self.todo_list},{self.id})"

    def __str__(self):
        functions = dict(
            (self.reg.sorting_key(func), getattr(func, "log_id"))
            for func in self.todo_list
        )
        return self.__class__.__name__ + f"({functions}, {self.id})"

    def __iter__(self):
        return iter(sorted(self.todo_list, key=self.reg.sorting_key))

    @classmethod
    def loop_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Cleans the cleaning object according to the cleaning functions."""
        iterations = -1
        start_time = time()
        new_cleaning_object = cleaning_object
        continue_cleaning = True
        while continue_cleaning:
            iterations += 1
            old_cleaning_object = new_cleaning_object
            new_cleaning_object = cls.list_cleanup(old_cleaning_object, cleaning_list)
            continue_cleaning = old_cleaning_object != new_cleaning_object
        if cls.DEBUG > 0:
            print(
                f"Cleaned in {iterations} loops. Elapsed time : {time() - start_time}"
            )
            if cls.DEBUG == 1:
                old_counts = cleaning_object.initial_conditions(2)
                new_counts = new_cleaning_object.initial_conditions(2)
                assert old_counts == new_counts, (
                    f"Counts differ:\nInitial counts: {old_counts}\nCleaned counts: {new_counts}"
                    + f"\n{cleaning_object}\n {new_cleaning_object}"
                    + f"\n{repr(cleaning_object)}"
                )

        return new_cleaning_object

    @classmethod
    def list_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Applies all functions in cleaning_list in order according to their index"""
        cleaning_list = sorted(cleaning_list, key=cls.reg.sorting_key)
        return cls.unordered_cleanup(cleaning_object, cleaning_list)

    @classmethod
    def unordered_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Applies all functions in cleaning_list without reordering"""
        new_cleaning_object = cleaning_object
        for func in cleaning_list:
            if not bool(new_cleaning_object):
                return new_cleaning_object
            new_cleaning_object = cls._debug(cls._log(func))(new_cleaning_object)
        return new_cleaning_object

    def tracked_cleanup(
        self, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Cleans cleaning_object according to the cleaning list,
        removes any completed cleaning functions from the cleaner's todo_list"""
        new_cleaning_object = self.list_cleanup(cleaning_object, cleaning_list)
        self.todo_list = tuple(set(self.todo_list) - set(cleaning_list))
        return new_cleaning_object

    @classmethod
    def make_full_cleaner(cls):
        """Returns an instance of a cleaner with all registered cleaning functions"""
        return cls(
            tuple(sorted(cls.reg.registered_functions, key=cls.reg.sorting_key)),
            "Full Cleaner",
        )

    @classmethod
    def full_cleanup(cls, cleaning_object: T) -> T:
        """Applies all cleanup functions."""
        return cls.make_full_cleaner()(cleaning_object)

    @classmethod
    def toggle_log(cls, level: int) -> None:
        """Using this to set LOG and reset debug tracker"""
        assert level in (0, 1, 2)
        print("toggle log")
        match level:
            case 0:
                print(f"{cls.__name__} Logging Dissabled")
            case 1:
                print(f"Logging {cls.__name__} Functions Globally")
            case 2:
                print(f"Logging {cls.__name__} Instances Seperately")
        cls.LOG = level
        cls.log_tracker = {
            "Global Tracker": {
                getattr(func, "log_id"): {
                    "Attempts": 0,
                    "Successes": 0,
                    "Time Spent": 0.0,
                }
                for func in cls.reg.registered_functions
            }
        }

    @classmethod
    def display_log(cls) -> str:
        """Returns a string to display cleaner log data"""
        print(cls.LOG)
        if cls.LOG == 1:
            data = {
                f"{cls.__name__} Global Data": cls.log_tracker["Global Tracker"]
            }.items()
        elif cls.LOG == 2:
            data = cls.log_tracker.items()
        else:
            return f"{cls.__name__} logging is disabled"
        all_tables = []
        headers = [
            "Attempts",
            "Successes",
            "Success\n Rate",
            "Time Spent",
            "Percent\n of Time",
        ]
        coalign = ("left", "right", "right", "right", "right", "right")
        rows = dict[str, float]()
        for key, value in data:
            temp_headers = [key] + headers
            total_time = sum(record["Time Spent"] for record in value.values())
            table = list[tuple[str, int, int, str, timedelta, str]]()
            for name, record in value.items():
                ftime = record["Time Spent"]
                rows.update(((name, ftime),))
                attempt = int(record["Attempts"])
                success = int(record["Successes"])
                table.append(
                    (
                        name,
                        attempt,
                        success,
                        f"{int((success / attempt) * 100)}%",
                        timedelta(seconds=int(ftime)),
                        f"{int((ftime / total_time) * 100)}%",
                    )
                )
            table.sort(key=lambda row: rows[row[0]], reverse=True)
            all_tables.append(
                tabulate(table, headers=temp_headers, colalign=coalign) + "\n"
            )
        return "    " + "\n".join(all_tables) + "\n"

    @classmethod
    def _log(cls, func: Callable[[T], T]):
        """Function used to log a function each time it is run"""
        if cls.DEBUG > 0:
            return func

        def wrapper(cleaning_object: T) -> T:
            start_time = time()
            new_object = func(cleaning_object)
            elapsed_time = time() - start_time
            changed = new_object != cleaning_object
            cls._update_log(func, elapsed_time, changed)
            return new_object

        return wrapper

    @classmethod
    def _update_log(cls, func: Callable[[T], T], time_spent: float, success: bool):
        """Function used to change log data"""
        log_id = getattr(func, "log_id")
        level = cls.LOG
        if level == 0:
            return
        if level > 0:
            cls.log_tracker["Global Tracker"][log_id]["Time Spent"] += round(
                time_spent, 4
            )
            cls.log_tracker["Global Tracker"][log_id]["Attempts"] += 1
            cls.log_tracker["Global Tracker"][log_id]["Successes"] += int(success)
        if level > 1:
            cls.log_tracker[cls._currently_tracking][log_id]["Time Spent"] += round(
                time_spent, 4
            )
            cls.log_tracker[cls._currently_tracking][log_id]["Attempts"] += 1
            cls.log_tracker[cls._currently_tracking][log_id]["Successes"] += int(
                success
            )

    @classmethod
    def _debug(cls, func: Callable[[T], T]):
        """Sets the debug behavior for cleaning functions."""
        if cls.DEBUG > 0:

            def wrapper(cleaning_object: T) -> T:
                start_time = time()
                new_object = func(cleaning_object)
                elapsed_time = time() - start_time
                changed = new_object != cleaning_object
                cls._update_log(func, elapsed_time, changed)
                if changed:
                    if cls.DEBUG > 1:

                        print(
                            f"++ {cls.__name__}.{func.__name__} elapsed time : {elapsed_time} ++"
                        )
                        old_counts = cleaning_object.initial_conditions(2)
                        new_counts = new_object.initial_conditions(2)
                        assert old_counts == new_counts, (
                            f"Counts differ after {cls.__name__}.{func.__name__}:"
                            + f"\nInitial counts: {old_counts}\nClean counts: {new_counts}"
                            + f"\n {cleaning_object}\n {new_object}"
                            + f"\n {repr(cleaning_object)}"
                        )
                elif cls.DEBUG > 1:
                    print(
                        f"-- {cls.__name__}.{func.__name__} elapsed time : {elapsed_time} --"
                    )
                return new_object

            return wrapper
        return func
