"""PartToPartShearCoupling"""

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
from mastapy._private.system_model.part_model.couplings import _2868

_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.connections_and_sockets.couplings import _2608
    from mastapy._private.system_model.part_model import _2704, _2743, _2753

    Self = TypeVar("Self", bound="PartToPartShearCoupling")
    CastSelf = TypeVar(
        "CastSelf", bound="PartToPartShearCoupling._Cast_PartToPartShearCoupling"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCoupling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCoupling:
    """Special nested class for casting PartToPartShearCoupling to subclasses."""

    __parent__: "PartToPartShearCoupling"

    @property
    def coupling(self: "CastSelf") -> "_2868.Coupling":
        return self.__parent__._cast(_2868.Coupling)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2753.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2753

        return self.__parent__._cast(_2753.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2704.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2704

        return self.__parent__._cast(_2704.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2743.Part":
        from mastapy._private.system_model.part_model import _2743

        return self.__parent__._cast(_2743.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        from mastapy._private.system_model import _2452

        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def part_to_part_shear_coupling(self: "CastSelf") -> "PartToPartShearCoupling":
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
class PartToPartShearCoupling(_2868.Coupling):
    """PartToPartShearCoupling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_TO_PART_SHEAR_COUPLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_diameter_for_loss_calculation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameterForLossCalculation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter_for_loss_calculation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameterForLossCalculation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def volumetric_oil_air_mixture_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "VolumetricOilAirMixtureRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @volumetric_oil_air_mixture_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def volumetric_oil_air_mixture_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "VolumetricOilAirMixtureRatio", value)

    @property
    @exception_bridge
    def part_to_part_shear_coupling_connection(
        self: "Self",
    ) -> "_2608.PartToPartShearCouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartToPartShearCouplingConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartToPartShearCoupling":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCoupling
        """
        return _Cast_PartToPartShearCoupling(self)
