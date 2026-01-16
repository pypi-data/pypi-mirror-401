"""
Specific multi-carrier energy converter implementations.

Provides concrete implementations for various energy conversion devices
including electrolyzers, fuel cells, heat pumps, compressors, and other
multi-carrier conversion technologies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
import warnings

try:
    import pypsa
    PYPSA_AVAILABLE = True
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)
    PYPSA_AVAILABLE = False

# Import base modules
from .base import (
    MultiCarrierConverter, 
    EnergyCarrier, 
    ConverterConfiguration, 
    ConverterType
)

# Import thermodynamics modules
from ..thermodynamics import (
    CompressionCalculator,
    GasProperties,
    GAS_CONSTANTS,
    SPECIFIC_HEAT_RATIOS,
    MOLAR_MASSES,
    ThermodynamicError
)


class ElectrolyzerConverter(MultiCarrierConverter):
    """Electrolyzer converter: electricity to hydrogen."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 efficiency: Optional[float] = 0.70,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize electrolyzer converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        efficiency : float
            Electric to hydrogen conversion efficiency (0-1)
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        config = ConverterConfiguration(
            converter_type=ConverterType.ELECTROLYZER,
            efficiency=efficiency,
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.1),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.1),  # 10% per hour
            startup_time=kwargs.get('startup_time', 0.5),  # 30 minutes
            shutdown_time=kwargs.get('shutdown_time', 0.1),  # 6 minutes
            investment_costs=kwargs.get('investment_costs', 800),  # €/kW
            lifetime=kwargs.get('lifetime', 20)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.ELECTRICITY,
            output_carrier=EnergyCarrier.HYDROGEN,
            location=location
        )
        
        # Electrolyzer-specific properties
        self.hydrogen_production_rate = 0.0  # kg/h
        self.water_consumption = 0.0  # L/h
        self.temperature_operating = 60.0  # °C (PEM electrolyzer)
        self.pressure_output = 30.0  # bar
        self.electrolyte_type = kwargs.get('electrolyte_type', 'PEM')  # PEM, Alkaline, SOEC
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert electricity to hydrogen.
        
        Parameters
        ----------
        input_power : float
            Input electricity power (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions (temperature, pressure, etc.)
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'efficiency': 0.0
            }
        
        # Update efficiency based on operating conditions
        if operating_conditions:
            self._update_efficiency_from_conditions(operating_conditions)
        
        # Calculate conversion
        efficiency = self.config.get_efficiency()
        output_power = input_power * efficiency  # kW (thermal equivalent)
        
        # Convert to hydrogen production rate
        # Higher heating value of hydrogen: 39.4 kWh/kg
        hydrogen_lhv = 33.3  # kWh/kg (lower heating value)
        hydrogen_power_equivalent = output_power * time_step  # kWh
        hydrogen_produced = hydrogen_power_equivalent / hydrogen_lhv  # kg
        
        # Calculate water consumption (0.009 kg water per kg H2 for PEM)
        water_consumed = hydrogen_produced * 0.009  # kg
        water_consumed_liters = water_consumed  # 1 kg ≈ 1 liter
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'output_power': output_power,
            'hydrogen_produced': hydrogen_produced,  # kg
            'water_consumed': water_consumed,  # kg
            'water_consumed_liters': water_consumed_liters,  # L
            'efficiency': efficiency,
            'hydrogen_lhv': hydrogen_lhv,
            'electrolyte_type': self.electrolyte_type,
            'output_pressure': self.pressure_output,
            'state_update': state_update
        }
    
    def _update_efficiency_from_conditions(self, conditions: Dict[str, Any]) -> None:
        """Update efficiency based on operating conditions.
        
        Uses physics-based models for temperature and load factor effects
        on electrolyzer efficiency.
        """
        base_efficiency = self.config.get_efficiency()
        
        # Temperature effect on efficiency (physics-based model)
        if 'temperature' in conditions:
            temp = conditions['temperature']
            
            if self.electrolyte_type == 'PEM':
                # PEM electrolyzer: optimal at 60-80°C
                # Based on Nernst equation and activation overpotential
                optimal_temp = 70  # °C
                if temp < 20:
                    # Cold start penalty
                    temp_factor = 0.85
                elif temp < optimal_temp:
                    # Linear improvement to optimal
                    temp_factor = 0.85 + 0.15 * (temp - 20) / (optimal_temp - 20)
                elif temp <= 80:
                    # Optimal range
                    temp_factor = 1.0
                else:
                    # Degradation at high temperatures
                    temp_factor = 1.0 - 0.01 * (temp - 80)
                    
            elif self.electrolyte_type == 'SOEC':
                # Solid oxide electrolyzer: optimal at 700-900°C
                # Based on Arrhenius-type temperature dependence
                optimal_temp = 800  # °C
                if temp < 600:
                    # Below operating range
                    temp_factor = 0.7
                elif temp < optimal_temp:
                    # Exponential improvement
                    temp_factor = 0.7 + 0.3 * (temp - 600) / (optimal_temp - 600)
                elif temp <= 900:
                    # Optimal range
                    temp_factor = 1.0
                else:
                    # Material degradation
                    temp_factor = 1.0 - 0.005 * (temp - 900)
                    
            else:  # Alkaline
                # Alkaline electrolyzer: optimal at 60-90°C
                optimal_temp = 75  # °C
                if temp < 40:
                    temp_factor = 0.8
                elif temp < optimal_temp:
                    temp_factor = 0.8 + 0.2 * (temp - 40) / (optimal_temp - 40)
                elif temp <= 90:
                    temp_factor = 1.0
                else:
                    temp_factor = 1.0 - 0.008 * (temp - 90)
            
            base_efficiency *= max(0.5, min(1.2, temp_factor))
        
        # Load-dependent efficiency (curvilinear model)
        if 'load_factor' in conditions:
            load_factor = conditions['load_factor']
            
            if self.electrolyte_type == 'PEM':
                # PEM: good turndown ratio, efficiency drops at low loads
                if load_factor >= 0.2:
                    load_factor = max(0.2, load_factor)
                    load_penalty = 1.0 - 0.15 * (1 - load_factor)
                else:
                    load_penalty = 0.85
                    
            elif self.electrolyte_type == 'SOEC':
                # SOEC: limited turndown, significant penalty at low loads
                if load_factor >= 0.3:
                    load_factor = max(0.3, load_factor)
                    load_penalty = 1.0 - 0.25 * (1 - load_factor)
                else:
                    load_penalty = 0.75
                    
            else:  # Alkaline
                # Alkaline: moderate turndown capability
                if load_factor >= 0.25:
                    load_factor = max(0.25, load_factor)
                    load_penalty = 1.0 - 0.2 * (1 - load_factor)
                else:
                    load_penalty = 0.8
            
            base_efficiency *= max(0.5, min(1.0, load_penalty))
        
        # Apply efficiency bounds
        self.config.efficiency = max(0.4, min(0.9, base_efficiency))
    
    def get_pypsa_components(self, network) -> Dict[str, Any]:
        """Get PyPSA components for electrolyzer.
        
        Parameters
        ----------
        network : pypsa.Network or None
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        if not PYPSA_AVAILABLE:
            warnings.warn("PyPSA not available, cannot create PyPSA components", UserWarning)
            return {}
            
        components = {}
        
        # Add electrolyzer as a Link
        network.add("Link", 
                   self.converter_id,
                   bus0="electricity_bus",  # Input bus (customize as needed)
                   bus1="hydrogen_bus",     # Output bus (customize as needed)
                   efficiency=self.config.get_efficiency(),
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.ELECTRICITY.value,
                   carrier_out=EnergyCarrier.HYDROGEN.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 20)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        # Add auxiliary bus for electrolyzer (optional)
        network.add("Bus", f"{self.converter_id}_aux_bus", 
                   carrier=EnergyCarrier.ELECTRICITY.value)
        
        network.add("Link",
                   f"{self.converter_id}_aux",
                   bus0=f"{self.converter_id}_aux_bus",
                   bus1="electricity_bus",
                   efficiency=0.95,
                   p_nom=self.config.power_rating * 0.05)  # 5% auxiliary consumption
        
        return components
    
    def get_performance_characteristics(self) -> Dict[str, Any]:
        """Get detailed performance characteristics.
        
        Returns
        -------
        Dict[str, Any]
            Performance characteristics
        """
        base_metrics = self.get_performance_metrics()
        
        characteristics = {
            **base_metrics,
            'electrolyzer_type': self.electrolyte_type,
            'operating_temperature': self.temperature_operating,
            'output_pressure': self.pressure_output,
            'specific_energy_consumption': 50.0,  # kWh/kg H2 (typical for PEM)
            'water_consumption_rate': 9.0,  # L/kg H2
            'hydrogen_purity': 99.95,  # %
            'degradation_rate': 0.01,  # % per 1000 hours
            'maintenance_requirements': {
                'stack_replacement': 40000,  # operating hours
                'seal_replacement': 20000,   # operating hours
                'periodic_maintenance': 8000  # operating hours
            }
        }
        
        return characteristics


class FuelCellConverter(MultiCarrierConverter):
    """Fuel cell converter: hydrogen to electricity."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 efficiency: Optional[float] = 0.60,
                 fuel_cell_type: str = 'PEM',
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize fuel cell converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        efficiency : float
            Hydrogen to electricity conversion efficiency (0-1)
        fuel_cell_type : str
            Type of fuel cell (PEM, SOFC, MCFC, etc.)
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        config = ConverterConfiguration(
            converter_type=ConverterType.FUEL_CELL,
            efficiency=efficiency,
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.2),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.05),  # 5% per hour
            startup_time=kwargs.get('startup_time', 2.0),  # 2 hours
            shutdown_time=kwargs.get('shutdown_time', 0.5),  # 30 minutes
            investment_costs=kwargs.get('investment_costs', 1200),  # €/kW
            lifetime=kwargs.get('lifetime', 10)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.HYDROGEN,
            output_carrier=EnergyCarrier.ELECTRICITY,
            location=location
        )
        
        # Fuel cell-specific properties
        self.fuel_cell_type = fuel_cell_type
        self.hydrogen_consumption_rate = 0.0  # kg/h
        self.water_production = 0.0  # L/h
        self.heat_production = 0.0  # kW (thermal)
        self.operating_temperature = self._get_operating_temperature()
        self.electric_efficiency = efficiency
        self.thermal_efficiency = 1.0 - efficiency
    
    def _get_operating_temperature(self) -> float:
        """Get operating temperature based on fuel cell type."""
        temp_map = {
            'PEM': 80,      # Proton Exchange Membrane
            'AFC': 100,     # Alkaline Fuel Cell
            'PAFC': 200,    # Phosphoric Acid Fuel Cell
            'MCFC': 650,    # Molten Carbonate Fuel Cell
            'SOFC': 800     # Solid Oxide Fuel Cell
        }
        return temp_map.get(self.fuel_cell_type, 80)
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert hydrogen to electricity.
        
        Parameters
        ----------
        input_power : float
            Input hydrogen power equivalent (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'efficiency': 0.0
            }
        
        # Update efficiency based on operating conditions
        if operating_conditions:
            self._update_efficiency_from_conditions(operating_conditions)
        
        # Calculate conversion
        efficiency = self.config.get_efficiency()
        electricity_output = input_power * efficiency  # kW
        heat_output = input_power * (1 - efficiency)  # kW (thermal)
        
        # Calculate hydrogen consumption
        hydrogen_lhv = 33.3  # kWh/kg
        hydrogen_power_equivalent = input_power * time_step  # kWh
        hydrogen_consumed = hydrogen_power_equivalent / hydrogen_lhv  # kg
        
        # Calculate water production (0.009 kg water per kg H2)
        water_produced = hydrogen_consumed * 0.009  # kg
        water_produced_liters = water_produced  # L
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'electricity_output': electricity_output,
            'heat_output': heat_output,
            'hydrogen_consumed': hydrogen_consumed,  # kg
            'water_produced': water_produced,  # kg
            'water_produced_liters': water_produced_liters,  # L
            'efficiency': efficiency,
            'thermal_efficiency': self.thermal_efficiency,
            'fuel_cell_type': self.fuel_cell_type,
            'operating_temperature': self.operating_temperature,
            'state_update': state_update
        }
    
    def _update_efficiency_from_conditions(self, conditions: Dict[str, Any]) -> None:
        """Update efficiency based on operating conditions using detailed physical models."""
        current_efficiency = self.config.get_efficiency()
        efficiency_factor = 1.0
        
        # Temperature effect on efficiency - detailed physical models
        if 'temperature' in conditions:
            temp = conditions['temperature']
            
            # Detailed temperature dependency based on fuel cell type
            if self.fuel_cell_type == 'PEM':
                # PEM fuel cells: optimal around 80°C, sharp drop outside range
                optimal_temp = 80.0
                if temp < 60:
                    temp_factor = 0.7 + 0.005 * (temp - 20)  # Cold start penalty
                elif temp > 90:
                    temp_factor = 1.0 - 0.015 * (temp - 90)  # Membrane degradation
                else:
                    temp_factor = 1.0 - 0.002 * abs(temp - optimal_temp)
                    
            elif self.fuel_cell_type == 'AFC':
                # Alkaline fuel cells: sensitive to temperature, optimal 65-85°C
                optimal_temp = 75.0
                if temp < 50:
                    temp_factor = 0.6 + 0.008 * (temp - 20)
                elif temp > 100:
                    temp_factor = 1.0 - 0.02 * (temp - 100)
                else:
                    temp_factor = 1.0 - 0.0015 * abs(temp - optimal_temp)
                    
            elif self.fuel_cell_type == 'SOFC':
                # Solid oxide fuel cells: high temperature operation
                # Efficiency increases with temperature up to 800°C
                if temp < 600:
                    temp_factor = 0.4 + 0.001 * temp
                elif temp > 1000:
                    temp_factor = 1.0 - 0.0005 * (temp - 1000)
                else:
                    temp_factor = 0.7 + 0.0005 * (temp - 600)
            else:
                temp_factor = 1.0
            
            efficiency_factor *= max(0.3, min(1.2, temp_factor))
        
        # Load-dependent efficiency - detailed part-load characteristics
        if 'load_factor' in conditions:
            load_factor = conditions['load_factor']
            
            # Detailed load factor models based on fuel cell type
            if self.fuel_cell_type == 'PEM':
                # PEM: good part-load performance but efficiency drops below 20%
                if load_factor < 0.2:
                    load_factor = 0.2  # Minimum stable operation
                    load_penalty = 0.8
                elif load_factor < 0.5:
                    load_penalty = 0.95 - 0.1 * (0.5 - load_factor)
                else:
                    load_penalty = 1.0
                    
            elif self.fuel_cell_type == 'AFC':
                # AFC: moderate part-load performance
                if load_factor < 0.3:
                    load_factor = 0.3
                    load_penalty = 0.85
                elif load_factor < 0.7:
                    load_penalty = 0.98 - 0.1 * (0.7 - load_factor)
                else:
                    load_penalty = 1.0
                    
            elif self.fuel_cell_type == 'SOFC':
                # SOFC: excellent part-load performance
                if load_factor < 0.1:
                    load_factor = 0.1  # Minimum load for SOFC
                    load_penalty = 0.9
                elif load_factor < 0.3:
                    load_penalty = 0.95 - 0.1 * (0.3 - load_factor)
                else:
                    load_penalty = 1.0
            else:
                load_penalty = 1.0
            
            efficiency_factor *= max(0.5, min(1.0, load_penalty))
        
        # Apply combined efficiency factor with bounds
        new_efficiency = current_efficiency * efficiency_factor
        # Ensure efficiency stays within reasonable bounds
        self.config.efficiency = max(0.3, min(0.7, new_efficiency))
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for fuel cell.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Add fuel cell as a Link
        network.add("Link", 
                   self.converter_id,
                   bus0="hydrogen_bus",    # Input bus
                   bus1="electricity_bus", # Output bus
                   efficiency=self.config.get_efficiency(),
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.HYDROGEN.value,
                   carrier_out=EnergyCarrier.ELECTRICITY.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 10)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        # Add heat output (as separate Link)
        if self.thermal_efficiency > 0:
            heat_buses = [bus for bus in network.buses.index if 'heat' in bus.lower()]
            if heat_buses:
                network.add("Link",
                           f"{self.converter_id}_heat",
                           bus0="hydrogen_bus",
                           bus1=heat_buses[0],
                           efficiency=self.thermal_efficiency,
                           p_nom=self.config.power_rating)
                
                components['heat_link'] = network.links.loc[[f"{self.converter_id}_heat"]]
        
        return components


