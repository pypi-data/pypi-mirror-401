"""RealMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import conversion, utility
from mastapy._private.math_utility import _1727

_REAL_MATRIX = python_net_import("SMT.MastaAPI.MathUtility", "RealMatrix")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1722, _1741, _1743, _1748, _1752

    Self = TypeVar("Self", bound="RealMatrix")
    CastSelf = TypeVar("CastSelf", bound="RealMatrix._Cast_RealMatrix")


__docformat__ = "restructuredtext en"
__all__ = ("RealMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealMatrix:
    """Special nested class for casting RealMatrix to subclasses."""

    __parent__: "RealMatrix"

    @property
    def generic_matrix(self: "CastSelf") -> "_1727.GenericMatrix":
        pass

        return self.__parent__._cast(_1727.GenericMatrix)

    @property
    def euler_parameters(self: "CastSelf") -> "_1722.EulerParameters":
        from mastapy._private.math_utility import _1722

        return self.__parent__._cast(_1722.EulerParameters)

    @property
    def quaternion(self: "CastSelf") -> "_1741.Quaternion":
        from mastapy._private.math_utility import _1741

        return self.__parent__._cast(_1741.Quaternion)

    @property
    def real_vector(self: "CastSelf") -> "_1743.RealVector":
        from mastapy._private.math_utility import _1743

        return self.__parent__._cast(_1743.RealVector)

    @property
    def square_matrix(self: "CastSelf") -> "_1748.SquareMatrix":
        from mastapy._private.math_utility import _1748

        return self.__parent__._cast(_1748.SquareMatrix)

    @property
    def vector_6d(self: "CastSelf") -> "_1752.Vector6D":
        from mastapy._private.math_utility import _1752

        return self.__parent__._cast(_1752.Vector6D)

    @property
    def real_matrix(self: "CastSelf") -> "RealMatrix":
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
class RealMatrix(_1727.GenericMatrix[float, "RealMatrix"]):
    """RealMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def get_column_at(self: "Self", index: "int") -> "List[float]":
        """List[float]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.to_list_any(
            pythonnet_method_call(self.wrapped, "GetColumnAt", index if index else 0)
        )

    @exception_bridge
    @enforce_parameter_types
    def get_row_at(self: "Self", index: "int") -> "List[float]":
        """List[float]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.to_list_any(
            pythonnet_method_call(self.wrapped, "GetRowAt", index if index else 0)
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RealMatrix":
        """Cast to another type.

        Returns:
            _Cast_RealMatrix
        """
        return _Cast_RealMatrix(self)
