"""Renewable energy component implementations.

This module provides physical modeling for renewable energy generation components,
including photovoltaic systems, wind turbines, hydroelectric generators,
and other renewable energy technologies.
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
    calculate_carnot_efficiency,
    calculate_exergy
)
from pyxesxxn.equipment_library.base import (
    EnergyCarrier as PyXESXXNEnergyCarrier,
    EquipmentType as PyXESXXNEquipmentType,
    EquipmentCategory as PyXESXXNEquipmentCategory
)


# =============================================================================
# Photovoltaic Systems
# =============================================================================

class FixedTiltPVSystem(ExtendedEnergyComponent):
    """Fixed tilt photovoltaic system physical model."""
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[ExtendedEquipmentConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize a fixed tilt PV system."""
        super().__init__(equipment_id=equipment_id, config=config, location=location, **kwargs)
    
    def get_default_scenario(self) -> str:
        """Get default scenario for PV system."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for fixed tilt PV system."""
        return {
            'module_area': 1.6,  # m² per module
            'module_efficiency': 0.20,  # 20% efficiency
            'tilt_angle': 30,  # degrees
            'azimuth_angle': 180,  # degrees (south-facing)
            'temperature_coefficient': -0.004,  # % per °C
            'nominal_operating_cell_temperature': 45,  # °C
            'wind_cooling_factor': 0.025,  # °C per m/s
            'ground_reflectance': 0.25,  # albedo
            'max_power_output': 350,  # W per module
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate PV system performance using physical model.
        
        Args:
            input_power: Solar irradiance (W/m²)
            time_step: Time step (hours)
            operating_conditions: Operating conditions including temperature, wind speed, etc.
            
        Returns:
            Performance metrics including power output, efficiency, and physical state
        """
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0)
        wind_speed = operating_conditions.get('wind_speed', 3.0)
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # Calculate module temperature using NOCT model
        delta_temp = (params['nominal_operating_cell_temperature'] - 20) / 800
        cell_temp = ambient_temp + (input_power * delta_temp) * (1 - params['module_efficiency']) / (1 + params['wind_cooling_factor'] * wind_speed)
        
        # Temperature derating factor
        temp_factor = 1 + params['temperature_coefficient'] * (cell_temp - 25)
        
        # Calculate power output per module
        module_power = input_power * params['module_area'] * params['module_efficiency'] * temp_factor
        
        # Calculate number of modules from power rating
        num_modules = self.config.power_rating * 1000 / params['max_power_output']  # Convert kW to W
        
        # Total power output in kW
        power_output = (module_power * num_modules) / 1000
        
        # Calculate actual efficiency
        actual_efficiency = (power_output * 1000) / (input_power * params['module_area'] * num_modules)
        
        # Update physical state
        physical_state = {
            'temperature': cell_temp,
            'pressure': 1.0,  # Atmospheric pressure
            'flow_rate': 0.0,  # No fluid flow
            'internal_state': {
                'cell_temperature': cell_temp,
                'ambient_temperature': ambient_temp,
                'wind_speed': wind_speed,
                'solar_irradiance': input_power,
                'temperature_factor': temp_factor
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                cell_temp,
                1.0,
                {'cp': 0.83, 'density': 2.32e-3}  # Silicon specific heat and density
            )
        }
        
        return {
            'power_output': max(0.0, power_output),
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'cell_temperature': cell_temp,
            'ambient_temperature': ambient_temp,
            'temperature_factor': temp_factor,
            **physical_state
        }


class SingleAxisTrackingPVSystem(FixedTiltPVSystem):
    """Single-axis tracking photovoltaic system physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for single-axis tracking PV system."""
        params = super()._get_default_physical_parameters()
        params.update({
            'tracking_accuracy': 0.98,  # 98% tracking accuracy
            'backtracking_efficiency': 0.99,  # Backtracking efficiency
            'max_tracking_angle': 80,  # degrees
            'tracking_speed': 5.0,  # degrees per minute
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate single-axis tracking PV system performance."""
        # Get fixed tilt performance
        fixed_perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Add tracking gain
        tracking_gain = 1.25  # Typical gain for single-axis tracking
        
        # Update power output and efficiency
        fixed_perf['power_output'] *= tracking_gain
        fixed_perf['efficiency'] *= tracking_gain
        fixed_perf['energy_produced'] *= tracking_gain
        
        # Update internal state with tracking information
        fixed_perf['internal_state'].update({
            'tracking_gain': tracking_gain,
            'tracking_type': 'single_axis'
        })
        
        return fixed_perf


class DualAxisTrackingPVSystem(FixedTiltPVSystem):
    """Dual-axis tracking photovoltaic system physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for dual-axis tracking PV system."""
        params = super()._get_default_physical_parameters()
        params.update({
            'tracking_accuracy': 0.99,  # 99% tracking accuracy
            'max_azimuth_angle': 360,  # degrees
            'max_elevation_angle': 90,  # degrees
            'tracking_speed': 10.0,  # degrees per minute
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate dual-axis tracking PV system performance."""
        # Get fixed tilt performance
        fixed_perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Add tracking gain
        tracking_gain = 1.4  # Typical gain for dual-axis tracking
        
        # Update power output and efficiency
        fixed_perf['power_output'] *= tracking_gain
        fixed_perf['efficiency'] *= tracking_gain
        fixed_perf['energy_produced'] *= tracking_gain
        
        # Update internal state with tracking information
        fixed_perf['internal_state'].update({
            'tracking_gain': tracking_gain,
            'tracking_type': 'dual_axis'
        })
        
        return fixed_perf


class DistributedRoofPV(FixedTiltPVSystem):
    """Distributed rooftop photovoltaic system physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for distributed rooftop PV system."""
        params = super()._get_default_physical_parameters()
        params.update({
            'roof_tilt': 20,  # degrees (typical for rooftops)
            'roof_orientation': 180,  # degrees (south-facing)
            'shading_factor': 0.95,  # 5% shading loss
            'system_losses': 0.15,  # 15% system losses
            'module_spacing': 0.5,  # meters
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate distributed rooftop PV system performance."""
        # Get fixed tilt performance
        perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Apply rooftop-specific losses
        perf['power_output'] *= self.config.physical_parameters['shading_factor']
        perf['power_output'] *= (1 - self.config.physical_parameters['system_losses'])
        
        perf['efficiency'] *= self.config.physical_parameters['shading_factor']
        perf['efficiency'] *= (1 - self.config.physical_parameters['system_losses'])
        
        perf['energy_produced'] *= self.config.physical_parameters['shading_factor']
        perf['energy_produced'] *= (1 - self.config.physical_parameters['system_losses'])
        
        return perf


class ConcentratedSolarPowerPlant(FixedTiltPVSystem):
    """Concentrated Solar Power (CSP) plant physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for CSP plant."""
        return {
            'concentration_ratio': 500,  # Solar concentration ratio
            'receiver_efficiency': 0.85,  # Receiver efficiency
            'thermal_storage_capacity': 12.0,  # hours of storage
            'thermal_to_electric_efficiency': 0.35,  # ORC efficiency
            'max_steam_temperature': 550,  # °C
            'min_steam_temperature': 200,  # °C
            'working_fluid': 'synthetic_oil',
            'heat_loss_factor': 0.05,  # 5% heat loss
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate CSP plant performance using physical model."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0)
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # Calculate concentrated solar power
        concentrated_power = input_power * params['concentration_ratio'] * params['receiver_efficiency']
        
        # Apply heat losses
        thermal_power = concentrated_power * (1 - params['heat_loss_factor'])
        
        # Calculate cell temperature (simplified)
        cell_temp = ambient_temp + (thermal_power / 10000)  # Simplified temperature rise
        
        # Calculate electric power output
        electric_power = thermal_power * params['thermal_to_electric_efficiency'] / 1000  # Convert to kW
        
        # Actual efficiency
        actual_efficiency = params['receiver_efficiency'] * params['thermal_to_electric_efficiency']
        
        return {
            'power_output': max(0.0, electric_power),
            'efficiency': actual_efficiency,
            'energy_produced': electric_power * time_step,
            'temperature': cell_temp,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {
                'concentrated_power': concentrated_power,
                'thermal_power': thermal_power,
                'ambient_temperature': ambient_temp,
                'concentration_ratio': params['concentration_ratio']
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                cell_temp,
                1.0,
                {'cp': 2.0, 'density': 850.0}  # Synthetic oil properties
            )
        }


# =============================================================================
# Wind Energy Systems
# =============================================================================

class FixedSpeedWindTurbine(ExtendedEnergyComponent):
    """Fixed speed wind turbine physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for wind turbine."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for fixed speed wind turbine."""
        return {
            'rotor_diameter': 80.0,  # meters
            'cut_in_wind_speed': 3.0,  # m/s
            'rated_wind_speed': 12.0,  # m/s
            'cut_out_wind_speed': 25.0,  # m/s
            'air_density': 1.225,  # kg/m³
            'power_coefficient': 0.45,  # Cp
            'generator_efficiency': 0.95,
            'gearbox_efficiency': 0.98,
            'rated_power': 2000,  # kW
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate wind turbine performance using Betz limit and power curve model.
        
        Args:
            input_power: Wind speed (m/s)
            time_step: Time step (hours)
            operating_conditions: Operating conditions including air density, temperature, etc.
            
        Returns:
            Performance metrics including power output, efficiency, and physical state
        """
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        air_density = operating_conditions.get('air_density', self.config.physical_parameters['air_density'])
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        wind_speed = input_power
        rotor_area = math.pi * (params['rotor_diameter'] / 2) ** 2
        
        # Calculate power output based on wind speed
        if wind_speed < params['cut_in_wind_speed'] or wind_speed > params['cut_out_wind_speed']:
            power_output = 0.0
        elif wind_speed <= params['rated_wind_speed']:
            # Below rated speed: cubic power relationship
            power_coefficient = params['power_coefficient']
            # Apply Betz limit (0.593 is theoretical maximum)
            power_coefficient = min(power_coefficient, 0.593)
            
            # Calculate aerodynamic power
            aerodynamic_power = 0.5 * air_density * rotor_area * wind_speed ** 3 / 1000  # Convert to kW
            
            # Apply efficiencies
            power_output = aerodynamic_power * power_coefficient * params['gearbox_efficiency'] * params['generator_efficiency']
        else:
            # Above rated speed: constant power output
            power_output = params['rated_power']
        
        # Calculate actual efficiency
        if wind_speed > 0:
            actual_efficiency = (power_output * 1000) / (0.5 * air_density * rotor_area * wind_speed ** 3) if wind_speed > 0 else 0.0
        else:
            actual_efficiency = 0.0
        
        # Calculate rotor speed (fixed speed)
        rotor_speed = 15.0  # RPM (fixed speed turbine)
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 45.0,  # Simplified temperature
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {
                'wind_speed': wind_speed,
                'air_density': air_density,
                'rotor_speed': rotor_speed,
                'rotor_power': 0.5 * air_density * rotor_area * wind_speed ** 3 if wind_speed > 0 else 0.0
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                45.0,
                1.0,
                {'cp': 1.005, 'density': air_density}
            )
        }


class VariableSpeedDFIGWindTurbine(FixedSpeedWindTurbine):
    """Variable Speed Doubly-Fed Induction Generator (DFIG) wind turbine physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for DFIG wind turbine."""
        params = super()._get_default_physical_parameters()
        params.update({
            'max_power_coefficient': 0.50,  # Higher Cp for variable speed
            'variable_speed_range': (6.0, 18.0),  # RPM range
            'converter_efficiency': 0.99,
            'dfig_efficiency': 0.96,
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate DFIG wind turbine performance using physical model."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        air_density = operating_conditions.get('air_density', self.config.physical_parameters['air_density'])
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        wind_speed = input_power
        rotor_area = math.pi * (params['rotor_diameter'] / 2) ** 2
        
        # Calculate power output based on wind speed
        if wind_speed < params['cut_in_wind_speed'] or wind_speed > params['cut_out_wind_speed']:
            power_output = 0.0
            rotor_speed = 0.0
        elif wind_speed <= params['rated_wind_speed']:
            # Below rated speed: optimize power coefficient
            # Power coefficient as function of tip-speed ratio
            tip_speed_ratio = (params['rotor_diameter'] / 2) * (2 * math.pi * params['variable_speed_range'][0] / 60) / wind_speed
            
            # Simplified Cp curve based on tip-speed ratio
            power_coefficient = params['max_power_coefficient'] * (1 - 0.05 * abs(tip_speed_ratio - 8))
            power_coefficient = max(0, min(power_coefficient, 0.593))  # Apply Betz limit
            
            # Calculate aerodynamic power
            aerodynamic_power = 0.5 * air_density * rotor_area * wind_speed ** 3 / 1000  # Convert to kW
            
            # Apply efficiencies
            power_output = aerodynamic_power * power_coefficient * params['gearbox_efficiency'] * params['dfig_efficiency'] * params['converter_efficiency']
            
            # Variable rotor speed (proportional to wind speed)
            rotor_speed = 6.0 + (wind_speed - params['cut_in_wind_speed']) * 1.2  # Simplified speed control
        else:
            # Above rated speed: constant power, variable rotor speed
            power_output = params['rated_power']
            rotor_speed = params['variable_speed_range'][1]
        
        # Calculate actual efficiency
        if wind_speed > 0:
            actual_efficiency = (power_output * 1000) / (0.5 * air_density * rotor_area * wind_speed ** 3) if wind_speed > 0 else 0.0
        else:
            actual_efficiency = 0.0
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 40.0,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {
                'wind_speed': wind_speed,
                'air_density': air_density,
                'rotor_speed': rotor_speed,
                'power_coefficient': power_coefficient if wind_speed > params['cut_in_wind_speed'] else 0.0
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                40.0,
                1.0,
                {'cp': 1.005, 'density': air_density}
            )
        }


class OffshoreDirectDriveWindTurbine(VariableSpeedDFIGWindTurbine):
    """Offshore Direct Drive wind turbine physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for offshore direct drive wind turbine."""
        params = super()._get_default_physical_parameters()
        params.update({
            'rotor_diameter': 164.0,  # Larger rotor for offshore
            'rated_power': 10000,  # 10 MW offshore turbine
            'cut_in_wind_speed': 3.5,  # Higher cut-in for offshore
            'rated_wind_speed': 11.5,  # Lower rated speed for offshore
            'cut_out_wind_speed': 28.0,  # Higher cut-out for offshore
            'direct_drive_efficiency': 0.97,  # No gearbox losses
            'offshore_wind_factor': 1.15,  # Higher wind resource offshore
            'foundation_loss_factor': 0.02,  # 2% loss from foundation
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate offshore direct drive wind turbine performance."""
        # Get DFIG performance
        perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Apply offshore wind factor and foundation losses
        perf['power_output'] *= self.config.physical_parameters['offshore_wind_factor']
        perf['power_output'] *= (1 - self.config.physical_parameters['foundation_loss_factor'])
        
        # Update efficiency accordingly
        perf['efficiency'] *= self.config.physical_parameters['offshore_wind_factor']
        perf['efficiency'] *= (1 - self.config.physical_parameters['foundation_loss_factor'])
        
        perf['energy_produced'] = perf['power_output'] * time_step
        
        return perf


class SmallVerticalAxisWindTurbine(FixedSpeedWindTurbine):
    """Small Vertical Axis Wind Turbine (VAWT) physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for small VAWT."""
        return {
            'rotor_height': 3.0,  # meters
            'rotor_diameter': 2.0,  # meters
            'cut_in_wind_speed': 2.5,  # m/s
            'rated_wind_speed': 12.0,  # m/s
            'cut_out_wind_speed': 20.0,  # m/s
            'air_density': 1.225,  # kg/m³
            'power_coefficient': 0.35,  # Lower Cp for VAWT
            'generator_efficiency': 0.90,
            'rated_power': 1.5,  # kW
            'urban_environment_factor': 0.85,  # Lower efficiency in turbulent urban environments
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate small VAWT performance using physical model."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        air_density = operating_conditions.get('air_density', self.config.physical_parameters['air_density'])
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        wind_speed = input_power
        rotor_area = params['rotor_height'] * params['rotor_diameter']  # Area for VAWT
        
        # Calculate power output based on wind speed
        if wind_speed < params['cut_in_wind_speed'] or wind_speed > params['cut_out_wind_speed']:
            power_output = 0.0
        elif wind_speed <= params['rated_wind_speed']:
            # Below rated speed: cubic power relationship
            power_coefficient = params['power_coefficient']
            
            # Calculate aerodynamic power
            aerodynamic_power = 0.5 * air_density * rotor_area * wind_speed ** 3 / 1000  # Convert to kW
            
            # Apply efficiencies and urban environment factor
            power_output = aerodynamic_power * power_coefficient * params['generator_efficiency'] * params['urban_environment_factor']
        else:
            # Above rated speed: constant power output
            power_output = params['rated_power']
        
        # Calculate actual efficiency
        if wind_speed > 0:
            actual_efficiency = (power_output * 1000) / (0.5 * air_density * rotor_area * wind_speed ** 3) if wind_speed > 0 else 0.0
        else:
            actual_efficiency = 0.0
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 35.0,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {
                'wind_speed': wind_speed,
                'air_density': air_density,
                'urban_environment_factor': params['urban_environment_factor']
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                35.0,
                1.0,
                {'cp': 1.005, 'density': air_density}
            )
        }


# =============================================================================
# Other Renewable Energy Systems
# =============================================================================

class TidalPowerGenerator(ExtendedEnergyComponent):
    """Tidal power generator physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for tidal power generator."""
        return "coastal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for tidal power generator."""
        return {
            'turbine_diameter': 10.0,  # meters
            'turbine_efficiency': 0.80,  # Water turbine efficiency
            'generator_efficiency': 0.95,
            'cut_in_current_speed': 1.0,  # m/s
            'rated_current_speed': 3.0,  # m/s
            'cut_out_current_speed': 5.0,  # m/s
            'water_density': 1025.0,  # kg/m³
            'rated_power': 1000,  # kW
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate tidal power generator performance."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        current_speed = input_power
        rotor_area = math.pi * (params['turbine_diameter'] / 2) ** 2
        
        # Calculate power output based on current speed
        if current_speed < params['cut_in_current_speed'] or current_speed > params['cut_out_current_speed']:
            power_output = 0.0
        elif current_speed <= params['rated_current_speed']:
            # Below rated speed: cubic power relationship
            # Calculate hydrodynamic power
            hydrodynamic_power = 0.5 * params['water_density'] * rotor_area * current_speed ** 3 / 1000  # Convert to kW
            
            # Apply efficiencies
            power_output = hydrodynamic_power * params['turbine_efficiency'] * params['generator_efficiency']
        else:
            # Above rated speed: constant power output
            power_output = params['rated_power']
        
        # Calculate actual efficiency
        if current_speed > 0:
            actual_efficiency = (power_output * 1000) / (0.5 * params['water_density'] * rotor_area * current_speed ** 3) if current_speed > 0 else 0.0
        else:
            actual_efficiency = 0.0
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 15.0,  # Water temperature
            'pressure': 1.0,  # Atmospheric pressure
            'flow_rate': current_speed * rotor_area,  # m³/s
            'internal_state': {
                'current_speed': current_speed,
                'water_density': params['water_density'],
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                15.0,
                1.0,
                {'cp': 4.18, 'density': params['water_density']}
            )
        }


class WaveEnergyConverter(ExtendedEnergyComponent):
    """Wave Energy Converter (WEC) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for wave energy converter."""
        return "coastal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for WEC."""
        return {
            'wave_absorber_area': 25.0,  # m²
            'absorption_efficiency': 0.75,  # Wave energy absorption efficiency
            'power_takeoff_efficiency': 0.85,  # PTO efficiency
            'cut_in_wave_height': 0.5,  # meters
            'rated_wave_height': 3.0,  # meters
            'cut_out_wave_height': 8.0,  # meters
            'wave_period': 8.0,  # seconds
            'water_density': 1025.0,  # kg/m³
            'rated_power': 500,  # kW
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate WEC performance using physical model."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        wave_period = operating_conditions.get('wave_period', self.config.physical_parameters['wave_period'])
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        wave_height = input_power  # input_power represents wave height in meters
        
        # Calculate wave power per unit length (W/m)
        wave_power_density = 0.5 * params['water_density'] * 9.81 * wave_height ** 2 * wave_period / (8 * math.pi)
        
        # Calculate total wave power
        total_wave_power = wave_power_density * params['wave_absorber_area'] ** 0.5  # Simplified
        
        # Calculate power output based on wave height
        if wave_height < params['cut_in_wave_height'] or wave_height > params['cut_out_wave_height']:
            power_output = 0.0
        elif wave_height <= params['rated_wave_height']:
            # Below rated height: linear relationship
            power_output = (total_wave_power * params['absorption_efficiency'] * params['power_takeoff_efficiency']) / 1000  # Convert to kW
        else:
            # Above rated height: constant power
            power_output = params['rated_power']
        
        # Calculate actual efficiency
        actual_efficiency = params['absorption_efficiency'] * params['power_takeoff_efficiency']
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 15.0,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {
                'wave_height': wave_height,
                'wave_period': wave_period,
                'wave_power_density': wave_power_density
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                15.0,
                1.0,
                {'cp': 4.18, 'density': params['water_density']}
            )
        }


class RunOfRiverHydroGenerator(ExtendedEnergyComponent):
    """Run-of-river hydroelectric generator physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for run-of-river hydro generator."""
        return "rural"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for run-of-river hydro generator."""
        return {
            'head': 20.0,  # meters of water head
            'flow_rate': 5.0,  # m³/s
            'turbine_efficiency': 0.85,  # Francis turbine efficiency
            'generator_efficiency': 0.95,
            'penstock_loss_factor': 0.05,  # 5% head loss in penstock
            'rated_power': 500,  # kW
            'water_density': 1000.0,  # kg/m³
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate run-of-river hydro generator performance."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # input_power represents flow rate in m³/s
        actual_flow_rate = input_power
        
        # Calculate effective head (after losses)
        effective_head = params['head'] * (1 - params['penstock_loss_factor'])
        
        # Calculate hydraulic power
        hydraulic_power = params['water_density'] * 9.81 * effective_head * actual_flow_rate / 1000  # Convert to kW
        
        # Calculate electric power output
        power_output = hydraulic_power * params['turbine_efficiency'] * params['generator_efficiency']
        
        # Calculate actual efficiency
        actual_efficiency = params['turbine_efficiency'] * params['generator_efficiency']
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 20.0,
            'pressure': 1.0 + (params['head'] * 0.0981),  # Pressure from water head
            'flow_rate': actual_flow_rate,
            'internal_state': {
                'flow_rate': actual_flow_rate,
                'effective_head': effective_head,
                'hydraulic_power': hydraulic_power
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                20.0,
                1.0 + (params['head'] * 0.0981),
                {'cp': 4.18, 'density': params['water_density']}
            )
        }


class ReservoirHydroGenerator(RunOfRiverHydroGenerator):
    """Reservoir hydroelectric generator physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for reservoir hydro generator."""
        params = super()._get_default_physical_parameters()
        params.update({
            'reservoir_capacity': 1000000,  # m³
            'max_head': 100.0,  # meters
            'min_head': 50.0,  # meters
            'rated_power': 10000,  # 10 MW
            'turbine_type': 'francis',
            'pump_efficiency': 0.88,  # For pumped storage operation
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate reservoir hydro generator performance."""
        # Get run-of-river performance
        perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Apply reservoir-specific adjustments
        perf['power_output'] *= 20  # Larger capacity for reservoir
        perf['energy_produced'] = perf['power_output'] * time_step
        
        return perf


class BiomassDirectCombustionGenerator(ExtendedEnergyComponent):
    """Biomass direct combustion generator physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for biomass generator."""
        return "rural"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for biomass generator."""
        return {
            'combustion_efficiency': 0.90,  # Combustion efficiency
            'boiler_efficiency': 0.85,  # Steam boiler efficiency
            'turbine_efficiency': 0.30,  # Steam turbine efficiency
            'generator_efficiency': 0.95,
            'biomass_heating_value': 18000,  # kJ/kg
            'emission_factor': 0.05,  # kg CO2/kWh (biogenic, considered carbon neutral)
            'rated_power': 5000,  # kW
            'min_part_load': 0.3,  # 30% minimum load
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate biomass generator performance."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # input_power represents biomass feed rate in kg/h
        biomass_feed_rate = input_power
        
        # Calculate thermal power from biomass
        thermal_power = biomass_feed_rate * params['biomass_heating_value'] / 3600  # Convert to kW
        
        # Apply combustion and boiler efficiencies
        steam_power = thermal_power * params['combustion_efficiency'] * params['boiler_efficiency']
        
        # Calculate electric power output
        power_output = steam_power * params['turbine_efficiency'] * params['generator_efficiency']
        
        # Apply minimum part load
        if power_output < params['rated_power'] * params['min_part_load']:
            power_output = 0.0  # Below minimum load, turbine shuts down
        
        # Calculate actual efficiency
        actual_efficiency = params['combustion_efficiency'] * params['boiler_efficiency'] * params['turbine_efficiency'] * params['generator_efficiency']
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': 550.0,  # Boiler temperature
            'pressure': 160.0,  # Steam pressure in bar
            'flow_rate': biomass_feed_rate,  # Biomass feed rate in kg/h
            'internal_state': {
                'biomass_feed_rate': biomass_feed_rate,
                'thermal_power': thermal_power,
                'steam_temperature': 550.0,
                'steam_pressure': 160.0
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                550.0,
                160.0,
                {'cp': 2.0, 'density': 0.6}  # Steam properties
            )
        }


class BiomassGasificationPowerSystem(BiomassDirectCombustionGenerator):
    """Biomass gasification power system physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for biomass gasification system."""
        params = super()._get_default_physical_parameters()
        params.update({
            'gasification_efficiency': 0.75,  # Gasification efficiency
            'gas_cleaning_efficiency': 0.98,  # Gas cleaning efficiency
            'gas_engine_efficiency': 0.40,  # Gas engine efficiency (higher than steam turbine)
            'syngas_heating_value': 12000,  # kJ/m³
            'gasification_temperature': 850,  # °C
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate biomass gasification system performance."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # input_power represents biomass feed rate in kg/h
        biomass_feed_rate = input_power
        
        # Calculate thermal power from biomass
        thermal_power = biomass_feed_rate * params['biomass_heating_value'] / 3600  # Convert to kW
        
        # Gasification process
        syngas_power = thermal_power * params['gasification_efficiency'] * params['gas_cleaning_efficiency']
        
        # Calculate electric power output
        power_output = syngas_power * params['gas_engine_efficiency']
        
        # Calculate actual efficiency
        actual_efficiency = params['gasification_efficiency'] * params['gas_cleaning_efficiency'] * params['gas_engine_efficiency']
        
        return {
            'power_output': power_output,
            'efficiency': actual_efficiency,
            'energy_produced': power_output * time_step,
            'temperature': params['gasification_temperature'],
            'pressure': 1.2,  # Slightly elevated pressure
            'flow_rate': biomass_feed_rate,
            'internal_state': {
                'biomass_feed_rate': biomass_feed_rate,
                'syngas_power': syngas_power,
                'gasification_temperature': params['gasification_temperature']
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                params['gasification_temperature'],
                1.2,
                {'cp': 1.2, 'density': 0.8}  # Syngas properties
            )
        }


class GeothermalORCPowerPlant(ExtendedEnergyComponent):
    """Geothermal Organic Rankine Cycle (ORC) power plant physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for geothermal power plant."""
        return "geothermal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for geothermal ORC power plant."""
        return {
            'geothermal_fluid_temperature': 180,  # °C
            'cooling_water_temperature': 25,  # °C
            'orc_efficiency': 0.15,  # ORC cycle efficiency
            'pump_efficiency': 0.85,
            'generator_efficiency': 0.95,
            'heat_exchanger_efficiency': 0.88,
            'geothermal_fluid_flow_rate': 50,  # kg/s
            'working_fluid': 'isobutane',
            'rated_power': 1000,  # kW
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate geothermal ORC power plant performance."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        # input_power represents geothermal fluid temperature in °C
        geothermal_temp = input_power
        
        # Calculate Carnot efficiency
        carnot_efficiency = calculate_carnot_efficiency(
            geothermal_temp + 273.15,
            params['cooling_water_temperature'] + 273.15
        )
        
        # Actual ORC efficiency is a fraction of Carnot efficiency
        actual_orc_efficiency = carnot_efficiency * 0.35  # Typical ORC efficiency factor
        
        # Calculate heat input from geothermal fluid (simplified)
        heat_input = geothermal_temp * params['geothermal_fluid_flow_rate'] * 4.186  # Simplified
        
        # Calculate electric power output
        power_output = heat_input * actual_orc_efficiency * params['generator_efficiency'] / 1000  # Convert to kW
        
        return {
            'power_output': power_output,
            'efficiency': actual_orc_efficiency * params['generator_efficiency'],
            'energy_produced': power_output * time_step,
            'temperature': geothermal_temp,
            'pressure': 10.0,  # Geothermal fluid pressure
            'flow_rate': params['geothermal_fluid_flow_rate'],
            'internal_state': {
                'geothermal_temperature': geothermal_temp,
                'carnot_efficiency': carnot_efficiency,
                'actual_orc_efficiency': actual_orc_efficiency
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                geothermal_temp,
                10.0,
                {'cp': 4.186, 'density': 950.0}  # Geothermal fluid properties
            )
        }


class CSPTowerSystem(ConcentratedSolarPowerPlant):
    """Concentrated Solar Power (CSP) Tower system physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for CSP tower system."""
        params = super()._get_default_physical_parameters()
        params.update({
            'concentration_ratio': 1000,  # Higher concentration for tower
            'receiver_efficiency': 0.90,  # Better receiver efficiency
            'max_steam_temperature': 600,  # °C (higher than trough)
            'thermal_to_electric_efficiency': 0.40,  # Higher efficiency
            'heliostat_field_area': 100000,  # m²
            'heliostat_reflectance': 0.92,
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate CSP tower system performance."""
        # Get CSP plant performance
        perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Apply tower-specific adjustments
        perf['power_output'] *= 1.5  # Higher efficiency for tower
        perf['efficiency'] *= 1.14  # Higher overall efficiency
        perf['energy_produced'] = perf['power_output'] * time_step
        
        return perf


class CSPTroughSystem(ConcentratedSolarPowerPlant):
    """Concentrated Solar Power (CSP) Trough system physical model."""
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for CSP trough system."""
        params = super()._get_default_physical_parameters()
        params.update({
            'concentration_ratio': 80,  # Lower concentration for trough
            'receiver_efficiency': 0.82,  # Receiver efficiency
            'max_steam_temperature': 400,  # °C
            'thermal_to_electric_efficiency': 0.38,  # Efficiency
            'trough_collector_area': 50000,  # m²
            'reflector_emissivity': 0.05,
        })
        return params
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate CSP trough system performance."""
        # Get CSP plant performance
        perf = super().calculate_physical_performance(input_power, time_step, operating_conditions)
        
        # Apply trough-specific adjustments
        perf['power_output'] *= 0.9  # Slightly lower efficiency for trough
        perf['efficiency'] *= 1.08  # Slightly higher than basic CSP
        perf['energy_produced'] = perf['power_output'] * time_step
        
        return perf


class SolarThermoelectricGenerator(ExtendedEnergyComponent):
    """Solar Thermoelectric Generator (STEG) physical model."""
    
    def get_default_scenario(self) -> str:
        """Get default scenario for solar thermoelectric generator."""
        return "universal"
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for STEG."""
        return {
            'thermoelectric_material_zT': 1.2,  # Figure of merit
            'hot_side_temperature': 250,  # °C
            'cold_side_temperature': 30,  # °C
            'solar_concentration_ratio': 50,
            'absorber_emissivity': 0.95,
            'thermoelectric_module_area': 0.01,  # m² per module
            'number_of_modules': 1000,  # Total modules
            'module_efficiency': 0.08,  # Module efficiency
            'rated_power': 10,  # kW (small scale)
        }
    
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate STEG performance using physical model."""
        # Default operating conditions
        if operating_conditions is None:
            operating_conditions = {}
        
        ambient_temp = operating_conditions.get('ambient_temperature', 25.0)
        
        # Extract physical parameters
        params = self.config.physical_parameters
        
        solar_irradiance = input_power  # W/m²
        
        # Calculate concentrated solar power
        concentrated_power = solar_irradiance * params['solar_concentration_ratio'] * params['absorber_emissivity']
        
        # Calculate hot side temperature (simplified)
        hot_side_temp = ambient_temp + (concentrated_power / 1000)
        
        # Calculate thermoelectric efficiency using simplified formula
        # Efficiency ~ (1 - Tc/Th)² * zT / 4
        tc = params['cold_side_temperature'] + 273.15
        th = hot_side_temp + 273.15
        efficiency = (1 - tc / th) ** 2 * params['thermoelectric_material_zT'] / 4
        efficiency = min(efficiency, params['module_efficiency'])
        
        # Calculate power output
        total_module_area = params['thermoelectric_module_area'] * params['number_of_modules']
        power_output = concentrated_power * total_module_area * efficiency / 1000  # Convert to kW
        
        return {
            'power_output': power_output,
            'efficiency': efficiency,
            'energy_produced': power_output * time_step,
            'temperature': hot_side_temp,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {
                'solar_irradiance': solar_irradiance,
                'hot_side_temperature': hot_side_temp,
                'cold_side_temperature': params['cold_side_temperature'],
                'zT': params['thermoelectric_material_zT']
            },
            'thermodynamic_state': calculate_thermodynamic_state(
                hot_side_temp,
                1.0,
                {'cp': 0.88, 'density': 7.2}  # Bismuth telluride properties
            )
        }


# =============================================================================
# Factory Registration
# =============================================================================

# Register all renewable energy component factories
register_component_factory(
    ExtendedEquipmentType.FIXED_TILT_PV,
    FixedTiltPVSystem
)

register_component_factory(
    ExtendedEquipmentType.SINGLE_AXIS_TRACKING_PV,
    SingleAxisTrackingPVSystem
)

register_component_factory(
    ExtendedEquipmentType.DUAL_AXIS_TRACKING_PV,
    DualAxisTrackingPVSystem
)

register_component_factory(
    ExtendedEquipmentType.DISTRIBUTED_ROOF_PV,
    DistributedRoofPV
)

register_component_factory(
    ExtendedEquipmentType.CONCENTRATED_SOLAR_POWER_PLANT,
    ConcentratedSolarPowerPlant
)

register_component_factory(
    ExtendedEquipmentType.FIXED_SPEED_WIND_TURBINE,
    FixedSpeedWindTurbine
)

register_component_factory(
    ExtendedEquipmentType.VARIABLE_SPEED_DFIG_WIND_TURBINE,
    VariableSpeedDFIGWindTurbine
)

register_component_factory(
    ExtendedEquipmentType.OFFSHORE_DIRECT_DRIVE_WIND_TURBINE,
    OffshoreDirectDriveWindTurbine
)

register_component_factory(
    ExtendedEquipmentType.SMALL_VERTICAL_AXIS_WIND_TURBINE,
    SmallVerticalAxisWindTurbine
)

register_component_factory(
    ExtendedEquipmentType.TIDAL_POWER_GENERATOR,
    TidalPowerGenerator
)

register_component_factory(
    ExtendedEquipmentType.WAVE_ENERGY_CONVERTER,
    WaveEnergyConverter
)

register_component_factory(
    ExtendedEquipmentType.RUN_OF_RIVER_HYDRO_GENERATOR,
    RunOfRiverHydroGenerator
)

register_component_factory(
    ExtendedEquipmentType.RESERVOIR_HYDRO_GENERATOR,
    ReservoirHydroGenerator
)

register_component_factory(
    ExtendedEquipmentType.BIOMASS_DIRECT_COMBUSTION_GENERATOR,
    BiomassDirectCombustionGenerator
)

register_component_factory(
    ExtendedEquipmentType.BIOMASS_GASIFICATION_POWER_SYSTEM,
    BiomassGasificationPowerSystem
)

register_component_factory(
    ExtendedEquipmentType.GEOTHERMAL_ORC_POWER_PLANT,
    GeothermalORCPowerPlant
)

register_component_factory(
    ExtendedEquipmentType.CSP_TOWER_SYSTEM,
    CSPTowerSystem
)

register_component_factory(
    ExtendedEquipmentType.CSP_TROUGH_SYSTEM,
    CSPTroughSystem
)

register_component_factory(
    ExtendedEquipmentType.SOLAR_THERMOELECTRIC_GENERATOR,
    SolarThermoelectricGenerator
)
