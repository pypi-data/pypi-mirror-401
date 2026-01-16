"""Advanced network functionality for PyXESXXN - Python for eXtended Energy System Analysis.

This module provides advanced network operations including network merging, slicing,
scenario management, and optimization capabilities. The design is completely independent
of PyPSA and provides enhanced functionality for multi-carrier energy system analysis.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Union, Any, Tuple, Callable
from enum import Enum
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import json

from .network import PyXESXXNNetwork, Component, Bus, Generator, Load, Line, StorageUnit

logger = logging.getLogger(__name__)


class NetworkOperation(Enum):
    """Enumeration of network operations."""
    MERGE = "merge"
    SLICE = "slice"
    SCENARIO = "scenario"
    OPTIMIZE = "optimize"
    CLUSTER = "cluster"
    TRANSFORM = "transform"


class Scenario:
    """Scenario class for managing different network scenarios."""
    
    def __init__(self, name: str, weight: float = 1.0, metadata: Optional[Dict] = None) -> None:
        """Initialize a scenario.
        
        Parameters
        ----------
        name : str
            Scenario name.
        weight : float, default=1.0
            Scenario weight for optimization.
        metadata : Optional[Dict], default=None
            Scenario metadata.
        """
        self.name = name
        self.weight = weight
        self.metadata = metadata or {}
        self.network: Optional[PyXESXXNNetwork] = None
    
    def set_network(self, network: PyXESXXNNetwork) -> None:
        """Set the network for this scenario."""
        self.network = network
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scenario to dictionary."""
        return {
            'name': self.name,
            'weight': self.weight,
            'metadata': self.metadata,
            'has_network': self.network is not None
        }


