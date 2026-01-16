"""Building Cluster Modeling for PyXESXXN Energy System Analysis.

This module provides comprehensive building cluster modeling capabilities for urban integrated energy systems (UIES),
including multi-type building load characteristics, building energy storage (BES), hydrogen-heat pump coupling, and 
cluster-level协同 optimization.
"""

import abc
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np

from .base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    ExtendedEquipmentCategory,
    register_component_factory,
    calculate_thermodynamic_state
)
from pyxesxxn.network import PyXESXXNNetwork


# =============================================================================
# Building Type Definitions
# =============================================================================

class BuildingType(Enum):
    """Building type enumeration."""
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"
    COMMERCIAL = "commercial"


class BuildingTemperatureParams:
    """Building temperature parameters for different building types."""
    RESIDENTIAL = {
        "min_temp": 20.0,  # °C
        "max_temp": 26.0,  # °C
        "set_temp_summer": 24.0,  # °C
        "set_temp_winter": 22.0,  # °C
        "max_temp_change": 1.0  # °C/hour
    }
    
    INDUSTRIAL = {
        "min_temp": 18.0,  # °C
        "max_temp": 22.0,  # °C
        "set_temp_summer": 20.0,  # °C
        "set_temp_winter": 20.0,  # °C
        "max_temp_change": 0.5  # °C/hour
    }
    
    COMMERCIAL = {
        "min_temp": 20.0,  # °C
        "max_temp": 25.0,  # °C
        "set_temp_summer": 23.0,  # °C
        "set_temp_winter": 22.0,  # °C
        "max_temp_change": 0.8  # °C/hour
    }


class BuildingIlluminanceParams:
    """Building illuminance parameters for different building types."""
    RESIDENTIAL = {
        "min_illuminance": 100,  # lx
        "max_illuminance": 500,  # lx
        "set_illuminance": 300   # lx
    }
    
    INDUSTRIAL = {
        "min_illuminance": 200,  # lx
        "max_illuminance": 750,  # lx
        "set_illuminance": 500   # lx
    }
    
    COMMERCIAL = {
        "min_illuminance": 300,  # lx
        "max_illuminance": 500,  # lx
        "set_illuminance": 400   # lx
    }


# =============================================================================
# Building Configuration Classes
# =============================================================================

