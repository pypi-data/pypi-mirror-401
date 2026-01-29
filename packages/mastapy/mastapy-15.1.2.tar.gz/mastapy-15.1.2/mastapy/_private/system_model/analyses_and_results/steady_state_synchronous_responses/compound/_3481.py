"""InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3451,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2944
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7936,
        _7940,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3347,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3421,
        _3425,
        _3428,
        _3433,
        _3438,
        _3443,
        _3446,
        _3449,
        _3454,
        _3456,
        _3464,
        _3470,
        _3475,
        _3479,
        _3483,
        _3486,
        _3489,
        _3499,
        _3508,
        _3511,
        _3518,
        _3521,
        _3524,
        _3527,
        _3536,
        _3542,
        _3545,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse._Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: (
        "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    )

    @property
    def connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3451.ConnectionCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3451.ConnectionCompoundSteadyStateSynchronousResponse
        )

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
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3421.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3421,
        )

        return self.__parent__._cast(
            _3421.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3425.BeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3425,
        )

        return self.__parent__._cast(
            _3425.BeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3428.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3428,
        )

        return self.__parent__._cast(
            _3428.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3433.BevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3433,
        )

        return self.__parent__._cast(
            _3433.BevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3438.ClutchConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3438,
        )

        return self.__parent__._cast(
            _3438.ClutchConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3443.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3443,
        )

        return self.__parent__._cast(
            _3443.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3446.ConceptGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3446,
        )

        return self.__parent__._cast(
            _3446.ConceptGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3449.ConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3449,
        )

        return self.__parent__._cast(
            _3449.ConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3454.CouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3454,
        )

        return self.__parent__._cast(
            _3454.CouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3456.CVTBeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3456,
        )

        return self.__parent__._cast(
            _3456.CVTBeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3464.CylindricalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3464,
        )

        return self.__parent__._cast(
            _3464.CylindricalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3470.FaceGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3470,
        )

        return self.__parent__._cast(
            _3470.FaceGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3475.GearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3475,
        )

        return self.__parent__._cast(
            _3475.GearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3479.HypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3479,
        )

        return self.__parent__._cast(
            _3479.HypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3483.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3483,
        )

        return self.__parent__._cast(
            _3483.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3486.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3486,
        )

        return self.__parent__._cast(
            _3486.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3489.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3489,
        )

        return self.__parent__._cast(
            _3489.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3499.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3499,
        )

        return self.__parent__._cast(
            _3499.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3508.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3508,
        )

        return self.__parent__._cast(
            _3508.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3511.RollingRingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3511,
        )

        return self.__parent__._cast(
            _3511.RollingRingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3518.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3518,
        )

        return self.__parent__._cast(
            _3518.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3521.SpringDamperConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3521,
        )

        return self.__parent__._cast(
            _3521.SpringDamperConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3524.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3524,
        )

        return self.__parent__._cast(
            _3524.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3527.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3527,
        )

        return self.__parent__._cast(
            _3527.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3536.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3536,
        )

        return self.__parent__._cast(
            _3536.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3542.WormGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3542,
        )

        return self.__parent__._cast(
            _3542.WormGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3545.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3545,
        )

        return self.__parent__._cast(
            _3545.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
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
class InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
    _3451.ConnectionCompoundSteadyStateSynchronousResponse
):
    """InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
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
    ) -> "List[_3347.InterMountableComponentConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.InterMountableComponentConnectionSteadyStateSynchronousResponse]

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
    ) -> "List[_3347.InterMountableComponentConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.InterMountableComponentConnectionSteadyStateSynchronousResponse]

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
    ) -> (
        "_Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    ):
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        """
        return _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
            self
        )
