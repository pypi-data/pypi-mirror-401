"""Electric Machinery Prognostics Module.

This module provides prognostics and health management capabilities for electric construction machinery,
including excavators, cranes, loaders, and forklifts. It integrates with the ProgPy framework to enable
fault prediction, state estimation, and health assessment for electric machinery components.
"""

from typing import Dict, List, Optional, Tuple, Callable, Any
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

try:
    from .faultmodel_wrapper import (
        FaultModelConfig,
        FaultModelWrapper,
        check_faultmodel_available,
        _FAULTMODEL_AVAILABLE
    )
    
    if _FAULTMODEL_AVAILABLE:
        import sys
        import os
        faultmodel_path = os.path.join(os.path.dirname(__file__), '..', 'faultmodel', 'src')
        if faultmodel_path not in sys.path:
            sys.path.insert(0, faultmodel_path)
        try:
            from faultmodel import PrognosticsModel
        except ImportError:
            PrognosticsModel = None
            _FAULTMODEL_AVAILABLE = False
    else:
        PrognosticsModel = None
    
    if _FAULTMODEL_AVAILABLE and PrognosticsModel:
        from faultmodel.predictors import MonteCarlo, UnscentedTransform
        from faultmodel.state_estimators import KalmanFilter, UnscentedKalmanFilter, ParticleFilter
        from faultmodel.uncertain_data import UnweightedSamples
    else:
        MonteCarlo = None
        UnscentedTransform = None
        KalmanFilter = None
        UnscentedKalmanFilter = None
        ParticleFilter = None
        UnweightedSamples = None
        
except ImportError:
    _FAULTMODEL_AVAILABLE = False
    PrognosticsModel = None
    MonteCarlo = None
    UnscentedTransform = None
    KalmanFilter = None
    UnscentedKalmanFilter = None
    ParticleFilter = None
    UnweightedSamples = None


class MachineryType(Enum):
    """Types of electric construction machinery."""
    EXCAVATOR = "excavator"
    CRANE = "crane"
    LOADER = "loader"
    FORKLIFT = "forklift"


class ComponentType(Enum):
    """Types of machinery components."""
    BATTERY = "battery"
    MOTOR = "motor"
    HYDRAULIC_SYSTEM = "hydraulic_system"
    CONTROL_SYSTEM = "control_system"
    MECHANICAL_STRUCTURE = "mechanical_structure"
    POWER_ELECTRONICS = "power_electronics"


class FaultMode(Enum):
    """Common fault modes in electric machinery."""
    BATTERY_CAPACITY_DEGRADATION = "battery_capacity_degradation"
    MOTOR_WINDING_FAILURE = "motor_winding_failure"
    MOTOR_BEARING_WEAR = "motor_bearing_wear"
    HYDRAULIC_LEAK = "hydraulic_leak"
    HYDRAULIC_PUMP_WEAR = "hydraulic_pump_wear"
    CONTROLLER_FAILURE = "controller_failure"
    STRUCTURAL_FATIGUE = "structural_fatigue"
    INVERTER_FAILURE = "inverter_failure"


@dataclass
class ElectricMachineryConfig:
    """Configuration for electric machinery prognostics.
    
    Attributes:
        machinery_type: Type of machinery
        rated_power: Rated power in kW
        rated_voltage: Rated voltage in V
        rated_current: Rated current in A
        battery_capacity: Battery capacity in kWh
        operating_temperature_range: Operating temperature range (min, max) in Celsius
        operating_hours: Total operating hours
        maintenance_interval: Maintenance interval in hours
        fault_thresholds: Dictionary of fault thresholds for different components
    """
    machinery_type: MachineryType
    rated_power: float
    rated_voltage: float
    rated_current: float
    battery_capacity: float
    operating_temperature_range: Tuple[float, float] = (-20.0, 50.0)
    operating_hours: float = 0.0
    maintenance_interval: float = 500.0
    fault_thresholds: Dict[str, float] = field(default_factory=lambda: {
        'battery_capacity': 0.7,
        'motor_efficiency': 0.85,
        'hydraulic_efficiency': 0.80,
        'controller_health': 0.70
    })


