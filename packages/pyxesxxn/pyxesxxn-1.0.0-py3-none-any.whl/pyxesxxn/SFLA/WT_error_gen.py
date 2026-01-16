"""
Wind Error Generator Module Wrapper

This module wraps the wind turbine error scenario generator for integration with PyXESXXN.
"""

try:
    from ..SFLA.WT_error_gen import WT_sce_gen
    generate_wind_error_scenarios = WT_sce_gen
    __all__ = [
        "WT_sce_gen",
        "generate_wind_error_scenarios"
    ]
except ImportError:
    __all__ = []
    pass