class NetworkCollection:
    """Collection of networks for batch operations."""
    
    def __init__(self, name: str = "Network Collection") -> None:
        """Initialize a network collection.
        
        Parameters
        ----------
        name : str, default="Network Collection"
            Collection name.
        """
        self.name = name
        self.networks: Dict[str, PyXESXXNNetwork] = {}
        self.scenarios: Dict[str, Scenario] = {}
        self.operations: List[NetworkOperation] = []
    
    def add_network(self, name: str, network: PyXESXXNNetwork) -> None:
        """Add a network to the collection.
        
        Parameters
        ----------
        name : str
            Network identifier.
        network : PyXESXXNNetwork
            Network to add.
        """
        if name in self.networks:
            raise ValueError(f"Network with name '{name}' already exists")
        self.networks[name] = network
        logger.info(f"Added network '{name}' to collection")
    
    def add_scenario(self, scenario: Scenario) -> None:
        """Add a scenario to the collection.
        
        Parameters
        ----------
        scenario : Scenario
            Scenario to add.
        """
        if scenario.name in self.scenarios:
            raise ValueError(f"Scenario '{scenario.name}' already exists")
        self.scenarios[scenario.name] = scenario
        logger.info(f"Added scenario '{scenario.name}' to collection")
    
    def merge_networks(self, network_names: List[str], merged_name: str, 
                      conflict_resolution: str = "raise") -> PyXESXXNNetwork:
        """Merge multiple networks into a single network.
        
        Parameters
        ----------
        network_names : List[str]
            Names of networks to merge.
        merged_name : str
            Name for the merged network.
        conflict_resolution : str, default="raise"
            How to handle conflicts: "raise", "overwrite", "rename"
            
        Returns
        -------
        PyXESXXNNetwork
            Merged network.
        """
        if not network_names:
            raise ValueError("No networks specified for merging")
        
        # Start with first network
        first_network = self.networks[network_names[0]]
        merged_network = PyXESXXNNetwork(name=merged_name)
        
        # Copy components from first network
        self._copy_network_components(first_network, merged_network)
        
        # Merge additional networks
        for network_name in network_names[1:]:
            network = self.networks[network_name]
            self._merge_single_network(merged_network, network, conflict_resolution)
        
        self.operations.append(NetworkOperation.MERGE)
        logger.info(f"Merged {len(network_names)} networks into '{merged_name}'")
        return merged_network
    
    def _copy_network_components(self, source: PyXESXXNNetwork, target: PyXESXXNNetwork) -> None:
        """Copy components from source to target network."""
        # Copy buses
        for bus_name, bus in source.buses.items():
            target.add_bus(bus_name, bus.carrier, **bus.parameters)
        
        # Copy other components
        for component_dict in source.to_dataframe().to_dict('records'):
            if component_dict['type'] == 'generator':
                target.add_generator(
                    component_dict['name'],
                    component_dict['bus'],
                    component_dict['carrier'],
                    component_dict['parameters'].get('capacity', 0),
                    **component_dict['parameters']
                )
            elif component_dict['type'] == 'load':
                target.add_load(
                    component_dict['name'],
                    component_dict['bus'],
                    component_dict['carrier'],
                    component_dict['parameters'].get('demand', 0),
                    **component_dict['parameters']
                )
            elif component_dict['type'] == 'line':
                target.add_line(
                    component_dict['name'],
                    component_dict['from_bus'],
                    component_dict['to_bus'],
                    component_dict['carrier'],
                    component_dict['parameters'].get('capacity', 0),
                    **component_dict['parameters']
                )
            elif component_dict['type'] == 'storage':
                target.add_storage_unit(
                    component_dict['name'],
                    component_dict['bus'],
                    component_dict['carrier'],
                    component_dict['parameters'].get('capacity', 0),
                    **component_dict['parameters']
                )
    
    def _merge_single_network(self, target: PyXESXXNNetwork, source: PyXESXXNNetwork, 
                            conflict_resolution: str) -> None:
        """Merge a single network into the target network."""
        for component_dict in source.to_dataframe().to_dict('records'):
            component_name = component_dict['name']
            
            # Handle conflicts
            if component_name in target.components:
                if conflict_resolution == "raise":
                    raise ValueError(f"Component '{component_name}' already exists")
                elif conflict_resolution == "overwrite":
                    # Remove existing component
                    self._remove_component(target, component_name)
                elif conflict_resolution == "rename":
                    # Generate unique name
                    counter = 1
                    new_name = f"{component_name}_{counter}"
                    while new_name in target.components:
                        counter += 1
                        new_name = f"{component_name}_{counter}"
                    component_dict['name'] = new_name
            
            # Add component
            self._add_component_from_dict(target, component_dict)
    
    def _remove_component(self, network: PyXESXXNNetwork, component_name: str) -> None:
        """Remove a component from the network."""
        if component_name in network.components:
            component = network.components[component_name]
            
            # Remove from specific component dictionaries
            if component_name in network.buses:
                del network.buses[component_name]
            elif component_name in network.generators:
                del network.generators[component_name]
            elif component_name in network.loads:
                del network.loads[component_name]
            elif component_name in network.lines:
                del network.lines[component_name]
            elif component_name in network.storage_units:
                del network.storage_units[component_name]
            
            del network.components[component_name]
    
    def _add_component_from_dict(self, network: PyXESXXNNetwork, component_dict: Dict) -> None:
        """Add a component to the network from dictionary."""
        if component_dict['type'] == 'bus':
            network.add_bus(
                component_dict['name'],
                component_dict['carrier'],
                **component_dict['parameters']
            )
        elif component_dict['type'] == 'generator':
            network.add_generator(
                component_dict['name'],
                component_dict['bus'],
                component_dict['carrier'],
                component_dict['parameters'].get('capacity', 0),
                **component_dict['parameters']
            )
        elif component_dict['type'] == 'load':
            network.add_load(
                component_dict['name'],
                component_dict['bus'],
                component_dict['carrier'],
                component_dict['parameters'].get('demand', 0),
                **component_dict['parameters']
            )
        elif component_dict['type'] == 'line':
            network.add_line(
                component_dict['name'],
                component_dict['from_bus'],
                component_dict['to_bus'],
                component_dict['carrier'],
                component_dict['parameters'].get('capacity', 0),
                **component_dict['parameters']
            )
        elif component_dict['type'] == 'storage':
            network.add_storage_unit(
                component_dict['name'],
                component_dict['bus'],
                component_dict['carrier'],
                component_dict['parameters'].get('capacity', 0),
                **component_dict['parameters']
            )
    
    def slice_network(self, network_name: str, component_names: List[str], 
                     slice_name: str = None) -> PyXESXXNNetwork:
        """Create a slice of a network containing only specified components.
        
        Parameters
        ----------
        network_name : str
            Name of the network to slice.
        component_names : List[str]
            Names of components to include in the slice.
        slice_name : str, optional
            Name for the sliced network.
            
        Returns
        -------
        PyXESXXNNetwork
            Sliced network.
        """
        if network_name not in self.networks:
            raise ValueError(f"Network '{network_name}' not found")
        
        source_network = self.networks[network_name]
        slice_name = slice_name or f"{network_name}_slice"
        sliced_network = PyXESXXNNetwork(name=slice_name)
        
        # Add specified components
        for component_name in component_names:
            if component_name not in source_network.components:
                logger.warning(f"Component '{component_name}' not found in network")
                continue
            
            component = source_network.components[component_name]
            component_dict = component.to_dict()
            self._add_component_from_dict(sliced_network, component_dict)
        
        self.operations.append(NetworkOperation.SLICE)
        logger.info(f"Created slice of network '{network_name}' with {len(component_names)} components")
        return sliced_network
    
    def optimize_scenarios(self, objective: str = "minimize_cost", 
                          time_horizon: int = 24) -> Dict[str, Any]:
        """Optimize all scenarios in the collection.
        
        Parameters
        ----------
        objective : str, default="minimize_cost"
            Optimization objective.
        time_horizon : int, default=24
            Optimization time horizon.
            
        Returns
        -------
        Dict[str, Any]
            Optimization results for each scenario.
        """
        results = {}
        
        for scenario_name, scenario in self.scenarios.items():
            if scenario.network is None:
                logger.warning(f"Scenario '{scenario_name}' has no network assigned")
                continue
            
            result = scenario.network.optimize(objective, time_horizon)
            result['scenario_weight'] = scenario.weight
            results[scenario_name] = result
        
        self.operations.append(NetworkOperation.OPTIMIZE)
        logger.info(f"Optimized {len(results)} scenarios")
        return results
    
    def export_collection(self, export_path: Union[str, Path]) -> None:
        """Export the network collection to a file.
        
        Parameters
        ----------
        export_path : Union[str, Path]
            Path for export.
        """
        export_data = {
            'name': self.name,
            'networks': {},
            'scenarios': {},
            'operations': [op.value for op in self.operations]
        }
        
        # Export network summaries
        for net_name, network in self.networks.items():
            export_data['networks'][net_name] = network.summary()
        
        # Export scenario summaries
        for scenario_name, scenario in self.scenarios.items():
            export_data['scenarios'][scenario_name] = scenario.to_dict()
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Exported network collection to {export_path}")
    
    def summary(self) -> Dict[str, Any]:
        """Generate a summary of the network collection."""
        return {
            'name': self.name,
            'total_networks': len(self.networks),
            'total_scenarios': len(self.scenarios),
            'operations_performed': [op.value for op in self.operations],
            'network_names': list(self.networks.keys()),
            'scenario_names': list(self.scenarios.keys())
        }


