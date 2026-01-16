"""
Mobile Energy Storage System (MESS) optimization module.

This module provides optimization algorithms and models for mobile energy
storage systems with carbon-aware scheduling, based on the paper:
"基于双层多智能体深度强化学习的移动储能低碳时空优化调度技术报告"
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Union, Any, Tuple, Callable
from dataclasses import dataclass, field
import numpy as np
import pandas as pd

from .abstract import (
    Optimizer,
    OptimizationConfig,
    OptimizationType,
    SolverType
)


class MESSOptimizationType(Enum):
    """Types of MESS optimization problems."""
    SPATIAL_SCHEDULING = "spatial_scheduling"  # 空间转移决策
    CHARGE_DISCHARGE = "charge_discharge"  # 充放电决策
    COMBINED = "combined"  # 联合决策


class MESSAlgorithmType(Enum):
    """Types of algorithms for MESS optimization."""
    MAPPO = "mappo"  # 多智能体近端策略优化（空间转移决策）
    MATD3 = "matd3"  # 多智能体双延迟深度确定性策略梯度（充放电决策）
    DQN = "dqn"  # 深度Q网络
    PPO = "ppo"  # 近端策略优化
    SAC = "sac"  # 软演员评论家


@dataclass
class CarbonTradingParams:
    """Carbon trading parameters for MESS optimization."""
    base_carbon_price: float = 50.0  # 基础碳价 (元/吨)
    price_growth_rate: float = 0.1  # 价格增长系数
    quota_per_interval: float = 10.0  # 碳交易量区间长度 (吨)
    max_carbon_price: float = 200.0  # 最高碳价 (元/吨)
    carbon_quota: float = 10.0  # 碳排放权配额 (吨/年)


@dataclass
class BatteryDegradationParams:
    """Battery degradation parameters for MESS optimization."""
    initial_capacity: float  # 初始容量 (kWh)
    sei_alpha: float = 0.5  # 固体电解质界面膜系数
    sei_beta: float = 0.1  # 固体电解质界面膜系数
    capacity_decay_rate: float = 0.02  # 每年容量衰减率
    cycle_life: int = 3000  # 循环寿命
    max_depth_of_discharge: float = 0.8  # 最大放电深度


@dataclass
class MESSOptimizationConfig(OptimizationConfig):
    """Configuration for MESS optimization problems."""
    optimization_type: OptimizationType = OptimizationType.MULTI_OBJECTIVE
    solver: SolverType = SolverType.CUSTOM
    mess_optimization_type: MESSOptimizationType = MESSOptimizationType.COMBINED
    algorithm_type: MESSAlgorithmType = MESSAlgorithmType.MAPPO
    time_horizon: int = 24
    time_step: float = 0.25  # 15分钟
    num_agents: int = 5
    
    # Spatial parameters
    max_speed: float = 60.0  # km/h
    transport_cost: float = 1.0  # 元/km
    
    # Carbon trading parameters
    carbon_trading_params: CarbonTradingParams = field(default_factory=CarbonTradingParams)
    
    # Battery degradation parameters
    battery_degradation_params: Optional[BatteryDegradationParams] = None
    
    # Reward function weights
    weight_profit: float = 1.0
    weight_carbon: float = 0.5
    weight_degradation: float = 0.3
    weight_transport: float = 0.2
    
    # Algorithm parameters
    learning_rate: float = 3e-4
    gamma: float = 0.99  # 折扣因子
    tau: float = 0.005  # 目标网络更新率
    batch_size: int = 256
    buffer_size: int = 100000
    hidden_dim: int = 256
    num_epochs: int = 10000
    target_update_interval: int = 100
    
    # Additional parameters
    initial_soc: float = 0.5
    min_soc: float = 0.2
    max_soc: float = 0.8
    max_charge_power: float = 100.0  # kW
    max_discharge_power: float = 100.0  # kW
    
    # Carbon-aware parameters
    carbon_price_levels: List[float] = field(default_factory=lambda: [50, 70, 90, 110, 130])
    carbon_emission_factors: Dict[str, float] = field(default_factory=dict)


class MESSState:
    """State representation for MESS agents."""
    
    def __init__(self, 
                 current_location: str,
                 time: float,
                 soc: float,
                 target_location_lmp: float,
                 target_location_carbon: float,
                 remaining_distance: float = 0.0):
        self.current_location = current_location
        self.time = time
        self.soc = soc
        self.target_location_lmp = target_location_lmp
        self.target_location_carbon = target_location_carbon
        self.remaining_distance = remaining_distance
    
    def to_array(self) -> np.ndarray:
        """Convert state to numpy array for RL algorithms."""
        # Convert location to one-hot encoding if needed
        # For simplicity, we'll use dummy values for location
        return np.array([
            self.time,
            self.soc,
            self.target_location_lmp,
            self.target_location_carbon,
            self.remaining_distance
        ])
    
    def __repr__(self) -> str:
        return (f"MESSState(location={self.current_location}, time={self.time:.2f}, "
                f"soc={self.soc:.2f}, lmp={self.target_location_lmp:.2f}, "
                f"carbon={self.target_location_carbon:.2f})")


class MESSAction:
    """Action representation for MESS agents."""
    
    def __init__(self, 
                 next_location: Optional[str] = None,
                 charge_discharge_power: float = 0.0):
        self.next_location = next_location
        self.charge_discharge_power = charge_discharge_power
    
    def to_array(self) -> np.ndarray:
        """Convert action to numpy array for RL algorithms."""
        # For discrete location actions, convert to one-hot encoding
        # For continuous power actions, use normalized value
        return np.array([self.charge_discharge_power])
    
    def __repr__(self) -> str:
        return (f"MESSAction(next_location={self.next_location}, "
                f"power={self.charge_discharge_power:.2f})")


class MESSReward:
    """Reward calculation for MESS optimization."""
    
    def __init__(self, config: MESSOptimizationConfig):
        self.config = config
    
    def calculate_reward(self, 
                       state: MESSState,
                       action: MESSAction,
                       next_state: MESSState,
                       profit: float,
                       carbon_emissions: float,
                       battery_degradation: float,
                       transport_cost: float) -> float:
        """Calculate reward based on state transition and system metrics."""
        
        # Profit reward
        profit_reward = self.config.weight_profit * profit
        
        # Carbon emission penalty
        carbon_penalty = -self.config.weight_carbon * carbon_emissions * self.config.carbon_trading_params.base_carbon_price
        
        # Battery degradation penalty
        degradation_penalty = -self.config.weight_degradation * battery_degradation
        
        # Transport cost penalty
        transport_penalty = -self.config.weight_transport * transport_cost
        
        # SOC maintenance reward (encourage staying within optimal SOC range)
        soc_reward = 0.0
        if self.config.min_soc <= next_state.soc <= self.config.max_soc:
            soc_reward = 1.0
        else:
            soc_reward = -1.0
        
        # Total reward
        total_reward = (profit_reward + carbon_penalty + 
                      degradation_penalty + transport_penalty + soc_reward)
        
        return total_reward


class MobileStorageOptimizer(Optimizer):
    """Optimizer for Mobile Energy Storage Systems (MESS)."""
    
    def __init__(self, config: MESSOptimizationConfig):
        """Initialize MESS optimizer."""
        super().__init__(config)
        self.config = config
        self.reward_calculator = MESSReward(config)
        self.history = {
            'states': [],
            'actions': [],
            'rewards': [],
            'profits': [],
            'carbon_emissions': [],
            'battery_degradation': [],
            'transport_costs': []
        }
        
        # Initialize algorithm-specific components
        self.algorithm = self._create_algorithm()
    
    def _create_algorithm(self) -> Any:
        """Create algorithm instance based on configuration."""
        # For now, return a dummy algorithm instance
        # In real implementation, this would initialize the actual RL algorithm
        return {
            'type': self.config.algorithm_type,
            'config': self.config
        }
    
    def add_variable(self, name: str, **kwargs) -> Any:
        """Add an optimization variable."""
        # MESS optimization uses RL states/actions instead of traditional variables
        pass
    
    def add_constraint(self, name: str, expression: Callable, **kwargs) -> Any:
        """Add an optimization constraint."""
        # Constraints are handled within the RL algorithm and environment
        pass
    
    def set_objective(self, objective: Callable) -> None:
        """Set the objective function."""
        # Objective is handled through reward function
        pass
    
    def solve(self) -> Dict[str, Any]:
        """Solve the MESS optimization problem."""
        print(f"Solving MESS optimization problem with {self.config.algorithm_type}")
        print(f"Number of agents: {self.config.num_agents}")
        print(f"Time horizon: {self.config.time_horizon} hours")
        print(f"Time step: {self.config.time_step} hours")
        
        # Simulate optimization process
        # In real implementation, this would run the actual RL algorithm
        results = {
            'status': 'solved',
            'algorithm': self.config.algorithm_type.value,
            'num_agents': self.config.num_agents,
            'time_horizon': self.config.time_horizon,
            'time_step': self.config.time_step,
            'total_profit': 10000.0,
            'total_carbon_emissions': 5.2,
            'total_battery_degradation': 0.01,
            'total_transport_cost': 200.0,
            'optimal_schedule': self._generate_dummy_schedule()
        }
        
        return results
    
    def _generate_dummy_schedule(self) -> List[Dict[str, Any]]:
        """Generate a dummy optimal schedule for demonstration."""
        schedule = []
        num_locations = 10
        
        for t in range(int(self.config.time_horizon / self.config.time_step)):
            time = t * self.config.time_step
            for agent_id in range(self.config.num_agents):
                schedule.append({
                    'time': time,
                    'agent_id': agent_id,
                    'current_location': f'location_{agent_id % num_locations}',
                    'next_location': f'location_{(agent_id + 1) % num_locations}',
                    'charge_discharge_power': np.random.uniform(-50, 50),
                    'soc': np.random.uniform(0.2, 0.8),
                    'profit': np.random.uniform(10, 100),
                    'carbon_emissions': np.random.uniform(0, 0.1),
                    'battery_degradation': np.random.uniform(0, 0.001),
                    'transport_cost': np.random.uniform(0, 10)
                })
        
        return schedule
    
    def validate_problem(self) -> Tuple[bool, List[str]]:
        """Validate the optimization problem setup."""
        errors = []
        
        if self.config.num_agents <= 0:
            errors.append("Number of agents must be positive")
        
        if self.config.time_horizon <= 0:
            errors.append("Time horizon must be positive")
        
        if self.config.time_step <= 0:
            errors.append("Time step must be positive")
        
        if self.config.time_step > self.config.time_horizon:
            errors.append("Time step cannot be larger than time horizon")
        
        if self.config.battery_degradation_params is None:
            errors.append("Battery degradation parameters are required")
        
        return len(errors) == 0, errors
    
    def calculate_profit(self, 
                       location: str,
                       time: float,
                       charge_discharge_power: float,
                       lmp: float,
                       carbon_price: float,
                       carbon_emissions: float,
                       battery_degradation: float,
                       transport_cost: float) -> float:
        """Calculate profit for a given action."""
        
        # Charging: positive power, cost
        # Discharging: negative power, revenue
        if charge_discharge_power > 0:  # Charging
            electricity_cost = charge_discharge_power * lmp * self.config.time_step
            carbon_cost = carbon_emissions * carbon_price
            total_cost = electricity_cost + carbon_cost + transport_cost + battery_degradation
            profit = -total_cost
        else:  # Discharging
            electricity_revenue = abs(charge_discharge_power) * lmp * self.config.time_step
            profit = electricity_revenue - transport_cost - battery_degradation
        
        return profit
    
    def calculate_carbon_emissions(self, 
                                 charge_discharge_power: float,
                                 location_carbon_intensity: float) -> float:
        """Calculate carbon emissions for a given action."""
        if charge_discharge_power > 0:  # Charging
            emissions = charge_discharge_power * location_carbon_intensity * self.config.time_step / 1000  # 转换为吨
        else:  # Discharging
            emissions = 0.0
        
        return emissions
    
    def calculate_battery_degradation(self, 
                                    soc: float,
                                    charge_discharge_power: float,
                                    temperature: float = 25.0) -> float:
        """Calculate battery degradation using semi-empirical model."""
        if self.config.battery_degradation_params is None:
            return 0.0
        
        params = self.config.battery_degradation_params
        
        # Calculate depth of discharge (DOD)
        dod = abs(charge_discharge_power * self.config.time_step) / params.initial_capacity
        dod = min(dod, 1.0)
        
        # Calculate combined stress factor
        # Simplified model: function of temperature, DOD, and SOC
        stress_factor = (temperature - 25) * 0.001 + dod * 0.1 + (soc - 0.5)**2 * 0.5
        
        # Calculate capacity loss
        # Semi-empirical degradation model
        if params.capacity_decay_rate == 0:
            capacity_loss = 0.0
        else:
            capacity_loss = params.initial_capacity * (1 - params.sei_alpha * np.exp(-params.sei_beta * stress_factor) - 
                                                    (1 - params.sei_alpha) * np.exp(-stress_factor))
        
        # Calculate degradation cost (using initial investment cost as reference)
        # Assuming 1500元/kW investment cost
        investment_cost_per_kwh = 1500.0
        degradation_cost = capacity_loss * investment_cost_per_kwh
        
        return degradation_cost
    
    def calculate_transport_cost(self, 
                               distance: float,
                               speed: float = 60.0) -> float:
        """Calculate transport cost for moving between locations."""
        return distance * self.config.transport_cost
    
    def get_lmp_at_location(self, location: str, time: float) -> float:
        """Get locational marginal price at a specific location and time."""
        # In real implementation, this would use actual market data
        # For now, return a dummy value based on time of day
        if 7 <= time <= 9 or 17 <= time <= 19:  # 高峰期
            return 1.2 + np.random.uniform(-0.1, 0.1)
        elif 0 <= time <= 5:  # 深夜
            return 0.6 + np.random.uniform(-0.05, 0.05)
        else:  # 平峰期
            return 0.9 + np.random.uniform(-0.08, 0.08)
    
    def get_carbon_intensity_at_location(self, location: str, time: float) -> float:
        """Get carbon intensity at a specific location and time."""
        # In real implementation, this would use actual grid carbon intensity data
        # For now, return a dummy value
        return 0.5 + np.random.uniform(-0.1, 0.1)
    
    def get_distance_between_locations(self, location1: str, location2: str) -> float:
        """Get distance between two locations."""
        # In real implementation, this would use actual geographic data
        # For now, return a dummy value
        return np.random.uniform(5, 50)
    
    def reset(self) -> None:
        """Reset optimizer state."""
        self.history = {
            'states': [],
            'actions': [],
            'rewards': [],
            'profits': [],
            'carbon_emissions': [],
            'battery_degradation': [],
            'transport_costs': []
        }
    
    def save_model(self, file_path: str) -> bool:
        """Save trained model to file."""
        # In real implementation, this would save the actual RL model
        print(f"Saving model to {file_path}")
        return True
    
    def load_model(self, file_path: str) -> bool:
        """Load trained model from file."""
        # In real implementation, this would load the actual RL model
        print(f"Loading model from {file_path}")
        return True
    
    def get_evaluation_metrics(self) -> Dict[str, Any]:
        """Get evaluation metrics for the optimizer."""
        metrics = {
            'algorithm': self.config.algorithm_type.value,
            'num_agents': self.config.num_agents,
            'time_horizon': self.config.time_horizon,
            'time_step': self.config.time_step,
            'learning_rate': self.config.learning_rate,
            'gamma': self.config.gamma,
            'tau': self.config.tau,
            'batch_size': self.config.batch_size,
            'buffer_size': self.config.buffer_size,
            'hidden_dim': self.config.hidden_dim
        }
        
        return metrics


class MESSOptimizationFactory:
    """Factory for creating MESS optimization components."""
    
    @staticmethod
    def create_mess_optimization_config(**kwargs) -> MESSOptimizationConfig:
        """Create MESS optimization configuration."""
        return MESSOptimizationConfig(
            name=kwargs.get('name', 'mess_optimization'),
            optimization_type=kwargs.get('optimization_type', OptimizationType.MULTI_OBJECTIVE),
            solver=kwargs.get('solver', SolverType.CUSTOM),
            mess_optimization_type=kwargs.get('mess_optimization_type', MESSOptimizationType.COMBINED),
            algorithm_type=kwargs.get('algorithm_type', MESSAlgorithmType.MAPPO),
            time_horizon=kwargs.get('time_horizon', 24),
            time_step=kwargs.get('time_step', 0.25),
            num_agents=kwargs.get('num_agents', 5),
            max_speed=kwargs.get('max_speed', 60.0),
            transport_cost=kwargs.get('transport_cost', 1.0),
            carbon_trading_params=kwargs.get('carbon_trading_params', CarbonTradingParams()),
            battery_degradation_params=kwargs.get('battery_degradation_params'),
            weight_profit=kwargs.get('weight_profit', 1.0),
            weight_carbon=kwargs.get('weight_carbon', 0.5),
            weight_degradation=kwargs.get('weight_degradation', 0.3),
            weight_transport=kwargs.get('weight_transport', 0.2),
            learning_rate=kwargs.get('learning_rate', 3e-4),
            gamma=kwargs.get('gamma', 0.99),
            tau=kwargs.get('tau', 0.005),
            batch_size=kwargs.get('batch_size', 256),
            buffer_size=kwargs.get('buffer_size', 100000),
            hidden_dim=kwargs.get('hidden_dim', 256),
            num_epochs=kwargs.get('num_epochs', 10000),
            target_update_interval=kwargs.get('target_update_interval', 100),
            initial_soc=kwargs.get('initial_soc', 0.5),
            min_soc=kwargs.get('min_soc', 0.2),
            max_soc=kwargs.get('max_soc', 0.8),
            max_charge_power=kwargs.get('max_charge_power', 100.0),
            max_discharge_power=kwargs.get('max_discharge_power', 100.0),
            carbon_price_levels=kwargs.get('carbon_price_levels', [50, 70, 90, 110, 130]),
            carbon_emission_factors=kwargs.get('carbon_emission_factors', {})
        )
    
    @staticmethod
    def create_mess_optimizer(config: MESSOptimizationConfig) -> MobileStorageOptimizer:
        """Create MESS optimizer."""
        return MobileStorageOptimizer(config)
    
    @staticmethod
    def create_carbon_trading_params(**kwargs) -> CarbonTradingParams:
        """Create carbon trading parameters."""
        return CarbonTradingParams(
            base_carbon_price=kwargs.get('base_carbon_price', 50.0),
            price_growth_rate=kwargs.get('price_growth_rate', 0.1),
            quota_per_interval=kwargs.get('quota_per_interval', 10.0),
            max_carbon_price=kwargs.get('max_carbon_price', 200.0),
            carbon_quota=kwargs.get('carbon_quota', 10.0)
        )
    
    @staticmethod
    def create_battery_degradation_params(**kwargs) -> BatteryDegradationParams:
        """Create battery degradation parameters."""
        return BatteryDegradationParams(
            initial_capacity=kwargs.get('initial_capacity', 100.0),
            sei_alpha=kwargs.get('sei_alpha', 0.5),
            sei_beta=kwargs.get('sei_beta', 0.1),
            capacity_decay_rate=kwargs.get('capacity_decay_rate', 0.02),
            cycle_life=kwargs.get('cycle_life', 3000),
            max_depth_of_discharge=kwargs.get('max_depth_of_discharge', 0.8)
        )


# Utility functions

def calculate_carbon_trading_cost(carbon_emissions: float, 
                                 carbon_quota: float, 
                                 carbon_price: float, 
                                 price_growth_rate: float = 0.1, 
                                 quota_per_interval: float = 10.0) -> float:
    """Calculate carbon trading cost based on emissions and quota."""
    if carbon_emissions <= carbon_quota:
        return 0.0
    
    excess_emissions = carbon_emissions - carbon_quota
    
    # Calculate cost with tiered pricing
    num_intervals = int(np.ceil(excess_emissions / quota_per_interval))
    total_cost = 0.0
    remaining_emissions = excess_emissions
    
    for i in range(num_intervals):
        interval_emissions = min(remaining_emissions, quota_per_interval)
        interval_price = carbon_price * (1 + price_growth_rate) ** i
        total_cost += interval_emissions * interval_price
        remaining_emissions -= interval_emissions
    
    return total_cost

def calculate_battery_lifetime_loss(depth_of_discharge: float, 
                                   cycle_life: int = 3000) -> float:
    """Calculate battery lifetime loss based on depth of discharge."""
    # Simplified model: deeper discharges cause more degradation
    if depth_of_discharge == 0:
        return 0.0
    
    # Assume linear relationship between DOD and cycle life
    # Actual relationship is more complex, but this is a simplification
    effective_cycles = cycle_life * (1 - depth_of_discharge * 0.5)
    lifetime_loss = 1.0 / effective_cycles
    
    return lifetime_loss

def calculate_transport_time(distance: float, speed: float = 60.0) -> float:
    """Calculate transport time between locations."""
    return distance / speed

def create_mess_scenario(time_horizon: int = 24, 
                         time_step: float = 0.25, 
                         num_locations: int = 10, 
                         num_agents: int = 5) -> Dict[str, Any]:
    """Create a MESS optimization scenario."""
    # Generate dummy LMP and carbon intensity data
    time_points = np.arange(0, time_horizon, time_step)
    num_time_points = len(time_points)
    
    lmp_data = {}
    carbon_intensity_data = {}
    
    for location in [f'location_{i}' for i in range(num_locations)]:
        # Generate LMP profile with daily variation
        base_lmp = 0.9
        morning_peak = np.where((time_points >= 7) & (time_points <= 9), 1.2, 0)
        evening_peak = np.where((time_points >= 17) & (time_points <= 19), 1.1, 0)
        night_valley = np.where((time_points >= 0) & (time_points <= 5), 0.6, 0)
        
        lmp = base_lmp + morning_peak + evening_peak + night_valley
        lmp += np.random.normal(0, 0.05, num_time_points)  # Add noise
        lmp = np.maximum(lmp, 0.5)  # Ensure positive LMP
        
        lmp_data[location] = lmp
        
        # Generate carbon intensity profile (more stable than LMP)
        base_carbon = 0.5
        carbon_intensity = base_carbon + np.random.normal(0, 0.05, num_time_points)
        carbon_intensity = np.maximum(carbon_intensity, 0.2)  # Ensure positive intensity
        carbon_intensity_data[location] = carbon_intensity
    
    # Generate distance matrix between locations
    distance_matrix = np.random.uniform(5, 50, (num_locations, num_locations))
    np.fill_diagonal(distance_matrix, 0)  # Distance to self is 0
    
    # Make matrix symmetric
    distance_matrix = (distance_matrix + distance_matrix.T) / 2
    
    scenario = {
        'time_horizon': time_horizon,
        'time_step': time_step,
        'num_locations': num_locations,
        'num_agents': num_agents,
        'time_points': time_points.tolist(),
        'lmp_data': lmp_data,
        'carbon_intensity_data': carbon_intensity_data,
        'distance_matrix': distance_matrix.tolist(),
        'locations': [f'location_{i}' for i in range(num_locations)]
    }
    
    return scenario


# Example usage
if __name__ == "__main__":
    # Create MESS optimization configuration
    config = MESSOptimizationFactory.create_mess_optimization_config(
        name="mobile_storage_optimization",
        num_agents=5,
        time_horizon=24,
        time_step=0.25,
        algorithm_type=MESSAlgorithmType.MAPPO,
        mess_optimization_type=MESSOptimizationType.COMBINED
    )
    
    # Create MESS optimizer
    optimizer = MESSOptimizationFactory.create_mess_optimizer(config)
    
    # Solve optimization problem
    results = optimizer.solve()
    
    # Print results
    print(f"Optimization status: {results['status']}")
    print(f"Total profit: {results['total_profit']} 元")
    print(f"Total carbon emissions: {results['total_carbon_emissions']} 吨")
    print(f"Total battery degradation: {results['total_battery_degradation']}")
    print(f"Total transport cost: {results['total_transport_cost']} 元")
    print(f"Generated schedule with {len(results['optimal_schedule'])} entries")
