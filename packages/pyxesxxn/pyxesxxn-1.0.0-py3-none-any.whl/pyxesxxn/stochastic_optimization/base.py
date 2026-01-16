"""
Base classes for stochastic optimization in PyXESXXN.

This module provides the fundamental data structures and interfaces
for chance-constrained optimization problems.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import numpy as np


class OptimizationMethod(Enum):
    """Enumeration of available optimization methods."""
    SFLA = "SFLA"
    FICA = "FICA"
    CVAR = "CVAR"
    EXACT_LHS = "EXACT_LHS"
    LA = "LA"


class NormType(Enum):
    """Enumeration of norm types for dual norm constraints."""
    L1 = 1
    L2 = 2
    LINF = np.inf


@dataclass
class ChanceConstraintConfig:
    """Configuration for chance-constrained optimization problems.
    
    Attributes:
        epsilon: Risk level for chance constraints (typically 0.01-0.1)
        theta: Wasserstein distance parameter
        N_WDR: Number of Wasserstein distance robust samples
        N_train: Number of training scenarios
        N_test: Number of testing scenarios
        T: Number of time periods
        bigM: Big-M constant for linearization
        MIPGap: MIP gap tolerance for solver
        norm_ord: Norm order for dual norm constraints (1, 2, or inf)
        seed: Random seed for reproducibility
        n_jobs: Number of parallel jobs
        thread: Number of threads per solver
    """
    epsilon: float = 0.03
    theta: float = 0.13
    N_WDR: int = 100
    N_train: int = 1000
    N_test: int = 100
    T: int = 24
    bigM: float = 100000
    MIPGap: float = 0.001
    norm_ord: int = 2
    seed: int = 0
    n_jobs: int = 1
    thread: int = 4
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'epsilon': self.epsilon,
            'theta': self.theta,
            'N_WDR': self.N_WDR,
            'N_train': self.N_train,
            'N_test': self.N_test,
            'T': self.T,
            'bigM': self.bigM,
            'MIPGap': self.MIPGap,
            'norm_ord': self.norm_ord,
            'seed': self.seed,
            'n_jobs': self.n_jobs,
            'thread': self.thread
        }


@dataclass
class OptimizationResult:
    """Result of stochastic optimization.
    
    Attributes:
        objective_value: Optimal objective value
        computation_time: Total computation time in seconds
        solver_time: Solver time in seconds
        status: Optimization status (optimal, infeasible, etc.)
        variables: Dictionary of optimized variables
        constraints: Dictionary of constraint information
        method: Method used for optimization
        config: Configuration used
        metadata: Additional metadata
    """
    objective_value: float
    computation_time: float
    solver_time: float
    status: str
    variables: Dict[str, np.ndarray] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    method: str = ""
    config: Optional[ChanceConstraintConfig] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'objective_value': self.objective_value,
            'computation_time': self.computation_time,
            'solver_time': self.solver_time,
            'status': self.status,
            'variables': {k: v.tolist() if isinstance(v, np.ndarray) else v 
                          for k, v in self.variables.items()},
            'constraints': self.constraints,
            'method': self.method,
            'config': self.config.to_dict() if self.config else None,
            'metadata': self.metadata
        }


class StochasticOptimizer:
    """Base class for stochastic optimization algorithms.
    
    This class provides a common interface for different stochastic
    optimization methods including SFLA and FICA.
    """
    
    def __init__(self, config: ChanceConstraintConfig):
        """Initialize the optimizer.
        
        Args:
            config: Configuration for the optimization problem
        """
        self.config = config
        self._result: Optional[OptimizationResult] = None
    
    def optimize(self, **kwargs) -> OptimizationResult:
        """Run the optimization.
        
        Args:
            **kwargs: Additional problem-specific parameters
            
        Returns:
            OptimizationResult object containing the solution
        """
        raise NotImplementedError("Subclasses must implement optimize()")
    
    def get_result(self) -> Optional[OptimizationResult]:
        """Get the last optimization result.
        
        Returns:
            OptimizationResult object or None if not optimized yet
        """
        return self._result
    
    def validate_config(self) -> bool:
        """Validate the configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if self.config.epsilon <= 0 or self.config.epsilon >= 1:
            return False
        if self.config.theta < 0:
            return False
        if self.config.N_WDR <= 0:
            return False
        if self.config.T <= 0:
            return False
        if self.config.bigM <= 0:
            return False
        if self.config.norm_ord not in [1, 2, np.inf]:
            return False
        return True
