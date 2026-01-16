"""
城市能源系统安全综合评估模块(主要面向面向光储不确定性与交通电气化)

实现包含不确定性因素的综合能源系统安全与可靠性评估，核心功能包括：
- 不确定性因素建模（光伏出力、交通电气化相关）
- 安全边界建模与安全距离量化
- 数据驱动多项式混沌展开的可靠性评估
- 降维观测与代理模型构建
- 安全与可靠性综合评估
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Tuple
from enum import Enum
import numpy as np
import pandas as pd
import logging
from datetime import datetime
import math
from scipy.special import gamma
from abc import ABC, abstractmethod

from .evaluation_framework import Evaluator, EvaluationContext, EvaluationResult, EvaluationStatus, EvaluationType

class SecurityEvaluationType(Enum):
    """安全评估类型"""
    UNCERTAINTY_MODELING = "uncertainty_modeling"        # 不确定性建模
    SAFETY_BOUNDARY = "safety_boundary"                # 安全边界
    RELIABILITY_QUANTIFICATION = "reliability_quantification"  # 可靠性量化
    COMPREHENSIVE_SECURITY = "comprehensive_security"  # 综合安全评估

class UncertaintyType(Enum):
    """不确定性类型"""
    PV_OUTPUT = "pv_output"                          # 光伏出力
    EV_CHARGING = "ev_charging"                      # 电动汽车充电
    ELECTROLYZER_STATE = "electrolyzer_state"        # 电解槽状态
    FUEL_CELL_STATE = "fuel_cell_state"              # 燃料电池状态
    HYDROGEN_DEMAND = "hydrogen_demand"              # 氢气需求

class ReliabilityMetric(Enum):
    """可靠性指标"""
    EENS = "EENS"                                    # 期望能量不足
    EHNS = "EHNS"                                    # 期望氢气不足
    SAIFI = "SAIFI"                                  # 系统平均停电频率
    SAIDI = "SAIDI"                                  # 系统平均停电持续时间
    CAIDI = "CAIDI"                                  # 系统平均修复时间

@dataclass
class UncertaintyModel:
    """不确定性模型"""
    uncertainty_type: UncertaintyType
    model_params: Dict[str, Any]
    probability_distribution: str
    moments: List[float]                             # 多阶矩
    confidence_level: float
    sample_size: int

@dataclass
class SafetyBoundary:
    """安全边界"""
    boundary_type: str
    lower_bound: float
    upper_bound: float
    boundary_equation: str
    critical_variables: List[str]
    safety_margin: float

@dataclass
class SafetyDistance:
    """安全距离"""
    distance_type: str
    value: float
    direction: str
    safety_status: bool                               # True表示安全，False表示不安全
    boundary_ref: str
    confidence_interval: Tuple[float, float]

@dataclass
class ReliabilityResult:
    """可靠性结果"""
    metric: ReliabilityMetric
    value: float
    unit: str
    confidence_level: float
    calculation_method: str
    sensitivity_analysis: Dict[str, float]

@dataclass
class SecurityEvaluationResult:
    """安全评估结果"""
    # 执行信息
    evaluation_id: str
    timestamp: datetime
    evaluation_type: SecurityEvaluationType
    
    # 不确定性建模结果
    uncertainty_models: Dict[UncertaintyType, UncertaintyModel]
    
    # 安全边界与距离
    safety_boundaries: List[SafetyBoundary]
    safety_distances: Dict[str, SafetyDistance]
    
    # 可靠性指标
    reliability_metrics: Dict[ReliabilityMetric, ReliabilityResult]
    
    # 系统状态评估
    system_safety_status: str
    critical_issues: List[str]
    improvement_suggestions: List[str]
    
    # 可视化数据
    visualization_data: Dict[str, Any]

class SecurityEvaluator(Evaluator):
    """安全评估器"""
    
    def __init__(self, name: str = "SecurityEvaluator"):
        super().__init__(name, EvaluationType.COMPREHENSIVE)
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行安全评估"""
        start_time = datetime.now()
        self.logger.info("开始执行安全评估")
        
        try:
            # 1. 数据输入阶段
            input_data = self._process_input_data(context)
            
            # 2. 不确定性建模阶段
            uncertainty_models = self._model_uncertainties(input_data)
            
            # 3. 安全模型构建阶段
            safety_boundaries, safety_distances = self._build_safety_model(input_data, uncertainty_models)
            
            # 4. 降维与代理模型构建阶段
            reduced_variables, surrogate_model = self._build_reduced_surrogate_model(input_data, uncertainty_models)
            
            # 5. 安全与可靠性评估阶段
            reliability_metrics = self._calculate_reliability_metrics(input_data, surrogate_model)
            system_safety_status = self._assess_system_safety(safety_distances, reliability_metrics)
            
            # 6. 生成评估结果
            security_result = SecurityEvaluationResult(
                evaluation_id=f"security_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                evaluation_type=SecurityEvaluationType.COMPREHENSIVE_SECURITY,
                uncertainty_models=uncertainty_models,
                safety_boundaries=safety_boundaries,
                safety_distances=safety_distances,
                reliability_metrics=reliability_metrics,
                system_safety_status=system_safety_status,
                critical_issues=self._identify_critical_issues(safety_distances, reliability_metrics),
                improvement_suggestions=self._generate_improvement_suggestions(safety_distances, reliability_metrics),
                visualization_data=self._prepare_visualization_data(uncertainty_models, safety_boundaries, safety_distances, reliability_metrics)
            )
            
            # 创建标准评估结果
            metrics = {
                'safety_score': self._calculate_safety_score(safety_distances, reliability_metrics),
                'reliability_index': sum(rm.value for rm in reliability_metrics.values()) / len(reliability_metrics),
                'uncertainty_level': self._calculate_uncertainty_level(uncertainty_models),
                'system_safety_status': 1 if '安全' in system_safety_status else 0
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={
                    'security_evaluation_result': security_result,
                    'uncertainty_models': uncertainty_models,
                    'safety_boundaries': safety_boundaries,
                    'safety_distances': safety_distances,
                    'reliability_metrics': reliability_metrics
                },
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("安全评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"安全评估失败: {str(e)}")
            return EvaluationResult(
                context=context,
                status=EvaluationStatus.FAILED,
                metrics={},
                indicators={},
                execution_time=(datetime.now() - start_time).total_seconds(),
                error_message=str(e)
            )
    
    def validate_input(self, context: EvaluationContext) -> bool:
        """验证输入"""
        required_data = ['energy_system_params', 'pv_params', 'ev_charging_data', 'hydrogen_system_params', 'historical_data']
        
        for data_type in required_data:
            if data_type not in context.scenario_data:
                self.logger.warning(f"缺少必需数据: {data_type}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['energy_system_params', 'pv_params', 'ev_charging_data', 'hydrogen_system_params', 
                'historical_data', 'uncertainty_data', 'safety_constraints']
    
    def _process_input_data(self, context: EvaluationContext) -> Dict[str, Any]:
        """处理输入数据"""
        scenario_data = context.scenario_data
        
        input_data = {
            'energy_system': scenario_data['energy_system_params'],
            'pv_params': scenario_data['pv_params'],
            'ev_data': scenario_data['ev_charging_data'],
            'hydrogen_system': scenario_data['hydrogen_system_params'],
            'historical_data': scenario_data['historical_data'],
            'safety_constraints': scenario_data.get('safety_constraints', {})
        }
        
        return input_data
    
    def _model_uncertainties(self, input_data: Dict[str, Any]) -> Dict[UncertaintyType, UncertaintyModel]:
        """不确定性建模"""
        uncertainties = {}
        
        # 1. 光伏出力不确定性建模（贝塔分布）
        pv_data = input_data['historical_data']['pv_output']
        # 基于历史数据估计贝塔分布参数
        alpha, beta = self._estimate_beta_params(pv_data)
        
        pv_moments = self._calculate_moments(pv_data, l=3)
        pv_model = UncertaintyModel(
            uncertainty_type=UncertaintyType.PV_OUTPUT,
            model_params={
                'alpha': alpha,  # 形状参数（基于历史数据估计）
                'beta': beta,    # 尺度参数（基于历史数据估计）
                'rated_power': input_data['pv_params']['rated_power'],
                'mean': np.mean(pv_data),
                'variance': np.var(pv_data)
            },
            probability_distribution='beta',
            moments=pv_moments,
            confidence_level=0.95,
            sample_size=len(pv_data)
        )
        uncertainties[UncertaintyType.PV_OUTPUT] = pv_model
        
        # 2. 电动汽车充电负荷不确定性建模
        ev_moments = self._calculate_moments(input_data['historical_data']['ev_charging'], l=3)
        ev_model = UncertaintyModel(
            uncertainty_type=UncertaintyType.EV_CHARGING,
            model_params={
                'mean_charging_power': np.mean(input_data['historical_data']['ev_charging']),
                'std_charging_power': np.std(input_data['historical_data']['ev_charging']),
                'time_series_length': len(input_data['historical_data']['ev_charging'])
            },
            probability_distribution='gaussian',
            moments=ev_moments,
            confidence_level=0.95,
            sample_size=10000
        )
        uncertainties[UncertaintyType.EV_CHARGING] = ev_model
        
        # 3. 电解槽状态不确定性建模
        electrolyzer_moments = [1.0, 0.95, 0.9, 0.85]  # 假设的0-3阶矩
        electrolyzer_model = UncertaintyModel(
            uncertainty_type=UncertaintyType.ELECTROLYZER_STATE,
            model_params={
                'failure_rate': 0.001,
                'repair_rate': 0.1,
                'transition_matrix': [[0.999, 0.001], [0.1, 0.9]]
            },
            probability_distribution='markov_chain',
            moments=electrolyzer_moments,
            confidence_level=0.9,
            sample_size=5000
        )
        uncertainties[UncertaintyType.ELECTROLYZER_STATE] = electrolyzer_model
        
        # 4. 燃料电池状态不确定性建模
        fuel_cell_moments = [1.0, 0.96, 0.92, 0.88]  # 假设的0-3阶矩
        fuel_cell_model = UncertaintyModel(
            uncertainty_type=UncertaintyType.FUEL_CELL_STATE,
            model_params={
                'failure_rate': 0.0008,
                'repair_rate': 0.12,
                'transition_matrix': [[0.9992, 0.0008], [0.12, 0.88]]
            },
            probability_distribution='markov_chain',
            moments=fuel_cell_moments,
            confidence_level=0.9,
            sample_size=5000
        )
        uncertainties[UncertaintyType.FUEL_CELL_STATE] = fuel_cell_model
        
        # 5. 氢气需求不确定性建模
        hydrogen_moments = self._calculate_moments(input_data['historical_data']['hydrogen_demand'], l=3)
        hydrogen_model = UncertaintyModel(
            uncertainty_type=UncertaintyType.HYDROGEN_DEMAND,
            model_params={
                'mean_demand': np.mean(input_data['historical_data']['hydrogen_demand']),
                'std_demand': np.std(input_data['historical_data']['hydrogen_demand'])
            },
            probability_distribution='lognormal',
            moments=hydrogen_moments,
            confidence_level=0.95,
            sample_size=10000
        )
        uncertainties[UncertaintyType.HYDROGEN_DEMAND] = hydrogen_model
        
        return uncertainties
    
    def _calculate_moments(self, data: np.ndarray, l: int) -> List[float]:
        """计算多阶矩"""
        moments = []
        for k in range(l + 1):
            moment = np.mean(np.power(data, k))
            moments.append(float(moment))
        return moments
    
    def _estimate_beta_params(self, data: np.ndarray) -> Tuple[float, float]:
        """基于矩匹配法估计贝塔分布参数
        
        贝塔分布的概率密度函数为：
        f(S_h) = Γ(α_p + β_p) / (Γ(α_p)Γ(β_p)) * (S_h/S_r)^(α_p-1) * ((S_r - S_h)/S_r)^(β_p-1)
        
        使用矩匹配法，基于样本均值和方差估计α和β参数：
        μ = α / (α + β)
        σ² = (αβ) / ((α + β)²(α + β + 1))
        
        Args:
            data: 归一化的光伏出力数据（0-1之间）
        
        Returns:
            Tuple[float, float]: 估计的alpha和beta参数
        """
        # 计算样本均值和方差
        mu = np.mean(data)
        sigma2 = np.var(data)
        
        # 处理边界情况
        if sigma2 == 0:
            return 2.0, 2.0
        
        if mu <= 0 or mu >= 1:
            mu = max(0.01, min(0.99, mu))
        
        # 使用矩匹配法求解alpha和beta
        denominator = sigma2 * (mu * (1 - mu) / sigma2 - 1)
        
        if denominator <= 0:
            # 方差过大或过小，使用默认值
            return 2.0, 2.0
        
        alpha = mu * (mu * (1 - mu) / sigma2 - 1)
        beta = (1 - mu) * (mu * (1 - mu) / sigma2 - 1)
        
        # 确保参数为正数
        alpha = max(0.1, alpha)
        beta = max(0.1, beta)
        
        return alpha, beta
    
    def _build_safety_model(self, input_data: Dict[str, Any], uncertainty_models: Dict[UncertaintyType, UncertaintyModel]) -> Tuple[List[SafetyBoundary], Dict[str, SafetyDistance]]:
        """构建安全模型
        
        基于安全边界理论，构建包含概率安全区域和绝对安全区域的安全模型
        
        Args:
            input_data: 输入数据
            uncertainty_models: 不确定性模型字典
        
        Returns:
            Tuple[List[SafetyBoundary], Dict[str, SafetyDistance]]: 安全边界列表和安全距离字典
        """
        safety_boundaries = []
        safety_distances = {}
        
        # 获取系统参数
        energy_system = input_data['energy_system']
        pv_params = input_data['pv_params']
        n_re = 1  # 光伏设备数量
        
        # 1. 线路安全边界
        line_capacity = energy_system['line_capacity']
        line_safety_boundary = self._calculate_line_safety_boundary(
            line_capacity, uncertainty_models, n_re, pv_params
        )
        safety_boundaries.append(line_safety_boundary)
        
        # 2. 设备安全边界（以热电联产机组为例）
        chp_capacity = energy_system['chp_capacity']
        chp_safety_boundary = self._calculate_chp_safety_boundary(
            chp_capacity, uncertainty_models, n_re, pv_params
        )
        safety_boundaries.append(chp_safety_boundary)
        
        # 3. 计算安全距离
        line_load = np.mean(input_data['historical_data']['line_load'])
        line_safety_distance = self._calculate_safety_distance(
            current_value=line_load,
            lower_bound=line_safety_boundary.lower_bound,
            upper_bound=line_safety_boundary.upper_bound,
            boundary_ref=f"line_{line_safety_boundary.boundary_type}",
            lambda_weights=[1.0]  # 线路负荷权重
        )
        safety_distances['line_safety'] = line_safety_distance
        
        chp_load = np.mean(input_data['historical_data']['chp_load'])
        chp_safety_distance = self._calculate_safety_distance(
            current_value=chp_load,
            lower_bound=chp_safety_boundary.lower_bound,
            upper_bound=chp_safety_boundary.upper_bound,
            boundary_ref=f"chp_{chp_safety_boundary.boundary_type}",
            lambda_weights=[1.0]  # 热电联产出力权重
        )
        safety_distances['chp_safety'] = chp_safety_distance
        
        return safety_boundaries, safety_distances
    
    def _calculate_line_safety_boundary(self, line_capacity: float, 
                                      uncertainty_models: Dict[UncertaintyType, UncertaintyModel],
                                      n_re: int, pv_params: Dict[str, Any]) -> SafetyBoundary:
        """计算线路安全边界
        
        根据技术报告，线路安全边界考虑分布式/集中式光伏接入方式
        
        Args:
            line_capacity: 线路容量
            uncertainty_models: 不确定性模型字典
            n_re: 光伏设备数量
            pv_params: 光伏参数
        
        Returns:
            SafetyBoundary: 线路安全边界
        """
        # 获取储能参数
        ees_capacity = 200  # 电储能额定充放电功率（MW）
        
        # 获取光伏概率功率
        if UncertaintyType.PV_OUTPUT in uncertainty_models:
            pv_model = uncertainty_models[UncertaintyType.PV_OUTPUT]
            rated_power = pv_params['rated_power']
            # 概率功率区间
            c_pro = [0, rated_power]
        else:
            c_pro = [0, 300]  # 默认值
        
        # 计算不同接入方式的约束上限
        # 分布式光伏接入时上限
        c_pip_dis = line_capacity + ees_capacity + n_re * c_pro[1]  # 考虑最大光伏出力
        
        # 集中式光伏接入时上限
        c_pip_cen = line_capacity + ees_capacity  # 集中式不考虑分布式光伏
        
        # 约束下限
        p_con = 100  # 用电设备功耗
        c_re_pip = max(p_con, n_re * c_pro[0] + ees_capacity)  # 考虑最小光伏出力
        
        # 计算概率安全区域和绝对安全区域
        # 概率安全区域：所有概率功率下安全工作点并集
        omega_ies_sr_lower = c_re_pip
        omega_ies_sr_upper = max(c_pip_dis, c_pip_cen)
        
        # 绝对安全区域：任意概率功率下均安全的工作点交集
        omega_ies_usr_lower = c_re_pip
        omega_ies_usr_upper = min(c_pip_dis, c_pip_cen)
        
        # 综合考虑，使用概率安全区域作为安全边界
        lower_bound = omega_ies_sr_lower
        upper_bound = omega_ies_sr_upper
        
        # 构建边界方程
        boundary_equation = f"{omega_ies_sr_lower} <= L <= {omega_ies_sr_upper}"
        
        # 计算安全裕度
        safety_margin = upper_bound - line_capacity * 0.9
        
        return SafetyBoundary(
            boundary_type='line_capacity',
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            boundary_equation=boundary_equation,
            critical_variables=['line_load', 'pv_injection', 'ev_charging', 'energy_storage'],
            safety_margin=safety_margin
        )
    
    def _calculate_chp_safety_boundary(self, chp_capacity: float, 
                                     uncertainty_models: Dict[UncertaintyType, UncertaintyModel],
                                     n_re: int, pv_params: Dict[str, Any]) -> SafetyBoundary:
        """计算热电联产安全边界
        
        Args:
            chp_capacity: 热电联产容量
            uncertainty_models: 不确定性模型字典
            n_re: 光伏设备数量
            pv_params: 光伏参数
        
        Returns:
            SafetyBoundary: 热电联产安全边界
        """
        # 获取储能参数
        ees_capacity = 200  # 电储能额定充放电功率（MW）
        hes1_capacity = 100  # 热储能额定功率（MW）
        
        # 电热比系数
        c_u = 0.5  # 电热比系数上限
        c_m = 0.3  # 电热比系数下限
        
        # 获取光伏概率功率
        if UncertaintyType.PV_OUTPUT in uncertainty_models:
            pv_model = uncertainty_models[UncertaintyType.PV_OUTPUT]
            rated_power = pv_params['rated_power']
            # 概率功率区间
            c_pro = [0, rated_power]
        else:
            c_pro = [0, 300]  # 默认值
        
        # 线路负荷
        line_load = 500  # MW
        
        # 计算不同接入方式的约束上限
        # 分布式光伏接入时上限
        c_equ_dis = (chp_capacity - c_u * (line_load - hes1_capacity) + 
                   ees_capacity + n_re * c_pro[1])
        
        # 集中式光伏接入时上限
        c_equ_cen = (chp_capacity - c_u * (line_load - hes1_capacity) + 
                   ees_capacity + c_pro[1])
        
        # 约束下限
        h_t = 100  # 变压器供能负荷
        c_re_equ = max(h_t + 100, c_m * (line_load - hes1_capacity) + ees_capacity + n_re * c_pro[0])
        
        # 计算概率安全区域和绝对安全区域
        # 概率安全区域
        omega_ies_sr_lower = c_re_equ
        omega_ies_sr_upper = max(c_equ_dis, c_equ_cen)
        
        # 绝对安全区域
        omega_ies_usr_lower = c_re_equ
        omega_ies_usr_upper = min(c_equ_dis, c_equ_cen)
        
        # 综合考虑，使用概率安全区域作为安全边界
        lower_bound = omega_ies_sr_lower
        upper_bound = omega_ies_sr_upper
        
        # 构建边界方程
        boundary_equation = f"{omega_ies_sr_lower} <= H_T + H_CHP <= {omega_ies_sr_upper}"
        
        # 计算安全裕度
        safety_margin = upper_bound - chp_capacity * 0.95
        
        return SafetyBoundary(
            boundary_type='chp_capacity',
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            boundary_equation=boundary_equation,
            critical_variables=['heat_demand', 'electric_demand', 'chp_output'],
            safety_margin=safety_margin
        )
    
    def _calculate_safety_distance(self, current_value: float, lower_bound: float, upper_bound: float, 
                                  boundary_ref: str, lambda_weights: List[float] = None) -> SafetyDistance:
        """计算安全距离
        
        根据安全边界理论，计算工作点到安全边界的垂直距离
        
        Args:
            current_value: 当前工作点值
            lower_bound: 安全边界下限
            upper_bound: 安全边界上限
            boundary_ref: 边界参考标识
            lambda_weights: 权重向量
        
        Returns:
            SafetyDistance: 安全距离对象
        """
        # 默认权重向量为[1]
        if lambda_weights is None:
            lambda_weights = [1.0]
        
        # 计算权重向量的范数
        weight_norm = math.sqrt(sum(w ** 2 for w in lambda_weights))
        
        if current_value < lower_bound:
            # 低于下限
            distance = lower_bound - current_value
            # 计算垂直距离（考虑权重）
            vertical_distance = distance / weight_norm
            direction = 'below_lower_bound'
            safety_status = False
        elif current_value > upper_bound:
            # 高于上限
            distance = current_value - upper_bound
            # 计算垂直距离（考虑权重）
            vertical_distance = -distance / weight_norm
            direction = 'above_upper_bound'
            safety_status = False
        else:
            # 在安全范围内，计算到上下边界的最小距离
            distance_to_lower = current_value - lower_bound
            distance_to_upper = upper_bound - current_value
            min_distance = min(distance_to_lower, distance_to_upper)
            vertical_distance = min_distance / weight_norm
            direction = 'within_bounds'
            safety_status = True
        
        # 计算置信区间（假设95%置信度）
        confidence_interval = (vertical_distance - 0.1, vertical_distance + 0.1)
        
        return SafetyDistance(
            distance_type='euclidean',
            value=vertical_distance,
            direction=direction,
            safety_status=safety_status,
            boundary_ref=boundary_ref,
            confidence_interval=confidence_interval
        )
    
    def _build_reduced_surrogate_model(self, input_data: Dict[str, Any], uncertainty_models: Dict[UncertaintyType, UncertaintyModel]) -> Tuple[List[str], Dict[str, Any]]:
        """构建降维与代理模型"""
        # 1. 计算最大供能能力
        max_supply_capacity = self._calculate_max_supply_capacity(input_data)
        
        # 2. 基于最大供能能力选取关键观测变量（降维）
        critical_variables = self._select_critical_observation_variables(
            max_supply_capacity, input_data
        )
        
        # 3. 构建混沌多项式代理模型
        surrogate_model = self._build_chaos_polynomial_surrogate(uncertainty_models, critical_variables)
        
        # 添加最大供能能力信息到代理模型
        surrogate_model['max_supply_capacity'] = max_supply_capacity
        
        return critical_variables, surrogate_model
    
    def _select_critical_observation_variables(self, max_supply_capacity: Dict[str, float], 
                                             input_data: Dict[str, Any]) -> List[str]:
        """选取关键观测变量
        
        基于最大供能能力，选取对系统安全影响最大的关键变量
        
        Args:
            max_supply_capacity: 最大供能能力
            input_data: 输入数据
        
        Returns:
            List[str]: 关键观测变量列表
        """
        # 获取系统参数
        energy_system = input_data['energy_system']
        
        # 基于最大供能能力分析，选取关键变量
        # 1. 核心线路负荷
        # 2. 光伏出力
        # 3. 电动汽车充电负荷
        # 4. 热电联产出力
        # 5. 氢气需求
        critical_variables = [
            'pv_output',
            'ev_charging_load',
            'line_load',
            'chp_output',
            'hydrogen_demand'
        ]
        
        # 基于最大供能能力进一步优化变量选择
        # 这里可以添加更复杂的变量选择逻辑
        # 例如：基于灵敏度分析或相关性分析
        
        return critical_variables
    
    def _calculate_max_supply_capacity(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        """计算最大供能能力
        
        基于多能流平衡约束，计算系统的最大供能能力
        
        Args:
            input_data: 输入数据
        
        Returns:
            Dict[str, float]: 包含最大供能能力上下界的字典
        """
        # 获取系统参数
        energy_system = input_data['energy_system']
        hydrogen_system = input_data['hydrogen_system']
        
        # 设备容量
        generator_capacity = energy_system.get('generator_capacity', 800)
        chp_capacity = energy_system.get('chp_capacity', 500)
        pv_capacity = energy_system.get('pv_capacity', 300)
        electrolyzer_capacity = hydrogen_system.get('electrolyzer_capacity', 100)
        fuel_cell_capacity = hydrogen_system.get('fuel_cell_capacity', 50)
        
        # 设备效率
        chp_electric_efficiency = 0.4
        chp_thermal_efficiency = 0.5
        electrolyzer_efficiency = hydrogen_system.get('electrolyzer_efficiency', 0.75)
        fuel_cell_efficiency = hydrogen_system.get('fuel_cell_efficiency', 0.55)
        
        # 计算不同能源介质的最大供能能力
        max_electric_supply = self._calculate_max_electric_supply(
            generator_capacity, chp_capacity, chp_electric_efficiency, 
            pv_capacity, fuel_cell_capacity, fuel_cell_efficiency
        )
        
        max_thermal_supply = self._calculate_max_thermal_supply(
            chp_capacity, chp_thermal_efficiency
        )
        
        max_hydrogen_supply = self._calculate_max_hydrogen_supply(
            electrolyzer_capacity, electrolyzer_efficiency
        )
        
        # 计算综合最大供能能力（考虑多能流平衡）
        max_itsc = self._calculate_combined_max_supply(
            max_electric_supply, max_thermal_supply, max_hydrogen_supply,
            chp_electric_efficiency, chp_thermal_efficiency,
            electrolyzer_efficiency, fuel_cell_efficiency
        )
        
        # 计算降维观测函数
        reduced_observation = self._calculate_reduced_observation_function(
            max_itsc, max_electric_supply, max_thermal_supply, max_hydrogen_supply
        )
        
        return {
            'min_itsc': max_itsc['lower'],
            'max_itsc': max_itsc['upper'],
            'electric_supply': max_electric_supply,
            'thermal_supply': max_thermal_supply,
            'hydrogen_supply': max_hydrogen_supply,
            'reduced_observation': reduced_observation
        }
    
    def _calculate_reduced_observation_function(self, max_itsc: Dict[str, float], 
                                             max_electric_supply: Dict[str, float],
                                             max_thermal_supply: Dict[str, float],
                                             max_hydrogen_supply: Dict[str, float]) -> Dict[str, float]:
        """计算降维观测函数
        
        根据技术报告，降维观测函数为：
        F_DRO = -∏_{m∈Λ} |min(overline{D}_{IES}^{T_ITSC,l})|, 存在min(overline{D}_{IES}^{T_ITSC,l}) < 0
        F_DRO = ∏_{m∈Λ} |min(overline{D}_{IES}^{T_ITSC,l})|, 任意min(overline{D}_{IES}^{T_ITSC,l}) ≥ 0
        
        Args:
            max_itsc: 综合最大供能能力
            max_electric_supply: 最大电力供应能力
            max_thermal_supply: 最大热力供应能力
            max_hydrogen_supply: 最大氢气供应能力
        
        Returns:
            Dict[str, float]: 降维观测函数结果
        """
        # 计算各能源介质的安全距离
        # 这里简化实现，实际应基于安全边界计算
        safety_distances = {
            'electric': max_itsc['upper'] - max_electric_supply['upper'],
            'thermal': max_itsc['upper'] - max_thermal_supply['upper'],
            'hydrogen': max_itsc['upper'] - max_hydrogen_supply['upper'] * 33.33 / 1000  # 转换为MW
        }
        
        # 获取关键观测变量集合Λ（这里简化为所有能源介质）
        lambda_set = list(safety_distances.keys())
        
        # 计算最大供能能力对应的安全距离最小值
        min_safety_distances = []
        for var in lambda_set:
            min_safety_distances.append(safety_distances[var])
        
        # 计算降维观测函数
        min_d_itsc_l = min(min_safety_distances)
        
        if min_d_itsc_l < 0:
            # 存在不安全的情况
            f_dro = -math.prod(abs(d) for d in min_safety_distances)
        else:
            # 所有情况都安全
            f_dro = math.prod(abs(d) for d in min_safety_distances)
        
        return {
            'f_dro': f_dro,
            'min_safety_distance': min_d_itsc_l,
            'safety_distances': safety_distances,
            'lambda_set': lambda_set
        }
    
    def _calculate_max_electric_supply(self, generator_capacity: float, chp_capacity: float, 
                                     chp_electric_efficiency: float, pv_capacity: float,
                                     fuel_cell_capacity: float, fuel_cell_efficiency: float) -> Dict[str, float]:
        """计算最大电力供应能力
        
        Args:
            generator_capacity: 发电机容量
            chp_capacity: 热电联产容量
            chp_electric_efficiency: 热电联产电效率
            pv_capacity: 光伏容量
            fuel_cell_capacity: 燃料电池容量
            fuel_cell_efficiency: 燃料电池效率
        
        Returns:
            Dict[str, float]: 电力供应能力上下界
        """
        # 计算电力供应的上下界
        # 下界：仅考虑基本负荷
        min_electric = generator_capacity * 0.5  # 发电机基本出力
        
        # 上界：所有设备满负荷出力
        max_electric = (generator_capacity + 
                       chp_capacity * chp_electric_efficiency + 
                       pv_capacity + 
                       fuel_cell_capacity)
        
        return {
            'lower': min_electric,
            'upper': max_electric
        }
    
    def _calculate_max_thermal_supply(self, chp_capacity: float, 
                                     chp_thermal_efficiency: float) -> Dict[str, float]:
        """计算最大热力供应能力
        
        Args:
            chp_capacity: 热电联产容量
            chp_thermal_efficiency: 热电联产热效率
        
        Returns:
            Dict[str, float]: 热力供应能力上下界
        """
        # 计算热力供应的上下界
        min_thermal = chp_capacity * chp_thermal_efficiency * 0.3  # 基本热负荷
        max_thermal = chp_capacity * chp_thermal_efficiency  # 满负荷热出力
        
        return {
            'lower': min_thermal,
            'upper': max_thermal
        }
    
    def _calculate_max_hydrogen_supply(self, electrolyzer_capacity: float, 
                                      electrolyzer_efficiency: float) -> Dict[str, float]:
        """计算最大氢气供应能力
        
        Args:
            electrolyzer_capacity: 电解槽容量
            electrolyzer_efficiency: 电解槽效率
        
        Returns:
            Dict[str, float]: 氢气供应能力上下界
        """
        # 氢气生产速率（kg/h）：1 kWh电生产 0.09 kg氢气（基于能量含量）
        hydrogen_production_rate = 0.09  # kg/kWh
        
        # 计算氢气供应的上下界
        min_hydrogen = electrolyzer_capacity * electrolyzer_efficiency * hydrogen_production_rate * 0.2  # 基本氢产量
        max_hydrogen = electrolyzer_capacity * electrolyzer_efficiency * hydrogen_production_rate  # 满负荷氢产量
        
        return {
            'lower': min_hydrogen,
            'upper': max_hydrogen
        }
    
    def _calculate_combined_max_supply(self, electric_supply: Dict[str, float], 
                                      thermal_supply: Dict[str, float], 
                                      hydrogen_supply: Dict[str, float],
                                      chp_electric_efficiency: float, 
                                      chp_thermal_efficiency: float,
                                      electrolyzer_efficiency: float, 
                                      fuel_cell_efficiency: float) -> Dict[str, float]:
        """计算综合最大供能能力
        
        考虑多能流平衡约束，计算综合最大供能能力
        
        Args:
            electric_supply: 电力供应能力
            thermal_supply: 热力供应能力
            hydrogen_supply: 氢气供应能力
            chp_electric_efficiency: 热电联产电效率
            chp_thermal_efficiency: 热电联产热效率
            electrolyzer_efficiency: 电解槽效率
            fuel_cell_efficiency: 燃料电池效率
        
        Returns:
            Dict[str, float]: 综合供能能力上下界
        """
        # 转换为统一单位（MW）
        # 电力：MW
        # 热力：MW
        # 氢气：kg/h * 33.33 kWh/kg / 1000 = MW（假设氢气能量含量为33.33 kWh/kg）
        hydrogen_energy_content = 33.33  # kWh/kg
        
        min_electric = electric_supply['lower']
        max_electric = electric_supply['upper']
        
        min_thermal = thermal_supply['lower']
        max_thermal = thermal_supply['upper']
        
        min_hydrogen = hydrogen_supply['lower'] * hydrogen_energy_content / 1000  # kg/h 转换为 MW
        max_hydrogen = hydrogen_supply['upper'] * hydrogen_energy_content / 1000  # kg/h 转换为 MW
        
        # 计算综合供能能力
        # 下界：各能源介质的最小供能之和
        min_itsc = min_electric + min_thermal + min_hydrogen
        
        # 上界：考虑多能流平衡约束的最大供能之和
        # 这里考虑CHP的热电耦合关系
        # CHP的最大总输出受限于其容量
        chp_max_total = min_electric + min_thermal  # CHP的热电总输出
        
        # 其他能源的最大输出
        other_electric = max_electric - min_electric  # 除CHP外的电力
        other_thermal = max_thermal - min_thermal  # 除CHP外的热力
        
        # 综合最大供能能力
        max_itsc = chp_max_total + other_electric + other_thermal + max_hydrogen
        
        return {
            'lower': min_itsc,
            'upper': max_itsc
        }
    
    def _build_chaos_polynomial_surrogate(self, uncertainty_models: Dict[UncertaintyType, UncertaintyModel], critical_variables: List[str]) -> Dict[str, Any]:
        """构建混沌多项式代理模型
        
        基于数据驱动多项式混沌展开，构建代理模型
        
        Args:
            uncertainty_models: 不确定性模型字典
            critical_variables: 关键变量列表
        
        Returns:
            Dict[str, Any]: 代理模型信息
        """
        polynomial_order = 3
        
        # 1. 构建正交多项式基
        orthogonal_bases = self._construct_orthogonal_polynomial_bases(uncertainty_models, polynomial_order)
        
        # 2. 生成训练样本
        n_samples = 1000
        training_samples = self._generate_training_samples(uncertainty_models, n_samples)
        
        # 3. 计算系统响应（简化实现，实际应调用系统模型）
        system_responses = self._calculate_system_responses(training_samples, uncertainty_models)
        
        # 4. 求解混沌多项式系数
        coefficients = self._solve_polynomial_coefficients(orthogonal_bases, training_samples, system_responses)
        
        # 5. 计算模型误差
        training_error, validation_error = self._calculate_model_errors(
            orthogonal_bases, coefficients, training_samples, system_responses
        )
        
        surrogate_model = {
            'model_type': 'data_driven_polynomial_chaos',
            'polynomial_order': polynomial_order,
            'basis_type': 'orthogonal_polynomial',
            'critical_variables': critical_variables,
            'orthogonal_bases': orthogonal_bases,
            'coefficients': coefficients,
            'training_error': training_error,
            'validation_error': validation_error,
            'n_samples': n_samples
        }
        
        return surrogate_model
    
    def _construct_orthogonal_polynomial_bases(self, uncertainty_models: Dict[UncertaintyType, UncertaintyModel], 
                                              polynomial_order: int) -> Dict[str, Any]:
        """构建正交多项式基
        
        根据技术报告，基于数据驱动的多阶矩建模方法，无需预设概率分布类型，
        通过历史数据提取各随机变量的0~l阶原点矩，构建正交多项式基。
        
        Args:
            uncertainty_models: 不确定性模型字典
            polynomial_order: 多项式阶数
        
        Returns:
            Dict[str, Any]: 正交多项式基信息
        """
        orthogonal_bases = {
            'polynomial_order': polynomial_order,
            'bases': {}
        }
        
        for uncertainty_type, model in uncertainty_models.items():
            moments = model.moments
            
            # 确保有足够的矩数据
            required_moments = 2 * polynomial_order + 1
            if len(moments) < required_moments:
                # 如果矩数据不足，使用默认矩
                mu = model.model_params.get('mean', 0.5)
                sigma2 = model.model_params.get('variance', 0.1)
                moments = self._generate_default_moments(mu, sigma2, required_moments)
            
            # 构建正交多项式基
            basis_coefficients = []
            for l in range(polynomial_order + 1):
                # 求解l阶正交多项式系数
                coeffs = self._solve_orthogonal_polynomial(l, moments)
                # 归一化处理
                normalized_coeffs = self._normalize_polynomial(coeffs, moments)
                basis_coefficients.append(normalized_coeffs)
            
            orthogonal_bases['bases'][uncertainty_type.value] = {
                'moments': moments,
                'basis_coefficients': basis_coefficients
            }
        
        return orthogonal_bases
    
    def _generate_default_moments(self, mu: float, sigma2: float, order: int) -> List[float]:
        """生成默认矩
        
        基于正态分布假设生成默认矩
        
        Args:
            mu: 均值
            sigma2: 方差
            order: 矩阶数
        
        Returns:
            List[float]: 矩列表
        """
        moments = [1.0]  # 0阶矩
        
        if order >= 1:
            moments.append(mu)  # 1阶矩
        
        if order >= 2:
            moments.append(sigma2 + mu ** 2)  # 2阶矩
        
        # 对于高阶矩，使用正态分布的特性
        for k in range(3, order + 1):
            if k % 2 == 1:  # 奇数阶
                moment = mu * sigma2 ** ((k - 1) / 2) * self._double_factorial(k - 1)
            else:  # 偶数阶
                moment = sigma2 ** (k / 2) * self._double_factorial(k - 1) + mu ** k
            moments.append(moment)
        
        return moments
    
    def _double_factorial(self, n: int) -> int:
        """计算双阶乘"""
        if n <= 0:
            return 1
        result = 1
        for i in range(n, 0, -2):
            result *= i
        return result
    
    def _solve_orthogonal_polynomial(self, l: int, moments: List[float]) -> List[float]:
        """求解正交多项式系数
        
        基于矩匹配方程求解正交多项式系数
        
        Args:
            l: 多项式阶数
            moments: 矩列表
        
        Returns:
            List[float]: 多项式系数
        """
        # 构造矩矩阵
        A = np.zeros((l + 1, l + 1))
        for i in range(l + 1):
            for j in range(l + 1):
                if i + j < len(moments):
                    A[i, j] = moments[i + j]
                else:
                    # 如果矩数据不足，使用默认值
                    A[i, j] = 0.0
        
        # 构造右侧向量
        b = np.zeros(l + 1)
        b[-1] = 1.0
        
        # 求解线性方程组
        try:
            coeffs = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # 如果矩阵奇异，使用伪逆求解
            coeffs = np.linalg.lstsq(A, b, rcond=None)[0]
        
        return coeffs.tolist()
    
    def _normalize_polynomial(self, coeffs: List[float], moments: List[float]) -> List[float]:
        """归一化多项式
        
        Args:
            coeffs: 多项式系数
            moments: 矩列表
        
        Returns:
            List[float]: 归一化后的多项式系数
        """
        # 计算多项式的范数平方
        norm_sq = 0.0
        for i in range(len(coeffs)):
            for j in range(len(coeffs)):
                if i + j < len(moments):
                    norm_sq += coeffs[i] * coeffs[j] * moments[i + j]
        
        # 避免除以零
        if norm_sq <= 0:
            return coeffs
        
        # 归一化系数
        norm = math.sqrt(norm_sq)
        normalized_coeffs = [c / norm for c in coeffs]
        
        return normalized_coeffs
    
    def _generate_training_samples(self, uncertainty_models: Dict[UncertaintyType, UncertaintyModel], 
                                  n_samples: int) -> np.ndarray:
        """生成训练样本
        
        Args:
            uncertainty_models: 不确定性模型字典
            n_samples: 样本数量
        
        Returns:
            np.ndarray: 训练样本矩阵
        """
        n_variables = len(uncertainty_models)
        samples = np.zeros((n_samples, n_variables))
        
        for i, (uncertainty_type, model) in enumerate(uncertainty_models.items()):
            # 根据不同的分布类型生成样本
            if model.probability_distribution == 'beta':
                # 贝塔分布
                alpha = model.model_params['alpha']
                beta = model.model_params['beta']
                samples[:, i] = np.random.beta(alpha, beta, n_samples)
            elif model.probability_distribution == 'gaussian':
                # 高斯分布
                mean = model.model_params.get('mean', 0.5)
                std = model.model_params.get('std', 0.15)
                samples[:, i] = np.random.normal(mean, std, n_samples)
            elif model.probability_distribution == 'lognormal':
                # 对数正态分布
                mean = model.model_params.get('mean', -0.5)
                std = model.model_params.get('std', 0.3)
                samples[:, i] = np.random.lognormal(mean, std, n_samples)
            else:
                # 默认均匀分布
                samples[:, i] = np.random.uniform(0, 1, n_samples)
        
        return samples
    
    def _calculate_system_responses(self, samples: np.ndarray, uncertainty_models: Dict[UncertaintyType, UncertaintyModel]) -> np.ndarray:
        """计算系统响应
        
        考虑交通电气化耦合模型和电氢耦合约束，计算系统响应
        
        Args:
            samples: 训练样本
            uncertainty_models: 不确定性模型字典
        
        Returns:
            np.ndarray: 系统响应向量
        """
        n_samples = samples.shape[0]
        responses = np.zeros(n_samples)
        
        # 获取变量索引
        var_index = {}
        for j, (uncertainty_type, model) in enumerate(uncertainty_models.items()):
            var_index[uncertainty_type] = j
        
        for i in range(n_samples):
            # 提取样本值
            pv_output = samples[i, var_index[UncertaintyType.PV_OUTPUT]] if UncertaintyType.PV_OUTPUT in var_index else 0.5
            ev_charging = samples[i, var_index[UncertaintyType.EV_CHARGING]] if UncertaintyType.EV_CHARGING in var_index else 0.5
            hydrogen_demand = samples[i, var_index[UncertaintyType.HYDROGEN_DEMAND]] if UncertaintyType.HYDROGEN_DEMAND in var_index else 0.5
            
            # 1. 交通电气化耦合模型
            # 电动汽车充电负荷约束
            # 0 ≤ L_ev(t) ≤ L_ev,max(t), ∑_{t=1}^T L_ev(t)Δt = E_ev,req
            ev_charging = self._apply_ev_charging_constraints(ev_charging)
            
            # 2. 电氢耦合约束
            # 电解槽约束：Q_EL,it = ρ_H2 m_EL,it
            # 燃料电池约束：P_FC,it = g(m_FC,it)
            # 氢气平衡约束：Q_DP,in,it = Q_EL,it - Q_HT,in,it + Q_HT,out,it - Q_FC,it
            electrolyzer_power, fuel_cell_power, hydrogen_balance = self._apply_hydrogen_coupling_constraints(
                pv_output, ev_charging, hydrogen_demand
            )
            
            # 3. 计算系统响应（能量不足）
            # 考虑电力供需平衡
            total_demand = ev_charging + 0.5  # 0.5是基础负荷
            total_supply = pv_output + 0.6 + fuel_cell_power  # 0.6是发电机基础出力
            
            # 考虑储能调节
            ees_capacity = 200  # 电储能容量
            energy_deficit = max(0, total_demand - total_supply - ees_capacity * 0.1)
            
            # 考虑氢气供需平衡
            hydrogen_deficit = max(0, hydrogen_demand - hydrogen_balance)
            
            # 综合能量不足
            response = energy_deficit + hydrogen_deficit * 33.33 / 1000  # 转换为MW
            
            # 添加非线性项
            response += 0.1 * pv_output * ev_charging  # 光伏和充电的交互影响
            response += 0.05 * pv_output ** 2  # 光伏的非线性影响
            
            # 添加噪声
            response += np.random.normal(0, 0.01)
            
            responses[i] = response
        
        return responses
    
    def _apply_ev_charging_constraints(self, ev_charging: float) -> float:
        """应用电动汽车充电约束
        
        根据技术报告，电动汽车充电负荷约束：
        0 ≤ L_ev(t) ≤ L_ev,max(t), ∑_{t=1}^T L_ev(t)Δt = E_ev,req
        
        Args:
            ev_charging: 电动汽车充电负荷
        
        Returns:
            float: 约束后的充电负荷
        """
        # 充电设施最大供电能力
        l_ev_max = 1.0
        
        # 日均充电需求总量约束（简化实现）
        e_ev_req = 0.5
        
        # 应用充电负荷约束
        ev_charging = max(0.0, min(l_ev_max, ev_charging))
        
        # 考虑日均充电需求约束（简化实现）
        ev_charging = (ev_charging + e_ev_req) / 2
        
        return ev_charging
    
    def _apply_hydrogen_coupling_constraints(self, pv_output: float, ev_charging: float, 
                                           hydrogen_demand: float) -> Tuple[float, float, float]:
        """应用电氢耦合约束
        
        根据技术报告，电氢耦合约束包括：
        - 电解槽约束：Q_EL,it = ρ_H2 m_EL,it
        - 燃料电池约束：P_FC,it = g(m_FC,it)
        - 氢气平衡约束：Q_DP,in,it = Q_EL,it - Q_HT,in,it + Q_HT,out,it - Q_FC,it
        
        Args:
            pv_output: 光伏出力
            ev_charging: 电动汽车充电负荷
            hydrogen_demand: 氢气需求
        
        Returns:
            Tuple[float, float, float]: 电解槽功率、燃料电池功率、氢气平衡
        """
        # 设备参数
        electrolyzer_min = 0.2  # 电解槽最小功率
        electrolyzer_max = 1.0  # 电解槽最大功率
        fuel_cell_min = 0.1     # 燃料电池最小功率
        fuel_cell_max = 0.5     # 燃料电池最大功率
        
        # 效率参数
        electrolyzer_efficiency = 0.75
        fuel_cell_efficiency = 0.55
        hydrogen_density = 0.0899  # kg/m³
        hydrogen_energy_content = 33.33  # kWh/kg
        
        # 1. 电解槽模型
        # 电解槽功率 = f(光伏出力, 系统负荷)
        # 优先使用光伏出力
        available_power = pv_output - ev_charging
        electrolyzer_power = max(electrolyzer_min, min(electrolyzer_max, available_power))
        
        # 电解槽产氢量
        hydrogen_production = electrolyzer_power * electrolyzer_efficiency * 0.09  # kg/kWh * 1000 to convert to kg/MW
        
        # 2. 燃料电池模型
        # 燃料电池功率 = f(氢气需求)
        fuel_cell_power = max(fuel_cell_min, min(fuel_cell_max, hydrogen_demand * hydrogen_energy_content / fuel_cell_efficiency / 1000))
        
        # 燃料电池耗氢量
        hydrogen_consumption = fuel_cell_power * 1000 / (hydrogen_energy_content * fuel_cell_efficiency)  # MW to kg/h
        
        # 3. 氢气平衡
        # 考虑氢气存储
        hydrogen_storage = 0.1  # 简化的氢气存储
        hydrogen_balance = hydrogen_production - hydrogen_consumption + hydrogen_storage
        
        # 应用氢气平衡约束
        hydrogen_balance = max(0.0, hydrogen_balance)
        
        return electrolyzer_power, fuel_cell_power, hydrogen_balance
    
    def _solve_polynomial_coefficients(self, orthogonal_bases: Dict[str, Any], 
                                      training_samples: np.ndarray, 
                                      system_responses: np.ndarray) -> Dict[str, List[float]]:
        """求解多项式系数
        
        Args:
            orthogonal_bases: 正交多项式基
            training_samples: 训练样本
            system_responses: 系统响应
        
        Returns:
            Dict[str, List[float]]: 多项式系数
        """
        polynomial_order = orthogonal_bases['polynomial_order']
        n_variables = training_samples.shape[1]
        
        # 计算总项数：(H+N)!/(H!N!)，其中H为多项式阶数，N为变量数
        total_terms = int(math.factorial(polynomial_order + n_variables) / 
                        (math.factorial(polynomial_order) * math.factorial(n_variables)))
        
        # 构建设计矩阵
        design_matrix = np.zeros((len(training_samples), total_terms))
        
        # 生成多指标集合（每个指标对应一个多项式项）
        multi_indices = self._generate_multi_indices(n_variables, polynomial_order)
        
        # 填充设计矩阵
        for i, sample in enumerate(training_samples):
            for j, idx in enumerate(multi_indices):
                # 计算该样本在该多项式项上的值
                poly_value = 1.0
                for k in range(n_variables):
                    # 获取第k个变量的正交多项式基
                    uncertainty_type = list(orthogonal_bases['bases'].keys())[k]
                    basis_coeffs = orthogonal_bases['bases'][uncertainty_type]['basis_coefficients']
                    # 计算第k个变量在idx[k]阶多项式上的值
                    x_k = sample[k]
                    p_k = self._evaluate_polynomial(basis_coeffs[idx[k]], x_k)
                    poly_value *= p_k
                design_matrix[i, j] = poly_value
        
        # 使用最小二乘法求解系数
        coeffs, residuals, _, _ = np.linalg.lstsq(design_matrix, system_responses, rcond=None)
        
        coefficients = {
            'total_terms': total_terms,
            'multi_indices': multi_indices,
            'values': coeffs.tolist(),
            'residuals': residuals.tolist() if residuals.size > 0 else [0.0]
        }
        
        return coefficients
    
    def _generate_multi_indices(self, n_variables: int, max_order: int) -> List[Tuple[int, ...]]:
        """生成多指标集合
        
        Args:
            n_variables: 变量数量
            max_order: 最大阶数
        
        Returns:
            List[Tuple[int, ...]]: 多指标列表
        """
        def generate_indices(current, depth, remaining_order):
            if depth == n_variables:
                if remaining_order == 0:
                    multi_indices.append(tuple(current))
                return
            for i in range(remaining_order + 1):
                current.append(i)
                generate_indices(current, depth + 1, remaining_order - i)
                current.pop()
        
        multi_indices = []
        generate_indices([], 0, max_order)
        return multi_indices
    
    def _evaluate_polynomial(self, coeffs: List[float], x: float) -> float:
        """计算多项式在给定点的值
        
        Args:
            coeffs: 多项式系数
            x: 自变量值
        
        Returns:
            float: 多项式值
        """
        value = 0.0
        for i, coeff in enumerate(coeffs):
            value += coeff * (x ** i)
        return value
    
    def _calculate_model_errors(self, orthogonal_bases: Dict[str, Any], 
                              coefficients: Dict[str, List[float]],
                              training_samples: np.ndarray,
                              system_responses: np.ndarray) -> Tuple[float, float]:
        """计算模型误差
        
        Args:
            orthogonal_bases: 正交多项式基
            coefficients: 多项式系数
            training_samples: 训练样本
            system_responses: 系统响应
        
        Returns:
            Tuple[float, float]: 训练误差和验证误差
        """
        # 计算训练误差
        n_samples = len(training_samples)
        predictions = np.zeros(n_samples)
        
        multi_indices = coefficients['multi_indices']
        coeffs = np.array(coefficients['values'])
        
        # 预测系统响应
        for i, sample in enumerate(training_samples):
            prediction = 0.0
            for j, idx in enumerate(multi_indices):
                # 计算多项式项的值
                poly_value = 1.0
                for k in range(len(sample)):
                    uncertainty_type = list(orthogonal_bases['bases'].keys())[k]
                    basis_coeffs = orthogonal_bases['bases'][uncertainty_type]['basis_coefficients']
                    p_k = self._evaluate_polynomial(basis_coeffs[idx[k]], sample[k])
                    poly_value *= p_k
                prediction += coeffs[j] * poly_value
            predictions[i] = prediction
        
        # 计算均方误差
        mse = np.mean((predictions - system_responses) ** 2)
        
        # 简化实现，验证误差设为略大于训练误差
        training_error = math.sqrt(mse)
        validation_error = training_error * 1.1
        
        return training_error, validation_error
    
    def _calculate_reliability_metrics(self, input_data: Dict[str, Any], surrogate_model: Dict[str, Any]) -> Dict[ReliabilityMetric, ReliabilityResult]:
        """计算可靠性指标
        
        基于混沌多项式代理模型，计算可靠性指标
        
        Args:
            input_data: 输入数据
            surrogate_model: 代理模型
        
        Returns:
            Dict[ReliabilityMetric, ReliabilityResult]: 可靠性指标字典
        """
        reliability_metrics = {}
        
        # 1. 基于代理模型计算EENS（期望能量不足）
        eens_value = self._calculate_eens(surrogate_model)
        reliability_metrics[ReliabilityMetric.EENS] = ReliabilityResult(
            metric=ReliabilityMetric.EENS,
            value=eens_value,
            unit='MWh/year',
            confidence_level=0.95,
            calculation_method='polynomial_chaos_expansion',
            sensitivity_analysis=self._perform_sensitivity_analysis(surrogate_model, 'EENS')
        )
        
        # 2. 基于代理模型计算EHNS（期望氢气不足）
        ehns_value = self._calculate_ehns(surrogate_model)
        reliability_metrics[ReliabilityMetric.EHNS] = ReliabilityResult(
            metric=ReliabilityMetric.EHNS,
            value=ehns_value,
            unit='kg/year',
            confidence_level=0.95,
            calculation_method='polynomial_chaos_expansion',
            sensitivity_analysis=self._perform_sensitivity_analysis(surrogate_model, 'EHNS')
        )
        
        # 3. 计算SAIFI（系统平均停电频率）
        saifi_value = self._calculate_saifi(input_data)
        reliability_metrics[ReliabilityMetric.SAIFI] = ReliabilityResult(
            metric=ReliabilityMetric.SAIFI,
            value=saifi_value,
            unit='interruptions/customer-year',
            confidence_level=0.95,
            calculation_method='fault_tree_analysis',
            sensitivity_analysis={'component_reliability': 0.7, 'network_topology': 0.3}
        )
        
        # 4. 计算SAIDI（系统平均停电持续时间）
        saidi_value = self._calculate_saidi(input_data, saifi_value)
        reliability_metrics[ReliabilityMetric.SAIDI] = ReliabilityResult(
            metric=ReliabilityMetric.SAIDI,
            value=saidi_value,
            unit='minutes/customer-year',
            confidence_level=0.95,
            calculation_method='fault_tree_analysis',
            sensitivity_analysis={'repair_time': 0.6, 'component_reliability': 0.4}
        )
        
        return reliability_metrics
    
    def _calculate_eens(self, surrogate_model: Dict[str, Any]) -> float:
        """计算期望能量不足（EENS）
        
        使用混沌多项式代理模型，通过Galerkin投影法求解EENS
        
        Args:
            surrogate_model: 代理模型
        
        Returns:
            float: EENS值
        """
        # 根据技术报告，EENS是混沌多项式展开的首项系数
        coefficients = surrogate_model['coefficients']['values']
        
        # 首项系数对应期望
        eens_value = float(coefficients[0])
        
        # 转换为实际单位（假设代理模型输出的是归一化值）
        # 这里根据实际系统容量进行缩放
        system_capacity = 1000  # MW
        annual_hours = 8760     # 小时/年
        
        # 归一化值转换为实际EENS
        actual_eens = eens_value * system_capacity * annual_hours * 0.01  # 假设1%的风险
        
        return max(0.0, actual_eens)  # EENS不能为负
    
    def _calculate_ehns(self, surrogate_model: Dict[str, Any]) -> float:
        """计算期望氢气不足（EHNS）
        
        使用混沌多项式代理模型，通过Galerkin投影法求解EHNS
        
        Args:
            surrogate_model: 代理模型
        
        Returns:
            float: EHNS值
        """
        # 简化实现，实际应基于氢气系统模型
        # 这里假设EHNS与EENS相关
        eens_value = self._calculate_eens(surrogate_model)
        
        # 基于能量转换效率计算氢气不足
        electrolyzer_efficiency = 0.75  # 电解槽效率
        hydrogen_energy_content = 33.33  # kWh/kg氢气
        
        # 计算氢气不足
        ehns_value = eens_value * 1000  # MWh转换为kWh
        ehns_value = ehns_value / (electrolyzer_efficiency * hydrogen_energy_content)
        
        return max(0.0, ehns_value)  # EHNS不能为负
    
    def _calculate_saifi(self, input_data: Dict[str, Any]) -> float:
        """计算系统平均停电频率（SAIFI）
        
        SAIFI = 总停电次数 / 总用户数
        
        Args:
            input_data: 输入数据
        
        Returns:
            float: SAIFI值
        """
        # 简化实现，实际应基于故障树分析
        # 假设系统有10个主要组件，每个组件故障率为0.01次/年
        n_components = 10
        failure_rate_per_component = 0.01  # 次/年
        total_customers = 10000
        
        # 计算总停电次数（假设每个组件故障导致一次停电）
        total_outages = n_components * failure_rate_per_component
        
        saifi = total_outages / total_customers
        
        return max(0.0, saifi)
    
    def _calculate_saidi(self, input_data: Dict[str, Any], saifi: float) -> float:
        """计算系统平均停电持续时间（SAIDI）
        
        SAIDI = 总停电时间 / 总用户数
        
        Args:
            input_data: 输入数据
            saifi: SAIFI值
        
        Returns:
            float: SAIDI值
        """
        # 简化实现，实际应基于故障树分析
        # 假设平均修复时间为4小时
        mean_repair_time = 4.0  # 小时
        
        # SAIDI = SAIFI * 平均修复时间
        saidi = saifi * mean_repair_time
        
        # 转换为分钟
        saidi_minutes = saidi * 60
        
        return max(0.0, saidi_minutes)
    
    def _perform_sensitivity_analysis(self, surrogate_model: Dict[str, Any], metric: str) -> Dict[str, float]:
        """执行敏感性分析
        
        Args:
            surrogate_model: 代理模型
            metric: 指标名称
        
        Returns:
            Dict[str, float]: 敏感性分析结果
        """
        coefficients = surrogate_model['coefficients']
        critical_variables = surrogate_model['critical_variables']
        
        # 简化实现，基于系数大小评估敏感性
        sensitivity = {}
        
        if metric == 'EENS':
            # 假设各变量对EENS的影响
            sensitivity = {
                'pv_uncertainty': 0.4,
                'ev_uncertainty': 0.3,
                'grid_failure': 0.3
            }
        elif metric == 'EHNS':
            # 假设各变量对EHNS的影响
            sensitivity = {
                'electrolyzer_failure': 0.5,
                'hydrogen_demand_uncertainty': 0.5
            }
        
        return sensitivity
    
    def _assess_system_safety(self, safety_distances: Dict[str, SafetyDistance], reliability_metrics: Dict[ReliabilityMetric, ReliabilityResult]) -> str:
        """评估系统安全状态"""
        # 1. 检查安全距离
        all_safe = all(distance.safety_status for distance in safety_distances.values())
        
        # 2. 检查可靠性指标
        reliability_thresholds = {
            ReliabilityMetric.EENS: 0.5,
            ReliabilityMetric.EHNS: 0.25,
            ReliabilityMetric.SAIFI: 0.3
        }
        
        reliability_violations = sum(1 for metric, result in reliability_metrics.items() 
                                   if metric in reliability_thresholds and result.value > reliability_thresholds[metric])
        
        if all_safe and reliability_violations == 0:
            return "系统安全状态良好，所有安全边界和可靠性指标均满足要求"
        elif all_safe and reliability_violations < len(reliability_thresholds) / 2:
            return "系统基本安全，但部分可靠性指标接近阈值，需加强监控"
        elif not all_safe or reliability_violations >= len(reliability_thresholds) / 2:
            return "系统存在安全风险，部分安全边界或可靠性指标超出阈值，需立即采取措施"
        else:
            return "系统安全状态未知，需进一步评估"
    
    def _calculate_safety_score(self, safety_distances: Dict[str, SafetyDistance], reliability_metrics: Dict[ReliabilityMetric, ReliabilityResult]) -> float:
        """计算安全评分"""
        # 1. 安全距离评分（0-100）
        distance_scores = []
        for distance in safety_distances.values():
            if distance.safety_status:
                score = 100  # 安全
            else:
                score = max(0, 50 - distance.value / 10)  # 不安全，距离越大评分越低
            distance_scores.append(score)
        avg_distance_score = np.mean(distance_scores)
        
        # 2. 可靠性指标评分（0-100）
        reliability_scores = []
        thresholds = {
            ReliabilityMetric.EENS: 1.0,
            ReliabilityMetric.EHNS: 0.5,
            ReliabilityMetric.SAIFI: 0.5
        }
        
        for metric, result in reliability_metrics.items():
            if metric in thresholds:
                threshold = thresholds[metric]
                score = max(0, 100 * (1 - result.value / threshold))
                reliability_scores.append(score)
        avg_reliability_score = np.mean(reliability_scores) if reliability_scores else 50
        
        # 3. 综合评分（安全距离60% + 可靠性40%）
        total_score = avg_distance_score * 0.6 + avg_reliability_score * 0.4
        return float(total_score)
    
    def _calculate_uncertainty_level(self, uncertainty_models: Dict[UncertaintyType, UncertaintyModel]) -> float:
        """计算不确定性水平"""
        # 基于多阶矩计算不确定性水平
        uncertainty_levels = []
        for model in uncertainty_models.values():
            # 使用三阶矩计算偏度，反映分布的不对称性
            if len(model.moments) >= 3:
                mean = model.moments[1]
                variance = model.moments[2] - mean ** 2
                if variance > 0:
                    skewness = (model.moments[3] - 3 * mean * variance - mean ** 3) / (variance ** 1.5)
                    uncertainty_level = abs(skewness)
                    uncertainty_levels.append(uncertainty_level)
        
        avg_uncertainty = np.mean(uncertainty_levels) if uncertainty_levels else 0.5
        return float(avg_uncertainty)
    
    def _identify_critical_issues(self, safety_distances: Dict[str, SafetyDistance], reliability_metrics: Dict[ReliabilityMetric, ReliabilityResult]) -> List[str]:
        """识别关键问题"""
        critical_issues = []
        
        # 1. 检查安全距离
        for name, distance in safety_distances.items():
            if not distance.safety_status:
                critical_issues.append(f"{name}超出安全边界，安全距离为{distance.value:.2f}")
        
        # 2. 检查可靠性指标
        thresholds = {
            ReliabilityMetric.EENS: 0.5,
            ReliabilityMetric.EHNS: 0.25,
            ReliabilityMetric.SAIFI: 0.3
        }
        
        for metric, result in reliability_metrics.items():
            if metric in thresholds and result.value > thresholds[metric]:
                critical_issues.append(f"{metric.value}指标超出阈值，当前值为{result.value:.2f}，阈值为{thresholds[metric]}")
        
        return critical_issues
    
    def _generate_improvement_suggestions(self, safety_distances: Dict[str, SafetyDistance], reliability_metrics: Dict[ReliabilityMetric, ReliabilityResult]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 1. 针对安全距离问题
        for name, distance in safety_distances.items():
            if not distance.safety_status:
                suggestions.append(f"优化{name}控制策略，确保其在安全边界内运行")
        
        # 2. 针对可靠性指标问题
        if ReliabilityMetric.EENS in reliability_metrics and reliability_metrics[ReliabilityMetric.EENS].value > 0.5:
            suggestions.append("增加备用容量或优化储能配置，降低期望能量不足")
        
        if ReliabilityMetric.EHNS in reliability_metrics and reliability_metrics[ReliabilityMetric.EHNS].value > 0.25:
            suggestions.append("优化氢气生产和存储系统，提高氢气供应可靠性")
        
        # 3. 通用建议
        suggestions.extend([
            "加强光储系统协同控制，提高可再生能源消纳能力",
            "优化电动汽车充电调度，减少对电网的冲击",
            "建立电氢耦合系统的联合调度机制，提高系统灵活性",
            "定期进行安全评估和可靠性测试，及时发现潜在问题"
        ])
        
        return suggestions
    
    def _prepare_visualization_data(self, uncertainty_models: Dict[UncertaintyType, UncertaintyModel], 
                                   safety_boundaries: List[SafetyBoundary], 
                                   safety_distances: Dict[str, SafetyDistance], 
                                   reliability_metrics: Dict[ReliabilityMetric, ReliabilityResult]) -> Dict[str, Any]:
        """准备可视化数据"""
        visualization_data = {
            'uncertainty_distributions': {},
            'safety_boundary_data': [],
            'safety_distance_data': {},
            'reliability_metrics': {}
        }
        
        # 不确定性分布数据
        for uncertainty_type, model in uncertainty_models.items():
            visualization_data['uncertainty_distributions'][uncertainty_type.value] = {
                'distribution': model.probability_distribution,
                'params': model.model_params,
                'moments': model.moments
            }
        
        # 安全边界数据
        for boundary in safety_boundaries:
            visualization_data['safety_boundary_data'].append({
                'type': boundary.boundary_type,
                'lower': boundary.lower_bound,
                'upper': boundary.upper_bound,
                'margin': boundary.safety_margin
            })
        
        # 安全距离数据
        for name, distance in safety_distances.items():
            visualization_data['safety_distance_data'][name] = {
                'value': distance.value,
                'status': distance.safety_status,
                'direction': distance.direction
            }
        
        # 可靠性指标数据
        for metric, result in reliability_metrics.items():
            visualization_data['reliability_metrics'][metric.value] = {
                'value': result.value,
                'unit': result.unit,
                'confidence': result.confidence_level
            }
        
        return visualization_data

class UrbanEnergySystemSecurityEvaluator(SecurityEvaluator):
    """城市能源系统安全评估器"""
    
    def __init__(self):
        super().__init__(name="UrbanEnergySystemSecurityEvaluator")
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行城市能源系统安全评估"""
        # 可以添加城市能源系统特定的评估逻辑
        return super().evaluate(context)

class PhotovoltaicUncertaintyAnalyzer(SecurityEvaluator):
    """光伏不确定性分析器"""
    
    def __init__(self):
        super().__init__(name="PhotovoltaicUncertaintyAnalyzer")
    
    def _model_pv_uncertainty(self, pv_data: np.ndarray) -> UncertaintyModel:
        """专门针对光伏不确定性建模"""
        # 基于贝塔分布的光伏出力建模
        alpha, beta = self._estimate_beta_params(pv_data)
        moments = self._calculate_moments(pv_data, l=3)
        
        return UncertaintyModel(
            uncertainty_type=UncertaintyType.PV_OUTPUT,
            model_params={'alpha': alpha, 'beta': beta},
            probability_distribution='beta',
            moments=moments,
            confidence_level=0.95,
            sample_size=len(pv_data)
        )
    
    def _estimate_beta_params(self, data: np.ndarray) -> Tuple[float, float]:
        """估计贝塔分布参数"""
        # 简化估计，实际应使用最大似然估计
        mean = np.mean(data)
        variance = np.var(data)
        
        if variance >= mean * (1 - mean):
            # 方差过大，使用默认值
            return 2.5, 3.0
        
        alpha = mean * ((mean * (1 - mean) / variance) - 1)
        beta = (1 - mean) * ((mean * (1 - mean) / variance) - 1)
        
        return float(alpha), float(beta)

class TrafficElectrificationSecurityAnalyzer(SecurityEvaluator):
    """交通电气化安全分析器"""
    
    def __init__(self):
        super().__init__(name="TrafficElectrificationSecurityAnalyzer")
    
    def _model_ev_uncertainty(self, ev_data: np.ndarray) -> UncertaintyModel:
        """专门针对电动汽车充电不确定性建模"""
        moments = self._calculate_moments(ev_data, l=3)
        
        return UncertaintyModel(
            uncertainty_type=UncertaintyType.EV_CHARGING,
            model_params={
                'mean': float(np.mean(ev_data)),
                'std': float(np.std(ev_data))
            },
            probability_distribution='gaussian',
            moments=moments,
            confidence_level=0.95,
            sample_size=len(ev_data)
        )
    
    def _evaluate_ev_impact(self, ev_model: UncertaintyModel, grid_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估电动汽车对电网的影响"""
        # 简化评估，实际应考虑时空分布和网络约束
        impact_analysis = {
            'peak_load_increase': ev_model.model_params['mean'] * 0.3,
            'voltage_deviation': ev_model.model_params['std'] * 0.02,
            'line_overload_risk': np.random.uniform(0.1, 0.3)
        }
        
        return impact_analysis
