"""
Dynamic Simulation Module for Energy Systems.

This module provides comprehensive dynamic simulation capabilities for energy systems,
including time-series simulation, dynamic system response modeling, control strategies,
and real-time operational optimization.

Key Features:
- Time-series data processing and management
- Dynamic system modeling and simulation
- Control strategies and optimization
- Real-time operational simulation
- Energy system stability analysis
- Frequency and voltage regulation modeling
"""

from .base import (
    SimulationBase,
    SimulationConfig,
    SimulationResult,
    SimulationEvent,
    SimulationState
)

from .time_series import (
    TimeSeriesProcessor,
    DataSource,
    WeatherDataSource,
    LoadDataSource,
    PriceDataSource,
    TimeSeriesConfig
)

from .dynamic_models import (
    DynamicComponent,
    FrequencyResponseModel,
    VoltageRegulationModel,
    StorageDynamicModel,
    GeneratorDynamicsModel,
    LoadResponseModel,
    GridStabilityModel
)

from .simulation_engine import (
    SimulationEngine,
    RealTimeSimulationEngine,
    BatchSimulationEngine,
    ParallelSimulationEngine
)

from .control_strategies import (
    ControlStrategy,
    MPCController,
    PredictiveController,
    AdaptiveController,
    DroopControl,
    FrequencyControl,
    VoltageControl,
    EnergyManagementSystem
)

__version__ = "1.0.0"
__all__ = [
    # Base classes
    "SimulationBase",
    "SimulationConfig", 
    "SimulationResult",
    "SimulationEvent",
    "SimulationState",
    
    # Time series processing
    "TimeSeriesProcessor",
    "DataSource",
    "WeatherDataSource",
    "LoadDataSource", 
    "PriceDataSource",
    "TimeSeriesConfig",
    
    # Dynamic models
    "DynamicComponent",
    "FrequencyResponseModel",
    "VoltageRegulationModel", 
    "StorageDynamicModel",
    "GeneratorDynamicsModel",
    "LoadResponseModel",
    "GridStabilityModel",
    
    # Simulation engines
    "SimulationEngine",
    "RealTimeSimulationEngine",
    "BatchSimulationEngine",
    "ParallelSimulationEngine",
    
    # Control strategies
    "ControlStrategy",
    "MPCController",
    "PredictiveController", 
    "AdaptiveController",
    "DroopControl",
    "FrequencyControl",
    "VoltageControl",
    "EnergyManagementSystem"
]

# Default simulation parameters
DEFAULT_SIMULATION_CONFIG = {
    'time_step': 1.0,  # seconds
    'simulation_duration': 3600,  # 1 hour in seconds
    'start_time': '2024-01-01 00:00:00',
    'data_sources': ['weather', 'load', 'price'],
    'control_strategies': ['frequency_control', 'voltage_control'],
    'dynamic_models': ['frequency_response', 'storage_dynamics'],
    'real_time_mode': False,
    'parallel_processing': False
}