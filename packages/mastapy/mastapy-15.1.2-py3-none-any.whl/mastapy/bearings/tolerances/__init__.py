"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._2139 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._2140 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._2141 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._2142 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._2143 import FitType
    from mastapy._private.bearings.tolerances._2144 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._2145 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._2146 import InterferenceDetail
    from mastapy._private.bearings.tolerances._2147 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._2148 import ITDesignation
    from mastapy._private.bearings.tolerances._2149 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._2150 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._2151 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._2152 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._2153 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._2154 import RingDetail
    from mastapy._private.bearings.tolerances._2155 import RingTolerance
    from mastapy._private.bearings.tolerances._2156 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._2157 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._2158 import SupportDetail
    from mastapy._private.bearings.tolerances._2159 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._2160 import SupportTolerance
    from mastapy._private.bearings.tolerances._2161 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._2162 import ToleranceCombination
    from mastapy._private.bearings.tolerances._2163 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._2139": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._2140": ["InternalClearanceClass"],
        "_private.bearings.tolerances._2141": ["BearingToleranceClass"],
        "_private.bearings.tolerances._2142": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._2143": ["FitType"],
        "_private.bearings.tolerances._2144": ["InnerRingTolerance"],
        "_private.bearings.tolerances._2145": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._2146": ["InterferenceDetail"],
        "_private.bearings.tolerances._2147": ["InterferenceTolerance"],
        "_private.bearings.tolerances._2148": ["ITDesignation"],
        "_private.bearings.tolerances._2149": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._2150": ["OuterRingTolerance"],
        "_private.bearings.tolerances._2151": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._2152": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._2153": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._2154": ["RingDetail"],
        "_private.bearings.tolerances._2155": ["RingTolerance"],
        "_private.bearings.tolerances._2156": ["RoundnessSpecification"],
        "_private.bearings.tolerances._2157": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._2158": ["SupportDetail"],
        "_private.bearings.tolerances._2159": ["SupportMaterialSource"],
        "_private.bearings.tolerances._2160": ["SupportTolerance"],
        "_private.bearings.tolerances._2161": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._2162": ["ToleranceCombination"],
        "_private.bearings.tolerances._2163": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
