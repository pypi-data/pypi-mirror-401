"""
Base classes and definitions for equipment library.

This module provides the fundamental classes, interfaces, and data structures
for all equipment in the library. It defines abstract base classes,
configuration management, and equipment categorization.
"""

import abc
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union, Set, Tuple, Type
import warnings

import numpy as np
import pandas as pd


class EquipmentCategory(Enum):
    """Equipment category enumeration."""
    GENERATION = "generation"
    STORAGE = "storage"
    CONVERSION = "conversion"
    TRANSPORT = "transport"
    LOADS = "loads"
    INFRASTRUCTURE = "infrastructure"
    CONTROL = "control"
    MEASUREMENT = "measurement"


class EquipmentType(Enum):
    """Equipment type enumeration."""
    # Generation equipment
    SOLAR_PV = "solar_pv"
    WIND_TURBINE = "wind_turbine"
    HYDRO_GENERATOR = "hydro_generator"
    BIOMASS_GENERATOR = "biomass_generator"
    GAS_TURBINE = "gas_turbine"
    COMBINED_HEAT_POWER = "combined_heat_power"
    DIESEL_GENERATOR = "diesel_generator"
    WAVE_ENERGY_CONVERTER = "wave_energy_converter"
    SOLAR_PUMP = "solar_pump"
    
    # Storage equipment
    BATTERY_STORAGE = "battery_storage"
    HYDROGEN_STORAGE = "hydrogen_storage"
    THERMAL_STORAGE = "thermal_storage"
    PUMPED_HYDRO = "pumped_hydro"
    
    # Conversion equipment
    ELECTROLYZER = "electrolyzer"
    FUEL_CELL = "fuel_cell"
    HEAT_PUMP = "heat_pump"
    COMPRESSOR = "compressor"
    RECTIFIER = "rectifier"
    INVERTER = "inverter"
    
    # Transport equipment
    EV_CHARGING = "ev_charging"
    SHORE_POWER = "shore_power"
    CONTAINER_CRANE = "container_crane"
    HYDROGEN_REFUELING = "hydrogen_refueling"
    RTG_CRANE = "rtg_crane"
    PRESSURE_AUGMENTATION = "pressure_augmentation"
    BATTERY_VEHICLE = "battery_vehicle"
    FUEL_CELL_VEHICLE = "fuel_cell_vehicle"
    TRACTION_SYSTEM = "traction_system"
    TRACTION_SUBSTATION = "traction_substation"   
    
    # Loads
    INDUSTRIAL_LOAD = "industrial_load"
    COMMERCIAL_LOAD = "commercial_load"
    RESIDENTIAL_LOAD = "residential_load"
    DISTRICT_HEATING = "district_heating"
    SMART_APPLIANCE = "smart_appliance"
    
    # Infrastructure
    TRANSFORMER = "transformer"
    BUS_BAR = "bus_bar"
    PROTECTION_DEVICE = "protection_device"
    GRID_CONNECTION = "grid_connection"
    DESALINATION_PLANT = "desalination_plant"
    BOILER = "boiler"
    HEAT_EXCHANGER = "heat_exchanger"
    SOLAR_DESALINATION = "solar_desalination"
    POWER_DISTRIBUTION = "power_distribution"
    
    # Control equipment
    EMS = "energy_management_system"
    LOAD_CONTROLLER = "load_controller"
    STORAGE_CONTROLLER = "storage_controller"
    POWER_QUALITY_CONTROLLER = "power_quality_controller"
    
    # Measurement equipment
    SMART_METER = "smart_meter"
    SENSOR = "sensor"
    MONITORING_SYSTEM = "monitoring_system"


class EnergyCarrier(Enum):
    """Energy carrier enumeration."""
    ELECTRICITY = "electricity"
    HEAT = "heat"
    HYDROGEN = "hydrogen"
    NATURAL_GAS = "natural_gas"
    BIOFUEL = "biofuel"
    CO2 = "co2"
    SYNTHETIC_METHANE = "synthetic_methane"
    BIOMASS = "biomass"
    WASTE = "waste"
    SOLAR_RADIATION = "solar_radiation"
    SOLAR = "solar"
    WIND = "wind"
    WATER_FLOW = "water_flow"
    PRESSURE_AIR = "pressure_air"


