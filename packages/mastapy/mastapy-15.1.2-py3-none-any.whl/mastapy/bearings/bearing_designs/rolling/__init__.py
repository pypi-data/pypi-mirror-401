"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling._2383 import (
        AngularContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2384 import (
        AngularContactThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2385 import (
        AsymmetricSphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2386 import (
        AxialThrustCylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2387 import (
        AxialThrustNeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2388 import BallBearing
    from mastapy._private.bearings.bearing_designs.rolling._2389 import (
        BallBearingShoulderDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2390 import (
        BarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2391 import (
        BearingProtection,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2392 import (
        BearingProtectionDetailsModifier,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2393 import (
        BearingProtectionLevel,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2394 import (
        BearingTypeExtraInformation,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2395 import CageBridgeShape
    from mastapy._private.bearings.bearing_designs.rolling._2396 import (
        CrossedRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2397 import (
        CylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2398 import (
        DeepGrooveBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2399 import DiameterSeries
    from mastapy._private.bearings.bearing_designs.rolling._2400 import (
        FatigueLoadLimitCalculationMethodEnum,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2401 import (
        FourPointContactAngleDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2402 import (
        FourPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2403 import (
        GeometricConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2404 import (
        GeometricConstantsForRollingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2405 import (
        GeometricConstantsForSlidingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2406 import HeightSeries
    from mastapy._private.bearings.bearing_designs.rolling._2407 import (
        MultiPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2408 import (
        NeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2409 import (
        NonBarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2410 import RollerBearing
    from mastapy._private.bearings.bearing_designs.rolling._2411 import RollerEndShape
    from mastapy._private.bearings.bearing_designs.rolling._2412 import RollerRibDetail
    from mastapy._private.bearings.bearing_designs.rolling._2413 import RollingBearing
    from mastapy._private.bearings.bearing_designs.rolling._2414 import (
        RollingBearingElement,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2415 import (
        SelfAligningBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2416 import (
        SKFSealFrictionalMomentConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2417 import SleeveType
    from mastapy._private.bearings.bearing_designs.rolling._2418 import (
        SphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2419 import (
        SphericalRollerThrustBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2420 import (
        TaperRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2421 import (
        ThreePointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2422 import (
        ThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2423 import (
        ToroidalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2424 import WidthSeries
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling._2383": [
            "AngularContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2384": [
            "AngularContactThrustBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2385": [
            "AsymmetricSphericalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2386": [
            "AxialThrustCylindricalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2387": [
            "AxialThrustNeedleRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2388": ["BallBearing"],
        "_private.bearings.bearing_designs.rolling._2389": [
            "BallBearingShoulderDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2390": ["BarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2391": ["BearingProtection"],
        "_private.bearings.bearing_designs.rolling._2392": [
            "BearingProtectionDetailsModifier"
        ],
        "_private.bearings.bearing_designs.rolling._2393": ["BearingProtectionLevel"],
        "_private.bearings.bearing_designs.rolling._2394": [
            "BearingTypeExtraInformation"
        ],
        "_private.bearings.bearing_designs.rolling._2395": ["CageBridgeShape"],
        "_private.bearings.bearing_designs.rolling._2396": ["CrossedRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2397": ["CylindricalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2398": ["DeepGrooveBallBearing"],
        "_private.bearings.bearing_designs.rolling._2399": ["DiameterSeries"],
        "_private.bearings.bearing_designs.rolling._2400": [
            "FatigueLoadLimitCalculationMethodEnum"
        ],
        "_private.bearings.bearing_designs.rolling._2401": [
            "FourPointContactAngleDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2402": [
            "FourPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2403": ["GeometricConstants"],
        "_private.bearings.bearing_designs.rolling._2404": [
            "GeometricConstantsForRollingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2405": [
            "GeometricConstantsForSlidingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2406": ["HeightSeries"],
        "_private.bearings.bearing_designs.rolling._2407": [
            "MultiPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2408": ["NeedleRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2409": ["NonBarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2410": ["RollerBearing"],
        "_private.bearings.bearing_designs.rolling._2411": ["RollerEndShape"],
        "_private.bearings.bearing_designs.rolling._2412": ["RollerRibDetail"],
        "_private.bearings.bearing_designs.rolling._2413": ["RollingBearing"],
        "_private.bearings.bearing_designs.rolling._2414": ["RollingBearingElement"],
        "_private.bearings.bearing_designs.rolling._2415": ["SelfAligningBallBearing"],
        "_private.bearings.bearing_designs.rolling._2416": [
            "SKFSealFrictionalMomentConstants"
        ],
        "_private.bearings.bearing_designs.rolling._2417": ["SleeveType"],
        "_private.bearings.bearing_designs.rolling._2418": ["SphericalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2419": [
            "SphericalRollerThrustBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2420": ["TaperRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2421": [
            "ThreePointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2422": ["ThrustBallBearing"],
        "_private.bearings.bearing_designs.rolling._2423": ["ToroidalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2424": ["WidthSeries"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "RollingBearingElement",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)
