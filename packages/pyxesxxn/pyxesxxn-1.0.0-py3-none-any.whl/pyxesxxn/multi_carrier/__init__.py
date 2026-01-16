"""
PyXESXXN Multi-Carrier Energy System Optimization Module

This module provides a completely independent implementation of multi-carrier
energy system optimization, replacing PyPSA dependencies with native PyXESXXN components.

Features:
- Independent multi-carrier energy system modeling
- Advanced optimization algorithms for energy hubs
- Cross-carrier conversion devices (electrolyzers, fuel cells, heat pumps, etc.)
- Renewable energy integration across multiple carriers
- Scenario-based optimization and analysis
- Fully independent architecture (no PyPSA dependency)
- Reinforcement learning and multi-objective optimization for energy scheduling

Key Components:
- MultiCarrierConverter: Base converter classes for different energy carriers
- EnergyHubModel: Modeling and optimization of energy hubs
- HubConfiguration: Configuration management for energy hubs
- OptimizationModel: Advanced optimization framework
- Energy RLMOGP: Reinforcement learning and multi-objective genetic algorithm for energy system optimization
"""

from .abstract import (
    MultiCarrierConverter,
    EnergyCarrier,
    ConverterType,
    ConverterConfig,
    EnergyFlow,
    HubConfiguration
)

from ..network import ComponentConfig

from .pyxesxxn_impl import (
    PyXESXXNConverter,
    PyXESXXNElectrolyzer as ElectrolyzerConverter,
    PyXESXXNFuelCell as FuelCellConverter,
    PyXESXXNHeatPump as HeatPumpConverter,
    PyXESXXNEnergyHub as EnergyHubModel,
    PyXESXXNOptimizationModel as OptimizationModel
)

from .RLMOGP import (
    # 多目标优化核心函数
    dominates,
    update_pareto_front,
    calculate_crowding_distance,
    select_nondominated_solutions,
    
    # 能源系统环境模型
    EnergySystemEnvironment,
    TaskGenerator,
    
    # 并行优化算法
    ParallelHeuristics,
    
    # 自适应树状遗传-差分架构
    AdaptiveTreeGP,
    
    # 强化学习智能体
    MachineAgent,
    
    # 多智能体调度器
    MultiAgentTaskScheduler
)

from .MOMTHRO import (
    # MOMTHRO多目标优化算法
    MOMTHROOptimizer,
    
    # 核心优化函数
    non_dominated_sort,
    crowding_distance,
    calculate_hypervolume,
    
    # 进化算法操作
    lhsdesign_modified,
    tournament_selection,
    simulated_binary_crossover,
    polynomial_mutation,
    adaptive_parameters
)

__all__ = [
    # Base classes and enums
    'MultiCarrierConverter',
    'EnergyCarrier',
    'ConverterType',
    'ConverterConfig',
    
    # Converters
    'ElectrolyzerConverter',
    'FuelCellConverter',
    'HeatPumpConverter',
    
    # Energy hubs and optimization
    'EnergyHubModel',
    'HubConfiguration',
    'OptimizationModel',
    'EnergyFlow',
    
    # Energy RLMOGP optimization
    'dominates',
    'update_pareto_front',
    'calculate_crowding_distance',
    'select_nondominated_solutions',
    'EnergySystemEnvironment',
    'TaskGenerator',
    'ParallelHeuristics',
    'AdaptiveTreeGP',
    'MachineAgent',
    'MultiAgentTaskScheduler',
    
    # MOMTHRO multi-objective optimization
    'MOMTHROOptimizer',
    'non_dominated_sort',
    'crowding_distance',
    'calculate_hypervolume',
    'lhsdesign_modified',
    'tournament_selection',
    'simulated_binary_crossover',
    'polynomial_mutation',
    'adaptive_parameters'
]

# Version information
__version__ = "2.0.0"
__author__ = "PyXESXXN Development Team"

# Default configuration for PyXESXXN multi-carrier systems
DEFAULT_CONFIG = {
    "solver": "glpk",  # Open-source solver by default
    "time_periods": 8760,  # Annual simulation
    "carrier_conversion_efficiency": {
        "electrolyzer": 0.70,  # 70% efficiency
        "fuel_cell": 0.60,     # 60% efficiency
        "heat_pump": 3.5,      # COP of 3.5
        "chp": 0.85,           # 85% overall efficiency
        "boiler": 0.90         # 90% efficiency
    },
    "storage_parameters": {
        "battery": {"self_discharge": 0.01, "efficiency": 0.95},
        "hydrogen": {"self_discharge": 0.001, "efficiency": 0.90},
        "thermal": {"self_discharge": 0.05, "efficiency": 0.98}
    },
    "renewable_parameters": {
        "solar_pv": {"capacity_factor": 0.20, "curtailment_limit": 0.05},
        "wind": {"capacity_factor": 0.35, "curtailment_limit": 0.03},
        "hydro": {"capacity_factor": 0.50, "curtailment_limit": 0.01}
    },
    "optimization_settings": {
        "objective": "minimize_cost",
        "time_horizon": 24,
        "constraint_tolerance": 1e-6,
        "max_iterations": 1000,
        "multi_objective_algorithm": "MOMTHRO"  # Set MOMTHRO as default multi-objective algorithm
    },
    "multi_objective_parameters": {
        "algorithm": "MOMTHRO",
        "population_size": 100,
        "max_iterations": 200,
        "crossover_probability": 0.9,
        "mutation_probability": 0.1,
        "reference_point": None  # Auto-calculated if not specified
    }
}