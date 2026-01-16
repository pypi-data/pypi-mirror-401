"""VistaDpy (PyVista) Integration Module - Advanced Wrapper.

This module provides a high-level, convenient interface for PyVista integration
within PyXESXXN, making 3D visualization and mesh analysis easily accessible.

Key Features:
- Simplified 3D visualization for energy networks
- One-line plotting functions
- Automatic mesh generation for network components
- Energy flow visualization with color mapping
- Spatial analysis tools
- Export capabilities for reports and presentations
"""

from __future__ import annotations

import numpy as np
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

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
    from pyxesxxn.network import Network


class VistaConfig:
    """Configuration for VistaDpy visualization."""
    
    def __init__(
        self,
        off_screen: bool = False,
        notebook: bool = False,
        theme: str = "default",
        window_size: tuple[int, int] = (1024, 768),
        background_color: str = "white",
        show_axes: bool = True,
        show_legend: bool = True,
        auto_close: bool = False
    ):
        self.off_screen = off_screen
        self.notebook = notebook
        self.theme = theme
        self.window_size = window_size
        self.background_color = background_color
        self.show_axes = show_axes
        self.show_legend = show_legend
        self.auto_close = auto_close


class VistaVisualizer:
    """High-level visualizer for energy networks using PyVista."""
    
    def __init__(self, config: Optional[VistaConfig] = None):
        """Initialize the visualizer.
        
        Args:
            config: VistaConfig instance with visualization settings
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError(
                "PyVista is not available. Install with: pip install pyvista"
            )
        
        self.config = config or VistaConfig()
        self._plotter = None
        self._network = None
        self._meshes = {}
        self._scalars = {}
        
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
        
        if self.config.show_axes:
            self._plotter.add_axes()
        
        return self._plotter
    
    def plot_network(
        self,
        network: Network,
        title: str = "Energy Network",
        show: bool = True,
        save_path: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Plotter:
        """Plot an energy network with one line.
        
        Args:
            network: PyXESXXN Network instance
            title: Plot title
            show: Whether to display the plot
            save_path: Optional path to save the plot
            **kwargs: Additional visualization options
            
        Returns:
            Plotter instance
        """
        if not self._plotter:
            self.create_plotter()
        
        self._plotter.add_text(title, position='upper_left', font_size=12)
        
        self._visualize_network_components(network, **kwargs)
        
        if self.config.show_legend:
            self._plotter.add_legend()
        
        if save_path:
            self._plotter.screenshot(str(save_path))
        
        if show:
            self._plotter.show()
        
        return self._plotter
    
    def plot_energy_flow(
        self,
        network: Network,
        flow_data: dict[str, np.ndarray],
        colormap: str = "jet",
        title: str = "Energy Flow",
        show: bool = True,
        save_path: Optional[Union[str, Path]] = None
    ) -> Plotter:
        """Plot energy flow through the network.
        
        Args:
            network: PyXESXXN Network instance
            flow_data: Dictionary mapping component names to flow values
            colormap: Colormap name
            title: Plot title
            show: Whether to display the plot
            save_path: Optional path to save the plot
            
        Returns:
            Plotter instance
        """
        if not self._plotter:
            self.create_plotter()
        
        self._visualize_network_components(network)
        
        if 'lines' in self._meshes:
            line_mesh = self._meshes['lines']
            flows = []
            for line_name, line in network.lines.items():
                flows.append(flow_data.get(line_name, 0.0))
            
            line_mesh["flow"] = np.array(flows)
            self._plotter.add_mesh(
                line_mesh,
                scalars="flow",
                cmap=colormap,
                scalar_bar_title="Energy Flow (MW)",
                line_width=3,
                show_scalar_bar=True
            )
        
        self._plotter.add_text(title, position='upper_left', font_size=12)
        
        if save_path:
            self._plotter.screenshot(str(save_path))
        
        if show:
            self._plotter.show()
        
        return self._plotter
    
    def plot_3d_network(
        self,
        network: Network,
        elevation_scale: float = 1.0,
        title: str = "3D Energy Network",
        show: bool = True,
        save_path: Optional[Union[str, Path]] = None
    ) -> Plotter:
        """Plot network in 3D with elevation.
        
        Args:
            network: PyXESXXN Network instance
            elevation_scale: Scale factor for elevation
            title: Plot title
            show: Whether to display the plot
            save_path: Optional path to save the plot
            
        Returns:
            Plotter instance
        """
        if not self._plotter:
            self.create_plotter()
        
        self._visualize_network_components_3d(network, elevation_scale)
        
        self._plotter.add_text(title, position='upper_left', font_size=12)
        
        if save_path:
            self._plotter.screenshot(str(save_path))
        
        if show:
            self._plotter.show()
        
        return self._plotter
    
    def _visualize_network_components(self, network: Network, **kwargs):
        """Visualize network components."""
        bus_color = kwargs.get('bus_color', 'blue')
        generator_color = kwargs.get('generator_color', 'green')
        load_color = kwargs.get('load_color', 'red')
        line_color = kwargs.get('line_color', 'gray')
        
        buses = []
        for bus in network.buses.values():
            if hasattr(bus, 'x') and hasattr(bus, 'y'):
                buses.append([bus.x, bus.y, 0])
        
        if buses:
            bus_points = np.array(buses)
            bus_mesh = PolyData(bus_points)
            self._plotter.add_mesh(
                bus_mesh,
                color=bus_color,
                point_size=20,
                render_points_as_spheres=True,
                label="Buses"
            )
            self._meshes['buses'] = bus_mesh
        
        generators = []
        for gen in network.generators.values():
            if hasattr(gen, 'x') and hasattr(gen, 'y'):
                generators.append([gen.x, gen.y, 0])
        
        if generators:
            gen_points = np.array(generators)
            gen_mesh = PolyData(gen_points)
            self._plotter.add_mesh(
                gen_mesh,
                color=generator_color,
                point_size=15,
                render_points_as_spheres=True,
                label="Generators"
            )
            self._meshes['generators'] = gen_mesh
        
        loads = []
        for load in network.loads.values():
            if hasattr(load, 'x') and hasattr(load, 'y'):
                loads.append([load.x, load.y, 0])
        
        if loads:
            load_points = np.array(loads)
            load_mesh = PolyData(load_points)
            self._plotter.add_mesh(
                load_mesh,
                color=load_color,
                point_size=15,
                render_points_as_spheres=True,
                label="Loads"
            )
            self._meshes['loads'] = load_mesh
        
        lines = []
        for line in network.lines.values():
            if hasattr(line, 'bus0') and hasattr(line, 'bus1'):
                bus0 = network.buses.get(line.bus0)
                bus1 = network.buses.get(line.bus1)
                if bus0 and bus1:
                    if hasattr(bus0, 'x') and hasattr(bus0, 'y') and \
                       hasattr(bus1, 'x') and hasattr(bus1, 'y'):
                        lines.append([[bus0.x, bus0.y, 0], [bus1.x, bus1.y, 0]])
        
        if lines:
            line_points = np.array(lines).reshape(-1, 3)
            line_mesh = PolyData(line_points)
            cells = np.arange(len(lines) * 2).reshape(-1, 2)
            line_mesh.lines = np.insert(cells, 0, 2, axis=1)
            self._plotter.add_mesh(
                line_mesh,
                color=line_color,
                line_width=2,
                label="Lines"
            )
            self._meshes['lines'] = line_mesh
    
    def _visualize_network_components_3d(self, network: Network, elevation_scale: float):
        """Visualize network components in 3D."""
        buses = []
        for bus in network.buses.values():
            if hasattr(bus, 'x') and hasattr(bus, 'y'):
                z = getattr(bus, 'z', 0) * elevation_scale
                buses.append([bus.x, bus.y, z])
        
        if buses:
            bus_points = np.array(buses)
            bus_mesh = PolyData(bus_points)
            self._plotter.add_mesh(
                bus_mesh,
                color='blue',
                point_size=25,
                render_points_as_spheres=True,
                label="Buses"
            )
        
        lines = []
        for line in network.lines.values():
            if hasattr(line, 'bus0') and hasattr(line, 'bus1'):
                bus0 = network.buses.get(line.bus0)
                bus1 = network.buses.get(line.bus1)
                if bus0 and bus1:
                    if hasattr(bus0, 'x') and hasattr(bus0, 'y') and \
                       hasattr(bus1, 'x') and hasattr(bus1, 'y'):
                        z0 = getattr(bus0, 'z', 0) * elevation_scale
                        z1 = getattr(bus1, 'z', 0) * elevation_scale
                        lines.append([[bus0.x, bus0.y, z0], [bus1.x, bus1.y, z1]])
        
        if lines:
            line_points = np.array(lines).reshape(-1, 3)
            line_mesh = PolyData(line_points)
            cells = np.arange(len(lines) * 2).reshape(-1, 2)
            line_mesh.lines = np.insert(cells, 0, 2, axis=1)
            self._plotter.add_mesh(
                line_mesh,
                color='gray',
                line_width=3,
                label="Lines"
            )
    
    def save_plot(self, filename: Union[str, Path], **kwargs):
        """Save the current plot to a file.
        
        Args:
            filename: Output filename
            **kwargs: Additional arguments for screenshot method
        """
        if self._plotter:
            self._plotter.screenshot(str(filename), **kwargs)
    
    def show(self):
        """Display the visualization."""
        if self._plotter:
            self._plotter.show()
    
    def close(self):
        """Close the plotter and release resources."""
        if self._plotter:
            self._plotter.close()
            if self.config.auto_close:
                self._plotter = None


class VistaMeshGenerator:
    """Generate meshes for energy system components."""
    
    @staticmethod
    def create_sphere(
        center: tuple[float, float, float],
        radius: float = 1.0,
        resolution: int = 20
    ) -> PolyData:
        """Create a sphere mesh.
        
        Args:
            center: (x, y, z) center coordinates
            radius: Sphere radius
            resolution: Mesh resolution
            
        Returns:
            PolyData sphere mesh
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
        
        sphere = examples.load_sphere()
        sphere.points[:, 0] = sphere.points[:, 0] * radius + center[0]
        sphere.points[:, 1] = sphere.points[:, 1] * radius + center[1]
        sphere.points[:, 2] = sphere.points[:, 2] * radius + center[2]
        return sphere
    
    @staticmethod
    def create_cylinder(
        start: tuple[float, float, float],
        end: tuple[float, float, float],
        radius: float = 0.1,
        resolution: int = 10
    ) -> PolyData:
        """Create a cylinder mesh.
        
        Args:
            start: Starting (x, y, z) coordinates
            end: Ending (x, y, z) coordinates
            radius: Cylinder radius
            resolution: Mesh resolution
            
        Returns:
            PolyData cylinder mesh
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
        
        from pyxesxxn.vistaDpy.pyvista import Cylinder
        
        direction = np.array(end) - np.array(start)
        length = np.linalg.norm(direction)
        direction = direction / length
        
        center = (np.array(start) + np.array(end)) / 2
        
        cylinder = Cylinder(
            center=center,
            direction=direction,
            radius=radius,
            height=length,
            resolution=resolution
        )
        
        return cylinder
    
    @staticmethod
    def create_box(
        center: tuple[float, float, float],
        size: tuple[float, float, float] = (1.0, 1.0, 1.0)
    ) -> PolyData:
        """Create a box mesh.
        
        Args:
            center: (x, y, z) center coordinates
            size: (x_size, y_size, z_size) dimensions
            
        Returns:
            PolyData box mesh
        """
        if not _PYVISTA_AVAILABLE:
            raise ImportError("PyVista is not available")
        
        from pyxesxxn.vistaDpy.pyvista import Cube
        
        cube = Cube(
            center=center,
            x_length=size[0],
            y_length=size[1],
            z_length=size[2]
        )
        return cube


def quick_plot(
    network: Network,
    title: str = "Energy Network",
    show: bool = True,
    save_path: Optional[Union[str, Path]] = None
) -> Plotter:
    """Quick one-line plot function for energy networks.
    
    Args:
        network: PyXESXXN Network instance
        title: Plot title
        show: Whether to display the plot
        save_path: Optional path to save the plot
        
    Returns:
        Plotter instance
    """
    visualizer = VistaVisualizer()
    return visualizer.plot_network(network, title=title, show=show, save_path=save_path)


def quick_flow_plot(
    network: Network,
    flow_data: dict[str, np.ndarray],
    colormap: str = "jet",
    title: str = "Energy Flow",
    show: bool = True,
    save_path: Optional[Union[str, Path]] = None
) -> Plotter:
    """Quick one-line plot function for energy flow visualization.
    
    Args:
        network: PyXESXXN Network instance
        flow_data: Dictionary mapping component names to flow values
        colormap: Colormap name
        title: Plot title
        show: Whether to display the plot
        save_path: Optional path to save the plot
        
    Returns:
        Plotter instance
    """
    visualizer = VistaVisualizer()
    return visualizer.plot_energy_flow(
        network, flow_data, colormap=colormap,
        title=title, show=show, save_path=save_path
    )


def check_vista_available() -> bool:
    """Check if VistaDpy (PyVista) is available.
    
    Returns:
        True if available, False otherwise
    """
    return _PYVISTA_AVAILABLE


def get_vista_version() -> Optional[str]:
    """Get the PyVista version.
    
    Returns:
        Version string or None if not available
    """
    return pyvista_version


def get_vtk_version() -> Optional[str]:
    """Get the VTK version.
    
    Returns:
        Version string or None if not available
    """
    if _PYVISTA_AVAILABLE and vtk_version_info:
        return str(vtk_version_info)
    return None


__all__ = [
    "VistaConfig",
    "VistaVisualizer",
    "VistaMeshGenerator",
    "quick_plot",
    "quick_flow_plot",
    "check_vista_available",
    "get_vista_version",
    "get_vtk_version",
    "_PYVISTA_AVAILABLE",
]
