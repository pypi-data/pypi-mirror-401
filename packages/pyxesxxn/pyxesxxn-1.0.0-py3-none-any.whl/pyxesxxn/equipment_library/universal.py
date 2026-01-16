"""
Universal Equipment Library.

This module provides equipment configurations that are suitable for
all types of scenarios and applications.
"""

from typing import Dict, List, Any
from .base import EquipmentConfig, EquipmentCategory, EquipmentType, EnergyCarrier


class UniversalEquipmentLibrary:
    """Universal equipment library with generic equipment configurations.
    
    This library contains equipment that can be used across all scenarios
    and is not scenario-specific.
    """
    
    def __init__(self):
        """Initialize the universal equipment library."""
        self.equipment_configs = self._create_universal_equipment()
        
    @property
    def equipment(self):
        """Alias for equipment_configs for backward compatibility."""
        return self.equipment_configs
    
    def _create_universal_equipment(self) -> Dict[str, EquipmentConfig]:
        """Create universal equipment configurations.
        
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations
        """
        configs = {}
        
        # Generic Solar PV System
        configs['solar_pv_residential'] = EquipmentConfig(
            equipment_id='solar_pv_residential',
            name='Residential Solar PV System',
            description='Generic residential solar photovoltaic system',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.SOLAR_PV,
            power_rating=5.0,  # kW
            efficiency=0.20,
            lifetime=25,
            investment_costs=1200.0,  # €/kW
            operation_costs=20.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'capacity_factor': 0.18,
                'degradation_rate': 0.005,
                'temperature_coefficient': -0.004
            }
        )
        
        # Generic Wind Turbine
        configs['wind_turbine_small'] = EquipmentConfig(
            equipment_id='wind_turbine_small',
            name='Small Scale Wind Turbine',
            description='Small scale wind turbine for distributed generation',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.WIND_TURBINE,
            power_rating=50.0,  # kW
            efficiency=0.45,
            lifetime=20,
            investment_costs=1500.0,  # €/kW
            operation_costs=30.0,  # €/kW/year
            co2_emissions=0.0,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'cut_in_speed': 3.0,  # m/s
                'rated_speed': 12.0,  # m/s
                'cut_out_speed': 25.0,  # m/s
                'hub_height': 30.0  # m
            }
        )
        
        # Battery Storage System
        configs['battery_storage_residential'] = EquipmentConfig(
            equipment_id='battery_storage_residential',
            name='Residential Battery Storage',
            description='Lithium-ion battery storage system for residential use',
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=5.0,  # kW
            capacity=10.0,  # kWh
            efficiency=0.95,
            lifetime=15,
            investment_costs=800.0,  # €/kWh
            operation_costs=10.0,  # €/kW/year
            co2_emissions=50.0,  # kg CO2/kWh (manufacturing)
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'self_discharge_rate': 0.001,  # per day
                'depth_of_discharge': 0.9,
                'cycle_life': 5000,
                'operating_temperature_range': [-10, 45]  # Celsius
            }
        )
        
        # Generic Heat Pump
        configs['heat_pump_residential'] = EquipmentConfig(
            equipment_id='heat_pump_residential',
            name='Residential Heat Pump',
            description='Air source heat pump for residential heating and cooling',
            category=EquipmentCategory.CONVERSION,
            equipment_type=EquipmentType.HEAT_PUMP,
            power_rating=10.0,  # kW
            efficiency=3.5,  # COP
            lifetime=20,
            investment_costs=1200.0,  # €/kW
            operation_costs=50.0,  # €/kW/year
            co2_emissions=300.0,  # kg CO2/unit (manufacturing)
            supported_carriers=[EnergyCarrier.ELECTRICITY, EnergyCarrier.HEAT],
            custom_parameters={
                'cop_heating': 3.5,
                'cop_cooling': 3.0,
                'min_operating_temp': -15.0,  # Celsius
                'max_supply_temp': 55.0  # Celsius
            }
        )
        
        # Diesel Generator (Backup)
        configs['diesel_generator'] = EquipmentConfig(
            equipment_id='diesel_generator',
            name='Diesel Generator',
            description='Diesel generator for backup power generation',
            category=EquipmentCategory.GENERATION,
            equipment_type=EquipmentType.GAS_TURBINE,
            power_rating=100.0,  # kW
            efficiency=0.35,
            lifetime=15,
            investment_costs=400.0,  # €/kW
            operation_costs=150.0,  # €/MWh
            co2_emissions=700.0,  # kg CO2/MWh
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'fuel_consumption_rate': 0.25,  # L/kWh
                'startup_time': 0.1,  # hours
                'maintenance_interval': 2000  # hours
            }
        )
        
        # Smart Meter
        configs['smart_meter'] = EquipmentConfig(
            equipment_id='smart_meter',
            name='Smart Meter',
            description='Digital smart meter for energy monitoring and billing',
            category=EquipmentCategory.MEASUREMENT,
            equipment_type=EquipmentType.SMART_METER,
            power_rating=0.005,  # kW (metering only)
            lifetime=15,
            investment_costs=200.0,  # €/unit
            operation_costs=5.0,  # €/unit/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'measurement_accuracy': 0.5,  # %
                'communication_protocol': 'DLMS/COSEM',
                'voltage_range': [180, 250],  # V
                'frequency': 50  # Hz
            }
        )
        
        # Energy Management System
        configs['energy_management_system'] = EquipmentConfig(
            equipment_id='energy_management_system',
            name='Energy Management System',
            description='Central energy management and control system',
            category=EquipmentCategory.CONTROL,
            equipment_type=EquipmentType.EMS,
            power_rating=1.0,  # kW (system consumption)
            lifetime=10,
            investment_costs=5000.0,  # €/system
            operation_costs=500.0,  # €/system/year
            supported_carriers=[
                EnergyCarrier.ELECTRICITY,
                EnergyCarrier.HEAT,
                EnergyCarrier.HYDROGEN
            ],
            custom_parameters={
                'response_time': 1.0,  # seconds
                'prediction_horizon': 24.0,  # hours
                'optimization_interval': 15.0,  # minutes
                'max_controllable_devices': 100
            }
        )
        
        # Transformer
        configs['distribution_transformer'] = EquipmentConfig(
            equipment_id='distribution_transformer',
            name='Distribution Transformer',
            description='Step-down transformer for distribution networks',
            category=EquipmentCategory.INFRASTRUCTURE,
            equipment_type=EquipmentType.TRANSFORMER,
            power_rating=200.0,  # kVA
            efficiency=0.98,
            lifetime=30,
            investment_costs=10000.0,  # €/kVA
            operation_costs=50.0,  # €/kVA/year
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters={
                'primary_voltage': 11.0,  # kV
                'secondary_voltage': 0.4,  # kV
                'no_load_losses': 500.0,  # W
                'load_losses': 2000.0  # W
            }
        )
        
        return configs
    
    def get_equipment(self, equipment_id: str) -> EquipmentConfig:
        """Get equipment configuration by ID.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier
            
        Returns
        -------
        EquipmentConfig
            Equipment configuration
        """
        if equipment_id not in self.equipment_configs:
            raise KeyError(f"Equipment '{equipment_id}' not found in universal library")
        return self.equipment_configs[equipment_id]
    
    def list_equipment(self) -> List[str]:
        """List all equipment IDs in the library.
        
        Returns
        -------
        List[str]
            List of equipment IDs
        """
        return list(self.equipment_configs.keys())
    
    def get_equipment_by_category(self, category: EquipmentCategory) -> Dict[str, EquipmentConfig]:
        """Get all equipment configurations by category.
        
        Parameters
        ----------
        category : EquipmentCategory
            Equipment category
            
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations by category
        """
        return {
            eq_id: eq_config for eq_id, eq_config in self.equipment_configs.items()
            if eq_config.category == category
        }
    
    def get_equipment_by_carrier(self, carrier: EnergyCarrier) -> Dict[str, EquipmentConfig]:
        """Get all equipment configurations by supported energy carrier.
        
        Parameters
        ----------
        carrier : EnergyCarrier
            Energy carrier
            
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of equipment configurations supporting the carrier
        """
        return {
            eq_id: eq_config for eq_id, eq_config in self.equipment_configs.items()
            if carrier in eq_config.supported_carriers
        }
    
    def search_equipment(self, 
                        name_pattern: str = None,
                        category: EquipmentCategory = None,
                        max_power: float = None,
                        min_efficiency: float = None) -> Dict[str, EquipmentConfig]:
        """Search equipment based on criteria.
        
        Parameters
        ----------
        name_pattern : str, optional
            Name pattern to search for (case-insensitive substring match)
        category : EquipmentCategory, optional
            Filter by equipment category
        max_power : float, optional
            Maximum power rating (kW)
        min_efficiency : float, optional
            Minimum efficiency
            
        Returns
        -------
        Dict[str, EquipmentConfig]
            Dictionary of matching equipment configurations
        """
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
            
            # Check efficiency
            if min_efficiency and eq_config.efficiency and eq_config.efficiency < min_efficiency:
                continue
            
            results[eq_id] = eq_config
        
        return results
    
    def export_library(self) -> Dict[str, Any]:
        """Export the complete equipment library.
        
        Returns
        -------
        Dict[str, Any]
            Complete equipment library as dictionary
        """
        return {
            'library_type': 'universal',
            'equipment': {
                eq_id: eq_config.to_dict() 
                for eq_id, eq_config in self.equipment_configs.items()
            }
        }
    
    def export_equipment_data(self) -> Dict[str, Any]:
        """Alias for export_library for backward compatibility.
        
        Returns
        -------
        Dict[str, Any]
            Complete equipment library as dictionary
        """
        return self.export_library()
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost summary statistics for the library.
        
        Returns
        -------
        Dict[str, Any]
            Cost summary statistics
        """
        costs = {
            'investment_costs': [],
            'operation_costs': [],
            'maintenance_costs': []
        }
        
        for eq_config in self.equipment_configs.values():
            if eq_config.investment_costs:
                costs['investment_costs'].append(eq_config.investment_costs)
            if eq_config.operation_costs:
                costs['operation_costs'].append(eq_config.operation_costs)
            if eq_config.maintenance_costs:
                costs['maintenance_costs'].append(eq_config.maintenance_costs)
        
        summary = {}
        for cost_type, cost_list in costs.items():
            if cost_list:
                summary[cost_type] = {
                    'min': min(cost_list),
                    'max': max(cost_list),
                    'mean': sum(cost_list) / len(cost_list),
                    'count': len(cost_list)
                }
        
        return summary