"""Strategy for verifying when a mappling has no parameters."""

from typing import Optional, Type, TypeVar, Any
from comb_spec_searcher import VerificationStrategy
from gridded_cayley_permutations import GriddedCayleyPerm
from mapplings import MappedTiling

NoParameterVerificationStrategyT = TypeVar(
    "NoParameterVerificationStrategyT", bound="NoParameterVerificationStrategy"
)


class NoParameterVerificationStrategy(
    VerificationStrategy[MappedTiling, GriddedCayleyPerm]
):
    """
    A strategy for verifying if a mappling has no parameters.
    """

    def __init__(
        self,
        rootmt: Optional[MappedTiling] = None,
        ignore_parent: bool = False,
    ):
        self._rootmt: MappedTiling | tuple[Any, ...] = (
            rootmt if rootmt is not None else tuple()
        )
        super().__init__(ignore_parent=ignore_parent)

    def change_root(
        self: NoParameterVerificationStrategyT,
        mapped_tiling: MappedTiling,
    ) -> NoParameterVerificationStrategyT:
        """
        Return a new version of the verification strategy with the given mappling instead
        of the current one.
        """
        return self.__class__(mapped_tiling, self.ignore_parent)

    @property
    def rootmt(self) -> MappedTiling | tuple[Any, ...]:
        """The root mapped tiling."""
        return self._rootmt

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from mapplings.strategies.tilescope_strategies import MappedTileScopePack

        return MappedTileScopePack.no_param_ver_point_placement()

    def verified(self, comb_class: MappedTiling) -> bool:
        if (
            comb_class.avoiding_parameters
            or comb_class.containing_parameters
            or comb_class.enumerating_parameters
        ):
            return False
        if comb_class == self.rootmt:
            return False
        return True

    def formal_step(self):
        return "The mappling has no parameters"

    def to_jsonable(self) -> dict:
        d: dict = super().to_jsonable()
        d["rootmt"] = self._rootmt.to_jsonable()
        return d

    @classmethod
    def from_dict(
        cls: Type[NoParameterVerificationStrategyT], d: dict
    ) -> NoParameterVerificationStrategyT:
        if "rootmt" in d and d["rootmt"] is not None:
            rootmt: Optional[MappedTiling] = MappedTiling.from_dict(d.pop("rootmt"))
        else:
            rootmt = d.pop("rootmt", None)
        return cls(rootmt=rootmt, **d)

    def __repr__(self) -> str:
        args = ", ".join(
            [
                f"root mapped tiling={self._rootmt}",
                f"ignore_parent={self.ignore_parent}",
            ]
        )
        return f"{self.__class__.__name__}({args})"
