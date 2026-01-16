"""
Dependency Injection container for PyXESXXN optimization module.

This module provides a dependency injection container that allows for
configurable component creation and easy testing through dependency
injection and mocking.
"""

from __future__ import annotations

from typing import Dict, Type, Any, Callable, Optional, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .abstract import (
    OptimizationType, SolverType, OptimizationConfig,
    OptimizationVariable, OptimizationConstraint, Optimizer,
    LinearOptimizer, NonlinearOptimizer, MultiObjectiveOptimizer,
    OptimizationFactory
)


class DependencyContainer(ABC):
    """Abstract base class for dependency injection containers."""
    
    @abstractmethod
    def register(self, interface: Type, implementation: Union[Type, Callable]) -> None:
        """Register an implementation for an interface."""
        pass
    
    @abstractmethod
    def resolve(self, interface: Type, **kwargs) -> Any:
        """Resolve an instance of the specified interface."""
        pass
    
    @abstractmethod
    def get_factory(self) -> OptimizationFactory:
        """Get the optimization factory from the container."""
        pass


@dataclass
class ComponentRegistration:
    """Registration information for a component."""
    implementation: Union[Type, Callable]
    singleton: bool = False
    instance: Optional[Any] = None


class PyXESXXNDependencyContainer(DependencyContainer):
    """Dependency injection container for PyXESXXN optimization components."""
    
    def __init__(self):
        self._registrations: Dict[Type, ComponentRegistration] = {}
        self._setup_default_registrations()
    
    def _setup_default_registrations(self) -> None:
        """Set up default component registrations."""
        
        # Import implementations here to avoid circular imports
        from .pyxesxxn_impl import (
            PyXESXXNOptimizationVariable, PyXESXXNOptimizationConstraint,
            PyXESXXNOptimizer, PyXESXXNLinearOptimizer, PyXESXXNNonlinearOptimizer,
            PyXESXXNMultiObjectiveOptimizer, PyXESXXNOptimizationFactory,
            create_pyxesxxn_optimizer, create_pyxesxxn_optimization_variable,
            create_pyxesxxn_optimization_constraint
        )
        from .abstract import get_default_optimization_factory
        
        # Register default implementations
        self.register(OptimizationVariable, PyXESXXNOptimizationVariable)
        self.register(OptimizationConstraint, PyXESXXNOptimizationConstraint)
        self.register(Optimizer, PyXESXXNOptimizer)
        self.register(LinearOptimizer, PyXESXXNLinearOptimizer)
        self.register(NonlinearOptimizer, PyXESXXNNonlinearOptimizer)
        self.register(MultiObjectiveOptimizer, PyXESXXNMultiObjectiveOptimizer)
        self.register(OptimizationFactory, PyXESXXNOptimizationFactory, singleton=True)
        
        # Register factory functions as singletons
        self.register("create_optimizer", create_pyxesxxn_optimizer, singleton=True)
        self.register("create_variable", create_pyxesxxn_optimization_variable, singleton=True)
        self.register("create_constraint", create_pyxesxxn_optimization_constraint, singleton=True)
        self.register("default_factory", get_default_optimization_factory, singleton=True)
    
    def register(self, interface: Union[Type, str], 
                implementation: Union[Type, Callable],
                singleton: bool = False) -> None:
        """Register an implementation for an interface."""
        
        if isinstance(interface, str):
            # For named registrations (like factory functions)
            interface_type = type(interface, (), {})
        else:
            interface_type = interface
        
        self._registrations[interface_type] = ComponentRegistration(
            implementation=implementation,
            singleton=singleton
        )
    
    def resolve(self, interface: Type, **kwargs) -> Any:
        """Resolve an instance of the specified interface."""
        
        if interface not in self._registrations:
            raise ValueError(f"No registration found for interface: {interface}")
        
        registration = self._registrations[interface]
        
        # Return singleton instance if available
        if registration.singleton and registration.instance is not None:
            return registration.instance
        
        # Create new instance
        implementation = registration.implementation
        
        if callable(implementation) and not isinstance(implementation, type):
            # Function-based implementation
            instance = implementation(**kwargs)
        else:
            # Class-based implementation
            instance = implementation(**kwargs)
        
        # Store singleton instance if configured
        if registration.singleton:
            registration.instance = instance
        
        return instance
    
    def get_factory(self) -> OptimizationFactory:
        """Get the optimization factory from the container."""
        return self.resolve(OptimizationFactory)
    
    def create_optimizer(self, config: OptimizationConfig) -> Optimizer:
        """Create an optimizer using the configured factory."""
        factory = self.get_factory()
        return factory.create_optimizer(config)
    
    def create_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """Create an optimization variable."""
        # Check if there's a custom registration for OptimizationVariable
        if OptimizationVariable in self._registrations:
            implementation = self._registrations[OptimizationVariable].implementation
            if isinstance(implementation, type):
                # Use the registered class directly
                return implementation(name, **kwargs)
            else:
                # Use the registered function
                return implementation(name, **kwargs)
        
        # Fall back to factory method
        factory = self.get_factory()
        return factory.create_variable(name, **kwargs)
    
    def create_constraint(self, name: str, expression: Callable, 
                         lower_bound: float, upper_bound: float) -> OptimizationConstraint:
        """Create an optimization constraint."""
        factory = self.get_factory()
        return factory.create_constraint(name, expression, lower_bound, upper_bound)


