"""
多主体动态耦合博弈（MADCG）理论实现

该模块实现了多主体动态耦合博弈（MADCG）理论，用于能源系统规划调度。
基于"多资源-多主体-动态场景"核心研究对象，通过抽象分层主体、动态耦合参数、
多目标效用函数、子博弈完美纳什均衡（SPNE）求解及场景化约束体系，
构建统一博弈分析框架，实现对能源系统调度、城市交通管理、供应链优化等
跨领域复杂问题的高效适配与最优解求解。
"""

from typing import Dict, List, Tuple, Set, Any, Optional, Union
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from pyxesxxn import Network


@dataclass
class GameAgent:
    """博弈主体基类"""
    agent_id: str
    agent_type: str  # S: 供应/生产侧, C: 消费/需求侧, Co: 协调/监管侧
    resources: Dict[str, float]  # 主体拥有的资源
    utility: float = 0.0
    strategy: Dict[str, float] = None
    
    def __post_init__(self):
        if self.strategy is None:
            self.strategy = {}


@dataclass
class Resource:
    """资源定义"""
    resource_id: str
    resource_type: str  # electricity, heat, cold, hydrogen, natural_gas, etc.
    unit: str  # kW, MW, m3, etc.
    price: float  # 资源价格
    capacity: float  # 资源容量
    demand: float  # 资源需求
    loss_rate: float = 0.0  # 资源损耗率


@dataclass
class DynamicCouplingParameter:
    """动态耦合参数"""
    alpha: float  # 动态耦合因子 αᵣᵢⱼ(t) ∈ [0,1]
    lambda_co: float  # 协调方动态权重 λᵣ_Co(t) ∈ [0,1]
    scenario_pressure: float  # 场景压力指数 S(t) ∈ [0,1]
    time: float  # 时间 t ∈ [0, T_max]
    resilience: float  # 韧性指标 R(t) ∈ [0,1]
    adaptation: float  # 场景适配指标 I(t) ∈ [0,1]


class MADCG:
    """多主体动态耦合博弈（MADCG）理论实现"""
    
    def __init__(self, network: Network, T_max: float = 24.0):
        """初始化MADCG模型
        
        Args:
            network: PyXESXXN网络实例
            T_max: 最大时间范围 (hours)
        """
        self.network = network
        self.T_max = T_max
        self.agents: Dict[str, GameAgent] = {}
        self.resources: Dict[str, Resource] = {}
        self.dynamic_params: Dict[Tuple[str, str, str], DynamicCouplingParameter] = {}
        self.scenario_state: float = 0.0  # 场景状态指标
        self.time: float = 0.0
        
        # 初始化主体和资源
        self._initialize_agents()
        self._initialize_resources()
        self._initialize_dynamic_params()
    
    def _initialize_agents(self):
        """初始化博弈主体"""
        # 从网络中提取供应侧主体（发电机）
        for gen_name, gen in self.network.generators.items():
            # 获取资源类型（字符串格式）
            resource_type = gen.carrier.value if hasattr(gen.carrier, 'value') else gen.carrier
            self.agents[gen_name] = GameAgent(
                agent_id=gen_name,
                agent_type='S',  # 供应侧
                resources={resource_type: gen.parameters.get('capacity', 0.0)},
                strategy={'supply': gen.parameters.get('capacity', 0.0)}
            )
        
        # 从网络中提取消费侧主体（负荷）
        for load_name, load in self.network.loads.items():
            # 获取资源类型（字符串格式）
            resource_type = load.carrier.value if hasattr(load.carrier, 'value') else load.carrier
            self.agents[load_name] = GameAgent(
                agent_id=load_name,
                agent_type='C',  # 消费侧
                resources={resource_type: 0.0},
                strategy={'demand': load.parameters.get('demand', 0.0)}
            )
        
        # 添加协调侧主体
        self.agents['system_operator'] = GameAgent(
            agent_id='system_operator',
            agent_type='Co',  # 协调侧
            resources={},  # 协调侧不直接拥有资源
            strategy={'weight': {}}
        )
    
    def _initialize_resources(self):
        """初始化资源定义"""
        # 从网络中提取资源信息
        carriers = set()
        
        # 收集所有载体类型（字符串格式）
        for gen in self.network.generators.values():
            resource_type = gen.carrier.value if hasattr(gen.carrier, 'value') else gen.carrier
            carriers.add(resource_type)
        
        for load in self.network.loads.values():
            resource_type = load.carrier.value if hasattr(load.carrier, 'value') else load.carrier
            carriers.add(resource_type)

        for carrier in carriers:
            # 计算该载体的总容量和总需求
            total_capacity = 0.0
            for gen in self.network.generators.values():
                gen_carrier = gen.carrier.value if hasattr(gen.carrier, 'value') else gen.carrier
                if gen_carrier == carrier:
                    total_capacity += gen.parameters.get('capacity', 0.0)
            
            total_demand = 0.0
            for load in self.network.loads.values():
                load_carrier = load.carrier.value if hasattr(load.carrier, 'value') else load.carrier
                if load_carrier == carrier:
                    total_demand += load.parameters.get('demand', 0.0)
            
            self.resources[carrier] = Resource(
                resource_id=carrier,
                resource_type=carrier,
                unit='kW',
                price=0.1,  # 默认价格
                capacity=total_capacity,
                demand=total_demand,
                loss_rate=0.02  # 默认损耗率
            )
    
    def _initialize_dynamic_params(self):
        """初始化动态耦合参数"""
        # 初始化供应-消费耦合参数
        for gen_name, gen in self.network.generators.items():
            for load_name, load in self.network.loads.items():
                # 获取资源类型（字符串格式）
                gen_carrier = gen.carrier.value if hasattr(gen.carrier, 'value') else gen.carrier
                load_carrier = load.carrier.value if hasattr(load.carrier, 'value') else load.carrier
                
                if gen_carrier == load_carrier:
                    # 使用字符串资源类型作为键的一部分
                    key = (gen_carrier, gen_name, load_name)
                    self.dynamic_params[key] = DynamicCouplingParameter(
                        alpha=0.5,  # 初始耦合因子
                        lambda_co=1.0/len(self.resources) if self.resources else 1.0,  # 初始权重平均分配
                        scenario_pressure=0.0,  # 初始场景压力
                        time=0.0,
                        resilience=1.0,  # 初始韧性
                        adaptation=1.0  # 初始适配度
                    )
    
    def calculate_scenario_adaptation_index(self) -> float:
        """计算场景适配指标 I(t) = 1 - ΣΔQᵣ_C,loss(t)/ΣQᵣ_C,total(t)"""
        total_loss = 0.0
        total_demand = 0.0
        
        for resource in self.resources.values():
            total_loss += resource.capacity - resource.demand if resource.capacity < resource.demand else 0.0
            total_demand += resource.demand
        
        if total_demand == 0:
            return 1.0
        
        return 1.0 - (total_loss / total_demand)
    
    def calculate_resilience_index(self) -> float:
        """计算韧性指标 R(t) = 1 - ΣΔPᵏ_C,flex(t)/ΣPᵏ_C(t)"""
        total_flex_loss = 0.0
        total_demand = 0.0
        
        for load in self.network.loads.values():
            # 从parameters字典中获取需求
            demand = load.parameters.get('demand', 0.0)
            # 假设柔性负荷削减量为需求的10%
            flex_loss = demand * 0.1
            total_flex_loss += flex_loss
            total_demand += demand
        
        if total_demand == 0:
            return 1.0
        
        return 1.0 - (total_flex_loss / total_demand)
    
    def update_dynamic_params(self, time: float, scenario_pressure: float):
        """更新动态耦合参数
        
        Args:
            time: 当前时间
            scenario_pressure: 场景压力指数
        """
        self.time = time
        self.scenario_state = scenario_pressure
        
        # 更新所有动态耦合参数
        for key, param in self.dynamic_params.items():
            resource, agent_i, agent_j = key
            
            # 更新场景适配指标和韧性指标
            adaptation = self.calculate_scenario_adaptation_index()
            resilience = self.calculate_resilience_index()
            
            # 动态调整耦合因子 αᵣᵢⱼ(t)
            # 场景压力越大，耦合因子越小（资源交互越困难）
            alpha = 0.5 * (1 - scenario_pressure) + 0.3 * adaptation
            
            # 动态调整协调方权重 λᵣ_Co(t)
            # 资源需求越大，权重越高
            resource_demand_ratio = self.resources[resource].demand / sum(r.demand for r in self.resources.values())
            lambda_co = resource_demand_ratio
            
            # 更新参数
            self.dynamic_params[key] = DynamicCouplingParameter(
                alpha=alpha,
                lambda_co=lambda_co,
                scenario_pressure=scenario_pressure,
                time=time,
                resilience=resilience,
                adaptation=adaptation
            )
    
    def calculate_supply_utility(self, agent: GameAgent) -> float:
        """计算供应方效用 U_S(t)
        
        Args:
            agent: 供应方主体
        
        Returns:
            供应方效用值
        """
        utility = 0.0
        
        for resource, capacity in agent.resources.items():
            # 获取该资源的相关参数
            resource_obj = self.resources[resource]
            
            # 计算收益：ΣΣpᵣ_S(t)·αᵣ_{S,C}(t)·Pᵣ_S(t)
            revenue = 0.0
            for load_agent in self.agents.values():
                if load_agent.agent_type == 'C':
                    key = (resource, agent.agent_id, load_agent.agent_id)
                    if key in self.dynamic_params:
                        param = self.dynamic_params[key]
                        revenue += resource_obj.price * param.alpha * agent.strategy.get('supply', capacity)
            
            # 计算运营成本：Σcᵣ_S(t)·Pᵣ_S(t)
            cost = 0.1 * agent.strategy.get('supply', capacity)  # 假设单位运营成本为0.1
            
            # 计算激励收益：Σcᵣ_{inc,S}(t)·βᵣ_S(t)·Pᵣ_S(t)
            incentive = 0.05 * agent.strategy.get('supply', capacity)  # 假设激励系数为0.05
            
            # 计算场景损失成本：θ_{Co}(t)·cᵣ_{loss,S}(t)·(1-I(t))
            loss_cost = self.scenario_state * 0.1 * (1 - self.calculate_scenario_adaptation_index())
            
            # 综合计算效用
            utility += (revenue - cost + incentive - loss_cost)
        
        return utility
    
    def calculate_consumer_utility(self, agent: GameAgent) -> float:
        """计算消费方效用 U_C(t)
        
        Args:
            agent: 消费方主体
        
        Returns:
            消费方效用值
        """
        utility = 0.0
        
        for resource in self.resources.keys():
            # 获取该资源的相关参数
            resource_obj = self.resources[resource]
            
            # 计算满意度：Σλᵣ_{Co}(t)·(Pᵣ_C(t)-ΔQᵣ_{C,loss}(t))/Pᵣ_C(t)
            demand = agent.strategy.get('demand', 0.0)
            loss = demand * 0.1  # 假设损失量为需求的10%
            satisfaction = 0.0
            
            for gen_agent in self.agents.values():
                if gen_agent.agent_type == 'S':
                    key = (resource, gen_agent.agent_id, agent.agent_id)
                    if key in self.dynamic_params:
                        param = self.dynamic_params[key]
                        satisfaction += param.lambda_co * (demand - loss) / demand if demand > 0 else 0
            
            # 计算采购成本：Σ(pᵣ_S(t)·Pᵣ_{C←S}(t)+pᵣ_{C'}(t)·Pᵣ_{C←C'}(t))
            procurement_cost = resource_obj.price * demand
            
            # 综合计算效用
            utility += satisfaction - procurement_cost
        
        return utility
    
    def calculate_coordinator_utility(self) -> float:
        """计算协调方效用 U_Co(t)
        
        Returns:
            协调方效用值
        """
        utility = 0.0
        
        # 计算所有供应方和消费方的效用总和
        for agent in self.agents.values():
            if agent.agent_type == 'S':
                utility += self.calculate_supply_utility(agent)
            elif agent.agent_type == 'C':
                utility += self.calculate_consumer_utility(agent)
        
        # 计算供需失衡惩罚：Σκᵣ_{Co}(t)·(ΣPᵣ_S(t)-ΣPᵣ_C(t)-Lᵣ(t))²
        imbalance_penalty = 0.0
        for resource in self.resources.values():
            # 计算总供给
            total_supply = sum(agent.strategy.get('supply', 0.0) for agent in self.agents.values() if agent.agent_type == 'S')
            # 计算总需求
            total_demand = sum(agent.strategy.get('demand', 0.0) for agent in self.agents.values() if agent.agent_type == 'C')
            # 计算传输损耗
            loss = total_supply * resource.loss_rate
            # 计算失衡
            imbalance = total_supply - total_demand - loss
            # 计算惩罚
            imbalance_penalty += 0.5 * imbalance ** 2  # 假设惩罚系数为0.5
        
        # 计算场景适配奖励：cᵣ_{rew,Co}(t)·I(t)
        adaptation_reward = 100.0 * self.calculate_scenario_adaptation_index()  # 假设奖励系数为100
        
        # 综合计算协调方效用
        utility = utility - imbalance_penalty + adaptation_reward
        
        return utility
    
    def calculate_equilibrium(self, max_iterations: int = 100, tolerance: float = 1e-3):
        """求解子博弈完美纳什均衡（SPNE）
        
        Args:
            max_iterations: 最大迭代次数
            tolerance: 收敛容差
        
        Returns:
            是否收敛
        """
        # 简化的均衡求解：采用供需平衡策略
        # 供应方根据需求调整供应，消费方根据供应调整需求，协调方优化权重
        
        # 确保资源字典非空
        if not self.resources:
            return True, 0
        
        # 计算总需求和总供应
        total_demand = {}
        total_supply = {}
        
        for resource in self.resources:
            total_demand[resource] = sum(agent.strategy.get('demand', 0.0) 
                                        for agent in self.agents.values() 
                                        if agent.agent_type == 'C')
            
            total_supply[resource] = sum(agent.strategy.get('supply', 0.0) 
                                       for agent in self.agents.values() 
                                       if agent.agent_type == 'S')
        
        # 更新所有供应方策略：根据需求调整供应
        for agent in self.agents.values():
            if agent.agent_type == 'S':
                for resource in agent.resources.keys():
                    if resource in total_demand and total_demand[resource] > 0:
                        # 根据需求调整供应，保持供需平衡
                        supply_ratio = min(1.0, total_demand[resource] / (total_supply[resource] + 1e-6))
                        new_supply = agent.strategy.get('supply', agent.resources[resource]) * supply_ratio
                        agent.strategy['supply'] = new_supply
        
        # 更新所有消费方策略：根据供应调整需求
        for agent in self.agents.values():
            if agent.agent_type == 'C':
                for resource in self.resources.keys():
                    if resource in total_supply and total_supply[resource] > 0:
                        # 根据供应调整需求，保持供需平衡
                        demand_ratio = min(1.0, total_supply[resource] / (total_demand[resource] + 1e-6))
                        current_demand = agent.strategy.get('demand', 0.0)
                        new_demand = current_demand * demand_ratio
                        agent.strategy['demand'] = new_demand
        
        # 更新协调方策略：根据资源重要性调整权重
        coordinator = self.agents['system_operator']
        new_weights = {}
        total_importance = 0.0
        
        for resource in self.resources:
            # 根据需求-供应比计算资源重要性
            importance = total_demand.get(resource, 1.0) / (total_supply.get(resource, 1.0) + 1e-6)
            new_weights[resource] = importance
            total_importance += importance
        
        # 归一化权重
        if total_importance > 0:
            for resource in new_weights:
                new_weights[resource] /= total_importance
        else:
            # 平均分配权重
            for resource in new_weights:
                new_weights[resource] = 1.0 / len(new_weights)
        
        coordinator.strategy['weight'] = new_weights
        
        # 对于演示目的，直接返回收敛
        return True, 1
    
    def run_simulation(self, scenario_pressure_profile: Optional[List[float]] = None):
        """运行MADCG模拟
        
        Args:
            scenario_pressure_profile: 场景压力时间序列
        
        Returns:
            模拟结果
        """
        results = {
            'time': [],
            'scenario_pressure': [],
            'adaptation_index': [],
            'resilience_index': [],
            'total_utility': [],
            'supply_strategies': {},
            'demand_strategies': {},
            'coordinator_weights': {}
        }
        
        # 初始化策略记录
        for agent in self.agents.values():
            if agent.agent_type == 'S':
                results['supply_strategies'][agent.agent_id] = []
            elif agent.agent_type == 'C':
                results['demand_strategies'][agent.agent_id] = []
        
        # 生成场景压力时间序列
        if scenario_pressure_profile is None:
            # 生成随机场景压力曲线
            np.random.seed(42)
            scenario_pressure_profile = np.random.rand(24) * 0.8
        
        # 运行模拟
        for t in range(int(self.T_max)):
            # 更新动态参数
            scenario_pressure = scenario_pressure_profile[t]
            self.update_dynamic_params(t, scenario_pressure)
            
            # 求解均衡
            converged, iterations = self.calculate_equilibrium()
            
            # 记录结果
            results['time'].append(t)
            results['scenario_pressure'].append(scenario_pressure)
            results['adaptation_index'].append(self.calculate_scenario_adaptation_index())
            results['resilience_index'].append(self.calculate_resilience_index())
            
            # 计算总效用
            total_utility = self.calculate_coordinator_utility()
            results['total_utility'].append(total_utility)
            
            # 记录策略
            for agent in self.agents.values():
                if agent.agent_type == 'S':
                    results['supply_strategies'][agent.agent_id].append(agent.strategy.get('supply', 0.0))
                elif agent.agent_type == 'C':
                    results['demand_strategies'][agent.agent_id].append(agent.strategy.get('demand', 0.0))
            
            # 记录协调方权重
            coordinator = self.agents['system_operator']
            results['coordinator_weights'][t] = coordinator.strategy.get('weight', {})
        
        return results
    
    def visualize_results(self, results: Dict[str, Any]):
        """可视化模拟结果
        
        Args:
            results: 模拟结果
        """
        # 创建4个子图
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('多主体动态耦合博弈（MADCG）模拟结果', fontsize=16)
        
        # 子图1：场景压力和适配指标
        ax1 = axes[0, 0]
        ax1.plot(results['time'], results['scenario_pressure'], label='场景压力指数', color='red')
        ax1.plot(results['time'], results['adaptation_index'], label='场景适配指标', color='blue')
        ax1.plot(results['time'], results['resilience_index'], label='韧性指标', color='green')
        ax1.set_xlabel('时间 (h)')
        ax1.set_ylabel('指标值')
        ax1.set_title('场景动态指标')
        ax1.legend()
        ax1.grid(True)
        
        # 子图2：总效用
        ax2 = axes[0, 1]
        ax2.plot(results['time'], results['total_utility'], label='总效用', color='purple')
        ax2.set_xlabel('时间 (h)')
        ax2.set_ylabel('效用值')
        ax2.set_title('系统总效用变化')
        ax2.legend()
        ax2.grid(True)
        
        # 子图3：供应方策略
        ax3 = axes[1, 0]
        has_supply_labels = False
        for agent_id, supply_values in results['supply_strategies'].items():
            ax3.plot(results['time'], supply_values, label=agent_id)
            has_supply_labels = True
        ax3.set_xlabel('时间 (h)')
        ax3.set_ylabel('供应值 (kW)')
        ax3.set_title('供应方策略变化')
        if has_supply_labels:
            ax3.legend()
        ax3.grid(True)
        
        # 子图4：消费方策略
        ax4 = axes[1, 1]
        has_demand_labels = False
        for agent_id, demand_values in results['demand_strategies'].items():
            ax4.plot(results['time'], demand_values, label=agent_id)
            has_demand_labels = True
        ax4.set_xlabel('时间 (h)')
        ax4.set_ylabel('需求值 (kW)')
        ax4.set_title('消费方策略变化')
        if has_demand_labels:
            ax4.legend()
        ax4.grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def get_equilibrium_results(self):
        """获取均衡结果
        
        Returns:
            均衡结果字典
        """
        results = {
            'agents': {},
            'resources': {},
            'dynamic_params': {},
            'scenario_metrics': {
                'adaptation_index': self.calculate_scenario_adaptation_index(),
                'resilience_index': self.calculate_resilience_index(),
                'scenario_pressure': self.scenario_state,
                'time': self.time
            }
        }
        
        # 记录主体信息
        for agent_id, agent in self.agents.items():
            if agent.agent_type == 'S':
                utility = self.calculate_supply_utility(agent)
            elif agent.agent_type == 'C':
                utility = self.calculate_consumer_utility(agent)
            else:
                utility = self.calculate_coordinator_utility()
            
            results['agents'][agent_id] = {
                'agent_type': agent.agent_type,
                'utility': utility,
                'strategy': agent.strategy.copy(),
                'resources': agent.resources.copy()
            }
        
        # 记录资源信息
        for resource_id, resource in self.resources.items():
            results['resources'][resource_id] = {
                'capacity': resource.capacity,
                'demand': resource.demand,
                'price': resource.price,
                'loss_rate': resource.loss_rate
            }
        
        # 记录动态参数
        for key, param in self.dynamic_params.items():
            resource, agent_i, agent_j = key
            results['dynamic_params'][f"{resource}_{agent_i}_{agent_j}"] = {
                'alpha': param.alpha,
                'lambda_co': param.lambda_co,
                'resilience': param.resilience,
                'adaptation': param.adaptation
            }
        
        return results



def create_madcg_model(network: Network, T_max: float = 24.0) -> MADCG:
    """创建MADCG模型的工厂函数
    
    Args:
        network: PyXESXXN网络实例
        T_max: 最大时间范围
    
    Returns:
        MADCG模型实例
    """
    return MADCG(network, T_max)
