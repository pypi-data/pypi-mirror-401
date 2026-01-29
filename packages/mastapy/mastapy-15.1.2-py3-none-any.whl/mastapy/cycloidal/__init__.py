"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.cycloidal._1664 import ContactSpecification
    from mastapy._private.cycloidal._1665 import CrowningSpecificationMethod
    from mastapy._private.cycloidal._1666 import CycloidalAssemblyDesign
    from mastapy._private.cycloidal._1667 import CycloidalDiscDesign
    from mastapy._private.cycloidal._1668 import CycloidalDiscDesignExporter
    from mastapy._private.cycloidal._1669 import CycloidalDiscMaterial
    from mastapy._private.cycloidal._1670 import CycloidalDiscMaterialDatabase
    from mastapy._private.cycloidal._1671 import CycloidalDiscModificationsSpecification
    from mastapy._private.cycloidal._1672 import DirectionOfMeasuredModifications
    from mastapy._private.cycloidal._1673 import GeometryToExport
    from mastapy._private.cycloidal._1674 import NamedDiscPhase
    from mastapy._private.cycloidal._1675 import RingPinsDesign
    from mastapy._private.cycloidal._1676 import RingPinsMaterial
    from mastapy._private.cycloidal._1677 import RingPinsMaterialDatabase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.cycloidal._1664": ["ContactSpecification"],
        "_private.cycloidal._1665": ["CrowningSpecificationMethod"],
        "_private.cycloidal._1666": ["CycloidalAssemblyDesign"],
        "_private.cycloidal._1667": ["CycloidalDiscDesign"],
        "_private.cycloidal._1668": ["CycloidalDiscDesignExporter"],
        "_private.cycloidal._1669": ["CycloidalDiscMaterial"],
        "_private.cycloidal._1670": ["CycloidalDiscMaterialDatabase"],
        "_private.cycloidal._1671": ["CycloidalDiscModificationsSpecification"],
        "_private.cycloidal._1672": ["DirectionOfMeasuredModifications"],
        "_private.cycloidal._1673": ["GeometryToExport"],
        "_private.cycloidal._1674": ["NamedDiscPhase"],
        "_private.cycloidal._1675": ["RingPinsDesign"],
        "_private.cycloidal._1676": ["RingPinsMaterial"],
        "_private.cycloidal._1677": ["RingPinsMaterialDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactSpecification",
    "CrowningSpecificationMethod",
    "CycloidalAssemblyDesign",
    "CycloidalDiscDesign",
    "CycloidalDiscDesignExporter",
    "CycloidalDiscMaterial",
    "CycloidalDiscMaterialDatabase",
    "CycloidalDiscModificationsSpecification",
    "DirectionOfMeasuredModifications",
    "GeometryToExport",
    "NamedDiscPhase",
    "RingPinsDesign",
    "RingPinsMaterial",
    "RingPinsMaterialDatabase",
)