@dataclass
class ElectricMachineryState:
    """State of electric machinery.
    
    Attributes:
        battery_state_of_charge: Battery state of charge (0-1)
        battery_health: Battery health indicator (0-1)
        motor_temperature: Motor temperature in Celsius
        motor_efficiency: Motor efficiency (0-1)
        hydraulic_pressure: Hydraulic pressure in bar
        hydraulic_temperature: Hydraulic fluid temperature in Celsius
        controller_status: Controller status (0-1)
        load_factor: Current load factor (0-1)
        operating_mode: Current operating mode
    """
    battery_state_of_charge: float = 1.0
    battery_health: float = 1.0
    motor_temperature: float = 25.0
    motor_efficiency: float = 0.95
    hydraulic_pressure: float = 200.0
    hydraulic_temperature: float = 40.0
    controller_status: float = 1.0
    load_factor: float = 0.0
    operating_mode: str = "idle"


class ElectricMachineryModel(ABC):
    """Base prognostics model for electric machinery.
    
    This class provides a physics-based model for simulating and predicting
    the degradation of electric construction machinery components.
    """
    
    def __init__(self, config: ElectricMachineryConfig, **kwargs):
        """Initialize the electric machinery model.
        
        Args:
            config: Configuration for the machinery
            **kwargs: Additional parameters for PrognosticsModel
        """
        self.config = config
        
        if PrognosticsModel:
            super().__init__(**kwargs)
        
        self.states = [
            'battery_health',
            'motor_efficiency',
            'hydraulic_efficiency',
            'controller_health',
            'structural_health'
        ]
        
        self.outputs = [
            'battery_voltage',
            'motor_temperature',
            'hydraulic_pressure',
            'power_consumption',
            'efficiency'
        ]
        
        self.inputs = [
            'load_demand',
            'ambient_temperature',
            'operating_mode'
        ]
        
        self.events = [
            'battery_failure',
            'motor_failure',
            'hydraulic_failure',
            'controller_failure'
        ]
        
        self.default_parameters = {
            'battery_degradation_rate': 1e-6,
            'motor_wear_rate': 2e-7,
            'hydraulic_wear_rate': 3e-7,
            'controller_degradation_rate': 1e-7,
            'structural_fatigue_rate': 1e-8,
            'temperature_factor': 1.2,
            'load_factor': 1.5
        }
        
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs)
        
        self.thresholds = {
            'battery_failure': config.fault_thresholds['battery_capacity'],
            'motor_failure': config.fault_thresholds['motor_efficiency'],
            'hydraulic_failure': config.fault_thresholds['hydraulic_efficiency'],
            'controller_failure': config.fault_thresholds['controller_health']
        }
    
    def next_state(self, t: float, x: Dict[str, float], u: Dict[str, float], dt: float = 0.1) -> Dict[str, float]:
        """Calculate next state based on current state and inputs.
        
        Args:
            t: Current time
            x: Current state dictionary
            u: Input dictionary
            dt: Time step
            
        Returns:
            Next state dictionary
        """
        x_next = x.copy()
        
        load_factor = u.get('load_demand', 0.5)
        temp = u.get('ambient_temperature', 25.0)
        
        temp_factor = 1.0 + self.parameters['temperature_factor'] * (temp - 25.0) / 100.0
        load_factor_effect = 1.0 + self.parameters['load_factor'] * load_factor
        
        x_next['battery_health'] -= self.parameters['battery_degradation_rate'] * temp_factor * load_factor_effect * dt
        x_next['motor_efficiency'] -= self.parameters['motor_wear_rate'] * temp_factor * load_factor_effect * dt
        x_next['hydraulic_efficiency'] -= self.parameters['hydraulic_wear_rate'] * temp_factor * load_factor_effect * dt
        x_next['controller_health'] -= self.parameters['controller_degradation_rate'] * temp_factor * load_factor_effect * dt
        x_next['structural_health'] -= self.parameters['structural_fatigue_rate'] * load_factor_effect * dt
        
        for key in x_next:
            x_next[key] = max(0.0, min(1.0, x_next[key]))
        
        return x_next
    
    def output(self, t: float, x: Dict[str, float], u: Dict[str, float]) -> Dict[str, float]:
        """Calculate outputs based on current state and inputs.
        
        Args:
            t: Current time
            x: Current state dictionary
            u: Input dictionary
            
        Returns:
            Output dictionary
        """
        load_factor = u.get('load_demand', 0.5)
        
        battery_voltage = self.config.rated_voltage * x['battery_health']
        motor_temperature = 25.0 + 50.0 * load_factor * (1.0 - x['motor_efficiency'])
        hydraulic_pressure = 200.0 * x['hydraulic_efficiency'] * load_factor
        power_consumption = self.config.rated_power * load_factor / x['motor_efficiency']
        efficiency = 0.95 * x['motor_efficiency'] * x['hydraulic_efficiency']
        
        return {
            'battery_voltage': battery_voltage,
            'motor_temperature': motor_temperature,
            'hydraulic_pressure': hydraulic_pressure,
            'power_consumption': power_consumption,
            'efficiency': efficiency
        }
    
    def event_state(self, t: float, x: Dict[str, float]) -> Dict[str, float]:
        """Calculate event state (distance to failure) for each event.
        
        Args:
            t: Current time
            x: Current state dictionary
            
        Returns:
            Event state dictionary
        """
        return {
            'battery_failure': x['battery_health'] - self.thresholds['battery_failure'],
            'motor_failure': x['motor_efficiency'] - self.thresholds['motor_failure'],
            'hydraulic_failure': x['hydraulic_efficiency'] - self.thresholds['hydraulic_failure'],
            'controller_failure': x['controller_health'] - self.thresholds['controller_failure']
        }
    
    def threshold_met(self, t: float, x: Dict[str, float]) -> Dict[str, bool]:
        """Check if any failure threshold has been met.
        
        Args:
            t: Current time
            x: Current state dictionary
            
        Returns:
            Dictionary indicating which thresholds have been met
        """
        event_state = self.event_state(t, x)
        return {key: value <= 0 for key, value in event_state.items()}


