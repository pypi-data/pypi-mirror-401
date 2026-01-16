"""
带有马尔可夫不确定性的高维多阶段随机规划的正则化分解技术实现

基于文献：Regularized Decomposition of High–Dimensional Multistage Stochastic Programs with Markov Uncertainty
作者：Tsvetan Asamov、Warren B. Powell（普林斯顿大学运筹学与金融工程系）
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Callable, Any, Union
import numpy as np
from scipy.linalg import block_diag

from .abstract import StochasticOptimizer, OptimizationConfig, OptimizationVariable, OptimizationConstraint


class UncertaintyType(Enum):
    """不确定性类型枚举"""
    STAGE_INDEPENDENT = "stage_independent"  # 阶段独立
    MARKOVIAN = "markovian"  # 马尔可夫依赖


@dataclass
class CuttingPlane:
    """切割平面数据结构"""
    alpha: float  # 截距
    beta: np.ndarray  # 斜率向量
    reference_state: np.ndarray  # 参考状态


@dataclass
class RegularizationParams:
    """正则化参数"""
    rho_0: float = 1.0  # 初始正则化系数
    decay_rate: float = 0.95  # 衰减率
    Q: Optional[np.ndarray] = None  # 缩放矩阵（默认单位矩阵）


@dataclass
class MarkovState:
    """马尔可夫状态数据结构"""
    state_id: int  # 状态ID
    transition_probs: Dict[int, float]  # 到其他状态的转移概率
    feature_vector: Optional[np.ndarray] = None  # 状态特征向量


class ValueFunctionApproximator(ABC):
    """值函数近似器抽象基类"""
    
    @abstractmethod
    def add_cutting_plane(self, stage: int, state: Union[int, None], plane: CuttingPlane) -> None:
        """添加切割平面"""
        pass
    
    @abstractmethod
    def evaluate(self, stage: int, state: Union[int, None], resource_state: np.ndarray) -> float:
        """评估值函数"""
        pass
    
    @abstractmethod
    def get_subgradient(self, stage: int, state: Union[int, None], resource_state: np.ndarray) -> np.ndarray:
        """获取值函数的次梯度"""
        pass


class CuttingPlaneApproximator(ValueFunctionApproximator):
    """基于切割平面的值函数近似器"""
    
    def __init__(self, uncertainty_type: UncertaintyType):
        self.uncertainty_type = uncertainty_type
        # 存储切割平面：{stage: {state: [CuttingPlane, ...]}}
        self.cutting_planes: Dict[int, Dict[Union[int, None], List[CuttingPlane]]] = {}
    
    def add_cutting_plane(self, stage: int, state: Union[int, None], plane: CuttingPlane) -> None:
        """添加切割平面"""
        if stage not in self.cutting_planes:
            self.cutting_planes[stage] = {}
        if state not in self.cutting_planes[stage]:
            self.cutting_planes[stage][state] = []
        self.cutting_planes[stage][state].append(plane)
    
    def evaluate(self, stage: int, state: Union[int, None], resource_state: np.ndarray) -> float:
        """评估值函数"""
        if stage not in self.cutting_planes or state not in self.cutting_planes[stage]:
            return 0.0
        
        # 找到最大值的切割平面
        max_value = -np.inf
        for plane in self.cutting_planes[stage][state]:
            value = plane.alpha + np.dot(plane.beta, (resource_state - plane.reference_state))
            if value > max_value:
                max_value = value
        
        return max_value
    
    def get_subgradient(self, stage: int, state: Union[int, None], resource_state: np.ndarray) -> np.ndarray:
        """获取值函数的次梯度"""
        if stage not in self.cutting_planes or state not in self.cutting_planes[stage]:
            return np.zeros_like(resource_state)
        
        # 找到最大值的切割平面，返回其斜率
        max_value = -np.inf
        best_beta = np.zeros_like(resource_state)
        for plane in self.cutting_planes[stage][state]:
            value = plane.alpha + np.dot(plane.beta, (resource_state - plane.reference_state))
            if value > max_value:
                max_value = value
                best_beta = plane.beta.copy()
        
        return best_beta


class RegularizedDecompositionOptimizer(StochasticOptimizer):
    """带有马尔可夫不确定性的高维多阶段随机规划的正则化分解优化器"""
    
    def __init__(self, config: OptimizationConfig):
        super().__init__(config)
        
        # 存储配置
        self._config = config
        
        # 获取配置参数
        self.uncertainty_type = config.parameters.get("uncertainty_type", UncertaintyType.STAGE_INDEPENDENT)
        self.stages = config.parameters.get("stages", 288)  # 默认288个阶段（24小时，5分钟间隔）
        self.resource_dim = config.parameters.get("resource_dim", 50)  # 默认50维资源状态
        
        # 正则化参数
        regularization_params = config.parameters.get("regularization_params", {})
        self.regularization = RegularizationParams(**regularization_params)
        
        # 值函数近似器
        self.value_function = CuttingPlaneApproximator(self.uncertainty_type)
        
        # 马尔可夫状态定义（如果是马尔可夫不确定性）
        self.markov_states: Dict[int, MarkovState] = config.parameters.get("markov_states", {})
        
        # 初始化变量和约束
        self.stage_variables: Dict[int, Dict[str, OptimizationVariable]] = {}
        self.stage_constraints: Dict[int, List[OptimizationConstraint]] = {}
        self.stage_objectives: Dict[int, Callable] = {}
        
        # 存储前向Pass的结果
        self.forward_results: List[Dict[str, Any]] = []
        
        # 初始化Q矩阵（如果未提供）
        if self.regularization.Q is None:
            self.regularization.Q = np.eye(self.resource_dim)
        
        # 初始化incumbent状态
        self.incumbent_resource_states: Dict[int, np.ndarray] = {}
        for t in range(self.stages):
            self.incumbent_resource_states[t] = np.zeros(self.resource_dim)
        
    def add_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """添加优化变量"""
        # 多阶段优化器需要指定阶段
        stage = kwargs.pop("stage", 0)
        if stage not in self.stage_variables:
            self.stage_variables[stage] = {}
        
        # 创建变量（这里使用简单实现，实际应使用工厂方法）
        variable = SimpleOptimizationVariable(name, **kwargs)
        self.stage_variables[stage][name] = variable
        return variable
    
    def add_constraint(self, name: str, expression: Callable, **kwargs) -> OptimizationConstraint:
        """添加优化约束"""
        # 多阶段优化器需要指定阶段
        stage = kwargs.pop("stage", 0)
        if stage not in self.stage_constraints:
            self.stage_constraints[stage] = []
        
        # 创建约束（这里使用简单实现，实际应使用工厂方法）
        constraint = SimpleOptimizationConstraint(name, expression, **kwargs)
        self.stage_constraints[stage].append(constraint)
        return constraint
    
    def set_objective(self, objective: Callable) -> None:
        """设置目标函数"""
        # 多阶段优化器通常为每个阶段设置目标
        self.stage_objectives[0] = objective
    
    def add_scenario(self, scenario_name: str, probability: float) -> None:
        """添加场景"""
        # 正则化分解算法通过采样生成场景，不需要显式添加
        pass
    
    def set_scenario_objective(self, scenario_name: str, objective: Callable) -> None:
        """设置场景目标"""
        # 正则化分解算法通过采样生成场景，不需要显式设置目标
        pass
    
    def get_expected_value(self) -> float:
        """获取目标函数的期望值"""
        if not self.forward_results:
            return 0.0
        
        # 计算所有前向Pass结果的平均值
        total_value = 0.0
        for result in self.forward_results:
            total_value += result["total_cost"]
        
        return total_value / len(self.forward_results)
    
    def get_scenario_solution(self, scenario_name: str) -> Dict[str, float]:
        """获取特定场景的解决方案"""
        # 返回最后一次前向Pass的结果
        if not self.forward_results:
            return {}
        
        return self.forward_results[-1]["solution"]
    
    def solve(self) -> Dict[str, Any]:
        """求解优化问题"""
        # 正则化分解算法主循环
        max_iterations = self._config.parameters.get("max_iterations", 300)
        
        for k in range(max_iterations):
            # 计算当前正则化系数
            rho_k = self.regularization.rho_0 * (self.regularization.decay_rate ** k)
            
            # 1. 前向Pass
            forward_result = self._forward_pass(rho_k, k)
            self.forward_results.append(forward_result)
            
            # 2. 后向Pass
            self._backward_pass(forward_result, k)
            
            # 3. 检查收敛性
            if self._check_convergence(k):
                break
        
        # 返回最终结果
        return {
            "status": "converged" if k < max_iterations - 1 else "max_iterations_reached",
            "iterations": k + 1,
            "expected_value": self.get_expected_value(),
            "solution": self.forward_results[-1]["solution"] if self.forward_results else {},
            "forward_results": self.forward_results
        }
    
    def _forward_pass(self, rho_k: float, iteration: int) -> Dict[str, Any]:
        """前向Pass：采样随机路径，求解各阶段决策"""
        # 初始化
        resource_state = np.zeros(self.resource_dim)  # 初始资源状态
        information_state = 0  # 初始信息状态（如果是马尔可夫不确定性）
        total_cost = 0.0
        solution = {}
        
        # 存储各阶段的决策后资源状态
        decision_resource_states = {}
        
        for t in range(self.stages):
            # 1. 采样当前阶段的不确定性
            uncertainty = self._sample_uncertainty(t, information_state)
            
            # 2. 构建当前阶段的优化问题
            stage_obj = self.stage_objectives.get(t, lambda x: 0.0)
            
            # 3. 添加正则化项到目标函数
            def regularized_objective(x):
                # 计算当前阶段的目标
                obj_value = stage_obj(x)
                
                # 计算决策后资源状态
                R_xt = self._compute_decision_resource_state(x, uncertainty)
                
                # 计算正则化项
                delta = R_xt - self.incumbent_resource_states[t]
                regularization_term = (rho_k / 2) * np.dot(delta, np.dot(self.regularization.Q, delta))
                
                # 计算值函数近似
                value_function_approx = self.value_function.evaluate(t, information_state, R_xt)
                
                return obj_value + value_function_approx + regularization_term
            
            # 4. 求解当前阶段的优化问题
            stage_solution = self._solve_stage_problem(t, regularized_objective, resource_state, uncertainty)
            
            # 5. 计算当前阶段的成本
            stage_cost = stage_obj(stage_solution)
            total_cost += stage_cost
            
            # 6. 计算决策后资源状态
            R_xt = self._compute_decision_resource_state(stage_solution, uncertainty)
            decision_resource_states[t] = R_xt
            
            # 7. 更新incumbent状态
            self.incumbent_resource_states[t] = R_xt
            
            # 8. 计算下一阶段的资源状态
            resource_state = self._compute_next_resource_state(R_xt, uncertainty)
            
            # 9. 更新信息状态（如果是马尔可夫不确定性）
            if self.uncertainty_type == UncertaintyType.MARKOVIAN:
                information_state = self._update_markov_state(information_state, uncertainty)
            
            # 10. 存储解决方案
            solution[f"stage_{t}"] = stage_solution
        
        return {
            "iteration": iteration,
            "total_cost": total_cost,
            "solution": solution,
            "decision_resource_states": decision_resource_states,
            "resource_states": resource_state,
            "rho": rho_k
        }
    
    def _backward_pass(self, forward_result: Dict[str, Any], iteration: int) -> None:
        """后向Pass：生成切割平面"""
        decision_resource_states = forward_result["decision_resource_states"]
        
        # 从最后一个阶段开始反向计算
        for t in range(self.stages - 1, -1, -1):
            # 获取当前阶段的决策后资源状态
            R_xt = decision_resource_states[t]
            
            # 计算下边界值和次梯度
            lower_bound, subgradient = self._compute_lower_bound(t, R_xt)
            
            # 创建切割平面
            plane = CuttingPlane(
                alpha=lower_bound,
                beta=subgradient,
                reference_state=R_xt
            )
            
            # 添加切割平面到值函数近似器
            # 对于马尔可夫不确定性，需要为每个信息状态添加切割平面
            if self.uncertainty_type == UncertaintyType.MARKOVIAN:
                # 获取当前阶段的信息状态（简化实现，实际应从forward_result中获取）
                information_state = 0  # 这里需要从forward_result中获取实际的信息状态
                self.value_function.add_cutting_plane(t, information_state, plane)
            else:
                self.value_function.add_cutting_plane(t, None, plane)
    
    def _sample_uncertainty(self, stage: int, information_state: int) -> Any:
        """采样当前阶段的不确定性"""
        # 根据不确定性类型采样
        if self.uncertainty_type == UncertaintyType.STAGE_INDEPENDENT:
            # 阶段独立采样
            return np.random.randn(self.resource_dim)
        else:
            # 马尔可夫依赖采样
            # 根据当前信息状态和转移概率采样下一个状态
            current_state = self.markov_states[information_state]
            next_states = list(current_state.transition_probs.keys())
            probs = list(current_state.transition_probs.values())
            next_state = np.random.choice(next_states, p=probs)
            return next_state
    
    def _compute_decision_resource_state(self, solution: Dict[str, float], uncertainty: Any) -> np.ndarray:
        """计算决策后资源状态"""
        # 简化实现：假设资源状态是决策变量的线性函数
        # 实际应根据具体问题定义资源状态的演化
        R_xt = np.zeros(self.resource_dim)
        # 这里需要根据具体问题实现资源状态的计算
        return R_xt
    
    def _compute_next_resource_state(self, R_xt: np.ndarray, uncertainty: Any) -> np.ndarray:
        """计算下一阶段的资源状态"""
        # 简化实现：假设资源状态演化是线性的
        # 实际应根据具体问题定义资源状态的演化
        # 资源状态演化：R_{t+1} = B_t x_t - b_t
        B = np.eye(self.resource_dim)  # 简化，实际应根据问题定义
        b = np.random.randn(self.resource_dim)  # 简化，实际应根据不确定性定义
        return B.dot(R_xt) - b
    
    def _update_markov_state(self, current_state: int, uncertainty: Any) -> int:
        """更新马尔可夫状态"""
        # 简化实现：假设不确定性直接给出下一状态
        return uncertainty
    
    def _solve_stage_problem(self, stage: int, objective: Callable, 
                            resource_state: np.ndarray, uncertainty: Any) -> Dict[str, float]:
        """求解单阶段优化问题"""
        # 简化实现：使用随机搜索（实际应使用高效求解器）
        # 这里可以替换为实际的求解器调用
        best_solution = {}
        best_value = float('inf')
        
        # 生成100个随机解，选择最优解
        for _ in range(100):
            # 生成随机解
            solution = {}
            for var_name in self.stage_variables.get(stage, {}):
                solution[var_name] = np.random.rand()
            
            # 计算目标值
            value = objective(solution)
            
            # 检查约束
            feasible = True
            for constraint in self.stage_constraints.get(stage, []):
                if not constraint.is_satisfied(solution):
                    feasible = False
                    break
            
            if feasible and value < best_value:
                best_value = value
                best_solution = solution
        
        return best_solution
    
    def _compute_lower_bound(self, stage: int, R_xt: np.ndarray) -> Tuple[float, np.ndarray]:
        """计算下边界值和次梯度"""
        # 简化实现：根据值函数近似器计算
        if stage == self.stages - 1:
            # 最后一个阶段没有后续成本
            return 0.0, np.zeros(self.resource_dim)
        
        # 计算下一阶段的期望成本
        expected_cost = 0.0
        expected_subgradient = np.zeros(self.resource_dim)
        
        if self.uncertainty_type == UncertaintyType.STAGE_INDEPENDENT:
            # 阶段独立：采样多个场景，计算期望
            num_scenarios = 10
            for _ in range(num_scenarios):
                uncertainty = self._sample_uncertainty(stage + 1, 0)
                
                # 计算下一阶段的最优决策
                def next_stage_obj(x):
                    obj = self.stage_objectives.get(stage + 1, lambda x: 0.0)(x)
                    R_xnext = self._compute_decision_resource_state(x, uncertainty)
                    return obj + self.value_function.evaluate(stage + 1, None, R_xnext)
                
                next_solution = self._solve_stage_problem(stage + 1, next_stage_obj, R_xt, uncertainty)
                
                # 计算次梯度
                R_xnext = self._compute_decision_resource_state(next_solution, uncertainty)
                subgradient = self.value_function.get_subgradient(stage + 1, None, R_xnext)
                
                # 计算目标值
                obj_value = self.stage_objectives.get(stage + 1, lambda x: 0.0)(next_solution)
                
                expected_cost += obj_value / num_scenarios
                expected_subgradient += subgradient / num_scenarios
        else:
            # 马尔可夫依赖：根据转移概率计算期望
            for state_id, state in self.markov_states.items():
                for next_state_id, prob in state.transition_probs.items():
                    # 计算下一阶段的最优决策
                    def next_stage_obj(x):
                        obj = self.stage_objectives.get(stage + 1, lambda x: 0.0)(x)
                        R_xnext = self._compute_decision_resource_state(x, next_state_id)
                        return obj + self.value_function.evaluate(stage + 1, next_state_id, R_xnext)
                    
                    next_solution = self._solve_stage_problem(stage + 1, next_stage_obj, R_xt, next_state_id)
                    
                    # 计算次梯度
                    R_xnext = self._compute_decision_resource_state(next_solution, next_state_id)
                    subgradient = self.value_function.get_subgradient(stage + 1, next_state_id, R_xnext)
                    
                    # 计算目标值
                    obj_value = self.stage_objectives.get(stage + 1, lambda x: 0.0)(next_solution)
                    
                    expected_cost += obj_value * prob
                    expected_subgradient += subgradient * prob
        
        return expected_cost, expected_subgradient
    
    def _check_convergence(self, iteration: int) -> bool:
        """检查收敛性"""
        # 简化实现：检查前后两次迭代的总成本变化
        if len(self.forward_results) < 2:
            return False
        
        current_cost = self.forward_results[-1]["total_cost"]
        previous_cost = self.forward_results[-2]["total_cost"]
        
        # 相对变化小于阈值则收敛
        if abs(current_cost - previous_cost) / max(1, abs(previous_cost)) < 1e-4:
            return True
        
        return False
    
    def validate_problem(self) -> Tuple[bool, List[str]]:
        """验证优化问题设置"""
        errors = []
        
        # 检查是否设置了所有阶段的目标
        for t in range(self.stages):
            if t not in self.stage_objectives:
                errors.append(f"Stage {t} has no objective function")
        
        # 检查资源维度是否匹配
        if self.regularization.Q.shape != (self.resource_dim, self.resource_dim):
            errors.append(f"Q matrix dimension {self.regularization.Q.shape} does not match resource dimension {self.resource_dim}")
        
        # 检查马尔可夫状态是否定义（如果是马尔可夫不确定性）
        if self.uncertainty_type == UncertaintyType.MARKOVIAN and not self.markov_states:
            errors.append("Markov states not defined for Markovian uncertainty")
        
        return len(errors) == 0, errors


# 简单的优化变量和约束实现（实际应使用工厂方法）
class SimpleOptimizationVariable(OptimizationVariable):
    """简单的优化变量实现"""
    
    def __init__(self, name: str, lower_bound: float = 0.0, 
                 upper_bound: float = float('inf'), variable_type: str = "continuous"):
        self._name = name
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._variable_type = variable_type
        self._value = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> Optional[float]:
        return self._value
    
    @value.setter
    def value(self, value: float) -> None:
        self._value = value
    
    @property
    def lower_bound(self) -> float:
        return self._lower_bound
    
    @property
    def upper_bound(self) -> float:
        return self._upper_bound


class SimpleOptimizationConstraint(OptimizationConstraint):
    """简单的优化约束实现"""
    
    def __init__(self, name: str, expression: Callable, 
                 lower_bound: float = 0.0, upper_bound: float = 0.0):
        self._name = name
        self._expression = expression
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
    
    @property
    def name(self) -> str:
        return self._name
    
    def evaluate(self, variables: Dict[str, float]) -> float:
        return self._expression(variables)
    
    def is_satisfied(self, variables: Dict[str, float]) -> bool:
        value = self.evaluate(variables)
        return self._lower_bound <= value <= self._upper_bound


# 将新优化器注册到工厂
from .pyxesxxn_impl import PyXESXXNOptimizationFactory

# 扩展PyXESXXNOptimizationFactory以支持正则化分解优化器
def register_regularized_decomposition_optimizer():
    """注册正则化分解优化器到工厂"""
    original_create = PyXESXXNOptimizationFactory.create_stochastic_optimizer
    
    def extended_create(self, config: OptimizationConfig) -> StochasticOptimizer:
        """扩展创建方法，支持正则化分解优化器"""
        optimizer_type = config.parameters.get("optimizer_type", "default")
        if optimizer_type == "regularized_decomposition":
            return RegularizedDecompositionOptimizer(config)
        return original_create(self, config)
    
    PyXESXXNOptimizationFactory.create_stochastic_optimizer = extended_create


# 自动注册
register_regularized_decomposition_optimizer()


# 工厂函数，用于创建正则化分解优化器
def create_regularized_decomposition_optimizer(config: OptimizationConfig) -> RegularizedDecompositionOptimizer:
    """创建正则化分解优化器"""
    return RegularizedDecompositionOptimizer(config)
