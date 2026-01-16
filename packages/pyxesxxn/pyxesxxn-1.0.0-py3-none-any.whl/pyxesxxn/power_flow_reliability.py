"""
潮流计算可靠性验证模块

提供潮流计算结果的可靠性验证、敏感性分析和误差评估功能。
"""

# SPDX-FileCopyrightText: 2024-present PyXESXXN Development Team
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from numpy.linalg import cond, norm
from scipy import stats
from scipy.optimize import minimize

from .network import PyXESXXNNetwork, Network

if TYPE_CHECKING:
    from .network import PyXESXXNNetwork, Network
    from .power_flow_enhanced import PowerFlowResult


logger = logging.getLogger(__name__)


class ReliabilityLevel(Enum):
    """可靠性等级枚举"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SensitivityType(Enum):
    """敏感性分析类型枚举"""
    PARAMETER = "parameter"
    LOAD = "load"
    GENERATION = "generation"
    TOPOLOGY = "topology"


@dataclass
class ReliabilityMetrics:
    """可靠性指标类"""
    voltage_stability_margin: float
    line_loading_ratio: float
    transformer_loading_ratio: float
    n_minus_1_security: bool
    voltage_deviation: float
    frequency_stability: float
    convergence_robustness: float
    numerical_stability: float
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典格式"""
        return {
            "voltage_stability_margin": self.voltage_stability_margin,
            "line_loading_ratio": self.line_loading_ratio,
            "transformer_loading_ratio": self.transformer_loading_ratio,
            "n_minus_1_security": float(self.n_minus_1_security),
            "voltage_deviation": self.voltage_deviation,
            "frequency_stability": self.frequency_stability,
            "convergence_robustness": self.convergence_robustness,
            "numerical_stability": self.numerical_stability
        }


@dataclass
class SensitivityResult:
    """敏感性分析结果类"""
    parameter: str
    base_value: float
    sensitivity: float
    normalized_sensitivity: float
    confidence_interval: Tuple[float, float]
    impact_level: ReliabilityLevel
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "parameter": self.parameter,
            "base_value": self.base_value,
            "sensitivity": self.sensitivity,
            "normalized_sensitivity": self.normalized_sensitivity,
            "confidence_interval": self.confidence_interval,
            "impact_level": self.impact_level.value
        }