@dataclass
class EquipmentConfig:
    """Equipment configuration data class.
    
    This class encapsulates all configuration parameters for an equipment
    instance, including technical specifications, operational parameters,
    and economic data.
    """
    
    # Equipment identification
    equipment_id: str
    name: str
    description: str
    category: EquipmentCategory
    equipment_type: EquipmentType
    
    # Technical specifications
    power_rating: float  # kW or MW
    voltage_level: Optional[float] = None  # kV
    efficiency: Optional[float] = None  # 0-1
    lifetime: Optional[int] = None  # years
    capacity: Optional[float] = None  # kWh for storage
    
    # Operational parameters
    min_part_load: Optional[float] = None  # 0-1
    max_part_load: Optional[float] = None  # 0-1
    ramp_rate: Optional[float] = None  # kW/min
    startup_time: Optional[float] = None  # hours
    shutdown_time: Optional[float] = None  # hours
    
    # Economic parameters
    investment_costs: Optional[float] = None  # €/kW
    operation_costs: Optional[float] = None  # €/MWh
    maintenance_costs: Optional[float] = None  # €/kW/year
    
    # Environmental parameters
    co2_emissions: Optional[float] = None  # kg CO2/kWh
    noise_level: Optional[float] = None  # dB
    footprint: Optional[float] = None  # m²
    
    # Scenario and location
    scenario: str = "universal"
    location: Optional[str] = None
    
    # Additional metadata
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    certification: Optional[str] = None
    installation_date: Optional[datetime] = None
    
    # Custom parameters
    custom_parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Compatibility settings
    supported_carriers: List[EnergyCarrier] = field(default_factory=list)
    compatible_voltage_levels: List[float] = field(default_factory=list)
    integration_requirements: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Configuration dictionary
        """
        config_dict = {}
        for key, value in self.__dict__.items():
            if key == 'supported_carriers':
                config_dict[key] = [carrier.value for carrier in value]
            elif key == 'custom_parameters' or key == 'integration_requirements':
                config_dict[key] = value.copy()
            elif isinstance(value, (datetime, EquipmentCategory, EquipmentType, EnergyCarrier)):
                config_dict[key] = value.value if hasattr(value, 'value') else str(value)
            else:
                config_dict[key] = value
        return config_dict
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'EquipmentConfig':
        """Create configuration from dictionary.
        
        Parameters
        ----------
        config_dict : Dict[str, Any]
            Configuration dictionary
            
        Returns
        -------
        EquipmentConfig
            Configuration instance
        """
        # Convert enum strings back to enums
        if 'category' in config_dict:
            config_dict['category'] = EquipmentCategory(config_dict['category'])
        if 'equipment_type' in config_dict:
            config_dict['equipment_type'] = EquipmentType(config_dict['equipment_type'])
        if 'supported_carriers' in config_dict:
            config_dict['supported_carriers'] = [
                EnergyCarrier(carrier) for carrier in config_dict['supported_carriers']
            ]
        
        # Handle datetime
        if 'installation_date' in config_dict and isinstance(config_dict['installation_date'], str):
            config_dict['installation_date'] = datetime.fromisoformat(config_dict['installation_date'])
        
        return cls(**config_dict)
    
    def update(self, **kwargs) -> 'EquipmentConfig':
        """Update configuration with new parameters.
        
        Parameters
        ----------
        **kwargs
            Parameters to update
            
        Returns
        -------
        EquipmentConfig
            Updated configuration
        """
        config_dict = self.to_dict()
        config_dict.update(kwargs)
        return EquipmentConfig.from_dict(config_dict)
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get configuration parameter value.
        
        Parameters
        ----------
        key : str
            Parameter key
        default : Any, optional
            Default value if parameter not found
            
        Returns
        -------
        Any
            Parameter value or default
        """
        return getattr(self, key, default) or self.custom_parameters.get(key, default)
    
    def validate(self) -> List[str]:
        """Validate configuration parameters.
        
        Returns
        -------
        List[str]
            List of validation errors
        """
        errors = []
        
        # Check required parameters
        if not self.power_rating or self.power_rating <= 0:
            errors.append("Invalid power rating")
        
        if self.efficiency is not None and not 0 <= self.efficiency <= 1:
            errors.append("Efficiency must be between 0 and 1")
        
        if self.lifetime is not None and self.lifetime <= 0:
            errors.append("Lifetime must be positive")
        
        # Check part-load parameters
        if self.min_part_load is not None and not 0 <= self.min_part_load <= 1:
            errors.append("Min part load must be between 0 and 1")
        
        if self.max_part_load is not None and not 0 <= self.max_part_load <= 1:
            errors.append("Max part load must be between 0 and 1")
        
        if (self.min_part_load is not None and self.max_part_load is not None and
            self.min_part_load > self.max_part_load):
            errors.append("Min part load cannot exceed max part load")
        
        return errors


