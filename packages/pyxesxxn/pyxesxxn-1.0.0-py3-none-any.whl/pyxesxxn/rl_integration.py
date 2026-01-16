"""Unified Reinforcement Learning Module.

This module provides a unified interface for all reinforcement learning
algorithms integrated into PyXESXXN, including MIP-DQN and PI-TD3.
"""

from typing import Optional, Dict, Any, Union
import warnings

try:
    from .OES_DRL_Mixed_Integer_Programming import (
        MIPDQNWrapper,
        MIPDQNConfig,
        EnergySystemEnvironment,
        BatteryParameters,
        DGParameters
    )
    _mip_drl_available = True
except ImportError:
    _mip_drl_available = False
    MIPDQNWrapper = None
    MIPDQNConfig = None
    EnergySystemEnvironment = None
    BatteryParameters = None
    DGParameters = None

try:
    from .EV2Gym_PI_TD3 import (
        EV2GymPIWrapper,
        PI_TD3Config,
        EVChargingEnvironment,
        EVChargingConfig
    )
    _ev2gym_pi_available = True
except ImportError:
    _ev2gym_pi_available = False
    EV2GymPIWrapper = None
    PI_TD3Config = None
    EVChargingEnvironment = None
    EVChargingConfig = None


class RLAgentFactory:
    """Factory class for creating reinforcement learning agents.
    
    This class provides a unified interface for creating different
    types of RL agents for energy system optimization.
    """
    
    @staticmethod
    def create_mip_dqn_agent(
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional['MIPDQNWrapper']:
        """Create a MIP-DQN agent for energy system scheduling.
        
        Args:
            config: Configuration dictionary for MIP-DQN
            **kwargs: Additional configuration parameters
            
        Returns:
            MIPDQNWrapper instance or None if not available
            
        Example:
            >>> agent = RLAgentFactory.create_mip_dqn_agent(
            ...     num_episodes=1000,
            ...     learning_rate=1e-4,
            ...     gpu_id=0
            ... )
            >>> results = agent.train()
        """
        if not _mip_drl_available:
            warnings.warn(
                "MIP-DQN module is not available. "
                "Please ensure all dependencies are installed.",
                ImportWarning
            )
            return None
        
        if config is None:
            config = {}
        
        config_dict = {**config, **kwargs}
        mip_config = MIPDQNConfig(**config_dict)
        
        return MIPDQNWrapper(config=mip_config)
    
    @staticmethod
    def create_pi_td3_agent(
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional['EV2GymPIWrapper']:
        """Create a PI-TD3 agent for EV charging management.
        
        Args:
            config: Configuration dictionary for PI-TD3
            **kwargs: Additional configuration parameters
            
        Returns:
            EV2GymPIWrapper instance or None if not available
            
        Example:
            >>> agent = RLAgentFactory.create_pi_td3_agent(
            ...     algorithm='pi_td3',
            ...     look_ahead=5,
            ...     device='cuda:0'
            ... )
            >>> results = agent.train()
        """
        if not _ev2gym_pi_available:
            warnings.warn(
                "EV2Gym-PI-TD3 module is not available. "
                "Please ensure all dependencies are installed.",
                ImportWarning
            )
            return None
        
        if config is None:
            config = {}
        
        config_dict = {**config, **kwargs}
        pi_config = PI_TD3Config(**config_dict)
        
        return EV2GymPIWrapper(config=pi_config)
    
    @staticmethod
    def create_energy_system_env(
        battery_params: Optional[Dict[str, Any]] = None,
        dg_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional['EnergySystemEnvironment']:
        """Create an energy system environment for MIP-DQN.
        
        Args:
            battery_params: Battery configuration parameters
            dg_params: Distributed generator configuration parameters
            **kwargs: Additional environment parameters
            
        Returns:
            EnergySystemEnvironment instance or None if not available
        """
        if not _mip_drl_available:
            warnings.warn(
                "MIP-DQN module is not available.",
                ImportWarning
            )
            return None
        
        battery_config = BatteryParameters(**(battery_params or {}))
        dg_config = None
        if dg_params:
            dg_config = {
                'gen_1': DGParameters(**(dg_params.get('gen_1', {}))),
                'gen_2': DGParameters(**(dg_params.get('gen_2', {}))),
                'gen_3': DGParameters(**(dg_params.get('gen_3', {})))
            }
        
        return EnergySystemEnvironment(
            battery_params=battery_config,
            dg_params=dg_config,
            **kwargs
        )
    
    @staticmethod
    def create_ev_charging_env(
        config_file: Optional[str] = None,
        **kwargs
    ) -> Optional['EVChargingEnvironment']:
        """Create an EV charging environment for PI-TD3.
        
        Args:
            config_file: Path to YAML configuration file
            **kwargs: Additional environment parameters
            
        Returns:
            EVChargingEnvironment instance or None if not available
        """
        if not _ev2gym_pi_available:
            warnings.warn(
                "EV2Gym-PI-TD3 module is not available.",
                ImportWarning
            )
            return None
        
        return EVChargingEnvironment(
            config_file=config_file,
            **kwargs
        )


def get_available_algorithms() -> Dict[str, bool]:
    """Get dictionary of available RL algorithms.
    
    Returns:
        Dictionary mapping algorithm names to availability status
    """
    return {
        'mip_dqn': _mip_drl_available,
        'pi_td3': _ev2gym_pi_available,
        'td3': _ev2gym_pi_available,
        'pi_sac': _ev2gym_pi_available,
        'sac': _ev2gym_pi_available,
        'ppo': _ev2gym_pi_available,
        'pi_ppo': _ev2gym_pi_available
    }


def check_dependencies() -> Dict[str, bool]:
    """Check availability of RL module dependencies.
    
    Returns:
        Dictionary mapping dependency names to availability status
    """
    dependencies = {
        'mip_drl': _mip_drl_available,
        'ev2gym_pi': _ev2gym_pi_available
    }
    
    return dependencies


__all__ = [
    'RLAgentFactory',
    'get_available_algorithms',
    'check_dependencies',
    'MIPDQNWrapper',
    'MIPDQNConfig',
    'EnergySystemEnvironment',
    'BatteryParameters',
    'DGParameters',
    'EV2GymPIWrapper',
    'PI_TD3Config',
    'EVChargingEnvironment',
    'EVChargingConfig'
]
