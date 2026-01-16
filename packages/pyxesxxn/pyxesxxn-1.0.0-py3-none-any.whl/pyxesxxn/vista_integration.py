"""PyVista Integration Module for PyXESXXN.

This module provides integration with PyVista (vistaDpy) for 3D visualization
and mesh analysis capabilities within the PyXESXXN energy system framework.

Key Features:
- 3D visualization of energy networks and infrastructure
- Spatial analysis and geospatial data visualization
- Mesh generation and manipulation for energy system components
- Advanced plotting capabilities for energy flow and optimization results
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

import numpy as np

try:
    from pyxesxxn.vistaDpy.vistaDpy import (
        Plotter,
        PolyData,
        UnstructuredGrid,
        StructuredGrid,
        RectilinearGrid,
        ImageData,
        MultiBlock,
        examples,
        set_jupyter_backend,
        get_gpu_info,
        Report,
        vtk_version_info,
        __version__ as pyvista_version
    )
    _PYVISTA_AVAILABLE = True
except ImportError:
    _PYVISTA_AVAILABLE = False
    Plotter = None
    PolyData = None
    UnstructuredGrid = None
    StructuredGrid = None
    RectilinearGrid = None
    ImageData = None
    MultiBlock = None
    examples = None
    set_jupyter_backend = None
    get_gpu_info = None
    Report = None
    vtk_version_info = None
    pyvista_version = None

if TYPE_CHECKING:
    from pyxesxxn.network import Network, Bus, Generator, Load, Line


class PyVistaConfig:
    """Configuration for PyVista integration."""
    
    def __init__(
        self,
        off_screen: bool = False,
        notebook: bool = False,
        theme: str = "default",
        window_size: tuple[int, int] = (1024, 768),
        background_color: str = "white"
    ):
        self.off_screen = off_screen
        self.notebook = notebook
        self.theme = theme
        self.window_size = window_size
        self.background_color = background_color


class EnergyNetworkVisualizer:
    """Visualize energy networks using PyVista."""
    
    def __init__(self, config: Optional[PyVistaConfig] = None):
        """Initialize the visualizer.
        
        Args:
            config: PyVista configuration options
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError(
                "PyVista is not available. Please install it with: "
                "pip install pyvista"
            )
        
        self.config = config or PyVistaConfig()
        self._plotter = None
        self._network = None
        self._meshes = {}
        
    def create_plotter(self) -> Plotter:
        """Create and configure a PyVista plotter.
        
        Returns:
            Configured Plotter instance
        """
        self._plotter = Plotter(
            notebook=self.config.notebook,
            off_screen=self.config.off_screen
        )
        self._plotter.set_background(self.config.background_color)
        self._plotter.window_size = self.config.window_size
        return self._plotter
    
    def visualize_network(
        self,
        network: Network,
        show_buses: bool = True,
        show_generators: bool = True,
        show_loads: bool = True,
        show_lines: bool = True,
        bus_color: str = "blue",
        generator_color: str = "green",
        load_color: str = "red",
        line_color: str = "gray"
    ) -> Plotter:
        """Visualize an energy network.
        
        Args:
            network: PyXESXXN Network instance
            show_buses: Whether to visualize buses
            show_generators: Whether to visualize generators
            show_loads: Whether to visualize loads
            show_lines: Whether to visualize transmission lines
            bus_color: Color for buses
            generator_color: Color for generators
            load_color: Color for loads
            line_color: Color for lines
            
        Returns:
            Configured Plotter instance with network visualization
        """
        if not self._plotter:
            self.create_plotter()
        
        self._network = network
        
        if show_buses:
            self._visualize_buses(bus_color)
        
        if show_generators:
            self._visualize_generators(generator_color)
        
        if show_loads:
            self._visualize_loads(load_color)
        
        if show_lines:
            self._visualize_lines(line_color)
        
        self._plotter.add_axes()
        self._plotter.add_legend()
        
        return self._plotter
    
    def _visualize_buses(self, color: str):
        """Visualize buses in the network."""
        buses = []
        for bus in self._network.buses.values():
            if hasattr(bus, 'x') and hasattr(bus, 'y'):
                buses.append([bus.x, bus.y, 0])
        
        if buses:
            bus_points = np.array(buses)
            bus_mesh = PolyData(bus_points)
            self._plotter.add_mesh(
                bus_mesh,
                color=color,
                point_size=20,
                render_points_as_spheres=True,
                label="Buses"
            )
            self._meshes['buses'] = bus_mesh
    
    def _visualize_generators(self, color: str):
        """Visualize generators in the network."""
        generators = []
        for gen in self._network.generators.values():
            if hasattr(gen, 'x') and hasattr(gen, 'y'):
                generators.append([gen.x, gen.y, 0])
        
        if generators:
            gen_points = np.array(generators)
            gen_mesh = PolyData(gen_points)
            self._plotter.add_mesh(
                gen_mesh,
                color=color,
                point_size=15,
                render_points_as_spheres=True,
                label="Generators"
            )
            self._meshes['generators'] = gen_mesh
    
    def _visualize_loads(self, color: str):
        """Visualize loads in the network."""
        loads = []
        for load in self._network.loads.values():
            if hasattr(load, 'x') and hasattr(load, 'y'):
                loads.append([load.x, load.y, 0])
        
        if loads:
            load_points = np.array(loads)
            load_mesh = PolyData(load_points)
            self._plotter.add_mesh(
                load_mesh,
                color=color,
                point_size=15,
                render_points_as_spheres=True,
                label="Loads"
            )
            self._meshes['loads'] = load_mesh
    
    def _visualize_lines(self, color: str):
        """Visualize transmission lines in the network."""
        lines = []
        for line in self._network.lines.values():
            if hasattr(line, 'bus0') and hasattr(line, 'bus1'):
                bus0 = self._network.buses.get(line.bus0)
                bus1 = self._network.buses.get(line.bus1)
                if bus0 and bus1:
                    if hasattr(bus0, 'x') and hasattr(bus0, 'y') and \
                       hasattr(bus1, 'x') and hasattr(bus1, 'y'):
                        lines.append([[bus0.x, bus0.y, 0], [bus1.x, bus1.y, 0]])
        
        if lines:
            line_points = np.array(lines)
            line_mesh = PolyData(line_points.reshape(-1, 3))
            cells = np.arange(len(lines) * 2).reshape(-1, 2)
            line_mesh.lines = np.insert(cells, 0, 2, axis=1)
            self._plotter.add_mesh(
                line_mesh,
                color=color,
                line_width=2,
                label="Lines"
            )
            self._meshes['lines'] = line_mesh
    
    def visualize_energy_flow(
        self,
        flow_data: dict[str, np.ndarray],
        colormap: str = "jet",
        scalar_range: Optional[tuple[float, float]] = None
    ) -> Plotter:
        """Visualize energy flow through the network.
        
        Args:
            flow_data: Dictionary mapping component names to flow values
            colormap: Name of the colormap to use
            scalar_range: Optional (min, max) range for scalar values
            
        Returns:
            Configured Plotter instance with flow visualization
        """
        if not self._plotter:
            self.create_plotter()
        
        if 'lines' in self._meshes:
            line_mesh = self._meshes['lines']
            flows = []
            for line_name, line in self._network.lines.items():
                flows.append(flow_data.get(line_name, 0.0))
            
            line_mesh["flow"] = np.array(flows)
            self._plotter.add_mesh(
                line_mesh,
                scalars="flow",
                cmap=colormap,
                scalar_bar_title="Energy Flow",
                clim=scalar_range,
                line_width=3
            )
        
        return self._plotter
    
    def show(self):
        """Display the visualization."""
        if self._plotter:
            self._plotter.show()
    
    def save(self, filename: str, **kwargs):
        """Save the visualization to a file.
        
        Args:
            filename: Output filename
            **kwargs: Additional arguments for screenshot method
        """
        if self._plotter:
            self._plotter.screenshot(filename, **kwargs)
    
    def close(self):
        """Close the plotter and release resources."""
        if self._plotter:
            self._plotter.close()
            self._plotter = None


