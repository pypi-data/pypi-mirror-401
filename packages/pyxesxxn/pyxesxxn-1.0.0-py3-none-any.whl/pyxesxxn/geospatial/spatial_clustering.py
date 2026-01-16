"""
Spatial Clustering Engine for PyPSA networks.

Provides spatial clustering algorithms for energy system modeling:
- K-means clustering
- Hierarchical clustering  
- DBSCAN clustering
- Grid-based clustering
- Custom clustering strategies
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from abc import ABC, abstractmethod

import warnings

try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    warnings.warn("Scikit-learn not installed. Clustering features will be limited.", UserWarning)

from .base import GeospatialProcessor


class ClusteringStrategy(ABC):
    """Abstract base class for clustering strategies."""
    
    @abstractmethod
    def fit_predict(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Fit clustering algorithm and predict cluster labels.
        
        Parameters
        ----------
        data : np.ndarray
            Input data for clustering
        **kwargs
            Algorithm-specific parameters
            
        Returns
        -------
        np.ndarray
            Cluster labels
        """
        pass


class KMeansStrategy(ClusteringStrategy):
    """K-means clustering strategy."""
    
    def __init__(self, n_clusters: int = 8, random_state: int = 42):
        """Initialize K-means clustering.
        
        Parameters
        ----------
        n_clusters : int
            Number of clusters
        random_state : int
            Random state for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = None
        
    def fit_predict(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Fit K-means and predict clusters."""
        if not HAS_SKLEARN:
            raise ImportError("Scikit-learn required for K-means clustering")
        
        # Handle parameters
        n_clusters = kwargs.get('n_clusters', self.n_clusters)
        
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=self.random_state,
            **kwargs
        )
        
        return self.model.fit_predict(data)


class DBSCANStrategy(ClusteringStrategy):
    """DBSCAN clustering strategy."""
    
    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        """Initialize DBSCAN clustering.
        
        Parameters
        ----------
        eps : float
            Maximum distance between two samples for them to be in same neighborhood
        min_samples : int
            Minimum samples in neighborhood for a point to be core point
        """
        self.eps = eps
        self.min_samples = min_samples
        self.model = None
        
    def fit_predict(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Fit DBSCAN and predict clusters."""
        if not HAS_SKLEARN:
            raise ImportError("Scikit-learn required for DBSCAN clustering")
        
        # Handle parameters
        eps = kwargs.get('eps', self.eps)
        min_samples = kwargs.get('min_samples', self.min_samples)
        
        self.model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            **kwargs
        )
        
        return self.model.fit_predict(data)


class HierarchicalStrategy(ClusteringStrategy):
    """Hierarchical clustering strategy."""
    
    def __init__(self, n_clusters: int = 8, linkage: str = 'ward'):
        """Initialize hierarchical clustering.
        
        Parameters
        ----------
        n_clusters : int
            Number of clusters
        linkage : str
            Linkage criterion ('ward', 'complete', 'average', 'single')
        """
        self.n_clusters = n_clusters
        self.linkage = linkage
        self.model = None
        
    def fit_predict(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Fit hierarchical clustering and predict clusters."""
        if not HAS_SKLEARN:
            raise ImportError("Scikit-learn required for hierarchical clustering")
        
        # Handle parameters
        n_clusters = kwargs.get('n_clusters', self.n_clusters)
        linkage = kwargs.get('linkage', self.linkage)
        
        self.model = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage=linkage,
            **kwargs
        )
        
        return self.model.fit_predict(data)


