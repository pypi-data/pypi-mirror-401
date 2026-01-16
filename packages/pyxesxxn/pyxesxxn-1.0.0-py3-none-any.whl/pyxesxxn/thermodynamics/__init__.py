"""Thermodynamics module for PyXESXXN.

Provides thermodynamic calculations for energy system components including:
- Gas compression calculations
- Heat transfer calculations
- Chemical reaction thermodynamics
- Fluid properties
"""

from .base import (
    ThermodynamicModel,
    IdealGasModel,
    RealGasModel,
    CompressionCalculator,
    GasProperties
)

from .constants import (
    GAS_CONSTANTS,
    SPECIFIC_HEAT_RATIOS,
    MOLAR_MASSES,
    CRITICAL_TEMPERATURES,
    CRITICAL_PRESSURES,
    STANDARD_TEMPERATURE,
    STANDARD_PRESSURE,
    BAR_TO_PA,
    PSI_TO_PA,
    ATM_TO_PA,
    WATER_SPECIFIC_HEAT,
    WATER_LATENT_HEAT_VAPORIZATION,
    WATER_LATENT_HEAT_FUSION
)

from .exceptions import (
    ThermodynamicError,
    GasPropertyError,
    ModelNotAvailableError,
    InvalidConditionError,
    ConvergenceError,
    ConfigurationError
)

__all__ = [
    # Base classes
    "ThermodynamicModel",
    "IdealGasModel",
    "RealGasModel",
    "CompressionCalculator",
    "GasProperties",
    
    # Constants
    "GAS_CONSTANTS",
    "SPECIFIC_HEAT_RATIOS",
    "MOLAR_MASSES",
    "CRITICAL_TEMPERATURES",
    "CRITICAL_PRESSURES",
    "STANDARD_TEMPERATURE",
    "STANDARD_PRESSURE",
    "BAR_TO_PA",
    "PSI_TO_PA",
    "ATM_TO_PA",
    "WATER_SPECIFIC_HEAT",
    "WATER_LATENT_HEAT_VAPORIZATION",
    "WATER_LATENT_HEAT_FUSION",
    
    # Exceptions
    "ThermodynamicError",
    "GasPropertyError",
    "ModelNotAvailableError",
    "InvalidConditionError",
    "ConvergenceError",
    "ConfigurationError",
]