class ElectricExcavatorModel(ElectricMachineryModel):
    """Prognostics model for electric excavator.
    
    Electric excavators are characterized by high power demands, frequent load cycles,
    and complex hydraulic systems for bucket and arm operation.
    """
    
    def __init__(self, config: Optional[ElectricMachineryConfig] = None, **kwargs):
        """Initialize electric excavator model.
        
        Args:
            config: Configuration for the excavator. If None, creates default config.
            **kwargs: Additional parameters
        """
        if config is None:
            config = ElectricMachineryConfig(
                machinery_type=MachineryType.EXCAVATOR,
                rated_power=300.0,
                rated_voltage=400.0,
                rated_current=500.0,
                battery_capacity=500.0,
                operating_hours=0.0,
                maintenance_interval=500.0
            )
        
        super().__init__(config, **kwargs)
        
        self.default_parameters.update({
            'hydraulic_wear_rate': 5e-7,
            'structural_fatigue_rate': 2e-7
        })
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs)


class ElectricCraneModel(ElectricMachineryModel):
    """Prognostics model for electric crane.
    
    Electric cranes are characterized by high torque requirements, precise control needs,
    and significant structural loads during lifting operations.
    """
    
    def __init__(self, config: Optional[ElectricMachineryConfig] = None, **kwargs):
        """Initialize electric crane model.
        
        Args:
            config: Configuration for the crane. If None, creates default config.
            **kwargs: Additional parameters
        """
        if config is None:
            config = ElectricMachineryConfig(
                machinery_type=MachineryType.CRANE,
                rated_power=250.0,
                rated_voltage=400.0,
                rated_current=400.0,
                battery_capacity=400.0,
                operating_hours=0.0,
                maintenance_interval=400.0
            )
        
        super().__init__(config, **kwargs)
        
        self.default_parameters.update({
            'structural_fatigue_rate': 3e-7,
            'motor_wear_rate': 3e-7
        })
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs)


