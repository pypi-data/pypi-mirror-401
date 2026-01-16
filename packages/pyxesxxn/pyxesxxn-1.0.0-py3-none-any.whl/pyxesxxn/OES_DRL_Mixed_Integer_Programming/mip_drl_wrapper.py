"""MIP-DRL Wrapper Module.

This module provides a convenient wrapper for the MIP-DQN algorithm,
integrating it with the PyXESXXN framework for energy system optimization.
"""

import os
import sys
import numpy as np
import torch
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Try to import required modules
try:
    from MIP_DQN import (
        AgentMIPDQN,
        Arguments,
        ReplayBuffer,
        Actor_MIP
    )
    from random_generator_battery import (
        ESSEnv,
        Battery,
        DG,
        Grid,
        DataManager,
        Constant
    )
    from Parameters import battery_parameters, dg_parameters
    _MIP_DQN_AVAILABLE = True
except ImportError as e:
    _MIP_DQN_AVAILABLE = False
    _IMPORT_ERROR = str(e)


@dataclass
class BatteryParameters:
    """Battery system parameters.
    
    Attributes:
        capacity: Battery capacity in kW
        max_charge: Maximum charging rate in kW
        max_discharge: Maximum discharging rate in kW
        efficiency: Charge/discharge efficiency (0-1)
        degradation: Degradation cost in euro/kW
        max_soc: Maximum state of charge (0-1)
        min_soc: Minimum state of charge (0-1)
        initial_capacity: Initial capacity (0-1)
    """
    capacity: float = 500
    max_charge: float = 100
    max_discharge: float = 100
    efficiency: float = 0.9
    degradation: float = 0
    max_soc: float = 0.8
    min_soc: float = 0.2
    initial_capacity: float = 0.2
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format for internal use."""
        return {
            'capacity': self.capacity,
            'max_charge': self.max_charge,
            'max_discharge': self.max_discharge,
            'efficiency': self.efficiency,
            'degradation': self.degradation,
            'max_soc': self.max_soc,
            'min_soc': self.min_soc,
            'initial_capacity': self.initial_capacity
        }


@dataclass
class DGParameters:
    """Distributed Generator parameters.
    
    Attributes:
        a: Quadratic cost coefficient
        b: Linear cost coefficient
        c: Constant cost coefficient
        power_output_max: Maximum power output in kW
        power_output_min: Minimum power output in kW
        ramping_up: Ramping up rate in kW/h
        ramping_down: Ramping down rate in kW/h
        min_up: Minimum up time in hours
        min_down: Minimum down time in hours
    """
    a: float = 0.0034
    b: float = 3.0
    c: float = 30.0
    power_output_max: float = 150.0
    power_output_min: float = 0.0
    ramping_up: float = 100.0
    ramping_down: float = 100.0
    min_up: int = 2
    min_down: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for internal use."""
        return {
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'd': 0.03,
            'e': 4.2,
            'f': 0.031,
            'power_output_max': self.power_output_max,
            'power_output_min': self.power_output_min,
            'heat_output_max': None,
            'heat_output_min': None,
            'ramping_up': self.ramping_up,
            'ramping_down': self.ramping_down,
            'min_up': self.min_up,
            'min_down': self.min_down
        }


@dataclass
class MIPDQNConfig:
    """Configuration for MIP-DQN training.
    
    Attributes:
        num_episode: Number of training episodes
        gamma: Discount factor
        learning_rate: Learning rate for neural networks
        soft_update_tau: Soft update coefficient for target networks
        net_dim: Neural network hidden layer dimension
        batch_size: Batch size for training
        repeat_times: Number of updates per batch
        target_step: Number of steps to collect before update
        max_memo: Maximum replay buffer size
        explore_decay: Exploration rate decay
        explore_min: Minimum exploration rate
        random_seed: Random seed for reproducibility
        gpu_id: GPU device ID (-1 for CPU)
        run_name: Name for the experiment run
        save_network: Whether to save trained networks
        enable_wandb: Whether to enable Weights & Biases logging
        constrain_on: Whether to enable constraint enforcement
    """
    num_episode: int = 3000
    gamma: float = 0.995
    learning_rate: float = 1e-4
    soft_update_tau: float = 1e-2
    net_dim: int = 64
    batch_size: int = 256
    repeat_times: int = 8
    target_step: int = 1000
    max_memo: int = 50000
    explore_decay: float = 0.99
    explore_min: float = 0.3
    random_seed: int = 1234
    gpu_id: int = 0
    run_name: str = 'MIP_DQN_experiments'
    save_network: bool = True
    enable_wandb: bool = False
    constrain_on: bool = True
    
    def to_args(self) -> 'Arguments':
        """Convert to Arguments object for internal use."""
        args = Arguments()
        args.num_episode = self.num_episode
        args.gamma = self.gamma
        args.learning_rate = self.learning_rate
        args.soft_update_tau = self.soft_update_tau
        args.net_dim = self.net_dim
        args.batch_size = self.batch_size
        args.repeat_times = self.repeat_times
        args.target_step = self.target_step
        args.max_memo = self.max_memo
        args.explorate_decay = self.explore_decay
        args.explorate_min = self.explore_min
        args.random_seed = self.random_seed
        args.visible_gpu = str(self.gpu_id) if self.gpu_id >= 0 else ''
        args.run_name = self.run_name
        args.save_network = self.save_network
        return args


