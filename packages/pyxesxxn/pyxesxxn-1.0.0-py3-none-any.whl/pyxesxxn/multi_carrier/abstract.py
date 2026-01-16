"""
Abstract interfaces for multi-carrier energy system components.

This module provides abstract base classes and interfaces that define the contract
for multi-carrier energy system components, enabling dependency injection and
testability while removing direct PyPSA dependencies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd


class EnergyCarrier(Enum):
    """Enumeration of energy carriers supported by PyXESXXN."""
    ELECTRICITY = "electricity"
    HEAT = "heat"
    HYDROGEN = "hydrogen"
    NATURAL_GAS = "natural_gas"
    BIOGAS = "biogas"
    SOLAR = "solar"
    WIND = "wind"
    HYDRO = "hydro"
    BIOMASS = "biomass"
    COAL = "coal"
    OIL = "oil"


class ConverterType(Enum):
    """Types of energy conversion devices."""
    ELECTROLYZER = "electrolyzer"
    FUEL_CELL = "fuel_cell"
    HEAT_PUMP = "heat_pump"
    CHP = "chp"
    BOILER = "boiler"
    TRANSFORMER = "transformer"


@dataclass
class ConverterConfig:
    """Configuration for energy conversion devices."""
    name: str
    converter_type: ConverterType
    input_carrier: EnergyCarrier
    output_carrier: EnergyCarrier
    efficiency: float
    capacity: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MultiCarrierConverter(ABC):
    """Abstract base class for multi-carrier energy converters."""
    
    def __init__(self, config: ConverterConfig):
        self.config = config
        self.name = config.name
        self.converter_type = config.converter_type
        self.input_carrier = config.input_carrier
        self.output_carrier = config.output_carrier
        self.efficiency = config.efficiency
        self.capacity = config.capacity
        self.parameters = config.parameters
        self.metadata = config.metadata
    
    @abstractmethod
    def convert(self, input_flow: float) -> float:
        """Convert input energy flow to output energy flow."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate converter configuration."""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert converter to dictionary representation."""
        return {
            'name': self.name,
            'type': self.converter_type.value,
            'input_carrier': self.input_carrier.value,
            'output_carrier': self.output_carrier.value,
            'efficiency': self.efficiency,
            'capacity': self.capacity,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


@dataclass
class EnergyFlow:
    """Data class representing energy flow between components."""
    from_component: str
    to_component: str
    carrier: EnergyCarrier
    flow_rate: float
    timestamp: pd.Timestamp
    metadata: Dict[str, Any] = field(default_factory=dict)


class EnergyHubInterface(ABC):
    """Abstract interface for energy hub models."""
    
    @abstractmethod
    def add_converter(self, converter: MultiCarrierConverter) -> None:
        """Add a converter to the energy hub."""
        pass
    
    @abstractmethod
    def add_energy_flow(self, from_component: str, to_component: str,
                       carrier: Union[str, EnergyCarrier], flow_rate: float,
                       timestamp: pd.Timestamp) -> None:
        """Add an energy flow record."""
        pass
    
    @abstractmethod
    def optimize(self, objective: str = "minimize_cost", 
                time_horizon: int = 24, **kwargs) -> Dict[str, Any]:
        """Optimize the energy hub operation."""
        pass
    
    @abstractmethod
    def calculate_efficiency(self) -> Dict[str, float]:
        """Calculate overall efficiency of the energy hub."""
        pass
    
    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        """Convert energy hub data to pandas DataFrame."""
        pass


@dataclass
class HubConfiguration:
    """Configuration for energy hub setup."""
    name: str
    location: str
    carriers: List[EnergyCarrier]
    capacity_limits: Dict[EnergyCarrier, float] = field(default_factory=dict)
    efficiency_targets: Dict[Tuple[EnergyCarrier, EnergyCarrier], float] = field(default_factory=dict)
    optimization_settings: Dict[str, Any] = field(default_factory=dict)


class OptimizationInterface(ABC):
    """Abstract interface for optimization models."""
    
    @abstractmethod
    def add_constraint(self, constraint: Any) -> None:
        """Add optimization constraint."""
        pass
    
    @abstractmethod
    def set_objective(self, objective: Any) -> None:
        """Set optimization objective function."""
        pass
    
    @abstractmethod
    def solve(self, solver: str = "glpk", **kwargs) -> Dict[str, Any]:
        """Solve the optimization problem."""
        pass


# Factory functions for dependency injection
def create_converter_factory() -> Dict[ConverterType, type]:
    """Create a factory mapping for converter types."""
    return {
        ConverterType.ELECTROLYZER: None,  # Will be implemented in converters module
        ConverterType.FUEL_CELL: None,
        ConverterType.HEAT_PUMP: None,
        ConverterType.CHP: None,
        ConverterType.BOILER: None,
        ConverterType.TRANSFORMER: None,
    }


def create_energy_hub_factory() -> Dict[str, type]:
    """Create a factory mapping for energy hub implementations."""
    return {
        'pyxesxxn': None,  # Native PyXESXXN implementation
        'pypsa': None,  # PyPSA-based implementation (for backward compatibility)
    }