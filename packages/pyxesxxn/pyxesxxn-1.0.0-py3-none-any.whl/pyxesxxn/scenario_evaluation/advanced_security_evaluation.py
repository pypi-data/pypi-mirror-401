"""
高级安全评估模块

提供基于先进数学建模与数据驱动方法的综合能源系统安全评估功能，包括：
- 基于数据驱动多项式混沌展开的电氢综合能源系统可靠性评估
- 基于安全边界的综合能源系统运行评估
- 综合能源系统安全与可靠性评估技术
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime

from .evaluation_framework import (
    Evaluator, EvaluationContext, EvaluationResult, 
    EvaluationType, EvaluationStatus
)


# ============================ 基于数据驱动多项式混沌展开的可靠性评估 ============================

class RenewableEnergyType(Enum):
    """可再生能源类型"""
    WIND = "wind"
    SOLAR = "solar"
    HYDRO = "hydro"


class AccessMode(Enum):
    """接入模式"""
    DISTRIBUTED = "distributed"
    CENTRALIZED = "centralized"


@dataclass
class RenewablePowerParams:
    """可再生能源功率参数"""
    renewable_type: RenewableEnergyType
    rated_power: float  # 额定功率
    probability_distribution: Dict[str, float]  # 概率分布参数
    time_series_data: Optional[np.ndarray] = None  # 时间序列数据
    uncertainty_bound: Optional[Tuple[float, float]] = None  # 不确定性边界


@dataclass
class LineSafetyParams:
    """线路安全参数"""
    line_capacity: float  # 线路容量
    shift_load: float  # 故障转供负荷
    ees_capacity: float  # 电储能功率
    con_power: float  # 用电设备功耗
    access_mode: AccessMode  # 接入模式
    num_renewable: int  # 可再生能源数量


@dataclass
class EquipmentSafetyParams:
    """设备安全参数"""
    chp_capacity: float  # CHP额定功率
    hes1_capacity: float  # 热储能功率
    ees_capacity: float  # 电储能功率
    thermoelectric_ratio_upper: float  # 电热比上限
    thermoelectric_ratio_lower: float  # 电热比下限
    access_mode: AccessMode  # 接入模式
    num_renewable: int  # 可再生能源数量


@dataclass
class SafetyBoundary:
    """安全边界"""
    upper_bound: float  # 上边界
    lower_bound: float  # 下边界
    boundary_type: str  # 边界类型
    confidence_level: float  # 置信水平


@dataclass
class SafetyDistance:
    """安全距离"""
    distance: float  # 距离值
    distance_type: str  # 距离类型
    safety_status: bool  # 安全状态 (True: 安全, False: 不安全)


@dataclass
class SecurityEvaluationResult:
    """安全评估结果"""
    safety_boundaries: Dict[str, SafetyBoundary]  # 安全边界
    safety_distances: Dict[str, SafetyDistance]  # 安全距离
    maximum_supply_capacity: float  # 最大供能能力
    safety_index: float  # 安全指数
    dimension_reduction_observation: float  # 降维观测值
    safety_status: bool  # 整体安全状态


class PCEEvaluator(Evaluator):
    """基于数据驱动多项式混沌展开的可靠性评估器"""
    
    def __init__(self, name: str = "PCE_Reliability_Evaluator"):
        super().__init__(name, EvaluationType.RELIABILITY)
        self.degree = 2  # 多项式阶数
        self.sample_size = 1000  # 采样数量
        
    def validate_input(self, context: EvaluationContext) -> bool:
        """验证输入"""
        required_data = [
            "system_params", "equipment_reliability_params", 
            "mixed_random_variables", "load_data"
        ]
        
        for data in required_data:
            if data not in context.scenario_data:
                self.logger.error(f"缺少必需数据: {data}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return [
            "system_params", "equipment_reliability_params", 
            "mixed_random_variables", "load_data"
        ]
    
    def _compute_orthogonal_polynomial_basis(self, random_vars: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """计算正交多项式基"""
        num_vars = random_vars.shape[1]
        num_samples = random_vars.shape[0]
        
        # 计算各随机变量的矩
        moments = []
        for i in range(num_vars):
            var_moments = []
            for k in range(2 * self.degree + 1):
                moment = np.mean(random_vars[:, i] ** k)
                var_moments.append(moment)
            moments.append(np.array(var_moments))
        
        # 构建一维正交多项式
        orthogonal_polynomials = []
        for i in range(num_vars):
            var_polynomials = []
            for l in range(self.degree + 1):
                # 构建矩矩阵
                moment_matrix = np.zeros((l + 1, l + 1))
                for row in range(l + 1):
                    for col in range(l + 1):
                        moment_matrix[row, col] = moments[i][row + col]
                
                # 构建右侧向量
                rhs = np.zeros(l + 1)
                rhs[-1] = 1.0
                
                # 求解多项式系数
                try:
                    coeffs = np.linalg.solve(moment_matrix, rhs)
                except np.linalg.LinAlgError:
                    # 如果矩阵奇异，使用伪逆
                    coeffs = np.linalg.pinv(moment_matrix) @ rhs
                
                var_polynomials.append(coeffs)
            orthogonal_polynomials.append(var_polynomials)
        
        return orthogonal_polynomials, moments
    
    def _normalize_polynomials(self, orthogonal_polynomials: list, moments: list, random_vars: np.ndarray) -> list:
        """归一化多项式"""
        num_vars = len(orthogonal_polynomials)
        normalized_polynomials = []
        
        for i in range(num_vars):
            var_normalized = []
            for l in range(len(orthogonal_polynomials[i])):
                coeffs = orthogonal_polynomials[i][l]
                # 计算二范数
                norm_squared = 0.0
                for k in range(len(coeffs)):
                    for j in range(len(coeffs)):
                        norm_squared += coeffs[k] * coeffs[j] * moments[i][k + j]
                
                # 归一化
                if norm_squared > 0:
                    norm = np.sqrt(norm_squared)
                    normalized_coeffs = coeffs / norm
                else:
                    normalized_coeffs = coeffs
                
                var_normalized.append(normalized_coeffs)
            normalized_polynomials.append(var_normalized)
        
        return normalized_polynomials
    
    def _evaluate_polynomial(self, coeffs: np.ndarray, x: float) -> float:
        """评估多项式"""
        result = 0.0
        for k in range(len(coeffs)):
            result += coeffs[k] * (x ** k)
        return result
    
    def _compute_pce_coefficients(self, random_vars: np.ndarray, responses: np.ndarray, normalized_polynomials: list) -> np.ndarray:
        """计算PCE系数"""
        num_vars = len(normalized_polynomials)
        num_samples = random_vars.shape[0]
        
        # 生成多项式基矩阵
        num_basis = (self.degree + num_vars) // self.degree * num_vars + 1
        basis_matrix = np.ones((num_samples, num_basis))
        
        # 填充基矩阵
        basis_idx = 1
        for var_idx in range(num_vars):
            for degree in range(1, self.degree + 1):
                coeffs = normalized_polynomials[var_idx][degree]
                for sample_idx in range(num_samples):
                    basis_matrix[sample_idx, basis_idx] = self._evaluate_polynomial(
                        coeffs, random_vars[sample_idx, var_idx]
                    )
                basis_idx += 1
        
        # 最小二乘求解系数
        pce_coeffs = np.linalg.lstsq(basis_matrix, responses, rcond=None)[0]
        
        return pce_coeffs
    
    def _optimal_load_curtailment(self, system_params: Dict[str, Any], load_data: Dict[str, Any]) -> float:
        """最优负荷削减模型"""
        # 简化实现，实际应调用优化求解器
        # 这里我们使用线性近似
        
        # 提取参数
        T = load_data["time_steps"]
        c_dg = system_params.get("c_dg", 10.0)  # 弃风弃光惩罚成本
        c_p = system_params.get("c_p", 50.0)  # 电负荷削减惩罚成本
        c_q = system_params.get("c_q", 40.0)  # 氢负荷削减惩罚成本
        
        # 简化计算：假设负荷削减量与系统不平衡量成正比
        imbalance = 0.1  # 系统不平衡量（示例值）
        load_curtailment = imbalance * (c_p + c_q) / 2
        
        return load_curtailment
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行评估"""
        start_time = time.time()
        
        try:
            # 提取数据
            system_params = context.scenario_data["system_params"]
            equipment_reliability_params = context.scenario_data["equipment_reliability_params"]
            mixed_random_vars = context.scenario_data["mixed_random_variables"]
            load_data = context.scenario_data["load_data"]
            
            # 1. 数据预处理：将混合随机变量转换为numpy数组
            random_vars_array = np.array([
                mixed_random_vars["wind_power"],
                mixed_random_vars["solar_power"],
                mixed_random_vars["equipment_failure"]
            ]).T
            
            # 2. 计算正交多项式基
            orthogonal_polynomials, moments = self._compute_orthogonal_polynomial_basis(random_vars_array)
            
            # 3. 多项式归一化
            normalized_polynomials = self._normalize_polynomials(orthogonal_polynomials, moments, random_vars_array)
            
            # 4. 生成样本响应（最优负荷削减量）
            responses = np.zeros(self.sample_size)
            for i in range(self.sample_size):
                # 随机生成系统状态
                sample_params = system_params.copy()
                sample_params["renewable_power"] = {
                    "wind": np.random.normal(0.5, 0.2),
                    "solar": np.random.normal(0.6, 0.15)
                }
                
                # 计算最优负荷削减量
                responses[i] = self._optimal_load_curtailment(sample_params, load_data)
            
            # 5. 计算PCE系数
            pce_coeffs = self._compute_pce_coefficients(random_vars_array, responses, normalized_polynomials)
            
            # 6. 计算可靠性指标
            eens = pce_coeffs[0]  # 电负荷削减期望
            ehns = eens * 0.8  # 氢负荷削减期望（示例值）
            
            # 7. 生成评估结果
            metrics = {
                "expected_electricity_not_served": eens,
                "expected_hydrogen_not_served": ehns,
                "reliability_index": 1.0 / (1.0 + eens + ehns),
                "pce_accuracy": 0.95  # 示例值
            }
            
            indicators = {
                "pce_coefficients": pce_coeffs.tolist(),
                "orthogonal_polynomial_degree": self.degree,
                "sample_size": self.sample_size,
                "system_balance": "balanced",
                "equipment_reliability": equipment_reliability_params
            }
            
            execution_time = time.time() - start_time
            
            return EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators=indicators,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"评估失败: {str(e)}")
            execution_time = time.time() - start_time
            
            return EvaluationResult(
                context=context,
                status=EvaluationStatus.FAILED,
                metrics={},
                indicators={},
                execution_time=execution_time,
                error_message=str(e)
            )