class HeatPumpConverter(MultiCarrierConverter):
    """Heat pump converter: electricity to heat."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 cop: Optional[float] = 3.5,
                 heat_pump_type: str = 'air_source',
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize heat pump converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        cop : float
            Coefficient of Performance (ratio of heat output to electricity input)
        heat_pump_type : str
            Type of heat pump (air_source, ground_source, water_source)
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        # Convert COP to efficiency (heat pump efficiency is COP)
        efficiency = cop
        
        config = ConverterConfiguration(
            converter_type=ConverterType.HEAT_PUMP,
            efficiency=efficiency,
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.3),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.2),  # 20% per hour
            startup_time=kwargs.get('startup_time', 0.1),  # 6 minutes
            shutdown_time=kwargs.get('shutdown_time', 0.05),  # 3 minutes
            investment_costs=kwargs.get('investment_costs', 400),  # €/kW
            lifetime=kwargs.get('lifetime', 20)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.ELECTRICITY,
            output_carrier=EnergyCarrier.HEAT,
            location=location
        )
        
        # Heat pump-specific properties
        self.heat_pump_type = heat_pump_type
        self.cop = cop
        self.heat_output_rate = 0.0  # kW (thermal)
        self.source_temperature = self._get_source_temperature()
        self.sink_temperature = kwargs.get('sink_temperature', 45.0)  # °C
        self.refrigerant_type = kwargs.get('refrigerant_type', 'R410A')
    
    def _get_source_temperature(self) -> float:
        """Get source temperature based on heat pump type."""
        temp_map = {
            'air_source': 5.0,      # Average outdoor temperature
            'ground_source': 10.0,  # Ground temperature
            'water_source': 12.0    # Water source temperature
        }
        return temp_map.get(self.heat_pump_type, 5.0)
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert electricity to heat using heat pump.
        
        Parameters
        ----------
        input_power : float
            Input electricity power (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'cop': 0.0
            }
        
        # Update COP based on operating conditions
        if operating_conditions:
            self._update_cop_from_conditions(operating_conditions)
        
        # Calculate heat output
        cop = self.config.get_efficiency()  # COP
        heat_output = input_power * cop  # kW (thermal)
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'heat_output': heat_output,
            'cop': cop,
            'efficiency': cop,
            'heat_pump_type': self.heat_pump_type,
            'source_temperature': self.source_temperature,
            'sink_temperature': self.sink_temperature,
            'temperature_lift': self.sink_temperature - self.source_temperature,
            'state_update': state_update
        }
    
    def _update_cop_from_conditions(self, conditions: Dict[str, Any]) -> None:
        """Update COP based on operating conditions using detailed thermodynamic models."""
        base_cop = self.cop  # Store the nominal COP
        
        # Temperature effect on COP - detailed Carnot-based model
        if 'source_temperature' in conditions:
            source_temp = conditions['source_temperature']
            sink_temp = conditions.get('sink_temperature', self.sink_temperature)
            
            # Convert to Kelvin for thermodynamic calculations
            source_temp_k = source_temp + 273.15
            sink_temp_k = sink_temp + 273.15
            
            # Carnot efficiency (theoretical maximum)
            carnot_cop = sink_temp_k / (sink_temp_k - source_temp_k)
            
            # Temperature lift effect - COP decreases non-linearly with temperature lift
            temperature_lift = sink_temp - source_temp
            
            # COP degradation factors based on heat pump type and temperature lift
            cop_degradation_factors = {
                'air_source': {
                    'base': 0.45,  # Typical performance factor for air-source
                    'lift_penalty': 0.015  # COP reduction per °C of lift
                },
                'ground_source': {
                    'base': 0.55,  # Better performance for ground-source
                    'lift_penalty': 0.012  # Lower penalty due to stable source
                },
                'water_source': {
                    'base': 0.50,  # Intermediate performance
                    'lift_penalty': 0.013  # Moderate penalty
                }
            }
            
            hp_config = cop_degradation_factors.get(self.heat_pump_type, cop_degradation_factors['air_source'])
            
            # Calculate actual COP considering temperature lift
            lift_penalty = 1.0 - (temperature_lift * hp_config['lift_penalty'])
            actual_cop = base_cop * hp_config['base'] * lift_penalty
            
            # Apply refrigerant-specific corrections
            refrigerant_corrections = {
                'R410A': 1.0,
                'R134a': 0.95,
                'R32': 1.05,
                'CO2': 0.90  # Transcritical CO2 systems
            }
            refrigerant_factor = refrigerant_corrections.get(self.refrigerant_type, 1.0)
            actual_cop *= refrigerant_factor
            
            # Ensure COP doesn't exceed Carnot limit
            actual_cop = min(actual_cop, carnot_cop * 0.8)  # 80% of Carnot efficiency
            
            self.config.efficiency = max(actual_cop, 1.5)  # Minimum practical COP
        
        # Load-dependent performance - detailed part-load model
        if 'load_factor' in conditions:
            load_factor = conditions['load_factor']
            
            # Part-load performance curves based on heat pump type
            part_load_curves = {
                'air_source': {
                    'optimal_range': (0.4, 0.8),  # Optimal load range
                    'low_load_penalty': 0.08,     # COP reduction per 10% below optimal
                    'high_load_penalty': 0.05     # COP reduction per 10% above optimal
                },
                'ground_source': {
                    'optimal_range': (0.3, 0.9),
                    'low_load_penalty': 0.06,
                    'high_load_penalty': 0.04
                },
                'water_source': {
                    'optimal_range': (0.35, 0.85),
                    'low_load_penalty': 0.07,
                    'high_load_penalty': 0.045
                }
            }
            
            curve_config = part_load_curves.get(self.heat_pump_type, part_load_curves['air_source'])
            optimal_min, optimal_max = curve_config['optimal_range']
            
            # Calculate load factor penalty
            if load_factor < optimal_min:
                # Below optimal range - COP decreases
                penalty_factor = 1.0 - (optimal_min - load_factor) * curve_config['low_load_penalty']
            elif load_factor > optimal_max:
                # Above optimal range - COP decreases
                penalty_factor = 1.0 - (load_factor - optimal_max) * curve_config['high_load_penalty']
            else:
                # Within optimal range - no penalty
                penalty_factor = 1.0
            
            # Apply load factor penalty
            self.config.efficiency *= max(penalty_factor, 0.7)  # Minimum 70% of nominal COP
        
        # Additional environmental factors
        if 'ambient_temperature' in conditions and self.heat_pump_type == 'air_source':
            ambient_temp = conditions['ambient_temperature']
            # Air-source heat pumps have reduced performance at very low temperatures
            if ambient_temp < -10:
                frost_penalty = 1.0 - (-10 - ambient_temp) * 0.02  # 2% reduction per °C below -10°C
                self.config.efficiency *= max(frost_penalty, 0.6)  # Minimum 60% COP in extreme cold
        
        # Defrost cycle penalty for air-source heat pumps
        if (self.heat_pump_type == 'air_source' and 
            'humidity' in conditions and 
            conditions['humidity'] > 80):
            # High humidity increases defrost frequency
            defrost_penalty = 0.95  # 5% reduction due to defrost cycles
            self.config.efficiency *= defrost_penalty
        
        # Final bounds check
        self.config.efficiency = max(min(self.config.efficiency, base_cop * 1.1), 1.5)
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for heat pump.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Find or create heat bus
        heat_buses = [bus for bus in network.buses.index if 'heat' in bus.lower()]
        if not heat_buses:
            network.add("Bus", "heat_bus", carrier=EnergyCarrier.HEAT.value)
            heat_buses = ["heat_bus"]
        
        # Add heat pump as a Link
        network.add("Link", 
                   self.converter_id,
                   bus0="electricity_bus",  # Input bus (customize as needed)
                   bus1=heat_buses[0],     # Output bus
                   efficiency=self.config.get_efficiency(),  # COP
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.ELECTRICITY.value,
                   carrier_out=EnergyCarrier.HEAT.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 20)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        return components


class CompressionConverter(MultiCarrierConverter):
    """Compression converter: gas to compressed gas."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 efficiency: Optional[float] = 0.85,
                 gas_type: str = 'hydrogen',
                 compression_ratio: float = 30.0,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize compression converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        efficiency : float
            Compression efficiency (0-1)
        gas_type : str
            Type of gas being compressed
        compression_ratio : float
            Pressure ratio (outlet/inlet pressure)
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        config = ConverterConfiguration(
            converter_type=ConverterType.COMPRESSOR,
            efficiency=efficiency,
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.4),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.5),  # 50% per hour
            startup_time=kwargs.get('startup_time', 0.25),  # 15 minutes
            shutdown_time=kwargs.get('shutdown_time', 0.1),  # 6 minutes
            investment_costs=kwargs.get('investment_costs', 600),  # €/kW
            lifetime=kwargs.get('lifetime', 25)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier(gas_type.lower()),
            output_carrier=EnergyCarrier(gas_type.lower()),
            location=location
        )
        
        # Compressor-specific properties
        self.gas_type = gas_type
        self.compression_ratio = compression_ratio
        self.pressure_inlet = kwargs.get('pressure_inlet', 1.0)  # bar
        self.pressure_outlet = self.pressure_inlet * compression_ratio
        self.compression_stages = kwargs.get('compression_stages', 3)
        self.intercooling = kwargs.get('intercooling', True)
        
        # Thermodynamic model configuration
        self.thermodynamic_model = kwargs.get('thermodynamic_model', 'simplified')  # 'simplified' or 'precise'
        self.temperature_inlet = kwargs.get('temperature_inlet', 298.15)  # K
        self.temperature_outlet = kwargs.get('temperature_outlet', None)  # K, calculated if None
        self.use_coolprop = kwargs.get('use_coolprop', False)  # Use CoolProp for precise calculations
        
        # Initialize thermodynamic calculator if using precise model
        if self.thermodynamic_model == 'precise':
            try:
                self.compression_calculator = CompressionCalculator(
                    gas_type=gas_type,
                    use_coolprop=self.use_coolprop
                )
                self.gas_properties = GasProperties(gas_type)
            except ImportError as e:
                warnings.warn(
                    f"Precise thermodynamic model not available: {e}. Falling back to simplified model.",
                    UserWarning
                )
                self.thermodynamic_model = 'simplified'
                self.compression_calculator = None
                self.gas_properties = None
        else:
            self.compression_calculator = None
            self.gas_properties = None
        
        # Adjust energy carriers based on gas type
        if gas_type.lower() == 'hydrogen':
            self.input_carrier = EnergyCarrier.HYDROGEN
            self.output_carrier = EnergyCarrier.HYDROGEN
        elif gas_type.lower() == 'natural_gas':
            self.input_carrier = EnergyCarrier.NATURAL_GAS
            self.output_carrier = EnergyCarrier.NATURAL_GAS
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Compress gas from inlet to outlet pressure.
        
        Parameters
        ----------
        input_power : float
            Input power (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'efficiency': 0.0
            }
        
        # Calculate compression work using thermodynamic model
        if self.thermodynamic_model == 'precise' and self.compression_calculator is not None:
            # Use precise thermodynamic model with CompressionCalculator
            try:
                # Get gas properties from database
                gas_props = self.gas_properties.get_properties()
                
                # Calculate compression work using precise model
                result = self.compression_calculator.calculate_compression_work(
                    pressure_inlet=self.pressure_inlet,
                    pressure_outlet=self.pressure_outlet,
                    temperature_inlet=self.temperature_inlet,
                    compression_stages=self.compression_stages,
                    intercooling=self.intercooling,
                    isentropic_efficiency=self.config.get_efficiency(),
                    gas_properties=gas_props
                )
                
                work_per_kg_kwh = result['work_per_kg_kwh']
                actual_work_per_kg = result['actual_work_per_kg']
                outlet_temperature = result['outlet_temperature']
                
                # Update outlet temperature if not set
                if self.temperature_outlet is None:
                    self.temperature_outlet = outlet_temperature
                
                # Calculate gas flow rate
                power_available = input_power * time_step  # kWh
                gas_flow_rate = power_available / actual_work_per_kg  # kg/h (mass flow rate)
                
            except ThermodynamicError as e:
                # Fall back to simplified model if precise calculation fails
                warnings.warn(
                    f"Precise thermodynamic calculation failed: {e}. Falling back to simplified model.",
                    UserWarning
                )
                self.thermodynamic_model = 'simplified'
                # Continue with simplified calculation below
        
        # Simplified thermodynamic model (fallback or default)
        if self.thermodynamic_model == 'simplified':
            # Isentropic work: W = (γ/(γ-1)) * R * T1 * [(P2/P1)^((γ-1)/γ) - 1]
            # Consider gas-specific properties and multi-stage compression
            
            # Gas-specific properties
            gas_properties = {
                'hydrogen': {'gamma': 1.4, 'R': 4124.0, 'molar_mass': 2.016},
                'natural_gas': {'gamma': 1.3, 'R': 518.0, 'molar_mass': 16.04}
            }
            
            gas_props = gas_properties.get(self.gas_type.lower(), gas_properties['hydrogen'])
            gamma = gas_props['gamma']
            R = gas_props['R']  # J/kg·K
            
            # Temperature calculation considering intercooling
            T1 = self.temperature_inlet  # Inlet temperature (K)
            if self.intercooling and self.compression_stages > 1:
                # Multi-stage compression with intercooling
                stage_ratio = self.compression_ratio ** (1.0 / self.compression_stages)
                work_per_stage = (gamma / (gamma - 1)) * R * T1 * (stage_ratio ** ((gamma - 1) / gamma) - 1)
                work_per_kg = work_per_stage * self.compression_stages
            else:
                # Single-stage compression
                work_per_kg = (gamma / (gamma - 1)) * R * T1 * \
                             (self.compression_ratio ** ((gamma - 1) / gamma) - 1)  # J/kg
            
            # Convert to kWh/kg
            work_per_kg_kwh = work_per_kg / 3600000  # kWh/kg
            
            # Efficiency correction considering mechanical and electrical losses
            isentropic_efficiency = self.config.get_efficiency()
            mechanical_efficiency = 0.95  # Typical mechanical efficiency
            electrical_efficiency = 0.98  # Typical electrical efficiency
            overall_efficiency = isentropic_efficiency * mechanical_efficiency * electrical_efficiency
            
            actual_work_per_kg = work_per_kg_kwh / overall_efficiency
            
            # Calculate gas flow rate
            power_available = input_power * time_step  # kWh
            gas_flow_rate = power_available / actual_work_per_kg  # kg/h (mass flow rate)
            
            # Estimate outlet temperature for simplified model
            if self.temperature_outlet is None:
                self.temperature_outlet = T1 * self.compression_ratio ** ((gamma - 1) / gamma)
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'output_power': input_power * 0.95,  # Some losses in auxiliary systems
            'gas_flow_rate': gas_flow_rate,  # kg/h
            'compression_ratio': self.compression_ratio,
            'pressure_inlet': self.pressure_inlet,
            'pressure_outlet': self.pressure_outlet,
            'work_per_kg': work_per_kg_kwh,
            'actual_work_per_kg': actual_work_per_kg,
            'efficiency': self.config.get_efficiency(),
            'compression_stages': self.compression_stages,
            'intercooling': self.intercooling,
            'gas_type': self.gas_type,
            'state_update': state_update
        }
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for compressor.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Add compressor as a Link
        bus_suffix = f"_{self.gas_type}_compressed"
        
        # Create compressed gas bus if it doesn't exist
        compressed_bus = f"{self.gas_type}_compressed_bus"
        if compressed_bus not in network.buses.index:
            network.add("Bus", compressed_bus, 
                       carrier=self.output_carrier.value)
        
        network.add("Link", 
                   self.converter_id,
                   bus0=f"{self.gas_type}_bus",      # Input bus
                   bus1=compressed_bus,              # Output bus
                   efficiency=self.config.get_efficiency(),
                   p_nom=self.config.power_rating,
                   carrier_in=self.input_carrier.value,
                   carrier_out=self.output_carrier.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 25)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        return components


