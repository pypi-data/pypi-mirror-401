"""
Rural Equipment Library.

This module provides equipment configurations specifically designed for
rural scenarios, including agricultural systems, remote communities,
and distributed energy resources.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class RuralEquipmentLibrary:
    """Rural equipment library with agricultural and remote area equipment configurations.
    
    This library contains equipment optimized for rural environments
    including agricultural processes, remote power systems, and
    distributed energy resources.
    """
    
    def __init__(self):
        """Initialize the rural equipment library."""
        self.equipment_configs = self._create_rural_equipment()
    
    @property
    def equipment(self) -> Dict[str, EquipmentConfig]:
        """Alias for equipment_configs to maintain backward compatibility.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        return self.equipment_configs
    
    def _create_rural_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create rural-specific equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # Agricultural Solar PV Farm
        configs['agricultural_solar'] = EquipmentConfig(
            equipment_id='agricultural_solar',
            name='Agricultural Solar PV Farm',
            description='Solar PV system integrated with agricultural activities',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PV,
            power_rating=2000.0,  # kW
            efficiency=0.18,
            lifetime=25,
            investment_costs=800.0,  # €/kW
            operation_costs=25.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'height_clearance': 4.0,  # m
                'crop_compatibility': ['tomatoes', 'lettuce', 'herbs'],
                'tracking_system': 'single_axis',
                'ground_coverage': 0.4,
                'agricultural_farming': True
            }
        )
        
        # Rural Wind Turbine
        configs['rural_wind_turbine'] = EquipmentConfig(
            equipment_id='rural_wind_turbine',
            name='Rural Wind Turbine',
            description='Medium-scale wind turbine for rural areas',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.WIND_TURBINE,
            power_rating=1500.0,  # kW
            efficiency=0.40,
            lifetime=20,
            investment_costs=1300.0,  # €/kW
            operation_costs=35.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'hub_height': 80.0,  # m
                'rotor_diameter': 80.0,  # m
                'cut_in_speed': 3.0,  # m/s
                'rated_speed': 11.0,  # m/s
                'cut_out_speed': 25.0,  # m/s
                'noise_level': 45.0,  # dB(A)
                'wildlife_compliance': True
            }
        )
        
        # Biogas Generator
        configs['biogas_generator'] = EquipmentConfig(
            equipment_id='biogas_generator',
            name='Agricultural Biogas Generator',
            description='Biogas generator using agricultural waste',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.BIOMASS_GENERATOR,
            power_rating=500.0,  # kW
            efficiency=0.38,
            lifetime=20,
            investment_costs=2000.0,  # €/kW
            operation_costs=80.0,  # €/kW/year
            co2_emissions=-800.0,  # Negative emissions (waste treatment)
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'feedstock': 'agricultural_waste',
                'biogas_production': 200.0,  # m³/day
                'methane_content': 0.55,
                'digester_volume': 1000.0,  # m³
                'waste_utilization': True,
                'co_generation': True
            }
        )
        
        # Rural Microgrid Controller
        configs['rural_microgrid'] = EquipmentConfig(
            equipment_id='rural_microgrid',
            name='Rural Microgrid Controller',
            description='Energy management system for rural microgrids',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=3.0,  # kW
            lifetime=15,
            investment_costs=20000.0,  # €/system
            operation_costs=1500.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT,
                EnergyCarrier.BIOMASS
            ],
            custom_parameters={
                'grid_isolation': True,
                'community_scale': 'village',
                'renewable_integration': True,
                'energy_storage_management': True,
                'load_shedding': True,
                'maintenance_monitoring': True
            }
        )
        
        # Agricultural Heat Pump
        configs['agricultural_heat_pump'] = EquipmentConfig(
            equipment_id='agricultural_heat_pump',
            name='Agricultural Heat Pump',
            description='Heat pump for agricultural heating and drying',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.HEAT_PUMP,
            power_rating=200.0,  # kW
            efficiency=3.5,  # COP
            lifetime=20,
            investment_costs=1200.0,  # €/kW
            operation_costs=60.0,  # €/kW/year
            co2_emissions=400.0,  # kg CO2/unit
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'heat_source': 'ground_source',
                'heating_application': 'greenhouse',
                'drying_capability': True,
                'temperature_control': 'precise',
                'agricultural_compliance': True
            }
        )
        
        # Rural Battery Storage
        configs['rural_battery_storage'] = EquipmentConfig(
            equipment_id='rural_battery_storage',
            name='Rural Battery Storage System',
            description='Battery storage for rural energy systems',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=500.0,  # kW
            capacity=1000.0,  # kWh
            efficiency=0.92,
            lifetime=15,
            investment_costs=700.0,  # €/kWh
            operation_costs=20.0,  # €/kW/year
            co2_emissions=60.0,  # kg CO2/kWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'technology': 'lithium_iron_phosphate',
                'temperature_range': [-20.0, 50.0],  # °C
                'maintenance_interval': 8760,  # hours
                'rural_environment': True,
                'remote_monitoring': True,
                'safety_systems': True
            }
        )
        
        # Agricultural Tractor Electric
        configs['electric_tractor'] = EquipmentConfig(
            equipment_id='electric_tractor',
            name='Electric Agricultural Tractor',
            description='Battery-powered tractor for sustainable farming',
            category=EquipmentCategory.TRANSPORT,
            equipment_type=EquipmentType.BATTERY_VEHICLE,
            power_rating=150.0,  # kW
            efficiency=0.85,
            lifetime=15,
            investment_costs=3000.0,  # €/kW
            operation_costs=50.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'battery_capacity': 300.0,  # kWh
                'operating_hours': 8.0,  # hours/day
                'charging_time': 6.0,  # hours
                'power_take_off': 100.0,  # kW
                'hitch_category': 'Category_3',
                'all_wheel_drive': True
            }
        )
        
        # Rural Water Pumping System
        configs['water_pumping_system'] = EquipmentConfig(
            equipment_id='water_pumping_system',
            name='Solar Water Pumping System',
            description='Solar-powered water pumping for irrigation',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PUMP,
            power_rating=50.0,  # kW
            efficiency=0.65,
            lifetime=20,
            investment_costs=1500.0,  # €/kW
            operation_costs=30.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'water_flow_rate': 100.0,  # m³/h
                'head_pressure': 50.0,  # m
                'solar_tracking': True,
                'battery_backup': True,
                'irrigation_control': True,
                'remote_monitoring': True
            }
        )
        
        # Rural Pellet Boiler
        configs['pellet_boiler'] = EquipmentConfig(
            equipment_id='pellet_boiler',
            name='Biomass Pellet Boiler',
            description='Biomass pellet boiler for rural heating',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.BOILER,
            power_rating=300.0,  # kW thermal
            efficiency=0.85,
            lifetime=20,
            investment_costs=600.0,  # €/kW thermal
            operation_costs=40.0,  # €/kW thermal/year
            co2_emissions=30.0,  # kg CO2/MWh thermal
            supported_carriers=[EnergyCarrier.HEAT],
            custom_parameters={
                'fuel_type': 'wood_pellets',
                'fuel_consumption': 60.0,  # kg/hour
                'ash_removal': 'automatic',
                'emission_control': True,
                'fuel_storage': 'integrated'
            }
        )
        
        # Rural Hydrogen System
        configs['rural_hydrogen'] = EquipmentConfig(
            equipment_id='rural_hydrogen',
            name='Rural Hydrogen Production System',
            description='Small-scale hydrogen production for rural areas',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.ELECTROLYZER,
            power_rating=100.0,  # kW
            efficiency=0.70,
            lifetime=15,
            investment_costs=2500.0,  # €/kW
            operation_costs=80.0,  # €/kW/year
            co2_emissions=3.0,  # kg CO2/kg H2
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HYDROGEN],
            custom_parameters={
                'hydrogen_production': 20.0,  # kg/day
                'storage_capacity': 100.0,  # kg H2
                'pressure': 350.0,  # bar
                'purity': 99.9,  # %
                'remote_operation': True,
                'solar_integration': True
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID."""
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in rural library")
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
                        agricultural_focus: bool = None) -> Dict[str, EquipmentConfig]:
        """Search equipment based on criteria."""
        results = {}
        
        for eq_id, eq_config in self.equipment_configs.items():
            # Check name pattern
            if name_pattern and name_pattern.lower() not in eq_config.name.lower():
                continue
            
            # Check category
            if category and eq_config.category != category:
                continue
            
            # Check agricultural focus
            if agricultural_focus:
                params = eq_config.custom_parameters
                if not (params.get('agricultural_compliance') or 
                       params.get('agricultural_farming') or
                       params.get('heating_application') == 'greenhouse'):
                    continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library."""
        return {
            'library_type': 'rural',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }