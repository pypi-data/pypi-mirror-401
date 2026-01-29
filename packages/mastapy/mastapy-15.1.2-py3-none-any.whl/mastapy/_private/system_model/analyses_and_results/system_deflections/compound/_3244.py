"""RootAssemblyCompoundSystemDeflection"""

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

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3154,
)

_ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "RootAssemblyCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1235
    from mastapy._private.system_model.analyses_and_results import _2944
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7940,
        _7943,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4579,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3095,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3147,
        _3199,
        _3229,
    )
    from mastapy._private.system_model.fe import _2675
    from mastapy._private.utility_gui.charts import _2105

    Self = TypeVar("Self", bound="RootAssemblyCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundSystemDeflection:
    """Special nested class for casting RootAssemblyCompoundSystemDeflection to subclasses."""

    __parent__: "RootAssemblyCompoundSystemDeflection"

    @property
    def assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3154.AssemblyCompoundSystemDeflection":
        return self.__parent__._cast(_3154.AssemblyCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3147.AbstractAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3147,
        )

        return self.__parent__._cast(_3147.AbstractAssemblyCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3229.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3229,
        )

        return self.__parent__._cast(_3229.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7943.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7943,
        )

        return self.__parent__._cast(_7943.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7940.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7940,
        )

        return self.__parent__._cast(_7940.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2944.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2944

        return self.__parent__._cast(_2944.DesignEntityAnalysis)

    @property
    def root_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundSystemDeflection":
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
class RootAssemblyCompoundSystemDeflection(_3154.AssemblyCompoundSystemDeflection):
    """RootAssemblyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duty_cycle_efficiency_results(
        self: "Self",
    ) -> "_3199.DutyCycleEfficiencyResults":
        """mastapy.system_model.analyses_and_results.system_deflections.compound.DutyCycleEfficiencyResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleEfficiencyResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_assembly_compound_power_flow(
        self: "Self",
    ) -> "_4579.RootAssemblyCompoundPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.compound.RootAssemblyCompoundPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootAssemblyCompoundPowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3095.RootAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bearing_race_f_es(self: "Self") -> "List[_2675.RaceBearingFESystemDeflection]":
        """List[mastapy.system_model.fe.RaceBearingFESystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingRaceFEs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3095.RootAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def peak_to_peak_transmission_error_chart(
        self: "Self",
        mesh_duty_cycles: "List[_1235.CylindricalGearMeshMicroGeometryDutyCycle]",
        header: "str",
        x_axis_title: "str",
        y_axis_title: "str",
    ) -> "_2105.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Args:
            mesh_duty_cycles (List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometryDutyCycle])
            header (str)
            x_axis_title (str)
            y_axis_title (str)
        """
        mesh_duty_cycles = conversion.mp_to_pn_objects_in_dotnet_list(mesh_duty_cycles)
        header = str(header)
        x_axis_title = str(x_axis_title)
        y_axis_title = str(y_axis_title)
        method_result = pythonnet_method_call(
            self.wrapped,
            "PeakToPeakTransmissionErrorChart",
            mesh_duty_cycles,
            header if header else "",
            x_axis_title if x_axis_title else "",
            y_axis_title if y_axis_title else "",
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssemblyCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundSystemDeflection
        """
        return _Cast_RootAssemblyCompoundSystemDeflection(self)
