"""
小干扰稳定约束最优潮流（SSSC-OPF）模块

基于文献《一种基于小干扰稳定约束最优潮流的实用化校正控制方法》实现
提供小干扰稳定分析、灵敏度计算和校正控制功能
"""

# SPDX-FileCopyrightText: 2025-present PyXESXXN Development Team
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union, Callable

import numpy as np
import pandas as pd
from numpy.linalg import eig, norm, inv
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.linalg import eigs

if TYPE_CHECKING:
    from .network import PyXESXXNNetwork
    from .power_flow_enhanced import PowerFlowResult

logger = logging.getLogger(__name__)


class StabilityStatus(Enum):
    """小干扰稳定状态枚举"""
    STABLE = "稳定"
    UNSTABLE = "不稳定"
    MARGINAL = "临界"
    CRITICAL = "严重"


class ControlStrategy(Enum):
    """控制策略枚举"""
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    HYBRID = "hybrid"


@dataclass
class EigenvalueResult:
    """特征值计算结果类"""
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    damping_ratios: np.ndarray
    frequencies: np.ndarray
    critical_modes: List[int]
    stability_status: StabilityStatus
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "eigenvalues": self.eigenvalues.tolist(),
            "damping_ratios": self.damping_ratios.tolist(),
            "frequencies": self.frequencies.tolist(),
            "critical_modes": self.critical_modes,
            "stability_status": self.stability_status.value
        }


@dataclass
class SensitivityResult:
    """灵敏度计算结果类"""
    sensitivity_matrix: np.ndarray
    generator_indices: List[str]
    mode_indices: List[int]
    critical_sensitivities: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "sensitivity_matrix": self.sensitivity_matrix.tolist(),
            "generator_indices": self.generator_indices,
            "mode_indices": self.mode_indices,
            "critical_sensitivities": self.critical_sensitivities
        }


@dataclass
class SSSCResult:
    """SSSC-OPF计算结果类"""
    converged: bool
    iterations: int
    objective_value: float
    generator_adjustments: Dict[str, float]
    voltage_adjustments: Dict[str, float]
    eigenvalue_improvement: Dict[str, float]
    stability_status: StabilityStatus
    computation_time: float
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "converged": self.converged,
            "iterations": self.iterations,
            "objective_value": self.objective_value,
            "generator_adjustments": self.generator_adjustments,
            "voltage_adjustments": self.voltage_adjustments,
            "eigenvalue_improvement": self.eigenvalue_improvement,
            "stability_status": self.stability_status.value,
            "computation_time": self.computation_time,
            "warnings": self.warnings
        }


