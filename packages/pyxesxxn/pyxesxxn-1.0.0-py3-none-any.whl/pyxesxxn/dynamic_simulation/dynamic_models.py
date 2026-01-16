"""
Dynamic models for energy system simulation.

This module provides classes and utilities for implementing dynamic models
of various energy system components, including generators, loads, storage,
and control systems. These models capture the time-varying behavior and
interactions within energy systems during simulation.
"""

import abc
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
import logging

import numpy as np
import pandas as pd

try:
    import pypsa
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)

from .base import SimulationState, SimulationConfig, SimulationStatus
from .time_series import TimeSeriesData, TimeSeriesManager


class ModelType(Enum):
    """Dynamic model type enumeration."""
    GENERATOR = "generator"
    LOAD = "load"
    STORAGE = "storage"
    CONVERTER = "converter"
    GRID = "grid"
    CONTROL = "control"
    RENEWABLE = "renewable"


class ModelStatus(Enum):
    """Dynamic model status enumeration."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    FAULT = "fault"
    MAINTENANCE = "maintenance"
    TESTING = "testing"


@dataclass
class ModelConfig:
    """Configuration for dynamic models.
    
    This class encapsulates all configuration parameters for a dynamic model,
    including model parameters, initialization values, and simulation settings.
    """
    
    # Basic model parameters
    model_id: str
    model_type: ModelType
    name: str
    component_id: Optional[str] = None
    
    # Physical parameters
    capacity: float = 0.0  # MW or MWh
    efficiency: float = 1.0
    ramp_rate: float = float('inf')  # MW/min
    response_time: float = 0.0  # seconds
    
    # Initialization parameters
    initial_power: float = 0.0  # MW
    initial_state_of_charge: float = 0.0  # for storage
    initial_voltage: float = 1.0  # p.u.
    initial_frequency: float = 50.0  # Hz
    
    # Operational limits
    min_power: float = 0.0  # MW
    max_power: float = 0.0  # MW
    min_voltage: float = 0.95  # p.u.
    max_voltage: float = 1.05  # p.u.
    min_frequency: float = 49.5  # Hz
    max_frequency: float = 50.5  # Hz
    
    # Control parameters
    kp: float = 0.0  # Proportional gain
    ki: float = 0.0  # Integral gain
    kd: float = 0.0  # Derivative gain
    setpoint: float = 0.0
    deadband: float = 0.0  # Hz for frequency regulation
    
    # State variables
    state_variables: List[str] = field(default_factory=list)
    control_variables: List[str] = field(default_factory=list)
    
    # Data requirements
    required_time_series: List[str] = field(default_factory=list)
    
    # Model-specific parameters
    custom_parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Performance parameters
    convergence_tolerance: float = 1e-6
    max_iterations: int = 100
    
    def validate(self) -> List[str]:
        """Validate model configuration.
        
        Returns
        -------
        List[str]
            List of validation errors
        """
        errors = []
        
        # Check basic parameters
        if not self.model_id:
            errors.append("Model ID must be specified")
        
        if not self.name:
            errors.append("Model name must be specified")
        
        # Check power limits
        if self.min_power < 0:
            errors.append("Minimum power cannot be negative")
        
        if self.max_power < self.min_power:
            errors.append("Maximum power must be greater than minimum power")
        
        if self.initial_power < self.min_power or self.initial_power > self.max_power:
            errors.append("Initial power must be within operational limits")
        
        # Check efficiency
        if not 0 <= self.efficiency <= 1:
            errors.append("Efficiency must be between 0 and 1")
        
        # Check ramp rate
        if self.ramp_rate <= 0:
            errors.append("Ramp rate must be positive")
        
        # Check voltage limits
        if self.min_voltage <= 0 or self.max_voltage <= 0:
            errors.append("Voltage limits must be positive")
        
        if self.min_voltage >= self.max_voltage:
            errors.append("Minimum voltage must be less than maximum voltage")
        
        # Check frequency limits
        if self.min_frequency <= 0 or self.max_frequency <= 0:
            errors.append("Frequency limits must be positive")
        
        if self.min_frequency >= self.max_frequency:
            errors.append("Minimum frequency must be less than maximum frequency")
        
        return errors


class DynamicModel(abc.ABC):
    """Abstract base class for dynamic models.
    
    This class defines the interface and common functionality for all
    dynamic models used in energy system simulations.
    """
    
    def __init__(self, config: ModelConfig, initial_state: Optional[SimulationState] = None):
        """Initialize dynamic model.
        
        Parameters
        ----------
        config : ModelConfig
            Model configuration
        initial_state : SimulationState, optional
            Initial simulation state
        """
        self.config = config
        self.initial_state = initial_state
        
        # Validate configuration
        validation_errors = config.validate()
        if validation_errors:
            raise ValueError(f"Invalid model configuration: {validation_errors}")
        
        # Initialize logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Model state
        self.status = ModelStatus.INACTIVE
        self.current_state = {}
        self.previous_state = {}
        self.state_derivatives = {}
        
        # Control variables
        self.control_inputs = {}
        self.output_variables = {}
        
        # Performance tracking
        self.convergence_history = []
        self.computation_times = []
        self.error_history = []
        
        # Initialize state variables
        self._initialize_state()
        
        # Register with initial state if provided
        if initial_state:
            self._register_with_simulation_state(initial_state)
    
    def _initialize_state(self) -> None:
        """Initialize model state variables."""
        # Initialize state variables
        for var in self.config.state_variables:
            self.current_state[var] = self._get_initial_value(var)
            self.previous_state[var] = self.current_state[var]
        
        # Initialize control variables
        for var in self.config.control_variables:
            self.control_inputs[var] = self._get_initial_control_value(var)
        
        # Initialize output variables
        self.output_variables = {
            'power': self.config.initial_power,
            'voltage': self.config.initial_voltage,
            'frequency': self.config.initial_frequency,
            'efficiency': self.config.efficiency,
            'status': self.status.value
        }
    
    def _get_initial_value(self, variable: str) -> float:
        """Get initial value for state variable.
        
        Parameters
        ----------
        variable : str
            Variable name
            
        Returns
        -------
        float
            Initial value
        """
        # Default initial values based on variable type
        initial_values = {
            'power': self.config.initial_power,
            'voltage': self.config.initial_voltage,
            'frequency': self.config.initial_frequency,
            'state_of_charge': self.config.initial_state_of_charge,
            'temperature': 20.0,  # Default ambient temperature
            'current': 0.0,
            'reactivity': 1.0,
            'inertia': 5.0
        }
        
        return initial_values.get(variable, 0.0)
    
    def _get_initial_control_value(self, variable: str) -> float:
        """Get initial value for control variable.
        
        Parameters
        ----------
        variable : str
            Control variable name
            
        Returns
        -------
        float
            Initial control value
        """
        initial_values = {
            'setpoint': self.config.setpoint,
            'reference': 1.0,
            'command': 0.0,
            'feedback': 0.0,
            'error': 0.0,
            'derivative': 0.0,
            'integral': 0.0
        }
        
        return initial_values.get(variable, 0.0)
    
    def _register_with_simulation_state(self, sim_state: SimulationState) -> None:
        """Register model with simulation state.
        
        Parameters
        ----------
        sim_state : SimulationState
            Simulation state
        """
        # Add model-specific state variables to simulation state
        if self.config.component_id:
            # Update generator states
            if self.config.model_type == ModelType.GENERATOR:
                sim_state.generator_states[self.config.component_id] = self.config.initial_power
            
            # Update storage states
            elif self.config.model_type == ModelType.STORAGE:
                sim_state.storage_states[self.config.component_id] = self.config.initial_state_of_charge
    
    def get_state(self, variable: str, default: float = 0.0) -> float:
        """Get current state variable value.
        
        Parameters
        ----------
        variable : str
            Variable name
        default : float
            Default value if variable not found
            
        Returns
        -------
        float
            Variable value
        """
        return self.current_state.get(variable, default)
    
    def set_state(self, variable: str, value: float) -> None:
        """Set state variable value.
        
        Parameters
        ----------
        variable : str
            Variable name
        value : float
            Variable value
        """
        self.current_state[variable] = value
    
    def get_control_input(self, variable: str, default: float = 0.0) -> float:
        """Get control input value.
        
        Parameters
        ----------
        variable : str
            Control variable name
        default : float
            Default value if variable not found
            
        Returns
        -------
        float
            Control input value
        """
        return self.control_inputs.get(variable, default)
    
    def set_control_input(self, variable: str, value: float) -> None:
        """Set control input value.
        
        Parameters
        ----------
        variable : str
            Control variable name
        value : float
            Variable value
        """
        self.control_inputs[variable] = value
    
    def get_output(self, variable: str, default: float = 0.0) -> float:
        """Get output variable value.
        
        Parameters
        ----------
        variable : str
            Output variable name
        default : float
            Default value if variable not found
            
        Returns
        -------
        float
            Output value
        """
        return self.output_variables.get(variable, default)
    
    def set_output(self, variable: str, value: float) -> None:
        """Set output variable value.
        
        Parameters
        ----------
        variable : str
            Output variable name
        value : float
            Variable value
        """
        self.output_variables[variable] = value
    
    # Abstract methods to be implemented by subclasses
    @abc.abstractmethod
    def update_model(self, 
                    time_step: float,
                    external_inputs: Dict[str, float],
                    time_series_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update model for one time step.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
        external_inputs : Dict[str, float]
            External input values
        time_series_data : Dict[str, Any], optional
            Time series data for current step
            
        Returns
        -------
        bool
            True if update successful
        """
        pass
    
    @abc.abstractmethod
    def calculate_derivatives(self) -> Dict[str, float]:
        """Calculate state variable derivatives.
        
        Returns
        -------
        Dict[str, float]
            State variable derivatives
        """
        pass
    
    @abc.abstractmethod
    def apply_constraints(self) -> List[str]:
        """Apply operational constraints.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        pass
    
    # Utility methods
    def activate(self) -> bool:
        """Activate the model.
        
        Returns
        -------
        bool
            True if successfully activated
        """
        try:
            self.status = ModelStatus.ACTIVE
            self.set_output('status', self.status.value)
            return True
        except Exception as e:
            self.logger.error(f"Failed to activate model: {e}")
            return False
    
    def deactivate(self) -> bool:
        """Deactivate the model.
        
        Returns
        -------
        bool
            True if successfully deactivated
        """
        try:
            self.status = ModelStatus.INACTIVE
            self.set_output('status', self.status.value)
            return True
        except Exception as e:
            self.logger.error(f"Failed to deactivate model: {e}")
            return False
    
    def set_fault(self, fault_type: str) -> bool:
        """Set model to fault state.
        
        Parameters
        ----------
        fault_type : str
            Fault type description
            
        Returns
        -------
        bool
            True if fault set successfully
        """
        try:
            self.status = ModelStatus.FAULT
            self.set_output('status', self.status.value)
            self.set_output('fault_type', fault_type)
            return True
        except Exception as e:
            self.logger.error(f"Failed to set fault: {e}")
            return False
    
    def check_limits(self, power: float, voltage: float, frequency: float) -> List[str]:
        """Check if values are within operational limits.
        
        Parameters
        ----------
        power : float
            Power output
        voltage : float
            Voltage level
        frequency : float
            System frequency
            
        Returns
        -------
        List[str]
            List of limit violations
        """
        violations = []
        
        if power < self.config.min_power:
            violations.append(f"Power below minimum: {power} < {self.config.min_power}")
        elif power > self.config.max_power:
            violations.append(f"Power above maximum: {power} > {self.config.max_power}")
        
        if voltage < self.config.min_voltage:
            violations.append(f"Voltage below minimum: {voltage} < {self.config.min_voltage}")
        elif voltage > self.config.max_voltage:
            violations.append(f"Voltage above maximum: {voltage} > {self.config.max_voltage}")
        
        if frequency < self.config.min_frequency:
            violations.append(f"Frequency below minimum: {frequency} < {self.config.min_frequency}")
        elif frequency > self.config.max_frequency:
            violations.append(f"Frequency above maximum: {frequency} > {self.config.max_frequency}")
        
        return violations
    
    def calculate_efficiency(self, input_power: float, output_power: float) -> float:
        """Calculate model efficiency.
        
        Parameters
        ----------
        input_power : float
            Input power
        output_power : float
            Output power
            
        Returns
        -------
        float
            Efficiency value
        """
        if input_power <= 0:
            return 1.0
        
        efficiency = output_power / input_power
        return max(0.0, min(1.0, efficiency))
    
    def apply_ramp_rate(self, current_power: float, target_power: float, time_step: float) -> float:
        """Apply ramp rate constraints.
        
        Parameters
        ----------
        current_power : float
            Current power output
        target_power : float
            Target power output
        time_step : float
            Time step in minutes
            
        Returns
        -------
        float
            Ramped power output
        """
        if not np.isfinite(self.config.ramp_rate):
            return target_power
        
        max_power_change = self.config.ramp_rate * time_step / 60.0  # Convert to MW
        
        if abs(target_power - current_power) <= max_power_change:
            return target_power
        else:
            if target_power > current_power:
                return current_power + max_power_change
            else:
                return current_power - max_power_change
    
    def log_performance_metrics(self) -> None:
        """Log current performance metrics."""
        self.logger.info(f"Model {self.config.name} ({self.config.model_id}): "
                        f"Status: {self.status.value}, "
                        f"Power: {self.get_output('power'):.2f} MW, "
                        f"Voltage: {self.get_output('voltage'):.3f} p.u., "
                        f"Efficiency: {self.get_output('efficiency'):.3f}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get model summary.
        
        Returns
        -------
        Dict[str, Any]
            Model summary
        """
        return {
            'model_id': self.config.model_id,
            'name': self.config.name,
            'type': self.config.model_type.value,
            'status': self.status.value,
            'capacity': self.config.capacity,
            'current_power': self.get_output('power'),
            'voltage': self.get_output('voltage'),
            'frequency': self.get_output('frequency'),
            'efficiency': self.get_output('efficiency'),
            'convergence_iterations': len(self.convergence_history),
            'average_computation_time': np.mean(self.computation_times) if self.computation_times else 0.0
        }
    
    def __repr__(self) -> str:
        """String representation of model."""
        return (f"{self.__class__.__name__}(id='{self.config.model_id}', "
                f"name='{self.config.name}', "
                f"type='{self.config.model_type.value}', "
                f"status='{self.status.value}')")


