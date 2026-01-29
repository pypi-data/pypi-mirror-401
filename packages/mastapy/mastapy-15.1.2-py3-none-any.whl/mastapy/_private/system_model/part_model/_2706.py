"""AbstractShaftOrHousing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model import _2715

_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2705, _2725, _2743
    from mastapy._private.system_model.part_model.cycloidal import _2852
    from mastapy._private.system_model.part_model.shaft_model import _2759

    Self = TypeVar("Self", bound="AbstractShaftOrHousing")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractShaftOrHousing._Cast_AbstractShaftOrHousing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousing:
    """Special nested class for casting AbstractShaftOrHousing to subclasses."""

    __parent__: "AbstractShaftOrHousing"

    @property
    def component(self: "CastSelf") -> "_2715.Component":
        return self.__parent__._cast(_2715.Component)

    @property
    def part(self: "CastSelf") -> "_2743.Part":
        from mastapy._private.system_model.part_model import _2743

        return self.__parent__._cast(_2743.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        from mastapy._private.system_model import _2452

        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2705.AbstractShaft":
        from mastapy._private.system_model.part_model import _2705

        return self.__parent__._cast(_2705.AbstractShaft)

    @property
    def fe_part(self: "CastSelf") -> "_2725.FEPart":
        from mastapy._private.system_model.part_model import _2725

        return self.__parent__._cast(_2725.FEPart)

    @property
    def shaft(self: "CastSelf") -> "_2759.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2759

        return self.__parent__._cast(_2759.Shaft)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2852.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2852

        return self.__parent__._cast(_2852.CycloidalDisc)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "AbstractShaftOrHousing":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class AbstractShaftOrHousing(_2715.Component):
    """AbstractShaftOrHousing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousing":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousing
        """
        return _Cast_AbstractShaftOrHousing(self)
