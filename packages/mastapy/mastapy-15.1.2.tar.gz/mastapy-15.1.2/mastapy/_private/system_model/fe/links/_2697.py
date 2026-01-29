"""PlanetBasedFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.fe.links import _2695

_PLANET_BASED_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "PlanetBasedFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2687, _2692, _2696, _2698

    Self = TypeVar("Self", bound="PlanetBasedFELink")
    CastSelf = TypeVar("CastSelf", bound="PlanetBasedFELink._Cast_PlanetBasedFELink")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetBasedFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetBasedFELink:
    """Special nested class for casting PlanetBasedFELink to subclasses."""

    __parent__: "PlanetBasedFELink"

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2695.MultiNodeFELink":
        return self.__parent__._cast(_2695.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2687.FELink":
        from mastapy._private.system_model.fe.links import _2687

        return self.__parent__._cast(_2687.FELink)

    @property
    def gear_with_duplicated_meshes_fe_link(
        self: "CastSelf",
    ) -> "_2692.GearWithDuplicatedMeshesFELink":
        from mastapy._private.system_model.fe.links import _2692

        return self.__parent__._cast(_2692.GearWithDuplicatedMeshesFELink)

    @property
    def planetary_connector_multi_node_fe_link(
        self: "CastSelf",
    ) -> "_2696.PlanetaryConnectorMultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2696

        return self.__parent__._cast(_2696.PlanetaryConnectorMultiNodeFELink)

    @property
    def planet_carrier_fe_link(self: "CastSelf") -> "_2698.PlanetCarrierFELink":
        from mastapy._private.system_model.fe.links import _2698

        return self.__parent__._cast(_2698.PlanetCarrierFELink)

    @property
    def planet_based_fe_link(self: "CastSelf") -> "PlanetBasedFELink":
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
class PlanetBasedFELink(_2695.MultiNodeFELink):
    """PlanetBasedFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_BASED_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetBasedFELink":
        """Cast to another type.

        Returns:
            _Cast_PlanetBasedFELink
        """
        return _Cast_PlanetBasedFELink(self)
