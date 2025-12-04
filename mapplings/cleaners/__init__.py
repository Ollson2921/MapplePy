"""A module for with the cleaning classes."""

from .cleaner import GenericCleaner, Register, CleanerLog
from .parameter_cleaner import ParamCleaner
from .mappling_cleaner import MTCleaner

__all__ = [
    "GenericCleaner",
    "Register",
    "CleanerLog",
    "ParamCleaner",
    "MTCleaner",
]
__version__ = "0.1.0"
