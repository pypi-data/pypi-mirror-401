"""
Spatial Load-Resource Matching for PyPSA.

This module provides algorithms for matching loads and resources spatially,
considering geographic constraints and optimization criteria.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod
import warnings

from .base import GeospatialProcessor


try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    HAS_GEOPANDAS = True
except ImportError:
    gpd = None
    Point = None
    Polygon = None
    HAS_GEOPANDAS = False


class SpatialLoadResourceMatcher(GeospatialProcessor):
    """Spatial matching engine for load-resource allocation."""
    
    def __init__(self, crs: str = "EPSG:4326", units: str = "degrees"):
        """Initialize spatial matcher.
        
        Parameters
        ----------
        crs : str
            Coordinate Reference System
        units : str
            Unit system
        """
        super().__init__(crs, units)
        self.matching_strategies = {
            'nearest': self._match_nearest,
            'capacity_weighted': self._match_capacity_weighted,
            'cost_optimized': self._match_cost_optimized
        }
    
    def match_loads_resources(self, 
                             loads: pd.DataFrame, 
                             resources: pd.DataFrame,
                             strategy: str = 'nearest',
                             max_distance: float = None,
                             **kwargs) -> pd.DataFrame:
        """Match loads to resources based on spatial criteria.
        
        Parameters
        ----------
        loads : pd.DataFrame
            Load data with coordinates and demand
        resources : pd.DataFrame
            Resource data with coordinates and capacity
        strategy : str
            Matching strategy ('nearest', 'capacity_weighted', 'cost_optimized')
        max_distance : float, optional
            Maximum allowed distance for matching
        
        Returns
        -------
        pd.DataFrame
            Matching results with load-resource pairs
        """
        if strategy not in self.matching_strategies:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        return self.matching_strategies[strategy](loads, resources, max_distance, **kwargs)
    
    def _match_nearest(self, loads: pd.DataFrame, resources: pd.DataFrame,
                      max_distance: float = None, **kwargs) -> pd.DataFrame:
        """Match each load to the nearest resource.
        
        Parameters
        ----------
        loads : pd.DataFrame
            Load data
        resources : pd.DataFrame
            Resource data
        max_distance : float, optional
            Maximum distance constraint
        
        Returns
        -------
        pd.DataFrame
            Nearest neighbor matches
        """
        matches = []
        
        for _, load in loads.iterrows():
            load_coords = (load.get('x', load.get('lon', 0)), 
                          load.get('y', load.get('lat', 0)))
            
            best_resource = None
            best_distance = float('inf')
            
            for _, resource in resources.iterrows():
                resource_coords = (resource.get('x', resource.get('lon', 0)), 
                                  resource.get('y', resource.get('lat', 0)))
                
                distance = self.calculate_distance(load_coords, resource_coords)
                
                if max_distance and distance > max_distance:
                    continue
                
                if distance < best_distance:
                    best_distance = distance
                    best_resource = resource
            
            if best_resource is not None:
                matches.append({
                    'load_id': load.get('id', load.name),
                    'resource_id': best_resource.get('id', best_resource.name),
                    'distance_km': best_distance,
                    'load_demand': load.get('demand', load.get('p_set', 0)),
                    'resource_capacity': best_resource.get('capacity', best_resource.get('p_nom', 0))
                })
        
        return pd.DataFrame(matches)
    
    def _match_capacity_weighted(self, loads: pd.DataFrame, resources: pd.DataFrame,
                                max_distance: float = None, **kwargs) -> pd.DataFrame:
        """Match loads to resources considering capacity constraints.
        
        Parameters
        ----------
        loads : pd.DataFrame
            Load data
        resources : pd.DataFrame
            Resource data
        max_distance : float, optional
            Maximum distance constraint
        
        Returns
        -------
        pd.DataFrame
            Capacity-weighted matches
        """
        # Simple greedy algorithm: assign loads to nearest resources
        # until capacity is exhausted, then move to next nearest
        matches = []
        
        # Create copy of resources to track remaining capacity
        resources_copy = resources.copy()
        resources_copy['remaining_capacity'] = resources_copy.get('capacity', resources_copy.get('p_nom', 0))
        
        # Sort loads by demand (largest first)
        loads_sorted = loads.sort_values(by='demand', ascending=False)
        
        for _, load in loads_sorted.iterrows():
            load_coords = (load.get('x', load.get('lon', 0)), 
                          load.get('y', load.get('lat', 0)))
            load_demand = load.get('demand', load.get('p_set', 0))
            
            # Find suitable resources with remaining capacity
            suitable_resources = resources_copy[resources_copy['remaining_capacity'] >= load_demand]
            
            if suitable_resources.empty:
                warnings.warn(f"No suitable resource found for load {load.get('id', load.name)}")
                continue
            
            # Find nearest suitable resource
            best_resource = None
            best_distance = float('inf')
            
            for _, resource in suitable_resources.iterrows():
                resource_coords = (resource.get('x', resource.get('lon', 0)), 
                                  resource.get('y', resource.get('lat', 0)))
                
                distance = self.calculate_distance(load_coords, resource_coords)
                
                if max_distance and distance > max_distance:
                    continue
                
                if distance < best_distance:
                    best_distance = distance
                    best_resource = resource
            
            if best_resource is not None:
                matches.append({
                    'load_id': load.get('id', load.name),
                    'resource_id': best_resource.get('id', best_resource.name),
                    'distance_km': best_distance,
                    'load_demand': load_demand,
                    'resource_capacity': best_resource.get('capacity', best_resource.get('p_nom', 0)),
                    'allocated_capacity': load_demand
                })
                
                # Update remaining capacity
                idx = resources_copy[resources_copy['id'] == best_resource['id']].index[0]
                resources_copy.loc[idx, 'remaining_capacity'] -= load_demand
        
        return pd.DataFrame(matches)
    
    def _match_cost_optimized(self, loads: pd.DataFrame, resources: pd.DataFrame,
                             max_distance: float = None, **kwargs) -> pd.DataFrame:
        """Optimize matching considering distance and cost factors.
        
        Parameters
        ----------
        loads : pd.DataFrame
            Load data
        resources : pd.DataFrame
            Resource data
        max_distance : float, optional
            Maximum distance constraint
        
        Returns
        -------
        pd.DataFrame
            Cost-optimized matches
        """
        # This is a simplified implementation
        # In practice, this would use optimization algorithms like linear programming
        
        # For now, use capacity-weighted matching with distance penalty
        matches = self._match_capacity_weighted(loads, resources, max_distance)
        
        # Add cost calculation based on distance
        if not matches.empty:
            matches['transport_cost'] = matches['distance_km'] * 0.1  # €/km/kW
            matches['total_cost'] = matches['allocated_capacity'] * matches['transport_cost']
        
        return matches
    
    def validate_matching(self, matches: pd.DataFrame, 
                         resources: pd.DataFrame) -> Dict[str, Any]:
        """Validate matching results for feasibility.
        
        Parameters
        ----------
        matches : pd.DataFrame
            Matching results
        resources : pd.DataFrame
            Original resource data
        
        Returns
        -------
        Dict[str, Any]
            Validation results
        """
        validation = {
            'total_load': matches['load_demand'].sum() if not matches.empty else 0,
            'total_capacity': resources['capacity'].sum() if 'capacity' in resources.columns else 0,
            'average_distance': matches['distance_km'].mean() if not matches.empty else 0,
            'max_distance': matches['distance_km'].max() if not matches.empty else 0,
            'unmatched_loads': 0,
            'capacity_utilization': 0
        }
        
        if validation['total_capacity'] > 0:
            validation['capacity_utilization'] = validation['total_load'] / validation['total_capacity']
        
        return validation