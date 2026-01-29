"""VirtualComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model import _2738

_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import (
        _2715,
        _2734,
        _2735,
        _2743,
        _2747,
        _2748,
        _2754,
    )

    Self = TypeVar("Self", bound="VirtualComponent")
    CastSelf = TypeVar("CastSelf", bound="VirtualComponent._Cast_VirtualComponent")


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponent:
    """Special nested class for casting VirtualComponent to subclasses."""

    __parent__: "VirtualComponent"

    @property
    def mountable_component(self: "CastSelf") -> "_2738.MountableComponent":
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
    def mass_disc(self: "CastSelf") -> "_2734.MassDisc":
        from mastapy._private.system_model.part_model import _2734

        return self.__parent__._cast(_2734.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2735.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2735

        return self.__parent__._cast(_2735.MeasurementComponent)

    @property
    def point_load(self: "CastSelf") -> "_2747.PointLoad":
        from mastapy._private.system_model.part_model import _2747

        return self.__parent__._cast(_2747.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2748.PowerLoad":
        from mastapy._private.system_model.part_model import _2748

        return self.__parent__._cast(_2748.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2754.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2754

        return self.__parent__._cast(_2754.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "VirtualComponent":
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
class VirtualComponent(_2738.MountableComponent):
    """VirtualComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponent":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponent
        """
        return _Cast_VirtualComponent(self)
