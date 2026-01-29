"""ElementPropertiesShellIntegrationRule"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_SHELL_INTEGRATION_RULE = python_net_import(
    "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums",
    "ElementPropertiesShellIntegrationRule",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementPropertiesShellIntegrationRule")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementPropertiesShellIntegrationRule._Cast_ElementPropertiesShellIntegrationRule",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesShellIntegrationRule",)


class ElementPropertiesShellIntegrationRule(Enum):
    """ElementPropertiesShellIntegrationRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELEMENT_PROPERTIES_SHELL_INTEGRATION_RULE

    GAUSSIAN = 1
    LOBATTO = 2
    SIMPSON = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElementPropertiesShellIntegrationRule.__setattr__ = __enum_setattr
ElementPropertiesShellIntegrationRule.__delattr__ = __enum_delattr
