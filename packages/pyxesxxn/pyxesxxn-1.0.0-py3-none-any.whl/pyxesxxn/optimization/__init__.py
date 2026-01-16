# SPDX-FileCopyrightText: PyXESXXN Contributors
#
# SPDX-License-Identifier: MIT

"""PyXESXXN Optimization Module - Independent Energy System Optimization

This module provides completely independent optimization functionality for PyXESXXN,
replacing PyPSA dependencies with native PyXESXXN optimization components.
"""

from .abstract import (
    OptimizationType,
    SolverType,
    OptimizationConfig,
    OptimizationVariable,
    OptimizationConstraint,
    Optimizer,
    LinearOptimizer,
    NonlinearOptimizer,
    MultiObjectiveOptimizer,
    StochasticOptimizer,
    OptimizationFactory,
    create_optimization_config,
    validate_optimization_problem,
    get_default_optimization_factory
)

from .regularized_decomposition import (
    RegularizedDecompositionOptimizer,
    UncertaintyType,
    RegularizationParams,
    MarkovState,
    CuttingPlane,
    ValueFunctionApproximator,
    CuttingPlaneApproximator,
    create_regularized_decomposition_optimizer
)

from .wemsco import (
    WEMSCOOptimizer,
    WEMSCOOptimizationType,
    UncertaintySide,
    WassersteinParams,
    FastInnerConvexApproxParams,
    AdversarialParams,
    WassersteinEnhancedCuttingPlaneApproximator,
    create_wemsco_optimizer,
    create_wasserstein_enhanced_optimizer
)

from .strong_duality import (
    StrongDualityOptimizer,
    DualVariables,
    UncertaintySet,
    EquipmentParameters,
    MainProblem,
    SubProblem,
    HierarchicalStrongDualityOptimizer,
    create_strong_duality_optimizer
)

__all__ = [
    "OptimizationType",
    "SolverType",
    "OptimizationConfig",
    "OptimizationVariable",
    "OptimizationConstraint",
    "Optimizer",
    "LinearOptimizer",
    "NonlinearOptimizer",
    "MultiObjectiveOptimizer",
    "StochasticOptimizer",
    "OptimizationFactory",
    "create_optimization_config",
    "validate_optimization_problem",
    "get_default_optimization_factory",
    "RegularizedDecompositionOptimizer",
    "UncertaintyType",
    "RegularizationParams",
    "MarkovState",
    "CuttingPlane",
    "ValueFunctionApproximator",
    "CuttingPlaneApproximator",
    "create_regularized_decomposition_optimizer",
    "WEMSCOOptimizer",
    "WEMSCOOptimizationType",
    "UncertaintySide",
    "WassersteinParams",
    "FastInnerConvexApproxParams",
    "AdversarialParams",
    "WassersteinEnhancedCuttingPlaneApproximator",
    "create_wemsco_optimizer",
    "create_wasserstein_enhanced_optimizer",
    "StrongDualityOptimizer",
    "DualVariables",
    "UncertaintySet",
    "EquipmentParameters",
    "MainProblem",
    "SubProblem",
    "HierarchicalStrongDualityOptimizer",
    "create_strong_duality_optimizer"
]

# Version information
__version__ = "2.0.0"
__author__ = "PyXESXXN Development Team"
__description__ = "Independent optimization module for PyXESXXN energy system modeling"
