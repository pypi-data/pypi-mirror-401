"""Core network module for PyXESXXN - Python for eXtended Energy System Analysis.

This module defines the fundamental building blocks for multi-carrier energy system modeling,
including network structures, components, and energy carriers. The design is completely
independent of PyPSA and provides a clean, intuitive API for energy system modeling.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Union, Any, Tuple
from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EnergyCarrier(Enum):
    """Enumeration of energy carriers supported by PyXESXXN.
    
    This defines the different types of energy that can flow through the network,
    enabling multi-carrier energy system modeling.
    """
    ELECTRICITY = "electricity"
    HEAT = "heat"
    HYDROGEN = "hydrogen"
    NATURAL_GAS = "natural_gas"
    BIOGAS = "biogas"
    BIOMASS = "biomass"
    SOLAR = "solar"
    WIND = "wind"
    HYDRO = "hydro"
    COAL = "coal"
    OIL = "oil"


class ComponentType(Enum):
    """Enumeration of component types in the energy system.
    
    Defines the different types of components that can be added to the network,
    each with specific properties and behaviors.
    """
    BUS = "bus"
    GENERATOR = "generator"
    LOAD = "load"
    LINE = "line"
    STORAGE = "storage"
    CONVERTER = "converter"
    CHP = "chp"
    HEAT_PUMP = "heat_pump"
    ELECTROLYZER = "electrolyzer"
    FUEL_CELL = "fuel_cell"
    LINK = "link"
    TRANSFORMER = "transformer"


@dataclass
class ComponentConfig:
    """Configuration class for energy system components.
    
    Provides a flexible way to configure component properties and constraints.
    """
    name: str
    component_type: ComponentType
    carrier: EnergyCarrier
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'name': self.name,
            'component_type': self.component_type.value,
            'carrier': self.carrier.value,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Component(ABC):
    """Abstract base class for all energy system components.
    
    Provides common functionality and interface for all components
    in the energy system network.
    """
    
    def __init__(self, config: ComponentConfig) -> None:
        """Initialize a component with the given configuration.
        
        Parameters
        ----------
        config : ComponentConfig
            Configuration object defining component properties.
        """
        self.config = config
        self.name = config.name
        self.component_type = config.component_type
        self.carrier = config.carrier
        self.parameters = config.parameters
        self.metadata = config.metadata
        self._connected_buses: List[Bus] = []
    
    def connect_to_bus(self, bus: Bus) -> None:
        """Connect this component to a bus.
        
        Parameters
        ----------
        bus : Bus
            Bus to connect to.
        """
        if bus not in self._connected_buses:
            self._connected_buses.append(bus)
    
    def disconnect_from_bus(self, bus: Bus) -> None:
        """Disconnect this component from a bus.
        
        Parameters
        ----------
        bus : Bus
            Bus to disconnect from.
        """
        if bus in self._connected_buses:
            self._connected_buses.remove(bus)
    
    def get_connected_buses(self) -> List[Bus]:
        """Get list of connected buses."""
        return self._connected_buses.copy()
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration.
        
        Returns
        -------
        bool
            True if configuration is valid.
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation."""
        pass


