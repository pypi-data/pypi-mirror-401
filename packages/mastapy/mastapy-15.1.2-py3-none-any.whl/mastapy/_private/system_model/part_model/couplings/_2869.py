"""CouplingHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.implicit import overridable
from mastapy._private.system_model.part_model import _2738

_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2715, _2743
    from mastapy._private.system_model.part_model.couplings import (
        _2863,
        _2866,
        _2872,
        _2874,
        _2876,
        _2883,
        _2892,
        _2895,
        _2896,
        _2897,
        _2899,
        _2901,
    )

    Self = TypeVar("Self", bound="CouplingHalf")
    CastSelf = TypeVar("CastSelf", bound="CouplingHalf._Cast_CouplingHalf")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalf:
    """Special nested class for casting CouplingHalf to subclasses."""

    __parent__: "CouplingHalf"

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
    def clutch_half(self: "CastSelf") -> "_2863.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2863

        return self.__parent__._cast(_2863.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2866.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2866

        return self.__parent__._cast(_2866.ConceptCouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2872.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2872

        return self.__parent__._cast(_2872.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2874.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2874

        return self.__parent__._cast(_2874.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2876.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2876

        return self.__parent__._cast(_2876.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2883.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2883

        return self.__parent__._cast(_2883.RollingRing)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2892.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2892

        return self.__parent__._cast(_2892.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2895.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2895

        return self.__parent__._cast(_2895.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2896.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2896

        return self.__parent__._cast(_2896.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2897.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2897

        return self.__parent__._cast(_2897.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2899.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2899

        return self.__parent__._cast(_2899.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2901.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2901

        return self.__parent__._cast(_2901.TorqueConverterTurbine)

    @property
    def coupling_half(self: "CastSelf") -> "CouplingHalf":
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
class CouplingHalf(_2738.MountableComponent):
    """CouplingHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Bore", value)

    @property
    @exception_bridge
    def diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Diameter", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalf":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalf
        """
        return _Cast_CouplingHalf(self)
