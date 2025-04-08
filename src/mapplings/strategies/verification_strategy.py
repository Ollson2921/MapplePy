from typing import Optional, Type, TypeVar
from comb_spec_searcher import VerificationStrategy
from mapplings import MappedTiling

RootVerificationStrategyType = TypeVar(
    "RootVerificationStrategyType", bound="RootVerificationStrategy"
)


class RootVerificationStrategy(VerificationStrategy[MappedTiling, MappedTiling]):
    """
    A base class for a verification strategy that needs to know the basis the
    Tilescope is currently running.
    """

    def __init__(
        self,
        rootmt: Optional[MappedTiling] = None,
        ignore_parent: bool = False,
    ):
        self._rootmt = rootmt if rootmt is not None else tuple()
        super().__init__(ignore_parent=ignore_parent)

    def change_root(
        self: RootVerificationStrategyType,
        mapped_tiling: MappedTiling,
    ) -> RootVerificationStrategyType:
        """
        Return a new version of the verification strategy with the given mappling instead
        of the current one.
        """
        return self.__class__(mapped_tiling, self.ignore_parent)

    @property
    def rootmt(self) -> MappedTiling:
        return self._rootmt

    def verified(self, comb_class: MappedTiling) -> bool:
        return self.rootmt == comb_class

    def formal_step(self):
        return "the mappling is the same as the root"

    def to_jsonable(self) -> dict:
        d: dict = super().to_jsonable()
        d["rootmt"] = self._rootmt
        return d

    @classmethod
    def from_dict(
        cls: Type[RootVerificationStrategyType], d: dict
    ) -> RootVerificationStrategyType:
        if "rootmt" in d and d["rootmt"] is not None:
            rootmt: Optional[MappedTiling] = d["rootmt"]
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