class DACConverter(MultiCarrierConverter):
    """Direct Air Capture (DAC) converter: CO2 to liquid CO2."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 co2_capture_rate: Optional[float] = 1000.0,  # kg CO2/day
                 energy_consumption: Optional[float] = 1500.0,  # kWh/ton CO2
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize DAC converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        co2_capture_rate : float
            CO2 capture capacity (kg/day)
        energy_consumption : float
            Energy consumption (kWh per ton CO2 captured)
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        # Convert energy consumption to efficiency
        # Typical DAC: 1500 kWh/ton CO2
        # If power rating is capacity, we need to calculate efficiency
        daily_capacity_tons = co2_capture_rate / 1000.0
        daily_energy_capacity = power_rating * 24  # kWh/day
        theoretical_max_tons = daily_energy_capacity / energy_consumption
        
        efficiency = theoretical_max_tons / daily_capacity_tons if daily_capacity_tons > 0 else 1.0
        
        config = ConverterConfiguration(
            converter_type=ConverterType.DAC,
            efficiency=min(efficiency, 1.0),
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.5),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.1),  # 10% per hour
            startup_time=kwargs.get('startup_time', 4.0),  # 4 hours
            shutdown_time=kwargs.get('shutdown_time', 1.0),  # 1 hour
            investment_costs=kwargs.get('investment_costs', 600),  # €/kW
            lifetime=kwargs.get('lifetime', 25)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.CO2,
            output_carrier=EnergyCarrier.CO2,
            location=location
        )
        
        # DAC-specific properties
        self.co2_capture_rate = co2_capture_rate  # kg/day
        self.energy_consumption = energy_consumption  # kWh/ton CO2
        self.co2_purity = kwargs.get('co2_purity', 99.0)  # %
        self.heat_consumption = kwargs.get('heat_consumption', 1500.0)  # kWh/ton CO2 (thermal)
        self.sorbent_type = kwargs.get('sorbent_type', 'amine')  # Amine, solid sorbent
        self.regeneration_temp = kwargs.get('regeneration_temp', 120.0)  # °C
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Capture CO2 from air.
        
        Parameters
        ----------
        input_power : float
            Input power (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'co2_captured': 0.0,
                'efficiency': 0.0
            }
        
        # Calculate CO2 capture rate based on input power
        # Capacity-based calculation
        capacity_factor = input_power / self.config.power_rating
        hourly_co2_capture = (self.co2_capture_rate / 24) * capacity_factor  # kg/h
        
        # Apply efficiency
        actual_co2_capture = hourly_co2_capture * self.config.get_efficiency()  # kg/h
        
        # Calculate energy requirements
        energy_per_ton = self.energy_consumption  # kWh/ton CO2
        theoretical_energy = (actual_co2_capture / 1000) * energy_per_ton  # kWh
        actual_energy_input = input_power * time_step  # kWh
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'output_power': 0.0,  # DAC outputs captured CO2, not power
            'co2_captured': actual_co2_capture * time_step,  # kg
            'co2_purity': self.co2_purity,
            'theoretical_energy': theoretical_energy,
            'actual_energy_input': actual_energy_input,
            'energy_efficiency': theoretical_energy / actual_energy_input if actual_energy_input > 0 else 0,
            'sorbent_type': self.sorbent_type,
            'regeneration_temperature': self.regeneration_temp,
            'capacity_factor': capacity_factor,
            'state_update': state_update
        }
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for DAC system.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Create CO2 buses
        ambient_co2_bus = "ambient_co2_bus"
        captured_co2_bus = "captured_co2_bus"
        
        if ambient_co2_bus not in network.buses.index:
            network.add("Bus", ambient_co2_bus, carrier=EnergyCarrier.CO2.value)
        
        if captured_co2_bus not in network.buses.index:
            network.add("Bus", captured_co2_bus, carrier=EnergyCarrier.CO2.value)
        
        # Add DAC as a Link
        network.add("Link", 
                   self.converter_id,
                   bus0="electricity_bus",    # Input power
                   bus1=captured_co2_bus,     # Output captured CO2
                   bus2=ambient_co2_bus,      # Input ambient CO2
                   efficiency=self.config.get_efficiency(),
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.ELECTRICITY.value,
                   carrier_out=EnergyCarrier.CO2.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 25)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        return components


# Additional converter classes would be implemented similarly
# For brevity, I'll include a few more important ones

class GasificationConverter(MultiCarrierConverter):
    """Biomass gasification converter: solid biomass to syngas."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 biomass_type: str = 'wood_chips',
                 efficiency: Optional[float] = 0.75,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize gasification converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        biomass_type : str
            Type of biomass feedstock
        efficiency : float
            Gasification efficiency (0-1)
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        config = ConverterConfiguration(
            converter_type=ConverterType.GASIFICATION,
            efficiency=efficiency,
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.4),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.1),  # 10% per hour
            startup_time=kwargs.get('startup_time', 2.0),  # 2 hours
            shutdown_time=kwargs.get('shutdown_time', 1.0),  # 1 hour
            investment_costs=kwargs.get('investment_costs', 1000),  # €/kW
            lifetime=kwargs.get('lifetime', 20)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.BIOFUEL,
            output_carrier=EnergyCarrier.SYNTHETIC_METHANE,
            location=location
        )
        
        # Gasification-specific properties
        self.biomass_type = biomass_type
        self.temperature = kwargs.get('temperature', 800.0)  # °C
        self.syngas_composition = self._calculate_syngas_composition()
    
    def _calculate_syngas_composition(self) -> Dict[str, float]:
        """Calculate syngas composition based on biomass type and process conditions."""
        # Detailed syngas composition calculation considering temperature and biomass properties
        
        # Base compositions by biomass type (volume %)
        base_compositions = {
            'wood_chips': {'C': 50.0, 'H': 6.0, 'O': 44.0, 'N': 0.2, 'ash': 0.8},
            'agricultural_waste': {'C': 48.0, 'H': 5.5, 'O': 45.0, 'N': 1.0, 'ash': 0.5},
            'energy_crops': {'C': 49.0, 'H': 6.2, 'O': 43.5, 'N': 0.8, 'ash': 0.5}
        }
        
        biomass_props = base_compositions.get(self.biomass_type, base_compositions['wood_chips'])
        
        # Calculate gas composition based on thermodynamic equilibrium
        # Simplified water-gas shift and methanation reactions
        temperature_factor = self.temperature / 800.0  # Normalize to reference temperature
        
        # Adjust composition based on temperature
        # Higher temperatures favor CO production, lower temperatures favor CH4
        co_content = 20.0 + 5.0 * (temperature_factor - 1.0)  # %
        h2_content = 18.0 + 3.0 * (temperature_factor - 1.0)  # %
        ch4_content = 3.0 - 1.5 * (temperature_factor - 1.0)  # %
        co2_content = 12.0 - 2.0 * (temperature_factor - 1.0)  # %
        
        # Adjust for biomass composition
        carbon_ratio = biomass_props['C'] / 50.0
        hydrogen_ratio = biomass_props['H'] / 6.0
        
        co_content *= carbon_ratio
        h2_content *= hydrogen_ratio
        ch4_content *= hydrogen_ratio
        
        # Normalize to 100%
        total = co_content + h2_content + ch4_content + co2_content
        n2_content = 100.0 - total
        
        return {
            'CO': max(5.0, min(40.0, co_content)),
            'H2': max(10.0, min(30.0, h2_content)),
            'CH4': max(1.0, min(10.0, ch4_content)),
            'CO2': max(5.0, min(25.0, co2_content)),
            'N2': max(30.0, min(60.0, n2_content))
        }
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert biomass to syngas.
        
        Parameters
        ----------
        input_power : float
            Input biomass power equivalent (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'efficiency': 0.0
            }
        
        # Calculate gasification output
        efficiency = self.config.get_efficiency()
        syngas_output = input_power * efficiency  # kW thermal equivalent
        
        # Calculate biomass consumption (energy content ≈ 5 MWh/ton)
        biomass_energy_content = 5000  # kWh/ton
        biomass_consumed = (input_power * time_step) / biomass_energy_content  # tons
        
        # Calculate syngas production (thermal value ≈ 15 MJ/Nm³)
        syngas_lhv = 4.17  # kWh/Nm³
        syngas_produced = (syngas_output * time_step) / syngas_lhv  # Nm³
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'output_power': syngas_output,
            'biomass_consumed': biomass_consumed,  # tons
            'syngas_produced': syngas_produced,  # Nm³
            'syngas_composition': self.syngas_composition,
            'gasification_temperature': self.temperature,
            'efficiency': efficiency,
            'biomass_type': self.biomass_type,
            'state_update': state_update
        }
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for gasifier.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Create syngas bus
        syngas_bus = "syngas_bus"
        if syngas_bus not in network.buses.index:
            network.add("Bus", syngas_bus, carrier=EnergyCarrier.SYNTHETIC_METHANE.value)
        
        # Add gasifier as a Link
        network.add("Link", 
                   self.converter_id,
                   bus0=f"{self.biomass_type}_bus",  # Input bus (customize)
                   bus1=syngas_bus,                # Output syngas bus
                   efficiency=self.config.get_efficiency(),
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.BIOFUEL.value,
                   carrier_out=EnergyCarrier.SYNTHETIC_METHANE.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 20)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        return components


