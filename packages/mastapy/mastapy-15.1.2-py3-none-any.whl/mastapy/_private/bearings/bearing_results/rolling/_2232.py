"""LoadedAsymmetricSphericalRollerBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.bearings.bearing_results.rolling import _2273

_LOADED_ASYMMETRIC_SPHERICAL_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAsymmetricSphericalRollerBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2113
    from mastapy._private.bearings.bearing_results import _2190, _2195, _2198
    from mastapy._private.bearings.bearing_results.rolling import _2277

    Self = TypeVar("Self", bound="LoadedAsymmetricSphericalRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAsymmetricSphericalRollerBearingResults._Cast_LoadedAsymmetricSphericalRollerBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAsymmetricSphericalRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAsymmetricSphericalRollerBearingResults:
    """Special nested class for casting LoadedAsymmetricSphericalRollerBearingResults to subclasses."""

    __parent__: "LoadedAsymmetricSphericalRollerBearingResults"

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
    def loaded_asymmetric_spherical_roller_bearing_results(
        self: "CastSelf",
    ) -> "LoadedAsymmetricSphericalRollerBearingResults":
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
class LoadedAsymmetricSphericalRollerBearingResults(_2273.LoadedRollerBearingResults):
    """LoadedAsymmetricSphericalRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ASYMMETRIC_SPHERICAL_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedAsymmetricSphericalRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedAsymmetricSphericalRollerBearingResults
        """
        return _Cast_LoadedAsymmetricSphericalRollerBearingResults(self)
