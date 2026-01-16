"""
Geospatial Enhancement Module for PyPSA.

This module provides geospatial analysis capabilities including:
- Regional partitioning and spatial clustering
- Load and resource spatial matching
- Geographic data processing with GeoPandas
- Spatial dimension reduction algorithms
"""

from .base import GeospatialProcessor
from .spatial_clustering import SpatialClusteringEngine
from .load_resource_matching import SpatialLoadResourceMatcher
from .region_analysis import RegionAnalyzer
from .visualization import GeospatialVisualizer

__all__ = [
    "GeospatialProcessor",
    "SpatialClusteringEngine", 
    "SpatialLoadResourceMatcher",
    "RegionAnalyzer",
    "GeospatialVisualizer"
]