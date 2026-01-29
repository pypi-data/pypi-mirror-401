"""ModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7947

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingConnectionLoadCase",
)
_CLUTCH_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ClutchConnectionLoadCase",
)
_CONCEPT_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConceptCouplingConnectionLoadCase",
)
_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CouplingConnectionLoadCase",
)
_SPRING_DAMPER_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpringDamperConnectionLoadCase",
)
_TORQUE_CONVERTER_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterConnectionLoadCase",
)
_STRAIGHT_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearLoadCase",
)
_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearSetLoadCase",
)
_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelPlanetGearLoadCase",
)
_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelSunGearLoadCase",
)
_WORM_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearLoadCase"
)
_WORM_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearSetLoadCase"
)
_ZEROL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ZerolBevelGearLoadCase"
)
_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearSetLoadCase",
)
_CYCLOIDAL_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalAssemblyLoadCase",
)
_CYCLOIDAL_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CycloidalDiscLoadCase"
)
_RING_PINS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RingPinsLoadCase"
)
_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingLoadCase",
)
_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingHalfLoadCase",
)
_BELT_DRIVE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BeltDriveLoadCase"
)
_CLUTCH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchLoadCase"
)
_CLUTCH_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchHalfLoadCase"
)
_CONCEPT_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptCouplingLoadCase"
)
_CONCEPT_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConceptCouplingHalfLoadCase",
)
_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingLoadCase"
)
_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingHalfLoadCase"
)
_CVT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTLoadCase"
)
_CVT_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTPulleyLoadCase"
)
_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PulleyLoadCase"
)
_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftHubConnectionLoadCase",
)
_ROLLING_RING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RollingRingLoadCase"
)
_ROLLING_RING_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RollingRingAssemblyLoadCase",
)
_SPRING_DAMPER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpringDamperLoadCase"
)
_SPRING_DAMPER_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpringDamperHalfLoadCase",
)
_SYNCHRONISER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SynchroniserLoadCase"
)
_SYNCHRONISER_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserHalfLoadCase",
)
_SYNCHRONISER_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserPartLoadCase",
)
_SYNCHRONISER_SLEEVE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserSleeveLoadCase",
)
_TORQUE_CONVERTER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "TorqueConverterLoadCase"
)
_TORQUE_CONVERTER_PUMP_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterPumpLoadCase",
)
_TORQUE_CONVERTER_TURBINE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterTurbineLoadCase",
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftToMountableComponentConnectionLoadCase",
)
_CVT_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CVTBeltConnectionLoadCase",
)
_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BeltConnectionLoadCase"
)
_COAXIAL_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CoaxialConnectionLoadCase",
)
_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectionLoadCase"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "InterMountableComponentConnectionLoadCase",
)
_PLANETARY_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryConnectionLoadCase",
)
_ROLLING_RING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RollingRingConnectionLoadCase",
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftToMountableComponentConnectionLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearMeshLoadCase",
)
_CONCEPT_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearMeshLoadCase"
)
_FACE_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearMeshLoadCase"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearMeshLoadCase",
)
_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearMeshLoadCase"
)
_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearMeshLoadCase"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearMeshLoadCase",
)
_CYLINDRICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearMeshLoadCase",
)
_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearMeshLoadCase"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
)
_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpiralBevelGearMeshLoadCase",
)
_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearMeshLoadCase",
)
_WORM_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearMeshLoadCase"
)
_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearMeshLoadCase",
)
_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearMeshLoadCase"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscCentralBearingConnectionLoadCase",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscPlanetaryBearingConnectionLoadCase",
)
_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RingPinsToDiscConnectionLoadCase",
)
_ABSTRACT_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AbstractShaftLoadCase"
)
_MICROPHONE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MicrophoneLoadCase"
)
_MICROPHONE_ARRAY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MicrophoneArrayLoadCase"
)
_ABSTRACT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractAssemblyLoadCase",
)
_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftOrHousingLoadCase",
)
_BEARING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BearingLoadCase"
)
_BOLT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BoltLoadCase"
)
_BOLTED_JOINT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BoltedJointLoadCase"
)
_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ComponentLoadCase"
)
_CONNECTOR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectorLoadCase"
)
_DATUM_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "DatumLoadCase"
)
_EXTERNAL_CAD_MODEL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ExternalCADModelLoadCase",
)
_FE_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FEPartLoadCase"
)
_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "FlexiblePinAssemblyLoadCase",
)
_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AssemblyLoadCase"
)
_GUIDE_DXF_MODEL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GuideDxfModelLoadCase"
)
_MASS_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MassDiscLoadCase"
)
_MEASUREMENT_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "MeasurementComponentLoadCase",
)
_MOUNTABLE_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "MountableComponentLoadCase",
)
_OIL_SEAL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "OilSealLoadCase"
)
_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)
_PLANET_CARRIER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PlanetCarrierLoadCase"
)
_POINT_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PointLoadLoadCase"
)
_POWER_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PowerLoadLoadCase"
)
_ROOT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RootAssemblyLoadCase"
)
_SPECIALISED_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpecialisedAssemblyLoadCase",
)
_UNBALANCED_MASS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "UnbalancedMassLoadCase"
)
_VIRTUAL_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "VirtualComponentLoadCase",
)
_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ShaftLoadCase"
)
_CONCEPT_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearLoadCase"
)
_CONCEPT_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearSetLoadCase"
)
_FACE_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearLoadCase"
)
_FACE_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearSetLoadCase"
)
_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearLoadCase",
)
_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearSetLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearSetLoadCase",
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialPlanetGearLoadCase",
)
_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialSunGearLoadCase",
)
_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearLoadCase"
)
_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearSetLoadCase"
)
_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearLoadCase"
)
_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearSetLoadCase"
)
_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CylindricalGearLoadCase"
)
_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearSetLoadCase",
)
_CYLINDRICAL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalPlanetGearLoadCase",
)
_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearLoadCase"
)
_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearSetLoadCase"
)
_HYPOID_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearLoadCase"
)
_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearSetLoadCase"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearSetLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearSetLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
)
_PLANETARY_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryGearSetLoadCase",
)
_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpiralBevelGearLoadCase"
)
_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpiralBevelGearSetLoadCase",
)
_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearLoadCase",
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearSetLoadCase",
)
_CLUTCH_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "ClutchConnection"
)
_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)
_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)
_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)
_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)
_STRAIGHT_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
)
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
)
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)
_WORM_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear")
_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)
_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)
_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)
_CONCEPT_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
)
_CONCEPT_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
)
_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")
_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)
_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)
_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)
_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")
_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)
_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)
_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)
_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)
_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)
_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")
_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")
_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
)
_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGear"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGear",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
)
_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)
_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
)
_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
)
_STRAIGHT_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
)
_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)
_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCouplingHalf"
)
_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)
_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")
_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)
_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)
_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)
_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)
_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)
_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")
_CVT_PULLEY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
)
_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)
_ROLLING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
)
_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)
_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)
_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)
_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)
_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)
_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)
_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)
_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)
_TORQUE_CONVERTER_PUMP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
)
_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)
_CVT_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTBeltConnection"
)
_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BeltConnection"
)
_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)
_PLANETARY_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetaryConnection"
)
_ROLLING_RING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RollingRingConnection"
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)
_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)
_FACE_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearMesh"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelDiffGearMesh"
)
_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)
_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)
_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)
_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "HypoidGearMesh"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidHypoidGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
)
_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)
_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)
_ZEROL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ZerolBevelGearMesh"
)
_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)
_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)
_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)
_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")
_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)
_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
_BOLTED_JOINT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint")
_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_CONNECTOR = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
_EXTERNAL_CAD_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
)
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)
_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)
_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)
_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)
_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")
_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)
_UNBALANCED_MASS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
)
_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")
_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses", "ModalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1720
    from mastapy._private.system_model.analyses_and_results import _2943
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7932
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6694,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6194,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6449,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4895,
        _4896,
        _4897,
        _4898,
        _4899,
        _4900,
        _4901,
        _4902,
        _4903,
        _4904,
        _4905,
        _4906,
        _4907,
        _4908,
        _4909,
        _4910,
        _4911,
        _4912,
        _4913,
        _4914,
        _4915,
        _4916,
        _4917,
        _4918,
        _4919,
        _4920,
        _4921,
        _4922,
        _4923,
        _4924,
        _4925,
        _4926,
        _4927,
        _4928,
        _4929,
        _4930,
        _4931,
        _4933,
        _4934,
        _4935,
        _4936,
        _4937,
        _4938,
        _4939,
        _4940,
        _4941,
        _4942,
        _4943,
        _4944,
        _4945,
        _4946,
        _4947,
        _4951,
        _4952,
        _4953,
        _4954,
        _4955,
        _4956,
        _4958,
        _4959,
        _4960,
        _4961,
        _4962,
        _4963,
        _4964,
        _4965,
        _4966,
        _4967,
        _4968,
        _4969,
        _4970,
        _4971,
        _4972,
        _4973,
        _4974,
        _4975,
        _4976,
        _4977,
        _4978,
        _4981,
        _4983,
        _4984,
        _4986,
        _4988,
        _4989,
        _4990,
        _4991,
        _4992,
        _4993,
        _4994,
        _4995,
        _4996,
        _4997,
        _4998,
        _4999,
        _5000,
        _5001,
        _5002,
        _5003,
        _5004,
        _5005,
        _5007,
        _5008,
        _5009,
        _5010,
        _5011,
        _5012,
        _5013,
        _5014,
        _5015,
        _5016,
        _5017,
        _5018,
        _5019,
        _5020,
        _5021,
        _5022,
        _5023,
        _5024,
        _5025,
        _5026,
        _5027,
        _5028,
        _5029,
        _5030,
        _5031,
        _5032,
        _5036,
        _5037,
        _5038,
        _5039,
        _5040,
        _5041,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7728,
        _7729,
        _7730,
        _7731,
        _7735,
        _7736,
        _7737,
        _7740,
        _7741,
        _7742,
        _7743,
        _7744,
        _7745,
        _7746,
        _7747,
        _7748,
        _7749,
        _7750,
        _7751,
        _7752,
        _7753,
        _7754,
        _7755,
        _7756,
        _7758,
        _7759,
        _7760,
        _7761,
        _7762,
        _7763,
        _7764,
        _7765,
        _7766,
        _7768,
        _7770,
        _7771,
        _7772,
        _7773,
        _7774,
        _7775,
        _7776,
        _7777,
        _7778,
        _7779,
        _7780,
        _7781,
        _7782,
        _7783,
        _7785,
        _7787,
        _7788,
        _7791,
        _7805,
        _7806,
        _7807,
        _7808,
        _7809,
        _7810,
        _7812,
        _7814,
        _7817,
        _7818,
        _7827,
        _7828,
        _7829,
        _7833,
        _7834,
        _7835,
        _7836,
        _7837,
        _7838,
        _7839,
        _7840,
        _7841,
        _7842,
        _7843,
        _7844,
        _7846,
        _7847,
        _7848,
        _7850,
        _7852,
        _7853,
        _7854,
        _7855,
        _7856,
        _7857,
        _7859,
        _7862,
        _7863,
        _7864,
        _7869,
        _7870,
        _7871,
        _7872,
        _7873,
        _7874,
        _7875,
        _7876,
        _7877,
        _7878,
        _7879,
        _7880,
        _7881,
        _7882,
        _7883,
        _7884,
        _7885,
        _7886,
        _7887,
        _7888,
        _7889,
        _7890,
        _7891,
        _7892,
        _7893,
        _7894,
        _7895,
        _7896,
        _7899,
        _7900,
        _7901,
        _7902,
        _7907,
        _7908,
        _7909,
        _7910,
        _7911,
        _7912,
        _7913,
        _7914,
    )
    from mastapy._private.system_model.connections_and_sockets import (
        _2525,
        _2528,
        _2529,
        _2532,
        _2533,
        _2541,
        _2547,
        _2552,
        _2555,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2602,
        _2604,
        _2606,
        _2608,
        _2610,
        _2612,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2595,
        _2598,
        _2601,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2559,
        _2561,
        _2563,
        _2565,
        _2567,
        _2569,
        _2571,
        _2573,
        _2575,
        _2578,
        _2579,
        _2580,
        _2583,
        _2585,
        _2587,
        _2589,
        _2591,
    )
    from mastapy._private.system_model.part_model import (
        _2703,
        _2704,
        _2705,
        _2706,
        _2709,
        _2712,
        _2713,
        _2715,
        _2718,
        _2719,
        _2724,
        _2725,
        _2726,
        _2727,
        _2734,
        _2735,
        _2736,
        _2737,
        _2738,
        _2740,
        _2743,
        _2745,
        _2747,
        _2748,
        _2751,
        _2753,
        _2754,
        _2756,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2860,
        _2862,
        _2863,
        _2865,
        _2866,
        _2868,
        _2869,
        _2871,
        _2872,
        _2873,
        _2874,
        _2876,
        _2883,
        _2884,
        _2885,
        _2891,
        _2892,
        _2893,
        _2895,
        _2896,
        _2897,
        _2898,
        _2899,
        _2901,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2851, _2852, _2853
    from mastapy._private.system_model.part_model.gears import (
        _2795,
        _2796,
        _2797,
        _2798,
        _2799,
        _2800,
        _2801,
        _2802,
        _2803,
        _2804,
        _2805,
        _2806,
        _2807,
        _2808,
        _2809,
        _2810,
        _2811,
        _2812,
        _2814,
        _2816,
        _2817,
        _2818,
        _2819,
        _2820,
        _2821,
        _2822,
        _2823,
        _2824,
        _2826,
        _2827,
        _2828,
        _2829,
        _2830,
        _2831,
        _2832,
        _2833,
        _2834,
        _2835,
        _2836,
        _2837,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2759

    Self = TypeVar("Self", bound="ModalAnalysis")
    CastSelf = TypeVar("CastSelf", bound="ModalAnalysis._Cast_ModalAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("ModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalAnalysis:
    """Special nested class for casting ModalAnalysis to subclasses."""

    __parent__: "ModalAnalysis"

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7947.StaticLoadAnalysisCase":
        return self.__parent__._cast(_7947.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7932.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7932,
        )

        return self.__parent__._cast(_7932.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2943.Context":
        from mastapy._private.system_model.analyses_and_results import _2943

        return self.__parent__._cast(_2943.Context)

    @property
    def modal_analysis_for_transfer_path_analysis(
        self: "CastSelf",
    ) -> "_6194.ModalAnalysisForTransferPathAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
            _6194,
        )

        return self.__parent__._cast(_6194.ModalAnalysisForTransferPathAnalysis)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6449.ModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6449,
        )

        return self.__parent__._cast(_6449.ModalAnalysisForHarmonicAnalysis)

    @property
    def modal_analysis(self: "CastSelf") -> "ModalAnalysis":
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
class ModalAnalysis(_7947.StaticLoadAnalysisCase):
    """ModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_settings(self: "Self") -> "_4983.ModalAnalysisOptions":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bar_model_export(self: "Self") -> "_4981.ModalAnalysisBarModelFEExportOptions":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysisBarModelFEExportOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BarModelExport")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def modal_analysis_results(self: "Self") -> "_6694.DynamicAnalysis":
        """mastapy.system_model.analyses_and_results.dynamic_analyses.DynamicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def normal_modes(self: "Self") -> "List[_1720.Eigenmode]":
        """List[mastapy.math_utility.Eigenmode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7853.PartToPartShearCouplingConnectionLoadCase",
    ) -> "_4989.PartToPartShearCouplingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_connection(
        self: "Self", design_entity: "_2602.ClutchConnection"
    ) -> "_4916.ClutchConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ClutchConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_connection_load_case(
        self: "Self", design_entity_analysis: "_7754.ClutchConnectionLoadCase"
    ) -> "_4916.ClutchConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ClutchConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_connection(
        self: "Self", design_entity: "_2604.ConceptCouplingConnection"
    ) -> "_4921.ConceptCouplingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_connection_load_case(
        self: "Self", design_entity_analysis: "_7760.ConceptCouplingConnectionLoadCase"
    ) -> "_4921.ConceptCouplingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_connection(
        self: "Self", design_entity: "_2606.CouplingConnection"
    ) -> "_4933.CouplingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CouplingConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_connection_load_case(
        self: "Self", design_entity_analysis: "_7773.CouplingConnectionLoadCase"
    ) -> "_4933.CouplingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CouplingConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_connection(
        self: "Self", design_entity: "_2610.SpringDamperConnection"
    ) -> "_5012.SpringDamperConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_connection_load_case(
        self: "Self", design_entity_analysis: "_7882.SpringDamperConnectionLoadCase"
    ) -> "_5012.SpringDamperConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_connection(
        self: "Self", design_entity: "_2612.TorqueConverterConnection"
    ) -> "_5027.TorqueConverterConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_connection_load_case(
        self: "Self", design_entity_analysis: "_7899.TorqueConverterConnectionLoadCase"
    ) -> "_5027.TorqueConverterConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7888.StraightBevelGearLoadCase"
    ) -> "_5019.StraightBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_set(
        self: "Self", design_entity: "_2831.StraightBevelGearSet"
    ) -> "_5020.StraightBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7890.StraightBevelGearSetLoadCase"
    ) -> "_5020.StraightBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear(
        self: "Self", design_entity: "_2832.StraightBevelPlanetGear"
    ) -> "_5021.StraightBevelPlanetGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelPlanetGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear_load_case(
        self: "Self", design_entity_analysis: "_7891.StraightBevelPlanetGearLoadCase"
    ) -> "_5021.StraightBevelPlanetGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelPlanetGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear(
        self: "Self", design_entity: "_2833.StraightBevelSunGear"
    ) -> "_5022.StraightBevelSunGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelSunGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear_load_case(
        self: "Self", design_entity_analysis: "_7892.StraightBevelSunGearLoadCase"
    ) -> "_5022.StraightBevelSunGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelSunGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear(
        self: "Self", design_entity: "_2834.WormGear"
    ) -> "_5037.WormGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.WormGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_load_case(
        self: "Self", design_entity_analysis: "_7909.WormGearLoadCase"
    ) -> "_5037.WormGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.WormGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_set(
        self: "Self", design_entity: "_2835.WormGearSet"
    ) -> "_5038.WormGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.WormGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7911.WormGearSetLoadCase"
    ) -> "_5038.WormGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.WormGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear(
        self: "Self", design_entity: "_2836.ZerolBevelGear"
    ) -> "_5040.ZerolBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7912.ZerolBevelGearLoadCase"
    ) -> "_5040.ZerolBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set(
        self: "Self", design_entity: "_2837.ZerolBevelGearSet"
    ) -> "_5041.ZerolBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7914.ZerolBevelGearSetLoadCase"
    ) -> "_5041.ZerolBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_assembly(
        self: "Self", design_entity: "_2851.CycloidalAssembly"
    ) -> "_4939.CycloidalAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalAssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_assembly_load_case(
        self: "Self", design_entity_analysis: "_7779.CycloidalAssemblyLoadCase"
    ) -> "_4939.CycloidalAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalAssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc(
        self: "Self", design_entity: "_2852.CycloidalDisc"
    ) -> "_4941.CycloidalDiscModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalDiscModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_load_case(
        self: "Self", design_entity_analysis: "_7781.CycloidalDiscLoadCase"
    ) -> "_4941.CycloidalDiscModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalDiscModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins(
        self: "Self", design_entity: "_2853.RingPins"
    ) -> "_4998.RingPinsModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RingPinsModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins_load_case(
        self: "Self", design_entity_analysis: "_7869.RingPinsLoadCase"
    ) -> "_4998.RingPinsModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RingPinsModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling(
        self: "Self", design_entity: "_2873.PartToPartShearCoupling"
    ) -> "_4991.PartToPartShearCouplingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_load_case(
        self: "Self", design_entity_analysis: "_7855.PartToPartShearCouplingLoadCase"
    ) -> "_4991.PartToPartShearCouplingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half(
        self: "Self", design_entity: "_2874.PartToPartShearCouplingHalf"
    ) -> "_4990.PartToPartShearCouplingHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingHalfModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half_load_case(
        self: "Self",
        design_entity_analysis: "_7854.PartToPartShearCouplingHalfLoadCase",
    ) -> "_4990.PartToPartShearCouplingHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingHalfModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_drive(
        self: "Self", design_entity: "_2860.BeltDrive"
    ) -> "_4905.BeltDriveModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BeltDriveModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_DRIVE],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_drive_load_case(
        self: "Self", design_entity_analysis: "_7743.BeltDriveLoadCase"
    ) -> "_4905.BeltDriveModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BeltDriveModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_DRIVE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch(
        self: "Self", design_entity: "_2862.Clutch"
    ) -> "_4918.ClutchModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ClutchModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_load_case(
        self: "Self", design_entity_analysis: "_7756.ClutchLoadCase"
    ) -> "_4918.ClutchModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ClutchModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_half(
        self: "Self", design_entity: "_2863.ClutchHalf"
    ) -> "_4917.ClutchHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ClutchHalfModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_HALF],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_half_load_case(
        self: "Self", design_entity_analysis: "_7755.ClutchHalfLoadCase"
    ) -> "_4917.ClutchHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ClutchHalfModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling(
        self: "Self", design_entity: "_2865.ConceptCoupling"
    ) -> "_4923.ConceptCouplingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_load_case(
        self: "Self", design_entity_analysis: "_7762.ConceptCouplingLoadCase"
    ) -> "_4923.ConceptCouplingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_half(
        self: "Self", design_entity: "_2866.ConceptCouplingHalf"
    ) -> "_4922.ConceptCouplingHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingHalfModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_half_load_case(
        self: "Self", design_entity_analysis: "_7761.ConceptCouplingHalfLoadCase"
    ) -> "_4922.ConceptCouplingHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingHalfModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling(
        self: "Self", design_entity: "_2868.Coupling"
    ) -> "_4935.CouplingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_load_case(
        self: "Self", design_entity_analysis: "_7775.CouplingLoadCase"
    ) -> "_4935.CouplingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_half(
        self: "Self", design_entity: "_2869.CouplingHalf"
    ) -> "_4934.CouplingHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CouplingHalfModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_half_load_case(
        self: "Self", design_entity_analysis: "_7774.CouplingHalfLoadCase"
    ) -> "_4934.CouplingHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CouplingHalfModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt(
        self: "Self", design_entity: "_2871.CVT"
    ) -> "_4937.CVTModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CVTModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_load_case(
        self: "Self", design_entity_analysis: "_7777.CVTLoadCase"
    ) -> "_4937.CVTModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CVTModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_pulley(
        self: "Self", design_entity: "_2872.CVTPulley"
    ) -> "_4938.CVTPulleyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CVTPulleyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_pulley_load_case(
        self: "Self", design_entity_analysis: "_7778.CVTPulleyLoadCase"
    ) -> "_4938.CVTPulleyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CVTPulleyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_PULLEY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_pulley(
        self: "Self", design_entity: "_2876.Pulley"
    ) -> "_4997.PulleyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PulleyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_pulley_load_case(
        self: "Self", design_entity_analysis: "_7864.PulleyLoadCase"
    ) -> "_4997.PulleyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PulleyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PULLEY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_hub_connection(
        self: "Self", design_entity: "_2885.ShaftHubConnection"
    ) -> "_5004.ShaftHubConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ShaftHubConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_HUB_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_hub_connection_load_case(
        self: "Self", design_entity_analysis: "_7875.ShaftHubConnectionLoadCase"
    ) -> "_5004.ShaftHubConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ShaftHubConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_HUB_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring(
        self: "Self", design_entity: "_2883.RollingRing"
    ) -> "_5002.RollingRingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RollingRingModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_load_case(
        self: "Self", design_entity_analysis: "_7873.RollingRingLoadCase"
    ) -> "_5002.RollingRingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RollingRingModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_assembly(
        self: "Self", design_entity: "_2884.RollingRingAssembly"
    ) -> "_5000.RollingRingAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RollingRingAssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_assembly_load_case(
        self: "Self", design_entity_analysis: "_7871.RollingRingAssemblyLoadCase"
    ) -> "_5000.RollingRingAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RollingRingAssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper(
        self: "Self", design_entity: "_2891.SpringDamper"
    ) -> "_5014.SpringDamperModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_load_case(
        self: "Self", design_entity_analysis: "_7884.SpringDamperLoadCase"
    ) -> "_5014.SpringDamperModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_half(
        self: "Self", design_entity: "_2892.SpringDamperHalf"
    ) -> "_5013.SpringDamperHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperHalfModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_half_load_case(
        self: "Self", design_entity_analysis: "_7883.SpringDamperHalfLoadCase"
    ) -> "_5013.SpringDamperHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperHalfModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser(
        self: "Self", design_entity: "_2893.Synchroniser"
    ) -> "_5024.SynchroniserModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_load_case(
        self: "Self", design_entity_analysis: "_7894.SynchroniserLoadCase"
    ) -> "_5024.SynchroniserModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_half(
        self: "Self", design_entity: "_2895.SynchroniserHalf"
    ) -> "_5023.SynchroniserHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserHalfModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_half_load_case(
        self: "Self", design_entity_analysis: "_7893.SynchroniserHalfLoadCase"
    ) -> "_5023.SynchroniserHalfModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserHalfModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_part(
        self: "Self", design_entity: "_2896.SynchroniserPart"
    ) -> "_5025.SynchroniserPartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserPartModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_PART],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_part_load_case(
        self: "Self", design_entity_analysis: "_7895.SynchroniserPartLoadCase"
    ) -> "_5025.SynchroniserPartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserPartModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_sleeve(
        self: "Self", design_entity: "_2897.SynchroniserSleeve"
    ) -> "_5026.SynchroniserSleeveModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserSleeveModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_SLEEVE],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_sleeve_load_case(
        self: "Self", design_entity_analysis: "_7896.SynchroniserSleeveLoadCase"
    ) -> "_5026.SynchroniserSleeveModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserSleeveModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_SLEEVE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter(
        self: "Self", design_entity: "_2898.TorqueConverter"
    ) -> "_5028.TorqueConverterModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_load_case(
        self: "Self", design_entity_analysis: "_7900.TorqueConverterLoadCase"
    ) -> "_5028.TorqueConverterModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_pump(
        self: "Self", design_entity: "_2899.TorqueConverterPump"
    ) -> "_5029.TorqueConverterPumpModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterPumpModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_PUMP],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_pump_load_case(
        self: "Self", design_entity_analysis: "_7901.TorqueConverterPumpLoadCase"
    ) -> "_5029.TorqueConverterPumpModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterPumpModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_PUMP_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_turbine(
        self: "Self", design_entity: "_2901.TorqueConverterTurbine"
    ) -> "_5030.TorqueConverterTurbineModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterTurbineModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_TURBINE],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_turbine_load_case(
        self: "Self", design_entity_analysis: "_7902.TorqueConverterTurbineLoadCase"
    ) -> "_5030.TorqueConverterTurbineModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterTurbineModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_TURBINE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2555.ShaftToMountableComponentConnection"
    ) -> "_5007.ShaftToMountableComponentConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ShaftToMountableComponentConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7877.ShaftToMountableComponentConnectionLoadCase",
    ) -> "_5007.ShaftToMountableComponentConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ShaftToMountableComponentConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_belt_connection(
        self: "Self", design_entity: "_2533.CVTBeltConnection"
    ) -> "_4936.CVTBeltConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CVTBeltConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_belt_connection_load_case(
        self: "Self", design_entity_analysis: "_7776.CVTBeltConnectionLoadCase"
    ) -> "_4936.CVTBeltConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CVTBeltConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_BELT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_connection(
        self: "Self", design_entity: "_2528.BeltConnection"
    ) -> "_4904.BeltConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BeltConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_connection_load_case(
        self: "Self", design_entity_analysis: "_7742.BeltConnectionLoadCase"
    ) -> "_4904.BeltConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BeltConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coaxial_connection(
        self: "Self", design_entity: "_2529.CoaxialConnection"
    ) -> "_4919.CoaxialConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CoaxialConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COAXIAL_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_coaxial_connection_load_case(
        self: "Self", design_entity_analysis: "_7758.CoaxialConnectionLoadCase"
    ) -> "_4919.CoaxialConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CoaxialConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COAXIAL_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_connection(
        self: "Self", design_entity: "_2532.Connection"
    ) -> "_4930.ConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_connection_load_case(
        self: "Self", design_entity_analysis: "_7771.ConnectionLoadCase"
    ) -> "_4930.ConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_inter_mountable_component_connection(
        self: "Self", design_entity: "_2541.InterMountableComponentConnection"
    ) -> "_4965.InterMountableComponentConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.InterMountableComponentConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_inter_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7833.InterMountableComponentConnectionLoadCase",
    ) -> "_4965.InterMountableComponentConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.InterMountableComponentConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_connection(
        self: "Self", design_entity: "_2547.PlanetaryConnection"
    ) -> "_4992.PlanetaryConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_connection_load_case(
        self: "Self", design_entity_analysis: "_7856.PlanetaryConnectionLoadCase"
    ) -> "_4992.PlanetaryConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_connection(
        self: "Self", design_entity: "_2552.RollingRingConnection"
    ) -> "_5001.RollingRingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RollingRingConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_connection_load_case(
        self: "Self", design_entity_analysis: "_7872.RollingRingConnectionLoadCase"
    ) -> "_5001.RollingRingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RollingRingConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2525.AbstractShaftToMountableComponentConnection"
    ) -> "_4898.AbstractShaftToMountableComponentConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftToMountableComponentConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7731.AbstractShaftToMountableComponentConnectionLoadCase",
    ) -> "_4898.AbstractShaftToMountableComponentConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftToMountableComponentConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh(
        self: "Self", design_entity: "_2561.BevelDifferentialGearMesh"
    ) -> "_4906.BevelDifferentialGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7745.BevelDifferentialGearMeshLoadCase"
    ) -> "_4906.BevelDifferentialGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_mesh(
        self: "Self", design_entity: "_2565.ConceptGearMesh"
    ) -> "_4924.ConceptGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7764.ConceptGearMeshLoadCase"
    ) -> "_4924.ConceptGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_mesh(
        self: "Self", design_entity: "_2571.FaceGearMesh"
    ) -> "_4952.FaceGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FaceGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7807.FaceGearMeshLoadCase"
    ) -> "_4952.FaceGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FaceGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh(
        self: "Self", design_entity: "_2585.StraightBevelDiffGearMesh"
    ) -> "_5015.StraightBevelDiffGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7886.StraightBevelDiffGearMeshLoadCase"
    ) -> "_5015.StraightBevelDiffGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_mesh(
        self: "Self", design_entity: "_2563.BevelGearMesh"
    ) -> "_4911.BevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7750.BevelGearMeshLoadCase"
    ) -> "_4911.BevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_mesh(
        self: "Self", design_entity: "_2567.ConicalGearMesh"
    ) -> "_4927.ConicalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7768.ConicalGearMeshLoadCase"
    ) -> "_4927.ConicalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh(
        self: "Self", design_entity: "_2559.AGMAGleasonConicalGearMesh"
    ) -> "_4899.AGMAGleasonConicalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7736.AGMAGleasonConicalGearMeshLoadCase"
    ) -> "_4899.AGMAGleasonConicalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh(
        self: "Self", design_entity: "_2569.CylindricalGearMesh"
    ) -> "_4943.CylindricalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7785.CylindricalGearMeshLoadCase"
    ) -> "_4943.CylindricalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_mesh(
        self: "Self", design_entity: "_2575.HypoidGearMesh"
    ) -> "_4962.HypoidGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7828.HypoidGearMeshLoadCase"
    ) -> "_4962.HypoidGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "Self", design_entity: "_2578.KlingelnbergCycloPalloidConicalGearMesh"
    ) -> "_4966.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7835.KlingelnbergCycloPalloidConicalGearMeshLoadCase",
    ) -> "_4966.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "Self", design_entity: "_2579.KlingelnbergCycloPalloidHypoidGearMesh"
    ) -> "_4969.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7838.KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
    ) -> "_4969.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2580.KlingelnbergCycloPalloidSpiralBevelGearMesh"
    ) -> "_4972.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7841.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
    ) -> "_4972.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2583.SpiralBevelGearMesh"
    ) -> "_5009.SpiralBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7880.SpiralBevelGearMeshLoadCase"
    ) -> "_5009.SpiralBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh(
        self: "Self", design_entity: "_2587.StraightBevelGearMesh"
    ) -> "_5018.StraightBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7889.StraightBevelGearMeshLoadCase"
    ) -> "_5018.StraightBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_mesh(
        self: "Self", design_entity: "_2589.WormGearMesh"
    ) -> "_5036.WormGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.WormGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7910.WormGearMeshLoadCase"
    ) -> "_5036.WormGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.WormGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh(
        self: "Self", design_entity: "_2591.ZerolBevelGearMesh"
    ) -> "_5039.ZerolBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7913.ZerolBevelGearMeshLoadCase"
    ) -> "_5039.ZerolBevelGearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_mesh(
        self: "Self", design_entity: "_2573.GearMesh"
    ) -> "_4958.GearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GearMeshModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7814.GearMeshLoadCase"
    ) -> "_4958.GearMeshModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GearMeshModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection(
        self: "Self", design_entity: "_2595.CycloidalDiscCentralBearingConnection"
    ) -> "_4940.CycloidalDiscCentralBearingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalDiscCentralBearingConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7780.CycloidalDiscCentralBearingConnectionLoadCase",
    ) -> "_4940.CycloidalDiscCentralBearingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalDiscCentralBearingConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection(
        self: "Self", design_entity: "_2598.CycloidalDiscPlanetaryBearingConnection"
    ) -> "_4942.CycloidalDiscPlanetaryBearingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalDiscPlanetaryBearingConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7782.CycloidalDiscPlanetaryBearingConnectionLoadCase",
    ) -> "_4942.CycloidalDiscPlanetaryBearingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CycloidalDiscPlanetaryBearingConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection(
        self: "Self", design_entity: "_2601.RingPinsToDiscConnection"
    ) -> "_4999.RingPinsToDiscConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RingPinsToDiscConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_TO_DISC_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection_load_case(
        self: "Self", design_entity_analysis: "_7870.RingPinsToDiscConnectionLoadCase"
    ) -> "_4999.RingPinsToDiscConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RingPinsToDiscConnectionModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection(
        self: "Self", design_entity: "_2608.PartToPartShearCouplingConnection"
    ) -> "_4989.PartToPartShearCouplingConnectionModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingConnectionModalAnalysis

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft(
        self: "Self", design_entity: "_2705.AbstractShaft"
    ) -> "_4896.AbstractShaftModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_load_case(
        self: "Self", design_entity_analysis: "_7729.AbstractShaftLoadCase"
    ) -> "_4896.AbstractShaftModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone(
        self: "Self", design_entity: "_2736.Microphone"
    ) -> "_4978.MicrophoneModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MicrophoneModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Microphone)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone_load_case(
        self: "Self", design_entity_analysis: "_7847.MicrophoneLoadCase"
    ) -> "_4978.MicrophoneModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MicrophoneModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MicrophoneLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone_array(
        self: "Self", design_entity: "_2737.MicrophoneArray"
    ) -> "_4977.MicrophoneArrayModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MicrophoneArrayModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MicrophoneArray)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_ARRAY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone_array_load_case(
        self: "Self", design_entity_analysis: "_7846.MicrophoneArrayLoadCase"
    ) -> "_4977.MicrophoneArrayModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MicrophoneArrayModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MicrophoneArrayLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_ARRAY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_assembly(
        self: "Self", design_entity: "_2704.AbstractAssembly"
    ) -> "_4895.AbstractAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractAssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_assembly_load_case(
        self: "Self", design_entity_analysis: "_7728.AbstractAssemblyLoadCase"
    ) -> "_4895.AbstractAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractAssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing(
        self: "Self", design_entity: "_2706.AbstractShaftOrHousing"
    ) -> "_4897.AbstractShaftOrHousingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftOrHousingModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing_load_case(
        self: "Self", design_entity_analysis: "_7730.AbstractShaftOrHousingLoadCase"
    ) -> "_4897.AbstractShaftOrHousingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftOrHousingModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bearing(
        self: "Self", design_entity: "_2709.Bearing"
    ) -> "_4903.BearingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BearingModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEARING],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bearing_load_case(
        self: "Self", design_entity_analysis: "_7741.BearingLoadCase"
    ) -> "_4903.BearingModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BearingModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEARING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolt(
        self: "Self", design_entity: "_2712.Bolt"
    ) -> "_4915.BoltModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BoltModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolt_load_case(
        self: "Self", design_entity_analysis: "_7753.BoltLoadCase"
    ) -> "_4915.BoltModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BoltModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolted_joint(
        self: "Self", design_entity: "_2713.BoltedJoint"
    ) -> "_4914.BoltedJointModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BoltedJointModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLTED_JOINT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolted_joint_load_case(
        self: "Self", design_entity_analysis: "_7752.BoltedJointLoadCase"
    ) -> "_4914.BoltedJointModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BoltedJointModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLTED_JOINT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_component(
        self: "Self", design_entity: "_2715.Component"
    ) -> "_4920.ComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_component_load_case(
        self: "Self", design_entity_analysis: "_7759.ComponentLoadCase"
    ) -> "_4920.ComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_connector(
        self: "Self", design_entity: "_2718.Connector"
    ) -> "_4931.ConnectorModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConnectorModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Connector)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTOR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_connector_load_case(
        self: "Self", design_entity_analysis: "_7772.ConnectorLoadCase"
    ) -> "_4931.ConnectorModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConnectorModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTOR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_datum(
        self: "Self", design_entity: "_2719.Datum"
    ) -> "_4947.DatumModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.DatumModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Datum)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DATUM],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_datum_load_case(
        self: "Self", design_entity_analysis: "_7791.DatumLoadCase"
    ) -> "_4947.DatumModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.DatumModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DATUM_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_external_cad_model(
        self: "Self", design_entity: "_2724.ExternalCADModel"
    ) -> "_4951.ExternalCADModelModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ExternalCADModelModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_EXTERNAL_CAD_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_external_cad_model_load_case(
        self: "Self", design_entity_analysis: "_7805.ExternalCADModelLoadCase"
    ) -> "_4951.ExternalCADModelModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ExternalCADModelModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_EXTERNAL_CAD_MODEL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_fe_part(
        self: "Self", design_entity: "_2725.FEPart"
    ) -> "_4955.FEPartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FEPartModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FE_PART],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_fe_part_load_case(
        self: "Self", design_entity_analysis: "_7809.FEPartLoadCase"
    ) -> "_4955.FEPartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FEPartModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FE_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_flexible_pin_assembly(
        self: "Self", design_entity: "_2726.FlexiblePinAssembly"
    ) -> "_4956.FlexiblePinAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FlexiblePinAssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FLEXIBLE_PIN_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_flexible_pin_assembly_load_case(
        self: "Self", design_entity_analysis: "_7810.FlexiblePinAssemblyLoadCase"
    ) -> "_4956.FlexiblePinAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FlexiblePinAssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_assembly(
        self: "Self", design_entity: "_2703.Assembly"
    ) -> "_4902.AssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_assembly_load_case(
        self: "Self", design_entity_analysis: "_7740.AssemblyLoadCase"
    ) -> "_4902.AssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_guide_dxf_model(
        self: "Self", design_entity: "_2727.GuideDxfModel"
    ) -> "_4961.GuideDxfModelModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GuideDxfModelModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GUIDE_DXF_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_guide_dxf_model_load_case(
        self: "Self", design_entity_analysis: "_7818.GuideDxfModelLoadCase"
    ) -> "_4961.GuideDxfModelModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GuideDxfModelModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GUIDE_DXF_MODEL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_mass_disc(
        self: "Self", design_entity: "_2734.MassDisc"
    ) -> "_4975.MassDiscModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MassDiscModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MASS_DISC],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_mass_disc_load_case(
        self: "Self", design_entity_analysis: "_7843.MassDiscLoadCase"
    ) -> "_4975.MassDiscModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MassDiscModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MASS_DISC_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_measurement_component(
        self: "Self", design_entity: "_2735.MeasurementComponent"
    ) -> "_4976.MeasurementComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MeasurementComponentModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MEASUREMENT_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_measurement_component_load_case(
        self: "Self", design_entity_analysis: "_7844.MeasurementComponentLoadCase"
    ) -> "_4976.MeasurementComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MeasurementComponentModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MEASUREMENT_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_mountable_component(
        self: "Self", design_entity: "_2738.MountableComponent"
    ) -> "_4984.MountableComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MountableComponentModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MOUNTABLE_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_mountable_component_load_case(
        self: "Self", design_entity_analysis: "_7848.MountableComponentLoadCase"
    ) -> "_4984.MountableComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.MountableComponentModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MOUNTABLE_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_oil_seal(
        self: "Self", design_entity: "_2740.OilSeal"
    ) -> "_4986.OilSealModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.OilSealModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_OIL_SEAL],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_oil_seal_load_case(
        self: "Self", design_entity_analysis: "_7850.OilSealLoadCase"
    ) -> "_4986.OilSealModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.OilSealModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_OIL_SEAL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part(
        self: "Self", design_entity: "_2743.Part"
    ) -> "_4988.PartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.Part)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_load_case(
        self: "Self", design_entity_analysis: "_7852.PartLoadCase"
    ) -> "_4988.PartModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_planet_carrier(
        self: "Self", design_entity: "_2745.PlanetCarrier"
    ) -> "_4994.PlanetCarrierModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PlanetCarrierModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANET_CARRIER],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_planet_carrier_load_case(
        self: "Self", design_entity_analysis: "_7859.PlanetCarrierLoadCase"
    ) -> "_4994.PlanetCarrierModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PlanetCarrierModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANET_CARRIER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_point_load(
        self: "Self", design_entity: "_2747.PointLoad"
    ) -> "_4995.PointLoadModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PointLoadModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POINT_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_point_load_load_case(
        self: "Self", design_entity_analysis: "_7862.PointLoadLoadCase"
    ) -> "_4995.PointLoadModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PointLoadModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POINT_LOAD_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_power_load(
        self: "Self", design_entity: "_2748.PowerLoad"
    ) -> "_4996.PowerLoadModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PowerLoadModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POWER_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_power_load_load_case(
        self: "Self", design_entity_analysis: "_7863.PowerLoadLoadCase"
    ) -> "_4996.PowerLoadModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PowerLoadModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POWER_LOAD_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_root_assembly(
        self: "Self", design_entity: "_2751.RootAssembly"
    ) -> "_5003.RootAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RootAssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROOT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_root_assembly_load_case(
        self: "Self", design_entity_analysis: "_7874.RootAssemblyLoadCase"
    ) -> "_5003.RootAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.RootAssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROOT_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_specialised_assembly(
        self: "Self", design_entity: "_2753.SpecialisedAssembly"
    ) -> "_5008.SpecialisedAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpecialisedAssemblyModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPECIALISED_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_specialised_assembly_load_case(
        self: "Self", design_entity_analysis: "_7878.SpecialisedAssemblyLoadCase"
    ) -> "_5008.SpecialisedAssemblyModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpecialisedAssemblyModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPECIALISED_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_unbalanced_mass(
        self: "Self", design_entity: "_2754.UnbalancedMass"
    ) -> "_5031.UnbalancedMassModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.UnbalancedMassModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_UNBALANCED_MASS],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_unbalanced_mass_load_case(
        self: "Self", design_entity_analysis: "_7907.UnbalancedMassLoadCase"
    ) -> "_5031.UnbalancedMassModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.UnbalancedMassModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_UNBALANCED_MASS_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_virtual_component(
        self: "Self", design_entity: "_2756.VirtualComponent"
    ) -> "_5032.VirtualComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.VirtualComponentModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_VIRTUAL_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_virtual_component_load_case(
        self: "Self", design_entity_analysis: "_7908.VirtualComponentLoadCase"
    ) -> "_5032.VirtualComponentModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.VirtualComponentModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_VIRTUAL_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft(
        self: "Self", design_entity: "_2759.Shaft"
    ) -> "_5005.ShaftModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ShaftModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_load_case(
        self: "Self", design_entity_analysis: "_7876.ShaftLoadCase"
    ) -> "_5005.ShaftModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ShaftModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear(
        self: "Self", design_entity: "_2803.ConceptGear"
    ) -> "_4925.ConceptGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_load_case(
        self: "Self", design_entity_analysis: "_7763.ConceptGearLoadCase"
    ) -> "_4925.ConceptGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_set(
        self: "Self", design_entity: "_2804.ConceptGearSet"
    ) -> "_4926.ConceptGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7765.ConceptGearSetLoadCase"
    ) -> "_4926.ConceptGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear(
        self: "Self", design_entity: "_2810.FaceGear"
    ) -> "_4953.FaceGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FaceGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_load_case(
        self: "Self", design_entity_analysis: "_7806.FaceGearLoadCase"
    ) -> "_4953.FaceGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FaceGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_set(
        self: "Self", design_entity: "_2811.FaceGearSet"
    ) -> "_4954.FaceGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FaceGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7808.FaceGearSetLoadCase"
    ) -> "_4954.FaceGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.FaceGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear(
        self: "Self", design_entity: "_2795.AGMAGleasonConicalGear"
    ) -> "_4900.AGMAGleasonConicalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_load_case(
        self: "Self", design_entity_analysis: "_7735.AGMAGleasonConicalGearLoadCase"
    ) -> "_4900.AGMAGleasonConicalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set(
        self: "Self", design_entity: "_2796.AGMAGleasonConicalGearSet"
    ) -> "_4901.AGMAGleasonConicalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7737.AGMAGleasonConicalGearSetLoadCase"
    ) -> "_4901.AGMAGleasonConicalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear(
        self: "Self", design_entity: "_2797.BevelDifferentialGear"
    ) -> "_4907.BevelDifferentialGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_load_case(
        self: "Self", design_entity_analysis: "_7744.BevelDifferentialGearLoadCase"
    ) -> "_4907.BevelDifferentialGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_set(
        self: "Self", design_entity: "_2798.BevelDifferentialGearSet"
    ) -> "_4908.BevelDifferentialGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7746.BevelDifferentialGearSetLoadCase"
    ) -> "_4908.BevelDifferentialGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear(
        self: "Self", design_entity: "_2799.BevelDifferentialPlanetGear"
    ) -> "_4909.BevelDifferentialPlanetGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialPlanetGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7747.BevelDifferentialPlanetGearLoadCase",
    ) -> "_4909.BevelDifferentialPlanetGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialPlanetGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear(
        self: "Self", design_entity: "_2800.BevelDifferentialSunGear"
    ) -> "_4910.BevelDifferentialSunGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialSunGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear_load_case(
        self: "Self", design_entity_analysis: "_7748.BevelDifferentialSunGearLoadCase"
    ) -> "_4910.BevelDifferentialSunGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialSunGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear(
        self: "Self", design_entity: "_2801.BevelGear"
    ) -> "_4912.BevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7749.BevelGearLoadCase"
    ) -> "_4912.BevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_set(
        self: "Self", design_entity: "_2802.BevelGearSet"
    ) -> "_4913.BevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7751.BevelGearSetLoadCase"
    ) -> "_4913.BevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.BevelGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear(
        self: "Self", design_entity: "_2805.ConicalGear"
    ) -> "_4928.ConicalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_load_case(
        self: "Self", design_entity_analysis: "_7766.ConicalGearLoadCase"
    ) -> "_4928.ConicalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_set(
        self: "Self", design_entity: "_2806.ConicalGearSet"
    ) -> "_4929.ConicalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7770.ConicalGearSetLoadCase"
    ) -> "_4929.ConicalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear(
        self: "Self", design_entity: "_2807.CylindricalGear"
    ) -> "_4944.CylindricalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_load_case(
        self: "Self", design_entity_analysis: "_7783.CylindricalGearLoadCase"
    ) -> "_4944.CylindricalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_set(
        self: "Self", design_entity: "_2808.CylindricalGearSet"
    ) -> "_4945.CylindricalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7787.CylindricalGearSetLoadCase"
    ) -> "_4945.CylindricalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_planet_gear(
        self: "Self", design_entity: "_2809.CylindricalPlanetGear"
    ) -> "_4946.CylindricalPlanetGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalPlanetGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_planet_gear_load_case(
        self: "Self", design_entity_analysis: "_7788.CylindricalPlanetGearLoadCase"
    ) -> "_4946.CylindricalPlanetGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.CylindricalPlanetGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear(
        self: "Self", design_entity: "_2812.Gear"
    ) -> "_4959.GearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_load_case(
        self: "Self", design_entity_analysis: "_7812.GearLoadCase"
    ) -> "_4959.GearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_set(
        self: "Self", design_entity: "_2814.GearSet"
    ) -> "_4960.GearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7817.GearSetLoadCase"
    ) -> "_4960.GearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear(
        self: "Self", design_entity: "_2816.HypoidGear"
    ) -> "_4963.HypoidGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_load_case(
        self: "Self", design_entity_analysis: "_7827.HypoidGearLoadCase"
    ) -> "_4963.HypoidGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_set(
        self: "Self", design_entity: "_2817.HypoidGearSet"
    ) -> "_4964.HypoidGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7829.HypoidGearSetLoadCase"
    ) -> "_4964.HypoidGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", design_entity: "_2818.KlingelnbergCycloPalloidConicalGear"
    ) -> "_4967.KlingelnbergCycloPalloidConicalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7834.KlingelnbergCycloPalloidConicalGearLoadCase",
    ) -> "_4967.KlingelnbergCycloPalloidConicalGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", design_entity: "_2819.KlingelnbergCycloPalloidConicalGearSet"
    ) -> "_4968.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7836.KlingelnbergCycloPalloidConicalGearSetLoadCase",
    ) -> "_4968.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", design_entity: "_2820.KlingelnbergCycloPalloidHypoidGear"
    ) -> "_4970.KlingelnbergCycloPalloidHypoidGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7837.KlingelnbergCycloPalloidHypoidGearLoadCase",
    ) -> "_4970.KlingelnbergCycloPalloidHypoidGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", design_entity: "_2821.KlingelnbergCycloPalloidHypoidGearSet"
    ) -> "_4971.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7839.KlingelnbergCycloPalloidHypoidGearSetLoadCase",
    ) -> "_4971.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", design_entity: "_2822.KlingelnbergCycloPalloidSpiralBevelGear"
    ) -> "_4973.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7840.KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
    ) -> "_4973.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2823.KlingelnbergCycloPalloidSpiralBevelGearSet"
    ) -> "_4974.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7842.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
    ) -> "_4974.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_gear_set(
        self: "Self", design_entity: "_2824.PlanetaryGearSet"
    ) -> "_4993.PlanetaryGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7857.PlanetaryGearSetLoadCase"
    ) -> "_4993.PlanetaryGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear(
        self: "Self", design_entity: "_2826.SpiralBevelGear"
    ) -> "_5010.SpiralBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7879.SpiralBevelGearLoadCase"
    ) -> "_5010.SpiralBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2827.SpiralBevelGearSet"
    ) -> "_5011.SpiralBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7881.SpiralBevelGearSetLoadCase"
    ) -> "_5011.SpiralBevelGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear(
        self: "Self", design_entity: "_2828.StraightBevelDiffGear"
    ) -> "_5016.StraightBevelDiffGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_load_case(
        self: "Self", design_entity_analysis: "_7885.StraightBevelDiffGearLoadCase"
    ) -> "_5016.StraightBevelDiffGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set(
        self: "Self", design_entity: "_2829.StraightBevelDiffGearSet"
    ) -> "_5017.StraightBevelDiffGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearSetModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7887.StraightBevelDiffGearSetLoadCase"
    ) -> "_5017.StraightBevelDiffGearSetModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearSetModalAnalysis

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear(
        self: "Self", design_entity: "_2830.StraightBevelGear"
    ) -> "_5019.StraightBevelGearModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearModalAnalysis

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @property
    def cast_to(self: "Self") -> "_Cast_ModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ModalAnalysis
        """
        return _Cast_ModalAnalysis(self)
