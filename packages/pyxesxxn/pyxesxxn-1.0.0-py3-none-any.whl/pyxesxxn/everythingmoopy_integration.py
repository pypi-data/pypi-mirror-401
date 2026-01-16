"""
EverythingMoopy Integration Module for PyXESXXN

This module provides a convenient interface to integrate everythingmoopy (pymoo-based
multi-objective optimization framework) into PyXESXXN without modifying core PyXESXXN code.

EverythingMoopy offers state-of-the-art single- and multi-objective optimization algorithms
and many features related to multi-objective optimization such as visualization and
decision making.

Key Features:
- Single-objective optimization algorithms (DE, PSO, GA, CMA-ES, etc.)
- Multi-objective optimization algorithms (NSGA-II, NSGA-III, MOEA/D, etc.)
- Standard test problems (ZDT, DTLZ, WFG, etc.)
- Constraint handling mechanisms
- Performance indicators (HV, IGD, GD, etc.)
- Visualization tools
- Termination criteria
- Custom problem definition support

Integration Approach:
- Lazy loading to avoid import errors if everythingmoopy is not available
- Wrapper classes for common use cases
- Energy system-specific optimization problems
- Compatibility with PyXESXXN network models
"""

from __future__ import annotations

from typing import Any, Optional, Dict, List, Union, Callable
import warnings

# Try to import everythingmoopy, set availability flag
try:
    import sys
    import os
    everythingmoopy_path = os.path.join(os.path.dirname(__file__), 'everythingmoopy')
    if everythingmoopy_path not in sys.path:
        sys.path.insert(0, everythingmoopy_path)
    
    from pymoo.optimize import minimize as pymoo_minimize
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.algorithms.moo.nsga3 import NSGA3
    from pymoo.algorithms.moo.moead import MOEAD
    from pymoo.algorithms.moo.rvea import RVEA
    from pymoo.algorithms.moo.sms import SMSEMOA
    from pymoo.algorithms.moo.age2 import AGEMOEA2
    from pymoo.algorithms.soo.de import DE
    from pymoo.algorithms.soo.pso import PSO
    from pymoo.algorithms.soo.ga import GA
    from pymoo.algorithms.soo.cmaes import CMAES
    from pymoo.algorithms.soo.nelder import NelderMead
    from pymoo.algorithms.soo.pattern import PatternSearch
    from pymoo.problems import get_problem as pymoo_get_problem
    from pymoo.core.problem import Problem as PymooProblem
    from pymoo.core.algorithm import Algorithm as PymooAlgorithm
    from pymoo.core.termination import Termination as PymooTermination
    from pymoo.termination import get_termination as pymoo_get_termination
    from pymoo.visualization.scatter import Scatter as PymooScatter
    from pymoo.visualization.pcp import PCP as PymooPCP
    from pymoo.visualization.radar import Radar as PymooRadar
    from pymoo.visualization.heatmap import Heatmap as PymooHeatmap
    from pymoo.indicators.hv import HV
    from pymoo.indicators.igd import IGD
    from pymoo.indicators.igd_plus import IGDPlus
    from pymoo.indicators.gd import GD
    from pymoo.indicators.gd_plus import GDPlus
    from pymoo.indicators.eps import EPS
    from pymoo.util.display import Display
    import numpy as np
    
    _EVERYTHINGMOOPY_AVAILABLE = True
except ImportError as e:
    _EVERYTHINGMOOPY_AVAILABLE = False
    _IMPORT_ERROR = str(e)
    
    # Create dummy classes for type hints
    class PymooProblem:
        pass
    class PymooAlgorithm:
        pass
    class PymooTermination:
        pass
    class PymooScatter:
        pass
    class PymooPCP:
        pass
    class PymooRadar:
        pass
    class PymooHeatmap:
        pass
    class HV:
        pass
    class IGD:
        pass
    class IGDPlus:
        pass
    class GD:
        pass
    class GDPlus:
        pass
    class EPS:
        pass


