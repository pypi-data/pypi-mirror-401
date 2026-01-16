"""
Simulation engine for dynamic energy system simulation.

This module provides the core simulation engine that orchestrates the execution
of dynamic models over time, including time stepping, event handling, and
result collection.
"""

import asyncio
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from queue import Queue, Empty
from threading import Event, Lock
from typing import Dict, List, Any, Optional, Callable, Tuple, Union
import warnings

import numpy as np
import pandas as pd

try:
    import pypsa
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)

from .base import SimulationState, SimulationConfig, SimulationStatus, SimulationEvent, SimulationResult
from .dynamic_models import DynamicModel, ModelType, create_generator_model, create_load_model, create_storage_model


class IntegrationMethod(Enum):
    """Numerical integration methods for dynamic simulation."""
    EULER = "euler"  # Forward Euler
    RK4 = "rk4"      # Runge-Kutta 4th order
    RK2 = "rk2"      # Runge-Kutta 2nd order
    BACKWARD_EULER = "backward_euler"  # Backward Euler
    TRAPEZOIDAL = "trapezoidal"  # Trapezoidal rule


@dataclass
class SimulationStep:
    """Information about a single simulation step."""
    step_number: int
    timestamp: datetime
    time_seconds: float
    time_minutes: float
    time_hours: float
    dt: float
    status: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    convergence_iterations: int = 0
    computation_time_ms: float = 0.0


@dataclass
class SimulationProgress:
    """Progress information for long-running simulations."""
    current_step: int
    total_steps: int
    progress_percent: float
    elapsed_time: float
    estimated_remaining_time: float
    steps_per_second: float
    current_iteration: int
    max_iterations: int


