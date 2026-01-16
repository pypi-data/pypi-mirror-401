"""
Wasserstein增强型多阶段随机凸优化（WEMSCO）框架实现

基于四篇文献核心技术的全新分布式鲁棒凸优化体系，聚焦高维、多阶段、含马尔可夫不确定性的复杂优化问题。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Callable, Any, Union
import numpy as np
from scipy.linalg import block_diag
from scipy.spatial.distance import cdist

from .abstract import (
    StochasticOptimizer, OptimizationConfig, OptimizationVariable, OptimizationConstraint,
    OptimizationType, SolverType
)
from .regularized_decomposition import (
    UncertaintyType, CuttingPlane, RegularizationParams, MarkovState,
    ValueFunctionApproximator, CuttingPlaneApproximator, SimpleOptimizationVariable,
    SimpleOptimizationConstraint
)


class WEMSCOOptimizationType(Enum):
    """WEMSCO优化类型枚举"""
    WASSERSTEIN_DISTRIBUTED_ROBUST = "wasserstein_distributed_robust"  # Wasserstein分布式鲁棒
    ADVERSARIAL_ENHANCED = "adversarial_enhanced"  # 对抗性增强
    FAST_INNER_CONVEX_APPROX = "fast_inner_convex_approx"  # 快速内凸近似
    FULL_INTEGRATION = "full_integration"  # 全集成模式


class UncertaintySide(Enum):
    """不确定性位置枚举"""
    LEFT_HAND_SIDE = "left_hand_side"  # 左端不确定性（LHS）
    RIGHT_HAND_SIDE = "right_hand_side"  # 右端不确定性（RHS）
    BOTH_SIDES = "both_sides"  # 两端均有不确定性


@dataclass
class WassersteinParams:
    """Wasserstein距离参数"""
    theta: float = 0.1  # Wasserstein半径
    epsilon: float = 0.05  # 约束满足的最小概率
    num_scenarios: int = 100  # 场景数量
    empirical_distribution: Optional[np.ndarray] = None  # 经验分布


@dataclass
class FastInnerConvexApproxParams:
    """快速内凸近似参数"""
    uncertainty_side: UncertaintySide = UncertaintySide.RIGHT_HAND_SIDE  # 不确定性位置
    key_scenario_threshold: float = 0.95  # 关键场景筛选阈值
    k: int = 5  # 关键场景数量
    kappa: float = 0.5  # 近似参数


@dataclass
class AdversarialParams:
    """对抗性增强参数"""
    rho: float = 0.1  # 约束松弛惩罚系数
    mu: float = 0.05  # 分布偏移容忍半径
    M: int = 5  # 扰动场景数量
    R_ell: float = 1.0  # 负载扰动边界
    R_beta: float = 1.0  # 容量扰动边界


class WassersteinEnhancedCuttingPlaneApproximator(CuttingPlaneApproximator):
    """Wasserstein增强的切割平面近似器"""
    
    def __init__(self, uncertainty_type: UncertaintyType, wasserstein_params: WassersteinParams):
        super().__init__(uncertainty_type)
        self.wasserstein_params = wasserstein_params
        # 存储Wasserstein增强的切割平面
        self.wasserstein_cutting_planes: Dict[int, Dict[Union[int, None], List[CuttingPlane]]] = {}
    
    def add_wasserstein_cutting_plane(self, stage: int, state: Union[int, None], plane: CuttingPlane) -> None:
        """添加Wasserstein增强的切割平面"""
        if stage not in self.wasserstein_cutting_planes:
            self.wasserstein_cutting_planes[stage] = {}
        if state not in self.wasserstein_cutting_planes[stage]:
            self.wasserstein_cutting_planes[stage][state] = []
        self.wasserstein_cutting_planes[stage][state].append(plane)
    
    def evaluate_with_wasserstein(self, stage: int, state: Union[int, None], 
                                 resource_state: np.ndarray) -> float:
        """使用Wasserstein增强的切割平面评估值函数"""
        # 首先使用常规切割平面评估
        regular_value = self.evaluate(stage, state, resource_state)
        
        # 然后使用Wasserstein增强的切割平面评估
        wasserstein_value = -np.inf
        if stage in self.wasserstein_cutting_planes and state in self.wasserstein_cutting_planes[stage]:
            for plane in self.wasserstein_cutting_planes[stage][state]:
                value = plane.alpha + np.dot(plane.beta, (resource_state - plane.reference_state))
                if value > wasserstein_value:
                    wasserstein_value = value
        
        # 返回较大值（更保守的估计）
        return max(regular_value, wasserstein_value if wasserstein_value > -np.inf else regular_value)


class WEMSCOOptimizer(StochasticOptimizer):
    """Wasserstein增强型多阶段随机凸优化（WEMSCO）优化器"""
    
    def __init__(self, config: OptimizationConfig):
        super().__init__(config)
        
        # 存储配置
        self._config = config
        
        # 获取配置参数
        self.optimization_type = config.parameters.get("wemsco_type", WEMSCOOptimizationType.FULL_INTEGRATION)
        self.uncertainty_type = config.parameters.get("uncertainty_type", UncertaintyType.STAGE_INDEPENDENT)
        self.stages = config.parameters.get("stages", 288)  # 默认288个阶段（24小时，5分钟间隔）
        self.resource_dim = config.parameters.get("resource_dim", 50)  # 默认50维资源状态
        
        # 正则化参数
        regularization_params = config.parameters.get("regularization_params", {})
        self.regularization = RegularizationParams(**regularization_params)
        
        # Wasserstein参数
        wasserstein_params = config.parameters.get("wasserstein_params", {})
        self.wasserstein_params = WassersteinParams(**wasserstein_params)
        
        # 快速内凸近似参数
        fic_params = config.parameters.get("fast_inner_convex_approx_params", {})
        self.fic_params = FastInnerConvexApproxParams(**fic_params)
        
        # 对抗性参数
        adversarial_params = config.parameters.get("adversarial_params", {})
        self.adversarial_params = AdversarialParams(**adversarial_params)
        
        # 值函数近似器（Wasserstein增强）
        self.value_function = WassersteinEnhancedCuttingPlaneApproximator(
            self.uncertainty_type, self.wasserstein_params
        )
        
        # 马尔可夫状态定义（如果是马尔可夫不确定性）
        self.markov_states: Dict[int, MarkovState] = config.parameters.get("markov_states", {})
        
        # 初始化变量和约束
        self.stage_variables: Dict[int, Dict[str, OptimizationVariable]] = {}
        self.stage_constraints: Dict[int, List[OptimizationConstraint]] = {}
        self.stage_objectives: Dict[int, Callable] = {}
        self.stage_uncertainty_sides: Dict[int, UncertaintySide] = {}
        
        # 存储前向Pass的结果
        self.forward_results: List[Dict[str, Any]] = []
        
        # 初始化Q矩阵（如果未提供）
        if self.regularization.Q is None:
            self.regularization.Q = np.eye(self.resource_dim)
        
        # 初始化incumbent状态
        self.incumbent_resource_states: Dict[int, np.ndarray] = {}
        for t in range(self.stages):
            self.incumbent_resource_states[t] = np.zeros(self.resource_dim)
        
        # 初始化场景数据
        self.scenarios: Dict[int, np.ndarray] = {}
        self.empirical_distribution: Optional[np.ndarray] = self.wasserstein_params.empirical_distribution
        
        # 初始化对偶变量
        self.dual_variables: Dict[int, Dict[str, float]] = {}
    
    def add_variable(self, name: str, **kwargs) -> OptimizationVariable:
        """添加优化变量"""
        # 多阶段优化器需要指定阶段
        stage = kwargs.pop("stage", 0)
        if stage not in self.stage_variables:
            self.stage_variables[stage] = {}
        
        # 创建变量
        variable = SimpleOptimizationVariable(name, **kwargs)
        self.stage_variables[stage][name] = variable
        return variable
    
    def add_constraint(self, name: str, expression: Callable, **kwargs) -> OptimizationConstraint:
        """添加优化约束"""
        # 多阶段优化器需要指定阶段
        stage = kwargs.pop("stage", 0)
        if stage not in self.stage_constraints:
            self.stage_constraints[stage] = []
        
        # 提取不确定性位置参数
        uncertainty_side = kwargs.pop("uncertainty_side", UncertaintySide.RIGHT_HAND_SIDE)
        
        # 创建约束（移除uncertainty_side参数）
        constraint = SimpleOptimizationConstraint(name, expression, **kwargs)
        self.stage_constraints[stage].append(constraint)
        
        # 设置不确定性位置
        self.stage_uncertainty_sides[stage] = uncertainty_side
        
        return constraint
    
    def set_objective(self, objective: Callable) -> None:
        """设置目标函数"""
        # 多阶段优化器通常为每个阶段设置目标
        self.stage_objectives[0] = objective
    
    def add_scenario(self, scenario_name: str, probability: float) -> None:
        """添加场景"""
        # WEMSCO使用场景方法生成和管理场景
        pass
    
    def set_scenario_objective(self, scenario_name: str, objective: Callable) -> None:
        """设置场景目标"""
        # WEMSCO使用统一的目标函数处理所有场景
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
        # WEMSCO算法主循环
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
            "forward_results": self.forward_results,
            "wasserstein_radius": self.wasserstein_params.theta,
            "constraint_satisfaction_probability": 1 - self.wasserstein_params.epsilon
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
                
                # 计算值函数近似（根据WEMSCO类型选择不同评估方法）
                if self.optimization_type in [
                    WEMSCOOptimizationType.WASSERSTEIN_DISTRIBUTED_ROBUST,
                    WEMSCOOptimizationType.FULL_INTEGRATION
                ]:
                    value_function_approx = self.value_function.evaluate_with_wasserstein(
                        t, information_state, R_xt
                    )
                else:
                    value_function_approx = self.value_function.evaluate(
                        t, information_state, R_xt
                    )
                
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
        """后向Pass：生成切割平面（含Wasserstein增强）"""
        decision_resource_states = forward_result["decision_resource_states"]
        
        # 从最后一个阶段开始反向计算
        for t in range(self.stages - 1, -1, -1):
            # 获取当前阶段的决策后资源状态
            R_xt = decision_resource_states[t]
            
            # 计算下边界值和次梯度（根据WEMSCO类型选择不同方法）
            if self.optimization_type in [
                WEMSCOOptimizationType.WASSERSTEIN_DISTRIBUTED_ROBUST,
                WEMSCOOptimizationType.FULL_INTEGRATION
            ]:
                lower_bound, subgradient = self._compute_wasserstein_lower_bound(t, R_xt)
            else:
                lower_bound, subgradient = self._compute_standard_lower_bound(t, R_xt)
            
            # 创建标准切割平面
            plane = CuttingPlane(
                alpha=lower_bound,
                beta=subgradient,
                reference_state=R_xt
            )
            
            # 添加切割平面到值函数近似器
            if self.uncertainty_type == UncertaintyType.MARKOVIAN:
                information_state = 0  # 这里需要从forward_result中获取实际的信息状态
                self.value_function.add_cutting_plane(t, information_state, plane)
            else:
                self.value_function.add_cutting_plane(t, None, plane)
            
            # 对于Wasserstein分布式鲁棒类型，添加增强的切割平面
            if self.optimization_type in [
                WEMSCOOptimizationType.WASSERSTEIN_DISTRIBUTED_ROBUST,
                WEMSCOOptimizationType.FULL_INTEGRATION
            ]:
                wasserstein_plane = self._create_wasserstein_enhanced_plane(t, R_xt, lower_bound, subgradient)
                if self.uncertainty_type == UncertaintyType.MARKOVIAN:
                    self.value_function.add_wasserstein_cutting_plane(t, information_state, wasserstein_plane)
                else:
                    self.value_function.add_wasserstein_cutting_plane(t, None, wasserstein_plane)
    
    def _compute_standard_lower_bound(self, stage: int, R_xt: np.ndarray) -> Tuple[float, np.ndarray]:
        """计算标准下边界值和次梯度"""
        if stage == self.stages - 1:
            return 0.0, np.zeros(self.resource_dim)
        
        expected_cost = 0.0
        expected_subgradient = np.zeros(self.resource_dim)
        
        if self.uncertainty_type == UncertaintyType.STAGE_INDEPENDENT:
            # 阶段独立：采样多个场景，计算期望
            num_scenarios = self.wasserstein_params.num_scenarios
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
    
    def _compute_wasserstein_lower_bound(self, stage: int, R_xt: np.ndarray) -> Tuple[float, np.ndarray]:
        """计算Wasserstein分布式鲁棒下边界值和次梯度"""
        if stage == self.stages - 1:
            return 0.0, np.zeros(self.resource_dim)
        
        # 生成场景集
        scenarios = self._generate_wasserstein_scenarios(stage + 1)
        
        expected_cost = 0.0
        expected_subgradient = np.zeros(self.resource_dim)
        
        for uncertainty in scenarios:
            # 计算下一阶段的最优决策
            def next_stage_obj(x):
                obj = self.stage_objectives.get(stage + 1, lambda x: 0.0)(x)
                R_xnext = self._compute_decision_resource_state(x, uncertainty)
                return obj + self.value_function.evaluate_with_wasserstein(stage + 1, None, R_xnext)
            
            next_solution = self._solve_stage_problem(stage + 1, next_stage_obj, R_xt, uncertainty)
            
            # 计算次梯度
            R_xnext = self._compute_decision_resource_state(next_solution, uncertainty)
            subgradient = self.value_function.get_subgradient(stage + 1, None, R_xnext)
            
            # 计算目标值
            obj_value = self.stage_objectives.get(stage + 1, lambda x: 0.0)(next_solution)
            
            # 应用Wasserstein分布权重
            weight = self._compute_wasserstein_scenario_weight(uncertainty)
            expected_cost += obj_value * weight
            expected_subgradient += subgradient * weight
        
        return expected_cost, expected_subgradient
    
    def _create_wasserstein_enhanced_plane(self, stage: int, R_xt: np.ndarray, 
                                          lower_bound: float, subgradient: np.ndarray) -> CuttingPlane:
        """创建Wasserstein增强的切割平面"""
        # 计算Wasserstein增强项
        wasserstein_enhancement = self.wasserstein_params.theta * np.linalg.norm(subgradient, 2)
        
        # 创建增强的切割平面
        enhanced_plane = CuttingPlane(
            alpha=lower_bound + wasserstein_enhancement,
            beta=subgradient,
            reference_state=R_xt
        )
        
        return enhanced_plane
    
    def _generate_wasserstein_scenarios(self, stage: int) -> List[Any]:
        """生成Wasserstein场景"""
        # 简化实现：基于经验分布生成场景
        num_scenarios = self.wasserstein_params.num_scenarios
        
        if self.wasserstein_params.empirical_distribution is not None:
            # 从经验分布中采样
            scenarios = []
            for _ in range(num_scenarios):
                idx = np.random.choice(len(self.wasserstein_params.empirical_distribution))
                scenarios.append(self.wasserstein_params.empirical_distribution[idx])
        else:
            # 生成随机场景
            scenarios = []
            for _ in range(num_scenarios):
                if self.uncertainty_type == UncertaintyType.STAGE_INDEPENDENT:
                    scenarios.append(np.random.randn(self.resource_dim))
                else:
                    # 马尔可夫依赖场景生成
                    current_state = np.random.choice(list(self.markov_states.keys()))
                    next_states = list(self.markov_states[current_state].transition_probs.keys())
                    probs = list(self.markov_states[current_state].transition_probs.values())
                    next_state = np.random.choice(next_states, p=probs)
                    scenarios.append(next_state)
        
        return scenarios
    
    def _compute_wasserstein_scenario_weight(self, uncertainty: Any) -> float:
        """计算Wasserstein场景权重"""
        # 简化实现：均匀权重
        return 1.0 / self.wasserstein_params.num_scenarios
    
    def _sample_uncertainty(self, stage: int, information_state: int) -> Any:
        """采样当前阶段的不确定性"""
        # 根据不确定性类型采样
        if self.uncertainty_type == UncertaintyType.STAGE_INDEPENDENT:
            # 阶段独立采样
            return np.random.randn(self.resource_dim)
        else:
            # 马尔可夫依赖采样
            current_state = self.markov_states[information_state]
            next_states = list(current_state.transition_probs.keys())
            probs = list(current_state.transition_probs.values())
            next_state = np.random.choice(next_states, p=probs)
            return next_state
    
    def _compute_decision_resource_state(self, solution: Dict[str, float], uncertainty: Any) -> np.ndarray:
        """计算决策后资源状态"""
        # 简化实现：假设资源状态是决策变量的线性函数
        R_xt = np.zeros(self.resource_dim)
        # 这里需要根据具体问题定义资源状态的演化
        return R_xt
    
    def _compute_next_resource_state(self, R_xt: np.ndarray, uncertainty: Any) -> np.ndarray:
        """计算下一阶段的资源状态"""
        # 简化实现：假设资源状态演化是线性的
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
        # 根据WEMSCO类型选择不同的求解方法
        if self.optimization_type in [
            WEMSCOOptimizationType.FAST_INNER_CONVEX_APPROX,
            WEMSCOOptimizationType.FULL_INTEGRATION
        ]:
            return self._solve_stage_problem_with_fic(stage, objective, resource_state, uncertainty)
        else:
            return self._solve_stage_problem_standard(stage, objective, resource_state, uncertainty)
    
    def _solve_stage_problem_standard(self, stage: int, objective: Callable, 
                                     resource_state: np.ndarray, uncertainty: Any) -> Dict[str, float]:
        """标准单阶段问题求解"""
        # 简化实现：使用随机搜索（实际应使用高效求解器）
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
    
    def _solve_stage_problem_with_fic(self, stage: int, objective: Callable, 
                                     resource_state: np.ndarray, uncertainty: Any) -> Dict[str, float]:
        """使用快速内凸近似求解单阶段问题"""
        # 获取当前阶段的不确定性位置
        uncertainty_side = self.stage_uncertainty_sides.get(
            stage, self.fic_params.uncertainty_side
        )
        
        # 根据不确定性位置应用不同的内凸近似方法
        if uncertainty_side == UncertaintySide.RIGHT_HAND_SIDE:
            return self._solve_rhs_uncertainty_problem(stage, objective, resource_state, uncertainty)
        elif uncertainty_side == UncertaintySide.LEFT_HAND_SIDE:
            return self._solve_lhs_uncertainty_problem(stage, objective, resource_state, uncertainty)
        else:
            # 两端均有不确定性，使用混合方法
            return self._solve_both_sides_uncertainty_problem(stage, objective, resource_state, uncertainty)
    
    def _solve_rhs_uncertainty_problem(self, stage: int, objective: Callable, 
                                      resource_state: np.ndarray, uncertainty: Any) -> Dict[str, float]:
        """求解右端不确定性问题"""
        # 快速内凸近似（SFLA）：筛选关键场景
        key_scenarios = self._select_key_scenarios(uncertainty, self.fic_params.k)
        
        # 简化实现：使用关键场景求解
        best_solution = {}
        best_value = float('inf')
        
        for _ in range(100):
            solution = {}
            for var_name in self.stage_variables.get(stage, {}):
                solution[var_name] = np.random.rand()
            
            # 仅使用关键场景检查约束
            feasible = True
            for scenario in key_scenarios:
                for constraint in self.stage_constraints.get(stage, []):
                    if not constraint.is_satisfied(solution):
                        feasible = False
                        break
                if not feasible:
                    break
            
            if feasible:
                value = objective(solution)
                if value < best_value:
                    best_value = value
                    best_solution = solution
        
        return best_solution
    
    def _solve_lhs_uncertainty_problem(self, stage: int, objective: Callable, 
                                      resource_state: np.ndarray, uncertainty: Any) -> Dict[str, float]:
        """求解左端不确定性问题"""
        # 快速内凸近似（FICA）：利用一维结构特性
        best_solution = {}
        best_value = float('inf')
        
        for _ in range(100):
            solution = {}
            for var_name in self.stage_variables.get(stage, {}):
                solution[var_name] = np.random.rand()
            
            # 计算约束的一维结构近似
            feasible = self._check_lhs_constraints_with_fica(solution, uncertainty)
            
            if feasible:
                value = objective(solution)
                if value < best_value:
                    best_value = value
                    best_solution = solution
        
        return best_solution
    
    def _solve_both_sides_uncertainty_problem(self, stage: int, objective: Callable, 
                                             resource_state: np.ndarray, uncertainty: Any) -> Dict[str, float]:
        """求解两端均有不确定性问题"""
        # 混合使用SFLA和FICA方法
        return self._solve_stage_problem_standard(stage, objective, resource_state, uncertainty)
    
    def _select_key_scenarios(self, uncertainty: Any, k: int) -> List[Any]:
        """选择关键场景"""
        # 简化实现：随机选择k个场景
        scenarios = self._generate_wasserstein_scenarios(0)
        # 确保scenarios是一维列表，直接返回前k个场景
        return scenarios[:min(k, len(scenarios))]
    
    def _check_lhs_constraints_with_fica(self, solution: Dict[str, float], 
                                       uncertainty: Any) -> bool:
        """使用FICA检查左端约束"""
        # 简化实现：基于关键场景的近似检查
        key_scenarios = self._select_key_scenarios(uncertainty, self.fic_params.k)
        
        for constraint in self.stage_constraints.get(stage, []):
            satisfied = True
            for scenario in key_scenarios:
                # 使用FICA近似评估约束
                approx_value = self._approximate_lhs_constraint(constraint, solution, scenario)
                if approx_value < 0:
                    satisfied = False
                    break
            if not satisfied:
                return False
        
        return True
    
    def _approximate_lhs_constraint(self, constraint: OptimizationConstraint, 
                                   solution: Dict[str, float], uncertainty: Any) -> float:
        """近似左端约束值"""
        # 简化实现：使用线性近似
        return constraint.evaluate(solution) if hasattr(constraint, 'evaluate') else 0.0
    
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
        
        # 检查Wasserstein参数
        if self.wasserstein_params.theta < 0:
            errors.append(f"Wasserstein radius theta {self.wasserstein_params.theta} must be non-negative")
        
        if not (0 < self.wasserstein_params.epsilon < 1):
            errors.append(f"Constraint satisfaction probability epsilon {self.wasserstein_params.epsilon} must be in (0, 1)")
        
        return len(errors) == 0, errors


# 将新优化器注册到工厂
def register_wemsco_optimizer():
    """注册WEMSCO优化器到工厂"""
    try:
        from .pyxesxxn_impl import PyXESXXNOptimizationFactory
        
        original_create = PyXESXXNOptimizationFactory.create_stochastic_optimizer
        
        def extended_create(self, config: OptimizationConfig) -> StochasticOptimizer:
            """扩展创建方法，支持WEMSCO优化器"""
            optimizer_type = config.parameters.get("optimizer_type", "default")
            if optimizer_type == "wemsco":
                return WEMSCOOptimizer(config)
            return original_create(self, config)
        
        PyXESXXNOptimizationFactory.create_stochastic_optimizer = extended_create
        return True
    except ImportError:
        return False


# 自动注册
register_wemsco_optimizer()


# 工厂函数，用于创建WEMSCO优化器
def create_wemsco_optimizer(config: OptimizationConfig) -> WEMSCOOptimizer:
    """创建WEMSCO优化器"""
    return WEMSCOOptimizer(config)


# 主入口函数，用于便捷创建和配置WEMSCO优化器
def create_wasserstein_enhanced_optimizer(
    stages: int = 288,
    resource_dim: int = 50,
    wemsco_type: WEMSCOOptimizationType = WEMSCOOptimizationType.FULL_INTEGRATION,
    uncertainty_type: UncertaintyType = UncertaintyType.STAGE_INDEPENDENT,
    wasserstein_theta: float = 0.1,
    wasserstein_epsilon: float = 0.05,
    num_scenarios: int = 100,
    **kwargs
) -> WEMSCOOptimizer:
    """
    创建Wasserstein增强型多阶段随机凸优化器
    
    Args:
        stages: 优化阶段数量
        resource_dim: 资源状态维度
        wemsco_type: WEMSCO优化类型
        uncertainty_type: 不确定性类型
        wasserstein_theta: Wasserstein半径
        wasserstein_epsilon: 约束满足的最小概率
        num_scenarios: 场景数量
        **kwargs: 其他配置参数
        
    Returns:
        配置好的WEMSCO优化器实例
    """
    # 创建优化配置
    config = OptimizationConfig(
        name="minimize_total_cost",
        optimization_type=OptimizationType.STOCHASTIC,
        solver=SolverType.SCIPY
    )
    
    # 设置WEMSCO参数
    config.parameters = {
        "optimizer_type": "wemsco",
        "wemsco_type": wemsco_type,
        "uncertainty_type": uncertainty_type,
        "stages": stages,
        "resource_dim": resource_dim,
        "max_iterations": kwargs.get("max_iterations", 300),
        "wasserstein_params": {
            "theta": wasserstein_theta,
            "epsilon": wasserstein_epsilon,
            "num_scenarios": num_scenarios
        },
        "regularization_params": kwargs.get("regularization_params", {
            "rho_0": 1.0,
            "decay_rate": 0.95
        }),
        "fast_inner_convex_approx_params": kwargs.get("fast_inner_convex_approx_params", {}),
        "adversarial_params": kwargs.get("adversarial_params", {})
    }
    
    # 添加马尔可夫状态（如果提供）
    if "markov_states" in kwargs:
        config.parameters["markov_states"] = kwargs["markov_states"]
    
    # 创建并返回WEMSCO优化器
    return WEMSCOOptimizer(config)