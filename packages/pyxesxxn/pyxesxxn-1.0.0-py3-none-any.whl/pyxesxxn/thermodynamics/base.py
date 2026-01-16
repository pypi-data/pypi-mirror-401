"""Base thermodynamic models and calculators.

This module provides base classes for thermodynamic calculations in energy systems.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, Tuple
import numpy as np


class ThermodynamicModel(ABC):
    """Abstract base class for thermodynamic models."""
    
    @abstractmethod
    def calculate_properties(self, temperature: float, pressure: float) -> Dict[str, float]:
        """Calculate thermodynamic properties at given conditions.
        
        Args:
            temperature: Temperature in Kelvin
            pressure: Pressure in Pascal
            
        Returns:
            Dictionary of thermodynamic properties
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model is available (e.g., dependencies installed)."""
        pass


class IdealGasModel(ThermodynamicModel):
    """Ideal gas model for thermodynamic calculations."""
    
    def __init__(self, gas_type: str, specific_heat_ratio: Optional[float] = None,
                 molar_mass: Optional[float] = None):
        """Initialize ideal gas model.
        
        Args:
            gas_type: Type of gas (e.g., 'hydrogen', 'natural_gas', 'air', 'co2')
            specific_heat_ratio: Specific heat ratio (gamma = cp/cv)
            molar_mass: Molar mass in kg/mol
        """
        self.gas_type = gas_type
        self.specific_heat_ratio = specific_heat_ratio
        self.molar_mass = molar_mass
        
    def calculate_properties(self, temperature: float, pressure: float) -> Dict[str, float]:
        """Calculate ideal gas properties."""
        # For now, return basic properties
        # In a real implementation, this would calculate density, enthalpy, etc.
        return {
            "temperature": temperature,
            "pressure": pressure,
            "gas_type": self.gas_type,
            "model": "ideal_gas"
        }
    
    def is_available(self) -> bool:
        """Ideal gas model is always available."""
        return True


class RealGasModel(ThermodynamicModel):
    """Real gas model using external libraries (CoolProp/REFPROP)."""
    
    def __init__(self, gas_type: str, backend: str = "HEOS"):
        """Initialize real gas model.
        
        Args:
            gas_type: Type of gas (e.g., 'hydrogen', 'natural_gas', 'air', 'co2')
            backend: Thermodynamic backend ('HEOS', 'REFPROP', etc.)
        """
        self.gas_type = gas_type
        self.backend = backend
        self._coolprop_available = False
        self._refprop_available = False
        
        # Try to import CoolProp
        try:
            import CoolProp
            self._coolprop_available = True
        except ImportError:
            pass
            
        # Try to import REFPROP (if available)
        try:
            import ctREFPROP
            self._refprop_available = True
        except ImportError:
            pass
    
    def calculate_properties(self, temperature: float, pressure: float) -> Dict[str, float]:
        """Calculate real gas properties using external library."""
        if not self.is_available():
            raise ModelNotAvailableError(
                f"Real gas model not available. Install CoolProp or REFPROP."
            )
        
        # This would be implemented with actual library calls
        # For now, return a placeholder
        return {
            "temperature": temperature,
            "pressure": pressure,
            "gas_type": self.gas_type,
            "model": "real_gas",
            "backend": self.backend,
            "density": 0.0,  # Placeholder
            "enthalpy": 0.0,  # Placeholder
            "entropy": 0.0,   # Placeholder
        }
    
    def is_available(self) -> bool:
        """Check if real gas model dependencies are installed."""
        return self._coolprop_available or self._refprop_available


class CompressionCalculator:
    """Calculator for gas compression work."""
    
    def __init__(self, gas_type: str, model_type: str = "simplified"):
        """Initialize compression calculator.
        
        Args:
            gas_type: Type of gas to compress
            model_type: Type of model to use ('simplified' or 'precise')
        """
        self.gas_type = gas_type
        self.model_type = model_type
        
        # Initialize appropriate model
        if model_type == "precise":
            self.model = RealGasModel(gas_type)
            if not self.model.is_available():
                # Fall back to simplified model
                self.model_type = "simplified"
                self.model = IdealGasModel(gas_type)
        else:
            self.model = IdealGasModel(gas_type)
    
    def calculate_compression_work(
        self,
        inlet_pressure: float,
        outlet_pressure: float,
        inlet_temperature: float,
        mass_flow_rate: float,
        efficiency: float = 0.85,
        stages: int = 1,
        intercooling: bool = False
    ) -> Dict[str, float]:
        """Calculate compression work.
        
        Args:
            inlet_pressure: Inlet pressure in Pa
            outlet_pressure: Outlet pressure in Pa
            inlet_temperature: Inlet temperature in K
            mass_flow_rate: Mass flow rate in kg/s
            efficiency: Isentropic efficiency (0-1)
            stages: Number of compression stages
            intercooling: Whether intercooling is used between stages
            
        Returns:
            Dictionary with compression work results
        """
        
        if self.model_type == "precise":
            return self._calculate_precise_compression_work(
                inlet_pressure, outlet_pressure, inlet_temperature,
                mass_flow_rate, efficiency, stages, intercooling
            )
        else:
            return self._calculate_simplified_compression_work(
                inlet_pressure, outlet_pressure, inlet_temperature,
                mass_flow_rate, efficiency, stages, intercooling
            )
    
    def _calculate_simplified_compression_work(
        self,
        inlet_pressure: float,
        outlet_pressure: float,
        inlet_temperature: float,
        mass_flow_rate: float,
        efficiency: float,
        stages: int,
        intercooling: bool
    ) -> Dict[str, float]:
        """Calculate compression work using simplified isentropic model."""
        # This is similar to the existing implementation in CompressionConverter
        # For hydrogen: gamma = 1.4, R = 4124.2 J/(kg·K)
        # For natural gas: gamma = 1.3, R = 518.3 J/(kg·K)
        
        gas_properties = {
            "hydrogen": {"gamma": 1.4, "R": 4124.2},
            "natural_gas": {"gamma": 1.3, "R": 518.3},
            "air": {"gamma": 1.4, "R": 287.1},
            "co2": {"gamma": 1.28, "R": 188.9},
        }
        
        if self.gas_type not in gas_properties:
            # Default to air properties
            props = gas_properties["air"]
        else:
            props = gas_properties[self.gas_type]
        
        gamma = props["gamma"]
        R = props["R"]
        
        # Compression ratio per stage
        total_compression_ratio = outlet_pressure / inlet_pressure
        stage_compression_ratio = total_compression_ratio ** (1 / stages)
        
        # Isentropic work per stage
        work_per_stage = (gamma / (gamma - 1)) * R * inlet_temperature * \
                        ((stage_compression_ratio ** ((gamma - 1) / gamma)) - 1)
        
        # Total isentropic work
        total_work = work_per_stage * stages
        
        # Actual work considering efficiency
        actual_work = total_work / efficiency
        
        # Power requirement
        power_required = mass_flow_rate * actual_work
        
        return {
            "power_required": power_required,
            "isentropic_work": total_work,
            "actual_work": actual_work,
            "compression_ratio": total_compression_ratio,
            "stage_compression_ratio": stage_compression_ratio,
            "efficiency": efficiency,
            "stages": stages,
            "intercooling": intercooling,
            "model": "simplified",
            "gas_type": self.gas_type
        }
    
    def _calculate_precise_compression_work(
        self,
        inlet_pressure: float,
        outlet_pressure: float,
        inlet_temperature: float,
        mass_flow_rate: float,
        efficiency: float,
        stages: int,
        intercooling: bool
    ) -> Dict[str, float]:
        """Calculate compression work using precise thermodynamic model."""
        # This would use CoolProp/REFPROP for precise calculations
        # For now, return simplified results with model type indicated
        result = self._calculate_simplified_compression_work(
            inlet_pressure, outlet_pressure, inlet_temperature,
            mass_flow_rate, efficiency, stages, intercooling
        )
        result["model"] = "precise"
        result["backend"] = self.model.backend
        
        return result


class GasProperties:
    """Gas property database and calculator."""
    
    def __init__(self):
        """Initialize gas properties database."""
        self._properties = self._load_default_properties()
    
    def _load_default_properties(self) -> Dict[str, Dict[str, float]]:
        """Load default gas properties."""
        return {
            "hydrogen": {
                "molar_mass": 0.002016,  # kg/mol
                "specific_heat_ratio": 1.4,
                "critical_temperature": 33.19,  # K
                "critical_pressure": 13.13e5,  # Pa
                "gas_constant": 4124.2,  # J/(kg·K)
            },
            "natural_gas": {
                "molar_mass": 0.01604,  # kg/mol (approx for methane)
                "specific_heat_ratio": 1.3,
                "critical_temperature": 190.56,  # K
                "critical_pressure": 45.99e5,  # Pa
                "gas_constant": 518.3,  # J/(kg·K)
            },
            "air": {
                "molar_mass": 0.02897,  # kg/mol
                "specific_heat_ratio": 1.4,
                "critical_temperature": 132.5,  # K
                "critical_pressure": 37.7e5,  # Pa
                "gas_constant": 287.1,  # J/(kg·K)
            },
            "co2": {
                "molar_mass": 0.04401,  # kg/mol
                "specific_heat_ratio": 1.28,
                "critical_temperature": 304.13,  # K
                "critical_pressure": 73.8e5,  # Pa
                "gas_constant": 188.9,  # J/(kg·K)
            },
        }
    
    def get_properties(self, gas_type: str) -> Dict[str, float]:
        """Get properties for a specific gas type."""
        if gas_type not in self._properties:
            raise GasPropertyError(f"Unknown gas type: {gas_type}")
        return self._properties[gas_type].copy()
    
    def add_custom_gas(self, name: str, properties: Dict[str, float]):
        """Add custom gas properties to the database."""
        self._properties[name] = properties.copy()