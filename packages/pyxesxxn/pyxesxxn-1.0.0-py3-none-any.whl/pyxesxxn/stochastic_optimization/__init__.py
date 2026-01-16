"""
Stochastic Optimization Module

This module provides a unified interface for stochastic optimization algorithms
in PyXESXXN, including SFLA and FICA methods for chance-constrained optimization.

Main Features:
- SFLA: Strengthened and Faster Linear Approximation for joint chance constraints
- FICA: Faster Inner Convex Approximation for decision-coupled uncertainty
- Unified API for chance-constrained optimization problems
"""

from .sfla_wrapper import SFLAWrapper, SFLAConfig
from .fica_wrapper import FICAWrapper, FICAConfig
from .base import (
    StochasticOptimizer,
    ChanceConstraintConfig,
    OptimizationResult
)

__all__ = [
    # Base classes
    "StochasticOptimizer",
    "ChanceConstraintConfig",
    "OptimizationResult",
    
    # SFLA
    "SFLAWrapper",
    "SFLAConfig",
    
    # FICA
    "FICAWrapper",
    "FICAConfig",
]