class MockDependencyContainer(DependencyContainer):
    """Mock dependency container for testing purposes."""
    
    def __init__(self):
        self._registrations: Dict[Type, Any] = {}
        self._mock_instances: Dict[Type, Any] = {}
    
    def register(self, interface: Type, implementation: Union[Type, Callable]) -> None:
        """Register a mock implementation."""
        self._registrations[interface] = implementation
    
    def register_mock(self, interface: Type, mock_instance: Any) -> None:
        """Register a pre-created mock instance."""
        self._mock_instances[interface] = mock_instance
    
    def resolve(self, interface: Type, **kwargs) -> Any:
        """Resolve a mock instance."""
        
        if interface in self._mock_instances:
            return self._mock_instances[interface]
        
        if interface in self._registrations:
            implementation = self._registrations[interface]
            if callable(implementation):
                return implementation(**kwargs)
            return implementation
        
        # Create a simple mock if no registration found
        from unittest.mock import MagicMock
        return MagicMock(spec=interface)
    
    def get_factory(self) -> OptimizationFactory:
        """Get a mock optimization factory."""
        from unittest.mock import MagicMock
        
        if OptimizationFactory in self._mock_instances:
            return self._mock_instances[OptimizationFactory]
        
        mock_factory = MagicMock(spec=OptimizationFactory)
        
        # Configure mock factory methods
        mock_factory.create_optimizer.return_value = MagicMock(spec=Optimizer)
        mock_factory.create_variable.return_value = MagicMock(spec=OptimizationVariable)
        mock_factory.create_constraint.return_value = MagicMock(spec=OptimizationConstraint)
        
        return mock_factory
    
    def create_optimizer(self, config: OptimizationConfig) -> Optimizer:
        """Create a mock optimizer using the configured factory."""
        # Check if there's a registered mock optimizer instance
        if Optimizer in self._mock_instances:
            return self._mock_instances[Optimizer]
        
        factory = self.get_factory()
        return factory.create_optimizer(config)
    
    def create_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """Create a mock optimization variable."""
        factory = self.get_factory()
        return factory.create_variable(name, **kwargs)
    
    def create_constraint(self, name: str, expression: Callable, 
                         lower_bound: float, upper_bound: float) -> OptimizationConstraint:
        """Create a mock optimization constraint."""
        factory = self.get_factory()
        return factory.create_constraint(name, expression, lower_bound, upper_bound)


# Global dependency container instance
_default_container: Optional[DependencyContainer] = None


def get_default_container() -> DependencyContainer:
    """Get the default dependency container."""
    global _default_container
    
    if _default_container is None:
        _default_container = PyXESXXNDependencyContainer()
    
    return _default_container


def set_default_container(container: DependencyContainer) -> None:
    """Set the default dependency container."""
    global _default_container
    _default_container = container


def reset_default_container() -> None:
    """Reset the default dependency container to the default implementation."""
    global _default_container
    _default_container = PyXESXXNDependencyContainer()


# Convenience functions for common operations
def create_optimizer_with_di(config: OptimizationConfig, 
                           container: Optional[DependencyContainer] = None) -> Optimizer:
    """Create an optimizer using dependency injection."""
    if container is None:
        container = get_default_container()
    return container.create_optimizer(config)


def create_variable_with_di(name: str, **kwargs) -> OptimizationVariable:
    """Create an optimization variable using dependency injection."""
    container = get_default_container()
    return container.create_variable(name, **kwargs)


def create_constraint_with_di(name: str, expression: Callable, 
                            lower_bound: float, upper_bound: float) -> OptimizationConstraint:
    """Create an optimization constraint using dependency injection."""
    container = get_default_container()
    return container.create_constraint(name, expression, lower_bound, upper_bound)


def get_optimization_factory_with_di() -> OptimizationFactory:
    """Get the optimization factory using dependency injection."""
    container = get_default_container()
    return container.get_factory()


# Context manager for temporary container configuration
from contextlib import contextmanager


@contextmanager
def temporary_container(container: DependencyContainer):
    """Context manager for temporarily using a different dependency container."""
    original_container = get_default_container()
    set_default_container(container)
    
    try:
        yield
    finally:
        set_default_container(original_container)


# Testing utilities
def create_test_container() -> MockDependencyContainer:
    """Create a test container with mock implementations."""
    return MockDependencyContainer()


def with_mock_container(test_func: Callable) -> Callable:
    """Decorator for tests that use a mock dependency container."""
    
    def wrapper(*args, **kwargs):
        original_container = get_default_container()
        mock_container = create_test_container()
        set_default_container(mock_container)
        
        try:
            return test_func(*args, **kwargs)
        finally:
            set_default_container(original_container)
    
    return wrapper