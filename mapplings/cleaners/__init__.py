"""A module for with the cleaning classes."""

from .cleaner import GenericCleaner, Register
from .parameter_cleaner import ParamCleaner
from .mappling_cleaner import MTCleaner

__all__ = [
    "GenericCleaner",
    "Register",
    "ParamCleaner",
    "MTCleaner",
]
__version__ = "0.1.0"
