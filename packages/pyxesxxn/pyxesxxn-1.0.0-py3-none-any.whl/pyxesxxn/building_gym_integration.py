"""
BuildingGym Integration Module for PyXESXXN

This module provides a convenient interface to integrate BuildingGym functionality
into PyXESXXN for building energy management using reinforcement learning.

BuildingGym is an open-source toolbox for AI-based building energy management
using reinforcement learning, supporting multiple RL algorithms.

Reference:
    Dai, Xilei et al. "BuildingGym: An open-source toolbox for AI-based 
    building energy management using reinforcement learning", Building Simulation, 2025.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Type
from dataclasses import dataclass, field
import warnings

try:
    import numpy as np
    import torch
    import pandas as pd
    import gymnasium as gym
    from gymnasium.spaces import Box, Discrete
    _BUILDINGGYM_BASE_DEPS = True
except ImportError as e:
    _BUILDINGGYM_BASE_DEPS = False
    warnings.warn(
        f"BuildingGym base dependencies not available: {e}. "
        "Install required packages: numpy, torch, pandas, gymnasium"
    )
    # Define placeholders for type hints
    Box = None
    Discrete = None

try:
    from stable_baselines3.common.buffers import ReplayBuffer
    _SB3_AVAILABLE = True
except ImportError:
    _SB3_AVAILABLE = False

_BUILDINGGYM_AVAILABLE = False

if _BUILDINGGYM_BASE_DEPS:
    try:
        buildinggym_path = Path(__file__).parent / "BuildingGym"
        if buildinggym_path.exists():
            sys.path.insert(0, str(buildinggym_path))
            
            from env.env import buildinggym_env
            from rl.ppo.ppo import PPO
            from rl.dqn.dqn import DQN
            from rl.a2c.a2c import A2C
            from rl.pg.pg import PG
            from rl.td3.td3 import TD3
            from rl.ppo.ppo_para import Args as PPOArgs
            from rl.dqn.dqn_para import Args as DQNArgs
            from rl.a2c.a2c_para import Args as A2CArgs
            from rl.pg.pg_para import Args as PGArgs
            from rl.td3.td3_para import Args as TD3Args
            _BUILDINGGYM_AVAILABLE = True
    except ImportError as e:
        warnings.warn(
            f"BuildingGym modules not available: {e}. "
            "BuildingGym integration will be limited."
        )


@dataclass
class BuildingGymConfig:
    """Configuration for BuildingGym environment and training.
    
    Attributes:
        idf_file: Path to EnergyPlus IDF file
        epw_file: Path to EnergyPlus EPW weather file
        algorithm: RL algorithm to use ('ppo', 'dqn', 'a2c', 'pg', 'td3')
        observation_vars: List of observation variable names
        external_obs_vars: Optional list of external observation variables
        action_type: Action space type (Box or Discrete)
        work_time_start: Work start time (HH:MM format)
        work_time_end: Work end time (HH:MM format)
        n_time_step: Time step in minutes
        device: Device to use ('cpu' or 'cuda')
    """
    idf_file: str
    epw_file: str
    algorithm: str = 'ppo'
    observation_vars: List[str] = field(default_factory=lambda: ['t_out', 't_in', 'occ', 'light', 'Equip'])
    external_obs_vars: Optional[List[str]] = None
    action_type: str = 'discrete'
    work_time_start: str = '08:00'
    work_time_end: str = '18:00'
    n_time_step: int = 10
    device: str = 'cpu'
    
    def __post_init__(self):
        if self.algorithm.lower() not in ['ppo', 'dqn', 'a2c', 'pg', 'td3']:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")


class BuildingGymWrapper:
    """Wrapper for BuildingGym functionality in PyXESXXN.
    
    This class provides a convenient interface to use BuildingGym's
    reinforcement learning algorithms for building energy management.
    
    Example:
        >>> config = BuildingGymConfig(
        ...     idf_file='building.idf',
        ...     epw_file='weather.epw',
        ...     algorithm='ppo'
        ... )
        >>> wrapper = BuildingGymWrapper(config)
        >>> wrapper.setup_environment()
        >>> results = wrapper.train(epochs=100)
    """
    
    @staticmethod
    def _get_algorithm_map():
        """Get algorithm map dynamically based on availability."""
        if not _BUILDINGGYM_AVAILABLE:
            return {}
        
        return {
            'ppo': (PPO, PPOArgs),
            'dqn': (DQN, DQNArgs),
            'a2c': (A2C, A2CArgs),
            'pg': (PG, PGArgs),
            'td3': (TD3, TD3Args)
        }
    
    def __init__(self, config: BuildingGymConfig):
        """Initialize BuildingGym wrapper.
        
        Args:
            config: BuildingGymConfig instance with environment and training parameters
        """
        if not _BUILDINGGYM_AVAILABLE:
            raise RuntimeError(
                "BuildingGym is not available. Please ensure BuildingGym directory "
                "exists and all dependencies are installed."
            )
        
        self.config = config
        self.env = None
        self.algo = None
        self.ep_world = None
        self.ep_para = None
        self._initialized = False
        
    def setup_environment(self, custom_env_class: Optional[Type] = None):
        """Setup the BuildingGym environment.
        
        Args:
            custom_env_class: Optional custom environment class that inherits from buildinggym_env
        """
        if not _BUILDINGGYM_AVAILABLE:
            raise RuntimeError("BuildingGym is not available")
        
        try:
            from controllables.core.tools.gymnasium import (
                DictSpace, BoxSpace, Agent
            )
            from controllables.energyplus import (
                System, Actuator, OutputVariable
            )
        except ImportError:
            raise ImportError(
                "controllables package not available. "
                "Install from: git+https://github.com/XileiDai/test"
            )
        
        self.ep_world = System(
            building=self.config.idf_file,
            weather=self.config.epw_file,
            report='tmp/ooep-report-pyxesxxn',
            repeat=False,
        ).add('logging:progress')
        
        self.ep_para = Agent(dict(
            action_space=DictSpace({
                'Thermostat': BoxSpace(
                    low=22., high=30.,
                    dtype=np.float32,
                    shape=(),
                ).bind(self.ep_world[Actuator.Ref(
                    type='Schedule:Compact',
                    control_type='Schedule Value',
                    key='Always 26',
                )])
            }),    
            observation_space=DictSpace({
                't_in': BoxSpace(
                    low=-np.inf, high=+np.inf,
                    dtype=np.float32,
                    shape=(),
                ).bind(self.ep_world[OutputVariable.Ref(
                    type='Zone Mean Air Temperature',
                    key='Perimeter_ZN_1 ZN',
                )]),
                't_out': BoxSpace(
                    low=-np.inf, high=+np.inf,
                    dtype=np.float32,
                    shape=(),
                ).bind(self.ep_world[OutputVariable.Ref(
                    type='Site Outdoor Air Drybulb Temperature',
                    key='Environment',
                )]),
                'occ': BoxSpace(
                    low=-np.inf, high=+np.inf,
                    dtype=np.float32,
                    shape=(),
                ).bind(self.ep_world[OutputVariable.Ref(
                    type='Schedule Value',
                    key='Small Office Bldg Occ',
                )]),
                'light': BoxSpace(
                    low=-np.inf, high=+np.inf,
                    dtype=np.float32,
                    shape=(),
                ).bind(self.ep_world[OutputVariable.Ref(
                    type='Schedule Value',
                    key='Office Bldg Light',
                )]),
                'Equip': BoxSpace(
                    low=-np.inf, high=+np.inf,
                    dtype=np.float32,
                    shape=(),
                ).bind(self.ep_world[OutputVariable.Ref(
                    type='Schedule Value',
                    key='Small Office Bldg Equip',
                )]),
            }),
        ))
        
        if custom_env_class is not None:
            env_class = custom_env_class
        else:
            env_class = type('DefaultBuildingEnv', (buildinggym_env,), {})
        
        action_space = self._create_action_space()
        
        self.env = env_class(
            idf_file=self.config.idf_file,
            epw_file=self.config.epw_file,
            ep_world=self.ep_world,
            ep_para=self.ep_para,
            action_type=action_space,
            args=self._get_algorithm_args(),
            inter_obs_var=self.config.observation_vars,
            ext_obs_var=self.config.external_obs_vars
        )
        
        self._initialized = True
        
    def _create_action_space(self):
        """Create action space based on configuration."""
        if not _BUILDINGGYM_BASE_DEPS:
            raise RuntimeError("BuildingGym base dependencies not available")
        
        if self.config.action_type.lower() == 'discrete':
            return Discrete(3)
        else:
            return Box(np.array([0.0]), np.array([1.0]))
    
    def _get_algorithm_args(self):
        """Get algorithm-specific arguments."""
        algo_map = self._get_algorithm_map()
        algo_class, args_class = algo_map[self.config.algorithm.lower()]
        return args_class
    
    def setup_algorithm(self, run_name: Optional[str] = None, **kwargs):
        """Setup the RL algorithm.
        
        Args:
            run_name: Optional name for the training run
            **kwargs: Additional algorithm-specific parameters
        """
        if not self._initialized:
            raise RuntimeError("Environment not initialized. Call setup_environment() first.")
        
        algo_map = self._get_algorithm_map()
        algo_class, args_class = algo_map[self.config.algorithm.lower()]
        args = args_class()
        
        for key, value in kwargs.items():
            if hasattr(args, key):
                setattr(args, key, value)
        
        if run_name is None:
            import time
            run_name = f"{self.config.algorithm}__{int(time.time())}"
        
        self.algo = algo_class(
            policy_network=None,
            env=self.env,
            args=args,
            run_name=run_name
        )
        
        self.env.setup(algo=self.algo)
        
    def train(self, total_epochs: int = 100, callback=None) -> Dict[str, Any]:
        """Train the RL agent.
        
        Args:
            total_epochs: Number of training epochs
            callback: Optional callback function
            
        Returns:
            Dictionary containing training results
        """
        if self.algo is None:
            raise RuntimeError("Algorithm not initialized. Call setup_algorithm() first.")
        
        _, performance = self.algo.learn(total_epochs, callback)
        
        return {
            'performance': performance,
            'algorithm': self.config.algorithm,
            'epochs': total_epochs
        }
    
    def run(self, train: bool = True) -> Dict[str, Any]:
        """Run the environment.
        
        Args:
            train: Whether to train during run
            
        Returns:
            Dictionary containing run results
        """
        if not self._initialized:
            raise RuntimeError("Environment not initialized. Call setup_environment() first.")
        
        self.env.run(agent=None, train=train)
        
        return {
            'status': 'completed',
            'train': train
        }
    
    def get_results(self) -> Optional[pd.DataFrame]:
        """Get simulation results if available.
        
        Returns:
            DataFrame with simulation results or None
        """
        if hasattr(self.env, 'sensor_dic'):
            return self.env.sensor_dic
        return None
    
    def save_model(self, path: str):
        """Save the trained model.
        
        Args:
            path: Path to save the model
        """
        if self.algo is None:
            raise RuntimeError("No trained model to save")
        
        torch.save(self.algo.policy.state_dict(), path)
    
    def load_model(self, path: str):
        """Load a trained model.
        
        Args:
            path: Path to load the model from
        """
        if self.algo is None:
            raise RuntimeError("Algorithm not initialized")
        
        self.algo.policy.load_state_dict(torch.load(path))


def create_building_gym_environment(
    idf_file: str,
    epw_file: str,
    algorithm: str = 'ppo',
    **kwargs
) -> BuildingGymWrapper:
    """Convenience function to create a BuildingGym environment.
    
    Args:
        idf_file: Path to EnergyPlus IDF file
        epw_file: Path to EnergyPlus EPW weather file
        algorithm: RL algorithm to use
        **kwargs: Additional configuration parameters
        
    Returns:
        Configured BuildingGymWrapper instance
    """
    config = BuildingGymConfig(
        idf_file=idf_file,
        epw_file=epw_file,
        algorithm=algorithm,
        **kwargs
    )
    wrapper = BuildingGymWrapper(config)
    wrapper.setup_environment()
    wrapper.setup_algorithm()
    
    return wrapper


def get_available_algorithms() -> List[str]:
    """Get list of available RL algorithms.
    
    Returns:
        List of algorithm names
    """
    if not _BUILDINGGYM_AVAILABLE:
        return []
    
    return list(BuildingGymWrapper._get_algorithm_map().keys())


def check_buildinggym_dependencies() -> Dict[str, bool]:
    """Check BuildingGym dependencies.
    
    Returns:
        Dictionary with dependency availability status
    """
    return {
        'base_dependencies': _BUILDINGGYM_BASE_DEPS,
        'stable_baselines3': _SB3_AVAILABLE,
        'buildinggym': _BUILDINGGYM_AVAILABLE
    }


__all__ = [
    'BuildingGymConfig',
    'BuildingGymWrapper',
    'create_building_gym_environment',
    'get_available_algorithms',
    'check_buildinggym_dependencies'
]
