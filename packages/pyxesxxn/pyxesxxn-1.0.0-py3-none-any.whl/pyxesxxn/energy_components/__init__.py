"""Energy Components Extension for PyXESXXN.

This module provides comprehensive physical modeling for over 130 energy system components,
covering renewable energy, electrochemical storage, hydrogen systems, ammonia/alcohol-based energy,
combined heat and power systems, carbon management, flexible loads, and distribution networks.

All components are implemented as extensions to the PyXESXXN equipment library without modifying core code.
"""

from .base import (
    # Extended enumerations
    ExtendedEquipmentType,
    ExtendedEquipmentCategory,
    
    # Base classes for extended components
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    
    # Utility functions
    create_extended_component,
    register_component_factory,
    get_component_factory
)

from .renewable_energy import (
    # Photovoltaic systems
    FixedTiltPVSystem,
    SingleAxisTrackingPVSystem,
    DualAxisTrackingPVSystem,
    DistributedRoofPV,
    ConcentratedSolarPowerPlant,
    
    # Wind energy systems
    FixedSpeedWindTurbine,
    VariableSpeedDFIGWindTurbine,
    OffshoreDirectDriveWindTurbine,
    SmallVerticalAxisWindTurbine,
    
    # Other renewable energy
    TidalPowerGenerator,
    WaveEnergyConverter,
    RunOfRiverHydroGenerator,
    ReservoirHydroGenerator,
    BiomassDirectCombustionGenerator,
    BiomassGasificationPowerSystem,
    GeothermalORCPowerPlant,
    CSPTowerSystem,
    CSPTroughSystem,
    SolarThermoelectricGenerator
)

from .electrochemical_storage import (
    # Battery systems
    LithiumIronPhosphateBattery,
    NMCBattery,
    LeadCarbonBattery,
    VanadiumRedoxFlowBattery,
    SodiumSulfurBattery,
    SodiumIonBattery,
    SolidStateBattery,
    Supercapacitor,
    FlywheelEnergyStorage,
    
    # Other storage systems
    TraditionalCompressedAirStorage,
    AdiabaticCompressedAirStorage,
    LargePumpedHydroStorage,
    SmallModularPumpedHydroStorage
)

from .hydrogen_system import (
    # Electrolyzers
    AlkalineElectrolyzer,
    PEMElectrolyzer,
    SolidOxideElectrolyzer,
    
    # Hydrogen storage
    HighPressureHydrogenTank,
    LiquidHydrogenTank,
    MetalHydrideHydrogenStorage,
    SaltCavernHydrogenStorage,
    
    # Hydrogen utilization
    PEMFuelCell,
    SolidOxideFuelCell,
    PhosphoricAcidFuelCell,
    HydrogenCompressor,
    HydrogenPurificationPSA,
    HydrogenRefuelingStation,
    HydrogenPipeline
)

from .ammonia_alcohol import (
    # Ammonia systems
    HaberBoschAmmoniaSynthesis,
    ElectrocatalyticAmmoniaSynthesis,
    AmmoniaStorageTank,
    AmmoniaCrackingSystem,
    DirectAmmoniaFuelCell,
    AmmoniaFuelGasTurbine,
    
    # Methanol systems
    MethanolSynthesisSystem,
    DirectMethanolFuelCell,
    
    # Ethanol systems
    EthanolFuelCell
)

from .chp_gas_systems import (
    # CHP systems
    NaturalGasICECHP,
    MicroGasTurbineCHP,
    IndustrialGasTurbineCHP,
    GasSteamCombinedCyclePlant,
    StirlingEngine,
    OrganicRankineCycleWasteHeatRecovery,
    
    # Cooling systems
    AbsorptionChiller,
    
    # Boilers and heat pumps
    NaturalGasBoiler,
    AirSourceHeatPump,
    
    # Thermal storage
    SensibleHeatStorageTank
)

from .carbon_management import (
    # Carbon capture
    PostCombustionCarbonCapture,
    DirectAirCapture,
    
    # Carbon transport and storage
    CO2Compressor,
    CO2StorageTank,
    GeologicCO2Storage
)

from .flexible_loads import (
    # Building loads
    CommercialBuildingLoad,
    IndustrialAdjustableLoad,
    ResidentialDemandResponseLoad,
    
    # EV charging
    DCFastEVCharger,
    
    # Other flexible loads
    DataCenterAdjustableLoad
)

from .transmission_distribution import (
    # Power lines
    ACGridLine,
    DCCable,
    ACToDCConverter,
    LoadTapChangerTransformer,
    StaticVarCompensator
)

from .control_auxiliary import (
    # Control and management systems
    EnergyManagementSystem,
    DistributedCoordinatedController,
    FrequencyRegulationReserveSystem,
    
    # Forecasting modules
    WeatherForecastingModule,
    LoadForecastingModule,
    
    # Carbon tracking
    CarbonFlowTrackingModule
)

from .emerging_technologies import (
    # Emerging energy technologies
    MagneticConfinementFusionReactor,
    SpaceSolarPowerStation,
    OceanThermalEnergyConversion,
    SuperconductingMagneticEnergyStorage,
    GravityEnergyStorage
)

