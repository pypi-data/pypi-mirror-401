"""LoadedDetailedBearingResults"""

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

from mastapy._private._internal import constructor, utility
from mastapy._private.bearings.bearing_results import _2198

_LOADED_DETAILED_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedDetailedBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2113
    from mastapy._private.bearings.bearing_results import _2190
    from mastapy._private.bearings.bearing_results.fluid_film import (
        _2367,
        _2368,
        _2369,
        _2370,
        _2372,
        _2375,
        _2376,
    )
    from mastapy._private.bearings.bearing_results.rolling import (
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
        _2277,
        _2280,
        _2284,
        _2287,
        _2292,
        _2295,
        _2298,
        _2301,
    )
    from mastapy._private.materials import _369

    Self = TypeVar("Self", bound="LoadedDetailedBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedDetailedBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedDetailedBearingResults:
    """Special nested class for casting LoadedDetailedBearingResults to subclasses."""

    __parent__: "LoadedDetailedBearingResults"

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2198.LoadedNonLinearBearingResults":
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
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2277.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2277

        return self.__parent__._cast(_2277.LoadedRollingBearingResults)

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
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2367.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2367

        return self.__parent__._cast(_2367.LoadedFluidFilmBearingResults)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2368.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2368

        return self.__parent__._cast(_2368.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2369.LoadedPadFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2369

        return self.__parent__._cast(_2369.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2370.LoadedPlainJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2370

        return self.__parent__._cast(_2370.LoadedPlainJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2372.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2372

        return self.__parent__._cast(_2372.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2375.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2375

        return self.__parent__._cast(_2375.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2376.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2376

        return self.__parent__._cast(_2376.LoadedTiltingPadThrustBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "LoadedDetailedBearingResults":
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
class LoadedDetailedBearingResults(_2198.LoadedNonLinearBearingResults):
    """LoadedDetailedBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_DETAILED_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lubricant_flow_rate(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFlowRate")

        if temp is None:
            return 0.0

        return temp

    @lubricant_flow_rate.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_flow_rate(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantFlowRate",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def oil_sump_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilSumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @oil_sump_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_sump_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilSumpTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def operating_air_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OperatingAirTemperature")

        if temp is None:
            return 0.0

        return temp

    @operating_air_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def operating_air_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OperatingAirTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def temperature_when_assembled(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureWhenAssembled")

        if temp is None:
            return 0.0

        return temp

    @temperature_when_assembled.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_when_assembled(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureWhenAssembled",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lubrication(self: "Self") -> "_369.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Lubrication")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedDetailedBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedDetailedBearingResults
        """
        return _Cast_LoadedDetailedBearingResults(self)