class AdvancedNetwork(PyXESXXNNetwork):
    """Advanced network class with enhanced functionality.
    
    This class extends PyXESXXNNetwork with advanced features like scenario management,
    network transformations, and optimization capabilities.
    """
    
    def __init__(self, name: str = "Advanced PyXESXXN Network") -> None:
        """Initialize an advanced network.
        
        Parameters
        ----------
        name : str, default="Advanced PyXESXXN Network"
            Network name.
        """
        super().__init__(name)
        self.scenarios: Dict[str, Scenario] = {}
        self.transformations: List[Callable] = []
        self.optimization_history: List[Dict] = []
    
    def add_scenario(self, scenario_name: str, weight: float = 1.0, 
                    metadata: Optional[Dict] = None) -> Scenario:
        """Add a scenario to the network.
        
        Parameters
        ----------
        scenario_name : str
            Scenario name.
        weight : float, default=1.0
            Scenario weight.
        metadata : Optional[Dict], default=None
            Scenario metadata.
            
        Returns
        -------
        Scenario
            Created scenario.
        """
        scenario = Scenario(scenario_name, weight, metadata)
        scenario.set_network(self)
        self.scenarios[scenario_name] = scenario
        logger.info(f"Added scenario '{scenario_name}' to network")
        return scenario
    
    def apply_transformation(self, transformation: Callable, *args, **kwargs) -> None:
        """Apply a transformation to the network.
        
        Parameters
        ----------
        transformation : Callable
            Transformation function.
        *args
            Arguments for the transformation.
        **kwargs
            Keyword arguments for the transformation.
        """
        transformation(self, *args, **kwargs)
        self.transformations.append(transformation)
        logger.info(f"Applied transformation: {transformation.__name__}")
    
    def cluster_components(self, component_type: str, clustering_method: str = "kmeans",
                          n_clusters: int = 3) -> Dict[str, Any]:
        """Cluster components of a specific type.
        
        Parameters
        ----------
        component_type : str
            Type of components to cluster.
        clustering_method : str, default="kmeans"
            Clustering method.
        n_clusters : int, default=3
            Number of clusters.
            
        Returns
        -------
        Dict[str, Any]
            Clustering results.
        """
        components = getattr(self, f"{component_type}s", {})
        if not components:
            raise ValueError(f"No {component_type} components found")
        
        # Extract features for clustering
        features = []
        component_names = []
        
        for name, component in components.items():
            features.append(list(component.parameters.values()))
            component_names.append(name)
        
        # Simple clustering implementation (placeholder)
        # In practice, this would use scikit-learn or similar
        clusters = {}
        for i, name in enumerate(component_names):
            cluster_id = i % n_clusters
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(name)
        
        result = {
            'method': clustering_method,
            'n_clusters': n_clusters,
            'clusters': clusters,
            'component_type': component_type
        }
        
        self.store_results('clustering', result)
        logger.info(f"Clustered {len(components)} {component_type} components into {n_clusters} clusters")
        return result
    
    def optimize_with_scenarios(self, objective: str = "minimize_cost",
                               time_horizon: int = 24) -> Dict[str, Any]:
        """Optimize the network considering all scenarios.
        
        Parameters
        ----------
        objective : str, default="minimize_cost"
            Optimization objective.
        time_horizon : int, default=24
            Optimization time horizon.
            
        Returns
        -------
        Dict[str, Any]
            Weighted optimization results.
        """
        if not self.scenarios:
            return self.optimize(objective, time_horizon)
        
        # Weighted optimization across scenarios
        weighted_results = {
            'objective': objective,
            'time_horizon': time_horizon,
            'scenario_results': {},
            'weighted_cost': 0.0
        }
        
        total_weight = sum(scenario.weight for scenario in self.scenarios.values())
        
        for scenario_name, scenario in self.scenarios.items():
            result = self.optimize(objective, time_horizon)
            weighted_results['scenario_results'][scenario_name] = result
            
            # Apply scenario weight
            weighted_cost = result.get('optimal_cost', 0) * scenario.weight / total_weight
            weighted_results['weighted_cost'] += weighted_cost
        
        self.optimization_history.append(weighted_results)
        self.store_results('weighted_optimization', weighted_results)
        
        logger.info(f"Optimized network with {len(self.scenarios)} scenarios")
        return weighted_results
    
    def get_transformation_history(self) -> List[Dict]:
        """Get the history of applied transformations."""
        return [
            {
                'transformation': trans.__name__,
                'module': trans.__module__
            }
            for trans in self.transformations
        ]
    
    def summary(self) -> Dict[str, Any]:
        """Generate an enhanced summary of the network."""
        base_summary = super().summary()
        base_summary.update({
            'scenarios': len(self.scenarios),
            'transformations_applied': len(self.transformations),
            'optimization_runs': len(self.optimization_history),
            'scenario_names': list(self.scenarios.keys())
        })
        return base_summary


