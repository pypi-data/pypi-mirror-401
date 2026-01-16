"""
场景评估模块

提供全面的能源系统场景评估功能，包括：
- 经济性评估：成本、收益、投资回报分析
- 可靠性评估：系统可靠性、冗余度分析
- 环境影响评估：碳排放、环境影响分析
- 风险评估：技术风险、经济风险评估
- 社会影响评估：社会效益、用户接受度分析
- 综合评分：多维度加权评分系统
"""

from .economic_evaluation import *
from .reliability_evaluation import *
from .environmental_evaluation import *
from .risk_evaluation import *
from .social_evaluation import *
from .comprehensive_evaluation import *
from .evaluation_framework import *
from .security_evaluation import *

__all__ = [
    # 经济评估
    'EconomicEvaluator', 'CostBenefitAnalyzer', 'ROIAnalyzer', 'NPVCalculator',
    'EconomicResult', 'CostItem',
    
    # 可靠性评估
    'ReliabilityEvaluator', 'LORAAnalyzer', 'LOLECalculator', 'EENSAnalyzer',
    'ReliabilityResult', 'ComponentReliability',
    
    # 环境影响评估
    'EnvironmentalEvaluator', 'LCAAnalyzer', 'CarbonFootprintAnalyzer',
    'EnvironmentalResult', 'EmissionFactor',
    
    # 风险评估
    'RiskEvaluator', 'MonteCarloAnalyzer', 'SensitivityAnalyzer', 'ScenarioRiskAnalyzer',
    'RiskResult', 'RiskProfile',
    
    # 社会影响评估
    'SocialEvaluator', 'ImpactAnalyzer', 'AcceptanceAnalyzer',
    'SocialResult', 'SocialIndicator',
    

    
    # 安全评估（新添加）
    'SecurityEvaluator', 'UrbanEnergySystemSecurityEvaluator', 'PhotovoltaicUncertaintyAnalyzer',
    'TrafficElectrificationSecurityAnalyzer', 'SecurityEvaluationResult',
    'SecurityEvaluationType', 'UncertaintyType', 'ReliabilityMetric',
    'UncertaintyModel', 'ReliabilityResult',
    
    # 综合评估
    'ComprehensiveEvaluator', 'MultiCriteriaEvaluator', 'ScoringSystem',
    'ComprehensiveResult', 'EvaluationWeights',
    
    # 评估框架
    'ScenarioEvaluator', 'EvaluationPipeline', 'EvaluationReport',
    'DEFAULT_EVALUATION_CONFIG'
]

# 默认评估配置
DEFAULT_EVALUATION_CONFIG = {
    'economic': {
        'evaluation_horizon': 20,  # 年
        'discount_rate': 0.08,     # 贴现率
        'currency': 'USD',
        'include_externalities': True
    },
    'reliability': {
        'analysis_period': 8760,   # 小时
        'confidence_level': 0.95,
        'consider_maintenance': True
    },
    'environmental': {
        'impact_categories': ['carbon', 'water', 'land', 'biodiversity'],
        'functional_unit': 'kWh',
        'include_lifecycle': True
    },
    'risk': {
        'confidence_levels': [0.05, 0.5, 0.95],
        'monte_carlo_runs': 10000,
        'sensitivity_analysis': True
    },
    'social': {
        'indicators': ['employment', 'energy_access', 'equity', 'acceptability'],
        'survey_size': 1000,
        'evaluation_method': 'multi_stakeholder'
    },
    'comprehensive': {
        'weights': {
            'economic': 0.3,
            'reliability': 0.25,
            'environmental': 0.2,
            'risk': 0.15,
            'social': 0.1
        },
        'normalization_method': 'min_max',
        'aggregation_method': 'weighted_sum'
    }
}