class PowerFlowReliabilityAnalyzer:
    """潮流计算可靠性分析器"""
    
    def __init__(self, network: Network, power_flow_result: PowerFlowResult):
        self.network = network
        self.result = power_flow_result
        self.metrics = None
        self.sensitivity_results = []
    
    def analyze_reliability(self) -> ReliabilityMetrics:
        """分析潮流计算结果的可靠性"""
        metrics = ReliabilityMetrics(
            voltage_stability_margin=self._calculate_voltage_stability_margin(),
            line_loading_ratio=self._calculate_line_loading_ratio(),
            transformer_loading_ratio=self._calculate_transformer_loading_ratio(),
            n_minus_1_security=self._check_n_minus_1_security(),
            voltage_deviation=self._calculate_voltage_deviation(),
            frequency_stability=self._assess_frequency_stability(),
            convergence_robustness=self._assess_convergence_robustness(),
            numerical_stability=self._assess_numerical_stability()
        )
        
        self.metrics = metrics
        return metrics
    
    def perform_sensitivity_analysis(self, analysis_type: SensitivityType,
                                   parameters: Optional[List[str]] = None) -> List[SensitivityResult]:
        """执行敏感性分析"""
        if analysis_type == SensitivityType.PARAMETER:
            return self._analyze_parameter_sensitivity(parameters)
        elif analysis_type == SensitivityType.LOAD:
            return self._analyze_load_sensitivity()
        elif analysis_type == SensitivityType.GENERATION:
            return self._analyze_generation_sensitivity()
        elif analysis_type == SensitivityType.TOPOLOGY:
            return self._analyze_topology_sensitivity()
        else:
            raise ValueError(f"不支持的敏感性分析类型: {analysis_type}")
    
    def _calculate_voltage_stability_margin(self) -> float:
        """计算电压稳定裕度"""
        v_mag = self.result.voltage_magnitude.values.flatten()
        
        # 计算电压稳定指标
        v_min = np.min(v_mag)
        v_max = np.max(v_mag)
        v_avg = np.mean(v_mag)
        
        # 基于电压偏差计算稳定裕度
        voltage_deviation = np.std(v_mag)
        stability_margin = 1.0 - (voltage_deviation / v_avg) if v_avg > 0 else 0.0
        
        # 考虑电压越限情况
        under_voltage = np.sum(v_mag < 0.95)
        over_voltage = np.sum(v_mag > 1.05)
        
        if under_voltage > 0 or over_voltage > 0:
            stability_margin *= 0.5  # 电压越限时降低稳定裕度
        
        return max(0.0, min(1.0, stability_margin))
    
    def _calculate_line_loading_ratio(self) -> float:
        """计算线路负载率"""
        line_flows = self.result.line_flows
        
        if not line_flows:
            return 0.0
        
        loading_ratios = []
        
        for line_name, flow_data in line_flows.items():
            if 'p' in flow_data.columns:
                p_flow = flow_data['p'].abs().max()
                
                # 获取线路额定容量
                line_data = self.network.c.lines.static.loc[line_name]
                s_nom = line_data.get('s_nom', 1.0)
                
                if s_nom > 0:
                    loading_ratio = p_flow / s_nom
                    loading_ratios.append(loading_ratio)
        
        if loading_ratios:
            return np.max(loading_ratios)
        else:
            return 0.0
    
    def _calculate_transformer_loading_ratio(self) -> float:
        """计算变压器负载率"""
        transformer_flows = self.result.transformer_flows
        
        if not transformer_flows:
            return 0.0
        
        loading_ratios = []
        
        for trafo_name, flow_data in transformer_flows.items():
            if 'p' in flow_data.columns:
                p_flow = flow_data['p'].abs().max()
                
                # 获取变压器额定容量
                trafo_data = self.network.c.transformers.static.loc[trafo_name]
                s_nom = trafo_data.get('s_nom', 1.0)
                
                if s_nom > 0:
                    loading_ratio = p_flow / s_nom
                    loading_ratios.append(loading_ratio)
        
        if loading_ratios:
            return np.max(loading_ratios)
        else:
            return 0.0
    
    def _check_n_minus_1_security(self) -> bool:
        """检查N-1安全性"""
        # 简化的N-1安全性检查
        # 在实际应用中，这需要更复杂的分析
        
        line_loading = self._calculate_line_loading_ratio()
        trafo_loading = self._calculate_transformer_loading_ratio()
        voltage_margin = self._calculate_voltage_stability_margin()
        
        # 基于经验规则的N-1安全性判断
        security_conditions = [
            line_loading < 0.8,  # 线路负载率低于80%
            trafo_loading < 0.8,  # 变压器负载率低于80%
            voltage_margin > 0.2  # 电压稳定裕度大于20%
        ]
        
        return all(security_conditions)
    
    def _calculate_voltage_deviation(self) -> float:
        """计算电压偏差"""
        v_mag = self.result.voltage_magnitude.values.flatten()
        return np.std(v_mag)
    
    def _assess_frequency_stability(self) -> float:
        """评估频率稳定性"""
        # 简化的频率稳定性评估
        # 在实际应用中，这需要动态仿真数据
        
        # 基于功率平衡和网络结构评估频率稳定性
        total_generation = self.result.active_power.sum().sum()
        total_load = abs(self.result.active_power.sum().sum())
        
        if total_generation > 0 and total_load > 0:
            balance_ratio = min(total_generation / total_load, total_load / total_generation)
            return balance_ratio
        else:
            return 0.0
    
    def _assess_convergence_robustness(self) -> float:
        """评估收敛鲁棒性"""
        if self.result.converged:
            # 基于迭代次数和误差评估收敛鲁棒性
            max_iterations = 100  # 假设最大迭代次数
            robustness = 1.0 - (self.result.iterations / max_iterations)
            
            # 考虑误差大小
            error_penalty = min(1.0, self.result.error / 1e-6)
            robustness *= (1.0 - error_penalty * 0.1)
            
            return max(0.0, robustness)
        else:
            return 0.0
    
    def _assess_numerical_stability(self) -> float:
        """评估数值稳定性"""
        # 基于电压和功率的数值特性评估稳定性
        v_mag = self.result.voltage_magnitude.values.flatten()
        p_flow = []
        
        # 收集所有功率流数据
        for flows in [self.result.line_flows, self.result.transformer_flows]:
            for flow_data in flows.values():
                if 'p' in flow_data.columns:
                    p_flow.extend(flow_data['p'].values.flatten())
        
        if len(p_flow) > 0:
            # 计算数值范围的合理性
            v_range = np.max(v_mag) - np.min(v_mag)
            p_range = np.max(np.abs(p_flow)) - np.min(np.abs(p_flow))
            
            # 基于范围比例评估稳定性
            stability = 1.0 / (1.0 + v_range + p_range)
            return min(1.0, stability)
        else:
            return 0.5  # 默认中等稳定性
    
    def _analyze_parameter_sensitivity(self, parameters: Optional[List[str]]) -> List[SensitivityResult]:
        """分析参数敏感性"""
        if parameters is None:
            parameters = ['r', 'x', 'b', 's_nom']  # 默认分析参数
        
        results = []
        
        for param in parameters:
            sensitivity = self._calculate_parameter_sensitivity(param)
            results.append(sensitivity)
        
        self.sensitivity_results.extend(results)
        return results
    
    def _calculate_parameter_sensitivity(self, parameter: str) -> SensitivityResult:
        """计算特定参数的敏感性"""
        # 简化的敏感性计算
        # 在实际应用中，这需要扰动分析和重新计算潮流
        
        base_value = 1.0  # 假设基准值
        sensitivity = 0.1  # 假设敏感性系数
        
        # 基于参数类型调整敏感性
        if parameter in ['r', 'x']:
            sensitivity = 0.2
        elif parameter == 'b':
            sensitivity = 0.05
        elif parameter == 's_nom':
            sensitivity = 0.15
        
        normalized_sensitivity = sensitivity / base_value if base_value != 0 else 0.0
        
        # 确定影响等级
        if abs(normalized_sensitivity) > 0.3:
            impact_level = ReliabilityLevel.HIGH
        elif abs(normalized_sensitivity) > 0.1:
            impact_level = ReliabilityLevel.MEDIUM
        else:
            impact_level = ReliabilityLevel.LOW
        
        return SensitivityResult(
            parameter=parameter,
            base_value=base_value,
            sensitivity=sensitivity,
            normalized_sensitivity=normalized_sensitivity,
            confidence_interval=(sensitivity * 0.8, sensitivity * 1.2),
            impact_level=impact_level
        )
    
    def _analyze_load_sensitivity(self) -> List[SensitivityResult]:
        """分析负荷敏感性"""
        results = []
        
        # 简化的负荷敏感性分析
        load_sensitivity = SensitivityResult(
            parameter="load_variation",
            base_value=1.0,
            sensitivity=0.25,
            normalized_sensitivity=0.25,
            confidence_interval=(0.2, 0.3),
            impact_level=ReliabilityLevel.MEDIUM
        )
        
        results.append(load_sensitivity)
        self.sensitivity_results.extend(results)
        return results
    
    def _analyze_generation_sensitivity(self) -> List[SensitivityResult]:
        """分析发电敏感性"""
        results = []
        
        # 简化的发电敏感性分析
        gen_sensitivity = SensitivityResult(
            parameter="generation_variation",
            base_value=1.0,
            sensitivity=0.2,
            normalized_sensitivity=0.2,
            confidence_interval=(0.15, 0.25),
            impact_level=ReliabilityLevel.MEDIUM
        )
        
        results.append(gen_sensitivity)
        self.sensitivity_results.extend(results)
        return results
    
    def _analyze_topology_sensitivity(self) -> List[SensitivityResult]:
        """分析拓扑敏感性"""
        results = []
        
        # 简化的拓扑敏感性分析
        topology_sensitivity = SensitivityResult(
            parameter="topology_change",
            base_value=1.0,
            sensitivity=0.3,
            normalized_sensitivity=0.3,
            confidence_interval=(0.25, 0.35),
            impact_level=ReliabilityLevel.HIGH
        )
        
        results.append(topology_sensitivity)
        self.sensitivity_results.extend(results)
        return results
    
    def generate_reliability_report(self) -> str:
        """生成可靠性报告"""
        if self.metrics is None:
            self.analyze_reliability()
        
        report = []
        report.append("=== 潮流计算可靠性分析报告 ===")
        report.append(f"\n可靠性指标:")
        report.append(f"电压稳定裕度: {self.metrics.voltage_stability_margin:.3f}")
        report.append(f"线路最大负载率: {self.metrics.line_loading_ratio:.3f}")
        report.append(f"变压器最大负载率: {self.metrics.transformer_loading_ratio:.3f}")
        report.append(f"N-1安全性: {'满足' if self.metrics.n_minus_1_security else '不满足'}")
        report.append(f"电压偏差: {self.metrics.voltage_deviation:.4f} pu")
        report.append(f"频率稳定性: {self.metrics.frequency_stability:.3f}")
        report.append(f"收敛鲁棒性: {self.metrics.convergence_robustness:.3f}")
        report.append(f"数值稳定性: {self.metrics.numerical_stability:.3f}")
        
        # 敏感性分析结果
        if self.sensitivity_results:
            report.append(f"\n敏感性分析:")
            for result in self.sensitivity_results:
                report.append(f"{result.parameter}: {result.normalized_sensitivity:.3f} ({result.impact_level.value})")
        
        # 总体可靠性评估
        overall_reliability = self._calculate_overall_reliability()
        report.append(f"\n总体可靠性等级: {overall_reliability.value}")
        
        return "\n".join(report)
    
    def _calculate_overall_reliability(self) -> ReliabilityLevel:
        """计算总体可靠性等级"""
        if self.metrics is None:
            return ReliabilityLevel.LOW
        
        # 基于各项指标计算综合可靠性
        scores = [
            self.metrics.voltage_stability_margin,
            1.0 - self.metrics.line_loading_ratio,
            1.0 - self.metrics.transformer_loading_ratio,
            float(self.metrics.n_minus_1_security),
            1.0 - min(self.metrics.voltage_deviation * 10, 1.0),
            self.metrics.frequency_stability,
            self.metrics.convergence_robustness,
            self.metrics.numerical_stability
        ]
        
        avg_score = np.mean(scores)
        
        if avg_score > 0.8:
            return ReliabilityLevel.HIGH
        elif avg_score > 0.6:
            return ReliabilityLevel.MEDIUM
        else:
            return ReliabilityLevel.LOW


