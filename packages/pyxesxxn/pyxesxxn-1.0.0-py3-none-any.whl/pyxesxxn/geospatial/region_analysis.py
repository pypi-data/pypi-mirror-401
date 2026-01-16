"""
Region Analysis Module for PyPSA.

This module provides regional analysis capabilities including:
- Regional partitioning and aggregation
- Load and generation analysis by region
- Regional constraint management
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod
import warnings

from .base import GeospatialProcessor


try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon, MultiPolygon
    HAS_GEOPANDAS = True
except ImportError:
    gpd = None
    Point = None
    Polygon = None
    MultiPolygon = None
    HAS_GEOPANDAS = False


class RegionAnalyzer(GeospatialProcessor):
    """Regional analysis engine for PyPSA networks."""
    
    def __init__(self, crs: str = "EPSG:4326", units: str = "degrees"):
        """Initialize region analyzer.
        
        Parameters
        ----------
        crs : str
            Coordinate Reference System
        units : str
            Unit system
        """
        super().__init__(crs, units)
        self.regions = {}
        self.regional_data = {}
    
    def define_regions(self, regions: Dict[str, Any]) -> None:
        """Define regions for analysis.
        
        Parameters
        ----------
        regions : Dict[str, Any]
            Region definitions with boundaries and metadata
        """
        self.regions = regions
        
        # Validate region definitions
        for region_id, region_data in regions.items():
            if 'boundary' not in region_data:
                raise ValueError(f"Region {region_id} must have 'boundary' defined")
    
    def assign_buses_to_regions(self, network) -> pd.DataFrame:
        """Assign network buses to defined regions.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        
        Returns
        -------
        pd.DataFrame
            Bus-region assignments
        """
        if not self.regions:
            raise ValueError("No regions defined. Call define_regions() first.")
        
        bus_assignments = []
        
        for bus_id, bus_data in network.buses.iterrows():
            bus_coords = (bus_data.get('x', 0), bus_data.get('y', 0))
            
            assigned_region = None
            for region_id, region_data in self.regions.items():
                if self._point_in_region(bus_coords, region_data['boundary']):
                    assigned_region = region_id
                    break
            
            bus_assignments.append({
                'bus_id': bus_id,
                'region': assigned_region,
                'x': bus_coords[0],
                'y': bus_coords[1]
            })
        
        return pd.DataFrame(bus_assignments)
    
    def _point_in_region(self, point: Tuple[float, float], 
                        boundary: Any) -> bool:
        """Check if point is within region boundary.
        
        Parameters
        ----------
        point : Tuple[float, float]
            Point coordinates
        boundary : Any
            Region boundary definition
        
        Returns
        -------
        bool
            True if point is within boundary
        """
        # Simplified implementation - in practice would use proper geometry operations
        if isinstance(boundary, (list, tuple)) and len(boundary) == 4:
            # Assume boundary is [min_x, min_y, max_x, max_y]
            min_x, min_y, max_x, max_y = boundary
            return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y
        
        # For complex boundaries, would use shapely geometry operations
        return True  # Placeholder
    
    def analyze_regional_loads(self, network, bus_assignments: pd.DataFrame) -> pd.DataFrame:
        """Analyze load distribution by region.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        bus_assignments : pd.DataFrame
            Bus-region assignments
        
        Returns
        -------
        pd.DataFrame
            Regional load analysis
        """
        regional_loads = {}
        
        for region_id in self.regions:
            # Get buses in this region
            region_buses = bus_assignments[bus_assignments['region'] == region_id]['bus_id'].tolist()
            
            # Calculate total load in region
            total_load = 0
            for bus_id in region_buses:
                # Find loads connected to this bus
                bus_loads = network.loads[network.loads.bus == bus_id]
                if not bus_loads.empty:
                    total_load += bus_loads['p_set'].sum()
            
            regional_loads[region_id] = {
                'total_load_mw': total_load,
                'num_buses': len(region_buses),
                'num_loads': len(network.loads[network.loads.bus.isin(region_buses)])
            }
        
        return pd.DataFrame.from_dict(regional_loads, orient='index')
    
    def analyze_regional_generation(self, network, bus_assignments: pd.DataFrame) -> pd.DataFrame:
        """Analyze generation capacity by region.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        bus_assignments : pd.DataFrame
            Bus-region assignments
        
        Returns
        -------
        pd.DataFrame
            Regional generation analysis
        """
        regional_generation = {}
        
        for region_id in self.regions:
            # Get buses in this region
            region_buses = bus_assignments[bus_assignments['region'] == region_id]['bus_id'].tolist()
            
            # Calculate generation capacity in region
            total_capacity = 0
            renewable_capacity = 0
            
            for bus_id in region_buses:
                # Find generators connected to this bus
                bus_generators = network.generators[network.generators.bus == bus_id]
                if not bus_generators.empty:
                    total_capacity += bus_generators['p_nom'].sum()
                    
                    # Identify renewable generators
                    renewable_types = ['solar', 'wind', 'hydro', 'biomass']
                    renewable_gens = bus_generators[
                        bus_generators['type'].str.lower().isin(renewable_types)
                    ]
                    renewable_capacity += renewable_gens['p_nom'].sum()
            
            regional_generation[region_id] = {
                'total_capacity_mw': total_capacity,
                'renewable_capacity_mw': renewable_capacity,
                'renewable_share': renewable_capacity / total_capacity if total_capacity > 0 else 0,
                'num_generators': len(network.generators[network.generators.bus.isin(region_buses)])
            }
        
        return pd.DataFrame.from_dict(regional_generation, orient='index')
    
    def calculate_regional_balance(self, network, bus_assignments: pd.DataFrame) -> pd.DataFrame:
        """Calculate regional energy balance.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        bus_assignments : pd.DataFrame
            Bus-region assignments
        
        Returns
        -------
        pd.DataFrame
            Regional energy balance
        """
        regional_balance = {}
        
        load_analysis = self.analyze_regional_loads(network, bus_assignments)
        generation_analysis = self.analyze_regional_generation(network, bus_assignments)
        
        for region_id in self.regions:
            load = load_analysis.loc[region_id, 'total_load_mw'] if region_id in load_analysis.index else 0
            generation = generation_analysis.loc[region_id, 'total_capacity_mw'] if region_id in generation_analysis.index else 0
            
            balance = generation - load
            self_sufficiency = generation / load if load > 0 else float('inf')
            
            regional_balance[region_id] = {
                'load_mw': load,
                'generation_mw': generation,
                'balance_mw': balance,
                'self_sufficiency': self_sufficiency,
                'status': 'surplus' if balance > 0 else 'deficit'
            }
        
        return pd.DataFrame.from_dict(regional_balance, orient='index')
    
    def create_regional_constraints(self, network, bus_assignments: pd.DataFrame,
                                   constraint_type: str = 'capacity') -> Dict[str, Any]:
        """Create regional constraints for optimization.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        bus_assignments : pd.DataFrame
            Bus-region assignments
        constraint_type : str
            Type of constraint ('capacity', 'renewable', 'emissions')
        
        Returns
        -------
        Dict[str, Any]
            Regional constraints
        """
        constraints = {}
        
        if constraint_type == 'capacity':
            generation_analysis = self.analyze_regional_generation(network, bus_assignments)
            
            for region_id in self.regions:
                if region_id in generation_analysis.index:
                    capacity = generation_analysis.loc[region_id, 'total_capacity_mw']
                    constraints[f'{region_id}_max_capacity'] = {
                        'type': 'inequality',
                        'expression': f'sum(generation_{region_id}) <= {capacity}',
                        'description': f'Maximum generation capacity in {region_id}'
                    }
        
        elif constraint_type == 'renewable':
            generation_analysis = self.analyze_regional_generation(network, bus_assignments)
            
            for region_id in self.regions:
                if region_id in generation_analysis.index:
                    renewable_share = generation_analysis.loc[region_id, 'renewable_share']
                    constraints[f'{region_id}_renewable_share'] = {
                        'type': 'inequality',
                        'expression': f'renewable_generation_{region_id} >= {renewable_share} * total_generation_{region_id}',
                        'description': f'Minimum renewable share in {region_id}'
                    }
        
        return constraints
    
    def generate_regional_report(self, network, bus_assignments: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive regional analysis report.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        bus_assignments : pd.DataFrame
            Bus-region assignments
        
        Returns
        -------
        Dict[str, Any]
            Regional analysis report
        """
        report = {
            'regional_loads': self.analyze_regional_loads(network, bus_assignments),
            'regional_generation': self.analyze_regional_generation(network, bus_assignments),
            'regional_balance': self.calculate_regional_balance(network, bus_assignments),
            'regional_constraints': self.create_regional_constraints(network, bus_assignments),
            'summary': {
                'total_regions': len(self.regions),
                'total_buses': len(bus_assignments),
                'assigned_buses': len(bus_assignments[bus_assignments['region'].notna()]),
                'unassigned_buses': len(bus_assignments[bus_assignments['region'].isna()])
            }
        }
        
        return report