from .building_cluster_modeling import (
    # Building type definitions
    BuildingType,
    BuildingTemperatureParams,
    BuildingIlluminanceParams,
    
    # Configuration classes
    BuildingConfig,
    HydrogenHeatRecoveryConfig,
    
    # Building components
    BaseBuilding,
    ResidentialBuilding,
    IndustrialBuilding,
    CommercialBuilding,
    BuildingCluster,
    HydrogenHeatRecoverySystem
)

__all__ = [
    # Base classes and enumerations
    'ExtendedEquipmentType',
    'ExtendedEquipmentCategory',
    'ExtendedEnergyComponent',
    'ExtendedEquipmentConfig',
    'create_extended_component',
    'register_component_factory',
    'get_component_factory',
    
    # Renewable energy components
    'FixedTiltPVSystem',
    'SingleAxisTrackingPVSystem',
    'DualAxisTrackingPVSystem',
    'DistributedRoofPV',
    'ConcentratedSolarPowerPlant',
    'FixedSpeedWindTurbine',
    'VariableSpeedDFIGWindTurbine',
    'OffshoreDirectDriveWindTurbine',
    'SmallVerticalAxisWindTurbine',
    'TidalPowerGenerator',
    'WaveEnergyConverter',
    'RunOfRiverHydroGenerator',
    'ReservoirHydroGenerator',
    'BiomassDirectCombustionGenerator',
    'BiomassGasificationPowerSystem',
    'GeothermalORCPowerPlant',
    'CSPTowerSystem',
    'CSPTroughSystem',
    'SolarThermoelectricGenerator',
    
    # Electrochemical storage components
    'LithiumIronPhosphateBattery',
    'NMCBattery',
    'LeadCarbonBattery',
    'VanadiumRedoxFlowBattery',
    'SodiumSulfurBattery',
    'SodiumIonBattery',
    'SolidStateBattery',
    'Supercapacitor',
    'FlywheelEnergyStorage',
    'TraditionalCompressedAirStorage',
    'AdiabaticCompressedAirStorage',
    'LargePumpedHydroStorage',
    'SmallModularPumpedHydroStorage',
    
    # Hydrogen system components
    'AlkalineElectrolyzer',
    'PEMElectrolyzer',
    'SolidOxideElectrolyzer',
    'HighPressureHydrogenTank',
    'LiquidHydrogenTank',
    'MetalHydrideHydrogenStorage',
    'SaltCavernHydrogenStorage',
    'PEMFuelCell',
    'SolidOxideFuelCell',
    'PhosphoricAcidFuelCell',
    'HydrogenCompressor',
    'HydrogenPurificationPSA',
    'HydrogenRefuelingStation',
    'HydrogenPipeline',
    
    # Ammonia/Alcohol energy components
    'HaberBoschAmmoniaSynthesis',
    'ElectrocatalyticAmmoniaSynthesis',
    'AmmoniaStorageTank',
    'AmmoniaCrackingSystem',
    'DirectAmmoniaFuelCell',
    'AmmoniaFuelGasTurbine',
    'MethanolSynthesisSystem',
    'DirectMethanolFuelCell',
    'EthanolFuelCell',
    
    # CHP and Gas systems
    'NaturalGasICECHP',
    'MicroGasTurbineCHP',
    'IndustrialGasTurbineCHP',
    'GasSteamCombinedCyclePlant',
    'StirlingEngine',
    'OrganicRankineCycleWasteHeatRecovery',
    'AbsorptionChiller',
    'NaturalGasBoiler',
    'AirSourceHeatPump',
    'SensibleHeatStorageTank',
    
    # Carbon management components
    'PostCombustionCarbonCapture',
    'DirectAirCapture',
    'CO2Compressor',
    'CO2StorageTank',
    'GeologicCO2Storage',
    
    # Flexible loads and terminals
    'CommercialBuildingLoad',
    'IndustrialAdjustableLoad',
    'ResidentialDemandResponseLoad',
    'DCFastEVCharger',
    'DataCenterAdjustableLoad',
    
    # Transmission and distribution components
    'ACGridLine',
    'DCCable',
    'ACToDCConverter',
    'LoadTapChangerTransformer',
    'StaticVarCompensator',
    
    # Control and auxiliary systems
    'EnergyManagementSystem',
    'DistributedCoordinatedController',
    'FrequencyRegulationReserveSystem',
    'WeatherForecastingModule',
    'LoadForecastingModule',
    'CarbonFlowTrackingModule',
    
    # Emerging technologies
    'MagneticConfinementFusionReactor',
    'SpaceSolarPowerStation',
    'OceanThermalEnergyConversion',
    'SuperconductingMagneticEnergyStorage',
    'GravityEnergyStorage',
    
    # Building cluster modeling
    'BuildingType',
    'BuildingTemperatureParams',
    'BuildingIlluminanceParams',
    'BuildingConfig',
    'HydrogenHeatRecoveryConfig',
    'BaseBuilding',
    'ResidentialBuilding',
    'IndustrialBuilding',
    'CommercialBuilding',
    'BuildingCluster',
    'HydrogenHeatRecoverySystem'
]
