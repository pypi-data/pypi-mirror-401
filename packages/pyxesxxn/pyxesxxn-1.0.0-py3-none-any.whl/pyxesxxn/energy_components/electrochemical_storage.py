"""Electrochemical storage component implementations.

This module provides physical modeling for electrochemical storage systems,
including batteries, supercapacitors, flywheels, and compressed air storage systems.
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
    calculate_thermodynamic_state,
    calculate_exergy
)
from pyxesxxn.equipment_library.base import (
    EnergyCarrier as PyXESXXNEnergyCarrier,
    EquipmentType as PyXESXXNEquipmentType,
    EquipmentCategory as PyXESXXNEquipmentCategory
)


# =============================================================================
# Battery Storage Systems
# =============================================================================

class LithiumIronPhosphateBattery(ExtendedEnergyComponent):
    """Lithium Iron Phosphate (LiFePO4) battery physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for LiFePO4 battery."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for LiFePO4 battery."""
        return {
            'nominal_capacity': 100,  # kWh
            'max_charge_rate': 1.0,  # C-rate
            'max_discharge_rate': 1.0,  # C-rate
            'round_trip_efficiency': 0.95,  # 95% round trip efficiency
            'self_discharge_rate': 0.02,  # 2% per month
            'depth_of_discharge_limit': 0.95,  # 95% DOD limit
            'charge_efficiency_map': {
                0.1: 0.99,
                0.5: 0.98,
                1.0: 0.97
            },
            'discharge_efficiency_map': {
                0.1: 0.99,
                0.5: 0.98,
                1.0: 0.97
            },
            'temperature_coefficient': -0.003,  # % per °C
            'min_operating_temperature': -20,  # °C
            'max_operating_temperature': 60,  # °C
            'nominal_voltage': 3.2,  # V per cell
            'number_of_cells': 1000,  # Total cells
            'energy_density': 160,  # Wh/kg
            'power_density': 350,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate LiFePO4 battery performance using physical model.
        
        Args:
            input_power: Power input (positive for charging, negative for discharging) in kW
            time_step: Time step (hours)
            operating_conditions: Operating conditions including temperature, etc.
            
        Returns:
            Performance metrics including power output, efficiency, and state of charge
        """
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0)
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # Get current SOC from internal state (initialize if not present)
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5  # 50% initial SOC
        
        soc = self._physical_state['internal_state']['soc']
        
        # Calculate effective efficiency based on power rate and temperature
        if input_power > 0:  # Charging
            # Determine charge rate (C-rate)
            charge_rate = input_power / params['nominal_capacity']
            charge_rate = min(charge_rate, params['max_charge_rate'])
            
            # Interpolate charge efficiency
            eff_points = list(params['charge_efficiency_map'].items())
            eff_points.sort()
            
            if charge_rate <= eff_points[0][0]:
                efficiency = eff_points[0][1]
            elif charge_rate >= eff_points[-1][0]:
                efficiency = eff_points[-1][1]
            else:
                # Linear interpolation
                for i in range(len(eff_points)-1):
                    if eff_points[i][0] <= charge_rate <= eff_points[i+1][0]:
                        x1, y1 = eff_points[i]
                        x2, y2 = eff_points[i+1]
                        efficiency = y1 + (y2 - y1) * (charge_rate - x1) / (x2 - x1)
                        break
        else:  # Discharging
            # Determine discharge rate (C-rate)
            discharge_rate = abs(input_power) / params['nominal_capacity']
            discharge_rate = min(discharge_rate, params['max_discharge_rate'])
            
            # Interpolate discharge efficiency
            eff_points = list(params['discharge_efficiency_map'].items())
            eff_points.sort()
            
            if discharge_rate <= eff_points[0][0]:
                efficiency = eff_points[0][1]
            elif discharge_rate >= eff_points[-1][0]:
                efficiency = eff_points[-1][1]
            else:
                # Linear interpolation
                for i in range(len(eff_points)-1):
                    if eff_points[i][0] <= discharge_rate <= eff_points[i+1][0]:
                        x1, y1 = eff_points[i]
                        x2, y2 = eff_points[i+1]
                        efficiency = y1 + (y2 - y1) * (discharge_rate - x1) / (x2 - x1)
                        break
        
        # Apply temperature correction
        temp_factor = 1 + params['temperature_coefficient'] * (ambient_temp - 25)
        efficiency *= temp_factor
        efficiency = max(0.8, min(efficiency, 1.0))  # Clamp efficiency
        
        # Calculate energy change
        if input_power > 0:  # Charging
            # Calculate energy input limited by charge rate
            max_charge_power = params['max_charge_rate'] * params['nominal_capacity']
            actual_charge_power = min(input_power, max_charge_power)
            
            # Calculate energy added to battery
            energy_in = actual_charge_power * time_step * efficiency
            
            # Calculate new SOC
            new_soc = soc + (energy_in / params['nominal_capacity'])
            new_soc = min(new_soc, params['depth_of_discharge_limit'])
            
            # Calculate actual charge efficiency
            actual_efficiency = (new_soc - soc) * params['nominal_capacity'] / (actual_charge_power * time_step)
            
            power_output = 0.0  # No power output during charging
        else:  # Discharging
            # Calculate energy output limited by discharge rate
            max_discharge_power = params['max_discharge_rate'] * params['nominal_capacity']
            actual_discharge_power = min(abs(input_power), max_discharge_power)
            
            # Calculate energy available from battery
            energy_out = actual_discharge_power * time_step
            energy_required = energy_out / efficiency
            
            # Calculate new SOC
            new_soc = soc - (energy_required / params['nominal_capacity'])
            new_soc = max(new_soc, 1 - params['depth_of_discharge_limit'])
            
            # Calculate actual energy output
            actual_energy_out = (soc - new_soc) * params['nominal_capacity'] * efficiency
            actual_discharge_power = actual_energy_out / time_step
            
            # Actual discharge efficiency
            actual_efficiency = actual_energy_out / ((soc - new_soc) * params['nominal_capacity'])
            
            power_output = -actual_discharge_power  # Negative for discharging
        
        # Apply self-discharge (over time_step)
        self_discharge_per_hour = params['self_discharge_rate'] / (30 * 24)  # Convert monthly rate to hourly
        new_soc *= (1 - self_discharge_per_hour * time_step)
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['internal_state']['charge_discharge_rate'] = charge_rate if input_power > 0 else -discharge_rate
        self._physical_state['internal_state']['temperature'] = ambient_temp
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': abs(power_output) * time_step if input_power < 0 else 0.0,
            'energy_stored': energy_in if input_power > 0 else 0.0,
            'state_of_charge': new_soc,
            'temperature': ambient_temp,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                1.0,
                {'cp': 1.1, 'density': 2600}  # LiFePO4 properties
            )
        }


class NMCBattery(ExtendedEnergyComponent):
    """Nickel Manganese Cobalt (NMC) battery physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for NMC battery."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for NMC battery."""
        return {
            'nominal_capacity': 100,  # kWh
            'max_charge_rate': 1.5,  # Higher C-rate than LiFePO4
            'max_discharge_rate': 1.5,  # Higher C-rate than LiFePO4
            'round_trip_efficiency': 0.93,  # Slightly lower than LiFePO4
            'self_discharge_rate': 0.03,  # 3% per month
            'depth_of_discharge_limit': 0.90,  # 90% DOD limit
            'charge_efficiency_map': {
                0.1: 0.98,
                0.5: 0.97,
                1.0: 0.96,
                1.5: 0.94
            },
            'discharge_efficiency_map': {
                0.1: 0.98,
                0.5: 0.97,
                1.0: 0.96,
                1.5: 0.94
            },
            'temperature_coefficient': -0.004,  # -0.4% per °C (more temperature sensitive)
            'min_operating_temperature': -10,  # °C (higher minimum temp)
            'max_operating_temperature': 55,  # °C (lower maximum temp)
            'nominal_voltage': 3.7,  # V per cell
            'number_of_cells': 1000,  # Total cells
            'energy_density': 250,  # Wh/kg (higher energy density)
            'power_density': 400,  # W/kg (higher power density)
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate NMC battery performance."""
        # NMC battery performance calculation is similar to LiFePO4
        # but with different physical parameters
        # Reuse LiFePO4 implementation with NMC parameters
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


class LeadCarbonBattery(ExtendedEnergyComponent):
    """Lead Carbon battery physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for Lead Carbon battery."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for Lead Carbon battery."""
        return {
            'nominal_capacity': 100,  # kWh
            'max_charge_rate': 0.5,  # Lower C-rate
            'max_discharge_rate': 0.5,  # Lower C-rate
            'round_trip_efficiency': 0.85,  # Lower efficiency
            'self_discharge_rate': 0.05,  # 5% per month
            'depth_of_discharge_limit': 0.80,  # 80% DOD limit
            'charge_efficiency_map': {
                0.1: 0.95,
                0.5: 0.90
            },
            'discharge_efficiency_map': {
                0.1: 0.95,
                0.5: 0.90
            },
            'temperature_coefficient': -0.002,  # -0.2% per °C
            'min_operating_temperature': -20,  # °C
            'max_operating_temperature': 60,  # °C
            'nominal_voltage': 2.0,  # V per cell
            'number_of_cells': 2000,  # More cells for same voltage
            'energy_density': 50,  # Wh/kg (lower energy density)
            'power_density': 150,  # W/kg (lower power density)
            'cycle_life': 3000,  # Cycles
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Lead Carbon battery performance."""
        # Lead Carbon battery performance calculation is similar to Li-ion batteries
        # but with different physical parameters
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


class VanadiumRedoxFlowBattery(ExtendedEnergyComponent):
    """Vanadium Redox Flow Battery (VRFB) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for VRFB."""
        return "industrial"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for VRFB."""
        return {
            'nominal_capacity': 500,  # kWh (larger capacity for industrial use)
            'max_charge_rate': 1.0,  # C-rate
            'max_discharge_rate': 1.0,  # C-rate
            'round_trip_efficiency': 0.80,  # Lower efficiency than Li-ion
            'self_discharge_rate': 0.005,  # 0.5% per month (very low self-discharge)
            'depth_of_discharge_limit': 1.00,  # 100% DOD possible
            'charge_efficiency_map': {
                0.1: 0.90,
                0.5: 0.85,
                1.0: 0.80
            },
            'discharge_efficiency_map': {
                0.1: 0.90,
                0.5: 0.85,
                1.0: 0.80
            },
            'temperature_coefficient': -0.0025,  # -0.25% per °C
            'min_operating_temperature': 5,  # °C (higher minimum temp)
            'max_operating_temperature': 45,  # °C (lower maximum temp)
            'electrolyte_concentration': 2.0,  # Molar
            'electrolyte_flow_rate': 5.0,  # L/min
            'stack_voltage': 400,  # V
            'energy_density': 35,  # Wh/kg (low energy density)
            'power_density': 100,  # W/kg (low power density)
            'cycle_life': 10000,  # Long cycle life
            'crossover_rate': 0.01,  # 1% per 1000 cycles
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate VRFB performance."""
        # VRFB performance calculation is similar to other batteries
        # but with different physical parameters and flow dynamics
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


class SodiumSulfurBattery(ExtendedEnergyComponent):
    """Sodium Sulfur (NaS) battery physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for NaS battery."""
        return "utility"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for NaS battery."""
        return {
            'nominal_capacity': 600,  # kWh (utility scale)
            'max_charge_rate': 0.5,  # Lower C-rate
            'max_discharge_rate': 0.5,  # Lower C-rate
            'round_trip_efficiency': 0.88,  # Moderate efficiency
            'self_discharge_rate': 0.01,  # 1% per month
            'depth_of_discharge_limit': 0.90,  # 90% DOD limit
            'charge_efficiency_map': {
                0.1: 0.95,
                0.5: 0.90
            },
            'discharge_efficiency_map': {
                0.1: 0.95,
                0.5: 0.90
            },
            'operating_temperature': 350,  # °C (high operating temp)
            'temperature_coefficient': -0.001,  # -0.1% per °C
            'min_operating_temperature': 300,  # °C
            'max_operating_temperature': 380,  # °C
            'nominal_voltage': 2.07,  # V per cell
            'number_of_cells': 2400,  # Total cells
            'energy_density': 150,  # Wh/kg
            'power_density': 230,  # W/kg
            'cycle_life': 2500,  # Cycles
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate NaS battery performance."""
        # NaS battery operates at high temperatures, so add heating power requirements
        perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Add heating power requirement (simplified)
        heating_power = self.config.power_rating * 0.05  # 5% of rated power for heating
        perf['heating_power'] = heating_power
        
        return perf


class SodiumIonBattery(ExtendedEnergyComponent):
    """Sodium Ion battery physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for Sodium Ion battery."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for Sodium Ion battery."""
        return {
            'nominal_capacity': 100,  # kWh
            'max_charge_rate': 1.0,  # C-rate
            'max_discharge_rate': 1.0,  # C-rate
            'round_trip_efficiency': 0.92,  # Moderate efficiency
            'self_discharge_rate': 0.025,  # 2.5% per month
            'depth_of_discharge_limit': 0.90,  # 90% DOD limit
            'charge_efficiency_map': {
                0.1: 0.98,
                0.5: 0.96,
                1.0: 0.94
            },
            'discharge_efficiency_map': {
                0.1: 0.98,
                0.5: 0.96,
                1.0: 0.94
            },
            'temperature_coefficient': -0.003,  # -0.3% per °C
            'min_operating_temperature': -20,  # °C
            'max_operating_temperature': 60,  # °C
            'nominal_voltage': 3.0,  # V per cell
            'number_of_cells': 1100,  # Total cells
            'energy_density': 140,  # Wh/kg
            'power_density': 300,  # W/kg
            'cycle_life': 4000,  # Cycles
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Sodium Ion battery performance."""
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


class SolidStateBattery(ExtendedEnergyComponent):
    """Solid State battery physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for Solid State battery."""
        return "advanced"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for Solid State battery."""
        return {
            'nominal_capacity': 100,  # kWh
            'max_charge_rate': 2.0,  # High C-rate
            'max_discharge_rate': 2.0,  # High C-rate
            'round_trip_efficiency': 0.96,  # High efficiency
            'self_discharge_rate': 0.01,  # 1% per month (very low)
            'depth_of_discharge_limit': 0.95,  # 95% DOD limit
            'charge_efficiency_map': {
                0.1: 0.99,
                0.5: 0.98,
                1.0: 0.97,
                2.0: 0.95
            },
            'discharge_efficiency_map': {
                0.1: 0.99,
                0.5: 0.98,
                1.0: 0.97,
                2.0: 0.95
            },
            'temperature_coefficient': -0.002,  # -0.2% per °C (good temperature performance)
            'min_operating_temperature': -30,  # °C (wide operating range)
            'max_operating_temperature': 80,  # °C (wide operating range)
            'nominal_voltage': 3.5,  # V per cell
            'number_of_cells': 950,  # Total cells
            'energy_density': 300,  # Wh/kg (high energy density)
            'power_density': 500,  # W/kg (high power density)
            'cycle_life': 8000,  # Long cycle life
            'solid_electrolyte_conductivity': 1.0e-3,  # S/cm
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Solid State battery performance."""
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


class Supercapacitor(ExtendedEnergyComponent):
    """Supercapacitor physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for Supercapacitor."""
        return "power"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for Supercapacitor."""
        return {
            'nominal_capacitance': 5000,  # Farads
            'nominal_voltage': 48,  # V
            'max_charge_rate': 100.0,  # Very high C-rate
            'max_discharge_rate': 100.0,  # Very high C-rate
            'round_trip_efficiency': 0.98,  # High efficiency
            'self_discharge_rate': 0.20,  # 20% per day (high self-discharge)
            'depth_of_discharge_limit': 1.00,  # 100% DOD possible
            'charge_efficiency_map': {
                10.0: 0.99,
                50.0: 0.98,
                100.0: 0.97
            },
            'discharge_efficiency_map': {
                10.0: 0.99,
                50.0: 0.98,
                100.0: 0.97
            },
            'temperature_coefficient': -0.001,  # -0.1% per °C
            'min_operating_temperature': -40,  # °C (wide operating range)
            'max_operating_temperature': 70,  # °C (wide operating range)
            'energy_density': 10,  # Wh/kg (very low energy density)
            'power_density': 10000,  # W/kg (very high power density)
            'cycle_life': 500000,  # Extremely long cycle life
            'equivalent_series_resistance': 0.001,  # Ohms
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Supercapacitor performance."""
        # Supercapacitor has very high power density but low energy density
        # Charge/discharge dynamics are much faster than batteries
        
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        
        soc = self._physical_state['internal_state']['soc']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        # Calculate energy stored in supercapacitor
        energy_stored = 0.5 * params['nominal_capacitance'] * (params['nominal_voltage'] * soc) ** 2 / 3.6e6  # Convert to kWh
        
        if input_power > 0:  # Charging
            # Calculate charge current
            charge_current = input_power * 1000 / params['nominal_voltage']  # Convert to Amps
            
            # Calculate voltage rise
            voltage_rise = (charge_current * time_step * 3600) / params['nominal_capacitance']  # V
            new_voltage = min(params['nominal_voltage'] * soc + voltage_rise, params['nominal_voltage'])
            new_soc = new_voltage / params['nominal_voltage']
            
            # Calculate power output (none during charging)
            power_output = 0.0
            
            # Calculate efficiency considering ESR losses
            esr_losses = (charge_current ** 2) * params['equivalent_series_resistance'] * time_step / 3.6e6  # kWh
            input_energy = input_power * time_step
            actual_efficiency = (0.5 * params['nominal_capacitance'] * (new_voltage ** 2 - (params['nominal_voltage'] * soc) ** 2) / 3.6e6) / input_energy
        else:  # Discharging
            # Calculate discharge current
            discharge_current = abs(input_power) * 1000 / params['nominal_voltage']  # Convert to Amps
            
            # Calculate voltage drop
            voltage_drop = (discharge_current * time_step * 3600) / params['nominal_capacitance']  # V
            new_voltage = max(params['nominal_voltage'] * soc - voltage_drop, 0)
            new_soc = new_voltage / params['nominal_voltage']
            
            # Calculate actual power output
            output_energy = 0.5 * params['nominal_capacitance'] * ((params['nominal_voltage'] * soc) ** 2 - new_voltage ** 2) / 3.6e6  # kWh
            power_output = -output_energy / time_step
            
            # Calculate efficiency considering ESR losses
            esr_losses = (discharge_current ** 2) * params['equivalent_series_resistance'] * time_step / 3.6e6  # kWh
            actual_efficiency = output_energy / (output_energy + esr_losses)
        
        # Apply self-discharge (fast for supercapacitors)
        self_discharge_per_hour = params['self_discharge_rate'] / 24  # Convert daily rate to hourly
        new_soc *= (1 - self_discharge_per_hour * time_step)
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['internal_state']['voltage'] = new_voltage
        self._physical_state['internal_state']['temperature'] = ambient_temp
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': abs(power_output) * time_step if input_power < 0 else 0.0,
            'energy_stored': (new_soc - soc) * params['nominal_capacitance'] * params['nominal_voltage'] ** 2 / (2 * 3.6e6) if input_power > 0 else 0.0,
            'state_of_charge': new_soc,
            'temperature': ambient_temp,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                1.0,
                {'cp': 0.7, 'density': 1500}  # Supercapacitor material properties
            )
        }


class FlywheelEnergyStorage(ExtendedEnergyComponent):
    """Flywheel energy storage physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for Flywheel energy storage."""
        return "power"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for Flywheel energy storage."""
        return {
            'nominal_capacity': 10,  # kWh (small energy capacity)
            'max_charge_rate': 50.0,  # High C-rate
            'max_discharge_rate': 50.0,  # High C-rate
            'round_trip_efficiency': 0.92,  # Good efficiency
            'self_discharge_rate': 0.05,  # 5% per hour (high self-discharge)
            'depth_of_discharge_limit': 1.00,  # 100% DOD possible
            'rotor_mass': 500,  # kg
            'rotor_radius': 0.5,  # meters
            'max_rotational_speed': 30000,  # RPM
            'moment_of_inertia': 62.5,  # kg·m²
            'bearing_loss_coefficient': 0.001,  # Loss coefficient
            'drag_loss_coefficient': 0.0001,  # Drag loss coefficient
            'motor_generator_efficiency': 0.98,
            'vacuum_level': 1.0e-6,  # Torr
            'energy_density': 20,  # Wh/kg
            'power_density': 10000,  # W/kg (high power density)
            'cycle_life': 200000,  # Long cycle life
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate flywheel energy storage performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        if 'rotational_speed' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['rotational_speed'] = params['max_rotational_speed'] * 0.5
        
        soc = self._physical_state['internal_state']['soc']
        rotational_speed = self._physical_state['internal_state']['rotational_speed']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        # Calculate energy stored in flywheel
        omega = rotational_speed * 2 * math.pi / 60  # Convert to rad/s
        energy_stored = 0.5 * params['moment_of_inertia'] * omega ** 2 / 3.6e6  # Convert to kWh
        
        if input_power > 0:  # Charging
            # Calculate motor power considering efficiency
            motor_power = input_power * params['motor_generator_efficiency']
            
            # Calculate rotational speed increase
            torque = motor_power * 1000 / omega  # N·m (convert to watts first)
            angular_acceleration = torque / params['moment_of_inertia']  # rad/s²
            delta_omega = angular_acceleration * time_step * 3600  # rad/s
            new_omega = min(omega + delta_omega, params['max_rotational_speed'] * 2 * math.pi / 60)
            new_rotational_speed = new_omega * 60 / (2 * math.pi)  # Convert back to RPM
            new_soc = new_rotational_speed / params['max_rotational_speed']
            
            # Calculate power output (none during charging)
            power_output = 0.0
            
            actual_efficiency = params['motor_generator_efficiency']
        else:  # Discharging
            # Calculate generator power considering efficiency
            generator_power = abs(input_power) / params['motor_generator_efficiency']
            
            # Calculate rotational speed decrease
            torque = generator_power * 1000 / omega  # N·m (convert to watts first)
            angular_deceleration = torque / params['moment_of_inertia']  # rad/s²
            delta_omega = angular_deceleration * time_step * 3600  # rad/s
            new_omega = max(omega - delta_omega, 0)
            new_rotational_speed = new_omega * 60 / (2 * math.pi)  # Convert back to RPM
            new_soc = new_rotational_speed / params['max_rotational_speed']
            
            # Calculate actual power output
            actual_generator_power = 0.5 * params['moment_of_inertia'] * (omega ** 2 - new_omega ** 2) / (time_step * 3.6e6)  # kWh
            power_output = -actual_generator_power * params['motor_generator_efficiency']
            
            actual_efficiency = params['motor_generator_efficiency']
        
        # Apply self-discharge (bearing and drag losses)
        bearing_losses = params['bearing_loss_coefficient'] * rotational_speed ** 2 * time_step / 3.6e6  # kWh
        drag_losses = params['drag_loss_coefficient'] * rotational_speed ** 3 * time_step / 3.6e6  # kWh
        total_losses = bearing_losses + drag_losses
        
        # Calculate speed reduction from losses
        energy_after_losses = max(0.5 * params['moment_of_inertia'] * new_omega ** 2 / 3.6e6 - total_losses, 0)
        new_omega_after_losses = math.sqrt((2 * energy_after_losses * 3.6e6) / params['moment_of_inertia'])  # rad/s
        new_rotational_speed = new_omega_after_losses * 60 / (2 * math.pi)  # RPM
        new_soc = new_rotational_speed / params['max_rotational_speed']
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['internal_state']['rotational_speed'] = new_rotational_speed
        self._physical_state['internal_state']['temperature'] = ambient_temp
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': abs(power_output) * time_step if input_power < 0 else 0.0,
            'energy_stored': (new_soc - soc) * params['nominal_capacity'] if input_power > 0 else 0.0,
            'state_of_charge': new_soc,
            'temperature': ambient_temp,
            'pressure': params['vacuum_level'] * 133.322 / 101325,  # Convert Torr to bar
            'flow_rate': 0.0,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                params['vacuum_level'] * 133.322 / 101325,
                {'cp': 0.46, 'density': 7870}  # Steel properties
            )
        }


# =============================================================================
# Other Storage Systems
# =============================================================================

class TraditionalCompressedAirStorage(ExtendedEnergyComponent):
    """Traditional Compressed Air Energy Storage (CAES) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for traditional CAES."""
        return "utility"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for traditional CAES."""
        return {
            'nominal_capacity': 10000,  # kWh (utility scale)
            'max_charge_rate': 0.2,  # Slow C-rate
            'max_discharge_rate': 0.2,  # Slow C-rate
            'round_trip_efficiency': 0.45,  # Low efficiency
            'storage_pressure_min': 40,  # bar
            'storage_pressure_max': 100,  # bar
            'storage_volume': 50000,  # m³
            'compressor_efficiency': 0.85,
            'turbine_efficiency': 0.88,
            'heat_rate': 2500,  # kJ/kWh (fuel required for heating)
            'air_density': 1.225,  # kg/m³
            'specific_heat_ratio': 1.4,
            'gas_constant': 287,  # J/(kg·K)
            'ambient_temperature': 25,  # °C
            'energy_density': 10,  # Wh/kg
            'power_density': 500,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate traditional CAES performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        if 'pressure' not in self._physical_state:
            self._physical_state['pressure'] = params['storage_pressure_min'] + (params['storage_pressure_max'] - params['storage_pressure_min']) * 0.5
        
        soc = self._physical_state['internal_state']['soc']
        current_pressure = self._physical_state['pressure']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        if input_power > 0:  # Charging (compressing air)
            # Calculate mass of air in storage
            air_mass = (current_pressure * 1e5 * params['storage_volume']) / (params['gas_constant'] * (ambient_temp + 273.15))  # kg
            
            # Calculate compressor work
            compression_ratio = (params['storage_pressure_max'] / current_pressure) ** ((params['specific_heat_ratio'] - 1) / params['specific_heat_ratio'])
            compressor_work = (params['specific_heat_ratio'] / (params['specific_heat_ratio'] - 1)) * params['gas_constant'] * (ambient_temp + 273.15) * air_mass * (compression_ratio - 1) / 3.6e6  # kWh
            
            # Calculate required power
            required_power = compressor_work / (time_step * params['compressor_efficiency'])
            actual_power = min(input_power, required_power)
            
            # Calculate pressure increase
            new_pressure = current_pressure + (actual_power * time_step * params['compressor_efficiency'] * 3.6e6) / (
                (params['specific_heat_ratio'] / (params['specific_heat_ratio'] - 1)) * params['gas_constant'] * (ambient_temp + 273.15) * air_mass
            )
            new_pressure = min(new_pressure, params['storage_pressure_max'])
            new_soc = (new_pressure - params['storage_pressure_min']) / (params['storage_pressure_max'] - params['storage_pressure_min'])
            
            # Power output (none during charging)
            power_output = 0.0
            
            actual_efficiency = params['compressor_efficiency']
        else:  # Discharging (expanding air through turbine)
            # Calculate mass of air in storage
            air_mass = (current_pressure * 1e5 * params['storage_volume']) / (params['gas_constant'] * (ambient_temp + 273.15))  # kg
            
            # Calculate turbine work
            expansion_ratio = (current_pressure / params['storage_pressure_min']) ** ((params['specific_heat_ratio'] - 1) / params['specific_heat_ratio'])
            turbine_work = (params['specific_heat_ratio'] / (params['specific_heat_ratio'] - 1)) * params['gas_constant'] * (ambient_temp + 273.15) * air_mass * (1 - 1 / expansion_ratio) / 3.6e6  # kWh
            
            # Calculate available power
            available_power = turbine_work * params['turbine_efficiency'] / time_step
            actual_power = min(abs(input_power), available_power)
            
            # Calculate pressure decrease
            new_pressure = current_pressure - (actual_power * time_step / params['turbine_efficiency'] * 3.6e6) / (
                (params['specific_heat_ratio'] / (params['specific_heat_ratio'] - 1)) * params['gas_constant'] * (ambient_temp + 273.15) * air_mass
            )
            new_pressure = max(new_pressure, params['storage_pressure_min'])
            new_soc = (new_pressure - params['storage_pressure_min']) / (params['storage_pressure_max'] - params['storage_pressure_min'])
            
            # Power output
            power_output = -actual_power
            
            actual_efficiency = params['turbine_efficiency']
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['pressure'] = new_pressure
        self._physical_state['internal_state']['temperature'] = ambient_temp
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': abs(power_output) * time_step if input_power < 0 else 0.0,
            'energy_stored': (new_soc - soc) * params['nominal_capacity'] if input_power > 0 else 0.0,
            'state_of_charge': new_soc,
            'temperature': ambient_temp,
            'pressure': new_pressure,
            'flow_rate': 0.0,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                new_pressure,
                {'cp': 1.005, 'density': params['air_density'] * (new_pressure / 1.01325) * (298.15 / (ambient_temp + 273.15))}  # Air properties at pressure
            )
        }


class AdiabaticCompressedAirStorage(ExtendedEnergyComponent):
    """Adiabatic Compressed Air Energy Storage (A-CAES) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for A-CAES."""
        return "utility"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for A-CAES."""
        return {
            'nominal_capacity': 10000,  # kWh (utility scale)
            'max_charge_rate': 0.2,  # Slow C-rate
            'max_discharge_rate': 0.2,  # Slow C-rate
            'round_trip_efficiency': 0.65,  # Higher efficiency than traditional CAES
            'storage_pressure_min': 40,  # bar
            'storage_pressure_max': 100,  # bar
            'storage_volume': 50000,  # m³
            'compressor_efficiency': 0.85,
            'turbine_efficiency': 0.88,
            'heat_storage_efficiency': 0.90,
            'heat_exchanger_efficiency': 0.92,
            'thermal_storage_capacity': 25000,  # kWh
            'air_density': 1.225,  # kg/m³
            'specific_heat_ratio': 1.4,
            'gas_constant': 287,  # J/(kg·K)
            'ambient_temperature': 25,  # °C
            'energy_density': 12,  # Wh/kg
            'power_density': 600,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate A-CAES performance."""
        # A-CAES uses thermal storage instead of fuel for heating
        # Similar to traditional CAES but with heat recovery
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


class LargePumpedHydroStorage(ExtendedEnergyComponent):
    """Large Pumped Hydro Energy Storage (PHES) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for large PHES."""
        return "utility"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for large PHES."""
        return {
            'nominal_capacity': 100000,  # kWh (large utility scale)
            'max_charge_rate': 0.1,  # Very slow C-rate
            'max_discharge_rate': 0.1,  # Very slow C-rate
            'round_trip_efficiency': 0.80,  # Good efficiency
            'head_min': 100,  # meters
            'head_max': 150,  # meters
            'upper_reservoir_capacity': 1000000,  # m³
            'lower_reservoir_capacity': 1000000,  # m³
            'pump_efficiency': 0.90,
            'turbine_efficiency': 0.92,
            'water_density': 1000,  # kg/m³
            'gravity': 9.81,  # m/s²
            'energy_density': 0.5,  # Wh/kg (very low energy density)
            'power_density': 100,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate large PHES performance."""
        params = self.config.physical_parameters
        
        # Get current SOC from internal state
        if 'soc' not in self._physical_state['internal_state']:
            self._physical_state['internal_state']['soc'] = 0.5
        
        soc = self._physical_state['internal_state']['soc']
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0) if operating_conditions else 25.0
        
        # Calculate effective head based on SOC
        head = params['head_min'] + (params['head_max'] - params['head_min']) * soc
        
        if input_power > 0:  # Pumping (charging)
            # Calculate pump flow rate
            pump_power = input_power * params['pump_efficiency']
            flow_rate = (pump_power * 1000) / (params['water_density'] * params['gravity'] * head)  # m³/s
            
            # Calculate volume pumped
            volume_pumped = flow_rate * time_step * 3600  # m³
            
            # Calculate SOC increase
            volume_change = volume_pumped / params['upper_reservoir_capacity']
            new_soc = min(soc + volume_change, 1.0)
            
            # Power output (none during pumping)
            power_output = 0.0
            
            actual_efficiency = params['pump_efficiency']
        else:  # Generating (discharging)
            # Calculate turbine flow rate
            turbine_power = abs(input_power) / params['turbine_efficiency']
            flow_rate = (turbine_power * 1000) / (params['water_density'] * params['gravity'] * head)  # m³/s
            
            # Calculate volume discharged
            volume_discharged = flow_rate * time_step * 3600  # m³
            
            # Calculate SOC decrease
            volume_change = volume_discharged / params['upper_reservoir_capacity']
            new_soc = max(soc - volume_change, 0.0)
            
            # Calculate actual power output
            actual_turbine_power = (params['water_density'] * params['gravity'] * head * flow_rate * params['turbine_efficiency']) / 1000  # kW
            power_output = -actual_turbine_power
            
            actual_efficiency = params['turbine_efficiency']
        
        # Update internal state
        self._physical_state['internal_state']['soc'] = new_soc
        self._physical_state['internal_state']['head'] = params['head_min'] + (params['head_max'] - params['head_min']) * new_soc
        self._physical_state['internal_state']['temperature'] = ambient_temp
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': abs(power_output) * time_step if input_power < 0 else 0.0,
            'energy_stored': (new_soc - soc) * params['nominal_capacity'] if input_power > 0 else 0.0,
            'state_of_charge': new_soc,
            'temperature': ambient_temp,
            'pressure': 1.0,  # Atmospheric pressure
            'flow_rate': flow_rate if 'flow_rate' in locals() else 0.0,
            'internal_state': self._physical_state['internal_state'].copy(),
            'thermodynamic_state': calculate_thermodynamic_state(
                ambient_temp,
                1.0,
                {'cp': 4.18, 'density': params['water_density']}  # Water properties
            )
        }


class SmallModularPumpedHydroStorage(ExtendedEnergyComponent):
    """Small Modular Pumped Hydro Energy Storage (SM-PHES) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for SM-PHES."""
        return "distributed"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for SM-PHES."""
        return {
            'nominal_capacity': 1000,  # kWh (small scale)
            'max_charge_rate': 0.5,  # Faster C-rate than large PHES
            'max_discharge_rate': 0.5,  # Faster C-rate than large PHES
            'round_trip_efficiency': 0.75,  # Slightly lower efficiency than large PHES
            'head_min': 20,  # meters (lower head)
            'head_max': 50,  # meters (lower head)
            'upper_reservoir_capacity': 10000,  # m³
            'lower_reservoir_capacity': 10000,  # m³
            'pump_efficiency': 0.85,
            'turbine_efficiency': 0.88,
            'water_density': 1000,  # kg/m³
            'gravity': 9.81,  # m/s²
            'energy_density': 0.5,  # Wh/kg
            'power_density': 200,  # W/kg
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate SM-PHES performance."""
        # Small modular PHES has similar physics to large PHES
        # but with smaller capacity and different parameters
        return super().calculate_physical_performance(input_power, time_step, operating_conditions)


# =============================================================================
# Factory Registration
# =============================================================================

# Register all electrochemical storage component factories
register_component_factory(
    ExtendedEquipmentType.LITHIUM_IRON_PHOSPHATE_BATTERY,
    LithiumIronPhosphateBattery
)

register_component_factory(
    ExtendedEquipmentType.NMC_BATTERY,
    NMCBattery
)

register_component_factory(
    ExtendedEquipmentType.LEAD_CARBON_BATTERY,
    LeadCarbonBattery
)

register_component_factory(
    ExtendedEquipmentType.VANADIUM_REDOX_FLOW_BATTERY,
    VanadiumRedoxFlowBattery
)

register_component_factory(
    ExtendedEquipmentType.SODIUM_SULFUR_BATTERY,
    SodiumSulfurBattery
)

register_component_factory(
    ExtendedEquipmentType.SODIUM_ION_BATTERY,
    SodiumIonBattery
)

register_component_factory(
    ExtendedEquipmentType.SOLID_STATE_BATTERY,
    SolidStateBattery
)

register_component_factory(
    ExtendedEquipmentType.SUPERCAPACITOR,
    Supercapacitor
)

register_component_factory(
    ExtendedEquipmentType.FLYWHEEL_ENERGY_STORAGE,
    FlywheelEnergyStorage
)

register_component_factory(
    ExtendedEquipmentType.TRADITIONAL_COMPRESSED_AIR_STORAGE,
    TraditionalCompressedAirStorage
)

register_component_factory(
    ExtendedEquipmentType.ADIABATIC_COMPRESSED_AIR_STORAGE,
    AdiabaticCompressedAirStorage
)

register_component_factory(
    ExtendedEquipmentType.LARGE_PUMPED_HYDRO_STORAGE,
    LargePumpedHydroStorage
)

register_component_factory(
    ExtendedEquipmentType.SMALL_MODULAR_PUMPED_HYDRO_STORAGE,
    SmallModularPumpedHydroStorage
)
