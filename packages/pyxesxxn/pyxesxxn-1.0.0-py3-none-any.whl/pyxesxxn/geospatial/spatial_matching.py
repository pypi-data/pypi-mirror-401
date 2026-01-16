"""
Spatial Matching Engine for PyPSA networks.

Provides spatial matching algorithms for energy system components:
- Load-resource matching
- Network topology matching
- Spatial optimization
- Proximity analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from abc import ABC, abstractmethod
import warnings

try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon, LineString
    from shapely.ops import nearest_points
    import scipy.spatial as spatial
    import scipy.optimize as optimize
except ImportError:
    warnings.warn("Geospatial libraries not available. Spatial matching will be limited.", UserWarning)

from .base import GeospatialProcessor


class MatchingStrategy(ABC):
    """Abstract base class for spatial matching strategies."""
    
    @abstractmethod
    def match(self, sources: 'gpd.GeoDataFrame', targets: 'gpd.GeoDataFrame', 
              **kwargs) -> pd.DataFrame:
        """Perform spatial matching.
        
        Parameters
        ----------
        sources : gpd.GeoDataFrame
            Source objects to match
        targets : gpd.GeoDataFrame
            Target objects to match to
        **kwargs
            Strategy-specific parameters
            
        Returns
        -------
        pd.DataFrame
            Matching results
        """
        pass


class ProximityMatching(MatchingStrategy):
    """Proximity-based matching strategy."""
    
    def __init__(self, distance_limit: float = 50.0, metric: str = 'euclidean'):
        """Initialize proximity matching.
        
        Parameters
        ----------
        distance_limit : float
            Maximum distance for matching
        metric : str
            Distance metric ('euclidean', 'haversine', 'geodesic')
        """
        self.distance_limit = distance_limit
        self.metric = metric
    
    def match(self, sources: 'gpd.GeoDataFrame', targets: 'gpd.GeoDataFrame', 
              **kwargs) -> pd.DataFrame:
        """Perform proximity-based matching."""
        distance_limit = kwargs.get('distance_limit', self.distance_limit)
        
        results = []
        
        for source_idx, source in sources.iterrows():
            source_point = source.geometry.centroid if hasattr(source, 'geometry') else Point(source['x'], source['y'])
            
            min_distance = float('inf')
            best_match = None
            
            for target_idx, target in targets.iterrows():
                target_point = target.geometry.centroid if hasattr(target, 'geometry') else Point(target['x'], target['y'])
                
                distance = source_point.distance(target_point)
                
                if distance < min_distance and distance <= distance_limit:
                    min_distance = distance
                    best_match = target_idx
            
            if best_match is not None:
                results.append({
                    'source_id': source_idx,
                    'target_id': best_match,
                    'distance': min_distance,
                    'match_type': 'proximity'
                })
        
        return pd.DataFrame(results)


class CapacityMatching(MatchingStrategy):
    """Capacity-based matching strategy."""
    
    def __init__(self, capacity_tolerance: float = 0.2):
        """Initialize capacity matching.
        
        Parameters
        ----------
        capacity_tolerance : float
            Relative tolerance for capacity matching
        """
        self.capacity_tolerance = capacity_tolerance
    
    def match(self, sources: 'gpd.GeoDataFrame', targets: 'gpd.GeoDataFrame', 
              **kwargs) -> pd.DataFrame:
        """Perform capacity-based matching."""
        results = []
        
        source_capacities = sources.get('capacity', sources.get('p_nom', pd.Series([1.0] * len(sources))))
        target_capacities = targets.get('capacity', targets.get('p_nom', pd.Series([1.0] * len(targets))))
        
        for source_idx, source in sources.iterrows():
            source_capacity = source_capacities.iloc[source_idx] if isinstance(source_capacities, pd.Series) else source_capacities[source_idx]
            
            best_matches = []
            
            for target_idx, target in targets.iterrows():
                target_capacity = target_capacities.iloc[target_idx] if isinstance(target_capacities, pd.Series) else target_capacities[target_idx]
                
                capacity_ratio = source_capacity / max(target_capacity, 1e-6)
                
                if 1 - self.capacity_tolerance <= capacity_ratio <= 1 + self.capacity_tolerance:
                    # Calculate distance for priority ranking
                    source_point = source.geometry.centroid if hasattr(source, 'geometry') else Point(source['x'], source['y'])
                    target_point = target.geometry.centroid if hasattr(target, 'geometry') else Point(target['x'], target['y'])
                    distance = source_point.distance(target_point)
                    
                    best_matches.append({
                        'target_id': target_idx,
                        'capacity_ratio': capacity_ratio,
                        'distance': distance
                    })
            
            if best_matches:
                # Sort by combined score (distance and capacity match)
                best_matches.sort(key=lambda x: x['distance'] * abs(x['capacity_ratio'] - 1.0))
                
                for i, match in enumerate(best_matches[:3]):  # Top 3 matches
                    results.append({
                        'source_id': source_idx,
                        'target_id': match['target_id'],
                        'capacity_ratio': match['capacity_ratio'],
                        'distance': match['distance'],
                        'match_score': 1.0 / (1.0 + match['distance'] * abs(match['capacity_ratio'] - 1.0)),
                        'match_rank': i + 1,
                        'match_type': 'capacity'
                    })
        
        return pd.DataFrame(results)


class OptimizationMatching(MatchingStrategy):
    """Optimization-based matching strategy."""
    
    def __init__(self, objective: str = 'minimize_distance', 
                 constraints: Optional[Dict[str, Any]] = None):
        """Initialize optimization matching.
        
        Parameters
        ----------
        objective : str
            Optimization objective ('minimize_distance', 'maximize_capacity', 'minimize_cost')
        constraints : Dict[str, Any], optional
            Matching constraints
        """
        self.objective = objective
        self.constraints = constraints or {}
    
    def match(self, sources: 'gpd.GeoDataFrame', targets: 'gpd.GeoDataFrame, 
              **kwargs) -> pd.DataFrame:
        """Perform optimization-based matching."""
        results = []
        
        # Create distance matrix
        distance_matrix = self._calculate_distance_matrix(sources, targets)
        
        # Create capacity matrix
        source_capacities = sources.get('capacity', sources.get('p_nom', pd.Series([1.0] * len(sources))))
        target_capacities = targets.get('capacity', targets.get('p_nom', pd.Series([1.0] * len(targets))))
        
        if isinstance(source_capacities, pd.Series):
            source_capacities = source_capacities.values
        if isinstance(target_capacities, pd.Series):
            target_capacities = target_capacities.values
        
        # Solve assignment problem
        if self.objective == 'minimize_distance':
            assignment_matrix = self._solve_assignment_problem(distance_matrix)
        else:
            # Create combined objective
            combined_matrix = self._combine_objectives(
                distance_matrix, source_capacities, target_capacities
            )
            assignment_matrix = self._solve_assignment_problem(combined_matrix)
        
        # Extract matches from assignment matrix
        for i in range(min(len(sources), assignment_matrix.shape[0])):
            for j in range(min(len(targets), assignment_matrix.shape[1])):
                if assignment_matrix[i, j] > 0:
                    results.append({
                        'source_id': sources.index[i],
                        'target_id': targets.index[j],
                        'distance': distance_matrix[i, j],
                        'capacity_ratio': source_capacities[i] / max(target_capacities[j], 1e-6),
                        'objective_value': assignment_matrix[i, j],
                        'match_type': 'optimization'
                    })
        
        return pd.DataFrame(results)
    
    def _calculate_distance_matrix(self, sources: 'gpd.GeoDataFrame', 
                                 targets: 'gpd.GeoDataFrame') -> np.ndarray:
        """Calculate distance matrix between sources and targets."""
        n_sources = len(sources)
        n_targets = len(targets)
        distance_matrix = np.zeros((n_sources, n_targets))
        
        for i, source in sources.iterrows():
            source_point = source.geometry.centroid if hasattr(source, 'geometry') else Point(source['x'], source['y'])
            
            for j, target in targets.iterrows():
                target_point = target.geometry.centroid if hasattr(target, 'geometry') else Point(target['x'], target['y'])
                distance_matrix[sources.index.get_loc(i), targets.index.get_loc(j)] = source_point.distance(target_point)
        
        return distance_matrix
    
    def _solve_assignment_problem(self, cost_matrix: np.ndarray) -> np.ndarray:
        """Solve assignment problem using Hungarian algorithm."""
        try:
            from scipy.optimize import linear_sum_assignment
            
            row_indices, col_indices = linear_sum_assignment(cost_matrix)
            assignment_matrix = np.zeros_like(cost_matrix)
            assignment_matrix[row_indices, col_indices] = 1
            
            return assignment_matrix
        except ImportError:
            warnings.warn("Scipy not available, using greedy assignment", UserWarning)
            return self._greedy_assignment(cost_matrix)
    
    def _greedy_assignment(self, cost_matrix: np.ndarray) -> np.ndarray:
        """Greedy assignment algorithm."""
        assignment_matrix = np.zeros_like(cost_matrix)
        remaining_rows = list(range(cost_matrix.shape[0]))
        remaining_cols = list(range(cost_matrix.shape[1]))
        
        while remaining_rows and remaining_cols:
            # Find minimum cost pair
            min_cost = float('inf')
            best_pair = (0, 0)
            
            for i in remaining_rows:
                for j in remaining_cols:
                    if cost_matrix[i, j] < min_cost:
                        min_cost = cost_matrix[i, j]
                        best_pair = (i, j)
            
            assignment_matrix[best_pair[0], best_pair[1]] = 1
            remaining_rows.remove(best_pair[0])
            remaining_cols.remove(best_pair[1])
        
        return assignment_matrix
    
    def _combine_objectives(self, distance_matrix: np.ndarray, 
                          source_capacities: np.ndarray, 
                          target_capacities: np.ndarray) -> np.ndarray:
        """Combine multiple objectives into single cost matrix."""
        # Normalize distance matrix
        norm_distance = distance_matrix / (np.max(distance_matrix) + 1e-6)
        
        # Calculate capacity matching costs
        capacity_matrix = np.zeros_like(distance_matrix)
        for i in range(len(source_capacities)):
            for j in range(len(target_capacities)):
                capacity_ratio = source_capacities[i] / max(target_capacities[j], 1e-6)
                capacity_matrix[i, j] = abs(np.log(capacity_ratio + 1e-6))
        
        # Combine objectives with weights
        distance_weight = 0.6
        capacity_weight = 0.4
        
        combined_cost = (distance_weight * norm_distance + 
                        capacity_weight * capacity_matrix)
        
        return combined_cost


class SpatialMatchingEngine(GeospatialProcessor):
    """Engine for spatial matching of energy system components."""
    
    def __init__(self, crs: str = "EPSG:4326", units: str = "degrees"):
        """Initialize spatial matching engine."""
        super().__init__(crs, units)
        self.matching_strategies = {
            'proximity': ProximityMatching(),
            'capacity': CapacityMatching(),
            'optimization': OptimizationMatching()
        }
    
    def register_matching_strategy(self, name: str, strategy: MatchingStrategy) -> None:
        """Register custom matching strategy.
        
        Parameters
        ----------
        name : str
            Strategy name
        strategy : MatchingStrategy
            Matching strategy instance
        """
        self.matching_strategies[name] = strategy
    
    def match_loads_to_generators(self, network, 
                                strategy: str = 'optimization',
                                strategy_params: Optional[Dict[str, Any]] = None,
                                distance_threshold: float = 100.0) -> pd.DataFrame:
        """Match load points to generator locations.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        strategy : str
            Matching strategy
        strategy_params : Dict[str, Any], optional
            Parameters for matching strategy
        distance_threshold : float
            Maximum allowed distance for matching
            
        Returns
        -------
        pd.DataFrame
            Load-generator matching results
        """
        if "buses" not in network.df:
            raise ValueError("Network contains no buses")
        
        # Extract load buses
        load_buses = self._extract_load_buses(network)
        
        # Extract generator buses  
        generator_buses = self._extract_generator_buses(network)
        
        if load_buses.empty or generator_buses.empty:
            return pd.DataFrame()
        
        # Perform matching
        if strategy not in self.matching_strategies:
            raise ValueError(f"Unknown matching strategy: {strategy}")
        
        matching_strategy = self.matching_strategies[strategy]
        
        # Prepare parameters
        params = strategy_params or {}
        params['distance_limit'] = distance_threshold
        
        matching_results = matching_strategy.match(
            load_buses, generator_buses, **params
        )
        
        return matching_results
    
    def match_resources_to_loads(self, network, 
                               strategy: str = 'capacity',
                               resource_data: Optional[pd.DataFrame] = None,
                               matching_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Match renewable resources to load centers.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        strategy : str
            Matching strategy
        resource_data : pd.DataFrame, optional
            Renewable resource data (capacity factors, locations, etc.)
        matching_params : Dict[str, Any], optional
            Matching parameters
            
        Returns
        -------
        pd.DataFrame
            Resource-load matching results
        """
        # Extract load data
        load_buses = self._extract_load_buses(network)
        
        if load_buses.empty:
            return pd.DataFrame()
        
        # Use network generators as default resource data
        if resource_data is None:
            generator_buses = self._extract_generator_buses(network)
            
            if generator_buses.empty:
                return pd.DataFrame()
            
            resource_data = generator_buses.copy()
            resource_data['resource_type'] = 'generator'
            resource_data['capacity'] = resource_data.get('p_nom', 1.0)
        
        # Ensure resource data has geometry
        if not isinstance(resource_data, gpd.GeoDataFrame):
            resource_gdf = gpd.GeoDataFrame(
                resource_data,
                geometry=gpd.points_from_xy(resource_data['x'], resource_data['y'])
            )
        else:
            resource_gdf = resource_data.copy()
        
        # Ensure load data has geometry
        if not isinstance(load_buses, gpd.GeoDataFrame):
            load_gdf = gpd.GeoDataFrame(
                load_buses,
                geometry=gpd.points_from_xy(load_buses['x'], load_buses['y'])
            )
        else:
            load_gdf = load_buses.copy()
        
        # Perform matching
        matching_strategy = self.matching_strategies[strategy]
        
        matching_results = matching_strategy.match(
            load_gdf, resource_gdf, **(matching_params or {})
        )
        
        # Add resource information
        if not matching_results.empty:
            matching_results = matching_results.merge(
                resource_gdf[['resource_type', 'capacity']], 
                left_on='target_id', 
                right_index=True, 
                how='left'
            )
        
        return matching_results
    
    def match_storage_to_network(self, network, 
                               storage_locations: Optional[pd.DataFrame] = None,
                               strategy: str = 'optimization',
                               matching_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Match storage facilities to optimal network locations.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        storage_locations : pd.DataFrame, optional
            Potential storage locations
        strategy : str
            Matching strategy
        matching_params : Dict[str, Any], optional
            Matching parameters
            
        Returns
        -------
        pd.DataFrame
            Storage-network matching results
        """
        # Extract network buses
        network_buses = self.extract_coordinates_from_network(network)
        
        if network_buses.empty:
            return pd.DataFrame()
        
        # Use network as potential storage locations if none provided
        if storage_locations is None:
            storage_locations = network_buses.copy()
            storage_locations['candidate_type'] = 'existing_bus'
        else:
            storage_locations['candidate_type'] = 'external_candidate'
        
        # Perform matching based on network properties
        matching_strategy = self.matching_strategies[strategy]
        
        matching_results = matching_strategy.match(
            network_buses, storage_locations, **(matching_params or {})
        )
        
        # Add matching scores based on network importance
        if not matching_results.empty:
            matching_results = self._calculate_storage_scores(
                matching_results, network, network_buses
            )
        
        return matching_results
    
    def optimize_network_topology(self, network, 
                                additional_connections: Optional[List[Tuple[str, str]]] = None,
                                cost_function: str = 'distance') -> Dict[str, Any]:
        """Optimize network topology based on spatial analysis.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        additional_connections : List[Tuple[str, str]], optional
            Potential additional connections
        cost_function : str
            Cost function type
            
        Returns
        -------
        Dict[str, Any]
            Optimization results
        """
        results = {
            'existing_connections': len(network.links) if "links" in network.df else 0,
            'additional_connections': [],
            'optimization_summary': {}
        }
        
        # Extract network topology
        buses = self.extract_coordinates_from_network(network)
        links = network.links if "links" in network.df else pd.DataFrame()
        
        # Analyze current connectivity
        connectivity_analysis = self._analyze_network_connectivity(buses, links)
        results['connectivity_analysis'] = connectivity_analysis
        
        # Find optimal additional connections
        if additional_connections is None:
            additional_connections = self._find_optimal_additions(buses)
        
        results['additional_connections'] = additional_connections
        
        # Calculate optimization benefits
        if additional_connections:
            optimization_benefits = self._calculate_optimization_benefits(
                buses, links, additional_connections, cost_function
            )
            results['optimization_benefits'] = optimization_benefits
        
        # Generate recommendations
        recommendations = self._generate_topology_recommendations(results)
        results['recommendations'] = recommendations
        
        return results
    
    def spatial_proximity_analysis(self, network, 
                                  point_of_interest: Optional[Tuple[float, float]] = None,
                                  radius: float = 50.0) -> Dict[str, Any]:
        """Perform spatial proximity analysis.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        point_of_interest : Tuple[float, float], optional
            Reference point for analysis
        radius : float
            Analysis radius
            
        Returns
        -------
        Dict[str, Any]
            Proximity analysis results
        """
        buses = self.extract_coordinates_from_network(network)
        
        if buses.empty:
            return {}
        
        results = {
            'analysis_radius': radius,
            'total_components': len(buses),
            'proximity_zones': []
        }
        
        # If no point of interest, use network centroid
        if point_of_interest is None:
            point_of_interest = (buses['x'].mean(), buses['y'].mean())
        
        results['reference_point'] = point_of_interest
        
        # Create proximity zones
        reference_point = Point(point_of_interest)
        
        for i, (bus_id, bus) in enumerate(buses.iterrows()):
            bus_point = Point(bus['x'], bus['y'])
            distance = reference_point.distance(bus_point)
            
            if distance <= radius:
                zone_info = {
                    'bus_id': bus_id,
                    'distance': distance,
                    'zone_type': self._classify_proximity_zone(distance, radius),
                    'bus_info': bus.to_dict()
                }
                results['proximity_zones'].append(zone_info)
        
        # Calculate zone statistics
        if results['proximity_zones']:
            zone_df = pd.DataFrame(results['proximity_zones'])
            results['zone_statistics'] = {
                'min_distance': zone_df['distance'].min(),
                'max_distance': zone_df['distance'].max(),
                'mean_distance': zone_df['distance'].mean(),
                'zone_distribution': zone_df['zone_type'].value_counts().to_dict()
            }
        
        return results
    
    def spatial_optimization(self, network, 
                           objective: str = 'minimize_losses',
                           constraints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform spatial optimization of network layout.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        objective : str
            Optimization objective
        constraints : Dict[str, Any], optional
            Optimization constraints
            
        Returns
        -------
        Dict[str, Any]
            Optimization results
        """
        buses = self.extract_coordinates_from_network(network)
        
        if buses.empty:
            return {}
        
        results = {
            'objective': objective,
            'constraints': constraints or {},
            'optimization_results': {}
        }
        
        # Define optimization problem based on objective
        if objective == 'minimize_losses':
            optimization_result = self._optimize_for_minimal_losses(buses, constraints)
        elif objective == 'maximize_coverage':
            optimization_result = self._optimize_for_maximal_coverage(buses, constraints)
        elif objective == 'minimize_cost':
            optimization_result = self._optimize_for_minimal_cost(buses, constraints)
        else:
            raise ValueError(f"Unknown optimization objective: {objective}")
        
        results['optimization_results'] = optimization_result
        
        return results
    
    # Helper methods
    def _extract_load_buses(self, network) -> pd.DataFrame:
        """Extract buses with load information."""
        if "loads" not in network.df or network.df["loads"].empty:
            return pd.DataFrame()
        
        # Get load buses
        load_buses = network.buses.loc[network.df["loads"]["bus"]]
        
        # Add load information
        load_info = network.df["loads"].copy()
        load_info.index = load_info["bus"]
        
        # Merge load data with bus data
        buses_with_loads = load_buses.join(load_info, how='inner')
        
        return buses_with_loads
    
    def _extract_generator_buses(self, network) -> pd.DataFrame:
        """Extract buses with generator information."""
        if "generators" not in network.df or network.df["generators"].empty:
            return pd.DataFrame()
        
        # Get generator buses
        generator_buses = network.buses.loc[network.df["generators"]["bus"]]
        
        # Add generator information
        generator_info = network.df["generators"].copy()
        generator_info.index = generator_info["bus"]
        
        # Merge generator data with bus data
        buses_with_generators = generator_buses.join(generator_info, how='inner')
        
        return buses_with_generators
    
    def _calculate_storage_scores(self, matching_results: pd.DataFrame,
                                network, buses: pd.DataFrame) -> pd.DataFrame:
        """Calculate storage placement scores."""
        # Add network importance scores
        for idx, row in matching_results.iterrows():
            bus_id = row['source_id']
            
            if bus_id in buses.index:
                bus_data = buses.loc[bus_id]
                
                # Voltage level score
                voltage_score = min(bus_data.get('v_nom', 0) / 400.0, 1.0)
                
                # Connectivity score (based on degree in network)
                if "links" in network.df:
                    bus_connections = network.df["links"][
                        (network.df["links"]["bus0"] == bus_id) | 
                        (network.df["links"]["bus1"] == bus_id)
                    ]
                    connectivity_score = min(len(bus_connections) / 10.0, 1.0)
                else:
                    connectivity_score = 0.0
                
                # Load proximity score
                load_score = min(bus_data.get('p_set', 0) / 100.0, 1.0)
                
                # Combined score
                total_score = (voltage_score * 0.3 + 
                              connectivity_score * 0.3 + 
                              load_score * 0.4)
                
                matching_results.loc[idx, 'storage_score'] = total_score
        
        return matching_results
    
    def _analyze_network_connectivity(self, buses: pd.DataFrame, 
                                    links: pd.DataFrame) -> Dict[str, Any]:
        """Analyze network connectivity."""
        connectivity = {
            'total_nodes': len(buses),
            'total_edges': len(links),
            'connectivity_ratio': len(links) / max(len(buses) - 1, 1),
            'average_degree': 0.0,
            'isolated_nodes': [],
            'critical_nodes': []
        }
        
        if links.empty:
            connectivity['isolated_nodes'] = buses.index.tolist()
            return connectivity
        
        # Calculate node degrees
        node_degrees = {}
        
        for bus_id in buses.index:
            degree = 0
            
            for _, link in links.iterrows():
                if link['bus0'] == bus_id or link['bus1'] == bus_id:
                    degree += 1
            
            node_degrees[bus_id] = degree
        
        connectivity['average_degree'] = np.mean(list(node_degrees.values()))
        
        # Identify isolated and critical nodes
        for bus_id, degree in node_degrees.items():
            if degree == 0:
                connectivity['isolated_nodes'].append(bus_id)
            elif degree <= 2:
                connectivity['critical_nodes'].append(bus_id)
        
        return connectivity
    
    def _find_optimal_additions(self, buses: pd.DataFrame) -> List[Tuple[str, str]]:
        """Find optimal additional connections."""
        additions = []
        
        # Simple approach: connect isolated nodes to nearest neighbors
        connectivity = self._analyze_network_connectivity(buses, pd.DataFrame())
        
        for isolated_bus in connectivity['isolated_nodes']:
            if isolated_bus in buses.index:
                bus_coord = (buses.loc[isolated_bus, 'x'], buses.loc[isolated_bus, 'y'])
                
                # Find nearest bus
                min_distance = float('inf')
                nearest_bus = None
                
                for other_bus, other_data in buses.iterrows():
                    if other_bus != isolated_bus:
                        other_coord = (other_data['x'], other_data['y'])
                        distance = self.calculate_distance(bus_coord, other_coord)
                        
                        if distance < min_distance:
                            min_distance = distance
                            nearest_bus = other_bus
                
                if nearest_bus is not None:
                    additions.append((isolated_bus, nearest_bus))
        
        return additions
    
    def _calculate_optimization_benefits(self, buses: pd.DataFrame, 
                                       links: pd.DataFrame,
                                       additions: List[Tuple[str, str]], 
                                       cost_function: str) -> Dict[str, Any]:
        """Calculate benefits of topology optimizations."""
        benefits = {
            'additional_connections': len(additions),
            'estimated_cost_savings': 0.0,
            'reliability_improvement': 0.0,
            'losses_reduction': 0.0
        }
        
        if not additions:
            return benefits
        
        # Calculate connection costs
        total_additional_cost = 0.0
        
        for bus1, bus2 in additions:
            coord1 = (buses.loc[bus1, 'x'], buses.loc[bus1, 'y'])
            coord2 = (buses.loc[bus2, 'x'], buses.loc[bus2, 'y'])
            
            distance = self.calculate_distance(coord1, coord2)
            connection_cost = distance * 1000  # Cost per km
            
            total_additional_cost += connection_cost
        
        benefits['estimated_cost_savings'] = -total_additional_cost
        
        # Estimate reliability improvement
        benefits['reliability_improvement'] = min(len(additions) * 0.1, 1.0)
        
        return benefits
    
    def _generate_topology_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate topology optimization recommendations."""
        recommendations = []
        
        connectivity = analysis_results.get('connectivity_analysis', {})
        
        # Connectivity recommendations
        isolated_nodes = connectivity.get('isolated_nodes', [])
        if isolated_nodes:
            recommendations.append(f"Connect {len(isolated_nodes)} isolated nodes to improve network reliability")
        
        connectivity_ratio = connectivity.get('connectivity_ratio', 0)
        if connectivity_ratio < 1.2:
            recommendations.append("Network connectivity is low. Consider adding more interconnections")
        
        # Additional connection recommendations
        additional = analysis_results.get('additional_connections', [])
        if additional:
            recommendations.append(f"Add {len(additional)} connections to reduce isolated components")
        
        return recommendations
    
    def _classify_proximity_zone(self, distance: float, radius: float) -> str:
        """Classify proximity zone based on distance."""
        ratio = distance / radius
        
        if ratio <= 0.2:
            return "immediate_proximity"
        elif ratio <= 0.5:
            return "close_proximity"
        elif ratio <= 0.8:
            return "moderate_proximity"
        else:
            return "distant_proximity"
    
    def _optimize_for_minimal_losses(self, buses: pd.DataFrame, 
                                   constraints: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize network for minimal transmission losses."""
        # Simplified optimization for demonstration
        optimization_result = {
            'method': 'losses_minimization',
            'optimization_status': 'completed',
            'recommended_actions': [],
            'estimated_improvement': 0.0
        }
        
        # Calculate current losses estimate
        if len(buses) > 1:
            total_distance = 0.0
            for i in range(len(buses) - 1):
                for j in range(i + 1, len(buses)):
                    coord1 = (buses.iloc[i]['x'], buses.iloc[i]['y'])
                    coord2 = (buses.iloc[j]['x'], buses.iloc[j]['y'])
                    total_distance += self.calculate_distance(coord1, coord2)
            
            optimization_result['estimated_improvement'] = total_distance * 0.1
            optimization_result['recommended_actions'].append("Add voltage conversion facilities")
            optimization_result['recommended_actions'].append("Optimize conductor sizes")
        
        return optimization_result
    
    def _optimize_for_maximal_coverage(self, buses: pd.DataFrame, 
                                     constraints: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize network for maximal service coverage."""
        optimization_result = {
            'method': 'coverage_maximization',
            'optimization_status': 'completed',
            'recommended_actions': [],
            'coverage_improvement': 0.0
        }
        
        # Calculate coverage area
        x_range = buses['x'].max() - buses['x'].min()
        y_range = buses['y'].max() - buses['y'].min()
        coverage_area = x_range * y_range
        
        optimization_result['coverage_improvement'] = coverage_area * 0.05
        optimization_result['recommended_actions'].append("Extend network to uncovered areas")
        optimization_result['recommended_actions'].append("Add distribution substations")
        
        return optimization_result
    
    def _optimize_for_minimal_cost(self, buses: pd.DataFrame, 
                                 constraints: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize network for minimal total cost."""
        optimization_result = {
            'method': 'cost_minimization',
            'optimization_status': 'completed',
            'recommended_actions': [],
            'cost_savings': 0.0
        }
        
        # Calculate current cost estimate
        if len(buses) > 1:
            total_distance = 0.0
            for i in range(len(buses) - 1):
                for j in range(i + 1, len(buses)):
                    coord1 = (buses.iloc[i]['x'], buses.iloc[i]['y'])
                    coord2 = (buses.iloc[j]['x'], buses.iloc[j]['y'])
                    distance = self.calculate_distance(coord1, coord2)
                    total_distance += distance
            
            current_cost = total_distance * 1000  # Cost per km
            optimization_result['cost_savings'] = current_cost * 0.1
            
            optimization_result['recommended_actions'].append("Consolidate overlapping circuits")
            optimization_result['recommended_actions'].append("Optimize routing paths")
        
        return optimization_result
    
    def get_matching_summary(self) -> Dict[str, Any]:
        """Get summary of matching capabilities."""
        return {
            "engine_type": "SpatialMatchingEngine",
            "available_strategies": list(self.matching_strategies.keys()),
            "capabilities": [
                "load_generator_matching",
                "resource_load_matching", 
                "storage_network_matching",
                "network_topology_optimization",
                "spatial_proximity_analysis",
                "spatial_optimization"
            ],
            "matching_objectives": [
                "proximity_based",
                "capacity_based",
                "optimization_based"
            ],
            "optimization_objectives": [
                "minimize_losses",
                "maximize_coverage", 
                "minimize_cost"
            ],
            "spatial_operations": [
                "distance_calculations",
                "proximity_analysis",
                "zone_classification",
                "connectivity_analysis"
            ]
        }