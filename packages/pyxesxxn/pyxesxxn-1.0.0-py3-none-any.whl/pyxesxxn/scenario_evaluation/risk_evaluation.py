"""
风险评估模块

提供能源系统的风险评估功能，包括：
- 风险识别：系统脆弱性、技术风险、市场风险
- 概率分析：风险发生概率、影响程度评估
- 敏感性分析：关键风险因子识别
- 风险量化：财务损失、运营中断、社会影响
- 风险缓解：缓解策略、应急预案
- 情景分析：极端情况下的风险评估
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
import math
from scipy import stats
import json

from .evaluation_framework import Evaluator, EvaluationContext, EvaluationResult, EvaluationStatus, EvaluationType

class RiskCategory(Enum):
    """风险类别"""
    TECHNICAL = "technical"                    # 技术风险
    FINANCIAL = "financial"                    # 财务风险
    MARKET = "market"                          # 市场风险
    OPERATIONAL = "operational"                # 运营风险
    REGULATORY = "regulatory"                  # 监管风险
    ENVIRONMENTAL = "environmental"             # 环境风险
    SOCIAL = "social"                          # 社会风险
    POLITICAL = "political"                    # 政治风险
    CYBERSECURITY = "cybersecurity"            # 网络安全风险
    SUPPLY_CHAIN = "supply_chain"              # 供应链风险

class RiskLevel(Enum):
    """风险等级"""
    VERY_LOW = "very_low"                      # 很低
    LOW = "low"                                # 低
    MEDIUM = "medium"                          # 中等
    HIGH = "high"                              # 高
    VERY_HIGH = "very_high"                    # 很高
    CRITICAL = "critical"                      # 关键

class ProbabilityRange(Enum):
    """概率范围"""
    VERY_UNLIKELY = "very_unlikely"            # 很少发生 (< 1%)
    UNLIKELY = "unlikely"                      # 不太可能 (1-10%)
    POSSIBLE = "possible"                      # 可能 (10-50%)
    LIKELY = "likely"                          # 很可能 (50-80%)
    VERY_LIKELY = "very_likely"                # 几乎确定 (> 80%)

class ImpactType(Enum):
    """影响类型"""
    FINANCIAL_LOSS = "financial_loss"          # 财务损失
    OPERATIONAL_DISRUPTION = "operational_disruption"  # 运营中断
    REPUTATION_DAMAGE = "reputation_damage"    # 声誉损害
    SAFETY_INCIDENT = "safety_incident"        # 安全事故
    ENVIRONMENTAL_DAMAGE = "environmental_damage"  # 环境损害
    REGULATORY_PENALTY = "regulatory_penalty"  # 监管处罚
    MARKET_POSITION_LOSS = "market_position_loss"  # 市场份额损失

@dataclass
class RiskFactor:
    """风险因子"""
    id: str
    name: str
    category: RiskCategory
    description: str
    
    # 概率参数
    probability: float                         # 发生概率 (0-1)
    probability_range: ProbabilityRange        # 概率范围
    
    # 影响参数
    impact_magnitude: float                    # 影响程度 (0-1)
    impact_type: ImpactType                    # 影响类型
    
    # 量化参数
    financial_impact: float                    # 财务影响金额
    time_to_impact: timedelta                  # 影响发生时间
    
    # 风险缓解
    mitigation_measures: List[str]             # 缓解措施
    residual_risk: float                       # 缓解后剩余风险
    risk_owner: str                            # 风险责任人
    
    # 关联性
    related_risks: List[str]                   # 相关风险
    trigger_events: List[str]                  # 触发事件

@dataclass
class ScenarioParameter:
    """情景参数"""
    parameter_name: str
    base_value: float
    scenario_value: float
    probability: float
    description: str

@dataclass
class RiskScenario:
    """风险情景"""
    id: str
    name: str
    description: str
    
    # 情景参数
    parameters: List[ScenarioParameter]
    
    # 影响分析
    financial_impact: float
    operational_impact: float
    reputational_impact: float
    environmental_impact: float
    
    # 概率评估
    occurrence_probability: float
    
    # 风险因子
    risk_factors: List[str]                    # 包含的风险因子ID
    trigger_conditions: List[str]              # 触发条件

@dataclass
class RiskMetrics:
    """风险指标"""
    # 总体风险
    overall_risk_score: float                  # 总体风险评分
    risk_level: RiskLevel                      # 风险等级
    
    # 财务风险
    expected_financial_loss: float             # 期望财务损失
    value_at_risk: float                      # 风险价值 (VaR)
    conditional_var: float                     # 条件风险价值 (CVaR)
    
    # 运营风险
    operational_disruption_probability: float  # 运营中断概率
    expected_downtime_hours: float             # 期望停机小时数
    recovery_time_estimate: float              # 预计恢复时间
    
    # 风险分布
    risk_concentration: Dict[RiskCategory, float]  # 风险集中度
    risk_correlation_matrix: np.ndarray        # 风险相关性矩阵
    
    # 敏感性分析
    key_risk_drivers: List[str]                # 关键风险驱动因素
    sensitivity_analysis: Dict[str, float]     # 敏感性分析结果

@dataclass
class RiskMitigationPlan:
    """风险缓解计划"""
    # 预防措施
    preventive_measures: List[str]             # 预防措施
    risk_control_effectiveness: float          # 风险控制有效性
    
    # 应急响应
    contingency_plans: Dict[str, List[str]]    # 应急预案
    emergency_response_time: float             # 应急响应时间
    crisis_management_capability: float        # 危机管理能力
    
    # 保险和转移
    insurance_coverage: float                  # 保险覆盖
    risk_transfer_mechanisms: List[str]        # 风险转移机制
    
    # 监控和审查
    monitoring_indicators: List[str]           # 监控指标
    review_frequency: str                      # 审查频率
    escalation_procedures: List[str]           # 升级程序

@dataclass
class RiskResult:
    """风险评估结果"""
    # 总体评估
    overall_risk_score: float
    risk_level: RiskLevel
    risk_appetite_alignment: float             # 风险偏好一致性
    
    # 详细分析
    risk_metrics: RiskMetrics
    top_risks: List[RiskFactor]                # 主要风险列表
    risk_scenarios: List[RiskScenario]         # 风险情景分析
    
    # 缓解计划
    mitigation_plan: RiskMitigationPlan
    
    # 建议措施
    immediate_actions: List[str]               # 即时行动
    short_term_measures: List[str]             # 短期措施
    long_term_strategies: List[str]            # 长期策略
    
    # 监控建议
    key_monitoring_points: List[str]           # 关键监控点
    early_warning_indicators: List[str]        # 早期预警指标

class RiskEvaluator(Evaluator):
    """风险评估器"""
    
    def __init__(self, assessment_period: int = 365):
        super().__init__("RiskEvaluator", EvaluationType.RISK)
        self.assessment_period = assessment_period
        self.risk_factors: Dict[str, RiskFactor] = {}
        self.risk_scenarios: Dict[str, RiskScenario] = {}
        self.risk_data: Dict[str, Any] = {}
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行风险评估"""
        start_time = datetime.now()
        self.logger.info("开始风险评估")
        
        try:
            # 从场景数据中提取风险信息
            scenario_data = context.scenario_data
            self._extract_risk_data(scenario_data)
            
            # 识别和分析风险因子
            risk_factors = self._identify_risk_factors()
            
            # 构建风险情景
            risk_scenarios = self._construct_risk_scenarios(risk_factors)
            
            # 计算风险指标
            risk_metrics = self._calculate_risk_metrics(risk_factors, risk_scenarios)
            
            # 敏感性分析
            sensitivity_analysis = self._perform_sensitivity_analysis(risk_factors)
            
            # 制定缓解计划
            mitigation_plan = self._develop_mitigation_plan(risk_factors, risk_metrics)
            
            # 创建风险结果
            result = RiskResult(
                overall_risk_score=risk_metrics.overall_risk_score,
                risk_level=risk_metrics.risk_level,
                risk_appetite_alignment=self._assess_risk_appetite_alignment(risk_metrics),
                risk_metrics=risk_metrics,
                top_risks=self._rank_top_risks(risk_factors),
                risk_scenarios=risk_scenarios,
                mitigation_plan=mitigation_plan,
                immediate_actions=self._suggest_immediate_actions(risk_factors),
                short_term_measures=self._suggest_short_term_measures(risk_factors),
                long_term_strategies=self._suggest_long_term_strategies(risk_factors),
                key_monitoring_points=self._define_key_monitoring_points(risk_factors),
                early_warning_indicators=self._define_early_warning_indicators(risk_factors)
            )
            
            # 创建标准评估结果
            metrics = {
                'overall_risk_score': result.overall_risk_score,
                'expected_financial_loss': result.risk_metrics.expected_financial_loss,
                'value_at_risk': result.risk_metrics.value_at_risk,
                'operational_disruption_probability': result.risk_metrics.operational_disruption_probability,
                'risk_level': result.risk_level.value
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={'risk_result': result},
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("风险评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"风险评估失败: {str(e)}")
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
        required_fields = ['risk_data', 'scenario_parameters', 'asset_information']
        for field in required_fields:
            if field not in context.metadata:
                self.logger.warning(f"缺少必需字段: {field}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['risk_data', 'scenario_parameters', 'asset_information', 'operational_data', 'financial_data']
    
    def add_risk_factor(self, risk_factor: RiskFactor):
        """添加风险因子"""
        self.risk_factors[risk_factor.id] = risk_factor
    
    def add_risk_scenario(self, scenario: RiskScenario):
        """添加风险情景"""
        self.risk_scenarios[scenario.id] = scenario
    
    def _extract_risk_data(self, scenario_data: Dict[str, Any]):
        """从场景数据中提取风险信息"""
        # 这里应该从场景数据中解析风险相关数据
        # 简化实现
        
        # 技术风险
        if 'technical_risks' in scenario_data:
            for risk_data in scenario_data['technical_risks']:
                risk_factor = RiskFactor(
                    id=risk_data.get('id', f"tech_risk_{len(self.risk_factors)}"),
                    name=risk_data.get('name', '技术风险'),
                    category=RiskCategory.TECHNICAL,
                    description=risk_data.get('description', ''),
                    probability=risk_data.get('probability', 0.1),
                    probability_range=ProbabilityRange.UNLIKELY,
                    impact_magnitude=risk_data.get('impact_magnitude', 0.3),
                    impact_type=ImpactType.OPERATIONAL_DISRUPTION,
                    financial_impact=risk_data.get('financial_impact', 1000000),
                    time_to_impact=timedelta(days=risk_data.get('time_to_impact_days', 30)),
                    mitigation_measures=risk_data.get('mitigation_measures', []),
                    residual_risk=risk_data.get('residual_risk', 0.05),
                    risk_owner=risk_data.get('risk_owner', '技术部门'),
                    related_risks=risk_data.get('related_risks', []),
                    trigger_events=risk_data.get('trigger_events', [])
                )
                self.risk_factors[risk_factor.id] = risk_factor
        
        # 市场风险
        if 'market_risks' in scenario_data:
            for risk_data in scenario_data['market_risks']:
                risk_factor = RiskFactor(
                    id=risk_data.get('id', f"market_risk_{len(self.risk_factors)}"),
                    name=risk_data.get('name', '市场风险'),
                    category=RiskCategory.MARKET,
                    description=risk_data.get('description', ''),
                    probability=risk_data.get('probability', 0.2),
                    probability_range=ProbabilityRange.POSSIBLE,
                    impact_magnitude=risk_data.get('impact_magnitude', 0.4),
                    impact_type=ImpactType.FINANCIAL_LOSS,
                    financial_impact=risk_data.get('financial_impact', 5000000),
                    time_to_impact=timedelta(days=risk_data.get('time_to_impact_days', 7)),
                    mitigation_measures=risk_data.get('mitigation_measures', []),
                    residual_risk=risk_data.get('residual_risk', 0.1),
                    risk_owner=risk_data.get('risk_owner', '市场部门'),
                    related_risks=risk_data.get('related_risks', []),
                    trigger_events=risk_data.get('trigger_events', [])
                )
                self.risk_factors[risk_factor.id] = risk_factor
    
    def _identify_risk_factors(self) -> List[RiskFactor]:
        """识别风险因子"""
        return list(self.risk_factors.values())
    
    def _construct_risk_scenarios(self, risk_factors: List[RiskFactor]) -> List[RiskScenario]:
        """构建风险情景"""
        scenarios = []
        
        # 极端天气情景
        extreme_weather = RiskScenario(
            id="extreme_weather",
            name="极端天气事件",
            description="遭遇极端天气事件导致的运营中断",
            parameters=[
                ScenarioParameter("weather_intensity", 1.0, 3.0, 0.05, "极端天气强度"),
                ScenarioParameter("duration_days", 1, 7, 0.1, "持续天数")
            ],
            financial_impact=10000000,
            operational_impact=0.8,
            reputational_impact=0.3,
            environmental_impact=0.6,
            occurrence_probability=0.1,
            risk_factors=[rf.id for rf in risk_factors if rf.category == RiskCategory.ENVIRONMENTAL],
            trigger_conditions=["极端天气预报", "连续恶劣天气"]
        )
        scenarios.append(extreme_weather)
        
        # 技术故障情景
        tech_failure = RiskScenario(
            id="tech_failure",
            name="关键技术故障",
            description="关键设备或系统发生故障",
            parameters=[
                ScenarioParameter("failure_probability", 0.1, 0.3, 0.15, "故障概率"),
                ScenarioParameter("recovery_time_hours", 1, 48, 0.2, "恢复时间")
            ],
            financial_impact=5000000,
            operational_impact=0.9,
            reputational_impact=0.4,
            environmental_impact=0.1,
            occurrence_probability=0.15,
            risk_factors=[rf.id for rf in risk_factors if rf.category == RiskCategory.TECHNICAL],
            trigger_conditions=["设备老化", "维护不当", "设计缺陷"]
        )
        scenarios.append(tech_failure)
        
        # 市场波动情景
        market_volatility = RiskScenario(
            id="market_volatility",
            name="市场大幅波动",
            description="能源价格或需求大幅波动",
            parameters=[
                ScenarioParameter("price_volatility", 0.2, 0.8, 0.25, "价格波动率"),
                ScenarioParameter("demand_change", 0.1, 0.4, 0.2, "需求变化")
            ],
            financial_impact=15000000,
            operational_impact=0.3,
            reputational_impact=0.2,
            environmental_impact=0.0,
            occurrence_probability=0.25,
            risk_factors=[rf.id for rf in risk_factors if rf.category == RiskCategory.MARKET],
            trigger_conditions=["政策变化", "经济衰退", "供需失衡"]
        )
        scenarios.append(market_volatility)
        
        return scenarios
    
    def _calculate_risk_metrics(self, risk_factors: List[RiskFactor], risk_scenarios: List[RiskScenario]) -> RiskMetrics:
        """计算风险指标"""
        # 总体风险评分 (加权平均)
        total_risk_score = sum(rf.probability * rf.impact_magnitude for rf in risk_factors) / len(risk_factors)
        
        # 风险等级
        risk_level = self._determine_risk_level(total_risk_score)
        
        # 期望财务损失
        expected_financial_loss = sum(rf.probability * rf.financial_impact for rf in risk_factors)
        
        # 风险价值 (VaR) - 简化计算 (95%置信度)
        risk_losses = [rf.probability * rf.financial_impact for rf in risk_factors]
        value_at_risk = np.percentile(risk_losses, 95) if risk_losses else 0
        
        # 条件风险价值 (CVaR)
        conditional_var = np.mean([loss for loss in risk_losses if loss >= value_at_risk]) if risk_losses else 0
        
        # 运营中断概率
        operational_risks = [rf for rf in risk_factors if rf.impact_type == ImpactType.OPERATIONAL_DISRUPTION]
        operational_disruption_probability = 1 - np.prod([1 - rf.probability for rf in operational_risks])
        
        # 期望停机时间
        downtime_risks = [rf for rf in operational_risks if hasattr(rf, 'time_to_impact')]
        expected_downtime_hours = sum(rf.probability * rf.time_to_impact.total_seconds() / 3600 
                                    for rf in downtime_risks) if downtime_risks else 0
        
        # 恢复时间估计
        recovery_time_estimate = max([rf.time_to_impact.total_seconds() / 3600 for rf in downtime_risks]) if downtime_risks else 24
        
        # 风险集中度
        risk_concentration = {}
        for category in RiskCategory:
            category_risks = [rf for rf in risk_factors if rf.category == category]
            if category_risks:
                concentration = sum(rf.probability * rf.impact_magnitude for rf in category_risks)
                risk_concentration[category] = concentration
            else:
                risk_concentration[category] = 0
        
        # 关键风险驱动因素
        risk_scores = [(rf.id, rf.probability * rf.impact_magnitude) for rf in risk_factors]
        risk_scores.sort(key=lambda x: x[1], reverse=True)
        key_risk_drivers = [rf_id for rf_id, score in risk_scores[:5]]
        
        return RiskMetrics(
            overall_risk_score=total_risk_score,
            risk_level=risk_level,
            expected_financial_loss=expected_financial_loss,
            value_at_risk=value_at_risk,
            conditional_var=conditional_var,
            operational_disruption_probability=operational_disruption_probability,
            expected_downtime_hours=expected_downtime_hours,
            recovery_time_estimate=recovery_time_estimate,
            risk_concentration=risk_concentration,
            risk_correlation_matrix=np.eye(len(risk_factors)),  # 简化假设为独立
            key_risk_drivers=key_risk_drivers,
            sensitivity_analysis={rf.id: rf.probability * rf.impact_magnitude for rf in risk_factors}
        )
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """确定风险等级"""
        if risk_score < 0.1:
            return RiskLevel.VERY_LOW
        elif risk_score < 0.25:
            return RiskLevel.LOW
        elif risk_score < 0.5:
            return RiskLevel.MEDIUM
        elif risk_score < 0.75:
            return RiskLevel.HIGH
        elif risk_score < 0.9:
            return RiskLevel.VERY_HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _perform_sensitivity_analysis(self, risk_factors: List[RiskFactor]) -> Dict[str, float]:
        """执行敏感性分析"""
        # 简化的敏感性分析：计算各风险因子对总体风险的贡献
        total_contribution = sum(rf.probability * rf.impact_magnitude for rf in risk_factors)
        
        sensitivity_analysis = {}
        for rf in risk_factors:
            contribution = (rf.probability * rf.impact_magnitude) / max(total_contribution, 0.01)
            sensitivity_analysis[rf.id] = contribution
        
        return sensitivity_analysis
    
    def _develop_mitigation_plan(self, risk_factors: List[RiskFactor], risk_metrics: RiskMetrics) -> RiskMitigationPlan:
        """制定缓解计划"""
        preventive_measures = []
        contingency_plans = {}
        
        # 基于风险类别制定措施
        for rf in risk_factors:
            # 预防措施
            preventive_measures.extend(rf.mitigation_measures)
            
            # 应急预案
            if rf.category not in contingency_plans:
                contingency_plans[rf.category.value] = []
            
            contingency_plans[rf.category.value].append(
                f"应对{rf.name}的应急预案"
            )
        
        # 监控指标
        monitoring_indicators = [
            "关键设备运行状态",
            "市场价格波动情况",
            "天气预警信息",
            "运营效率指标",
            "财务风险指标"
        ]
        
        # 风险控制有效性
        control_effectiveness = 1 - (sum(rf.residual_risk for rf in risk_factors) / len(risk_factors))
        
        return RiskMitigationPlan(
            preventive_measures=list(set(preventive_measures)),
            risk_control_effectiveness=control_effectiveness,
            contingency_plans=contingency_plans,
            emergency_response_time=4.0,  # 4小时
            crisis_management_capability=0.8,  # 80%能力
            insurance_coverage=0.7,  # 70%保险覆盖
            risk_transfer_mechanisms=["保险", "对冲", "外包"],
            monitoring_indicators=monitoring_indicators,
            review_frequency="季度",
            escalation_procedures=["通知风险管理部门", "启动应急响应", "上报高级管理层"]
        )
    
    def _assess_risk_appetite_alignment(self, risk_metrics: RiskMetrics) -> float:
        """评估风险偏好一致性"""
        # 假设组织风险偏好阈值为0.3
        risk_appetite_threshold = 0.3
        
        if risk_metrics.overall_risk_score <= risk_appetite_threshold:
            return 1.0  # 完全一致
        elif risk_metrics.overall_risk_score <= risk_appetite_threshold * 2:
            return 0.8  # 基本一致
        else:
            return max(0.1, 1.0 - (risk_metrics.overall_risk_score - risk_appetite_threshold * 2))
    
    def _rank_top_risks(self, risk_factors: List[RiskFactor]) -> List[RiskFactor]:
        """排序主要风险"""
        # 按风险评分排序
        scored_risks = [(rf, rf.probability * rf.impact_magnitude) for rf in risk_factors]
        scored_risks.sort(key=lambda x: x[1], reverse=True)
        
        return [rf for rf, score in scored_risks[:10]]  # 返回前10个主要风险
    
    def _suggest_immediate_actions(self, risk_factors: List[RiskFactor]) -> List[str]:
        """建议即时行动"""
        actions = []
        
        # 针对高风险因子
        high_risks = [rf for rf in risk_factors if rf.probability * rf.impact_magnitude > 0.5]
        for rf in high_risks:
            actions.append(f"立即关注和处理{rf.name}")
        
        # 通用即时行动
        actions.append("建立风险监控机制")
        actions.append("更新应急预案")
        actions.append("加强关键设备维护")
        actions.append("提高员工风险意识")
        
        return actions
    
    def _suggest_short_term_measures(self, risk_factors: List[RiskFactor]) -> List[str]:
        """建议短期措施"""
        measures = [
            "完善风险管理流程",
            "加强供应商风险管理",
            "建立风险数据库",
            "开展风险培训",
            "制定详细应急预案",
            "购买补充保险",
            "建立备件库存"
        ]
        
        return measures
    
    def _suggest_long_term_strategies(self, risk_factors: List[RiskFactor]) -> List[str]:
        """建议长期策略"""
        strategies = [
            "建立全面风险管理体系",
            "投资风险缓解技术",
            "建立战略合作伙伴关系",
            "开发多元化收入来源",
            "建立行业风险预警系统",
            "制定长期风险策略",
            "培养风险管理专业人才"
        ]
        
        return strategies
    
    def _define_key_monitoring_points(self, risk_factors: List[RiskFactor]) -> List[str]:
        """定义关键监控点"""
        monitoring_points = [
            "设备运行状态监控系统",
            "市场价格预警系统",
            "天气监测系统",
            "财务风险监控系统",
            "运营效率监控",
            "供应链风险监控",
            "合规性检查"
        ]
        
        return monitoring_points
    
    def _define_early_warning_indicators(self, risk_factors: List[RiskFactor]) -> List[str]:
        """定义早期预警指标"""
        indicators = [
            "设备性能指标异常",
            "市场价格异常波动",
            "天气预警升级",
            "运营效率下降",
            "财务指标恶化",
            "供应商绩效下降",
            "合规性风险增加",
            "员工满意度下降"
        ]
        
        return indicators

class TechnicalRiskAnalyzer(RiskEvaluator):
    """技术风险分析器"""
    
    def analyze_component_reliability(self) -> Dict[str, float]:
        """分析组件可靠性"""
        # 假设有技术风险数据
        reliability_data = {}
        
        for rf_id, rf in self.risk_factors.items():
            if rf.category == RiskCategory.TECHNICAL:
                # 基于概率计算可靠性
                reliability = 1 - rf.probability
                reliability_data[rf_id] = reliability
        
        return reliability_data
    
    def analyze_failure_scenarios(self) -> List[Dict[str, Any]]:
        """分析失效情景"""
        failure_scenarios = []
        
        for rf in self.risk_factors.values():
            if rf.category == RiskCategory.TECHNICAL:
                scenario = {
                    'failure_type': rf.name,
                    'failure_probability': rf.probability,
                    'impact_level': rf.impact_magnitude,
                    'recovery_time': rf.time_to_impact,
                    'financial_impact': rf.financial_impact,
                    'mitigation': rf.mitigation_measures
                }
                failure_scenarios.append(scenario)
        
        return failure_scenarios

class FinancialRiskAnalyzer(RiskEvaluator):
    """财务风险分析器"""
    
    def calculate_var(self, confidence_level: float = 0.95, time_horizon: int = 1) -> float:
        """计算风险价值 (VaR)"""
        # 简化的VaR计算
        losses = [rf.probability * rf.financial_impact for rf in self.risk_factors.values()]
        
        if not losses:
            return 0
        
        sorted_losses = sorted(losses, reverse=True)
        var_index = int(len(sorted_losses) * (1 - confidence_level))
        
        return sorted_losses[var_index] if var_index < len(sorted_losses) else 0
    
    def analyze_sensitivity_to_market_changes(self) -> Dict[str, float]:
        """分析对市场变化的敏感性"""
        market_risks = [rf for rf in self.risk_factors.values() if rf.category == RiskCategory.MARKET]
        
        sensitivity = {}
        for rf in market_risks:
            # 计算市场风险敏感性
            market_sensitivity = rf.probability * rf.impact_magnitude
            sensitivity[rf.id] = market_sensitivity
        
        return sensitivity

class OperationalRiskAnalyzer(RiskEvaluator):
    """运营风险分析器"""
    
    def analyze_downtime_risks(self) -> Dict[str, float]:
        """分析停机风险"""
        downtime_risks = {}
        
        for rf in self.risk_factors.values():
            if rf.impact_type == ImpactType.OPERATIONAL_DISRUPTION:
                # 计算停机风险
                downtime_risk = rf.probability * rf.impact_magnitude
                downtime_risks[rf.id] = downtime_risk
        
        return downtime_risks
    
    def calculate_capacity_utilization_risk(self) -> float:
        """计算容量利用风险"""
        operational_risks = [rf for rf in self.risk_factors.values() 
                           if rf.impact_type == ImpactType.OPERATIONAL_DISRUPTION]
        
        if not operational_risks:
            return 0
        
        # 简化的容量利用风险计算
        total_risk = sum(rf.probability * rf.impact_magnitude for rf in operational_risks)
        return min(1.0, total_risk)