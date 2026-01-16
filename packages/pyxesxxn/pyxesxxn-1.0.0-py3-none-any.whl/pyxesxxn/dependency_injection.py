"""
Dependency Injection Container for PyXESXXN.

This module provides a dependency injection container that allows for loose coupling
between PyXESXXN modules and facilitates testing by enabling easy mocking of dependencies.
"""

from __future__ import annotations

from typing import Dict, Type, Any, Callable, Optional, Union
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class ServiceProvider(ABC):
    """Abstract base class for service providers."""
    
    @abstractmethod
    def get_service(self, service_type: Type) -> Any:
        """Get a service instance of the specified type."""
        pass
    
    @abstractmethod
    def register_service(self, service_type: Type, implementation: Union[Type, Callable]) -> None:
        """Register a service implementation."""
        pass


class DependencyInjectionContainer(ServiceProvider):
    """Simple dependency injection container for PyXESXXN."""
    
    def __init__(self):
        self._services: Dict[Type, Union[Type, Callable]] = {}
        self._instances: Dict[Type, Any] = {}
        self._singletons: Dict[Type, bool] = {}
    
    def register_service(self, service_type: Type, 
                         implementation: Union[Type, Callable], 
                         singleton: bool = True) -> None:
        """Register a service implementation.
        
        Args:
            service_type: The interface or abstract class type
            implementation: The concrete implementation class or factory function
            singleton: Whether to create a single instance (True) or new instance each time (False)
        """
        self._services[service_type] = implementation
        self._singletons[service_type] = singleton
        logger.debug(f"Registered service: {service_type.__name__} -> {implementation.__name__}")
    
    def get_service(self, service_type: Type) -> Any:
        """Get a service instance of the specified type."""
        if service_type not in self._services:
            raise KeyError(f"Service {service_type.__name__} not registered")
        
        # Return existing singleton instance if available
        if self._singletons[service_type] and service_type in self._instances:
            return self._instances[service_type]
        
        # Create new instance
        implementation = self._services[service_type]
        
        if callable(implementation) and not isinstance(implementation, type):
            # Factory function
            instance = implementation()
        else:
            # Class - create instance with dependency injection
            instance = self._create_instance(implementation)
        
        # Store singleton instance
        if self._singletons[service_type]:
            self._instances[service_type] = instance
        
        return instance
    
    def _create_instance(self, implementation: Type) -> Any:
        """Create an instance of a class with dependency injection."""
        # Get the constructor signature
        import inspect
        signature = inspect.signature(implementation.__init__)
        
        # Prepare arguments
        args = {}
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue
            
            # Check if parameter has a type annotation
            if param.annotation != inspect.Parameter.empty:
                try:
                    args[param_name] = self.get_service(param.annotation)
                except KeyError:
                    # Service not registered, use default value if available
                    if param.default != inspect.Parameter.empty:
                        args[param_name] = param.default
                    else:
                        raise ValueError(
                            f"Cannot resolve dependency {param_name} of type {param.annotation.__name__} "
                            f"for {implementation.__name__}"
                        )
            else:
                # No type annotation, use default value
                if param.default != inspect.Parameter.empty:
                    args[param_name] = param.default
                else:
                    raise ValueError(
                        f"Cannot resolve dependency {param_name} for {implementation.__name__} "
                        f"(no type annotation)"
                    )
        
        return implementation(**args)
    
    def clear_instances(self) -> None:
        """Clear all cached instances (useful for testing)."""
        self._instances.clear()
        logger.debug("Cleared all service instances")


# Global dependency injection container
_container: Optional[DependencyInjectionContainer] = None


def get_container() -> DependencyInjectionContainer:
    """Get the global dependency injection container."""
    global _container
    if _container is None:
        _container = DependencyInjectionContainer()
        _setup_default_services(_container)
    return _container


def set_container(container: DependencyInjectionContainer) -> None:
    """Set the global dependency injection container."""
    global _container
    _container = container


def reset_container() -> None:
    """Reset the global dependency injection container."""
    global _container
    _container = None


def _setup_default_services(container: DependencyInjectionContainer) -> None:
    """Setup default service registrations for PyXESXXN."""
    # Import modules to avoid circular imports
    from .multi_carrier.abstract import (
        MultiCarrierConverter, EnergyHubInterface, OptimizationInterface
    )
    from .multi_carrier.pyxesxxn_impl import (
        PyXESXXNMultiCarrierConverter, PyXESXXNEnergyHubModel, PyXESXXNOptimizationModel
    )
    from .optimization.abstract import (
        Optimizer, LinearOptimizer, NonlinearOptimizer, MultiObjectiveOptimizer
    )
    from .optimization.pyxesxxn_impl import (
        PyXESXXNOptimizer, PyXESXXNLinearOptimizer, PyXESXXNNonlinearOptimizer, 
        PyXESXXNMultiObjectiveOptimizer
    )
    
    # Register multi-carrier services
    container.register_service(MultiCarrierConverter, PyXESXXNMultiCarrierConverter)
    container.register_service(EnergyHubInterface, PyXESXXNEnergyHubModel)
    container.register_service(OptimizationInterface, PyXESXXNOptimizationModel)
    
    # Register optimization services
    container.register_service(Optimizer, PyXESXXNOptimizer)
    container.register_service(LinearOptimizer, PyXESXXNLinearOptimizer)
    container.register_service(NonlinearOptimizer, PyXESXXNNonlinearOptimizer)
    container.register_service(MultiObjectiveOptimizer, PyXESXXNMultiObjectiveOptimizer)
    
    logger.info("Default PyXESXXN services registered in dependency injection container")


# Convenience functions for common operations
def get_service(service_type: Type) -> Any:
    """Get a service instance from the global container."""
    return get_container().get_service(service_type)


def register_service(service_type: Type, implementation: Union[Type, Callable], 
                    singleton: bool = True) -> None:
    """Register a service in the global container."""
    get_container().register_service(service_type, implementation, singleton)


def create_energy_hub_model(config: Any) -> Any:
    """Create an energy hub model using dependency injection."""
    from .multi_carrier.abstract import EnergyHubInterface
    hub_model = get_service(EnergyHubInterface)
    # Configure the model if needed
    return hub_model


def create_optimizer(config: Any) -> Any:
    """Create an optimizer using dependency injection."""
    from .optimization.abstract import Optimizer
    optimizer = get_service(Optimizer)
    # Configure the optimizer if needed
    return optimizer


# Context manager for testing
class TestContainer:
    """Context manager for testing with a clean container."""
    
    def __init__(self, test_services: Optional[Dict[Type, Any]] = None):
        self.test_services = test_services or {}
        self.original_container: Optional[DependencyInjectionContainer] = None
    
    def __enter__(self) -> DependencyInjectionContainer:
        # Save original container
        self.original_container = _container
        
        # Create new container for testing
        test_container = DependencyInjectionContainer()
        
        # Register test services
        for service_type, implementation in self.test_services.items():
            test_container.register_service(service_type, implementation)
        
        set_container(test_container)
        return test_container
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original container
        set_container(self.original_container)