class EnergySystemEnvironment:
    """Wrapper for the Energy System Environment.
    
    This class provides a convenient interface to the energy system
    environment used for reinforcement learning training.
    """
    
    def __init__(
        self,
        battery_params: Optional[BatteryParameters] = None,
        dg_params: Optional[Dict[str, DGParameters]] = None,
        episode_length: int = 24,
        train_mode: bool = True
    ):
        """Initialize the energy system environment.
        
        Args:
            battery_params: Battery parameters
            dg_params: Dictionary of DG parameters
            episode_length: Length of each episode in hours
            train_mode: Whether to use training mode (True) or test mode (False)
        """
        self.battery_params = battery_params or BatteryParameters()
        self.dg_params = dg_params or {
            'gen_1': DGParameters(a=0.0034, b=3.0, c=30.0, power_output_max=150.0),
            'gen_2': DGParameters(a=0.001, b=10.0, c=40.0, power_output_max=375.0),
            'gen_3': DGParameters(a=0.001, b=15.0, c=70.0, power_output_max=500.0)
        }
        self.episode_length = episode_length
        self.train_mode = train_mode
        
        self._env = None
        self._initialize_environment()
    
    def _initialize_environment(self):
        """Initialize the internal environment."""
        if not _MIP_DQN_AVAILABLE:
            raise ImportError(
                f"MIP-DQN modules are not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        battery_dict = self.battery_params.to_dict()
        dg_dict = {k: v.to_dict() for k, v in self.dg_params.items()}
        
        self._env = ESSEnv(
            battery_parameters=battery_dict,
            dg_parameters=dg_dict,
            episode_length=self.episode_length
        )
        self._env.TRAIN = self.train_mode
    
    def reset(self) -> np.ndarray:
        """Reset the environment.
        
        Returns:
            Initial state observation
        """
        return self._env.reset()
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float, bool]:
        """Execute one step in the environment.
        
        Args:
            action: Action to take [battery_action, dg1_action, dg2_action, dg3_action]
            
        Returns:
            Tuple of (current_obs, next_obs, reward, done)
        """
        return self._env.step(action)
    
    def render(self, current_obs, next_obs, reward, done):
        """Render the current step."""
        self._env.render(current_obs, next_obs, reward, done)
    
    @property
    def state_space(self):
        """Get state space."""
        return self._env.state_space
    
    @property
    def action_space(self):
        """Get action space."""
        return self._env.action_space
    
    @property
    def operation_cost(self) -> float:
        """Get current operation cost."""
        return self._env.operation_cost
    
    @property
    def real_unbalance(self) -> float:
        """Get real unbalance."""
        return self._env.real_unbalance


