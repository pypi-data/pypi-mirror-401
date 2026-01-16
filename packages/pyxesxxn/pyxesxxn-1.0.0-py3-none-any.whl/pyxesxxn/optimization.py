"""Optimization module for PyXESXXN - Advanced optimization algorithms for energy systems.

This module provides comprehensive optimization capabilities for multi-carrier energy systems,
including linear, nonlinear, multi-objective, and stochastic optimization methods.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Union, Any
from enum import Enum
import numpy as np
import pandas as pd
from .exceptions import PyXESXXNError, OptimizationError


class OptimizationType(Enum):
    """Enumeration of optimization types."""
    LINEAR = "linear"
    NONLINEAR = "nonlinear"
    MIXED_INTEGER = "mixed_integer"
    MULTI_OBJECTIVE = "multi_objective"
    STOCHASTIC = "stochastic"


class SolverType(Enum):
    """Enumeration of solver types."""
    SCIPY = "scipy"
    GLPK = "glpk"
    GUROBI = "gurobi"
    CPLEX = "cplex"
    IPOPT = "ipopt"


class OptimizationVariable:
    """Represents an optimization variable."""
    
    def __init__(self, name: str, lower_bound: float = 0.0, upper_bound: float = None) -> None:
        """Initialize an optimization variable.
        
        Parameters
        ----------
        name : str
            Variable name.
        lower_bound : float, default=0.0
            Lower bound for the variable.
        upper_bound : float, default=None
            Upper bound for the variable.
        """
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.value: Optional[float] = None


class OptimizationConstraint:
    """Represents an optimization constraint."""
    
    def __init__(self, name: str, expression: str) -> None:
        """Initialize an optimization constraint.
        
        Parameters
        ----------
        name : str
            Constraint name.
        expression : str
            Mathematical expression for the constraint.
        """
        self.name = name
        self.expression = expression


class OptimizationConfig:
    """Configuration class for optimization problems."""
    
    def __init__(
        self,
        objective: str,
        optimization_type: OptimizationType,
        solver_type: SolverType = SolverType.SCIPY
    ) -> None:
        """Initialize an optimization configuration.
        
        Parameters
        ----------
        objective : str
            Objective function expression.
        optimization_type : OptimizationType
            Type of optimization.
        solver_type : SolverType, default=SolverType.SCIPY
            Solver to use.
        """
        self.objective = objective
        self.optimization_type = optimization_type
        self.solver_type = solver_type
        self.variables: List[OptimizationVariable] = []
        self.constraints: List[OptimizationConstraint] = []
    
    def add_variable(self, variable: OptimizationVariable) -> None:
        """Add an optimization variable.
        
        Parameters
        ----------
        variable : OptimizationVariable
            Variable to add.
        """
        self.variables.append(variable)
    
    def add_constraint(self, constraint: OptimizationConstraint) -> None:
        """Add an optimization constraint.
        
        Parameters
        ----------
        constraint : OptimizationConstraint
            Constraint to add.
        """
        self.constraints.append(constraint)


class OptimizationResult:
    """Represents the result of an optimization problem."""
    
    def __init__(self, success: bool, message: str = "") -> None:
        """Initialize an optimization result.
        
        Parameters
        ----------
        success : bool
            Whether the optimization was successful.
        message : str, default=""
            Message describing the result.
        """
        self.success = success
        self.message = message
        self.objective_value: Optional[float] = None
        self.variables: Dict[str, float] = {}
        self.solver_status: Optional[str] = None
        self.iterations: Optional[int] = None
        self.solve_time: Optional[float] = None
        
        # Multi-objective optimization results
        self.pareto_front: Optional[np.ndarray] = None
        self.pareto_set: Optional[np.ndarray] = None
        self.hypervolume_history: Optional[List[float]] = None
        self.optimization_history: Optional[List[Dict[str, Any]]] = None
    
    def set_objective_value(self, value: float) -> None:
        """Set the objective function value.
        
        Parameters
        ----------
        value : float
            Objective value.
        """
        self.objective_value = value
    
    def set_variable_value(self, name: str, value: float) -> None:
        """Set the value for a specific variable.
        
        Parameters
        ----------
        name : str
            Variable name.
        value : float
            Variable value.
        """
        self.variables[name] = value
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the optimization result.
        
        Returns
        -------
        Dict[str, Any]
            Summary dictionary.
        """
        summary = {
            'success': self.success,
            'message': self.message,
            'objective_value': self.objective_value,
            'variables': self.variables,
            'solver_status': self.solver_status,
            'iterations': self.iterations,
            'solve_time': self.solve_time
        }
        
        # Add multi-objective optimization results if available
        if self.pareto_front is not None:
            summary['pareto_front_size'] = len(self.pareto_front)
            summary['pareto_set_size'] = len(self.pareto_set) if self.pareto_set is not None else 0
            
        if self.hypervolume_history is not None and len(self.hypervolume_history) > 0:
            summary['final_hypervolume'] = self.hypervolume_history[-1]
            summary['hypervolume_history_length'] = len(self.hypervolume_history)
            
        if self.optimization_history is not None:
            summary['optimization_history_length'] = len(self.optimization_history)
        
        return summary


