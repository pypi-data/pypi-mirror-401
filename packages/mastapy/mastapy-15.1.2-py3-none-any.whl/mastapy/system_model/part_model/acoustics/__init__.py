"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2911 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2912 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2913 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2914 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2915 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2916 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2917 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2918 import (
        CylindricalEnvelopeTypes,
    )
    from mastapy._private.system_model.part_model.acoustics._2919 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2920 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2921 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2922 import (
        HemisphericalEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2923 import (
        MeshedReflectingPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2924 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2925 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2926 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2927 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2928 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2929 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2930 import PlaneShape
    from mastapy._private.system_model.part_model.acoustics._2931 import (
        ReflectingPlaneCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2932 import (
        ReflectingPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2933 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2934 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2935 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2936 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2937 import (
        RightParallelepipedEnvelopeTypes,
    )
    from mastapy._private.system_model.part_model.acoustics._2938 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2939 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2911": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2912": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2913": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2914": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2915": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2916": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2917": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2918": [
            "CylindricalEnvelopeTypes"
        ],
        "_private.system_model.part_model.acoustics._2919": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2920": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2921": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2922": [
            "HemisphericalEnvelopeType"
        ],
        "_private.system_model.part_model.acoustics._2923": ["MeshedReflectingPlane"],
        "_private.system_model.part_model.acoustics._2924": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2925": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2926": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2927": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2928": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2929": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2930": ["PlaneShape"],
        "_private.system_model.part_model.acoustics._2931": [
            "ReflectingPlaneCollection"
        ],
        "_private.system_model.part_model.acoustics._2932": ["ReflectingPlaneOptions"],
        "_private.system_model.part_model.acoustics._2933": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2934": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2935": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2936": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2937": [
            "RightParallelepipedEnvelopeTypes"
        ],
        "_private.system_model.part_model.acoustics._2938": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2939": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "CylindricalEnvelopeTypes",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "HemisphericalEnvelopeType",
    "MeshedReflectingPlane",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "PlaneShape",
    "ReflectingPlaneCollection",
    "ReflectingPlaneOptions",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "RightParallelepipedEnvelopeTypes",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)
