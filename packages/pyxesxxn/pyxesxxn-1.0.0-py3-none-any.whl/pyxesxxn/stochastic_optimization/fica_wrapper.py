"""
FICA (Faster Inner Convex Approximation) Wrapper

This module provides a convenient wrapper for the FICA algorithm
for chance-constrained power dispatch problems with decision-coupled uncertainty.
"""

import sys
import os
from typing import Optional, Dict, Any, Union
import numpy as np

from .base import StochasticOptimizer, ChanceConstraintConfig, OptimizationResult


class FICAConfig(ChanceConstraintConfig):
    """Configuration specific to FICA algorithm.
    
    Extends ChanceConstraintConfig with FICA-specific parameters.
    
    Attributes:
        method: FICA method variant ('FICA', 'CVAR', 'ExactLHS')
        num_gen: Number of generators
        num_WT: Number of wind turbines
        num_branch: Number of transmission branches
        gen_bus_list: List of generator bus indices
        WT_bus_list: List of wind turbine bus indices
        load_scaling_factor: Load scaling factor for testing
    """
    def __init__(
        self,
        method: str = "FICA",
        num_gen: int = 19,
        num_WT: int = 3,
        num_branch: int = 38,
        gen_bus_list: Optional[list] = None,
        WT_bus_list: Optional[list] = None,
        load_scaling_factor: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.method = method
        self.num_gen = num_gen
        self.num_WT = num_WT
        self.num_branch = num_branch
        self.gen_bus_list = gen_bus_list if gen_bus_list is not None else []
        self.WT_bus_list = WT_bus_list if WT_bus_list is not None else []
        self.load_scaling_factor = load_scaling_factor


class FICAWrapper(StochasticOptimizer):
    """Wrapper for FICA algorithm.
    
    This class provides a convenient interface for using FICA
    for chance-constrained power dispatch problems.
    """
    
    def __init__(self, config: FICAConfig):
        """Initialize the FICA wrapper.
        
        Args:
            config: FICA configuration
        """
        super().__init__(config)
        self.config = config
        
        # Import FICA modules
        try:
            from ..FICA.PD import solve_PD, check_JCC
            from ..FICA.WT_error_gen import WT_sce_gen
            self._pd_solver = solve_PD
            self._jcc_checker = check_JCC
            self._wt_gen = WT_sce_gen
        except ImportError as e:
            raise ImportError(
                f"Failed to import FICA modules. Please ensure required dependencies are installed: {e}"
            )
    
    def solve_power_dispatch(
        self,
        load_bus_all: np.ndarray,
        PTDF: np.ndarray,
        gen_cap_individual: np.ndarray,
        gen_pmin_individual: np.ndarray,
        WT_pred: np.ndarray,
        WT_error_scenarios_train: np.ndarray,
        P_line_limit: np.ndarray,
        gen_cost: np.ndarray,
        gen_cost_quadra: Optional[np.ndarray] = None,
        WT_error_scenarios_test: Optional[np.ndarray] = None,
        **kwargs
    ) -> OptimizationResult:
        """Solve chance-constrained power dispatch problem.
        
        Args:
            load_bus_all: Load at all buses (T, num_bus)
            PTDF: Power transfer distribution factor matrix (num_bus, num_branch)
            gen_cap_individual: Generator capacity limits (num_gen,)
            gen_pmin_individual: Generator minimum limits (num_gen,)
            WT_pred: Wind power forecast (T, num_WT)
            WT_error_scenarios_train: Wind error scenarios for training (N_train, T, num_WT)
            P_line_limit: Line flow limits (num_branch,)
            gen_cost: Generation cost coefficients (num_gen,)
            gen_cost_quadra: Quadratic generation cost coefficients (num_gen,)
            WT_error_scenarios_test: Wind error scenarios for testing (N_test, T, num_WT)
            **kwargs: Additional parameters
            
        Returns:
            OptimizationResult object
        """
        import time
        
        # Generate wind error scenarios for testing if not provided
        if WT_error_scenarios_test is None:
            rng = np.random.RandomState(self.config.seed)
            WT_error_scenarios_test = self._wt_gen(
                self.config.N_test,
                self.config.T,
                self.config.num_WT,
                rng
            )
        
        # Prepare parameters
        params = {
            'T': self.config.T,
            'num_gen': self.config.num_gen,
            'num_WT': self.config.num_WT,
            'num_branch': self.config.num_branch,
            'load_bus_all': load_bus_all,
            'PTDF': PTDF,
            'gen_cap_individual': gen_cap_individual,
            'gen_pmin_individual': gen_pmin_individual,
            'WT_pred': WT_pred,
            'WT_error_scenarios_train': WT_error_scenarios_train,
            'P_line_limit': P_line_limit,
            'gen_bus_list': self.config.gen_bus_list,
            'WT_bus_list': self.config.WT_bus_list,
            'N_WDR': self.config.N_WDR,
            'epsilon': self.config.epsilon,
            'theta': self.config.theta,
            'MIPGap': self.config.MIPGap,
            'rng': np.random.RandomState(self.config.seed),
            'bigM': self.config.bigM,
            'gen_cost': gen_cost,
            'gen_cost_quadra': gen_cost_quadra if gen_cost_quadra is not None else np.zeros_like(gen_cost),
            'gurobi_seed': self.config.seed,
            'method': self.config.method,
            'njobs': self.config.n_jobs,
            'thread': self.config.thread,
            'norm_ord': self.config.norm_ord,
            **kwargs
        }
        
        # Run optimization
        start_time = time.time()
        
        try:
            result = self._pd_solver(**params)
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
            
            # Check JCC satisfaction rate if test scenarios provided
            jcc_satisfaction_rate = None
            if WT_error_scenarios_test is not None and 'gen_power_all' in variables:
                try:
                    jcc_satisfaction_rate = self._jcc_checker(
                        T=self.config.T,
                        num_gen=self.config.num_gen,
                        num_branch=self.config.num_branch,
                        gen_power_all=variables['gen_power_all'],
                        gen_alpha_all=variables.get('gen_alpha_all', np.zeros((self.config.T, self.config.num_gen))),
                        load_bus_all=load_bus_all,
                        PTDF=PTDF,
                        gen_cap_individual=gen_cap_individual,
                        gen_pmin_individual=gen_pmin_individual,
                        WT_pred=WT_pred,
                        WT_error_scenarios_test=WT_error_scenarios_test,
                        P_line_limit=P_line_limit,
                        gen_bus_list=self.config.gen_bus_list,
                        WT_bus_list=self.config.WT_bus_list
                    )
                except Exception as e:
                    pass
            
            opt_result = OptimizationResult(
                objective_value=objective_value,
                computation_time=computation_time,
                solver_time=computation_time,
                status=status,
                variables=variables,
                method=f"FICA-{self.config.method}",
                config=self.config,
                metadata={
                    'problem_type': 'power_dispatch',
                    'num_scenarios': self.config.N_WDR,
                    'num_time_periods': self.config.T,
                    'jcc_satisfaction_rate': jcc_satisfaction_rate
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
                method=f"FICA-{self.config.method}",
                config=self.config
            )
    
    def verify_jcc(
        self,
        gen_power_all: np.ndarray,
        gen_alpha_all: np.ndarray,
        load_bus_all: np.ndarray,
        PTDF: np.ndarray,
        gen_cap_individual: np.ndarray,
        gen_pmin_individual: np.ndarray,
        WT_pred: np.ndarray,
        WT_error_scenarios_test: np.ndarray,
        P_line_limit: np.ndarray
    ) -> float:
        """Verify JCC satisfaction rate for given solution.
        
        Args:
            gen_power_all: Generator power schedule (T, num_gen)
            gen_alpha_all: AGC factors (T, num_gen)
            load_bus_all: Load at all buses (T, num_bus)
            PTDF: Power transfer distribution factor matrix
            gen_cap_individual: Generator capacity limits
            gen_pmin_individual: Generator minimum limits
            WT_pred: Wind power forecast
            WT_error_scenarios_test: Wind error scenarios for testing
            P_line_limit: Line flow limits
            
        Returns:
            JCC satisfaction rate (0-1)
        """
        return self._jcc_checker(
            T=self.config.T,
            num_gen=self.config.num_gen,
            num_branch=self.config.num_branch,
            gen_power_all=gen_power_all,
            gen_alpha_all=gen_alpha_all,
            load_bus_all=load_bus_all,
            PTDF=PTDF,
            gen_cap_individual=gen_cap_individual,
            gen_pmin_individual=gen_pmin_individual,
            WT_pred=WT_pred,
            WT_error_scenarios_test=WT_error_scenarios_test,
            P_line_limit=P_line_limit,
            gen_bus_list=self.config.gen_bus_list,
            WT_bus_list=self.config.WT_bus_list
        )
    
    def optimize(self, problem_type: str = "power_dispatch", **kwargs) -> OptimizationResult:
        """Run optimization (alias for specific problem solvers).
        
        Args:
            problem_type: Type of problem (currently only 'power_dispatch')
            **kwargs: Problem-specific parameters
            
        Returns:
            OptimizationResult object
        """
        if problem_type == "power_dispatch":
            return self.solve_power_dispatch(**kwargs)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")
