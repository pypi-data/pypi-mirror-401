"""LoadedRollingBearingResults"""

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

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private.bearings.bearing_results import _2195

_LOADED_ROLLING_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollingBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _2113, _2122
    from mastapy._private.bearings.bearing_results import _2190, _2198
    from mastapy._private.bearings.bearing_results.rolling import (
        _2211,
        _2215,
        _2220,
        _2221,
        _2223,
        _2226,
        _2229,
        _2232,
        _2237,
        _2240,
        _2245,
        _2248,
        _2252,
        _2255,
        _2260,
        _2264,
        _2267,
        _2273,
        _2278,
        _2280,
        _2284,
        _2287,
        _2292,
        _2295,
        _2298,
        _2301,
        _2304,
    )
    from mastapy._private.bearings.bearing_results.rolling.abma import _2365
    from mastapy._private.bearings.bearing_results.rolling.fitting import (
        _2357,
        _2359,
        _2360,
    )
    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2350,
        _2351,
        _2352,
    )
    from mastapy._private.bearings.bearing_results.rolling.skf_module import _2345

    Self = TypeVar("Self", bound="LoadedRollingBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedRollingBearingResults._Cast_LoadedRollingBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollingBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollingBearingResults:
    """Special nested class for casting LoadedRollingBearingResults to subclasses."""

    __parent__: "LoadedRollingBearingResults"

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2195.LoadedDetailedBearingResults":
        return self.__parent__._cast(_2195.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2198.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2198

        return self.__parent__._cast(_2198.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2190.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2190

        return self.__parent__._cast(_2190.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2113.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2113

        return self.__parent__._cast(_2113.BearingLoadCaseResultsLightweight)

    @property
    def loaded_angular_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2226.LoadedAngularContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2226

        return self.__parent__._cast(_2226.LoadedAngularContactBallBearingResults)

    @property
    def loaded_angular_contact_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2229.LoadedAngularContactThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2229

        return self.__parent__._cast(_2229.LoadedAngularContactThrustBallBearingResults)

    @property
    def loaded_asymmetric_spherical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2232.LoadedAsymmetricSphericalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2232

        return self.__parent__._cast(
            _2232.LoadedAsymmetricSphericalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2237.LoadedAxialThrustCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2237

        return self.__parent__._cast(
            _2237.LoadedAxialThrustCylindricalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2240.LoadedAxialThrustNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2240

        return self.__parent__._cast(_2240.LoadedAxialThrustNeedleRollerBearingResults)

    @property
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2245.LoadedBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2245

        return self.__parent__._cast(_2245.LoadedBallBearingResults)

    @property
    def loaded_crossed_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2248.LoadedCrossedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2248

        return self.__parent__._cast(_2248.LoadedCrossedRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2252.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2252

        return self.__parent__._cast(_2252.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_deep_groove_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2255.LoadedDeepGrooveBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2255

        return self.__parent__._cast(_2255.LoadedDeepGrooveBallBearingResults)

    @property
    def loaded_four_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2260.LoadedFourPointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2260

        return self.__parent__._cast(_2260.LoadedFourPointContactBallBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2264.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2264

        return self.__parent__._cast(_2264.LoadedNeedleRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2267.LoadedNonBarrelRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2267

        return self.__parent__._cast(_2267.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2273.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2273

        return self.__parent__._cast(_2273.LoadedRollerBearingResults)

    @property
    def loaded_self_aligning_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2280.LoadedSelfAligningBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2280

        return self.__parent__._cast(_2280.LoadedSelfAligningBallBearingResults)

    @property
    def loaded_spherical_roller_radial_bearing_results(
        self: "CastSelf",
    ) -> "_2284.LoadedSphericalRollerRadialBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2284

        return self.__parent__._cast(_2284.LoadedSphericalRollerRadialBearingResults)

    @property
    def loaded_spherical_roller_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2287.LoadedSphericalRollerThrustBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2287

        return self.__parent__._cast(_2287.LoadedSphericalRollerThrustBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2292.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2292

        return self.__parent__._cast(_2292.LoadedTaperRollerBearingResults)

    @property
    def loaded_three_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2295.LoadedThreePointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2295

        return self.__parent__._cast(_2295.LoadedThreePointContactBallBearingResults)

    @property
    def loaded_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2298.LoadedThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2298

        return self.__parent__._cast(_2298.LoadedThrustBallBearingResults)

    @property
    def loaded_toroidal_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2301.LoadedToroidalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2301

        return self.__parent__._cast(_2301.LoadedToroidalRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "LoadedRollingBearingResults":
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
class LoadedRollingBearingResults(_2195.LoadedDetailedBearingResults):
    """LoadedRollingBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLING_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_to_radial_load_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialToRadialLoadRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cage_angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CageAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_element_diameter_due_to_thermal_expansion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInElementDiameterDueToThermalExpansion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_operating_radial_internal_clearance_due_to_element_thermal_expansion(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ChangeInOperatingRadialInternalClearanceDueToElementThermalExpansion",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def drag_loss_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DragLossFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElementTemperature")

        if temp is None:
            return 0.0

        return temp

    @element_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def element_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ElementTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def fluid_film_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluidFilmDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fluid_film_temperature_source(
        self: "Self",
    ) -> "_2122.FluidFilmTemperatureOptions":
        """mastapy.bearings.FluidFilmTemperatureOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluidFilmTemperatureSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.FluidFilmTemperatureOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2122", "FluidFilmTemperatureOptions"
        )(value)

    @property
    @exception_bridge
    def frequency_of_over_rolling_on_inner_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfOverRollingOnInnerRing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frequency_of_over_rolling_on_outer_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfOverRollingOnOuterRing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frequency_of_over_rolling_on_rolling_element(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FrequencyOfOverRollingOnRollingElement"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_moment_of_drag_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalMomentOfDragLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_moment_of_seals(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalMomentOfSeals")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def include_centrifugal_effects(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeCentrifugalEffects")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def include_centrifugal_ring_expansion(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeCentrifugalRingExpansion")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def include_fitting_effects(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeFittingEffects")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def include_gear_blank_elastic_distortion(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeGearBlankElasticDistortion")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def include_inner_race_deflections(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeInnerRaceDeflections")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def include_thermal_expansion_effects(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeThermalExpansionEffects")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_inner_ring_rotating_relative_to_load(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsInnerRingRotatingRelativeToLoad")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_outer_ring_rotating_relative_to_load(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsOuterRingRotatingRelativeToLoad")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def kinematic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KinematicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def kinematic_viscosity_of_oil_for_efficiency_calculations(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KinematicViscosityOfOilForEfficiencyCalculations"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lambda_ratio_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lambda_ratio_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_film_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFilmTemperature")

        if temp is None:
            return 0.0

        return temp

    @lubricant_film_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_film_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantFilmTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lubricant_windage_and_churning_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LubricantWindageAndChurningTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @lubricant_windage_and_churning_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_windage_and_churning_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantWindageAndChurningTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_normal_load_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalLoadInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_load_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalLoadOuter")

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
    def number_of_elements_in_contact(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfElementsInContact")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def oil_dip_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDipCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ratio_of_operating_element_diameter_to_element_pcd(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RatioOfOperatingElementDiameterToElementPCD"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rolling_frictional_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingFrictionalMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_friction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingFrictionCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_frictional_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingFrictionalMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_factor_dmn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactorDmn")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_factor_dn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactorDn")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_equivalent_load_capacity_ratio_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticEquivalentLoadCapacityRatioLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surrounding_lubricant_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurroundingLubricantDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_element_raceway_contact_area_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_element_raceway_contact_area_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_element_raceway_contact_area_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_element_raceway_contact_area_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_frictional_moment_from_skf_loss_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalFrictionalMomentFromSKFLossMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ansiabma(self: "Self") -> "_2365.ANSIABMAResults":
        """mastapy.bearings.bearing_results.rolling.abma.ANSIABMAResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din7322010(self: "Self") -> "_2211.DIN7322010Results":
        """mastapy.bearings.bearing_results.rolling.DIN7322010Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DIN7322010")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso162812025(self: "Self") -> "_2350.ISO162812025Results":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.ISO162812025Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO162812025")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso179562025(self: "Self") -> "_2220.ISO179562025Results":
        """mastapy.bearings.bearing_results.rolling.ISO179562025Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO179562025")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso2812007(self: "Self") -> "_2351.ISO2812007Results":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.ISO2812007Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso762006(self: "Self") -> "_2352.ISO762006Results":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.ISO762006Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO762006")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def isotr1417912001(self: "Self") -> "_2221.ISOTR1417912001Results":
        """mastapy.bearings.bearing_results.rolling.ISOTR1417912001Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOTR1417912001")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def isotr1417922001(self: "Self") -> "_2223.ISOTR1417922001Results":
        """mastapy.bearings.bearing_results.rolling.ISOTR1417922001Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOTR1417922001")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_ring_fitting_at_assembly(
        self: "Self",
    ) -> "_2357.InnerRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.InnerRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRingFittingAtAssembly")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_ring_fitting_at_operating_conditions(
        self: "Self",
    ) -> "_2357.InnerRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.InnerRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerRingFittingAtOperatingConditions"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_operating_internal_clearance(self: "Self") -> "_2215.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumOperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_static_contact_stress(
        self: "Self",
    ) -> "_2304.MaximumStaticContactStress":
        """mastapy.bearings.bearing_results.rolling.MaximumStaticContactStress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumStaticContactStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_operating_internal_clearance(self: "Self") -> "_2215.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_ring_fitting_at_assembly(
        self: "Self",
    ) -> "_2359.OuterRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.OuterRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRingFittingAtAssembly")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_ring_fitting_at_operating_conditions(
        self: "Self",
    ) -> "_2359.OuterRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.OuterRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRingFittingAtOperatingConditions"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def skf_module_results(self: "Self") -> "_2345.SKFModuleResults":
        """mastapy.bearings.bearing_results.rolling.skf_module.SKFModuleResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFModuleResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def all_mounting_results(self: "Self") -> "List[_2360.RingFittingThermalResults]":
        """List[mastapy.bearings.bearing_results.rolling.fitting.RingFittingThermalResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllMountingResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rows(self: "Self") -> "List[_2278.LoadedRollingBearingRow]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedRollingBearingRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollingBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollingBearingResults
        """
        return _Cast_LoadedRollingBearingResults(self)
