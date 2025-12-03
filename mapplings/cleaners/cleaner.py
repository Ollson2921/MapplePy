"""Module with the generic cleaner and register classes"""

from typing import TypeVar, Callable, Generic, Iterable
from time import time
from datetime import timedelta
from tabulate import tabulate, SEPARATING_LINE

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
            output += f"\n{getattr(func, 'index')} : {func.__name__}"
            for key, value in tuple(func.__dict__.items())[1:]:
                output += f"\n    -{key}={value}"
            output += "\n"
        return output


class CleanerLog(Generic[T]):
    """A class for tracking cleaners"""

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        logged_functions: Iterable[Callable[[T], T]],
        log_level: int = 0,
        debug_level: int = 0,
        name: str = "Unspecified",
    ):
        self.name = name
        self.log_level = log_level
        self.debug_level = debug_level
        self.functions = logged_functions
        self.tracker = {
            getattr(func, "log_id"): {
                "Attempts": 0,
                "Successes": 0,
                "Success Time": 0.0,
                "Fail Time": 0.0,
            }
            for func in self.functions
        }
        self.global_tracker: "CleanerLog" | None = None
        self.total_times = [0.0, 0.0]
        self.runs = 0
        self.changes_made = 0

    def __call__(self, func: Callable[[T], T]):
        return self._debug(self._log(func))

    def add_function(self, func: Callable[[T], T]):
        """Adds a function to the tracker"""
        self.tracker.update(
            {
                getattr(func, "log_id"): {
                    "Attempts": 0,
                    "Successes": 0,
                    "Success Time": 0.0,
                    "Fail Time": 0.0,
                }
            }
        )

    def reset_log(self) -> dict[str, dict[str, int | float]]:
        """Using this to set LOG and reset debug tracker"""
        return {
            getattr(func, "log_id"): {
                "Attempts": 0,
                "Successes": 0,
                "Success Time": 0.0,
                "Fail Time": 0.0,
            }
            for func in self.functions
        }

    def wrap_functions(
        self, functions: Iterable[Callable[[T], T]]
    ) -> Iterable[Callable[[T], T]]:
        """Applies the debug and log wrappers to each function"""
        return (self._debug(self._log(func)) for func in functions)

    def display(self) -> str:
        """Returns a string to display cleaner log data"""
        # pylint: disable=too-many-locals
        if self.log_level == 0:
            return f"\n{self.name} logging is disabled \n"
        headers = [
            "",
            "\nAttempts",
            "\nSuccesses",
            "Success\n Rate",
            "Time Spent\n on Successes",
            "Time Spent\n on Failures",
            "Total\nElapsed Time",
            "Percent of\n Total Time",
        ]
        coalign = (
            "left",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
        )
        table = list[tuple[str, int, int, str, timedelta, timedelta, timedelta, str]]()
        rows = dict[str, float]()
        total_attempt = 0
        total_success = 0
        total_time = sum(self.total_times)
        if self.global_tracker is None:
            time_ratio = 100.0
        else:
            global_time = sum(self.global_tracker.total_times)
            if global_time == 0:
                time_ratio = 100.0
            else:
                time_ratio = total_time / global_time * 100
        for name, record in self.tracker.items():
            ftime = record["Success Time"] + record["Fail Time"]
            rows.update(((f"    {name}", ftime),))
            attempt = int(record["Attempts"])
            success = int(record["Successes"])
            total_attempt += attempt
            total_success += success
            if self.log_level > 1:
                if total_time == 0:
                    ftime_ratio = 0
                else:
                    ftime_ratio = int((ftime / total_time) * 100)
                table.append(
                    (
                        f"    {name}",
                        attempt,
                        success,
                        f"{int((success / (max(attempt, attempt == 0))) * 100)}%",
                        timedelta(seconds=int(record["Success Time"])),
                        timedelta(seconds=int(record["Fail Time"])),
                        timedelta(seconds=int(ftime)),
                        f"{ftime_ratio}%",
                    )
                )
        table.sort(key=lambda row: rows[row[0]], reverse=True)
        if total_attempt == 0:
            attempt_ratio = 0.0
        else:
            attempt_ratio = (total_success / total_attempt) * 100
        table = [
            (
                self.name,
                self.runs,
                self.changes_made,
                f"{int(attempt_ratio)}%",
                timedelta(seconds=int(self.total_times[1])),
                timedelta(seconds=int(self.total_times[0])),
                timedelta(seconds=int(total_time)),
                f"{int(time_ratio)}%",
            ),
            SEPARATING_LINE,
        ] + table

        return "\n" + tabulate(table, headers=headers, colalign=coalign)

    def _log(self, func: Callable[[T], T]):
        """Function used to log a function each time it is run"""
        if self.debug_level > 0 or self.log_level == 0:
            return func

        def wrapper(cleaning_object: T) -> T:
            start_time = time()
            new_object = func(cleaning_object)
            elapsed_time = time() - start_time
            changed = new_object != cleaning_object
            self._update_log(func, elapsed_time, changed)
            return new_object

        return wrapper

    def _update_log(self, func: Callable[[T], T], time_spent: float, success: bool):
        """Function used to change log data"""
        log_id = getattr(func, "log_id")

        if success:
            key = "Success Time"
        else:
            key = "Fail Time"
        if self.global_tracker is not None:
            if self.global_tracker.log_level > 0:
                if log_id not in self.global_tracker.tracker:
                    self.global_tracker.add_function(func)
                self.global_tracker.tracker[log_id][key] += round(time_spent, 4)
                self.global_tracker.tracker[log_id]["Attempts"] += 1
                self.global_tracker.tracker[log_id]["Successes"] += int(success)
            self.global_tracker.total_times[success] += time_spent
        if self.log_level > 0:
            if log_id not in self.tracker:
                self.add_function(func)
            self.tracker[log_id][key] += round(time_spent, 4)
            self.tracker[log_id]["Attempts"] += 1
            self.tracker[log_id]["Successes"] += int(success)
            self.total_times[success] += time_spent

    def _debug(self, func: Callable[[T], T]):
        """Sets the debug behavior for cleaning functions."""
        if self.debug_level > 0:

            def wrapper(cleaning_object: T) -> T:
                start_time = time()
                new_object = func(cleaning_object)
                elapsed_time = time() - start_time
                changed = new_object != cleaning_object
                self._update_log(func, elapsed_time, changed)
                if changed:
                    if self.debug_level > 1:
                        old_counts = cleaning_object.initial_conditions(2)
                        new_counts = new_object.initial_conditions(2)
                        assert old_counts == new_counts, (
                            f"Counts differ after {self.name}.{func.__name__}:"
                            + f"\nInitial counts: {old_counts}\nClean counts: {new_counts}"
                            + f"\n {cleaning_object}\n {new_object}"
                            + f"\n {repr(cleaning_object)}"
                        )
                        print(
                            f"++ {self.name}.{func.__name__} elapsed time : {elapsed_time} ++"
                        )
                elif self.debug_level > 1:
                    print(
                        f"-- {self.name}.{func.__name__} elapsed time : {elapsed_time} --"
                    )
                return new_object

            return wrapper
        return func


