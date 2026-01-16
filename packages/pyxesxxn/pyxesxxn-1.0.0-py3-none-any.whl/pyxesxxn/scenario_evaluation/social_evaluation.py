"""
社会评估模块

提供能源系统的社会影响评估功能，包括：
- 社会接受度：公众对能源项目的接受程度
- 就业影响：创造就业机会、就业质量分析
- 能源可及性：能源服务获取性、可负担性
- 社会公平：能源分配公平性、弱势群体影响
- 文化影响：文化遗产保护、社区影响
- 社会治理：公众参与、社会责任
- 健康影响：空气质量、噪音污染、健康效益
- 社会经济效益：收入分配、经济包容性
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

from .evaluation_framework import Evaluator, EvaluationContext, EvaluationResult, EvaluationStatus, EvaluationType

class SocialIndicator(Enum):
    """社会指标"""
    EMPLOYMENT_CREATION = "employment_creation"          # 就业创造
    ENERGY_ACCESS = "energy_access"                     # 能源可及性
    ENERGY_AFFORDABILITY = "energy_affordability"       # 能源可负担性
    SOCIAL_ACCEPTANCE = "social_acceptance"             # 社会接受度
    COMMUNITY_IMPACT = "community_impact"              # 社区影响
    HEALTH_BENEFITS = "health_benefits"               # 健康效益
    SOCIAL_INCLUSION = "social_inclusion"              # 社会包容
    PUBLIC_PARTICIPATION = "public_participation"      # 公众参与

class StakeholderGroup(Enum):
    """利益相关者群体"""
    LOCAL_COMMUNITY = "local_community"                # 当地社区
    GOVERNMENT = "government"                          # 政府
    INDUSTRY = "industry"                              # 产业
    ENVIRONMENTAL_GROUPS = "environmental_groups"      # 环保组织
    ACADEMIC_INSTITUTIONS = "academic_institutions"    # 学术机构
    GENERAL_PUBLIC = "general_public"                  # 公众
    INDIGENOUS_PEOPLES = "indigenous_peoples"          # 原住民

class ImpactCategory(Enum):
    """影响类别"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class StakeholderInput:
    """利益相关者输入数据"""
    stakeholder_group: StakeholderGroup
    stakeholder_id: str
    satisfaction_score: float                # 满意度评分 (0-10)
    concern_level: float                     # 关注度 (0-10)
    acceptance_level: float                  # 接受度 (0-10)
    impact_perception: Dict[str, float]      # 对各项影响的感知
    suggestions: List[str]                   # 建议意见
    
@dataclass
class SocialImpactData:
    """社会影响数据"""
    component_id: str
    region: str
    
    # 就业影响
    direct_jobs_created: int = 0             # 直接就业
    indirect_jobs_created: int = 0           # 间接就业
    induced_jobs_created: int = 0            # 诱发就业
    job_quality_score: float = 0             # 就业质量评分
    local_employment_rate: float = 0         # 当地就业率
    
    # 能源可及性
    population_served: int = 0               # 服务人口
    electrification_rate_increase: float = 0 # 电气化率提升
    rural_access_improvement: float = 0     # 农村可及性改善
    
    # 经济影响
    local_procurement_rate: float = 0        # 当地采购率
    local_tax_contribution: float = 0        # 当地税收贡献
    community_investment: float = 0          # 社区投资
    energy_cost_reduction: float = 0         # 能源成本降低
    
    # 健康影响
    air_quality_improvement: float = 0       # 空气质量改善
    noise_reduction: float = 0               # 噪音减少
    health_benefits_value: float = 0         # 健康效益价值
    
    # 社会接受度
    public_support_score: float = 0          # 公众支持评分
    media_sentiment: float = 0               # 媒体情绪
    protest_risk: float = 0                  # 抗议风险
    
@dataclass
class EmploymentAnalysis:
    """就业分析"""
    total_jobs_created: int                  # 总就业创造
    permanent_jobs: int                     # 永久就业
    temporary_jobs: int                     # 临时就业
    construction_jobs: int                  # 建设期就业
    operations_jobs: int                    # 运营期就业
    
    # 就业质量
    average_wage_level: float               # 平均工资水平
    skill_level_distribution: Dict[str, int] # 技能水平分布
    gender_distribution: Dict[str, int]     # 性别分布
    age_distribution: Dict[str, int]        # 年龄分布
    
    # 当地化分析
    local_employment_percentage: float      # 当地就业比例
    skills_gap_analysis: Dict[str, float]   # 技能缺口分析
    training_requirements: Dict[str, int]   # 培训需求