class ElectricLoaderModel(ElectricMachineryModel):
    """Prognostics model for electric loader.
    
    Electric loaders are characterized by high cycle rates, significant hydraulic demands,
    and continuous operation in harsh environments.
    """
    
    def __init__(self, config: Optional[ElectricMachineryConfig] = None, **kwargs):
        """Initialize electric loader model.
        
        Args:
            config: Configuration for the loader. If None, creates default config.
            **kwargs: Additional parameters
        """
        if config is None:
            config = ElectricMachineryConfig(
                machinery_type=MachineryType.LOADER,
                rated_power=200.0,
                rated_voltage=400.0,
                rated_current=350.0,
                battery_capacity=300.0,
                operating_hours=0.0,
                maintenance_interval=600.0
            )
        
        super().__init__(config, **kwargs)
        
        self.default_parameters.update({
            'hydraulic_wear_rate': 4e-7,
            'motor_wear_rate': 2.5e-7
        })
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs)


class ElectricForkliftModel(ElectricMachineryModel):
    """Prognostics model for electric forklift.
    
    Electric forklifts are characterized by frequent start-stop cycles, variable load demands,
    and indoor operation requirements.
    """
    
    def __init__(self, config: Optional[ElectricMachineryConfig] = None, **kwargs):
        """Initialize electric forklift model.
        
        Args:
            config: Configuration for the forklift. If None, creates default config.
            **kwargs: Additional parameters
        """
        if config is None:
            config = ElectricMachineryConfig(
                machinery_type=MachineryType.FORKLIFT,
                rated_power=50.0,
                rated_voltage=48.0,
                rated_current=150.0,
                battery_capacity=80.0,
                operating_hours=0.0,
                maintenance_interval=1000.0
            )
        
        super().__init__(config, **kwargs)
        
        self.default_parameters.update({
            'battery_degradation_rate': 2e-6,
            'motor_wear_rate': 1.5e-7
        })
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs)


class ElectricMachineryFaultPredictor:
    """Fault predictor for electric machinery.
    
    This class provides fault prediction capabilities using the ProgPy framework,
    enabling estimation of remaining useful life (RUL) for different components.
    """
    
    def __init__(self, model: ElectricMachineryModel, config: Optional[FaultModelConfig] = None):
        """Initialize the fault predictor.
        
        Args:
            model: Electric machinery prognostics model
            config: Fault model configuration
        """
        if not _FAULTMODEL_AVAILABLE:
            raise ImportError("Faultmodel (ProgPy) is not available")
        
        self.model = model
        self.config = config or FaultModelConfig()
        self.wrapper = FaultModelWrapper(self.config)
        self.wrapper.set_model(model)
    
    def predict_fault(
        self,
        current_state: Dict[str, float],
        future_loading: Callable[[float], Dict[str, float]],
        dt: float = 0.1,
        **kwargs
    ):
        """Predict future faults and RUL.
        
        Args:
            current_state: Current state of the machinery
            future_loading: Function describing future loading
            dt: Time step for prediction
            **kwargs: Additional prediction parameters
            
        Returns:
            Prediction results containing RUL and fault probabilities
        """
        self.wrapper.state_estimator.x = UnweightedSamples([current_state])
        
        prediction = self.wrapper.predict(future_loading, dt=dt, **kwargs)
        
        return {
            'time_of_event': prediction.time_of_event,
            'event_states': prediction.event_states,
            'states': prediction.states,
            'outputs': prediction.outputs,
            'times': prediction.times
        }
    
    def get_rul(self, prediction: Dict[str, Any]) -> Dict[str, float]:
        """Extract remaining useful life from prediction.
        
        Args:
            prediction: Prediction results from predict_fault
            
        Returns:
            Dictionary of RUL values for each event type
        """
        rul = {}
        for event, toe in prediction['time_of_event'].items():
            if hasattr(toe, 'mean'):
                rul[event] = toe.mean
            elif hasattr(toe, '__iter__'):
                rul[event] = np.mean(toe)
            else:
                rul[event] = toe
        return rul