# Utility functions for network operations

def create_network(name: str = None) -> PyXESXXNNetwork:
    """Create a new PyXESXXN network.
    
    Parameters
    ----------
    name : str, optional
        Name of the network. If None, uses default name.
        
    Returns
    -------
    PyXESXXNNetwork
        Newly created network.
    """
    return PyXESXXNNetwork(name=name or "PyXESXXN Network")


def convert_network(network: PyXESXXNNetwork, target_format: str = "standard") -> PyXESXXNNetwork:
    """Convert a network to a different format or representation.
    
    Parameters
    ----------
    network : PyXESXXNNetwork
        Network to convert.
    target_format : str, default="standard"
        Target format for conversion.
        
    Returns
    -------
    PyXESXXNNetwork
        Converted network.
    """
    # For now, return the same network as a placeholder
    # In a real implementation, this would convert between different formats
    return network


def create_network_from_dict(network_dict: Dict) -> PyXESXXNNetwork:
    """Create a network from a dictionary representation.
    
    Parameters
    ----------
    network_dict : Dict
        Dictionary containing network data.
        
    Returns
    -------
    PyXESXXNNetwork
        Created network.
    """
    network = PyXESXXNNetwork(name=network_dict.get('name', 'Imported Network'))
    
    # Add components from dictionary
    for component_data in network_dict.get('components', []):
        if component_data['type'] == 'bus':
            network.add_bus(component_data['name'], component_data['carrier'], 
                          **component_data.get('parameters', {}))
        elif component_data['type'] == 'generator':
            network.add_generator(component_data['name'], component_data['bus'],
                                 component_data['carrier'], component_data['parameters'].get('capacity', 0),
                                 **component_data.get('parameters', {}))
        elif component_data['type'] == 'load':
            network.add_load(component_data['name'], component_data['bus'],
                           component_data['carrier'], component_data['parameters'].get('demand', 0),
                           **component_data.get('parameters', {}))
        elif component_data['type'] == 'line':
            network.add_line(component_data['name'], component_data['from_bus'],
                           component_data['to_bus'], component_data['carrier'],
                           component_data['parameters'].get('capacity', 0),
                           **component_data.get('parameters', {}))
        elif component_data['type'] == 'storage':
            network.add_storage_unit(component_data['name'], component_data['bus'],
                                   component_data['carrier'], component_data['parameters'].get('capacity', 0),
                                   **component_data.get('parameters', {}))
    
    return network


