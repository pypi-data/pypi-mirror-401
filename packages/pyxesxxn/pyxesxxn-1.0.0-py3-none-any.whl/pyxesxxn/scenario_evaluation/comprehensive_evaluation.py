"""
综合评估模块

整合经济性、可靠性、环境、社会和风险评估结果，提供：
- 综合评分计算：多维度评估结果整合
- 权重管理：不同评估维度的权重配置
- 权衡分析：各维度之间的权衡关系
- 综合报告：综合性评估报告生成
- 决策支持：基于综合评估的决策建议
- 基准比较：与行业标准或竞争对手比较
- 综合指标：综合可持续发展指标
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Tuple
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
import math
from collections import defaultdict

from .evaluation_framework import Evaluator, EvaluationContext, EvaluationResult, EvaluationStatus, EvaluationType
from .economic_evaluation import EconomicResult
from .reliability_evaluation import ReliabilityResult
from .environment_evaluation import EnvironmentalResult
from .social_evaluation import SocialResult
from .risk_evaluation import RiskResult

class EvaluationDimension(Enum):
    """评估维度"""
    ECONOMIC = "economic"                    # 经济性
    RELIABILITY = "reliability"              # 可靠性
    ENVIRONMENTAL = "environmental"           # 环境性
    SOCIAL = "social"                        # 社会性
    RISK = "risk"                           # 风险性

class WeightingMethod(Enum):
    """权重方法"""
    EQUAL_WEIGHTING = "equal_weighting"        # 等权重
    STAKEHOLDER_PREFERENCE = "stakeholder_preference"  # 利益相关者偏好
    ANALYTIC_HIERARCHY_PROCESS = "analytic_hierarchy_process"  # 层次分析法
    ENTROPY_WEIGHTING = "entropy_weighting"   # 熵权法
    CUSTOM_WEIGHTING = "custom_weighting"     # 自定义权重

class RankingMethod(Enum):
    """排名方法"""
    WEIGHTED_SCORING = "weighted_scoring"      # 加权评分
    TOPSIS = "topsis"                         # TOPSIS法
    PROMETHEE = "promethee"                   # PROMETHEE法
    ELECTRE = "electre"                       # ELECTRE法

@dataclass
class DimensionWeight:
    """维度权重"""
    dimension: EvaluationDimension
    weight: float
    justification: str                        # 权重理由
    confidence_level: float                   # 置信度
    
    def __post_init__(self):
        if not (0 <= self.weight <= 1):
            raise ValueError("权重必须在0-1之间")
        if not (0 <= self.confidence_level <= 1):
            raise ValueError("置信度必须在0-1之间")

@dataclass
class CriterionScore:
    """标准评分"""
    criterion_name: str
    score: float                              # 评分 (0-10)
    weight: float                            # 权重
    data_quality: float                      # 数据质量 (0-1)
    uncertainty: float                       # 不确定性 (0-1)
    benchmark_value: Optional[float] = None # 基准值
    best_practice_value: Optional[float] = None  # 最佳实践值

@dataclass
class BenchmarkComparison:
    """基准比较"""
    metric_name: str
    project_value: float
    industry_average: float
    best_in_class: float
    percentile_rank: float                   # 百分位排名
    gap_analysis: Dict[str, float]           # 差距分析
    
@dataclass
class TradeOffAnalysis:
    """权衡分析"""
    dimension_pairs: List[Tuple[EvaluationDimension, EvaluationDimension]]
    trade_off_ratios: Dict[Tuple[EvaluationDimension, EvaluationDimension], float]
    sensitivity_analysis: Dict[str, float]   # 敏感性分析
    critical_thresholds: Dict[str, float]    # 关键阈值

@dataclass
class ComprehensiveIndicators:
    """综合指标"""
    # 总体评分
    overall_sustainability_score: float       # 综合可持续性评分
    overall_performance_index: float         # 综合绩效指数
    
    # 分维度评分
    economic_performance_score: float
    reliability_performance_score: float
    environmental_performance_score: float
    social_performance_score: float
    risk_performance_score: float
    
    # 综合指数
    sustainability_index: Dict[str, float]    # 可持续发展指数
    competitiveness_index: float              # 竞争力指数
    resilience_index: float                   # 韧性指数
    
    # 特殊指标
    triple_bottom_line_score: float          # 底线三重评分
    stakeholder_value_score: float           # 利益相关者价值评分
    future_readiness_score: float            # 未来就绪度评分
    
    # 基准比较
    benchmark_performance: Dict[str, BenchmarkComparison]
    
    # 权衡分析
    trade_off_analysis: TradeOffAnalysis

@dataclass
class ComprehensiveResult:
    """综合评估结果"""
    # 执行信息
    evaluation_id: str
    timestamp: datetime
    evaluation_method: str
    weighting_method: WeightingMethod
    ranking_method: RankingMethod
    
    # 权重配置
    dimension_weights: List[DimensionWeight]
    total_weight: float
    
    # 综合指标
    indicators: ComprehensiveIndicators
    
    # 详细评分
    detailed_scores: Dict[str, CriterionScore]
    
    # 排名结果
    ranking: Dict[str, int]                   # 各维度排名
    
    # 综合评估结论
    overall_assessment: str                  # 总体评估
    key_strengths: List[str]                 # 主要优势
    key_weaknesses: List[str]                # 主要劣势
    critical_issues: List[str]               # 关键问题
    
    # 决策建议
    immediate_actions: List[str]             # 即时行动建议
    strategic_recommendations: List[str]     # 战略建议
    improvement_priorities: List[str]        # 改进优先级
    
    # 未来展望
    future_outlook: str                     # 未来展望
    monitoring_recommendations: List[str]   # 监控建议

class ComprehensiveEvaluator(Evaluator):
    """综合评估器"""
    
    def __init__(self, assessment_period: int = 365):
        super().__init__("ComprehensiveEvaluator", EvaluationType.COMPREHENSIVE)
        self.assessment_period = assessment_period
        self.weighting_method = WeightingMethod.EQUAL_WEIGHTING
        self.ranking_method = RankingMethod.WEIGHTED_SCORING
        
        # 评估结果缓存
        self.evaluation_results: Dict[EvaluationType, EvaluationResult] = {}
        
        # 维度权重
        self.dimension_weights: Dict[EvaluationDimension, DimensionWeight] = {}
        
        # 基准数据
        self.benchmark_data: Dict[str, Any] = {}
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行综合评估"""
        start_time = datetime.now()
        self.logger.info("开始综合评估")
        
        try:
            # 收集各维度评估结果
            self._collect_evaluation_results(context)
            
            # 配置权重
            self._configure_weights(context)
            
            # 计算综合指标
            comprehensive_indicators = self._calculate_comprehensive_indicators()
            
            # 执行基准比较
            benchmark_comparisons = self._perform_benchmark_comparison()
            
            # 进行权衡分析
            trade_off_analysis = self._conduct_trade_off_analysis()
            
            # 生成综合结果
            comprehensive_result = ComprehensiveResult(
                evaluation_id=f"comp_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                evaluation_method="Multi-dimensional Comprehensive Assessment",
                weighting_method=self.weighting_method,
                ranking_method=self.ranking_method,
                dimension_weights=list(self.dimension_weights.values()),
                total_weight=sum(dw.weight for dw in self.dimension_weights.values()),
                indicators=comprehensive_indicators,
                detailed_scores=self._generate_detailed_scores(),
                ranking=self._calculate_rankings(),
                overall_assessment=self._generate_overall_assessment(comprehensive_indicators),
                key_strengths=self._identify_key_strengths(),
                key_weaknesses=self._identify_key_weaknesses(),
                critical_issues=self._identify_critical_issues(),
                immediate_actions=self._suggest_immediate_actions(),
                strategic_recommendations=self._suggest_strategic_recommendations(),
                improvement_priorities=self._prioritize_improvements(),
                future_outlook=self._generate_future_outlook(),
                monitoring_recommendations=self._suggest_monitoring_recommendations()
            )
            
            # 创建标准评估结果
            metrics = {
                'overall_sustainability_score': comprehensive_result.indicators.overall_sustainability_score,
                'overall_performance_index': comprehensive_result.indicators.overall_performance_index,
                'economic_score': comprehensive_result.indicators.economic_performance_score,
                'reliability_score': comprehensive_result.indicators.reliability_performance_score,
                'environmental_score': comprehensive_result.indicators.environmental_performance_score,
                'social_score': comprehensive_result.indicators.social_performance_score,
                'risk_score': comprehensive_result.indicators.risk_performance_score
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={
                    'comprehensive_result': comprehensive_result,
                    'benchmark_comparisons': benchmark_comparisons,
                    'trade_off_analysis': trade_off_analysis
                },
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("综合评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"综合评估失败: {str(e)}")
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
        required_evaluations = [
            EvaluationType.ECONOMIC,
            EvaluationType.RELIABILITY,
            EvaluationType.ENVIRONMENTAL,
            EvaluationType.SOCIAL,
            EvaluationType.RISK
        ]
        
        for eval_type in required_evaluations:
            if eval_type not in context.evaluation_results:
                self.logger.warning(f"缺少必需评估结果: {eval_type}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['economic_results', 'reliability_results', 'environmental_results', 
                'social_results', 'risk_results', 'stakeholder_preferences', 'benchmark_data']
    
    def set_weighting_method(self, method: WeightingMethod, custom_weights: Optional[Dict[EvaluationDimension, float]] = None):
        """设置权重方法"""
        self.weighting_method = method
        
        if method == WeightingMethod.EQUAL_WEIGHTING:
            # 等权重分配
            weight_value = 1.0 / len(EvaluationDimension)
            for dimension in EvaluationDimension:
                self.dimension_weights[dimension] = DimensionWeight(
                    dimension=dimension,
                    weight=weight_value,
                    justification="等权重分配",
                    confidence_level=1.0
                )
        
        elif method == WeightingMethod.CUSTOM_WEIGHTING and custom_weights:
            # 自定义权重
            for dimension, weight in custom_weights.items():
                self.dimension_weights[dimension] = DimensionWeight(
                    dimension=dimension,
                    weight=weight,
                    justification="自定义权重",
                    confidence_level=0.8
                )
    
    def set_ranking_method(self, method: RankingMethod):
        """设置排名方法"""
        self.ranking_method = method
    
    def add_evaluation_result(self, eval_type: EvaluationType, result: EvaluationResult):
        """添加评估结果"""
        self.evaluation_results[eval_type] = result
    
    def _collect_evaluation_results(self, context: EvaluationContext):
        """收集各维度评估结果"""
        # 从上下文中获取各评估结果
        self.evaluation_results = {}
        
        if 'economic_results' in context.metadata:
            self.evaluation_results[EvaluationType.ECONOMIC] = context.metadata['economic_results']
        
        if 'reliability_results' in context.metadata:
            self.evaluation_results[EvaluationType.RELIABILITY] = context.metadata['reliability_results']
        
        if 'environmental_results' in context.metadata:
            self.evaluation_results[EvaluationType.ENVIRONMENTAL] = context.metadata['environmental_results']
        
        if 'social_results' in context.metadata:
            self.evaluation_results[EvaluationType.SOCIAL] = context.metadata['social_results']
        
        if 'risk_results' in context.metadata:
            self.evaluation_results[EvaluationType.RISK] = context.metadata['risk_results']
    
    def _configure_weights(self, context: EvaluationContext):
        """配置权重"""
        # 默认使用等权重
        if not self.dimension_weights:
            self.set_weighting_method(WeightingMethod.EQUAL_WEIGHTING)
        
        # 调整权重基于利益相关者偏好
        if 'stakeholder_preferences' in context.metadata:
            stakeholder_prefs = context.metadata['stakeholder_preferences']
            self._adjust_weights_from_stakeholder_input(stakeholder_prefs)
    
    def _adjust_weights_from_stakeholder_input(self, stakeholder_prefs: Dict[str, Any]):
        """基于利益相关者输入调整权重"""
        # 简化实现：根据利益相关者偏好调整权重
        if 'preference_weights' in stakeholder_prefs:
            pref_weights = stakeholder_prefs['preference_weights']
            total_pref = sum(pref_weights.values())
            
            for dimension, pref_value in pref_weights.items():
                try:
                    dim = EvaluationDimension(dimension)
                    if dim in self.dimension_weights:
                        # 将偏好转换为权重
                        normalized_pref = pref_value / total_pref
                        current_weight = self.dimension_weights[dim].weight
                        
                        # 加权平均
                        adjusted_weight = (current_weight * 0.7 + normalized_pref * 0.3)
                        self.dimension_weights[dim].weight = adjusted_weight
                        self.dimension_weights[dim].justification = "基于利益相关者偏好调整"
                except ValueError:
                    continue
    
    def _calculate_comprehensive_indicators(self) -> ComprehensiveIndicators:
        """计算综合指标"""
        # 获取各维度评分
        economic_score = self._get_dimension_score(EvaluationType.ECONOMIC)
        reliability_score = self._get_dimension_score(EvaluationType.RELIABILITY)
        environmental_score = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        social_score = self._get_dimension_score(EvaluationType.SOCIAL)
        risk_score = self._get_dimension_score(EvaluationType.RISK)
        
        # 计算加权总体评分
        overall_sustainability_score = sum(
            self.dimension_weights[EvaluationDimension.ECONOMIC].weight * economic_score +
            self.dimension_weights[EvaluationDimension.RELIABILITY].weight * reliability_score +
            self.dimension_weights[EvaluationDimension.ENVIRONMENTAL].weight * environmental_score +
            self.dimension_weights[EvaluationDimension.SOCIAL].weight * social_score +
            self.dimension_weights[EvaluationDimension.RISK].weight * risk_score
        )
        
        # 计算综合绩效指数
        overall_performance_index = (overall_sustainability_score + 
                                   self._calculate_competitiveness_index() +
                                   self._calculate_resilience_index()) / 3
        
        # 计算可持续发展指数
        sustainability_index = {
            'economic_sustainability': economic_score / 10,
            'environmental_sustainability': environmental_score / 10,
            'social_sustainability': social_score / 10,
            'institutional_sustainability': (reliability_score + risk_score) / 20
        }
        
        # 底线三重评分
        triple_bottom_line_score = (economic_score * 0.4 + 
                                  environmental_score * 0.3 + 
                                  social_score * 0.3)
        
        # 利益相关者价值评分
        stakeholder_value_score = (economic_score * 0.3 + reliability_score * 0.2 + 
                                 environmental_score * 0.2 + social_score * 0.3)
        
        # 未来就绪度评分
        future_readiness_score = (reliability_score * 0.3 + environmental_score * 0.3 + 
                                social_score * 0.2 + risk_score * 0.2)
        
        return ComprehensiveIndicators(
            overall_sustainability_score=overall_sustainability_score,
            overall_performance_index=overall_performance_index,
            economic_performance_score=economic_score,
            reliability_performance_score=reliability_score,
            environmental_performance_score=environmental_score,
            social_performance_score=social_score,
            risk_performance_score=risk_score,
            sustainability_index=sustainability_index,
            competitiveness_index=self._calculate_competitiveness_index(),
            resilience_index=self._calculate_resilience_index(),
            triple_bottom_line_score=triple_bottom_line_score,
            stakeholder_value_score=stakeholder_value_score,
            future_readiness_score=future_readiness_score,
            benchmark_performance={},
            trade_off_analysis=TradeOffAnalysis([], {}, {}, {})
        )
    
    def _get_dimension_score(self, eval_type: EvaluationType) -> float:
        """获取维度评分"""
        if eval_type not in self.evaluation_results:
            return 5.0  # 默认中性评分
        
        result = self.evaluation_results[eval_type]
        
        # 尝试从metrics中获取主要评分
        if 'metrics' in result:
            if eval_type == EvaluationType.ECONOMIC and 'net_present_value' in result.metrics:
                # 将NPV转换为评分（简化）
                npv = result.metrics['net_present_value']
                score = min(10, max(0, 5 + (npv / 1000000)))  # 假设100万为满分
                return score
            elif eval_type == EvaluationType.RELIABILITY and 'reliability_index' in result.metrics:
                return result.metrics['reliability_index'] * 10
            elif eval_type == EvaluationType.ENVIRONMENTAL and 'environmental_impact_score' in result.metrics:
                return result.metrics['environmental_impact_score']
            elif eval_type == EvaluationType.SOCIAL and 'overall_social_score' in result.metrics:
                return result.metrics['overall_social_score']
            elif eval_type == EvaluationType.RISK and 'overall_risk_score' in result.metrics:
                # 风险评分需要反转（风险越低评分越高）
                risk_score = result.metrics['overall_risk_score']
                return max(0, 10 - risk_score * 10)
        
        # 如果没有特定指标，返回默认值
        return 7.0
    
    def _calculate_competitiveness_index(self) -> float:
        """计算竞争力指数"""
        # 基于经济性、可靠性和环境性的竞争力分析
        economic = self._get_dimension_score(EvaluationType.ECONOMIC)
        reliability = self._get_dimension_score(EvaluationType.RELIABILITY)
        environmental = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        
        # 竞争力 = 经济性 * 0.4 + 可靠性 * 0.3 + 环境性 * 0.3
        competitiveness = (economic * 0.4 + reliability * 0.3 + environmental * 0.3)
        return min(10, max(0, competitiveness))
    
    def _calculate_resilience_index(self) -> float:
        """计算韧性指数"""
        # 基于可靠性、风险和环境性的韧性分析
        reliability = self._get_dimension_score(EvaluationType.RELIABILITY)
        risk = self._get_dimension_score(EvaluationType.RISK)
        environmental = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        
        # 韧性 = 可靠性 * 0.4 + 风险抗性 * 0.3 + 环境适应性 * 0.3
        resilience = (reliability * 0.4 + risk * 0.3 + environmental * 0.3)
        return min(10, max(0, resilience))
    
    def _perform_benchmark_comparison(self) -> Dict[str, BenchmarkComparison]:
        """执行基准比较"""
        comparisons = {}
        
        # 行业基准数据（简化）
        benchmark_data = {
            'economic_performance': {'industry_avg': 7.0, 'best_practice': 9.0},
            'reliability_performance': {'industry_avg': 7.5, 'best_practice': 9.5},
            'environmental_performance': {'industry_avg': 6.5, 'best_practice': 9.0},
            'social_performance': {'industry_avg': 6.8, 'best_practice': 8.5},
            'risk_performance': {'industry_avg': 6.0, 'best_practice': 8.8}
        }
        
        # 项目评分
        project_scores = {
            'economic_performance': self._get_dimension_score(EvaluationType.ECONOMIC),
            'reliability_performance': self._get_dimension_score(EvaluationType.RELIABILITY),
            'environmental_performance': self._get_dimension_score(EvaluationType.ENVIRONMENTAL),
            'social_performance': self._get_dimension_score(EvaluationType.SOCIAL),
            'risk_performance': self._get_dimension_score(EvaluationType.RISK)
        }
        
        for metric_name, values in benchmark_data.items():
            if metric_name in project_scores:
                project_value = project_scores[metric_name]
                industry_avg = values['industry_avg']
                best_practice = values['best_practice']
                
                # 计算百分位排名（简化）
                percentile_rank = min(100, max(0, (project_value / 10) * 100))
                
                # 差距分析
                gap_analysis = {
                    'gap_to_industry': project_value - industry_avg,
                    'gap_to_best_practice': project_value - best_practice,
                    'improvement_potential': best_practice - project_value
                }
                
                comparisons[metric_name] = BenchmarkComparison(
                    metric_name=metric_name,
                    project_value=project_value,
                    industry_average=industry_avg,
                    best_in_class=best_practice,
                    percentile_rank=percentile_rank,
                    gap_analysis=gap_analysis
                )
        
        return comparisons
    
    def _conduct_trade_off_analysis(self) -> TradeOffAnalysis:
        """进行权衡分析"""
        # 定义维度对
        dimension_pairs = [
            (EvaluationDimension.ECONOMIC, EvaluationDimension.ENVIRONMENTAL),
            (EvaluationDimension.ECONOMIC, EvaluationDimension.SOCIAL),
            (EvaluationDimension.ECONOMIC, EvaluationDimension.RELIABILITY),
            (EvaluationDimension.ENVIRONMENTAL, EvaluationDimension.SOCIAL),
            (EvaluationDimension.RELIABILITY, EvaluationDimension.RISK)
        ]
        
        # 计算权衡比率
        trade_off_ratios = {}
        for dim1, dim2 in dimension_pairs:
            score1 = self._get_dimension_score(EvaluationType(dim1.value))
            score2 = self._get_dimension_score(EvaluationType(dim2.value))
            
            if score2 != 0:
                ratio = score1 / score2
                trade_off_ratios[(dim1, dim2)] = ratio
        
        # 敏感性分析
        sensitivity_analysis = {}
        for dimension in EvaluationDimension:
            # 简化的敏感性分析
            score = self._get_dimension_score(EvaluationType(dimension.value))
            sensitivity = score / 10.0
            sensitivity_analysis[dimension.value] = sensitivity
        
        # 关键阈值
        critical_thresholds = {
            'minimum_economic_score': 6.0,
            'minimum_reliability_score': 7.0,
            'minimum_environmental_score': 5.5,
            'minimum_social_score': 6.0,
            'minimum_risk_score': 5.0
        }
        
        return TradeOffAnalysis(
            dimension_pairs=dimension_pairs,
            trade_off_ratios=trade_off_ratios,
            sensitivity_analysis=sensitivity_analysis,
            critical_thresholds=critical_thresholds
        )
    
    def _generate_detailed_scores(self) -> Dict[str, CriterionScore]:
        """生成详细评分"""
        detailed_scores = {}
        
        # 经济性评分
        detailed_scores['economic_viability'] = CriterionScore(
            criterion_name="经济可行性",
            score=self._get_dimension_score(EvaluationType.ECONOMIC),
            weight=0.25,
            data_quality=0.8,
            uncertainty=0.2
        )
        
        # 可靠性评分
        detailed_scores['system_reliability'] = CriterionScore(
            criterion_name="系统可靠性",
            score=self._get_dimension_score(EvaluationType.RELIABILITY),
            weight=0.25,
            data_quality=0.9,
            uncertainty=0.15
        )
        
        # 环境性评分
        detailed_scores['environmental_impact'] = CriterionScore(
            criterion_name="环境影响",
            score=self._get_dimension_score(EvaluationType.ENVIRONMENTAL),
            weight=0.2,
            data_quality=0.7,
            uncertainty=0.3
        )
        
        # 社会性评分
        detailed_scores['social_acceptance'] = CriterionScore(
            criterion_name="社会接受度",
            score=self._get_dimension_score(EvaluationType.SOCIAL),
            weight=0.2,
            data_quality=0.6,
            uncertainty=0.4
        )
        
        # 风险性评分
        detailed_scores['risk_management'] = CriterionScore(
            criterion_name="风险管理",
            score=self._get_dimension_score(EvaluationType.RISK),
            weight=0.1,
            data_quality=0.8,
            uncertainty=0.25
        )
        
        return detailed_scores
    
    def _calculate_rankings(self) -> Dict[str, int]:
        """计算排名"""
        dimension_scores = {
            'economic': self._get_dimension_score(EvaluationType.ECONOMIC),
            'reliability': self._get_dimension_score(EvaluationType.RELIABILITY),
            'environmental': self._get_dimension_score(EvaluationType.ENVIRONMENTAL),
            'social': self._get_dimension_score(EvaluationType.SOCIAL),
            'risk': self._get_dimension_score(EvaluationType.RISK)
        }
        
        # 按分数排序（降序）
        sorted_dimensions = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)
        
        ranking = {}
        for rank, (dimension, score) in enumerate(sorted_dimensions, 1):
            ranking[dimension] = rank
        
        return ranking
    
    def _generate_overall_assessment(self, indicators: ComprehensiveIndicators) -> str:
        """生成总体评估"""
        score = indicators.overall_sustainability_score
        
        if score >= 8.5:
            return "项目在所有维度表现优异，具有很强的可持续性和竞争力，建议作为最佳实践案例推广。"
        elif score >= 7.0:
            return "项目整体表现良好，在多数维度表现优秀，具备较强的可持续发展潜力，建议持续优化。"
        elif score >= 5.5:
            return "项目表现中等，在某些维度存在改进空间，需要重点关注薄弱环节以提升整体表现。"
        elif score >= 4.0:
            return "项目表现需要改进，多个维度存在明显不足，建议制定全面的改进计划。"
        else:
            return "项目表现不佳，存在重大问题，需要重新评估项目可行性和实施策略。"
    
    def _identify_key_strengths(self) -> List[str]:
        """识别主要优势"""
        strengths = []
        
        # 基于各维度评分识别优势
        economic_score = self._get_dimension_score(EvaluationType.ECONOMIC)
        reliability_score = self._get_dimension_score(EvaluationType.RELIABILITY)
        environmental_score = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        social_score = self._get_dimension_score(EvaluationType.SOCIAL)
        risk_score = self._get_dimension_score(EvaluationType.RISK)
        
        if economic_score >= 8.0:
            strengths.append("经济表现优异，具有良好的成本效益比")
        
        if reliability_score >= 8.0:
            strengths.append("系统可靠性强，能够稳定运行并提供可靠服务")
        
        if environmental_score >= 8.0:
            strengths.append("环境表现突出，对环境影响较小，符合可持续发展要求")
        
        if social_score >= 8.0:
            strengths.append("社会效益显著，获得广泛社会支持和认可")
        
        if risk_score >= 8.0:
            strengths.append("风险控制能力强，具备良好的风险管理体系")
        
        # 默认优势
        if not strengths:
            strengths.append("项目具备基础的功能性和可行性")
            strengths.append("具备进一步优化和提升的潜力")
        
        return strengths
    
    def _identify_key_weaknesses(self) -> List[str]:
        """识别主要劣势"""
        weaknesses = []
        
        # 基于各维度评分识别劣势
        economic_score = self._get_dimension_score(EvaluationType.ECONOMIC)
        reliability_score = self._get_dimension_score(EvaluationType.RELIABILITY)
        environmental_score = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        social_score = self._get_dimension_score(EvaluationType.SOCIAL)
        risk_score = self._get_dimension_score(EvaluationType.RISK)
        
        if economic_score < 5.0:
            weaknesses.append("经济表现不佳，成本效益比需要改善")
        
        if reliability_score < 5.0:
            weaknesses.append("系统可靠性不足，影响运营稳定性")
        
        if environmental_score < 5.0:
            weaknesses.append("环境影响较大，需要加强环境保护措施")
        
        if social_score < 5.0:
            weaknesses.append("社会效益不足，需要改善公众接受度")
        
        if risk_score < 5.0:
            weaknesses.append("风险控制能力弱，存在较大的运营风险")
        
        # 通用劣势
        if not weaknesses:
            weaknesses.append("在某些维度有进一步提升的空间")
            weaknesses.append("需要持续优化和改进")
        
        return weaknesses
    
    def _identify_critical_issues(self) -> List[str]:
        """识别关键问题"""
        critical_issues = []
        
        # 检查是否存在低于关键阈值的问题
        economic_score = self._get_dimension_score(EvaluationType.ECONOMIC)
        reliability_score = self._get_dimension_score(EvaluationType.RELIABILITY)
        environmental_score = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        
        if economic_score < 4.0:
            critical_issues.append("经济可行性存在严重问题，可能影响项目成功")
        
        if reliability_score < 4.0:
            critical_issues.append("系统可靠性存在严重问题，影响基本功能")
        
        if environmental_score < 3.0:
            critical_issues.append("环境影响严重，可能面临法规限制")
        
        return critical_issues
    
    def _suggest_immediate_actions(self) -> List[str]:
        """建议即时行动"""
        immediate_actions = []
        
        # 基于最弱维度提出建议
        dimension_scores = {
            'economic': self._get_dimension_score(EvaluationType.ECONOMIC),
            'reliability': self._get_dimension_score(EvaluationType.RELIABILITY),
            'environmental': self._get_dimension_score(EvaluationType.ENVIRONMENTAL),
            'social': self._get_dimension_score(EvaluationType.SOCIAL),
            'risk': self._get_dimension_score(EvaluationType.RISK)
        }
        
        weakest_dimension = min(dimension_scores, key=dimension_scores.get)
        weakest_score = dimension_scores[weakest_dimension]
        
        if weakest_score < 5.0:
            if weakest_dimension == 'economic':
                immediate_actions.append("立即优化成本结构和收入模式")
                immediate_actions.append("重新评估项目的经济效益")
            elif weakest_dimension == 'reliability':
                immediate_actions.append("加强系统维护和监控")
                immediate_actions.append("建立备件库存和应急预案")
            elif weakest_dimension == 'environmental':
                immediate_actions.append("制定环境保护改进计划")
                immediate_actions.append("加强环境监测和报告")
            elif weakest_dimension == 'social':
                immediate_actions.append("开展利益相关者沟通活动")
                immediate_actions.append("改善项目社会形象")
            elif weakest_dimension == 'risk':
                immediate_actions.append("完善风险管理制度")
                immediate_actions.append("加强风险监控和预警")
        
        # 通用即时行动
        immediate_actions.extend([
            "建立综合评估监控体系",
            "制定关键绩效指标追踪机制",
            "建立定期评估和报告制度"
        ])
        
        return immediate_actions
    
    def _suggest_strategic_recommendations(self) -> List[str]:
        """建议战略建议"""
        recommendations = [
            "建立全面的可持续发展战略",
            "制定长期竞争力提升计划",
            "加强利益相关者参与和治理",
            "投资于技术创新和数字化转型",
            "建立供应链可持续发展体系",
            "制定气候变化应对策略",
            "建立持续改进和创新的文化",
            "加强人才培养和能力建设"
        ]
        
        return recommendations
    
    def _prioritize_improvements(self) -> List[str]:
        """优先化改进"""
        improvements = []
        
        # 基于维度权重和当前表现排序改进优先级
        dimension_scores = {
            'economic': self._get_dimension_score(EvaluationType.ECONOMIC),
            'reliability': self._get_dimension_score(EvaluationType.RELIABILITY),
            'environmental': self._get_dimension_score(EvaluationType.ENVIRONMENTAL),
            'social': self._get_dimension_score(EvaluationType.SOCIAL),
            'risk': self._get_dimension_score(EvaluationType.RISK)
        }
        
        dimension_weights = {
            'economic': self.dimension_weights[EvaluationDimension.ECONOMIC].weight,
            'reliability': self.dimension_weights[EvaluationDimension.RELIABILITY].weight,
            'environmental': self.dimension_weights[EvaluationDimension.ENVIRONMENTAL].weight,
            'social': self.dimension_weights[EvaluationDimension.SOCIAL].weight,
            'risk': self.dimension_weights[EvaluationDimension.RISK].weight
        }
        
        # 计算改进潜力（权重×(满分-当前分数)）
        improvement_potential = {}
        for dimension in dimension_scores:
            potential = dimension_weights[dimension] * (10 - dimension_scores[dimension])
            improvement_potential[dimension] = potential
        
        # 按改进潜力排序
        sorted_improvements = sorted(improvement_potential.items(), key=lambda x: x[1], reverse=True)
        
        for dimension, potential in sorted_improvements:
            if potential > 0.5:  # 只包括有意义的改进
                if dimension == 'economic':
                    improvements.append("提高经济效益 - 高优先级")
                elif dimension == 'reliability':
                    improvements.append("增强系统可靠性 - 高优先级")
                elif dimension == 'environmental':
                    improvements.append("改善环境表现 - 中优先级")
                elif dimension == 'social':
                    improvements.append("提升社会效益 - 中优先级")
                elif dimension == 'risk':
                    improvements.append("加强风险管理 - 中优先级")
        
        return improvements
    
    def _generate_future_outlook(self) -> str:
        """生成未来展望"""
        score = self._calculate_comprehensive_indicators().overall_sustainability_score
        
        if score >= 8.0:
            return "项目具备良好的发展前景，建议继续投资和优化，预期将成为行业标杆。"
        elif score >= 6.5:
            return "项目有良好的发展潜力，通过持续改进可以取得更好的表现，建议制定发展路线图。"
        elif score >= 5.0:
            return "项目前景一般，需要重点改进薄弱环节，建议制定针对性改进计划。"
        else:
            return "项目前景需要密切关注和重大改进，建议重新评估项目策略和实施计划。"
    
    def _suggest_monitoring_recommendations(self) -> List[str]:
        """建议监控"""
        recommendations = [
            "建立综合绩效仪表板",
            "设置关键预警指标",
            "实施定期评估机制",
            "建立利益相关者反馈系统",
            "监控行业基准变化",
            "跟踪技术创新趋势",
            "评估政策环境影响",
            "建立风险预警系统"
        ]
        
        return recommendations

class SustainabilityIndexCalculator(ComprehensiveEvaluator):
    """可持续性指数计算器"""
    
    def calculate_comprehensive_sustainability_index(self) -> Dict[str, float]:
        """计算综合可持续性指数"""
        indicators = self._calculate_comprehensive_indicators()
        
        sustainability_index = {
            'economic_dimension': indicators.sustainability_index['economic_sustainability'],
            'environmental_dimension': indicators.sustainability_index['environmental_sustainability'],
            'social_dimension': indicators.sustainability_index['social_sustainability'],
            'institutional_dimension': indicators.sustainability_index['institutional_sustainability'],
            'overall_sustainability': indicators.overall_sustainability_score / 10
        }
        
        return sustainability_index
    
    def calculate_advanced_sustainability_metrics(self) -> Dict[str, float]:
        """计算高级可持续性指标"""
        economic_score = self._get_dimension_score(EvaluationType.ECONOMIC)
        environmental_score = self._get_dimension_score(EvaluationType.ENVIRONMENTAL)
        social_score = self._get_dimension_score(EvaluationType.SOCIAL)
        
        advanced_metrics = {
            'circular_economy_index': (economic_score * 0.4 + environmental_score * 0.6) / 10,
            'social_inclusion_index': social_score / 10,
            'climate_resilience_index': (environmental_score * 0.6 + self._get_dimension_score(EvaluationType.RELIABILITY) * 0.4) / 10,
            'innovation_readiness_index': (economic_score * 0.5 + social_score * 0.5) / 10,
            'governance_effectiveness_index': (self._get_dimension_score(EvaluationType.SOCIAL) * 0.6 + self._get_dimension_score(EvaluationType.RISK) * 0.4) / 10
        }
        
        return advanced_metrics

class ComparativeAnalyzer(ComprehensiveEvaluator):
    """比较分析器"""
    
    def compare_with_benchmarks(self, benchmarks: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """与基准比较"""
        comparisons = {}
        
        project_scores = {
            'economic': self._get_dimension_score(EvaluationType.ECONOMIC),
            'reliability': self._get_dimension_score(EvaluationType.RELIABILITY),
            'environmental': self._get_dimension_score(EvaluationType.ENVIRONMENTAL),
            'social': self._get_dimension_score(EvaluationType.SOCIAL),
            'risk': self._get_dimension_score(EvaluationType.RISK)
        }
        
        for metric, project_value in project_scores.items():
            if metric in benchmarks:
                benchmark_value = benchmarks[metric]
                comparison = {
                    'project_value': project_value,
                    'benchmark_value': benchmark_value,
                    'difference': project_value - benchmark_value,
                    'relative_performance': project_value / benchmark_value if benchmark_value != 0 else 0
                }
                comparisons[metric] = comparison
        
        return comparisons
    
    def analyze_scenario_comparison(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析情景比较"""
        scenario_analysis = {}
        
        for i, scenario in enumerate(scenarios):
            scenario_name = scenario.get('name', f'Scenario_{i+1}')
            
            # 提取情景数据并计算评分
            temp_evaluator = ComprehensiveEvaluator()
            temp_evaluator.evaluation_results = scenario.get('evaluation_results', {})
            
            indicators = temp_evaluator._calculate_comprehensive_indicators()
            scenario_analysis[scenario_name] = {
                'overall_score': indicators.overall_sustainability_score,
                'performance_ranking': temp_evaluator._calculate_rankings(),
                'key_advantages': temp_evaluator._identify_key_strengths(),
                'main_concerns': temp_evaluator._identify_key_weaknesses()
            }
        
        # 生成比较结果
        sorted_scenarios = sorted(scenario_analysis.items(), 
                                key=lambda x: x[1]['overall_score'], reverse=True)
        
        return {
            'scenario_rankings': sorted_scenarios,
            'best_scenario': sorted_scenarios[0][0] if sorted_scenarios else None,
            'performance_gaps': self._calculate_performance_gaps(scenario_analysis)
        }
    
    def _calculate_performance_gaps(self, scenarios: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """计算绩效差距"""
        if not scenarios:
            return {}
        
        # 获取最佳情景作为基准
        best_scenario = max(scenarios.items(), key=lambda x: x[1]['overall_score'])
        best_scores = best_scenario[1]
        
        gaps = {}
        for scenario_name, scenario_data in scenarios.items():
            if scenario_name != best_scenario[0]:
                gap = best_scores['overall_score'] - scenario_data['overall_score']
                gaps[scenario_name] = gap
        
        return gaps