class ElectricMachineryStateEstimator:
    """State estimator for electric machinery.
    
    This class provides state estimation capabilities using Kalman filtering
    or particle filtering to estimate the true state of the machinery from noisy measurements.
    """
    
    def __init__(self, model: ElectricMachineryModel, config: Optional[FaultModelConfig] = None):
        """Initialize the state estimator.
        
        Args:
            model: Electric machinery prognostics model
            config: Fault model configuration
        """
        if not _FAULTMODEL_AVAILABLE:
            raise ImportError("Faultmodel (ProgPy) is not available")
        
        self.model = model
        self.config = config or FaultModelConfig()
        self.wrapper = FaultModelWrapper(self.config)
        self.wrapper.set_model(model)
    
    def estimate(
        self,
        t: float,
        u: Dict[str, float],
        z: Dict[str, float]
    ) -> Dict[str, float]:
        """Estimate current state from measurements.
        
        Args:
            t: Current time
            u: Input dictionary
            z: Measurement dictionary
            
        Returns:
            Estimated state dictionary
        """
        estimated_state = self.wrapper.estimate_state(t, u, z)
        
        if hasattr(estimated_state, 'mean'):
            return estimated_state.mean
        elif hasattr(estimated_state, '__iter__'):
            return {key: np.mean([s[key] for s in estimated_state]) for key in estimated_state[0]}
        else:
            return estimated_state


class ElectricMachineryHealthAssessor:
    """Health assessor for electric machinery.
    
    This class provides comprehensive health assessment capabilities,
    including health index calculation, fault diagnosis, and maintenance recommendations.
    """
    
    def __init__(self, model: ElectricMachineryModel):
        """Initialize the health assessor.
        
        Args:
            model: Electric machinery prognostics model
        """
        self.model = model
    
    def calculate_health_index(self, state: Dict[str, float]) -> float:
        """Calculate overall health index.
        
        Args:
            state: Current state of the machinery
            
        Returns:
            Overall health index (0-1)
        """
        weights = {
            'battery_health': 0.3,
            'motor_efficiency': 0.3,
            'hydraulic_efficiency': 0.2,
            'controller_health': 0.1,
            'structural_health': 0.1
        }
        
        health_index = sum(weights[key] * state.get(key, 1.0) for key in weights)
        return health_index
    
    def diagnose_faults(self, state: Dict[str, float]) -> Dict[str, Any]:
        """Diagnose potential faults based on current state.
        
        Args:
            state: Current state of the machinery
            
        Returns:
            Dictionary containing fault diagnosis results
        """
        diagnosis = {}
        
        for event, threshold in self.model.thresholds.items():
            component = event.replace('_failure', '_health')
            if component in state:
                health = state[component]
                if health < threshold:
                    severity = (threshold - health) / threshold
                    diagnosis[event] = {
                        'detected': True,
                        'severity': severity,
                        'current_health': health,
                        'threshold': threshold
                    }
                else:
                    diagnosis[event] = {
                        'detected': False,
                        'severity': 0.0,
                        'current_health': health,
                        'threshold': threshold
                    }
            else:
                diagnosis[event] = {
                    'detected': False,
                    'severity': 0.0,
                    'current_health': 1.0,
                    'threshold': threshold
                }
        
        return diagnosis
    
    def get_maintenance_recommendation(
        self,
        state: Dict[str, float],
        diagnosis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate maintenance recommendations.
        
        Args:
            state: Current state of the machinery
            diagnosis: Fault diagnosis results
            
        Returns:
            Dictionary containing maintenance recommendations
        """
        health_index = self.calculate_health_index(state)
        
        if health_index > 0.9:
            priority = "low"
            action = "Continue normal operation"
        elif health_index > 0.7:
            priority = "medium"
            action = "Schedule preventive maintenance within 100 hours"
        elif health_index > 0.5:
            priority = "high"
            action = "Schedule maintenance within 24 hours"
        else:
            priority = "critical"
            action = "Immediate maintenance required - consider equipment shutdown"
        
        recommendations = {
            'health_index': health_index,
            'priority': priority,
            'action': action,
            'component_actions': {}
        }
        
        for event, fault_info in diagnosis.items():
            if fault_info['detected']:
                component = event.replace('_failure', '')
                if fault_info['severity'] > 0.5:
                    recommendations['component_actions'][component] = "Immediate replacement required"
                elif fault_info['severity'] > 0.2:
                    recommendations['component_actions'][component] = "Schedule replacement soon"
                else:
                    recommendations['component_actions'][component] = "Monitor closely"
        
        return recommendations