class SimulationEngine:
    """Core simulation engine for dynamic energy system simulation.
    
    This class manages the overall simulation execution, including:
    - Time stepping and integration
    - Model coordination and updates
    - Event handling
    - Result collection and logging
    - Performance monitoring
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize simulation engine.
        
        Parameters
        ----------
        config : SimulationConfig
            Simulation configuration
        """
        self.config = config
        
        # Initialize logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Simulation state
        self.status = SimulationStatus.INITIALIZED
        self.current_state = SimulationState()
        self.initial_state = SimulationState()
        
        # Dynamic models
        self.models: Dict[str, DynamicModel] = {}
        self.model_execution_order: List[str] = []
        
        # Time management
        self.current_time = config.start_time
        self.time_step = config.time_step_seconds
        self.total_simulation_time = 0.0
        self.time_step_counter = 0
        
        # Integration method
        self.integration_method = IntegrationMethod(config.integration_method)
        
        # Results storage
        self.time_series_results: Dict[str, List[float]] = {}
        self.snapshot_results: Dict[int, SimulationState] = {}
        self.step_results: List[SimulationStep] = []
        
        # Performance tracking
        self.computation_times: List[float] = []
        self.convergence_history: List[int] = []
        self.memory_usage: List[float] = []
        
        # Event handling
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.event_queue: Queue = Queue()
        
        # Threading
        self.is_running = False
        self.should_stop = Event()
        self.progress_callback: Optional[Callable] = None
        self.progress_lock = Lock()
        
        # Parallel execution
        self.use_parallel = config.enable_parallel_execution
        self.max_workers = config.max_parallel_workers
        
        # Initialize time series results storage
        self._initialize_results_storage()
    
    def _initialize_results_storage(self) -> None:
        """Initialize storage for simulation results."""
        # Create time series storage for common variables
        common_variables = [
            'time', 'time_minutes', 'time_hours', 'step_number',
            'total_power', 'total_load', 'frequency', 'voltage',
            'total_generation', 'total_storage', 'system_losses'
        ]
        
        for var in common_variables:
            self.time_series_results[var] = []
        
        # Initialize empty storage for model-specific variables
        for model_id in self.models:
            model_vars = [
                f"{model_id}_power",
                f"{model_id}_voltage",
                f"{model_id}_frequency",
                f"{model_id}_efficiency",
                f"{model_id}_status"
            ]
            for var in model_vars:
                self.time_series_results[var] = []
    
    def add_model(self, model: DynamicModel, execution_order: Optional[int] = None) -> None:
        """Add a dynamic model to the simulation.
        
        Parameters
        ----------
        model : DynamicModel
            Dynamic model to add
        execution_order : int, optional
            Execution order (lower numbers execute first)
        """
        self.models[model.config.model_id] = model
        
        if execution_order is not None:
            # Insert model at specified position
            while len(self.model_execution_order) <= execution_order:
                self.model_execution_order.append(None)
            self.model_execution_order[execution_order] = model.config.model_id
        else:
            # Add to end of execution order
            self.model_execution_order.append(model.config.model_id)
        
        # Register model with simulation state
        model._register_with_simulation_state(self.current_state)
        
        # Add model variables to results storage
        model_vars = [
            f"{model.config.model_id}_power",
            f"{model.config.model_id}_voltage",
            f"{model.config.model_id}_frequency",
            f"{model.config.model_id}_efficiency",
            f"{model.config.model_id}_status"
        ]
        
        for var in model_vars:
            if var not in self.time_series_results:
                self.time_series_results[var] = []
        
        self.logger.info(f"Added model {model.config.model_id} ({model.config.name})")
    
    def remove_model(self, model_id: str) -> bool:
        """Remove a model from the simulation.
        
        Parameters
        ----------
        model_id : str
            Model identifier
            
        Returns
        -------
        bool
            True if model was removed
        """
        if model_id not in self.models:
            return False
        
        # Remove model
        del self.models[model_id]
        
        # Remove from execution order
        if model_id in self.model_execution_order:
            self.model_execution_order.remove(model_id)
        
        # Remove from results storage
        model_vars = [
            f"{model_id}_power",
            f"{model_id}_voltage",
            f"{model_id}_frequency",
            f"{model_id}_efficiency",
            f"{model_id}_status"
        ]
        
        for var in model_vars:
            if var in self.time_series_results:
                del self.time_series_results[var]
        
        self.logger.info(f"Removed model {model_id}")
        return True
    
    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """Register an event handler.
        
        Parameters
        ----------
        event_type : str
            Event type to handle
        handler : Callable
            Handler function
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
    
    def set_progress_callback(self, callback: Callable[[SimulationProgress], None]) -> None:
        """Set progress callback for monitoring simulation progress.
        
        Parameters
        ----------
        callback : Callable
            Progress callback function
        """
        self.progress_callback = callback
    
    def _update_progress(self, step: int, total_steps: int, max_iterations: int = 0) -> None:
        """Update simulation progress.
        
        Parameters
        ----------
        step : int
            Current step
        total_steps : int
            Total number of steps
        max_iterations : int
            Current iteration count
        """
        if not self.progress_callback:
            return
        
        with self.progress_lock:
            elapsed_time = (datetime.now() - self.config.start_time).total_seconds()
            progress_percent = (step / total_steps * 100.0) if total_steps > 0 else 0.0
            
            # Estimate remaining time
            if step > 0:
                avg_time_per_step = elapsed_time / step
                estimated_remaining_time = (total_steps - step) * avg_time_per_step
            else:
                estimated_remaining_time = 0.0
            
            # Calculate steps per second
            if elapsed_time > 0:
                steps_per_second = step / elapsed_time
            else:
                steps_per_second = 0.0
            
            progress = SimulationProgress(
                current_step=step,
                total_steps=total_steps,
                progress_percent=progress_percent,
                elapsed_time=elapsed_time,
                estimated_remaining_time=estimated_remaining_time,
                steps_per_second=steps_per_second,
                current_iteration=max_iterations,
                max_iterations=self.config.max_iterations
            )
            
            self.progress_callback(progress)
    
    def _fire_event(self, event_type: str, event_data: Any) -> None:
        """Fire an event to registered handlers.
        
        Parameters
        ----------
        event_type : str
            Event type
        event_data : Any
            Event data
        """
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event_type, event_data)
                except Exception as e:
                    self.logger.error(f"Event handler failed: {e}")
    
    def _prepare_time_series_data(self) -> Dict[str, Any]:
        """Prepare time series data for current time step.
        
        Returns
        -------
        Dict[str, Any]
            Time series data
        """
        data = {}
        
        # Add current time information
        data['timestamp'] = self.current_time
        data['time_hours'] = self.current_time.hour
        data['day_of_week'] = self.current_time.weekday()
        data['season'] = (self.current_time.month - 1) // 3  # 0-3 for seasons
        
        # Add previous step data for interpolation
        if self.time_step_counter > 0:
            for model_id, model in self.models.items():
                if hasattr(model, 'get_output'):
                    data[f'{model_id}_previous_power'] = model.get_output('power', 0.0)
                    data[f'{model_id}_previous_voltage'] = model.get_output('voltage', 1.0)
        
        return data
    
    def _get_external_inputs(self) -> Dict[str, float]:
        """Get external inputs for all models.
        
        Returns
        -------
        Dict[str, float]
            External inputs
        """
        # Get global system inputs
        inputs = {
            'system_frequency': 50.0,  # Default nominal frequency
            'system_voltage': 1.0,     # Default nominal voltage
            'ambient_temperature': 20.0,  # Default ambient temperature
            'time_hours': self.current_time.hour,
            'time_minutes': self.current_time.minute
        }
        
        # Add time series inputs if available
        if self.config.time_series_data:
            time_key = self.current_time.strftime('%Y-%m-%d %H:%M:%S')
            if time_key in self.config.time_series_data:
                ts_data = self.config.time_series_data[time_key]
                inputs.update(ts_data)
        
        return inputs
    
    def _update_models_sequential(self, time_step: float) -> Tuple[bool, List[str]]:
        """Update all models sequentially.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Tuple[bool, List[str]]
            Success flag and list of errors
        """
        errors = []
        successful_updates = 0
        
        # Prepare inputs
        external_inputs = self._get_external_inputs()
        time_series_data = self._prepare_time_series_data()
        
        # Update models in order
        for model_id in self.model_execution_order:
            if model_id not in self.models:
                continue
            
            model = self.models[model_id]
            
            try:
                # Update model
                if model.status.value != 'inactive':
                    success = model.update_model(time_step, external_inputs, time_series_data)
                    if success:
                        successful_updates += 1
                    else:
                        errors.append(f"Model {model_id} update failed")
                
            except Exception as e:
                error_msg = f"Exception in model {model_id}: {str(e)}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        success = successful_updates == len(self.models)
        return success, errors
    
    def _update_models_parallel(self, time_step: float) -> Tuple[bool, List[str]]:
        """Update all models in parallel using threads.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Tuple[bool, List[str]]
            Success flag and list of errors
        """
        if not self.use_parallel:
            return self._update_models_sequential(time_step)
        
        errors = []
        successful_updates = 0
        model_results = {}
        
        # Prepare inputs for each model
        external_inputs = self._get_external_inputs()
        time_series_data = self._prepare_time_series_data()
        
        # Define update function for parallel execution
        def update_single_model(model_pair):
            model_id, model = model_pair
            try:
                if model.status.value != 'inactive':
                    success = model.update_model(time_step, external_inputs, time_series_data)
                    return model_id, success, None
                else:
                    return model_id, True, None
            except Exception as e:
                return model_id, False, str(e)
        
        # Execute updates in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            model_items = list(self.models.items())
            futures = {executor.submit(update_single_model, item): item[0] for item in model_items}
            
            for future in futures:
                try:
                    model_id, success, error = future.result(timeout=30.0)  # 30 second timeout
                    if success:
                        successful_updates += 1
                    else:
                        errors.append(f"Model {model_id} update failed: {error}")
                except Exception as e:
                    errors.append(f"Future execution failed for {futures[future]}: {str(e)}")
        
        success = successful_updates == len(self.models)
        return success, errors
    
    def _calculate_system_averages(self) -> Dict[str, float]:
        """Calculate system-wide average values.
        
        Returns
        -------
        Dict[str, float]
            System averages
        """
        total_power = 0.0
        total_load = 0.0
        total_generation = 0.0
        total_storage = 0.0
        voltage_sum = 0.0
        frequency_sum = 0.0
        efficiency_sum = 0.0
        
        active_models = 0
        
        for model_id, model in self.models.items():
            if model.status.value == 'inactive':
                continue
            
            active_models += 1
            power = model.get_output('power', 0.0)
            voltage = model.get_output('voltage', 1.0)
            frequency = model.get_output('frequency', 50.0)
            efficiency = model.get_output('efficiency', 1.0)
            
            total_power += power
            
            # Categorize by model type
            if hasattr(model.config, 'model_type'):
                if model.config.model_type == ModelType.LOAD:
                    total_load += abs(power)
                elif model.config.model_type == ModelType.GENERATOR:
                    total_generation += max(0, power)
                elif model.config.model_type == ModelType.STORAGE:
                    total_storage += power
                elif model.config.model_type == ModelType.RENEWABLE:
                    total_generation += max(0, power)
            
            voltage_sum += voltage
            frequency_sum += frequency
            efficiency_sum += efficiency
        
        # Calculate averages
        if active_models > 0:
            avg_voltage = voltage_sum / active_models
            avg_frequency = frequency_sum / active_models
            avg_efficiency = efficiency_sum / active_models
        else:
            avg_voltage = 1.0
            avg_frequency = 50.0
            avg_efficiency = 1.0
        
        return {
            'total_power': total_power,
            'total_load': total_load,
            'total_generation': total_generation,
            'total_storage': total_storage,
            'average_voltage': avg_voltage,
            'average_frequency': avg_frequency,
            'average_efficiency': avg_efficiency,
            'system_losses': total_load - total_generation - total_storage
        }
    
    def _store_step_results(self, step_info: SimulationStep) -> None:
        """Store results for current step.
        
        Parameters
        ----------
        step_info : SimulationStep
            Step information
        """
        # Store step information
        self.step_results.append(step_info)
        
        # Store system-wide values
        system_averages = self._calculate_system_averages()
        
        self.time_series_results['time'].append(self.current_time.timestamp())
        self.time_series_results['time_minutes'].append(self.total_simulation_time / 60.0)
        self.time_series_results['time_hours'].append(self.total_simulation_time / 3600.0)
        self.time_series_results['step_number'].append(step_info.step_number)
        self.time_series_results['total_power'].append(system_averages['total_power'])
        self.time_series_results['total_load'].append(system_averages['total_load'])
        self.time_series_results['frequency'].append(system_averages['average_frequency'])
        self.time_series_results['voltage'].append(system_averages['average_voltage'])
        self.time_series_results['total_generation'].append(system_averages['total_generation'])
        self.time_series_results['total_storage'].append(system_averages['total_storage'])
        self.time_series_results['system_losses'].append(system_averages['system_losses'])
        
        # Store individual model values
        for model_id, model in self.models.items():
            self.time_series_results[f"{model_id}_power"].append(model.get_output('power', 0.0))
            self.time_series_results[f"{model_id}_voltage"].append(model.get_output('voltage', 1.0))
            self.time_series_results[f"{model_id}_frequency"].append(model.get_output('frequency', 50.0))
            self.time_series_results[f"{model_id}_efficiency"].append(model.get_output('efficiency', 1.0))
            self.time_series_results[f"{model_id}_status"].append(model.get_output('status', 'unknown'))
        
        # Take snapshots at specified intervals
        if self.config.snapshot_interval_steps > 0:
            if step_info.step_number % self.config.snapshot_interval_steps == 0:
                self.snapshot_results[step_info.step_number] = self.current_state.copy()
        
        # Fire event for step completion
        self._fire_event('step_completed', step_info)
    
    def _validate_simulation(self) -> List[str]:
        """Validate simulation setup.
        
        Returns
        -------
        List[str]
            List of validation errors
        """
        errors = []
        
        # Check if models are added
        if not self.models:
            errors.append("No models added to simulation")
        
        # Check time step
        if self.time_step <= 0:
            errors.append("Invalid time step")
        
        # Check integration method compatibility
        if self.integration_method == IntegrationMethod.RK4 and self.time_step > 60:
            errors.append("RK4 method requires time step <= 60 seconds")
        
        # Check for convergence issues
        if self.config.convergence_tolerance <= 0:
            errors.append("Invalid convergence tolerance")
        
        # Check iteration limits
        if self.config.max_iterations <= 0:
            errors.append("Invalid maximum iterations")
        
        return errors
    
    def run_simulation(self) -> SimulationResult:
        """Run the complete simulation.
        
        Returns
        -------
        SimulationResult
            Simulation results
        """
        self.logger.info("Starting simulation")
        
        # Set status
        self.status = SimulationStatus.RUNNING
        self.is_running = True
        
        # Save initial state
        self.initial_state = self.current_state.copy()
        
        # Validate simulation
        validation_errors = self._validate_simulation()
        if validation_errors:
            error_msg = f"Simulation validation failed: {validation_errors}"
            self.logger.error(error_msg)
            self.status = SimulationStatus.FAILED
            raise ValueError(error_msg)
        
        # Calculate total steps
        total_steps = int(self.config.simulation_duration_seconds / self.time_step)
        self.logger.info(f"Running simulation for {total_steps} steps")
        
        try:
            # Initialize progress reporting
            if self.progress_callback:
                self._update_progress(0, total_steps)
            
            # Run simulation loop
            step_start_time = datetime.now()
            
            for step in range(total_steps):
                # Check if simulation should stop
                if self.should_stop.is_set():
                    self.logger.info("Simulation stopped by user")
                    self.status = SimulationStatus.STOPPED
                    break
                
                # Update time
                self.current_time += timedelta(seconds=self.time_step)
                self.total_simulation_time += self.time_step
                self.time_step_counter += 1
                
                # Initialize step
                step_errors = []
                step_warnings = []
                convergence_iterations = 0
                
                # Perform integration step
                step_start = time.time()
                success, step_errors = self._perform_integration_step(self.time_step)
                step_computation_time = (time.time() - step_start) * 1000.0
                
                if not success:
                    self.logger.error(f"Step {step} failed: {step_errors}")
                    self.status = SimulationStatus.FAILED
                    break
                
                # Collect step results
                step_info = SimulationStep(
                    step_number=step,
                    timestamp=self.current_time,
                    time_seconds=self.total_simulation_time,
                    time_minutes=self.total_simulation_time / 60.0,
                    time_hours=self.total_simulation_time / 3600.0,
                    dt=self.time_step,
                    status="success",
                    warnings=step_warnings,
                    errors=step_errors,
                    convergence_iterations=convergence_iterations,
                    computation_time_ms=step_computation_time
                )
                
                # Store results
                self._store_step_results(step_info)
                
                # Track performance
                self.computation_times.append(step_computation_time)
                
                # Update progress
                if step % max(1, total_steps // 20) == 0:  # Update every 5%
                    self._update_progress(step + 1, total_steps)
                
                # Check for convergence issues
                if step_errors:
                    self.logger.warning(f"Step {step} had errors: {step_errors}")
                
                # Fire events
                if step % self.config.event_check_interval == 0:
                    self._check_for_events(step)
            
            # Finalize simulation
            if self.status == SimulationStatus.RUNNING:
                self.status = SimulationStatus.COMPLETED
                self.logger.info("Simulation completed successfully")
            
        except Exception as e:
            error_msg = f"Simulation failed with exception: {str(e)}"
            self.logger.error(error_msg)
            self.status = SimulationStatus.FAILED
            self.logger.exception("Simulation exception details")
            raise
        
        finally:
            self.is_running = False
        
        # Create and return results
        return self._create_simulation_result()
    
    def _perform_integration_step(self, time_step: float) -> Tuple[bool, List[str]]:
        """Perform a single integration step.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Tuple[bool, List[str]]
            Success flag and error messages
        """
        # Use specified integration method
        if self.integration_method == IntegrationMethod.EULER:
            return self._euler_step(time_step)
        elif self.integration_method == IntegrationMethod.RK2:
            return self._rk2_step(time_step)
        elif self.integration_method == IntegrationMethod.RK4:
            return self._rk4_step(time_step)
        else:
            # Default to Euler for unsupported methods
            return self._euler_step(time_step)
    
    def _euler_step(self, time_step: float) -> Tuple[bool, List[str]]:
        """Perform forward Euler integration step.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Tuple[bool, List[str]]
            Success flag and error messages
        """
        success, errors = self._update_models_parallel(time_step)
        
        # Store previous states for convergence checking
        for model in self.models.values():
            for var in model.current_state:
                model.previous_state[var] = model.current_state[var]
        
        return success, errors
    
    def _rk2_step(self, time_step: float) -> Tuple[bool, List[str]]:
        """Perform Runge-Kutta 2nd order integration step.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Tuple[bool, List[str]]
            Success flag and error messages
        """
        # Store original states
        original_states = {}
        for model_id, model in self.models.items():
            original_states[model_id] = model.current_state.copy()
        
        # k1 = f(t, y)
        success1, errors1 = self._update_models_parallel(time_step)
        
        if not success1:
            return False, errors1
        
        # Calculate k1 derivatives
        k1_derivatives = {}
        for model_id, model in self.models.items():
            k1_derivatives[model_id] = model.calculate_derivatives()
        
        # Restore original states
        for model_id, model in self.models.items():
            model.current_state = original_states[model_id].copy()
        
        # k2 = f(t + dt, y + dt*k1)
        # Update states with k1 * dt
        for model_id, model in self.models.items():
            for var, derivative in k1_derivatives[model_id].items():
                if var in model.current_state:
                    model.current_state[var] += derivative * time_step
        
        success2, errors2 = self._update_models_parallel(time_step)
        
        if not success2:
            return False, errors2
        
        # y_new = y + dt/2 * (k1 + k2)
        k2_derivatives = {}
        for model_id, model in self.models.items():
            k2_derivatives[model_id] = model.calculate_derivatives()
        
        # Apply final update
        for model_id, model in self.models.items():
            for var in model.current_state:
                if var in k1_derivatives[model_id] and var in k2_derivatives[model_id]:
                    k1 = k1_derivatives[model_id][var]
                    k2 = k2_derivatives[model_id][var]
                    delta = (k1 + k2) * 0.5 * time_step
                    model.current_state[var] = original_states[model_id][var] + delta
        
        # Store previous states for convergence checking
        for model in self.models.values():
            model.previous_state = original_states[model.config.model_id].copy()
        
        return True, errors1 + errors2
    
    def _rk4_step(self, time_step: float) -> Tuple[bool, List[str]]:
        """Perform Runge-Kutta 4th order integration step.
        
        This is a simplified RK4 implementation that focuses on stability
        rather than full mathematical rigor for dynamic models.
        
        Parameters
        ----------
        time_step : float
            Time step in seconds
            
        Returns
        -------
        Tuple[bool, List[str]]
            Success flag and error messages
        """
        # Store original states
        original_states = {}
        for model_id, model in self.models.items():
            original_states[model_id] = model.current_state.copy()
        
        all_errors = []
        
        # k1 = f(t, y)
        success1, errors1 = self._update_models_parallel(time_step)
        if not success1:
            return False, errors1
        all_errors.extend(errors1)
        
        k1_derivatives = {}
        for model_id, model in self.models.items():
            k1_derivatives[model_id] = model.calculate_derivatives()
        
        # Restore states for k2 calculation
        for model_id, model in self.models.items():
            model.current_state = original_states[model_id].copy()
        
        # k2 = f(t + dt/2, y + dt/2*k1)
        for model_id, model in self.models.items():
            for var in model.current_state:
                if var in k1_derivatives[model_id]:
                    model.current_state[var] += k1_derivatives[model_id][var] * time_step * 0.5
        
        success2, errors2 = self._update_models_parallel(time_step * 0.5)
        if not success2:
            return False, errors2
        all_errors.extend(errors2)
        
        k2_derivatives = {}
        for model_id, model in self.models.items():
            k2_derivatives[model_id] = model.calculate_derivatives()
        
        # Restore states for k3 calculation
        for model_id, model in self.models.items():
            model.current_state = original_states[model_id].copy()
        
        # k3 = f(t + dt/2, y + dt/2*k2)
        for model_id, model in self.models.items():
            for var in model.current_state:
                if var in k2_derivatives[model_id]:
                    model.current_state[var] += k2_derivatives[model_id][var] * time_step * 0.5
        
        success3, errors3 = self._update_models_parallel(time_step * 0.5)
        if not success3:
            return False, errors3
        all_errors.extend(errors3)
        
        k3_derivatives = {}
        for model_id, model in self.models.items():
            k3_derivatives[model_id] = model.calculate_derivatives()
        
        # Restore states for k4 calculation
        for model_id, model in self.models.items():
            model.current_state = original_states[model_id].copy()
        
        # k4 = f(t + dt, y + dt*k3)
        for model_id, model in self.models.items():
            for var in model.current_state:
                if var in k3_derivatives[model_id]:
                    model.current_state[var] += k3_derivatives[model_id][var] * time_step
        
        success4, errors4 = self._update_models_parallel(time_step)
        if not success4:
            return False, errors4
        all_errors.extend(errors4)
        
        k4_derivatives = {}
        for model_id, model in self.models.items():
            k4_derivatives[model_id] = model.calculate_derivatives()
        
        # Final update: y_new = y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
        for model_id, model in self.models.items():
            for var in model.current_state:
                if (var in k1_derivatives[model_id] and var in k2_derivatives[model_id] and
                    var in k3_derivatives[model_id] and var in k4_derivatives[model_id]):
                    k1 = k1_derivatives[model_id][var]
                    k2 = k2_derivatives[model_id][var]
                    k3 = k3_derivatives[model_id][var]
                    k4 = k4_derivatives[model_id][var]
                    delta = (k1 + 2*k2 + 2*k3 + k4) * time_step / 6.0
                    model.current_state[var] = original_states[model_id][var] + delta
        
        # Store previous states for convergence checking
        for model in self.models.values():
            model.previous_state = original_states[model.config.model_id].copy()
        
        return True, all_errors
    
    def _check_for_events(self, step: int) -> None:
        """Check for simulation events.
        
        Parameters
        ----------
        step : int
            Current step number
        """
        # Check for constraint violations
        for model_id, model in self.models.items():
            violations = model.apply_constraints()
            for violation in violations:
                self._fire_event('constraint_violation', {
                    'model_id': model_id,
                    'step': step,
                    'violation': violation,
                    'timestamp': self.current_time
                })
        
        # Check for convergence issues
        if step > 0:
            recent_convergence = self.convergence_history[-10:] if len(self.convergence_history) >= 10 else self.convergence_history
            if recent_convergence and max(recent_convergence) > self.config.convergence_tolerance * 10:
                self._fire_event('convergence_warning', {
                    'step': step,
                    'max_convergence_error': max(recent_convergence),
                    'timestamp': self.current_time
                })
        
        # Check for performance issues
        if len(self.computation_times) > 0:
            recent_times = self.computation_times[-10:] if len(self.computation_times) >= 10 else self.computation_times
            if recent_times:
                avg_time = sum(recent_times) / len(recent_times)
                if avg_time > 100.0:  # 100ms per step
                    self._fire_event('performance_warning', {
                        'step': step,
                        'avg_computation_time_ms': avg_time,
                        'timestamp': self.current_time
                    })
    
    def stop_simulation(self) -> None:
        """Stop the running simulation."""
        self.should_stop.set()
        self.logger.info("Stop signal sent to simulation")
    
    def pause_simulation(self) -> None:
        """Pause the simulation."""
        self.should_stop.set()
        self.status = SimulationStatus.PAUSED
        self.logger.info("Simulation paused")
    
    def resume_simulation(self) -> None:
        """Resume a paused simulation."""
        self.should_stop.clear()
        self.status = SimulationStatus.RUNNING
        self.logger.info("Simulation resumed")
    
    def _create_simulation_result(self) -> SimulationResult:
        """Create final simulation result.
        
        Returns
        -------
        SimulationResult
            Simulation results
        """
        # Calculate performance statistics
        total_simulation_time = (datetime.now() - self.config.start_time).total_seconds()
        avg_computation_time = sum(self.computation_times) / len(self.computation_times) if self.computation_times else 0.0
        max_computation_time = max(self.computation_times) if self.computation_times else 0.0
        steps_per_second = len(self.step_results) / total_simulation_time if total_simulation_time > 0 else 0.0
        
        # Create time series DataFrame
        if self.time_series_results:
            time_series_df = pd.DataFrame(self.time_series_results)
        else:
            time_series_df = pd.DataFrame()
        
        # Create result
        result = SimulationResult(
            status=self.status,
            start_time=self.config.start_time,
            end_time=datetime.now(),
            total_steps=len(self.step_results),
            total_simulation_time=self.total_simulation_time,
            time_series_results=time_series_df,
            snapshot_results=self.snapshot_results,
            model_summaries={model_id: model.get_summary() 
                           for model_id, model in self.models.items()},
            performance_metrics={
                'avg_computation_time_ms': avg_computation_time,
                'max_computation_time_ms': max_computation_time,
                'steps_per_second': steps_per_second,
                'total_wall_time': total_simulation_time,
                'memory_usage': self.memory_usage
            },
            final_state=self.current_state.copy()
        )
        
        return result
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current simulation status.
        
        Returns
        -------
        Dict[str, Any]
            Current status information
        """
        return {
            'status': self.status.value,
            'current_time': self.current_time,
            'current_step': self.time_step_counter,
            'total_simulation_time': self.total_simulation_time,
            'is_running': self.is_running,
            'num_models': len(self.models),
            'model_statuses': {model_id: model.status.value 
                             for model_id, model in self.models.items()},
            'avg_computation_time': sum(self.computation_times) / len(self.computation_times) if self.computation_times else 0.0
        }
    
    def reset_simulation(self) -> None:
        """Reset simulation to initial state."""
        self.logger.info("Resetting simulation")
        
        # Reset all models
        for model in self.models.values():
            model._initialize_state()
            if hasattr(model, 'deactivate'):
                model.deactivate()
        
        # Reset time and counters
        self.current_time = self.config.start_time
        self.total_simulation_time = 0.0
        self.time_step_counter = 0
        
        # Reset status
        self.status = SimulationStatus.INITIALIZED
        
        # Clear results
        self.time_series_results.clear()
        self.snapshot_results.clear()
        self.step_results.clear()
        self.computation_times.clear()
        self.convergence_history.clear()
        self.memory_usage.clear()
        
        # Reinitialize results storage
        self._initialize_results_storage()
        
        self.logger.info("Simulation reset complete")


# Define import for Enum if not available
try:
    from enum import Enum
except ImportError:
    class Enum:
        def __init__(self, *args):
            for item in args:
                setattr(self, item.replace(' ', '_'), item)


# Define __all__ for module exports
__all__ = [
    # Core engine class
    'SimulationEngine',
    
    # Data classes
    'SimulationStep',
    'SimulationProgress',
    
    # Enumerations
    'IntegrationMethod'
]