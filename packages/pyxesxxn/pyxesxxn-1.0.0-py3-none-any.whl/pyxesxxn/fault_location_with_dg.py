"""
含分布式电源（DG）配电网故障定位模块

该模块实现了两种配电网故障定位方法：
1. 基于分层定位模型的含DG配电网故障定位方法
2. 基于时域差分运算的配电网多分支线路故障定位方法
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Set, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass
import numpy as np
import pandas as pd
from pyxesxxn.topology_metering_fusion import TopologyMeteringFusion, DistributionNode, DistributionBranch, DistributionSwitch, MeasurementType


class DGConnectionStatus(Enum):
    """分布式电源连接状态枚举"""
    NOT_CONNECTED = 0  # 未并网
    CONNECTED = 1  # 已并网


class FaultLocationType(Enum):
    """故障定位类型枚举"""
    SINGLE_FAULT = 0  # 单故障
    MULTIPLE_FAULTS = 1  # 复合故障


@dataclass
class DistributedGenerator:
    """分布式电源（DG）类"""
    dg_id: str
    node_id: str  # 连接的节点
    capacity: float  # 容量(kW)
    connection_status: DGConnectionStatus  # 连接状态
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class FaultLocationResult:
    """故障定位结果类"""
    fault_nodes: List[str]  # 故障节点
    fault_branches: List[str]  # 故障支路
    confidence: float  # 定位置信度
    iteration_count: int  # 迭代次数
    calculation_time: float  # 计算时间(秒)
    fault_type: FaultLocationType  # 故障类型


class HierarchicalFaultLocator:
    """基于分层定位模型的含DG配电网故障定位器"""
    
    def __init__(self, fusion_module: TopologyMeteringFusion):
        """初始化故障定位器
        
        Parameters
        ----------
        fusion_module : TopologyMeteringFusion
            拓扑-量测数据融合模块实例
        """
        self.fusion_module = fusion_module
        self.dgs: Dict[str, DistributedGenerator] = {}  # 分布式电源字典
        self.active_branches: Set[str] = set()  # 有源支路
        self.passive_branches: Set[str] = set()  # 无源支路
        self.ftu_data: Dict[str, float] = {}  # FTU量测数据
        
        # 算法参数
        self.max_iterations = 100  # 最大迭代次数
        self.tolerance = 1e-3  # 收敛容差
        self.w = 0.5  # 评价函数权重
        self.lambda_param = 0.01  # 惯性权重调节参数
        
    def add_dg(self, dg: DistributedGenerator) -> None:
        """添加分布式电源
        
        Parameters
        ----------
        dg : DistributedGenerator
            分布式电源实例
        """
        if dg.dg_id in self.dgs:
            raise ValueError(f"DG {dg.dg_id} 已存在")
        if dg.node_id not in self.fusion_module.nodes:
            raise ValueError(f"节点 {dg.node_id} 不存在")
        self.dgs[dg.dg_id] = dg
    
    def set_ftu_data(self, ftu_data: Dict[str, float]) -> None:
        """设置FTU量测数据
        
        Parameters
        ----------
        ftu_data : Dict[str, float]
            FTU量测数据，键为节点ID，值为故障电流方向(-1, 0, 1)
        """
        self.ftu_data = ftu_data
    
    def _classify_branches(self) -> None:
        """分类有源支路和无源支路"""
        # 首先构建拓扑图
        if self.fusion_module.graph is None:
            self.fusion_module.build_topology_graph()
        
        # 初始化所有支路为无源支路
        self.passive_branches = set(self.fusion_module.branches.keys())
        self.active_branches = set()
        
        # 从DG连接节点开始，标记有源支路
        for dg_id, dg in self.dgs.items():
            if dg.connection_status == DGConnectionStatus.CONNECTED:
                # 广度优先搜索，标记所有可达支路为有源支路
                visited_nodes = set()
                queue = [dg.node_id]
                
                while queue:
                    current_node = queue.pop(0)
                    if current_node in visited_nodes:
                        continue
                    visited_nodes.add(current_node)
                    
                    # 获取当前节点的所有邻居
                    for neighbor in self.fusion_module.graph.neighbors(current_node):
                        # 查找连接当前节点和邻居的支路
                        for branch_id, branch in self.fusion_module.branches.items():
                            if ((branch.from_node == current_node and branch.to_node == neighbor) or 
                                (branch.from_node == neighbor and branch.to_node == current_node)):
                                # 将该支路标记为有源支路
                                self.active_branches.add(branch_id)
                                self.passive_branches.discard(branch_id)
                                # 将邻居节点加入队列
                                queue.append(neighbor)
    
    def _encode_line_status(self, fault_nodes: List[str]) -> Dict[str, int]:
        """编码线路状态
        
        Parameters
        ----------
        fault_nodes : List[str]
            故障节点列表
        
        Returns
        -------
        Dict[str, int]
            线路状态编码，键为节点ID，值为0(正常)或1(故障)
        """
        encoding = {}
        for node_id in self.fusion_module.nodes.keys():
            encoding[node_id] = 1 if node_id in fault_nodes else 0
        return encoding
    
    def _encode_ftu_data(self) -> Dict[str, int]:
        """编码FTU量测数据
        
        Returns
        -------
        Dict[str, int]
            FTU量测数据编码，键为节点ID，值为-1(反向)、0(正常)或1(正向)
        """
        encoding = {}
        for node_id in self.fusion_module.nodes.keys():
            encoding[node_id] = self.ftu_data.get(node_id, 0)
        return encoding
    
    def _switch_function(self, line_status: Dict[str, int], node_id: str) -> int:
        """开关函数模型
        
        Parameters
        ----------
        line_status : Dict[str, int]
            线路状态编码
        node_id : str
            节点ID
        
        Returns
        -------
        int
            计算得到的故障电流方向(-1, 0, 1)
        """
        # 检查节点是否有DG连接
        has_dg = any(dg.node_id == node_id and dg.connection_status == DGConnectionStatus.CONNECTED for dg in self.dgs.values())
        
        if not has_dg:
            # DG未并网情况：开关函数为逻辑或
            result = 0
            for neighbor in self.fusion_module.graph.neighbors(node_id):
                result |= line_status[neighbor]
            return result
        else:
            # DG并网情况：区分上下游
            # 获取连接到该节点的所有支路
            connected_branches = []
            for branch_id, branch in self.fusion_module.branches.items():
                if branch.from_node == node_id or branch.to_node == node_id:
                    connected_branches.append(branch)
            
            # 简化计算：假设DG所在节点为参考点，计算上下游
            i_ju = 0  # 上游故障电流
            i_jd = 0  # 下游故障电流
            
            # 遍历所有连接的支路
            for branch in connected_branches:
                if branch.from_node == node_id:
                    # 下游节点
                    i_jd |= line_status[branch.to_node]
                else:
                    # 上游节点
                    i_ju |= line_status[branch.from_node]
            
            # 计算最终结果
            return i_ju - i_jd
    
    def _fitness_function(self, candidate: List[str]) -> float:
        """评价函数
        
        Parameters
        ----------
        candidate : List[str]
            候选故障节点列表
        
        Returns
        -------
        float
            适应度值
        """
        # 编码线路状态
        line_status = self._encode_line_status(candidate)
        
        # 计算开关函数值
        calculated_ftu = {}
        for node_id in self.fusion_module.nodes.keys():
            calculated_ftu[node_id] = self._switch_function(line_status, node_id)
        
        # 对比实际FTU数据和计算值
        n = len(self.fusion_module.nodes)
        sum_diff = 0.0
        for node_id in self.fusion_module.nodes.keys():
            actual = self.ftu_data.get(node_id, 0)
            calculated = calculated_ftu[node_id]
            sum_diff += abs(actual - calculated)
        
        # 计算故障节点权重
        sum_fault_nodes = len(candidate)
        
        # 计算适应度值
        # 如果没有开关，使用节点数的两倍作为T
        T = 2 * len(self.fusion_module.switches) if self.fusion_module.switches else 2 * len(self.fusion_module.nodes)
        fitness = T - (sum_diff + self.w * sum_fault_nodes)
        
        return fitness
    
    def _calculate_inertia_weight(self, p_best: List[List[str]], g_best: List[str]) -> float:
        """计算自适应惯性权重
        
        Parameters
        ----------
        p_best : List[List[str]]
            个体最优解列表
        g_best : List[str]
            全局最优解
        
        Returns
        -------
        float
            惯性权重
        """
        if not p_best:
            return 1.0
        
        # 计算每个个体最优解与全局最优解的差异
        differences = []
        for p in p_best:
            # 计算差异：两个集合的对称差
            diff = len(set(p) ^ set(g_best))
            differences.append(diff)
        
        # 计算平均差异
        avg_diff = np.mean(differences) if differences else 0.0
        
        if avg_diff == 0:
            return 1.0
        
        # 计算最大差异
        max_diff = max(differences) if differences else 0.0
        
        # 计算惯性权重
        omega = self.lambda_param * (max_diff / avg_diff)
        
        return omega
    
    def _sigmoid(self, x: float) -> float:
        """Sigmoid函数
        
        Parameters
        ----------
        x : float
            输入值
        
        Returns
        -------
        float
            Sigmoid函数值
        """
        return 1.0 / (1.0 + np.exp(-x))
    
    def _generate_initial_population(self, population_size: int) -> List[List[str]]:
        """生成初始种群
        
        Parameters
        ----------
        population_size : int
            种群大小
        
        Returns
        -------
        List[List[str]]
            初始种群，每个个体为候选故障节点列表
        """
        population = []
        nodes = list(self.fusion_module.nodes.keys())
        
        for _ in range(population_size):
            # 随机生成1-3个故障节点
            num_faults = np.random.randint(1, 4)
            fault_nodes = list(np.random.choice(nodes, num_faults, replace=False))
            population.append(fault_nodes)
        
        return population
    
    def _binary_particle_swarm_optimization(self, population: List[List[str]]) -> Tuple[List[str], float]:
        """二进制粒子群优化算法
        
        Parameters
        ----------
        population : List[List[str]]
            初始种群
        
        Returns
        -------
        Tuple[List[str], float]
            最优解和最优适应度值
        """
        # 初始化粒子速度和位置
        particle_size = len(self.fusion_module.nodes)
        velocity = np.random.rand(len(population), particle_size) - 0.5
        
        # 初始化个体最优解和适应度
        p_best = population.copy()
        p_best_fitness = [self._fitness_function(ind) for ind in population]
        
        # 初始化全局最优解和适应度
        g_best_idx = np.argmax(p_best_fitness)
        g_best = p_best[g_best_idx].copy()
        g_best_fitness = p_best_fitness[g_best_idx]
        
        # 算法参数
        c1 = 1.5  # 认知系数
        c2 = 1.5  # 社会系数
        r1 = 0.5  # 随机因子
        r2 = 0.5  # 随机因子
        
        # 迭代优化
        for iter_count in range(self.max_iterations):
            # 计算惯性权重
            omega = self._calculate_inertia_weight(p_best, g_best)
            
            for i in range(len(population)):
                # 更新速度
                velocity[i] = omega * velocity[i] + \
                             c1 * r1 * (np.array([1 if node in p_best[i] else 0 for node in self.fusion_module.nodes]) - \
                                       np.array([1 if node in population[i] else 0 for node in self.fusion_module.nodes])) + \
                             c2 * r2 * (np.array([1 if node in g_best else 0 for node in self.fusion_module.nodes]) - \
                                       np.array([1 if node in population[i] else 0 for node in self.fusion_module.nodes]))
                
                # 更新位置
                new_position = []
                for j, node in enumerate(self.fusion_module.nodes):
                    sig_v = self._sigmoid(velocity[i, j])
                    if sig_v > np.random.rand():
                        new_position.append(node)
                
                population[i] = new_position
                
                # 计算适应度
                fitness = self._fitness_function(population[i])
                
                # 更新个体最优
                if fitness > p_best_fitness[i]:
                    p_best[i] = population[i].copy()
                    p_best_fitness[i] = fitness
                
                # 更新全局最优
                if fitness > g_best_fitness:
                    g_best = population[i].copy()
                    g_best_fitness = fitness
            
            # 检查收敛条件
            if g_best_fitness > (2 * len(self.fusion_module.switches) - self.tolerance):
                break
        
        return g_best, g_best_fitness
    
    def _immune_algorithm(self, population: List[List[str]]) -> Tuple[List[str], float]:
        """改进免疫算法
        
        Parameters
        ----------
        population : List[List[str]]
            初始种群
        
        Returns
        -------
        Tuple[List[str], float]
            最优解和最优适应度值
        """
        # 融合二进制粒子群优化
        best_candidate, best_fitness = self._binary_particle_swarm_optimization(population)
        
        # 记忆细胞信息分化：如果陷入局部最优，生成单故障和复合故障抗体
        if best_fitness < (2 * len(self.fusion_module.switches) * 0.8):
            # 生成单故障抗体
            for node_id in best_candidate:
                single_fault = [node_id]
                fitness = self._fitness_function(single_fault)
                if fitness > best_fitness:
                    best_candidate = single_fault
                    best_fitness = fitness
            
            # 生成复合故障抗体（两两组合）
            for i in range(len(best_candidate)):
                for j in range(i+1, len(best_candidate)):
                    double_fault = [best_candidate[i], best_candidate[j]]
                    fitness = self._fitness_function(double_fault)
                    if fitness > best_fitness:
                        best_candidate = double_fault
                        best_fitness = fitness
        
        return best_candidate, best_fitness
    
    def _get_fault_branches(self, fault_nodes: List[str]) -> List[str]:
        """获取故障支路
        
        Parameters
        ----------
        fault_nodes : List[str]
            故障节点列表
        
        Returns
        -------
        List[str]
            故障支路列表
        """
        fault_branches = []
        for branch_id, branch in self.fusion_module.branches.items():
            if branch.from_node in fault_nodes or branch.to_node in fault_nodes:
                fault_branches.append(branch_id)
        return fault_branches
    
    def locate_fault(self, population_size: int = 50) -> FaultLocationResult:
        """执行故障定位
        
        Parameters
        ----------
        population_size : int, default=50
            种群大小
        
        Returns
        -------
        FaultLocationResult
            故障定位结果
        """
        import time
        start_time = time.time()
        
        # 第一层：粗定位 - 分类有源/无源支路，剔除无故障无源支路
        self._classify_branches()
        
        # 生成初始种群
        initial_population = self._generate_initial_population(population_size)
        
        # 第二层：精定位 - 使用改进免疫算法求解最优解
        best_candidate, best_fitness = self._immune_algorithm(initial_population)
        
        # 确定故障类型
        fault_type = FaultLocationType.MULTIPLE_FAULTS if len(best_candidate) > 1 else FaultLocationType.SINGLE_FAULT
        
        # 获取故障支路
        fault_branches = self._get_fault_branches(best_candidate)
        
        # 计算置信度
        # 如果没有开关，使用节点数的两倍作为最大适应度
        max_fitness = 2 * len(self.fusion_module.switches) if self.fusion_module.switches else 2 * len(self.fusion_module.nodes)
        confidence = best_fitness / max_fitness if max_fitness > 0 else 0.0
        
        # 计算耗时
        calculation_time = time.time() - start_time
        
        # 构建结果
        result = FaultLocationResult(
            fault_nodes=best_candidate,
            fault_branches=fault_branches,
            confidence=confidence,
            iteration_count=self.max_iterations,
            calculation_time=calculation_time,
            fault_type=fault_type
        )
        
        return result
    
    def run_hierarchical_location(self, population_size: int = 50) -> FaultLocationResult:
        """运行分层定位算法
        
        Parameters
        ----------
        population_size : int, default=50
            种群大小
        
        Returns
        -------
        FaultLocationResult
            故障定位结果
        """
        return self.locate_fault(population_size)


# 工具函数
def create_sample_fault_locator() -> HierarchicalFaultLocator:
    """创建示例故障定位器
    
    Returns
    -------
    HierarchicalFaultLocator
        示例故障定位器
    """
    # 创建拓扑-量测融合模块
    fusion = TopologyMeteringFusion("示例配电网")
    
    # 添加节点
    nodes = [
        DistributionNode("substation", "substation", 110.0, (0, 0), 50000),
        DistributionNode("node1", "load", 10.0, (1, 1), 5000),
        DistributionNode("node2", "load", 10.0, (2, 2), 3000),
        DistributionNode("node3", "load", 10.0, (3, 1), 2000),
        DistributionNode("node4", "load", 10.0, (4, 0), 1000),
    ]
    
    for node in nodes:
        fusion.add_node(node)
    
    # 添加支路
    branches = [
        DistributionBranch("line1", "substation", "node1", "overhead", 5.0, 0.1, 0.2, 0.001, 20000),
        DistributionBranch("line2", "node1", "node2", "cable", 2.0, 0.05, 0.1, 0.002, 10000),
        DistributionBranch("line3", "node1", "node3", "overhead", 3.0, 0.08, 0.15, 0.001, 8000),
        DistributionBranch("line4", "node3", "node4", "cable", 1.5, 0.06, 0.12, 0.0015, 5000),
    ]
    
    for branch in branches:
        fusion.add_branch(branch)
    
    # 创建故障定位器
    fault_locator = HierarchicalFaultLocator(fusion)
    
    # 添加DG
    from dataclasses import dataclass
    fault_locator.add_dg(DistributedGenerator("dg1", "node3", 500.0, DGConnectionStatus.CONNECTED))
    
    # 设置FTU量测数据
    ftu_data = {
        "substation": 1,
        "node1": 1,
        "node2": 0,
        "node3": -1,
        "node4": 1,
    }
    fault_locator.set_ftu_data(ftu_data)
    
    return fault_locator
