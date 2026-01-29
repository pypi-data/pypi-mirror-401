"""LoadedElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility

_LOADED_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedElement"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    from mastapy._private.bearings.bearing_results import _2185
    from mastapy._private.bearings.bearing_results.rolling import (
        _2215,
        _2225,
        _2228,
        _2231,
        _2236,
        _2239,
        _2243,
        _2247,
        _2251,
        _2254,
        _2258,
        _2262,
        _2263,
        _2270,
        _2272,
        _2279,
        _2282,
        _2283,
        _2289,
        _2291,
        _2294,
        _2297,
        _2300,
        _2320,
    )

    Self = TypeVar("Self", bound="LoadedElement")
    CastSelf = TypeVar("CastSelf", bound="LoadedElement._Cast_LoadedElement")


__docformat__ = "restructuredtext en"
__all__ = ("LoadedElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedElement:
    """Special nested class for casting LoadedElement to subclasses."""

    __parent__: "LoadedElement"

    @property
    def loaded_angular_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2225.LoadedAngularContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2225

        return self.__parent__._cast(_2225.LoadedAngularContactBallBearingElement)

    @property
    def loaded_angular_contact_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2228.LoadedAngularContactThrustBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2228

        return self.__parent__._cast(_2228.LoadedAngularContactThrustBallBearingElement)

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
    def loaded_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2243.LoadedBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2243

        return self.__parent__._cast(_2243.LoadedBallBearingElement)

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
    def loaded_deep_groove_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2254.LoadedDeepGrooveBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2254

        return self.__parent__._cast(_2254.LoadedDeepGrooveBallBearingElement)

    @property
    def loaded_four_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2258.LoadedFourPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2258

        return self.__parent__._cast(_2258.LoadedFourPointContactBallBearingElement)

    @property
    def loaded_multi_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2262.LoadedMultiPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2262

        return self.__parent__._cast(_2262.LoadedMultiPointContactBallBearingElement)

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
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2272.LoadedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2272

        return self.__parent__._cast(_2272.LoadedRollerBearingElement)

    @property
    def loaded_self_aligning_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2279.LoadedSelfAligningBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2279

        return self.__parent__._cast(_2279.LoadedSelfAligningBallBearingElement)

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
    def loaded_three_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2294.LoadedThreePointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2294

        return self.__parent__._cast(_2294.LoadedThreePointContactBallBearingElement)

    @property
    def loaded_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2297.LoadedThrustBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2297

        return self.__parent__._cast(_2297.LoadedThrustBallBearingElement)

    @property
    def loaded_toroidal_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2300.LoadedToroidalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2300

        return self.__parent__._cast(_2300.LoadedToroidalRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "LoadedElement":
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
class LoadedElement(_0.APIBase):
    """LoadedElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialLoading")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def central_lubricating_film_thickness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CentralLubricatingFilmThicknessInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def central_lubricating_film_thickness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CentralLubricatingFilmThicknessOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementId")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def element_raceway_contact_area_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_raceway_contact_area_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_raceway_contact_area_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_raceway_contact_area_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_load_inner(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalLoadInner")

        if temp is None:
            return 0.0

        return temp

    @normal_load_inner.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_load_inner(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalLoadInner", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def normal_load_outer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalLoadOuter")

        if temp is None:
            return 0.0

        return temp

    @normal_load_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_load_outer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalLoadOuter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def race_deflection_inner(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RaceDeflectionInner")

        if temp is None:
            return 0.0

        return temp

    @race_deflection_inner.setter
    @exception_bridge
    @enforce_parameter_types
    def race_deflection_inner(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RaceDeflectionInner",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def race_deflection_outer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RaceDeflectionOuter")

        if temp is None:
            return 0.0

        return temp

    @race_deflection_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def race_deflection_outer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RaceDeflectionOuter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def race_deflection_total(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RaceDeflectionTotal")

        if temp is None:
            return 0.0

        return temp

    @race_deflection_total.setter
    @exception_bridge
    @enforce_parameter_types
    def race_deflection_total(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RaceDeflectionTotal",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def race_separation_at_element_axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceSeparationAtElementAxial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def race_separation_at_element_radial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceSeparationAtElementRadial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_from_inner_race(self: "Self") -> "_2185.ElementForce":
        """mastapy.bearings.bearing_results.ElementForce

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceFromInnerRace")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def operating_internal_clearance(self: "Self") -> "_2215.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def subsurface_shear_stress_distribution_inner(
        self: "Self",
    ) -> "List[_2320.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceShearStressDistributionInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_shear_stress_distribution_outer(
        self: "Self",
    ) -> "List[_2320.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceShearStressDistributionOuter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_von_mises_stress_distribution_inner(
        self: "Self",
    ) -> "List[_2320.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceVonMisesStressDistributionInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_von_mises_stress_distribution_outer(
        self: "Self",
    ) -> "List[_2320.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceVonMisesStressDistributionOuter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def normal_contact_stress_at_points_along_raceway(
        self: "Self", is_inner: "bool"
    ) -> "List[float]":
        """List[float]

        Args:
            is_inner (bool)
        """
        is_inner = bool(is_inner)
        return conversion.to_list_any(
            pythonnet_method_call(
                self.wrapped,
                "NormalContactStressAtPointsAlongRaceway",
                is_inner if is_inner else False,
            )
        )

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedElement
        """
        return _Cast_LoadedElement(self)
