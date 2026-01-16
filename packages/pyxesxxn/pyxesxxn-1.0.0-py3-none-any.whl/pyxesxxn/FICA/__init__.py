"""
FICA (Faster Inner Convex Approximation) Module

This module provides implementations for faster inner convex approximation
of chance constrained grid dispatch with decision-coupled uncertainty.

Main Components:
- PD (Power Dispatch): Chance-constrained power dispatch problem solver
- WTErrorGenerator: Wind turbine forecasting error scenario generator

Reference:
Yihong Zhou, Hanbin Yang, Thomas Morstyn (2025).
FICA: Faster Inner Convex Approximation of Chance Constrained Grid Dispatch with Decision-Coupled Uncertainty.
Available at arXiv https://arxiv.org/abs/2506.18806.
"""

from .pd import (
    solve_PD,
    check_JCC,
    dual_norm_constr,
    dual_norm_constr_exact_method
)

from .wt_error_gen import (
    WT_sce_gen,
    generate_wind_error_scenarios
)

__all__ = [
    # Power Dispatch module
    "solve_PD",
    "check_JCC",
    "dual_norm_constr",
    "dual_norm_constr_exact_method",
    
    # Wind Error Generator
    "WT_sce_gen",
    "generate_wind_error_scenarios",
]
