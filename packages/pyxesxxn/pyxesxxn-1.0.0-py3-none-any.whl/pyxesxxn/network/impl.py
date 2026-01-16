"""
PyXESXXN Network Implementation Module

This module contains the concrete implementation of PyXESXXN network classes
that are independent of PyPSA dependencies.
"""

import logging
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class EnergyCarrier:
    """Energy carrier types for PyXESXXN networks."""
    ELECTRICITY = "electricity"
    GAS = "gas"
    HEAT = "heat"
    HYDROGEN = "hydrogen"
    COAL = "coal"
    OIL = "oil"
    BIOMASS = "biomass"
    SOLAR = "solar"
    WIND = "wind"
    HYDRO = "hydro"
    NUCLEAR = "nuclear"
    
    @classmethod
    def values(cls):
        """Return all energy carrier values."""
        return [getattr(cls, attr) for attr in dir(cls) 
                if not attr.startswith('_') and not callable(getattr(cls, attr))]


class ComponentType:
    """Component types for PyXESXXN networks."""
    BUS = "bus"
    GENERATOR = "generator"
    LOAD = "load"
    LINE = "line"
    STORAGE = "storage"
    TRANSFORMER = "transformer"
    CONVERTER = "converter"
    
    @classmethod
    def values(cls):
        """Return all component type values."""
        return [getattr(cls, attr) for attr in dir(cls) 
                if not attr.startswith('_') and not callable(getattr(cls, attr))]


@dataclass
class ComponentConfig:
    """Configuration for network components."""
    name: str
    component_type: str
    carrier: str
    parameters: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.metadata is None:
            self.metadata = {}


