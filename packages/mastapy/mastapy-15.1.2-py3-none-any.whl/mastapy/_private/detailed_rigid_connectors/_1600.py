"""DetailedRigidConnectorDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import conversion, utility

_DETAILED_RIGID_CONNECTOR_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors", "DetailedRigidConnectorDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    from mastapy._private.detailed_rigid_connectors import _1601
    from mastapy._private.detailed_rigid_connectors.interference_fits import _1658
    from mastapy._private.detailed_rigid_connectors.keyed_joints import _1650
    from mastapy._private.detailed_rigid_connectors.splines import (
        _1603,
        _1606,
        _1610,
        _1613,
        _1614,
        _1621,
        _1628,
        _1633,
    )

    Self = TypeVar("Self", bound="DetailedRigidConnectorDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DetailedRigidConnectorDesign._Cast_DetailedRigidConnectorDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DetailedRigidConnectorDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedRigidConnectorDesign:
    """Special nested class for casting DetailedRigidConnectorDesign to subclasses."""

    __parent__: "DetailedRigidConnectorDesign"

    @property
    def custom_spline_joint_design(self: "CastSelf") -> "_1603.CustomSplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1603

        return self.__parent__._cast(_1603.CustomSplineJointDesign)

    @property
    def din5480_spline_joint_design(
        self: "CastSelf",
    ) -> "_1606.DIN5480SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1606

        return self.__parent__._cast(_1606.DIN5480SplineJointDesign)

    @property
    def gbt3478_spline_joint_design(
        self: "CastSelf",
    ) -> "_1610.GBT3478SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1610

        return self.__parent__._cast(_1610.GBT3478SplineJointDesign)

    @property
    def iso4156_spline_joint_design(
        self: "CastSelf",
    ) -> "_1613.ISO4156SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1613

        return self.__parent__._cast(_1613.ISO4156SplineJointDesign)

    @property
    def jisb1603_spline_joint_design(
        self: "CastSelf",
    ) -> "_1614.JISB1603SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1614

        return self.__parent__._cast(_1614.JISB1603SplineJointDesign)

    @property
    def sae_spline_joint_design(self: "CastSelf") -> "_1621.SAESplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1621

        return self.__parent__._cast(_1621.SAESplineJointDesign)

    @property
    def spline_joint_design(self: "CastSelf") -> "_1628.SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1628

        return self.__parent__._cast(_1628.SplineJointDesign)

    @property
    def standard_spline_joint_design(
        self: "CastSelf",
    ) -> "_1633.StandardSplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1633

        return self.__parent__._cast(_1633.StandardSplineJointDesign)

    @property
    def keyed_joint_design(self: "CastSelf") -> "_1650.KeyedJointDesign":
        from mastapy._private.detailed_rigid_connectors.keyed_joints import _1650

        return self.__parent__._cast(_1650.KeyedJointDesign)

    @property
    def interference_fit_design(self: "CastSelf") -> "_1658.InterferenceFitDesign":
        from mastapy._private.detailed_rigid_connectors.interference_fits import _1658

        return self.__parent__._cast(_1658.InterferenceFitDesign)

    @property
    def detailed_rigid_connector_design(
        self: "CastSelf",
    ) -> "DetailedRigidConnectorDesign":
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
class DetailedRigidConnectorDesign(_0.APIBase):
    """DetailedRigidConnectorDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_RIGID_CONNECTOR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_spline_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDSplineDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def length_of_engagement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfEngagement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def halves(self: "Self") -> "List[_1601.DetailedRigidConnectorHalfDesign]":
        """List[mastapy.detailed_rigid_connectors.DetailedRigidConnectorHalfDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Halves")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedRigidConnectorDesign":
        """Cast to another type.

        Returns:
            _Cast_DetailedRigidConnectorDesign
        """
        return _Cast_DetailedRigidConnectorDesign(self)