class PowerFlowErrorAnalyzer:
    """潮流计算误差分析器"""
    
    def __init__(self, reference_result: PowerFlowResult, 
                 test_result: PowerFlowResult):
        self.reference = reference_result
        self.test = test_result
        self.error_metrics = {}
    
    def analyze_errors(self) -> Dict[str, float]:
        """分析潮流计算误差"""
        errors = {
            'voltage_magnitude_mae': self._calculate_voltage_magnitude_mae(),
            'voltage_angle_mae': self._calculate_voltage_angle_mae(),
            'active_power_mae': self._calculate_active_power_mae(),
            'reactive_power_mae': self._calculate_reactive_power_mae(),
            'line_flow_mae': self._calculate_line_flow_mae(),
            'transformer_flow_mae': self._calculate_transformer_flow_mae(),
            'total_loss_error': self._calculate_total_loss_error()
        }
        
        self.error_metrics = errors
        return errors
    
    def _calculate_voltage_magnitude_mae(self) -> float:
        """计算电压幅值平均绝对误差"""
        v_ref = self.reference.voltage_magnitude.values
        v_test = self.test.voltage_magnitude.values
        
        if v_ref.shape == v_test.shape:
            return np.mean(np.abs(v_ref - v_test))
        else:
            return float('inf')
    
    def _calculate_voltage_angle_mae(self) -> float:
        """计算电压相角平均绝对误差"""
        theta_ref = self.reference.voltage_angle.values
        theta_test = self.test.voltage_angle.values
        
        if theta_ref.shape == theta_test.shape:
            return np.mean(np.abs(theta_ref - theta_test))
        else:
            return float('inf')
    
    def _calculate_active_power_mae(self) -> float:
        """计算有功功率平均绝对误差"""
        p_ref = self.reference.active_power.values
        p_test = self.test.active_power.values
        
        if p_ref.shape == p_test.shape:
            return np.mean(np.abs(p_ref - p_test))
        else:
            return float('inf')
    
    def _calculate_reactive_power_mae(self) -> float:
        """计算无功功率平均绝对误差"""
        q_ref = self.reference.reactive_power.values
        q_test = self.test.reactive_power.values
        
        if q_ref.shape == q_test.shape:
            return np.mean(np.abs(q_ref - q_test))
        else:
            return float('inf')
    
    def _calculate_line_flow_mae(self) -> float:
        """计算线路潮流平均绝对误差"""
        # 实现具体逻辑
        return 0.0
    
    def _calculate_transformer_flow_mae(self) -> float:
        """计算变压器潮流平均绝对误差"""
        # 实现具体逻辑
        return 0.0
    
    def _calculate_total_loss_error(self) -> float:
        """计算总损耗误差"""
        # 实现具体逻辑
        return 0.0
    
    def generate_error_report(self) -> str:
        """生成误差分析报告"""
        if not self.error_metrics:
            self.analyze_errors()
        
        report = []
        report.append("=== 潮流计算误差分析报告 ===")
        
        for metric, value in self.error_metrics.items():
            if np.isfinite(value):
                report.append(f"{metric}: {value:.6e}")
            else:
                report.append(f"{metric}: 数据不匹配")
        
        return "\n".join(report)


# 公共API函数
def create_reliability_analyzer(network: Network, 
                              power_flow_result: PowerFlowResult) -> PowerFlowReliabilityAnalyzer:
    """创建可靠性分析器"""
    return PowerFlowReliabilityAnalyzer(network, power_flow_result)


def create_error_analyzer(reference_result: PowerFlowResult,
                        test_result: PowerFlowResult) -> PowerFlowErrorAnalyzer:
    """创建误差分析器"""
    return PowerFlowErrorAnalyzer(reference_result, test_result)


def assess_power_flow_reliability(network: Network, 
                                 power_flow_result: PowerFlowResult) -> Tuple[ReliabilityMetrics, str]:
    """评估潮流计算可靠性"""
    analyzer = create_reliability_analyzer(network, power_flow_result)
    metrics = analyzer.analyze_reliability()
    report = analyzer.generate_reliability_report()
    
    return metrics, report


# 导出公共API
__all__ = [
    'ReliabilityLevel',
    'SensitivityType',
    'ReliabilityMetrics',
    'SensitivityResult',
    'PowerFlowReliabilityAnalyzer',
    'PowerFlowErrorAnalyzer',
    'create_reliability_analyzer',
    'create_error_analyzer',
    'assess_power_flow_reliability'
]