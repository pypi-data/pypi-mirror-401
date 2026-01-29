"""GearMesh"""

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
from mastapy._private.system_model.connections_and_sockets import _2541

_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _1075
    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.connections_and_sockets import _2532
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2559,
        _2561,
        _2563,
        _2565,
        _2567,
        _2569,
        _2571,
        _2575,
        _2578,
        _2579,
        _2580,
        _2583,
        _2585,
        _2587,
        _2589,
        _2591,
    )

    Self = TypeVar("Self", bound="GearMesh")
    CastSelf = TypeVar("CastSelf", bound="GearMesh._Cast_GearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("GearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMesh:
    """Special nested class for casting GearMesh to subclasses."""

    __parent__: "GearMesh"

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2541.InterMountableComponentConnection":
        return self.__parent__._cast(_2541.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2532.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2532

        return self.__parent__._cast(_2532.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        from mastapy._private.system_model import _2452

        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2559.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2559

        return self.__parent__._cast(_2559.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2561.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2561

        return self.__parent__._cast(_2561.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2563.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2563

        return self.__parent__._cast(_2563.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2565.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2565

        return self.__parent__._cast(_2565.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2567.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2567

        return self.__parent__._cast(_2567.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2569.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2569

        return self.__parent__._cast(_2569.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2571.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2571

        return self.__parent__._cast(_2571.FaceGearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2575.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2575

        return self.__parent__._cast(_2575.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2578.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2578

        return self.__parent__._cast(_2578.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2579.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2579

        return self.__parent__._cast(_2579.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2580.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2580

        return self.__parent__._cast(_2580.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2583.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2583

        return self.__parent__._cast(_2583.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2585.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2585

        return self.__parent__._cast(_2585.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2587.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2587

        return self.__parent__._cast(_2587.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2589.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2589

        return self.__parent__._cast(_2589.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2591.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2591

        return self.__parent__._cast(_2591.ZerolBevelGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "GearMesh":
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
class GearMesh(_2541.InterMountableComponentConnection):
    """GearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mesh_efficiency(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MeshEfficiency")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mesh_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh_efficiency(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MeshEfficiency", value)

    @property
    @exception_bridge
    def use_specified_mesh_stiffness(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSpecifiedMeshStiffness")

        if temp is None:
            return False

        return temp

    @use_specified_mesh_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def use_specified_mesh_stiffness(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSpecifiedMeshStiffness",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def user_specified_mesh_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedMeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @user_specified_mesh_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_mesh_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedMeshStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def active_gear_mesh_design(self: "Self") -> "_1075.GearMeshDesign":
        """mastapy.gears.gear_designs.GearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMesh":
        """Cast to another type.

        Returns:
            _Cast_GearMesh
        """
        return _Cast_GearMesh(self)
