"""
Base Geospatial Processor for PyPSA.

Provides the foundation for geospatial analysis capabilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from abc import ABC, abstractmethod
import warnings

try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon, MultiPolygon
    from shapely.ops import unary_union
    HAS_GEOPANDAS = True
except ImportError:
    gpd = None
    Point = None
    Polygon = None
    MultiPolygon = None
    HAS_GEOPANDAS = False
    warnings.warn("GeoPandas not installed. Geospatial features will be limited.", UserWarning)


class GeospatialProcessor(ABC):
    """Base class for geospatial processing in PyPSA networks."""
    
    def __init__(self, crs: str = "EPSG:4326", units: str = "degrees"):
        """Initialize geospatial processor.
        
        Parameters
        ----------
        crs : str
            Coordinate Reference System (default: WGS84)
        units : str
            Unit system ('degrees', 'meters', 'kilometers')
        """
        self.crs = crs
        self.units = units
        self._validate_geospatial_dependencies()
    
    def _validate_geospatial_dependencies(self) -> None:
        """Validate that required geospatial dependencies are available."""
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas is required for geospatial features. "
                            "Install with: pip install geopandas")
    
    def create_point_geometry(self, x: float, y: float, 
                             crs: Optional[str] = None) -> 'Point':
        """Create a Point geometry.
        
        Parameters
        ----------
        x, y : float
            Coordinates
        crs : str, optional
            Coordinate reference system
            
        Returns
        -------
        Point
            Shapely Point geometry
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for geometry creation")
        
        if crs is None:
            crs = self.crs
        
        return Point(x, y)
    
    def create_polygon_geometry(self, coordinates: List[Tuple[float, float]], 
                               crs: Optional[str] = None) -> 'Polygon':
        """Create a Polygon geometry.
        
        Parameters
        ----------
        coordinates : List[Tuple[float, float]]
            List of coordinate pairs defining polygon boundary
        crs : str, optional
            Coordinate reference system
            
        Returns
        -------
        Polygon
            Shapely Polygon geometry
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for geometry creation")
        
        if crs is None:
            crs = self.crs
        
        return Polygon(coordinates)
    
    def calculate_distance(self, point1: Tuple[float, float], 
                          point2: Tuple[float, float], 
                          unit: str = "km") -> float:
        """Calculate distance between two points.
        
        Parameters
        ----------
        point1, point2 : Tuple[float, float]
            Coordinate pairs (lon, lat)
        unit : str
            Distance unit ('km', 'm', 'degrees')
            
        Returns
        -------
        float
            Distance between points
        """
        lon1, lat1 = point1
        lon2, lat2 = point2
        
        if unit == "degrees":
            return np.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)
        elif unit == "km":
            # Haversine formula
            R = 6371.0  # Earth radius in km
            dlat = np.radians(lat2 - lat1)
            dlon = np.radians(lon2 - lon1)
            a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
            return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        elif unit == "m":
            return self.calculate_distance(point1, point2, "km") * 1000
        else:
            raise ValueError(f"Unsupported distance unit: {unit}")
    
    def convert_coordinates(self, x: float, y: float, 
                           from_crs: str, to_crs: str) -> Tuple[float, float]:
        """Convert coordinates between CRS.
        
        Parameters
        ----------
        x, y : float
            Source coordinates
        from_crs, to_crs : str
            Source and target coordinate reference systems
            
        Returns
        -------
        Tuple[float, float]
            Converted coordinates
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for coordinate conversion")
        
        point = gpd.GeoSeries([Point(x, y)], crs=from_crs)
        point_converted = point.to_crs(to_crs)
        
        return point_converted.geometry.iloc[0].x, point_converted.geometry.iloc[0].y
    
    def create_geodataframe(self, data: pd.DataFrame, 
                           geometry_column: str = "geometry",
                           crs: Optional[str] = None) -> 'gpd.GeoDataFrame':
        """Create a GeoDataFrame from regular DataFrame.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input data
        geometry_column : str
            Name of geometry column
        crs : str, optional
            Coordinate reference system
            
        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame with geometry column
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for GeoDataFrame creation")
        
        if crs is None:
            crs = self.crs
        
        return gpd.GeoDataFrame(data, geometry=geometry_column, crs=crs)
    
    def extract_coordinates_from_network(self, network) -> pd.DataFrame:
        """Extract coordinate information from PyPSA network.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network with buses
            
        Returns
        -------
        pd.DataFrame
            DataFrame with bus coordinates and metadata
        """
        if "buses" not in network.df or network.df["buses"].empty:
            return pd.DataFrame()
        
        buses = network.df["buses"].copy()
        
        # Check for existing coordinate columns
        coord_columns = []
        for col in ["x", "y", "lon", "lat", "longitude", "latitude"]:
            if col in buses.columns:
                coord_columns.append(col)
        
        if not coord_columns:
            # Generate synthetic coordinates for demonstration
            warnings.warn("No coordinate columns found, generating synthetic coordinates")
            n_buses = len(buses)
            buses["x"] = np.random.uniform(-10, 10, n_buses)
            buses["y"] = np.random.uniform(-10, 10, n_buses)
        
        # Standardize coordinate names
        if "lon" in coord_columns:
            buses["x"] = buses["lon"]
        elif "longitude" in coord_columns:
            buses["x"] = buses["longitude"]
        
        if "lat" in coord_columns:
            buses["y"] = buses["lat"]
        elif "latitude" in coord_columns:
            buses["y"] = buses["latitude"]
        
        # Create geometry column
        try:
            buses["geometry"] = buses.apply(
                lambda row: Point(row["x"], row["y"]), axis=1
            )
            buses_gdf = gpd.GeoDataFrame(buses, crs=self.crs)
        except:
            # Fallback if Point creation fails
            buses_gdf = buses.copy()
        
        return buses_gdf
    
    def calculate_area(self, geometry) -> float:
        """Calculate area of geometry.
        
        Parameters
        ----------
        geometry : shapely.Geometry
            Input geometry
            
        Returns
        -------
        float
            Area in appropriate units
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for area calculation")
        
        if isinstance(geometry, (Polygon, MultiPolygon)):
            return geometry.area
        else:
            return 0.0
    
    def calculate_perimeter(self, geometry) -> float:
        """Calculate perimeter of geometry.
        
        Parameters
        ----------
        geometry : shapely.Geometry
            Input geometry
            
        Returns
        -------
        float
            Perimeter in appropriate units
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for perimeter calculation")
        
        if isinstance(geometry, (Polygon, MultiPolygon)):
            return geometry.length
        else:
            return 0.0
    
    def buffer_geometry(self, geometry, distance: float, resolution: int = 16) -> 'Polygon':
        """Create buffer around geometry.
        
        Parameters
        ----------
        geometry : shapely.Geometry
            Input geometry
        distance : float
            Buffer distance
        resolution : int
            Number of points in buffer
            
        Returns
        -------
        Polygon
            Buffered geometry
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for geometry buffering")
        
        return geometry.buffer(distance, resolution=resolution)
    
    def find_nearest_neighbors(self, points_gdf: 'gpd.GeoDataFrame', 
                              reference_points: List[Tuple[float, float]],
                              k: int = 1) -> pd.DataFrame:
        """Find k nearest neighbors for reference points.
        
        Parameters
        ----------
        points_gdf : gpd.GeoDataFrame
            Points to search from
        reference_points : List[Tuple[float, float]]
            Reference points (x, y)
        k : int
            Number of nearest neighbors to find
            
        Returns
        -------
        pd.DataFrame
            Nearest neighbors information
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for nearest neighbor search")
        
        results = []
        
        for i, (ref_x, ref_y) in enumerate(reference_points):
            # Create reference point geometry
            ref_point = Point(ref_x, ref_y)
            
            # Calculate distances
            distances = points_gdf.geometry.apply(
                lambda geom: geom.distance(ref_point)
            )
            
            # Get k nearest
            nearest_indices = distances.nsmallest(k).index
            
            for j, idx in enumerate(nearest_indices):
                results.append({
                    "reference_point": i,
                    "reference_x": ref_x,
                    "reference_y": ref_y,
                    "nearest_index": idx,
                    "nearest_x": points_gdf.loc[idx, "x"] if "x" in points_gdf.columns else None,
                    "nearest_y": points_gdf.loc[idx, "y"] if "y" in points_gdf.columns else None,
                    "distance": distances.loc[idx],
                    "rank": j + 1
                })
        
        return pd.DataFrame(results)
    
    def spatial_join(self, left_gdf: 'gpd.GeoDataFrame', 
                    right_gdf: 'gpd.GeoDataFrame',
                    how: str = "inner",
                    predicate: str = "intersects") -> 'gpd.GeoDataFrame':
        """Perform spatial join between two GeoDataFrames.
        
        Parameters
        ----------
        left_gdf, right_gdf : gpd.GeoDataFrame
            GeoDataFrames to join
        how : str
            Join type ('inner', 'left', 'right', 'outer')
        predicate : str
            Spatial predicate ('intersects', 'contains', 'within', etc.)
            
        Returns
        -------
        gpd.GeoDataFrame
            Result of spatial join
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for spatial join")
        
        return gpd.sjoin(left_gdf, right_gdf, how=how, predicate=predicate)
    
    def create_voronoi_diagram(self, points: List[Tuple[float, float]]) -> 'gpd.GeoDataFrame':
        """Create Voronoi diagram for given points.
        
        Parameters
        ----------
        points : List[Tuple[float, float]]
            List of (x, y) coordinate pairs
            
        Returns
        -------
        gpd.GeoDataFrame
            Voronoi polygons
        """
        if not HAS_GEOPANDAS:
            raise ImportError("GeoPandas required for Voronoi diagram creation")
        
        # Create point GeoDataFrame
        points_gdf = gpd.GeoDataFrame(
            {"id": range(len(points))},
            geometry=[Point(x, y) for x, y in points],
            crs=self.crs
        )
        
        # Create bounding box
        bounds = points_gdf.total_bounds
        bbox = Polygon([
            (bounds[0] - 0.1, bounds[1] - 0.1),
            (bounds[2] + 0.1, bounds[1] - 0.1),
            (bounds[2] + 0.1, bounds[3] + 0.1),
            (bounds[0] - 0.1, bounds[3] + 0.1)
        ])
        
        # Create Voronoi polygons
        from shapely.ops import voronoi_diagram
        voronoi = voronoi_diagram(points_gdf.unary_union, bbox=bbox)
        
        voronoi_gdf = gpd.GeoDataFrame(
            {"id": range(len(voronoi.geoms))},
            geometry=voronoi.geoms,
            crs=self.crs
        )
        
        return voronoi_gdf
    
    @abstractmethod
    def process_network_geospatial(self, network, **kwargs) -> Any:
        """Process network with geospatial analysis.
        
        This method should be implemented by subclasses to provide
        specific geospatial processing functionality.
        
        Parameters
        ----------
        network : pypsa.Network
            PyPSA network to process
        **kwargs
            Additional processing parameters
            
        Returns
        -------
        Any
            Processing results
        """
        pass
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of processor capabilities.
        
        Returns
        -------
        Dict[str, Any]
            Summary of available methods and capabilities
        """
        return {
            "processor_type": self.__class__.__name__,
            "coordinate_system": self.crs,
            "units": self.units,
            "capabilities": [
                "coordinate_conversion",
                "distance_calculation", 
                "geometry_creation",
                "spatial_analysis",
                "network_coordinate_extraction"
            ],
            "required_dependencies": ["geopandas", "shapely", "numpy", "pandas"],
            "supported_units": ["degrees", "km", "m"],
            "spatial_operations": [
                "buffer",
                "intersection", 
                "union",
                "difference",
                "spatial_join",
                "nearest_neighbor"
            ]
        }