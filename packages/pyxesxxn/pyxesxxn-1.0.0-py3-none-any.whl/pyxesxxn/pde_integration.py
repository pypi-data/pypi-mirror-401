"""PDE Integration Module for PyXESXXN.

This module provides a convenient interface to the MorePDEpy-based PDE solver
for solving partial differential equations in energy system applications.

The integration allows PyXESXXN users to:
- Solve diffusion, convection, and source term PDEs
- Model transient and steady-state phenomena
- Handle complex boundary conditions
- Visualize PDE solutions

Example usage:
    >>> import pyxesxxn as px
    >>> from pyxesxxn.pde_integration import solve_diffusion_1d
    >>> result = solve_diffusion_1d(diffusion_coeff=1.0, time_steps=100)
"""

__all__ = [
    "PDESolver",
    "solve_diffusion_1d",
    "solve_diffusion_2d",
    "solve_convection_diffusion",
    "solve_heat_equation",
    "create_mesh_1d",
    "create_mesh_2d",
    "create_mesh_3d",
    "PDEConfig",
    "PDEResult",
    "PDEMesh",
    "PDEBoundaryCondition",
    "PDESolverType",
    "check_pde_dependencies",
    "get_available_solvers",
]

import logging
from typing import Optional, Union, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

_logger = logging.getLogger(__name__)

# Try to import MorePDEpy modules
try:
    import sys
    import os
    morepdepy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'morepdepy', 'morepdepy')
    sys.path.insert(0, morepdepy_path)
    
    from meshes import (
        Grid1D,
        Grid2D,
        Grid3D,
    )
    from variables import (
        CellVariable,
        FaceVariable,
    )
    from terms import (
        TransientTerm,
        DiffusionTerm,
        ConvectionTerm,
        ImplicitSourceTerm,
    )
    from boundaryConditions import (
        FixedValue,
        FixedFlux,
    )
    from solvers import (
        LinearLUSolver,
        LinearGMRESSolver,
        LinearCGSolver,
        LinearBicgstabSolver,
    )
    from viewers.matplotlibViewer import (
        Matplotlib1DViewer,
        Matplotlib2DViewer,
    )
    _morepdepy_available = True
except ImportError as e:
    _morepdepy_available = False
    _logger.warning(f"MorePDEpy not available: {e}")
    _logger.warning("PDE functionality will be limited")


class PDESolverType(Enum):
    """Available PDE solver types."""
    LU = "lu"
    GMRES = "gmres"
    CG = "cg"
    BICGSTAB = "bicgstab"


@dataclass
class PDEConfig:
    """Configuration for PDE solver."""
    solver_type: PDESolverType = PDESolverType.LU
    tolerance: float = 1e-10
    max_iterations: int = 1000
    verbose: bool = False
    parallel: bool = False
    cache_results: bool = True


@dataclass
class PDEMesh:
    """Mesh configuration for PDE domain."""
    nx: int = 50
    ny: int = 50
    nz: int = 50
    dx: float = 1.0
    dy: float = 1.0
    dz: float = 1.0
    mesh_type: str = "grid"
    periodic: bool = False


@dataclass
class PDEBoundaryCondition:
    """Boundary condition for PDE."""
    value: float = 0.0
    flux: float = 0.0
    type: str = "fixed_value"


@dataclass
class PDEResult:
    """Result from PDE solver."""
    solution: np.ndarray
    time: float
    iterations: int
    residual: float
    converged: bool
    mesh_info: Dict[str, Any] = field(default_factory=dict)
    solver_info: Dict[str, Any] = field(default_factory=dict)