class BaseEquipment(abc.ABC):
    """Abstract base class for all equipment.
    
    This class defines the common interface and functionality that all
    equipment types must implement. It provides methods for configuration,
    PyXESXXN integration, performance modeling, and metadata management.
    """
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[EquipmentConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize equipment.
        
        Parameters
        ----------
        equipment_id : str
            Unique equipment identifier
        config : EquipmentConfig, optional
            Equipment configuration
        location : str, optional
            Equipment location
        **kwargs
            Additional configuration parameters
        """
        self.equipment_id = equipment_id
        self.location = location
        
        # Create or update configuration
        if config is not None:
            self.config = config
        else:
            # Create default configuration and update with kwargs
            self.config = self._create_default_config(**kwargs)
        
        # Validate configuration
        validation_errors = self.config.validate()
        if validation_errors:
            raise ValueError(f"Invalid equipment configuration: {validation_errors}")
        
        # Equipment state
        self._is_operational = False
        self._current_state = {
            'power_output': 0.0,
            'efficiency': self.config.efficiency or 0.0,
            'operational_hours': 0.0,
            'maintenance_due': False
        }
        
        # Initialize equipment
        self._initialize_equipment()
    
    def _create_default_config(self, **kwargs) -> EquipmentConfig:
        """Create default configuration for the equipment type.
        
        Parameters
        ----------
        **kwargs
            Additional configuration parameters
            
        Returns
        -------
        EquipmentConfig
            Default configuration
        """
        # Default configuration will be overridden by subclasses
        return EquipmentConfig(
            equipment_id=self.equipment_id,
            name=self.__class__.__name__,
            description="Equipment instance",
            category=EquipmentCategory.INFRASTRUCTURE,
            equipment_type=EquipmentType.GRID_CONNECTION,
            power_rating=100.0,
            scenario=self.get_default_scenario(),
            location=self.location,
            **kwargs
        )
    
    def _initialize_equipment(self) -> None:
        """Initialize equipment-specific settings."""
        pass
    
    @property
    def equipment_id(self) -> str:
        """Equipment identifier."""
        return self._equipment_id
    
    @equipment_id.setter
    def equipment_id(self, value: str) -> None:
        if not value:
            raise ValueError("Equipment ID cannot be empty")
        self._equipment_id = value
    
    @property
    def config(self) -> EquipmentConfig:
        """Equipment configuration."""
        return self._config
    
    @config.setter
    def config(self, value: EquipmentConfig) -> None:
        if not isinstance(value, EquipmentConfig):
            raise TypeError("Config must be an EquipmentConfig instance")
        self._config = value
    
    @property
    def name(self) -> str:
        """Equipment name."""
        return self.config.name
    
    @property
    def category(self) -> EquipmentCategory:
        """Equipment category."""
        return self.config.category
    
    @property
    def equipment_type(self) -> EquipmentType:
        """Equipment type."""
        return self.config.equipment_type
    
    @property
    def power_rating(self) -> float:
        """Equipment power rating."""
        return self.config.power_rating
    
    @property
    def efficiency(self) -> float:
        """Current efficiency."""
        return self._current_state['efficiency']
    
    @property
    def is_operational(self) -> bool:
        """Equipment operational status."""
        return self._is_operational
    
    @property
    def current_state(self) -> Dict[str, Any]:
        """Current equipment state."""
        return self._current_state.copy()
    
    @abc.abstractmethod
    def get_default_scenario(self) -> str:
        """Get the default scenario for this equipment type.
        
        Returns
        -------
        str
            Default scenario name
        """
        pass
    
    def start_operation(self) -> bool:
        """Start equipment operation.
        
        Returns
        -------
        bool
            True if successfully started
        """
        try:
            self._is_operational = True
            self._current_state['operational_hours'] = 0.0
            return True
        except Exception as e:
            warnings.warn(f"Failed to start equipment {self.equipment_id}: {e}", UserWarning)
            return False
    
    def stop_operation(self) -> bool:
        """Stop equipment operation.
        
        Returns
        -------
        bool
            True if successfully stopped
        """
        try:
            self._is_operational = False
            return True
        except Exception as e:
            warnings.warn(f"Failed to stop equipment {self.equipment_id}: {e}", UserWarning)
            return False
    
    def get_current_performance(self) -> Dict[str, Any]:
        """Get current performance metrics.
        
        Returns
        -------
        Dict[str, Any]
            Performance metrics
        """
        return {
            'equipment_id': self.equipment_id,
            'power_output': self._current_state['power_output'],
            'efficiency': self.efficiency,
            'is_operational': self._is_operational,
            'operational_hours': self._current_state['operational_hours'],
            'maintenance_due': self._current_state['maintenance_due']
        }
    
    @abc.abstractmethod
    def create_components(self, network: 'PyXESXXNNetwork') -> Dict[str, Any]:
        """Create PyXESXXN components for this equipment.
        
        Parameters
        ----------
        network : PyXESXXNNetwork
            PyXESXXN network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyXESXXN components
        """
        pass
    
    @abc.abstractmethod
    def calculate_performance(self, 
                            input_power: float,
                            time_step: float = 1.0,
                            operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate equipment performance.
        
        Parameters
        ----------
        input_power : float
            Input power (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Performance calculation results
        """
        pass
    
    def get_equipment_metadata(self) -> Dict[str, Any]:
        """Get equipment metadata for database storage.
        
        Returns
        -------
        Dict[str, Any]
            Equipment metadata
        """
        return {
            'id': self.equipment_id,
            'name': self.name,
            'description': self.config.description,
            'category': self.category.value,
            'type': self.equipment_type.value,
            'scenario': self.config.scenario,
            'location': self.location,
            'manufacturer': self.config.manufacturer,
            'model': self.config.model,
            'config': self.config.to_dict()
        }
    
    def get_equipment_config(self) -> Dict[str, Any]:
        """Get equipment configuration dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Equipment configuration
        """
        return {
            'id': self.equipment_id,
            'scenario': self.config.scenario,
            'location': self.location,
            'config': self.config.to_dict()
        }
    
    def update_configuration(self, **kwargs) -> 'BaseEquipment':
        """Update equipment configuration.
        
        Parameters
        ----------
        **kwargs
            Configuration parameters to update
            
        Returns
        -------
        BaseEquipment
            Self reference for method chaining
        """
        # Validate that equipment is not operational for major changes
        operational_changes = {'power_rating', 'voltage_level', 'equipment_type'}
        if self._is_operational and any(key in operational_changes for key in kwargs):
            raise ValueError("Cannot modify operational parameters while equipment is running")
        
        # Update configuration
        new_config_dict = self.config.to_dict()
        new_config_dict.update(kwargs)
        self.config = EquipmentConfig.from_dict(new_config_dict)
        
        return self
    
    def get_supported_carriers(self) -> List[EnergyCarrier]:
        """Get list of supported energy carriers.
        
        Returns
        -------
        List[EnergyCarrier]
            Supported energy carriers
        """
        return self.config.supported_carriers or []
    
    def get_compatible_voltage_levels(self) -> List[float]:
        """Get list of compatible voltage levels.
        
        Returns
        -------
        List[float]
            Compatible voltage levels in kV
        """
        return self.config.compatible_voltage_levels or []
    
    def get_compatible_scenarios(self) -> List[str]:
        """Get list of compatible scenarios.
        
        Returns
        -------
        List[str]
            Compatible scenarios
        """
        if self.config.scenario == "universal":
            return ["urban", "rural", "port"]
        return [self.config.scenario]
    
    def get_integration_requirements(self) -> Dict[str, Any]:
        """Get integration requirements for system integration.
        
        Returns
        -------
        Dict[str, Any]
            Integration requirements
        """
        return self.config.integration_requirements.copy()
    
    def get_comparison_metrics(self) -> Dict[str, Any]:
        """Get metrics for equipment comparison.
        
        Returns
        -------
        Dict[str, Any]
            Comparison metrics
        """
        return {
            'power_rating': self.power_rating,
            'efficiency': self.efficiency,
            'lifetime': self.config.lifetime,
            'investment_costs': self.config.investment_costs,
            'co2_emissions': self.config.co2_emissions,
            'scenario': self.config.scenario,
            'category': self.category.value,
            'type': self.equipment_type.value
        }
    
    def estimate_costs(self, 
                      capacity_factor: float = 0.5,
                      operational_hours: float = 8760) -> Dict[str, Any]:
        """Estimate equipment costs.
        
        Parameters
        ----------
        capacity_factor : float
            Capacity factor (0-1)
        operational_hours : float
            Annual operational hours
            
        Returns
        -------
        Dict[str, Any]
            Cost estimates
        """
        annual_energy = self.power_rating * capacity_factor * operational_hours  # kWh/year
        
        costs = {
            'annual_energy_production': annual_energy,
            'capital_costs': self.config.investment_costs * self.power_rating if self.config.investment_costs else 0,
            'annual_operation_costs': (self.config.operation_costs * annual_energy / 1000 
                                     if self.config.operation_costs else 0),
            'annual_maintenance_costs': (self.config.maintenance_costs * self.power_rating 
                                       if self.config.maintenance_costs else 0),
            'levelized_cost_of_energy': 0.0
        }
        
        # Calculate LCOE
        total_annual_costs = costs['annual_operation_costs'] + costs['annual_maintenance_costs']
        if costs['capital_costs'] > 0 and annual_energy > 0:
            # Simplified LCOE calculation
            capital_recovery = (costs['capital_costs'] * 0.1) / annual_energy  # 10% discount rate
            costs['levelized_cost_of_energy'] = capital_recovery + (total_annual_costs / annual_energy)
        
        return costs
    
    def check_maintenance_requirements(self) -> bool:
        """Check if maintenance is required.
        
        Returns
        -------
        bool
            True if maintenance is required
        """
        operational_hours = self._current_state['operational_hours']
        
        # Simple maintenance check based on operational hours
        maintenance_intervals = {
            EquipmentType.SOLAR_PV: 8760 * 5,  # 5 years
            EquipmentType.WIND_TURBINE: 8760 * 2,  # 2 years
            EquipmentType.BATTERY_STORAGE: 8760 * 1,  # 1 year
        }
        
        interval = maintenance_intervals.get(self.equipment_type)
        if interval and operational_hours >= interval:
            self._current_state['maintenance_due'] = True
            return True
        
        return False
    
    def perform_maintenance(self) -> bool:
        """Perform equipment maintenance.
        
        Returns
        -------
        bool
            True if maintenance was successful
        """
        if not self._current_state['maintenance_due']:
            return True
        
        try:
            # Reset maintenance flag
            self._current_state['maintenance_due'] = False
            
            # Reset some performance parameters (e.g., efficiency)
            if self.config.efficiency:
                self._current_state['efficiency'] = min(self.config.efficiency * 1.02, 1.0)
            
            return True
        except Exception as e:
            warnings.warn(f"Maintenance failed for equipment {self.equipment_id}: {e}", UserWarning)
            return False
    
    def export_to_json(self, file_path: str) -> bool:
        """Export equipment configuration to JSON file.
        
        Parameters
        ----------
        file_path : str
            Output file path
            
        Returns
        -------
        bool
            True if successfully exported
        """
        try:
            export_data = self.get_equipment_config()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            warnings.warn(f"Failed to export equipment {self.equipment_id}: {e}", UserWarning)
            return False
    
    def clone(self, new_equipment_id: str, **kwargs) -> 'BaseEquipment':
        """Create a clone of this equipment.
        
        Parameters
        ----------
        new_equipment_id : str
            ID for the cloned equipment
        **kwargs
            Additional configuration parameters for the clone
            
        Returns
        -------
        BaseEquipment
            Cloned equipment instance
        """
        # Create new configuration
        config_dict = self.config.to_dict()
        config_dict.update(kwargs)
        
        # Create cloned equipment
        cloned_config = EquipmentConfig.from_dict(config_dict)
        
        return self.__class__(
            equipment_id=new_equipment_id,
            config=cloned_config,
            location=self.location
        )
    
    def __repr__(self) -> str:
        """String representation of equipment."""
        return (f"{self.__class__.__name__}(id='{self.equipment_id}', "
                f"type='{self.equipment_type.value}', "
                f"power={self.power_rating}kW, "
                f"scenario='{self.config.scenario}')")
    
    def __str__(self) -> str:
        """String representation of equipment."""
        return f"{self.name} ({self.equipment_id})"
    
    def __eq__(self, other) -> bool:
        """Check equipment equality."""
        if not isinstance(other, BaseEquipment):
            return False
        return (self.equipment_id == other.equipment_id and 
                self.config.equipment_type == other.config.equipment_type)
    
    def __hash__(self) -> int:
        """Hash equipment for use in sets and dictionaries."""
        return hash((self.equipment_id, self.config.equipment_type))


# Utility functions for equipment management
def validate_equipment_config(config: EquipmentConfig) -> List[str]:
    """Validate equipment configuration.
    
    Parameters
    ----------
    config : EquipmentConfig
        Equipment configuration to validate
        
    Returns
    -------
    List[str]
        List of validation errors
    """
    return config.validate()


def create_equipment_from_config(config_dict: Dict[str, Any]) -> Optional[BaseEquipment]:
    """Create equipment instance from configuration dictionary.
    
    Parameters
    ----------
    config_dict : Dict[str, Any]
        Equipment configuration dictionary
        
    Returns
    -------
    BaseEquipment, optional
        Equipment instance or None if creation fails
    """
    try:
        config = EquipmentConfig.from_dict(config_dict.get('config', config_dict))
        
        # Determine equipment class based on type and scenario
        # This would typically be handled by the EquipmentLibrary
        # For now, return None as this requires factory logic
        
        return None
    except Exception as e:
        warnings.warn(f"Failed to create equipment from config: {e}", UserWarning)
        return None


def validate_equipment_compatibility(equipment1: BaseEquipment, 
                                   equipment2: BaseEquipment) -> Dict[str, Any]:
    """Validate compatibility between two equipment instances.
    
    Parameters
    ----------
    equipment1 : BaseEquipment
        First equipment
    equipment2 : BaseEquipment
        Second equipment
        
    Returns
    -------
    Dict[str, Any]
        Compatibility assessment
    """
    compatibility = {
        'compatible': True,
        'warnings': [],
        'errors': []
    }
    
    # Check voltage level compatibility
    if (equipment1.config.voltage_level and equipment2.config.voltage_level and
        abs(equipment1.config.voltage_level - equipment2.config.voltage_level) > 0.1):
        compatibility['warnings'].append("Voltage level mismatch")
    
    # Check energy carrier compatibility
    carriers1 = set(carrier.value for carrier in equipment1.get_supported_carriers())
    carriers2 = set(carrier.value for carrier in equipment2.get_supported_carriers())
    
    if not carriers1.intersection(carriers2):
        compatibility['errors'].append("No compatible energy carriers")
        compatibility['compatible'] = False
    
    # Check scenario compatibility
    scenarios1 = set(equipment1.get_compatible_scenarios())
    scenarios2 = set(equipment2.get_compatible_scenarios())
    
    if not scenarios1.intersection(scenarios2):
        compatibility['warnings'].append("Scenario compatibility limited")
    
    return compatibility


# Define __all__ for module exports
__all__ = [
    # Core classes
    'BaseEquipment',
    'EquipmentConfig',
    
    # Enumerations
    'EquipmentCategory',
    'EquipmentType', 
    'EnergyCarrier',
    
    # Utility functions
    'validate_equipment_config',
    'create_equipment_from_config',
    'validate_equipment_compatibility'
]