class SpatialClusteringEngine(GeospatialProcessor):
    """Engine for spatial clustering of energy system components."""
    
    def __init__(self, crs: str = "EPSG:4326", units: str = "degrees"):
        """Initialize spatial clustering engine.
        
        Parameters
        ----------
        crs : str
            Coordinate Reference System
        units : str
            Unit system for measurements
        """
        super().__init__(crs, units)
        self.clustering_strategies = {
            'kmeans': KMeansStrategy(),
            'dbscan': DBSCANStrategy(),
            'hierarchical': HierarchicalStrategy()
        }
        self.scaler = StandardScaler()
        
    def register_clustering_strategy(self, name: str, strategy: ClusteringStrategy) -> None:
        """Register custom clustering strategy.
        
        Parameters
        ----------
        name : str
            Strategy name
        strategy : ClusteringStrategy
            Clustering strategy instance
        """
        self.clustering_strategies[name] = strategy
    
    def cluster_network_buses(self, network, 
                             strategy: str = 'kmeans',
                             algorithm_params: Optional[Dict[str, Any]] = None,
                             preprocessing_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Cluster network buses based on spatial location.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to cluster
        strategy : str
            Clustering strategy ('kmeans', 'dbscan', 'hierarchical')
        algorithm_params : Dict[str, Any], optional
            Parameters for clustering algorithm
        preprocessing_params : Dict[str, Any], optional
            Parameters for data preprocessing
            
        Returns
        -------
        pd.DataFrame
            Clustering results with bus IDs and cluster labels
        """
        if "buses" not in network.df or network.df["buses"].empty:
            raise ValueError("Network contains no buses for clustering")
        
        # Extract coordinate data
        buses_gdf = self.extract_coordinates_from_network(network)
        
        if buses_gdf.empty:
            raise ValueError("No coordinate data available for clustering")
        
        # Prepare clustering data
        clustering_data = self._prepare_clustering_data(
            buses_gdf, preprocessing_params or {}
        )
        
        # Apply clustering
        if strategy not in self.clustering_strategies:
            raise ValueError(f"Unknown clustering strategy: {strategy}")
        
        strategy_instance = self.clustering_strategies[strategy]
        cluster_labels = strategy_instance.fit_predict(
            clustering_data, **(algorithm_params or {})
        )
        
        # Create results DataFrame
        results = buses_gdf.copy()
        results['cluster_id'] = cluster_labels
        results['cluster_strategy'] = strategy
        
        # Add cluster statistics
        results = self._add_cluster_statistics(results)
        
        return results
    
    def _prepare_clustering_data(self, buses_gdf: 'gpd.GeoDataFrame', 
                               params: Dict[str, Any]) -> np.ndarray:
        """Prepare data for clustering.
        
        Parameters
        ----------
        buses_gdf : gpd.GeoDataFrame
            Bus data with coordinates
        params : Dict[str, Any]
            Preprocessing parameters
            
        Returns
        -------
        np.ndarray
            Preprocessed data for clustering
        """
        # Extract coordinate features
        features = ['x', 'y']
        
        # Add voltage level as feature if available
        if 'v_nom' in buses_gdf.columns:
            features.append('v_nom')
            
        # Add load magnitude as feature if available
        if 'p_set' in buses_gdf.columns:
            features.append('p_set')
        
        # Extract feature matrix
        data_matrix = buses_gdf[features].values
        
        # Handle missing values
        data_matrix = pd.DataFrame(data_matrix).fillna(0).values
        
        # Apply scaling if requested
        if params.get('scale_data', True):
            data_matrix = self.scaler.fit_transform(data_matrix)
        
        # Add spatial weight if requested
        if params.get('add_spatial_weight', False):
            spatial_weight = params.get('spatial_weight', 0.5)
            # Apply spatial weighting to coordinate features
            data_matrix[:, :2] *= (1 + spatial_weight)
        
        return data_matrix
    
    def _add_cluster_statistics(self, results: 'gpd.GeoDataFrame') -> 'gpd.GeoDataFrame':
        """Add cluster statistics to results.
        
        Parameters
        ----------
        results : gpd.GeoDataFrame
            Clustering results
            
        Returns
        -------
        gpd.GeoDataFrame
            Results with added cluster statistics
        """
        cluster_stats = results.groupby('cluster_id').agg({
            'x': ['mean', 'std', 'min', 'max'],
            'y': ['mean', 'std', 'min', 'max'],
            'geometry': 'count'  # Number of buses per cluster
        }).round(4)
        
        # Flatten column names
        cluster_stats.columns = ['_'.join(col).strip() for col in cluster_stats.columns]
        cluster_stats = cluster_stats.rename(columns={'geometry_count': 'bus_count'})
        
        # Merge statistics back to results
        results = results.merge(
            cluster_stats, 
            left_on='cluster_id', 
            right_index=True, 
            suffixes=('', '_cluster_stats')
        )
        
        return results
    
    def cluster_by_voltage_level(self, network, 
                               voltage_levels: Optional[List[float]] = None) -> pd.DataFrame:
        """Cluster buses by voltage level.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        voltage_levels : List[float], optional
            Voltage levels to consider
            
        Returns
        -------
        pd.DataFrame
            Clustering results by voltage level
        """
        if "buses" not in network.df or network.df["buses"].empty:
            raise ValueError("Network contains no buses")
        
        buses_gdf = self.extract_coordinates_from_network(network)
        
        if 'v_nom' not in buses_gdf.columns:
            raise ValueError("Network buses have no voltage level information")
        
        if voltage_levels is None:
            # Auto-detect voltage levels
            voltage_levels = sorted(buses_gdf['v_nom'].unique())
        
        # Create voltage-based clusters
        results = []
        
        for voltage in voltage_levels:
            voltage_buses = buses_gdf[buses_gdf['v_nom'] == voltage].copy()
            
            if not voltage_buses.empty:
                voltage_buses['cluster_id'] = f"voltage_{int(voltage)}kV"
                results.append(voltage_buses)
        
        if results:
            return pd.concat(results, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def cluster_by_functional_zones(self, network, 
                                  zone_types: Optional[List[str]] = None) -> pd.DataFrame:
        """Cluster buses by functional zones (urban, rural, industrial, etc.).
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        zone_types : List[str], optional
            Zone types to consider
            
        Returns
        -------
        pd.DataFrame
            Clustering results by functional zones
        """
        if "buses" not in network.df or network.df["buses"].empty:
            raise ValueError("Network contains no buses")
        
        buses_gdf = self.extract_coordinates_from_network(network)
        
        # Define default zone classification rules
        if zone_types is None:
            zone_types = ['urban', 'suburban', 'rural', 'industrial', 'commercial']
        
        # Classify buses into functional zones
        results = self._classify_functional_zones(buses_gdf, zone_types)
        
        return results
    
    def _classify_functional_zones(self, buses_gdf: 'gpd.GeoDataFrame', 
                                 zone_types: List[str]) -> 'gpd.GeoDataFrame':
        """Classify buses into functional zones based on available data.
        
        Parameters
        ----------
        buses_gdf : gpd.GeoDataFrame
            Bus data
        zone_types : List[str]
            Zone types to consider
            
        Returns
        -------
        gpd.GeoDataFrame
            Buses with functional zone classification
        """
        results = buses_gdf.copy()
        results['cluster_id'] = 'unclassified'
        
        # Classification based on available attributes
        for bus_id, row in results.iterrows():
            bus_name = str(row.get('name', '')).lower()
            bus_v_nom = row.get('v_nom', 0)
            load_info = str(row.get('type', '')).lower()
            
            # Industrial zones
            if any(keyword in bus_name for keyword in ['industrial', 'factory', 'plant', 'manufacturing']):
                results.loc[bus_id, 'cluster_id'] = 'industrial'
            
            # Commercial zones
            elif any(keyword in bus_name for keyword in ['commercial', 'shopping', 'office', 'business']):
                results.loc[bus_id, 'cluster_id'] = 'commercial'
            
            # Rural zones (low voltage, agricultural keywords)
            elif (bus_v_nom <= 20 and 
                  any(keyword in bus_name for keyword in ['farm', 'agricultural', 'rural', 'ag'])):
                results.loc[bus_id, 'cluster_id'] = 'rural'
            
            # Urban zones (high density indicators)
            elif (bus_v_nom >= 110 or 
                  any(keyword in bus_name for keyword in ['urban', 'city', 'downtown', 'central'])):
                results.loc[bus_id, 'cluster_id'] = 'urban'
            
            # Default classification based on voltage level
            else:
                if bus_v_nom >= 110:
                    results.loc[bus_id, 'cluster_id'] = 'transmission'
                elif bus_v_nom >= 20:
                    results.loc[bus_id, 'cluster_id'] = 'suburban'
                else:
                    results.loc[bus_id, 'cluster_id'] = 'residential'
        
        return results
    
    def cluster_islanded_systems(self, network, connection_tolerance: float = 0.01) -> pd.DataFrame:
        """Identify and cluster islanded/isolated systems.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network
        connection_tolerance : float
            Distance tolerance for considering buses connected
            
        Returns
        -------
        pd.DataFrame
            Islanded system clusters
        """
        if "buses" not in network.df or network.df["buses"].empty:
            raise ValueError("Network contains no buses")
        
        if "links" not in network.df or network.df["links"].empty:
            # No connections, all buses are islanded
            buses_gdf = self.extract_coordinates_from_network(network)
            buses_gdf['cluster_id'] = 'islanded_system'
            return buses_gdf
        
        buses_gdf = self.extract_coordinates_from_network(network)
        
        # Build connection graph
        connection_matrix = self._build_connection_matrix(buses_gdf, connection_tolerance)
        
        # Find connected components
        clusters = self._find_connected_components(connection_matrix)
        
        # Assign cluster labels
        buses_gdf['cluster_id'] = clusters
        
        return buses_gdf
    
    def process_network_geospatial(self, network, **kwargs) -> Any:
        """Process network with geospatial analysis.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to process
        **kwargs
            Additional parameters
            
        Returns
        -------
        Any
            Processed network data
        """
        if not HAS_SKLEARN:
            raise ImportError("Scikit-learn required for spatial clustering")
        
        # Extract bus coordinates from network
        buses_gdf = self.extract_coordinates_from_network(network)
        
        # Perform clustering
        strategy = kwargs.get('strategy', 'kmeans')
        n_clusters = kwargs.get('n_clusters', 8)
        
        if strategy == 'kmeans':
            cluster_labels = self.cluster_network_buses(
                network, strategy='kmeans', n_clusters=n_clusters
            )
        else:
            cluster_labels = self.cluster_network_buses(network, strategy=strategy)
        
        return cluster_labels
    
    def _build_connection_matrix(self, buses_gdf: 'gpd.GeoDataFrame', 
                               tolerance: float) -> np.ndarray:
        """Build connection matrix based on network links and spatial proximity.
        
        Parameters
        ----------
        buses_gdf : gpd.GeoDataFrame
            Bus data
        tolerance : float
            Connection tolerance
            
        Returns
        -------
        np.ndarray
            Binary connection matrix
        """
        n_buses = len(buses_gdf)
        connection_matrix = np.zeros((n_buses, n_buses), dtype=bool)
        
        # Check direct connections from network links
        if "links" in network.df:
            for _, link in network.df["links"].iterrows():
                if link['bus0'] in buses_gdf.index and link['bus1'] in buses_gdf.index:
                    bus0_idx = list(buses_gdf.index).index(link['bus0'])
                    bus1_idx = list(buses_gdf.index).index(link['bus1'])
                    connection_matrix[bus0_idx, bus1_idx] = True
                    connection_matrix[bus1_idx, bus0_idx] = True
        
        # Check spatial proximity (within tolerance)
        coordinates = buses_gdf[['x', 'y']].values
        
        for i in range(n_buses):
            for j in range(i + 1, n_buses):
                distance = self.calculate_distance(
                    tuple(coordinates[i]), tuple(coordinates[j])
                )
                
                if distance <= tolerance:
                    connection_matrix[i, j] = True
                    connection_matrix[j, i] = True
        
        return connection_matrix
    
    def _find_connected_components(self, connection_matrix: np.ndarray) -> List[int]:
        """Find connected components in the graph.
        
        Parameters
        ----------
        connection_matrix : np.ndarray
            Binary connection matrix
            
        Returns
        -------
        List[int]
            Cluster labels for each node
        """
        n_nodes = len(connection_matrix)
        visited = [False] * n_nodes
        cluster_labels = [-1] * n_nodes
        current_cluster = 0
        
        def dfs(node: int):
            """Depth-first search for connected component."""
            stack = [node]
            
            while stack:
                current = stack.pop()
                
                if not visited[current]:
                    visited[current] = True
                    cluster_labels[current] = current_cluster
                    
                    # Add connected neighbors to stack
                    for neighbor in range(n_nodes):
                        if (connection_matrix[current, neighbor] and 
                            not visited[neighbor]):
                            stack.append(neighbor)
        
        for node in range(n_nodes):
            if not visited[node]:
                dfs(node)
                current_cluster += 1
        
        return cluster_labels
    
    def evaluate_clustering_quality(self, clustering_results: pd.DataFrame, 
                                  network) -> Dict[str, float]:
        """Evaluate quality of clustering results.
        
        Parameters
        ----------
        clustering_results : pd.DataFrame
            Results from clustering
        network : pypsa.Network
            Original network
            
        Returns
        -------
        Dict[str, float]
            Quality metrics
        """
        if 'cluster_id' not in clustering_results.columns:
            raise ValueError("Clustering results must contain cluster_id column")
        
        metrics = {}
        
        # Number of clusters
        metrics['n_clusters'] = clustering_results['cluster_id'].nunique()
        
        # Cluster size distribution
        cluster_sizes = clustering_results.groupby('cluster_id').size()
        metrics['avg_cluster_size'] = cluster_sizes.mean()
        metrics['std_cluster_size'] = cluster_sizes.std()
        metrics['min_cluster_size'] = cluster_sizes.min()
        metrics['max_cluster_size'] = cluster_sizes.max()
        
        # Silhouette score (if sklearn available)
        if HAS_SKLEARN:
            try:
                from sklearn.metrics import silhouette_score
                
                features = clustering_results[['x', 'y']].values
                labels = clustering_results['cluster_id'].values
                
                if len(np.unique(labels)) > 1:
                    metrics['silhouette_score'] = silhouette_score(features, labels)
                else:
                    metrics['silhouette_score'] = 0.0
            except:
                metrics['silhouette_score'] = 0.0
        else:
            metrics['silhouette_score'] = 0.0
        
        # Spatial dispersion within clusters
        if 'x_cluster_stats' in clustering_results.columns:
            metrics['avg_within_cluster_variance'] = clustering_results['x_std_cluster_stats'].mean()
        
        return metrics
    
    def create_cluster_network(self, clustering_results: pd.DataFrame, 
                             network, 
                             aggregation_method: str = 'representative') -> 'Network':
        """Create a network representing the clustering results.
        
        Parameters
        ----------
        clustering_results : pd.DataFrame
            Clustering results
        network : pypsa.Network
            Original network
        aggregation_method : str
            Method for aggregating cluster properties
            
        Returns
        -------
        Network
            Network with aggregated clusters
        """
        from pypsa import Network
        
        # Create new network
        cluster_network = Network()
        
        # Create cluster buses
        cluster_buses = self._aggregate_cluster_properties(
            clustering_results, aggregation_method
        )
        
        for bus_id, bus_data in cluster_buses.iterrows():
            cluster_network.add("Bus", bus_id, **bus_data.to_dict())
        
        # Create inter-cluster links (simplified)
        self._create_inter_cluster_links(
            cluster_network, clustering_results, network
        )
        
        return cluster_network
    
    def _aggregate_cluster_properties(self, clustering_results: pd.DataFrame,
                                    method: str) -> pd.DataFrame:
        """Aggregate properties within clusters.
        
        Parameters
        ----------
        clustering_results : pd.DataFrame
            Clustering results
        method : str
            Aggregation method
            
        Returns
        -------
        pd.DataFrame
            Aggregated cluster properties
        """
        aggregated = {}
        
        for cluster_id, cluster_data in clustering_results.groupby('cluster_id'):
            cluster_info = {}
            
            # Aggregate coordinates (centroid)
            cluster_info['x'] = cluster_data['x'].mean()
            cluster_info['y'] = cluster_data['y'].mean()
            
            # Aggregate voltage level (mode)
            if 'v_nom' in cluster_data.columns:
                cluster_info['v_nom'] = cluster_data['v_nom'].mode().iloc[0]
            
            # Aggregate load (sum)
            if 'p_set' in cluster_data.columns:
                cluster_info['total_load'] = cluster_data['p_set'].sum()
            
            # Add cluster metadata
            cluster_info['cluster_id'] = cluster_id
            cluster_info['n_original_buses'] = len(cluster_data)
            
            aggregated[f'cluster_{cluster_id}'] = cluster_info
        
        return pd.DataFrame.from_dict(aggregated, orient='index')
    
    def _create_inter_cluster_links(self, cluster_network: 'Network', 
                                  clustering_results: pd.DataFrame, 
                                  original_network: 'Network') -> None:
        """Create links between clusters in the new network.
        
        Parameters
        ----------
        cluster_network : Network
            Network to add links to
        clustering_results : pd.DataFrame
            Clustering results
        original_network : Network
            Original network with connection information
        """
        # Simplified approach: create links between cluster centroids
        cluster_centers = clustering_results.groupby('cluster_id')[['x', 'y']].mean()
        
        cluster_names = cluster_centers.index.tolist()
        
        for i in range(len(cluster_names)):
            for j in range(i + 1, len(cluster_names)):
                cluster1, cluster2 = cluster_names[i], cluster_names[j]
                
                # Calculate distance
                coord1 = (cluster_centers.loc[cluster1, 'x'], cluster_centers.loc[cluster1, 'y'])
                coord2 = (cluster_centers.loc[cluster2, 'x'], cluster_centers.loc[cluster2, 'y'])
                distance = self.calculate_distance(coord1, coord2, "km")
                
                # Add link with capacity proportional to inverse of distance
                capacity = max(10, 1000 / (distance + 1))  # MW
                
                cluster_network.add(
                    "Link",
                    f"link_{cluster1}_{cluster2}",
                    bus0=f"cluster_{cluster1}",
                    bus1=f"cluster_{cluster2}",
                    p_nom=capacity,
                    marginal_cost=distance * 0.1,
                    efficiency=0.95
                )
    
    def get_clustering_summary(self) -> Dict[str, Any]:
        """Get summary of clustering capabilities.
        
        Returns
        -------
        Dict[str, Any]
            Summary of available strategies and capabilities
        """
        return {
            "engine_type": "SpatialClusteringEngine",
            "available_strategies": list(self.clustering_strategies.keys()),
            "capabilities": [
                "kmeans_clustering",
                "dbscan_clustering", 
                "hierarchical_clustering",
                "voltage_level_clustering",
                "functional_zone_clustering",
                "islanded_system_detection",
                "clustering_evaluation",
                "cluster_network_creation"
            ],
            "preprocessing_options": [
                "data_scaling",
                "spatial_weighting", 
                "feature_selection"
            ],
            "quality_metrics": [
                "n_clusters",
                "cluster_size_distribution",
                "silhouette_score",
                "spatial_dispersion"
            ],
            "aggregation_methods": [
                "representative",
                "centroid",
                "weighted_average"
            ]
        }