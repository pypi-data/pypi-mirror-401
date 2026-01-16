"""
Abstract interfaces for optimization components.

This module defines abstract base classes and interfaces for optimization
functionality, completely independent of PyPSA and Linopy dependencies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Union, Any, Tuple, Callable
from dataclasses import dataclass, field


class OptimizationType(Enum):
    """Types of optimization problems supported by PyXESXXN."""
    LINEAR = "linear"
    NONLINEAR = "nonlinear"
    MIXED_INTEGER = "mixed_integer"
    MULTI_OBJECTIVE = "multi_objective"
    STOCHASTIC = "stochastic"


class SolverType(Enum):
    """Types of optimization solvers supported by PyXESXXN."""
    GLPK = "glpk"  # Open-source linear programming
    CBC = "cbc"    # Open-source mixed-integer programming
    IPOPT = "ipopt" # Open-source nonlinear programming
    SCIP = "scip"  # Open-source constraint programming
    SCIPY = "scipy" # SciPy optimization algorithms
    GUROBI = "gurobi" # Gurobi optimization solver
    CPLEX = "cplex" # CPLEX optimization solver
    CUSTOM = "custom"  # Custom solver implementation


@dataclass
class OptimizationConfig:
    """Configuration for optimization problems."""
    name: str
    optimization_type: OptimizationType
    solver: SolverType
    time_horizon: int = 24
    objective_function: Optional[Callable] = None
    constraints: List[Callable] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class OptimizationVariable(ABC):
    """Abstract base class for optimization variables."""
    
    @abstractmethod
    def __init__(self, name: str, lower_bound: float = 0.0, 
                 upper_bound: float = float('inf'), variable_type: str = "continuous"):
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the variable name."""
        pass
    
    @property
    @abstractmethod
    def value(self) -> Optional[float]:
        """Get the variable value after optimization."""
        pass
    
    @value.setter
    @abstractmethod
    def value(self, value: float) -> None:
        """Set the variable value."""
        pass


