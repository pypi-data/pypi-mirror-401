"""MountableComponentFromCAD"""

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

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model.import_from_cad import _2775

_MOUNTABLE_COMPONENT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "MountableComponentFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2774,
        _2776,
        _2777,
        _2778,
        _2779,
        _2780,
        _2781,
        _2782,
        _2783,
        _2787,
        _2788,
        _2789,
    )

    Self = TypeVar("Self", bound="MountableComponentFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="MountableComponentFromCAD._Cast_MountableComponentFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentFromCAD:
    """Special nested class for casting MountableComponentFromCAD to subclasses."""

    __parent__: "MountableComponentFromCAD"

    @property
    def component_from_cad(self: "CastSelf") -> "_2775.ComponentFromCAD":
        return self.__parent__._cast(_2775.ComponentFromCAD)

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2776.ComponentFromCADBase":
        from mastapy._private.system_model.part_model.import_from_cad import _2776

        return self.__parent__._cast(_2776.ComponentFromCADBase)

    @property
    def clutch_from_cad(self: "CastSelf") -> "_2774.ClutchFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2774

        return self.__parent__._cast(_2774.ClutchFromCAD)

    @property
    def concept_bearing_from_cad(self: "CastSelf") -> "_2777.ConceptBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2777

        return self.__parent__._cast(_2777.ConceptBearingFromCAD)

    @property
    def connector_from_cad(self: "CastSelf") -> "_2778.ConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2778

        return self.__parent__._cast(_2778.ConnectorFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2779.CylindricalGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2779

        return self.__parent__._cast(_2779.CylindricalGearFromCAD)

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2780.CylindricalGearInPlanetarySetFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2780

        return self.__parent__._cast(_2780.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_planet_gear_from_cad(
        self: "CastSelf",
    ) -> "_2781.CylindricalPlanetGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2781

        return self.__parent__._cast(_2781.CylindricalPlanetGearFromCAD)

    @property
    def cylindrical_ring_gear_from_cad(
        self: "CastSelf",
    ) -> "_2782.CylindricalRingGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2782

        return self.__parent__._cast(_2782.CylindricalRingGearFromCAD)

    @property
    def cylindrical_sun_gear_from_cad(
        self: "CastSelf",
    ) -> "_2783.CylindricalSunGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2783

        return self.__parent__._cast(_2783.CylindricalSunGearFromCAD)

    @property
    def pulley_from_cad(self: "CastSelf") -> "_2787.PulleyFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2787

        return self.__parent__._cast(_2787.PulleyFromCAD)

    @property
    def rigid_connector_from_cad(self: "CastSelf") -> "_2788.RigidConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2788

        return self.__parent__._cast(_2788.RigidConnectorFromCAD)

    @property
    def rolling_bearing_from_cad(self: "CastSelf") -> "_2789.RollingBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2789

        return self.__parent__._cast(_2789.RollingBearingFromCAD)

    @property
    def mountable_component_from_cad(self: "CastSelf") -> "MountableComponentFromCAD":
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
class MountableComponentFromCAD(_2775.ComponentFromCAD):
    """MountableComponentFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @exception_bridge
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentFromCAD":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentFromCAD
        """
        return _Cast_MountableComponentFromCAD(self)
