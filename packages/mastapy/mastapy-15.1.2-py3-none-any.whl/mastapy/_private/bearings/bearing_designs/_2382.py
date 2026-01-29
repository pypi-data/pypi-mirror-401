"""NonLinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.bearings.bearing_designs import _2378

_NON_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "NonLinearBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2379
    from mastapy._private.bearings.bearing_designs.concept import _2446, _2447, _2448
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2436,
        _2438,
        _2440,
        _2442,
        _2443,
        _2444,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2383,
        _2384,
        _2385,
        _2386,
        _2387,
        _2388,
        _2390,
        _2396,
        _2397,
        _2398,
        _2402,
        _2407,
        _2408,
        _2409,
        _2410,
        _2413,
        _2415,
        _2418,
        _2419,
        _2420,
        _2421,
        _2422,
        _2423,
    )

    Self = TypeVar("Self", bound="NonLinearBearing")
    CastSelf = TypeVar("CastSelf", bound="NonLinearBearing._Cast_NonLinearBearing")


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearBearing:
    """Special nested class for casting NonLinearBearing to subclasses."""

    __parent__: "NonLinearBearing"

    @property
    def bearing_design(self: "CastSelf") -> "_2378.BearingDesign":
        return self.__parent__._cast(_2378.BearingDesign)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2379.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2379

        return self.__parent__._cast(_2379.DetailedBearing)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2383.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2383

        return self.__parent__._cast(_2383.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2384.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2384

        return self.__parent__._cast(_2384.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2385.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2385

        return self.__parent__._cast(_2385.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2386.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2386

        return self.__parent__._cast(_2386.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2387.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2387

        return self.__parent__._cast(_2387.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2388.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2388

        return self.__parent__._cast(_2388.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2390.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2390

        return self.__parent__._cast(_2390.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2396.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2396

        return self.__parent__._cast(_2396.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2397.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2397

        return self.__parent__._cast(_2397.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2398.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2398

        return self.__parent__._cast(_2398.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2402.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2402

        return self.__parent__._cast(_2402.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2407.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2407

        return self.__parent__._cast(_2407.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2408.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2408

        return self.__parent__._cast(_2408.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2409.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2409

        return self.__parent__._cast(_2409.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2410.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2410

        return self.__parent__._cast(_2410.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2413.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2413

        return self.__parent__._cast(_2413.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2415.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2415

        return self.__parent__._cast(_2415.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2418.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2418

        return self.__parent__._cast(_2418.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2419.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2419

        return self.__parent__._cast(_2419.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2420.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2420

        return self.__parent__._cast(_2420.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2421.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2421

        return self.__parent__._cast(_2421.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2422.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2422

        return self.__parent__._cast(_2422.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2423.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2423

        return self.__parent__._cast(_2423.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2436.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2436

        return self.__parent__._cast(_2436.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2438.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2438

        return self.__parent__._cast(_2438.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2440.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2440

        return self.__parent__._cast(_2440.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2442.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2442

        return self.__parent__._cast(_2442.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2443.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2443

        return self.__parent__._cast(_2443.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2444.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2444

        return self.__parent__._cast(_2444.TiltingPadThrustBearing)

    @property
    def concept_axial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2446.ConceptAxialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2446

        return self.__parent__._cast(_2446.ConceptAxialClearanceBearing)

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "_2447.ConceptClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2447

        return self.__parent__._cast(_2447.ConceptClearanceBearing)

    @property
    def concept_radial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2448.ConceptRadialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2448

        return self.__parent__._cast(_2448.ConceptRadialClearanceBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "NonLinearBearing":
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
class NonLinearBearing(_2378.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NonLinearBearing":
        """Cast to another type.

        Returns:
            _Cast_NonLinearBearing
        """
        return _Cast_NonLinearBearing(self)