@dataclass
class BuildingConfig(ExtendedEquipmentConfig):
    """Building configuration with specific parameters."""
    building_type: BuildingType = BuildingType.RESIDENTIAL
    floor_area: float = 1000.0  # m²
    window_area: float = 200.0  # m²
    wall_area: float = 400.0  # m²
    thermal_mass: float = 10000.0  # kJ/°C
    heat_transfer_coefficient: float = 2.0  # W/m²·°C
    roof_area: float = 1000.0  # m²
    occupancy: Dict[int, float] = field(default_factory=lambda: {
        0: 0.8, 1: 0.8, 2: 0.8, 3: 0.7, 4: 0.6, 5: 0.4,
        6: 0.3, 7: 0.2, 8: 0.1, 9: 0.1, 10: 0.2, 11: 0.3,
        12: 0.4, 13: 0.5, 14: 0.5, 15: 0.6, 16: 0.7, 17: 0.8,
        18: 0.9, 19: 0.9, 20: 0.9, 21: 0.8, 22: 0.8, 23: 0.8
    })
    # Initial indoor temperature
    initial_indoor_temp: float = 23.0  # °C
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        config_dict = super().to_dict()
        config_dict.update({
            'building_type': self.building_type.value,
            'floor_area': self.floor_area,
            'window_area': self.window_area,
            'wall_area': self.wall_area,
            'thermal_mass': self.thermal_mass,
            'heat_transfer_coefficient': self.heat_transfer_coefficient,
            'roof_area': self.roof_area,
            'occupancy': self.occupancy.copy(),
            'initial_indoor_temp': self.initial_indoor_temp
        })
        return config_dict
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'BuildingConfig':
        """Create configuration from dictionary."""
        # Extract building-specific parameters
        building_type = BuildingType(config_dict.pop('building_type'))
        floor_area = config_dict.pop('floor_area', 1000.0)
        window_area = config_dict.pop('window_area', 200.0)
        wall_area = config_dict.pop('wall_area', 400.0)
        thermal_mass = config_dict.pop('thermal_mass', 10000.0)
        heat_transfer_coefficient = config_dict.pop('heat_transfer_coefficient', 2.0)
        roof_area = config_dict.pop('roof_area', 1000.0)
        occupancy = config_dict.pop('occupancy', {
            0: 0.8, 1: 0.8, 2: 0.8, 3: 0.7, 4: 0.6, 5: 0.4,
            6: 0.3, 7: 0.2, 8: 0.1, 9: 0.1, 10: 0.2, 11: 0.3,
            12: 0.4, 13: 0.5, 14: 0.5, 15: 0.6, 16: 0.7, 17: 0.8,
            18: 0.9, 19: 0.9, 20: 0.9, 21: 0.8, 22: 0.8, 23: 0.8
        })
        initial_indoor_temp = config_dict.pop('initial_indoor_temp', 23.0)
        
        # Create extended configuration
        base_config = super().from_dict(config_dict)
        
        return cls(
            **base_config.__dict__,
            building_type=building_type,
            floor_area=floor_area,
            window_area=window_area,
            wall_area=wall_area,
            thermal_mass=thermal_mass,
            heat_transfer_coefficient=heat_transfer_coefficient,
            roof_area=roof_area,
            occupancy=occupancy,
            initial_indoor_temp=initial_indoor_temp
        )


@dataclass
class HydrogenHeatRecoveryConfig(ExtendedEquipmentConfig):
    """Hydrogen heat recovery configuration."""
    hydrogen_system_capacity: float = 100.0  # kW
    heat_recovery_efficiency: float = 0.85  # 85%
    heat_pump_cop: float = 3.5  # Coefficient of Performance
    max_heat_sharing: float = 0.3  # Maximum percentage of heat load that can be shared
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        config_dict = super().to_dict()
        config_dict.update({
            'hydrogen_system_capacity': self.hydrogen_system_capacity,
            'heat_recovery_efficiency': self.heat_recovery_efficiency,
            'heat_pump_cop': self.heat_pump_cop,
            'max_heat_sharing': self.max_heat_sharing
        })
        return config_dict
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'HydrogenHeatRecoveryConfig':
        """Create configuration from dictionary."""
        # Extract hydrogen heat recovery parameters
        hydrogen_system_capacity = config_dict.pop('hydrogen_system_capacity', 100.0)
        heat_recovery_efficiency = config_dict.pop('heat_recovery_efficiency', 0.85)
        heat_pump_cop = config_dict.pop('heat_pump_cop', 3.5)
        max_heat_sharing = config_dict.pop('max_heat_sharing', 0.3)
        
        # Create extended configuration
        base_config = super().from_dict(config_dict)
        
        return cls(
            **base_config.__dict__,
            hydrogen_system_capacity=hydrogen_system_capacity,
            heat_recovery_efficiency=heat_recovery_efficiency,
            heat_pump_cop=heat_pump_cop,
            max_heat_sharing=max_heat_sharing
        )


# =============================================================================
# Building Component Classes
# =============================================================================