@dataclass
class EnergyAccessibility:
    """能源可及性"""
    # 基础能源服务
    population_with_electricity: int        # 有电力的人口
    population_with_clean_cooking: int      # 有清洁烹饪的人口
    reliability_hours_per_year: float       # 年可靠性小时数
    
    # 可负担性
    energy_expenditure_ratio: float         # 能源支出比例
    subsidy_eligible_population: int        # 可享受补贴的人口
    lifeline_pricing_available: bool        # 是否有生活电价
    
    # 能源贫困
    energy_poverty_rate: float              # 能源贫困率
    energy_burden_households: int           # 能源负担过重家庭
    
    # 地理分布
    urban_access_rate: float                # 城市可及率
    rural_access_rate: float                # 农村可及率
    remote_area_service: float              # 偏远地区服务

@dataclass
class SocialCohesionMetrics:
    """社会凝聚力指标"""
    community_satisfaction: float           # 社区满意度
    social_capital_index: float            # 社会资本指数
    conflict_incidents: int                # 冲突事件数
    collaboration_projects: int            # 合作项目数
    
    # 文化影响
    cultural_heritage_impact: float         # 文化遗产影响
    traditional_knowledge_preservation: float  # 传统知识保护
    community_cohesion_change: float        # 社区凝聚力变化
    
    # 社会包容
    marginalized_groups_inclusion: float    # 边缘群体包容性
    gender_equity_index: float             # 性别平等指数
    intergenerational_equity: float        # 代际公平

@dataclass
class SocialResult:
    """社会评估结果"""
    # 总体指标
    overall_social_score: float             # 总体社会评分
    social_sustainability_index: float      # 社会可持续性指数
    
    # 详细分析
    employment_analysis: EmploymentAnalysis
    energy_accessibility: EnergyAccessibility
    social_cohesion: SocialCohesionMetrics
    
    # 利益相关者分析
    stakeholder_feedback: Dict[StakeholderGroup, float]
    public_acceptance_index: float          # 公众接受度指数
    social_risk_level: float               # 社会风险等级
    
    # 影响评估
    positive_impacts: List[str]
    negative_impacts: List[str]
    mitigation_measures: List[str]
    
    # 建议和对策
    policy_recommendations: List[str]
    engagement_strategies: List[str]
    monitoring_indicators: List[str]

class SocialEvaluator(Evaluator):
    """社会评估器"""
    
    def __init__(self, assessment_period: int = 365):
        super().__init__("SocialEvaluator", EvaluationType.SOCIAL)
        self.assessment_period = assessment_period
        self.social_data: Dict[str, SocialImpactData] = {}
        self.stakeholder_inputs: List[StakeholderInput] = []
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行社会评估"""
        start_time = datetime.now()
        self.logger.info("开始社会评估")
        
        try:
            # 从场景数据中提取社会信息
            scenario_data = context.scenario_data
            self._extract_social_data(scenario_data)
            
            # 分析就业影响
            employment_analysis = self._analyze_employment_impact()
            
            # 评估能源可及性
            energy_accessibility = self._assess_energy_accessibility()
            
            # 分析社会凝聚力
            social_cohesion = self._analyze_social_cohesion()
            
            # 利益相关者分析
            stakeholder_analysis = self._analyze_stakeholder_feedback()
            
            # 创建结果
            result = SocialResult(
                overall_social_score=self._calculate_overall_score(),
                social_sustainability_index=self._calculate_sustainability_index(),
                employment_analysis=employment_analysis,
                energy_accessibility=energy_accessibility,
                social_cohesion=social_cohesion,
                stakeholder_feedback=stakeholder_analysis,
                public_acceptance_index=self._calculate_public_acceptance(),
                social_risk_level=self._assess_social_risk(),
                positive_impacts=self._identify_positive_impacts(),
                negative_impacts=self._identify_negative_impacts(),
                mitigation_measures=self._suggest_mitigation_measures(),
                policy_recommendations=self._generate_policy_recommendations(),
                engagement_strategies=self._suggest_engagement_strategies(),
                monitoring_indicators=self._define_monitoring_indicators()
            )
            
            # 创建标准评估结果
            metrics = {
                'overall_social_score': result.overall_social_score,
                'employment_created': result.employment_analysis.total_jobs_created,
                'energy_access_improvement': energy_accessibility.urban_access_rate,
                'social_acceptance_index': result.public_acceptance_index,
                'community_satisfaction': result.social_cohesion.community_satisfaction
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={'social_result': result},
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("社会评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"社会评估失败: {str(e)}")
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
        required_fields = ['demographic_data', 'employment_data', 'energy_access_data']
        for field in required_fields:
            if field not in context.metadata:
                self.logger.warning(f"缺少必需字段: {field}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['demographic_data', 'employment_data', 'energy_access_data', 'stakeholder_feedback']
    
    def add_social_data(self, social_data: SocialImpactData):
        """添加社会数据"""
        self.social_data[social_data.component_id] = social_data
    
    def add_stakeholder_input(self, input_data: StakeholderInput):
        """添加利益相关者输入"""
        self.stakeholder_inputs.append(input_data)
    
    def _extract_social_data(self, scenario_data: Dict[str, Any]):
        """从场景数据中提取社会信息"""
        # 这里应该从场景数据中解析社会影响相关数据
        # 简化实现
        if 'social_impact_data' in scenario_data:
            social_data = scenario_data['social_impact_data']
            for comp_id, data in social_data.items():
                if comp_id not in self.social_data:
                    social_impact = SocialImpactData(
                        component_id=comp_id,
                        region=data.get('region', 'unknown'),
                        direct_jobs_created=data.get('direct_jobs', 0),
                        population_served=data.get('population_served', 0),
                        public_support_score=data.get('public_support', 5.0)
                    )
                    self.social_data[comp_id] = social_impact
    
    def _analyze_employment_impact(self) -> EmploymentAnalysis:
        """分析就业影响"""
        total_direct = sum(data.direct_jobs_created for data in self.social_data.values())
        total_indirect = sum(data.indirect_jobs_created for data in self.social_data.values())
        total_induced = sum(data.induced_jobs_created for data in self.social_data.values())
        
        # 简化分配：建设期60%，运营期40%
        construction_jobs = int((total_direct + total_indirect + total_induced) * 0.6)
        operations_jobs = int((total_direct + total_indirect + total_induced) * 0.4)
        
        # 永久/临时就业分配（假设70%永久，30%临时）
        permanent_jobs = int((total_direct + total_indirect + total_induced) * 0.7)
        temporary_jobs = int((total_direct + total_indirect + total_induced) * 0.3)
        
        # 当地就业分析
        local_rates = [data.local_employment_rate for data in self.social_data.values()]
        avg_local_rate = np.mean(local_rates) if local_rates else 0
        
        return EmploymentAnalysis(
            total_jobs_created=total_direct + total_indirect + total_induced,
            permanent_jobs=permanent_jobs,
            temporary_jobs=temporary_jobs,
            construction_jobs=construction_jobs,
            operations_jobs=operations_jobs,
            average_wage_level=35000,  # 假设值
            skill_level_distribution={
                'high_skill': int((total_direct + total_indirect + total_induced) * 0.3),
                'medium_skill': int((total_direct + total_indirect + total_induced) * 0.5),
                'low_skill': int((total_direct + total_indirect + total_induced) * 0.2)
            },
            gender_distribution={
                'male': int((total_direct + total_indirect + total_induced) * 0.6),
                'female': int((total_direct + total_indirect + total_induced) * 0.4)
            },
            age_distribution={
                '18-30': int((total_direct + total_indirect + total_induced) * 0.3),
                '31-45': int((total_direct + total_indirect + total_induced) * 0.4),
                '46-60': int((total_direct + total_indirect + total_induced) * 0.3)
            },
            local_employment_percentage=avg_local_rate * 100,
            skills_gap_analysis={'high_skill': 0.2, 'medium_skill': 0.15, 'low_skill': 0.1},
            training_requirements={'high_skill': 50, 'medium_skill': 80, 'low_skill': 30}
        )
    
    def _assess_energy_accessibility(self) -> EnergyAccessibility:
        """评估能源可及性"""
        total_population_served = sum(data.population_served for data in self.social_data.values())
        
        # 简化的能源可及性分析
        electrification_improvements = [data.electrification_rate_increase for data in self.social_data.values()]
        avg_electrification_improvement = np.mean(electrification_improvements) if electrification_improvements else 0
        
        rural_improvements = [data.rural_access_improvement for data in self.social_data.values()]
        avg_rural_improvement = np.mean(rural_improvements) if rural_improvements else 0
        
        return EnergyAccessibility(
            population_with_electricity=total_population_served,
            population_with_clean_cooking=int(total_population_served * 0.7),  # 假设70%有清洁烹饪
            reliability_hours_per_year=8000,  # 假设值
            energy_expenditure_ratio=0.05,    # 假设5%收入用于能源
            subsidy_eligible_population=int(total_population_served * 0.3),  # 假设30%可享受补贴
            lifeline_pricing_available=True,
            energy_poverty_rate=0.15,         # 假设15%能源贫困率
            energy_burden_households=int(total_population_served * 0.05 / 4),  # 假设4人/户
            urban_access_rate=0.95 + avg_electrification_improvement,
            rural_access_rate=0.6 + avg_rural_improvement,
            remote_area_service=0.4
        )
    
    def _analyze_social_cohesion(self) -> SocialCohesionMetrics:
        """分析社会凝聚力"""
        satisfaction_scores = [data.public_support_score for data in self.social_data.values()]
        avg_satisfaction = np.mean(satisfaction_scores) if satisfaction_scores else 5.0
        
        # 媒体情绪分析（简化）
        media_sentiments = [data.media_sentiment for data in self.social_data.values() if hasattr(data, 'media_sentiment')]
        avg_media_sentiment = np.mean(media_sentiments) if media_sentiments else 0
        
        return SocialCohesionMetrics(
            community_satisfaction=avg_satisfaction,
            social_capital_index=avg_satisfaction / 10.0,  # 简化为满意度/10
            conflict_incidents=int((10 - avg_satisfaction) * 0.5),  # 简化为反比关系
            collaboration_projects=max(1, int(avg_satisfaction * 0.3)),
            cultural_heritage_impact=0.1,  # 假设较小影响
            traditional_knowledge_preservation=0.8,  # 假设较好保护
            community_cohesion_change=avg_satisfaction - 5.0,  # 相对于中性状态的变化
            marginalized_groups_inclusion=0.7,  # 假设70%包容性
            gender_equity_index=0.8,           # 假设80%性别平等
            intergenerational_equity=0.75      # 假设75%代际公平
        )
    
    def _analyze_stakeholder_feedback(self) -> Dict[StakeholderGroup, float]:
        """分析利益相关者反馈"""
        if not self.stakeholder_inputs:
            # 如果没有利益相关者输入数据，基于社会数据生成模拟数据
            return self._generate_simulated_stakeholder_feedback()
        
        feedback_by_group = {}
        
        for group in StakeholderGroup:
            group_inputs = [input_data for input_data in self.stakeholder_inputs 
                          if input_data.stakeholder_group == group]
            
            if group_inputs:
                avg_acceptance = np.mean([input_data.acceptance_level for input_data in group_inputs])
                feedback_by_group[group] = avg_acceptance
            else:
                feedback_by_group[group] = 5.0  # 默认中性值
        
        return feedback_by_group
    
    def _generate_simulated_stakeholder_feedback(self) -> Dict[StakeholderGroup, float]:
        """生成模拟利益相关者反馈"""
        return {
            StakeholderGroup.LOCAL_COMMUNITY: 7.5,
            StakeholderGroup.GOVERNMENT: 8.0,
            StakeholderGroup.INDUSTRY: 8.5,
            StakeholderGroup.ENVIRONMENTAL_GROUPS: 6.0,
            StakeholderGroup.ACADEMIC_INSTITUTIONS: 7.8,
            StakeholderGroup.GENERAL_PUBLIC: 7.2,
            StakeholderGroup.INDIGENOUS_PEOPLES: 6.5
        }
    
    def _calculate_overall_score(self) -> float:
        """计算总体社会评分"""
        # 基础评分
        base_score = 5.0
        
        # 就业影响加分
        employment_bonus = sum(data.job_quality_score for data in self.social_data.values()) / len(self.social_data) if self.social_data else 0
        
        # 公众支持加分
        support_bonus = np.mean([data.public_support_score for data in self.social_data.values()]) if self.social_data else 5.0
        
        # 计算综合评分
        overall_score = (base_score + employment_bonus + support_bonus) / 3
        return min(10.0, max(0.0, overall_score))
    
    def _calculate_sustainability_index(self) -> float:
        """计算社会可持续性指数"""
        # 基于多个指标计算可持续性指数
        social_score = self._calculate_overall_score()
        
        # 就业可持续性
        employment_sustainability = min(1.0, self._analyze_employment_impact().total_jobs_created / 1000)
        
        # 能源可及性可持续性
        energy_sustainability = min(1.0, self._assess_energy_accessibility().urban_access_rate)
        
        # 社会凝聚力可持续性
        cohesion_sustainability = self._analyze_social_cohesion().social_capital_index
        
        # 综合可持续性指数
        sustainability_index = (social_score / 10.0 + employment_sustainability + 
                               energy_sustainability + cohesion_sustainability) / 4
        
        return sustainability_index
    
    def _calculate_public_acceptance(self) -> float:
        """计算公众接受度"""
        # 基于利益相关者反馈和公众支持度计算
        if self.stakeholder_inputs:
            general_public_feedback = [input_data.acceptance_level for input_data in self.stakeholder_inputs 
                                     if input_data.stakeholder_group == StakeholderGroup.GENERAL_PUBLIC]
            if general_public_feedback:
                return np.mean(general_public_feedback)
        
        # 如果没有利益相关者数据，使用社会数据中的支持度
        support_scores = [data.public_support_score for data in self.social_data.values()]
        return np.mean(support_scores) if support_scores else 7.0
    
    def _assess_social_risk(self) -> float:
        """评估社会风险等级"""
        # 基于多个风险因子计算社会风险
        risk_factors = []
        
        # 公众支持度风险
        public_support = self._calculate_public_acceptance()
        support_risk = max(0, (10 - public_support) / 10)
        risk_factors.append(support_risk)
        
        # 抗议风险
        protest_risks = [data.protest_risk for data in self.social_data.values()]
        avg_protest_risk = np.mean(protest_risks) if protest_risks else 0.1
        risk_factors.append(avg_protest_risk)
        
        # 冲突事件风险
        cohesion = self._analyze_social_cohesion()
        conflict_risk = max(0, (10 - cohesion.community_satisfaction) / 10)
        risk_factors.append(conflict_risk)
        
        # 综合风险等级
        social_risk = np.mean(risk_factors)
        return min(1.0, max(0.0, social_risk))
    
    def _identify_positive_impacts(self) -> List[str]:
        """识别正面影响"""
        positive_impacts = []
        
        # 基于就业分析的影响
        employment = self._analyze_employment_impact()
        if employment.total_jobs_created > 0:
            positive_impacts.append(f"创造就业机会: {employment.total_jobs_created}个就业岗位")
        
        # 基于能源可及性的影响
        accessibility = self._assess_energy_accessibility()
        if accessibility.population_with_electricity > 0:
            positive_impacts.append(f"改善能源可及性: 服务人口 {accessibility.population_with_electricity:,}")
        
        # 基于社会凝聚力的影响
        cohesion = self._analyze_social_cohesion()
        if cohesion.community_satisfaction > 6:
            positive_impacts.append(f"提升社区满意度: {cohesion.community_satisfaction:.1f}/10")
        
        # 经济效益
        total_investment = sum(data.community_investment for data in self.social_data.values())
        if total_investment > 0:
            positive_impacts.append(f"促进社区投资: {total_investment:,.0f}元")
        
        # 健康效益
        health_benefits = sum(data.health_benefits_value for data in self.social_data.values())
        if health_benefits > 0:
            positive_impacts.append(f"产生健康效益: {health_benefits:,.0f}元")
        
        return positive_impacts
    
    def _identify_negative_impacts(self) -> List[str]:
        """识别负面影响"""
        negative_impacts = []
        
        # 社会风险
        social_risk = self._assess_social_risk()
        if social_risk > 0.5:
            negative_impacts.append(f"存在较高社会风险: {social_risk:.1f}/1.0")
        
        # 社区满意度不足
        cohesion = self._analyze_social_cohesion()
        if cohesion.community_satisfaction < 5:
            negative_impacts.append(f"社区满意度偏低: {cohesion.community_satisfaction:.1f}/10")
        
        # 技能缺口
        employment = self._analyze_employment_impact()
        if employment.skills_gap_analysis.get('high_skill', 0) > 0.3:
            negative_impacts.append("存在技术技能缺口，需要加强培训")
        
        # 能源贫困问题
        accessibility = self._assess_energy_accessibility()
        if accessibility.energy_poverty_rate > 0.2:
            negative_impacts.append(f"能源贫困率较高: {accessibility.energy_poverty_rate:.1%}")
        
        return negative_impacts
    
    def _suggest_mitigation_measures(self) -> List[str]:
        """建议缓解措施"""
        measures = []
        
        social_risk = self._assess_social_risk()
        if social_risk > 0.3:
            measures.append("建立社区参与机制，定期召开利益相关者会议")
            measures.append("设立社会影响监测系统，及时发现和解决社会问题")
        
        employment = self._analyze_employment_impact()
        if employment.local_employment_percentage < 80:
            measures.append("增加当地就业培训和技能提升项目")
            measures.append("优先雇用当地劳动力")
        
        accessibility = self._assess_energy_accessibility()
        if accessibility.rural_access_rate < 0.8:
            measures.append("加强农村电网建设和改造")
            measures.append("提供能源补贴和优惠电价政策")
        
        cohesion = self._analyze_social_cohesion()
        if cohesion.conflict_incidents > 0:
            measures.append("建立冲突预防和解决机制")
            measures.append("加强与社区的沟通协调")
        
        measures.append("建立社会责任报告制度")
        measures.append("定期开展社会影响评估")
        
        return measures
    
    def _generate_policy_recommendations(self) -> List[str]:
        """生成政策建议"""
        recommendations = []
        
        # 就业政策建议
        employment = self._analyze_employment_impact()
        if employment.total_jobs_created > 0:
            recommendations.append("制定促进当地就业的激励政策")
            recommendations.append("建立技能培训和认证体系")
        
        # 能源可及性政策建议
        accessibility = self._assess_energy_accessibility()
        if accessibility.energy_poverty_rate > 0.1:
            recommendations.append("实施能源贫困缓解政策")
            recommendations.append("建立城乡能源服务均等化机制")
        
        # 社会包容政策建议
        cohesion = self._analyze_social_cohesion()
        if cohesion.marginalized_groups_inclusion < 0.8:
            recommendations.append("加强社会包容性政策制定")
            recommendations.append("保护弱势群体权益")
        
        # 参与式治理建议
        recommendations.append("建立公众参与能源决策的制度机制")
        recommendations.append("完善能源项目社会影响评估制度")
        
        return recommendations
    
    def _suggest_engagement_strategies(self) -> List[str]:
        """建议参与策略"""
        strategies = []
        
        # 利益相关者参与
        stakeholder_feedback = self._analyze_stakeholder_feedback()
        
        if any(score < 6 for score in stakeholder_feedback.values()):
            strategies.append("针对低支持度群体开展专项沟通活动")
            strategies.append("组织现场参观和体验活动")
        
        # 社区参与
        cohesion = self._analyze_social_cohesion()
        if cohesion.community_satisfaction < 7:
            strategies.append("建立社区咨询委员会")
            strategies.append("定期举办社区开放日活动")
        
        # 信息透明
        strategies.append("建立项目信息公开平台")
        strategies.append("制作通俗易懂的项目宣传材料")
        
        # 能力建设
        strategies.append("开展能源素养教育活动")
        strategies.append("支持当地社区组织能力建设")
        
        return strategies
    
    def _define_monitoring_indicators(self) -> List[str]:
        """定义监测指标"""
        indicators = [
            # 就业监测
            "当地就业率",
            "就业质量指数",
            "技能培训参与率",
            
            # 能源可及性监测
            "电气化率",
            "能源可负担性指数",
            "能源服务质量满意度",
            
            # 社会接受度监测
            "公众支持度调查结果",
            "媒体报道情绪分析",
            "投诉和建议处理率",
            
            # 社会凝聚力监测
            "社区满意度调查",
            "冲突事件发生率",
            "社区合作项目数量",
            
            # 可持续性监测
            "社会可持续发展指标",
            "代际公平评估",
            "社会包容性指数"
        ]
        
        return indicators

class EmploymentImpactAnalyzer(SocialEvaluator):
    """就业影响分析器"""
    
    def analyze_employment_multipliers(self) -> Dict[str, float]:
        """分析就业乘数效应"""
        total_direct_jobs = sum(data.direct_jobs_created for data in self.social_data.values())
        total_indirect_jobs = sum(data.indirect_jobs_created for data in self.social_data.values())
        total_induced_jobs = sum(data.induced_jobs_created for data in self.social_data.values())
        
        # 计算就业乘数
        if total_direct_jobs > 0:
            indirect_multiplier = total_indirect_jobs / total_direct_jobs
            induced_multiplier = total_induced_jobs / total_direct_jobs
            total_multiplier = (total_direct_jobs + total_indirect_jobs + total_induced_jobs) / total_direct_jobs
        else:
            indirect_multiplier = induced_multiplier = total_multiplier = 0
        
        return {
            'direct_employment': total_direct_jobs,
            'indirect_employment': total_indirect_jobs,
            'induced_employment': total_induced_jobs,
            'indirect_multiplier': indirect_multiplier,
            'induced_multiplier': induced_multiplier,
            'total_multiplier': total_multiplier
        }
    
    def analyze_employment_quality(self) -> Dict[str, Any]:
        """分析就业质量"""
        employment = self._analyze_employment_impact()
        
        # 就业质量指标
        quality_metrics = {
            'permanent_employment_rate': employment.permanent_jobs / max(1, employment.total_jobs_created),
            'average_wage_comparison': employment.average_wage_level / 30000,  # 相对于基准工资
            'skills_mismatch_rate': 0.15,  # 假设15%技能不匹配
            'training_provision_rate': 0.8,  # 假设80%提供培训
            'working_conditions_score': 7.5  # 假设工作条件评分
        }
        
        return quality_metrics

class SocialAcceptanceAnalyzer(SocialEvaluator):
    """社会接受度分析器"""
    
    def analyze_acceptance_factors(self) -> Dict[str, float]:
        """分析接受度影响因素"""
        factors = {}
        
        # 基于利益相关者反馈分析
        if self.stakeholder_inputs:
            # 经济因素
            economic_acceptance = np.mean([input_data.satisfaction_score for input_data in self.stakeholder_inputs])
            factors['economic_benefit_acceptance'] = economic_acceptance / 10.0
            
            # 环境因素
            environmental_acceptance = economic_acceptance * 0.9  # 简化处理
            factors['environmental_acceptance'] = environmental_acceptance / 10.0
            
            # 社会因素
            social_acceptance = economic_acceptance * 0.95
            factors['social_cohesion_acceptance'] = social_acceptance / 10.0
        else:
            # 使用社会数据作为替代
            base_acceptance = np.mean([data.public_support_score for data in self.social_data.values()]) if self.social_data else 7.0
            factors = {
                'economic_benefit_acceptance': base_acceptance / 10.0,
                'environmental_acceptance': (base_acceptance - 1) / 10.0,
                'social_cohesion_acceptance': base_acceptance / 10.0
            }
        
        return factors
    
    def identify_acceptance_barriers(self) -> List[str]:
        """识别接受度障碍"""
        barriers = []
        
        # 基于公众接受度分析
        public_acceptance = self._calculate_public_acceptance()
        if public_acceptance < 6:
            barriers.append("公众对项目的经济效益认知不足")
            barriers.append("缺乏透明的项目信息和沟通渠道")
        
        # 基于社会风险分析
        social_risk = self._assess_social_risk()
        if social_risk > 0.4:
            barriers.append("社区对项目潜在负面影响担忧")
            barriers.append("缺乏有效的参与和反馈机制")
        
        # 基于利益相关者分析
        stakeholder_feedback = self._analyze_stakeholder_feedback()
        low_acceptance_groups = [group for group, score in stakeholder_feedback.items() if score < 5]
        if low_acceptance_groups:
            barriers.append(f"部分利益相关者群体支持度较低: {[group.value for group in low_acceptance_groups]}")
        
        return barriers