class OptimizationConstraint(ABC):
    """Abstract base class for optimization constraints."""
    
    @abstractmethod
    def __init__(self, name: str, expression: Callable, 
                 lower_bound: float = 0.0, upper_bound: float = 0.0):
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the constraint name."""
        pass
    
    @abstractmethod
    def evaluate(self, variables: Dict[str, float]) -> float:
        """Evaluate the constraint expression."""
        pass
    
    @abstractmethod
    def is_satisfied(self, variables: Dict[str, float]) -> bool:
        """Check if constraint is satisfied."""
        pass


class Optimizer(ABC):
    """Abstract base class for optimization algorithms."""
    
    @abstractmethod
    def __init__(self, config: OptimizationConfig):
        pass
    
    @abstractmethod
    def add_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """Add an optimization variable."""
        pass
    
    @abstractmethod
    def add_constraint(self, name: str, expression: Callable, **kwargs) -> OptimizationConstraint:
        """Add an optimization constraint."""
        pass
    
    @abstractmethod
    def set_objective(self, objective: Callable) -> None:
        """Set the objective function."""
        pass
    
    @abstractmethod
    def solve(self) -> Dict[str, Any]:
        """Solve the optimization problem."""
        pass
    
    @abstractmethod
    def validate_problem(self) -> Tuple[bool, List[str]]:
        """Validate the optimization problem setup."""
        pass


class LinearOptimizer(Optimizer):
    """Abstract base class for linear programming optimizers."""
    
    @abstractmethod
    def __init__(self, config: OptimizationConfig):
        pass
    
    @abstractmethod
    def set_coefficient(self, variable_name: str, coefficient: float) -> None:
        """Set coefficient for a variable in the objective function."""
        pass
    
    @abstractmethod
    def add_linear_constraint(self, name: str, coefficients: Dict[str, float], 
                            lower_bound: float, upper_bound: float) -> OptimizationConstraint:
        """Add a linear constraint."""
        pass


class NonlinearOptimizer(Optimizer):
    """Abstract base class for nonlinear programming optimizers."""
    
    @abstractmethod
    def __init__(self, config: OptimizationConfig):
        pass
    
    @abstractmethod
    def set_gradient(self, gradient: Callable) -> None:
        """Set the gradient function for the objective."""
        pass
    
    @abstractmethod
    def set_hessian(self, hessian: Callable) -> None:
        """Set the Hessian function for the objective."""
        pass
    
    @abstractmethod
    def add_nonlinear_constraint(self, name: str, expression: Callable, 
                               lower_bound: float, upper_bound: float) -> OptimizationConstraint:
        """Add a nonlinear constraint."""
        pass


class MultiObjectiveOptimizer(Optimizer):
    """Abstract base class for multi-objective optimization."""
    
    @abstractmethod
    def __init__(self, config: OptimizationConfig):
        pass
    
    @abstractmethod
    def add_objective(self, objective: Callable, weight: float = 1.0) -> None:
        """Add an objective function with weight."""
        pass
    
    @abstractmethod
    def get_pareto_front(self) -> List[Dict[str, float]]:
        """Get the Pareto front of optimal solutions."""
        pass
    
    @abstractmethod
    def set_preference(self, preferences: Dict[str, float]) -> None:
        """Set preferences for multi-objective optimization."""
        pass


class StochasticOptimizer(Optimizer):
    """Abstract base class for stochastic optimization."""
    
    @abstractmethod
    def __init__(self, config: OptimizationConfig):
        pass
    
    @abstractmethod
    def add_scenario(self, scenario_name: str, probability: float) -> None:
        """Add a scenario with associated probability."""
        pass
    
    @abstractmethod
    def set_scenario_objective(self, scenario_name: str, objective: Callable) -> None:
        """Set objective function for a specific scenario."""
        pass
    
    @abstractmethod
    def get_expected_value(self) -> float:
        """Get the expected value of the objective function."""
        pass
    
    @abstractmethod
    def get_scenario_solution(self, scenario_name: str) -> Dict[str, float]:
        """Get the solution for a specific scenario."""
        pass


# Factory interface for creating optimization components
class OptimizationFactory(ABC):
    """Abstract factory for creating optimization components."""
    
    @abstractmethod
    def create_optimizer(self, config: OptimizationConfig) -> Optimizer:
        """Create an optimizer based on configuration."""
        pass
    
    @abstractmethod
    def create_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """Create an optimization variable."""
        pass
    
    @abstractmethod
    def create_constraint(self, name: str, expression: Callable, **kwargs) -> OptimizationConstraint:
        """Create an optimization constraint."""
        pass
    
    @abstractmethod
    def create_linear_optimizer(self, config: OptimizationConfig) -> LinearOptimizer:
        """Create a linear optimizer."""
        pass
    
    @abstractmethod
    def create_nonlinear_optimizer(self, config: OptimizationConfig) -> NonlinearOptimizer:
        """Create a nonlinear optimizer."""
        pass
    
    @abstractmethod
    def create_multi_objective_optimizer(self, config: OptimizationConfig) -> MultiObjectiveOptimizer:
        """Create a multi-objective optimizer."""
        pass
    
    @abstractmethod
    def create_stochastic_optimizer(self, config: OptimizationConfig) -> StochasticOptimizer:
        """Create a stochastic optimizer."""
        pass


# Utility functions for optimization
def create_optimization_config(name: str, optimization_type: OptimizationType, 
                             solver: SolverType, **kwargs) -> OptimizationConfig:
    """Create an optimization configuration."""
    return OptimizationConfig(name=name, optimization_type=optimization_type, 
                            solver=solver, **kwargs)


def validate_optimization_problem(variables: List[OptimizationVariable], 
                                constraints: List[OptimizationConstraint], 
                                objective: Optional[Callable]) -> Tuple[bool, List[str]]:
    """Validate an optimization problem setup."""
    errors = []
    
    if not variables:
        errors.append("No optimization variables defined")
    
    if objective is None:
        errors.append("Objective function not set")
    
    # Check variable bounds
    for variable in variables:
        if hasattr(variable, 'lower_bound') and hasattr(variable, 'upper_bound'):
            if variable.lower_bound > variable.upper_bound:
                errors.append(f"Variable {variable.name} has invalid bounds")
    
    return len(errors) == 0, errors


# Default optimization factory implementation
def get_default_optimization_factory() -> OptimizationFactory:
    """Get the default optimization factory implementation."""
    from .pyxesxxn_impl import PyXESXXNOptimizationFactory
    return PyXESXXNOptimizationFactory()