class EverythingMoopyConfig:
    """Configuration for EverythingMoopy integration."""
    
    def __init__(
        self,
        verbose: bool = True,
        save_history: bool = False,
        seed: Optional[int] = None,
        display: Optional[Any] = None
    ):
        self.verbose = verbose
        self.save_history = save_history
        self.seed = seed
        self.display = display


class EnergySystemOptimizationProblem(PymooProblem):
    """
    Wrapper class for defining energy system optimization problems using everythingmoopy.
    
    This class allows users to define custom optimization problems for energy systems
    while leveraging everythingmoopy's powerful optimization algorithms.
    """
    
    def __init__(
        self,
        objective_func: Callable,
        n_var: int,
        n_obj: int = 1,
        n_ieq_constr: int = 0,
        n_eq_constr: int = 0,
        xl: Optional[Union[float, np.ndarray]] = None,
        xu: Optional[Union[float, np.ndarray]] = None,
        constraint_func: Optional[Callable] = None,
        problem_name: str = "EnergySystemProblem"
    ):
        """
        Initialize an energy system optimization problem.
        
        Args:
            objective_func: Function that computes objectives given decision variables
            n_var: Number of decision variables
            n_obj: Number of objectives
            n_ieq_constr: Number of inequality constraints
            n_eq_constr: Number of equality constraints
            xl: Lower bounds for variables
            xu: Upper bounds for variables
            constraint_func: Function that computes constraints
            problem_name: Name of the problem
        """
        self.objective_func = objective_func
        self.constraint_func = constraint_func
        self.problem_name = problem_name
        
        if xl is None:
            xl = np.zeros(n_var)
        if xu is None:
            xu = np.ones(n_var)
        
        super().__init__(
            n_var=n_var,
            n_obj=n_obj,
            n_ieq_constr=n_ieq_constr,
            n_eq_constr=n_eq_constr,
            xl=xl,
            xu=xu
        )
    
    def _evaluate(self, X, out, *args, **kwargs):
        """Evaluate the problem for given solutions."""
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        # Compute objectives
        out["F"] = self.objective_func(X)
        
        # Compute constraints if provided
        if self.constraint_func is not None:
            out["G"] = self.constraint_func(X)


class PyXESXXNOptimizationProblem(PymooProblem):
    """
    Deep integration class for PyXESXXN OptimizationModel.
    
    This class converts a PyXESXXN OptimizationModel to a pymoo Problem,
    allowing direct optimization of PyXESXXN models using everythingmoopy algorithms.
    """
    
    def __init__(self, pyxesxxn_model: Any):
        """
        Initialize with a PyXESXXN OptimizationModel.
        
        Args:
            pyxesxxn_model: PyXESXXN OptimizationModel instance
        """
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        # Import PyXESXXN components here to avoid circular imports
        from .optimization import OptimizationModel, OptimizationVariable
        
        self.pyxesxxn_model = pyxesxxn_model
        self.optimization_config = pyxesxxn_model.config
        
        # Extract variables from PyXESXXN model
        self.variables = self.optimization_config.variables
        self.n_var = len(self.variables)
        
        # Determine number of objectives
        self.n_obj = 1  # Default to single objective
        if "multi_objective" in self.optimization_config.optimization_type.value.lower():
            self.n_obj = 2  # Default to 2 objectives for multi-objective
        
        # Extract bounds
        xl = []
        xu = []
        for var in self.variables:
            xl.append(var.lower_bound)
            xu.append(var.upper_bound if var.upper_bound is not None else np.inf)
        
        super().__init__(
            n_var=self.n_var,
            n_obj=self.n_obj,
            n_ieq_constr=len(self.optimization_config.constraints),
            n_eq_constr=0,
            xl=np.array(xl),
            xu=np.array(xu)
        )
    
    def _evaluate(self, X, out, *args, **kwargs):
        """
        Evaluate the PyXESXXN OptimizationModel for given solutions.
        
        Args:
            X: Decision variable values
            out: Dictionary to store outputs
        """
        # Prepare objective and constraint functions
        def objective_func(x):
            """Objective function wrapper for PyXESXXN model."""
            # Set variable values in PyXESXXN model
            for i, var in enumerate(self.variables):
                var.value = x[i]
            
            # Solve PyXESXXN model
            result = self.pyxesxxn_model.solve()
            
            # Return objective value (assuming minimization)
            return np.array([result.objective_value])
        
        def constraint_func(x):
            """Constraint function wrapper for PyXESXXN model."""
            # For now, we'll return dummy constraints
            # In a real implementation, we would parse and evaluate the constraint expressions
            return np.array([0.0] * len(self.optimization_config.constraints))
        
        # Compute objectives for all solutions
        F = np.zeros((X.shape[0], self.n_obj))
        G = np.zeros((X.shape[0], self.n_ieq_constr))
        
        for i, x in enumerate(X):
            F[i] = objective_func(x)
            if self.n_ieq_constr > 0:
                G[i] = constraint_func(x)
        
        out["F"] = F
        if self.n_ieq_constr > 0:
            out["G"] = G