class GeneratorModel(DynamicModel):
    """Dynamic generator model.
    
    This class implements a simplified dynamic model for power generators,
    including frequency response and power control.
    """
    
    def __init__(self, config: ModelConfig, initial_state: Optional[SimulationState] = None):
        """Initialize generator model.
        
        Parameters
        ----------
        config : ModelConfig
            Model configuration
        initial_state : SimulationState, optional
            Initial simulation state
        """
        # Set default state variables for generator
        config.state_variables.extend(['rotor_angle', 'angular_velocity', 'field_voltage'])
        config.control_variables.extend(['setpoint', 'frequency_deviation'])
        
        super().__init__(config, initial_state)
        
        # Generator-specific parameters
        self.governor_time_constant = 2.0  # seconds
        self.inertia_constant = 5.0  # seconds
        self.damping_coefficient = 0.1
        
        # Initialize specific states
        self.set_state('rotor_angle', 0.0)
        self.set_state('angular_velocity', 1.0)  # p.u.
        self.set_state('field_voltage', self.config.initial_voltage)
        self.set_control_input('frequency_deviation', 0.0)
    
    def update_model(self, 
                    time_step: float,
                    external_inputs: Dict[str, float],
                    time_series_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update generator model.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
        external_inputs : Dict[str, float]
            External input values
        time_series_data : Dict[str, Any], optional
            Time series data
            
        Returns
        -------
        bool
            True if update successful
        """
        try:
            start_time = datetime.now()
            
            # Get external inputs
            system_frequency = external_inputs.get('system_frequency', 50.0)
            system_voltage = external_inputs.get('system_voltage', 1.0)
            load_demand = external_inputs.get('load_demand', 0.0)
            
            # Update control inputs
            frequency_deviation = system_frequency - 50.0  # Nominal frequency
            self.set_control_input('frequency_deviation', frequency_deviation)
            
            # Calculate power output with governor response
            if abs(frequency_deviation) > self.config.deadband:
                # Primary frequency response
                power_change = -self.config.kp * frequency_deviation
                new_power = self.get_state('power') + power_change
            else:
                new_power = self.config.setpoint
            
            # Apply ramp rate constraints
            current_power = self.get_output('power')
            new_power = self.apply_ramp_rate(current_power, new_power, time_step / 60.0)
            
            # Apply power limits
            new_power = max(self.config.min_power, min(self.config.max_power, new_power))
            
            # Update rotor dynamics
            delta_omega = (-frequency_deviation / self.inertia_constant - 
                          self.damping_coefficient * (self.get_state('angular_velocity') - 1.0))
            
            new_angular_velocity = self.get_state('angular_velocity') + delta_omega * time_step
            new_angular_velocity = max(0.9, min(1.1, new_angular_velocity))  # Keep within reasonable limits
            
            # Update states
            self.set_state('power', new_power)
            self.set_state('angular_velocity', new_angular_velocity)
            self.set_state('rotor_angle', self.get_state('rotor_angle') + 
                          2 * np.pi * (new_angular_velocity - 1.0) * time_step)
            
            # Calculate efficiency
            efficiency = self.calculate_efficiency(self.config.capacity * 0.9, new_power)
            
            # Update outputs
            self.set_output('power', new_power)
            self.set_output('voltage', system_voltage)
            self.set_output('frequency', system_frequency)
            self.set_output('efficiency', efficiency)
            self.set_output('angular_velocity', new_angular_velocity)
            
            # Track performance
            computation_time = (datetime.now() - start_time).total_seconds()
            self.computation_times.append(computation_time)
            
            # Check convergence
            power_error = abs(new_power - current_power)
            self.convergence_history.append(power_error)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Generator model update failed: {e}")
            return False
    
    def calculate_derivatives(self) -> Dict[str, float]:
        """Calculate generator state derivatives.
        
        Returns
        -------
        Dict[str, float]
            State derivatives
        """
        frequency_deviation = self.get_control_input('frequency_deviation')
        
        derivatives = {
            'rotor_angle': 2 * np.pi * (self.get_state('angular_velocity') - 1.0),
            'angular_velocity': (-frequency_deviation / self.inertia_constant - 
                               self.damping_coefficient * (self.get_state('angular_velocity') - 1.0)),
            'field_voltage': 0.0,  # Simplified
            'power': -self.config.kp * frequency_deviation
        }
        
        return derivatives
    
    def apply_constraints(self) -> List[str]:
        """Apply generator constraints.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        violations = []
        
        # Check power limits
        power = self.get_output('power')
        violations.extend(self.check_limits(power, self.get_output('voltage'), self.get_output('frequency')))
        
        # Check rotor speed limits
        angular_velocity = self.get_state('angular_velocity')
        if not 0.9 <= angular_velocity <= 1.1:
            violations.append(f"Rotor speed out of limits: {angular_velocity} p.u.")
        
        return violations


class LoadModel(DynamicModel):
    """Dynamic load model.
    
    This class implements a dynamic model for electrical loads,
    including frequency and voltage dependency.
    """
    
    def __init__(self, config: ModelConfig, initial_state: Optional[SimulationState] = None):
        """Initialize load model.
        
        Parameters
        ----------
        config : ModelConfig
            Model configuration
        initial_state : SimulationState, optional
            Initial simulation state
        """
        # Set default state variables for load
        config.state_variables.extend(['active_power', 'reactive_power'])
        config.control_variables.extend(['demand_factor'])
        
        super().__init__(config, initial_state)
        
        # Load-specific parameters
        self.voltage_coefficient = 1.0  # Voltage dependency exponent
        self.frequency_coefficient = 0.5  # Frequency dependency exponent
        self.temperature_coefficient = 0.2  # Temperature dependency
        
        # Initialize specific states
        self.set_state('active_power', self.config.initial_power)
        self.set_state('reactive_power', self.config.initial_power * 0.6)  # Assume PF = 0.8
        self.set_control_input('demand_factor', 1.0)
    
    def update_model(self, 
                    time_step: float,
                    external_inputs: Dict[str, float],
                    time_series_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update load model.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
        external_inputs : Dict[str, float]
            External input values
        time_series_data : Dict[str, Any], optional
            Time series data
            
        Returns
        -------
        bool
            True if update successful
        """
        try:
            start_time = datetime.now()
            
            # Get external inputs
            system_voltage = external_inputs.get('system_voltage', 1.0)
            system_frequency = external_inputs.get('system_frequency', 50.0)
            ambient_temperature = external_inputs.get('ambient_temperature', 20.0)
            
            # Get time series data if available
            if time_series_data:
                demand_multiplier = time_series_data.get('demand_multiplier', 1.0)
                if 'load' in time_series_data:
                    base_demand = time_series_data['load']
                else:
                    base_demand = self.config.initial_power
            else:
                base_demand = self.config.initial_power
                demand_multiplier = self.get_control_input('demand_factor')
            
            # Calculate voltage dependency
            voltage_factor = (system_voltage ** self.voltage_coefficient)
            
            # Calculate frequency dependency
            frequency_factor = (system_frequency / 50.0) ** self.frequency_coefficient
            
            # Calculate temperature dependency
            temperature_factor = 1.0 + self.temperature_coefficient * (ambient_temperature - 20.0) / 20.0
            
            # Calculate total demand
            total_demand = (base_demand * demand_multiplier * voltage_factor * 
                          frequency_factor * temperature_factor)
            
            # Apply load limits
            total_demand = max(0.0, min(self.config.max_power, total_demand))
            
            # Update states
            self.set_state('active_power', total_demand)
            
            # Assume constant power factor for reactive power
            power_factor = 0.8
            reactive_power = total_demand * np.sqrt(1 - power_factor**2) / power_factor
            self.set_state('reactive_power', reactive_power)
            
            # Update control inputs
            self.set_control_input('demand_factor', demand_multiplier)
            
            # Update outputs
            self.set_output('power', total_demand)
            self.set_output('voltage', system_voltage)
            self.set_output('frequency', system_frequency)
            self.set_output('efficiency', 1.0)  # Loads don't have efficiency in traditional sense
            
            # Track performance
            computation_time = (datetime.now() - start_time).total_seconds()
            self.computation_times.append(computation_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Load model update failed: {e}")
            return False
    
    def calculate_derivatives(self) -> Dict[str, float]:
        """Calculate load state derivatives.
        
        Returns
        -------
        Dict[str, float]
            State derivatives
        """
        # For load models, derivatives are typically small (assuming relatively constant loads)
        return {
            'active_power': 0.0,
            'reactive_power': 0.0
        }
    
    def apply_constraints(self) -> List[str]:
        """Apply load constraints.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        violations = []
        
        # Check that load doesn't exceed limits
        active_power = self.get_state('active_power')
        if active_power > self.config.max_power:
            violations.append(f"Load power exceeds maximum: {active_power} > {self.config.max_power}")
        
        return violations


class StorageModel(DynamicModel):
    """Dynamic storage model.
    
    This class implements a dynamic model for energy storage systems,
    including state of charge dynamics and charge/discharge control.
    """
    
    def __init__(self, config: ModelConfig, initial_state: Optional[SimulationState] = None):
        """Initialize storage model.
        
        Parameters
        ----------
        config : ModelConfig
            Model configuration
        initial_state : SimulationState, optional
            Initial simulation state
        """
        # Set default state variables for storage
        config.state_variables.extend(['state_of_charge', 'charging_power', 'discharging_power'])
        config.control_variables.extend(['charge_command', 'discharge_command'])
        
        super().__init__(config, initial_state)
        
        # Storage-specific parameters
        self.charge_efficiency = config.efficiency
        self.discharge_efficiency = config.efficiency
        self.self_discharge_rate = 0.001  # % per hour
        self.max_charge_rate = config.max_power
        self.max_discharge_rate = config.max_power
        
        # Initialize specific states
        self.set_state('state_of_charge', config.initial_state_of_charge)
        self.set_state('charging_power', 0.0)
        self.set_state('discharging_power', 0.0)
        self.set_control_input('charge_command', 0.0)
        self.set_control_input('discharge_command', 0.0)
    
    def update_model(self, 
                    time_step: float,
                    external_inputs: Dict[str, float],
                    time_series_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update storage model.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
        external_inputs : Dict[str, float]
            External input values
        time_series_data : Dict[str, Any], optional
            Time series data
            
        Returns
        -------
        bool
            True if update successful
        """
        try:
            start_time = datetime.now()
            
            # Get external inputs
            system_frequency = external_inputs.get('system_frequency', 50.0)
            system_voltage = external_inputs.get('system_voltage', 1.0)
            
            # Get control commands
            charge_command = self.get_control_input('charge_command')
            discharge_command = self.get_control_input('discharge_command')
            
            # Apply ramp rate constraints to commands
            time_step_hours = time_step / 3600.0
            charge_rate_limit = self.max_charge_rate * time_step_hours
            discharge_rate_limit = self.max_discharge_rate * time_step_hours
            
            max_charge_change = self.config.ramp_rate * time_step / 60.0
            max_discharge_change = self.config.ramp_rate * time_step / 60.0
            
            current_charge_power = self.get_state('charging_power')
            current_discharge_power = self.get_state('discharging_power')
            
            # Apply ramp rate constraints
            charge_power = self.apply_ramp_rate(current_charge_power, charge_command, time_step / 60.0)
            discharge_power = self.apply_ramp_rate(current_discharge_power, discharge_command, time_step / 60.0)
            
            # Apply power limits
            charge_power = max(0.0, min(charge_rate_limit, charge_power))
            discharge_power = max(0.0, min(discharge_rate_limit, discharge_power))
            
            # Get current state of charge
            soc = self.get_state('state_of_charge')
            
            # Calculate energy changes
            charge_energy = charge_power * time_step_hours * self.charge_efficiency
            discharge_energy = discharge_power * time_step_hours / self.discharge_efficiency
            
            # Apply capacity constraints
            if soc + charge_energy / self.config.capacity > 1.0:
                # Storage full
                charge_power = max(0.0, (1.0 - soc) * self.config.capacity / time_step_hours)
                charge_energy = charge_power * time_step_hours * self.charge_efficiency
            
            if soc - discharge_energy / self.config.capacity < 0.0:
                # Storage empty
                discharge_power = 0.0
                discharge_energy = 0.0
            
            # Apply self-discharge
            self_discharge_energy = soc * self.self_discharge_rate * time_step_hours * self.config.capacity
            
            # Update state of charge
            soc_change = (charge_energy - discharge_energy - self_discharge_energy) / self.config.capacity
            new_soc = max(0.0, min(1.0, soc + soc_change))
            
            # Update states
            self.set_state('state_of_charge', new_soc)
            self.set_state('charging_power', charge_power)
            self.set_state('discharging_power', discharge_power)
            
            # Update control inputs
            self.set_control_input('charge_command', charge_power)
            self.set_control_input('discharge_command', discharge_power)
            
            # Calculate net power (positive for discharge, negative for charge)
            net_power = discharge_power - charge_power
            
            # Update outputs
            self.set_output('power', net_power)
            self.set_output('voltage', system_voltage)
            self.set_output('frequency', system_frequency)
            self.set_output('efficiency', self.charge_efficiency)
            self.set_output('state_of_charge', new_soc)
            
            # Track performance
            computation_time = (datetime.now() - start_time).total_seconds()
            self.computation_times.append(computation_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Storage model update failed: {e}")
            return False
    
    def calculate_derivatives(self) -> Dict[str, float]:
        """Calculate storage state derivatives.
        
        Returns
        -------
        Dict[str, float]
            State derivatives
        """
        time_step = 1.0  # Assuming 1 second for derivative calculation
        
        charge_power = self.get_state('charging_power')
        discharge_power = self.get_state('discharging_power')
        soc = self.get_state('state_of_charge')
        
        # Energy flows per second
        charge_energy_rate = charge_power * self.charge_efficiency / 3600.0  # MW/s
        discharge_energy_rate = discharge_power / (self.discharge_efficiency * 3600.0)  # MW/s
        self_discharge_rate = soc * self.self_discharge_rate / 3600.0  # SOC per second
        
        derivatives = {
            'state_of_charge': charge_energy_rate - discharge_energy_rate - self_discharge_rate,
            'charging_power': 0.0,
            'discharging_power': 0.0
        }
        
        return derivatives
    
    def apply_constraints(self) -> List[str]:
        """Apply storage constraints.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        violations = []
        
        # Check state of charge limits
        soc = self.get_state('state_of_charge')
        if soc < 0.0:
            violations.append(f"State of charge below minimum: {soc}")
        elif soc > 1.0:
            violations.append(f"State of charge above maximum: {soc}")
        
        # Check power limits
        charge_power = self.get_state('charging_power')
        discharge_power = self.get_state('discharging_power')
        
        if charge_power < 0.0:
            violations.append("Negative charging power")
        elif charge_power > self.max_charge_rate:
            violations.append(f"Charging power above maximum: {charge_power} > {self.max_charge_rate}")
        
        if discharge_power < 0.0:
            violations.append("Negative discharging power")
        elif discharge_power > self.max_discharge_rate:
            violations.append(f"Discharging power above maximum: {discharge_power} > {self.max_discharge_rate}")
        
        return violations
    
    def get_available_energy(self) -> float:
        """Get available energy for discharge.
        
        Returns
        -------
        float
            Available energy in MWh
        """
        soc = self.get_state('state_of_charge')
        return soc * self.config.capacity
    
    def get_charge_capacity(self) -> float:
        """Get available capacity for charging.
        
        Returns
        -------
        float
            Available capacity in MWh
        """
        soc = self.get_state('state_of_charge')
        return (1.0 - soc) * self.config.capacity


class RenewableModel(DynamicModel):
    """Dynamic renewable energy model.
    
    This class implements a dynamic model for renewable energy sources,
    including weather-dependent generation.
    """
    
    def __init__(self, config: ModelConfig, initial_state: Optional[SimulationState] = None):
        """Initialize renewable model.
        
        Parameters
        ----------
        config : ModelConfig
            Model configuration
        initial_state : SimulationState, optional
            Initial simulation state
        """
        # Set default state variables for renewable
        config.state_variables.extend(['available_power', 'actual_power'])
        config.control_variables.extend(['availability_factor'])
        
        super().__init__(config, initial_state)
        
        # Renewable-specific parameters
        self.cut_in_speed = 3.0  # m/s for wind
        self.rated_speed = 12.0  # m/s for wind
        self.cut_out_speed = 25.0  # m/s for wind
        self.irradiance_max = 1000.0  # W/m² for solar
        
        # Initialize specific states
        self.set_state('available_power', 0.0)
        self.set_state('actual_power', 0.0)
        self.set_control_input('availability_factor', 1.0)
    
    def update_model(self, 
                    time_step: float,
                    external_inputs: Dict[str, float],
                    time_series_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update renewable model.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
        external_inputs : Dict[str, float]
            External input values
        time_series_data : Dict[str, Any], optional
            Time series data
            
        Returns
        -------
        bool
            True if update successful
        """
        try:
            start_time = datetime.now()
            
            # Get external inputs
            system_frequency = external_inputs.get('system_frequency', 50.0)
            system_voltage = external_inputs.get('system_voltage', 1.0)
            
            # Get weather data from external inputs or time series
            if 'wind_speed' in external_inputs:
                wind_speed = external_inputs['wind_speed']
            elif time_series_data and 'wind_speed' in time_series_data:
                wind_speed = time_series_data['wind_speed']
            else:
                wind_speed = 0.0
            
            if 'solar_irradiance' in external_inputs:
                solar_irradiance = external_inputs['solar_irradiance']
            elif time_series_data and 'solar_irradiance' in time_series_data:
                solar_irradiance = time_series_data['solar_irradiance']
            else:
                solar_irradiance = 0.0
            
            # Get availability factor
            availability = self.get_control_input('availability_factor')
            
            # Calculate available power based on model type
            if self.config.model_type == ModelType.RENEWABLE:
                if 'solar' in self.config.name.lower():
                    # Solar PV model
                    available_power = self._calculate_solar_power(solar_irradiance, availability)
                elif 'wind' in self.config.name.lower():
                    # Wind turbine model
                    available_power = self._calculate_wind_power(wind_speed, availability)
                else:
                    # Generic renewable model
                    available_power = self.config.capacity * availability
            else:
                available_power = self.config.capacity * availability
            
            # Apply ramp rate constraints
            current_power = self.get_output('power')
            new_power = self.apply_ramp_rate(current_power, available_power, time_step / 60.0)
            
            # Apply power limits
            new_power = max(0.0, min(self.config.max_power, new_power))
            
            # Update states
            self.set_state('available_power', available_power)
            self.set_state('actual_power', new_power)
            
            # Update outputs
            self.set_output('power', new_power)
            self.set_output('voltage', system_voltage)
            self.set_output('frequency', system_frequency)
            self.set_output('efficiency', 1.0)  # Renewable sources are typically 100% efficient
            self.set_output('capacity_factor', available_power / self.config.capacity if self.config.capacity > 0 else 0)
            
            # Track performance
            computation_time = (datetime.now() - start_time).total_seconds()
            self.computation_times.append(computation_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Renewable model update failed: {e}")
            return False
    
    def _calculate_solar_power(self, irradiance: float, availability: float) -> float:
        """Calculate solar power output.
        
        Parameters
        ----------
        irradiance : float
            Solar irradiance (W/m²)
        availability : float
            Availability factor
            
        Returns
        -------
        float
            Power output
        """
        # Normalize irradiance
        if self.irradiance_max > 0:
            irradiance_factor = min(1.0, irradiance / self.irradiance_max)
        else:
            irradiance_factor = 0.0
        
        power = self.config.capacity * irradiance_factor * availability
        
        return max(0.0, power)
    
    def _calculate_wind_power(self, wind_speed: float, availability: float) -> float:
        """Calculate wind power output.
        
        Parameters
        ----------
        wind_speed : float
            Wind speed (m/s)
        availability : float
            Availability factor
            
        Returns
        -------
        float
            Power output
        """
        # Wind power curve (simplified)
        if wind_speed < self.cut_in_speed or wind_speed >= self.cut_out_speed:
            power = 0.0
        elif wind_speed >= self.rated_speed:
            power = self.config.capacity
        else:
            # Cubic relationship between cut-in and rated speed
            power = self.config.capacity * ((wind_speed - self.cut_in_speed) / 
                                          (self.rated_speed - self.cut_in_speed)) ** 3
        
        power *= availability
        
        return max(0.0, power)
    
    def calculate_derivatives(self) -> Dict[str, float]:
        """Calculate renewable state derivatives.
        
        Returns
        -------
        Dict[str, float]
            State derivatives
        """
        # Renewable sources typically have slow dynamics
        return {
            'available_power': 0.0,
            'actual_power': 0.0
        }
    
    def apply_constraints(self) -> List[str]:
        """Apply renewable constraints.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        violations = []
        
        # Check power limits
        power = self.get_output('power')
        if power < 0.0:
            violations.append("Negative power output")
        elif power > self.config.max_power:
            violations.append(f"Power output above maximum: {power} > {self.config.max_power}")
        
        # Check capacity factor limits
        capacity_factor = self.get_output('capacity_factor')
        if not 0.0 <= capacity_factor <= 1.0:
            violations.append(f"Capacity factor out of bounds: {capacity_factor}")
        
        return violations


class ControlModel(DynamicModel):
    """Dynamic control system model.
    
    This class implements a dynamic model for control systems,
    including PID controllers and other control algorithms.
    """
    
    def __init__(self, config: ModelConfig, initial_state: Optional[SimulationState] = None):
        """Initialize control model.
        
        Parameters
        ----------
        config : ModelConfig
            Model configuration
        initial_state : SimulationState, optional
            Initial simulation state
        """
        # Set default state variables for control
        config.state_variables.extend(['error', 'integral', 'derivative', 'output'])
        config.control_variables.extend(['reference', 'feedback', 'setpoint'])
        
        super().__init__(config, initial_state)
        
        # Control-specific parameters
        self.kp = config.kp
        self.ki = config.ki
        self.kd = config.kd
        
        # Initialize specific states
        self.set_state('error', 0.0)
        self.set_state('integral', 0.0)
        self.set_state('derivative', 0.0)
        self.set_state('output', 0.0)
        self.set_control_input('reference', config.setpoint)
        self.set_control_input('feedback', 0.0)
        self.set_control_input('setpoint', config.setpoint)
    
    def update_model(self, 
                    time_step: float,
                    external_inputs: Dict[str, float],
                    time_series_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update control model.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
        external_inputs : Dict[str, float]
            External input values
        time_series_data : Dict[str, Any], optional
            Time series data
            
        Returns
        -------
        bool
            True if update successful
        """
        try:
            start_time = datetime.now()
            
            # Get external inputs
            system_frequency = external_inputs.get('system_frequency', 50.0)
            system_voltage = external_inputs.get('system_voltage', 1.0)
            
            # Get control inputs
            reference = self.get_control_input('reference')
            feedback = self.get_control_input('feedback')
            setpoint = self.get_control_input('setpoint')
            
            # Use setpoint as reference if available
            if setpoint != self.config.setpoint:
                reference = setpoint
            
            # Calculate error
            error = reference - feedback
            
            # Update integral and derivative terms
            previous_error = self.get_state('error')
            previous_integral = self.get_state('integral')
            
            # Integral windup protection
            integral = previous_integral + error * time_step
            if self.ki > 0:
                max_integral = self.config.max_power / self.ki if self.config.max_power > 0 else 10.0
                integral = np.clip(integral, -max_integral, max_integral)
            
            # Derivative calculation (with low-pass filter to reduce noise)
            derivative = (error - previous_error) / time_step
            derivative = self._filter_derivative(derivative, self.get_state('derivative'), time_step)
            
            # PID output calculation
            output = (self.kp * error + 
                     self.ki * integral + 
                     self.kd * derivative)
            
            # Apply output limits
            output = np.clip(output, self.config.min_power, self.config.max_power)
            
            # Update states
            self.set_state('error', error)
            self.set_state('integral', integral)
            self.set_state('derivative', derivative)
            self.set_state('output', output)
            
            # Update outputs
            self.set_output('power', output)
            self.set_output('voltage', system_voltage)
            self.set_output('frequency', system_frequency)
            self.set_output('error', error)
            self.set_output('integral', integral)
            self.set_output('derivative', derivative)
            self.set_output('efficiency', 1.0)
            
            # Track performance
            computation_time = (datetime.now() - start_time).total_seconds()
            self.computation_times.append(computation_time)
            
            # Track convergence
            self.convergence_history.append(abs(error))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Control model update failed: {e}")
            return False
    
    def _filter_derivative(self, raw_derivative: float, previous_derivative: float, time_step: float) -> float:
        """Filter derivative to reduce noise.
        
        Parameters
        ----------
        raw_derivative : float
            Raw derivative value
        previous_derivative : float
            Previous filtered derivative
        time_step : float
            Time step
            
        Returns
        -------
        float
            Filtered derivative
        """
        # Simple first-order filter
        alpha = time_step / (time_step + 0.1)  # Filter coefficient
        filtered_derivative = alpha * raw_derivative + (1 - alpha) * previous_derivative
        
        return filtered_derivative
    
    def calculate_derivatives(self) -> Dict[str, float]:
        """Calculate control state derivatives.
        
        Returns
        -------
        Dict[str, float]
            State derivatives
        """
        error = self.get_state('error')
        integral = self.get_state('integral')
        derivative = self.get_state('derivative')
        output = self.get_state('output')
        
        derivatives = {
            'error': 0.0,  # Error is input, not a state
            'integral': error,  # Integral of error
            'derivative': 0.0,  # Derivative is filtered
            'output': self.kp * 0 + self.ki * error + self.kd * 0  # Output derivative
        }
        
        return derivatives
    
    def apply_constraints(self) -> List[str]:
        """Apply control constraints.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        violations = []
        
        # Check output limits
        output = self.get_state('output')
        if output < self.config.min_power:
            violations.append(f"Control output below minimum: {output} < {self.config.min_power}")
        elif output > self.config.max_power:
            violations.append(f"Control output above maximum: {output} > {self.config.max_power}")
        
        # Check for excessive error
        error = self.get_state('error')
        if abs(error) > 10.0:  # Allow large errors but flag them
            violations.append(f"Large control error: {error}")
        
        # Check for integral windup
        integral = self.get_state('integral')
        if abs(integral) > 100.0:  # Arbitrary threshold for integral windup
            violations.append(f"Potential integral windup: {integral}")
        
        return violations


# Utility functions
def create_generator_model(model_id: str,
                          name: str,
                          capacity: float,
                          **kwargs) -> GeneratorModel:
    """Create a generator model with default configuration.
    
    Parameters
    ----------
    model_id : str
        Model identifier
    name : str
        Model name
    capacity : float
        Generator capacity in MW
    **kwargs
        Additional configuration parameters
        
    Returns
    -------
    GeneratorModel
        Configured generator model
    """
    config = ModelConfig(
        model_id=model_id,
        model_type=ModelType.GENERATOR,
        name=name,
        capacity=capacity,
        max_power=capacity,
        min_power=0.0,
        initial_power=capacity * 0.5,  # Start at 50% capacity
        kp=0.05,  # Default governor gain
        ki=0.01,
        kd=0.0,
        ramp_rate=capacity * 0.1  # 10% capacity per minute
    )
    
    # Update with any provided parameters
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return GeneratorModel(config)


def create_load_model(model_id: str,
                     name: str,
                     capacity: float,
                     **kwargs) -> LoadModel:
    """Create a load model with default configuration.
    
    Parameters
    ----------
    model_id : str
        Model identifier
    name : str
        Model name
    capacity : float
        Load capacity in MW
    **kwargs
        Additional configuration parameters
        
    Returns
    -------
    LoadModel
        Configured load model
    """
    config = ModelConfig(
        model_id=model_id,
        model_type=ModelType.LOAD,
        name=name,
        capacity=capacity,
        max_power=capacity,
        initial_power=capacity,
        min_power=0.0
    )
    
    # Update with any provided parameters
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return LoadModel(config)


def create_storage_model(model_id: str,
                        name: str,
                        capacity: float,
                        energy_capacity: float,
                        **kwargs) -> StorageModel:
    """Create a storage model with default configuration.
    
    Parameters
    ----------
    model_id : str
        Model identifier
    name : str
        Model name
    capacity : float
        Power capacity in MW
    energy_capacity : float
        Energy capacity in MWh
    **kwargs
        Additional configuration parameters
        
    Returns
    -------
    StorageModel
        Configured storage model
    """
    config = ModelConfig(
        model_id=model_id,
        model_type=ModelType.STORAGE,
        name=name,
        capacity=capacity,
        efficiency=0.9,  # Round-trip efficiency
        initial_power=0.0,
        initial_state_of_charge=0.5  # 50% initial charge
    )
    
    # Update with any provided parameters
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return StorageModel(config)


# Define imports for compatibility
try:
    from enum import Enum
except ImportError:
    # Fallback for Python < 3.4
    class Enum:
        def __init__(self, *args):
            for item in args:
                setattr(self, item.replace(' ', '_'), item)


# Define __all__ for module exports
__all__ = [
    # Core classes
    'DynamicModel',
    'GeneratorModel',
    'LoadModel',
    'StorageModel',
    'RenewableModel',
    'ControlModel',
    
    # Configuration classes
    'ModelConfig',
    
    # Enumerations
    'ModelType',
    'ModelStatus',
    
    # Factory functions
    'create_generator_model',
    'create_load_model',
    'create_storage_model'
]