class GenericCleaner(Generic[T]):
    """A class for cleaning combinatorial objects.
    Core fuctions are decorated with @reg(index)
    where index is the order of cleaning

    DEBUG = 0 skips any debugging
    DEBUG = 1 checks counts and elapsed time after loop cleaning
    DEBUG = 2 checks counts and elapsed time after each function

    LOG = 0 Skips logging
    LOG = 1 Displays info per cleaner instance
    LOG = 2 Displays info per function per cleaner instance

    DEBUG and LOG can be changed globally with global toggle functions
    or per instance with cleaner_instance.LOG = # or cleaner_instance.DEBUG = #
    """

    DEBUG = 0
    LOG = 0
    reg = Register[T]()
    _unnamed = 0
    global_tracker = CleanerLog[T](
        set(reg.registered_functions), LOG, DEBUG, "Global Tracker"
    )
    all_loggers = set[CleanerLog]()
    _currently_tracking = global_tracker

    def __init__(
        self, todo_list: Iterable[Callable[[T], T]], tracker_id: str = "Unnamed"
    ):

        if tracker_id == "Unnamed":
            self.id = f"Unnamed {self.__class__.__name__} {self.__class__._unnamed}"
            self.__class__._unnamed += 1
        else:
            self.id = tracker_id
        self.logger = CleanerLog[T](
            todo_list, self.__class__.LOG, self.__class__.DEBUG, self.id
        )
        self.logger.global_tracker = self.__class__.global_tracker
        self.todo_list: tuple[Callable[[T], T], ...] = tuple(
            sorted(todo_list, key=self.__class__.reg.sorting_key)
        )
        self.__class__.all_loggers.add(self.logger)
        super().__init__()

    def __call__(self, cleaning_object: T) -> T:
        """Cleans the input cleaning_object according to the cleaner's todo_list"""
        self.__class__._currently_tracking = self.logger
        new_object = self.__class__.loop_cleanup(cleaning_object, self.todo_list)
        self.__class__._currently_tracking = self.__class__.global_tracker
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

    def __setattr__(self, name, value):
        if name == "LOG":
            self.logger.log_level = value
        elif name == "DEBUG":
            self.logger.debug_level = value
        else:
            super().__setattr__(name, value)

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
        if cls.LOG > 0:
            cls._currently_tracking.runs += 1
            cls._currently_tracking.changes_made += int(iterations > 0)
            cls.global_tracker.runs += 1
            cls.global_tracker.changes_made += int(iterations > 0)
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
        log = cls._currently_tracking
        for func in cleaning_list:
            if not bool(new_cleaning_object):  # fix this
                return new_cleaning_object
            new_cleaning_object = log(func)(new_cleaning_object)
        return new_cleaning_object

    def tracked_cleanup(
        self, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:  # This function is currn
        """Cleans cleaning_object according to the cleaning list,
        removes any completed cleaning functions from the cleaner's todo_list"""
        new_cleaning_object = self.list_cleanup(cleaning_object, cleaning_list)
        self.todo_list = tuple(set(self.todo_list) - set(cleaning_list))
        return new_cleaning_object

    @classmethod
    def make_full_cleaner(cls, name: str = "Full Cleaner"):
        """Returns an instance of a cleaner with all registered cleaning functions"""
        return cls(
            tuple(sorted(cls.reg.registered_functions, key=cls.reg.sorting_key)),
            name,
        )

    @classmethod
    def full_cleanup(cls, cleaning_object: T) -> T:
        """Applies all cleanup functions."""
        return cls.make_full_cleaner()(cleaning_object)

    @classmethod
    def global_log_toggle(cls, level: int) -> None:
        """Updates the log level of all cleaner instances and resets tracking"""
        cls.LOG = level
        for logger in cls.all_loggers:
            logger.log_level = level
            logger.tracker = logger.reset_log()

    @classmethod
    def global_debug_toggle(cls, level: int) -> None:
        """Applies a debug level to all cleaner instances"""
        cls.DEBUG = level
        for logger in cls.all_loggers:
            logger.debug_level = level

    @classmethod
    def status_update(cls) -> str:
        """Gives the full status update for all cleaner instances"""
        logs = list(log for log in cls.all_loggers if log.log_level > 0)
        if not logs:
            return f"Logging dissabled for all {cls.__name__} cleaners.\n"
        logs.sort(key=lambda log: log.total_times, reverse=True)
        all_tables = (logger.display() for logger in logs)
        return f"{cls.__name__} Status:\n    " + "\n".join(all_tables) + "\n"
