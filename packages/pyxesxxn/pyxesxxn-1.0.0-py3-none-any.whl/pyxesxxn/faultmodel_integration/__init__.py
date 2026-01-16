"""PyXESXXN Fault Model Integration Module.

This module integrates the NASA Prognostics Python Package (ProgPy) into PyXESXXN,
providing advanced prognostics and health management capabilities for engineering systems.
"""

from .faultmodel_wrapper import (
    FaultModelConfig,
    FaultModelWrapper,
    PrognosticsModel,
    check_faultmodel_available,
    get_faultmodel_version,
    _FAULTMODEL_AVAILABLE
)

try:
    from .faultmodel_wrapper import StateEstimator
except ImportError:
    StateEstimator = None

try:
    from .faultmodel_wrapper import Predictor
except ImportError:
    Predictor = None

try:
    from .faultmodel_wrapper import UncertainData
except ImportError:
    UncertainData = None

from .electric_machinery import (
    ElectricMachineryModel,
    ElectricMachineryConfig,
    ElectricMachineryState,
    ElectricMachineryFaultPredictor,
    ElectricMachineryStateEstimator,
    ElectricMachineryHealthAssessor,
    ElectricExcavatorModel,
    ElectricCraneModel,
    ElectricLoaderModel,
    ElectricForkliftModel,
    MachineryType,
    ComponentType,
    FaultMode
)

__all__ = [
    "FaultModelConfig",
    "FaultModelWrapper",
    "PrognosticsModel",
    "StateEstimator",
    "Predictor",
    "UncertainData",
    "check_faultmodel_available",
    "get_faultmodel_version",
    "_FAULTMODEL_AVAILABLE",
    "ElectricMachineryModel",
    "ElectricMachineryConfig",
    "ElectricMachineryState",
    "ElectricMachineryFaultPredictor",
    "ElectricMachineryStateEstimator",
    "ElectricMachineryHealthAssessor",
    "ElectricExcavatorModel",
    "ElectricCraneModel",
    "ElectricLoaderModel",
    "ElectricForkliftModel",
    "MachineryType",
    "ComponentType",
    "FaultMode"
]