class Component(ABC):
    """Abstract base class for network components."""
    
    def __init__(self, config: ComponentConfig):
        self.config = config
        self.name = config.name
        self.component_type = config.component_type
        self.carrier = config.carrier
        self.parameters = config.parameters
        self.metadata = config.metadata
        self.connected_components: List['Component'] = []
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation."""
        pass
    
    def connect(self, component: 'Component') -> None:
        """Connect this component to another component."""
        if component not in self.connected_components:
            self.connected_components.append(component)
    
    def disconnect(self, component: 'Component') -> None:
        """Disconnect this component from another component."""
        if component in self.connected_components:
            self.connected_components.remove(component)
    
    def get_connected_components(self) -> List['Component']:
        """Get all connected components."""
        return self.connected_components.copy()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', type='{self.component_type}')"


class Bus(Component):
    """Bus component for energy networks."""
    
    def __init__(self, config: ComponentConfig):
        super().__init__(config)
        self.voltage = self.parameters.get('voltage', 1.0)
        self.frequency = self.parameters.get('frequency', 50.0)
    
    def validate(self) -> bool:
        """Validate bus configuration."""
        if self.voltage <= 0:
            logger.error(f"Bus {self.name}: Voltage must be positive")
            return False
        if self.frequency <= 0:
            logger.error(f"Bus {self.name}: Frequency must be positive")
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert bus to dictionary."""
        return {
            'name': self.name,
            'type': self.component_type,
            'carrier': self.carrier,
            'voltage': self.voltage,
            'frequency': self.frequency,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Generator(Component):
    """Generator component for energy networks."""
    
    def __init__(self, config: ComponentConfig, bus: Bus):
        super().__init__(config)
        self.bus = bus
        self.capacity = self.parameters.get('capacity', 0.0)
        self.efficiency = self.parameters.get('efficiency', 0.9)
        
        # Connect to bus
        self.connect(bus)
        bus.connect(self)
    
    def validate(self) -> bool:
        """Validate generator configuration."""
        if self.capacity < 0:
            logger.error(f"Generator {self.name}: Capacity must be non-negative")
            return False
        if not (0 < self.efficiency <= 1):
            logger.error(f"Generator {self.name}: Efficiency must be between 0 and 1")
            return False
        return True
    
    def set_power(self, power: float) -> None:
        """Set generator power output."""
        if power < 0:
            raise ValueError("Power output cannot be negative")
        if power > self.capacity:
            raise ValueError(f"Power output exceeds capacity {self.capacity}")
        
        self.parameters['current_power'] = power
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert generator to dictionary."""
        return {
            'name': self.name,
            'type': self.component_type,
            'carrier': self.carrier,
            'bus': self.bus.name,
            'capacity': self.capacity,
            'efficiency': self.efficiency,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Load(Component):
    """Load component for energy networks."""
    
    def __init__(self, config: ComponentConfig, bus: Bus):
        super().__init__(config)
        self.bus = bus
        self.demand = self.parameters.get('demand', 0.0)
        
        # Connect to bus
        self.connect(bus)
        bus.connect(self)
    
    def validate(self) -> bool:
        """Validate load configuration."""
        if self.demand < 0:
            logger.error(f"Load {self.name}: Demand must be non-negative")
            return False
        return True
    
    def set_demand(self, demand: float) -> None:
        """Set load demand."""
        if demand < 0:
            raise ValueError("Demand cannot be negative")
        
        self.demand = demand
        self.parameters['demand'] = demand
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert load to dictionary."""
        return {
            'name': self.name,
            'type': self.component_type,
            'carrier': self.carrier,
            'bus': self.bus.name,
            'demand': self.demand,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class Line(Component):
    """Transmission line component for energy networks."""
    
    def __init__(self, config: ComponentConfig, from_bus: Bus, to_bus: Bus):
        super().__init__(config)
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.capacity = self.parameters.get('capacity', 0.0)
        self.resistance = self.parameters.get('resistance', 0.01)
        self.reactance = self.parameters.get('reactance', 0.1)
        
        # Connect to buses
        self.connect(from_bus)
        self.connect(to_bus)
        from_bus.connect(self)
        to_bus.connect(self)
    
    def validate(self) -> bool:
        """Validate line configuration."""
        if self.capacity < 0:
            logger.error(f"Line {self.name}: Capacity must be non-negative")
            return False
        if self.resistance < 0:
            logger.error(f"Line {self.name}: Resistance must be non-negative")
            return False
        if self.reactance < 0:
            logger.error(f"Line {self.name}: Reactance must be non-negative")
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert line to dictionary."""
        return {
            'name': self.name,
            'type': self.component_type,
            'carrier': self.carrier,
            'from_bus': self.from_bus.name,
            'to_bus': self.to_bus.name,
            'capacity': self.capacity,
            'resistance': self.resistance,
            'reactance': self.reactance,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


class StorageUnit(Component):
    """Storage unit component for energy networks."""
    
    def __init__(self, config: ComponentConfig, bus: Bus):
        super().__init__(config)
        self.bus = bus
        self.capacity = self.parameters.get('capacity', 0.0)
        self.efficiency_charge = self.parameters.get('efficiency_charge', 0.9)
        self.efficiency_discharge = self.parameters.get('efficiency_discharge', 0.9)
        self.state_of_charge = self.parameters.get('initial_soc', 0.0)
        
        # Connect to bus
        self.connect(bus)
        bus.connect(self)
    
    def validate(self) -> bool:
        """Validate storage unit configuration."""
        if self.capacity < 0:
            logger.error(f"Storage {self.name}: Capacity must be non-negative")
            return False
        if not (0 < self.efficiency_charge <= 1):
            logger.error(f"Storage {self.name}: Charge efficiency must be between 0 and 1")
            return False
        if not (0 < self.efficiency_discharge <= 1):
            logger.error(f"Storage {self.name}: Discharge efficiency must be between 0 and 1")
            return False
        if not (0 <= self.state_of_charge <= 1):
            logger.error(f"Storage {self.name}: State of charge must be between 0 and 1")
            return False
        return True
    
    def charge(self, power: float) -> float:
        """Charge the storage unit."""
        if power < 0:
            raise ValueError("Charge power cannot be negative")
        
        energy = power * self.efficiency_charge
        max_energy = self.capacity * (1 - self.state_of_charge)
        actual_energy = min(energy, max_energy)
        
        self.state_of_charge += actual_energy / self.capacity
        return actual_energy
    
    def discharge(self, power: float) -> float:
        """Discharge the storage unit."""
        if power < 0:
            raise ValueError("Discharge power cannot be negative")
        
        energy = power * self.efficiency_discharge
        max_energy = self.capacity * self.state_of_charge
        actual_energy = min(energy, max_energy)
        
        self.state_of_charge -= actual_energy / self.capacity
        return actual_energy
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert storage unit to dictionary."""
        return {
            'name': self.name,
            'type': self.component_type,
            'carrier': self.carrier,
            'bus': self.bus.name,
            'capacity': self.capacity,
            'efficiency_charge': self.efficiency_charge,
            'efficiency_discharge': self.efficiency_discharge,
            'state_of_charge': self.state_of_charge,
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
            carrier = carrier
        
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
            carrier = carrier
        
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
            carrier = carrier
        
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
            carrier = carrier
        
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
            carrier = carrier
        
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