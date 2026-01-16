"""EV2Gym_PI_TD3 Wrapper Module.

This module provides a convenient wrapper for the PI-TD3 algorithm,
integrating it with the PyXESXXN framework for EV charging optimization.
"""

import os
import sys
import numpy as np
import torch
import yaml
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Try to import required modules
try:
    from ev2gym.models.ev2gym_env import EV2Gym
    from algorithms.pi_TD3 import PI_TD3
    from algorithms.TD3 import TD3
    from algorithms.SAC.sac import SAC
    from algorithms.SAC.pi_SAC import PI_SAC
    from algorithms.ppo import PPO
    from algorithms.pi_ppo import PhysicsInformedPPO
    from agent.state import V2G_grid_state_ModelBasedRL
    from agent.reward import Grid_V2G_profitmaxV2, V2G_profitmaxV2
    from agent.transition_fn import V2G_Grid_StateTransition
    from agent.loss_fn import V2GridLoss
    from agent.utils import ReplayBuffer
    _EV2GYM_PI_AVAILABLE = True
except ImportError as e:
    _EV2GYM_PI_AVAILABLE = False
    _IMPORT_ERROR = str(e)


@dataclass
class EVChargingConfig:
    """Configuration for EV charging environment.
    
    Attributes:
        config_file: Path to YAML configuration file
        simulation_length: Number of time steps in simulation
        timescale: Time step resolution in minutes
        num_buses: Number of grid buses
        base_power: Base power in kVA
        battery_capacity: EV battery capacity in kWh
        max_charge_power: Maximum charging power in kW
        min_battery: Minimum battery level in kWh
        num_charging_stations: Number of charging stations
        seed: Random seed for reproducibility
    """
    config_file: Optional[str] = None
    simulation_length: int = 96
    timescale: int = 15
    num_buses: int = 34
    base_power: float = 10000.0
    battery_capacity: float = 70.0
    max_charge_power: float = 22.0
    min_battery: float = 15.0
    num_charging_stations: int = 10
    seed: Optional[int] = None
    
    def get_config_path(self) -> str:
        """Get the path to the configuration file."""
        if self.config_file is None:
            return str(Path(__file__).parent / 'EV2Gym_PI_TD3' / 'config_files' / 'v2g_grid_150_300.yaml')
        return self.config_file


@dataclass
class PI_TD3Config:
    """Configuration for PI-TD3 training.
    
    Attributes:
        algorithm: Algorithm to use ('pi_td3', 'td3', 'pi_sac', 'sac', 'ppo', 'pi_ppo')
        discount: Discount factor gamma
        tau: Soft update coefficient
        lambda_: TD(lambda) parameter
        policy_noise: Policy noise for target policy smoothing
        noise_clip: Noise clip for target policy smoothing
        policy_freq: Frequency of delayed policy updates
        look_ahead: Lookahead horizon for physics-informed methods
        ph_coeff: Physics coefficient for physics-informed loss
        mlp_hidden_dim: Hidden layer dimension for neural networks
        actor_lr: Actor learning rate
        critic_lr: Critic learning rate
        batch_size: Batch size for training
        buffer_size: Maximum replay buffer size
        max_timesteps: Maximum training timesteps
        eval_freq: Evaluation frequency
        device: Device to use ('cuda:0', 'cpu')
        seed: Random seed
        enable_wandb: Whether to enable Weights & Biases logging
        group_name: WandB experiment group name
        discrete_actions: Number of discrete action steps (0 for continuous)
    """
    algorithm: str = 'pi_td3'
    discount: float = 0.99
    tau: float = 0.005
    lambda_: float = 0.95
    policy_noise: float = 0.2
    noise_clip: float = 0.5
    policy_freq: int = 2
    look_ahead: int = 2
    ph_coeff: float = 1.0
    mlp_hidden_dim: int = 256
    actor_lr: float = 2e-3
    critic_lr: float = 5e-4
    batch_size: int = 256
    buffer_size: int = 1000000
    max_timesteps: int = 1000000
    eval_freq: int = 5000
    device: str = 'cuda:0'
    seed: int = 0
    enable_wandb: bool = False
    group_name: str = 'ev2gym_experiments'
    discrete_actions: int = 0


