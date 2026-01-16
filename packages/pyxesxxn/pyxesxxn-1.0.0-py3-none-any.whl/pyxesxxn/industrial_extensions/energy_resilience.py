"""
能源系统韧性评估与应急响应模块

工业能源系统在极端情况下的韧性评估与应急响应策略
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from .base import (
    BaseIndustrialExtension,
    OptimizationObjective,
    OptimizationResult,
    EnergyCalculator,
    TimeSeriesGenerator,
    ResultAnalyzer
)


class ThreatType(Enum):
    """威胁类型"""
    NATURAL_DISASTER = "natural_disaster"
    CYBER_ATTACK = "cyber_attack"
    EQUIPMENT_FAILURE = "equipment_failure"
    SUPPLY_DISRUPTION = "supply_disruption"
    EXTREME_WEATHER = "extreme_weather"
    GRID_OUTAGE = "grid_outage"
    DEMAND_SURGE = "demand_surge"


class ResilienceLevel(Enum):
    """韧性等级"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ResponseStrategy(Enum):
    """响应策略"""
    LOAD_SHEDDING = "load_shedding"
    ISLANDING = "islanding"
    EMERGENCY_GENERATION = "emergency_generation"
    STORAGE_DISCHARGE = "storage_discharge"
    DEMAND_RESPONSE = "demand_response"
    NETWORK_RECONFIGURATION = "network_reconfiguration"
    EXTERNAL_SUPPORT = "external_support"


@dataclass
class ThreatScenario:
    """威胁场景"""
    scenario_id: str
    threat_type: ThreatType
    description: str
    probability: float  # 0-1
    impact_severity: float  # 0-1
    duration: timedelta
    affected_components: List[str]
    start_time: datetime
    end_time: datetime


@dataclass
class ResilienceMetric:
    """韧性指标"""
    metric_id: str
    metric_name: str
    metric_type: str  # robustness, recoverability, adaptability, resourcefulness
    current_value: float
    target_value: float
    unit: str
    threshold_warning: float
    threshold_critical: float


@dataclass
class EmergencyResponse:
    """应急响应"""
    response_id: str
    threat_scenario_id: str
    response_strategy: ResponseStrategy
    trigger_time: datetime
    response_time: timedelta
    affected_components: List[str]
    response_actions: List[Dict[str, Any]]
    effectiveness: float  # 0-1
    cost: float  # 元


@dataclass
class ResilienceAssessment:
    """韧性评估"""
    assessment_id: str
    assessment_date: datetime
    overall_resilience_score: float  # 0-1
    resilience_level: ResilienceLevel
    metrics: Dict[str, ResilienceMetric]
    identified_vulnerabilities: List[str]
    recommended_improvements: List[Dict[str, Any]]


