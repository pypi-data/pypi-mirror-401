"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results._2940 import (
        CompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2941 import (
        AnalysisCaseVariable,
    )
    from mastapy._private.system_model.analyses_and_results._2942 import (
        ConnectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2943 import Context
    from mastapy._private.system_model.analyses_and_results._2944 import (
        DesignEntityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2945 import (
        DesignEntityGroupAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2946 import (
        DesignEntitySingleContextAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2950 import PartAnalysis
    from mastapy._private.system_model.analyses_and_results._2951 import (
        CompoundAdvancedSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results._2952 import (
        CompoundAdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2953 import (
        CompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2954 import (
        CompoundCriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2955 import (
        CompoundDynamicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2956 import (
        CompoundDynamicModelAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2957 import (
        CompoundDynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2958 import (
        CompoundDynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2959 import (
        CompoundDynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2960 import (
        CompoundDynamicModelForSteadyStateSynchronousResponse,
    )
    from mastapy._private.system_model.analyses_and_results._2961 import (
        CompoundHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2962 import (
        CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2963 import (
        CompoundHarmonicAnalysisOfSingleExcitation,
    )
    from mastapy._private.system_model.analyses_and_results._2964 import (
        CompoundModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2965 import (
        CompoundModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2966 import (
        CompoundModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2967 import (
        CompoundModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2968 import (
        CompoundMultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2969 import (
        CompoundPowerFlow,
    )
    from mastapy._private.system_model.analyses_and_results._2970 import (
        CompoundStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2971 import (
        CompoundSteadyStateSynchronousResponse,
    )
    from mastapy._private.system_model.analyses_and_results._2972 import (
        CompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2973 import (
        CompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from mastapy._private.system_model.analyses_and_results._2974 import (
        CompoundSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results._2975 import (
        CompoundTorsionalSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results._2976 import (
        TESetUpForDynamicAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results._2977 import TimeOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results._2940": ["CompoundAnalysis"],
        "_private.system_model.analyses_and_results._2941": ["AnalysisCaseVariable"],
        "_private.system_model.analyses_and_results._2942": ["ConnectionAnalysis"],
        "_private.system_model.analyses_and_results._2943": ["Context"],
        "_private.system_model.analyses_and_results._2944": ["DesignEntityAnalysis"],
        "_private.system_model.analyses_and_results._2945": [
            "DesignEntityGroupAnalysis"
        ],
        "_private.system_model.analyses_and_results._2946": [
            "DesignEntitySingleContextAnalysis"
        ],
        "_private.system_model.analyses_and_results._2950": ["PartAnalysis"],
        "_private.system_model.analyses_and_results._2951": [
            "CompoundAdvancedSystemDeflection"
        ],
        "_private.system_model.analyses_and_results._2952": [
            "CompoundAdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2953": [
            "CompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2954": [
            "CompoundCriticalSpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2955": ["CompoundDynamicAnalysis"],
        "_private.system_model.analyses_and_results._2956": [
            "CompoundDynamicModelAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2957": [
            "CompoundDynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2958": [
            "CompoundDynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2959": [
            "CompoundDynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2960": [
            "CompoundDynamicModelForSteadyStateSynchronousResponse"
        ],
        "_private.system_model.analyses_and_results._2961": [
            "CompoundHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2962": [
            "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2963": [
            "CompoundHarmonicAnalysisOfSingleExcitation"
        ],
        "_private.system_model.analyses_and_results._2964": ["CompoundModalAnalysis"],
        "_private.system_model.analyses_and_results._2965": [
            "CompoundModalAnalysisAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2966": [
            "CompoundModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2967": [
            "CompoundModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2968": [
            "CompoundMultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2969": ["CompoundPowerFlow"],
        "_private.system_model.analyses_and_results._2970": [
            "CompoundStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2971": [
            "CompoundSteadyStateSynchronousResponse"
        ],
        "_private.system_model.analyses_and_results._2972": [
            "CompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2973": [
            "CompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_private.system_model.analyses_and_results._2974": [
            "CompoundSystemDeflection"
        ],
        "_private.system_model.analyses_and_results._2975": [
            "CompoundTorsionalSystemDeflection"
        ],
        "_private.system_model.analyses_and_results._2976": [
            "TESetUpForDynamicAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results._2977": ["TimeOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CompoundAnalysis",
    "AnalysisCaseVariable",
    "ConnectionAnalysis",
    "Context",
    "DesignEntityAnalysis",
    "DesignEntityGroupAnalysis",
    "DesignEntitySingleContextAnalysis",
    "PartAnalysis",
    "CompoundAdvancedSystemDeflection",
    "CompoundAdvancedSystemDeflectionSubAnalysis",
    "CompoundAdvancedTimeSteppingAnalysisForModulation",
    "CompoundCriticalSpeedAnalysis",
    "CompoundDynamicAnalysis",
    "CompoundDynamicModelAtAStiffness",
    "CompoundDynamicModelForHarmonicAnalysis",
    "CompoundDynamicModelForModalAnalysis",
    "CompoundDynamicModelForStabilityAnalysis",
    "CompoundDynamicModelForSteadyStateSynchronousResponse",
    "CompoundHarmonicAnalysis",
    "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "CompoundHarmonicAnalysisOfSingleExcitation",
    "CompoundModalAnalysis",
    "CompoundModalAnalysisAtASpeed",
    "CompoundModalAnalysisAtAStiffness",
    "CompoundModalAnalysisForHarmonicAnalysis",
    "CompoundMultibodyDynamicsAnalysis",
    "CompoundPowerFlow",
    "CompoundStabilityAnalysis",
    "CompoundSteadyStateSynchronousResponse",
    "CompoundSteadyStateSynchronousResponseAtASpeed",
    "CompoundSteadyStateSynchronousResponseOnAShaft",
    "CompoundSystemDeflection",
    "CompoundTorsionalSystemDeflection",
    "TESetUpForDynamicAnalysisOptions",
    "TimeOptions",
)
