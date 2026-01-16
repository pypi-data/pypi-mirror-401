"""
Control strategies for dynamic energy system simulation.

This module provides various control strategies for managing dynamic energy systems,
including load following, economic dispatch, frequency control, and other
advanced control algorithms.
"""

import logging
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Tuple, Union
import numpy as np
import pandas as pd

try:
    import pypsa
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)


class ControlStrategyType(Enum):
    """Types of control strategies."""
    PID = "pid"
    MPC = "mpc"  # Model Predictive Control
    HIERARCHICAL = "hierarchical"
    DECENTRALIZED = "decentralized"
    LOAD_FOLLOWING = "load_following"
    ECONOMIC_DISPATCH = "economic_dispatch"
    FREQUENCY_CONTROL = "frequency_control"
    VOLTAGE_CONTROL = "voltage_control"
    ADAPTIVE = "adaptive"
    RULE_BASED = "rule_based"
    OPTIMAL = "optimal"
    FUZZY = "fuzzy"


class ControlMode(Enum):
    """Control operation modes."""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SCHEDULED = "scheduled"
    EMERGENCY = "emergency"
    MAINTENANCE = "maintenance"


class ControlStatus(Enum):
    """Control system status."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    STANDBY = "standby"
    ERROR = "error"
    CALIBRATING = "calibrating"


@dataclass
class ControlAction:
    """Represents a control action to be executed."""
    action_id: str
    target_device: str
    action_type: str
    value: float
    timestamp: float
    priority: int = 1
    execution_time: float = 0.0
    estimated_duration: float = 0.0
    preconditions: List[str] = field(default_factory=list)
    rollback_action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ControlConfig:
    """Configuration for control strategies."""
    strategy_type: ControlStrategyType
    control_mode: ControlMode
    sample_time: float = 1.0  # seconds
    min_update_interval: float = 0.1  # seconds
    max_update_interval: float = 60.0  # seconds
    control_deadband: float = 0.02  # 2% deadband
    output_limit_min: float = 0.0
    output_limit_max: float = 1.0
    enable_feedback: bool = True
    enable_feedforward: bool = False
    enable_adaptation: bool = False
    adaptation_rate: float = 0.1
    safety_limits: Dict[str, float] = field(default_factory=dict)
    priority_weights: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ControlState:
    """State information for control system."""
    controller_id: str
    status: ControlStatus
    mode: ControlMode
    current_time: float
    last_update_time: float
    setpoints: Dict[str, float] = field(default_factory=dict)
    measurements: Dict[str, float] = field(default_factory=dict)
    outputs: Dict[str, float] = field(default_factory=dict)
    errors: Dict[str, float] = field(default_factory=dict)
    derivative_errors: Dict[str, float] = field(default_factory=dict)
    integral_errors: Dict[str, float] = field(default_factory=dict)
    tuning_parameters: Dict[str, float] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    active_actions: List[ControlAction] = field(default_factory=list)


class BaseControlStrategy(ABC):
    """Base class for all control strategies.
    
    This abstract base class defines the common interface and functionality
    that all control strategies must implement.
    """
    
    def __init__(self, config: ControlConfig):
        """Initialize control strategy.
        
        Parameters
        ----------
        config : ControlConfig
            Control strategy configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.state = ControlState(
            controller_id=str(id(self)),
            status=ControlStatus.INACTIVE,
            mode=config.control_mode,
            current_time=0.0,
            last_update_time=0.0,
            tuning_parameters=self._initialize_tuning_parameters()
        )
        
        # Control loop timing
        self.last_control_time = 0.0
        self.control_timer = 0.0
        
        # Performance tracking
        self.performance_history: Dict[str, List[float]] = {
            'tracking_error': [],
            'control_effort': [],
            'settling_time': [],
            'overshoot': [],
            'steady_state_error': []
        }
        
        # Safety and limits
        self.safety_constraints_active = False
        self.emergency_shutdown_triggered = False
    
    def _initialize_tuning_parameters(self) -> Dict[str, float]:
        """Initialize tuning parameters based on strategy type.
        
        Returns
        -------
        Dict[str, float]
            Tuning parameters
        """
        if self.config.strategy_type == ControlStrategyType.PID:
            return {
                'kp': 1.0,  # Proportional gain
                'ki': 0.1,  # Integral gain
                'kd': 0.05  # Derivative gain
            }
        elif self.config.strategy_type == ControlStrategyType.MPC:
            return {
                'prediction_horizon': 10,  # Steps
                'control_horizon': 5,      # Steps
                'sampling_time': self.config.sample_time,
                'cost_weights': {'tracking': 1.0, 'effort': 0.1, 'constraints': 100.0}
            }
        elif self.config.strategy_type == ControlStrategyType.FREQUENCY_CONTROL:
            return {
                'droop': 0.05,         # 5% droop
                'deadband': 0.1,       # Hz
                'max_ramp_rate': 0.1,  # MW/min
                'reserve_margin': 0.15  # 15% reserves
            }
        elif self.config.strategy_type == ControlStrategyType.VOLTAGE_CONTROL:
            return {
                'voltage_setpoint': 1.0,    # p.u.
                'voltage_tolerance': 0.05,  # p.u.
                'reactive_power_factor': 0.95
            }
        else:
            # Default parameters
            return {'default_gain': 1.0}
    
    @abstractmethod
    def calculate_control_output(self, 
                               setpoints: Dict[str, float],
                               measurements: Dict[str, float],
                               external_inputs: Dict[str, float],
                               time_step: float) -> Dict[str, float]:
        """Calculate control output for current time step.
        
        Parameters
        ----------
        setpoints : Dict[str, float]
            Target setpoints
        measurements : Dict[str, float]
            Current measurements
        external_inputs : Dict[str, float]
            External input signals
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Dict[str, float]
            Control outputs
        """
        pass
    
    def initialize(self, initial_setpoints: Dict[str, float] = None) -> None:
        """Initialize control strategy.
        
        Parameters
        ----------
        initial_setpoints : Dict[str, float], optional
            Initial setpoints
        """
        if initial_setpoints:
            self.state.setpoints.update(initial_setpoints)
        
        # Reset integral and derivative terms
        self.state.integral_errors.clear()
        self.state.derivative_errors.clear()
        self.state.errors.clear()
        
        # Reset performance tracking
        for history in self.performance_history.values():
            history.clear()
        
        self.state.status = ControlStatus.ACTIVE
        self.logger.info(f"Control strategy {self.__class__.__name__} initialized")
    
    def update(self, 
               current_time: float,
               setpoints: Dict[str, float],
               measurements: Dict[str, float],
               external_inputs: Dict[str, float],
               time_step: float) -> List[ControlAction]:
        """Update control strategy for current time step.
        
        Parameters
        ----------
        current_time : float
            Current simulation time
        setpoints : Dict[str, float]
            Target setpoints
        measurements : Dict[str, float]
            Current measurements
        external_inputs : Dict[str, float]
            External input signals
        time_step : float
            Time step in seconds
            
        Returns
        -------
        List[ControlAction]
            Control actions to execute
        """
        # Update timing
        self.state.current_time = current_time
        self.control_timer = current_time - self.last_control_time
        
        # Check if control update is needed
        if self.control_timer < self.config.min_update_interval:
            return []
        
        # Update measurements and setpoints
        self.state.measurements.update(measurements)
        self.state.setpoints.update(setpoints)
        
        # Calculate control output
        try:
            outputs = self.calculate_control_output(
                self.state.setpoints.copy(),
                self.state.measurements.copy(),
                external_inputs.copy(),
                time_step
            )
            
            # Apply safety constraints
            safe_outputs = self._apply_safety_constraints(outputs)
            self.state.outputs = safe_outputs
            
            # Generate control actions
            actions = self._generate_control_actions(safe_outputs)
            
            # Update performance metrics
            self._update_performance_metrics(setpoints, measurements, outputs)
            
            # Check for emergency conditions
            self._check_emergency_conditions(measurements)
            
            self.last_control_time = current_time
            self.state.status = ControlStatus.ACTIVE
            
            return actions
            
        except Exception as e:
            self.logger.error(f"Control update failed: {str(e)}")
            self.state.status = ControlStatus.ERROR
            return []
    
    def _apply_safety_constraints(self, outputs: Dict[str, float]) -> Dict[str, float]:
        """Apply safety constraints to control outputs.
        
        Parameters
        ----------
        outputs : Dict[str, float]
            Raw control outputs
            
        Returns
        -------
        Dict[str, float]
            Constrained outputs
        """
        safe_outputs = {}
        
        for key, value in outputs.items():
            # Apply output limits
            if 'limit_min' in self.config.safety_limits and key in self.config.safety_limits:
                lower_bound = self.config.safety_limits[f'{key}_limit_min']
                value = max(value, lower_bound)
            
            if 'limit_max' in self.config.safety_limits and key in self.config.safety_limits:
                upper_bound = self.config.safety_limits[f'{key}_limit_max']
                value = min(value, upper_bound)
            
            # Apply general output limits
            value = max(self.config.output_limit_min, 
                       min(self.config.output_limit_max, value))
            
            safe_outputs[key] = value
        
        # Check for critical violations
        critical_violations = []
        for key, value in safe_outputs.items():
            safety_key = f'{key}_safety_limit'
            if safety_key in self.config.safety_limits:
                safety_limit = self.config.safety_limits[safety_key]
                if abs(value) > safety_limit:
                    critical_violations.append(f"{key}: {value} > {safety_limit}")
        
        if critical_violations:
            self.logger.warning(f"Safety constraint violations: {critical_violations}")
            self.safety_constraints_active = True
        
        return safe_outputs
    
    def _generate_control_actions(self, outputs: Dict[str, float]) -> List[ControlAction]:
        """Generate control actions from outputs.
        
        Parameters
        ----------
        outputs : Dict[str, float]
            Control outputs
            
        Returns
        -------
        List[ControlAction]
            Control actions
        """
        actions = []
        action_id_counter = 0
        
        for device_id, output_value in outputs.items():
            # Only create action if output changed significantly
            if device_id in self.state.outputs:
                previous_value = self.state.outputs[device_id]
                if abs(output_value - previous_value) < self.config.control_deadband:
                    continue
            
            action = ControlAction(
                action_id=f"action_{self.state.controller_id}_{action_id_counter}",
                target_device=device_id,
                action_type="setpoint",
                value=output_value,
                timestamp=self.state.current_time,
                priority=self.config.priority_weights.get(device_id, 1),
                execution_time=1.0,  # Default 1 second
                metadata={
                    'controller_type': self.config.strategy_type.value,
                    'control_mode': self.config.control_mode.value
                }
            )
            
            actions.append(action)
            action_id_counter += 1
        
        return actions
    
    def _update_performance_metrics(self, 
                                   setpoints: Dict[str, float],
                                   measurements: Dict[str, float],
                                   outputs: Dict[str, float]) -> None:
        """Update performance metrics.
        
        Parameters
        ----------
        setpoints : Dict[str, float]
            Setpoints
        measurements : Dict[str, float]
            Measurements
        outputs : Dict[str, float]
            Control outputs
        """
        # Calculate tracking error
        tracking_errors = {}
        for key in setpoints:
            if key in measurements:
                tracking_error = abs(setpoints[key] - measurements[key])
                tracking_errors[key] = tracking_error
        
        if tracking_errors:
            avg_tracking_error = sum(tracking_errors.values()) / len(tracking_errors)
            self.performance_history['tracking_error'].append(avg_tracking_error)
        
        # Calculate control effort
        if self.state.outputs:
            control_effort = sum(abs(outputs[key] - self.state.outputs.get(key, 0.0))
                               for key in outputs)
            self.performance_history['control_effort'].append(control_effort)
        
        # Limit history size
        max_history = 1000
        for history in self.performance_history.values():
            if len(history) > max_history:
                history[:len(history) - max_history] = []
    
    def _check_emergency_conditions(self, measurements: Dict[str, float]) -> None:
        """Check for emergency conditions.
        
        Parameters
        ----------
        measurements : Dict[str, float]
            Current measurements
        """
        emergency_conditions = []
        
        # Check frequency limits
        if 'system_frequency' in measurements:
            freq = measurements['system_frequency']
            if freq < 49.5 or freq > 50.5:  # ±0.5 Hz from nominal
                emergency_conditions.append(f"Frequency out of range: {freq} Hz")
        
        # Check voltage limits
        if 'system_voltage' in measurements:
            voltage = measurements['system_voltage']
            if voltage < 0.9 or voltage > 1.1:  # ±10% from nominal
                emergency_conditions.append(f"Voltage out of range: {voltage} p.u.")
        
        # Check temperature limits
        if 'ambient_temperature' in measurements:
            temp = measurements['ambient_temperature']
            if temp > 50.0:  # 50°C maximum
                emergency_conditions.append(f"Temperature too high: {temp}°C")
        
        if emergency_conditions:
            self.logger.error(f"Emergency conditions detected: {emergency_conditions}")
            self.emergency_shutdown_triggered = True
            self.state.status = ControlStatus.ERROR
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary.
        
        Returns
        -------
        Dict[str, Any]
            Performance summary
        """
        summary = {
            'controller_id': self.state.controller_id,
            'strategy_type': self.config.strategy_type.value,
            'status': self.state.status.value,
            'control_actions_executed': len(self.state.active_actions),
            'emergency_shutdowns': 1 if self.emergency_shutdown_triggered else 0,
            'safety_constraints_active': self.safety_constraints_active
        }
        
        # Add statistical metrics
        for metric_name, history in self.performance_history.items():
            if history:
                summary[f'{metric_name}_mean'] = np.mean(history)
                summary[f'{metric_name}_std'] = np.std(history)
                summary[f'{metric_name}_max'] = np.max(history)
                summary[f'{metric_name}_min'] = np.min(history)
        
        return summary
    
    def reset(self) -> None:
        """Reset control strategy to initial state."""
        self.state.status = ControlStatus.INACTIVE
        self.state.setpoints.clear()
        self.state.measurements.clear()
        self.state.outputs.clear()
        self.state.errors.clear()
        self.state.derivative_errors.clear()
        self.state.integral_errors.clear()
        
        # Reset tuning parameters
        self.state.tuning_parameters = self._initialize_tuning_parameters()
        
        # Reset performance tracking
        for history in self.performance_history.values():
            history.clear()
        
        self.last_control_time = 0.0
        self.control_timer = 0.0
        self.safety_constraints_active = False
        self.emergency_shutdown_triggered = False
        
        self.logger.info("Control strategy reset")


class PIDController(BaseControlStrategy):
    """Proportional-Integral-Derivative (PID) controller."""
    
    def __init__(self, config: ControlConfig):
        """Initialize PID controller.
        
        Parameters
        ----------
        config : ControlConfig
            PID controller configuration
        """
        super().__init__(config)
        
        # PID specific parameters
        self.kp = config.metadata.get('kp', 1.0)
        self.ki = config.metadata.get('ki', 0.1)
        self.kd = config.metadata.get('kd', 0.05)
        self.integral_windup_limit = config.metadata.get('integral_windup_limit', 10.0)
        self.derivative_filter_time = config.metadata.get('derivative_filter_time', 0.1)
        
        # Derivative filter
        self.derivative_filter = {}
        self.previous_derivative = {}
        
    def calculate_control_output(self, 
                               setpoints: Dict[str, float],
                               measurements: Dict[str, float],
                               external_inputs: Dict[str, float],
                               time_step: float) -> Dict[str, float]:
        """Calculate PID control output.
        
        Parameters
        ----------
        setpoints : Dict[str, float]
            Target setpoints
        measurements : Dict[str, float]
            Current measurements
        external_inputs : Dict[str, float]
            External input signals
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Dict[str, float]
            Control outputs
        """
        outputs = {}
        
        for control_variable in setpoints:
            if control_variable not in measurements:
                continue
            
            # Calculate error
            error = setpoints[control_variable] - measurements[control_variable]
            
            # Update integral term (with windup protection)
            if control_variable not in self.state.integral_errors:
                self.state.integral_errors[control_variable] = 0.0
            
            self.state.integral_errors[control_variable] += error * time_step
            
            # Apply windup protection
            if self.state.integral_errors[control_variable] > self.integral_windup_limit:
                self.state.integral_errors[control_variable] = self.integral_windup_limit
            elif self.state.integral_errors[control_variable] < -self.integral_windup_limit:
                self.state.integral_errors[control_variable] = -self.integral_windup_limit
            
            # Calculate derivative term (with filtering)
            if control_variable not in self.derivative_filter:
                self.derivative_filter[control_variable] = 0.0
                self.previous_derivative[control_variable] = 0.0
            
            # Derivative of error
            raw_derivative = error - self.state.errors.get(control_variable, 0.0) / time_step
            
            # Apply first-order filter
            alpha = time_step / (time_step + self.derivative_filter_time)
            self.derivative_filter[control_variable] = (alpha * raw_derivative + 
                                                      (1 - alpha) * self.previous_derivative[control_variable])
            
            self.previous_derivative[control_variable] = self.derivative_filter[control_variable]
            
            # Calculate PID output
            proportional = self.kp * error
            integral = self.ki * self.state.integral_errors[control_variable]
            derivative = self.kd * self.derivative_filter[control_variable]
            
            output = proportional + integral + derivative
            
            # Apply deadband
            if abs(error) < self.config.control_deadband:
                output = 0.0
            
            outputs[control_variable] = output
        
        # Store current error for next iteration
        self.state.errors = {k: setpoints[k] - measurements.get(k, 0.0) for k in setpoints}
        
        return outputs


class LoadFollowingController(BaseControlStrategy):
    """Load following controller for power systems.
    
    This controller manages the balance between generation and load
    by adjusting generation setpoints based on frequency and power deviations.
    """
    
    def __init__(self, config: ControlConfig):
        """Initialize load following controller.
        
        Parameters
        ----------
        config : ControlConfig
            Load following controller configuration
        """
        super().__init__(config)
        
        # Load following parameters
        self.nominal_frequency = config.metadata.get('nominal_frequency', 50.0)
        self.frequency_bias = config.metadata.get('frequency_bias', 0.05)
        self.power_bias = config.metadata.get('power_bias', 0.02)
        self.ramp_rate_limit = config.metadata.get('ramp_rate_limit', 0.1)  # MW/min
        self.min_generation = config.metadata.get('min_generation', 0.0)
        self.max_generation = config.metadata.get('max_generation', 1.0)
        
        # AGC parameters
        self.use_agc = config.metadata.get('use_agc', False)
        self.agc_time_constant = config.metadata.get('agc_time_constant', 10.0)
        
    def calculate_control_output(self, 
                               setpoints: Dict[str, float],
                               measurements: Dict[str, float],
                               external_inputs: Dict[str, float],
                               time_step: float) -> Dict[str, float]:
        """Calculate load following control output.
        
        Parameters
        ----------
        setpoints : Dict[str, float]
            Target setpoints
        measurements : Dict[str, float]
            Current measurements
        external_inputs : Dict[str, float]
            External input signals
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Dict[str, float]
            Control outputs
        """
        outputs = {}
        
        # Get system measurements
        system_frequency = measurements.get('system_frequency', self.nominal_frequency)
        total_load = measurements.get('total_load', 0.0)
        total_generation = measurements.get('total_generation', 0.0)
        frequency_deviation = system_frequency - self.nominal_frequency
        
        # Calculate power imbalance
        power_imbalance = total_load - total_generation
        
        # Primary frequency control (droop characteristic)
        primary_control_output = -self.frequency_bias * frequency_deviation
        
        # Secondary control (power imbalance correction)
        secondary_control_output = -self.power_bias * power_imbalance
        
        # Combine control actions
        total_control_output = primary_control_output + secondary_control_output
        
        # Apply ramp rate limits
        if 'generation_setpoint' in self.state.setpoints:
            current_setpoint = self.state.setpoints['generation_setpoint']
            max_ramp_change = self.ramp_rate_limit * time_step / 60.0  # Convert MW/min to per time step
            
            ramp_limited_output = max(
                current_setpoint - max_ramp_change,
                min(current_setpoint + max_ramp_change, total_control_output)
            )
        else:
            ramp_limited_output = total_control_output
        
        # Apply generation limits
        final_output = max(self.min_generation, 
                          min(self.max_generation, ramp_limited_output))
        
        # Set output for generation units
        outputs['generation_adjustment'] = final_output
        
        # Individual generator control if multiple generators
        if 'generator_units' in measurements:
            generator_units = measurements['generator_units']
            if isinstance(generator_units, dict):
                total_capacity = sum(gen.get('capacity', 1.0) for gen in generator_units.values())
                if total_capacity > 0:
                    # Distribute control based on generator capacity
                    for gen_id, gen_data in generator_units.items():
                        gen_capacity = gen_data.get('capacity', 1.0)
                        gen_share = gen_capacity / total_capacity
                        outputs[f'gen_{gen_id}_adjustment'] = final_output * gen_share
        
        return outputs


class EconomicDispatchController(BaseControlStrategy):
    """Economic dispatch controller for optimal power flow.
    
    This controller optimizes generation dispatch based on economic factors
    while respecting system constraints.
    """
    
    def __init__(self, config: ControlConfig):
        """Initialize economic dispatch controller.
        
        Parameters
        ----------
        config : ControlConfig
            Economic dispatch controller configuration
        """
        super().__init__(config)
        
        # Economic dispatch parameters
        self.merit_order = config.metadata.get('merit_order', True)
        self.lambda_iteration_limit = config.metadata.get('lambda_iteration_limit', 100)
        self.tolerance = config.metadata.get('tolerance', 0.01)
        
        # Generator cost parameters
        self.cost_functions = config.metadata.get('cost_functions', {})
        
    def calculate_control_output(self, 
                               setpoints: Dict[str, float],
                               measurements: Dict[str, float],
                               external_inputs: Dict[str, float],
                               time_step: float) -> Dict[str, float]:
        """Calculate economic dispatch control output.
        
        Parameters
        ----------
        setpoints : Dict[str, float]
            Target setpoints
        measurements : Dict[str, float]
            Current measurements
        external_inputs : Dict[str, float]
            External input signals
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Dict[str, float]
            Control outputs
        """
        outputs = {}
        
        # Get system data
        total_load = measurements.get('total_load', 0.0)
        generator_units = measurements.get('generator_units', {})
        
        if not generator_units:
            return outputs
        
        # Economic dispatch calculation
        if self.merit_order:
            # Merit order dispatch (simplified)
            generators_sorted = self._sort_generators_by_cost(generator_units)
            dispatch = self._dispatch_by_merit_order(total_load, generators_sorted)
        else:
            # Lambda iteration method
            dispatch = self._lambda_iteration_dispatch(total_load, generator_units)
        
        # Generate control actions for each generator
        for gen_id, dispatch_power in dispatch.items():
            outputs[f'gen_{gen_id}_setpoint'] = dispatch_power
        
        return outputs
    
    def _sort_generators_by_cost(self, generators: Dict[str, Dict]) -> List[Tuple[str, float]]:
        """Sort generators by merit order (cost).
        
        Parameters
        ----------
        generators : Dict[str, Dict]
            Generator data
            
        Returns
        -------
        List[Tuple[str, float]]
            List of (generator_id, cost) tuples sorted by cost
        """
        generator_costs = []
        
        for gen_id, gen_data in generators.items():
            # Get cost function coefficients
            cost_coeffs = self.cost_functions.get(gen_id, {'a': 0.01, 'b': 25.0, 'c': 100.0})
            
            # Calculate marginal cost at current operating point
            current_output = gen_data.get('current_output', 0.0)
            marginal_cost = (2 * cost_coeffs['a'] * current_output + 
                           cost_coeffs['b'])
            
            generator_costs.append((gen_id, marginal_cost))
        
        # Sort by marginal cost (lowest first)
        generator_costs.sort(key=lambda x: x[1])
        
        return generator_costs
    
    def _dispatch_by_merit_order(self, total_load: float, 
                                sorted_generators: List[Tuple[str, float]]) -> Dict[str, float]:
        """Dispatch generation based on merit order.
        
        Parameters
        ----------
        total_load : float
            Total system load
        sorted_generators : List[Tuple[str, float]]
            Generators sorted by merit order
            
        Returns
        -------
        Dict[str, float]
            Dispatch for each generator
        """
        dispatch = {}
        remaining_load = total_load
        
        for gen_id, _ in sorted_generators:
            # Get generator limits (simplified - assume from measurements)
            max_capacity = 100.0  # Default capacity
            min_capacity = 0.0    # Minimum output
            
            # Dispatch generator
            dispatched = min(remaining_load, max_capacity)
            dispatched = max(min_capacity, dispatched)
            
            dispatch[gen_id] = dispatched
            remaining_load -= dispatched
            
            if remaining_load <= 0:
                break
        
        return dispatch
    
    def _lambda_iteration_dispatch(self, total_load: float, 
                                  generators: Dict[str, Dict]) -> Dict[str, float]:
        """Perform lambda iteration for economic dispatch.
        
        Parameters
        ----------
        total_load : float
            Total system load
        generators : Dict[str, float]
            Generator data
            
        Returns
        -------
        Dict[str, float]
            Dispatch for each generator
        """
        # Initialize lambda (system lambda)
        lambda_value = 30.0  # Initial guess
        
        # Iterative solution
        for iteration in range(self.lambda_iteration_limit):
            dispatch = {}
            total_generation = 0.0
            
            # Calculate dispatch for each generator
            for gen_id, gen_data in generators.items():
                cost_coeffs = self.cost_functions.get(gen_id, {'a': 0.01, 'b': 25.0, 'c': 100.0})
                
                # Calculate optimal output for given lambda
                if cost_coeffs['a'] > 0:
                    optimal_output = (lambda_value - cost_coeffs['b']) / (2 * cost_coeffs['a'])
                else:
                    optimal_output = 0.0
                
                # Apply limits
                max_capacity = gen_data.get('max_capacity', 100.0)
                min_capacity = gen_data.get('min_capacity', 0.0)
                
                optimal_output = max(min_capacity, min(max_capacity, optimal_output))
                
                dispatch[gen_id] = optimal_output
                total_generation += optimal_output
            
            # Check convergence
            error = abs(total_generation - total_load)
            if error < self.tolerance:
                break
            
            # Update lambda
            generation_diff = total_generation - total_load
            lambda_value -= generation_diff * 0.1  # Simple gradient descent
        
        return dispatch


class FrequencyController(BaseControlStrategy):
    """Frequency control strategy for power systems.
    
    This controller maintains system frequency within acceptable limits
    through primary and secondary frequency control.
    """
    
    def __init__(self, config: ControlConfig):
        """Initialize frequency controller.
        
        Parameters
        ----------
        config : ControlConfig
            Frequency controller configuration
        """
        super().__init__(config)
        
        # Frequency control parameters
        self.nominal_frequency = config.metadata.get('nominal_frequency', 50.0)
        self.primary_droop = config.metadata.get('primary_droop', 0.05)
        self.secondary_time_constant = config.metadata.get('secondary_time_constant', 30.0)
        self.tertiary_response_time = config.metadata.get('tertiary_response_time', 600.0)
        
        # Frequency limits
        self.frequency_deviation_limit = config.metadata.get('frequency_deviation_limit', 0.5)  # Hz
        self.under_frequency_load_shedding = config.metadata.get('ufls_levels', [])
        
        # Inertia parameters
        self.system_inertia = config.metadata.get('system_inertia', 5.0)  # seconds
        self.inertia_constant = config.metadata.get('inertia_constant', 6.0)
        
    def calculate_control_output(self, 
                               setpoints: Dict[str, float],
                               measurements: Dict[str, float],
                               external_inputs: Dict[str, float],
                               time_step: float) -> Dict[str, float]:
        """Calculate frequency control output.
        
        Parameters
        ----------
        setpoints : Dict[str, float]
            Target setpoints
        measurements : Dict[str, float]
            Current measurements
        external_inputs : Dict[str, float]
            External input signals
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Dict[str, float]
            Control outputs
        """
        outputs = {}
        
        # Get system measurements
        system_frequency = measurements.get('system_frequency', self.nominal_frequency)
        frequency_deviation = system_frequency - self.nominal_frequency
        total_generation = measurements.get('total_generation', 0.0)
        total_load = measurements.get('total_load', 0.0)
        
        # Primary frequency control (droop)
        primary_control = -frequency_deviation / self.primary_droop
        
        # Secondary frequency control (AGC)
        if 'frequency_error' not in self.state.integral_errors:
            self.state.integral_errors['frequency_error'] = 0.0
        
        # Update frequency error integral
        self.state.integral_errors['frequency_error'] += frequency_deviation * time_step
        
        # Secondary control response
        secondary_control = -self.state.integral_errors['frequency_error'] / self.secondary_time_constant
        
        # Total frequency control
        total_control = primary_control + secondary_control
        
        # Apply frequency deviation limits
        if abs(frequency_deviation) > self.frequency_deviation_limit:
            # Emergency frequency control
            emergency_control = self._emergency_frequency_control(frequency_deviation, total_generation)
            outputs['emergency_frequency_control'] = emergency_control
        else:
            # Normal frequency control
            outputs['frequency_control'] = total_control
        
        # Under-frequency load shedding
        if system_frequency < self.nominal_frequency - 0.5:
            ufls_action = self._under_frequency_load_shedding(system_frequency)
            if ufls_action:
                outputs['load_shedding'] = ufls_action
        
        return outputs
    
    def _emergency_frequency_control(self, frequency_deviation: float, 
                                   total_generation: float) -> float:
        """Emergency frequency control for large deviations.
        
        Parameters
        ----------
        frequency_deviation : float
            Frequency deviation in Hz
        total_generation : float
            Current total generation
            
        Returns
        -------
        float
            Emergency control output
        """
        # Fast generation increase for under-frequency
        if frequency_deviation < -0.5:
            emergency_response = min(0.1 * total_generation, 50.0)  # Max 10% or 50MW
            return emergency_response
        
        # Fast load shedding for over-frequency
        elif frequency_deviation > 0.5:
            emergency_response = -min(0.05 * total_generation, 25.0)  # Max 5% or 25MW
            return emergency_response
        
        return 0.0
    
    def _under_frequency_load_shedding(self, system_frequency: float) -> float:
        """Under-frequency load shedding.
        
        Parameters
        ----------
        system_frequency : float
            Current system frequency
            
        Returns
        -------
        float
            Load to shed as fraction
        """
        # Simplified UFLS logic
        load_to_shed = 0.0
        
        for level in self.under_frequency_load_shedding:
            if system_frequency < level['frequency_threshold']:
                load_to_shed += level['load_fraction']
        
        return load_to_shed


class ControlStrategyFactory:
    """Factory class for creating control strategies."""
    
    @staticmethod
    def create_control_strategy(strategy_type: ControlStrategyType, 
                              config: ControlConfig) -> BaseControlStrategy:
        """Create a control strategy instance.
        
        Parameters
        ----------
        strategy_type : ControlStrategyType
            Type of control strategy
        config : ControlConfig
            Configuration parameters
            
        Returns
        -------
        BaseControlStrategy
            Control strategy instance
        """
        if strategy_type == ControlStrategyType.PID:
            return PIDController(config)
        elif strategy_type == ControlStrategyType.LOAD_FOLLOWING:
            return LoadFollowingController(config)
        elif strategy_type == ControlStrategyType.ECONOMIC_DISPATCH:
            return EconomicDispatchController(config)
        elif strategy_type == ControlStrategyType.FREQUENCY_CONTROL:
            return FrequencyController(config)
        else:
            # Default to PID for unknown types
            return PIDController(config)
    
    @staticmethod
    def get_default_config(strategy_type: ControlStrategyType) -> ControlConfig:
        """Get default configuration for a strategy type.
        
        Parameters
        ----------
        strategy_type : ControlStrategyType
            Strategy type
            
        Returns
        -------
        ControlConfig
            Default configuration
        """
        if strategy_type == ControlStrategyType.PID:
            return ControlConfig(
                strategy_type=strategy_type,
                control_mode=ControlMode.AUTOMATIC,
                sample_time=1.0,
                min_update_interval=0.1,
                max_update_interval=10.0,
                control_deadband=0.02,
                output_limit_min=0.0,
                output_limit_max=1.0,
                enable_feedback=True,
                enable_feedforward=False,
                enable_adaptation=False,
                metadata={'kp': 1.0, 'ki': 0.1, 'kd': 0.05}
            )
        elif strategy_type == ControlStrategyType.LOAD_FOLLOWING:
            return ControlConfig(
                strategy_type=strategy_type,
                control_mode=ControlMode.AUTOMATIC,
                sample_time=2.0,
                min_update_interval=0.5,
                max_update_interval=60.0,
                control_deadband=0.01,
                output_limit_min=-1.0,
                output_limit_max=1.0,
                enable_feedback=True,
                enable_feedforward=True,
                metadata={
                    'nominal_frequency': 50.0,
                    'frequency_bias': 0.05,
                    'power_bias': 0.02,
                    'ramp_rate_limit': 0.1
                }
            )
        elif strategy_type == ControlStrategyType.FREQUENCY_CONTROL:
            return ControlConfig(
                strategy_type=strategy_type,
                control_mode=ControlMode.AUTOMATIC,
                sample_time=0.5,
                min_update_interval=0.1,
                max_update_interval=5.0,
                control_deadband=0.001,
                output_limit_min=-1.0,
                output_limit_max=1.0,
                enable_feedback=True,
                enable_feedforward=False,
                metadata={
                    'nominal_frequency': 50.0,
                    'primary_droop': 0.05,
                    'secondary_time_constant': 30.0,
                    'frequency_deviation_limit': 0.5
                }
            )
        else:
            # Default configuration
            return ControlConfig(
                strategy_type=strategy_type,
                control_mode=ControlMode.AUTOMATIC,
                sample_time=1.0,
                min_update_interval=0.1,
                max_update_interval=60.0,
                control_deadband=0.02,
                output_limit_min=0.0,
                output_limit_max=1.0,
                enable_feedback=True
            )


# Define __all__ for module exports
__all__ = [
    # Enumerations
    'ControlStrategyType',
    'ControlMode',
    'ControlStatus',
    
    # Data classes
    'ControlAction',
    'ControlConfig',
    'ControlState',
    
    # Abstract base class
    'BaseControlStrategy',
    
    # Concrete implementations
    'PIDController',
    'LoadFollowingController',
    'EconomicDispatchController',
    'FrequencyController',
    
    # Factory
    'ControlStrategyFactory'
]