class PDESolver:
    """High-level PDE solver interface for PyXESXXN.
    
    This class provides a simplified interface to the MorePDEpy PDE solver,
    making it easy to solve common PDE problems in energy system applications.
    """
    
    def __init__(self, config: Optional[PDEConfig] = None):
        """Initialize PDE solver.
        
        Args:
            config: Solver configuration. If None, uses default config.
        """
        self.config = config or PDEConfig()
        self._mesh = None
        self._variable = None
        self._equation = None
        self._solver = None
        self._boundary_conditions = {}
        
        if not _morepdepy_available:
            _logger.warning("MorePDEpy not available. PDE solver will be limited.")
    
    def create_mesh_1d(
        self,
        nx: int = 100,
        dx: float = 1.0,
        periodic: bool = False
    ) -> Any:
        """Create a 1D mesh.
        
        Args:
            nx: Number of grid points
            dx: Grid spacing
            periodic: Whether to use periodic boundary conditions
            
        Returns:
            Mesh object
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for mesh creation")
        
        if periodic:
            self._mesh = Grid1D(nx=nx, dx=dx)
        else:
            self._mesh = Grid1D(nx=nx, dx=dx)
        
        return self._mesh
    
    def create_mesh_2d(
        self,
        nx: int = 50,
        ny: int = 50,
        dx: float = 1.0,
        dy: float = 1.0,
        periodic: bool = False
    ) -> Any:
        """Create a 2D mesh.
        
        Args:
            nx: Number of grid points in x direction
            ny: Number of grid points in y direction
            dx: Grid spacing in x direction
            dy: Grid spacing in y direction
            periodic: Whether to use periodic boundary conditions
            
        Returns:
            Mesh object
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for mesh creation")
        
        if periodic:
            self._mesh = Grid2D(nx=nx, ny=ny, dx=dx, dy=dy)
        else:
            self._mesh = Grid2D(nx=nx, ny=ny, dx=dx, dy=dy)
        
        return self._mesh
    
    def create_mesh_3d(
        self,
        nx: int = 30,
        ny: int = 30,
        nz: int = 30,
        dx: float = 1.0,
        dy: float = 1.0,
        dz: float = 1.0,
        periodic: bool = False
    ) -> Any:
        """Create a 3D mesh.
        
        Args:
            nx: Number of grid points in x direction
            ny: Number of grid points in y direction
            nz: Number of grid points in z direction
            dx: Grid spacing in x direction
            dy: Grid spacing in y direction
            dz: Grid spacing in z direction
            periodic: Whether to use periodic boundary conditions
            
        Returns:
            Mesh object
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for mesh creation")
        
        if periodic:
            self._mesh = Grid3D(nx=nx, ny=ny, nz=nz, dx=dx, dy=dy, dz=dz)
        else:
            self._mesh = Grid3D(nx=nx, ny=ny, nz=nz, dx=dx, dy=dy, dz=dz)
        
        return self._mesh
    
    def create_variable(
        self,
        name: str = "phi",
        initial_value: float = 0.0,
        has_old: bool = True
    ) -> Any:
        """Create a variable on the mesh.
        
        Args:
            name: Variable name
            initial_value: Initial value
            has_old: Whether to store old values (for transient problems)
            
        Returns:
            Variable object
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for variable creation")
        
        if self._mesh is None:
            raise ValueError("Mesh must be created before creating a variable")
        
        self._variable = CellVariable(
            name=name,
            mesh=self._mesh,
            value=initial_value,
            hasOld=has_old
        )
        
        return self._variable
    
    def set_boundary_condition(
        self,
        boundary: str,
        value: float,
        condition_type: str = "fixed_value"
    ):
        """Set boundary condition.
        
        Args:
            boundary: Boundary identifier (e.g., 'left', 'right', 'top', 'bottom')
            value: Boundary value or flux
            condition_type: Type of condition ('fixed_value' or 'fixed_flux')
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for boundary conditions")
        
        if self._variable is None:
            raise ValueError("Variable must be created before setting boundary conditions")
        
        # Map boundary names to mesh face attributes
        boundary_map = {
            'left': 'facesLeft',
            'right': 'facesRight',
            'top': 'facesTop',
            'bottom': 'facesBottom',
            'front': 'facesFront',
            'back': 'facesBack'
        }
        face_attr = boundary_map.get(boundary.lower(), None)
        if face_attr is None:
            raise ValueError(f"Unknown boundary: {boundary}")
        
        # Get the face mask
        face_mask = getattr(self._mesh, face_attr, None)
        if face_mask is None:
            raise ValueError(f"Could not get faces for boundary: {boundary}")
        
        # For fixed_value, constrain the variable value
        # For fixed_flux, we need to handle differently (not implemented yet)
        if condition_type == "fixed_value":
            self._variable.constrain(value, where=face_mask)
        elif condition_type == "fixed_flux":
            raise NotImplementedError("Fixed flux boundary conditions are not yet implemented")
        else:
            raise ValueError(f"Unknown condition type: {condition_type}")
        
        self._boundary_conditions[boundary] = (condition_type, value, face_mask)
    
    def solve_diffusion(
        self,
        diffusion_coeff: float = 1.0,
        dt: float = 0.1,
        steps: int = 100,
        steady_state: bool = False
    ) -> PDEResult:
        """Solve diffusion equation.
        
        Args:
            diffusion_coeff: Diffusion coefficient
            dt: Time step (for transient problems)
            steps: Number of time steps
            steady_state: Whether to solve steady-state problem
            
        Returns:
            PDEResult object with solution and metadata
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for PDE solving")
        
        if self._variable is None:
            raise ValueError("Variable must be created before solving")
        
        if steady_state:
            eq = DiffusionTerm(coeff=diffusion_coeff) == 0
            eq.solve(var=self._variable, solver=self._get_solver())
            time = 0.0
            iterations = 1
        else:
            eq = TransientTerm() == DiffusionTerm(coeff=diffusion_coeff)
            for i in range(steps):
                eq.solve(var=self._variable, dt=dt, solver=self._get_solver())
            time = dt * steps
            iterations = steps
        
        return PDEResult(
            solution=self._variable.value.copy(),
            time=time,
            iterations=iterations,
            residual=0.0,
            converged=True,
            mesh_info={"nx": self._mesh.nx, "ny": getattr(self._mesh, 'ny', 1)},
            solver_info={"type": self.config.solver_type.value}
        )
    
    def solve_convection_diffusion(
        self,
        diffusion_coeff: float = 1.0,
        convection_velocity: Union[float, Tuple[float, ...]] = 1.0,
        dt: float = 0.1,
        steps: int = 100
    ) -> PDEResult:
        """Solve convection-diffusion equation.
        
        Args:
            diffusion_coeff: Diffusion coefficient
            convection_velocity: Convection velocity (scalar or vector)
            dt: Time step
            steps: Number of time steps
            
        Returns:
            PDEResult object with solution and metadata
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for PDE solving")
        
        if self._variable is None:
            raise ValueError("Variable must be created before solving")
        
        # For 1D meshes, convert scalar velocity to tuple
        if self._mesh.dim == 1 and isinstance(convection_velocity, (int, float)):
            convection_velocity = (convection_velocity,)
        
        eq = (TransientTerm() == 
              DiffusionTerm(coeff=diffusion_coeff) + 
              ConvectionTerm(coeff=convection_velocity))
        
        for i in range(steps):
            eq.solve(var=self._variable, dt=dt, solver=self._get_solver())
        
        return PDEResult(
            solution=self._variable.value.copy(),
            time=dt * steps,
            iterations=steps,
            residual=0.0,
            converged=True,
            mesh_info={"nx": self._mesh.nx, "ny": getattr(self._mesh, 'ny', 1)},
            solver_info={"type": self.config.solver_type.value}
        )
    
    def solve_heat_equation(
        self,
        thermal_diffusivity: float = 1.0,
        dt: float = 0.1,
        steps: int = 100
    ) -> PDEResult:
        """Solve heat equation (diffusion equation for temperature).
        
        Args:
            thermal_diffusivity: Thermal diffusivity
            dt: Time step
            steps: Number of time steps
            
        Returns:
            PDEResult object with solution and metadata
        """
        return self.solve_diffusion(
            diffusion_coeff=thermal_diffusivity,
            dt=dt,
            steps=steps
        )
    
    def _get_solver(self) -> Any:
        """Get configured solver instance."""
        if not _morepdepy_available:
            return None
        
        if self._solver is None:
            solver_map = {
                PDESolverType.LU: LinearLUSolver,
                PDESolverType.GMRES: LinearGMRESSolver,
                PDESolverType.CG: LinearCGSolver,
                PDESolverType.BICGSTAB: LinearBicgstabSolver,
            }
            solver_class = solver_map.get(self.config.solver_type, LinearLUSolver)
            self._solver = solver_class(
                tolerance=self.config.tolerance,
                iterations=self.config.max_iterations
            )
        
        return self._solver
    
    def visualize(self, title: str = "PDE Solution"):
        """Visualize the current solution.
        
        Args:
            title: Plot title
        """
        if not _morepdepy_available:
            raise ImportError("MorePDEpy is required for visualization")
        
        if self._variable is None:
            raise ValueError("Variable must be created and solved before visualization")
        
        if self._mesh.dim == 1:
            viewer = Matplotlib1DViewer(vars=self._variable, title=title)
        elif self._mesh.dim == 2:
            viewer = Matplotlib2DViewer(vars=self._variable, title=title)
        else:
            raise ValueError("3D visualization not yet supported")
        
        viewer.plot()
        return viewer


def check_pde_dependencies() -> Dict[str, bool]:
    """Check if PDE solver dependencies are available.
    
    Returns:
        Dictionary with dependency availability status
    """
    return {
        "morepdepy": _morepdepy_available,
        "scipy": True,
        "numpy": True,
    }


def get_available_solvers() -> List[str]:
    """Get list of available PDE solvers.
    
    Returns:
        List of solver names
    """
    if not _morepdepy_available:
        return []
    
    return [solver_type.value for solver_type in PDESolverType]


def solve_diffusion_1d(
    diffusion_coeff: float = 1.0,
    nx: int = 100,
    dx: float = 1.0,
    dt: float = 0.1,
    steps: int = 100,
    boundary_left: float = 0.0,
    boundary_right: float = 1.0,
    steady_state: bool = False
) -> PDEResult:
    """Solve 1D diffusion equation.
    
    Convenience function for solving the 1D diffusion equation:
    ∂φ/∂t = D ∂²φ/∂x²
    
    Args:
        diffusion_coeff: Diffusion coefficient (D)
        nx: Number of grid points
        dx: Grid spacing
        dt: Time step
        steps: Number of time steps
        boundary_left: Left boundary value
        boundary_right: Right boundary value
        steady_state: Whether to solve steady-state problem
        
    Returns:
        PDEResult object with solution and metadata
    """
    solver = PDESolver()
    solver.create_mesh_1d(nx=nx, dx=dx)
    solver.create_variable(name="phi", initial_value=0.0)
    solver.set_boundary_condition("left", boundary_left, "fixed_value")
    solver.set_boundary_condition("right", boundary_right, "fixed_value")
    
    return solver.solve_diffusion(
        diffusion_coeff=diffusion_coeff,
        dt=dt,
        steps=steps,
        steady_state=steady_state
    )


def solve_diffusion_2d(
    diffusion_coeff: float = 1.0,
    nx: int = 50,
    ny: int = 50,
    dx: float = 1.0,
    dy: float = 1.0,
    dt: float = 0.1,
    steps: int = 100,
    boundary_value: float = 0.0,
    steady_state: bool = False
) -> PDEResult:
    """Solve 2D diffusion equation.
    
    Convenience function for solving the 2D diffusion equation:
    ∂φ/∂t = D (∂²φ/∂x² + ∂²φ/∂y²)
    
    Args:
        diffusion_coeff: Diffusion coefficient (D)
        nx: Number of grid points in x direction
        ny: Number of grid points in y direction
        dx: Grid spacing in x direction
        dy: Grid spacing in y direction
        dt: Time step
        steps: Number of time steps
        boundary_value: Boundary value (all boundaries)
        steady_state: Whether to solve steady-state problem
        
    Returns:
        PDEResult object with solution and metadata
    """
    solver = PDESolver()
    solver.create_mesh_2d(nx=nx, ny=ny, dx=dx, dy=dy)
    solver.create_variable(name="phi", initial_value=0.0)
    solver.set_boundary_condition("left", boundary_value, "fixed_value")
    solver.set_boundary_condition("right", boundary_value, "fixed_value")
    solver.set_boundary_condition("bottom", boundary_value, "fixed_value")
    solver.set_boundary_condition("top", boundary_value, "fixed_value")
    
    return solver.solve_diffusion(
        diffusion_coeff=diffusion_coeff,
        dt=dt,
        steps=steps,
        steady_state=steady_state
    )


def solve_convection_diffusion(
    diffusion_coeff: float = 1.0,
    convection_velocity: Union[float, Tuple[float, ...]] = 1.0,
    nx: int = 100,
    dx: float = 1.0,
    dt: float = 0.1,
    steps: int = 100,
    boundary_left: float = 0.0,
    boundary_right: float = 1.0
) -> PDEResult:
    """Solve 1D convection-diffusion equation.
    
    Convenience function for solving the 1D convection-diffusion equation:
    ∂φ/∂t = D ∂²φ/∂x² - v ∂φ/∂x
    
    Args:
        diffusion_coeff: Diffusion coefficient (D)
        convection_velocity: Convection velocity (v)
        nx: Number of grid points
        dx: Grid spacing
        dt: Time step
        steps: Number of time steps
        boundary_left: Left boundary value
        boundary_right: Right boundary value
        
    Returns:
        PDEResult object with solution and metadata
    """
    solver = PDESolver()
    solver.create_mesh_1d(nx=nx, dx=dx)
    solver.create_variable(name="phi", initial_value=0.0)
    solver.set_boundary_condition("left", boundary_left, "fixed_value")
    solver.set_boundary_condition("right", boundary_right, "fixed_value")
    
    # For 1D, convection velocity must be a tuple
    if isinstance(convection_velocity, (int, float)):
        convection_velocity = (convection_velocity,)
    
    return solver.solve_convection_diffusion(
        diffusion_coeff=diffusion_coeff,
        convection_velocity=convection_velocity,
        dt=dt,
        steps=steps
    )


def solve_heat_equation(
    thermal_diffusivity: float = 1.0,
    nx: int = 100,
    dx: float = 1.0,
    dt: float = 0.1,
    steps: int = 100,
    boundary_left: float = 0.0,
    boundary_right: float = 100.0,
    steady_state: bool = False
) -> PDEResult:
    """Solve 1D heat equation.
    
    Convenience function for solving the 1D heat equation:
    ∂T/∂t = α ∂²T/∂x²
    
    Args:
        thermal_diffusivity: Thermal diffusivity (α)
        nx: Number of grid points
        dx: Grid spacing
        dt: Time step
        steps: Number of time steps
        boundary_left: Left boundary temperature
        boundary_right: Right boundary temperature
        steady_state: Whether to solve steady-state problem
        
    Returns:
        PDEResult object with solution and metadata
    """
    return solve_diffusion_1d(
        diffusion_coeff=thermal_diffusivity,
        nx=nx,
        dx=dx,
        dt=dt,
        steps=steps,
        boundary_left=boundary_left,
        boundary_right=boundary_right,
        steady_state=steady_state
    )


def create_mesh_1d(nx: int = 100, dx: float = 1.0, periodic: bool = False) -> Any:
    """Create a 1D mesh.
    
    Args:
        nx: Number of grid points
        dx: Grid spacing
        periodic: Whether to use periodic boundary conditions
        
    Returns:
        Mesh object
    """
    solver = PDESolver()
    return solver.create_mesh_1d(nx=nx, dx=dx, periodic=periodic)


def create_mesh_2d(
    nx: int = 50,
    ny: int = 50,
    dx: float = 1.0,
    dy: float = 1.0,
    periodic: bool = False
) -> Any:
    """Create a 2D mesh.
    
    Args:
        nx: Number of grid points in x direction
        ny: Number of grid points in y direction
        dx: Grid spacing in x direction
        dy: Grid spacing in y direction
        periodic: Whether to use periodic boundary conditions
        
    Returns:
        Mesh object
    """
    solver = PDESolver()
    return solver.create_mesh_2d(nx=nx, ny=ny, dx=dx, dy=dy, periodic=periodic)


def create_mesh_3d(
    nx: int = 30,
    ny: int = 30,
    nz: int = 30,
    dx: float = 1.0,
    dy: float = 1.0,
    dz: float = 1.0,
    periodic: bool = False
) -> Any:
    """Create a 3D mesh.
    
    Args:
        nx: Number of grid points in x direction
        ny: Number of grid points in y direction
        nz: Number of grid points in z direction
        dx: Grid spacing in x direction
        dy: Grid spacing in y direction
        dz: Grid spacing in z direction
        periodic: Whether to use periodic boundary conditions
        
    Returns:
        Mesh object
    """
    solver = PDESolver()
    return solver.create_mesh_3d(nx=nx, ny=ny, nz=nz, dx=dx, dy=dy, dz=dz, periodic=periodic)
