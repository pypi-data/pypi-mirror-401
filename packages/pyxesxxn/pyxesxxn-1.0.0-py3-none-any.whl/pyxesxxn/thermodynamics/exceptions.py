"""Custom exceptions for thermodynamics module."""

from ..exceptions import PyXESXXNError, CalculationError


class ThermodynamicError(CalculationError):
    """Base exception for thermodynamic calculations."""
    pass


class GasPropertyError(ThermodynamicError):
    """Exception for gas property errors."""
    
    def __init__(self, gas_type: str, message: str = ""):
        self.gas_type = gas_type
        if not message:
            message = f"Invalid gas properties for gas type: {gas_type}"
        super().__init__(message)


class ModelNotAvailableError(ThermodynamicError):
    """Exception when a thermodynamic model is not available."""
    
    def __init__(self, model_name: str, message: str = ""):
        self.model_name = model_name
        if not message:
            message = f"Thermodynamic model '{model_name}' is not available. " \
                     f"Install required dependencies (CoolProp/REFPROP)."
        super().__init__(message)


class InvalidConditionError(ThermodynamicError):
    """Exception for invalid thermodynamic conditions."""
    
    def __init__(self, condition: str, value: float, valid_range: str = ""):
        self.condition = condition
        self.value = value
        message = f"Invalid {condition}: {value}"
        if valid_range:
            message += f". Valid range: {valid_range}"
        super().__init__(message)


class ConvergenceError(ThermodynamicError):
    """Exception when thermodynamic calculation fails to converge."""
    
    def __init__(self, calculation_type: str, max_iterations: int = 100):
        self.calculation_type = calculation_type
        self.max_iterations = max_iterations
        message = f"{calculation_type} calculation failed to converge " \
                 f"after {max_iterations} iterations."
        super().__init__(message)


class ConfigurationError(ThermodynamicError):
    """Exception for configuration errors in thermodynamic models."""
    
    def __init__(self, parameter: str, value: str, reason: str = ""):
        self.parameter = parameter
        self.value = value
        message = f"Invalid configuration for {parameter}: {value}"
        if reason:
            message += f". Reason: {reason}"
        super().__init__(message)