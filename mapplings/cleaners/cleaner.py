"""Module with the generic cleaner and register classes"""

from typing import TypeVar, Callable, Generic, Iterable, Any
from time import time

from comb_spec_searcher.combinatorial_class import CombinatorialClass

T = TypeVar("T", bound=CombinatorialClass)
Cell = tuple[int, int]


class Register(Generic[T]):
    """Used within cleaners to register core functions.
    Initialize with a string to determine the name of the index attribute added to functions.
    Initialize with flag_name = bool to make flag_name an attribute of all registered functions.
    """

    def __init__(self, attr_name: str = "index", **additional_flags: bool):
        self.registered_functions: set[Callable[[T], T]] = set()
        self.map: dict[int, Callable[[T], T]] = {}
        self.flags = dict(additional_flags)
        self.attr_name = attr_name

    def __call__(
        self, idx: int, update_register: bool = True, **flag_updates: bool
    ) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
        """Used as the decorator to register functions.
        Setting update_register to False doesn't add the function to registered functions
        Flag updates will overwrite the register's default flag states."""

        def register_function(func: Callable[[T], T]) -> Callable[[T], T]:
            if update_register:
                self.add_to_register(func, idx)
            setattr(func, self.attr_name, idx)
            return self.set_flags(func, flag_updates)

        return register_function

    def add_to_register(self, func: Callable[[T], T], idx: int) -> None:
        """Used to add functions to the register"""
        assert idx not in self.map, (
            f"{self.attr_name} {idx} is already assigned to {self[idx].__qualname__} "
            + f"and cannot be assigned to {func.__qualname__}"
        )
        self.registered_functions.add(func)
        self.map[idx] = func

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
        assert hasattr(
            func, self.attr_name
        ), f"{func.__qualname__} has no assigned {self.attr_name}"
        return getattr(func, self.attr_name)

    def __getitem__(self, key: int) -> Callable[[T], T]:
        return self.map[key]

    def __repr__(self):
        output = f"{self.__class__.__name__}(attr_name={self.attr_name}"
        for key, value in self.flags.items():
            output += f", {key}={value}"
        return output + ")"

    def __str__(self):
        funcs = sorted(self.registered_functions, key=self.sorting_key)
        output = f"{funcs[0].__qualname__.split('.')[0]} has registered the following functions:"
        for func in funcs:
            output += f"\n{getattr(func, self.attr_name)} : {func.__name__}"
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
    global_tracker = {
        func.__name__: {"Attempts": 0, "Successes": 0, "Time Spent": 0.0}
        for func in reg.registered_functions
    }
    _currently_tracking = "Unspecified"
    _unnamed = 0
    detailed_tracker = dict[str, dict[str, Any]]()

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

        if (
            self.__class__.LOG >= 2
            and self.id not in self.__class__.detailed_tracker.keys()
        ):
            self.__class__.detailed_tracker[self.id] = {
                func.__name__: {"Attempts": 0, "Successes": 0, "Time Spent": 0.0}
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
        return (
            self.__class__.__name__
            + f"({dict((self.reg.sorting_key(func) , func.__name__) for func in self.todo_list)})"
        )

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
        cls.global_tracker = {
            func.__name__: {"Attempts": 0, "Successes": 0, "Time Spent": 0.0}
            for func in cls.reg.registered_functions
        }
        cls.detailed_tracker = {"Unspecified": cls.global_tracker}

    @classmethod
    def display_log(cls) -> str:
        """Returns a string to display cleaner log data"""
        if cls.LOG == 0:
            return f"{cls.__name__} logging is disabled"

        if cls.LOG == 1:
            data = {"Global Cleaner Data": cls.global_tracker}
        if cls.LOG == 2:
            data = cls.detailed_tracker
        else:
            return " "
        output = ""
        for key, value in data.items():
            output += f"{key} :"
            output += f"\n     Attempts   : {value['Attempts']}"
            output += f"\n     Successes  : {value['Successes']}"
            output += f"\n     Time Spent : {value['Time Spent']}"
        return output

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
        match cls.LOG:
            case 0:
                pass
            case 1:
                cls.global_tracker[func.__name__]["Time Spent"] += round(time_spent, 5)
                cls.global_tracker[func.__name__]["Attempts"] += 1
                cls.global_tracker[func.__name__]["Successes"] += int(success)
            case 2:
                cls.detailed_tracker[cls._currently_tracking][func.__name__][
                    "Time Spent"
                ] += round(time_spent, 5)
                cls.detailed_tracker[cls._currently_tracking]["Attempts"] += 1
                cls.detailed_tracker[cls._currently_tracking]["Successes"] += int(
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
