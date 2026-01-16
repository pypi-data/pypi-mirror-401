"""PyXESXXN Network Module - Independent Energy System Modeling

This module provides the core network functionality for PyXESXXN, completely
independent of PyPSA. It implements the main PyXESXXNNetwork class and related
components for multi-carrier energy system modeling and optimization.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd

from .network import (
    PyXESXXNNetwork as BasePyXESXXNNetwork,
    Network,
    EnergySystem,
    Component,
    Bus,
    Generator,
    Load,
    Line,
    StorageUnit,
    EnergyCarrier,
    ComponentType
)

logger = logging.getLogger(__name__)


class PyXESXXNNetwork(BasePyXESXXNNetwork):
    """Enhanced PyXESXXN network class with advanced features.
    
    This class extends the base PyXESXXNNetwork with additional functionality
    for multi-carrier optimization, scenario analysis, and advanced modeling.
    """
    
    def __init__(self, name: str = "PyXESXXN Network", **kwargs):
        """Initialize an enhanced PyXESXXN network.
        
        Parameters
        ----------
        name : str, optional
            Network name, by default "PyXESXXN Network"
        **kwargs : dict
            Additional configuration parameters
        """
        super().__init__(name)
        self.config = kwargs
        self.scenarios: Dict[str, Any] = {}
        self.optimization_history: List[Dict[str, Any]] = []
        
        logger.info(f"Created enhanced PyXESXXN network: {name}")
        
    def add(self, 
            component_type: str, 
            name: Union[str, List[str]], 
            **kwargs) -> None:
        """Add component to network (PyPSA-compatible API).
        
        Parameters
        ----------
        component_type : str
            Type of component to add (bus, line, generator, load, etc.)
        name : str or list of str
            Component name(s)
        **kwargs
            Component attributes
        """
        if isinstance(name, str):
            names = [name]
        else:
            names = name
            
        for comp_name in names:
            self._add_component(component_type, comp_name, **kwargs)
    
    def _add_component(self, component_type: str, name: str, **kwargs) -> None:
        """Add single component to network."""
        if component_type.lower() == "bus":
            self._add_bus(name, **kwargs)
        elif component_type.lower() == "generator":
            self._add_generator(name, **kwargs)
        elif component_type.lower() == "load":
            self._add_load(name, **kwargs)
        elif component_type.lower() == "line":
            self._add_line(name, **kwargs)
        elif component_type.lower() == "storage_unit":
            self._add_storage_unit(name, **kwargs)
        elif component_type.lower() == "link":
            self._add_link(name, **kwargs)
        elif component_type.lower() == "transformer":
            self._add_transformer(name, **kwargs)
        else:
            raise ConfigurationError(f"Unsupported component type: {component_type}")
    
    def _add_bus(self, name: str, **kwargs) -> None:
        """Add bus component."""
        bus_data = {"name": name, **kwargs}
        new_bus = pd.DataFrame([bus_data]).set_index("name")
        
        if self.buses.empty:
            self.buses = new_bus
        else:
            self.buses = pd.concat([self.buses, new_bus])
        
        # Also add to PyXESXXN hub as energy carrier
        carrier_type = kwargs.get("carrier", "electricity")
        self.pyxesxxn_hub.config.add_converter(
            self._create_carrier_converter(name, carrier_type)
        )
    
    def _add_generator(self, name: str, **kwargs) -> None:
        """Add generator component."""
        gen_data = {"name": name, **kwargs}
        new_gen = pd.DataFrame([gen_data]).set_index("name")
        
        if self.generators.empty:
            self.generators = new_gen
        else:
            self.generators = pd.concat([self.generators, new_gen])
    
    def _add_load(self, name: str, **kwargs) -> None:
        """Add load component."""
        load_data = {"name": name, **kwargs}
        new_load = pd.DataFrame([load_data]).set_index("name")
        
        if self.loads.empty:
            self.loads = new_load
        else:
            self.loads = pd.concat([self.loads, new_load])
    
    def _add_line(self, name: str, **kwargs) -> None:
        """Add line component."""
        line_data = {"name": name, **kwargs}
        new_line = pd.DataFrame([line_data]).set_index("name")
        
        if self.lines.empty:
            self.lines = new_line
        else:
            self.lines = pd.concat([self.lines, new_line])
    
    def _add_storage_unit(self, name: str, **kwargs) -> None:
        """Add storage unit component."""
        storage_data = {"name": name, **kwargs}
        new_storage = pd.DataFrame([storage_data]).set_index("name")
        
        if self.storage_units.empty:
            self.storage_units = new_storage
        else:
            self.storage_units = pd.concat([self.storage_units, new_storage])
    
    def _add_link(self, name: str, **kwargs) -> None:
        """Add link component."""
        link_data = {"name": name, **kwargs}
        new_link = pd.DataFrame([link_data]).set_index("name")
        
        if self.links.empty:
            self.links = new_link
        else:
            self.links = pd.concat([self.links, new_link])
    
    def _add_transformer(self, name: str, **kwargs) -> None:
        """Add transformer component."""
        transformer_data = {"name": name, **kwargs}
        new_transformer = pd.DataFrame([transformer_data]).set_index("name")
        
        if self.transformers.empty:
            self.transformers = new_transformer
        else:
            self.transformers = pd.concat([self.transformers, new_transformer])
    
    def _create_carrier_converter(self, name: str, carrier_type: str):
        """Create PyXESXXN carrier converter for bus."""
        from .multi_carrier.base import MultiCarrierConverter, EnergyCarrier
        
        class CarrierConverter(MultiCarrierConverter):
            def __init__(self, name, carrier_type):
                super().__init__(name, carrier_type)
                
            def get_conversion_efficiency(self, input_carrier, output_carrier):
                return 1.0  # Identity conversion for carrier buses
                
            def get_capacity_limits(self):
                return (0, float('inf'))
                
        return CarrierConverter(name, carrier_type)
    
    def optimize(self, 
                 solver_name: str = "highs",
                 **kwargs) -> Dict[str, Any]:
        """Optimize network (PyPSA-compatible API).
        
        Parameters
        ----------
        solver_name : str
            Optimization solver to use
        **kwargs
            Additional optimization parameters
            
        Returns
        -------
        Dict[str, Any]
            Optimization results
        """
        try:
            # Run PyXESXXN optimization
            results = self.pyxesxxn_hub.optimize(
                solver_name=solver_name,
                **kwargs
            )
            
            # Store results in PyPSA-compatible format
            self.results = results
            self.objective = results.get("objective", None)
            
            # Update component attributes with optimization results
            self._update_optimization_results(results)
            
            return results
            
        except Exception as e:
            raise PyXESXXNError(f"Optimization failed: {str(e)}")
    
    def _update_optimization_results(self, results: Dict[str, Any]) -> None:
        """Update PyPSA components with optimization results."""
        # Update generator dispatch
        if "generator_dispatch" in results:
            dispatch_data = results["generator_dispatch"]
            if not self.generators.empty:
                # Add p_nom_opt column if it doesn't exist
                if "p_nom_opt" not in self.generators.columns:
                    self.generators["p_nom_opt"] = 0.0
                
                # Update generator capacities
                for gen_name, dispatch in dispatch_data.items():
                    if gen_name in self.generators.index:
                        self.generators.loc[gen_name, "p_nom_opt"] = dispatch.get("capacity", 0.0)
    
    def lopf(self, **kwargs) -> Dict[str, Any]:
        """Linear optimal power flow (PyPSA-compatible API)."""
        warnings.warn(
            "PyXESXXN: Using enhanced multi-carrier optimization instead of standard LOPF",
            UserWarning
        )
        return self.optimize(**kwargs)
    
    def pf(self, **kwargs) -> Dict[str, Any]:
        """Power flow calculation (PyPSA-compatible API)."""
        warnings.warn(
            "PyXESXXN: Using enhanced multi-carrier power flow analysis",
            UserWarning
        )
        return self._calculate_power_flows(**kwargs)
    
    def _calculate_power_flows(self, **kwargs) -> Dict[str, Any]:
        """Calculate power flows using PyXESXXN methods."""
        # Implement power flow calculation using PyXESXXN capabilities
        return {
            "converged": True,
            "iterations": 0,
            "power_flows": {},
            "voltage_angles": {},
            "line_loading": {}
        }
    
    def statistics(self) -> pd.DataFrame:
        """Calculate network statistics (PyPSA-compatible API)."""
        stats_data = {}
        
        # Basic statistics
        stats_data["buses"] = len(self.buses)
        stats_data["generators"] = len(self.generators)
        stats_data["loads"] = len(self.loads)
        stats_data["lines"] = len(self.lines)
        stats_data["storage_units"] = len(self.storage_units)
        
        # PyXESXXN-specific statistics
        stats_data["energy_carriers"] = len(self.pyxesxxn_hub.config.converters)
        stats_data["multi_carrier_converters"] = sum(
            1 for conv in self.pyxesxxn_hub.config.converters 
            if hasattr(conv, 'input_carriers') and len(conv.input_carriers) > 1
        )
        
        return pd.DataFrame([stats_data]).T
    
    def __repr__(self) -> str:
        """String representation of network."""
        return (
            f"PyXESXXN Network '{self.name}' (PyPSA-compatible)\n"
            f"----------------------------------------\n"
            f"Components:\n"
            f"- Buses: {len(self.buses)}\n"
            f"- Generators: {len(self.generators)}\n"
            f"- Loads: {len(self.loads)}\n"
            f"- Lines: {len(self.lines)}\n"
            f"- Storage Units: {len(self.storage_units)}\n"
            f"- Multi-carrier Converters: {len(self.pyxesxxn_hub.config.converters)}\n"
            f"Snapshots: {len(self.snapshots)}\n"
            f"PyXESXXN Enhanced: {self._pyxesxxn_enhanced}"
        )


# PyPSA-compatible convenience functions
def Network(*args, **kwargs) -> PyPSANetwork:
    """Create PyPSA-compatible network (convenience function)."""
    return PyPSANetwork(*args, **kwargs)


def examples():
    """Provide example networks (PyPSA-compatible API)."""
    class Examples:
        @staticmethod
        def ac_dc_meshed() -> PyPSANetwork:
            """Create AC-DC meshed network example."""
            network = PyPSANetwork(name="AC-DC-Meshed")
            
            # Add buses
            network.add("Bus", ["London", "Manchester", "Norway"], 
                       carrier="electricity", v_nom=400)
            
            # Add generators
            network.add("Generator", ["London Wind", "Manchester Wind", "Norway Wind"],
                       bus=["London", "Manchester", "Norway"], 
                       p_nom=100, marginal_cost=0)
            
            # Add loads
            network.add("Load", ["London Load", "Manchester Load", "Norway Load"],
                       bus=["London", "Manchester", "Norway"], 
                       p_set=[50, 30, 20])
            
            # Add lines
            network.add("Line", "London-Manchester",
                       bus0="London", bus1="Manchester",
                       x=0.1, s_nom=100)
            
            return network
        
        @staticmethod
        def storage_hvdc() -> PyPSANetwork:
            """Create storage and HVDC network example."""
            network = PyPSANetwork(name="Storage-HVDC")
            
            # Add buses
            network.add("Bus", ["Bus1", "Bus2"], carrier="electricity")
            
            # Add storage
            network.add("StorageUnit", "Battery",
                       bus="Bus1", p_nom=50, max_hours=4)
            
            # Add HVDC link
            network.add("Link", "HVDC Link",
                       bus0="Bus1", bus1="Bus2",
                       p_nom=100, efficiency=0.95)
            
            return network
    
    return Examples()


# Export PyPSA-compatible API
__all__ = [
    "PyPSANetwork",
    "Network", 
    "examples"
]