class BaseBuilding(ExtendedEnergyComponent, abc.ABC):
    """Base class for all building types."""
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[BuildingConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize a building component."""
        # Call parent constructor - parent will handle default config creation
        super().__init__(equipment_id=equipment_id, config=config, location=location, **kwargs)
        
        # Initialize building-specific state
        self._indoor_temp = self.config.initial_indoor_temp
        self._prev_indoor_temp = self.config.initial_indoor_temp
        self._heat_storage_state = 0.0  # kWh
        self._current_illuminance = self._get_default_illuminance()
        self._occupancy = 0.0
        self._outdoor_temp = 20.0  # Default outdoor temperature
        self._solar_radiation = 0.0  # Default solar radiation (W/m²)
        
        # Get temperature and illuminance parameters based on building type
        self._temp_params = {
            BuildingType.RESIDENTIAL: BuildingTemperatureParams.RESIDENTIAL,
            BuildingType.INDUSTRIAL: BuildingTemperatureParams.INDUSTRIAL,
            BuildingType.COMMERCIAL: BuildingTemperatureParams.COMMERCIAL
        }[self.config.building_type]
        
        self._illum_params = {
            BuildingType.RESIDENTIAL: BuildingIlluminanceParams.RESIDENTIAL,
            BuildingType.INDUSTRIAL: BuildingIlluminanceParams.INDUSTRIAL,
            BuildingType.COMMERCIAL: BuildingIlluminanceParams.COMMERCIAL
        }[self.config.building_type]
    
    def _get_default_illuminance(self) -> float:
        """Get default illuminance based on building type."""
        return 300.0  # lx
    
    def _create_default_config(self, **kwargs) -> BuildingConfig:
        """Create default configuration for a building."""
        # Create base config from parent
        base_config = super()._create_default_config(**kwargs)
        
        # Convert to BuildingConfig with appropriate defaults
        return BuildingConfig(
            building_type=kwargs.get('building_type', BuildingType.RESIDENTIAL),
            floor_area=kwargs.get('floor_area', 1000.0),
            window_area=kwargs.get('window_area', 200.0),
            wall_area=kwargs.get('wall_area', 400.0),
            thermal_mass=kwargs.get('thermal_mass', 10000.0),
            heat_transfer_coefficient=kwargs.get('heat_transfer_coefficient', 2.0),
            roof_area=kwargs.get('roof_area', 1000.0),
            initial_indoor_temp=kwargs.get('initial_indoor_temp', 23.0),
            # Copy base config attributes
            equipment_id=base_config.equipment_id,
            name=base_config.name,
            description=base_config.description,
            category=base_config.category,
            equipment_type=base_config.equipment_type,
            power_rating=base_config.power_rating,
            scenario=base_config.scenario,
            location=base_config.location,
            supported_carriers=base_config.supported_carriers,
            custom_parameters=base_config.custom_parameters,
            **kwargs
        )
    
    def set_outdoor_conditions(self, outdoor_temp: float, solar_radiation: float) -> None:
        """Set outdoor conditions for the building."""
        self._outdoor_temp = outdoor_temp
        self._solar_radiation = solar_radiation
    
    def set_occupancy(self, hour: int) -> None:
        """Set occupancy based on hour of day."""
        self._occupancy = self.config.occupancy.get(hour, 0.5)
    
    def calculate_baseline_load(self, hour: int) -> Dict[str, float]:
        """Calculate baseline load for the building."""
        # This method should be overridden by subclasses
        return {
            'electricity': 10.0,
            'heat': 5.0,
            'light': 2.0
        }
    
    def calculate_solar_gain(self) -> float:
        """Calculate solar heat gain."""
        # Solar heat gain formula: Q_solar = A_win * I_solar * SC * tau_win
        # Assume shading coefficient (SC) = 0.7 and transmittance (tau_win) = 0.8
        sc = 0.7
        tau_win = 0.8
        return (self.config.window_area * self._solar_radiation * sc * tau_win) / 1000.0  # Convert to kW
    
    def calculate_internal_gain(self) -> float:
        """Calculate internal heat gain from occupancy and equipment."""
        # Assume 100 W per person and 5 W/m² equipment load
        people_gain = self._occupancy * self.config.floor_area * 0.1  # 100 W/m² converted to kW/m²
        equipment_gain = self.config.floor_area * 0.005  # 5 W/m² converted to kW/m²
        return people_gain + equipment_gain  # kW
    
    def calculate_heat_loss(self) -> float:
        """Calculate heat loss through envelope."""
        # Heat loss formula: Q_loss = U * A * (T_in - T_out)
        delta_temp = self._indoor_temp - self._outdoor_temp
        total_loss = (self.config.heat_transfer_coefficient * (self.config.wall_area + self.config.window_area) * delta_temp) / 1000.0  # Convert to kW
        return total_loss
    
    def calculate_thermal_performance(self, 
                                     heat_pump_power: float,
                                     heat_recovery: float,
                                     time_step: float = 1.0) -> Dict[str, float]:
        """Calculate thermal performance of the building."""
        # Calculate all heat gains and losses
        solar_gain = self.calculate_solar_gain()
        internal_gain = self.calculate_internal_gain()
        heat_loss = self.calculate_heat_loss()
        
        # Heat pump heating
        heat_pump_heating = heat_pump_power * self._temp_params.get('heat_pump_cop', 3.5)
        
        # Total heat balance
        total_heat = (solar_gain + internal_gain + heat_pump_heating + heat_recovery - heat_loss) * time_step  # kWh
        
        # Calculate temperature change
        temp_change = (total_heat * 3600) / self.config.thermal_mass  # Convert kWh to kJ, then to °C
        
        # Update indoor temperature
        self._prev_indoor_temp = self._indoor_temp
        self._indoor_temp += temp_change
        
        # Apply temperature constraints
        self._indoor_temp = max(self._temp_params['min_temp'], min(self._temp_params['max_temp'], self._indoor_temp))
        
        # Apply temperature change rate constraint
        max_temp_change = self._temp_params['max_temp_change']
        if abs(self._indoor_temp - self._prev_indoor_temp) > max_temp_change:
            if self._indoor_temp > self._prev_indoor_temp:
                self._indoor_temp = self._prev_indoor_temp + max_temp_change
            else:
                self._indoor_temp = self._prev_indoor_temp - max_temp_change
        
        return {
            'indoor_temperature': self._indoor_temp,
            'solar_gain': solar_gain,
            'internal_gain': internal_gain,
            'heat_loss': heat_loss,
            'heat_pump_heating': heat_pump_heating,
            'heat_recovery': heat_recovery,
            'total_heat_balance': total_heat,
            'temperature_change': temp_change
        }
    
    def calculate_illuminance(self, lighting_power: float) -> float:
        """Calculate illuminance based on lighting power and natural light."""
        # This is a simplified model - in reality, it's more complex
        natural_light = self._solar_radiation * 0.01  # Rough conversion from W/m² to lx
        artificial_light = lighting_power * 100  # Rough conversion from kW to lx
        
        total_illuminance = natural_light + artificial_light
        
        # Apply illuminance constraints
        self._current_illuminance = max(
            self._illum_params['min_illuminance'],
            min(self._illum_params['max_illuminance'], total_illuminance)
        )
        
        return self._current_illuminance
    
    def calculate_physical_performance(self, 
                                      input_power: Dict[str, float],
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate physical performance of the building."""
        # Extract input powers
        heat_pump_power = input_power.get('heat_pump', 0.0)
        lighting_power = input_power.get('lighting', 0.0)
        heat_recovery = input_power.get('heat_recovery', 0.0)
        
        # Calculate thermal performance
        thermal_perf = self.calculate_thermal_performance(
            heat_pump_power=heat_pump_power,
            heat_recovery=heat_recovery,
            time_step=time_step
        )
        
        # Calculate illuminance
        illuminance = self.calculate_illuminance(lighting_power=lighting_power)
        
        # Calculate baseline load
        baseline_load = self.calculate_baseline_load(0)  # Default hour 0
        
        return {
            **thermal_perf,
            'illuminance': illuminance,
            'lighting_power': lighting_power,
            'heat_pump_power': heat_pump_power,
            'heat_recovery': heat_recovery,
            'baseline_load': baseline_load,
            'occupancy': self._occupancy,
            'outdoor_temperature': self._outdoor_temp,
            'solar_radiation': self._solar_radiation
        }
    
    def create_components(self, network: PyXESXXNNetwork) -> Dict[str, Any]:
        """Create PyXESXXN components for this building."""
        components = {}
        
        # Create buses for electricity, heat, and hydrogen
        bus_id = f"bus_{self.equipment_id}_electricity"
        network.add_bus(bus_id, "electricity")
        components['electricity_bus'] = bus_id
        
        bus_id = f"bus_{self.equipment_id}_heat"
        network.add_bus(bus_id, "heat")
        components['heat_bus'] = bus_id
        
        bus_id = f"bus_{self.equipment_id}_hydrogen"
        network.add_bus(bus_id, "hydrogen")
        components['hydrogen_bus'] = bus_id
        
        return components


class ResidentialBuilding(BaseBuilding):
    """Residential building component."""
    
    def calculate_baseline_load(self, hour: int) -> Dict[str, float]:
        """Calculate baseline load for residential building."""
        # Simplified residential load profile
        base_electric_load = {
            0: 3.0, 1: 2.5, 2: 2.0, 3: 1.8, 4: 1.5, 5: 2.0,
            6: 4.0, 7: 5.0, 8: 3.0, 9: 2.5, 10: 2.0, 11: 2.2,
            12: 2.5, 13: 2.8, 14: 3.0, 15: 3.2, 16: 3.5, 17: 5.0,
            18: 6.0, 19: 7.0, 20: 6.5, 21: 5.5, 22: 4.5, 23: 3.5
        }.get(hour, 3.0)
        
        # Heat load depends on outdoor temperature difference
        heat_load = max(0.0, 0.5 * (self._temp_params['set_temp_winter'] - self._outdoor_temp))
        
        # Lighting load depends on hour and occupancy
        lighting_load = {
            0: 0.8, 1: 0.6, 2: 0.4, 3: 0.3, 4: 0.2, 5: 0.5,
            6: 1.0, 7: 1.2, 8: 0.5, 9: 0.3, 10: 0.2, 11: 0.2,
            12: 0.3, 13: 0.3, 14: 0.2, 15: 0.3, 16: 0.5, 17: 1.0,
            18: 1.5, 19: 1.8, 20: 1.6, 21: 1.2, 22: 0.8, 23: 0.6
        }.get(hour, 0.5)
        
        return {
            'electricity': base_electric_load,
            'heat': heat_load,
            'light': lighting_load
        }


class IndustrialBuilding(BaseBuilding):
    """Industrial building component."""
    
    def calculate_baseline_load(self, hour: int) -> Dict[str, float]:
        """Calculate baseline load for industrial building."""
        # Industrial load is relatively stable
        base_electric_load = 20.0  # kW
        
        # Industrial process heat load is high
        process_heat_load = 15.0  # kW
        space_heat_load = max(0.0, 0.3 * (self._temp_params['set_temp_winter'] - self._outdoor_temp))
        total_heat_load = process_heat_load + space_heat_load
        
        # Lighting load is relatively constant
        lighting_load = 3.0  # kW
        
        return {
            'electricity': base_electric_load,
            'heat': total_heat_load,
            'light': lighting_load
        }


class CommercialBuilding(BaseBuilding):
    """Commercial building component."""
    
    def calculate_baseline_load(self, hour: int) -> Dict[str, float]:
        """Calculate baseline load for commercial building."""
        # Commercial load profile - higher during business hours
        base_electric_load = {
            0: 5.0, 1: 4.5, 2: 4.0, 3: 3.5, 4: 3.0, 5: 4.0,
            6: 8.0, 7: 12.0, 8: 15.0, 9: 18.0, 10: 20.0, 11: 22.0,
            12: 23.0, 13: 22.0, 14: 21.0, 15: 20.0, 16: 19.0, 17: 22.0,
            18: 18.0, 19: 12.0, 20: 8.0, 21: 6.0, 22: 5.5, 23: 5.0
        }.get(hour, 10.0)
        
        # Heat load depends on outdoor temperature and business hours
        heat_load_multiplier = 1.0 if 8 <= hour <= 18 else 0.5
        heat_load = max(0.0, heat_load_multiplier * 0.4 * (self._temp_params['set_temp_winter'] - self._outdoor_temp))
        
        # Lighting load depends on business hours
        lighting_load = 10.0 if 8 <= hour <= 18 else 2.0
        
        return {
            'electricity': base_electric_load,
            'heat': heat_load,
            'light': lighting_load
        }


class BuildingCluster(ExtendedEnergyComponent):
    """Building cluster component that manages multiple buildings."""
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[ExtendedEquipmentConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize a building cluster component."""
        # Call parent constructor - parent will handle default config creation
        super().__init__(equipment_id=equipment_id, config=config, location=location, **kwargs)
        
        # Initialize cluster state
        self._buildings: Dict[str, BaseBuilding] = {}
        self._heat_sharing: Dict[Tuple[str, str], float] = {}
        self._electricity_sharing: Dict[Tuple[str, str], float] = {}
        self._max_power_sharing = 100.0  # kW
        self._total_carbon_emissions = 0.0  # kg CO2
    
    def _create_default_config(self, **kwargs) -> ExtendedEquipmentConfig:
        """Create default configuration for building cluster."""
        # Create base config from parent
        base_config = super()._create_default_config(**kwargs)
        
        # Return the base config - no additional building cluster specific parameters needed
        return base_config
    
    def add_building(self, building: BaseBuilding) -> None:
        """Add a building to the cluster."""
        self._buildings[building.equipment_id] = building
    
    def remove_building(self, building_id: str) -> None:
        """Remove a building from the cluster."""
        if building_id in self._buildings:
            del self._buildings[building_id]
    
    def set_outdoor_conditions(self, outdoor_temp: float, solar_radiation: float) -> None:
        """Set outdoor conditions for all buildings in the cluster."""
        for building in self._buildings.values():
            building.set_outdoor_conditions(outdoor_temp, solar_radiation)
    
    def set_occupancy(self, hour: int) -> None:
        """Set occupancy for all buildings in the cluster."""
        for building in self._buildings.values():
            building.set_occupancy(hour)
    
    def calculate_heat_sharing(self) -> Dict[Tuple[str, str], float]:
        """Calculate heat sharing between buildings."""
        heat_sharing = {}
        
        # Get industrial buildings (heat sources) and other buildings (heat sinks)
        industrial_buildings = [b for b in self._buildings.values() if isinstance(b, IndustrialBuilding)]
        other_buildings = [b for b in self._buildings.values() if not isinstance(b, IndustrialBuilding)]
        
        # Simple heat sharing model: industrial buildings share heat with others
        for source in industrial_buildings:
            # Assume industrial building has 20 kW of excess heat to share
            excess_heat = 20.0
            
            if excess_heat > 0:
                # Distribute excess heat to other buildings
                heat_per_building = excess_heat / max(1, len(other_buildings))
                
                for sink in other_buildings:
                    # Limit heat sharing to max 30% of sink's heat load
                    max_share = sink.calculate_baseline_load(0)['heat'] * 0.3
                    shared_heat = min(heat_per_building, max_share)
                    
                    heat_sharing[(source.equipment_id, sink.equipment_id)] = shared_heat
        
        self._heat_sharing = heat_sharing
        return heat_sharing
    
    def calculate_electricity_sharing(self) -> Dict[Tuple[str, str], float]:
        """Calculate electricity sharing between buildings."""
        electricity_sharing = {}
        
        # Simple electricity sharing model - this would be more complex in reality
        # For now, just return empty dict
        self._electricity_sharing = electricity_sharing
        return electricity_sharing
    
    def calculate_physical_performance(self, 
                                      input_power: Dict[str, float],
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate physical performance of the building cluster."""
        performance = {
            'buildings': {},
            'heat_sharing': self._heat_sharing,
            'electricity_sharing': self._electricity_sharing,
            'total_carbon_emissions': self._total_carbon_emissions
        }
        
        # Calculate performance for each building
        for building_id, building in self._buildings.items():
            building_perf = building.calculate_physical_performance(
                input_power.get(building_id, {}),
                time_step,
                operating_conditions
            )
            performance['buildings'][building_id] = building_perf
        
        return performance
    
    def calculate_carbon_emissions(self, electricity_consumption: Dict[str, float],
                                 heat_consumption: Dict[str, float]) -> float:
        """Calculate carbon emissions for the building cluster."""
        # Carbon emission factors (kg CO2/kWh)
        elec_emission_factor = 0.4  # kg CO2/kWh
        heat_emission_factor = 0.2  # kg CO2/kWh
        
        total_emissions = 0.0
        
        # Calculate electricity emissions
        for building_id, consumption in electricity_consumption.items():
            total_emissions += consumption * elec_emission_factor
        
        # Calculate heat emissions
        for building_id, consumption in heat_consumption.items():
            total_emissions += consumption * heat_emission_factor
        
        self._total_carbon_emissions = total_emissions
        return total_emissions
    
    def create_components(self, network: PyXESXXNNetwork) -> Dict[str, Any]:
        """Create PyXESXXN components for this building cluster."""
        components = {'buildings': {}}
        
        # Create cluster-level buses
        bus_id = f"bus_{self.equipment_id}_cluster_electricity"
        network.add_bus(bus_id, "electricity")
        components['cluster_electricity_bus'] = bus_id
        
        bus_id = f"bus_{self.equipment_id}_cluster_heat"
        network.add_bus(bus_id, "heat")
        components['cluster_heat_bus'] = bus_id
        
        bus_id = f"bus_{self.equipment_id}_cluster_hydrogen"
        network.add_bus(bus_id, "hydrogen")
        components['cluster_hydrogen_bus'] = bus_id
        
        # Create components for each building
        for building_id, building in self._buildings.items():
            building_components = building.create_components(network)
            components['buildings'][building_id] = building_components
            
            # Connect building buses to cluster buses
            network.add_line(
                f"line_{building_id}_to_cluster_elec",
                building_components['electricity_bus'],
                components['cluster_electricity_bus'],
                "electricity",  # Carrier type
                100.0  # Capacity in kW
            )
            
            network.add_line(
                f"line_{building_id}_to_cluster_heat",
                building_components['heat_bus'],
                components['cluster_heat_bus'],
                "heat",  # Carrier type
                100.0  # Capacity in kW
            )
        
        return components


class HydrogenHeatRecoverySystem(ExtendedEnergyComponent):
    """Hydrogen heat recovery system component."""
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[HydrogenHeatRecoveryConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize a hydrogen heat recovery system."""
        # Call parent constructor - parent will handle default config creation
        super().__init__(equipment_id=equipment_id, config=config, location=location, **kwargs)
        
        # Initialize system state
        self._hydrogen_consumption = 0.0  # kg
        self._heat_recovered = 0.0  # kWh
        self._heat_pump_power = 0.0  # kW
        self._heat_output = 0.0  # kW
    
    def _create_default_config(self, **kwargs) -> HydrogenHeatRecoveryConfig:
        """Create default configuration for hydrogen heat recovery system."""
        # Create base config from parent
        base_config = super()._create_default_config(**kwargs)
        
        # Convert to HydrogenHeatRecoveryConfig with appropriate defaults
        return HydrogenHeatRecoveryConfig(
            hydrogen_system_capacity=kwargs.get('hydrogen_system_capacity', 100.0),
            heat_recovery_efficiency=kwargs.get('heat_recovery_efficiency', 0.85),
            heat_pump_cop=kwargs.get('heat_pump_cop', 3.5),
            max_heat_sharing=kwargs.get('max_heat_sharing', 0.3),
            # Copy base config attributes
            equipment_id=base_config.equipment_id,
            name=base_config.name,
            description=base_config.description,
            category=base_config.category,
            equipment_type=base_config.equipment_type,
            power_rating=base_config.power_rating,
            scenario=base_config.scenario,
            location=base_config.location,
            supported_carriers=base_config.supported_carriers,
            custom_parameters=base_config.custom_parameters,
            **kwargs
        )
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate physical performance of the hydrogen heat recovery system."""
        # Hydrogen consumption (kg)
        # Assume 33 kWh/kg H2 LHV
        hydrogen_consumption = input_power / 33.0  # kg
        
        # Heat recovered from hydrogen system
        heat_recovered = input_power * self.config.heat_recovery_efficiency  # kWh
        
        # Heat pump power and heat output
        heat_pump_power = input_power * 0.5  # Assume 50% of input power is used for heat pump
        heat_pump_heating = heat_pump_power * self.config.heat_pump_cop  # kWh
        
        # Total heat output
        total_heat_output = heat_recovered + heat_pump_heating  # kWh
        
        # Update system state
        self._hydrogen_consumption = hydrogen_consumption
        self._heat_recovered = heat_recovered
        self._heat_pump_power = heat_pump_power
        self._heat_output = total_heat_output
        
        return {
            'hydrogen_consumption': hydrogen_consumption,
            'heat_recovered': heat_recovered,
            'heat_pump_power': heat_pump_power,
            'heat_pump_heating': heat_pump_heating,
            'total_heat_output': total_heat_output
        }
    
    def create_components(self, network: PyXESXXNNetwork) -> Dict[str, Any]:
        """Create PyXESXXN components for this hydrogen heat recovery system."""
        components = {}
        
        # Create buses for electricity, heat, and hydrogen
        bus_id = f"bus_{self.equipment_id}_electricity"
        network.add_bus(bus_id, "electricity")
        components['electricity_bus'] = bus_id
        
        bus_id = f"bus_{self.equipment_id}_heat"
        network.add_bus(bus_id, "heat")
        components['heat_bus'] = bus_id
        
        bus_id = f"bus_{self.equipment_id}_hydrogen"
        network.add_bus(bus_id, "hydrogen")
        components['hydrogen_bus'] = bus_id
        
        return components


# =============================================================================
# Register Component Factories
# =============================================================================

# Add new equipment types to ExtendedEquipmentType enum
# Note: We'll use the existing mechanism without modifying the original enum

def _register_building_cluster_components():
    """Register building cluster components."""
    # Register residential building
    register_component_factory(ExtendedEquipmentType.COMMERCIAL_BUILDING_LOAD, CommercialBuilding)
    
    # Register industrial building
    register_component_factory(ExtendedEquipmentType.INDUSTRIAL_ADJUSTABLE_LOAD, IndustrialBuilding)
    
    # Register commercial building
    register_component_factory(ExtendedEquipmentType.RESIDENTIAL_DEMAND_RESPONSE_LOAD, ResidentialBuilding)


# Register components when module is imported
_register_building_cluster_components()


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Building type definitions
    'BuildingType',
    'BuildingTemperatureParams',
    'BuildingIlluminanceParams',
    
    # Configuration classes
    'BuildingConfig',
    'HydrogenHeatRecoveryConfig',
    
    # Building components
    'BaseBuilding',
    'ResidentialBuilding',
    'IndustrialBuilding',
    'CommercialBuilding',
    'BuildingCluster',
    'HydrogenHeatRecoverySystem'
]
