"""
Grid Feedback Optimizer Integration Module for PyXESXXN

This module provides a convenient interface to integrate grid feedback optimizer
functionality into PyXESXXN for voltage regulation and congestion management
in electrical distribution grids.

Reference:
    Haberle, V. et al. "Gradient Projection for Feedback-Based Optimization 
    of Power Grids", IEEE Control Systems Letters, 2021.
    
    Dall'Anese, E. & Simonetto, A. "Optimal Power Flow Pursuit", 
    IEEE Transactions on Smart Grid, 2018.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
from dataclasses import dataclass, field
import warnings
import copy

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    _GRID_FEEDBACK_BASE_DEPS = True
except ImportError as e:
    _GRID_FEEDBACK_BASE_DEPS = False
    warnings.warn(
        f"Grid Feedback Optimizer base dependencies not available: {e}. "
        "Install required packages: numpy, pandas, matplotlib"
    )

_GRID_FEEDBACK_AVAILABLE = False

if _GRID_FEEDBACK_BASE_DEPS:
    try:
        grid_feedback_path = Path(__file__).parent / "grid_feedback_optimizer" / "src"
        if grid_feedback_path.exists():
            sys.path.insert(0, str(grid_feedback_path))
            
            from grid_feedback_optimizer.models.loader import load_network, load_network_from_excel
            from grid_feedback_optimizer.models.network import Network, Bus, Line, Transformer, Source, RenewGen, Load
            from grid_feedback_optimizer.engine.solve import solve
            from grid_feedback_optimizer.engine.powerflow import PowerFlowSolver
            from grid_feedback_optimizer.engine.grad_proj_optimizer import GradientProjectionOptimizer
            from grid_feedback_optimizer.engine.primal_dual_optimizer import PrimalDualOptimizer
            from grid_feedback_optimizer.models.solve_data import OptimizationInputs, SolveResults
            from grid_feedback_optimizer.utils.utils import network_to_model_data
            _GRID_FEEDBACK_AVAILABLE = True
    except ImportError as e:
        warnings.warn(
            f"Grid Feedback Optimizer modules not available: {e}. "
            "Grid Feedback Optimizer integration will be limited."
        )
        # Define placeholders for type hints
        SolveResults = None
        Network = None
        Bus = None
        Line = None
        Transformer = None
        Source = None
        RenewGen = None
        Load = None
        OptimizationInputs = None


@dataclass
class GridFeedbackConfig:
    """Configuration for Grid Feedback Optimizer.
    
    Attributes:
        algorithm: Optimization algorithm ('gp' for Gradient Projection, 'pd' for Primal-Dual)
        max_iter: Maximum number of iterations
        tol: Convergence tolerance
        delta_p: Active power perturbation for sensitivity analysis
        delta_q: Reactive power perturbation for sensitivity analysis
        alpha: Step size parameter
        alpha_v: Voltage penalty weight (for PD algorithm)
        alpha_l: Line loading penalty weight (for PD algorithm)
        alpha_t: Transformer loading penalty weight (for PD algorithm)
        solver: Convex solver to use ('CLARABEL', 'ECOS', 'OSQP', 'SCS')
        loading_meas_side: Measurement side for line loading ('from' or 'to')
        rel_tol: Relative tolerance for voltage
        rel_tol_line: Relative tolerance for line loading
        record_iterates: Whether to record iteration history
    """
    algorithm: str = 'gp'
    max_iter: int = 1000
    tol: float = 1e-3
    delta_p: float = 1.0
    delta_q: float = 1.0
    alpha: float = 0.5
    alpha_v: float = 10.0
    alpha_l: float = 10.0
    alpha_t: float = 10.0
    solver: str = 'CLARABEL'
    loading_meas_side: str = 'from'
    rel_tol: float = 1e-4
    rel_tol_line: float = 1e-2
    record_iterates: bool = True
    
    def __post_init__(self):
        if self.algorithm.lower() not in ['gp', 'pd']:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}. Use 'gp' or 'pd'")
        if self.loading_meas_side not in ['from', 'to']:
            raise ValueError(f"loading_meas_side must be 'from' or 'to'")


class GridFeedbackOptimizer:
    """Wrapper for Grid Feedback Optimizer functionality in PyXESXXN.
    
    This class provides a convenient interface to use grid feedback optimization
    for voltage regulation and congestion management in electrical distribution grids.
    
    Example:
        >>> config = GridFeedbackConfig(algorithm='gp', max_iter=500)
        >>> optimizer = GridFeedbackOptimizer(config)
        >>> optimizer.load_network('network.json')
        >>> results = optimizer.optimize()
        >>> results.print_summary()
    """
    
    def __init__(self, config: Optional[GridFeedbackConfig] = None):
        """Initialize Grid Feedback Optimizer.
        
        Args:
            config: GridFeedbackConfig instance with optimization parameters
        """
        if not _GRID_FEEDBACK_AVAILABLE:
            raise RuntimeError(
                "Grid Feedback Optimizer is not available. Please ensure "
                "grid_feedback_optimizer directory exists and all dependencies are installed."
            )
        
        self.config = config if config is not None else GridFeedbackConfig()
        self.network: Optional[Network] = None
        self.power_flow_solver: Optional[PowerFlowSolver] = None
        self.results: Optional[SolveResults] = None
        self._loaded = False
        
    def load_network(self, file_path: Union[str, Path]):
        """Load network from JSON or Excel file.
        
        Args:
            file_path: Path to network file (.json or .xlsx)
        """
        if not _GRID_FEEDBACK_AVAILABLE:
            raise RuntimeError("Grid Feedback Optimizer is not available")
        
        file_path = Path(file_path)
        
        if file_path.suffix == '.xlsx':
            self.network = load_network_from_excel(file_path)
        else:
            self.network = load_network(file_path)
        
        self.power_flow_solver = PowerFlowSolver(self.network)
        self._loaded = True
        
    def create_network(
        self,
        buses: List[Dict[str, Any]],
        lines: List[Dict[str, Any]],
        sources: List[Dict[str, Any]],
        transformers: Optional[List[Dict[str, Any]]] = None,
        loads: Optional[List[Dict[str, Any]]] = None,
        renew_gens: Optional[List[Dict[str, Any]]] = None
    ):
        """Create network programmatically.
        
        Args:
            buses: List of bus configurations
            lines: List of line configurations
            sources: List of source configurations
            transformers: Optional list of transformer configurations
            loads: Optional list of load configurations
            renew_gens: Optional list of renewable generator configurations
        """
        if not _GRID_FEEDBACK_AVAILABLE:
            raise RuntimeError("Grid Feedback Optimizer is not available")
        
        self.network = Network()
        
        for bus_config in buses:
            self.network.add_bus(Bus(**bus_config))
        
        for line_config in lines:
            self.network.add_line(Line(**line_config))
        
        for source_config in sources:
            self.network.add_source(Source(**source_config))
        
        if transformers is not None:
            for trans_config in transformers:
                self.network.add_transformer(Transformer(**trans_config))
        
        if loads is not None:
            for load_config in loads:
                self.network.add_load(Load(**load_config))
        
        if renew_gens is not None:
            for renew_config in renew_gens:
                self.network.add_renew_gen(RenewGen(**renew_config))
        
        self.power_flow_solver = PowerFlowSolver(self.network)
        self._loaded = True
        
    def check_congestion(self) -> bool:
        """Check if network is congested.
        
        Returns:
            True if network is congested, False otherwise
        """
        if not self._loaded:
            raise RuntimeError("Network not loaded. Call load_network() or create_network() first.")
        
        return self.power_flow_solver.is_congested
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information.
        
        Returns:
            Dictionary with network statistics
        """
        if not self._loaded:
            raise RuntimeError("Network not loaded. Call load_network() or create_network() first.")
        
        return {
            'num_buses': len(self.network.buses),
            'num_lines': len(self.network.lines),
            'num_sources': len(self.network.sources),
            'num_transformers': len(self.network.transformers),
            'num_loads': len(self.network.loads),
            'num_renew_gens': len(self.network.renew_gens),
            'is_congested': self.power_flow_solver.is_congested
        }
    
    def optimize(self, **kwargs):
        """Run grid feedback optimization.
        
        Args:
            **kwargs: Override configuration parameters
            
        Returns:
            SolveResults with optimization results
        """
        if not self._loaded:
            raise RuntimeError("Network not loaded. Call load_network() or create_network() first.")
        
        config = copy.deepcopy(self.config)
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        self.results = solve(
            network=self.network,
            max_iter=config.max_iter,
            tol=config.tol,
            delta_p=config.delta_p,
            delta_q=config.delta_q,
            algorithm=config.algorithm,
            alpha=config.alpha,
            alpha_v=config.alpha_v,
            alpha_l=config.alpha_l,
            alpha_t=config.alpha_t,
            record_iterates=config.record_iterates,
            solver=config.solver,
            loading_meas_side=config.loading_meas_side,
            rel_tol=config.rel_tol,
            rel_tol_line=config.rel_tol_line
        )
        
        return self.results
    
    def get_results(self) -> Optional[SolveResults]:
        """Get optimization results.
        
        Returns:
            SolveResults or None if optimization hasn't been run
        """
        return self.results
    
    def print_summary(self):
        """Print optimization results summary."""
        if self.results is None:
            print("No optimization results available. Run optimize() first.")
            return
        
        self.results.print_summary()
    
    def save_results(self, file_path: Union[str, Path]):
        """Save optimization results to file.
        
        Args:
            file_path: Path to save results (.json)
        """
        if self.results is None:
            raise RuntimeError("No optimization results to save. Run optimize() first.")
        
        self.results.save(file_path)
    
    def plot_iterations(self, figsize: tuple = (12, 8)):
        """Plot optimization iteration history.
        
        Args:
            figsize: Figure size (width, height)
        """
        if self.results is None:
            raise RuntimeError("No optimization results to plot. Run optimize() first.")
        
        self.results.plot_iterations(figsize=figsize)
    
    def get_final_setpoints(self) -> Dict[str, np.ndarray]:
        """Get final generator setpoints.
        
        Returns:
            Dictionary with final active and reactive power setpoints
        """
        if self.results is None:
            raise RuntimeError("No optimization results available. Run optimize() first.")
        
        return {
            'p_setpoints': self.results.final_gen_update[:, 0],
            'q_setpoints': self.results.final_gen_update[:, 1]
        }
    
    def get_voltage_profile(self) -> np.ndarray:
        """Get final voltage profile.
        
        Returns:
            Array of bus voltages in per-unit
        """
        if self.results is None:
            raise RuntimeError("No optimization results available. Run optimize() first.")
        
        from power_grid_model import ComponentType
        return np.array(self.results.final_output[ComponentType.node]['u_pu'])
    
    def get_line_loadings(self) -> Dict[str, np.ndarray]:
        """Get final line loadings.
        
        Returns:
            Dictionary with line active and reactive power flows
        """
        if self.results is None:
            raise RuntimeError("No optimization results available. Run optimize() first.")
        
        from power_grid_model import ComponentType
        output = self.results.final_output
        
        return {
            'p_line': np.array(output[ComponentType.line]['p_from']),
            'q_line': np.array(output[ComponentType.line]['q_from'])
        }