def compare_networks(network1: PyXESXXNNetwork, network2: PyXESXXNNetwork) -> Dict[str, Any]:
    """Compare two networks and identify differences.
    
    Parameters
    ----------
    network1 : PyXESXXNNetwork
        First network.
    network2 : PyXESXXNNetwork
        Second network.
        
    Returns
    -------
    Dict[str, Any]
        Comparison results.
    """
    comparison = {
        'networks': [network1.name, network2.name],
        'component_differences': {},
        'parameter_differences': {},
        'is_identical': True
    }
    
    # Compare component counts
    for comp_type in ['buses', 'generators', 'loads', 'lines', 'storage_units']:
        count1 = len(getattr(network1, comp_type, {}))
        count2 = len(getattr(network2, comp_type, {}))
        
        if count1 != count2:
            comparison['component_differences'][comp_type] = {
                'network1': count1,
                'network2': count2
            }
            comparison['is_identical'] = False
    
    # Compare parameter values (simplified)
    # In practice, this would do a detailed parameter-by-parameter comparison
    
    return comparison


# Example transformation functions

def scale_network_capacity(network: PyXESXXNNetwork, scale_factor: float) -> None:
    """Scale all component capacities by a factor.
    
    Parameters
    ----------
    network : PyXESXXNNetwork
        Network to transform.
    scale_factor : float
        Scaling factor.
    """
    for component in network.components.values():
        if 'capacity' in component.parameters:
            component.parameters['capacity'] *= scale_factor


def add_redundant_lines(network: PyXESXXNNetwork, redundancy_factor: float = 1.5) -> None:
    """Add redundant transmission lines for reliability.
    
    Parameters
    ----------
    network : PyXESXXNNetwork
        Network to transform.
    redundancy_factor : float, default=1.5
        Redundancy factor for line capacities.
    """
    for line_name, line in network.lines.items():
        if 'capacity' in line.parameters:
            line.parameters['capacity'] *= redundancy_factor