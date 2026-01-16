"""
强对偶技术实现 - 适配分层结构规划调度模型

将专利中"针对双层鲁棒优化的强对偶应用"扩展为"面向分层结构（分布式鲁棒凸优化主问题+元启发式算法子问题）的普适性强对偶技术"，
核心逻辑是：通过强对偶理论实现"主-子问题"的解耦与线性化转化，处理非凸决策与多阶段时序约束，
同时保留元启发式算法对子问题的高效求解能力，最终形成"对偶转化-分层求解-时序协同"的完整技术框架。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any, Union
import numpy as np
from scipy.optimize import minimize
from .abstract import StochasticOptimizer, OptimizationConfig, OptimizationVariable, OptimizationConstraint


@dataclass
class DualVariables:
    """对偶变量数据结构"""
    # 功率平衡对偶变量
    lambda_t: np.ndarray  # 形状: (T,)
    # 安全约束对偶变量
    mu_t: np.ndarray      # 形状: (T,)
    # 时序协同对偶变量
    nu_t: np.ndarray      # 形状: (T,)
    # 储能时序对偶强化变量
    tau_t: np.ndarray     # 形状: (T-1,)
    
    def __init__(self, T: int):
        """初始化对偶变量
        
        参数
        ----------
        T : int
            时间阶段数
        """
        self.lambda_t = np.zeros(T)
        self.mu_t = np.zeros(T)
        self.nu_t = np.zeros(T)
        self.tau_t = np.zeros(T-1)
    
    def update(self, other: DualVariables) -> None:
        """更新对偶变量
        
        参数
        ----------
        other : DualVariables
            新的对偶变量值
        """
        self.lambda_t = other.lambda_t.copy()
        self.mu_t = other.mu_t.copy()
        self.nu_t = other.nu_t.copy()
        self.tau_t = other.tau_t.copy()
    
    def norm_diff(self, other: DualVariables) -> float:
        """计算与另一个对偶变量的范数差
        
        参数
        ----------
        other : DualVariables
            另一个对偶变量
        
        返回
        ----------
        float
            范数差
        """
        diff_lambda = np.linalg.norm(self.lambda_t - other.lambda_t)
        diff_mu = np.linalg.norm(self.mu_t - other.mu_t)
        diff_nu = np.linalg.norm(self.nu_t - other.nu_t)
        diff_tau = np.linalg.norm(self.tau_t - other.tau_t)
        return diff_lambda + diff_mu + diff_nu + diff_tau
    
    def to_array(self) -> np.ndarray:
        """转换为数组形式
        
        返回
        ----------
        np.ndarray
            扁平化的对偶变量数组
        """
        return np.concatenate([self.lambda_t, self.mu_t, self.nu_t, self.tau_t])
    
    @classmethod
    def from_array(cls, arr: np.ndarray, T: int) -> DualVariables:
        """从数组创建对偶变量
        
        参数
        ----------
        arr : np.ndarray
            扁平化的对偶变量数组
        T : int
            时间阶段数
        
        返回
        ----------
        DualVariables
            对偶变量对象
        """
        dual = cls(T)
        offset = 0
        dual.lambda_t = arr[offset:offset+T].copy()
        offset += T
        dual.mu_t = arr[offset:offset+T].copy()
        offset += T
        dual.nu_t = arr[offset:offset+T].copy()
        offset += T
        dual.tau_t = arr[offset:offset+T-1].copy()
        return dual


@dataclass
class UncertaintySet:
    """不确定性集数据结构"""
    # 基准值
    xi0_pv: np.ndarray    # 光伏基准功率: (T,)
    xi0_wt: np.ndarray    # 风电基准功率: (T,)
    xi0_load: np.ndarray  # 负荷基准值: (T,)
    # 偏差范围
    delta_pv: np.ndarray  # 光伏偏差: (T,)
    delta_wt: np.ndarray  # 风电偏差: (T,)
    delta_load: np.ndarray  # 负荷偏差: (T,)
    # 鲁棒调节系数
    gamma_t: np.ndarray   # 鲁棒调节系数: (T,)


@dataclass
class EquipmentParameters:
    """设备参数数据结构"""
    # 微型燃气轮机
    mt_max_p: np.ndarray   # 最大出力: (T,)
    mt_min_p: np.ndarray   # 最小出力: (T,)
    c_mt: np.ndarray       # 运行成本: (T,)
    c_start: float         # 启动成本
    c_shut: float          # 停机成本
    
    # 电网交互
    c_grid: np.ndarray     # 购售电成本: (T,)
    
    # 储能系统
    eta_chr: float         # 充电效率
    eta_dis: float         # 放电效率
    soc_initial: float     # 初始SOC
    soc_max: float         # 最大SOC
    soc_min: float         # 最小SOC
    
    # 设备组合0-1决策变量
    delta_t: Optional[np.ndarray] = None  # 设备运行状态: (T,)，1=运行，0=停机


class MainProblem:
    """主问题：分布式鲁棒凸优化模型"""
    
    def __init__(self, T: int, uncertainty_set: UncertaintySet, equipment_params: EquipmentParameters):
        """初始化主问题
        
        参数
        ----------
        T : int
            时间阶段数
        uncertainty_set : UncertaintySet
            不确定性集
        equipment_params : EquipmentParameters
            设备参数
        """
        self.T = T
        self.uncertainty = uncertainty_set
        self.equipment = equipment_params
    
    def dual_objective(self, dual_vars: DualVariables) -> float:
        """主问题的对偶目标函数
        
        参数
        ----------
        dual_vars : DualVariables
            对偶变量
        
        返回
        ----------
        float
            对偶目标函数值
        """
        objective = 0.0
        
        # 主问题对偶目标函数：min_{u, \lambda, \mu, \nu} sum_{t=1}^T [ \lambda_t (\xi^0_{load,t} - \xi^0_{pv,t} - \xi^0_{wt,t}) + \nu_t SOC_{t-1} + CVaR(\lambda, \mu, \nu) ]
        for t in range(self.T):
            # 功率平衡项
            lambda_term = dual_vars.lambda_t[t] * (self.uncertainty.xi0_load[t] - self.uncertainty.xi0_pv[t] - self.uncertainty.xi0_wt[t])
            
            # 储能SOC项
            soc_prev = self.equipment.soc_initial if t == 0 else 0.0  # SOC_{t-1}，这里简化处理
            nu_term = dual_vars.nu_t[t] * soc_prev
            
            objective += lambda_term + nu_term
        
        # 简化CVaR计算（实际应用中需要更复杂的实现）
        cvar_term = 0.01 * np.sum(dual_vars.lambda_t ** 2)
        objective += cvar_term
        
        return objective
    
    def dual_constraints(self, dual_vars: DualVariables) -> List[float]:
        """主问题的对偶约束
        
        参数
        ----------
        dual_vars : DualVariables
            对偶变量
        
        返回
        ----------
        List[float]
            约束违反值列表，所有值<=0表示约束满足
        """
        constraints = []
        
        for t in range(self.T):
            # 微型燃气轮机对偶约束：c_{mt} - lambda_t - mu_t R_{mt} = 0
            # 简化：假设R_{mt}=1
            constraint1 = self.equipment.c_mt[t] - dual_vars.lambda_t[t] - dual_vars.mu_t[t] - 0.0
            constraints.append(constraint1)
            constraints.append(-constraint1)  # 等式约束转化为两个不等式约束
            
            # 电网购售电对偶约束：c_{grid,t} - lambda_t - mu_t R_{grid} = 0
            # 简化：假设R_{grid}=1
            constraint2 = self.equipment.c_grid[t] - dual_vars.lambda_t[t] - dual_vars.mu_t[t] - 0.0
            constraints.append(constraint2)
            constraints.append(-constraint2)  # 等式约束转化为两个不等式约束
            
            # 储能充电对偶约束：-ν_t eta_{chr} - lambda_t <= 0
            constraint3 = -dual_vars.nu_t[t] * self.equipment.eta_chr - dual_vars.lambda_t[t]
            constraints.append(constraint3)
            
            # 储能放电对偶约束：ν_t / eta_{dis} - lambda_t <= 0
            constraint4 = dual_vars.nu_t[t] / self.equipment.eta_dis - dual_vars.lambda_t[t]
            constraints.append(constraint4)
            
            # 不确定性对偶约束：lambda_t Delta xi_{pv,t} + lambda_t Delta xi_{wt,t} - lambda_t Delta xi_{load,t} <= Gamma_t
            uncertainty_term = (dual_vars.lambda_t[t] * self.uncertainty.delta_pv[t] + 
                               dual_vars.lambda_t[t] * self.uncertainty.delta_wt[t] - 
                               dual_vars.lambda_t[t] * self.uncertainty.delta_load[t])
            constraint5 = uncertainty_term - self.uncertainty.gamma_t[t]
            constraints.append(constraint5)
        
        # 时序协同对偶强化约束：ν_t - ν_{t+1} - τ_t = 0，t=1,...,T-1
        for t in range(self.T-1):
            constraint6 = dual_vars.nu_t[t] - dual_vars.nu_t[t+1] - dual_vars.tau_t[t] - 0.0
            constraints.append(constraint6)
            constraints.append(-constraint6)  # 等式约束转化为两个不等式约束
        
        return constraints
    
    def solve_dual(self, initial_dual: DualVariables) -> DualVariables:
        """求解主问题的对偶模型
        
        参数
        ----------
        initial_dual : DualVariables
            对偶变量初始值
        
        返回
        ----------
        DualVariables
            最优对偶变量
        """
        # 定义优化问题的目标函数（转换为scipy.optimize的minimize格式）
        def objective(x):
            dual = DualVariables.from_array(x, self.T)
            return self.dual_objective(dual)
        
        # 定义约束条件
        def constraints(x):
            dual = DualVariables.from_array(x, self.T)
            return self.dual_constraints(dual)
        
        # 初始解
        x0 = initial_dual.to_array()
        
        # 定义约束类型
        cons = [{'type': 'ineq', 'fun': constraints}]
        
        # 求解优化问题
        result = minimize(objective, x0, method='SLSQP', constraints=cons)
        
        # 转换回DualVariables对象
        optimal_dual = DualVariables.from_array(result.x, self.T)
        return optimal_dual


class SubProblem:
    """子问题：元启发式算法求解的非凸设备组合模型"""
    
    def __init__(self, T: int, equipment_params: EquipmentParameters, dual_vars: DualVariables):
        """初始化子问题
        
        参数
        ----------
        T : int
            时间阶段数
        equipment_params : EquipmentParameters
            设备参数
        dual_vars : DualVariables
            主问题传递的对偶变量
        """
        self.T = T
        self.equipment = equipment_params
        self.dual_vars = dual_vars
    
    def objective(self, delta_t: np.ndarray) -> float:
        """子问题目标函数：最小化设备启停成本
        
        参数
        ----------
        delta_t : np.ndarray
            设备运行状态，1=运行，0=停机: (T,)
        
        返回
        ----------
        float
            目标函数值
        """
        objective = 0.0
        
        for t in range(self.T):
            # 设备启停成本：c_start * delta_t - c_shut * (1 - delta_t)
            start_cost = self.equipment.c_start * delta_t[t]
            shut_cost = self.equipment.c_shut * (1 - delta_t[t])
            
            # 嵌入主问题对偶变量：lambda_t P_{mt,max} delta_t
            dual_term = self.dual_vars.lambda_t[t] * self.equipment.mt_max_p[t] * delta_t[t]
            
            objective += start_cost - shut_cost + dual_term
        
        return objective
    
    def constraints(self, delta_t: np.ndarray) -> List[float]:
        """子问题约束
        
        参数
        ----------
        delta_t : np.ndarray
            设备运行状态
        
        返回
        ----------
        List[float]
            约束违反值列表，所有值<=0表示约束满足
        """
        constraints = []
        
        for t in range(self.T):
            # 设备运行状态必须是0或1（通过目标函数中的整数约束实现，这里仅做检查）
            if not (delta_t[t] in [0, 1]):
                constraints.append(abs(delta_t[t] - 0.5))  # 非整数惩罚
        
        # 启停时序约束：delta_t - delta_{t-1} <= 1 和 (1 - delta_t) - (1 - delta_{t-1}) <= 1
        # 简化：实际上这两个约束总是满足，因为delta_t是0-1变量
        for t in range(1, self.T):
            constraint1 = delta_t[t] - delta_t[t-1] - 1.0
            constraint2 = (1 - delta_t[t]) - (1 - delta_t[t-1]) - 1.0
            constraints.append(constraint1)
            constraints.append(constraint2)
        
        return constraints
    
    def solve(self, population_size: int = 50, max_iterations: int = 100) -> np.ndarray:
        """使用元启发式算法求解子问题
        
        参数
        ----------
        population_size : int, default=50
            种群大小
        max_iterations : int, default=100
            最大迭代次数
        
        返回
        ----------
        np.ndarray
            最优设备运行状态
        """
        # 使用简单的遗传算法求解
        best_delta = None
        best_fitness = float('inf')
        
        # 初始化种群
        population = []
        for _ in range(population_size):
            delta = np.random.randint(0, 2, self.T)
            fitness = self.objective(delta)
            population.append((delta, fitness))
            
            if fitness < best_fitness:
                best_fitness = fitness
                best_delta = delta.copy()
        
        # 遗传算法主循环
        for _ in range(max_iterations):
            # 选择父母
            parents = sorted(population, key=lambda x: x[1])[:population_size//2]
            
            # 交叉和变异
            new_population = []
            for i in range(0, len(parents), 2):
                if i+1 < len(parents):
                    # 单点交叉
                    cross_point = np.random.randint(1, self.T-1)
                    child1 = np.concatenate([parents[i][0][:cross_point], parents[i+1][0][cross_point:]])
                    child2 = np.concatenate([parents[i+1][0][:cross_point], parents[i][0][cross_point:]])
                    
                    # 变异
                    if np.random.rand() < 0.1:
                        mutate_point = np.random.randint(self.T)
                        child1[mutate_point] = 1 - child1[mutate_point]
                    if np.random.rand() < 0.1:
                        mutate_point = np.random.randint(self.T)
                        child2[mutate_point] = 1 - child2[mutate_point]
                    
                    # 计算适应度
                    fitness1 = self.objective(child1)
                    fitness2 = self.objective(child2)
                    
                    new_population.append((child1, fitness1))
                    new_population.append((child2, fitness2))
            
            # 合并种群并选择最优个体
            population = sorted(population + new_population, key=lambda x: x[1])[:population_size]
            
            # 更新最优解
            current_best = min(population, key=lambda x: x[1])
            if current_best[1] < best_fitness:
                best_fitness = current_best[1]
                best_delta = current_best[0].copy()
        
        return best_delta


class HierarchicalStrongDualityOptimizer:
    """分层结构规划调度模型的强对偶优化器"""
    
    def __init__(self, T: int, uncertainty_set: UncertaintySet, equipment_params: EquipmentParameters):
        """初始化强对偶优化器
        
        参数
        ----------
        T : int
            时间阶段数
        uncertainty_set : UncertaintySet
            不确定性集
        equipment_params : EquipmentParameters
            设备参数
        """
        self.T = T
        self.uncertainty = uncertainty_set
        self.equipment = equipment_params
        
        # 初始化对偶变量
        self.dual_vars = DualVariables(T)
        
        # 初始化主问题和子问题
        self.main_prob = MainProblem(T, uncertainty_set, equipment_params)
        self.sub_prob = SubProblem(T, equipment_params, self.dual_vars)
    
    def solve(self, max_iterations: int = 100, epsilon: float = 1e-3) -> Dict[str, Any]:
        """求解分层结构规划调度模型
        
        参数
        ----------
        max_iterations : int, default=100
            最大迭代次数
        epsilon : float, default=1e-3
            收敛阈值
        
        返回
        ----------
        Dict[str, Any]
            优化结果
        """
        iteration = 0
        convergence = False
        
        # 分层求解流程：对偶转化-分层求解-时序协同
        while iteration < max_iterations and not convergence:
            iteration += 1
            
            # 1. 子问题求解：元启发式算法求解非凸设备组合模型
            delta_t = self.sub_prob.solve()
            self.equipment.delta_t = delta_t
            
            # 2. 主问题求解：分布式鲁棒凸优化的对偶模型
            new_dual_vars = self.main_prob.solve_dual(self.dual_vars)
            
            # 3. 收敛判断：检查对偶变量变化
            diff = self.dual_vars.norm_diff(new_dual_vars)
            if diff <= epsilon:
                convergence = True
            
            # 4. 更新对偶变量
            self.dual_vars.update(new_dual_vars)
            self.sub_prob.dual_vars = self.dual_vars  # 更新子问题的对偶变量
            
            print(f"迭代 {iteration}: 对偶变量差 = {diff:.6f}")
        
        # 生成最终结果
        result = {
            "status": "converged" if convergence else "max_iterations_reached",
            "iterations": iteration,
            "dual_variables": self.dual_vars,
            "equipment_status": self.equipment.delta_t,
            "objective_value": self.main_prob.dual_objective(self.dual_vars) + 
                              self.sub_prob.objective(self.equipment.delta_t),
            "convergence": convergence
        }
        
        return result


class StrongDualityOptimizer(StochasticOptimizer):
    """适配PyXESXXN框架的强对偶优化器"""
    
    def __init__(self, config: OptimizationConfig):
        """初始化强对偶优化器
        
        参数
        ----------
        config : OptimizationConfig
            优化配置
        """
        super().__init__(config)
        
        # 从配置中获取参数
        self.T = config.parameters.get("time_stages", 24)  # 时间阶段数，默认24小时
        
        # 初始化不确定性集
        uncertainty_params = config.parameters.get("uncertainty_set", {})
        self.uncertainty = UncertaintySet(
            xi0_pv=np.array(uncertainty_params.get("xi0_pv", [0.0]*self.T)),
            xi0_wt=np.array(uncertainty_params.get("xi0_wt", [0.0]*self.T)),
            xi0_load=np.array(uncertainty_params.get("xi0_load", [100.0]*self.T)),
            delta_pv=np.array(uncertainty_params.get("delta_pv", [10.0]*self.T)),
            delta_wt=np.array(uncertainty_params.get("delta_wt", [15.0]*self.T)),
            delta_load=np.array(uncertainty_params.get("delta_load", [20.0]*self.T)),
            gamma_t=np.array(uncertainty_params.get("gamma_t", [5.0]*self.T))
        )
        
        # 初始化设备参数
        equipment_params = config.parameters.get("equipment_params", {})
        self.equipment = EquipmentParameters(
            mt_max_p=np.array(equipment_params.get("mt_max_p", [200.0]*self.T)),
            mt_min_p=np.array(equipment_params.get("mt_min_p", [50.0]*self.T)),
            c_mt=np.array(equipment_params.get("c_mt", [1.0]*self.T)),
            c_start=equipment_params.get("c_start", 100.0),
            c_shut=equipment_params.get("c_shut", 50.0),
            c_grid=np.array(equipment_params.get("c_grid", [0.8]*self.T)),
            eta_chr=equipment_params.get("eta_chr", 0.9),
            eta_dis=equipment_params.get("eta_dis", 0.9),
            soc_initial=equipment_params.get("soc_initial", 0.5),
            soc_max=equipment_params.get("soc_max", 1.0),
            soc_min=equipment_params.get("soc_min", 0.2)
        )
        
        # 初始化强对偶求解器
        self.solver = HierarchicalStrongDualityOptimizer(self.T, self.uncertainty, self.equipment)
    
    def add_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """添加优化变量（强对偶优化器不需要显式添加变量）"""
        pass
    
    def add_constraint(self, name: str, expression: str, **kwargs) -> OptimizationConstraint:
        """添加优化约束（强对偶优化器不需要显式添加约束）"""
        pass
    
    def set_objective(self, objective: Callable) -> None:
        """设置目标函数（强对偶优化器有统一的目标函数）"""
        pass
    
    def add_scenario(self, scenario_name: str, probability: float) -> None:
        """添加场景（强对偶优化器通过不确定性集处理）"""
        pass
    
    def set_scenario_objective(self, scenario_name: str, objective: Callable) -> None:
        """设置场景目标（强对偶优化器有统一的目标函数）"""
        pass
    
    def get_expected_value(self) -> float:
        """获取目标函数的期望值"""
        if hasattr(self, "result"):
            return self.result["objective_value"]
        return 0.0
    
    def get_scenario_solution(self, scenario_name: str) -> Dict[str, float]:
        """获取特定场景的解决方案"""
        if hasattr(self, "result"):
            return {
                "equipment_status": self.result["equipment_status"].tolist(),
                "dual_lambda": self.result["dual_variables"].lambda_t.tolist()
            }
        return {}
    
    def solve(self) -> Dict[str, Any]:
        """求解优化问题"""
        max_iterations = self._config.parameters.get("max_iterations", 100)
        epsilon = self._config.parameters.get("convergence_epsilon", 1e-3)
        
        self.result = self.solver.solve(max_iterations, epsilon)
        return self.result
    
    def validate_problem(self) -> Tuple[bool, List[str]]:
        """验证优化问题设置"""
        errors = []
        
        # 检查时间阶段数
        if self.T <= 0:
            errors.append(f"无效的时间阶段数: {self.T}")
        
        # 检查不确定性集参数
        if any(self.uncertainty.gamma_t < 0):
            errors.append("鲁棒调节系数不能为负")
        
        # 检查设备参数
        if any(self.equipment.mt_max_p < self.equipment.mt_min_p):
            errors.append("设备最大出力不能小于最小出力")
        
        return len(errors) == 0, errors


# 将强对偶优化器注册到PyXESXXN优化工厂
def register_strong_duality_optimizer():
    """注册强对偶优化器到工厂"""
    try:
        from .pyxesxxn_impl import PyXESXXNOptimizationFactory
        
        original_create = PyXESXXNOptimizationFactory.create_stochastic_optimizer
        
        def extended_create(self, config: OptimizationConfig) -> StochasticOptimizer:
            """扩展创建方法，支持强对偶优化器"""
            optimizer_type = config.parameters.get("optimizer_type", "default")
            if optimizer_type == "strong_duality":
                return StrongDualityOptimizer(config)
            return original_create(self, config)
        
        PyXESXXNOptimizationFactory.create_stochastic_optimizer = extended_create
        print("强对偶优化器已成功注册到PyXESXXN优化工厂")
    except ImportError as e:
        print(f"注册强对偶优化器失败: {e}")


# 自动注册
register_strong_duality_optimizer()


# 工厂函数，用于创建强对偶优化器
def create_strong_duality_optimizer(config: OptimizationConfig) -> StrongDualityOptimizer:
    """创建强对偶优化器
    
    参数
    ----------
    config : OptimizationConfig
        优化配置
    
    返回
    ----------
    StrongDualityOptimizer
        强对偶优化器实例
    """
    return StrongDualityOptimizer(config)