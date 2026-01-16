"""
SFLA (Strengthened and Faster Linear Approximation) Wrapper

This module provides a convenient wrapper for the SFLA algorithms
for chance-constrained unit commitment and bilevel storage problems.
"""

import sys
import os
from typing import Optional, Dict, Any, Union
import numpy as np

from .base import StochasticOptimizer, ChanceConstraintConfig, OptimizationResult


class SFLAConfig(ChanceConstraintConfig):
    """Configuration specific to SFLA algorithm.
    
    Extends ChanceConstraintConfig with SFLA-specific parameters.
    
    Attributes:
        method: SFLA method variant ('proposed', 'ori', 'exact')
        k: Parameter for SFLA (typically 0.01-0.05)
        num_gen: Number of generators
        num_WT: Number of wind turbines
        num_storage: Number of storage units
        load_scaling_factor: Load scaling factor for testing
    """
    def __init__(
        self,
        method: str = "proposed",
        k: float = 0.01,
        num_gen: int = 19,
        num_WT: int = 3,
        num_storage: int = 2,
        load_scaling_factor: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.method = method
        self.k = k
        self.num_gen = num_gen
        self.num_WT = num_WT
        self.num_storage = num_storage
        self.load_scaling_factor = load_scaling_factor


class SFLAWrapper(StochasticOptimizer):
    """Wrapper for SFLA algorithms.
    
    This class provides a convenient interface for using SFLA
    for chance-constrained optimization problems.
    """
    
    def __init__(self, config: SFLAConfig):
        """Initialize the SFLA wrapper.
        
        Args:
            config: SFLA configuration
        """
        super().__init__(config)
        self.config = config
        
        # Import SFLA modules
        try:
            from ..SFLA.SUC import solve_stochastic_unit_commitment
            from ..SFLA.Bilevel_Storage import solve_bilevel_storage
            from ..SFLA.WT_error_gen import WT_sce_gen
            self._suc_solver = solve_stochastic_unit_commitment
            self._bilevel_solver = solve_bilevel_storage
            self._wt_gen = WT_sce_gen
        except ImportError as e:
            raise ImportError(
                f"Failed to import SFLA modules. Please ensure required dependencies are installed: {e}"
            )
    
    def solve_unit_commitment(
        self,
        LOAD: np.ndarray,
        R_UP_EX: np.ndarray,
        R_DN_EX: np.ndarray,
        P_MIN: np.ndarray,
        P_MAX: np.ndarray,
        R_MAX_UP: np.ndarray,
        R_MAX_DN: np.ndarray,
        W_FORE: np.ndarray,
        c: np.ndarray,
        c_rs: np.ndarray,
        c_cur: np.ndarray,
        WT_error_scenarios: Optional[np.ndarray] = None,
        **kwargs
    ) -> OptimizationResult:
        """Solve chance-constrained unit commitment problem.
        
        Args:
            LOAD: Load profile (T,)
            R_UP_EX: Reserve up requirement (T,)
            R_DN_EX: Reserve down requirement (T,)
            P_MIN: Minimum generation limits (num_gen,)
            P_MAX: Maximum generation limits (num_gen,)
            R_MAX_UP: Maximum reserve up (num_gen,)
            R_MAX_DN: Maximum reserve down (num_gen,)
            W_FORE: Wind forecast (T, num_WT)
            c: Generation cost coefficients (num_gen,)
            c_rs: Reserve start-up cost (num_gen,)
            c_cur: Curtailment cost (num_WT,)
            WT_error_scenarios: Wind error scenarios (N_train, T, num_WT)
            **kwargs: Additional parameters
            
        Returns:
            OptimizationResult object
        """
        import time
        import gurobipy as gp
        from gurobipy import GRB
        
        # Generate wind error scenarios if not provided
        if WT_error_scenarios is None:
            rng = np.random.RandomState(self.config.seed)
            WT_error_scenarios = self._wt_gen(
                self.config.N_train,
                self.config.T,
                self.config.num_WT,
                rng
            )
        
        # Prepare parameters
        params = {
            'LOAD': LOAD,
            'R_UP_EX': R_UP_EX,
            'R_DN_EX': R_DN_EX,
            'T': self.config.T,
            'num_gen': self.config.num_gen,
            'num_WT': self.config.num_WT,
            'N': self.config.N_WDR,
            'epsilon': self.config.epsilon,
            'theta': self.config.theta,
            'k': self.config.k,
            'M': self.config.bigM,
            'random_var_scenarios': WT_error_scenarios,
            'P_MIN': P_MIN,
            'P_MAX': P_MAX,
            'R_MAX_UP': R_MAX_UP,
            'R_MAX_DN': R_MAX_DN,
            'W_FORE': W_FORE,
            'c': c,
            'c_rs': c_rs,
            'c_cur': c_cur,
            'gurobi_seed': self.config.seed,
            'method': self.config.method,
            'njobs': self.config.n_jobs,
            'thread': self.config.thread,
            **kwargs
        }
        
        # Run optimization
        start_time = time.time()
        
        try:
            result = self._suc_solver(**params)
            computation_time = time.time() - start_time
            
            # Parse result
            if isinstance(result, dict):
                objective_value = result.get('objective_value', float('inf'))
                status = result.get('status', 'unknown')
                variables = {k: v for k, v in result.items() 
                           if k not in ['objective_value', 'status', 'time']}
            else:
                objective_value = result
                status = 'optimal'
                variables = {}
            
            opt_result = OptimizationResult(
                objective_value=objective_value,
                computation_time=computation_time,
                solver_time=computation_time,
                status=status,
                variables=variables,
                method=f"SFLA-{self.config.method}",
                config=self.config,
                metadata={
                    'problem_type': 'unit_commitment',
                    'num_scenarios': self.config.N_WDR,
                    'num_time_periods': self.config.T
                }
            )
            
            self._result = opt_result
            return opt_result
            
        except Exception as e:
            return OptimizationResult(
                objective_value=float('inf'),
                computation_time=time.time() - start_time,
                solver_time=time.time() - start_time,
                status=f'error: {str(e)}',
                method=f"SFLA-{self.config.method}",
                config=self.config
            )
    
    def solve_bilevel_storage(
        self,
        LOAD: np.ndarray,
        R_UP_EX: np.ndarray,
        R_DN_EX: np.ndarray,
        P_MIN: np.ndarray,
        P_MAX: np.ndarray,
        R_MAX_UP: np.ndarray,
        R_MAX_DN: np.ndarray,
        W_FORE: np.ndarray,
        c: np.ndarray,
        c_rs: np.ndarray,
        c_cur: np.ndarray,
        storage_params: Dict[str, Any],
        WT_error_scenarios: Optional[np.ndarray] = None,
        **kwargs
    ) -> OptimizationResult:
        """Solve bilevel strategic bidding problem with storage.
        
        Args:
            LOAD: Load profile (T,)
            R_UP_EX: Reserve up requirement (T,)
            R_DN_EX: Reserve down requirement (T,)
            P_MIN: Minimum generation limits (num_gen,)
            P_MAX: Maximum generation limits (num_gen,)
            R_MAX_UP: Maximum reserve up (num_gen,)
            R_MAX_DN: Maximum reserve down (num_gen,)
            W_FORE: Wind forecast (T, num_WT)
            c: Generation cost coefficients (num_gen,)
            c_rs: Reserve start-up cost (num_gen,)
            c_cur: Curtailment cost (num_WT,)
            storage_params: Dictionary of storage parameters
            WT_error_scenarios: Wind error scenarios (N_train, T, num_WT)
            **kwargs: Additional parameters
            
        Returns:
            OptimizationResult object
        """
        import time
        
        # Generate wind error scenarios if not provided
        if WT_error_scenarios is None:
            rng = np.random.RandomState(self.config.seed)
            WT_error_scenarios = self._wt_gen(
                self.config.N_train,
                self.config.T,
                self.config.num_WT,
                rng
            )
        
        # Prepare parameters
        params = {
            'LOAD': LOAD,
            'R_UP_EX': R_UP_EX,
            'R_DN_EX': R_DN_EX,
            'T': self.config.T,
            'num_gen': self.config.num_gen,
            'num_WT': self.config.num_WT,
            'num_storage': self.config.num_storage,
            'N': self.config.N_WDR,
            'epsilon': self.config.epsilon,
            'theta': self.config.theta,
            'k': self.config.k,
            'M': self.config.bigM,
            'random_var_scenarios': WT_error_scenarios,
            'P_MIN': P_MIN,
            'P_MAX': P_MAX,
            'R_MAX_UP': R_MAX_UP,
            'R_MAX_DN': R_MAX_DN,
            'W_FORE': W_FORE,
            'c': c,
            'c_rs': c_rs,
            'c_cur': c_cur,
            'gurobi_seed': self.config.seed,
            'method': self.config.method,
            'njobs': self.config.n_jobs,
            'thread': self.config.thread,
            **storage_params,
            **kwargs
        }
        
        # Run optimization
        start_time = time.time()
        
        try:
            result = self._bilevel_solver(**params)
            computation_time = time.time() - start_time
            
            # Parse result
            if isinstance(result, dict):
                objective_value = result.get('objective_value', float('inf'))
                status = result.get('status', 'unknown')
                variables = {k: v for k, v in result.items() 
                           if k not in ['objective_value', 'status', 'time']}
            else:
                objective_value = result
                status = 'optimal'
                variables = {}
            
            opt_result = OptimizationResult(
                objective_value=objective_value,
                computation_time=computation_time,
                solver_time=computation_time,
                status=status,
                variables=variables,
                method=f"SFLA-{self.config.method}",
                config=self.config,
                metadata={
                    'problem_type': 'bilevel_storage',
                    'num_scenarios': self.config.N_WDR,
                    'num_time_periods': self.config.T
                }
            )
            
            self._result = opt_result
            return opt_result
            
        except Exception as e:
            return OptimizationResult(
                objective_value=float('inf'),
                computation_time=time.time() - start_time,
                solver_time=time.time() - start_time,
                status=f'error: {str(e)}',
                method=f"SFLA-{self.config.method}",
                config=self.config
            )
    
    def optimize(self, problem_type: str = "unit_commitment", **kwargs) -> OptimizationResult:
        """Run optimization (alias for specific problem solvers).
        
        Args:
            problem_type: Type of problem ('unit_commitment' or 'bilevel_storage')
            **kwargs: Problem-specific parameters
            
        Returns:
            OptimizationResult object
        """
        if problem_type == "unit_commitment":
            return self.solve_unit_commitment(**kwargs)
        elif problem_type == "bilevel_storage":
            return self.solve_bilevel_storage(**kwargs)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")
