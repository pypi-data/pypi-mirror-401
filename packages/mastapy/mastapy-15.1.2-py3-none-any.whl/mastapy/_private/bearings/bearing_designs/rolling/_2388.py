"""BallBearing"""

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

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.implicit import overridable
from mastapy._private.bearings.bearing_designs.rolling import _2413

_BALL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "BallBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2378, _2379, _2382
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2383,
        _2384,
        _2389,
        _2398,
        _2402,
        _2407,
        _2415,
        _2421,
        _2422,
    )

    Self = TypeVar("Self", bound="BallBearing")
    CastSelf = TypeVar("CastSelf", bound="BallBearing._Cast_BallBearing")


__docformat__ = "restructuredtext en"
__all__ = ("BallBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BallBearing:
    """Special nested class for casting BallBearing to subclasses."""

    __parent__: "BallBearing"

    @property
    def rolling_bearing(self: "CastSelf") -> "_2413.RollingBearing":
        return self.__parent__._cast(_2413.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2379.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2379

        return self.__parent__._cast(_2379.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2382.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2382

        return self.__parent__._cast(_2382.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2378.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2378

        return self.__parent__._cast(_2378.BearingDesign)

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
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2415.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2415

        return self.__parent__._cast(_2415.SelfAligningBallBearing)

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
    def ball_bearing(self: "CastSelf") -> "BallBearing":
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
class BallBearing(_2413.RollingBearing):
    """BallBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BALL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_radius_at_right_angle_to_rolling_direction_inner(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusAtRightAngleToRollingDirectionInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_radius_at_right_angle_to_rolling_direction_outer(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusAtRightAngleToRollingDirectionOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def curvature_sum_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureSumInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def curvature_sum_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureSumOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementDiameter", value)

    @property
    @exception_bridge
    def inner_groove_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerGrooveRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_groove_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_groove_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerGrooveRadius", value)

    @property
    @exception_bridge
    def inner_groove_radius_as_percentage_of_element_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "InnerGrooveRadiusAsPercentageOfElementDiameter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_groove_radius_as_percentage_of_element_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_groove_radius_as_percentage_of_element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "InnerGrooveRadiusAsPercentageOfElementDiameter", value
        )

    @property
    @exception_bridge
    def inner_left_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerLeftShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_left_shoulder_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_left_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerLeftShoulderDiameter", value)

    @property
    @exception_bridge
    def inner_race_osculation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRaceOsculation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_race_osculation.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_race_osculation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRaceOsculation", value)

    @property
    @exception_bridge
    def inner_right_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRightShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_right_shoulder_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_right_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRightShoulderDiameter", value)

    @property
    @exception_bridge
    def inner_ring_left_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingLeftShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_left_shoulder_height.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_left_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingLeftShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_ring_right_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingRightShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_right_shoulder_height.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_right_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingRightShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_ring_shoulder_chamfer(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingShoulderChamfer")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_shoulder_chamfer.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_shoulder_chamfer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingShoulderChamfer", value)

    @property
    @exception_bridge
    def outer_groove_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterGrooveRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_groove_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_groove_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterGrooveRadius", value)

    @property
    @exception_bridge
    def outer_groove_radius_as_percentage_of_element_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "OuterGrooveRadiusAsPercentageOfElementDiameter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_groove_radius_as_percentage_of_element_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_groove_radius_as_percentage_of_element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "OuterGrooveRadiusAsPercentageOfElementDiameter", value
        )

    @property
    @exception_bridge
    def outer_left_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterLeftShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_left_shoulder_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_left_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterLeftShoulderDiameter", value)

    @property
    @exception_bridge
    def outer_race_osculation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRaceOsculation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_race_osculation.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_race_osculation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRaceOsculation", value)

    @property
    @exception_bridge
    def outer_right_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRightShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_right_shoulder_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_right_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRightShoulderDiameter", value)

    @property
    @exception_bridge
    def outer_ring_left_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingLeftShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @outer_ring_left_shoulder_height.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_left_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRingLeftShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_ring_right_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingRightShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @outer_ring_right_shoulder_height.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_right_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRingRightShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_ring_shoulder_chamfer(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingShoulderChamfer")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_shoulder_chamfer.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_shoulder_chamfer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingShoulderChamfer", value)

    @property
    @exception_bridge
    def relative_curvature_difference_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeCurvatureDifferenceInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_curvature_difference_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeCurvatureDifferenceOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shoulders(self: "Self") -> "List[_2389.BallBearingShoulderDefinition]":
        """List[mastapy.bearings.bearing_designs.rolling.BallBearingShoulderDefinition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shoulders")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BallBearing":
        """Cast to another type.

        Returns:
            _Cast_BallBearing
        """
        return _Cast_BallBearing(self)
