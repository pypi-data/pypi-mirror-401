"""
Base classes and interfaces for multi-carrier energy systems.

Provides fundamental abstractions for modeling and optimizing 
multi-carrier energy systems with cross-carrier energy conversion.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
from abc import ABC, abstractmethod
from enum import Enum
import warnings

try:
    import pypsa
    PYPSA_AVAILABLE = True
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)
    PYPSA_AVAILABLE = False


class EnergyCarrier(Enum):
    """Enumeration of different energy carriers."""
    # Electricity
    ELECTRICITY = "electricity"
    
    # Thermal
    HEAT = "heat"
    COLD = "cold"
    
    # Gaseous fuels
    HYDROGEN = "hydrogen"
    NATURAL_GAS = "natural_gas"
    BIOGAS = "biogas"
    SYNTHETIC_METHANE = "synthetic_methane"
    
    # Liquid fuels
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    BIOFUEL = "biofuel"
    JET_FUEL = "jet_fuel"
    LIQUID_HYDROGEN = "liquid_hydrogen"
    
    # Chemical feedstocks
    CO2 = "co2"
    CO = "co"
    CH4 = "ch4"
    
    # Mechanical
    MECHANICAL_POWER = "mechanical_power"
    
    # Information/Communication
    DATA = "data"
    
    # Mobility
    TRANSPORT = "transport"


class ConverterType(Enum):
    """Types of energy converters."""
    # Electrical converters
    TRANSFORMER = "transformer"
    RECTIFIER = "rectifier"
    INVERTER = "inverter"
    
    # Electrochemical converters
    ELECTROLYZER = "electrolyzer"
    FUEL_CELL = "fuel_cell"
    BATTERY = "battery"
    
    # Thermal converters
    BOILER = "boiler"
    HEAT_PUMP = "heat_pump"
    CHILLER = "chiller"
    THERMAL_STORAGE = "thermal_storage"
    
    # Chemical converters
    COMPRESSOR = "compressor"
    DECOMPRESSOR = "decompressor"
    GASIFICATION = "gasification"
    PYROLYSIS = "pyrolysis"
    METHANATION = "methanation"
    FISCHER_TROPSCH = "fischer_tropsch"
    
    # Direct air capture
    DAC = "dac"  # Direct Air Capture
    
    # Mobility converters
    TRACTION_INVERTER = "traction_inverter"
    CHARGING_STATION = "charging_station"
    
    # Combined converters
    CHP = "chp"  # Combined Heat and Power
    COGENERATION = "cogeneration"


class ConverterConfiguration:
    """Configuration for energy converter devices."""
    
    def __init__(self, 
                 converter_type: ConverterType,
                 efficiency: Union[float, Dict[str, float]],
                 power_rating: float,
                 ramp_rate: Optional[float] = None,
                 startup_time: Optional[float] = None,
                 shutdown_time: Optional[float] = None,
                 min_part_load: Optional[float] = None,
                 max_part_load: Optional[float] = None,
                 maintenance_costs: Optional[Dict[str, float]] = None,
                 investment_costs: Optional[float] = None,
                 lifetime: Optional[float] = None):
        """Initialize converter configuration.
        
        Parameters
        ----------
        converter_type : ConverterType
            Type of converter
        efficiency : Union[float, Dict[str, float]]
            Conversion efficiency (constant or temperature/load dependent)
        power_rating : float
            Maximum power rating (kW)
        ramp_rate : float, optional
            Maximum ramp rate (kW/h)
        startup_time : float, optional
            Startup time (hours)
        shutdown_time : float, optional
            Shutdown time (hours)
        min_part_load : float, optional
            Minimum part load fraction (0-1)
        max_part_load : float, optional
            Maximum part load fraction (0-1)
        maintenance_costs : Dict[str, float], optional
            Maintenance cost parameters
        investment_costs : float, optional
            Investment cost (€/kW)
        lifetime : float, optional
            Equipment lifetime (years)
        """
        self.converter_type = converter_type
        self.efficiency = efficiency
        self.power_rating = power_rating
        self.ramp_rate = ramp_rate
        self.startup_time = startup_time
        self.shutdown_time = shutdown_time
        self.min_part_load = min_part_load if min_part_load is not None else 0.0
        self.max_part_load = max_part_load if max_part_load is not None else 1.0
        self.maintenance_costs = maintenance_costs or {}
        self.investment_costs = investment_costs
        self.lifetime = lifetime
    
    def get_efficiency(self, operating_conditions: Optional[Dict[str, Any]] = None) -> float:
        """Get conversion efficiency under given conditions.
        
        Parameters
        ----------
        operating_conditions : Dict[str, Any], optional
            Operating conditions (temperature, pressure, load, etc.)
            
        Returns
        -------
        float
            Conversion efficiency
        """
        if isinstance(self.efficiency, dict):
            if operating_conditions is None:
                # Return average efficiency
                return np.mean(list(self.efficiency.values()))
            else:
                # Interpolate based on conditions
                # Simplified implementation - in reality would use proper interpolation
                return list(self.efficiency.values())[0]
        else:
            return self.efficiency
    
    def validate_configuration(self) -> List[str]:
        """Validate converter configuration.
        
        Returns
        -------
        List[str]
            List of validation errors
        """
        errors = []
        
        if not 0 < self.power_rating:
            errors.append("Power rating must be positive")
        
        if not 0 <= self.min_part_load <= 1:
            errors.append("Minimum part load must be between 0 and 1")
        
        if not 0 <= self.max_part_load <= 1:
            errors.append("Maximum part load must be between 0 and 1")
        
        if self.min_part_load > self.max_part_load:
            errors.append("Minimum part load cannot exceed maximum part load")
        
        if not 0 <= self.get_efficiency() <= 1:
            errors.append("Efficiency must be between 0 and 1")
        
        if self.ramp_rate is not None and self.ramp_rate < 0:
            errors.append("Ramp rate cannot be negative")
        
        return errors


class MultiCarrierConverter(ABC):
    """Abstract base class for multi-carrier energy converters."""
    
    def __init__(self, 
                 converter_id: str,
                 config: ConverterConfiguration,
                 input_carrier: EnergyCarrier,
                 output_carrier: EnergyCarrier,
                 location: Optional[str] = None):
        """Initialize multi-carrier converter.
        
        Parameters
        ----------
        converter_id : str
            Unique identifier for the converter
        config : ConverterConfiguration
            Converter configuration
        input_carrier : EnergyCarrier
            Input energy carrier
        output_carrier : EnergyCarrier
            Output energy carrier
        location : str, optional
            Location identifier
        """
        self.converter_id = converter_id
        self.config = config
        self.input_carrier = input_carrier
        self.output_carrier = output_carrier
        self.location = location
        
        # Operating state
        self.current_power = 0.0
        self.is_operating = False
        
        # Performance metrics
        self.total_energy_converted = 0.0
        self.efficiency_history = []
        self.operating_hours = 0
    
    @abstractmethod
    def convert_energy(self, 
                      input_power: float, 
                      time_step: float = 1.0,
                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convert energy from input to output carrier.
        
        Parameters
        ----------
        input_power : float
            Input power (kW)
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions (temperature, pressure, etc.)
            
        Returns
        -------
        Dict[str, Any]
            Conversion results containing output power, efficiency, losses, etc.
        """
        pass
    
    @abstractmethod
    def get_pypsa_components(self, network: 'pypsa.Network') -> Dict[str, Any]:
        """Get PyPSA components for this converter.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyPSA components
        """
        pass
    
    def can_operate_at_power(self, requested_power: float) -> bool:
        """Check if converter can operate at requested power level.
        
        Parameters
        ----------
        requested_power : float
            Requested power level (kW)
            
        Returns
        -------
        bool
            True if converter can operate at requested power
        """
        # Check power rating
        if requested_power > self.config.power_rating:
            return False
        
        # Check part load constraints
        max_power = self.config.max_part_load * self.config.power_rating
        min_power = self.config.min_part_load * self.config.power_rating
        
        if requested_power > max_power or requested_power < min_power:
            return False
        
        return True
    
    def calculate_energy_balance(self, time_horizon: float = 1.0) -> Dict[str, float]:
        """Calculate energy balance over time horizon.
        
        Parameters
        ----------
        time_horizon : float
            Time horizon (hours)
            
        Returns
        -------
        Dict[str, float]
            Energy balance dictionary
        """
        return {
            'input_energy': self.current_power * time_horizon,
            'output_energy': self.current_power * self.config.get_efficiency() * time_horizon,
            'losses': self.current_power * (1 - self.config.get_efficiency()) * time_horizon,
            'efficiency': self.config.get_efficiency()
        }
    
    def get_operating_limits(self) -> Dict[str, float]:
        """Get operating power limits.
        
        Returns
        -------
        Dict[str, float]
            Operating limits dictionary
        """
        return {
            'min_power': self.config.min_part_load * self.config.power_rating,
            'max_power': self.config.max_part_load * self.config.power_rating,
            'power_rating': self.config.power_rating,
            'current_power': self.current_power
        }
    
    def update_operating_state(self, 
                              new_power: float, 
                              time_step: float = 1.0) -> Dict[str, Any]:
        """Update converter operating state.
        
        Parameters
        ----------
        new_power : float
            New operating power (kW)
        time_step : float
            Time step (hours)
            
        Returns
        -------
        Dict[str, Any]
            Update results
        """
        # Calculate ramp rate
        ramp_rate = abs(new_power - self.current_power) / time_step if time_step > 0 else 0
        
        # Check ramp rate constraint
        if self.config.ramp_rate is not None and ramp_rate > self.config.ramp_rate:
            # Limit ramp rate
            if new_power > self.current_power:
                new_power = self.current_power + self.config.ramp_rate * time_step
            else:
                new_power = self.current_power - self.config.ramp_rate * time_step
        
        # Update state
        old_power = self.current_power
        self.current_power = new_power
        self.is_operating = self.current_power > 0
        
        if self.is_operating:
            self.operating_hours += time_step
            energy_converted = self.current_power * time_step
            self.total_energy_converted += energy_converted
            
            # Record efficiency
            current_efficiency = self.config.get_efficiency()
            self.efficiency_history.append(current_efficiency)
        
        return {
            'old_power': old_power,
            'new_power': self.current_power,
            'actual_ramp_rate': ramp_rate,
            'ramp_constrained': self.config.ramp_rate is not None and ramp_rate > self.config.ramp_rate,
            'efficiency': self.config.get_efficiency(),
            'is_operating': self.is_operating,
            'energy_converted': self.current_power * time_step if self.is_operating else 0
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get converter performance metrics.
        
        Returns
        -------
        Dict[str, Any]
            Performance metrics dictionary
        """
        avg_efficiency = np.mean(self.efficiency_history) if self.efficiency_history else self.config.get_efficiency()
        
        return {
            'total_energy_converted': self.total_energy_converted,  # kWh
            'operating_hours': self.operating_hours,
            'average_efficiency': avg_efficiency,
            'efficiency_variance': np.var(self.efficiency_history) if self.efficiency_history else 0,
            'capacity_factor': self.operating_hours / 8760 if hasattr(self, 'total_hours') else None,
            'utilization_rate': self.total_energy_converted / (self.config.power_rating * 8760) if self.config.power_rating > 0 else 0,
            'current_utilization': self.current_power / self.config.power_rating if self.config.power_rating > 0 else 0
        }
    
    def reset_state(self) -> None:
        """Reset converter operating state."""
        self.current_power = 0.0
        self.is_operating = False
        self.total_energy_converted = 0.0
        self.efficiency_history = []
        self.operating_hours = 0
    
    def __str__(self) -> str:
        """String representation of converter."""
        return (f"Converter {self.converter_id}: "
                f"{self.input_carrier.value} → {self.output_carrier.value} "
                f"({self.config.power_rating} kW)")
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"MultiCarrierConverter(id='{self.converter_id}', "
                f"type='{self.config.converter_type.value}', "
                f"power={self.config.power_rating} kW, "
                f"efficiency={self.config.get_efficiency():.3f})")


class MultiCarrierNetwork:
    """Network class for managing multi-carrier energy systems."""
    
    def __init__(self, network_id: str = "multi_carrier_network"):
        """Initialize multi-carrier network.
        
        Parameters
        ----------
        network_id : str
            Network identifier
        """
        self.network_id = network_id
        self.converters: Dict[str, MultiCarrierConverter] = {}
        self.energy_carriers: Dict[EnergyCarrier, Dict[str, Any]] = {}
        self.connections: List[Dict[str, Any]] = []
        
        # Initialize default energy carriers
        self._initialize_energy_carriers()
    
    def _initialize_energy_carriers(self) -> None:
        """Initialize default energy carrier properties."""
        # Default energy carrier properties
        carrier_properties = {
            EnergyCarrier.ELECTRICITY: {
                'unit': 'kWh',
                'density': 0.0,  # kWh/kg for storage comparison
                'storage_efficiency': 0.95,
                'transport_loss': 0.02,
                'color': '#FFD700'
            },
            EnergyCarrier.HYDROGEN: {
                'unit': 'kWh',
                'density': 33.33,  # kWh/kg (HHV)
                'storage_efficiency': 0.90,
                'transport_loss': 0.05,
                'color': '#00CED1'
            },
            EnergyCarrier.HEAT: {
                'unit': 'kWh',
                'density': 0.001,  # kWh/kg (very low for comparison)
                'storage_efficiency': 0.85,
                'transport_loss': 0.10,
                'color': '#FF6347'
            },
            EnergyCarrier.NATURAL_GAS: {
                'unit': 'kWh',
                'density': 13.9,  # kWh/kg
                'storage_efficiency': 0.98,
                'transport_loss': 0.01,
                'color': '#87CEEB'
            }
        }
        
        for carrier, properties in carrier_properties.items():
            self.energy_carriers[carrier] = properties.copy()
    
    def add_converter(self, converter: MultiCarrierConverter) -> None:
        """Add converter to network.
        
        Parameters
        ----------
        converter : MultiCarrierConverter
            Converter to add
        """
        self.converters[converter.converter_id] = converter
        print(f"Added converter {converter.converter_id}")
    
    def remove_converter(self, converter_id: str) -> bool:
        """Remove converter from network.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier to remove
            
        Returns
        -------
        bool
            True if converter was removed
        """
        if converter_id in self.converters:
            del self.converters[converter_id]
            print(f"Removed converter {converter_id}")
            return True
        return False
    
    def get_converter(self, converter_id: str) -> Optional[MultiCarrierConverter]:
        """Get converter by ID.
        
        Parameters
        ----------
        converter_id : str
            Converter identifier
            
        Returns
        -------
        MultiCarrierConverter or None
            Converter if found
        """
        return self.converters.get(converter_id)
    
    def list_converters_by_carrier(self, 
                                 input_carrier: Optional[EnergyCarrier] = None,
                                 output_carrier: Optional[EnergyCarrier] = None) -> List[str]:
        """List converters filtered by energy carriers.
        
        Parameters
        ----------
        input_carrier : EnergyCarrier, optional
            Filter by input carrier
        output_carrier : EnergyCarrier, optional
            Filter by output carrier
            
        Returns
        -------
        List[str]
            List of converter IDs
        """
        converter_ids = []
        
        for converter in self.converters.values():
            if input_carrier is not None and converter.input_carrier != input_carrier:
                continue
            if output_carrier is not None and converter.output_carrier != output_carrier:
                continue
            converter_ids.append(converter.converter_id)
        
        return converter_ids
    
    def get_network_summary(self) -> Dict[str, Any]:
        """Get network summary statistics.
        
        Returns
        -------
        Dict[str, Any]
            Network summary
        """
        total_converters = len(self.converters)
        carrier_coverage = len(set(c.input_carrier for c in self.converters.values()) | 
                              set(c.output_carrier for c in self.converters.values()))
        
        # Group converters by type
        converter_types = {}
        for converter in self.converters.values():
            converter_type = converter.config.converter_type
            if converter_type not in converter_types:
                converter_types[converter_type] = 0
            converter_types[converter_type] += 1
        
        # Calculate total capacity
        total_capacity = sum(c.config.power_rating for c in self.converters.values())
        total_efficiency = np.mean([c.config.get_efficiency() for c in self.converters.values()])
        
        return {
            'network_id': self.network_id,
            'total_converters': total_converters,
            'energy_carriers_covered': carrier_coverage,
            'converter_types': dict(converter_types),
            'total_capacity': total_capacity,
            'average_efficiency': total_efficiency,
            'converters': list(self.converters.keys())
        }
    
    def export_to_pypsa(self, network: 'pypsa.Network') -> 'pypsa.Network':
        """Export multi-carrier network to PyPSA network.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to export to
            
        Returns
        -------
        pypsa.Network
            Updated PyPSA network
        """
        # Add energy carrier-specific data
        for carrier, properties in self.energy_carriers.items():
            carrier_name = carrier.value
            
            if carrier_name not in network.carriers:
                network.add("Carrier", carrier_name, **properties)
        
        # Add converters as links with multiple energy carriers
        for converter_id, converter in self.converters.items():
            # Get PyPSA components
            components = converter.get_pypsa_components(network)
            
            # Add additional attributes for multi-carrier
            for component_type, component_data in components.items():
                # Add efficiency data
                if hasattr(component_data, 'index'):
                    for idx in component_data.index:
                        network.add(component_type, idx,
                                  efficiency=converter.config.get_efficiency(),
                                  p_nom=converter.config.power_rating,
                                  carrier_in=converter.input_carrier.value,
                                  carrier_out=converter.output_carrier.value)
        
        return network
    
    def clear_network(self) -> None:
        """Clear all converters and connections."""
        self.converters.clear()
        self.connections.clear()
        print("Network cleared")
    
    def __len__(self) -> int:
        """Number of converters in network."""
        return len(self.converters)
    
    def __contains__(self, converter_id: str) -> bool:
        """Check if converter ID exists in network."""
        return converter_id in self.converters
    
    def __iter__(self):
        """Iterate over converters."""
        return iter(self.converters.values())


class OptimizationProblem(ABC):
    """Abstract base class for multi-carrier optimization problems."""
    
    def __init__(self, network: MultiCarrierNetwork):
        """Initialize optimization problem.
        
        Parameters
        ----------
        network : MultiCarrierNetwork
            Multi-carrier network to optimize
        """
        self.network = network
        self.objective_function = None
        self.constraints = []
        self.variables = {}
        self.parameters = {}
    
    @abstractmethod
    def define_objective(self) -> str:
        """Define optimization objective function.
        
        Returns
        -------
        str
            Objective function expression
        """
        pass
    
    @abstractmethod
    def add_constraints(self) -> None:
        """Add optimization constraints."""
        pass
    
    @abstractmethod
    def solve(self, solver: str = 'gurobi', **solver_options) -> Dict[str, Any]:
        """Solve optimization problem.
        
        Parameters
        ----------
        solver : str
            Solver to use
        **solver_options
            Additional solver options
            
        Returns
        -------
        Dict[str, Any]
            Optimization results
        """
        pass


# Utility functions
def convert_energy_units(value: float, 
                        from_unit: str, 
                        to_unit: str, 
                        energy_carrier: Optional[EnergyCarrier] = None) -> float:
    """Convert energy values between different units.
    
    Parameters
    ----------
    value : float
        Energy value
    from_unit : str
        Source unit
    to_unit : str
        Target unit
    energy_carrier : EnergyCarrier, optional
        Energy carrier for density conversions
        
    Returns
    -------
    float
        Converted energy value
    """
    # Energy unit conversions (base unit: kWh)
    energy_conversions = {
        'kWh': 1.0,
        'MWh': 1000.0,
        'GWh': 1000000.0,
        'J': 1/3600000,  # Joules to kWh
        'MJ': 1/3600,    # MJ to kWh
        'GJ': 1/3.6,     # GJ to kWh
        'BTU': 1/3412.14, # BTU to kWh
        'cal': 1/859845,  # Calories to kWh
        'kcal': 1/859.845, # kcal to kWh
        'therm': 29.3,    # Therm to kWh
        'tce': 8141.0,    # Ton coal equivalent to kWh
        'toe': 11630.0    # Ton oil equivalent to kWh
    }
    
    if from_unit not in energy_conversions or to_unit not in energy_conversions:
        raise ValueError(f"Unsupported energy unit conversion: {from_unit} to {to_unit}")
    
    # Convert to base unit, then to target
    base_value = value * energy_conversions[from_unit]
    converted_value = base_value / energy_conversions[to_unit]
    
    # Handle mass-based conversions if energy carrier is provided
    if energy_carrier is not None and energy_carrier in [EnergyCarrier.HYDROGEN, EnergyCarrier.NATURAL_GAS]:
        density_map = {
            EnergyCarrier.HYDROGEN: 33.33,  # kWh/kg
            EnergyCarrier.NATURAL_GAS: 13.9  # kWh/kg
        }
        
        if energy_carrier in density_map:
            density = density_map[energy_carrier]
            
            # kg to kWh conversions
            mass_unit_to_kg = {
                'kg': 1.0,
                'ton': 1000.0,
                'lb': 0.453592,
                'g': 0.001
            }
            
            if from_unit in mass_unit_to_kg:
                # Mass to energy
                kg_value = value * mass_unit_to_kg[from_unit]
                converted_value = kg_value * density
            elif to_unit in mass_unit_to_kg:
                # Energy to mass
                converted_value = value / density / mass_unit_to_kg[to_unit]
    
    return converted_value


def calculate_system_efficiency(converters: List[MultiCarrierConverter], 
                               conversion_chain: List[str]) -> float:
    """Calculate overall system efficiency for conversion chain.
    
    Parameters
    ----------
    converters : List[MultiCarrierConverter]
        List of converters in the chain
    conversion_chain : List[str]
        Ordered list of converter IDs
        
    Returns
    -------
    float
        Overall system efficiency
    """
    if not conversion_chain:
        return 1.0
    
    overall_efficiency = 1.0
    
    for converter_id in conversion_chain:
        converter = None
        for c in converters:
            if c.converter_id == converter_id:
                converter = c
                break
        
        if converter is None:
            raise ValueError(f"Converter {converter_id} not found in converters list")
        
        overall_efficiency *= converter.config.get_efficiency()
    
    return overall_efficiency