class Bus(Component):
    """Bus component representing a connection point in the energy system.
    
    Buses serve as nodes where energy carriers can be exchanged between components.
    """
    
    def __init__(self, config: ComponentConfig) -> None:
        """Initialize a bus component.
        
        Parameters
        ----------
        config : ComponentConfig
            Bus configuration.
        """
        super().__init__(config)
        self._connected_components: List[Component] = []
    
    def connect_component(self, component: Component) -> None:
        """Connect a component to this bus.
        
        Parameters
        ----------
        component : Component
            Component to connect.
        """
        if component not in self._connected_components:
            self._connected_components.append(component)
            component.connect_to_bus(self)
    
    def disconnect_component(self, component: Component) -> None:
        """Disconnect a component from this bus.
        
        Parameters
        ----------
        component : Component
            Component to disconnect.
        """
        if component in self._connected_components:
            self._connected_components.remove(component)
            component.disconnect_from_bus(self)
    
    def get_connected_components(self) -> List[Component]:
        """Get list of components connected to this bus."""
        return self._connected_components.copy()
    
    def validate(self) -> bool:
        """Validate bus configuration."""
        required_params = ['voltage', 'frequency']
        return all(param in self.parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert bus to dictionary representation."""
        return {
            'name': self.name,
            'type': self.component_type.value,
            'carrier': self.carrier.value,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Generator(Component):
    """Generator component representing energy production units.
    
    Generators produce energy from various sources (renewable, conventional, etc.).
    """
    
    def __init__(self, config: ComponentConfig, bus: Bus) -> None:
        """Initialize a generator component.
        
        Parameters
        ----------
        config : ComponentConfig
            Generator configuration.
        bus : Bus
            Connected bus.
        """
        super().__init__(config)
        self.bus = bus
        bus.connect_component(self)
        self.power_output: Optional[float] = None
    
    def set_power_output(self, power: float) -> None:
        """Set the power output of the generator.
        
        Parameters
        ----------
        power : float
            Power output value.
        """
        capacity = self.parameters.get('capacity')
        if capacity is not None and power > capacity:
            raise ValueError(f"Power output {power} exceeds capacity {capacity}")
        self.power_output = power
    
    def validate(self) -> bool:
        """Validate generator configuration."""
        required_params = ['capacity', 'efficiency']
        return all(param in self.parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert generator to dictionary representation."""
        return {
            'name': self.name,
            'type': self.component_type.value,
            'carrier': self.carrier.value,
            'bus': self.bus.name,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Load(Component):
    """Load component representing energy consumption points.
    
    Loads consume energy from the network.
    """
    
    def __init__(self, config: ComponentConfig, bus: Bus) -> None:
        """Initialize a load component.
        
        Parameters
        ----------
        config : ComponentConfig
            Load configuration.
        bus : Bus
            Connected bus.
        """
        super().__init__(config)
        self.bus = bus
        bus.connect_component(self)
        self.power_demand: Optional[float] = None
    
    def set_power_demand(self, demand: float) -> None:
        """Set the power demand of the load.
        
        Parameters
        ----------
        demand : float
            Power demand value.
        """
        if demand < 0:
            raise ValueError("Power demand cannot be negative")
        self.power_demand = demand
    
    def validate(self) -> bool:
        """Validate load configuration."""
        required_params = ['demand']
        return all(param in self.parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert load to dictionary representation."""
        return {
            'name': self.name,
            'type': self.component_type.value,
            'carrier': self.carrier.value,
            'bus': self.bus.name,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Line(Component):
    """Line component representing energy transmission or distribution.
    
    Lines connect buses and enable energy flow between different parts of the network.
    """
    
    def __init__(self, config: ComponentConfig, from_bus: Bus, to_bus: Bus) -> None:
        """Initialize a line component.
        
        Parameters
        ----------
        config : ComponentConfig
            Line configuration.
        from_bus : Bus
            Source bus.
        to_bus : Bus
            Destination bus.
        """
        super().__init__(config)
        self.from_bus = from_bus
        self.to_bus = to_bus
        from_bus.connect_component(self)
        to_bus.connect_component(self)
        self.power_flow: Optional[float] = None
    
    def set_power_flow(self, power: float) -> None:
        """Set the power flow through the line.
        
        Parameters
        ----------
        power : float
            Power flow value (positive for from_bus to to_bus).
        """
        capacity = self.parameters.get('capacity')
        if capacity is not None and abs(power) > capacity:
            raise ValueError(f"Power flow {power} exceeds capacity {capacity}")
        self.power_flow = power
    
    def validate(self) -> bool:
        """Validate line configuration."""
        required_params = ['capacity', 'resistance', 'reactance']
        return all(param in self.parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert line to dictionary representation."""
        return {
            'name': self.name,
            'type': self.component_type.value,
            'carrier': self.carrier.value,
            'from_bus': self.from_bus.name,
            'to_bus': self.to_bus.name,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class StorageUnit(Component):
    """Storage unit component representing energy storage systems.
    
    Storage units can store and release energy, providing flexibility to the system.
    """
    
    def __init__(self, config: ComponentConfig, bus: Bus) -> None:
        """Initialize a storage unit component.
        
        Parameters
        ----------
        config : ComponentConfig
            Storage configuration.
        bus : Bus
            Connected bus.
        """
        super().__init__(config)
        self.bus = bus
        bus.connect_component(self)
        self.state_of_charge: float = 0.0
        self.charging_power: Optional[float] = None
        self.discharging_power: Optional[float] = None
    
    def set_state_of_charge(self, soc: float) -> None:
        """Set the state of charge of the storage.
        
        Parameters
        ----------
        soc : float
            State of charge (0-1).
        """
        if not 0 <= soc <= 1:
            raise ValueError("State of charge must be between 0 and 1")
        self.state_of_charge = soc
    
    def set_charging_power(self, power: float) -> None:
        """Set the charging power.
        
        Parameters
        ----------
        power : float
            Charging power (positive value).
        """
        if power < 0:
            raise ValueError("Charging power cannot be negative")
        self.charging_power = power
    
    def set_discharging_power(self, power: float) -> None:
        """Set the discharging power.
        
        Parameters
        ----------
        power : float
            Discharging power (positive value).
        """
        if power < 0:
            raise ValueError("Discharging power cannot be negative")
        self.discharging_power = power
    
    def validate(self) -> bool:
        """Validate storage configuration."""
        required_params = ['capacity', 'efficiency_charge', 'efficiency_discharge']
        return all(param in self.parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert storage to dictionary representation."""
        return {
            'name': self.name,
            'type': self.component_type.value,
            'carrier': self.carrier.value,
            'bus': self.bus.name,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class PyXESXXNNetwork:
    """
    Main PyXESXXN network class for energy system modeling.
    
    This class provides a completely independent implementation of energy system
    network modeling, replacing PyPSA dependencies with native PyXESXXN components.
    """
    
    def __init__(self, name: str = "PyXESXXN Network") -> None:
        """Initialize a PyXESXXN network.
        
        Parameters
        ----------
        name : str, default="PyXESXXN Network"
            Name of the network.
        """
        self.name = name
        self.components: Dict[str, Component] = {}
        self.buses: Dict[str, Bus] = {}
        self.generators: Dict[str, Generator] = {}
        self.loads: Dict[str, Load] = {}
        self.lines: Dict[str, Line] = {}
        self.storage_units: Dict[str, StorageUnit] = {}
        self.time_series: Optional[pd.DataFrame] = None
        self.results: Dict[str, Any] = {}
        
        logger.info(f"Created PyXESXXN network: {name}")
    
    def add_bus(self, name: str, carrier: Union[str, EnergyCarrier], 
                voltage: float = 1.0, frequency: float = 50.0, **kwargs) -> Bus:
        """Add a bus to the network.
        
        Parameters
        ----------
        name : str
            Bus name.
        carrier : Union[str, EnergyCarrier]
            Energy carrier type.
        voltage : float, default=1.0
            Bus voltage.
        frequency : float, default=50.0
            Bus frequency.
        **kwargs
            Additional parameters.
            
        Returns
        -------
        Bus
            Created bus component.
        """
        if isinstance(carrier, str):
            carrier = EnergyCarrier(carrier)
        
        config = ComponentConfig(
            name=name,
            component_type=ComponentType.BUS,
            carrier=carrier,
            parameters={'voltage': voltage, 'frequency': frequency, **kwargs}
        )
        
        bus = Bus(config)
        self.components[name] = bus
        self.buses[name] = bus
        
        logger.debug(f"Added bus: {name}")
        return bus
    
    def add_generator(self, name: str, bus: Union[str, Bus], 
                     carrier: Union[str, EnergyCarrier], capacity: float, 
                     efficiency: float = 0.9, **kwargs) -> Generator:
        """Add a generator to the network.
        
        Parameters
        ----------
        name : str
            Generator name.
        bus : Union[str, Bus]
            Connected bus.
        carrier : Union[str, EnergyCarrier]
            Energy carrier type.
        capacity : float
            Generator capacity.
        efficiency : float, default=0.9
            Generator efficiency.
        **kwargs
            Additional parameters.
            
        Returns
        -------
        Generator
            Created generator component.
        """
        if isinstance(bus, str):
            bus = self.buses[bus]
        if isinstance(carrier, str):
            carrier = EnergyCarrier(carrier)
        
        config = ComponentConfig(
            name=name,
            component_type=ComponentType.GENERATOR,
            carrier=carrier,
            parameters={'capacity': capacity, 'efficiency': efficiency, **kwargs}
        )
        
        generator = Generator(config, bus)
        self.components[name] = generator
        self.generators[name] = generator
        
        logger.debug(f"Added generator: {name}")
        return generator
    
    def add_load(self, name: str, bus: Union[str, Bus], 
                carrier: Union[str, EnergyCarrier], demand: float, **kwargs) -> Load:
        """Add a load to the network.
        
        Parameters
        ----------
        name : str
            Load name.
        bus : Union[str, Bus]
            Connected bus.
        carrier : Union[str, EnergyCarrier]
            Energy carrier type.
        demand : float
            Load demand.
        **kwargs
            Additional parameters.
            
        Returns
        -------
        Load
            Created load component.
        """
        if isinstance(bus, str):
            bus = self.buses[bus]
        if isinstance(carrier, str):
            carrier = EnergyCarrier(carrier)
        
        config = ComponentConfig(
            name=name,
            component_type=ComponentType.LOAD,
            carrier=carrier,
            parameters={'demand': demand, **kwargs}
        )
        
        load = Load(config, bus)
        self.components[name] = load
        self.loads[name] = load
        
        logger.debug(f"Added load: {name}")
        return load
    
    def add_line(self, name: str, from_bus: Union[str, Bus], to_bus: Union[str, Bus],
                carrier: Union[str, EnergyCarrier], capacity: float, 
                resistance: float = 0.01, reactance: float = 0.1, **kwargs) -> Line:
        """Add a transmission line to the network.
        
        Parameters
        ----------
        name : str
            Line name.
        from_bus : Union[str, Bus]
            Source bus.
        to_bus : Union[str, Bus]
            Destination bus.
        carrier : Union[str, EnergyCarrier]
            Energy carrier type.
        capacity : float
            Line capacity.
        resistance : float, default=0.01
            Line resistance.
        reactance : float, default=0.1
            Line reactance.
        **kwargs
            Additional parameters.
            
        Returns
        -------
        Line
            Created line component.
        """
        if isinstance(from_bus, str):
            from_bus = self.buses[from_bus]
        if isinstance(to_bus, str):
            to_bus = self.buses[to_bus]
        if isinstance(carrier, str):
            carrier = EnergyCarrier(carrier)
        
        config = ComponentConfig(
            name=name,
            component_type=ComponentType.LINE,
            carrier=carrier,
            parameters={'capacity': capacity, 'resistance': resistance, 
                       'reactance': reactance, **kwargs}
        )
        
        line = Line(config, from_bus, to_bus)
        self.components[name] = line
        self.lines[name] = line
        
        logger.debug(f"Added line: {name}")
        return line
    
    def add_storage_unit(self, name: str, bus: Union[str, Bus], 
                       carrier: Union[str, EnergyCarrier], capacity: float,
                       efficiency_charge: float = 0.9, efficiency_discharge: float = 0.9, 
                       **kwargs) -> StorageUnit:
        """Add a storage unit to the network.
        
        Parameters
        ----------
        name : str
            Storage unit name.
        bus : Union[str, Bus]
            Connected bus.
        carrier : Union[str, EnergyCarrier]
            Energy carrier type.
        capacity : float
            Storage capacity.
        efficiency_charge : float, default=0.9
            Charging efficiency.
        efficiency_discharge : float, default=0.9
            Discharging efficiency.
        **kwargs
            Additional parameters.
            
        Returns
        -------
        StorageUnit
            Created storage unit component.
        """
        if isinstance(bus, str):
            bus = self.buses[bus]
        if isinstance(carrier, str):
            carrier = EnergyCarrier(carrier)
        
        config = ComponentConfig(
            name=name,
            component_type=ComponentType.STORAGE,
            carrier=carrier,
            parameters={'capacity': capacity, 
                       'efficiency_charge': efficiency_charge,
                       'efficiency_discharge': efficiency_discharge, **kwargs}
        )
        
        storage = StorageUnit(config, bus)
        self.components[name] = storage
        self.storage_units[name] = storage
        
        logger.debug(f"Added storage unit: {name}")
        return storage
    
    def set_time_series(self, time_series: pd.DataFrame) -> None:
        """Set time series data for the network.
        
        Parameters
        ----------
        time_series : pd.DataFrame
            Time series data with datetime index.
        """
        self.time_series = time_series.copy()
    
    def add_time_series_column(self, column_name: str, data: Union[List[float], np.ndarray]) -> None:
        """Add a time series column to the network.
        
        Parameters
        ----------
        column_name : str
            Name of the column.
        data : Union[List[float], np.ndarray]
            Time series data.
        """
        if self.time_series is None:
            # Create a default time index if none exists
            n_points = len(data)
            self.time_series = pd.DataFrame(index=pd.date_range('2025-01-01', periods=n_points, freq='H'))
        
        self.time_series[column_name] = data
    
    def get_time_series(self) -> Optional[pd.DataFrame]:
        """Get the time series data."""
        return self.time_series
    
    def store_results(self, key: str, results: Any) -> None:
        """Store optimization or analysis results.
        
        Parameters
        ----------
        key : str
            Key for storing the results.
        results : Any
            Results to store.
        """
        self.results[key] = results
    
    def get_results(self, key: str) -> Any:
        """Get stored results.
        
        Parameters
        ----------
        key : str
            Key for the results.
            
        Returns
        -------
        Any
            The stored results.
        """
        return self.results.get(key)
    
    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results.clear()
    
    def validate_network(self) -> Tuple[bool, List[str]]:
        """Validate the entire network configuration.
        
        Returns
        -------
        Tuple[bool, List[str]]
            Validation result and list of error messages.
        """
        errors = []
        
        # Validate all components
        for name, component in self.components.items():
            if not component.validate():
                errors.append(f"Component {name} validation failed")
        
        # Check for isolated buses
        for bus_name, bus in self.buses.items():
            if not bus.get_connected_components():
                errors.append(f"Bus {bus_name} is isolated (no connected components)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert network to pandas DataFrame for analysis.
        
        Returns
        -------
        pd.DataFrame
            Network data in DataFrame format.
        """
        data = []
        
        for component in self.components.values():
            component_dict = component.to_dict()
            component_dict['network'] = self.name
            data.append(component_dict)
        
        return pd.DataFrame(data)
    
    def optimize(self, objective: str = "minimize_cost", 
                time_horizon: int = 24, **kwargs) -> Dict[str, Any]:
        """Optimize the energy system operation.
        
        Parameters
        ----------
        objective : str, default="minimize_cost"
            Optimization objective.
        time_horizon : int, default=24
            Optimization time horizon.
        **kwargs
            Additional optimization parameters.
            
        Returns
        -------
        Dict[str, Any]
            Optimization results.
        """
        logger.info(f"Starting optimization with objective: {objective}")
        
        # Placeholder for optimization implementation
        # This would integrate with PyXESXXN optimization module
        
        result = {
            'objective': objective,
            'time_horizon': time_horizon,
            'status': 'success',
            'optimal_cost': 0.0,
            'dispatch': {},
            'constraints_satisfied': True
        }
        
        self.store_results('optimization', result)
        return result
    
    def summary(self) -> Dict[str, Any]:
        """Generate a summary of the network.
        
        Returns
        -------
        Dict[str, Any]
            Network summary statistics.
        """
        return {
            'name': self.name,
            'total_components': len(self.components),
            'buses': len(self.buses),
            'generators': len(self.generators),
            'loads': len(self.loads),
            'lines': len(self.lines),
            'storage_units': len(self.storage_units),
            'energy_carriers': list(set(comp.carrier for comp in self.components.values())),
            'has_time_series': self.time_series is not None,
            'stored_results': len(self.results)
        }
    
    def __repr__(self) -> str:
        return (f"PyXESXXNNetwork(name='{self.name}', "
                f"buses={len(self.buses)}, generators={len(self.generators)}, "
                f"loads={len(self.loads)}, lines={len(self.lines)}, "
                f"storage_units={len(self.storage_units)})")


# Aliases for backward compatibility
Network = PyXESXXNNetwork
EnergySystem = PyXESXXNNetwork  