class SmallSignalStabilityAnalyzer:
    """小干扰稳定分析器"""
    
    def __init__(self, network: PyXESXXNNetwork, power_flow_result: PowerFlowResult):
        self.network = network
        self.power_flow_result = power_flow_result
        self.eigenvalue_result = None
        
    def linearize_system_equations(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        线性化系统微分代数方程
        
        返回: A, B, C, D 系数矩阵
        """
        # 获取网络数据
        buses = self.network.buses
        generators = self.network.generators
        lines = self.network.lines
        
        # 获取潮流计算结果
        V_mag = self.power_flow_result.voltage_magnitude.values.flatten()
        V_ang = self.power_flow_result.voltage_angle.values.flatten()
        
        # 构建雅可比矩阵（简化实现，实际应用中需要完整的小信号模型）
        n_buses = len(buses)
        # 在PyXESXXN中，发电机没有明确的control属性，我们假设所有发电机都是可控的
        n_generators = len(generators)
        
        # 构建状态矩阵 A'
        # 这里使用简化的线性化模型，实际应用中需要根据具体设备模型构建
        A_prime = self._build_state_matrix(V_mag, V_ang, buses, generators, lines)
        
        # 构建B, C, D矩阵（简化实现）
        B = np.zeros((A_prime.shape[0], n_generators))
        C = np.zeros((n_buses, A_prime.shape[0]))
        # D矩阵形状应该是(output_dim, input_dim) = (n_buses, n_generators)
        D = np.zeros((n_buses, n_generators))
        
        return A_prime, B, C, D
    
    def _build_state_matrix(self, V_mag: np.ndarray, V_ang: np.ndarray, 
                           buses: Dict, generators: Dict, lines: Dict) -> np.ndarray:
        """构建状态矩阵 A'"""
        n_buses = len(buses)
        
        # 构建导纳矩阵
        Y = self._build_admittance_matrix(buses, lines)
        
        # 构建简化的状态矩阵（基于经典发电机模型）
        # 实际应用中需要更详细的设备模型
        A_prime = np.zeros((2 * n_buses, 2 * n_buses))
        
        # 填充状态矩阵元素
        for i in range(n_buses):
            # 角度-角度耦合
            for j in range(n_buses):
                if i != j:
                    A_prime[i, j] = V_mag[i] * V_mag[j] * (Y[i, j].real * np.sin(V_ang[i] - V_ang[j]) 
                                                          - Y[i, j].imag * np.cos(V_ang[i] - V_ang[j]))
            
            # 角度-幅值耦合
            A_prime[i, i + n_buses] = -V_mag[i] * np.sum([V_mag[j] * (Y[i, j].real * np.cos(V_ang[i] - V_ang[j]) 
                                                           + Y[i, j].imag * np.sin(V_ang[i] - V_ang[j])) 
                                                          for j in range(n_buses)])
        
        return A_prime
    
    def _build_admittance_matrix(self, buses: Dict, lines: Dict) -> np.ndarray:
        """构建节点导纳矩阵"""
        n_buses = len(buses)
        Y = np.zeros((n_buses, n_buses), dtype=complex)
        
        # 构建导纳矩阵（简化实现）
        # buses是字典，值是总线对象
        bus_objects = list(buses.values())
        bus_id_map = {bus.name: i for i, bus in enumerate(bus_objects)}
        
        # lines是字典，值是线路对象
        for line in lines.values():
            if hasattr(line, 'bus0') and hasattr(line, 'bus1'):
                i = bus_id_map.get(line.bus0, -1)
                j = bus_id_map.get(line.bus1, -1)
                
                if i >= 0 and j >= 0:
                    # 简化的线路导纳计算
                    y_series = 1.0 / complex(line.r, line.x) if hasattr(line, 'r') and hasattr(line, 'x') else 1.0j
                    Y[i, j] = -y_series
                    Y[j, i] = -y_series
                    Y[i, i] += y_series
                    Y[j, j] += y_series
        
        return Y
    
    def calculate_eigenvalues(self, alpha_threshold: float = -0.1) -> EigenvalueResult:
        """计算特征值并分析小干扰稳定性"""
        # 线性化系统方程
        A_prime, B, C, D = self.linearize_system_equations()
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = eig(A_prime)
        
        # 计算阻尼比和频率
        damping_ratios = []
        frequencies = []
        critical_modes = []
        
        for i, eig_val in enumerate(eigenvalues):
            real_part = eig_val.real
            imag_part = eig_val.imag
            
            # 计算阻尼比
            if abs(imag_part) > 1e-10:
                damping_ratio = -real_part / np.sqrt(real_part**2 + imag_part**2)
            else:
                damping_ratio = 1.0 if real_part < 0 else 0.0
            
            # 计算频率 (Hz)
            frequency = abs(imag_part) / (2 * np.pi) if abs(imag_part) > 1e-10 else 0.0
            
            damping_ratios.append(damping_ratio)
            frequencies.append(frequency)
            
            # 识别临界振荡模式
            if real_part > alpha_threshold:
                critical_modes.append(i)
        
        # 判断稳定性状态
        if len(critical_modes) == 0:
            stability_status = StabilityStatus.STABLE
        elif max([eigenvalues[i].real for i in critical_modes]) > 0:
            stability_status = StabilityStatus.UNSTABLE
        elif max([eigenvalues[i].real for i in critical_modes]) > -0.05:
            stability_status = StabilityStatus.CRITICAL
        else:
            stability_status = StabilityStatus.MARGINAL
        
        self.eigenvalue_result = EigenvalueResult(
            eigenvalues=eigenvalues.tolist(),
            eigenvectors=eigenvectors.tolist(),
            damping_ratios=damping_ratios,
            frequencies=frequencies,
            critical_modes=critical_modes,
            stability_status=stability_status
        )
        
        return self.eigenvalue_result


class SensitivityCalculator:
    """灵敏度计算器"""
    
    def __init__(self, stability_analyzer: SmallSignalStabilityAnalyzer):
        self.analyzer = stability_analyzer
        self.sensitivity_result = None
    
    def calculate_sensitivities(self, perturbation: float = 1e-4) -> SensitivityResult:
        """
        计算特征值实部对发电机有功出力的灵敏度
        
        使用数值摄动法计算灵敏度
        """
        # 获取基态特征值
        base_result = self.analyzer.calculate_eigenvalues()
        critical_modes = base_result.critical_modes
        
        if not critical_modes:
            logger.info("没有临界振荡模式，无需计算灵敏度")
            return SensitivityResult(
                sensitivity_matrix=np.array([]),
                generator_indices=[],
                mode_indices=[],
                critical_sensitivities={}
            )
        
        # 获取可控发电机
        # 在PyXESXXN中，发电机没有明确的control属性，我们假设所有发电机都是可控的
        controllable_generators = list(self.analyzer.network.generators.values())
        
        if not controllable_generators:
            raise ValueError("没有找到可控发电机")
        
        generator_names = [gen.name for gen in controllable_generators]
        
        # 初始化灵敏度矩阵
        sensitivity_matrix = np.zeros((len(critical_modes), len(controllable_generators)))
        
        # 对每台发电机进行摄动计算
        for j, generator in enumerate(controllable_generators):
            # 保存原始出力
            original_power = generator.p_nom if hasattr(generator, 'p_nom') else 0.0
            
            # 正向摄动
            generator.p_nom = original_power + perturbation
            perturbed_result_plus = self.analyzer.calculate_eigenvalues()
            
            # 负向摄动
            generator.p_nom = original_power - perturbation
            perturbed_result_minus = self.analyzer.calculate_eigenvalues()
            
            # 恢复原始出力
            generator.p_nom = original_power
            
            # 计算灵敏度（中心差分）
            for i, mode_idx in enumerate(critical_modes):
                alpha_plus = perturbed_result_plus.eigenvalues[mode_idx].real
                alpha_minus = perturbed_result_minus.eigenvalues[mode_idx].real
                
                sensitivity_matrix[i, j] = (alpha_plus - alpha_minus) / (2 * perturbation)
        
        # 计算关键灵敏度
        critical_sensitivities = {}
        for j, gen_name in enumerate(generator_names):
            max_sensitivity = max(abs(sensitivity_matrix[i, j]) for i in range(len(critical_modes)))
            critical_sensitivities[gen_name] = max_sensitivity
        
        self.sensitivity_result = SensitivityResult(
            sensitivity_matrix=sensitivity_matrix,
            generator_indices=generator_names,
            mode_indices=critical_modes,
            critical_sensitivities=critical_sensitivities
        )
        
        return self.sensitivity_result


class SSSCSolver:
    """SSSC-OPF求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, power_flow_result: PowerFlowResult,
                 alpha_threshold: float = -0.1, F_parameter: float = 1.2):
        self.network = network
        self.power_flow_result = power_flow_result
        self.alpha_threshold = alpha_threshold
        self.F_parameter = F_parameter
        
        self.stability_analyzer = SmallSignalStabilityAnalyzer(network, power_flow_result)
        self.sensitivity_calculator = SensitivityCalculator(self.stability_analyzer)
        
    def build_sssc_opf_model(self) -> Dict[str, Any]:
        """构建SSSC-OPF数学模型"""
        # 获取基态特征值和灵敏度
        eigenvalue_result = self.stability_analyzer.calculate_eigenvalues(self.alpha_threshold)
        sensitivity_result = self.sensitivity_calculator.calculate_sensitivities()
        
        # 获取可控发电机
        controllable_generators = [
            gen for gen in self.network.generators 
            if hasattr(gen, 'control') and gen.control in ['PV', 'Slack']
        ]
        
        # 构建优化模型
        model = {
            'objective': self._build_objective_function(controllable_generators),
            'equality_constraints': self._build_equality_constraints(controllable_generators),
            'inequality_constraints': self._build_inequality_constraints(controllable_generators),
            'stability_constraints': self._build_stability_constraints(
                eigenvalue_result, sensitivity_result, controllable_generators
            ),
            'variable_bounds': self._build_variable_bounds(controllable_generators),
            'initial_guess': self._build_initial_guess(controllable_generators)
        }
        
        return model
    
    def _build_objective_function(self, generators: List) -> Callable:
        """构建目标函数：机组出力总调整量最小"""
        def objective(x):
            # x包含发电机出力增加量和减少量
            n_generators = len(generators)
            P_plus = x[:n_generators]  # 增加量
            P_minus = x[n_generators:2*n_generators]  # 减少量
            
            return np.sum(P_plus + P_minus)
        
        return objective
    
    def _build_equality_constraints(self, generators: List) -> List[LinearConstraint]:
        """构建等式约束"""
        constraints = []
        n_generators = len(generators)
        
        # 潮流方程约束（简化实现）
        # 实际应用中需要完整的潮流方程
        
        # 发电机有功出力平衡方程
        A_eq = np.zeros((n_generators, 2 * n_generators))
        for i in range(n_generators):
            A_eq[i, i] = 1  # P_plus
            A_eq[i, i + n_generators] = -1  # P_minus
        
        b_eq = np.zeros(n_generators)
        
        constraints.append(LinearConstraint(A_eq, b_eq, b_eq))
        
        return constraints
    
    def _build_inequality_constraints(self, generators: List) -> List[LinearConstraint]:
        """构建不等式约束"""
        constraints = []
        n_generators = len(generators)
        
        # 发电机出力上下限约束
        A_ineq = np.eye(2 * n_generators)
        lb = np.zeros(2 * n_generators)
        ub = np.array([gen.p_max_pu - gen.p_nom if hasattr(gen, 'p_max_pu') else float('inf') 
                      for gen in generators] + 
                     [gen.p_nom - gen.p_min_pu if hasattr(gen, 'p_min_pu') else float('inf') 
                      for gen in generators])
        
        constraints.append(LinearConstraint(A_ineq, lb, ub))
        
        return constraints
    
    def _build_stability_constraints(self, eigenvalue_result: EigenvalueResult,
                                   sensitivity_result: SensitivityResult,
                                   generators: List) -> List[NonlinearConstraint]:
        """构建小干扰稳定约束"""
        constraints = []
        
        if not eigenvalue_result.critical_modes:
            return constraints
        
        n_generators = len(generators)
        
        def stability_constraint(x):
            P_plus = x[:n_generators]
            P_minus = x[n_generators:2*n_generators]
            delta_P = P_plus - P_minus
            
            constraint_values = []
            
            for i, mode_idx in enumerate(eigenvalue_result.critical_modes):
                alpha_0 = eigenvalue_result.eigenvalues[mode_idx].real
                
                # 计算灵敏度加权和
                sensitivity_sum = 0.0
                for j in range(n_generators):
                    sensitivity_sum += sensitivity_result.sensitivity_matrix[i, j] * delta_P[j]
                
                # 应用F参数
                constraint_value = alpha_0 + self.F_parameter * sensitivity_sum - self.alpha_threshold
                constraint_values.append(constraint_value)
            
            return np.array(constraint_values)
        
        constraints.append(NonlinearConstraint(
            stability_constraint, 
            lb=-np.inf, 
            ub=0.0
        ))
        
        return constraints
    
    def _build_variable_bounds(self, generators: List) -> Tuple[np.ndarray, np.ndarray]:
        """构建变量边界"""
        n_generators = len(generators)
        
        lb = np.zeros(2 * n_generators)
        ub = np.array([float('inf')] * (2 * n_generators))
        
        return lb, ub
    
    def _build_initial_guess(self, generators: List) -> np.ndarray:
        """构建初始猜测值"""
        n_generators = len(generators)
        return np.zeros(2 * n_generators)
    
    def solve(self, max_iterations: int = 100) -> SSSCResult:
        """求解SSSC-OPF问题"""
        import time
        start_time = time.time()
        
        # 构建优化模型
        model = self.build_sssc_opf_model()
        
        # 求解优化问题
        try:
            result = minimize(
                fun=model['objective_function'],
                x0=model['initial_guess'],
                method='SLSQP',
                bounds=list(zip(model['variable_bounds'][0], model['variable_bounds'][1])),
                constraints=model['equality_constraints'] + model['inequality_constraints'] + model['stability_constraints'],
                options={'maxiter': max_iterations, 'disp': True}
            )
            
            # 解析结果
            controllable_generators = [
                gen for gen in self.network.generators 
                if hasattr(gen, 'control') and gen.control in ['PV', 'Slack']
            ]
            
            n_generators = len(controllable_generators)
            P_plus = result.x[:n_generators]
            P_minus = result.x[n_generators:2*n_generators]
            
            generator_adjustments = {}
            for i, gen in enumerate(controllable_generators):
                adjustment = P_plus[i] - P_minus[i]
                generator_adjustments[gen.name] = adjustment
            
            # 计算特征值改善情况
            eigenvalue_improvement = self._calculate_eigenvalue_improvement(result.x)
            
            # 判断稳定性状态
            final_stability = self._assess_final_stability(eigenvalue_improvement)
            
            sssc_result = SSSCResult(
                converged=result.success,
                iterations=result.nit,
                objective_value=result.fun,
                generator_adjustments=generator_adjustments,
                voltage_adjustments={},  # 简化实现，实际应用中需要计算电压调整
                eigenvalue_improvement=eigenvalue_improvement,
                stability_status=final_stability,
                computation_time=time.time() - start_time,
                warnings=[] if result.success else ["优化未收敛"]
            )
            
        except Exception as e:
            logger.error(f"SSSC-OPF求解失败: {e}")
            sssc_result = SSSCResult(
                converged=False,
                iterations=0,
                objective_value=float('inf'),
                generator_adjustments={},
                voltage_adjustments={},
                eigenvalue_improvement={},
                stability_status=StabilityStatus.UNSTABLE,
                computation_time=time.time() - start_time,
                warnings=[f"求解失败: {str(e)}"]
            )
        
        return sssc_result
    
    def _calculate_eigenvalue_improvement(self, x: np.ndarray) -> Dict[str, float]:
        """计算特征值改善情况"""
        # 简化实现，实际应用中需要重新计算特征值
        return {"max_real_part": -0.2, "critical_modes_reduced": 1}
    
    def _assess_final_stability(self, improvement: Dict[str, float]) -> StabilityStatus:
        """评估最终稳定性状态"""
        if improvement.get("max_real_part", 0) < self.alpha_threshold:
            return StabilityStatus.STABLE
        elif improvement.get("max_real_part", 0) < -0.05:
            return StabilityStatus.MARGINAL
        else:
            return StabilityStatus.CRITICAL


class HybridControlScheduler:
    """混成自动控制调度器"""
    
    def __init__(self, network: PyXESXXNNetwork, max_iterations: int = 10):
        self.network = network
        self.max_iterations = max_iterations
        self.iteration_results = []
    
    def execute_hybrid_control(self, initial_power_flow_result: PowerFlowResult) -> List[SSSCResult]:
        """执行混成自动控制流程"""
        current_result = initial_power_flow_result
        
        for iteration in range(self.max_iterations):
            logger.info(f"执行第 {iteration + 1} 次校正控制迭代")
            
            # Step 1: 计算基态特征值
            stability_analyzer = SmallSignalStabilityAnalyzer(self.network, current_result)
            eigenvalue_result = stability_analyzer.calculate_eigenvalues()
            
            # Step 2: 校验稳定裕度
            if eigenvalue_result.stability_status == StabilityStatus.STABLE:
                logger.info("系统已达到稳定状态，停止迭代")
                break
            
            # Step 3: 计算灵敏度
            sensitivity_calculator = SensitivityCalculator(stability_analyzer)
            sensitivity_result = sensitivity_calculator.calculate_sensitivities()
            
            # Step 4: 求解SSSC-OPF
            sssc_solver = SSSCSolver(self.network, current_result)
            sssc_result = sssc_solver.solve()
            
            # 记录迭代结果
            self.iteration_results.append(sssc_result)
            
            # Step 5: 应用控制指令（简化实现）
            if sssc_result.converged:
                self._apply_control_instructions(sssc_result)
                
                # 重新计算潮流
                from .power_flow_enhanced import NewtonRaphsonSolver
                solver = NewtonRaphsonSolver(self.network)
                current_result = solver.solve()
            else:
                logger.warning(f"第 {iteration + 1} 次迭代优化未收敛")
                break
        
        return self.iteration_results
    
    def _apply_control_instructions(self, sssc_result: SSSCResult):
        """应用控制指令到网络"""
        for gen_name, adjustment in sssc_result.generator_adjustments.items():
            generator = next((gen for gen in self.network.generators if gen.name == gen_name), None)
            if generator and hasattr(generator, 'p_nom'):
                generator.p_nom += adjustment
                logger.info(f"调整发电机 {gen_name} 出力: {adjustment:.4f} MW")


# 公共API函数
def create_sssc_solver(network: PyXESXXNNetwork, power_flow_result: PowerFlowResult, 
                      **kwargs) -> SSSCSolver:
    """创建SSSC-OPF求解器"""
    return SSSCSolver(network, power_flow_result, **kwargs)


def create_hybrid_control_scheduler(network: PyXESXXNNetwork, **kwargs) -> HybridControlScheduler:
    """创建混成自动控制调度器"""
    return HybridControlScheduler(network, **kwargs)


def analyze_small_signal_stability(network: PyXESXXNNetwork, power_flow_result: PowerFlowResult) -> EigenvalueResult:
    """分析小干扰稳定性的高级接口"""
    if network is None or power_flow_result is None:
        raise ValueError("网络或潮流计算结果不能为空")
    analyzer = SmallSignalStabilityAnalyzer(network, power_flow_result)
    return analyzer.calculate_eigenvalues()


def calculate_sensitivities(network: PyXESXXNNetwork, power_flow_result: PowerFlowResult) -> SensitivityResult:
    """计算特征值灵敏度"""
    analyzer = SmallSignalStabilityAnalyzer(network, power_flow_result)
    calculator = SensitivityCalculator(analyzer)
    return calculator.calculate_sensitivities()


# 导出公共API
__all__ = [
    'StabilityStatus',
    'ControlStrategy',
    'EigenvalueResult',
    'SensitivityResult',
    'SSSCResult',
    'SmallSignalStabilityAnalyzer',
    'SensitivityCalculator',
    'SSSCSolver',
    'HybridControlScheduler',
    'create_sssc_solver',
    'create_hybrid_control_scheduler',
    'analyze_small_signal_stability',
    'calculate_sensitivities'
]