class MIPDQNWrapper:
    """Wrapper for MIP-DQN algorithm.
    
    This class provides a high-level interface for training and evaluating
    the MIP-DQN algorithm on energy system optimization tasks.
    """
    
    def __init__(
        self,
        config: Optional[MIPDQNConfig] = None,
        environment: Optional[EnergySystemEnvironment] = None
    ):
        """Initialize the MIP-DQN wrapper.
        
        Args:
            config: Configuration for training
            environment: Energy system environment
        """
        self.config = config or MIPDQNConfig()
        self.environment = environment or EnergySystemEnvironment()
        
        self.agent = None
        self.buffer = None
        self.is_trained = False
        
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the agent and replay buffer."""
        self.agent = AgentMIPDQN()
        
        env = self.environment._env
        self.agent.init(
            self.config.net_dim,
            env.state_space.shape[0],
            env.action_space.shape[0],
            self.config.learning_rate,
            gpu_id=self.config.gpu_id
        )
        
        self.buffer = ReplayBuffer(
            max_len=self.config.max_memo,
            state_dim=env.state_space.shape[0],
            action_dim=env.action_space.shape[0],
            gpu_id=self.config.gpu_id
        )
    
    def train(
        self,
        num_episodes: Optional[int] = None,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """Train the MIP-DQN agent.
        
        Args:
            num_episodes: Number of training episodes (overrides config)
            verbose: Whether to print training progress
            
        Returns:
            Dictionary containing training metrics
        """
        num_episodes = num_episodes or self.config.num_episode
        
        env = self.environment._env
        agent = self.agent
        buffer = self.buffer
        config = self.config
        
        gamma = config.gamma
        batch_size = config.batch_size
        target_step = config.target_step
        repeat_times = config.repeat_times
        soft_update_tau = config.soft_update_tau
        
        reward_record = {
            'episode': [],
            'mean_episode_reward': [],
            'unbalance': [],
            'episode_operation_cost': []
        }
        loss_record = {
            'episode': [],
            'critic_loss': [],
            'actor_loss': []
        }
        
        if config.enable_wandb:
            try:
                import wandb
                wandb.init(
                    project='MIP_DQN_experiments',
                    name=config.run_name,
                    settings=wandb.Settings(start_method="fork")
                )
                wandb.config.update({
                    "epochs": num_episodes,
                    "batch_size": batch_size
                })
            except ImportError:
                if verbose:
                    print("WandB not available, skipping logging")
        
        agent.state = env.reset()
        
        collect_data = True
        while collect_data:
            if verbose:
                print(f'Collecting data... buffer: {buffer.now_len}')
            
            with torch.no_grad():
                trajectory = agent.explore_env(env, target_step)
                self._update_buffer(trajectory, gamma)
                buffer.update_now_len()
            
            if buffer.now_len >= 10000:
                collect_data = False
        
        for i_episode in range(num_episodes):
            critic_loss, actor_loss = agent.update_net(
                buffer, batch_size, repeat_times, soft_update_tau
            )
            
            if config.enable_wandb:
                try:
                    import wandb
                    wandb.log({'critic loss': critic_loss, 'custom_step': i_episode})
                    wandb.log({'actor loss': actor_loss, 'custom_step': i_episode})
                except ImportError:
                    pass
            
            loss_record['episode'].append(i_episode)
            loss_record['critic_loss'].append(critic_loss)
            loss_record['actor_loss'].append(actor_loss)
            
            with torch.no_grad():
                episode_reward, episode_unbalance, episode_operation_cost = \
                    self._get_episode_return(env, agent.act, agent.device)
                
                if config.enable_wandb:
                    try:
                        import wandb
                        wandb.log({'mean_episode_reward': episode_reward, 'custom_step': i_episode})
                        wandb.log({'unbalance': episode_unbalance, 'custom_step': i_episode})
                        wandb.log({'episode_operation_cost': episode_operation_cost, 'custom_step': i_episode})
                    except ImportError:
                        pass
                
                reward_record['episode'].append(i_episode)
                reward_record['mean_episode_reward'].append(episode_reward)
                reward_record['unbalance'].append(episode_unbalance)
                reward_record['episode_operation_cost'].append(episode_operation_cost)
            
            if verbose:
                print(
                    f'Episode {i_episode}: reward={episode_reward:.2f}, '
                    f'unbalance={episode_unbalance:.2f}, '
                    f'buffer_length={buffer.now_len}'
                )
            
            if i_episode % 10 == 0:
                with torch.no_grad():
                    agent._update_exploration_rate(config.explore_decay, config.explore_min)
                    trajectory = agent.explore_env(env, target_step)
                    self._update_buffer(trajectory, gamma)
        
        if config.enable_wandb:
            try:
                import wandb
                wandb.finish()
            except ImportError:
                pass
        
        self.is_trained = True
        
        if config.save_network:
            self._save_network()
        
        return {
            'rewards': reward_record,
            'losses': loss_record
        }
    
    def _update_buffer(self, trajectory, gamma):
        """Update replay buffer with new trajectory."""
        ten_state = torch.as_tensor([item[0] for item in trajectory], dtype=torch.float32)
        ary_other = torch.as_tensor([item[1] for item in trajectory])
        ary_other[:, 0] = ary_other[:, 0]
        ary_other[:, 1] = (1.0 - ary_other[:, 1]) * gamma
        
        self.buffer.extend_buffer(ten_state, ary_other)
    
    def _get_episode_return(self, env, act, device) -> Tuple[float, float, float]:
        """Get episode return and metrics."""
        episode_return = 0.0
        episode_unbalance = 0.0
        episode_operation_cost = 0.0
        
        state = env.reset()
        for i in range(24):
            s_tensor = torch.as_tensor((state,), device=device)
            a_tensor = act(s_tensor)
            action = a_tensor.detach().cpu().numpy()[0]
            state, next_state, reward, done = env.step(action)
            state = next_state
            episode_return += reward
            episode_unbalance += env.real_unbalance
            episode_operation_cost += env.operation_cost
            if done:
                break
        
        return episode_return, episode_unbalance, episode_operation_cost
    
    def _save_network(self):
        """Save trained networks."""
        cwd = f'./{self.agent.__class__.__name__}/{self.config.run_name}'
        os.makedirs(cwd, exist_ok=True)
        
        act_save_path = f'{cwd}/actor.pth'
        cri_save_path = f'{cwd}/critic.pth'
        
        torch.save(self.agent.act.state_dict(), act_save_path)
        torch.save(self.agent.cri.state_dict(), cri_save_path)
        
        print(f'Networks saved to {cwd}')
    
    def evaluate(self, num_episodes: int = 10) -> Dict[str, float]:
        """Evaluate the trained agent.
        
        Args:
            num_episodes: Number of evaluation episodes
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if not self.is_trained:
            raise RuntimeError("Agent must be trained before evaluation")
        
        env = self.environment._env
        env.TRAIN = False
        
        rewards = []
        unbalances = []
        operation_costs = []
        
        for _ in range(num_episodes):
            state = env.reset()
            episode_reward = 0.0
            episode_unbalance = 0.0
            episode_operation_cost = 0.0
            
            for i in range(24):
                s_tensor = torch.as_tensor((state,), device=self.agent.device)
                with torch.no_grad():
                    a_tensor = self.agent.act(s_tensor)
                action = a_tensor.detach().cpu().numpy()[0]
                state, next_state, reward, done = env.step(action)
                state = next_state
                episode_reward += reward
                episode_unbalance += env.real_unbalance
                episode_operation_cost += env.operation_cost
                if done:
                    break
            
            rewards.append(episode_reward)
            unbalances.append(episode_unbalance)
            operation_costs.append(episode_operation_cost)
        
        return {
            'mean_reward': np.mean(rewards),
            'std_reward': np.std(rewards),
            'mean_unbalance': np.mean(unbalances),
            'mean_operation_cost': np.mean(operation_costs)
        }
    
    def predict(self, state: np.ndarray) -> np.ndarray:
        """Get action for a given state.
        
        Args:
            state: Current state observation
            
        Returns:
            Action to take
        """
        if not self.is_trained:
            raise RuntimeError("Agent must be trained before prediction")
        
        s_tensor = torch.as_tensor((state,), device=self.agent.device)
        with torch.no_grad():
            a_tensor = self.agent.act(s_tensor)
        action = a_tensor.detach().cpu().numpy()[0]
        return action
    
    def load_model(self, model_path: str):
        """Load a trained model.
        
        Args:
            model_path: Path to the model directory
        """
        act_path = f'{model_path}/actor.pth'
        cri_path = f'{model_path}/critic.pth'
        
        self.agent.act.load_state_dict(torch.load(act_path))
        self.agent.cri.load_state_dict(torch.load(cri_path))
        self.is_trained = True
        print(f'Model loaded from {model_path}')


def create_mip_dqn_agent(
    config: Optional[MIPDQNConfig] = None,
    environment: Optional[EnergySystemEnvironment] = None
) -> MIPDQNWrapper:
    """Create a MIP-DQN agent with default configuration.
    
    Args:
        config: Configuration for training
        environment: Energy system environment
        
    Returns:
        Configured MIPDQNWrapper instance
    """
    return MIPDQNWrapper(config, environment)