class EVChargingEnvironment:
    """Wrapper for the EV2Gym environment.
    
    This class provides a convenient interface to the EV charging
    environment used for reinforcement learning training.
    """
    
    def __init__(
        self,
        config: Optional[EVChargingConfig] = None,
        config_file: Optional[str] = None,
        seed: Optional[int] = None
    ):
        """Initialize the EV charging environment.
        
        Args:
            config: EV charging configuration
            config_file: Path to YAML configuration file (overrides config)
            seed: Random seed (overrides config)
        """
        self.config = config or EVChargingConfig()
        if config_file is not None:
            self.config.config_file = config_file
        if seed is not None:
            self.config.seed = seed
        
        self._env = None
        self._initialize_environment()
    
    def _initialize_environment(self):
        """Initialize the internal environment."""
        if not _EV2GYM_PI_AVAILABLE:
            raise ImportError(
                f"EV2Gym-PI-TD3 modules are not available. "
                f"Import error: {_IMPORT_ERROR}"
            )
        
        config_path = self.config.get_config_path()
        
        self._env = EV2Gym(
            config_file=config_path,
            seed=self.config.seed,
            verbose=False
        )
    
    def reset(self, seed: Optional[int] = None) -> Tuple[np.ndarray, Dict]:
        """Reset the environment.
        
        Args:
            seed: Random seed for this episode
            
        Returns:
            Tuple of (observation, info)
        """
        if seed is not None:
            return self._env.reset(seed=seed)
        return self._env.reset()
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute one step in the environment.
        
        Args:
            action: Action to take
            
        Returns:
            Tuple of (observation, reward, terminated, truncated, info)
        """
        return self._env.step(action)
    
    @property
    def observation_space(self):
        """Get observation space."""
        return self._env.observation_space
    
    @property
    def action_space(self):
        """Get action space."""
        return self._env.action_space
    
    @property
    def simulation_length(self) -> int:
        """Get simulation length."""
        return self._env.simulation_length


class EV2GymPIWrapper:
    """Wrapper for PI-TD3 algorithm.
    
    This class provides a high-level interface for training and evaluating
    physics-informed reinforcement learning algorithms on EV charging tasks.
    """
    
    def __init__(
        self,
        config: Optional[PI_TD3Config] = None,
        environment: Optional[EVChargingEnvironment] = None
    ):
        """Initialize the EV2Gym PI wrapper.
        
        Args:
            config: Configuration for training
            environment: EV charging environment
        """
        self.config = config or PI_TD3Config()
        self.environment = environment or EVChargingEnvironment()
        
        self.agent = None
        self.replay_buffer = None
        self.is_trained = False
        
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the agent and replay buffer."""
        env = self.environment._env
        
        state_dim = env.observation_space.shape[0]
        action_dim = env.action_space.shape[0]
        max_action = env.action_space.high[0]
        
        device = torch.device(self.config.device if torch.cuda.is_available() else 'cpu')
        
        if self.config.algorithm == 'pi_td3':
            self.agent = PI_TD3(
                state_dim=state_dim,
                action_dim=action_dim,
                max_action=max_action,
                device=device,
                ph_coeff=self.config.ph_coeff,
                discount=self.config.discount,
                tau=self.config.tau,
                lambda_=self.config.lambda_,
                policy_noise=self.config.policy_noise,
                noise_clip=self.config.noise_clip,
                policy_freq=self.config.policy_freq,
                mlp_hidden_dim=self.config.mlp_hidden_dim,
                look_ahead=self.config.look_ahead
            )
        elif self.config.algorithm == 'td3':
            self.agent = TD3(
                state_dim=state_dim,
                action_dim=action_dim,
                max_action=max_action,
                device=device,
                discount=self.config.discount,
                tau=self.config.tau,
                policy_noise=self.config.policy_noise,
                noise_clip=self.config.noise_clip,
                policy_freq=self.config.policy_freq,
                mlp_hidden_dim=self.config.mlp_hidden_dim
            )
        else:
            raise ValueError(f"Algorithm {self.config.algorithm} not supported")
        
        self.replay_buffer = ReplayBuffer(
            state_dim=state_dim,
            action_dim=action_dim,
            max_size=self.config.buffer_size,
            device=device
        )
    
    def train(
        self,
        max_timesteps: Optional[int] = None,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """Train the agent.
        
        Args:
            max_timesteps: Maximum training timesteps (overrides config)
            verbose: Whether to print training progress
            
        Returns:
            Dictionary containing training metrics
        """
        max_timesteps = max_timesteps or self.config.max_timesteps
        
        env = self.environment._env
        agent = self.agent
        replay_buffer = self.replay_buffer
        config = self.config
        
        state, _ = env.reset(seed=config.seed)
        
        episode_reward = 0
        episode_num = 0
        
        training_rewards = []
        training_losses = {
            'critic_loss': [],
            'actor_loss': [],
            'physics_loss': []
        }
        
        if config.enable_wandb:
            try:
                import wandb
                wandb.init(
                    project='EV2Gym_PI_TD3',
                    name=config.group_name,
                    config=config.__dict__
                )
            except ImportError:
                if verbose:
                    print("WandB not available, skipping logging")
        
        for t in range(max_timesteps):
            action = agent.select_action(state)
            
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            replay_buffer.add(state, action, reward, next_state, done)
            state = next_state
            episode_reward += reward
            
            if done:
                episode_num += 1
                training_rewards.append(episode_reward)
                
                if verbose and episode_num % 10 == 0:
                    print(f"Episode {episode_num}, Reward: {episode_reward:.2f}")
                
                state, _ = env.reset(seed=config.seed + episode_num)
                episode_reward = 0
            
            if t >= config.batch_size:
                loss_info = agent.train(replay_buffer, batch_size=config.batch_size)
                
                if hasattr(agent, 'loss_dict'):
                    training_losses['critic_loss'].append(agent.loss_dict.get('critic_loss', 0))
                    training_losses['actor_loss'].append(agent.loss_dict.get('actor_loss', 0))
                    training_losses['physics_loss'].append(agent.loss_dict.get('physics_loss', 0))
                
                if config.enable_wandb and t % 100 == 0:
                    try:
                        import wandb
                        wandb.log({
                            'episode': episode_num,
                            'reward': episode_reward,
                            'timestep': t,
                            **agent.loss_dict
                        })
                    except ImportError:
                        pass
        
        if config.enable_wandb:
            try:
                import wandb
                wandb.finish()
            except ImportError:
                pass
        
        self.is_trained = True
        
        return {
            'rewards': training_rewards,
            'losses': training_losses
        }
    
    def evaluate(
        self,
        num_episodes: int = 10,
        seed: Optional[int] = None
    ) -> Dict[str, float]:
        """Evaluate the trained agent.
        
        Args:
            num_episodes: Number of evaluation episodes
            seed: Random seed for evaluation
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if not self.is_trained:
            raise RuntimeError("Agent must be trained before evaluation")
        
        env = self.environment._env
        agent = self.agent
        
        rewards = []
        
        for i in range(num_episodes):
            state, _ = env.reset(seed=seed + i if seed else None)
            episode_reward = 0
            done = False
            
            while not done:
                action = agent.select_action(state, evaluate=True)
                state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                episode_reward += reward
            
            rewards.append(episode_reward)
        
        return {
            'mean_reward': np.mean(rewards),
            'std_reward': np.std(rewards),
            'min_reward': np.min(rewards),
            'max_reward': np.max(rewards)
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
        
        return self.agent.select_action(state)
    
    def save_model(self, model_path: str):
        """Save the trained model.
        
        Args:
            model_path: Path to save the model
        """
        if not self.is_trained:
            raise RuntimeError("Agent must be trained before saving")
        
        os.makedirs(model_path, exist_ok=True)
        
        torch.save({
            'actor_state_dict': self.agent.actor.state_dict(),
            'critic_state_dict': self.agent.critic.state_dict(),
            'actor_target_state_dict': self.agent.actor_target.state_dict(),
            'critic_target_state_dict': self.agent.critic_target.state_dict(),
            'actor_optimizer_state_dict': self.agent.actor_optimizer.state_dict(),
            'critic_optimizer_state_dict': self.agent.critic_optimizer.state_dict(),
            'config': self.config.__dict__
        }, os.path.join(model_path, 'model.pth'))
        
        print(f'Model saved to {model_path}')
    
    def load_model(self, model_path: str):
        """Load a trained model.
        
        Args:
            model_path: Path to the model file
        """
        checkpoint = torch.load(model_path)
        
        self.agent.actor.load_state_dict(checkpoint['actor_state_dict'])
        self.agent.critic.load_state_dict(checkpoint['critic_state_dict'])
        self.agent.actor_target.load_state_dict(checkpoint['actor_target_state_dict'])
        self.agent.critic_target.load_state_dict(checkpoint['critic_target_state_dict'])
        self.agent.actor_optimizer.load_state_dict(checkpoint['actor_optimizer_state_dict'])
        self.agent.critic_optimizer.load_state_dict(checkpoint['critic_optimizer_state_dict'])
        
        self.is_trained = True
        print(f'Model loaded from {model_path}')


def create_ev2gym_pi_agent(
    config: Optional[PI_TD3Config] = None,
    environment: Optional[EVChargingEnvironment] = None
) -> EV2GymPIWrapper:
    """Create an EV2Gym PI-TD3 agent with default configuration.
    
    Args:
        config: Configuration for training
        environment: EV charging environment
        
    Returns:
        Configured EV2GymPIWrapper instance
    """
    return EV2GymPIWrapper(config, environment)
