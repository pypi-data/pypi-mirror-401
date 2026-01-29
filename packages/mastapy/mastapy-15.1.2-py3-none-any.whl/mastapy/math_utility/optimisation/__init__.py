"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.optimisation._1755 import AbstractOptimisable
    from mastapy._private.math_utility.optimisation._1756 import (
        DesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1757 import InputSetter
    from mastapy._private.math_utility.optimisation._1758 import Optimisable
    from mastapy._private.math_utility.optimisation._1759 import OptimisationHistory
    from mastapy._private.math_utility.optimisation._1760 import OptimizationInput
    from mastapy._private.math_utility.optimisation._1761 import OptimizationProperty
    from mastapy._private.math_utility.optimisation._1762 import OptimizationVariable
    from mastapy._private.math_utility.optimisation._1763 import (
        ParetoOptimisationFilter,
    )
    from mastapy._private.math_utility.optimisation._1764 import ParetoOptimisationInput
    from mastapy._private.math_utility.optimisation._1765 import (
        ParetoOptimisationOutput,
    )
    from mastapy._private.math_utility.optimisation._1766 import (
        ParetoOptimisationStrategy,
    )
    from mastapy._private.math_utility.optimisation._1767 import (
        ParetoOptimisationStrategyBars,
    )
    from mastapy._private.math_utility.optimisation._1768 import (
        ParetoOptimisationStrategyChartInformation,
    )
    from mastapy._private.math_utility.optimisation._1769 import (
        ParetoOptimisationStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1770 import (
        ParetoOptimisationVariable,
    )
    from mastapy._private.math_utility.optimisation._1771 import (
        ParetoOptimisationVariableBase,
    )
    from mastapy._private.math_utility.optimisation._1772 import (
        PropertyTargetForDominantCandidateSearch,
    )
    from mastapy._private.math_utility.optimisation._1773 import (
        ReportingOptimizationInput,
    )
    from mastapy._private.math_utility.optimisation._1774 import (
        SpecifyOptimisationInputAs,
    )
    from mastapy._private.math_utility.optimisation._1775 import TargetingPropertyTo
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.optimisation._1755": ["AbstractOptimisable"],
        "_private.math_utility.optimisation._1756": [
            "DesignSpaceSearchStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1757": ["InputSetter"],
        "_private.math_utility.optimisation._1758": ["Optimisable"],
        "_private.math_utility.optimisation._1759": ["OptimisationHistory"],
        "_private.math_utility.optimisation._1760": ["OptimizationInput"],
        "_private.math_utility.optimisation._1761": ["OptimizationProperty"],
        "_private.math_utility.optimisation._1762": ["OptimizationVariable"],
        "_private.math_utility.optimisation._1763": ["ParetoOptimisationFilter"],
        "_private.math_utility.optimisation._1764": ["ParetoOptimisationInput"],
        "_private.math_utility.optimisation._1765": ["ParetoOptimisationOutput"],
        "_private.math_utility.optimisation._1766": ["ParetoOptimisationStrategy"],
        "_private.math_utility.optimisation._1767": ["ParetoOptimisationStrategyBars"],
        "_private.math_utility.optimisation._1768": [
            "ParetoOptimisationStrategyChartInformation"
        ],
        "_private.math_utility.optimisation._1769": [
            "ParetoOptimisationStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1770": ["ParetoOptimisationVariable"],
        "_private.math_utility.optimisation._1771": ["ParetoOptimisationVariableBase"],
        "_private.math_utility.optimisation._1772": [
            "PropertyTargetForDominantCandidateSearch"
        ],
        "_private.math_utility.optimisation._1773": ["ReportingOptimizationInput"],
        "_private.math_utility.optimisation._1774": ["SpecifyOptimisationInputAs"],
        "_private.math_utility.optimisation._1775": ["TargetingPropertyTo"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractOptimisable",
    "DesignSpaceSearchStrategyDatabase",
    "InputSetter",
    "Optimisable",
    "OptimisationHistory",
    "OptimizationInput",
    "OptimizationProperty",
    "OptimizationVariable",
    "ParetoOptimisationFilter",
    "ParetoOptimisationInput",
    "ParetoOptimisationOutput",
    "ParetoOptimisationStrategy",
    "ParetoOptimisationStrategyBars",
    "ParetoOptimisationStrategyChartInformation",
    "ParetoOptimisationStrategyDatabase",
    "ParetoOptimisationVariable",
    "ParetoOptimisationVariableBase",
    "PropertyTargetForDominantCandidateSearch",
    "ReportingOptimizationInput",
    "SpecifyOptimisationInputAs",
    "TargetingPropertyTo",
)