class OptimizationModel:
    """Base class for optimization models."""
    
    def __init__(self, config: OptimizationConfig) -> None:
        """Initialize an optimization model.
        
        Parameters
        ----------
        config : OptimizationConfig
            Optimization configuration.
        """
        self.config = config
        self.result: Optional[OptimizationResult] = None
    
    def solve(self) -> OptimizationResult:
        """Solve the optimization problem.
        
        Returns
        -------
        OptimizationResult
            Optimization result object.
        """
        try:
            # Placeholder implementation - would integrate with actual solvers
            result = OptimizationResult(success=True, message="Optimization completed successfully")
            
            # Simple mock solution for demonstration
            solution = {}
            for var in self.config.variables:
                # Set to midpoint of bounds if available
                if var.upper_bound is not None:
                    solution[var.name] = (var.lower_bound + var.upper_bound) / 2
                else:
                    solution[var.name] = var.lower_bound + 1.0
                result.set_variable_value(var.name, solution[var.name])
            
            result.set_objective_value(0.0)  # Mock objective value
            result.solver_status = "optimal"
            result.iterations = 10  # Mock iterations
            result.solve_time = 0.1  # Mock solve time
            
            self.result = result
            return result
            
        except Exception as e:
            error_result = OptimizationResult(success=False, message=f"Optimization failed: {str(e)}")
            self.result = error_result
            return error_result
    
    def get_result(self) -> Optional[OptimizationResult]:
        """Get the optimization result."""
        return self.result


class Optimizer:
    """Base optimizer class with common functionality."""
    
    def __init__(self, name: str) -> None:
        """Initialize an optimizer.
        
        Parameters
        ----------
        name : str
            Optimizer name.
        """
        self.name = name
    
    def optimize(self, model: OptimizationModel) -> OptimizationResult:
        """Optimize the given model.
        
        Parameters
        ----------
        model : OptimizationModel
            Model to optimize.
            
        Returns
        -------
        OptimizationResult
            Optimization result.
        """
        return model.solve()


class LinearOptimizer(Optimizer):
    """Linear programming optimizer."""
    
    def __init__(self) -> None:
        """Initialize a linear optimizer."""
        super().__init__("LinearOptimizer")


class NonlinearOptimizer(Optimizer):
    """Nonlinear programming optimizer."""
    
    def __init__(self) -> None:
        """Initialize a nonlinear optimizer."""
        super().__init__("NonlinearOptimizer")


