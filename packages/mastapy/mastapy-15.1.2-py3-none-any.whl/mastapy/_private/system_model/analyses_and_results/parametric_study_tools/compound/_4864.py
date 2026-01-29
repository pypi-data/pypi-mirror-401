"""SpecialisedAssemblyCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

from mastapy._private._internal import conversion, utility
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4764,
)

_SPECIALISED_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "SpecialisedAssemblyCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2944
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7940,
        _7943,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4733,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4770,
        _4774,
        _4777,
        _4782,
        _4784,
        _4785,
        _4790,
        _4795,
        _4798,
        _4801,
        _4805,
        _4807,
        _4813,
        _4819,
        _4821,
        _4824,
        _4828,
        _4832,
        _4835,
        _4838,
        _4841,
        _4845,
        _4846,
        _4850,
        _4857,
        _4867,
        _4868,
        _4873,
        _4876,
        _4879,
        _4883,
        _4891,
        _4894,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundParametricStudyTool._Cast_SpecialisedAssemblyCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundParametricStudyTool:
    """Special nested class for casting SpecialisedAssemblyCompoundParametricStudyTool to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundParametricStudyTool"

    @property
    def abstract_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4764.AbstractAssemblyCompoundParametricStudyTool":
        return self.__parent__._cast(_4764.AbstractAssemblyCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4845.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4845,
        )

        return self.__parent__._cast(_4845.PartCompoundParametricStudyTool)

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
    def agma_gleason_conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4770.AGMAGleasonConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4770,
        )

        return self.__parent__._cast(
            _4770.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        )

    @property
    def belt_drive_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4774.BeltDriveCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4774,
        )

        return self.__parent__._cast(_4774.BeltDriveCompoundParametricStudyTool)

    @property
    def bevel_differential_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4777.BevelDifferentialGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4777,
        )

        return self.__parent__._cast(
            _4777.BevelDifferentialGearSetCompoundParametricStudyTool
        )

    @property
    def bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4782.BevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4782,
        )

        return self.__parent__._cast(_4782.BevelGearSetCompoundParametricStudyTool)

    @property
    def bolted_joint_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4784.BoltedJointCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4784,
        )

        return self.__parent__._cast(_4784.BoltedJointCompoundParametricStudyTool)

    @property
    def clutch_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4785.ClutchCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4785,
        )

        return self.__parent__._cast(_4785.ClutchCompoundParametricStudyTool)

    @property
    def concept_coupling_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4790.ConceptCouplingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4790,
        )

        return self.__parent__._cast(_4790.ConceptCouplingCompoundParametricStudyTool)

    @property
    def concept_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4795.ConceptGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4795,
        )

        return self.__parent__._cast(_4795.ConceptGearSetCompoundParametricStudyTool)

    @property
    def conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4798.ConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4798,
        )

        return self.__parent__._cast(_4798.ConicalGearSetCompoundParametricStudyTool)

    @property
    def coupling_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4801.CouplingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4801,
        )

        return self.__parent__._cast(_4801.CouplingCompoundParametricStudyTool)

    @property
    def cvt_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4805.CVTCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4805,
        )

        return self.__parent__._cast(_4805.CVTCompoundParametricStudyTool)

    @property
    def cycloidal_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4807.CycloidalAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4807,
        )

        return self.__parent__._cast(_4807.CycloidalAssemblyCompoundParametricStudyTool)

    @property
    def cylindrical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4813.CylindricalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4813,
        )

        return self.__parent__._cast(
            _4813.CylindricalGearSetCompoundParametricStudyTool
        )

    @property
    def face_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4819.FaceGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4819,
        )

        return self.__parent__._cast(_4819.FaceGearSetCompoundParametricStudyTool)

    @property
    def flexible_pin_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4821.FlexiblePinAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4821,
        )

        return self.__parent__._cast(
            _4821.FlexiblePinAssemblyCompoundParametricStudyTool
        )

    @property
    def gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4824.GearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4824,
        )

        return self.__parent__._cast(_4824.GearSetCompoundParametricStudyTool)

    @property
    def hypoid_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4828.HypoidGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4828,
        )

        return self.__parent__._cast(_4828.HypoidGearSetCompoundParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4832.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4832,
        )

        return self.__parent__._cast(
            _4832.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4835.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4835,
        )

        return self.__parent__._cast(
            _4835.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4838.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4838,
        )

        return self.__parent__._cast(
            _4838.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool
        )

    @property
    def microphone_array_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4841.MicrophoneArrayCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4841,
        )

        return self.__parent__._cast(_4841.MicrophoneArrayCompoundParametricStudyTool)

    @property
    def part_to_part_shear_coupling_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4846.PartToPartShearCouplingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4846,
        )

        return self.__parent__._cast(
            _4846.PartToPartShearCouplingCompoundParametricStudyTool
        )

    @property
    def planetary_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4850.PlanetaryGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4850,
        )

        return self.__parent__._cast(_4850.PlanetaryGearSetCompoundParametricStudyTool)

    @property
    def rolling_ring_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4857.RollingRingAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4857,
        )

        return self.__parent__._cast(
            _4857.RollingRingAssemblyCompoundParametricStudyTool
        )

    @property
    def spiral_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4867.SpiralBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4867,
        )

        return self.__parent__._cast(
            _4867.SpiralBevelGearSetCompoundParametricStudyTool
        )

    @property
    def spring_damper_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4868.SpringDamperCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4868,
        )

        return self.__parent__._cast(_4868.SpringDamperCompoundParametricStudyTool)

    @property
    def straight_bevel_diff_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4873.StraightBevelDiffGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4873,
        )

        return self.__parent__._cast(
            _4873.StraightBevelDiffGearSetCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4876.StraightBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4876,
        )

        return self.__parent__._cast(
            _4876.StraightBevelGearSetCompoundParametricStudyTool
        )

    @property
    def synchroniser_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4879.SynchroniserCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4879,
        )

        return self.__parent__._cast(_4879.SynchroniserCompoundParametricStudyTool)

    @property
    def torque_converter_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4883.TorqueConverterCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4883,
        )

        return self.__parent__._cast(_4883.TorqueConverterCompoundParametricStudyTool)

    @property
    def worm_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4891.WormGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4891,
        )

        return self.__parent__._cast(_4891.WormGearSetCompoundParametricStudyTool)

    @property
    def zerol_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4894.ZerolBevelGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4894,
        )

        return self.__parent__._cast(_4894.ZerolBevelGearSetCompoundParametricStudyTool)

    @property
    def specialised_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundParametricStudyTool":
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
class SpecialisedAssemblyCompoundParametricStudyTool(
    _4764.AbstractAssemblyCompoundParametricStudyTool
):
    """SpecialisedAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4733.SpecialisedAssemblyParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool]

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

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4733.SpecialisedAssemblyParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundParametricStudyTool
        """
        return _Cast_SpecialisedAssemblyCompoundParametricStudyTool(self)
