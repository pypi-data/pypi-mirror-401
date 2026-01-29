"""InterMountableComponentConnectionCompoundCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _7081,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
        "InterMountableComponentConnectionCompoundCriticalSpeedAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2944
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7936,
        _7940,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6980,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _7051,
        _7055,
        _7058,
        _7063,
        _7068,
        _7073,
        _7076,
        _7079,
        _7084,
        _7086,
        _7094,
        _7100,
        _7105,
        _7109,
        _7113,
        _7116,
        _7119,
        _7129,
        _7138,
        _7141,
        _7148,
        _7151,
        _7154,
        _7157,
        _7166,
        _7172,
        _7175,
    )

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionCompoundCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundCriticalSpeedAnalysis._Cast_InterMountableComponentConnectionCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundCriticalSpeedAnalysis:
    """Special nested class for casting InterMountableComponentConnectionCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundCriticalSpeedAnalysis"

    @property
    def connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7081.ConnectionCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_7081.ConnectionCompoundCriticalSpeedAnalysis)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7936.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7936,
        )

        return self.__parent__._cast(_7936.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7051.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7051,
        )

        return self.__parent__._cast(
            _7051.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def belt_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7055.BeltConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7055,
        )

        return self.__parent__._cast(_7055.BeltConnectionCompoundCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7058.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7058,
        )

        return self.__parent__._cast(
            _7058.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7063.BevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7063,
        )

        return self.__parent__._cast(_7063.BevelGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def clutch_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7068.ClutchConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7068,
        )

        return self.__parent__._cast(
            _7068.ClutchConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7073.ConceptCouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7073,
        )

        return self.__parent__._cast(
            _7073.ConceptCouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7076.ConceptGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7076,
        )

        return self.__parent__._cast(_7076.ConceptGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7079.ConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7079,
        )

        return self.__parent__._cast(_7079.ConicalGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7084.CouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7084,
        )

        return self.__parent__._cast(
            _7084.CouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cvt_belt_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7086.CVTBeltConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7086,
        )

        return self.__parent__._cast(
            _7086.CVTBeltConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7094.CylindricalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7094,
        )

        return self.__parent__._cast(
            _7094.CylindricalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7100.FaceGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7100,
        )

        return self.__parent__._cast(_7100.FaceGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7105.GearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7105,
        )

        return self.__parent__._cast(_7105.GearMeshCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7109.HypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7109,
        )

        return self.__parent__._cast(_7109.HypoidGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7113.KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7113,
        )

        return self.__parent__._cast(
            _7113.KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7116.KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7116,
        )

        return self.__parent__._cast(
            _7116.KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_7119.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7119,
        )

        return self.__parent__._cast(
            _7119.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7129.PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7129,
        )

        return self.__parent__._cast(
            _7129.PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def ring_pins_to_disc_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7138.RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7138,
        )

        return self.__parent__._cast(
            _7138.RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7141.RollingRingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7141,
        )

        return self.__parent__._cast(
            _7141.RollingRingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7148.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7148,
        )

        return self.__parent__._cast(
            _7148.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def spring_damper_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7151.SpringDamperConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7151,
        )

        return self.__parent__._cast(
            _7151.SpringDamperConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7154.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7154,
        )

        return self.__parent__._cast(
            _7154.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7157.StraightBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7157,
        )

        return self.__parent__._cast(
            _7157.StraightBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def torque_converter_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7166.TorqueConverterConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7166,
        )

        return self.__parent__._cast(
            _7166.TorqueConverterConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7172.WormGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7172,
        )

        return self.__parent__._cast(_7172.WormGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7175.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7175,
        )

        return self.__parent__._cast(
            _7175.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def inter_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundCriticalSpeedAnalysis":
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
class InterMountableComponentConnectionCompoundCriticalSpeedAnalysis(
    _7081.ConnectionCompoundCriticalSpeedAnalysis
):
    """InterMountableComponentConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6980.InterMountableComponentConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.InterMountableComponentConnectionCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6980.InterMountableComponentConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.InterMountableComponentConnectionCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
        """
        return _Cast_InterMountableComponentConnectionCompoundCriticalSpeedAnalysis(
            self
        )
