"""PartCompoundHarmonicAnalysisOfSingleExcitation"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7943

_PART_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "PartCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2944
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7940
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6452,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6502,
        _6503,
        _6504,
        _6506,
        _6508,
        _6509,
        _6510,
        _6512,
        _6513,
        _6515,
        _6516,
        _6517,
        _6518,
        _6520,
        _6521,
        _6522,
        _6523,
        _6525,
        _6527,
        _6528,
        _6530,
        _6531,
        _6533,
        _6534,
        _6536,
        _6538,
        _6539,
        _6541,
        _6543,
        _6544,
        _6545,
        _6547,
        _6549,
        _6551,
        _6552,
        _6553,
        _6554,
        _6555,
        _6557,
        _6558,
        _6559,
        _6560,
        _6562,
        _6563,
        _6564,
        _6566,
        _6568,
        _6570,
        _6571,
        _6573,
        _6574,
        _6576,
        _6577,
        _6578,
        _6579,
        _6580,
        _6581,
        _6582,
        _6584,
        _6586,
        _6588,
        _6589,
        _6590,
        _6591,
        _6592,
        _6593,
        _6595,
        _6596,
        _6598,
        _6599,
        _6600,
        _6602,
        _6603,
        _6605,
        _6606,
        _6608,
        _6609,
        _6611,
        _6612,
        _6614,
        _6615,
        _6616,
        _6617,
        _6618,
        _6619,
        _6620,
        _6621,
        _6623,
        _6624,
        _6625,
        _6626,
        _6627,
        _6629,
        _6630,
        _6632,
    )

    Self = TypeVar("Self", bound="PartCompoundHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundHarmonicAnalysisOfSingleExcitation._Cast_PartCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting PartCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "PartCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7943.PartCompoundAnalysis":
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
    def abstract_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6502.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6502,
        )

        return self.__parent__._cast(
            _6502.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6503.AbstractShaftCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6503,
        )

        return self.__parent__._cast(
            _6503.AbstractShaftCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_or_housing_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6504.AbstractShaftOrHousingCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6504,
        )

        return self.__parent__._cast(
            _6504.AbstractShaftOrHousingCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6506.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6506,
        )

        return self.__parent__._cast(
            _6506.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6508.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6508,
        )

        return self.__parent__._cast(
            _6508.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6509.AssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6509,
        )

        return self.__parent__._cast(
            _6509.AssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bearing_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6510.BearingCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6510,
        )

        return self.__parent__._cast(
            _6510.BearingCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def belt_drive_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6512.BeltDriveCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6512,
        )

        return self.__parent__._cast(
            _6512.BeltDriveCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6513.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6513,
        )

        return self.__parent__._cast(
            _6513.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6515.BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6515,
        )

        return self.__parent__._cast(
            _6515.BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_planet_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6516.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6516,
        )

        return self.__parent__._cast(
            _6516.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_sun_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6517.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6517,
        )

        return self.__parent__._cast(
            _6517.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6518.BevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6518,
        )

        return self.__parent__._cast(
            _6518.BevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6520.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6520,
        )

        return self.__parent__._cast(
            _6520.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolt_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6521.BoltCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6521,
        )

        return self.__parent__._cast(
            _6521.BoltCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bolted_joint_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6522.BoltedJointCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6522,
        )

        return self.__parent__._cast(
            _6522.BoltedJointCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def clutch_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6523.ClutchCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6523,
        )

        return self.__parent__._cast(
            _6523.ClutchCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def clutch_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6525.ClutchHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6525,
        )

        return self.__parent__._cast(
            _6525.ClutchHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6527.ComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6527,
        )

        return self.__parent__._cast(
            _6527.ComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6528.ConceptCouplingCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6528,
        )

        return self.__parent__._cast(
            _6528.ConceptCouplingCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6530.ConceptCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6530,
        )

        return self.__parent__._cast(
            _6530.ConceptCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6531.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6531,
        )

        return self.__parent__._cast(
            _6531.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6533.ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6533,
        )

        return self.__parent__._cast(
            _6533.ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6534.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6534,
        )

        return self.__parent__._cast(
            _6534.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6536.ConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6536,
        )

        return self.__parent__._cast(
            _6536.ConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connector_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6538.ConnectorCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6538,
        )

        return self.__parent__._cast(
            _6538.ConnectorCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6539.CouplingCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6539,
        )

        return self.__parent__._cast(
            _6539.CouplingCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6541.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6541,
        )

        return self.__parent__._cast(
            _6541.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6543.CVTCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6543,
        )

        return self.__parent__._cast(
            _6543.CVTCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_pulley_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6544.CVTPulleyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6544,
        )

        return self.__parent__._cast(
            _6544.CVTPulleyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6545.CycloidalAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6545,
        )

        return self.__parent__._cast(
            _6545.CycloidalAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6547.CycloidalDiscCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6547,
        )

        return self.__parent__._cast(
            _6547.CycloidalDiscCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6549.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6549,
        )

        return self.__parent__._cast(
            _6549.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6551.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6551,
        )

        return self.__parent__._cast(
            _6551.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_planet_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6552.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6552,
        )

        return self.__parent__._cast(
            _6552.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def datum_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6553.DatumCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6553,
        )

        return self.__parent__._cast(
            _6553.DatumCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def external_cad_model_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6554.ExternalCADModelCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6554,
        )

        return self.__parent__._cast(
            _6554.ExternalCADModelCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6555.FaceGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6555,
        )

        return self.__parent__._cast(
            _6555.FaceGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6557.FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6557,
        )

        return self.__parent__._cast(
            _6557.FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def fe_part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6558.FEPartCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6558,
        )

        return self.__parent__._cast(
            _6558.FEPartCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def flexible_pin_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6559.FlexiblePinAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6559,
        )

        return self.__parent__._cast(
            _6559.FlexiblePinAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6560.GearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6560,
        )

        return self.__parent__._cast(
            _6560.GearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6562.GearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6562,
        )

        return self.__parent__._cast(
            _6562.GearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def guide_dxf_model_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6563.GuideDxfModelCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6563,
        )

        return self.__parent__._cast(
            _6563.GuideDxfModelCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6564.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6564,
        )

        return self.__parent__._cast(
            _6564.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6566.HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6566,
        )

        return self.__parent__._cast(
            _6566.HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6568.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6568,
        )

        return self.__parent__._cast(
            _6568.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6570.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6570,
        )

        return self.__parent__._cast(
            _6570.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6571.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6571,
        )

        return self.__parent__._cast(
            _6571.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6573.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6573,
        )

        return self.__parent__._cast(
            _6573.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6574.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6574,
        )

        return self.__parent__._cast(
            _6574.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6576.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6576,
        )

        return self.__parent__._cast(
            _6576.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mass_disc_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6577.MassDiscCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6577,
        )

        return self.__parent__._cast(
            _6577.MassDiscCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def measurement_component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6578.MeasurementComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6578,
        )

        return self.__parent__._cast(
            _6578.MeasurementComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_array_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6579.MicrophoneArrayCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6579,
        )

        return self.__parent__._cast(
            _6579.MicrophoneArrayCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6580.MicrophoneCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6580,
        )

        return self.__parent__._cast(
            _6580.MicrophoneCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mountable_component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6581.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6581,
        )

        return self.__parent__._cast(
            _6581.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def oil_seal_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6582.OilSealCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6582,
        )

        return self.__parent__._cast(
            _6582.OilSealCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6584.PartToPartShearCouplingCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6584,
        )

        return self.__parent__._cast(
            _6584.PartToPartShearCouplingCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6586.PartToPartShearCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6586,
        )

        return self.__parent__._cast(
            _6586.PartToPartShearCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6588.PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6588,
        )

        return self.__parent__._cast(
            _6588.PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planet_carrier_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6589.PlanetCarrierCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6589,
        )

        return self.__parent__._cast(
            _6589.PlanetCarrierCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def point_load_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6590.PointLoadCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6590,
        )

        return self.__parent__._cast(
            _6590.PointLoadCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def power_load_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6591.PowerLoadCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6591,
        )

        return self.__parent__._cast(
            _6591.PowerLoadCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def pulley_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6592.PulleyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6592,
        )

        return self.__parent__._cast(
            _6592.PulleyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def ring_pins_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6593.RingPinsCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6593,
        )

        return self.__parent__._cast(
            _6593.RingPinsCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6595.RollingRingAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6595,
        )

        return self.__parent__._cast(
            _6595.RollingRingAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6596.RollingRingCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6596,
        )

        return self.__parent__._cast(
            _6596.RollingRingCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def root_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6598.RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6598,
        )

        return self.__parent__._cast(
            _6598.RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6599.ShaftCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6599,
        )

        return self.__parent__._cast(
            _6599.ShaftCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_hub_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6600.ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6600,
        )

        return self.__parent__._cast(
            _6600.ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def specialised_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6602.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6602,
        )

        return self.__parent__._cast(
            _6602.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6603.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6603,
        )

        return self.__parent__._cast(
            _6603.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6605.SpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6605,
        )

        return self.__parent__._cast(
            _6605.SpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6606.SpringDamperCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6606,
        )

        return self.__parent__._cast(
            _6606.SpringDamperCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6608.SpringDamperHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6608,
        )

        return self.__parent__._cast(
            _6608.SpringDamperHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6609.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6609,
        )

        return self.__parent__._cast(
            _6609.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6611.StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6611,
        )

        return self.__parent__._cast(
            _6611.StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6612.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6612,
        )

        return self.__parent__._cast(
            _6612.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6614.StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6614,
        )

        return self.__parent__._cast(
            _6614.StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_planet_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6615.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6615,
        )

        return self.__parent__._cast(
            _6615.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_sun_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6616.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6616,
        )

        return self.__parent__._cast(
            _6616.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6617.SynchroniserCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6617,
        )

        return self.__parent__._cast(
            _6617.SynchroniserCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6618.SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6618,
        )

        return self.__parent__._cast(
            _6618.SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6619.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6619,
        )

        return self.__parent__._cast(
            _6619.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_sleeve_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6620.SynchroniserSleeveCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6620,
        )

        return self.__parent__._cast(
            _6620.SynchroniserSleeveCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6621.TorqueConverterCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6621,
        )

        return self.__parent__._cast(
            _6621.TorqueConverterCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_pump_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6623.TorqueConverterPumpCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6623,
        )

        return self.__parent__._cast(
            _6623.TorqueConverterPumpCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_turbine_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6624.TorqueConverterTurbineCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6624,
        )

        return self.__parent__._cast(
            _6624.TorqueConverterTurbineCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def unbalanced_mass_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6625.UnbalancedMassCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6625,
        )

        return self.__parent__._cast(
            _6625.UnbalancedMassCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def virtual_component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6626.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6626,
        )

        return self.__parent__._cast(
            _6626.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6627.WormGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6627,
        )

        return self.__parent__._cast(
            _6627.WormGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6629.WormGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6629,
        )

        return self.__parent__._cast(
            _6629.WormGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6630.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6630,
        )

        return self.__parent__._cast(
            _6630.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_set_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6632.ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6632,
        )

        return self.__parent__._cast(
            _6632.ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "PartCompoundHarmonicAnalysisOfSingleExcitation":
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
class PartCompoundHarmonicAnalysisOfSingleExcitation(_7943.PartCompoundAnalysis):
    """PartCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6452.PartHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.PartHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6452.PartHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.PartHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PartCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_PartCompoundHarmonicAnalysisOfSingleExcitation(self)