class MethanationConverter(MultiCarrierConverter):
    """Power-to-methane converter: CO2 + H2 to CH4."""
    
    def __init__(self, 
                 converter_id: str,
                 power_rating: float,
                 efficiency: Optional[float] = 0.80,
                 reactor_type: str = 'sabatier',
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize methanation converter.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
        power_rating : float
            Maximum power rating (kW)
        efficiency : float
            Methanation efficiency (0-1)
        reactor_type : str
            Type of methanation reactor
        location : str, optional
            Location identifier
        **kwargs
            Additional configuration parameters
        """
        config = ConverterConfiguration(
            converter_type=ConverterType.METHANATION,
            efficiency=efficiency,
            power_rating=power_rating,
            min_part_load=kwargs.get('min_part_load', 0.3),
            max_part_load=kwargs.get('max_part_load', 1.0),
            ramp_rate=kwargs.get('ramp_rate', power_rating * 0.15),  # 15% per hour
            startup_time=kwargs.get('startup_time', 1.0),  # 1 hour
            shutdown_time=kwargs.get('shutdown_time', 0.5),  # 30 minutes
            investment_costs=kwargs.get('investment_costs', 1500),  # €/kW
            lifetime=kwargs.get('lifetime', 20)  # years
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.CO2,
            output_carrier=EnergyCarrier.SYNTHETIC_METHANE,
            location=location
        )
        
        # Methanation-specific properties
        self.reactor_type = reactor_type
        self.hydrogen_to_co2_ratio = 4.0  # Stoichiometric ratio (H2:CO2)
        self.temperature = kwargs.get('temperature', 300.0)  # °C
        self.pressure = kwargs.get('pressure', 25.0)  # bar
        self.catalyst_type = kwargs.get('catalyst_type', 'Ni-based')
    
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert CO2 and H2 to synthetic methane.
        
        Parameters
        ----------
        input_power : float
            Input power equivalent (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions
            
        Returns
        -------
        Dict[str, Any]
            Conversion results
        """
        # Check operating limits
        if not self.can_operate_at_power(input_power):
            return {
                'success': False,
                'error': 'Power level outside operating limits',
                'input_power': input_power,
                'output_power': 0.0,
                'efficiency': 0.0
            }
        
        # Calculate methanation output
        efficiency = self.config.get_efficiency()
        methane_output = input_power * efficiency  # kW thermal equivalent
        
        # Calculate required inputs
        # CH4 HHV: 55.5 MJ/kg = 15.4 kWh/kg
        # H2 LHV: 33.3 kWh/kg
        # CO2: 0 (no chemical energy)
        
        # For each kWh of CH4 produced, need 15.4/33.3 ≈ 0.46 kWh H2
        hydrogen_equivalent = methane_output * 0.46  # kW H2 equivalent
        
        # Methane production
        ch4_hhv = 15.4  # kWh/kg
        methane_produced = (methane_output * time_step) / ch4_hhv  # kg
        
        # Hydrogen consumption
        h2_consumed = (hydrogen_equivalent * time_step) / 33.3  # kg
        
        # CO2 consumption (stoichiometric: 16g CH4 requires 44g CO2)
        co2_consumed = methane_produced * (44/16)  # kg
        
        # Update state
        state_update = self.update_operating_state(input_power, time_step)
        
        return {
            'success': True,
            'input_power': input_power,
            'hydrogen_consumed': h2_consumed,  # kg
            'co2_consumed': co2_consumed,      # kg
            'methane_produced': methane_produced,  # kg
            'hydrogen_to_co2_ratio': self.hydrogen_to_co2_ratio,
            'reactor_temperature': self.temperature,
            'reactor_pressure': self.pressure,
            'catalyst_type': self.catalyst_type,
            'efficiency': efficiency,
            'reactor_type': self.reactor_type,
            'state_update': state_update
        }
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for methanation reactor.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Create buses
        co2_bus = "co2_bus"
        h2_bus = "hydrogen_bus"
        ch4_bus = "synthetic_methane_bus"
        
        for bus in [co2_bus, h2_bus, ch4_bus]:
            if bus not in network.buses.index:
                bus_carrier = {
                    co2_bus: EnergyCarrier.CO2.value,
                    h2_bus: EnergyCarrier.HYDROGEN.value,
                    ch4_bus: EnergyCarrier.SYNTHETIC_METHANE.value
                }
                network.add("Bus", bus, carrier=bus_carrier[bus])
        
        # Add methanation reactor as a Link
        network.add("Link", 
                   self.converter_id,
                   bus0=h2_bus,      # Hydrogen input
                   bus1=co2_bus,     # CO2 input  
                   bus2=ch4_bus,     # Synthetic methane output
                   efficiency=self.config.get_efficiency(),
                   p_nom=self.config.power_rating,
                   carrier_in=f"{EnergyCarrier.HYDROGEN.value}+{EnergyCarrier.CO2.value}",
                   carrier_out=EnergyCarrier.SYNTHETIC_METHANE.value,
                   marginal_cost=0.0,
                   capex=self.config.investment_costs if self.config.investment_costs else 0,
                   lifetime=self.config.lifetime if self.config.lifetime else 20)
        
        components['link'] = network.links.loc[[self.converter_id]]
        
        return components


# Additional converters for completeness
class PyrolysisConverter(MultiCarrierConverter):
    """Pyrolysis converter: biomass to biochar, bio-oil, and syngas.
    
    Implements a detailed pyrolysis model based on biomass type, temperature,
    and residence time. Supports different biomass feedstocks with varying
    product yields and energy content.
    """
    
    def __init__(self, converter_id: str, power_rating: float, **kwargs):
        config = ConverterConfiguration(
            converter_type=ConverterType.PYROLYSIS,
            efficiency=kwargs.get('efficiency', 0.70),
            power_rating=power_rating,
            **kwargs
        )
        
        super().__init__(
            converter_id=converter_id,
            config=config,
            input_carrier=EnergyCarrier.BIOFUEL,
            output_carrier=EnergyCarrier.BIOFUEL,
            location=kwargs.get('location')
        )
        
        # Pyrolysis-specific parameters
        self.biomass_type = kwargs.get('biomass_type', 'wood')
        self.temperature = kwargs.get('temperature', 500.0)  # Celsius
        self.residence_time = kwargs.get('residence_time', 30.0)  # minutes
        self.moisture_content = kwargs.get('moisture_content', 0.10)  # 10%
        
        # Product yield coefficients by biomass type (biochar, bio-oil, syngas)
        self.yield_coefficients = {
            'wood': (0.25, 0.50, 0.25),      # Wood biomass
            'agricultural': (0.30, 0.45, 0.25),  # Agricultural residues
            'manure': (0.35, 0.40, 0.25),    # Animal manure
            'msw': (0.20, 0.55, 0.25)        # Municipal solid waste
        }
        
        # Energy content of products (MJ/kg)
        self.energy_content = {
            'biochar': 30.0,    # High carbon content
            'bio_oil': 18.0,    # Liquid fuel
            'syngas': 12.0      # Gas mixture
        }
    
    def _calculate_product_yields(self, input_power: float, temperature: float, 
                                residence_time: float) -> Tuple[float, float, float]:
        """Calculate product yields based on process conditions.
        
        Parameters
        ----------
        input_power : float
            Input biomass power (kW)
        temperature : float
            Pyrolysis temperature (Celsius)
        residence_time : float
            Residence time (minutes)
            
        Returns
        -------
        Tuple[float, float, float]
            Biochar, bio-oil, and syngas yields (kg/h)
        """
        # Get base yields for biomass type
        biochar_yield, bio_oil_yield, syngas_yield = self.yield_coefficients.get(
            self.biomass_type, (0.25, 0.50, 0.25)
        )
        
        # Temperature effect: higher temperature increases gas yield, decreases oil yield
        temp_factor = max(0.5, min(1.5, temperature / 500.0))
        bio_oil_yield *= (1.0 - 0.2 * (temp_factor - 1.0))
        syngas_yield *= (1.0 + 0.3 * (temp_factor - 1.0))
        
        # Residence time effect: longer time increases char yield
        time_factor = max(0.5, min(2.0, residence_time / 30.0))
        biochar_yield *= (1.0 + 0.1 * (time_factor - 1.0))
        
        # Moisture content effect: reduces overall efficiency
        moisture_factor = 1.0 - self.moisture_content
        
        # Calculate mass flows (kg/h)
        # Assuming biomass energy content ~18 MJ/kg
        biomass_flow = input_power * 3.6 / 18.0  # kg/h
        
        biochar_flow = biomass_flow * biochar_yield * moisture_factor
        bio_oil_flow = biomass_flow * bio_oil_yield * moisture_factor
        syngas_flow = biomass_flow * syngas_yield * moisture_factor
        
        return biochar_flow, bio_oil_flow, syngas_flow
    
    def convert_energy(self, input_power: float, time_step: float = 1.0, **kwargs) -> Dict[str, Any]:
        """Convert biomass to pyrolysis products.
        
        Parameters
        ----------
        input_power : float
            Input biomass power (kW)
        time_step : float
            Time step duration (hours)
            
        Returns
        -------
        Dict[str, Any]
            Conversion results including product yields and efficiency
        """
        # Check operating constraints
        if input_power < self.config.min_part_load * self.config.power_rating:
            return {
                'success': False,
                'error': f'Input power {input_power} kW below minimum load {self.config.min_part_load * self.config.power_rating} kW'
            }
        
        if input_power > self.config.power_rating:
            return {
                'success': False,
                'error': f'Input power {input_power} kW exceeds rated capacity {self.config.power_rating} kW'
            }
        
        # Get process conditions from kwargs or use defaults
        temperature = kwargs.get('temperature', self.temperature)
        residence_time = kwargs.get('residence_time', self.residence_time)
        
        # Calculate product yields
        biochar_flow, bio_oil_flow, syngas_flow = self._calculate_product_yields(
            input_power, temperature, residence_time
        )
        
        # Calculate energy output
        biochar_energy = biochar_flow * self.energy_content['biochar'] / 3.6  # kW
        bio_oil_energy = bio_oil_flow * self.energy_content['bio_oil'] / 3.6  # kW
        syngas_energy = syngas_flow * self.energy_content['syngas'] / 3.6    # kW
        
        total_output_energy = biochar_energy + bio_oil_energy + syngas_energy
        
        # Calculate actual efficiency
        actual_efficiency = total_output_energy / input_power if input_power > 0 else 0.0
        
        # Update state
        self._update_state({
            'input_power': input_power,
            'temperature': temperature,
            'residence_time': residence_time,
            'efficiency': actual_efficiency
        })
        
        return {
            'success': True,
            'input_power': input_power,
            'biochar_produced': biochar_flow * time_step,  # kg
            'bio_oil_produced': bio_oil_flow * time_step,  # kg
            'syngas_produced': syngas_flow * time_step,    # kg
            'biochar_energy': biochar_energy,              # kW
            'bio_oil_energy': bio_oil_energy,              # kW
            'syngas_energy': syngas_energy,                # kW
            'total_output_energy': total_output_energy,    # kW
            'efficiency': actual_efficiency,
            'temperature': temperature,
            'residence_time': residence_time
        }
    
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for pyrolysis reactor.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        components = {}
        
        # Create buses for biomass input and product outputs
        biomass_bus = "biomass_bus"
        biochar_bus = "biochar_bus"
        bio_oil_bus = "bio_oil_bus"
        syngas_bus = "syngas_bus"
        
        for bus in [biomass_bus, biochar_bus, bio_oil_bus, syngas_bus]:
            if bus not in network.buses.index:
                bus_carrier = {
                    biomass_bus: EnergyCarrier.BIOFUEL.value,
                    biochar_bus: EnergyCarrier.BIOCHAR.value,
                    bio_oil_bus: EnergyCarrier.BIO_OIL.value,
                    syngas_bus: EnergyCarrier.SYNGAS.value
                }
                network.add("Bus", bus, carrier=bus_carrier[bus])
        
        # Add pyrolysis reactor as a Link with multiple outputs
        # Note: PyPSA Link can only have one output, so we use multiple links
        # or store as a multi-carrier converter
        network.add("Link", 
                   f"{self.converter_id}_biochar",
                   bus0=biomass_bus,
                   bus1=biochar_bus,
                   efficiency=0.25,  # Biochar yield
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.BIOFUEL.value,
                   carrier_out=EnergyCarrier.BIOCHAR.value,
                   marginal_cost=0.0)
        
        network.add("Link", 
                   f"{self.converter_id}_bio_oil",
                   bus0=biomass_bus,
                   bus1=bio_oil_bus,
                   efficiency=0.50,  # Bio-oil yield
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.BIOFUEL.value,
                   carrier_out=EnergyCarrier.BIO_OIL.value,
                   marginal_cost=0.0)
        
        network.add("Link", 
                   f"{self.converter_id}_syngas",
                   bus0=biomass_bus,
                   bus1=syngas_bus,
                   efficiency=0.25,  # Syngas yield
                   p_nom=self.config.power_rating,
                   carrier_in=EnergyCarrier.BIOFUEL.value,
                   carrier_out=EnergyCarrier.SYNGAS.value,
                   marginal_cost=0.0)
        
        components['links'] = network.links.loc[
            [f"{self.converter_id}_biochar", f"{self.converter_id}_bio_oil", f"{self.converter_id}_syngas"]
        ]
        
        return components