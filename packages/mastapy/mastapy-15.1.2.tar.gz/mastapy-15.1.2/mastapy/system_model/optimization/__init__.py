"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization._2476 import (
        ConicalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2477 import (
        ConicalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2478 import (
        ConicalGearOptimizationStrategyDatabase,
    )
    from mastapy._private.system_model.optimization._2479 import (
        CylindricalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2480 import (
        CylindricalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2481 import (
        MeasuredAndFactorViewModel,
    )
    from mastapy._private.system_model.optimization._2482 import (
        MicroGeometryOptimisationTarget,
    )
    from mastapy._private.system_model.optimization._2483 import OptimizationParameter
    from mastapy._private.system_model.optimization._2484 import OptimizationStep
    from mastapy._private.system_model.optimization._2485 import OptimizationStrategy
    from mastapy._private.system_model.optimization._2486 import (
        OptimizationStrategyBase,
    )
    from mastapy._private.system_model.optimization._2487 import (
        OptimizationStrategyDatabase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization._2476": ["ConicalGearOptimisationStrategy"],
        "_private.system_model.optimization._2477": ["ConicalGearOptimizationStep"],
        "_private.system_model.optimization._2478": [
            "ConicalGearOptimizationStrategyDatabase"
        ],
        "_private.system_model.optimization._2479": [
            "CylindricalGearOptimisationStrategy"
        ],
        "_private.system_model.optimization._2480": ["CylindricalGearOptimizationStep"],
        "_private.system_model.optimization._2481": ["MeasuredAndFactorViewModel"],
        "_private.system_model.optimization._2482": ["MicroGeometryOptimisationTarget"],
        "_private.system_model.optimization._2483": ["OptimizationParameter"],
        "_private.system_model.optimization._2484": ["OptimizationStep"],
        "_private.system_model.optimization._2485": ["OptimizationStrategy"],
        "_private.system_model.optimization._2486": ["OptimizationStrategyBase"],
        "_private.system_model.optimization._2487": ["OptimizationStrategyDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationParameter",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)
