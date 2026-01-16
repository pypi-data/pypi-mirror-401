"""
SFLA (Strengthened and Faster Linear Approximation) Module

This module provides implementations for strengthened and faster linear approximation
to joint chance constraints with Wasserstein ambiguity.

Main Components:
- SUC (Stochastic Unit Commitment): Chance-constrained unit commitment problem solver
- BilevelStorage: Bilevel strategic bidding problem solver with storage
- WTErrorGenerator: Wind turbine forecasting error scenario generator

Reference:
Yihong Zhou, Yuxin Xia, Hanbin Yang, Thomas Morstyn (2024).
Strengthened and Faster Linear Approximation to Joint Chance Constraints with Wasserstein Ambiguity.
"""

from .suc import (
    solve_stochastic_unit_commitment,
    solve_VaR,
    solve_all_VaR,
    linearize_complementarity
)

from .bilevel_storage import (
    solve_bilevel_storage,
    market_clear_exact_JCC
)

from .wt_error_gen import (
    WT_sce_gen,
    generate_wind_error_scenarios
)

__all__ = [
    # SUC module
    "solve_stochastic_unit_commitment",
    "solve_VaR",
    "solve_all_VaR",
    "linearize_complementarity",
    
    # Bilevel Storage module
    "solve_bilevel_storage",
    "market_clear_exact_JCC",
    
    # Wind Error Generator
    "WT_sce_gen",
    "generate_wind_error_scenarios",
]
