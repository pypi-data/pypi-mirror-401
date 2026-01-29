"""MaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.utility.databases import _2061

_MATERIAL_DATABASE = python_net_import("SMT.MastaAPI.Materials", "MaterialDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.cycloidal import _1670, _1677
    from mastapy._private.electric_machines import _1432, _1446, _1466, _1481
    from mastapy._private.gears.materials import _698, _700, _704, _705, _707, _708
    from mastapy._private.materials import _371
    from mastapy._private.shafts import _25
    from mastapy._private.utility.databases import _2057, _2065

    Self = TypeVar("Self", bound="MaterialDatabase")
    CastSelf = TypeVar("CastSelf", bound="MaterialDatabase._Cast_MaterialDatabase")

T = TypeVar("T", bound="_371.Material")

__docformat__ = "restructuredtext en"
__all__ = ("MaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialDatabase:
    """Special nested class for casting MaterialDatabase to subclasses."""

    __parent__: "MaterialDatabase"

    @property
    def named_database(self: "CastSelf") -> "_2061.NamedDatabase":
        return self.__parent__._cast(_2061.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_2065.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _2065

        return self.__parent__._cast(_2065.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2057.Database":
        pass

        from mastapy._private.utility.databases import _2057

        return self.__parent__._cast(_2057.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_698.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _698

        return self.__parent__._cast(_698.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_700.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _700

        return self.__parent__._cast(_700.BevelGearISOMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_704.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _704

        return self.__parent__._cast(_704.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_705.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _705

        return self.__parent__._cast(_705.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_707.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _707

        return self.__parent__._cast(_707.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_708.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _708

        return self.__parent__._cast(_708.CylindricalGearPlasticMaterialDatabase)

    @property
    def general_electric_machine_material_database(
        self: "CastSelf",
    ) -> "_1432.GeneralElectricMachineMaterialDatabase":
        from mastapy._private.electric_machines import _1432

        return self.__parent__._cast(_1432.GeneralElectricMachineMaterialDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1446.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1446

        return self.__parent__._cast(_1446.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1466.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1466

        return self.__parent__._cast(_1466.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1481.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1481

        return self.__parent__._cast(_1481.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1670.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1670

        return self.__parent__._cast(_1670.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1677.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1677

        return self.__parent__._cast(_1677.RingPinsMaterialDatabase)

    @property
    def material_database(self: "CastSelf") -> "MaterialDatabase":
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
class MaterialDatabase(_2061.NamedDatabase[T]):
    """MaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_MaterialDatabase
        """
        return _Cast_MaterialDatabase(self)
