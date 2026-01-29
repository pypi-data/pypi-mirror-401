"""AbstractStaticLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private.system_model.analyses_and_results.load_case_groups import _6002
from mastapy._private.system_model.analyses_and_results.static_loads import (
    _7741,
    _7783,
    _7785,
    _7787,
    _7809,
    _7812,
    _7814,
    _7817,
    _7862,
    _7863,
)
from mastapy._private.system_model.connections_and_sockets.gears import _2569, _2573
from mastapy._private.system_model.part_model import _2709, _2725, _2747, _2748
from mastapy._private.system_model.part_model.gears import _2807, _2808, _2812, _2814

_ABSTRACT_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "AbstractStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import (
        _2940,
        _2951,
        _2953,
        _2954,
        _2961,
        _2964,
        _2969,
        _2970,
        _2971,
        _2974,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _6001,
        _6006,
        _6007,
        _6010,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _6016,
        _6019,
        _6020,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7727,
        _7739,
    )

    Self = TypeVar("Self", bound="AbstractStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractStaticLoadCaseGroup._Cast_AbstractStaticLoadCaseGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractStaticLoadCaseGroup:
    """Special nested class for casting AbstractStaticLoadCaseGroup to subclasses."""

    __parent__: "AbstractStaticLoadCaseGroup"

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_6002.AbstractLoadCaseGroup":
        return self.__parent__._cast(_6002.AbstractLoadCaseGroup)

    @property
    def abstract_design_state_load_case_group(
        self: "CastSelf",
    ) -> "_6001.AbstractDesignStateLoadCaseGroup":
        return self.__parent__._cast(_6001.AbstractDesignStateLoadCaseGroup)

    @property
    def design_state(self: "CastSelf") -> "_6006.DesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _6006,
        )

        return self.__parent__._cast(_6006.DesignState)

    @property
    def duty_cycle(self: "CastSelf") -> "_6007.DutyCycle":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _6007,
        )

        return self.__parent__._cast(_6007.DutyCycle)

    @property
    def sub_group_in_single_design_state(
        self: "CastSelf",
    ) -> "_6010.SubGroupInSingleDesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _6010,
        )

        return self.__parent__._cast(_6010.SubGroupInSingleDesignState)

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "AbstractStaticLoadCaseGroup":
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
class AbstractStaticLoadCaseGroup(_6002.AbstractLoadCaseGroup):
    """AbstractStaticLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def max_number_of_load_cases_to_display(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaxNumberOfLoadCasesToDisplay")

        if temp is None:
            return 0

        return temp

    @max_number_of_load_cases_to_display.setter
    @exception_bridge
    @enforce_parameter_types
    def max_number_of_load_cases_to_display(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaxNumberOfLoadCasesToDisplay",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def bearings(
        self: "Self",
    ) -> (
        "List[_6016.ComponentStaticLoadCaseGroup[_2709.Bearing, _7741.BearingLoadCase]]"
    ):
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ComponentStaticLoadCaseGroup[mastapy.system_model.part_model.Bearing, mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gear_sets(
        self: "Self",
    ) -> "List[_6019.GearSetStaticLoadCaseGroup[_2808.CylindricalGearSet, _2807.CylindricalGear, _7783.CylindricalGearLoadCase, _2569.CylindricalGearMesh, _7785.CylindricalGearMeshLoadCase, _7787.CylindricalGearSetLoadCase]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.GearSetStaticLoadCaseGroup[mastapy.system_model.part_model.gears.CylindricalGearSet, mastapy.system_model.part_model.gears.CylindricalGear, mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase, mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh, mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase, mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def design_states(self: "Self") -> "List[_6001.AbstractDesignStateLoadCaseGroup]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.AbstractDesignStateLoadCaseGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignStates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def fe_parts(
        self: "Self",
    ) -> "List[_6016.ComponentStaticLoadCaseGroup[_2725.FEPart, _7809.FEPartLoadCase]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ComponentStaticLoadCaseGroup[mastapy.system_model.part_model.FEPart, mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_sets(
        self: "Self",
    ) -> "List[_6019.GearSetStaticLoadCaseGroup[_2814.GearSet, _2812.Gear, _7812.GearLoadCase, _2573.GearMesh, _7814.GearMeshLoadCase, _7817.GearSetLoadCase]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.GearSetStaticLoadCaseGroup[mastapy.system_model.part_model.gears.GearSet, mastapy.system_model.part_model.gears.Gear, mastapy.system_model.analyses_and_results.static_loads.GearLoadCase, mastapy.system_model.connections_and_sockets.gears.GearMesh, mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase, mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def parts_with_excitations(self: "Self") -> "List[_6020.PartStaticLoadCaseGroup]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.PartStaticLoadCaseGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartsWithExcitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def point_loads(
        self: "Self",
    ) -> "List[_6016.ComponentStaticLoadCaseGroup[_2747.PointLoad, _7862.PointLoadLoadCase]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ComponentStaticLoadCaseGroup[mastapy.system_model.part_model.PointLoad, mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def power_loads(
        self: "Self",
    ) -> "List[_6016.ComponentStaticLoadCaseGroup[_2748.PowerLoad, _7863.PowerLoadLoadCase]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ComponentStaticLoadCaseGroup[mastapy.system_model.part_model.PowerLoad, mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def static_loads(self: "Self") -> "List[_7727.StaticLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def static_loads_limited_by_max_number_of_load_cases_to_display(
        self: "Self",
    ) -> "List[_7727.StaticLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def compound_system_deflection(self: "Self") -> "_2974.CompoundSystemDeflection":
        """mastapy.system_model.analyses_and_results.CompoundSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundSystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_power_flow(self: "Self") -> "_2969.CompoundPowerFlow":
        """mastapy.system_model.analyses_and_results.CompoundPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundPowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_advanced_system_deflection(
        self: "Self",
    ) -> "_2951.CompoundAdvancedSystemDeflection":
        """mastapy.system_model.analyses_and_results.CompoundAdvancedSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundAdvancedSystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_harmonic_analysis(self: "Self") -> "_2961.CompoundHarmonicAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundHarmonicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundHarmonicAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_steady_state_synchronous_response(
        self: "Self",
    ) -> "_2971.CompoundSteadyStateSynchronousResponse":
        """mastapy.system_model.analyses_and_results.CompoundSteadyStateSynchronousResponse

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CompoundSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_modal_analysis(self: "Self") -> "_2964.CompoundModalAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_critical_speed_analysis(
        self: "Self",
    ) -> "_2954.CompoundCriticalSpeedAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundCriticalSpeedAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundCriticalSpeedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_stability_analysis(self: "Self") -> "_2970.CompoundStabilityAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundStabilityAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundStabilityAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def compound_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "_2953.CompoundAdvancedTimeSteppingAnalysisForModulation":
        """mastapy.system_model.analyses_and_results.CompoundAdvancedTimeSteppingAnalysisForModulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CompoundAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def clear_user_specified_excitation_data_for_all_load_cases(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForAllLoadCases"
        )

    @exception_bridge
    def run_power_flow(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RunPowerFlow")

    @exception_bridge
    def set_face_widths_for_specified_safety_factors_from_power_flow(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow"
        )

    @exception_bridge
    @enforce_parameter_types
    def analysis_of(
        self: "Self", analysis_type: "_7739.AnalysisType"
    ) -> "_2940.CompoundAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundAnalysis

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)
        """
        analysis_type = conversion.mp_to_pn_enum(
            analysis_type,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.AnalysisType",
        )
        method_result = pythonnet_method_call(self.wrapped, "AnalysisOf", analysis_type)
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_AbstractStaticLoadCaseGroup
        """
        return _Cast_AbstractStaticLoadCaseGroup(self)
