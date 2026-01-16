"""
Geospatial visualization module for PyXESXXN.

This module provides visualization capabilities for geospatial data analysis,
including map plotting, heatmaps, and interactive visualizations.
"""

import warnings
from typing import Optional, Dict, Any, List, Union
import numpy as np
import pandas as pd

# Optional imports for visualization
try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib.patches import Polygon as MplPolygon
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None
    mcolors = None
    MplPolygon = None
    warnings.warn("matplotlib is not available. Some visualization features will be disabled.")

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    folium = None
    warnings.warn("folium is not available. Interactive map features will be disabled.")

from .base import GeospatialProcessor


class GeospatialVisualizer:
    """
    Geospatial visualization engine for PyXESXXN.
    
    This class provides methods for creating various types of geospatial visualizations
    including static maps, interactive maps, heatmaps, and thematic maps.
    """
    
    def __init__(self, geospatial_processor: Optional[GeospatialProcessor] = None):
        """
        Initialize the geospatial visualizer.
        
        Args:
            geospatial_processor: Optional GeospatialProcessor instance for coordinate handling
        """
        self.geospatial_processor = geospatial_processor
        self._default_crs = "EPSG:4326"  # WGS84
        
    def create_static_map(self, 
                         data: Union[pd.DataFrame, Dict],
                         geometry_column: str = "geometry",
                         value_column: Optional[str] = None,
                         title: str = "Geospatial Map",
                         figsize: tuple = (12, 8),
                         cmap: str = "viridis",
                         alpha: float = 0.7,
                         **kwargs) -> Optional[Any]:
        """
        Create a static map visualization.
        
        Args:
            data: DataFrame or dictionary containing geospatial data
            geometry_column: Name of the geometry column
            value_column: Name of the column to use for coloring
            title: Map title
            figsize: Figure size (width, height)
            cmap: Colormap for value-based coloring
            alpha: Transparency level
            **kwargs: Additional plotting parameters
            
        Returns:
            matplotlib Figure object if matplotlib is available, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE:
            warnings.warn("matplotlib is required for static map creation")
            return None
            
        fig, ax = plt.subplots(figsize=figsize)
        
        if isinstance(data, pd.DataFrame):
            # Handle DataFrame input
            geometries = data[geometry_column]
            
            if value_column and value_column in data.columns:
                values = data[value_column]
                # Create scatter plot with color coding
                scatter = ax.scatter(
                    [geom.x for geom in geometries],
                    [geom.y for geom in geometries],
                    c=values,
                    cmap=cmap,
                    alpha=alpha,
                    **kwargs
                )
                plt.colorbar(scatter, ax=ax, label=value_column)
            else:
                # Simple point plot
                ax.scatter(
                    [geom.x for geom in geometries],
                    [geom.y for geom in geometries],
                    alpha=alpha,
                    **kwargs
                )
        
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def create_interactive_map(self,
                              data: Union[pd.DataFrame, Dict],
                              geometry_column: str = "geometry",
                              value_column: Optional[str] = None,
                              location: tuple = (0, 0),
                              zoom_start: int = 10,
                              tiles: str = "OpenStreetMap",
                              **kwargs) -> Optional[Any]:
        """
        Create an interactive map using folium.
        
        Args:
            data: DataFrame or dictionary containing geospatial data
            geometry_column: Name of the geometry column
            value_column: Name of the column to use for popup information
            location: Initial map center (lat, lon)
            zoom_start: Initial zoom level
            tiles: Map tile provider
            **kwargs: Additional folium parameters
            
        Returns:
            folium Map object if folium is available, None otherwise
        """
        if not FOLIUM_AVAILABLE:
            warnings.warn("folium is required for interactive map creation")
            return None
            
        m = folium.Map(location=location, zoom_start=zoom_start, tiles=tiles)
        
        if isinstance(data, pd.DataFrame):
            for idx, row in data.iterrows():
                geom = row[geometry_column]
                popup_text = f"Index: {idx}"
                
                if value_column and value_column in row:
                    popup_text += f"<br>{value_column}: {row[value_column]}"
                
                folium.Marker(
                    [geom.y, geom.x],
                    popup=folium.Popup(popup_text, max_width=300),
                    **kwargs
                ).add_to(m)
        
        return m
    
    def create_heatmap(self,
                       data: Union[pd.DataFrame, Dict],
                       geometry_column: str = "geometry",
                       value_column: Optional[str] = None,
                       resolution: int = 100,
                       blur: float = 0.5,
                       radius: int = 15,
                       **kwargs) -> Optional[Any]:
        """
        Create a heatmap visualization.
        
        Args:
            data: DataFrame or dictionary containing geospatial data
            geometry_column: Name of the geometry column
            value_column: Name of the column to use for heat intensity
            resolution: Heatmap resolution
            blur: Heatmap blur factor
            radius: Heatmap point radius
            **kwargs: Additional folium heatmap parameters
            
        Returns:
            folium Map object with heatmap layer if folium is available, None otherwise
        """
        if not FOLIUM_AVAILABLE:
            warnings.warn("folium is required for heatmap creation")
            return None
            
        if isinstance(data, pd.DataFrame) and value_column in data.columns:
            # Prepare data for heatmap
            heat_data = []
            for _, row in data.iterrows():
                geom = row[geometry_column]
                value = row[value_column]
                heat_data.append([geom.y, geom.x, value])
            
            # Create base map
            m = folium.Map(location=[0, 0], zoom_start=2)
            
            # Add heatmap layer
            from folium.plugins import HeatMap
            HeatMap(heat_data, radius=radius, blur=blur, **kwargs).add_to(m)
            
            return m
        
        return None
    
    def create_thematic_map(self,
                           data: pd.DataFrame,
                           geometry_column: str = "geometry",
                           category_column: str = None,
                           color_scheme: Optional[Dict] = None,
                           **kwargs) -> Optional[Any]:
        """
        Create a thematic map with categorical coloring.
        
        Args:
            data: DataFrame containing geospatial data
            geometry_column: Name of the geometry column
            category_column: Name of the categorical column
            color_scheme: Optional color mapping for categories
            **kwargs: Additional plotting parameters
            
        Returns:
            matplotlib Figure object if matplotlib is available, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE:
            warnings.warn("matplotlib is required for thematic map creation")
            return None
            
        if category_column not in data.columns:
            warnings.warn(f"Category column '{category_column}' not found in data")
            return None
            
        categories = data[category_column].unique()
        
        # Generate color scheme if not provided
        if color_scheme is None:
            color_scheme = {}
            cmap = plt.cm.Set3
            for i, category in enumerate(categories):
                color_scheme[category] = cmap(i / len(categories))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for category in categories:
            category_data = data[data[category_column] == category]
            geometries = category_data[geometry_column]
            
            ax.scatter(
                [geom.x for geom in geometries],
                [geom.y for geom in geometries],
                c=[color_scheme[category]] * len(geometries),
                label=category,
                alpha=0.7,
                **kwargs
            )
        
        ax.legend(title=category_column)
        ax.set_title(f"Thematic Map - {category_column}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def save_map(self, 
                 map_obj: Union[Any, Any], 
                 filename: str, 
                 **kwargs) -> bool:
        """
        Save a map to file.
        
        Args:
            map_obj: Map object to save (matplotlib Figure or folium Map)
            filename: Output filename
            **kwargs: Additional save parameters
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if isinstance(map_obj, plt.Figure):
                map_obj.savefig(filename, bbox_inches='tight', **kwargs)
                return True
            elif isinstance(map_obj, folium.Map):
                map_obj.save(filename)
                return True
            else:
                warnings.warn(f"Unsupported map object type: {type(map_obj)}")
                return False
        except Exception as e:
            warnings.warn(f"Failed to save map: {e}")
            return False
    
    def plot_network_topology(self,
                             nodes: pd.DataFrame,
                             edges: pd.DataFrame,
                             node_geometry_column: str = "geometry",
                             edge_geometry_column: str = "geometry",
                             node_size_column: Optional[str] = None,
                             edge_width_column: Optional[str] = None,
                             **kwargs) -> Optional[Any]:
        """
        Plot network topology with nodes and edges.
        
        Args:
            nodes: DataFrame containing node data
            edges: DataFrame containing edge data
            node_geometry_column: Name of the node geometry column
            edge_geometry_column: Name of the edge geometry column
            node_size_column: Optional column for node sizing
            edge_width_column: Optional column for edge width
            **kwargs: Additional plotting parameters
            
        Returns:
            matplotlib Figure object if matplotlib is available, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE:
            warnings.warn("matplotlib is required for network topology plotting")
            return None
            
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot edges
        for _, edge in edges.iterrows():
            edge_geom = edge[edge_geometry_column]
            if hasattr(edge_geom, 'coords'):
                coords = list(edge_geom.coords)
                x_coords = [coord[0] for coord in coords]
                y_coords = [coord[1] for coord in coords]
                
                linewidth = 1.0
                if edge_width_column and edge_width_column in edge:
                    linewidth = edge[edge_width_column] / edge[edge_width_column].max() * 3 + 0.5
                
                ax.plot(x_coords, y_coords, 'b-', linewidth=linewidth, alpha=0.7)
        
        # Plot nodes
        if node_size_column and node_size_column in nodes.columns:
            sizes = nodes[node_size_column] / nodes[node_size_column].max() * 100 + 10
        else:
            sizes = 20
        
        node_geoms = nodes[node_geometry_column]
        ax.scatter(
            [geom.x for geom in node_geoms],
            [geom.y for geom in node_geoms],
            s=sizes,
            c='red',
            alpha=0.8,
            **kwargs
        )
        
        ax.set_title("Network Topology")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True, alpha=0.3)
        
        return fig