"""
Island Equipment Library.

This module provides equipment configurations specifically designed for
island scenarios, including remote islands, microgrids, desalination,
and island-specific energy systems.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class IslandEquipmentLibrary:
    """Island equipment library with island-specific equipment configurations.
    
    This library contains equipment optimized for island environments
    including desalination systems, microgrids, renewable energy integration,
    and remote island operations.
    """
    
    def __init__(self):
        """Initialize the island equipment library."""
        self.equipment_configs = self._create_island_equipment()
    
    @property
    def equipment(self):
        """Alias for equipment_configs for backward compatibility."""
        return self.equipment_configs
    
    def _create_island_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create island-specific equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # Island Solar PV Farm
        configs['island_solar_farm'] = EquipmentConfig(
            equipment_id='island_solar_farm',
            name='Island Solar PV Farm',
            description='Salt-resistant solar PV system for island environments',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PV,
            power_rating=5000.0,  # kW
            efficiency=0.19,
            lifetime=25,
            investment_costs=1000.0,  # €/kW
            operation_costs=30.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'salt_resistance': True,
                'corrosion_protection': 'marine_grade',
                'hurricane_rating': 250.0,  # km/h
                'tracking_system': 'fixed_tilt_optimized',
                'maintenance_access': 'elevated_platforms',
                'anti_reflective_coating': True
            }
        )
        
        # Island Wind Turbine
        configs['island_wind_turbine'] = EquipmentConfig(
            equipment_id='island_wind_turbine',
            name='Island Wind Turbine',
            description='Marine environment wind turbine for islands',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.WIND_TURBINE,
            power_rating=3000.0,  # kW
            efficiency=0.42,
            lifetime=20,
            investment_costs=1800.0,  # €/kW
            operation_costs=45.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'hub_height': 80.0,  # m
                'rotor_diameter': 90.0,  # m
                'marine_coating': True,
                'lightning_protection': 'advanced',
                'hurricane_storm_protection': True,
                'corrosion_resistance': 'seawater',
                'wildlife_compliance': True
            }
        )
        
        # Reverse Osmosis Desalination Plant
        configs['ro_desalination'] = EquipmentConfig(
            equipment_id='ro_desalination',
            name='Island Reverse Osmosis Desalination',
            description='Energy-efficient RO desalination for islands',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.DESALINATION_PLANT,
            power_rating=2000.0,  # kW
            efficiency=0.60,
            lifetime=20,
            investment_costs=2000.0,  # €/m³/day capacity
            operation_costs=1.2,  # €/m³
            co2_emissions=3.5,  # kg CO2/m³
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'water_production': 2000.0,  # m³/day
                'recovery_rate': 0.45,
                'energy_recovery': 'peltier_based',
                'intake_protection': 'screening_system',
                'brine_management': 'deep_water_discharge',
                'remote_monitoring': True
            }
        )
        
        # Island Microgrid Controller
        configs['island_microgrid'] = EquipmentConfig(
            equipment_id='island_microgrid',
            name='Island Microgrid Controller',
            description='Energy management system for island microgrids',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=5.0,  # kW
            lifetime=15,
            investment_costs=30000.0,  # €/system
            operation_costs=2500.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT,
                EnergyCarrier.HYDROGEN
            ],
            custom_parameters={
                'island_scale': 'small_medium',
                'renewable_penetration': 0.80,
                'grid_isolation': True,
                'diesel_fallback': True,
                'desalination_integration': True,
                'weather_forecasting': True,
                'emergency_power': True
            }
        )
        
        # Island Battery Storage
        configs['island_battery_storage'] = EquipmentConfig(
            equipment_id='island_battery_storage',
            name='Island Battery Storage System',
            description='Marine-grade battery storage for island systems',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=2000.0,  # kW
            capacity=4000.0,  # kWh
            efficiency=0.90,
            lifetime=20,
            investment_costs=1000.0,  # €/kWh
            operation_costs=30.0,  # €/kW/year
            co2_emissions=80.0,  # kg CO2/kWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'technology': 'lithium_iron_phosphate',
                'marine_environment': True,
                'temperature_control': 'advanced_cooling',
                'humidity_protection': 'sealed',
                'hurricane_resistance': True,
                'remote_monitoring': True,
                'maintenance_interval': 17520  # hours
            }
        )
        
        # Solar Powered Desalination
        configs['solar_desalination'] = EquipmentConfig(
            equipment_id='solar_desalination',
            name='Solar Powered Desalination',
            description='Solar-powered desalination system for islands',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.SOLAR_DESALINATION,
            power_rating=500.0,  # kW
            efficiency=0.45,
            lifetime=15,
            investment_costs=3000.0,  # €/m³/day capacity
            operation_costs=0.8,  # €/m³
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.SOLAR, EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'water_production': 500.0,  # m³/day
                'solar_tracking': 'dual_axis',
                'energy_storage': 'battery_included',
                'brine_concentration': 'solar_evaporation',
                'modular_design': True,
                'low_maintenance': True
            }
        )
        
        # Island Diesel Generator (Emergency Backup)
        configs['diesel_generator_island'] = EquipmentConfig(
            equipment_id='diesel_generator_island',
            name='Island Emergency Diesel Generator',
            description='Reliable diesel generator for island emergency power',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.DIESEL_GENERATOR,
            power_rating=1500.0,  # kW
            efficiency=0.40,
            lifetime=25,
            investment_costs=800.0,  # €/kW
            operation_costs=60.0,  # €/kW/year
            co2_emissions=650.0,  # kg CO2/MWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'fuel_consumption': 300.0,  # L/hour at full load
                'fuel_storage': 10000.0,  # L
                'automatic_start': True,
                'weatherproof': 'IP65',
                'fuel_filtering': 'advanced',
                'emission_control': 'tier_3',
                'noise_level': 75.0  # dB(A)
            }
        )
        
        # Island Hydrogen System
        configs['island_hydrogen'] = EquipmentConfig(
            equipment_id='island_hydrogen',
            name='Island Hydrogen Production and Storage',
            description='Hydrogen system for island energy storage and mobility',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.ELECTROLYZER,
            power_rating=300.0,  # kW
            efficiency=0.75,
            lifetime=20,
            investment_costs=4000.0,  # €/kW
            operation_costs=120.0,  # €/kW/year
            co2_emissions=2.0,  # kg CO2/kg H2
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HYDROGEN],
            custom_parameters={
                'hydrogen_production': 60.0,  # kg/day
                'storage_capacity': 300.0,  # kg H2
                'pressure': 350.0,  # bar
                'purity': 99.95,  # %
                'fuel_cell_integration': True,
                'hydrogen_vehicles': True,
                'solar_integration': True
            }
        )
        
        # Wave Energy Converter
        configs['wave_energy_converter'] = EquipmentConfig(
            equipment_id='wave_energy_converter',
            name='Island Wave Energy Converter',
            description='Wave energy converter for island power generation',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.WAVE_ENERGY_CONVERTER,
            power_rating=500.0,  # kW
            efficiency=0.35,
            lifetime=15,
            investment_costs=5000.0,  # €/kW
            operation_costs=150.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'wave_height_range': [1.0, 5.0],  # m
                'operational_wave_period': [8.0, 15.0],  # seconds
                'mooring_system': 'anchored',
                'marine_growth_protection': True,
                'emergency_shutdown': True,
                'environmental_monitoring': True
            }
        )
        
        # Island Electric Vehicle Charging
        configs['island_ev_charging'] = EquipmentConfig(
            equipment_id='island_ev_charging',
            name='Island EV Charging Infrastructure',
            description='Solar-powered EV charging stations for islands',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.EV_CHARGING,
            power_rating=50.0,  # kW
            efficiency=0.95,
            lifetime=15,
            investment_costs=2000.0,  # €/kW
            operation_costs=100.0,  # €/kW/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'charging_levels': ['AC_level_2', 'DC_fast'],
                'solar_integration': True,
                'battery_storage': 100.0,  # kWh
                'vehicle_types': ['private', 'taxi', 'delivery'],
                'payment_system': 'contactless',
                'weather_resistance': 'coastal'
            }
        )
        
        # Island Waste-to-Energy
        configs['island_waste_energy'] = EquipmentConfig(
            equipment_id='island_waste_energy',
            name='Island Waste-to-Energy Plant',
            description='Waste-to-energy system for island waste management',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.BIOMASS_GENERATOR,
            power_rating=800.0,  # kW
            efficiency=0.25,
            lifetime=20,
            investment_costs=6000.0,  # €/kW
            operation_costs=120.0,  # €/kW/year
            co2_emissions=-500.0,  # Negative emissions (waste diversion)
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'waste_processing': 50.0,  # tonnes/day
                'thermal_output': 1200.0,  # kW thermal
                'emission_control': 'advanced',
                'ash_handling': 'integrated',
                'island_specific': True,
                'modular_design': True
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID."""
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in island library")
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
                        marine_environment: bool = None,
                        renewable_focus: bool = None) -> Dict[str, EquipmentConfig]:
        """Search equipment based on criteria."""
        results = {}
        
        for eq_id, eq_config in self.equipment_configs.items():
            # Check name pattern
            if name_pattern and name_pattern.lower() not in eq_config.name.lower():
                continue
            
            # Check category
            if category and eq_config.category != category:
                continue
            
            # Check marine environment adaptation
            if marine_environment:
                params = eq_config.custom_parameters
                if not (params.get('marine_environment') or
                       params.get('salt_resistance') or
                       params.get('hurricane_rating') or
                       params.get('corrosion_protection') or
                       'island' in eq_config.name.lower()):
                    continue
            
            # Check renewable energy focus
            if renewable_focus:
                if not (eq_config.category == EquipmentCategory.GENERATION and
                       eq_config.co2_emissions == 0.0 and
                       eq_config.equipment_type in [EquipmentType.SOLAR_PV, 
                                                   EquipmentType.WIND_TURBINE,
                                                   EquipmentType.WAVE_ENERGY_CONVERTER]):
                    continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library."""
        return {
            'library_type': 'island',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }