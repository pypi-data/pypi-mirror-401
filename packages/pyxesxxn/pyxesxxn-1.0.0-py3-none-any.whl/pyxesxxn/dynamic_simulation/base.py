"""
Base classes and definitions for dynamic simulation.

This module provides fundamental classes, interfaces, and data structures
for dynamic simulation of energy systems. It defines abstract base classes,
configuration management, state tracking, and event handling.
"""

import abc
import json
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union, Set, Tuple, Type, Callable
import logging

import numpy as np
import pandas as pd

try:
    import pypsa
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)


class SimulationType(Enum):
    """Simulation type enumeration."""
    TIME_SERIES = "time_series"
    REAL_TIME = "real_time"
    MONTE_CARLO = "monte_carlo"
    CONTINGENCY = "contingency"
    STABILITY = "stability"
    OPTIMIZATION = "optimization"


class SimulationStatus(Enum):
    """Simulation status enumeration."""
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EventType(Enum):
    """Simulation event type enumeration."""
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    LOAD_CHANGE = "load_change"
    GENERATION_CHANGE = "generation_change"
    CONTINGENCY = "contingency"
    CONTROL_ACTION = "control_action"
    ALARM = "alarm"
    WARNING = "warning"
    DATA_UPDATE = "data_update"
    THRESHOLD_EXCEEDED = "threshold_exceeded"


class Priority(Enum):
    """Priority level enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SimulationConfig:
    """Configuration for dynamic simulation.
    
    This class encapsulates all configuration parameters for a simulation,
    including time settings, model parameters, and simulation options.
    """
    
    # Basic simulation parameters
    simulation_id: str
    simulation_type: SimulationType
    time_step: float = 1.0  # seconds
    simulation_duration: float = 3600.0  # seconds
    start_time: datetime = field(default_factory=datetime.now)
    
    # Time series data settings
    data_sources: List[str] = field(default_factory=list)
    weather_data_file: Optional[str] = None
    load_data_file: Optional[str] = None
    price_data_file: Optional[str] = None
    renewable_data_file: Optional[str] = None
    
    # Model configuration
    dynamic_models: List[str] = field(default_factory=list)
    control_strategies: List[str] = field(default_factory=list)
    enable_grid_stability: bool = True
    enable_frequency_response: bool = True
    enable_voltage_regulation: bool = True
    
    # Simulation mode settings
    real_time_mode: bool = False
    parallel_processing: bool = False
    max_workers: int = 4
    batch_size: int = 100
    
    # Output and logging settings
    output_directory: str = "./simulation_output"
    save_results: bool = True
    save_intermediate_results: bool = False
    log_level: str = "INFO"
    save_frequency: int = 60  # Save every N time steps
    
    # Performance settings
    enable_caching: bool = True
    cache_size: int = 1000
    optimize_performance: bool = True
    memory_limit: Optional[int] = None  # MB
    
    # Scenario and case settings
    scenario: str = "base_case"
    contingency_scenarios: List[str] = field(default_factory=list)
    monte_carlo_runs: int = 0
    
    # Custom parameters
    custom_parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Validation and constraints
    max_time_step: float = 3600.0  # 1 hour
    min_time_step: float = 0.001  # 1 millisecond
    convergence_tolerance: float = 1e-6
    max_iterations: int = 1000
    
    def validate(self) -> List[str]:
        """Validate simulation configuration.
        
        Returns
        -------
        List[str]
            List of validation errors
        """
        errors = []
        
        # Check time parameters
        if self.time_step <= 0:
            errors.append("Time step must be positive")
        elif self.time_step < self.min_time_step:
            errors.append(f"Time step too small: {self.time_step} < {self.min_time_step}")
        elif self.time_step > self.max_time_step:
            errors.append(f"Time step too large: {self.time_step} > {self.max_time_step}")
        
        if self.simulation_duration <= 0:
            errors.append("Simulation duration must be positive")
        
        if self.simulation_duration < self.time_step:
            errors.append("Simulation duration must be greater than time step")
        
        # Check output settings
        if not self.output_directory:
            errors.append("Output directory must be specified")
        
        # Check parallel processing settings
        if self.parallel_processing and self.max_workers <= 0:
            errors.append("Max workers must be positive when using parallel processing")
        
        # Check Monte Carlo settings
        if self.simulation_type == SimulationType.MONTE_CARLO:
            if self.monte_carlo_runs <= 0:
                errors.append("Monte Carlo runs must be positive")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Configuration dictionary
        """
        config_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                config_dict[key] = value.isoformat()
            elif isinstance(value, (SimulationType, EventType, Priority)):
                config_dict[key] = value.value
            elif isinstance(value, list) and value and hasattr(value[0], 'value'):
                # Handle lists of enums
                config_dict[key] = [item.value for item in value]
            elif key == 'custom_parameters':
                config_dict[key] = value.copy()
            else:
                config_dict[key] = value
        return config_dict
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'SimulationConfig':
        """Create configuration from dictionary.
        
        Parameters
        ----------
        config_dict : Dict[str, Any]
            Configuration dictionary
            
        Returns
        -------
        SimulationConfig
            Configuration instance
        """
        # Convert enum strings back to enums
        if 'simulation_type' in config_dict:
            config_dict['simulation_type'] = SimulationType(config_dict['simulation_type'])
        
        # Handle datetime
        if 'start_time' in config_dict and isinstance(config_dict['start_time'], str):
            config_dict['start_time'] = datetime.fromisoformat(config_dict['start_time'])
        
        return cls(**config_dict)


@dataclass
class SimulationState:
    """Current simulation state.
    
    This class represents the current state of a simulation, including
    time, status, and system variables.
    """
    
    simulation_id: str
    current_time: datetime
    time_step: int
    simulation_status: SimulationStatus
    elapsed_time: float  # seconds
    total_time_steps: int
    
    # System state variables
    system_frequency: float = 50.0  # Hz
    system_voltage: float = 1.0  # p.u.
    total_generation: float = 0.0  # MW
    total_load: float = 0.0  # MW
    reserve_margin: float = 0.0  # %
    
    # Component states
    generator_states: Dict[str, float] = field(default_factory=dict)
    storage_states: Dict[str, float] = field(default_factory=dict)
    load_states: Dict[str, float] = field(default_factory=dict)
    
    # Control system states
    control_actions: Dict[str, float] = field(default_factory=dict)
    setpoints: Dict[str, float] = field(default_factory=dict)
    
    # Performance metrics
    convergence_metrics: Dict[str, float] = field(default_factory=dict)
    computation_time: float = 0.0  # seconds
    memory_usage: float = 0.0  # MB
    
    # Event queue
    pending_events: List['SimulationEvent'] = field(default_factory=list)
    
    def update(self, **kwargs) -> 'SimulationState':
        """Update state with new values.
        
        Parameters
        ----------
        **kwargs
            State parameters to update
            
        Returns
        -------
        SimulationState
            Updated state
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        return self
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get state variable value.
        
        Parameters
        ----------
        name : str
            Variable name
        default : Any, optional
            Default value if variable not found
            
        Returns
        -------
        Any
            Variable value or default
        """
        # Check direct attributes
        if hasattr(self, name):
            return getattr(self, name)
        
        # Check nested dictionaries
        for attr_name in ['generator_states', 'storage_states', 'load_states', 
                         'control_actions', 'setpoints', 'convergence_metrics']:
            if hasattr(self, attr_name):
                nested_dict = getattr(self, attr_name)
                if name in nested_dict:
                    return nested_dict[name]
        
        return default
    
    def set_variable(self, name: str, value: Any) -> None:
        """Set state variable value.
        
        Parameters
        ----------
        name : str
            Variable name
        value : Any
            Variable value
        """
        # Check direct attributes
        if hasattr(self, name):
            setattr(self, name, value)
            return
        
        # Try to find in nested dictionaries
        nested_attrs = ['generator_states', 'storage_states', 'load_states', 
                       'control_actions', 'setpoints', 'convergence_metrics']
        
        for attr_name in nested_attrs:
            if hasattr(self, attr_name):
                nested_dict = getattr(self, attr_name)
                nested_dict[name] = value
                return
        
        # If not found, create new attribute
        setattr(self, name, value)
    
    def check_constraints(self) -> List[str]:
        """Check system constraints and limits.
        
        Returns
        -------
        List[str]
            List of constraint violations
        """
        violations = []
        
        # Frequency constraints
        if not 49.5 <= self.system_frequency <= 50.5:
            violations.append(f"Frequency outside limits: {self.system_frequency} Hz")
        
        # Voltage constraints
        if not 0.95 <= self.system_voltage <= 1.05:
            violations.append(f"Voltage outside limits: {self.system_voltage} p.u.")
        
        # Reserve margin constraints
        if self.reserve_margin < 5.0:  # Minimum 5% reserve
            violations.append(f"Low reserve margin: {self.reserve_margin}%")
        
        # Power balance check
        power_balance_error = abs(self.total_generation - self.total_load)
        if power_balance_error > 1.0:  # 1 MW tolerance
            violations.append(f"Power balance error: {power_balance_error} MW")
        
        return violations
    
    def get_summary(self) -> Dict[str, Any]:
        """Get simulation state summary.
        
        Returns
        -------
        Dict[str, Any]
            State summary
        """
        return {
            'simulation_id': self.simulation_id,
            'current_time': self.current_time.isoformat(),
            'time_step': self.time_step,
            'status': self.simulation_status.value,
            'elapsed_time': self.elapsed_time,
            'system_frequency': self.system_frequency,
            'system_voltage': self.system_voltage,
            'total_generation': self.total_generation,
            'total_load': self.total_load,
            'reserve_margin': self.reserve_margin,
            'computation_time': self.computation_time,
            'memory_usage': self.memory_usage,
            'pending_events': len(self.pending_events)
        }


@dataclass
class SimulationEvent:
    """Simulation event for real-time event handling.
    
    This class represents events that can occur during simulation,
    such as system changes, contingencies, or control actions.
    """
    
    event_id: str
    event_type: EventType
    timestamp: datetime
    priority: Priority = Priority.NORMAL
    
    # Event data
    description: str = ""
    source_component: Optional[str] = None
    target_component: Optional[str] = None
    
    # Event parameters
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Event state
    processed: bool = False
    processing_time: Optional[datetime] = None
    result: Optional[Any] = None
    
    def process(self, handler: Callable) -> Any:
        """Process the event using provided handler.
        
        Parameters
        ----------
        handler : Callable
            Event handler function
            
        Returns
        -------
        Any
            Processing result
        """
        try:
            self.processing_time = datetime.now()
            self.result = handler(self)
            self.processed = True
            return self.result
        except Exception as e:
            self.result = f"Processing failed: {str(e)}"
            return self.result
    
    def get_priority_value(self) -> int:
        """Get numeric priority value for sorting.
        
        Returns
        -------
        int
            Priority value (higher number = higher priority)
        """
        priority_mapping = {
            Priority.LOW: 1,
            Priority.NORMAL: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4
        }
        return priority_mapping.get(self.priority, 2)


@dataclass 
class SimulationResult:
    """Simulation results container.
    
    This class stores and manages simulation results, including
    time series data, statistics, and performance metrics.
    """
    
    simulation_id: str
    config: SimulationConfig
    start_time: datetime
    end_time: datetime
    status: SimulationStatus
    
    # Time series data
    time_series: Dict[str, pd.DataFrame] = field(default_factory=dict)
    
    # Summary statistics
    summary_statistics: Dict[str, Any] = field(default_factory=dict)
    
    # Performance metrics
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    
    # System metrics
    system_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Events log
    events_log: List[SimulationEvent] = field(default_factory=list)
    
    # Convergence information
    convergence_info: Dict[str, Any] = field(default_factory=dict)
    
    def add_time_series(self, name: str, data: pd.DataFrame) -> None:
        """Add time series data.
        
        Parameters
        ----------
        name : str
            Time series name
        data : pd.DataFrame
            Time series data
        """
        self.time_series[name] = data.copy()
    
    def get_time_series(self, name: str) -> Optional[pd.DataFrame]:
        """Get time series data.
        
        Parameters
        ----------
        name : str
            Time series name
            
        Returns
        -------
        pd.DataFrame, optional
            Time series data
        """
        return self.time_series.get(name)
    
    def calculate_statistics(self) -> None:
        """Calculate summary statistics for all time series."""
        for name, data in self.time_series.items():
            stats = {}
            for column in data.columns:
                if pd.api.types.is_numeric_dtype(data[column]):
                    series = data[column].dropna()
                    if len(series) > 0:
                        stats[column] = {
                            'mean': series.mean(),
                            'std': series.std(),
                            'min': series.min(),
                            'max': series.max(),
                            'median': series.median(),
                            'q25': series.quantile(0.25),
                            'q75': series.quantile(0.75)
                        }
            self.summary_statistics[name] = stats
    
    def export_results(self, file_path: str, format: str = "hdf5") -> bool:
        """Export simulation results to file.
        
        Parameters
        ----------
        file_path : str
            Output file path
        format : str
            Export format ('hdf5', 'csv', 'json')
            
        Returns
        -------
        bool
            True if successfully exported
        """
        try:
            if format.lower() == "hdf5":
                with pd.HDFStore(file_path, mode='w') as store:
                    for name, data in self.time_series.items():
                        store.put(name, data)
                    store.put('config', pd.DataFrame([self.config.to_dict()]))
                    store.put('summary_statistics', pd.DataFrame([self.summary_statistics]))
            elif format.lower() == "csv":
                base_path = file_path.rsplit('.', 1)[0]
                for name, data in self.time_series.items():
                    data.to_csv(f"{base_path}_{name}.csv", index=True)
                # Save config as JSON
                with open(f"{base_path}_config.json", 'w') as f:
                    json.dump(self.config.to_dict(), f, indent=2, default=str)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return True
        except Exception as e:
            logging.error(f"Failed to export results: {e}")
            return False
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary.
        
        Returns
        -------
        Dict[str, Any]
            Performance summary
        """
        total_time = (self.end_time - self.start_time).total_seconds()
        
        return {
            'total_simulation_time': total_time,
            'average_step_time': self.performance_metrics.get('avg_step_time', 0),
            'memory_usage_peak': self.performance_metrics.get('peak_memory', 0),
            'convergence_failures': self.convergence_info.get('total_failures', 0),
            'events_processed': len([e for e in self.events_log if e.processed]),
            'total_events': len(self.events_log)
        }


class SimulationBase(abc.ABC):
    """Abstract base class for all simulation components.
    
    This class defines the common interface and functionality that all
    simulation components must implement. It provides methods for
    configuration, initialization, execution, and result management.
    """
    
    def __init__(self, 
                 simulation_id: str,
                 config: Optional[SimulationConfig] = None,
                 **kwargs):
        """Initialize simulation component.
        
        Parameters
        ----------
        simulation_id : str
            Unique simulation identifier
        config : SimulationConfig, optional
            Simulation configuration
        **kwargs
            Additional configuration parameters
        """
        self.simulation_id = simulation_id
        self.config = config or self._create_default_config(**kwargs)
        
        # Validate configuration
        validation_errors = self.config.validate()
        if validation_errors:
            raise ValueError(f"Invalid simulation configuration: {validation_errors}")
        
        # Initialize logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.setLevel(getattr(logging, self.config.log_level))
        
        # Initialize state
        self.state = SimulationState(
            simulation_id=simulation_id,
            current_time=self.config.start_time,
            time_step=0,
            simulation_status=SimulationStatus.INITIALIZED,
            elapsed_time=0.0,
            total_time_steps=int(self.config.simulation_duration / self.config.time_step)
        )
        
        # Event handling
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.event_queue: List[SimulationEvent] = []
        
        # Performance tracking
        self.performance_metrics = {
            'total_computation_time': 0.0,
            'step_computation_times': [],
            'memory_usage_history': []
        }
        
        # Initialize component
        self._initialize_simulation()
    
    def _create_default_config(self, **kwargs) -> SimulationConfig:
        """Create default simulation configuration.
        
        Parameters
        ----------
        **kwargs
            Additional configuration parameters
            
        Returns
        -------
        SimulationConfig
            Default configuration
        """
        return SimulationConfig(
            simulation_id=self.simulation_id,
            simulation_type=SimulationType.TIME_SERIES,
            **kwargs
        )
    
    def _initialize_simulation(self) -> None:
        """Initialize simulation-specific components."""
        pass
    
    @property
    def simulation_id(self) -> str:
        """Simulation identifier."""
        return self._simulation_id
    
    @simulation_id.setter
    def simulation_id(self, value: str) -> None:
        if not value:
            raise ValueError("Simulation ID cannot be empty")
        self._simulation_id = value
    
    @property
    def config(self) -> SimulationConfig:
        """Simulation configuration."""
        return self._config
    
    @config.setter
    def config(self, value: SimulationConfig) -> None:
        if not isinstance(value, SimulationConfig):
            raise TypeError("Config must be a SimulationConfig instance")
        self._config = value
    
    @property
    def state(self) -> SimulationState:
        """Current simulation state."""
        return self._state
    
    @state.setter
    def state(self, value: SimulationState) -> None:
        if not isinstance(value, SimulationState):
            raise TypeError("State must be a SimulationState instance")
        self._state = value
    
    @property
    def status(self) -> SimulationStatus:
        """Current simulation status."""
        return self.state.simulation_status
    
    # Event handling methods
    def register_event_handler(self, event_type: EventType, handler: Callable) -> None:
        """Register event handler.
        
        Parameters
        ----------
        event_type : EventType
            Event type to handle
        handler : Callable
            Event handler function
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def add_event(self, event: SimulationEvent) -> None:
        """Add event to queue.
        
        Parameters
        ----------
        event : SimulationEvent
            Event to add
        """
        self.event_queue.append(event)
        # Sort by priority
        self.event_queue.sort(key=lambda e: e.get_priority_value(), reverse=True)
    
    def process_events(self) -> None:
        """Process pending events."""
        processed_events = []
        
        for event in self.event_queue:
            if event.event_type in self.event_handlers:
                for handler in self.event_handlers[event.event_type]:
                    try:
                        event.process(handler)
                    except Exception as e:
                        self.logger.error(f"Event processing failed: {e}")
            
            processed_events.append(event)
        
        # Remove processed events
        for event in processed_events:
            if event in self.event_queue:
                self.event_queue.remove(event)
    
    # Abstract methods to be implemented by subclasses
    @abc.abstractmethod
    def initialize(self) -> bool:
        """Initialize simulation.
        
        Returns
        -------
        bool
            True if successfully initialized
        """
        pass
    
    @abc.abstractmethod
    def execute_step(self) -> bool:
        """Execute single simulation step.
        
        Returns
        -------
        bool
            True if step executed successfully
        """
        pass
    
    @abc.abstractmethod
    def finalize(self) -> SimulationResult:
        """Finalize simulation and return results.
        
        Returns
        -------
        SimulationResult
            Simulation results
        """
        pass
    
    # Utility methods
    def start_simulation(self) -> bool:
        """Start simulation.
        
        Returns
        -------
        bool
            True if started successfully
        """
        try:
            self.state.simulation_status = SimulationStatus.RUNNING
            self.state.elapsed_time = 0.0
            return True
        except Exception as e:
            self.logger.error(f"Failed to start simulation: {e}")
            return False
    
    def pause_simulation(self) -> bool:
        """Pause simulation.
        
        Returns
        -------
        bool
            True if paused successfully
        """
        try:
            self.state.simulation_status = SimulationStatus.PAUSED
            return True
        except Exception as e:
            self.logger.error(f"Failed to pause simulation: {e}")
            return False
    
    def resume_simulation(self) -> bool:
        """Resume simulation.
        
        Returns
        -------
        bool
            True if resumed successfully
        """
        try:
            self.state.simulation_status = SimulationStatus.RUNNING
            return True
        except Exception as e:
            self.logger.error(f"Failed to resume simulation: {e}")
            return False
    
    def stop_simulation(self) -> bool:
        """Stop simulation.
        
        Returns
        -------
        bool
            True if stopped successfully
        """
        try:
            self.state.simulation_status = SimulationStatus.COMPLETED
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop simulation: {e}")
            return False
    
    def get_progress(self) -> float:
        """Get simulation progress (0-1).
        
        Returns
        -------
        float
            Progress fraction
        """
        if self.state.total_time_steps <= 0:
            return 0.0
        
        return min(1.0, self.state.time_step / self.state.total_time_steps)
    
    def log_performance_metrics(self) -> None:
        """Log current performance metrics."""
        self.logger.info(f"Simulation {self.simulation_id} - Step {self.state.time_step}: "
                        f"Frequency: {self.state.system_frequency:.2f} Hz, "
                        f"Voltage: {self.state.system_voltage:.3f} p.u., "
                        f"Generation: {self.state.total_generation:.1f} MW, "
                        f"Load: {self.state.total_load:.1f} MW")
    
    def __repr__(self) -> str:
        """String representation of simulation."""
        return (f"{self.__class__.__name__}(id='{self.simulation_id}', "
                f"type='{self.config.simulation_type.value}', "
                f"status='{self.status.value}')")


