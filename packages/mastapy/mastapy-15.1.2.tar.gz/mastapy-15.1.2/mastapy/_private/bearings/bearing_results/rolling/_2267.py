"""LoadedNonBarrelRollerBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

from mastapy._private._internal import constructor, utility
from mastapy._private.bearings.bearing_results.rolling import _2273

_LOADED_NON_BARREL_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedNonBarrelRollerBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2113
    from mastapy._private.bearings.bearing_results import _2190, _2195, _2198
    from mastapy._private.bearings.bearing_results.rolling import (
        _2237,
        _2240,
        _2252,
        _2264,
        _2277,
        _2292,
        _2319,
    )

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerBearingResults:
    """Special nested class for casting LoadedNonBarrelRollerBearingResults to subclasses."""

    __parent__: "LoadedNonBarrelRollerBearingResults"

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2273.LoadedRollerBearingResults":
        return self.__parent__._cast(_2273.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2277.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2277

        return self.__parent__._cast(_2277.LoadedRollingBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2195.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2195

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
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2252.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2252

        return self.__parent__._cast(_2252.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2264.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2264

        return self.__parent__._cast(_2264.LoadedNeedleRollerBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2292.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2292

        return self.__parent__._cast(_2292.LoadedTaperRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerBearingResults":
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
class LoadedNonBarrelRollerBearingResults(_2273.LoadedRollerBearingResults):
    """LoadedNonBarrelRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def smt_rib_stress(self: "Self") -> "_2319.SMTRibStressResults":
        """mastapy.bearings.bearing_results.rolling.SMTRibStressResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SMTRibStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerBearingResults
        """
        return _Cast_LoadedNonBarrelRollerBearingResults(self)
