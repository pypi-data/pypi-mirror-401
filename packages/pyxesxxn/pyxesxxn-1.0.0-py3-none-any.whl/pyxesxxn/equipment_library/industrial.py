"""
Industrial Equipment Library.

This module provides equipment configurations specifically designed for
industrial scenarios, including manufacturing, heavy industry, and
large-scale energy consumers.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class IndustrialEquipmentLibrary:
    """Industrial equipment library with industry-specific equipment configurations.
    
    This library contains equipment optimized for industrial environments
    including manufacturing processes, heavy machinery, process heating, etc.
    """
    
    def __init__(self):
        """Initialize the industrial equipment library."""
        self.equipment_configs = self._create_industrial_equipment()
    
    @property
    def equipment(self):
        """Alias for equipment_configs for backward compatibility."""
        return self.equipment_configs
    
    def _create_industrial_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create industrial-specific equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # Industrial Gas Turbine Generator
        configs['gas_turbine_industrial'] = EquipmentConfig(
            equipment_id='gas_turbine_industrial',
            name='Industrial Gas Turbine Generator',
            description='Large gas turbine for industrial power generation',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.GAS_TURBINE,
            power_rating=50000.0,  # kW
            efficiency=0.35,
            lifetime=25,
            investment_costs=1200.0,  # €/kW
            operation_costs=20.0,  # €/kW/year
            co2_emissions=400.0,  # kg CO2/MWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'fuel_type': 'natural_gas',
                'exhaust_heat_recovery': True,
                'startup_time': 30.0,  # minutes
                'load_following': True
            }
        )
        
        # Industrial Steam Boiler
        configs['steam_boiler_industrial'] = EquipmentConfig(
            equipment_id='steam_boiler_industrial',
            name='Industrial Steam Boiler',
            description='High-pressure steam boiler for industrial processes',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.BOILER,
            power_rating=50000.0,  # kW thermal
            efficiency=0.85,
            lifetime=30,
            investment_costs=800.0,  # €/kW thermal
            operation_costs=15.0,  # €/MWh thermal
            co2_emissions=120.0,  # kg CO2/MWh thermal
            supported_carriers=[EnergyCarrier.HEAT],
            custom_parameters={
                'steam_pressure': 40.0,  # bar
                'steam_temperature': 450.0,  # °C
                'water_pressure': 50.0,  # bar
                'fuel_efficiency': 0.85
            }
        )
        
        # Industrial Electrolyzer
        configs['electrolyzer_industrial'] = EquipmentConfig(
            equipment_id='electrolyzer_industrial',
            name='Industrial PEM Electrolyzer',
            description='Large-scale PEM electrolyzer for hydrogen production',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.ELECTROLYZER,
            power_rating=10000.0,  # kW
            efficiency=0.75,  # H2 production efficiency
            lifetime=20,
            investment_costs=1500.0,  # €/kW
            operation_costs=50.0,  # €/kW/year
            co2_emissions=2.0,  # kg CO2/kg H2
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HYDROGEN],
            custom_parameters={
                'hydrogen_production_rate': 200.0,  # kg/hour
                'operating_pressure': 30.0,  # bar
                'operating_temperature': 80.0,  # °C
                'water_consumption': 9.0,  # L/kg H2
                'cell_stack_lifetime': 80000,  # hours
                'hydrogen_purity': 99.9  # %
            }
        )
        
        # Industrial Process Heat Recovery
        configs['heat_recovery_system'] = EquipmentConfig(
            equipment_id='heat_recovery_system',
            name='Industrial Heat Recovery System',
            description='Waste heat recovery system for industrial processes',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.HEAT_EXCHANGER,
            power_rating=5000.0,  # kW thermal
            efficiency=0.70,
            lifetime=20,
            investment_costs=400.0,  # €/kW thermal
            operation_costs=25.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.HEAT],
            custom_parameters={
                'temperature_in': 300.0,  # °C
                'temperature_out': 150.0,  # °C
                'heat_medium': 'thermal_oil',
                'integration_points': 5,
                'maintenance_interval': 8760  # hours
            }
        )
        
        # Industrial Compressed Air System
        configs['compressed_air_system'] = EquipmentConfig(
            equipment_id='compressed_air_system',
            name='Industrial Compressed Air System',
            description='High-pressure compressed air system for industrial use',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.COMPRESSOR,
            power_rating=2000.0,  # kW
            efficiency=0.80,
            lifetime=25,
            investment_costs=600.0,  # €/kW
            operation_costs=40.0,  # €/kW/year
            supported_carriers=[EnergyCarrier.PRESSURE_AIR],
            custom_parameters={
                'air_pressure': 8.0,  # bar
                'air_flow_rate': 200.0,  # m³/min
                'air_quality': 'ISO_8573_1_Class_1',
                'variable_speed_drive': True,
                'heat_recovery': True
            }
        )
        
        # Industrial Fuel Cell
        configs['fuel_cell_industrial'] = EquipmentConfig(
            equipment_id='fuel_cell_industrial',
            name='Industrial SOFC Fuel Cell',
            description='Solid oxide fuel cell for combined heat and power',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.FUEL_CELL,
            power_rating=1500.0,  # kW
            efficiency=0.60,
            lifetime=10,
            investment_costs=3000.0,  # €/kW
            operation_costs=80.0,  # €/kW/year
            co2_emissions=350.0,  # kg CO2/MWh (with natural gas)
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'fuel_type': 'natural_gas',
                'electrical_efficiency': 0.60,
                'thermal_efficiency': 0.25,
                'stack_lifetime': 40000,  # hours
                'startup_time': 60.0  # minutes
            }
        )
        
        # Industrial Process Controller
        configs['process_controller'] = EquipmentConfig(
            equipment_id='process_controller',
            name='Industrial Process Energy Controller',
            description='Advanced energy management for industrial processes',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.LOAD_CONTROLLER,
            power_rating=5.0,  # kW
            lifetime=15,
            investment_costs=25000.0,  # €/system
            operation_costs=2000.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT,
                EnergyCarrier.PRESSURE_AIR
            ],
            custom_parameters={
                'process_types': ['manufacturing', 'chemical', 'metal'],
                'optimization_algorithms': ['linear_programming', 'genetic_algorithm'],
                'real_time_monitoring': True,
                'predictive_maintenance': True,
                'iso_50001_compliance': True
            }
        )
        
        # Industrial Thermal Storage
        configs['thermal_storage_industrial'] = EquipmentConfig(
            equipment_id='thermal_storage_industrial',
            name='Industrial Thermal Energy Storage',
            description='Large-scale thermal energy storage for industrial processes',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.THERMAL_STORAGE,
            power_rating=3000.0,  # kW thermal
            capacity=50000.0,  # kWh thermal
            efficiency=0.85,
            lifetime=25,
            investment_costs=50.0,  # €/kWh thermal
            operation_costs=5.0,  # €/kW/year
            supported_carriers=[EnergyCarrier.HEAT],
            custom_parameters={
                'storage_medium': 'molten_salt',
                'temperature_range': [290.0, 393.0],  # °C
                'thermal_stratification': True,
                'heat_loss_rate': 0.001,  # %/hour
                'charge_discharge_cycles': 10000
            }
        )
        
        # Industrial Wind Farm
        configs['wind_farm_industrial'] = EquipmentConfig(
            equipment_id='wind_farm_industrial',
            name='Industrial Wind Farm',
            description='Large-scale wind farm for industrial power supply',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.WIND_TURBINE,
            power_rating=10000.0,  # kW
            efficiency=0.45,
            lifetime=20,
            investment_costs=1500.0,  # €/kW
            operation_costs=30.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'turbine_count': 5,
                'hub_height': 100.0,  # m
                'rotor_diameter': 120.0,  # m
                'cut_in_speed': 3.0,  # m/s
                'rated_speed': 12.0,  # m/s
                'cut_out_speed': 25.0,  # m/s
                'grid_connection': 'industrial_substation'
            }
        )
        
        # Industrial Energy Management System
        configs['industrial_ems'] = EquipmentConfig(
            equipment_id='industrial_ems',
            name='Industrial Energy Management System',
            description='Comprehensive EMS for industrial facilities',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=10.0,  # kW
            lifetime=10,
            investment_costs=50000.0,  # €/system
            operation_costs=5000.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT,
                EnergyCarrier.HYDROGEN,
                EnergyCarrier.PRESSURE_AIR
            ],
            custom_parameters={
                'facility_size': 'large_industrial',
                'submetering_points': 100,
                'real_time_optimization': True,
                'demand_response': True,
                'carbon_accounting': True,
                'compliance_reporting': True,
                'machine_learning_optimization': True
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID."""
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in industrial library")
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
                        min_power: float = None,
                        carrier: EnergyCarrier = None) -> Dict[str, EquipmentConfig]:
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
            if min_power and eq_config.power_rating < min_power:
                continue
            
            # Check carrier compatibility
            if carrier and carrier not in eq_config.supported_carriers:
                continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library."""
        return {
            'library_type': 'industrial',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }