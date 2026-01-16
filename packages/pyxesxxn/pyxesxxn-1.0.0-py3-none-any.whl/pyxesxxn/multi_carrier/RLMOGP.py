import numpy as np
import random
import math
from collections import deque
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Tuple, Set
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical, Normal
import torch.multiprocessing as mp
from torch.utils.data import Dataset, DataLoader
import threading
import time

# -------------------------- 多目标优化核心函数 --------------------------
def dominates(solution1: Dict, solution2: Dict, objectives: List[str]) -> bool:
    """判断solution1是否支配solution2
    
    Args:
        solution1: 第一个解
        solution2: 第二个解
        objectives: 目标函数列表，每个目标的格式为(name, is_minimize)
            例如：[("energy_cost", True), ("carbon_emission", True), ("reliability", False)]
    
    Returns:
        True if solution1 dominates solution2, False otherwise
    """
    better_in_any = False
    for obj_name, is_minimize in objectives:
        val1 = solution1[obj_name]
        val2 = solution2[obj_name]
        
        if is_minimize:
            if val1 > val2:
                return False
            if val1 < val2:
                better_in_any = True
        else:
            if val1 < val2:
                return False
            if val1 > val2:
                better_in_any = True
    
    return better_in_any

def update_pareto_front(solutions: List[Dict], objectives: List[str]) -> List[Dict]:
    """更新Pareto前沿
    
    Args:
        solutions: 待评估的解列表
        objectives: 目标函数列表
    
    Returns:
        更新后的Pareto前沿解列表
    """
    pareto_front = []
    
    for solution in solutions:
        dominated = False
        to_remove = []
        
        for i, front_solution in enumerate(pareto_front):
            if dominates(front_solution, solution, objectives):
                dominated = True
                break
            if dominates(solution, front_solution, objectives):
                to_remove.append(i)
        
        if not dominated:
            # 移除被当前解支配的前沿解
            for i in sorted(to_remove, reverse=True):
                pareto_front.pop(i)
            # 添加当前解到前沿
            pareto_front.append(solution)
    
    return pareto_front

def calculate_crowding_distance(solutions: List[Dict], objectives: List[str]) -> List[Dict]:
    """计算解的拥挤距离
    
    Args:
        solutions: 解列表
        objectives: 目标函数列表
    
    Returns:
        添加了crowding_distance字段的解列表
    """
    if len(solutions) <= 2:
        for solution in solutions:
            solution["crowding_distance"] = float('inf')
        return solutions
    
    # 初始化拥挤距离为0
    for solution in solutions:
        solution["crowding_distance"] = 0.0
    
    # 对每个目标维度计算拥挤距离
    for obj_name, is_minimize in objectives:
        # 按目标值排序
        sorted_solutions = sorted(solutions, key=lambda x: x[obj_name], reverse=not is_minimize)
        
        # 边界解设置为无穷大
        sorted_solutions[0]["crowding_distance"] = float('inf')
        sorted_solutions[-1]["crowding_distance"] = float('inf')
        
        # 计算目标值范围
        obj_range = sorted_solutions[-1][obj_name] - sorted_solutions[0][obj_name]
        if obj_range == 0:
            continue
        
        # 计算中间解的拥挤距离
        for i in range(1, len(sorted_solutions) - 1):
            sorted_solutions[i]["crowding_distance"] += (
                sorted_solutions[i+1][obj_name] - sorted_solutions[i-1][obj_name]
            ) / obj_range
    
    return solutions

def select_nondominated_solutions(solutions: List[Dict], objectives: List[str], n: int) -> List[Dict]:
    """选择非支配解
    
    Args:
        solutions: 解列表
        objectives: 目标函数列表
        n: 要选择的解数量
    
    Returns:
        选择的非支配解列表
    """
    if len(solutions) <= n:
        return solutions
    
    # 计算拥挤距离
    solutions_with_cd = calculate_crowding_distance(solutions, objectives)
    
    # 按拥挤距离排序（从大到小）
    solutions_with_cd.sort(key=lambda x: x["crowding_distance"], reverse=True)
    
    return solutions_with_cd[:n]


# -------------------------- GRPO核心算法组件 --------------------------
class GRPOPolicyNetwork(nn.Module):
    """GRPO策略网络：基于PyTorch的神经网络实现"""
    
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 128):
        super(GRPOPolicyNetwork, self).__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # 策略网络
        self.policy_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
        
        # 价值网络（用于基线估计）
        self.value_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        
        # 优化器
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        
    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """前向传播"""
        logits = self.policy_net(state)
        value = self.value_net(state)
        return logits, value
    
    def get_action(self, state: torch.Tensor) -> Tuple[int, torch.Tensor, torch.Tensor]:
        """根据状态选择动作"""
        logits, value = self.forward(state)
        probs = F.softmax(logits, dim=-1)
        dist = Categorical(probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action.item(), log_prob, value


class GRPOExperienceReplay:
    """GRPO经验回放缓冲区"""
    
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.lock = threading.Lock()
        
    def push(self, state: np.ndarray, action: int, reward: float, 
             next_state: np.ndarray, done: bool, log_prob: float, value: float):
        """存储经验"""
        with self.lock:
            self.buffer.append({
                'state': state,
                'action': action,
                'reward': reward,
                'next_state': next_state,
                'done': done,
                'log_prob': log_prob,
                'value': value
            })
            
    def sample(self, batch_size: int) -> List[Dict]:
        """采样批次经验"""
        with self.lock:
            if len(self.buffer) < batch_size:
                return []
            return random.sample(self.buffer, batch_size)
        
    def __len__(self) -> int:
        """返回缓冲区大小"""
        return len(self.buffer)


class GRPOAgent:
    """分布式多智能体GRPO智能体"""
    
    def __init__(self, agent_id: int, state_dim: int, action_dim: int, 
                 gamma: float = 0.99, gae_lambda: float = 0.95, 
                 clip_epsilon: float = 0.2, entropy_coef: float = 0.01):
        self.agent_id = agent_id
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_epsilon = clip_epsilon
        self.entropy_coef = entropy_coef
        
        # 策略网络
        self.policy_net = GRPOPolicyNetwork(state_dim, action_dim)
        
        # 经验回放
        self.memory = GRPOExperienceReplay()
        
        # 训练参数
        self.learning_rate = 0.001
        self.batch_size = 32
        self.epochs = 4
        
        # 多目标奖励权重
        self.reward_weights = {
            "energy_cost": 0.4,
            "carbon_emission": 0.3,
            "reliability": 0.2,
            "priority": 0.1
        }
        
        # 分布式训练参数
        self.global_step = 0
        self.update_frequency = 100
        
    def select_action(self, state: np.ndarray) -> int:
        """选择动作"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        action, log_prob, value = self.policy_net.get_action(state_tensor)
        
        # 存储经验用于训练
        self.memory.push(state, action, 0.0, state, False, 
                        log_prob.item(), value.item())
        
        return action
    
    def store_experience(self, state: np.ndarray, action: int, reward: Dict[str, float], 
                         next_state: np.ndarray, done: bool, log_prob: float, value: float):
        """存储完整经验"""
        # 多目标奖励加权
        if isinstance(reward, dict):
            weighted_reward = sum(self.reward_weights.get(key, 0) * val for key, val in reward.items())
        else:
            weighted_reward = reward
            
        self.memory.push(state, action, weighted_reward, next_state, done, log_prob, value)
        
    def compute_advantages(self, rewards: List[float], values: List[float], 
                          dones: List[bool]) -> List[float]:
        """计算GAE优势函数"""
        advantages = []
        last_advantage = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0.0  # 终止状态
            else:
                next_value = values[t + 1] * (1 - dones[t])
                
            delta = rewards[t] + self.gamma * next_value - values[t]
            advantage = delta + self.gamma * self.gae_lambda * last_advantage * (1 - dones[t])
            advantages.insert(0, advantage)
            last_advantage = advantage
            
        return advantages
    
    def train_step(self, batch: List[Dict]) -> Dict[str, float]:
        """单步训练"""
        if not batch:
            return {}
            
        # 提取批次数据
        states = torch.FloatTensor([exp['state'] for exp in batch])
        actions = torch.LongTensor([exp['action'] for exp in batch])
        rewards = torch.FloatTensor([exp['reward'] for exp in batch])
        next_states = torch.FloatTensor([exp['next_state'] for exp in batch])
        dones = torch.BoolTensor([exp['done'] for exp in batch])
        old_log_probs = torch.FloatTensor([exp['log_prob'] for exp in batch])
        old_values = torch.FloatTensor([exp['value'] for exp in batch])
        
        # 计算优势函数
        advantages = self.compute_advantages(rewards.tolist(), old_values.tolist(), dones.tolist())
        advantages = torch.FloatTensor(advantages)
        
        # 归一化优势
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # 多轮训练
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_entropy = 0.0
        
        for _ in range(self.epochs):
            # 计算新策略的概率
            logits, values = self.policy_net(states)
            probs = F.softmax(logits, dim=-1)
            dist = Categorical(probs)
            new_log_probs = dist.log_prob(actions)
            entropy = dist.entropy().mean()
            
            # 策略损失（PPO裁剪目标）
            ratio = torch.exp(new_log_probs - old_log_probs)
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
            policy_loss = -torch.min(surr1, surr2).mean()
            
            # 价值损失
            value_loss = F.mse_loss(values.squeeze(), rewards)
            
            # 总损失
            loss = policy_loss + 0.5 * value_loss - self.entropy_coef * entropy
            
            # 反向传播
            self.policy_net.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 0.5)
            self.policy_net.optimizer.step()
            
            total_policy_loss += policy_loss.item()
            total_value_loss += value_loss.item()
            total_entropy += entropy.item()
            
        return {
            'policy_loss': total_policy_loss / self.epochs,
            'value_loss': total_value_loss / self.epochs,
            'entropy': total_entropy / self.epochs
        }
    
    def train(self) -> Dict[str, float]:
        """训练智能体"""
        batch = self.memory.sample(self.batch_size)
        if not batch:
            return {}
            
        metrics = self.train_step(batch)
        self.global_step += 1
        
        return metrics
    
    def sync_parameters(self, global_agent: 'GRPOAgent') -> None:
        """同步全局参数（分布式训练）"""
        self.policy_net.load_state_dict(global_agent.policy_net.state_dict())
    
    def get_parameters(self) -> Dict[str, torch.Tensor]:
        """获取智能体参数"""
        return self.policy_net.state_dict()
    
    def set_parameters(self, parameters: Dict[str, torch.Tensor]) -> None:
        """设置智能体参数"""
        self.policy_net.load_state_dict(parameters)
        
    def save_checkpoint(self, filepath: str) -> None:
        """保存检查点"""
        torch.save({
            'policy_state_dict': self.policy_net.state_dict(),
            'optimizer_state_dict': self.policy_net.optimizer.state_dict(),
            'global_step': self.global_step
        }, filepath)
        
    def load_checkpoint(self, filepath: str) -> None:
        """加载检查点"""
        checkpoint = torch.load(filepath)
        self.policy_net.load_state_dict(checkpoint['policy_state_dict'])
        self.policy_net.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.global_step = checkpoint['global_step']


class DistributedGRPOCoordinator:
    """分布式GRPO协调器"""
    
    def __init__(self, num_agents: int, state_dim: int, action_dim: int):
        self.num_agents = num_agents
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # 全局智能体
        self.global_agent = GRPOAgent(0, state_dim, action_dim)
        
        # 本地智能体
        self.local_agents = [GRPOAgent(i, state_dim, action_dim) for i in range(num_agents)]
        
        # 同步参数
        self.sync_interval = 100
        self.global_step = 0
        
        # 训练线程
        self.training_threads = []
        self.stop_training = False
        
    def start_training(self) -> None:
        """启动分布式训练"""
        self.stop_training = False
        
        for agent_id, agent in enumerate(self.local_agents):
            thread = threading.Thread(target=self._training_worker, args=(agent_id,))
            thread.daemon = True
            thread.start()
            self.training_threads.append(thread)
            
    def stop_training(self) -> None:
        """停止训练"""
        self.stop_training = True
        for thread in self.training_threads:
            thread.join()
            
    def _training_worker(self, agent_id: int) -> None:
        """训练工作线程"""
        agent = self.local_agents[agent_id]
        
        while not self.stop_training:
            # 同步全局参数
            if agent.global_step % self.sync_interval == 0:
                agent.sync_parameters(self.global_agent)
                
            # 训练本地智能体
            metrics = agent.train()
            
            # 定期更新全局参数
            if agent.global_step % self.sync_interval == 0 and metrics:
                self._update_global_agent(agent)
                
            time.sleep(0.01)  # 避免过度占用CPU
            
    def _update_global_agent(self, local_agent: GRPOAgent) -> None:
        """更新全局智能体参数"""
        # 简单的参数平均（可替换为更复杂的聚合策略）
        global_state_dict = self.global_agent.policy_net.state_dict()
        local_state_dict = local_agent.policy_net.state_dict()
        
        for key in global_state_dict:
            global_state_dict[key] = 0.9 * global_state_dict[key] + 0.1 * local_state_dict[key]
            
        self.global_agent.policy_net.load_state_dict(global_state_dict)
        self.global_step += 1
    
    def synchronize_parameters(self, agent_parameters: List[Dict[str, torch.Tensor]]) -> List[Dict[str, torch.Tensor]]:
        """同步所有智能体参数（分布式训练）"""
        if not agent_parameters:
            return []
        
        # 使用简单的参数平均策略
        synchronized_params = []
        
        # 对每个参数键进行平均
        for i in range(len(agent_parameters)):
            avg_params = {}
            for key in agent_parameters[0].keys():
                # 收集所有智能体的该参数
                param_list = [params[key] for params in agent_parameters]
                # 计算平均值
                avg_param = torch.stack(param_list).mean(dim=0)
                avg_params[key] = avg_param
            
            synchronized_params.append(avg_params)
        
        return synchronized_params


# -------------------------- 1. 能源系统环境模型 --------------------------
class EnergySystemEnvironment:
    """能源系统环境模型：模拟发电机组、储能设备、负荷等能源系统组件"""

    def __init__(self, generator_num: int = 3, storage_num: int = 2, load_num: int = 5):
        """初始化能源系统环境
        
        Args:
            generator_num: 发电机组数量
            storage_num: 储能设备数量  
            load_num: 负荷节点数量
        """
        # 能源系统组件类型定义：0-发电机，1-储能设备，2-负荷
        self.component_types = {0: "发电机", 1: "储能设备", 2: "负荷"}
        
        # 能源价格（元/kWh）
        self.energy_prices = {
            0: 0.3,  # 发电机
            1: 0.2,  # 储能设备（放电）
            2: 0.5   # 负荷（购电价格）
        }
        
        # 碳排放系数（kgCO2/kWh）
        self.carbon_factors = {
            0: 0.8,  # 火电机组
            1: 0.0,  # 储能设备
            2: 0.0   # 负荷
        }
        
        self.nodes = self._init_energy_nodes(generator_num, storage_num, load_num)
        self.node_count = len(self.nodes)
        self.connection_matrix = self._init_connection_matrix()  # 能源传输网络连接矩阵

    def _init_energy_nodes(self, generator_num: int, storage_num: int, load_num: int) -> List[Dict]:
        """初始化能源系统节点"""
        nodes = []
        node_id = 0

        # 1. 发电机组节点
        for _ in range(generator_num):
            nodes.append({
                "node_id": node_id,
                "type": 0,  # 发电机
                "capacity": random.uniform(100, 500),  # 发电容量 (kW)
                "remaining_capacity": random.uniform(50, 200),  # 剩余发电容量
                "min_output": random.uniform(10, 50),  # 最小出力
                "max_output": random.uniform(100, 300),  # 最大出力
                "ramp_rate": random.uniform(10, 30),  # 爬坡速率 (kW/min)
                "fuel_cost": random.uniform(0.2, 0.5),  # 燃料成本 (元/kWh)
                "efficiency": random.uniform(0.8, 0.95),  # 发电效率
                "carbon_factor": self.carbon_factors[0],  # 碳排放系数
                "position": (random.uniform(0, 100), random.uniform(0, 100)),  # 地理位置
                "status": 1  # 运行状态
            })
            node_id += 1

        # 2. 储能设备节点
        for _ in range(storage_num):
            nodes.append({
                "node_id": node_id,
                "type": 1,  # 储能设备
                "capacity": random.uniform(200, 1000),  # 储能容量 (kWh)
                "remaining_capacity": random.uniform(50, 400),  # 剩余容量
                "charge_rate": random.uniform(50, 200),  # 充电功率 (kW)
                "discharge_rate": random.uniform(50, 200),  # 放电功率 (kW)
                "efficiency": random.uniform(0.85, 0.92),  # 充放电效率
                "soc": random.uniform(0.2, 0.8),  # 当前荷电状态
                "min_soc": 0.1,  # 最小荷电状态
                "max_soc": 0.9,  # 最大荷电状态
                "carbon_factor": self.carbon_factors[1],
                "position": (random.uniform(0, 100), random.uniform(0, 100)),
                "status": 1
            })
            node_id += 1

        # 3. 负荷节点
        for _ in range(load_num):
            nodes.append({
                "node_id": node_id,
                "type": 2,  # 负荷
                "demand": random.uniform(50, 300),  # 负荷需求 (kW)
                "remaining_demand": random.uniform(20, 150),  # 剩余需求
                "priority": random.randint(1, 5),  # 负荷优先级 (1-5)
                "critical": random.choice([True, False]),  # 是否关键负荷
                "voltage_level": random.choice([10, 35, 110]),  # 电压等级 (kV)
                "carbon_factor": self.carbon_factors[2],
                "position": (random.uniform(0, 100), random.uniform(0, 100)),
                "status": 1
            })
            node_id += 1
            
        return nodes

    def _init_connection_matrix(self) -> np.ndarray:
        """初始化能源传输网络连接矩阵"""
        matrix = np.full((self.node_count, self.node_count), float('inf'))
        
        # 对角线设为0（自身连接）
        np.fill_diagonal(matrix, 0)
        
        # 随机生成连接关系（简化网络拓扑）
        for i in range(self.node_count):
            for j in range(i + 1, self.node_count):
                if random.random() < 0.3:  # 30%概率建立连接
                    distance = random.uniform(1, 50)  # 距离 (km)
                    capacity = random.uniform(100, 500)  # 传输容量 (kW)
                    loss_rate = random.uniform(0.01, 0.05)  # 传输损耗率
                    
                    matrix[i][j] = distance
                    matrix[j][i] = distance
        
        return matrix

    def update_resource_usage(self, node_id: int, power_consumption: float) -> None:
        """更新能源系统资源使用情况
        
        Args:
            node_id: 节点ID
            power_consumption: 功率消耗 (kW)
        """
        node = self.nodes[node_id]
        
        if node["type"] == 0:  # 发电机
            node["remaining_capacity"] = max(0, node["remaining_capacity"] - power_consumption)
        elif node["type"] == 1:  # 储能设备
            # 如果是放电，减少容量；如果是充电，增加容量
            if power_consumption > 0:  # 放电
                node["remaining_capacity"] = max(0, node["remaining_capacity"] - power_consumption)
                node["soc"] = node["remaining_capacity"] / node["capacity"]
            else:  # 充电
                node["remaining_capacity"] = min(node["capacity"], node["remaining_capacity"] - power_consumption)
                node["soc"] = node["remaining_capacity"] / node["capacity"]
        elif node["type"] == 2:  # 负荷
            node["remaining_demand"] = max(0, node["remaining_demand"] - power_consumption)

    def reset_resources(self) -> None:
        """重置能源系统资源"""
        for node in self.nodes:
            if node["type"] == 0:  # 发电机
                node["remaining_capacity"] = random.uniform(50, 200)
            elif node["type"] == 1:  # 储能设备
                node["remaining_capacity"] = random.uniform(50, 400)
                node["soc"] = node["remaining_capacity"] / node["capacity"]
            elif node["type"] == 2:  # 负荷
                node["remaining_demand"] = random.uniform(20, 150)

    def get_energy_cost(self, node_id: int, power: float) -> float:
        """计算能源成本
        
        Args:
            node_id: 节点ID
            power: 功率 (kW)
            
        Returns:
            float: 能源成本 (元)
        """
        node = self.nodes[node_id]
        price = self.energy_prices[node["type"]]
        return power * price

    def get_carbon_emission(self, node_id: int, power: float) -> float:
        """计算碳排放量
        
        Args:
            node_id: 节点ID
            power: 功率 (kW)
            
        Returns:
            float: 碳排放量 (kgCO2)
        """
        node = self.nodes[node_id]
        factor = self.carbon_factors[node["type"]]
        return power * factor

    def get_transmission_loss(self, from_node: int, to_node: int, power: float) -> float:
        """计算传输损耗
        
        Args:
            from_node: 源节点ID
            to_node: 目标节点ID
            power: 传输功率 (kW)
            
        Returns:
            float: 传输损耗 (kW)
        """
        distance = self.connection_matrix[from_node][to_node]
        if distance == float('inf'):
            return float('inf')
        
        loss_rate = 0.03  # 假设每公里损耗率3%
        return power * loss_rate * distance / 100


class TaskGenerator:
    """能源调度任务生成器"""

    def __init__(self, task_types: List[str] = None):
        self.task_types = task_types if task_types else ["generation_dispatch", "load_balancing", "storage_optimization", "grid_stability"]
        self.task_id_counter = 0

    def generate_task(self) -> Dict:
        """生成能源调度任务实例"""
        task_type = random.choice(self.task_types)
        # 任务属性：功率需求、持续时间、截止时间、优先级、可靠性要求
        if task_type == "generation_dispatch":
            power_demand = random.uniform(50, 200)  # 功率需求 (kW)
            duration = random.uniform(1, 4)  # 持续时间 (小时)
            deadline = random.uniform(2, 6)  # 截止时间 (小时)
            priority = random.randint(1, 3)
            reliability = random.uniform(0.9, 0.99)  # 可靠性要求
        elif task_type == "load_balancing":
            power_demand = random.uniform(20, 100)  # 功率需求 (kW)
            duration = random.uniform(0.5, 2)  # 持续时间 (小时)
            budget = random.uniform(10, 30)  # 预算约束 (元)
            priority = random.randint(2, 4)
            reliability = random.uniform(0.95, 0.99)
        elif task_type == "storage_optimization":
            power_demand = random.uniform(-100, 100)  # 功率需求 (kW，负值为充电)
            duration = random.uniform(0.5, 1.5)  # 持续时间 (小时)
            budget = random.uniform(5, 20)  # 预算约束 (元)
            priority = random.randint(1, 2)
            reliability = random.uniform(0.98, 0.999)
        else:  # grid_stability
            power_demand = random.uniform(10, 50)  # 功率需求 (kW)
            duration = random.uniform(0.1, 0.5)  # 持续时间 (小时)
            budget = random.uniform(2, 10)  # 预算约束 (元)
            priority = random.randint(3, 5)
            reliability = random.uniform(0.99, 0.999)

        task = {
            "task_id": self.task_id_counter,
            "task_type": task_type,
            "power_demand": power_demand,  # 功率需求 (kW)
            "duration": duration,  # 持续时间 (小时)
            "budget": budget,  # 预算约束 (元)
            "priority": priority,  # 1-5级优先级
            "reliability": reliability,  # 可靠性要求 (0-1)
            "release_time": 0.0,
            "completion_time": None,
            "assigned_node": None
        }
        self.task_id_counter += 1
        return task

    def generate_task_batch(self, batch_size: int = 10) -> List[Dict]:
        """生成任务批次"""
        return [self.generate_task() for _ in range(batch_size)]

    def generate_optimization_tasks(self, time_horizon: int = 24, objectives: List[str] = None) -> List[Dict]:
        """生成多目标优化任务
        
        Args:
            time_horizon: 优化时间范围（小时）
            objectives: 优化目标列表
        
        Returns:
            优化任务列表
        """
        if objectives is None:
            objectives = ["成本最小化", "碳排放最小化", "可再生能源利用率最大化", "供电可靠性最大化"]
        
        optimization_tasks = []
        
        # 为每个时间步生成优化任务
        for time_step in range(time_horizon):
            # 生成不同类型的优化任务
            task_types = [
                "发电调度优化", "储能调度优化", "负荷管理优化", 
                "可再生能源优化", "备用调度优化", "多目标权衡优化"
            ]
            
            for task_type in task_types:
                task = {
                    "task_id": self.task_id_counter,
                    "task_type": task_type,
                    "time_step": time_step,
                    "objectives": objectives.copy(),
                    "power_demand": random.uniform(10, 200),  # 功率需求
                    "duration": 1,  # 持续时间（小时）
                    "budget": random.uniform(5, 50),  # 预算约束
                    "priority": random.randint(1, 5),  # 优先级
                    "reliability": random.uniform(0.9, 0.999),  # 可靠性要求
                    "release_time": time_step,
                    "completion_time": None,
                    "assigned_node": None,
                    "optimization_parameters": {
                        "time_horizon": time_horizon,
                        "time_step": time_step,
                        "objectives": objectives,
                        "constraints": ["功率平衡", "设备容量", "运行安全"]
                    }
                }
                self.task_id_counter += 1
                optimization_tasks.append(task)
        
        return optimization_tasks


# -------------------------- 2. 四种并行搜索算子实现 --------------------------
class ParallelHeuristics:
    """并行启发式搜索算子集合：DOA、THRO、CPO、PGA"""

    @staticmethod
    def space_bound(x, lb, ub):
        """边界处理函数"""
        x = np.clip(x, lb, ub)
        return x

    @staticmethod
    def levy(d):
        """Levy飞行函数"""
        b = 1.5
        s = (math.gamma(1 + b) * math.sin(math.pi * b / 2) /
             (math.gamma((1 + b) / 2) * b * 2 ** ((b - 1) / 2))) ** (1 / b)
        u = np.random.normal(0, 1, d) * s
        v = np.random.normal(0, 1, d)
        return u / np.abs(v) ** (1 / b)

    @staticmethod
    def doa_optimize(candidates, max_iter=10, pop_size=10):
        """梦境优化算法(DOA)算子"""
        if not candidates:
            return []

        dim = len(candidates)
        if dim == 0:
            return []
        lb = 0
        ub = dim - 1
        pop = np.random.randint(lb, ub + 1, size=(pop_size, 1))
        pop = np.clip(pop, lb, ub).astype(int)

        best_idx = np.argmin([candidates[i][2]['energy_cost'] for i in range(dim)])
        best_score = candidates[best_idx][2]['energy_cost']

        for _ in range(max_iter):
            # 探索阶段
            for i in range(pop_size):
                if np.random.rand() < 0.9:
                    new_idx = pop[i][0] + int((np.random.rand() * (ub - lb) + lb) *
                                              (np.cos((_ + max_iter / 10) * np.pi / max_iter) + 1) / 2)
                else:
                    new_idx = np.random.randint(lb, ub + 1)

                new_idx = np.clip(new_idx, lb, ub)
                current_score = candidates[pop[i][0]][2]['energy_cost']
                new_score = candidates[new_idx][2]['energy_cost']

                if new_score < current_score:
                    pop[i][0] = new_idx
                    if new_score < best_score:
                        best_score = new_score
                        best_idx = new_idx

        # 利用阶段
        for _ in range(int(max_iter * 0.1)):
            for i in range(pop_size):
                new_idx = best_idx + int((np.random.rand() * (ub - lb) + lb) *
                                         (np.cos((_ + max_iter) * np.pi / max_iter) + 1) / 2)
                new_idx = np.clip(new_idx, lb, ub)
                new_score = candidates[new_idx][2]['energy_cost']

                if new_score < best_score:
                    best_score = new_score
                    best_idx = new_idx

        return [candidates[best_idx]]

    @staticmethod
    def thro_optimize(candidates, max_iter=10, pop_size=10):
        """田忌赛马优化算法(THRO)算子"""
        if not candidates:
            return []

        dim = len(candidates)
        if dim == 0:
            return []
        n_pop = pop_size // 2
        if n_pop == 0:
            n_pop = 1
        tianji_pos = np.random.randint(0, dim, n_pop)
        king_pos = np.random.randint(0, dim, n_pop)

        tianji_fit = np.array([candidates[i][2]['energy_cost'] for i in tianji_pos])
        king_fit = np.array([candidates[i][2]['energy_cost'] for i in king_pos])

        best_idx = np.argmin(np.concatenate([tianji_fit, king_fit]))
        if best_idx < n_pop:
            best_idx = tianji_pos[best_idx]
        else:
            best_idx = king_pos[best_idx - n_pop]
        best_score = candidates[best_idx][2]['energy_cost']

        for it in range(max_iter):
            p = 1 - it / max_iter

            # 种群混合与排序
            combined_pos = np.concatenate([tianji_pos, king_pos])
            combined_fit = np.concatenate([tianji_fit, king_fit])
            sorted_idx = np.argsort(combined_fit)
            combined_pos = combined_pos[sorted_idx]

            tianji_pos = combined_pos[:n_pop]
            king_pos = combined_pos[n_pop:]
            tianji_fit = np.array([candidates[i][2]['energy_cost'] for i in tianji_pos])
            king_fit = np.array([candidates[i][2]['energy_cost'] for i in king_pos])

            # 生成新解
            for i in range(n_pop):
                # 田忌种群更新
                if np.random.rand() > 0.5:
                    tr4, tr5 = np.random.choice(n_pop, 2, replace=False)
                    lt = 0.2 * ParallelHeuristics.levy(1)[0]
                    new_idx = int(tianji_pos[i] + lt * (tianji_pos[tr4] - tianji_pos[tr5]))
                else:
                    mt = 0.5 * (1 + 0.001 * (1 - it / max_iter) ** 2 * np.sin(np.pi * np.random.rand()))
                    ft_idx = np.argmin(tianji_fit)
                    new_idx = int(tianji_pos[ft_idx] + mt * (tianji_pos[ft_idx] - tianji_pos[i]))

                new_idx = np.clip(new_idx, 0, dim - 1)
                new_score = candidates[new_idx][2]['energy_cost']
                if new_score < tianji_fit[i]:
                    tianji_pos[i] = new_idx
                    tianji_fit[i] = new_score
                    if new_score < best_score:
                        best_score = new_score
                        best_idx = new_idx

                # 齐王种群更新
                if np.random.rand() > 0.5:
                    kr1, kr2 = np.random.choice(n_pop, 2, replace=False)
                    lk = 0.2 * ParallelHeuristics.levy(1)[0]
                    new_idx = int(king_pos[i] + lk * (king_pos[kr1] - king_pos[kr2]))
                else:
                    mk = 0.5 * (1 + 0.001 * (1 - it / max_iter) ** 2 * np.sin(np.pi * np.random.rand()))
                    fk_idx = np.argmin(king_fit)
                    new_idx = int(king_pos[fk_idx] + mk * (king_pos[fk_idx] - king_pos[i]))

                new_idx = np.clip(new_idx, 0, dim - 1)
                new_score = candidates[new_idx][2]['energy_cost']
                if new_score < king_fit[i]:
                    king_pos[i] = new_idx
                    king_fit[i] = new_score
                    if new_score < best_score:
                        best_score = new_score
                        best_idx = new_idx

        return [candidates[best_idx]]

    @staticmethod
    def cpo_optimize(candidates, max_iter=10, pop_size=10):
        """冠豪猪优化算法(CPO)算子"""
        if not candidates:
            return []

        dim = len(candidates)
        if dim == 0:
            return []
        lb, ub = 0, dim - 1
        pop = np.random.randint(lb, ub + 1, size=pop_size)
        pop = np.clip(pop, lb, ub)

        fitness = np.array([candidates[i][2]['energy_cost'] for i in pop])
        best_idx = pop[np.argmin(fitness)]
        best_score = np.min(fitness)

        n_min = int(0.8 * pop_size)
        alpha = 0.2
        tf = 0.8

        for t in range(max_iter):
            r2 = np.random.rand()
            new_pop = pop.copy()
            new_fitness = fitness.copy()

            for i in range(pop_size):
                if np.random.rand() < 0.5:  # 探索阶段
                    if np.random.rand() < 0.5:  # 第一种防御机制
                        y = (pop[i] + pop[np.random.randint(pop_size)]) / 2
                        new_idx = int(pop[i] + np.random.randn() * np.abs(2 * np.random.rand() * best_idx - y))
                    else:  # 第二种防御机制
                        y = (pop[i] + pop[np.random.randint(pop_size)]) / 2
                        u1 = np.random.rand() > np.random.rand()
                        if u1:
                            new_idx = int(y + np.random.rand() * (
                                        pop[np.random.randint(pop_size)] - pop[np.random.randint(pop_size)]))
                        else:
                            new_idx = pop[i]
                else:  # 利用阶段
                    yt = 2 * np.random.rand() * (1 - t / max_iter) ** (t / max_iter)
                    u2 = np.random.rand() < 0.5

                    if np.random.rand() < tf:  # 第三种防御机制
                        st = np.exp(fitness[i] / (np.sum(fitness) + 1e-10))
                        s = st * yt * (1 if u2 else -1)
                        new_idx = int(pop[np.random.randint(pop_size)] + st *
                                      (pop[np.random.randint(pop_size)] - pop[np.random.randint(pop_size)]) - s)
                    else:  # 第四种防御机制
                        mt = np.exp(fitness[i] / (np.sum(fitness) + 1e-10))
                        vt = pop[i]
                        vtp = pop[np.random.randint(pop_size)]
                        ft = np.random.rand() * mt * (-vt + vtp)
                        s = ft * yt * (1 if u2 else -1)
                        new_idx = int(best_idx + (alpha * (1 - r2) + r2) *
                                      ((1 if u2 else -1) * best_idx - vt) - s)

                new_idx = np.clip(new_idx, lb, ub)
                new_score = candidates[new_idx][2]['energy_cost']

                if new_score < fitness[i]:
                    new_pop[i] = new_idx
                    new_fitness[i] = new_score
                    if new_score < best_score:
                        best_score = new_score
                        best_idx = new_idx

            pop = new_pop
            fitness = new_fitness
            pop_size = max(n_min, int(n_min + (pop_size - n_min) *
                                      (1 - (np.mod(t, max_iter / 2) / (max_iter / 2)))))

        return [candidates[best_idx]]

    @staticmethod
    def pga_optimize(candidates, max_iter=10, pop_size=10):
        """向光优化算法(PGA)算子"""
        if not candidates:
            return []

        dim = len(candidates)
        if dim == 0:
            return []
        lb, ub = 0, dim - 1
        pop = np.random.randint(lb, ub + 1, size=pop_size)
        pop = np.clip(pop, lb, ub)

        fitness = np.array([candidates[i][2]['energy_cost'] for i in pop])
        best_idx = pop[np.argmin(fitness)]
        best_score = np.min(fitness)

        vec_flag = [1, -1]
        nl = int((0.2 * np.random.rand() + 0.4) * pop_size)
        if nl == 0:
            nl = 1
        ns = pop_size - nl
        if ns == 0:
            ns = 1

        for t in range(max_iter):
            alpha = np.exp(-t / max_iter)
            # 确保数组大小正确
            if pop.size < pop_size:
                # 如果pop数组大小不足，重新生成
                pop = np.random.randint(lb, ub + 1, size=pop_size)
                pop = np.clip(pop, lb, ub)
            x_s = pop[:ns]
            x_l = pop[ns:]
            fit_s = fitness[:ns]
            fit_l = fitness[ns:]

            # 局部最优更新
            best_s_idx = np.argmin(fit_s)
            best_s = x_s[best_s_idx]
            best_l_idx = np.argmin(fit_l)
            best_l = x_l[best_l_idx]

            # 向光性更新
            beta = np.random.choice(vec_flag)
            curvature = beta * (alpha - np.mean(fit_s) / (best_score + 1e-10))

            # 长距离个体更新
            new_x_l = []
            new_fit_l = []
            for i in range(len(x_l)):
                r2, r3, r4 = np.random.rand(3) * 2 - 1
                dd = np.random.randint(pop_size)

                # 两种更新策略
                idx1 = int(pop[dd] + beta * alpha * r2 * np.abs(pop[dd] - x_l[i]) +
                           beta * alpha * r3 * np.abs(best_l - x_l[i]))
                idx2 = int(x_l[i] + alpha * r4 * np.abs(best_l - x_l[i]))

                idx1 = np.clip(idx1, lb, ub)
                idx2 = np.clip(idx2, lb, ub)

                new_x_l.extend([idx1, idx2])
                new_fit_l.extend([candidates[idx1][2]['energy_cost'], candidates[idx2][2]['energy_cost']])

            # 短距离个体更新
            new_x_s = []
            new_fit_s = []
            for i in range(len(x_s)):
                r = np.random.rand() * 2 - 1
                beta = np.random.choice(vec_flag)

                # 两种更新策略
                idx1 = int(x_s[i] + beta * alpha * r * np.abs(x_s[i] - pop[np.random.randint(pop_size)]))
                idx2 = int(x_l[np.random.randint(len(x_l))] + beta * alpha * r * (best_l - x_s[i]))

                idx1 = np.clip(idx1, lb, ub)
                idx2 = np.clip(idx2, lb, ub)

                new_x_s.extend([idx1, idx2])
                new_fit_s.extend([candidates[idx1][2]['energy_cost'], candidates[idx2][2]['energy_cost']])

            # 合并并选择最优
            x_s = np.concatenate([x_s, new_x_s])
            fit_s = np.concatenate([fit_s, new_fit_s])
            if len(fit_s) > 0:
                sorted_idx = np.argsort(fit_s)
                x_s = x_s[sorted_idx[:ns]]
                fit_s = fit_s[sorted_idx[:ns]]
            else:
                x_s = x_s[:ns]
                fit_s = fit_s[:ns]

            x_l = np.concatenate([x_l, new_x_l])
            fit_l = np.concatenate([fit_l, new_fit_l])
            if len(fit_l) > 0:
                sorted_idx = np.argsort(fit_l)
                x_l = x_l[sorted_idx[:nl]]
                fit_l = fit_l[sorted_idx[:nl]]
            else:
                x_l = x_l[:nl]
                fit_l = fit_l[:nl]

            # 全局更新
            pop = np.concatenate([x_s, x_l])
            fitness = np.concatenate([fit_s, fit_l])

            current_best_idx = np.argmin(fitness)
            if fitness[current_best_idx] < best_score:
                best_score = fitness[current_best_idx]
                best_idx = pop[current_best_idx]

        return [candidates[best_idx]]


# -------------------------- 3. 树状遗传编程超启发式算法实现 --------------------------
class TreeNode:
    """树节点：构成遗传编程的基本单元"""

    def __init__(self, node_type: str, value: str = None):
        self.node_type = node_type  # "function" 或 "terminal"
        self.value = value  # 函数（+,-,*,/,max,min）或终端（资源属性）
        self.children = []  # 子节点（函数节点有子节点，终端节点无）

    def add_child(self, child_node: "TreeNode") -> None:
        """添加子节点"""
        self.children.append(child_node)

    def calculate(self, node_features: Dict) -> float:
        """计算节点值：根据节点类型和输入特征"""
        if self.node_type == "terminal":
            # 终端节点：返回对应能源系统特征值
            feature_mapping = {
                "CAP": node_features.get("capacity", 0.0),  # 容量
                "RCAP": node_features.get("remaining_capacity", 0.0),  # 剩余容量
                "EFF": node_features.get("efficiency", 0.0),  # 效率
                "CF": node_features.get("carbon_factor", 0.0),  # 碳排放系数
                "FC": node_features.get("fuel_cost", 0.0),  # 燃料成本
                "EP": node_features.get("energy_price", 0.0),  # 能源价格
                "SOC": node_features.get("soc", 0.0),  # 荷电状态
                "PRI": node_features.get("priority", 0.0),  # 优先级
                "CRI": 1.0 if node_features.get("critical", False) else 0.0,  # 关键负荷
                "EC": node_features.get("energy_cost", 0.0),  # 能源成本
                "CE": node_features.get("carbon_emission", 0.0),  # 碳排放
                "REL": node_features.get("reliability", 0.0),  # 可靠性
                "DIST": node_features.get("distance", 0.0)  # 距离
            }
            return feature_mapping.get(self.value, 0.0)
        else:
            # 函数节点：计算子节点值并应用函数
            child_values = [child.calculate(node_features) for child in self.children]
            if len(child_values) == 0:
                return 0.0

            # 处理NaN和无穷大值
            clean_values = []
            for val in child_values:
                if np.isnan(val) or np.isinf(val):
                    clean_values.append(0.0)
                else:
                    clean_values.append(val)

            if len(clean_values) == 0:
                return 0.0

            if self.value == "+":
                return sum(clean_values)
            elif self.value == "-":
                if len(clean_values) >= 2:
                    return clean_values[0] - clean_values[1]
                else:
                    return clean_values[0]
            elif self.value == "*":
                result = 1.0
                for val in clean_values:
                    result *= val
                return result
            elif self.value == "/":
                denominator = clean_values[1] if len(clean_values) >= 2 else 1.0
                if denominator == 0:
                    return 1.0  # 避免除零
                else:
                    return clean_values[0] / denominator
            elif self.value == "max":
                if len(clean_values) == 0:
                    return 0.0
                else:
                    return max(clean_values)
            elif self.value == "min":
                if len(clean_values) == 0:
                    return 0.0
                else:
                    return min(clean_values)
            else:
                return 0.0

    def get_depth(self) -> int:
        """计算树深度"""
        if not self.children:
            return 1
        return 1 + max(child.get_depth() for child in self.children)

    def copy(self) -> "TreeNode":
        """复制节点（用于遗传操作）"""
        new_node = TreeNode(self.node_type, self.value)
        for child in self.children:
            new_node.add_child(child.copy())
        return new_node

    def _subtree_to_vector(self, vector: List, depth: int, max_depth: int, function_set: List[str],
                           terminal_set: List[str]) -> List:
        """递归地将树转换为一个固定长度的向量表示。"""
        # 为当前节点编码
        if self.node_type == "function":
            # 函数节点用正数表示
            func_index = function_set.index(self.value) + 1
            vector.append(func_index)
        else:
            # 终端节点用负数表示
            term_index = terminal_set.index(self.value) + 1
            vector.append(-term_index)

        # 如果未达到最大深度，则递归处理子节点
        if depth < max_depth:
            if self.node_type == "function":
                for child in self.children:
                    vector = self._subtree_to_vector(vector, depth + 1, max_depth, function_set, terminal_set)
            else:
                # 终端节点在非叶子层，用0填充子节点位置
                num_children = 2  # 假设所有函数都是二元的
                for _ in range(num_children):
                    vector = self._subtree_to_vector(vector, depth + 1, max_depth, function_set, terminal_set)
        return vector

    def tree_to_vector(self, max_depth: int, function_set: List[str], terminal_set: List[str]) -> np.ndarray:
        """将树转换为一个固定长度的向量表示。"""
        # 计算满二叉树的节点总数
        num_nodes = (2 ** max_depth) - 1
        vector = []
        vector = self._subtree_to_vector(vector, 1, max_depth, function_set, terminal_set)
        # 确保向量长度正确
        if len(vector) < num_nodes:
            vector.extend([0] * (num_nodes - len(vector)))
        return np.array(vector, dtype=float)

    @classmethod
    def _vector_to_subtree(cls, vector: List, index: int, depth: int, max_depth: int, function_set: List[str],
                           terminal_set: List[str]) -> Tuple["TreeNode", int]:
        """从向量递归地构建树。"""
        if index >= len(vector):
            return None, index

        node_value = vector[index]
        index += 1

        if node_value > 0:
            # 函数节点
            func_index = int(node_value) - 1
            if func_index >= len(function_set):
                # 如果索引越界，随机选择一个函数
                func_index = random.randint(0, len(function_set) - 1)
            node = cls("function", function_set[func_index])
            if depth < max_depth:
                # 递归构建子节点
                child1, index = cls._vector_to_subtree(vector, index, depth + 1, max_depth, function_set, terminal_set)
                child2, index = cls._vector_to_subtree(vector, index, depth + 1, max_depth, function_set, terminal_set)
                if child1:
                    node.add_child(child1)
                if child2:
                    node.add_child(child2)
            return node, index
        elif node_value < 0:
            # 终端节点
            term_index = int(-node_value) - 1
            if term_index >= len(terminal_set):
                # 如果索引越界，随机选择一个终端
                term_index = random.randint(0, len(terminal_set) - 1)
            node = cls("terminal", terminal_set[term_index])
            return node, index
        else:
            # 值为0，返回一个随机终端节点
            term_index = random.randint(0, len(terminal_set) - 1)
            node = cls("terminal", terminal_set[term_index])
            return node, index

    @classmethod
    def vector_to_tree(cls, vector: np.ndarray, max_depth: int, function_set: List[str],
                       terminal_set: List[str]) -> "TreeNode":
        """从向量构建树。"""
        vector_list = vector.tolist()
        root, _ = cls._vector_to_subtree(vector_list, 0, 1, max_depth, function_set, terminal_set)
        if not root:
            # 如果根节点为空，创建一个默认的简单树
            root = cls("function", "+")
            root.add_child(cls("terminal", random.choice(terminal_set)))
            root.add_child(cls("terminal", random.choice(terminal_set)))
        return root

    def grow_to_max_depth(self, max_depth: int, function_set: List[str], terminal_set: List[str]) -> None:
        """将树生长到指定的最大深度。"""

        def _grow(node: TreeNode, current_depth: int):
            if current_depth < max_depth:
                if node.node_type == "function":
                    # 确保函数节点有足够的子节点
                    while len(node.children) < 2:
                        child = TreeNode("terminal", random.choice(terminal_set))
                        node.add_child(child)
                    # 递归生长子节点
                    for child in node.children:
                        _grow(child, current_depth + 1)
                else:  # node.node_type == "terminal"
                    # 在非叶子层的终端节点，有一定概率变为函数节点
                    if random.random() < 0.7:  # 70%的概率变为函数节点
                        node.node_type = "function"
                        node.value = random.choice(function_set)
                        # 为新的函数节点添加子节点
                        node.add_child(TreeNode("terminal", random.choice(terminal_set)))
                        node.add_child(TreeNode("terminal", random.choice(terminal_set)))
                        # 递归生长子节点
                        for child in node.children:
                            _grow(child, current_depth + 1)

        _grow(self, 1)


class AdaptiveTreeGP:
    """自适应树状遗传-差分架构：结合TreeGP与JADE算法"""

    def __init__(self, pop_size: int = 30, generations: int = 10, d_min: int = 2, d_max: int = 7,
                 function_set: List[str] = None, terminal_set: List[str] = None):
        # TreeGP参数
        self.d_min = d_min
        self.d_max = d_max
        self.function_set = function_set if function_set else ["+", "-", "*", "/", "max", "min"]
        self.terminal_set = terminal_set if terminal_set else [
            "CCI", "RMC", "RSC", "ABW", "PQ", "NMP",
            "RCC", "ET", "ATT", "R", "POW", "DIST"
        ]
        self.function_arity = {"+": 2, "-": 2, "*": 2, "/": 2, "max": 2, "min": 2}

        # JADE参数
        self.pop_size = pop_size  # 种群规模
        self.generations = generations  # 每轮任务分配的演化代数
        self.c = 0.1  # 控制因子
        self.p = 0.05  # 精英比例
        self.top = max(1, int(self.p * self.pop_size))  # 每代中最优的top个
        self.archive = []  # 外部存档

        # 自适应参数
        self.u_cr = 0.5  # CR的均值
        self.u_f = 0.5  # F的均值

        # 向量表示的维度（基于最大深度的满二叉树）
        self.vector_dim = (2 ** self.d_max) - 1
        # 向量的边界
        self.lb = -len(self.terminal_set)
        self.ub = len(self.function_set)

        # 当前种群
        self.population = self._initialize_population()

    def _initialize_population(self) -> List[Tuple[TreeNode, np.ndarray]]:
        """初始化种群，每个个体包含树和其向量表示"""
        population = []
        for _ in range(self.pop_size):
            tree = self.generate_tree(method="ramped_half_and_half")
            # 确保树达到最大深度，以便向量表示一致
            tree.grow_to_max_depth(self.d_max, self.function_set, self.terminal_set)
            vector = tree.tree_to_vector(self.d_max, self.function_set, self.terminal_set)
            population.append((tree, vector))
        return population

    def generate_full_tree(self, current_depth: int, max_depth: int) -> TreeNode:
        """Full方法生成树"""
        if current_depth == max_depth:
            terminal = random.choice(self.terminal_set)
            return TreeNode("terminal", terminal)
        else:
            function = random.choice(self.function_set)
            node = TreeNode("function", function)
            for _ in range(self.function_arity[function]):
                child = self.generate_full_tree(current_depth + 1, max_depth)
                node.add_child(child)
            return node

    def generate_grow_tree(self, current_depth: int, max_depth: int) -> TreeNode:
        """Grow方法生成树"""
        if current_depth == max_depth:
            terminal = random.choice(self.terminal_set)
            return TreeNode("terminal", terminal)
        else:
            if random.random() < 0.7 and current_depth < max_depth - 1:
                function = random.choice(self.function_set)
                node = TreeNode("function", function)
                for _ in range(self.function_arity[function]):
                    child = self.generate_grow_tree(current_depth + 1, max_depth)
                    node.add_child(child)
                return node
            else:
                terminal = random.choice(self.terminal_set)
                return TreeNode("terminal", terminal)

    def generate_tree(self, method: str = "ramped_half_and_half") -> TreeNode:
        """生成树"""
        if method == "full":
            return self.generate_full_tree(1, self.d_max)
        elif method == "grow":
            depth = random.randint(self.d_min, self.d_max)
            return self.generate_grow_tree(1, depth)
        elif method == "ramped_half_and_half":
            if random.random() < 0.5:
                return self.generate_full_tree(1, self.d_max)
            else:
                depth = random.randint(self.d_min, self.d_max)
                return self.generate_grow_tree(1, depth)
        else:
            raise ValueError("Unsupported tree generation method")

    def _evaluate_fitness(self, tree: TreeNode, candidate_nodes: List[Tuple[int, Dict, Dict]]) -> float:
        """评估树的适应度：使用多目标评估方法
        
        基于非支配排序和拥挤距离，评估树对候选节点的排序质量。
        考虑的目标包括：最小化能源成本、最小化碳排放、最大化可靠性。
        """
        if not candidate_nodes:
            return 0.0
        
        # 为每个候选节点计算多目标值
        solutions = []
        for _, _, metrics in candidate_nodes:
            solution = {
                "energy_cost": metrics["energy_cost"],  # 最小化
                "carbon_emission": metrics["carbon_emission"],  # 最小化
                "reliability": metrics["reliability"]  # 最大化
            }
            solutions.append(solution)
        
        # 选择非支配解
        objectives = [("energy_cost", True), ("carbon_emission", True), ("reliability", False)]
        n = min(5, len(solutions))  # 选择最多5个非支配解
        nondominated_solutions = select_nondominated_solutions(solutions, objectives, n)
        if not nondominated_solutions:
            return 0.0
        
        # 获取非支配解的索引
        nondominated_indices = [solutions.index(sol) for sol in nondominated_solutions]
        
        # 计算拥挤距离（使用numpy数组格式）
        objectives_list = []
        for _, _, metrics in candidate_nodes:
            objectives = [
                metrics["energy_cost"],  # 最小化
                metrics["carbon_emission"],  # 最小化
                -metrics["reliability"]  # 最大化转换为最小化
            ]
            objectives_list.append(np.array(objectives))
        
        crowding_distances = self._crowding_distance(objectives_list, nondominated_indices)
        
        # 计算树对所有节点的评分
        scores = []
        for _, features, _ in candidate_nodes:
            score = tree.calculate(features)
            scores.append(score if not np.isnan(score) and not np.isinf(score) else 0.0)
        
        # 评估树的性能：非支配解的平均得分与其他解的平均得分之差
        if scores and max(scores) > 0:
            # 归一化分数
            max_score = max(scores)
            min_score = min(scores)
            if max_score - min_score > 0:
                normalized_scores = [(s - min_score) / (max_score - min_score) for s in scores]
            else:
                normalized_scores = [0.5 for _ in scores]
            
            # 计算非支配解和支配解的平均归一化分数
            nondominated_scores = [normalized_scores[i] for i in nondominated_indices]
            dominated_scores = [normalized_scores[i] for i in range(len(scores)) if i not in nondominated_indices]
            
            avg_nondominated_score = np.mean(nondominated_scores) if nondominated_scores else 0.0
            avg_dominated_score = np.mean(dominated_scores) if dominated_scores else 0.0
            
            # 适应度：非支配解的平均分数应高于支配解
            fitness = avg_nondominated_score - avg_dominated_score
            
            # 调整适应度范围，确保为正
            return max(0.1, fitness + 1.0)
        else:
            return 0.1

    def _get_candidate_multiobjectives(self, candidate_nodes: List[Tuple[int, Dict, Dict]]) -> List[np.ndarray]:
        """获取候选节点的多目标值向量列表"""
        objectives_list = []
        for node_id, node, task in candidate_nodes:
            # 计算多目标值：能源成本、碳排放、可靠性
            energy_cost = self._calculate_energy_cost(node, task)
            carbon_emission = self._calculate_carbon_emission(node, task)
            reliability = self._calculate_reliability(node, task)
            objectives_list.append(np.array([energy_cost, carbon_emission, 1 - reliability]))  # 可靠性取反，所有目标都求最小化
        return objectives_list

    def _non_dominated_sort(self, objectives_list: List[np.ndarray]) -> List[List[int]]:
        """非支配排序，返回各前沿的索引列表"""
        n = len(objectives_list)
        dominated_counts = [0] * n  # 被支配计数
        dominates_list = [[] for _ in range(n)]  # 支配的个体列表
        fronts = []  # 各前沿

        # 计算支配关系
        for i in range(n):
            for j in range(n):
                if i != j:
                    if self._dominates(objectives_list[i], objectives_list[j]):
                        dominates_list[i].append(j)
                    elif self._dominates(objectives_list[j], objectives_list[i]):
                        dominated_counts[i] += 1

        # 第一前沿：被支配计数为0的个体
        front_1 = [i for i in range(n) if dominated_counts[i] == 0]
        fronts.append(front_1)

        # 计算后续前沿
        while front_1:
            next_front = []
            for i in front_1:
                for j in dominates_list[i]:
                    dominated_counts[j] -= 1
                    if dominated_counts[j] == 0:
                        next_front.append(j)
            if next_front:
                fronts.append(next_front)
            front_1 = next_front

        return fronts

    def _dominates(self, obj1: np.ndarray, obj2: np.ndarray) -> bool:
        """检查obj1是否支配obj2（所有目标都不劣，至少一个目标更优）"""
        return all(obj1[i] <= obj2[i] for i in range(len(obj1))) and any(obj1[i] < obj2[i] for i in range(len(obj1)))

    def _crowding_distance(self, objectives_list: List[np.ndarray], front_indices: List[int]) -> Dict[int, float]:
        """计算拥挤距离"""
        n_obj = len(objectives_list[0])
        crowding_dist = {i: 0.0 for i in front_indices}

        # 对每个目标维度进行排序
        for m in range(n_obj):
            # 按第m个目标排序
            sorted_front = sorted(front_indices, key=lambda i: objectives_list[i][m])
            n = len(sorted_front)
            
            # 边界点拥挤距离设为无穷大
            if n > 0:
                crowding_dist[sorted_front[0]] = float('inf')
                crowding_dist[sorted_front[-1]] = float('inf')

            # 计算中间点的拥挤距离
            for i in range(1, n - 1):
                if objectives_list[sorted_front[-1]][m] != objectives_list[sorted_front[0]][m]:
                    crowding_dist[sorted_front[i]] += (
                        objectives_list[sorted_front[i+1]][m] - objectives_list[sorted_front[i-1]][m]
                    ) / (objectives_list[sorted_front[-1]][m] - objectives_list[sorted_front[0]][m])

        return crowding_dist

    def _multi_objective_selection(self, parents: List[Tuple[TreeNode, np.ndarray]], 
                                 offsprings: List[Tuple[TreeNode, np.ndarray]], 
                                 candidate_nodes: List[Tuple[int, Dict, Dict]]) -> List[Tuple[TreeNode, np.ndarray]]:
        """多目标选择：将父母和子代合并，通过非支配排序和拥挤距离选择"""
        combined = parents + offsprings
        combined_trees = [tree for tree, vec in combined]
        combined_vectors = [vec for tree, vec in combined]

        # 计算每个个体的多目标适应度值
        fitness_values = []
        for tree in combined_trees:
            # 使用多目标适应度评估
            fitness = self._evaluate_fitness(tree, candidate_nodes)
            fitness_values.append(fitness)

        # 非支配排序
        fronts = self._non_dominated_sort([np.array([f]) for f in fitness_values])  # 使用适应度作为单一目标进行排序

        # 选择新种群
        new_population = []
        for front in fronts:
            if len(new_population) + len(front) <= self.pop_size:
                # 前沿可以全部加入
                for idx in front:
                    new_population.append(combined[idx])
            else:
                # 需要按拥挤距离选择部分个体
                crowding_dist = self._crowding_distance([np.array([f]) for f in fitness_values], front)
                # 按拥挤距离降序排序
                sorted_front = sorted(front, key=lambda i: crowding_dist[i], reverse=True)
                needed = self.pop_size - len(new_population)
                for idx in sorted_front[:needed]:
                    new_population.append(combined[idx])
                break

        return new_population

    def evolve(self, candidate_nodes: List[Tuple[int, Dict, Dict]]) -> TreeNode:
        """执行JADE演化过程，返回最优的树"""
        if not candidate_nodes:
            return self.generate_tree()

        # 主迭代
        for gen in range(self.generations):
            # 1. 为每个个体生成CR和F
            cr_list = []
            f_list = []
            for _ in range(self.pop_size):
                # 生成CR
                cr = np.random.normal(self.u_cr, 0.1)
                while cr > 1 or cr < 0:
                    cr = np.random.normal(self.u_cr, 0.1)
                cr_list.append(cr)

                # 生成F
                f = np.random.standard_cauchy() * 0.1 + self.u_f
                while f <= 0:
                    f = np.random.standard_cauchy() * 0.1 + self.u_f
                if f > 1:
                    f = 1.0
                f_list.append(f)

            # 2. 评估当前种群的适应度
            fitness_pop = [self._evaluate_fitness(tree, candidate_nodes) for tree, _ in self.population]
            best_idx = np.argmin(fitness_pop)
            best_fitness = fitness_pop[best_idx]
            best_tree, best_vector = self.population[best_idx]

            # 3. 准备进行变异：获取Pbest和随机个体
            sorted_indices = np.argsort(fitness_pop)
            pbest_trees = [self.population[i][0] for i in sorted_indices[:self.top]]
            pbest_vectors = [self.population[i][1] for i in sorted_indices[:self.top]]

            # 4. 变异和交叉
            trial_vectors = []
            for i in range(self.pop_size):
                # a. 变异 (Mutation)
                # 选择pbest
                pbest_idx = random.randint(0, len(pbest_vectors) - 1)
                x_pbest_vec = pbest_vectors[pbest_idx]

                # 从当前种群选择r1
                r1_idx = random.randint(0, self.pop_size - 1)
                while r1_idx == i:
                    r1_idx = random.randint(0, self.pop_size - 1)
                x_r1_vec = self.population[r1_idx][1]

                # 从当前种群和存档中选择r2
                pandA_vectors = [ind[1] for ind in self.population] + self.archive
                if len(pandA_vectors) == 0:
                    # 如果存档为空，只从当前种群选择
                    r2_idx = random.randint(0, self.pop_size - 1)
                    while r2_idx == i or r2_idx == r1_idx:
                        r2_idx = random.randint(0, self.pop_size - 1)
                    x_r2_vec = self.population[r2_idx][1]
                else:
                    r2_idx = random.randint(0, len(pandA_vectors) - 1)
                    while r2_idx == i or r2_idx == r1_idx:
                        r2_idx = random.randint(0, len(pandA_vectors) - 1)
                    x_r2_vec = pandA_vectors[r2_idx]

                # DE/current-to-pbest/1
                x_i_vec = self.population[i][1]
                v_vec = x_i_vec + f_list[i] * (x_pbest_vec - x_i_vec) + f_list[i] * (x_r1_vec - x_r2_vec)

                # b. 交叉 (Crossover)
                j_rand = random.randint(0, self.vector_dim - 1)
                u_vec = np.copy(x_i_vec)
                for j in range(self.vector_dim):
                    if random.random() <= cr_list[i] or j == j_rand:
                        u_vec[j] = v_vec[j]

                # c. 边界处理 (Bounds Handling)
                for j in range(self.vector_dim):
                    if u_vec[j] < self.lb or u_vec[j] > self.ub:
                        # 随机重置
                        u_vec[j] = random.uniform(self.lb, self.ub)
                trial_vectors.append(u_vec)

            # 5. 生成试验个体
            trial_individuals = []
            for i in range(self.pop_size):
                trial_tree = TreeNode.vector_to_tree(trial_vectors[i], self.d_max, self.function_set, self.terminal_set)
                trial_individuals.append((trial_tree, trial_vectors[i]))

            # 6. 多目标选择和存档 (Selection and Archiving)
            successful_cr = []
            successful_f = []
            
            # 多目标选择：合并父母和子代，选择新种群
            new_population = self._multi_objective_selection(self.population, trial_individuals, candidate_nodes)

            # 记录成功的CR和F
            for i in range(self.pop_size):
                trial_tree = trial_individuals[i][0]
                trial_fitness = self._evaluate_fitness(trial_tree, candidate_nodes)
                parent_fitness = self._evaluate_fitness(self.population[i][0], candidate_nodes)
                
                if trial_fitness < parent_fitness:
                    # 试验个体更优，记录成功的CR和F
                    successful_cr.append(cr_list[i])
                    successful_f.append(f_list[i])

            self.population = new_population

            # 7. 维护存档：使用Pareto前沿
            all_vectors = [vec for tree, vec in self.population] + self.archive
            all_individuals = self.population + [(TreeNode.vector_to_tree(vec, self.d_max, self.function_set, self.terminal_set), vec) for vec in self.archive]
            
            if all_individuals:
                # 计算所有个体的多目标值
                all_fitness = [self._evaluate_fitness(tree, candidate_nodes) for tree, vec in all_individuals]
                objectives_list = [np.array([f]) for f in all_fitness]
                
                # 非支配排序
                fronts = self._non_dominated_sort(objectives_list)
                
                # 构建新存档：包含所有非支配解
                new_archive = []
                for idx in fronts[0]:  # 第一前沿为非支配解
                    new_archive.append(all_individuals[idx][1])
                
                # 限制存档大小
                if len(new_archive) > self.pop_size:
                    # 按拥挤距离排序
                    crowding_dist = self._crowding_distance(objectives_list, fronts[0])
                    sorted_archive = sorted(fronts[0], key=lambda i: crowding_dist[i], reverse=True)
                    new_archive = [all_individuals[idx][1] for idx in sorted_archive[:self.pop_size]]
                
                self.archive = new_archive

            # 8. 自适应更新参数均值
            if successful_cr:
                self.u_cr = (1 - self.c) * self.u_cr + self.c * np.mean(successful_cr)
            if successful_f:
                # Lehmer mean for F
                numerator = np.sum(np.square(successful_f))
                denominator = np.sum(successful_f)
                if denominator != 0:
                    self.u_f = (1 - self.c) * self.u_f + self.c * (numerator / denominator)

        # 返回演化后种群中的最优树（第一个非支配解）
        final_trees = [tree for tree, vec in self.population]
        final_fitness = [self._evaluate_fitness(tree, candidate_nodes) for tree in final_trees]
        fronts = self._non_dominated_sort([np.array([f]) for f in final_fitness])
        if fronts:
            return self.population[fronts[0][0]][0]  # 返回第一个非支配解
        else:
            # 异常情况处理
            best_final_idx = np.argmin(final_fitness)
            return self.population[best_final_idx][0]


# -------------------------- 4. 多智能体强化学习任务调度实现（GRPO版本） --------------------------
class MachineAgent:
    """工程机械智能体：基于GRPO算法的分布式多智能体实现"""

    def __init__(self, agent_id: int, state_dim: int, action_dim: int,
                 gamma: float = 0.99, epsilon: float = 0.1, lr: float = 0.001):
        self.agent_id = agent_id  # 智能体ID（对应工程机械节点ID）
        self.state_dim = state_dim  # 状态维度
        self.action_dim = action_dim  # 动作维度
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.lr = lr  # 学习率
        
        # 使用GRPO策略网络替换Q网络
        self.grpo_agent = GRPOAgent(agent_id, state_dim, action_dim, gamma=gamma)
        
        # 多目标奖励权重
        self.reward_weights = {
            "energy_cost": 0.4,
            "carbon_emission": 0.3,
            "reliability": 0.2,
            "priority": 0.1
        }

    def select_action(self, state: np.ndarray) -> int:
        """选择动作：基于GRPO策略"""
        # 确保状态没有NaN或Inf
        state = np.nan_to_num(state, nan=0.0, posinf=1.0, neginf=0.0)
        
        # ε-贪婪策略：随机探索或GRPO策略选择
        if random.random() < self.epsilon:
            # 探索：随机选择动作
            return random.randint(0, self.action_dim - 1)
        else:
            # 利用：使用GRPO策略选择动作
            return self.grpo_agent.select_action(state)

    def store_experience(self, state: np.ndarray, action: int, reward: Dict[str, float] or float,
                         next_state: np.ndarray, done: bool) -> None:
        """存储经验到GRPO经验回放池
        
        Args:
            reward: 多目标奖励字典，或已加权的标量奖励
        """
        # 确保状态没有NaN或Inf
        state = np.nan_to_num(state, nan=0.0, posinf=1.0, neginf=0.0)
        next_state = np.nan_to_num(next_state, nan=0.0, posinf=1.0, neginf=0.0)
        
        # 如果是多目标奖励字典，进行线性加权
        if isinstance(reward, dict):
            weighted_reward = sum(self.reward_weights.get(key, 0) * val for key, val in reward.items())
        else:
            weighted_reward = reward
            
        # 使用GRPO智能体存储经验
        # 注意：这里需要获取GRPO策略的log_prob和value，但为了简化，我们使用默认值
        # 在实际实现中，应该在select_action时记录这些值
        log_prob = 0.0  # 简化处理
        value = 0.0     # 简化处理
        
        self.grpo_agent.store_experience(state, action, reward, next_state, done, log_prob, value)

    def train(self, batch_size: int = 32) -> Dict[str, float]:
        """训练GRPO策略网络"""
        # 使用GRPO智能体进行训练
        metrics = self.grpo_agent.train()
        return metrics if metrics else {}

    def decay_epsilon(self, decay_rate: float = 0.995) -> None:
        """衰减探索率"""
        self.epsilon = max(0.01, self.epsilon * decay_rate)
        
    def sync_parameters(self, global_agent: 'MachineAgent') -> None:
        """同步全局参数（分布式训练）"""
        self.grpo_agent.sync_parameters(global_agent.grpo_agent)
        
    def save_checkpoint(self, filepath: str) -> None:
        """保存检查点"""
        self.grpo_agent.save_checkpoint(filepath)
        
    def load_checkpoint(self, filepath: str) -> None:
        """加载检查点"""
        self.grpo_agent.load_checkpoint(filepath)


class MultiAgentTaskScheduler:
    """多智能体任务调度器：整合并行启发式算子与分布式GRPO强化学习"""

    def __init__(self, env: EnergySystemEnvironment, task_generator: TaskGenerator, 
                 distributed_training: bool = True, num_processes: int = 4,
                 training_interval: int = 10, sync_interval: int = 50):
        self.env = env  # 云边环境
        self.task_generator = task_generator  # 任务生成器
        self.distributed_training = distributed_training  # 是否启用分布式训练
        self.num_processes = num_processes  # 进程数量
        self.training_interval = training_interval  # 训练间隔
        self.sync_interval = sync_interval  # 参数同步间隔
        
        # 初始化分布式协调器（如果启用分布式训练）
        if distributed_training:
            # 状态维度：机械状态（6）+任务状态（5）=11
            state_dim = 11
            # 动作维度：3（本地执行、卸载到边缘、卸载到云端）
            action_dim = 3
            self.distributed_coordinator = DistributedGRPOCoordinator(
                num_agents=len([n for n in self.env.nodes if n["type"] == 2]),
                state_dim=state_dim,
                action_dim=action_dim
            )
        else:
            self.distributed_coordinator = None
            
        self.machine_agents = self._init_agents()  # 工程机械智能体集合
        self.tbgp_hh = self._init_adaptive_tbgp_hh()  # 自适应树状遗传-差分架构
        self.parallel_heuristics = ParallelHeuristics()  # 并行启发式算子
        self.task_history = []  # 任务处理历史
        self.total_energy_cost = 0.0  # 总能源成本
        self.budget_exceed_count = 0  # 预算超出次数
        # 多目标Pareto前沿维护
        self.pareto_front = []  # Pareto前沿解集合
        self.pareto_history = []  # Pareto前沿历史记录
        
        # GRPO训练相关参数
        self.training_interval = 10  # 训练间隔（每处理多少个任务训练一次）
        self.sync_interval = 50  # 参数同步间隔
        self.checkpoint_interval = 100  # 检查点保存间隔
        self.training_step = 0  # 训练步数计数器

    def _init_agents(self) -> Dict[int, MachineAgent]:
        """初始化工程机械智能体"""
        agents = {}
        # 仅为工程机械节点创建智能体（type=2）
        machine_nodes = [node for node in self.env.nodes if node["type"] == 2]
        for node in machine_nodes:
            agent_id = node["node_id"]
            # 状态维度：机械状态（6）+任务状态（5）=11
            state_dim = 11
            # 动作维度：3（本地执行、卸载到边缘、卸载到云端）
            action_dim = 3
            agent = MachineAgent(agent_id, state_dim, action_dim)
            agents[agent_id] = agent
        return agents

    def _init_adaptive_tbgp_hh(self) -> AdaptiveTreeGP:
        """初始化自适应树状遗传-差分架构"""
        function_set = ["+", "-", "*", "/", "max", "min"]
        terminal_set = [
            "CAP", "RCAP", "EFF", "CF", "FC", "EP",
            "SOC", "PRI", "CRI", "EC", "CE", "REL", "DIST"
        ]
        return AdaptiveTreeGP(pop_size=30, generations=10, d_min=2, d_max=7,
                              function_set=function_set, terminal_set=terminal_set)

    def calculate_task_metrics(self, task: Dict, node_id: int) -> Dict:
        """计算任务 metrics：能源成本、碳排放、可靠性"""
        node = self.env.nodes[node_id]
        
        # 1. 响应时间：基于节点功率和任务需求计算
        if node["type"] == 0:  # 发电机：响应时间基于功率输出
            response_time = task["power_demand"] / node["capacity"] if node["capacity"] > 0 else float('inf')
        elif node["type"] == 1:  # 储能设备：响应时间基于充放电效率
            response_time = task["power_demand"] / (node["capacity"] * node["efficiency"]) if node["capacity"] > 0 else float('inf')
        else:  # 负荷节点：响应时间基于需求响应
            response_time = task["power_demand"] / node["demand"] if node["demand"] > 0 else float('inf')
            
        # 2. 能源成本计算：根据节点类型和能源价格计算
        if node["type"] == 0:  # 发电机
            energy_cost = task["power_demand"] * node["fuel_cost"]
        elif node["type"] == 1:  # 储能设备
            energy_cost = task["power_demand"] * self.env.energy_prices[1]  # 放电成本
        else:  # 负荷节点（购电成本）
            energy_cost = task["power_demand"] * self.env.energy_prices[2]

        # 3. 碳排放计算：根据节点类型和碳排放系数
        if node["type"] == 0:  # 发电机
            carbon_emission = task["power_demand"] * node["carbon_factor"]
        elif node["type"] == 1:  # 储能设备
            carbon_emission = task["power_demand"] * self.env.carbon_factors[1]
        else:  # 负荷节点
            carbon_emission = task["power_demand"] * self.env.carbon_factors[2]

        # 4. 传输损耗：基于连接距离计算
        distance = 0.0
        transmission_loss = 0.0
        # 在能源系统中，传输损耗主要考虑电网传输
        if node["type"] != 0:  # 非发电机节点（储能和负荷）
            # 找到最近的发电机作为电源点
            generator_nodes = [n for n in self.env.nodes if n["type"] == 0]
            if generator_nodes:
                nearest_generator = min(generator_nodes, 
                                       key=lambda n: self.env.connection_matrix[n["node_id"]][node_id])
                distance = self.env.connection_matrix[nearest_generator["node_id"]][node_id]
                if distance < float('inf'):  # 有效连接
                    transmission_loss = distance * 0.01  # 假设每单位距离损耗1%
                else:
                    transmission_loss = 0.0  # 无直接连接，无损耗

        # 5. 可靠性：基于节点类型和运行状态
        reliability = node["status"] * 0.95  # 运行状态良好的可靠性为0.95
        if node["type"] == 0:  # 发电机可靠性考虑运行时间
            # 使用默认的故障率参数
            lambda_e = node.get("lambda_e", 0.001)  # 默认故障率
            reliability *= math.exp(-lambda_e * response_time) if response_time < float('inf') else 0.0
        elif node["type"] == 1:  # 储能设备可靠性考虑荷电状态
            reliability *= node.get("soc", 0.5)  # SOC越高可靠性越高

        return {
            "response_time": response_time,
            "energy_cost": energy_cost,
            "carbon_emission": carbon_emission,
            "transmission_loss": transmission_loss,
            "reliability": reliability,
            "distance": distance,
            "remaining_capacity": node["remaining_capacity"] if node["type"] in [0, 1] else node["remaining_demand"]
        }

    def get_agent_state(self, agent_id: int, task: Dict) -> np.ndarray:
        """获取智能体状态"""
        agent_node = self.env.nodes[agent_id]
        # 能源系统状态（6维）：剩余容量/需求、容量/需求、效率、碳排放系数、位置x、位置y
        if agent_node["type"] in [0, 1]:  # 发电机和储能设备
            remaining_ratio = agent_node["remaining_capacity"] / agent_node["capacity"] if agent_node["capacity"] > 0 else 0.0
        else:  # 负荷节点
            remaining_ratio = agent_node["remaining_demand"] / agent_node["demand"] if agent_node["demand"] > 0 else 0.0
            
        machine_state = [
            remaining_ratio,  # 剩余容量/需求比例
            agent_node["capacity"] / 1000 if agent_node["type"] in [0, 1] else agent_node["demand"] / 1000,  # 容量/需求归一化
            agent_node.get("efficiency", 0.9),  # 效率
            agent_node["carbon_factor"],  # 碳排放系数
            agent_node["position"][0] / 100,
            agent_node["position"][1] / 100
        ]
        # 任务状态（5维）：功率需求、优先级、截止时间、预算、距离最近发电机
        generator_nodes = [n for n in self.env.nodes if n["type"] == 0]
        if generator_nodes:
            nearest_generator = min(generator_nodes,
                                   key=lambda n: math.hypot(agent_node["position"][0] - n["position"][0],
                                                            agent_node["position"][1] - n["position"][1]))
            distance_to_generator = math.hypot(agent_node["position"][0] - nearest_generator["position"][0],
                                              agent_node["position"][1] - nearest_generator["position"][1])
        else:
            distance_to_generator = 0.0

        task_state = [
            task["power_demand"] / 100,  # 归一化
            task["priority"] / 5,
            task.get("deadline", 10.0) / 100,  # 为没有deadline的任务提供默认值
            task["budget"] / 100,
            distance_to_generator / 100
        ]
        # 合并状态（11维）
        state = np.array(machine_state + task_state, dtype=np.float32)
        return state

    def calculate_reward(self, task: Dict, metrics: Dict) -> Dict[str, float]:
        """计算多目标奖励
        
        Returns:
            Dict[str, float]: 包含多个目标的奖励字典
                - deadline: 截止时间奖励
                - energy: 能耗奖励
                - reliability: 可靠性奖励
                - priority: 优先级奖励
        """
        # 1. 能源成本奖励：成本越低奖励越高
        energy_cost_reward = -metrics["energy_cost"] * 0.1
        # 2. 碳排放奖励：排放越低奖励越高
        carbon_reward = -metrics["carbon_emission"] * 0.05
        # 3. 可靠性奖励：可靠性越高奖励越高
        reliability_reward = metrics["reliability"] * 5.0
        # 4. 优先级奖励：高优先级任务完成奖励更高
        priority_reward = task["priority"] * 2.0 if metrics["energy_cost"] <= task["budget"] else 0.0

        # 返回多目标奖励字典
        return {
            "energy_cost": energy_cost_reward,
            "carbon_emission": carbon_reward,
            "reliability": reliability_reward,
            "priority": priority_reward
        }

    def _get_node_features(self, node: Dict, task: Dict) -> Dict:
        """获取节点特征向量
        
        Args:
            node: 节点信息字典
            task: 任务信息字典
            
        Returns:
            Dict: 节点特征向量
        """
        metrics = self.calculate_task_metrics(task, node["node_id"])
        
        # 根据节点类型提取不同的特征
        if node["type"] == 0:  # 发电机
            features = {
                "capacity": node["capacity"],  # 发电容量
                "remaining_capacity": node["remaining_capacity"],  # 剩余容量
                "efficiency": node.get("efficiency", 0.9),  # 发电效率
                "carbon_factor": node["carbon_factor"],  # 碳排放系数
                "fuel_cost": node.get("fuel_cost", 0.5),  # 燃料成本
                "energy_price": self.env.energy_prices[node["type"]],  # 能源价格
                "soc": 0.0,  # 发电机无SOC
                "priority": 0,  # 发电机无优先级
                "critical": 0.0,  # 发电机无关键性
                "energy_cost": metrics["energy_cost"],  # 能源成本
                "carbon_emission": metrics["carbon_emission"],  # 碳排放
                "reliability": metrics["reliability"],  # 可靠性
                "distance": metrics["distance"]  # 传输距离
            }
        elif node["type"] == 1:  # 储能设备
            features = {
                "capacity": node["capacity"],  # 储能容量
                "remaining_capacity": node["remaining_capacity"],  # 剩余容量
                "efficiency": node.get("efficiency", 0.9),  # 充放电效率
                "carbon_factor": node["carbon_factor"],  # 碳排放系数
                "energy_price": self.env.energy_prices[node["type"]],  # 能源价格
                "soc": node.get("soc", 0.5),  # 荷电状态
                "priority": 0,  # 储能设备无优先级
                "critical": 0.0,  # 储能设备无关键性
                "energy_cost": metrics["energy_cost"],  # 能源成本
                "carbon_emission": metrics["carbon_emission"],  # 碳排放
                "reliability": metrics["reliability"],  # 可靠性
                "distance": metrics["distance"]  # 传输距离
            }
        else:  # 负荷节点
            features = {
                "capacity": node["demand"],  # 负荷需求作为容量
                "remaining_capacity": node["remaining_demand"],  # 剩余需求
                "efficiency": 1.0,  # 负荷效率为1
                "carbon_factor": node["carbon_factor"],  # 碳排放系数
                "energy_price": self.env.energy_prices[node["type"]],  # 能源价格
                "soc": 0.0,  # 负荷无SOC
                "priority": node.get("priority", 0),  # 负荷优先级
                "critical": 1.0 if node.get("critical", False) else 0.0,  # 是否关键负荷
                "energy_cost": metrics["energy_cost"],  # 能源成本
                "carbon_emission": metrics["carbon_emission"],  # 碳排放
                "reliability": metrics["reliability"],  # 可靠性
                "distance": metrics["distance"]  # 传输距离
            }
        
        return features

    def task_assignment(self, task: Dict) -> Tuple[int, Dict]:
        """任务分配：结合并行启发式算子与多智能体决策"""
        # 1. 生成候选节点：满足资源约束
        candidate_nodes = []
        for node_id in range(self.env.node_count):
            node = self.env.nodes[node_id]
            # 根据节点类型检查资源约束
            if node["type"] == 0:  # 发电机：检查发电容量
                if node["remaining_capacity"] >= task["power_demand"]:
                    candidate_nodes.append((node_id, self._get_node_features(node, task), self.calculate_task_metrics(task, node_id)))
            elif node["type"] == 1:  # 储能设备：检查充放电能力
                if node["remaining_capacity"] >= task["power_demand"] or node["capacity"] - node["remaining_capacity"] >= task["power_demand"]:
                    candidate_nodes.append((node_id, self._get_node_features(node, task), self.calculate_task_metrics(task, node_id)))
            elif node["type"] == 2:  # 负荷：检查负荷需求
                if node["remaining_demand"] >= task["power_demand"]:
                    candidate_nodes.append((node_id, self._get_node_features(node, task), self.calculate_task_metrics(task, node_id)))

        if not candidate_nodes:
            cloud_nodes = [n for n in self.env.nodes if n["type"] == 0]
            if cloud_nodes:
                cloud_node_id = cloud_nodes[0]["node_id"]
                metrics = self.calculate_task_metrics(task, cloud_node_id)
                return cloud_node_id, metrics
            else:
                for node_id in range(self.env.node_count):
                    node = self.env.nodes[node_id]
                    metrics = self.calculate_task_metrics(task, node_id)
                    return node_id, metrics

        # 2. 并行启发式搜索：四种算法分别优化
        doa_result = self.parallel_heuristics.doa_optimize(candidate_nodes)
        thro_result = self.parallel_heuristics.thro_optimize(candidate_nodes)
        cpo_result = self.parallel_heuristics.cpo_optimize(candidate_nodes)
        pga_result = self.parallel_heuristics.pga_optimize(candidate_nodes)

        # 收集所有优化结果
        heuristic_results = doa_result + thro_result + cpo_result + pga_result

        # 3. 使用自适应树状遗传-差分架构评估候选节点
        best_tree = self.tbgp_hh.evolve(candidate_nodes)

        node_scores = []
        for node_id, features, metrics in heuristic_results:
            score = best_tree.calculate(features)
            if np.isnan(score) or np.isinf(score):
                score = 0.0
            node_scores.append((node_id, score, metrics))

        # 4. 多智能体决策
        machine_agents = list(self.machine_agents.values())
        if not machine_agents:
            best_node_id, best_score, best_metrics = max(node_scores, key=lambda x: x[1])
            self.env.update_resource_usage(
                best_node_id,
                task["power_demand"]
            )
            task["assigned_node"] = best_node_id
            task["completion_time"] = best_metrics["energy_cost"]
            if best_metrics["energy_cost"] > task["budget"]:
                self.budget_exceed_count += 1
            return best_node_id, best_metrics

        best_agent = None
        best_state = None
        best_action = None
        best_metrics = None
        best_reward = -float('inf')
        final_target_node_id = None

        for agent in machine_agents:
            state = self.get_agent_state(agent.agent_id, task)
            if np.any(np.isnan(state)) or np.any(np.isinf(state)):
                continue
            action = agent.select_action(state)

            if action == 0:
                local_candidates = [(nid, s, m) for nid, s, m in node_scores if nid == agent.agent_id]
                if local_candidates:
                    target_node_id = agent.agent_id
                    target_metrics = local_candidates[0][2]
                else:
                    target_node_id, _, target_metrics = max(node_scores, key=lambda x: x[1])
            elif action == 1:
                edge_candidates = [(nid, s, m) for nid, s, m in node_scores if self.env.nodes[nid]["type"] == 1]
                if edge_candidates:
                    target_node_id, _, target_metrics = max(edge_candidates, key=lambda x: x[1])
                else:
                    target_node_id, _, target_metrics = max(node_scores, key=lambda x: x[1])
            else:
                cloud_candidates = [(nid, s, m) for nid, s, m in node_scores if self.env.nodes[nid]["type"] == 0]
                if cloud_candidates:
                    target_node_id, _, target_metrics = max(cloud_candidates, key=lambda x: x[1])
                else:
                    target_node_id, _, target_metrics = max(node_scores, key=lambda x: x[1])

            reward = self.calculate_reward(task, target_metrics)
            
            # 将多目标奖励转换为标量进行比较（使用第一个智能体的权重作为基准）
            if isinstance(reward, dict) and machine_agents:
                first_agent = machine_agents[0] if machine_agents else None
                weighted_reward = sum(first_agent.reward_weights.get(key, 0) * val for key, val in reward.items())
            else:
                weighted_reward = reward

            if weighted_reward > best_reward:
                best_reward = weighted_reward
                best_agent = agent
                best_state = state
                best_action = action
                best_metrics = target_metrics
                final_target_node_id = target_node_id

        if final_target_node_id is None:
            best_node_id, best_score, best_metrics = max(node_scores, key=lambda x: x[1])
            final_target_node_id = best_node_id
            best_agent = machine_agents[0] if machine_agents else None
            best_state = self.get_agent_state(best_agent.agent_id, task) if best_agent else np.zeros(11)
            best_action = 0
            best_reward = self.calculate_reward(task, best_metrics)

        # 5. 更新资源和任务信息
        self.env.update_resource_usage(
            final_target_node_id,
            task["power_demand"]
        )

        if self.env.nodes[final_target_node_id]["type"] == 2:
            # 负荷节点：更新剩余需求
            self.env.nodes[final_target_node_id]["remaining_demand"] -= task["power_demand"]
            self.total_energy_cost += best_metrics["energy_cost"]

        task["assigned_node"] = final_target_node_id
        task["completion_time"] = best_metrics["energy_cost"]
        if best_metrics["energy_cost"] > task["budget"]:
            self.budget_exceed_count += 1

        # 6. 分布式GRPO智能体训练
        if best_agent is not None:
            next_state = self.get_agent_state(best_agent.agent_id, task)
            done = True
            
            # 使用GRPO智能体存储经验
            # MachineAgent.store_experience只接受5个参数：state, action, reward, next_state, done
            best_agent.store_experience(best_state, best_action, best_reward, next_state, done)
            
            # 分布式训练逻辑
            self.training_step += 1
            
            # 定期训练
            if self.training_step % self.training_interval == 0:
                training_metrics = best_agent.train()
                if training_metrics:
                    print(f"训练步数 {self.training_step}: {training_metrics}")
            
            # 定期同步参数（分布式训练）
            if self.distributed_training and self.training_step % self.sync_interval == 0:
                self._sync_distributed_parameters()
                print(f"参数同步完成 (步数: {self.training_step})")
            
            # 定期保存检查点
            if self.training_step % self.checkpoint_interval == 0:
                checkpoint_file = f"grpo_checkpoint_{self.training_step}.pth"
                best_agent.save_checkpoint(checkpoint_file)
                print(f"检查点已保存: {checkpoint_file}")
            
            best_agent.decay_epsilon()
        
        # 7. 将当前解添加到Pareto前沿
        # 多目标定义：目标名称和优化方向（True表示最小化，False表示最大化）
        objective_definitions = [
            ("energy_cost", True),      # 最小化能源成本
            ("carbon_emission", True),  # 最小化碳排放
            ("reliability", False),     # 最大化可靠性
            ("budget_satisfaction", True)  # 最小化预算超出（0表示满足，1表示超出）
        ]
        
        # 多目标值向量
        objective_values = [
            best_metrics["energy_cost"],  # 最小化
            best_metrics["carbon_emission"],  # 最小化
            best_metrics["reliability"],  # 最大化
            0.0 if best_metrics["energy_cost"] > task["budget"] else 1.0  # 二进制：0表示未满足，1表示满足
        ]
        
        # 解的表示：包含任务信息和多目标值
        solution = {
            "task_id": task["task_id"],
            "assigned_node": final_target_node_id,
            "node_type": self.env.component_types[self.env.nodes[final_target_node_id]["type"]],
            "energy_cost": best_metrics["energy_cost"],
            "carbon_emission": best_metrics["carbon_emission"],
            "reliability": best_metrics["reliability"],
            "budget_satisfaction": 0.0 if best_metrics["energy_cost"] > task["budget"] else 1.0,
            "metrics": best_metrics,
            "rewards": best_reward
        }
        
        # 更新Pareto前沿
        self.pareto_front = update_pareto_front(self.pareto_front + [solution], objective_definitions)
        
        return final_target_node_id, best_metrics

    def _sync_distributed_parameters(self) -> None:
        """同步分布式智能体参数"""
        if not self.distributed_training or self.distributed_coordinator is None:
            return
        
        # 收集所有智能体的参数
        agent_params = []
        for agent in self.machine_agents.values():
            agent_params.append(agent.grpo_agent.get_parameters())
        
        # 使用分布式协调器同步参数
        synchronized_params = self.distributed_coordinator.synchronize_parameters(agent_params)
        
        # 更新所有智能体的参数
        for agent, new_params in zip(self.machine_agents.values(), synchronized_params):
            agent.grpo_agent.set_parameters(new_params)
        
        print(f"分布式参数同步完成，共同步 {len(agent_params)} 个智能体")

    def run_simulation(self, episodes: int = 50, tasks_per_episode: int = 20) -> None:
        """运行仿真：多轮任务调度（支持分布式GRPO训练）"""
        print("Starting task scheduling simulation with Distributed GRPO...")
        
        # 启动分布式训练（如果启用）
        if self.distributed_training and self.distributed_coordinator is not None:
            print("启动分布式训练协调器...")
            self.distributed_coordinator.start_training()
        
        metrics_history = {
            "episode": [], "total_carbon_emission": [], "budget_exceed_rate": [], 
            "avg_energy_cost": [], "avg_reliability": [],
            "training_step": [], "policy_loss": [], "value_loss": [], "entropy_loss": []
        }

        for episode in range(episodes):
            self.env.reset_resources()
            self.total_energy_cost = 0.0
            self.budget_exceed_count = 0
            episode_tasks = self.task_generator.generate_task_batch(tasks_per_episode)
            episode_energy_costs = []
            episode_reliabilities = []
            episode_carbon_emissions = []
            
            # 记录训练指标
            episode_policy_loss = []
            episode_value_loss = []
            episode_entropy_loss = []

            for task in episode_tasks:
                assigned_node_id, metrics = self.task_assignment(task)
                self.task_history.append({
                    "task_id": task["task_id"], "episode": episode, "assigned_node": assigned_node_id,
                    "node_type": self.env.component_types[self.env.nodes[assigned_node_id]["type"]],
                    "energy_cost": metrics["energy_cost"], "budget": task["budget"],
                    "budget_exceeded": metrics["energy_cost"] > task["budget"],
                    "carbon_emission": metrics["carbon_emission"], "reliability": metrics["reliability"]
                })
                episode_energy_costs.append(metrics["energy_cost"])
                episode_reliabilities.append(metrics["reliability"])
                episode_carbon_emissions.append(metrics["carbon_emission"])

            avg_energy_cost = np.mean(episode_energy_costs) if episode_energy_costs else 0.0
            avg_reliability = np.mean(episode_reliabilities) if episode_reliabilities else 0.0
            budget_exceed_rate = self.budget_exceed_count / tasks_per_episode
            total_carbon_emission = sum(episode_carbon_emissions) if episode_carbon_emissions else 0.0
            
            # 计算平均训练损失
            avg_policy_loss = np.mean(episode_policy_loss) if episode_policy_loss else 0.0
            avg_value_loss = np.mean(episode_value_loss) if episode_value_loss else 0.0
            avg_entropy_loss = np.mean(episode_entropy_loss) if episode_entropy_loss else 0.0

            metrics_history["episode"].append(episode)
            metrics_history["total_carbon_emission"].append(total_carbon_emission)
            metrics_history["budget_exceed_rate"].append(budget_exceed_rate)
            metrics_history["avg_energy_cost"].append(avg_energy_cost)
            metrics_history["avg_reliability"].append(avg_reliability)
            metrics_history["training_step"].append(self.training_step)
            metrics_history["policy_loss"].append(avg_policy_loss)
            metrics_history["value_loss"].append(avg_value_loss)
            metrics_history["entropy_loss"].append(avg_entropy_loss)

            print(f"Episode {episode + 1}/{episodes} | "
                  f"训练步数: {self.training_step} | "
                  f"总碳排放: {total_carbon_emission:.2f}kg | "
                  f"预算超出率: {budget_exceed_rate:.2%} | "
                  f"平均能源成本: {avg_energy_cost:.2f}元 | "
                  f"平均可靠性: {avg_reliability:.4f}")
            
            if episode_policy_loss:
                print(f"训练损失 - 策略: {avg_policy_loss:.4f}, 价值: {avg_value_loss:.4f}, 熵: {avg_entropy_loss:.4f}")

        # 关闭分布式训练
        if self.distributed_training and self.distributed_coordinator is not None:
            print("关闭分布式训练协调器...")
            self.distributed_coordinator.stop_training()
            
        # 保存最终检查点
        final_checkpoint = "grpo_final_checkpoint.pth"
        if self.machine_agents:
            first_agent = list(self.machine_agents.values())[0]
            first_agent.save_checkpoint(final_checkpoint)
            print(f"最终检查点已保存: {final_checkpoint}")

        self.save_results(metrics_history)
        self.plot_results(metrics_history)

    def save_results(self, metrics_history: Dict) -> None:
        """保存结果到CSV文件"""
        task_df = pd.DataFrame(self.task_history)
        task_df.to_csv("task_scheduling_history.csv", index=False)
        metrics_df = pd.DataFrame(metrics_history)
        metrics_df.to_csv("scheduling_metrics.csv", index=False)
        print("Results saved to task_scheduling_history.csv and scheduling_metrics.csv")

    def plot_results(self, metrics_history: Dict) -> None:
        """可视化调度结果"""
        
    def schedule_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """调度优化任务
        
        Args:
            tasks: 待调度的优化任务列表
            
        Returns:
            已调度的任务列表
        """
        scheduled_tasks = []
        
        for task in tasks:
            try:
                # 使用任务分配算法分配任务
                assigned_node_id, metrics = self.task_assignment(task)
                
                # 更新任务状态
                task["assigned_node"] = assigned_node_id
                task["completion_time"] = metrics["energy_cost"]
                task["metrics"] = metrics
                
                # 记录任务调度历史
                self.task_history.append({
                    "task_id": task["task_id"],
                    "task_type": task["task_type"],
                    "time_step": task["time_step"],
                    "assigned_node": assigned_node_id,
                    "node_type": self.env.component_types[self.env.nodes[assigned_node_id]["type"]],
                    "energy_cost": metrics["energy_cost"],
                    "carbon_emission": metrics["carbon_emission"],
                    "reliability": metrics["reliability"],
                    "budget": task["budget"],
                    "budget_exceeded": metrics["energy_cost"] > task["budget"]
                })
                
                scheduled_tasks.append(task)
                
            except Exception as e:
                print(f"任务 {task['task_id']} 调度失败: {e}")
                # 如果调度失败，将任务标记为未分配
                task["assigned_node"] = None
                task["completion_time"] = None
                task["metrics"] = None
                scheduled_tasks.append(task)
        
        return scheduled_tasks
    
    def get_scheduling_performance(self) -> Dict:
        """获取任务调度性能指标
        
        Returns:
            调度性能指标字典
        """
        if not self.task_history:
            return {
                "total_tasks": 0,
                "success_rate": 0.0,
                "avg_energy_cost": 0.0,
                "avg_carbon_emission": 0.0,
                "avg_reliability": 0.0,
                "budget_exceed_rate": 0.0,
                "pareto_solutions": len(self.pareto_front)
            }
        
        total_tasks = len(self.task_history)
        successful_tasks = [t for t in self.task_history if t["assigned_node"] is not None]
        success_rate = len(successful_tasks) / total_tasks if total_tasks > 0 else 0.0
        
        avg_energy_cost = np.mean([t["energy_cost"] for t in successful_tasks]) if successful_tasks else 0.0
        avg_carbon_emission = np.mean([t["carbon_emission"] for t in successful_tasks]) if successful_tasks else 0.0
        avg_reliability = np.mean([t["reliability"] for t in successful_tasks]) if successful_tasks else 0.0
        
        budget_exceeded_tasks = [t for t in successful_tasks if t["budget_exceeded"]]
        budget_exceed_rate = len(budget_exceeded_tasks) / len(successful_tasks) if successful_tasks else 0.0
        
        return {
            "total_tasks": total_tasks,
            "success_rate": success_rate,
            "avg_energy_cost": avg_energy_cost,
            "avg_carbon_emission": avg_carbon_emission,
            "avg_reliability": avg_reliability,
            "budget_exceed_rate": budget_exceed_rate,
            "pareto_solutions": len(self.pareto_front)
        }

    def plot_results(self, metrics_history: Dict) -> None:
        """可视化调度结果"""
        # 解决负号显示问题
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        axes[0, 0].plot(metrics_history["episode"], metrics_history["total_carbon_emission"],
                        marker='o', linewidth=2, color='#2E86AB')
        axes[0, 0].set_title('Episode总碳排放趋势', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Episode')
        axes[0, 0].set_ylabel('总碳排放（kg）')
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].plot(metrics_history["episode"], metrics_history["budget_exceed_rate"],
                        marker='s', linewidth=2, color='#A23B72')
        axes[0, 1].set_title('Episode预算超出率', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Episode')
        axes[0, 1].set_ylabel('超出率')
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].plot(metrics_history["episode"], metrics_history["avg_energy_cost"],
                        marker='^', linewidth=2, color='#F18F01')
        axes[1, 0].set_title('Episode平均能源成本', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Episode')
        axes[1, 0].set_ylabel('平均能源成本（元）')
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].plot(metrics_history["episode"], metrics_history["avg_reliability"],
                        marker='d', linewidth=2, color='#C73E1D')
        axes[1, 1].set_title('Episode平均任务可靠性', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Episode')
        axes[1, 1].set_ylabel('平均可靠性')
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("task_scheduling_results.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("Result plot saved to task_scheduling_results.png")


# -------------------------- 5. 主程序：系统初始化与运行 --------------------------
if __name__ == "__main__":
    
    """主程序：初始化能源系统环境、任务生成器和多智能体任务调度器"""
    
    # 1. 初始化能源系统环境
    env = EnergySystemEnvironment(generator_num=1, storage_num=2, load_num=2)
    print(f"能源系统环境初始化完成，共{env.node_count}个节点:")
    for node in env.nodes:
        if node['type'] == 2:  # 负荷节点
            print(f"节点 {node['node_id']}: {env.component_types[node['type']]} | "
                  f"需求: {node['demand']:.0f} kW | "
                  f"剩余: {node['remaining_demand']:.0f} kW")
        else:
            print(f"节点 {node['node_id']}: {env.component_types[node['type']]} | "
                  f"容量: {node['capacity']:.0f} kW | "
                  f"剩余: {node['remaining_capacity']:.0f} kW")

    # 2. 初始化任务生成器
    task_generator = TaskGenerator(task_types=["excavation", "transport", "detection", "maintenance"])
    print(f"任务生成器初始化完成，支持{len(task_generator.task_types)}种任务类型")

    # 3. 初始化多智能体任务调度器（启用分布式GRPO训练）
    scheduler = MultiAgentTaskScheduler(
        env=env, 
        task_generator=task_generator,
        distributed_training=True,  # 启用分布式训练
        num_processes=4,            # 使用4个进程
        training_interval=5,       # 每5个任务训练一次
        sync_interval=20            # 每20个任务同步一次参数
    )
    print(f"多智能体调度器初始化完成，包含{len(scheduler.machine_agents)}个智能体")
    print("分布式GRPO训练已启用，使用4个进程进行并行训练")

    # 4. 运行仿真
    print("\n开始分布式GRPO训练仿真...")
    scheduler.run_simulation(episodes=50, tasks_per_episode=20)

    # 5. 输出最终统计信息
    task_df = pd.DataFrame(scheduler.task_history)
    final_stats = {
        "总任务数": len(task_df),
        "平均能源成本": task_df["energy_cost"].mean(),
        "平均可靠性": task_df["reliability"].mean(),
        "总碳排放": task_df["carbon_emission"].sum(),
        "预算超出率": task_df["budget_exceeded"].mean(),
        "Pareto解数量": len(scheduler.pareto_front)
    }
    print("\n最终调度统计信息:")
    for key, value in final_stats.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
    
    # 6. 输出训练统计信息
    if hasattr(scheduler, 'training_step'):
        print(f"\n训练统计:")
        print(f"总训练步数: {scheduler.training_step}")
        print(f"参数同步次数: {scheduler.training_step // scheduler.sync_interval}")
        print(f"检查点保存: grpo_final_checkpoint.pth")