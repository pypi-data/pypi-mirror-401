"""
Urban Equipment Library.

This module provides equipment configurations specifically designed for
urban scenarios, including high-density residential, commercial, and
municipal energy systems.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class UrbanEquipmentLibrary:
    """Urban equipment library with city-specific equipment configurations.
    
    This library contains equipment optimized for urban environments
    including high-rise buildings, district heating, EV charging, etc.
    """
    
    def __init__(self):
        """Initialize the urban equipment library."""
        self.equipment_configs = self._create_urban_equipment()
    
    @property
    def equipment(self):
        """Alias for equipment_configs for backward compatibility."""
        return self.equipment_configs
    
    def _create_urban_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create urban-specific equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # High-Efficiency Solar PV for Urban Rooftops
        configs['solar_pv_rooftop'] = EquipmentConfig(
            equipment_id='solar_pv_rooftop',
            name='Urban Rooftop Solar PV System',
            description='High-efficiency rooftop solar PV system for urban buildings',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PV,
            power_rating=10.0,  # kW
            efficiency=0.22,
            lifetime=25,
            investment_costs=1300.0,  # €/kW
            operation_costs=25.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'capacity_factor': 0.15,  # Lower in urban areas
                'building_integration': True,
                'roof_mounting': 'optimized_angle',
                'bypass_diodes': True
            }
        )
        
        # Urban Wind Turbine
        configs['wind_turbine_urban'] = EquipmentConfig(
            equipment_id='wind_turbine_urban',
            name='Urban Wind Turbine',
            description='Small vertical axis wind turbine for urban environments',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.WIND_TURBINE,
            power_rating=5.0,  # kW
            efficiency=0.35,
            lifetime=15,
            investment_costs=2000.0,  # €/kW
            operation_costs=40.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'vertical_axis': True,
                'low_noise': True,
                'turbulence_tolerance': 0.3,
                'minimum_wind_speed': 2.0  # m/s
            }
        )
        
        # District Heating Network
        configs['district_heating_plant'] = EquipmentConfig(
            equipment_id='district_heating_plant',
            name='Urban District Heating Plant',
            description='Combined heat and power plant for district heating',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.COMBINED_HEAT_POWER,
            power_rating=1000.0,  # kW thermal
            efficiency=0.85,  # Total efficiency
            lifetime=30,
            investment_costs=2000.0,  # €/kW thermal
            operation_costs=50.0,  # €/MWh thermal
            co2_emissions=200.0,  # kg CO2/MWh thermal
            supported_carriers=[EnergyCarrier.HEAT, EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'thermal_power': 1000.0,  # kW
                'electrical_power': 500.0,  # kW
                'heat_to_power_ratio': 2.0,
                'district_network_pressure': 16.0  # bar
            }
        )
        
        # EV Charging Station
        configs['ev_charging_station'] = EquipmentConfig(
            equipment_id='ev_charging_station',
            name='Urban EV Charging Station',
            description='Fast charging station for electric vehicles',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.EV_CHARGING,
            power_rating=150.0,  # kW
            efficiency=0.95,
            lifetime=15,
            investment_costs=150.0,  # €/kW
            operation_costs=20.0,  # €/kW/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'charging_power': 150.0,  # kW DC
                'connector_type': 'CCS',
                'max_vehicles': 4,
                'payment_system': True,
                'grid_impact_monitoring': True
            }
        )
        
        # Urban Battery Storage
        configs['battery_storage_grid'] = EquipmentConfig(
            equipment_id='battery_storage_grid',
            name='Grid-Scale Battery Storage',
            description='Large-scale battery storage for urban grid stabilization',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=1000.0,  # kW
            capacity=2000.0,  # kWh
            efficiency=0.90,
            lifetime=20,
            investment_costs=600.0,  # €/kWh
            operation_costs=15.0,  # €/kW/year
            co2_emissions=80.0,  # kg CO2/kWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'grid_services': ['frequency_control', 'voltage_support'],
                'response_time': 0.1,  # seconds
                'cycle_life': 10000,
                'thermal_management': 'liquid_cooling'
            }
        )
        
        # Smart Building Controller
        configs['smart_building_controller'] = EquipmentConfig(
            equipment_id='smart_building_controller',
            name='Smart Building Energy Controller',
            description='AI-powered energy management for urban buildings',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.LOAD_CONTROLLER,
            power_rating=0.5,  # kW
            lifetime=10,
            investment_costs=3000.0,  # €/building
            operation_costs=300.0,  # €/building/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT
            ],
            custom_parameters={
                'building_types': ['residential', 'commercial', 'office'],
                'smart_appliance_control': True,
                'occupancy_based_control': True,
                'demand_response': True,
                'ai_optimization': True
            }
        )
        
        # Urban Heat Pump
        configs['heat_pump_centralized'] = EquipmentConfig(
            equipment_id='heat_pump_centralized',
            name='Centralized Urban Heat Pump',
            description='Large-scale heat pump for urban district heating',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.HEAT_PUMP,
            power_rating=500.0,  # kW
            efficiency=4.0,  # COP
            lifetime=25,
            investment_costs=1500.0,  # €/kW
            operation_costs=80.0,  # €/kW/year
            co2_emissions=500.0,  # kg CO2/unit
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'heat_source': 'ambient_air',
                'heating_capacity': 500.0,  # kW
                'heating_cop': 4.0,
                'cooling_cop': 3.5,
                'district_integration': True
            }
        )
        
        # Urban Waste-to-Energy
        configs['waste_to_energy'] = EquipmentConfig(
            equipment_id='waste_to_energy',
            name='Urban Waste-to-Energy Plant',
            description='Municipal waste-to-energy conversion plant',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.BIOMASS_GENERATOR,
            power_rating=2000.0,  # kW
            efficiency=0.25,
            lifetime=25,
            investment_costs=4000.0,  # €/kW
            operation_costs=100.0,  # €/kW/year
            co2_emissions=-800.0,  # Negative emissions (waste avoided)
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'waste_treatment_capacity': 100.0,  # tonnes/day
                'thermal_output': 3000.0,  # kW thermal
                'emission_control': True,
                'ash_handling': True
            }
        )
        
        # Urban Hydrogen Storage
        configs['hydrogen_storage_urban'] = EquipmentConfig(
            equipment_id='hydrogen_storage_urban',
            name='Urban Hydrogen Storage Facility',
            description='Hydrogen storage facility for urban energy systems',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.HYDROGEN_STORAGE,
            power_rating=100.0,  # kW (electrolyzer)
            capacity=500.0,  # kg H2
            efficiency=0.70,
            lifetime=20,
            investment_costs=5000.0,  # €/kg H2 storage
            operation_costs=50.0,  # €/kg H2/year
            co2_emissions=10.0,  # kg CO2/kg H2
            supported_carriers=[EnergyCarrier.HYDROGEN],
            custom_parameters={
                'storage_pressure': 350.0,  # bar
                'storage_type': 'compressed_gas',
                'purity_requirement': 99.9,  # %
                'refueling_capacity': 10.0  # kg/day
            }
        )
        
        # Urban Microgrid Controller
        configs['microgrid_controller'] = EquipmentConfig(
            equipment_id='microgrid_controller',
            name='Urban Microgrid Controller',
            description='Advanced control system for urban microgrids',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=2.0,  # kW
            lifetime=15,
            investment_costs=15000.0,  # €/system
            operation_costs=1000.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT,
                EnergyCarrier.HYDROGEN
            ],
            custom_parameters={
                'islanding_capability': True,
                'grid_restoration': True,
                'black_start': True,
                'load_shedding': True,
                'renewable_forecasting': True
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID."""
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in urban library")
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
                        max_power: float = None) -> Dict[str, EquipmentConfig]:
        """Search equipment based on criteria."""
        results = {}
        
        for eq_id, eq_config in self.equipment_configs.items():
            # Check name pattern
            if name_pattern and name_pattern.lower() not in eq_config.name.lower():
                continue
            
            # Check category
            if category and eq_config.category != category:
                continue
            
            # Check power rating
            if max_power and eq_config.power_rating > max_power:
                continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library."""
        return {
            'library_type': 'urban',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }