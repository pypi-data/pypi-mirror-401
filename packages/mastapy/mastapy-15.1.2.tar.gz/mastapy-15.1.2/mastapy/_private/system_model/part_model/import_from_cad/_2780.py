"""CylindricalGearInPlanetarySetFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model.import_from_cad import _2779

_CYLINDRICAL_GEAR_IN_PLANETARY_SET_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2775,
        _2776,
        _2781,
        _2782,
        _2783,
        _2785,
    )

    Self = TypeVar("Self", bound="CylindricalGearInPlanetarySetFromCAD")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearInPlanetarySetFromCAD._Cast_CylindricalGearInPlanetarySetFromCAD",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearInPlanetarySetFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearInPlanetarySetFromCAD:
    """Special nested class for casting CylindricalGearInPlanetarySetFromCAD to subclasses."""

    __parent__: "CylindricalGearInPlanetarySetFromCAD"

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2779.CylindricalGearFromCAD":
        return self.__parent__._cast(_2779.CylindricalGearFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2785.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2785

        return self.__parent__._cast(_2785.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2775.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2775

        return self.__parent__._cast(_2775.ComponentFromCAD)

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2776.ComponentFromCADBase":
        from mastapy._private.system_model.part_model.import_from_cad import _2776

        return self.__parent__._cast(_2776.ComponentFromCADBase)

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
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "CylindricalGearInPlanetarySetFromCAD":
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
class CylindricalGearInPlanetarySetFromCAD(_2779.CylindricalGearFromCAD):
    """CylindricalGearInPlanetarySetFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_IN_PLANETARY_SET_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearInPlanetarySetFromCAD":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearInPlanetarySetFromCAD
        """
        return _Cast_CylindricalGearInPlanetarySetFromCAD(self)
