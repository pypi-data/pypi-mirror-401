"""LoadedRollerBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import conversion, utility
from mastapy._private.bearings.bearing_results.rolling import _2257

_LOADED_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollerBearingElement"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2231,
        _2236,
        _2239,
        _2247,
        _2251,
        _2263,
        _2270,
        _2282,
        _2283,
        _2289,
        _2291,
        _2300,
        _2313,
    )

    Self = TypeVar("Self", bound="LoadedRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedRollerBearingElement._Cast_LoadedRollerBearingElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollerBearingElement:
    """Special nested class for casting LoadedRollerBearingElement to subclasses."""

    __parent__: "LoadedRollerBearingElement"

    @property
    def loaded_element(self: "CastSelf") -> "_2257.LoadedElement":
        return self.__parent__._cast(_2257.LoadedElement)

    @property
    def loaded_asymmetric_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2231.LoadedAsymmetricSphericalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2231

        return self.__parent__._cast(
            _2231.LoadedAsymmetricSphericalRollerBearingElement
        )

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2236.LoadedAxialThrustCylindricalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2236

        return self.__parent__._cast(
            _2236.LoadedAxialThrustCylindricalRollerBearingElement
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2239.LoadedAxialThrustNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2239

        return self.__parent__._cast(_2239.LoadedAxialThrustNeedleRollerBearingElement)

    @property
    def loaded_crossed_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2247.LoadedCrossedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2247

        return self.__parent__._cast(_2247.LoadedCrossedRollerBearingElement)

    @property
    def loaded_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2251.LoadedCylindricalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2251

        return self.__parent__._cast(_2251.LoadedCylindricalRollerBearingElement)

    @property
    def loaded_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2263.LoadedNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2263

        return self.__parent__._cast(_2263.LoadedNeedleRollerBearingElement)

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "_2270.LoadedNonBarrelRollerElement":
        from mastapy._private.bearings.bearing_results.rolling import _2270

        return self.__parent__._cast(_2270.LoadedNonBarrelRollerElement)

    @property
    def loaded_spherical_radial_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2282.LoadedSphericalRadialRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2282

        return self.__parent__._cast(_2282.LoadedSphericalRadialRollerBearingElement)

    @property
    def loaded_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2283.LoadedSphericalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2283

        return self.__parent__._cast(_2283.LoadedSphericalRollerBearingElement)

    @property
    def loaded_spherical_thrust_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2289.LoadedSphericalThrustRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2289

        return self.__parent__._cast(_2289.LoadedSphericalThrustRollerBearingElement)

    @property
    def loaded_taper_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2291.LoadedTaperRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2291

        return self.__parent__._cast(_2291.LoadedTaperRollerBearingElement)

    @property
    def loaded_toroidal_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2300.LoadedToroidalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2300

        return self.__parent__._cast(_2300.LoadedToroidalRollerBearingElement)

    @property
    def loaded_roller_bearing_element(self: "CastSelf") -> "LoadedRollerBearingElement":
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
class LoadedRollerBearingElement(_2257.LoadedElement):
    """LoadedRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_length_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLengthInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_length_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLengthOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_tilt(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElementTilt")

        if temp is None:
            return 0.0

        return temp

    @element_tilt.setter
    @exception_bridge
    @enforce_parameter_types
    def element_tilt(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ElementTilt", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_contact_width_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactWidthInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_contact_width_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactWidthOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_depth_of_maximum_shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumDepthOfMaximumShearStressInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_depth_of_maximum_shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumDepthOfMaximumShearStressOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_edge_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalEdgeStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_edge_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalEdgeStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_separation_between_roller_end_and_rib_inner_left(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSeparationBetweenRollerEndAndRibInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_separation_between_roller_end_and_rib_inner_right(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSeparationBetweenRollerEndAndRibInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_separation_between_roller_end_and_rib_outer_left(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSeparationBetweenRollerEndAndRibOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_separation_between_roller_end_and_rib_outer_right(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSeparationBetweenRollerEndAndRibOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rib_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RibLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def results_at_roller_offsets(self: "Self") -> "List[_2313.ResultsAtRollerOffset]":
        """List[mastapy.bearings.bearing_results.rolling.ResultsAtRollerOffset]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsAtRollerOffsets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollerBearingElement
        """
        return _Cast_LoadedRollerBearingElement(self)
