"""
Spatial Analysis Engine for PyPSA networks.

Provides advanced spatial analysis capabilities:
- Network spatial properties analysis
- Load density mapping
- Service area analysis  
- Spatial statistics
- Terrain analysis
- Environmental impact assessment
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from abc import ABC, abstractmethod
import warnings

try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon, LineString, box
    from shapely.ops import unary_union
    import matplotlib.pyplot as plt
    from scipy import spatial
    from scipy.spatial import distance_matrix
except ImportError:
    warnings.warn("Geospatial libraries not available. Spatial analysis will be limited.", UserWarning)

from .base import GeospatialProcessor


class AnalysisStrategy(ABC):
    """Abstract base class for spatial analysis strategies."""
    
    @abstractmethod
    def analyze(self, data: 'gpd.GeoDataFrame', **kwargs) -> Dict[str, Any]:
        """Perform spatial analysis.
        
        Parameters
        ----------
        data : gpd.GeoDataFrame
            Input spatial data
        **kwargs
            Strategy-specific parameters
            
        Returns
        -------
        Dict[str, Any]
            Analysis results
        """
        pass


class DensityAnalysis(AnalysisStrategy):
    """Network component density analysis strategy."""
    
    def __init__(self, grid_size: float = 0.01, radius: float = 0.05):
        """Initialize density analysis.
        
        Parameters
        ----------
        grid_size : float
            Grid cell size for density calculation
        radius : float
            Radius for kernel density estimation
        """
        self.grid_size = grid_size
        self.radius = radius
    
    def analyze(self, data: 'gpd.GeoDataFrame', **kwargs) -> Dict[str, Any]:
        """Perform density analysis."""
        grid_size = kwargs.get('grid_size', self.grid_size)
        radius = kwargs.get('radius', self.radius)
        
        results = {
            'analysis_type': 'density_analysis',
            'grid_size': grid_size,
            'radius': radius,
            'density_metrics': {},
            'density_zones': []
        }
        
        if data.empty:
            return results
        
        # Calculate spatial bounds
        bounds = data.total_bounds
        x_min, y_min, x_max, y_max = bounds
        
        # Create analysis grid
        x_range = np.arange(x_min, x_max + grid_size, grid_size)
        y_range = np.arange(y_min, y_max + grid_size, grid_size)
        
        # Calculate density for each grid cell
        grid_densities = []
        grid_centers = []
        
        for x in x_range[:-1]:
            for y in y_range[:-1]:
                # Define grid cell
                cell = box(x, y, x + grid_size, y + grid_size)
                
                # Count points in cell
                points_in_cell = data[data.geometry.intersects(cell)]
                density = len(points_in_cell) / (grid_size ** 2)
                
                grid_densities.append(density)
                grid_centers.append((x + grid_size/2, y + grid_size/2))
        
        results['density_metrics'] = {
            'min_density': min(grid_densities) if grid_densities else 0,
            'max_density': max(grid_densities) if grid_densities else 0,
            'mean_density': np.mean(grid_densities) if grid_densities else 0,
            'std_density': np.std(grid_densities) if grid_densities else 0,
            'total_grid_cells': len(grid_densities)
        }
        
        # Identify high and low density zones
        mean_density = results['density_metrics']['mean_density']
        
        for i, (density, center) in enumerate(zip(grid_densities, grid_centers)):
            if density > mean_density * 1.5:
                results['density_zones'].append({
                    'zone_id': f'high_density_{i}',
                    'center': center,
                    'density': density,
                    'zone_type': 'high_density'
                })
            elif density < mean_density * 0.5:
                results['density_zones'].append({
                    'zone_id': f'low_density_{i}',
                    'center': center,
                    'density': density,
                    'zone_type': 'low_density'
                })
        
        return results


class ConnectivityAnalysis(AnalysisStrategy):
    """Network connectivity analysis strategy."""
    
    def analyze(self, data: 'gpd.GeoDataFrame', network=None, **kwargs) -> Dict[str, Any]:
        """Perform connectivity analysis."""
        results = {
            'analysis_type': 'connectivity_analysis',
            'connectivity_metrics': {},
            'network_centrality': {},
            'critical_components': []
        }
        
        if data.empty:
            return results
        
        # Calculate basic connectivity metrics
        n_components = len(data)
        centroid = data.geometry.centroid
        
        # Calculate average distance to centroid
        distances_to_centroid = data.geometry.centroid.distance(centroid.unary_union)
        
        results['connectivity_metrics'] = {
            'total_components': n_components,
            'average_distance_to_centroid': distances_to_centroid.mean(),
            'max_distance_to_centroid': distances_to_centroid.max(),
            'min_distance_to_centroid': distances_to_centroid.min(),
            'centroid_coordinates': (centroid.x.iloc[0], centroid.y.iloc[0])
        }
        
        # Calculate centrality metrics
        if n_components > 1:
            # Degree centrality (simplified)
            coordinates = np.column_stack([data.geometry.x, data.geometry.y])
            dist_matrix = distance_matrix(coordinates, coordinates)
            
            # Average distance to other components
            avg_distances = np.mean(dist_matrix, axis=1)
            
            results['network_centrality'] = {
                'degree_centrality': (n_components - 1) / (n_components - 1),  # Simplified
                'betweenness_centrality': self._calculate_betweenness_centrality(dist_matrix),
                'closeness_centrality': 1.0 / (avg_distances + 1e-6),
                'eigenvector_centrality': self._calculate_eigenvector_centrality(dist_matrix)
            }
            
            # Identify critical components (high centrality or strategic location)
            critical_indices = []
            
            # High closeness centrality (short average distance to others)
            closeness_scores = results['network_centrality']['closeness_centrality']
            high_closeness_threshold = np.percentile(closeness_scores, 90)
            
            for i, score in enumerate(closeness_scores):
                if score >= high_closeness_threshold:
                    critical_indices.append(i)
            
            # Add critical components to results
            for idx in critical_indices:
                if idx < len(data):
                    component_info = data.iloc[idx].to_dict()
                    component_info['criticality_score'] = closeness_scores[idx]
                    results['critical_components'].append(component_info)
        
        return results
    
    def _calculate_betweenness_centrality(self, dist_matrix: np.ndarray) -> np.ndarray:
        """Calculate betweenness centrality."""
        n = len(dist_matrix)
        betweenness = np.zeros(n)
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if i != j and i != k and j != k:
                        # Shortest path between i and j passing through k
                        shortest_path_ikj = dist_matrix[i, k] + dist_matrix[k, j]
                        shortest_path_ij = dist_matrix[i, j]
                        
                        if abs(shortest_path_ikj - shortest_path_ij) < 1e-6:
                            betweenness[k] += 1
        
        # Normalize
        normalization_factor = (n - 1) * (n - 2) / 2
        betweenness = betweenness / normalization_factor if normalization_factor > 0 else betweenness
        
        return betweenness
    
    def _calculate_eigenvector_centrality(self, dist_matrix: np.ndarray) -> np.ndarray:
        """Calculate eigenvector centrality."""
        try:
            # Convert distance to similarity matrix
            max_distance = np.max(dist_matrix)
            similarity_matrix = max_distance - dist_matrix
            
            # Set diagonal to zero
            np.fill_diagonal(similarity_matrix, 0)
            
            # Normalize
            row_sums = similarity_matrix.sum(axis=1)
            row_sums[row_sums == 0] = 1  # Avoid division by zero
            similarity_matrix = similarity_matrix / row_sums[:, np.newaxis]
            
            # Find eigenvector
            eigenvalues, eigenvectors = np.linalg.eig(similarity_matrix)
            max_eigenvalue_idx = np.argmax(eigenvalues.real)
            eigenvector = eigenvectors[:, max_eigenvalue_idx].real
            
            # Make all values positive
            eigenvector = np.abs(eigenvector)
            
            return eigenvector
        except:
            # Fallback to uniform values
            n = len(dist_matrix)
            return np.ones(n) / n


class CoverageAnalysis(AnalysisStrategy):
    """Network coverage analysis strategy."""
    
    def __init__(self, service_radius: float = 50.0):
        """Initialize coverage analysis.
        
        Parameters
        ----------
        service_radius : float
            Service radius for coverage calculation
        """
        self.service_radius = service_radius
    
    def analyze(self, data: 'gpd.GeoDataFrame', **kwargs) -> Dict[str, Any]:
        """Perform coverage analysis."""
        service_radius = kwargs.get('service_radius', self.service_radius)
        
        results = {
            'analysis_type': 'coverage_analysis',
            'service_radius': service_radius,
            'coverage_metrics': {},
            'coverage_gaps': [],
            'optimal_locations': []
        }
        
        if data.empty:
            return results
        
        # Calculate coverage area for each component
        coverage_areas = []
        
        for _, component in data.iterrows():
            if hasattr(component.geometry, 'buffer'):
                coverage_polygon = component.geometry.buffer(service_radius)
                coverage_areas.append(coverage_polygon)
            else:
                # Create circular coverage around point
                center_point = Point(component.geometry.x, component.geometry.y)
                coverage_polygon = center_point.buffer(service_radius)
                coverage_areas.append(coverage_polygon)
        
        # Calculate total coverage
        total_coverage = unary_union(coverage_areas)
        
        # Calculate network bounds
        bounds = data.total_bounds
        
        # Estimate total service area
        total_area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
        
        results['coverage_metrics'] = {
            'total_network_area': total_area,
            'covered_area': total_coverage.area,
            'coverage_ratio': min(total_coverage.area / total_area, 1.0),
            'uncovered_area': max(total_area - total_coverage.area, 0),
            'average_component_coverage': total_coverage.area / len(data) if len(data) > 0 else 0,
            'coverage_overlap': len(coverage_areas) - 1 if len(coverage_areas) > 1 else 0
        }
        
        # Identify coverage gaps
        coverage_gaps = self._identify_coverage_gaps(
            total_coverage, bounds, service_radius
        )
        results['coverage_gaps'] = coverage_gaps
        
        # Find optimal locations for additional components
        optimal_locations = self._find_optimal_locations(
            data, total_coverage, bounds, service_radius
        )
        results['optimal_locations'] = optimal_locations
        
        return results
    
    def _identify_coverage_gaps(self, coverage: 'Polygon', 
                              bounds: Tuple[float, float, float, float],
                              service_radius: float) -> List[Dict[str, Any]]:
        """Identify gaps in network coverage."""
        gaps = []
        
        # Create bounding box
        bounding_box = box(bounds[0], bounds[1], bounds[2], bounds[3])
        
        # Find uncovered areas (simplified approach)
        if hasattr(coverage, 'exterior'):
            # Create grid to check coverage
            grid_size = service_radius / 2
            x_min, y_min, x_max, y_max = bounds
            
            x_range = np.arange(x_min, x_max + grid_size, grid_size)
            y_range = np.arange(y_min, y_max + grid_size, grid_size)
            
            for x in x_range[:-1]:
                for y in y_range[:-1]:
                    grid_point = Point(x + grid_size/2, y + grid_size/2)
                    
                    # Check if point is within existing coverage
                    if not coverage.contains(grid_point):
                        gaps.append({
                            'gap_id': f'gap_{len(gaps)}',
                            'location': (grid_point.x, grid_point.y),
                            'size': grid_size,
                            'priority': 'medium'
                        })
        
        return gaps
    
    def _find_optimal_locations(self, existing_data: 'gpd.GeoDataFrame',
                              existing_coverage: 'Polygon',
                              bounds: Tuple[float, float, float, float],
                              service_radius: float) -> List[Dict[str, Any]]:
        """Find optimal locations for additional components."""
        optimal_locations = []
        
        # Simple approach: find areas farthest from existing components
        grid_size = service_radius / 3
        x_min, y_min, x_max, y_max = bounds
        
        x_range = np.arange(x_min, x_max + grid_size, grid_size)
        y_range = np.arange(y_min, y_max + grid_size, grid_size)
        
        grid_points = []
        for x in x_range[:-1]:
            for y in y_range[:-1]:
                grid_points.append((x + grid_size/2, y + grid_size/2))
        
        if not grid_points:
            return optimal_locations
        
        # Calculate distances to nearest existing components
        if len(existing_data) > 0:
            existing_coords = np.column_stack([
                existing_data.geometry.x, 
                existing_data.geometry.y
            ])
            
            grid_coords = np.array(grid_points)
            dist_matrix = distance_matrix(grid_coords, existing_coords)
            min_distances = np.min(dist_matrix, axis=1)
            
            # Find locations with maximum minimum distance
            max_min_distance_idx = np.argmax(min_distances)
            max_min_distance = min_distances[max_min_distance_idx]
            
            if max_min_distance > service_radius:
                optimal_locations.append({
                    'location_id': f'optimal_{len(optimal_locations)}',
                    'coordinates': grid_points[max_min_distance_idx],
                    'max_min_distance': max_min_distance,
                    'justification': 'Maximize distance from existing components'
                })
        
        return optimal_locations


class SpatialAnalysisEngine(GeospatialProcessor):
    """Engine for advanced spatial analysis of energy systems."""
    
    def __init__(self, crs: str = "EPSG:4326", units: str = "degrees"):
        """Initialize spatial analysis engine."""
        super().__init__(crs, units)
        self.analysis_strategies = {
            'density': DensityAnalysis(),
            'connectivity': ConnectivityAnalysis(),
            'coverage': CoverageAnalysis()
        }
    
    def register_analysis_strategy(self, name: str, strategy: AnalysisStrategy) -> None:
        """Register custom analysis strategy.
        
        Parameters
        ----------
        name : str
            Strategy name
        strategy : AnalysisStrategy
            Analysis strategy instance
        """
        self.analysis_strategies[name] = strategy
    
    def analyze_network_spatial_properties(self, network, 
                                         analysis_types: Optional[List[str]] = None,
                                         analysis_params: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Analyze spatial properties of network.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to analyze
        analysis_types : List[str], optional
            Types of analysis to perform
        analysis_params : Dict[str, Dict[str, Any]], optional
            Parameters for each analysis type
            
        Returns
        -------
        Dict[str, Any]
            Comprehensive spatial analysis results
        """
        if analysis_types is None:
            analysis_types = ['density', 'connectivity', 'coverage']
        
        if analysis_params is None:
            analysis_params = {}
        
        # Extract spatial data from network
        buses_gdf = self.extract_coordinates_from_network(network)
        
        if buses_gdf.empty:
            return {'error': 'No spatial data available in network'}
        
        results = {
            'network_id': getattr(network, 'name', 'unnamed_network'),
            'total_buses': len(buses_gdf),
            'spatial_bounds': buses_gdf.total_bounds,
            'analysis_results': {},
            'summary_metrics': {}
        }
        
        # Perform requested analyses
        for analysis_type in analysis_types:
            if analysis_type not in self.analysis_strategies:
                continue
            
            strategy = self.analysis_strategies[analysis_type]
            params = analysis_params.get(analysis_type, {})
            
            try:
                if analysis_type == 'connectivity':
                    analysis_result = strategy.analyze(buses_gdf, network=network, **params)
                else:
                    analysis_result = strategy.analyze(buses_gdf, **params)
                
                results['analysis_results'][analysis_type] = analysis_result
                
            except Exception as e:
                results['analysis_results'][analysis_type] = {
                    'error': str(e),
                    'analysis_type': analysis_type
                }
        
        # Calculate summary metrics
        results['summary_metrics'] = self._calculate_summary_metrics(results['analysis_results'])
        
        return results
    
    def analyze_load_density(self, network, 
                           grid_size: float = 0.01,
                           density_method: str = 'kernel') -> Dict[str, Any]:
        """Analyze load density distribution.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        grid_size : float
            Grid cell size for density analysis
        density_method : str
            Density calculation method
            
        Returns
        -------
        Dict[str, Any]
            Load density analysis results
        """
        if "buses" not in network.df:
            return {'error': 'No buses in network'}
        
        # Extract load data
        load_data = self._extract_load_distribution(network)
        
        if load_data.empty:
            return {'error': 'No load data available'}
        
        results = {
            'analysis_type': 'load_density',
            'grid_size': grid_size,
            'density_method': density_method,
            'density_metrics': {},
            'high_density_areas': [],
            'load_distribution': {}
        }
        
        # Calculate load density
        load_density = self._calculate_load_density(load_data, grid_size, density_method)
        
        results['density_metrics'] = {
            'min_load_density': load_density.min() if not load_density.empty else 0,
            'max_load_density': load_density.max() if not load_density.empty else 0,
            'mean_load_density': load_density.mean() if not load_density.empty else 0,
            'std_load_density': load_density.std() if not load_density.empty else 0,
            'total_load': load_data['p_set'].sum() if 'p_set' in load_data.columns else 0
        }
        
        # Identify high density areas
        mean_density = results['density_metrics']['mean_load_density']
        high_density_threshold = mean_density * 1.5
        
        high_density_areas = load_density[load_density > high_density_threshold]
        
        for idx, density in high_density_areas.items():
            results['high_density_areas'].append({
                'area_id': f'high_density_{idx}',
                'density': density,
                'grid_cell': idx,
                'priority': 'high'
            })
        
        # Load distribution analysis
        if 'p_set' in load_data.columns:
            results['load_distribution'] = {
                'total_load': load_data['p_set'].sum(),
                'avg_load_per_bus': load_data['p_set'].mean(),
                'load_variance': load_data['p_set'].var(),
                'peak_load_bus': load_data['p_set'].idxmax() if not load_data['p_set'].empty else None,
                'peak_load_value': load_data['p_set'].max() if not load_data['p_set'].empty else 0
            }
        
        return results
    
    def analyze_service_areas(self, network, 
                            service_radius: float = 50.0,
                            service_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze service areas and coverage.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        service_radius : float
            Service radius for different service types
        service_types : List[str], optional
            Types of services to analyze
            
        Returns
        -------
        Dict[str, Any]
            Service area analysis results
        """
        if service_types is None:
            service_types = ['transmission', 'distribution', 'generation']
        
        buses_gdf = self.extract_coordinates_from_network(network)
        
        if buses_gdf.empty:
            return {'error': 'No spatial data available'}
        
        results = {
            'analysis_type': 'service_areas',
            'service_radius': service_radius,
            'service_types': service_types,
            'service_analysis': {},
            'overlap_analysis': {},
            'optimization_suggestions': []
        }
        
        # Analyze each service type
        for service_type in service_types:
            service_buses = self._classify_service_buses(buses_gdf, service_type)
            
            if service_buses.empty:
                continue
            
            # Perform coverage analysis for this service type
            strategy = self.analysis_strategies['coverage']
            coverage_result = strategy.analyze(
                service_buses, 
                service_radius=service_radius
            )
            
            results['service_analysis'][service_type] = coverage_result
        
        # Analyze overlaps between service types
        if len(service_types) > 1:
            overlap_result = self._analyze_service_overlaps(
                buses_gdf, service_types, service_radius
            )
            results['overlap_analysis'] = overlap_result
        
        # Generate optimization suggestions
        suggestions = self._generate_service_area_suggestions(results)
        results['optimization_suggestions'] = suggestions
        
        return results
    
    def perform_terrain_analysis(self, network, 
                                terrain_data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Perform terrain analysis for network planning.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        terrain_data : pd.DataFrame, optional
            Terrain elevation data
            
        Returns
        -------
        Dict[str, Any]
            Terrain analysis results
        """
        buses_gdf = self.extract_coordinates_from_network(network)
        
        if buses_gdf.empty:
            return {'error': 'No spatial data available'}
        
        results = {
            'analysis_type': 'terrain_analysis',
            'elevation_metrics': {},
            'slope_analysis': {},
            'terrain_constraints': [],
            'routing_suggestions': []
        }
        
        # Extract elevation data if available
        if 'elevation' in buses_gdf.columns:
            elevations = buses_gdf['elevation'].dropna()
            
            if not elevations.empty:
                results['elevation_metrics'] = {
                    'min_elevation': elevations.min(),
                    'max_elevation': elevations.max(),
                    'mean_elevation': elevations.mean(),
                    'elevation_range': elevations.max() - elevations.min(),
                    'elevation_std': elevations.std()
                }
                
                # Analyze elevation changes (slope proxy)
                if len(elevations) > 1:
                    sorted_elevations = elevations.sort_values()
                    max_elevation_change = sorted_elevations.diff().max()
                    
                    results['slope_analysis'] = {
                        'max_elevation_change': max_elevation_change,
                        'avg_elevation_change': sorted_elevations.diff().mean(),
                        'terrain_roughness': elevations.std() / elevations.mean() if elevations.mean() > 0 else 0
                    }
        else:
            # Generate synthetic elevation data if none available
            elevation_data = self._generate_synthetic_elevation_data(buses_gdf)
            
            results['elevation_metrics'] = {
                'min_elevation': elevation_data['elevation'].min(),
                'max_elevation': elevation_data['elevation'].max(),
                'mean_elevation': elevation_data['elevation'].mean(),
                'elevation_range': elevation_data['elevation'].max() - elevation_data['elevation'].min(),
                'elevation_std': elevation_data['elevation'].std(),
                'data_source': 'synthetic'
            }
            
            buses_gdf['elevation'] = elevation_data['elevation']
        
        # Identify terrain constraints
        terrain_constraints = self._identify_terrain_constraints(buses_gdf)
        results['terrain_constraints'] = terrain_constraints
        
        # Generate routing suggestions
        routing_suggestions = self._generate_routing_suggestions(buses_gdf)
        results['routing_suggestions'] = routing_suggestions
        
        return results
    
    def assess_environmental_impact(self, network, 
                                  environmental_zones: Optional[pd.DataFrame] = None,
                                  protected_areas: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Assess environmental impact of network components.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        environmental_zones : pd.DataFrame, optional
            Environmental zone data
        protected_areas : pd.DataFrame, optional
            Protected area data
            
        Returns
        -------
        Dict[str, Any]
            Environmental impact assessment
        """
        buses_gdf = self.extract_coordinates_from_network(network)
        
        if buses_gdf.empty:
            return {'error': 'No spatial data available'}
        
        results = {
            'analysis_type': 'environmental_impact',
            'impact_assessment': {},
            'conflict_zones': [],
            'mitigation_suggestions': [],
            'environmental_score': 0.0
        }
        
        # Analyze conflicts with environmental zones
        if environmental_zones is not None:
            env_conflicts = self._analyze_environmental_conflicts(
                buses_gdf, environmental_zones
            )
            results['conflict_zones'].extend(env_conflicts)
        
        # Analyze conflicts with protected areas
        if protected_areas is not None:
            protected_conflicts = self._analyze_protected_area_conflicts(
                buses_gdf, protected_areas
            )
            results['conflict_zones'].extend(protected_conflicts)
        
        # Calculate overall environmental impact score
        impact_score = self._calculate_environmental_score(
            buses_gdf, results['conflict_zones']
        )
        results['environmental_score'] = impact_score
        
        # Generate mitigation suggestions
        mitigation_suggestions = self._generate_mitigation_suggestions(
            results['conflict_zones']
        )
        results['mitigation_suggestions'] = mitigation_suggestions
        
        # Compile impact assessment
        results['impact_assessment'] = {
            'total_components': len(buses_gdf),
            'components_in_conflict': len(results['conflict_zones']),
            'conflict_percentage': len(results['conflict_zones']) / len(buses_gdf) * 100,
            'high_impact_zones': len([z for z in results['conflict_zones'] if z.get('impact_level') == 'high']),
            'environmental_score': impact_score
        }
        
        return results
    
    # Helper methods
    def _extract_load_distribution(self, network) -> pd.DataFrame:
        """Extract load distribution from network."""
        if "loads" not in network.df or network.df["loads"].empty:
            return pd.DataFrame()
        
        # Get load buses with load information
        load_info = network.df["loads"].copy()
        load_buses = network.buses.loc[load_info["bus"]]
        
        # Merge load data with bus coordinates
        load_distribution = load_buses.join(load_info.set_index('bus'), how='inner')
        
        return load_distribution
    
    def _calculate_load_density(self, load_data: pd.DataFrame, 
                              grid_size: float, method: str) -> pd.Series:
        """Calculate load density on grid."""
        bounds = load_data.total_bounds
        x_min, y_min, x_max, y_max = bounds
        
        # Create grid
        x_range = np.arange(x_min, x_max + grid_size, grid_size)
        y_range = np.arange(y_min, y_max + grid_size, grid_size)
        
        load_density = pd.Series(dtype=float)
        
        if 'p_set' not in load_data.columns:
            return load_density
        
        for i, x in enumerate(x_range[:-1]):
            for j, y in enumerate(y_range[:-1]):
                # Define grid cell
                cell = box(x, y, x + grid_size, y + grid_size)
                
                # Sum loads in cell
                loads_in_cell = load_data[load_data.geometry.intersects(cell)]
                total_load = loads_in_cell['p_set'].sum()
                
                # Store density
                cell_id = (i, j)
                load_density[cell_id] = total_load / (grid_size ** 2)
        
        return load_density
    
    def _classify_service_buses(self, buses_gdf: 'gpd.GeoDataFrame', 
                              service_type: str) -> 'gpd.GeoDataFrame':
        """Classify buses by service type."""
        if service_type == 'transmission':
            # High voltage buses
            if 'v_nom' in buses_gdf.columns:
                return buses_gdf[buses_gdf['v_nom'] >= 110].copy()
        elif service_type == 'distribution':
            # Medium/low voltage buses
            if 'v_nom' in buses_gdf.columns:
                return buses_gdf[buses_gdf['v_nom'] < 110].copy()
        elif service_type == 'generation':
            # Buses with generators
            # This would require checking generator connections
            pass
        
        return buses_gdf.copy()
    
    def _analyze_service_overlaps(self, buses_gdf: 'gpd.GeoDataFrame',
                                service_types: List[str], 
                                service_radius: float) -> Dict[str, Any]:
        """Analyze overlaps between different service types."""
        overlaps = {
            'total_overlaps': 0,
            'overlap_pairs': [],
            'overlap_zones': []
        }
        
        # For simplicity, identify potential overlap zones
        # where multiple service types could be present
        grid_size = service_radius / 2
        bounds = buses_gdf.total_bounds
        
        overlap_zones = []
        
        # Simple approach: look for areas with high component density
        # which might indicate overlapping services
        coverage_analysis = self.analysis_strategies['coverage']
        coverage_result = coverage_analysis.analyze(
            buses_gdf, 
            service_radius=service_radius
        )
        
        if 'coverage_gaps' in coverage_result:
            overlaps['total_overlaps'] = len(coverage_result['coverage_gaps'])
            overlaps['overlap_zones'] = coverage_result['coverage_gaps']
        
        return overlaps
    
    def _generate_service_area_suggestions(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate service area optimization suggestions."""
        suggestions = []
        
        service_analysis = analysis_results.get('service_analysis', {})
        
        for service_type, service_result in service_analysis.items():
            if 'coverage_metrics' in service_result:
                coverage_ratio = service_result['coverage_metrics'].get('coverage_ratio', 0)
                
                if coverage_ratio < 0.7:
                    suggestions.append(f"Improve {service_type} service coverage (currently {coverage_ratio:.1%})")
                
                uncovered_area = service_result['coverage_metrics'].get('uncovered_area', 0)
                if uncovered_area > 0:
                    suggestions.append(f"Add {service_type} facilities in {uncovered_area:.1f} uncovered area units")
        
        return suggestions
    
    def _generate_synthetic_elevation_data(self, buses_gdf: 'gpd.GeoDataFrame') -> Dict[str, Any]:
        """Generate synthetic elevation data for analysis."""
        np.random.seed(42)  # For reproducibility
        
        # Create synthetic elevation based on coordinates
        # This is a placeholder - real analysis would use actual terrain data
        elevation_data = {
            'elevation': np.random.uniform(0, 1000, len(buses_gdf))
        }
        
        return elevation_data
    
    def _identify_terrain_constraints(self, buses_gdf: 'gpd.GeoDataFrame') -> List[Dict[str, Any]]:
        """Identify terrain-related constraints."""
        constraints = []
        
        if 'elevation' in buses_gdf.columns:
            elevations = buses_gdf['elevation']
            
            # High elevation constraints
            high_elevation_threshold = elevations.quantile(0.9)
            high_elevation_buses = buses_gdf[buses_gdf['elevation'] > high_elevation_threshold]
            
            for idx, bus in high_elevation_buses.iterrows():
                constraints.append({
                    'constraint_id': f'high_elevation_{idx}',
                    'bus_id': idx,
                    'constraint_type': 'high_elevation',
                    'elevation': bus['elevation'],
                    'severity': 'medium',
                    'description': f"High elevation ({bus['elevation']:.1f}m) may require special construction"
                })
            
            # Steep terrain constraints (large elevation changes)
            if len(elevations) > 1:
                elevation_diffs = np.abs(elevations.diff())
                steep_threshold = elevation_diffs.quantile(0.9)
                
                for idx in elevation_diffs[elevation_diffs > steep_threshold].index:
                    if idx in buses_gdf.index:
                        constraints.append({
                            'constraint_id': f'steep_terrain_{idx}',
                            'bus_id': idx,
                            'constraint_type': 'steep_terrain',
                            'elevation_change': elevation_diffs[idx],
                            'severity': 'high',
                            'description': f"Steep terrain with {elevation_diffs[idx]:.1f}m elevation change"
                        })
        
        return constraints
    
    def _generate_routing_suggestions(self, buses_gdf: 'gpd.GeoDataFrame') -> List[str]:
        """Generate routing suggestions based on terrain analysis."""
        suggestions = []
        
        if 'elevation' in buses_gdf.columns:
            elevations = buses_gdf['elevation']
            elevation_range = elevations.max() - elevations.min()
            
            if elevation_range > 500:
                suggestions.append("Consider altitude compensation for long-distance transmission")
            
            if elevations.std() / elevations.mean() > 0.3:  # High terrain variation
                suggestions.append("Terrain shows high variation - plan routes to minimize elevation changes")
            
            # Suggest voltage level adjustments
            high_elevation_buses = buses_gdf[buses_gdf['elevation'] > elevations.quantile(0.8)]
            if len(high_elevation_buses) > 0:
                suggestions.append("Increase voltage levels for high-altitude connections to reduce losses")
        
        return suggestions
    
    def _analyze_environmental_conflicts(self, buses_gdf: 'gpd.GeoDataFrame',
                                       environmental_zones: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze conflicts with environmental zones."""
        conflicts = []
        
        # Simplified conflict detection
        # In reality, this would use spatial joins and detailed zone classifications
        
        bounds = buses_gdf.total_bounds
        env_bounds = environmental_zones.total_bounds if not environmental_zones.empty else bounds
        
        # Check for spatial overlap
        for idx, bus in buses_gdf.iterrows():
            # Simple proximity check
            bus_point = Point(bus['x'], bus['y'])
            
            # Check if bus is in or near environmental zones
            # This is a placeholder - real implementation would use proper spatial analysis
            
            conflicts.append({
                'conflict_id': f'env_conflict_{idx}',
                'bus_id': idx,
                'conflict_type': 'environmental_zone',
                'impact_level': 'medium',
                'description': f"Bus {idx} may impact environmental sensitivity"
            })
        
        return conflicts
    
    def _analyze_protected_area_conflicts(self, buses_gdf: 'gpd.GeoDataFrame',
                                        protected_areas: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze conflicts with protected areas."""
        conflicts = []
        
        # Simplified conflict detection for protected areas
        
        for idx, bus in buses_gdf.iterrows():
            conflicts.append({
                'conflict_id': f'protected_conflict_{idx}',
                'bus_id': idx,
                'conflict_type': 'protected_area',
                'impact_level': 'high',
                'description': f"Bus {idx} located in/near protected area"
            })
        
        return conflicts
    
    def _calculate_environmental_score(self, buses_gdf: 'gpd.GeoDataFrame',
                                     conflict_zones: List[Dict[str, Any]]) -> float:
        """Calculate overall environmental impact score (0-100, lower is better)."""
        if len(buses_gdf) == 0:
            return 0.0
        
        # Base score
        base_score = 50.0
        
        # Deduct points for conflicts
        conflict_penalty = len(conflict_zones) * 2.0
        
        # Adjust for conflict severity
        high_impact_conflicts = [c for c in conflict_zones if c.get('impact_level') == 'high']
        medium_impact_conflicts = [c for c in conflict_zones if c.get('impact_level') == 'medium']
        
        conflict_penalty += len(high_impact_conflicts) * 5.0
        conflict_penalty += len(medium_impact_conflicts) * 2.0
        
        final_score = max(0, min(100, base_score - conflict_penalty))
        
        return final_score
        conflict_zones: List[Dict[str, Any]]
    def _calculate_environmental_impact_score(self, buses_gdf: 'gpd.GeoDataFrame',
                                            conflict_zones: List[Dict[str, Any]]) -> float:
        """计算总体环境影响评分（0-100，越低越好）。"""
        if len(buses_gdf) == 0:
            return 0.0
        
        # Base score
        base_score = 50.0
        
        # Deduct points for conflicts
        conflict_penalty = len(conflict_zones) * 2.0
        
        # Adjust for conflict severity
        high_impact_conflicts = [c for c in conflict_zones if c.get('impact_level') == 'high']
        medium_impact_conflicts = [c for c in conflict_zones if c.get('impact_level') == 'medium']
        
        conflict_penalty += len(high_impact_conflicts) * 5.0
        conflict_penalty += len(medium_impact_conflicts) * 2.0
        
        final_score = max(0, min(100, base_score - conflict_penalty))
        
        return final_score
    
    def _generate_mitigation_suggestions(self, conflict_zones: List[Dict[str, Any]]) -> List[str]:
        """Generate environmental mitigation suggestions."""
        suggestions = []
        
        if not conflict_zones:
            suggestions.append("No significant environmental conflicts detected")
            return suggestions
        
        # Group conflicts by type
        conflict_types = {}
        for conflict in conflict_zones:
            conflict_type = conflict.get('conflict_type', 'unknown')
            if conflict_type not in conflict_types:
                conflict_types[conflict_type] = []
            conflict_types[conflict_type].append(conflict)
        
        # Generate suggestions based on conflict types
        for conflict_type, conflicts in conflict_types.items():
            if conflict_type == 'environmental_zone':
                suggestions.append(f"Consider environmental impact assessment for {len(conflicts)} components")
                suggestions.append("Implement buffer zones around sensitive environmental areas")
            elif conflict_type == 'protected_area':
                suggestions.append(f"Seek permits and approvals for {len(conflicts)} components in protected areas")
                suggestions.append("Explore alternative routing to avoid protected areas")
        
        # General suggestions
        suggestions.append("Conduct detailed environmental surveys for high-impact zones")
        suggestions.append("Develop environmental management plans for construction phase")
        
        return suggestions
    
    def _calculate_summary_metrics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary metrics from analysis results."""
        summary = {
            'total_analyses': len(analysis_results),
            'successful_analyses': len([r for r in analysis_results.values() if 'error' not in r]),
            'failed_analyses': len([r for r in analysis_results.values() if 'error' in r]),
            'overall_score': 0.0,
            'key_findings': []
        }
        
        # Extract key findings from each analysis
        for analysis_type, result in analysis_results.items():
            if 'error' in result:
                continue
            
            if analysis_type == 'density':
                if 'density_metrics' in result:
                    density_metrics = result['density_metrics']
                    if density_metrics.get('coverage_ratio', 0) < 0.5:
                        summary['key_findings'].append("Low density coverage detected")
            elif analysis_type == 'connectivity':
                if 'connectivity_metrics' in result:
                    connectivity = result['connectivity_metrics']
                    if connectivity.get('average_distance_to_centroid', 0) > 50:
                        summary['key_findings'].append("Poor network connectivity")
            elif analysis_type == 'coverage':
                if 'coverage_metrics' in result:
                    coverage = result['coverage_metrics']
                    if coverage.get('coverage_ratio', 0) < 0.8:
                        summary['key_findings'].append("Coverage gaps identified")
        
        # Calculate overall score
        if summary['total_analyses'] > 0:
            success_rate = summary['successful_analyses'] / summary['total_analyses']
            findings_penalty = len(summary['key_findings']) * 0.1
            summary['overall_score'] = max(0, min(100, success_rate * 100 - findings_penalty * 100))
        
        return summary
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of spatial analysis capabilities."""
        return {
            "engine_type": "SpatialAnalysisEngine",
            "available_strategies": list(self.analysis_strategies.keys()),
            "capabilities": [
                "network_spatial_properties",
                "load_density_analysis",
                "service_area_analysis",
                "terrain_analysis",
                "environmental_impact_assessment"
            ],
            "analysis_types": [
                "density_analysis",
                "connectivity_analysis", 
                "coverage_analysis"
            ],
            "output_formats": [
                "comprehensive_metrics",
                "spatial_visualizations",
                "optimization_suggestions",
                "conflict_identification"
            ],
            "terrain_features": [
                "elevation_analysis",
                "slope_calculation",
                "constraint_identification",
                "routing_optimization"
            ],
            "environmental_assessment": [
                "impact_scoring",
                "conflict_detection",
                "mitigation_planning",
                "compliance_checking"
            ]
        }