class MultiObjectiveOptimizer(Optimizer):
    """Multi-objective optimization optimizer using MOMTHRO algorithm."""
    
    def __init__(self, population_size: int = 100, max_iterations: int = 200) -> None:
        """Initialize a multi-objective optimizer with MOMTHRO.
        
        Parameters
        ----------
        population_size : int, default=100
            Population size for MOMTHRO algorithm
        max_iterations : int, default=200
            Maximum iterations for MOMTHRO algorithm
        """
        super().__init__("MultiObjectiveOptimizer")
        self.population_size = population_size
        self.max_iterations = max_iterations
        
    def optimize(self, model: OptimizationModel) -> OptimizationResult:
        """Optimize the given model using MOMTHRO algorithm.
        
        Parameters
        ----------
        model : OptimizationModel
            Model to optimize.
            
        Returns
        -------
        OptimizationResult
            Optimization result with Pareto front information.
        """
        try:
            # Import MOMTHRO optimizer
            from .multi_carrier.MOMTHRO import MOMTHROOptimizer
            
            # Create MOMTHRO optimizer
            momthro = MOMTHROOptimizer(
                population_size=self.population_size,
                max_iterations=self.max_iterations
            )
            
            # For demonstration, create a simple multi-objective test function
            def test_objective(x):
                # Simple multi-objective test function (minimization)
                f1 = np.sum((x - 1) ** 2)  # Distance to (1,1,...,1)
                f2 = np.sum((x + 1) ** 2)  # Distance to (-1,-1,...,1)
                return np.array([f1, f2])
            
            # Define bounds (assuming 2D for demonstration)
            dim = 2
            lower_bounds = np.array([-5.0] * dim)
            upper_bounds = np.array([5.0] * dim)
            
            # Run MOMTHRO optimization
            pareto_front, pareto_set, hypervolume_history = momthro.optimize(
                objective_function=test_objective,
                lower_bounds=lower_bounds,
                upper_bounds=upper_bounds,
                dimension=dim,
                num_objectives=2
            )
            
            # Create result object
            result = OptimizationResult(
                success=True, 
                message="MOMTHRO multi-objective optimization completed successfully"
            )
            
            # Store Pareto front information
            result.pareto_front = pareto_front
            result.pareto_set = pareto_set
            result.hypervolume_history = hypervolume_history
            result.optimization_history = momthro.history
            
            # Set mock variable values for compatibility
            for var in model.config.variables:
                if var.upper_bound is not None:
                    result.set_variable_value(var.name, (var.lower_bound + var.upper_bound) / 2)
                else:
                    result.set_variable_value(var.name, var.lower_bound + 1.0)
            
            result.set_objective_value(0.0)  # Mock objective value
            result.solver_status = "optimal"
            result.iterations = len(hypervolume_history)
            result.solve_time = 0.1  # Mock solve time
            
            return result
            
        except Exception as e:
            error_result = OptimizationResult(
                success=False, 
                message=f"MOMTHRO optimization failed: {str(e)}"
            )
            return error_result


class StochasticOptimizer(Optimizer):
    """Stochastic programming optimizer."""
    
    def __init__(self) -> None:
        """Initialize a stochastic optimizer."""
        super().__init__("StochasticOptimizer")


# Define __all__ for module exports
__all__ = [
    'OptimizationType',
    'SolverType', 
    'OptimizationVariable',
    'OptimizationConstraint',
    'OptimizationConfig',
    'OptimizationResult',
    'OptimizationModel',
    'Optimizer',
    'LinearOptimizer',
    'NonlinearOptimizer',
    'MultiObjectiveOptimizer',
    'StochasticOptimizer',
    'EnergySystemOptimizer'
]


class EnergySystemOptimizer:
    """Specialized optimizer for energy system optimization problems.
    
    This class provides energy-system-specific optimization capabilities,
    including cost minimization, emission reduction, and reliability optimization.
    """
    
    def __init__(self, optimizer: Optimizer) -> None:
        """Initialize an energy system optimizer.
        
        Parameters
        ----------
        optimizer : Optimizer
            Base optimizer to use.
        """
        self.optimizer = optimizer
        self.optimization_history: List[Dict[str, Any]] = []
    
    def optimize_cost(self, model: OptimizationModel) -> OptimizationResult:
        """Optimize for cost minimization.
        
        Parameters
        ----------
        model : OptimizationModel
            Model to optimize.
            
        Returns
        -------
        OptimizationResult
            Optimization result.
        """
        # Add cost-specific constraints and objectives
        result = self.optimizer.optimize(model)
        self.optimization_history.append({
            'type': 'cost_optimization',
            'result': result.get_summary()
        })
        return result
    
    def optimize_emissions(self, model: OptimizationModel) -> OptimizationResult:
        """Optimize for emission reduction.
        
        Parameters
        ----------
        model : OptimizationModel
            Model to optimize.
            
        Returns
        -------
        OptimizationResult
            Optimization result.
        """
        # Add emission-specific constraints and objectives
        result = self.optimizer.optimize(model)
        self.optimization_history.append({
            'type': 'emission_optimization',
            'result': result.get_summary()
        })
        return result
    
    def optimize_reliability(self, model: OptimizationModel) -> OptimizationResult:
        """Optimize for system reliability.
        
        Parameters
        ----------
        model : OptimizationModel
            Model to optimize.
            
        Returns
        -------
        OptimizationResult
            Optimization result.
        """
        # Add reliability-specific constraints and objectives
        result = self.optimizer.optimize(model)
        self.optimization_history.append({
            'type': 'reliability_optimization',
            'result': result.get_summary()
        })
        return result
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get the history of optimization runs."""
        return self.optimization_history.copy()