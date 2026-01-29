"""ConceptCouplingHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model.couplings import _2869

_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2715, _2738, _2743

    Self = TypeVar("Self", bound="ConceptCouplingHalf")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptCouplingHalf._Cast_ConceptCouplingHalf"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptCouplingHalf:
    """Special nested class for casting ConceptCouplingHalf to subclasses."""

    __parent__: "ConceptCouplingHalf"

    @property
    def coupling_half(self: "CastSelf") -> "_2869.CouplingHalf":
        return self.__parent__._cast(_2869.CouplingHalf)

    @property
    def mountable_component(self: "CastSelf") -> "_2738.MountableComponent":
        from mastapy._private.system_model.part_model import _2738

        return self.__parent__._cast(_2738.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2715.Component":
        from mastapy._private.system_model.part_model import _2715

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
    def concept_coupling_half(self: "CastSelf") -> "ConceptCouplingHalf":
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
class ConceptCouplingHalf(_2869.CouplingHalf):
    """ConceptCouplingHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_COUPLING_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptCouplingHalf":
        """Cast to another type.

        Returns:
            _Cast_ConceptCouplingHalf
        """
        return _Cast_ConceptCouplingHalf(self)