class EnergyResilienceAssessor(BaseIndustrialExtension):
    """能源韧性评估器
    
    工业能源系统在极端情况下的韧性评估与应急响应策略
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化能源韧性评估器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - threat_scenarios: 威胁场景列表
            - resilience_metrics: 韧性指标列表
            - emergency_responses: 应急响应列表
            - resilience_assessments: 韧性评估列表
        """
        super().__init__(config)
        
        self.threat_scenarios: Dict[str, ThreatScenario] = {}
        self.resilience_metrics: Dict[str, ResilienceMetric] = {}
        self.emergency_responses: Dict[str, EmergencyResponse] = {}
        self.resilience_assessments: Dict[str, ResilienceAssessment] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'threat_scenarios' in config:
            for scenario_config in config['threat_scenarios']:
                scenario = ThreatScenario(**scenario_config)
                self.threat_scenarios[scenario.scenario_id] = scenario
        
        if 'resilience_metrics' in config:
            for metric_config in config['resilience_metrics']:
                metric = ResilienceMetric(**metric_config)
                self.resilience_metrics[metric.metric_id] = metric
        
        if 'emergency_responses' in config:
            for response_config in config['emergency_responses']:
                response = EmergencyResponse(**response_config)
                self.emergency_responses[response.response_id] = response
        
        if 'resilience_assessments' in config:
            for assessment_config in config['resilience_assessments']:
                assessment = ResilienceAssessment(**assessment_config)
                self.resilience_assessments[assessment.assessment_id] = assessment
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.threat_scenarios:
                print("警告: 未配置威胁场景")
            
            if not self.resilience_metrics:
                print("警告: 未配置韧性指标")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_threat_scenario(self, scenario: ThreatScenario):
        """添加威胁场景
        
        Parameters
        ----------
        scenario : ThreatScenario
            威胁场景
        """
        self.threat_scenarios[scenario.scenario_id] = scenario
    
    def add_resilience_metric(self, metric: ResilienceMetric):
        """添加韧性指标
        
        Parameters
        ----------
        metric : ResilienceMetric
            韧性指标
        """
        self.resilience_metrics[metric.metric_id] = metric
    
    def add_emergency_response(self, response: EmergencyResponse):
        """添加应急响应
        
        Parameters
        ----------
        response : EmergencyResponse
            应急响应
        """
        self.emergency_responses[response.response_id] = response
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.RELIABILITY,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化韧性
        
        Parameters
        ----------
        objective : OptimizationObjective
            优化目标
        time_horizon : int
            优化时间范围（小时）
        **kwargs
            其他参数
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        if not self.initialized:
            return OptimizationResult(
                success=False,
                objective_value=0.0,
                total_cost=0.0,
                total_carbon_emissions=0.0,
                energy_schedule={},
                component_utilization={},
                convergence_time=0.0,
                error_message="模块未初始化"
            )
        
        start_time = datetime.now()
        
        try:
            if objective == OptimizationObjective.COST:
                result = self._optimize_cost(time_horizon)
            elif objective == OptimizationObjective.CARBON:
                result = self._optimize_carbon(time_horizon)
            elif objective == OptimizationObjective.RELIABILITY:
                result = self._optimize_reliability(time_horizon)
            elif objective == OptimizationObjective.EFFICIENCY:
                result = self._optimize_efficiency(time_horizon)
            else:
                result = self._optimize_multi_objective(time_horizon)
            
            convergence_time = (datetime.now() - start_time).total_seconds()
            result.convergence_time = convergence_time
            
            self.results = {
                'optimization_result': result,
                'objective': objective,
                'time_horizon': time_horizon
            }
            
            return result
            
        except Exception as e:
            return OptimizationResult(
                success=False,
                objective_value=0.0,
                total_cost=0.0,
                total_carbon_emissions=0.0,
                energy_schedule={},
                component_utilization={},
                convergence_time=0.0,
                error_message=str(e)
            )
    
    def _optimize_cost(self, time_horizon: int) -> OptimizationResult:
        """成本优化
        
        Parameters
        ----------
        time_horizon : int
            时间范围
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        total_cost = 0.0
        total_carbon = 0.0
        energy_schedule = {}
        component_utilization = {}
        
        for scenario_id, scenario in self.threat_scenarios.items():
            hourly_cost = scenario.impact_severity * 1000.0
            schedule = []
            
            for hour in range(time_horizon):
                mitigation_cost = hourly_cost * 0.3
                total_cost += mitigation_cost
                
                schedule.append({
                    'hour': hour,
                    'impact_severity': scenario.impact_severity,
                    'mitigation_cost': mitigation_cost
                })
            
            energy_schedule[scenario_id] = schedule
            component_utilization[scenario_id] = 0.7
        
        for response_id, response in self.emergency_responses.items():
            utilization = 0.5 + np.random.random() * 0.4
            component_utilization[response_id] = utilization
            
            response_cost = response.cost * 0.1 / time_horizon
            total_cost += response_cost
        
        return OptimizationResult(
            success=True,
            objective_value=total_cost,
            total_cost=total_cost,
            total_carbon_emissions=total_carbon,
            energy_schedule=energy_schedule,
            component_utilization=component_utilization,
            convergence_time=0.0,
            additional_metrics={
                'cost_components': {
                    'mitigation_cost': total_cost * 0.7,
                    'response_cost': total_cost * 0.3
                },
                'emission_sources': {}
            }
        )
    
    def _optimize_carbon(self, time_horizon: int) -> OptimizationResult:
        """碳排放优化
        
        Parameters
        ----------
        time_horizon : int
            时间范围
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        total_cost = 0.0
        total_carbon = 0.0
        energy_schedule = {}
        component_utilization = {}
        
        for scenario_id, scenario in self.threat_scenarios.items():
            hourly_emissions = scenario.impact_severity * 500.0
            schedule = []
            
            for hour in range(time_horizon):
                mitigation_emissions = hourly_emissions * 0.2
                total_carbon += mitigation_emissions
                
                schedule.append({
                    'hour': hour,
                    'impact_severity': scenario.impact_severity,
                    'mitigation_emissions': mitigation_emissions
                })
            
            energy_schedule[scenario_id] = schedule
            component_utilization[scenario_id] = 0.8
        
        for response_id, response in self.emergency_responses.items():
            component_utilization[response_id] = 0.7
        
        return OptimizationResult(
            success=True,
            objective_value=total_carbon,
            total_cost=total_cost,
            total_carbon_emissions=total_carbon,
            energy_schedule=energy_schedule,
            component_utilization=component_utilization,
            convergence_time=0.0,
            additional_metrics={
                'cost_components': {},
                'emission_sources': {
                    'threat_mitigation': total_carbon
                }
            }
        )
    
    def _optimize_reliability(self, time_horizon: int) -> OptimizationResult:
        """可靠性优化
        
        Parameters
        ----------
        time_horizon : int
            时间范围
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        total_cost = 0.0
        total_carbon = 0.0
        energy_schedule = {}
        component_utilization = {}
        
        reliability_score = 0.0
        
        for scenario_id, scenario in self.threat_scenarios.items():
            schedule = []
            
            for hour in range(time_horizon):
                resilience = 1.0 - scenario.impact_severity * (0.2 + np.random.random() * 0.2)
                reliability_score += resilience
                
                schedule.append({
                    'hour': hour,
                    'impact_severity': scenario.impact_severity,
                    'resilience': resilience
                })
            
            energy_schedule[scenario_id] = schedule
            component_utilization[scenario_id] = 0.85
        
        for response_id, response in self.emergency_responses.items():
            component_utilization[response_id] = 0.9
            reliability_score += response.effectiveness
        
        return OptimizationResult(
            success=True,
            objective_value=reliability_score,
            total_cost=total_cost,
            total_carbon_emissions=total_carbon,
            energy_schedule=energy_schedule,
            component_utilization=component_utilization,
            convergence_time=0.0,
            additional_metrics={
                'reliability_score': reliability_score,
                'cost_components': {},
                'emission_sources': {}
            }
        )
    
    def _optimize_efficiency(self, time_horizon: int) -> OptimizationResult:
        """效率优化
        
        Parameters
        ----------
        time_horizon : int
            时间范围
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        total_cost = 0.0
        total_carbon = 0.0
        energy_schedule = {}
        component_utilization = {}
        
        efficiency_score = 0.0
        
        for scenario_id, scenario in self.threat_scenarios.items():
            schedule = []
            
            for hour in range(time_horizon):
                efficiency = 1.0 - scenario.impact_severity * (0.1 + np.random.random() * 0.15)
                efficiency_score += efficiency
                
                schedule.append({
                    'hour': hour,
                    'impact_severity': scenario.impact_severity,
                    'efficiency': efficiency
                })
            
            energy_schedule[scenario_id] = schedule
            component_utilization[scenario_id] = 0.8
        
        for response_id, response in self.emergency_responses.items():
            component_utilization[response_id] = 0.75
            efficiency_score += response.effectiveness
        
        return OptimizationResult(
            success=True,
            objective_value=efficiency_score,
            total_cost=total_cost,
            total_carbon_emissions=total_carbon,
            energy_schedule=energy_schedule,
            component_utilization=component_utilization,
            convergence_time=0.0,
            additional_metrics={
                'efficiency_score': efficiency_score,
                'cost_components': {},
                'emission_sources': {}
            }
        )
    
    def _optimize_multi_objective(self, time_horizon: int) -> OptimizationResult:
        """多目标优化
        
        Parameters
        ----------
        time_horizon : int
            时间范围
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        weights = {'cost': 0.3, 'carbon': 0.2, 'reliability': 0.5}
        
        cost_result = self._optimize_cost(time_horizon)
        carbon_result = self._optimize_carbon(time_horizon)
        reliability_result = self._optimize_reliability(time_horizon)
        
        normalized_cost = abs(cost_result.total_cost) / 10000.0
        normalized_carbon = abs(carbon_result.total_carbon_emissions) / 1000.0
        normalized_reliability = 1.0 - (reliability_result.objective_value / 
                                       (len(self.threat_scenarios) + len(self.emergency_responses)))
        
        objective_value = (
            weights['cost'] * normalized_cost +
            weights['carbon'] * normalized_carbon +
            weights['reliability'] * normalized_reliability
        )
        
        return OptimizationResult(
            success=True,
            objective_value=objective_value,
            total_cost=cost_result.total_cost,
            total_carbon_emissions=carbon_result.total_carbon_emissions,
            energy_schedule=cost_result.energy_schedule,
            component_utilization=cost_result.component_utilization,
            convergence_time=0.0,
            additional_metrics={
                'multi_objective_weights': weights,
                'normalized_scores': {
                    'cost': normalized_cost,
                    'carbon': normalized_carbon,
                    'reliability': normalized_reliability
                },
                'cost_components': cost_result.additional_metrics.get('cost_components', {}),
                'emission_sources': carbon_result.additional_metrics.get('emission_sources', {})
            }
        )
    
    def assess_resilience(
        self,
        component_ids: List[str],
        threat_scenarios: List[str] = None
    ) -> ResilienceAssessment:
        """评估韧性
        
        Parameters
        ----------
        component_ids : List[str]
            组件ID列表
        threat_scenarios : List[str], optional
            威胁场景ID列表
        
        Returns
        -------
        ResilienceAssessment
            韧性评估结果
        """
        if threat_scenarios is None:
            threat_scenarios = list(self.threat_scenarios.keys())
        
        metrics = {}
        overall_score = 0.0
        identified_vulnerabilities = []
        recommended_improvements = []
        
        for metric_id, metric in self.resilience_metrics.items():
            if metric.metric_type == 'robustness':
                current_value = 0.7 + np.random.random() * 0.25
            elif metric.metric_type == 'recoverability':
                current_value = 0.6 + np.random.random() * 0.3
            elif metric.metric_type == 'adaptability':
                current_value = 0.65 + np.random.random() * 0.25
            else:  # resourcefulness
                current_value = 0.75 + np.random.random() * 0.2
            
            metrics[metric_id] = ResilienceMetric(
                metric_id=metric.metric_id,
                metric_name=metric.metric_name,
                metric_type=metric.metric_type,
                current_value=current_value,
                target_value=metric.target_value,
                unit=metric.unit,
                threshold_warning=metric.threshold_warning,
                threshold_critical=metric.threshold_critical
            )
            
            overall_score += current_value
            
            if current_value < metric.threshold_critical:
                identified_vulnerabilities.append({
                    'metric_id': metric_id,
                    'severity': 'critical',
                    'current_value': current_value,
                    'threshold': metric.threshold_critical
                })
                
                recommended_improvements.append({
                    'metric_id': metric_id,
                    'improvement_type': 'critical_upgrade',
                    'description': f"{metric.metric_name}严重低于阈值，需要立即升级",
                    'priority': 1,
                    'estimated_cost': 50000.0,
                    'expected_improvement': metric.target_value - current_value
                })
            elif current_value < metric.threshold_warning:
                identified_vulnerabilities.append({
                    'metric_id': metric_id,
                    'severity': 'warning',
                    'current_value': current_value,
                    'threshold': metric.threshold_warning
                })
                
                recommended_improvements.append({
                    'metric_id': metric_id,
                    'improvement_type': 'preventive_maintenance',
                    'description': f"{metric.metric_name}低于警告阈值，建议进行预防性维护",
                    'priority': 2,
                    'estimated_cost': 20000.0,
                    'expected_improvement': metric.target_value - current_value
                })
        
        overall_score = overall_score / len(metrics) if metrics else 0.0
        
        if overall_score > 0.8:
            resilience_level = ResilienceLevel.VERY_HIGH
        elif overall_score > 0.6:
            resilience_level = ResilienceLevel.HIGH
        elif overall_score > 0.4:
            resilience_level = ResilienceLevel.MEDIUM
        elif overall_score > 0.2:
            resilience_level = ResilienceLevel.LOW
        else:
            resilience_level = ResilienceLevel.VERY_LOW
        
        assessment = ResilienceAssessment(
            assessment_id=f"assessment_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            assessment_date=datetime.now(),
            overall_resilience_score=overall_score,
            resilience_level=resilience_level,
            metrics=metrics,
            identified_vulnerabilities=identified_vulnerabilities,
            recommended_improvements=recommended_improvements
        )
        
        self.resilience_assessments[assessment.assessment_id] = assessment
        return assessment
    
    def develop_emergency_response_plan(
        self,
        threat_scenario_id: str,
        response_strategies: List[ResponseStrategy]
    ) -> EmergencyResponse:
        """开发应急响应计划
        
        Parameters
        ----------
        threat_scenario_id : str
            威胁场景ID
        response_strategies : List[ResponseStrategy]
            响应策略列表
        
        Returns
        -------
        EmergencyResponse
            应急响应
        """
        if threat_scenario_id not in self.threat_scenarios:
            raise ValueError("威胁场景不存在")
        
        scenario = self.threat_scenarios[threat_scenario_id]
        
        response_actions = []
        total_cost = 0.0
        
        for strategy in response_strategies:
            if strategy == ResponseStrategy.LOAD_SHEDDING:
                action = {
                    'strategy': 'load_shedding',
                    'description': '削减非关键负荷',
                    'priority': 1,
                    'implementation_time': timedelta(minutes=5),
                    'expected_reduction': 0.3,
                    'cost': 10000.0
                }
            elif strategy == ResponseStrategy.ISLANDING:
                action = {
                    'strategy': 'islanding',
                    'description': '切换到孤岛运行模式',
                    'priority': 1,
                    'implementation_time': timedelta(minutes=15),
                    'expected_reduction': 0.5,
                    'cost': 50000.0
                }
            elif strategy == ResponseStrategy.EMERGENCY_GENERATION:
                action = {
                    'strategy': 'emergency_generation',
                    'description': '启动应急发电设备',
                    'priority': 1,
                    'implementation_time': timedelta(minutes=10),
                    'expected_reduction': 0.4,
                    'cost': 30000.0
                }
            elif strategy == ResponseStrategy.STORAGE_DISCHARGE:
                action = {
                    'strategy': 'storage_discharge',
                    'description': '释放储能系统',
                    'priority': 2,
                    'implementation_time': timedelta(minutes=2),
                    'expected_reduction': 0.25,
                    'cost': 5000.0
                }
            elif strategy == ResponseStrategy.DEMAND_RESPONSE:
                action = {
                    'strategy': 'demand_response',
                    'description': '实施需求响应',
                    'priority': 2,
                    'implementation_time': timedelta(minutes=30),
                    'expected_reduction': 0.2,
                    'cost': 15000.0
                }
            elif strategy == ResponseStrategy.NETWORK_RECONFIGURATION:
                action = {
                    'strategy': 'network_reconfiguration',
                    'description': '重新配置网络拓扑',
                    'priority': 1,
                    'implementation_time': timedelta(minutes=20),
                    'expected_reduction': 0.35,
                    'cost': 25000.0
                }
            elif strategy == ResponseStrategy.EXTERNAL_SUPPORT:
                action = {
                    'strategy': 'external_support',
                    'description': '请求外部支援',
                    'priority': 3,
                    'implementation_time': timedelta(hours=1),
                    'expected_reduction': 0.15,
                    'cost': 100000.0
                }
            else:
                continue
            
            response_actions.append(action)
            total_cost += action['cost']
        
        effectiveness = 1.0 - scenario.impact_severity * (1.0 - sum(a['expected_reduction'] for a in response_actions) / len(response_strategies))
        
        response = EmergencyResponse(
            response_id=f"response_{threat_scenario_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            threat_scenario_id=threat_scenario_id,
            response_strategy=response_strategies[0] if response_strategies else ResponseStrategy.LOAD_SHEDDING,
            trigger_time=datetime.now(),
            response_time=timedelta(minutes=15),
            affected_components=scenario.affected_components,
            response_actions=response_actions,
            effectiveness=effectiveness,
            cost=total_cost
        )
        
        self.emergency_responses[response.response_id] = response
        return response
    
    def simulate_threat_impact(
        self,
        scenario_id: str,
        time_horizon: int = 24
    ) -> Dict[str, Any]:
        """模拟威胁影响
        
        Parameters
        ----------
        scenario_id : str
            场景ID
        time_horizon : int
            时间范围
        
        Returns
        -------
        Dict[str, Any]
            威胁影响模拟结果
        """
        if scenario_id not in self.threat_scenarios:
            return {'error': '威胁场景不存在'}
        
        scenario = self.threat_scenarios[scenario_id]
        
        impact_timeline = []
        total_energy_loss = 0.0
        total_cost = 0.0
        
        for hour in range(time_horizon):
            impact_factor = scenario.impact_severity * (0.8 + np.random.random() * 0.2)
            energy_loss = impact_factor * 1000.0  # kWh
            total_energy_loss += energy_loss
            
            cost = energy_loss * 1.2  # 元/kWh
            total_cost += cost
            
            impact_timeline.append({
                'hour': hour,
                'impact_factor': impact_factor,
                'energy_loss': energy_loss,
                'cost': cost
            })
        
        return {
            'scenario_id': scenario_id,
            'threat_type': scenario.threat_type.value,
            'impact_timeline': impact_timeline,
            'total_energy_loss': total_energy_loss,
            'total_cost': total_cost,
            'average_impact': np.mean([t['impact_factor'] for t in impact_timeline]),
            'peak_impact': max([t['impact_factor'] for t in impact_timeline]),
            'affected_components': scenario.affected_components,
            'duration': scenario.duration
        }
    
    def generate_resilience_report(self) -> Dict[str, Any]:
        """生成韧性报告
        
        Returns
        -------
        Dict[str, Any]
            韧性报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        latest_assessment = list(self.resilience_assessments.values())[-1] if self.resilience_assessments else None
        
        report = {
            'summary': {
                'total_threat_scenarios': len(self.threat_scenarios),
                'total_resilience_metrics': len(self.resilience_metrics),
                'total_emergency_responses': len(self.emergency_responses),
                'total_assessments': len(self.resilience_assessments),
                'overall_resilience_score': latest_assessment.overall_resilience_score if latest_assessment else 0.0,
                'resilience_level': latest_assessment.resilience_level.value if latest_assessment else 'unknown',
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'threat_scenario_details': {},
            'resilience_metric_details': {},
            'emergency_response_details': {},
            'assessment_details': {}
        }
        
        for scenario_id, scenario in self.threat_scenarios.items():
            report['threat_scenario_details'][scenario_id] = {
                'type': scenario.threat_type.value,
                'description': scenario.description,
                'probability': scenario.probability,
                'impact_severity': scenario.impact_severity,
                'duration': str(scenario.duration),
                'affected_components': scenario.affected_components,
                'start_time': scenario.start_time,
                'end_time': scenario.end_time
            }
        
        for metric_id, metric in self.resilience_metrics.items():
            report['resilience_metric_details'][metric_id] = {
                'name': metric.metric_name,
                'type': metric.metric_type,
                'current_value': metric.current_value,
                'target_value': metric.target_value,
                'unit': metric.unit,
                'threshold_warning': metric.threshold_warning,
                'threshold_critical': metric.threshold_critical,
                'gap': metric.target_value - metric.current_value,
                'status': 'critical' if metric.current_value < metric.threshold_critical else 'warning' if metric.current_value < metric.threshold_warning else 'normal'
            }
        
        for response_id, response in self.emergency_responses.items():
            report['emergency_response_details'][response_id] = {
                'threat_scenario_id': response.threat_scenario_id,
                'response_strategy': response.response_strategy.value,
                'trigger_time': response.trigger_time,
                'response_time': str(response.response_time),
                'affected_components': response.affected_components,
                'number_of_actions': len(response.response_actions),
                'effectiveness': response.effectiveness,
                'cost': response.cost
            }
        
        if latest_assessment:
            report['assessment_details'] = {
                'assessment_id': latest_assessment.assessment_id,
                'assessment_date': latest_assessment.assessment_date,
                'overall_resilience_score': latest_assessment.overall_resilience_score,
                'resilience_level': latest_assessment.resilience_level.value,
                'number_of_metrics': len(latest_assessment.metrics),
                'number_of_vulnerabilities': len(latest_assessment.identified_vulnerabilities),
                'number_of_improvements': len(latest_assessment.recommended_improvements),
                'vulnerability_severity': {
                    'critical': sum(1 for v in latest_assessment.identified_vulnerabilities if v['severity'] == 'critical'),
                    'warning': sum(1 for v in latest_assessment.identified_vulnerabilities if v['severity'] == 'warning')
                },
                'improvement_priority': {
                    'high': sum(1 for i in latest_assessment.recommended_improvements if i['priority'] == 1),
                    'medium': sum(1 for i in latest_assessment.recommended_improvements if i['priority'] == 2),
                    'low': sum(1 for i in latest_assessment.recommended_improvements if i['priority'] >= 3)
                }
            }
        
        return report