# Utility functions
def validate_simulation_config(config: SimulationConfig) -> List[str]:
    """Validate simulation configuration.
    
    Parameters
    ----------
    config : SimulationConfig
        Configuration to validate
        
    Returns
    -------
    List[str]
        List of validation errors
    """
    return config.validate()


def create_simulation_result(simulation_id: str,
                           config: SimulationConfig,
                           status: SimulationStatus) -> SimulationResult:
    """Create simulation result instance.
    
    Parameters
    ----------
    simulation_id : str
        Simulation identifier
    config : SimulationConfig
        Simulation configuration
    status : SimulationStatus
        Simulation status
        
    Returns
    -------
    SimulationResult
        Simulation result instance
    """
    return SimulationResult(
        simulation_id=simulation_id,
        config=config,
        start_time=config.start_time,
        end_time=config.start_time + timedelta(seconds=config.simulation_duration),
        status=status
    )


# Define __all__ for module exports
__all__ = [
    # Core classes
    'SimulationBase',
    'SimulationConfig',
    'SimulationResult',
    'SimulationEvent',
    'SimulationState',
    
    # Enumerations
    'SimulationType',
    'SimulationStatus',
    'EventType',
    'Priority',
    
    # Utility functions
    'validate_simulation_config',
    'create_simulation_result'
]