def create_grid_feedback_optimizer(
    network_file: Union[str, Path],
    algorithm: str = 'gp',
    **kwargs
) -> GridFeedbackOptimizer:
    """Convenience function to create and setup a Grid Feedback Optimizer.
    
    Args:
        network_file: Path to network file (.json or .xlsx)
        algorithm: Optimization algorithm ('gp' or 'pd')
        **kwargs: Additional configuration parameters
        
    Returns:
        Configured GridFeedbackOptimizer instance
    """
    config = GridFeedbackConfig(algorithm=algorithm, **kwargs)
    optimizer = GridFeedbackOptimizer(config)
    optimizer.load_network(network_file)
    
    return optimizer


def optimize_grid(
    network_file: Union[str, Path],
    algorithm: str = 'gp',
    save_path: Optional[Union[str, Path]] = None,
    **kwargs
):
    """Convenience function to run grid feedback optimization.
    
    Args:
        network_file: Path to network file (.json or .xlsx)
        algorithm: Optimization algorithm ('gp' or 'pd')
        save_path: Optional path to save results
        **kwargs: Additional configuration parameters
        
    Returns:
        SolveResults with optimization results
    """
    optimizer = create_grid_feedback_optimizer(network_file, algorithm, **kwargs)
    results = optimizer.optimize()
    
    if save_path is not None:
        results.save(save_path)
    
    return results


def check_grid_feedback_dependencies() -> Dict[str, bool]:
    """Check Grid Feedback Optimizer dependencies.
    
    Returns:
        Dictionary with dependency availability status
    """
    return {
        'base_dependencies': _GRID_FEEDBACK_BASE_DEPS,
        'grid_feedback_optimizer': _GRID_FEEDBACK_AVAILABLE
    }


__all__ = [
    'GridFeedbackConfig',
    'GridFeedbackOptimizer',
    'create_grid_feedback_optimizer',
    'optimize_grid',
    'check_grid_feedback_dependencies'
]
