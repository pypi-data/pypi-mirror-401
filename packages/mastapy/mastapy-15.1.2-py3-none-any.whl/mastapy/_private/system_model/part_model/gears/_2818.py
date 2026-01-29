"""KlingelnbergCycloPalloidConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model.gears import _2805

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2715, _2738, _2743
    from mastapy._private.system_model.part_model.gears import _2812, _2820, _2822

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGear._Cast_KlingelnbergCycloPalloidConicalGear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGear:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGear to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2805.ConicalGear":
        return self.__parent__._cast(_2805.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2812.Gear":
        from mastapy._private.system_model.part_model.gears import _2812

        return self.__parent__._cast(_2812.Gear)

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
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2820.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2820

        return self.__parent__._cast(_2820.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2822.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2822

        return self.__parent__._cast(_2822.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGear":
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
class KlingelnbergCycloPalloidConicalGear(_2805.ConicalGear):
    """KlingelnbergCycloPalloidConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGear":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGear
        """
        return _Cast_KlingelnbergCycloPalloidConicalGear(self)
