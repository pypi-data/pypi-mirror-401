"""
Integration tests for PyXESXXN optimization module.
Tests the decoupling between abstract interfaces and PyXESXXN implementations.
"""

import pytest
from typing import Dict, Any, Callable
import logging

# Import the abstract interfaces
from pyxesxxn.optimization.abstract import (
    OptimizationType, SolverType, OptimizationConfig,
    OptimizationVariable, OptimizationConstraint, Optimizer,
    LinearOptimizer, NonlinearOptimizer, MultiObjectiveOptimizer,
    OptimizationFactory, get_default_optimization_factory
)

# Import the PyXESXXN implementations
from pyxesxxn.optimization.pyxesxxn_impl import (
    PyXESXXNOptimizationVariable, PyXESXXNOptimizationConstraint,
    PyXESXXNOptimizer, PyXESXXNLinearOptimizer, PyXESXXNNonlinearOptimizer,
    PyXESXXNMultiObjectiveOptimizer, PyXESXXNOptimizationFactory,
    create_pyxesxxn_optimizer, create_pyxesxxn_optimization_variable,
    create_pyxesxxn_optimization_constraint
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestOptimizationIntegration:
    """Integration tests for optimization module decoupling."""
    
    def test_abstract_interface_inheritance(self):
        """Test that PyXESXXN implementations correctly inherit from abstract interfaces."""
        
        # Test variable inheritance
        assert issubclass(PyXESXXNOptimizationVariable, OptimizationVariable)
        
        # Test constraint inheritance
        assert issubclass(PyXESXXNOptimizationConstraint, OptimizationConstraint)
        
        # Test optimizer inheritance
        assert issubclass(PyXESXXNOptimizer, Optimizer)
        assert issubclass(PyXESXXNLinearOptimizer, (PyXESXXNOptimizer, LinearOptimizer))
        assert issubclass(PyXESXXNNonlinearOptimizer, (PyXESXXNOptimizer, NonlinearOptimizer))
        assert issubclass(PyXESXXNMultiObjectiveOptimizer, (PyXESXXNOptimizer, MultiObjectiveOptimizer))
        
        # Test factory inheritance
        assert issubclass(PyXESXXNOptimizationFactory, OptimizationFactory)
        
        logger.info("[OK] All PyXESXXN implementations correctly inherit from abstract interfaces")
    
    def test_variable_creation_and_properties(self):
        """Test variable creation and property access."""
        
        # Create variable using abstract interface
        var_config = {
            'lower_bound': 0.0,
            'upper_bound': 10.0,
            'initial_value': 5.0,
            'variable_type': 'continuous'
        }
        
        # Test direct creation
        variable = PyXESXXNOptimizationVariable("test_var", **var_config)
        assert isinstance(variable, OptimizationVariable)
        assert variable.name == "test_var"
        assert variable.lower_bound == 0.0
        assert variable.upper_bound == 10.0
        assert variable.initial_value == 5.0
        
        # Test factory creation
        factory_var = create_pyxesxxn_optimization_variable("factory_var", **var_config)
        assert isinstance(factory_var, OptimizationVariable)
        
        logger.info("[OK] Variable creation and properties work correctly")
    
    def test_constraint_creation_and_evaluation(self):
        """Test constraint creation and evaluation."""
        
        def constraint_expression(variables: Dict[str, float]) -> float:
            return variables.get('x', 0.0) + variables.get('y', 0.0)
        
        # Create constraint using abstract interface
        constraint = PyXESXXNOptimizationConstraint(
            "test_constraint", constraint_expression, 0.0, 10.0
        )
        assert isinstance(constraint, OptimizationConstraint)
        assert constraint.name == "test_constraint"
        
        # Test constraint evaluation
        test_variables = {'x': 3.0, 'y': 4.0}
        value = constraint.evaluate(test_variables)
        assert value == 7.0
        assert constraint.is_satisfied(test_variables)
        
        # Test factory creation
        factory_constraint = create_pyxesxxn_optimization_constraint(
            "factory_constraint", constraint_expression, 0.0, 10.0
        )
        assert isinstance(factory_constraint, OptimizationConstraint)
        
        logger.info("[OK] Constraint creation and evaluation work correctly")
    
    def test_optimizer_creation_and_basic_operations(self):
        """Test optimizer creation and basic operations."""
        
        # Create optimization configuration
        config = OptimizationConfig(
            name="test_optimization",
            optimization_type=OptimizationType.LINEAR,
            solver=SolverType.SCIPY
        )
        
        # Test direct creation
        optimizer = PyXESXXNLinearOptimizer(config)
        assert isinstance(optimizer, LinearOptimizer)
        assert isinstance(optimizer, PyXESXXNOptimizer)
        assert optimizer.name == "test_optimization"
        
        # Test variable addition
        variable = optimizer.add_variable("x", lower_bound=0.0, upper_bound=10.0)
        assert isinstance(variable, OptimizationVariable)
        assert "x" in optimizer.variables
        
        # Test constraint addition
        def constraint_expr(vars_dict):
            return vars_dict.get('x', 0.0)
        
        constraint = optimizer.add_constraint("c1", constraint_expr, lower_bound=0.0, upper_bound=5.0)
        assert isinstance(constraint, OptimizationConstraint)
        assert "c1" in optimizer.constraints
        
        # Test objective setting
        def objective(vars_dict):
            return vars_dict.get('x', 0.0)
        
        optimizer.set_objective(objective)
        assert optimizer.objective_function is not None
        
        logger.info("[OK] Optimizer creation and basic operations work correctly")
    
    def test_factory_pattern(self):
        """Test the factory pattern for creating optimization components."""
        
        # Create configuration
        config = OptimizationConfig(
            name="factory_test",
            optimization_type=OptimizationType.NONLINEAR,
            solver=SolverType.SCIPY
        )
        
        # Test factory creation
        factory = PyXESXXNOptimizationFactory()
        
        # Create optimizer
        optimizer = factory.create_optimizer(config)
        assert isinstance(optimizer, Optimizer)
        assert isinstance(optimizer, PyXESXXNNonlinearOptimizer)
        
        # Create variable
        variable = factory.create_variable("factory_var", lower_bound=0.0, upper_bound=1.0)
        assert isinstance(variable, OptimizationVariable)
        
        # Create constraint
        def constraint_expr(vars_dict):
            return vars_dict.get('factory_var', 0.0)
        
        constraint = factory.create_constraint(
            "factory_constraint", constraint_expr, 0.0, 1.0
        )
        assert isinstance(constraint, OptimizationConstraint)
        
        logger.info("[OK] Factory pattern works correctly")
    
    def test_default_factory_function(self):
        """Test the default factory function."""
        
        # Test default factory
        factory = get_default_optimization_factory()
        assert isinstance(factory, OptimizationFactory)
        assert isinstance(factory, PyXESXXNOptimizationFactory)
        
        # Create configuration
        config = OptimizationConfig(
            name="default_factory_test",
            optimization_type=OptimizationType.MULTI_OBJECTIVE,
            solver=SolverType.SCIPY
        )
        
        # Create optimizer using default factory
        optimizer = factory.create_optimizer(config)
        assert isinstance(optimizer, Optimizer)
        assert isinstance(optimizer, PyXESXXNMultiObjectiveOptimizer)
        
        logger.info("[OK] Default factory function works correctly")
    
    def test_multi_objective_optimizer(self):
        """Test multi-objective optimizer specific functionality."""
        
        config = OptimizationConfig(
            name="multi_obj_test",
            optimization_type=OptimizationType.MULTI_OBJECTIVE,
            solver=SolverType.SCIPY
        )
        
        optimizer = PyXESXXNMultiObjectiveOptimizer(config)
        
        # Test adding multiple objectives
        def obj1(vars_dict):
            return vars_dict.get('x', 0.0)
        
        def obj2(vars_dict):
            return -vars_dict.get('x', 0.0)  # Opposite objective
        
        optimizer.add_objective(obj1, weight=0.7)
        optimizer.add_objective(obj2, weight=0.3)
        
        assert len(optimizer.objective_functions) == 2
        assert len(optimizer.weights) == 2
        assert optimizer.weights[0] == 0.7
        assert optimizer.weights[1] == 0.3
        
        # Test preferences
        preferences = {'obj1': 0.8, 'obj2': 0.2}
        optimizer.set_preference(preferences)
        assert optimizer.preferences == preferences
        
        logger.info("[OK] Multi-objective optimizer functionality works correctly")
    
    def test_optimization_solving(self):
        """Test optimization problem solving."""
        
        # Create a simple linear optimization problem
        config = OptimizationConfig(
            name="solve_test",
            optimization_type=OptimizationType.LINEAR,
            solver=SolverType.SCIPY
        )
        
        optimizer = PyXESXXNLinearOptimizer(config)
        
        # Add variable
        optimizer.add_variable("x", lower_bound=0.0, upper_bound=10.0)
        
        # Add constraint
        def constraint_expr(vars_dict):
            return vars_dict.get('x', 0.0)
        
        optimizer.add_constraint("c1", constraint_expr, lower_bound=0.0, upper_bound=5.0)
        
        # Set objective (maximize x)
        def objective(vars_dict):
            return vars_dict.get('x', 0.0)
        
        optimizer.set_objective(objective)
        
        # Solve the problem
        result = optimizer.solve()
        
        # Verify result structure
        assert 'status' in result
        assert 'optimal_value' in result
        assert 'solution' in result
        assert 'iterations' in result
        assert 'solver_time' in result
        
        # Verify solution
        if result['status'] == 'success':
            assert 'x' in result['solution']
            assert 0.0 <= result['solution']['x'] <= 5.0  # Constraint should be satisfied
            assert result['optimal_value'] == result['solution']['x']
        
        logger.info("[OK] Optimization solving works correctly")
    
    def test_error_handling(self):
        """Test error handling and validation."""
        
        config = OptimizationConfig(
            name="error_test",
            optimization_type=OptimizationType.LINEAR,
            solver=SolverType.SCIPY
        )
        
        optimizer = PyXESXXNLinearOptimizer(config)
        
        # Test invalid variable bounds
        with pytest.raises(ValueError):
            optimizer.add_variable("invalid_var", lower_bound=10.0, upper_bound=5.0)
        
        # Test problem validation
        is_valid, errors = optimizer.validate_problem()
        assert not is_valid
        assert "Objective function not set" in errors
        assert "No variables defined" in errors
        
        logger.info("[OK] Error handling and validation work correctly")


def run_all_tests():
    """Run all integration tests and report results."""
    
    test_instance = TestOptimizationIntegration()
    
    # Run all test methods
    test_methods = [
        'test_abstract_interface_inheritance',
        'test_variable_creation_and_properties',
        'test_constraint_creation_and_evaluation',
        'test_optimizer_creation_and_basic_operations',
        'test_factory_pattern',
        'test_default_factory_function',
        'test_multi_objective_optimizer',
        'test_optimization_solving',
        'test_error_handling'
    ]
    
    results = {}
    for method_name in test_methods:
        try:
            method = getattr(test_instance, method_name)
            method()
            results[method_name] = 'PASS'
            logger.info(f"[OK] {method_name}: PASS")
        except Exception as e:
            results[method_name] = f'FAIL: {str(e)}'
            logger.error(f"[ERROR] {method_name}: FAIL - {str(e)}")
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("INTEGRATION TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for result in results.values() if result == 'PASS')
    total = len(results)
    
    for test_name, result in results.items():
        status = "[OK] PASS" if result == 'PASS' else f"[ERROR] {result}"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("[START] All integration tests passed! The optimization module is properly decoupled.")
    else:
        logger.warning(f"[WARNING] {total - passed} test(s) failed. Please review the implementation.")
    
    return passed == total


if __name__ == "__main__":
    # Run the tests when executed directly
    success = run_all_tests()
    exit(0 if success else 1)