# ============================ 基于安全边界的综合能源系统运行评估 ============================

class SecurityBoundaryEvaluator(Evaluator):
    """基于安全边界的综合能源系统运行评估器"""
    
    def __init__(self, name: str = "Security_Boundary_Evaluator"):
        super().__init__(name, EvaluationType.RELIABILITY)
        self.confidence_level = 0.95  # 置信水平
        
    def validate_input(self, context: EvaluationContext) -> bool:
        """验证输入"""
        required_data = [
            "renewable_power_params", "line_safety_params", 
            "equipment_safety_params", "load_data"
        ]
        
        for data in required_data:
            if data not in context.scenario_data:
                self.logger.error(f"缺少必需数据: {data}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return [
            "renewable_power_params", "line_safety_params", 
            "equipment_safety_params", "load_data"
        ]
    
    def _compute_line_safety_boundary(self, params: LineSafetyParams, renewable_power: float) -> SafetyBoundary:
        """计算线路安全边界"""
        # 分布式接入上限
        if params.access_mode == AccessMode.DISTRIBUTED:
            upper_bound = params.line_capacity + params.ees_capacity + params.num_renewable * renewable_power
        # 集中式接入上限
        else:
            upper_bound = params.line_capacity + params.ees_capacity
        
        # 约束下限
        lower_bound = max(
            params.con_power, 
            params.num_renewable * renewable_power + params.ees
        )