"""Hydrogen system component implementations.

This module provides physical modeling for hydrogen production, storage, and utilization systems,
including electrolyzers, hydrogen storage tanks, fuel cells, and hydrogen infrastructure.
"""

import math
from typing import Dict, Any, Optional
import numpy as np

from .base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    ExtendedEquipmentCategory,
    register_component_factory,
    calculate_thermodynamic_state
)
from pyxesxxn.equipment_library.base import (
    EnergyCarrier as PyXESXXNEnergyCarrier,
    EquipmentType as PyXESXXNEquipmentType,
    EquipmentCategory as PyXESXXNEquipmentCategory
)


# =============================================================================
# Hydrogen Production - Electrolyzers
# =============================================================================

class AlkalineElectrolyzer(ExtendedEnergyComponent):
    """Alkaline Electrolyzer (AEC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for alkaline electrolyzer."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for alkaline electrolyzer."""
        return {
            'nominal_power': 1000,  # kW
            'hydrogen_production_rate': 180,  # Nm³/h per MW
            'efficiency': 0.68,  # 68% efficiency
            'operating_pressure': 30,  # bar
            'cell_voltage': 1.8,  # V per cell
            'number_of_cells': 500,
            'stack_temperature': 80,  # °C
            'minimum_load': 0.15,  # 15% minimum load
            'maximum_load': 1.10,  # 110% maximum load
            'response_time': 30,  # seconds
            'specific_energy_consumption': 4.3,  # kWh/Nm³
            'electrolyte_concentration': 30,  # % KOH
            'energy_density': 0.2,  # Wh/kg
            'power_density': 300,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate alkaline electrolyzer performance."""
        params = self.config.physical_parameters
        
        # Check if operating within load limits
        load_factor = input_power / params['nominal_power']
        
        if load_factor < params['minimum_load']:
            # Below minimum load, shut down
            power_output = 0.0
            hydrogen_production = 0.0
            actual_efficiency = 0.0
        elif load_factor > params['maximum_load']:
            # Above maximum load, operate at maximum
            actual_power = params['nominal_power'] * params['maximum_load']
            
            # Calculate hydrogen production
            hydrogen_production = actual_power * params['hydrogen_production_rate'] / 1000  # Nm³/h
            
            # Calculate efficiency
            actual_efficiency = params['efficiency'] * (1 - 0.1 * (load_factor - 1.0))  # Efficiency decreases at high load
            actual_efficiency = max(0.6, actual_efficiency)  # Minimum efficiency
            
            power_output = 0.0  # Electrolyzer consumes power, no power output
        else:
            # Normal operation
            actual_power = input_power
            
            # Calculate hydrogen production
            hydrogen_production = actual_power * params['hydrogen_production_rate'] / 1000  # Nm³/h
            
            # Calculate efficiency based on load factor
            if load_factor < 0.5:
                # Efficiency increases with load up to 50%
                actual_efficiency = params['efficiency'] * (0.8 + 0.4 * load_factor)
            else:
                # Efficiency decreases slightly at higher loads
                actual_efficiency = params['efficiency'] * (1 - 0.1 * (load_factor - 0.5))
            
            power_output = 0.0  # Electrolyzer consumes power, no power output
        
        # Calculate hydrogen production in kg/h (density of H2 is 0.0899 kg/Nm³)
        hydrogen_production_kg = hydrogen_production * 0.0899
        
        # Calculate heat generated (waste heat)
        heat_generated = actual_power * (1 - actual_efficiency)  # kWh
        
        # Update physical state
        self._physical_state['temperature'] = params['stack_temperature'] + (actual_power / params['nominal_power']) * 10  # Simplified temperature rise
        self._physical_state['pressure'] = params['operating_pressure']
        self._physical_state['flow_rate'] = hydrogen_production
        
        self._physical_state['internal_state'].update({
            'hydrogen_production': hydrogen_production,
            'hydrogen_production_kg': hydrogen_production_kg,
            'load_factor': load_factor,
            'heat_generated': heat_generated,
            'actual_efficiency': actual_efficiency
        })
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_production': hydrogen_production,
            'hydrogen_production_kg': hydrogen_production_kg,
            'heat_generated': heat_generated,
            'temperature': self._physical_state['temperature'],
            'pressure': self._physical_state['pressure'],
            'flow_rate': self._physical_state['flow_rate'],
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                self._physical_state['temperature'],
                self._physical_state['pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class PEMElectrolyzer(ExtendedEnergyComponent):
    """Proton Exchange Membrane Electrolyzer (PEMEC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for PEM electrolyzer."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for PEM electrolyzer."""
        return {
            'nominal_power': 500,  # kW
            'hydrogen_production_rate': 190,  # Nm³/h per MW
            'efficiency': 0.65,  # 65% efficiency
            'operating_pressure': 70,  # bar (higher pressure than alkaline)
            'cell_voltage': 1.75,  # V per cell
            'number_of_cells': 400,
            'stack_temperature': 60,  # °C (lower temperature than alkaline)
            'minimum_load': 0.05,  # 5% minimum load (faster response)
            'maximum_load': 1.20,  # 120% maximum load
            'response_time': 5,  # seconds (fast response)
            'specific_energy_consumption': 4.5,  # kWh/Nm³
            'membrane_thickness': 50,  # μm
            'energy_density': 0.3,  # Wh/kg
            'power_density': 500,  # W/kg (higher power density than alkaline)
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate PEM electrolyzer performance."""
        params = self.config.physical_parameters
        
        # Check if operating within load limits
        load_factor = input_power / params['nominal_power']
        
        if load_factor < params['minimum_load']:
            # Below minimum load, shut down
            power_output = 0.0
            hydrogen_production = 0.0
            actual_efficiency = 0.0
        elif load_factor > params['maximum_load']:
            # Above maximum load, operate at maximum
            actual_power = params['nominal_power'] * params['maximum_load']
            
            # Calculate hydrogen production
            hydrogen_production = actual_power * params['hydrogen_production_rate'] / 1000  # Nm³/h
            
            # Calculate efficiency
            actual_efficiency = params['efficiency'] * (1 - 0.15 * (load_factor - 1.0))  # Efficiency decreases at high load
            actual_efficiency = max(0.55, actual_efficiency)  # Minimum efficiency
            
            power_output = 0.0  # Electrolyzer consumes power, no power output
        else:
            # Normal operation
            actual_power = input_power
            
            # Calculate hydrogen production
            hydrogen_production = actual_power * params['hydrogen_production_rate'] / 1000  # Nm³/h
            
            # Calculate efficiency based on load factor
            if load_factor < 0.3:
                # Efficiency increases with load up to 30%
                actual_efficiency = params['efficiency'] * (0.7 + 1.0 * load_factor)
            else:
                # Efficiency decreases slightly at higher loads
                actual_efficiency = params['efficiency'] * (1 - 0.1 * (load_factor - 0.3))
            
            power_output = 0.0  # Electrolyzer consumes power, no power output
        
        # Calculate hydrogen production in kg/h
        hydrogen_production_kg = hydrogen_production * 0.0899
        
        # Calculate heat generated (waste heat)
        heat_generated = actual_power * (1 - actual_efficiency)  # kWh
        
        # Update physical state
        self._physical_state['temperature'] = params['stack_temperature'] + (actual_power / params['nominal_power']) * 15  # Simplified temperature rise
        self._physical_state['pressure'] = params['operating_pressure']
        self._physical_state['flow_rate'] = hydrogen_production
        
        self._physical_state['internal_state'].update({
            'hydrogen_production': hydrogen_production,
            'hydrogen_production_kg': hydrogen_production_kg,
            'load_factor': load_factor,
            'heat_generated': heat_generated,
            'actual_efficiency': actual_efficiency
        })
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_production': hydrogen_production,
            'hydrogen_production_kg': hydrogen_production_kg,
            'heat_generated': heat_generated,
            'temperature': self._physical_state['temperature'],
            'pressure': self._physical_state['pressure'],
            'flow_rate': self._physical_state['flow_rate'],
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                self._physical_state['temperature'],
                self._physical_state['pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class SolidOxideElectrolyzer(ExtendedEnergyComponent):
    """Solid Oxide Electrolyzer (SOEC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for SOEC."""
        return "advanced"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for SOEC."""
        return {
            'nominal_power': 500,  # kW
            'hydrogen_production_rate': 220,  # Nm³/h per MW
            'efficiency': 0.85,  # 85% efficiency (higher than PEM/AEC)
            'operating_pressure': 10,  # bar (lower pressure)
            'cell_voltage': 1.1,  # V per cell (lower voltage)
            'number_of_cells': 600,
            'stack_temperature': 850,  # °C (high temperature)
            'minimum_load': 0.20,  # 20% minimum load
            'maximum_load': 1.10,  # 110% maximum load
            'response_time': 600,  # seconds (slow response)
            'specific_energy_consumption': 3.5,  # kWh/Nm³ (lower energy consumption)
            'fuel_utilization': 0.85,  # 85% fuel utilization
            'oxygen_utilization': 0.50,  # 50% oxygen utilization
            'energy_density': 0.15,  # Wh/kg
            'power_density': 400,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate SOEC performance."""
        params = self.config.physical_parameters
        
        # Check if operating within load limits
        load_factor = input_power / params['nominal_power']
        
        if load_factor < params['minimum_load']:
            # Below minimum load, shut down
            power_output = 0.0
            hydrogen_production = 0.0
            actual_efficiency = 0.0
        elif load_factor > params['maximum_load']:
            # Above maximum load, operate at maximum
            actual_power = params['nominal_power'] * params['maximum_load']
            
            # Calculate hydrogen production
            hydrogen_production = actual_power * params['hydrogen_production_rate'] / 1000  # Nm³/h
            
            # Calculate efficiency
            actual_efficiency = params['efficiency'] * (1 - 0.1 * (load_factor - 1.0))  # Efficiency decreases at high load
            actual_efficiency = max(0.75, actual_efficiency)  # Minimum efficiency
            
            power_output = 0.0  # Electrolyzer consumes power, no power output
        else:
            # Normal operation
            actual_power = input_power
            
            # Calculate hydrogen production
            hydrogen_production = actual_power * params['hydrogen_production_rate'] / 1000  # Nm³/h
            
            # Calculate efficiency based on load factor
            if load_factor < 0.5:
                # Efficiency increases with load up to 50%
                actual_efficiency = params['efficiency'] * (0.9 + 0.2 * load_factor)
            else:
                # Efficiency remains high at higher loads
                actual_efficiency = params['efficiency'] * (1 - 0.05 * (load_factor - 0.5))
            
            power_output = 0.0  # Electrolyzer consumes power, no power output
        
        # Calculate hydrogen production in kg/h
        hydrogen_production_kg = hydrogen_production * 0.0899
        
        # Calculate heat required/available
        # SOEC can operate in endothermic mode at high efficiency
        if actual_efficiency > 1.0:
            # Heat input required (endothermic)
            heat_required = actual_power * (actual_efficiency - 1.0)
            heat_generated = -heat_required
        else:
            # Heat generated (exothermic)
            heat_generated = actual_power * (1 - actual_efficiency)
        
        # Update physical state
        self._physical_state['temperature'] = params['stack_temperature'] + (actual_power / params['nominal_power'] - 0.5) * 50  # Temperature varies with load
        self._physical_state['pressure'] = params['operating_pressure']
        self._physical_state['flow_rate'] = hydrogen_production
        
        self._physical_state['internal_state'].update({
            'hydrogen_production': hydrogen_production,
            'hydrogen_production_kg': hydrogen_production_kg,
            'load_factor': load_factor,
            'heat_generated': heat_generated,
            'actual_efficiency': actual_efficiency
        })
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_production': hydrogen_production,
            'hydrogen_production_kg': hydrogen_production_kg,
            'heat_generated': heat_generated,
            'temperature': self._physical_state['temperature'],
            'pressure': self._physical_state['pressure'],
            'flow_rate': self._physical_state['flow_rate'],
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                self._physical_state['temperature'],
                self._physical_state['pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


# =============================================================================
# Hydrogen Storage Systems
# =============================================================================

class HighPressureHydrogenTank(ExtendedEnergyComponent):
    """High Pressure Hydrogen Tank physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for high pressure hydrogen tank."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for high pressure hydrogen tank."""
        return {
            'storage_capacity': 500,  # kg
            'operating_pressure': 70,  # bar
            'minimum_pressure': 5,  # bar
            'maximum_pressure': 875,  # bar (125% design pressure)
            'tank_volume': 25,  # m³
            'tank_material': 'carbon_fiber',
            'heat_loss_coefficient': 0.05,  # % per hour
            'refueling_rate': 5,  # kg/min (fast refueling)
            'defueling_rate': 3,  # kg/min
            'hydrogen_density': 0.0899,  # kg/Nm³
            'energy_density': 33000,  # Wh/kg (hydrogen energy density)
            'power_density': 0.1,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate high pressure hydrogen tank performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        
        soc = self._physical_state['internal_state']['soc']
        current_mass = soc * params['storage_capacity']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        if input_power > 0:  # Filling the tank
            # Calculate mass flow rate (input_power represents kg/h)
            mass_flow_rate = input_power
            
            # Calculate mass increase
            mass_increase = mass_flow_rate * time_step
            new_mass = min(current_mass + mass_increase, params['storage_capacity'])
            new_soc = new_mass / params['storage_capacity']
            
            # Calculate pressure (ideal gas law)
            new_pressure = params['operating_pressure'] * new_soc / (params['storage_capacity'] / params['tank_volume'] * params['hydrogen_density'])
            new_pressure = min(new_pressure, params['maximum_pressure'])
            
            power_output = 0.0  # No power output during filling
            actual_efficiency = 0.99  # Very high efficiency for storage
        else:  # Emptying the tank
            # Calculate mass flow rate (input_power represents kg/h, negative)
            mass_flow_rate = abs(input_power)
            
            # Calculate mass decrease
            mass_decrease = mass_flow_rate * time_step
            new_mass = max(current_mass - mass_decrease, 0)
            new_soc = new_mass / params['storage_capacity']
            
            # Calculate pressure (ideal gas law)
            new_pressure = params['operating_pressure'] * new_soc / (params['storage_capacity'] / params['tank_volume'] * params['hydrogen_density'])
            new_pressure = max(new_pressure, params['minimum_pressure'])
            
            power_output = 0.0  # No power output during emptying
            actual_efficiency = 0.99  # Very high efficiency for storage
        
        # Apply heat losses
        heat_loss = current_mass * 14300 * params['heat_loss_coefficient'] / 100 * time_step / 3600  # kWh
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['pressure'] = new_pressure
        self._physical_state['temperature'] = ambient_temp
        self._physical_state['flow_rate'] = mass_flow_rate
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_stored': new_mass,
            'hydrogen_flow_rate': mass_flow_rate,
            'temperature': ambient_temp,
            'pressure': new_pressure,
            'flow_rate': mass_flow_rate,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                new_pressure,
                {'cp': 14.3, 'density': params['hydrogen_density']}  # Hydrogen properties
            )
        }


class LiquidHydrogenTank(ExtendedEnergyComponent):
    """Liquid Hydrogen Tank physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for liquid hydrogen tank."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for liquid hydrogen tank."""
        return {
            'storage_capacity': 1000,  # kg
            'operating_temperature': -253,  # °C (boiling point of hydrogen)
            'vapor_pressure': 1.5,  # bar
            'maximum_pressure': 3.0,  # bar
            'tank_volume': 14,  # m³ (1000 kg LH2)
            'tank_material': 'stainless_steel',
            'heat_loss_rate': 50,  # W/m²
            'tank_surface_area': 50,  # m²
            'boil_off_rate': 0.05,  # % per day
            'filling_rate': 10,  # kg/min
            'withdrawal_rate': 5,  # kg/min
            'liquid_hydrogen_density': 70.8,  # kg/m³
            'energy_density': 33000,  # Wh/kg (hydrogen energy density)
            'power_density': 0.05,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate liquid hydrogen tank performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        
        soc = self._physical_state['internal_state']['soc']
        current_mass = soc * params['storage_capacity']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        if input_power > 0:  # Filling the tank
            # Calculate mass flow rate (input_power represents kg/h)
            mass_flow_rate = input_power
            
            # Calculate mass increase
            mass_increase = mass_flow_rate * time_step
            new_mass = min(current_mass + mass_increase, params['storage_capacity'])
            new_soc = new_mass / params['storage_capacity']
            
            power_output = 0.0  # No power output during filling
            actual_efficiency = 0.98  # High efficiency for storage
        else:  # Emptying the tank
            # Calculate mass flow rate (input_power represents kg/h, negative)
            mass_flow_rate = abs(input_power)
            
            # Calculate mass decrease
            mass_decrease = mass_flow_rate * time_step
            new_mass = max(current_mass - mass_decrease, 0)
            new_soc = new_mass / params['storage_capacity']
            
            power_output = 0.0  # No power output during emptying
            actual_efficiency = 0.98  # High efficiency for storage
        
        # Apply boil-off losses
        boil_off_per_hour = params['boil_off_rate'] / 24  # % per hour
        boil_off_mass = new_mass * boil_off_per_hour * time_step
        new_mass_after_boil_off = max(new_mass - boil_off_mass, 0)
        new_soc_after_boil_off = new_mass_after_boil_off / params['storage_capacity']
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc_after_boil_off
        self._physical_state['pressure'] = params['vapor_pressure']
        self._physical_state['temperature'] = params['operating_temperature']
        self._physical_state['flow_rate'] = mass_flow_rate
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_stored': new_mass_after_boil_off,
            'hydrogen_flow_rate': mass_flow_rate,
            'boil_off_rate': boil_off_mass / time_step,
            'temperature': params['operating_temperature'],
            'pressure': params['vapor_pressure'],
            'flow_rate': mass_flow_rate,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                params['operating_temperature'],
                params['vapor_pressure'],
                {'cp': 14.3, 'density': params['liquid_hydrogen_density']}  # LH2 properties
            )
        }


class MetalHydrideHydrogenStorage(ExtendedEnergyComponent):
    """Metal Hydride Hydrogen Storage physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for metal hydride storage."""
        return "distributed"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for metal hydride storage."""
        return {
            'storage_capacity': 50,  # kg
            'operating_pressure': 30,  # bar
            'minimum_pressure': 2,  # bar
            'maximum_pressure': 45,  # bar
            'hydrogen_to_metal_ratio': 1.5,  # wt%
            'absorption_rate': 0.5,  # kg/h
            'desorption_rate': 0.3,  # kg/h
            'absorption_heat': 30,  # kJ/mol
            'desorption_heat': 35,  # kJ/mol
            'operating_temperature': 80,  # °C
            'minimum_temperature': 20,  # °C
            'maximum_temperature': 120,  # °C
            'thermal_conductivity': 10,  # W/(m·K)
            'energy_density': 1500,  # Wh/kg (system energy density)
            'power_density': 0.2,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate metal hydride storage performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        
        soc = self._physical_state['internal_state']['soc']
        current_mass = soc * params['storage_capacity']
        ambient_temp = operating_conditions.get('ambient_temperature', 80.0) if operating_conditions else 80.0
        
        if input_power > 0:  # Absorbing hydrogen
            # Calculate mass flow rate (input_power represents kg/h)
            mass_flow_rate = min(input_power, params['absorption_rate'])
            
            # Calculate mass increase
            mass_increase = mass_flow_rate * time_step
            new_mass = min(current_mass + mass_increase, params['storage_capacity'])
            new_soc = new_mass / params['storage_capacity']
            
            # Calculate absorption heat (exothermic)
            heat_generated = mass_increase * (params['absorption_heat'] / 2.016) * 1000 / 3600  # kWh
            
            power_output = 0.0  # No power output during absorption
            actual_efficiency = 0.95  # High efficiency for storage
        else:  # Desorbing hydrogen
            # Calculate mass flow rate (input_power represents kg/h, negative)
            mass_flow_rate = min(abs(input_power), params['desorption_rate'])
            
            # Calculate mass decrease
            mass_decrease = mass_flow_rate * time_step
            new_mass = max(current_mass - mass_decrease, 0)
            new_soc = new_mass / params['storage_capacity']
            
            # Calculate desorption heat (endothermic)
            heat_required = mass_decrease * (params['desorption_heat'] / 2.016) * 1000 / 3600  # kWh
            heat_generated = -heat_required
            
            power_output = 0.0  # No power output during desorption
            actual_efficiency = 0.95  # High efficiency for storage
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['pressure'] = params['operating_pressure']
        self._physical_state['temperature'] = ambient_temp
        self._physical_state['flow_rate'] = mass_flow_rate
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_stored': new_mass,
            'hydrogen_flow_rate': mass_flow_rate,
            'heat_generated': heat_generated,
            'temperature': ambient_temp,
            'pressure': params['operating_pressure'],
            'flow_rate': mass_flow_rate,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                params['operating_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class SaltCavernHydrogenStorage(ExtendedEnergyComponent):
    """Salt Cavern Hydrogen Storage physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for salt cavern storage."""
        return "utility"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for salt cavern storage."""
        return {
            'storage_capacity': 100000,  # kg
            'operating_pressure': 100,  # bar
            'minimum_pressure': 30,  # bar
            'maximum_pressure': 150,  # bar
            'cavern_volume': 100000,  # m³
            'porosity': 0.95,
            'permeability': 1.0e-12,  # m²
            'compression_factor': 1.0,
            'filling_rate': 500,  # kg/h
            'withdrawal_rate': 300,  # kg/h
            'hydrogen_density': 0.0899,  # kg/Nm³
            'energy_density': 30000,  # Wh/kg (hydrogen energy density)
            'power_density': 0.01,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate salt cavern storage performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        
        soc = self._physical_state['internal_state']['soc']
        current_mass = soc * params['storage_capacity']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        if input_power > 0:  # Filling the cavern
            # Calculate mass flow rate (input_power represents kg/h)
            mass_flow_rate = min(input_power, params['filling_rate'])
            
            # Calculate mass increase
            mass_increase = mass_flow_rate * time_step
            new_mass = min(current_mass + mass_increase, params['storage_capacity'])
            new_soc = new_mass / params['storage_capacity']
            
            # Calculate pressure (simplified)
            new_pressure = params['minimum_pressure'] + (params['maximum_pressure'] - params['minimum_pressure']) * new_soc
            
            power_output = 0.0  # No power output during filling
            actual_efficiency = 0.995  # Very high efficiency for storage
        else:  # Emptying the cavern
            # Calculate mass flow rate (input_power represents kg/h, negative)
            mass_flow_rate = min(abs(input_power), params['withdrawal_rate'])
            
            # Calculate mass decrease
            mass_decrease = mass_flow_rate * time_step
            new_mass = max(current_mass - mass_decrease, 0)
            new_soc = new_mass / params['storage_capacity']
            
            # Calculate pressure (simplified)
            new_pressure = params['minimum_pressure'] + (params['maximum_pressure'] - params['minimum_pressure']) * new_soc
            
            power_output = 0.0  # No power output during emptying
            actual_efficiency = 0.995  # Very high efficiency for storage
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['pressure'] = new_pressure
        self._physical_state['temperature'] = ambient_temp
        self._physical_state['flow_rate'] = mass_flow_rate
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_stored': new_mass,
            'hydrogen_flow_rate': mass_flow_rate,
            'temperature': ambient_temp,
            'pressure': new_pressure,
            'flow_rate': mass_flow_rate,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                new_pressure,
                {'cp': 14.3, 'density': params['hydrogen_density']}  # Hydrogen properties
            )
        }


# =============================================================================
# Hydrogen Utilization - Fuel Cells
# =============================================================================

class PEMFuelCell(ExtendedEnergyComponent):
    """Proton Exchange Membrane Fuel Cell (PEMFC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for PEM fuel cell."""
        return "mobile"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for PEM fuel cell."""
        return {
            'nominal_power': 100,  # kW
            'efficiency': 0.55,  # 55% efficiency
            'operating_pressure': 3,  # bar
            'cell_voltage': 0.7,  # V per cell
            'number_of_cells': 200,
            'stack_temperature': 80,  # °C
            'minimum_load': 0.10,  # 10% minimum load
            'maximum_load': 1.20,  # 120% maximum load
            'response_time': 5,  # seconds (fast response)
            'specific_energy_consumption': 0.3,  # kg/kWh
            'hydrogen_utilization': 0.85,  # 85% hydrogen utilization
            'air_utilization': 2.0,  # Air stoichiometric ratio
            'water_management': 'liquid',
            'energy_density': 400,  # Wh/kg
            'power_density': 2000,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate PEM fuel cell performance."""
        params = self.config.physical_parameters
        
        # input_power represents hydrogen flow rate in kg/h
        hydrogen_flow_rate = input_power
        
        # Calculate hydrogen energy input (HHV of hydrogen is 33.3 kWh/kg)
        hydrogen_energy = hydrogen_flow_rate * 33.3  # kWh/h
        
        # Calculate electrical power output
        power_output = hydrogen_energy * params['efficiency']
        
        # Check if operating within load limits
        load_factor = power_output / params['nominal_power']
        
        if load_factor < params['minimum_load']:
            # Below minimum load, shut down
            power_output = 0.0
            actual_efficiency = 0.0
        elif load_factor > params['maximum_load']:
            # Above maximum load, operate at maximum
            power_output = params['nominal_power'] * params['maximum_load']
            actual_efficiency = params['efficiency'] * (1 - 0.15 * (load_factor - 1.0))
            actual_efficiency = max(0.45, actual_efficiency)
        else:
            # Normal operation
            # Calculate efficiency based on load factor
            if load_factor < 0.5:
                actual_efficiency = params['efficiency'] * (0.8 + 0.4 * load_factor)
            else:
                actual_efficiency = params['efficiency'] * (1 - 0.1 * (load_factor - 0.5))
        
        # Calculate actual hydrogen consumption
        actual_hydrogen_consumption = power_output / (33.3 * actual_efficiency)  # kg/h
        
        # Calculate heat generated
        heat_generated = power_output * (1 / actual_efficiency - 1)  # kWh
        
        # Update physical state
        stack_temperature = params['stack_temperature'] + (load_factor - 0.5) * 20  # Simplified temperature rise
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_consumption': actual_hydrogen_consumption,
            'heat_generated': heat_generated,
            'temperature': stack_temperature,
            'pressure': params['operating_pressure'],
            'flow_rate': actual_hydrogen_consumption,
            'internal_state': {
                'load_factor': load_factor,
                'hydrogen_flow_rate': actual_hydrogen_consumption,
                'stack_temperature': stack_temperature
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                stack_temperature,
                params['operating_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class SolidOxideFuelCell(ExtendedEnergyComponent):
    """Solid Oxide Fuel Cell (SOFC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for SOFC."""
        return "stationary"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for SOFC."""
        return {
            'nominal_power': 250,  # kW
            'efficiency': 0.65,  # 65% efficiency (higher than PEMFC)
            'operating_pressure': 1,  # bar (atmospheric pressure)
            'cell_voltage': 0.85,  # V per cell
            'number_of_cells': 150,
            'stack_temperature': 750,  # °C (high temperature)
            'minimum_load': 0.20,  # 20% minimum load
            'maximum_load': 1.10,  # 110% maximum load
            'response_time': 300,  # seconds (slow response)
            'specific_energy_consumption': 0.25,  # kg/kWh (lower consumption)
            'fuel_utilization': 0.85,  # 85% fuel utilization
            'air_utilization': 1.5,  # Air stoichiometric ratio
            'co_tolerance': 1.0,  # % CO tolerance
            'energy_density': 300,  # Wh/kg
            'power_density': 1500,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate SOFC performance."""
        params = self.config.physical_parameters
        
        # input_power represents hydrogen flow rate in kg/h
        hydrogen_flow_rate = input_power
        
        # Calculate hydrogen energy input (HHV of hydrogen is 33.3 kWh/kg)
        hydrogen_energy = hydrogen_flow_rate * 33.3  # kWh/h
        
        # Calculate electrical power output
        power_output = hydrogen_energy * params['efficiency']
        
        # Check if operating within load limits
        load_factor = power_output / params['nominal_power']
        
        if load_factor < params['minimum_load']:
            # Below minimum load, shut down
            power_output = 0.0
            actual_efficiency = 0.0
        elif load_factor > params['maximum_load']:
            # Above maximum load, operate at maximum
            power_output = params['nominal_power'] * params['maximum_load']
            actual_efficiency = params['efficiency'] * (1 - 0.1 * (load_factor - 1.0))
            actual_efficiency = max(0.55, actual_efficiency)
        else:
            # Normal operation
            # Calculate efficiency based on load factor
            if load_factor < 0.5:
                actual_efficiency = params['efficiency'] * (0.9 + 0.2 * load_factor)
            else:
                actual_efficiency = params['efficiency'] * (1 - 0.05 * (load_factor - 0.5))
        
        # Calculate actual hydrogen consumption
        actual_hydrogen_consumption = power_output / (33.3 * actual_efficiency)  # kg/h
        
        # Calculate heat generated
        heat_generated = power_output * (1 / actual_efficiency - 1)  # kWh
        
        # Update physical state
        stack_temperature = params['stack_temperature'] + (load_factor - 0.5) * 50  # Simplified temperature rise
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_consumption': actual_hydrogen_consumption,
            'heat_generated': heat_generated,
            'temperature': stack_temperature,
            'pressure': params['operating_pressure'],
            'flow_rate': actual_hydrogen_consumption,
            'internal_state': {
                'load_factor': load_factor,
                'hydrogen_flow_rate': actual_hydrogen_consumption,
                'stack_temperature': stack_temperature
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                stack_temperature,
                params['operating_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class PhosphoricAcidFuelCell(ExtendedEnergyComponent):
    """Phosphoric Acid Fuel Cell (PAFC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for PAFC."""
        return "stationary"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for PAFC."""
        return {
            'nominal_power': 200,  # kW
            'efficiency': 0.45,  # 45% efficiency
            'operating_pressure': 1,  # bar
            'cell_voltage': 0.75,  # V per cell
            'number_of_cells': 180,
            'stack_temperature': 200,  # °C
            'minimum_load': 0.15,  # 15% minimum load
            'maximum_load': 1.10,  # 110% maximum load
            'response_time': 120,  # seconds
            'specific_energy_consumption': 0.35,  # kg/kWh
            'fuel_utilization': 0.85,  # 85% fuel utilization
            'air_utilization': 2.5,  # Air stoichiometric ratio
            'co_tolerance': 1.5,  # % CO tolerance
            'energy_density': 300,  # Wh/kg
            'power_density': 1000,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate PAFC performance."""
        params = self.config.physical_parameters
        
        # input_power represents hydrogen flow rate in kg/h
        hydrogen_flow_rate = input_power
        
        # Calculate hydrogen energy input (HHV of hydrogen is 33.3 kWh/kg)
        hydrogen_energy = hydrogen_flow_rate * 33.3  # kWh/h
        
        # Calculate electrical power output
        power_output = hydrogen_energy * params['efficiency']
        
        # Check if operating within load limits
        load_factor = power_output / params['nominal_power']
        
        if load_factor < params['minimum_load']:
            # Below minimum load, shut down
            power_output = 0.0
            actual_efficiency = 0.0
        elif load_factor > params['maximum_load']:
            # Above maximum load, operate at maximum
            power_output = params['nominal_power'] * params['maximum_load']
            actual_efficiency = params['efficiency'] * (1 - 0.12 * (load_factor - 1.0))
            actual_efficiency = max(0.35, actual_efficiency)
        else:
            # Normal operation
            # Calculate efficiency based on load factor
            if load_factor < 0.4:
                actual_efficiency = params['efficiency'] * (0.8 + 0.5 * load_factor)
            else:
                actual_efficiency = params['efficiency'] * (1 - 0.08 * (load_factor - 0.4))
        
        # Calculate actual hydrogen consumption
        actual_hydrogen_consumption = power_output / (33.3 * actual_efficiency)  # kg/h
        
        # Calculate heat generated
        heat_generated = power_output * (1 / actual_efficiency - 1)  # kWh
        
        # Update physical state
        stack_temperature = params['stack_temperature'] + (load_factor - 0.5) * 30  # Simplified temperature rise
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_consumption': actual_hydrogen_consumption,
            'heat_generated': heat_generated,
            'temperature': stack_temperature,
            'pressure': params['operating_pressure'],
            'flow_rate': actual_hydrogen_consumption,
            'internal_state': {
                'load_factor': load_factor,
                'hydrogen_flow_rate': actual_hydrogen_consumption,
                'stack_temperature': stack_temperature
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                stack_temperature,
                params['operating_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


# =============================================================================
# Hydrogen Infrastructure
# =============================================================================

class HydrogenCompressor(ExtendedEnergyComponent):
    """Hydrogen Compressor physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for hydrogen compressor."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for hydrogen compressor."""
        return {
            'nominal_power': 100,  # kW
            'flow_rate': 100,  # Nm³/h
            'inlet_pressure': 5,  # bar
            'outlet_pressure': 70,  # bar
            'efficiency': 0.75,  # 75% efficiency
            'compression_ratio': 14,  # Outlet pressure / inlet pressure
            'number_of_stages': 4,
            'compressor_type': 'reciprocating',
            'specific_energy_consumption': 1.2,  # kWh/Nm³
            'response_time': 60,  # seconds
            'energy_density': 0.1,  # Wh/kg
            'power_density': 500,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate hydrogen compressor performance."""
        params = self.config.physical_parameters
        
        # input_power represents hydrogen flow rate in Nm³/h
        hydrogen_flow_rate = input_power
        
        # Calculate power required for compression
        # Using isentropic compression formula for hydrogen (γ = 1.41)
        power_required = (hydrogen_flow_rate / 3600) * 100000 * params['inlet_pressure'] * math.log(params['compression_ratio']) / (params['efficiency'] * 1000)  # kW
        
        # Calculate actual power output (compressor consumes power)
        power_output = -power_required
        
        # Calculate temperature rise during compression
        temperature_rise = 298.15 * (params['compression_ratio'] ** ((1.41 - 1) / 1.41) - 1)  # K
        outlet_temperature = 25 + temperature_rise  # °C
        
        return {
            'power_output': power_output,
            'efficiency': params['efficiency'],
            'hydrogen_flow_rate': hydrogen_flow_rate,
            'outlet_temperature': outlet_temperature,
            'temperature': outlet_temperature,
            'pressure': params['outlet_pressure'],
            'flow_rate': hydrogen_flow_rate,
            'internal_state': {
                'compression_ratio': params['compression_ratio'],
                'power_required': power_required,
                'outlet_temperature': outlet_temperature
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                outlet_temperature,
                params['outlet_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class HydrogenPurificationPSA(ExtendedEnergyComponent):
    """Hydrogen Purification (PSA) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for hydrogen purification."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for hydrogen purification."""
        return {
            'nominal_capacity': 500,  # Nm³/h
            'efficiency': 0.90,  # 90% efficiency
            'inlet_pressure': 20,  # bar
            'outlet_pressure': 18,  # bar (pressure drop)
            'inlet_purity': 0.90,  # 90% inlet purity
            'outlet_purity': 0.9999,  # 99.99% outlet purity
            'cycle_time': 4,  # minutes
            'adsorbent_material': 'activated_carbon',
            'specific_energy_consumption': 0.1,  # kWh/Nm³
            'recovery_rate': 0.85,  # 85% hydrogen recovery
            'energy_density': 0.05,  # Wh/kg
            'power_density': 200,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate hydrogen purification performance."""
        params = self.config.physical_parameters
        
        # input_power represents hydrogen flow rate in Nm³/h
        inlet_flow_rate = input_power
        
        # Calculate outlet flow rate based on recovery rate
        outlet_flow_rate = inlet_flow_rate * params['recovery_rate']
        
        # Calculate power consumption
        power_consumption = outlet_flow_rate * params['specific_energy_consumption']  # kW
        
        # Power output (purification consumes power)
        power_output = -power_consumption
        
        # Calculate temperature rise (minimal for PSA)
        temperature_rise = 5  # °C
        
        return {
            'power_output': power_output,
            'efficiency': params['efficiency'],
            'inlet_flow_rate': inlet_flow_rate,
            'outlet_flow_rate': outlet_flow_rate,
            'hydrogen_purity': params['outlet_purity'],
            'temperature': 25 + temperature_rise,
            'pressure': params['outlet_pressure'],
            'flow_rate': outlet_flow_rate,
            'internal_state': {
                'recovery_rate': params['recovery_rate'],
                'power_consumption': power_consumption,
                'hydrogen_purity': params['outlet_purity']
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                25 + temperature_rise,
                params['outlet_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class HydrogenRefuelingStation(ExtendedEnergyComponent):
    """Hydrogen Refueling Station physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for hydrogen refueling station."""
        return "transport"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for hydrogen refueling station."""
        return {
            'refueling_rate': 5,  # kg/min
            'storage_capacity': 1000,  # kg
            'operating_pressure': 875,  # bar
            'minimum_pressure': 350,  # bar
            'cooling_power': 50,  # kW
            'refueling_time': 5,  # minutes
            'station_efficiency': 0.90,  # 90% efficiency
            'number_of_dispensers': 4,
            'energy_density': 0.1,  # Wh/kg
            'power_density': 300,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate hydrogen refueling station performance."""
        params = self.config.physical_parameters
        
        # input_power represents number of vehicles refueling
        num_vehicles = input_power
        
        # Calculate total hydrogen dispensed
        hydrogen_dispensed = num_vehicles * 5  # kg per vehicle
        hydrogen_flow_rate = hydrogen_dispensed / (time_step * 60)  # kg/min
        
        # Calculate power required for cooling
        cooling_power = params['cooling_power'] * num_vehicles / params['number_of_dispensers']  # kW
        
        # Calculate power output (refueling consumes power for cooling)
        power_output = -cooling_power
        
        return {
            'power_output': power_output,
            'efficiency': params['station_efficiency'],
            'hydrogen_dispensed': hydrogen_dispensed,
            'hydrogen_flow_rate': hydrogen_flow_rate,
            'number_of_vehicles': num_vehicles,
            'temperature': -40,  # °C (cooled hydrogen)
            'pressure': params['operating_pressure'],
            'flow_rate': hydrogen_flow_rate,
            'internal_state': {
                'cooling_power': cooling_power,
                'refueling_rate': hydrogen_flow_rate
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                -40,
                params['operating_pressure'],
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


class HydrogenPipeline(ExtendedEnergyComponent):
    """Hydrogen Pipeline physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for hydrogen pipeline."""
        return "infrastructure"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for hydrogen pipeline."""
        return {
            'length': 100,  # km
            'diameter': 0.5,  # meters
            'operating_pressure': 50,  # bar
            'minimum_pressure': 20,  # bar
            'maximum_pressure': 60,  # bar
            'flow_rate': 1000,  # Nm³/h
            'pressure_drop': 0.5,  # bar/km
            'pipe_material': 'steel',
            'leak_rate': 0.01,  # % per year
            'thermal_conductivity': 50,  # W/(m·K)
            'energy_density': 0.01,  # Wh/kg
            'power_density': 100,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate hydrogen pipeline performance."""
        params = self.config.physical_parameters
        
        # input_power represents hydrogen flow rate in Nm³/h
        hydrogen_flow_rate = input_power
        
        # Calculate pressure drop
        pressure_drop = params['pressure_drop'] * params['length']  # bar
        outlet_pressure = max(params['operating_pressure'] - pressure_drop, params['minimum_pressure'])
        
        # Calculate leakage losses
        leakage_rate_per_hour = params['leak_rate'] / (365 * 24)  # % per hour
        leakage = hydrogen_flow_rate * leakage_rate_per_hour / 100  # Nm³/h
        
        # Calculate heat losses
        heat_loss = (params['length'] * 1000) * params['thermal_conductivity'] * 25 / 1000000  # kW (simplified)
        
        # Pipeline doesn't produce power
        power_output = 0.0
        actual_efficiency = 1.0 - leakage_rate_per_hour / 100  # Account for leakage
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'hydrogen_flow_rate': hydrogen_flow_rate,
            'outlet_pressure': outlet_pressure,
            'leakage': leakage,
            'heat_loss': heat_loss,
            'temperature': 25,  # °C
            'pressure': outlet_pressure,
            'flow_rate': hydrogen_flow_rate,
            'internal_state': {
                'pressure_drop': pressure_drop,
                'leakage_rate': leakage,
                'heat_loss': heat_loss
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                25,
                outlet_pressure,
                {'cp': 14.3, 'density': 0.0899}  # Hydrogen properties
            )
        }


# =============================================================================
# Factory Registration
# =============================================================================

# Register all hydrogen system component factories
register_component_factory(
    ExtendedEquipmentType.ALKALINE_ELECTROLYZER,
    AlkalineElectrolyzer
)

register_component_factory(
    ExtendedEquipmentType.PEM_ELECTROLYZER,
    PEMElectrolyzer
)

register_component_factory(
    ExtendedEquipmentType.SOLID_OXIDE_ELECTROLYZER,
    SolidOxideElectrolyzer
)

register_component_factory(
    ExtendedEquipmentType.HIGH_PRESSURE_HYDROGEN_TANK,
    HighPressureHydrogenTank
)

register_component_factory(
    ExtendedEquipmentType.LIQUID_HYDROGEN_TANK,
    LiquidHydrogenTank
)

register_component_factory(
    ExtendedEquipmentType.METAL_HYDRIDE_HYDROGEN_STORAGE,
    MetalHydrideHydrogenStorage
)

register_component_factory(
    ExtendedEquipmentType.SALT_CAVERN_HYDROGEN_STORAGE,
    SaltCavernHydrogenStorage
)

register_component_factory(
    ExtendedEquipmentType.PEM_FUEL_CELL,
    PEMFuelCell
)

register_component_factory(
    ExtendedEquipmentType.SOLID_OXIDE_FUEL_CELL,
    SolidOxideFuelCell
)

register_component_factory(
    ExtendedEquipmentType.PHOSPHORIC_ACID_FUEL_CELL,
    PhosphoricAcidFuelCell
)

register_component_factory(
    ExtendedEquipmentType.HYDROGEN_COMPRESSOR,
    HydrogenCompressor
)

register_component_factory(
    ExtendedEquipmentType.HYDROGEN_PURIFICATION_PSA,
    HydrogenPurificationPSA
)

register_component_factory(
    ExtendedEquipmentType.HYDROGEN_REFUELING_STATION,
    HydrogenRefuelingStation
)

register_component_factory(
    ExtendedEquipmentType.HYDROGEN_PIPELINE,
    HydrogenPipeline
)
