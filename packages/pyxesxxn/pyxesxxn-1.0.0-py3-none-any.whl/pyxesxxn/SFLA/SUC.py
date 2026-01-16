"""
SUC (Stochastic Unit Commitment) Module Wrapper

This module wraps the SFLA SUC implementation for integration with PyXESXXN.
"""

try:
    from ..SFLA.SUC import solve_stochastic_unit_commitment, solve_VaR, solve_all_VaR, linearize_complementarity
    __all__ = [
        "solve_stochastic_unit_commitment",
        "solve_VaR",
        "solve_all_VaR",
        "linearize_complementarity"
    ]
except ImportError:
    __all__ = []
    pass