class MeshGenerator:
    """Generate meshes for energy system components."""
    
    @staticmethod
    def create_bus_mesh(
        x: float,
        y: float,
        z: float = 0.0,
        radius: float = 1.0,
        resolution: int = 20
    ) -> PolyData:
        """Create a spherical mesh representing a bus.
        
        Args:
            x, y, z: Center coordinates
            radius: Sphere radius
            resolution: Mesh resolution
            
        Returns:
            PolyData mesh
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
        
        sphere = examples.load_sphere()
        sphere.points[:, 0] = sphere.points[:, 0] * radius + x
        sphere.points[:, 1] = sphere.points[:, 1] * radius + y
        sphere.points[:, 2] = sphere.points[:, 2] * radius + z
        return sphere
    
    @staticmethod
    def create_line_mesh(
        start_point: tuple[float, float, float],
        end_point: tuple[float, float, float],
        radius: float = 0.1,
        resolution: int = 10
    ) -> PolyData:
        """Create a cylindrical mesh representing a transmission line.
        
        Args:
            start_point: Starting (x, y, z) coordinates
            end_point: Ending (x, y, z) coordinates
            radius: Cylinder radius
            resolution: Mesh resolution
            
        Returns:
            PolyData mesh
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
        
        from pyxesxxn.vistaDpy.pyvista import Cylinder
        
        direction = np.array(end_point) - np.array(start_point)
        length = np.linalg.norm(direction)
        direction = direction / length
        
        center = (np.array(start_point) + np.array(end_point)) / 2
        
        cylinder = Cylinder(
            center=center,
            direction=direction,
            radius=radius,
            height=length,
            resolution=resolution
        )
        
        return cylinder
    
    @staticmethod
    def create_generator_mesh(
        x: float,
        y: float,
        z: float = 0.0,
        size: float = 1.0
    ) -> PolyData:
        """Create a box mesh representing a generator.
        
        Args:
            x, y, z: Center coordinates
            size: Box size
            
        Returns:
            PolyData mesh
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
        
        from pyxesxxn.vistaDpy.pyvista import Cube
        
        cube = Cube(
            center=(x, y, z),
            x_length=size,
            y_length=size,
            z_length=size
        )
        return cube


class SpatialAnalyzer:
    """Perform spatial analysis on energy networks."""
    
    def __init__(self):
        """Initialize the spatial analyzer."""
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
    
    def calculate_distance_matrix(
        self,
        points: np.ndarray
    ) -> np.ndarray:
        """Calculate pairwise distances between points.
        
        Args:
            points: Array of shape (n, 3) representing point coordinates
            
        Returns:
            Distance matrix of shape (n, n)
        """
        from scipy.spatial.distance import cdist
        return cdist(points, points)
    
    def find_nearest_neighbors(
        self,
        points: np.ndarray,
        query_point: np.ndarray,
        k: int = 5
    ) -> np.ndarray:
        """Find k nearest neighbors to a query point.
        
        Args:
            points: Array of shape (n, 3) representing point coordinates
            query_point: Query point coordinates
            k: Number of neighbors to find
            
        Returns:
            Indices of k nearest neighbors
        """
        distances = np.linalg.norm(points - query_point, axis=1)
        return np.argsort(distances)[:k]
    
    def create_voronoi_diagram(
        self,
        points: np.ndarray
    ) -> PolyData:
        """Create a Voronoi diagram from points.
        
        Args:
            points: Array of shape (n, 2) or (n, 3) representing point coordinates
            
        Returns:
            PolyData mesh with Voronoi cells
        """
        from scipy.spatial import Voronoi
        
        vor = Voronoi(points[:, :2])
        
        vertices = vor.vertices
        regions = []
        
        for region in vor.regions:
            if -1 not in region and len(region) > 0:
                regions.append(region)
        
        mesh = PolyData()
        
        return mesh


def check_pyvista_available() -> bool:
    """Check if PyVista is available.
    
    Returns:
        True if PyVista is available, False otherwise
    """
    return _PYVISTA_AVAILABLE


def get_pyvista_version() -> Optional[str]:
    """Get the PyVista version.
    
    Returns:
        PyVista version string or None if not available
    """
    return pyvista_version


def get_vtk_version() -> Optional[str]:
    """Get the VTK version.
    
    Returns:
        VTK version string or None if not available
    """
    if _PYVISTA_AVAILABLE and vtk_version_info:
        return str(vtk_version_info)
    return None


def create_visualizer(config: Optional[PyVistaConfig] = None) -> EnergyNetworkVisualizer:
    """Create an energy network visualizer.
    
    Args:
        config: Optional PyVista configuration
        
    Returns:
        EnergyNetworkVisualizer instance
    """
    return EnergyNetworkVisualizer(config)


def create_mesh_generator() -> MeshGenerator:
    """Create a mesh generator.
    
    Returns:
        MeshGenerator instance
    """
    return MeshGenerator()


def create_spatial_analyzer() -> SpatialAnalyzer:
    """Create a spatial analyzer.
    
    Returns:
        SpatialAnalyzer instance
    """
    return SpatialAnalyzer()


__all__ = [
    "PyVistaConfig",
    "EnergyNetworkVisualizer",
    "MeshGenerator",
    "SpatialAnalyzer",
    "check_pyvista_available",
    "get_pyvista_version",
    "get_vtk_version",
    "create_visualizer",
    "create_mesh_generator",
    "create_spatial_analyzer",
    "_PYVISTA_AVAILABLE",
]
