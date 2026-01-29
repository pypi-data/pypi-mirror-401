"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bolts._1678 import AxialLoadType
    from mastapy._private.bolts._1679 import BoltedJointMaterial
    from mastapy._private.bolts._1680 import BoltedJointMaterialDatabase
    from mastapy._private.bolts._1681 import BoltGeometry
    from mastapy._private.bolts._1682 import BoltGeometryDatabase
    from mastapy._private.bolts._1683 import BoltMaterial
    from mastapy._private.bolts._1684 import BoltMaterialDatabase
    from mastapy._private.bolts._1685 import BoltSection
    from mastapy._private.bolts._1686 import BoltShankType
    from mastapy._private.bolts._1687 import BoltTypes
    from mastapy._private.bolts._1688 import ClampedSection
    from mastapy._private.bolts._1689 import ClampedSectionMaterialDatabase
    from mastapy._private.bolts._1690 import DetailedBoltDesign
    from mastapy._private.bolts._1691 import DetailedBoltedJointDesign
    from mastapy._private.bolts._1692 import HeadCapTypes
    from mastapy._private.bolts._1693 import JointGeometries
    from mastapy._private.bolts._1694 import JointTypes
    from mastapy._private.bolts._1695 import LoadedBolt
    from mastapy._private.bolts._1696 import RolledBeforeOrAfterHeatTreatment
    from mastapy._private.bolts._1697 import StandardSizes
    from mastapy._private.bolts._1698 import StrengthGrades
    from mastapy._private.bolts._1699 import ThreadTypes
    from mastapy._private.bolts._1700 import TighteningTechniques
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bolts._1678": ["AxialLoadType"],
        "_private.bolts._1679": ["BoltedJointMaterial"],
        "_private.bolts._1680": ["BoltedJointMaterialDatabase"],
        "_private.bolts._1681": ["BoltGeometry"],
        "_private.bolts._1682": ["BoltGeometryDatabase"],
        "_private.bolts._1683": ["BoltMaterial"],
        "_private.bolts._1684": ["BoltMaterialDatabase"],
        "_private.bolts._1685": ["BoltSection"],
        "_private.bolts._1686": ["BoltShankType"],
        "_private.bolts._1687": ["BoltTypes"],
        "_private.bolts._1688": ["ClampedSection"],
        "_private.bolts._1689": ["ClampedSectionMaterialDatabase"],
        "_private.bolts._1690": ["DetailedBoltDesign"],
        "_private.bolts._1691": ["DetailedBoltedJointDesign"],
        "_private.bolts._1692": ["HeadCapTypes"],
        "_private.bolts._1693": ["JointGeometries"],
        "_private.bolts._1694": ["JointTypes"],
        "_private.bolts._1695": ["LoadedBolt"],
        "_private.bolts._1696": ["RolledBeforeOrAfterHeatTreatment"],
        "_private.bolts._1697": ["StandardSizes"],
        "_private.bolts._1698": ["StrengthGrades"],
        "_private.bolts._1699": ["ThreadTypes"],
        "_private.bolts._1700": ["TighteningTechniques"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
