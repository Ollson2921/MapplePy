"""A module for working with mapped tilings."""

from .factor import Factor, ILFactorInverted, ILFactorNormal
from .row_col_sep_mt import LTRowColSeparationMT, LTORERowColSeparationMT
from .point_placement import MTRequirementPlacement


__all__ = [
    "Factor",
    "ILFactorNormal",
    "ILFactorInverted",
    "LTRowColSeparationMT",
    "LTORERowColSeparationMT",
    "MTRequirementPlacement",
]
__version__ = "0.1.0"
