"""StraightBevelGearMesh"""

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
from mastapy._private.system_model.connections_and_sockets.gears import _2563

_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.straight_bevel import _1088
    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.connections_and_sockets import _2532, _2541
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2559,
        _2567,
        _2573,
    )

    Self = TypeVar("Self", bound="StraightBevelGearMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="StraightBevelGearMesh._Cast_StraightBevelGearMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearMesh:
    """Special nested class for casting StraightBevelGearMesh to subclasses."""

    __parent__: "StraightBevelGearMesh"

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2563.BevelGearMesh":
        return self.__parent__._cast(_2563.BevelGearMesh)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2559.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2559

        return self.__parent__._cast(_2559.AGMAGleasonConicalGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2567.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2567

        return self.__parent__._cast(_2567.ConicalGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2573.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2573

        return self.__parent__._cast(_2573.GearMesh)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2541.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2541

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
    def straight_bevel_gear_mesh(self: "CastSelf") -> "StraightBevelGearMesh":
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
class StraightBevelGearMesh(_2563.BevelGearMesh):
    """StraightBevelGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bevel_gear_mesh_design(self: "Self") -> "_1088.StraightBevelGearMeshDesign":
        """mastapy.gears.gear_designs.straight_bevel.StraightBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def straight_bevel_gear_mesh_design(
        self: "Self",
    ) -> "_1088.StraightBevelGearMeshDesign":
        """mastapy.gears.gear_designs.straight_bevel.StraightBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearMesh":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearMesh
        """
        return _Cast_StraightBevelGearMesh(self)
