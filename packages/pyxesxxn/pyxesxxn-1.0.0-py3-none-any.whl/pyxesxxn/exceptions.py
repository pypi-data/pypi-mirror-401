"""Custom exception hierarchy for PyXESXXN library.

This module defines a comprehensive exception hierarchy for the PyXESXXN library,
providing clear, actionable error messages and structured error handling.
"""

from typing import Any, Optional


class PyXESXXNError(Exception):
    """Base exception class for all PyXESXXN errors.
    
    All custom exceptions in PyXESXXN should inherit from this class.
    This provides a consistent way to catch PyXESXXN-specific errors.
    """
    
    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        """Initialize the PyXESXXNError.
        
        Parameters
        ----------
        message : str
            Human-readable error message.
        details : Optional[Any], default=None
            Additional error details for debugging.
        """
        self.message = message
        self.details = details
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format the error message with optional details."""
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message
    
    def __str__(self) -> str:
        return self._format_message()


class ConfigurationError(PyXESXXNError):
    """Exception raised for configuration-related errors.
    
    This includes:
    - Invalid configuration parameters
    - Missing required configuration
    - Configuration file parsing errors
    - Inconsistent configuration values
    """
    pass


class CalculationError(PyXESXXNError):
    """Exception raised for calculation-related errors.
    
    This includes:
    - Numerical calculation failures
    - Convergence issues in iterative methods
    - Invalid input values for calculations
    - Thermodynamic property calculation errors
    """
    pass





class OptimizationError(PyXESXXNError):
    """Exception raised for optimization-related errors.
    
    This includes:
    - Optimization solver failures
    - Infeasible optimization problems
    - Convergence issues in optimization algorithms
    - Invalid optimization constraints or objectives
    """
    pass


class ValidationError(PyXESXXNError):
    """Exception raised for data validation errors.
    
    This includes:
    - Invalid input data formats
    - Data type mismatches
    - Value range violations
    - Missing required data fields
    """
    pass


class ConvergenceError(CalculationError):
    """Exception raised when numerical methods fail to converge.
    
    This includes:
    - Iterative solvers not converging within maximum iterations
    - Numerical instability in calculations
    - Divergence in iterative processes
    """
    pass


class InputError(PyXESXXNError):
    """Exception raised for invalid user input.
    
    This includes:
    - Invalid function arguments
    - Missing required arguments
    - Argument type mismatches
    - Argument value violations
    """
    pass


class FileError(PyXESXXNError):
    """Exception raised for file-related errors.
    
    This includes:
    - File not found
    - Permission denied
    - Invalid file format
    - File parsing errors
    """
    pass


class DependencyError(PyXESXXNError):
    """Exception raised for missing or incompatible dependencies.
    
    This includes:
    - Missing required packages
    - Incompatible package versions
    - Failed imports of optional dependencies
    """
    pass


class NotImplementedFeatureError(PyXESXXNError):
    """Exception raised for features that are not yet implemented.
    
    This provides clear feedback to users about planned but not yet
    available functionality.
    """
    pass


class WarningManager:
    """Manager for issuing warnings in PyXESXXN.
    
    This class provides a consistent way to issue warnings with
    appropriate categories and formatting.
    """
    
    @staticmethod
    def warn_deprecated(feature: str, version: str, alternative: str = None) -> None:
        """Issue a deprecation warning.
        
        Parameters
        ----------
        feature : str
            Name of the deprecated feature.
        version : str
            Version in which the feature will be removed.
        alternative : str, optional
            Alternative feature to use instead.
        """
        import warnings
        
        message = f"'{feature}' is deprecated and will be removed in version {version}."
        if alternative:
            message += f" Use '{alternative}' instead."
        
        warnings.warn(message, DeprecationWarning, stacklevel=2)
    
    @staticmethod
    def warn_experimental(feature: str) -> None:
        """Issue an experimental feature warning.
        
        Parameters
        ----------
        feature : str
            Name of the experimental feature.
        """
        import warnings
        
        message = f"'{feature}' is experimental and may change in future releases."
        warnings.warn(message, FutureWarning, stacklevel=2)
    
    @staticmethod
    def warn_performance(feature: str, suggestion: str = None) -> None:
        """Issue a performance warning.
        
        Parameters
        ----------
        feature : str
            Name of the feature with performance implications.
        suggestion : str, optional
            Suggestion for improving performance.
        """
        import warnings
        
        message = f"'{feature}' may have performance implications."
        if suggestion:
            message += f" {suggestion}"
        
        warnings.warn(message, RuntimeWarning, stacklevel=2)


# Convenience functions for common error patterns
def raise_config_error(message: str, param: str = None, value: Any = None) -> None:
    """Raise a ConfigurationError with formatted message.
    
    Parameters
    ----------
    message : str
        Base error message.
    param : str, optional
        Name of the problematic parameter.
    value : Any, optional
        Value that caused the error.
    """
    details = {}
    if param:
        details["parameter"] = param
    if value is not None:
        details["value"] = value
    
    raise ConfigurationError(message, details if details else None)


def raise_calculation_error(message: str, calculation_type: str = None, 
                           inputs: dict = None) -> None:
    """Raise a CalculationError with formatted message.
    
    Parameters
    ----------
    message : str
        Base error message.
    calculation_type : str, optional
        Type of calculation that failed.
    inputs : dict, optional
        Input values that caused the error.
    """
    details = {}
    if calculation_type:
        details["calculation_type"] = calculation_type
    if inputs:
        details["inputs"] = inputs
    
    raise CalculationError(message, details if details else None)


def raise_validation_error(message: str, field: str = None, 
                          expected: Any = None, actual: Any = None) -> None:
    """Raise a ValidationError with formatted message.
    
    Parameters
    ----------
    message : str
        Base error message.
    field : str, optional
        Name of the field that failed validation.
    expected : Any, optional
        Expected value or constraint.
    actual : Any, optional
        Actual value that failed validation.
    """
    details = {}
    if field:
        details["field"] = field
    if expected is not None:
        details["expected"] = expected
    if actual is not None:
        details["actual"] = actual
    
    raise ValidationError(message, details if details else None)