class EverythingMoopyOptimizer:
    """
    Main optimizer class that provides a convenient interface to everythingmoopy.
    
    This class wraps everythingmoopy's optimization capabilities and provides
    energy system-specific convenience methods.
    """
    
    def __init__(self, config: Optional[EverythingMoopyConfig] = None):
        """
        Initialize the optimizer.
        
        Args:
            config: Configuration for the optimizer
        """
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        self.config = config or EverythingMoopyConfig()
    
    def minimize(
        self,
        problem: Union[PymooProblem, str],
        algorithm: Union[PymooAlgorithm, str],
        termination: Union[PymooTermination, tuple, str],
        **kwargs
    ) -> Any:
        """
        Minimize an optimization problem.
        
        Args:
            problem: Problem instance or problem name (for standard test problems)
            algorithm: Algorithm instance or algorithm name
            termination: Termination criterion
            **kwargs: Additional arguments passed to minimize
            
        Returns:
            Optimization result
        """
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        # Handle string inputs for convenience
        if isinstance(problem, str):
            problem = pymoo_get_problem(problem)
        
        if isinstance(algorithm, str):
            algorithm = self._get_algorithm_from_string(algorithm)
        
        if isinstance(termination, str):
            termination = pymoo_get_termination(termination)
        
        # Merge config with kwargs
        if self.config.verbose:
            kwargs.setdefault('verbose', True)
        if self.config.save_history:
            kwargs.setdefault('save_history', True)
        if self.config.seed is not None:
            kwargs.setdefault('seed', self.config.seed)
        if self.config.display is not None:
            kwargs.setdefault('display', self.config.display)
        
        # Run optimization
        result = pymoo_minimize(problem, algorithm, termination, **kwargs)
        return result
    
    def _get_algorithm_from_string(self, algorithm_name: str) -> PymooAlgorithm:
        """Get algorithm instance from string name."""
        algorithm_name = algorithm_name.lower()
        
        algorithms = {
            # Multi-objective algorithms
            'nsga2': NSGA2,
            'nsga3': NSGA3,
            'moead': MOEAD,
            'rvea': RVEA,
            'smsemoa': SMSEMOA,
            'age2': AGEMOEA2,
            # Single-objective algorithms
            'de': DE,
            'pso': PSO,
            'ga': GA,
            'cmaes': CMAES,
            'nelder': NelderMead,
            'pattern': PatternSearch
        }
        
        if algorithm_name not in algorithms:
            raise ValueError(
                f"Unknown algorithm: {algorithm_name}. "
                f"Available: {list(algorithms.keys())}"
            )
        
        return algorithms[algorithm_name]()
    
    def optimize_energy_system(
        self,
        objective_func: Callable,
        n_var: int,
        algorithm: Union[str, PymooAlgorithm] = 'nsga2',
        n_obj: int = 1,
        xl: Optional[Union[float, np.ndarray]] = None,
        xu: Optional[Union[float, np.ndarray]] = None,
        n_gen: int = 100,
        pop_size: int = 100,
        constraint_func: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """
        Optimize an energy system problem with convenience defaults.
        
        Args:
            objective_func: Function that computes objectives
            n_var: Number of decision variables
            algorithm: Algorithm name or instance
            n_obj: Number of objectives
            xl: Lower bounds
            xu: Upper bounds
            n_gen: Number of generations
            pop_size: Population size
            constraint_func: Constraint function
            **kwargs: Additional arguments
            
        Returns:
            Optimization result
        """
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        # Create problem
        problem = EnergySystemOptimizationProblem(
            objective_func=objective_func,
            n_var=n_var,
            n_obj=n_obj,
            xl=xl,
            xu=xu,
            constraint_func=constraint_func
        )
        
        # Get algorithm
        if isinstance(algorithm, str):
            algo_instance = self._get_algorithm_from_string(algorithm)
            if hasattr(algo_instance, 'pop_size'):
                algo_instance.pop_size = pop_size
        else:
            algo_instance = algorithm
        
        # Set termination
        termination = ('n_gen', n_gen)
        
        # Optimize
        result = self.minimize(problem, algo_instance, termination, **kwargs)
        return result
    
    def optimize_pyxesxxn_model(
        self,
        pyxesxxn_model: Any,
        algorithm: Union[str, PymooAlgorithm] = 'nsga2',
        n_gen: int = 100,
        pop_size: int = 100,
        **kwargs
    ) -> Any:
        """
        Optimize a PyXESXXN OptimizationModel using everythingmoopy.
        
        Args:
            pyxesxxn_model: PyXESXXN OptimizationModel instance to optimize
            algorithm: Algorithm name or instance
            n_gen: Number of generations
            pop_size: Population size
            **kwargs: Additional arguments
            
        Returns:
            Optimization result with PyXESXXN model integration
        """
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        # Create PyXESXXN optimization problem
        problem = PyXESXXNOptimizationProblem(pyxesxxn_model)
        
        # Get algorithm
        if isinstance(algorithm, str):
            algo_instance = self._get_algorithm_from_string(algorithm)
            if hasattr(algo_instance, 'pop_size'):
                algo_instance.pop_size = pop_size
        else:
            algo_instance = algorithm
        
        # Set termination
        termination = ('n_gen', n_gen)
        
        # Optimize
        result = self.minimize(problem, algo_instance, termination, **kwargs)
        
        # Set results back to PyXESXXN model
        if hasattr(result, 'X') and len(result.X) > 0:
            best_solution = result.X[0]
            for i, var in enumerate(problem.variables):
                var.value = best_solution[i]
        
        return result


class PerformanceIndicator:
    """Wrapper for performance indicators."""
    
    def __init__(self):
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
    
    def hypervolume(self, ref_point: np.ndarray) -> HV:
        """Calculate Hypervolume indicator."""
        return HV(ref_point=ref_point)
    
    def igd(self, pf: np.ndarray) -> IGD:
        """Calculate Inverted Generational Distance."""
        return IGD(pf)
    
    def igd_plus(self, pf: np.ndarray) -> IGDPlus:
        """Calculate Inverted Generational Distance Plus."""
        return IGDPlus(pf)
    
    def gd(self, pf: np.ndarray) -> GD:
        """Calculate Generational Distance."""
        return GD(pf)
    
    def gd_plus(self, pf: np.ndarray) -> GDPlus:
        """Calculate Generational Distance Plus."""
        return GDPlus(pf)
    
    def epsilon(self, pf: np.ndarray) -> EPS:
        """Calculate Epsilon indicator."""
        return EPS(pf)
    
    def calculate_all(self, F: np.ndarray, pf: np.ndarray, ref_point: np.ndarray) -> Dict[str, float]:
        """Calculate all performance indicators."""
        indicators = {
            'hypervolume': self.hypervolume(ref_point)(F),
            'igd': self.igd(pf)(F),
            'igd_plus': self.igd_plus(pf)(F),
            'gd': self.gd(pf)(F),
            'gd_plus': self.gd_plus(pf)(F),
            'epsilon': self.epsilon(pf)(F)
        }
        return indicators


class OptimizationVisualizer:
    """Wrapper for visualization tools."""
    
    def __init__(self):
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
    
    def scatter_plot(self) -> PymooScatter:
        """Create a scatter plot for Pareto front visualization."""
        return PymooScatter()
    
    def pcp_plot(self) -> PymooPCP:
        """Create a Parallel Coordinate Plot for solution visualization."""
        return PymooPCP()
    
    def radar_plot(self) -> PymooRadar:
        """Create a Radar Plot for solution comparison."""
        return PymooRadar()
    
    def heatmap_plot(self) -> PymooHeatmap:
        """Create a Heatmap for variable correlation analysis."""
        return PymooHeatmap()
    
    def plot_pareto_front(self, F: np.ndarray, title: str = "Pareto Front") -> None:
        """Plot the Pareto front."""
        plot = self.scatter_plot()
        plot.add(F)
        plot.title(title)
        plot.show()
    
    def plot_solution_comparison(self, F: np.ndarray, X: np.ndarray, title: str = "Solution Comparison") -> None:
        """Plot solution comparison using PCP."""
        plot = self.pcp_plot()
        plot.add(F)
        plot.title(title)
        plot.show()
    
    def plot_algorithm_comparison(self, results: Dict[str, Any], title: str = "Algorithm Comparison") -> None:
        """Plot comparison of multiple algorithms."""
        plot = self.scatter_plot()
        for name, result in results.items():
            if hasattr(result, 'F'):
                plot.add(result.F, label=name)
        plot.title(title)
        plot.legend()
        plot.show()


def check_everythingmoopy_available() -> bool:
    """Check if everythingmoopy is available."""
    return _EVERYTHINGMOOPY_AVAILABLE


def get_available_algorithms() -> List[str]:
    """Get list of available optimization algorithms."""
    if not _EVERYTHINGMOOPY_AVAILABLE:
        return []
    
    return [
        # Multi-objective algorithms
        'nsga2', 'nsga3', 'moead', 'rvea', 'smsemoa', 'age2',
        # Single-objective algorithms
        'de', 'pso', 'ga', 'cmaes', 'nelder', 'pattern'
    ]


def compare_algorithms(
    problem: Union[PymooProblem, str],
    algorithms: List[Union[str, PymooAlgorithm]],
    termination: Union[PymooTermination, tuple, str] = ('n_gen', 100),
    pop_size: int = 100,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Compare multiple algorithms on the same problem.
    
    Args:
        problem: Problem instance or problem name
        algorithms: List of algorithm names or instances
        termination: Termination criterion
        pop_size: Population size for all algorithms
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary of algorithm results
    """
    if not _EVERYTHINGMOOPY_AVAILABLE:
        raise ImportError(
            "EverythingMoopy is not available. "
            f"Import error: {_IMPORT_ERROR}"
        )
    
    results = {}
    optimizer = create_optimizer(seed=seed)
    
    for algo in algorithms:
        algo_name = algo if isinstance(algo, str) else algo.__class__.__name__
        print(f"Running {algo_name}...")
        
        if isinstance(algo, str):
            # Create algorithm instance with specified population size
            algo_instance = optimizer._get_algorithm_from_string(algo)
            if hasattr(algo_instance, 'pop_size'):
                algo_instance.pop_size = pop_size
        else:
            algo_instance = algo
        
        # Run optimization
        result = optimizer.minimize(problem, algo_instance, termination)
        results[algo_name] = result
    
    return results


def suggest_algorithm(problem_type: str, n_var: int, n_obj: int, has_constraints: bool) -> str:
    """
    Suggest an appropriate algorithm based on problem characteristics.
    
    Args:
        problem_type: Type of problem ('single' or 'multi')
        n_var: Number of variables
        n_obj: Number of objectives
        has_constraints: Whether the problem has constraints
        
    Returns:
        Suggested algorithm name
    """
    if problem_type == 'single':
        if n_var < 10:
            return 'nelder'  # Nelder-Mead for small dimensional problems
        elif n_var < 100:
            return 'de'      # Differential Evolution for medium dimensional problems
        else:
            return 'cmaes'   # CMA-ES for high dimensional problems
    else:
        if n_obj == 2:
            return 'nsga2'   # NSGA-II for 2-objective problems
        elif n_obj <= 10:
            return 'nsga3'   # NSGA-III for 3-10 objectives
        else:
            return 'moead'   # MOEA/D for many-objective problems


def get_available_problems() -> List[str]:
    """Get list of available standard test problems."""
    if not _EVERYTHINGMOOPY_AVAILABLE:
        return []
    
    return [
        'zdt1', 'zdt2', 'zdt3', 'zdt4', 'zdt5', 'zdt6',
        'dtlz1', 'dtlz2', 'dtlz3', 'dtlz4', 'dtlz5', 'dtlz6', 'dtlz7',
        'wfg1', 'wfg2', 'wfg3', 'wfg4', 'wfg5', 'wfg6', 'wfg7', 'wfg8', 'wfg9',
        'ackley', 'rastrigin', 'rosenbrock', 'griewank', 'sphere',
        'bnh', 'kursawe', 'osy', 'tnk', 'srn'
    ]


def create_optimizer(
    verbose: bool = True,
    save_history: bool = False,
    seed: Optional[int] = None
) -> EverythingMoopyOptimizer:
    """
    Create an EverythingMoopy optimizer with specified configuration.
    
    Args:
        verbose: Whether to print progress
        save_history: Whether to save optimization history
        seed: Random seed for reproducibility
        
    Returns:
        Configured EverythingMoopyOptimizer instance
    """
    config = EverythingMoopyConfig(
        verbose=verbose,
        save_history=save_history,
        seed=seed
    )
    return EverythingMoopyOptimizer(config)


def optimize_standard_problem(
    problem_name: str,
    algorithm: str = 'nsga2',
    n_gen: int = 100,
    pop_size: int = 100,
    verbose: bool = True,
    seed: Optional[int] = None
) -> Any:
    """
    Optimize a standard test problem.
    
    Args:
        problem_name: Name of the standard problem (e.g., 'zdt1', 'dtlz2')
        algorithm: Algorithm to use
        n_gen: Number of generations
        pop_size: Population size
        verbose: Whether to print progress
        seed: Random seed
        
    Returns:
        Optimization result
    """
    if not _EVERYTHINGMOOPY_AVAILABLE:
        raise ImportError(
            "EverythingMoopy is not available. "
            f"Import error: {_IMPORT_ERROR}"
        )
    
    optimizer = create_optimizer(verbose=verbose, seed=seed)
    result = optimizer.minimize(
        problem=problem_name,
        algorithm=algorithm,
        termination=('n_gen', n_gen)
    )
    
    if hasattr(result.algorithm, 'pop_size'):
        result.algorithm.pop_size = pop_size
    
    return result


class MultiCarrierEnergySystemProblem(PymooProblem):
    """
    Specialized problem class for multi-carrier energy system optimization.
    
    This class provides specific support for optimizing EnergyHubModel instances
    with multiple energy carriers (electricity, heat, hydrogen, etc.).
    """
    
    def __init__(self, energy_hub: Any, objectives: List[str] = ['cost']):
        """
        Initialize with an EnergyHubModel.
        
        Args:
            energy_hub: EnergyHubModel instance
            objectives: List of objectives to optimize (e.g., ['cost', 'emissions'])
        """
        if not _EVERYTHINGMOOPY_AVAILABLE:
            raise ImportError(
                "EverythingMoopy is not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        # Import MultiCarrier components here to avoid circular imports
        from .multi_carrier import EnergyHubModel
        
        self.energy_hub = energy_hub
        self.objectives = objectives
        self.n_obj = len(objectives)
        
        # Extract variables from EnergyHub
        self.input_carriers = self.energy_hub.config.input_carriers
        self.n_var = len(self.input_carriers)
        
        # Set bounds based on carrier properties
        xl = np.zeros(self.n_var)  # Minimum flow is 0
        xu = []
        for carrier in self.input_carriers:
            # Set upper bound based on carrier capacity or default to 100
            capacity = getattr(carrier, 'capacity', 100.0)
            xu.append(capacity)
        
        super().__init__(
            n_var=self.n_var,
            n_obj=self.n_obj,
            n_ieq_constr=0,
            n_eq_constr=0,
            xl=np.array(xl),
            xu=np.array(xu)
        )
    
    def _evaluate(self, X, out, *args, **kwargs):
        """
        Evaluate the multi-carrier energy system for given solutions.
        
        Args:
            X: Input flow rates for each carrier
            out: Dictionary to store outputs
        """
        F = np.zeros((X.shape[0], self.n_obj))
        
        for i, x in enumerate(X):
            # Set input flows
            for j, carrier in enumerate(self.input_carriers):
                self.energy_hub.set_input_flow(carrier, x[j])
            
            # Calculate conversion
            output_flows = self.energy_hub.calculate_conversion()
            
            # Calculate objectives
            obj_values = []
            for obj in self.objectives:
                if obj == 'cost':
                    # Calculate total cost
                    total_cost = 0.0
                    for j, carrier in enumerate(self.input_carriers):
                        cost = getattr(carrier, 'cost', 0.0)
                        total_cost += x[j] * cost
                    obj_values.append(total_cost)
                elif obj == 'emissions':
                    # Calculate total emissions
                    total_emissions = 0.0
                    for j, carrier in enumerate(self.input_carriers):
                        emission_factor = getattr(carrier, 'emission_factor', 0.0)
                        total_emissions += x[j] * emission_factor
                    obj_values.append(total_emissions)
                elif obj == 'efficiency':
                    # Calculate overall efficiency
                    total_input = np.sum(x)
                    total_output = np.sum(list(output_flows.values()))
                    efficiency = total_output / total_input if total_input > 0 else 0.0
                    obj_values.append(1.0 - efficiency)  # Minimize (1 - efficiency) to maximize efficiency
            
            F[i] = np.array(obj_values)
        
        out["F"] = F


def optimize_energy_hub(
    energy_hub: Any,
    objectives: List[str] = ['cost'],
    algorithm: str = 'nsga2',
    n_gen: int = 100,
    pop_size: int = 100,
    seed: Optional[int] = None
) -> Any:
    """
    Optimize an EnergyHubModel using everythingmoopy.
    
    Args:
        energy_hub: EnergyHubModel instance to optimize
        objectives: List of objectives to optimize
        algorithm: Algorithm name or instance
        n_gen: Number of generations
        pop_size: Population size
        seed: Random seed
        
    Returns:
        Optimization result
    """
    if not _EVERYTHINGMOOPY_AVAILABLE:
        raise ImportError(
            "EverythingMoopy is not available. "
            f"Import error: {_IMPORT_ERROR}"
        )
    
    # Create multi-carrier problem
    problem = MultiCarrierEnergySystemProblem(energy_hub, objectives)
    
    # Create optimizer
    optimizer = create_optimizer(seed=seed)
    
    # Run optimization
    result = optimizer.minimize(
        problem=problem,
        algorithm=algorithm,
        termination=('n_gen', n_gen),
        pop_size=pop_size
    )
    
    # Set results back to energy hub
    if hasattr(result, 'X') and len(result.X) > 0:
        best_solution = result.X[0]
        for i, carrier in enumerate(problem.input_carriers):
            energy_hub.set_input_flow(carrier, best_solution[i])
    
    return result


__all__ = [
    'check_everythingmoopy_available',
    'get_available_algorithms',
    'get_available_problems',
    'create_optimizer',
    'optimize_standard_problem',
    'compare_algorithms',
    'suggest_algorithm',
    'optimize_energy_hub',
    'EverythingMoopyConfig',
    'EverythingMoopyOptimizer',
    'EnergySystemOptimizationProblem',
    'PyXESXXNOptimizationProblem',
    'MultiCarrierEnergySystemProblem',
    'PerformanceIndicator',
    'OptimizationVisualizer',
    '_EVERYTHINGMOOPY_AVAILABLE'
]
