"""
Port Equipment Library.

This module provides equipment configurations specifically designed for
port scenarios, including maritime operations, cargo handling,
and port energy systems.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class PortEquipmentLibrary:
    """Port equipment library with maritime and port-specific equipment configurations.
    
    This library contains equipment optimized for port environments
    including container handling, ship power supply, and maritime energy systems.
    """
    
    def __init__(self):
        """Initialize the port equipment library."""
        self.equipment_configs = self._create_port_equipment()
    
    @property
    def equipment(self) -> Dict[str, EquipmentConfig]:
        """Alias for equipment_configs to maintain backward compatibility.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        return self.equipment_configs
    
    def _create_port_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create port-specific equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # Port Container Crane Electric
        configs['container_crane_electric'] = EquipmentConfig(
            equipment_id='container_crane_electric',
            name='Electric Container Crane',
            description='Electric powered container handling crane',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.CONTAINER_CRANE,
            power_rating=800.0,  # kW
            efficiency=0.75,
            lifetime=25,
            investment_costs=4000.0,  # €/kW
            operation_costs=200.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'lifting_capacity': 65.0,  # tonnes
                'span': 65.0,  # m
                'lift_height': 45.0,  # m
                'travel_speed': 180.0,  # m/min
                'trolley_speed': 120.0,  # m/min
                'emission_reduction': True,
                'regenerative_braking': True
            }
        )
        
        # Ship Shore Power Connection
        configs['shore_power_system'] = EquipmentConfig(
            equipment_id='shore_power_system',
            name='Ship Shore Power System',
            description='High-voltage shore power connection for ships',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.SHORE_POWER,
            power_rating=15000.0,  # kW
            efficiency=0.95,
            lifetime=30,
            investment_costs=800.0,  # €/kW
            operation_costs=25.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'voltage_levels': [6600.0, 11000.0],  # V AC
                'frequency': 60.0,  # Hz
                'connection_standard': 'IEC_80005_3',
                'cable_management': 'automated',
                'vessel_compatibility': ['container', 'bulk', 'tanker'],
                'load_monitoring': True,
                'weather_protection': 'IP65'
            }
        )
        
        # Port Hydrogen Refueling Station
        configs['port_hydrogen_station'] = EquipmentConfig(
            equipment_id='port_hydrogen_station',
            name='Port Hydrogen Refueling Station',
            description='Hydrogen refueling station for maritime vessels',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.HYDROGEN_STORAGE,
            power_rating=500.0,  # kW
            capacity=2000.0,  # kg H2
            efficiency=0.80,
            lifetime=20,
            investment_costs=8000.0,  # €/kg H2
            operation_costs=100.0,  # €/kg H2/year
            co2_emissions=5.0,  # kg CO2/kg H2
            supported_carriers=[EnergyCarrier.HYDROGEN],
            custom_parameters={
                'refueling_pressure': 350.0,  # bar
                'storage_capacity': 2000.0,  # kg H2
                'refueling_rate': 50.0,  # kg/min
                'purity_level': 99.9,  # %
                'maritime_vessels': True,
                'safety_systems': 'class_I_DIV_2',
                'cryogenic_storage': True
            }
        )
        
        # Port Solar Farm
        configs['port_solar_farm'] = EquipmentConfig(
            equipment_id='port_solar_farm',
            name='Port Solar Farm',
            description='Large-scale solar PV installation in port areas',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PV,
            power_rating=10000.0,  # kW
            efficiency=0.20,
            lifetime=25,
            investment_costs=900.0,  # €/kW
            operation_costs=25.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'tracking_system': 'single_axis',
                'salt_resistance': True,
                'wind_load_rating': 250.0,  # km/h
                'ground_mounted': True,
                'port_area_optimized': True,
                'maritime_environment': True
            }
        )
        
        # Electric Rubber Tyre Gantry Crane
        configs['rtg_crane_electric'] = EquipmentConfig(
            equipment_id='rtg_crane_electric',
            name='Electric Rubber Tyre Gantry Crane',
            description='Electric RTG crane for container stacking',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.RTG_CRANE,
            power_rating=400.0,  # kW
            efficiency=0.80,
            lifetime=20,
            investment_costs=2500.0,  # €/kW
            operation_costs=150.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'lifting_capacity': 40.0,  # tonnes
                'span': 23.0,  # m
                'stack_height': 1.0,  # containers high
                'container_type': '20ft_40ft',
                'positioning_accuracy': 0.1,  # m
                'battery_option': True,
                'fuel_cell_option': True
            }
        )
        
        # Port Battery Storage System
        configs['port_battery_storage'] = EquipmentConfig(
            equipment_id='port_battery_storage',
            name='Port Grid-Scale Battery Storage',
            description='Large battery storage for port energy management',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=20000.0,  # kW
            capacity=40000.0,  # kWh
            efficiency=0.88,
            lifetime=20,
            investment_costs=500.0,  # €/kWh
            operation_costs=20.0,  # €/kW/year
            co2_emissions=70.0,  # kg CO2/kWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'technology': 'lithium_ion',
                'grid_services': ['frequency_regulation', 'peak_shaving'],
                'response_time': 0.1,  # seconds
                'thermal_management': 'liquid_cooling',
                'fire_suppression': 'advanced',
                'maritime_environment': True
            }
        )
        
        # Port Fuel Cell Generator
        configs['port_fuel_cell'] = EquipmentConfig(
            equipment_id='port_fuel_cell',
            name='Port Fuel Cell Generator',
            description='Hydrogen fuel cell generator for port power',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.FUEL_CELL,
            power_rating=1000.0,  # kW
            efficiency=0.55,
            lifetime=15,
            investment_costs=3500.0,  # €/kW
            operation_costs=100.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'fuel_type': 'hydrogen',
                'electrical_efficiency': 0.55,
                'thermal_efficiency': 0.30,
                'stack_lifetime': 60000,  # hours
                'startup_time': 10.0,  # minutes
                'low_noise': True,
                'emission_free': True
            }
        )
        
        # Electric Forklift Fleet
        configs['electric_forklift'] = EquipmentConfig(
            equipment_id='electric_forklift',
            name='Electric Port Forklift',
            description='Electric forklift for port cargo handling',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.BATTERY_VEHICLE,
            power_rating=15.0,  # kW
            efficiency=0.85,
            lifetime=10,
            investment_costs=2000.0,  # €/kW
            operation_costs=100.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'lifting_capacity': 7.0,  # tonnes
                'battery_capacity': 80.0,  # kWh
                'operating_hours': 8.0,  # hours
                'charging_time': 4.0,  # hours
                'fast_charging': True,
                'regenerative_braking': True,
                'maritime_duty': True
            }
        )
        
        # Port Energy Management System
        configs['port_energy_management'] = EquipmentConfig(
            equipment_id='port_energy_management',
            name='Port Energy Management System',
            description='Advanced EMS for port operations',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=10.0,  # kW
            lifetime=12,
            investment_costs=40000.0,  # €/system
            operation_costs=4000.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HYDROGEN
            ],
            custom_parameters={
                'port_scale': 'large',
                'equipment_monitoring': 100,
                'energy_optimization': True,
                'emission_monitoring': True,
                'cost_optimization': True,
                'grid_integration': True,
                'renewable_energy_integration': True
            }
        )
        
        # Automated Guided Vehicle
        configs['agv_port'] = EquipmentConfig(
            equipment_id='agv_port',
            name='Port Automated Guided Vehicle',
            description='Electric AGV for container transportation',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.BATTERY_VEHICLE,
            power_rating=25.0,  # kW
            efficiency=0.80,
            lifetime=12,
            investment_costs=1500.0,  # €/kW
            operation_costs=200.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'load_capacity': 40.0,  # tonnes
                'battery_capacity': 150.0,  # kWh
                'operating_range': 50.0,  # km
                'navigation': 'autonomous',
                'safety_systems': 'full',
                'communication': '5g_v2x',
                'weather_resistance': 'ip65'
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID."""
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in port library")
        return self.equipment_configs[equipment_id]
    
    def list_equipment(self) -> List[str]:
        """List all equipment IDs in the library."""
        return list(self.equipment_configs.keys())
    
    def get_equipment_by_category(self, category: EquipmentCategory) -> Dict[str, EquipmentConfig]:
        """Get all equipment configurations by category."""
        return {
            eq_id: eq_config for eq_id, eq_config in self.equipment_configs.items()
            if eq_config.category == category
        }
    
    def search_equipment(self, 
                        name_pattern: str = None,
                        category: EquipmentCategory = None,
                        maritime_focus: bool = None) -> Dict[str, EquipmentConfig]:
        """Search equipment based on criteria."""
        results = {}
        
        for eq_id, eq_config in self.equipment_configs.items():
            # Check name pattern
            if name_pattern and name_pattern.lower() not in eq_config.name.lower():
                continue
            
            # Check category
            if category and eq_config.category != category:
                continue
            
            # Check maritime focus
            if maritime_focus:
                params = eq_config.custom_parameters
                if not (params.get('maritime_environment') or
                       params.get('maritime_vessels') or
                       'port' in eq_config.name.lower() or
                       'shore_power' in eq_id):
                    continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library."""
        return {
            'library_type': 'port',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }