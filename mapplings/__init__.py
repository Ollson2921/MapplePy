"""A module for working with mapped tilings."""

from .mapped_tiling import MappedTiling
from .parameter import Parameter
from .parameter_list import ParameterList
from .cleaner import MTCleaner, ParamCleaner
from .strategies import LTRowColSeparationMT

__all__ = ["MappedTiling", "Parameter", "ParameterList", "MTCleaner", "ParamCleaner"]
__version__ = "0.1.0"
