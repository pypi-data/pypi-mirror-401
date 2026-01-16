"""
Railway Equipment Library.

This module provides equipment configurations specifically designed for
railway scenarios, including electrified railways, energy recovery,
and transportation energy systems.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class RailwayEquipmentLibrary:
    """Railway equipment library with transportation-specific equipment configurations.
    
    This library contains equipment optimized for railway transportation
    systems including traction power, energy storage, and power distribution.
    """
    
    def __init__(self):
        """Initialize the railway equipment library."""
        self.equipment_configs = self._create_railway_equipment()
    
    @property
    def equipment(self) -> Dict[str, EquipmentConfig]:
        """Alias for equipment_configs to maintain backward compatibility.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        return self.equipment_configs
    
    def _create_railway_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create railway-specific equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # High-Speed Railway Traction System
        configs['traction_system_hsr'] = EquipmentConfig(
            equipment_id='traction_system_hsr',
            name='High-Speed Railway Traction System',
            description='Advanced traction system for high-speed rail',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.TRACTION_SYSTEM,
            power_rating=8000.0,  # kW per train
            efficiency=0.85,
            lifetime=30,
            investment_costs=2000.0,  # €/kW
            operation_costs=100.0,  # €/kW/year
            co2_emissions=0.0,  # Electric operation
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'voltage_levels': [25000.0, 1500.0],  # AC, DC volts
                'max_speed': 320.0,  # km/h
                'acceleration': 0.5,  # m/s²
                'regenerative_braking': True,
                'catenary_supply': True,
                'pantograph_type': 'double_arm'
            }
        )
        
        # Railway Substation
        configs['railway_substation'] = EquipmentConfig(
            equipment_id='railway_substation',
            name='Railway Traction Substation',
            description='Transformer substation for railway power supply',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.TRACTION_SUBSTATION,
            power_rating=50000.0,  # kVA
            efficiency=0.98,
            lifetime=40,
            investment_costs=800.0,  # €/kVA
            operation_costs=20.0,  # €/kVA/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'input_voltage': 132000.0,  # V AC
                'output_voltage': 25000.0,  # V AC
                'protection_level': 'IEC_61850',
                'rectification': True,
                'harmonic_filtering': True,
                'grounding_system': 'impedance_grounded'
            }
        )
        
        # Railway Energy Storage System
        configs['railway_energy_storage'] = EquipmentConfig(
            equipment_id='railway_energy_storage',
            name='Railway Energy Recovery System',
            description='Energy storage for railway regenerative braking',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=5000.0,  # kW
            capacity=10000.0,  # kWh
            efficiency=0.90,
            lifetime=20,
            investment_costs=800.0,  # €/kWh
            operation_costs=25.0,  # €/kW/year
            co2_emissions=50.0,  # kg CO2/kWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'storage_type': 'lithium_ion',
                'charge_time': 0.5,  # hours
                'discharge_time': 0.5,  # hours
                'cycle_life': 15000,
                'temperature_range': [0.0, 45.0],  # °C
                'fire_suppression': True,
                'emc_protection': True
            }
        )
        
        # Electric Locomotive
        configs['electric_locomotive'] = EquipmentConfig(
            equipment_id='electric_locomotive',
            name='Electric Freight Locomotive',
            description='High-power electric locomotive for freight transport',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.TRACTION_SYSTEM,
            power_rating=6000.0,  # kW
            efficiency=0.82,
            lifetime=35,
            investment_costs=3000.0,  # €/kW
            operation_costs=120.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'traction_power': 6000.0,  # kW
                'adhesion_coefficient': 0.25,
                'max_speed': 120.0,  # km/h
                'axle_load': 25.0,  # tonnes
                ' regenerative_braking': True,
                'dynamic_braking': True,
                'wheel_drive': 'electric'
            }
        )
        
        # Hydrogen Fuel Cell Train
        configs['hydrogen_train'] = EquipmentConfig(
            equipment_id='hydrogen_train',
            name='Hydrogen Fuel Cell Passenger Train',
            description='Zero-emission hydrogen-powered passenger train',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.FUEL_CELL_VEHICLE,
            power_rating=800.0,  # kW
            efficiency=0.65,
            lifetime=25,
            investment_costs=5000.0,  # €/kW
            operation_costs=200.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.HYDROGEN],
            custom_parameters={
                'fuel_cell_power': 800.0,  # kW
                'hydrogen_capacity': 800.0,  # kg
                'range': 800.0,  # km
                'max_speed': 140.0,  # km/h
                'passenger_capacity': 200,
                'refueling_time': 15.0,  # minutes
                'emergency_hydrogen_dumping': True
            }
        )
        
        # Railway Solar Installation
        configs['railway_solar'] = EquipmentConfig(
            equipment_id='railway_solar',
            name='Railway Station Solar PV System',
            description='Solar PV system integrated with railway infrastructure',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PV,
            power_rating=500.0,  # kW
            efficiency=0.20,
            lifetime=25,
            investment_costs=1200.0,  # €/kW
            operation_costs=30.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'tracking_system': 'dual_axis',
                'ground_mounted': True,
                'canopy_function': True,
                'snow_shedding': True,
                'railway_safety_compliance': True,
                'integration_with_catenary': True
            }
        )
        
        # Railway Power Quality Controller
        configs['railway_pqc'] = EquipmentConfig(
            equipment_id='railway_pqc',
            name='Railway Power Quality Controller',
            description='Advanced power quality management for railway systems',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.POWER_QUALITY_CONTROLLER,
            power_rating=2000.0,  # kW
            efficiency=0.95,
            lifetime=20,
            investment_costs=400.0,  # €/kW
            operation_costs=50.0,  # €/kW/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'harmonic_filtering': True,
                'reactive_power_compensation': True,
                'voltage_fluctuation_control': True,
                'frequency_regulation': True,
                'railway_track_earth_current': True,
                'emc_mitigation': True
            }
        )
        
        # Railway Energy Management System
        configs['railway_ems'] = EquipmentConfig(
            equipment_id='railway_ems',
            name='Railway Energy Management System',
            description='Integrated energy management for railway operations',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=5.0,  # kW
            lifetime=15,
            investment_costs=30000.0,  # €/system
            operation_costs=3000.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HYDROGEN
            ],
            custom_parameters={
                'network_coverage': 'entire_railway',
                'real_time_monitoring': True,
                'predictive_maintenance': True,
                'energy_optimization': True,
                'carbon_footprint_tracking': True,
                'integration_with_timetable': True,
                'regenerative_braking_optimization': True
            }
        )
        
        # Railway Battery Electric Multiple Unit
        configs['battery_emutrain'] = EquipmentConfig(
            equipment_id='battery_emutrain',
            name='Battery Electric Multiple Unit',
            description='Battery-powered train for non-electrified routes',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.BATTERY_VEHICLE,
            power_rating=1500.0,  # kW
            efficiency=0.80,
            lifetime=25,
            investment_costs=2500.0,  # €/kW
            operation_costs=100.0,  # €/kW/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'battery_capacity': 2000.0,  # kWh
                'range': 150.0,  # km
                'charging_time': 4.0,  # hours
                'max_speed': 160.0,  # km/h
                'passenger_capacity': 150,
                'rapid_charging': True,
                'regenerative_braking': True
            }
        )
        
        # Railway Catenary System
        configs['catenary_system'] = EquipmentConfig(
            equipment_id='catenary_system',
            name='Railway Catenary System',
            description='Overhead contact system for electric railways',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.POWER_DISTRIBUTION,
            power_rating=200000.0,  # kW
            efficiency=0.99,
            lifetime=50,
            investment_costs=100.0,  # €/m
            operation_costs=2.0,  # €/m/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'voltage': 25000.0,  # V AC
                'frequency': 50.0,  # Hz
                'span_length': 50.0,  # m
                'wire_material': 'copper_cadmium',
                'insulation_level': 'class_B',
                'weather_resistance': 'heavy',
                'maintenance_interval': 8760  # hours
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID."""
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in railway library")
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
                        power_range: tuple = None,
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
            
            # Check power range
            if power_range:
                min_power, max_power = power_range
                if not (min_power <= eq_config.power_rating <= max_power):
                    continue
            
            # Check carrier compatibility
            if carrier and carrier not in eq_config.supported_carriers:
                continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library."""
        return {
            'library_type': 'railway',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }