"""
碳足迹核算与碳中和路径规划模块

精细化的工业产品全生命周期碳足迹计算与企业级碳中和路径规划工具
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


class EmissionScope(Enum):
    """排放范围"""
    SCOPE1 = "scope1"  # 直接排放
    SCOPE2 = "scope2"  # 间接排放
    SCOPE3 = "scope3"  # 价值链排放


class CarbonReductionStrategy(Enum):
    """碳减排策略"""
    ENERGY_EFFICIENCY = "energy_efficiency"
    RENEWABLE_ENERGY = "renewable_energy"
    CARBON_CAPTURE = "carbon_capture"
    PROCESS_OPTIMIZATION = "process_optimization"
    MATERIAL_SUBSTITUTION = "material_substitution"
    TRANSPORTATION_OPTIMIZATION = "transportation_optimization"
    CIRCULAR_ECONOMY = "circular_economy"


@dataclass
class EmissionSource:
    """排放源"""
    source_id: str
    source_type: str  # fuel, electricity, process, transportation
    scope: EmissionScope
    emission_factor: float  # kg CO2e/unit
    activity_data: float  # unit amount
    unit: str  # kWh, kg, m³, km, etc.
    location: str
    description: str = ""


@dataclass
class ProductCarbonFootprint:
    """产品碳足迹"""
    product_id: str
    product_name: str
    production_volume: float  # units/year
    total_emissions: float  # kg CO2e/year
    emissions_by_scope: Dict[EmissionScope, float]
    emissions_by_stage: Dict[str, float]  # raw_material, production, transportation, use_phase, end_of_life
    carbon_intensity: float  # kg CO2e/unit


@dataclass
class CarbonReductionMeasure:
    """碳减排措施"""
    measure_id: str
    strategy: CarbonReductionStrategy
    description: str
    applicable_sources: List[str]
    reduction_potential: float  # kg CO2e/year
    implementation_cost: float  # 元
    annual_operating_cost: float  # 元/年
    payback_period: float  # 年
    feasibility: float  # 0-1
    priority: int  # 1-5


@dataclass
class CarbonNeutralPathway:
    """碳中和路径"""
    pathway_id: str
    target_year: int
    baseline_emissions: float  # kg CO2e/year
    target_emissions: float  # kg CO2e/year
    reduction_measures: List[CarbonReductionMeasure]
    annual_emissions_trajectory: Dict[int, float]
    total_investment: float  # 元
    cumulative_savings: float  # 元
    achievement_probability: float  # 0-1


class CarbonFootprintCalculator(BaseIndustrialExtension):
    """碳足迹计算器
    
    精细化的工业产品全生命周期碳足迹计算与企业级碳中和路径规划工具
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化碳足迹计算器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - emission_sources: 排放源列表
            - product_footprints: 产品碳足迹列表
            - reduction_measures: 碳减排措施列表
            - carbon_pathways: 碳中和路径列表
        """
        super().__init__(config)
        
        self.emission_sources: Dict[str, EmissionSource] = {}
        self.product_footprints: Dict[str, ProductCarbonFootprint] = {}
        self.reduction_measures: Dict[str, CarbonReductionMeasure] = {}
        self.carbon_pathways: Dict[str, CarbonNeutralPathway] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'emission_sources' in config:
            for source_config in config['emission_sources']:
                source = EmissionSource(**source_config)
                self.emission_sources[source.source_id] = source
        
        if 'product_footprints' in config:
            for footprint_config in config['product_footprints']:
                footprint = ProductCarbonFootprint(**footprint_config)
                self.product_footprints[footprint.product_id] = footprint
        
        if 'reduction_measures' in config:
            for measure_config in config['reduction_measures']:
                measure = CarbonReductionMeasure(**measure_config)
                self.reduction_measures[measure.measure_id] = measure
        
        if 'carbon_pathways' in config:
            for pathway_config in config['carbon_pathways']:
                pathway = CarbonNeutralPathway(**pathway_config)
                self.carbon_pathways[pathway.pathway_id] = pathway
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.emission_sources:
                print("警告: 未配置排放源")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_emission_source(self, source: EmissionSource):
        """添加排放源
        
        Parameters
        ----------
        source : EmissionSource
            排放源
        """
        self.emission_sources[source.source_id] = source
    
    def add_product_footprint(self, footprint: ProductCarbonFootprint):
        """添加产品碳足迹
        
        Parameters
        ----------
        footprint : ProductCarbonFootprint
            产品碳足迹
        """
        self.product_footprints[footprint.product_id] = footprint
    
    def add_reduction_measure(self, measure: CarbonReductionMeasure):
        """添加碳减排措施
        
        Parameters
        ----------
        measure : CarbonReductionMeasure
            碳减排措施
        """
        self.reduction_measures[measure.measure_id] = measure
    
    def calculate_emissions(
        self,
        source_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """计算排放
        
        Parameters
        ----------
        source_id : str, optional
            排放源ID，如果为None则计算所有排放源
        
        Returns
        -------
        Dict[str, Any]
            排放计算结果
        """
        sources_to_calculate = [source_id] if source_id else list(self.emission_sources.keys())
        
        results = {
            'total_emissions': 0.0,
            'emissions_by_source': {},
            'emissions_by_scope': {
                'scope1': 0.0,
                'scope2': 0.0,
                'scope3': 0.0
            },
            'emissions_by_type': {}
        }
        
        for sid in sources_to_calculate:
            if sid not in self.emission_sources:
                continue
            
            source = self.emission_sources[sid]
            emissions = source.activity_data * source.emission_factor
            
            results['total_emissions'] += emissions
            results['emissions_by_source'][sid] = emissions
            results['emissions_by_scope'][source.scope.value] += emissions
            
            if source.source_type not in results['emissions_by_type']:
                results['emissions_by_type'][source.source_type] = 0.0
            results['emissions_by_type'][source.source_type] += emissions
        
        return results
    
    def calculate_product_footprint(
        self,
        product_id: str,
        raw_material_emissions: float,
        production_emissions: float,
        transportation_emissions: float,
        use_phase_emissions: float,
        end_of_life_emissions: float
    ) -> ProductCarbonFootprint:
        """计算产品碳足迹
        
        Parameters
        ----------
        product_id : str
            产品ID
        raw_material_emissions : float
            原材料阶段排放
        production_emissions : float
            生产阶段排放
        transportation_emissions : float
            运输阶段排放
        use_phase_emissions : float
            使用阶段排放
        end_of_life_emissions : float
            终期处理阶段排放
        
        Returns
        -------
        ProductCarbonFootprint
            产品碳足迹
        """
        total_emissions = (
            raw_material_emissions +
            production_emissions +
            transportation_emissions +
            use_phase_emissions +
            end_of_life_emissions
        )
        
        emissions_by_stage = {
            'raw_material': raw_material_emissions,
            'production': production_emissions,
            'transportation': transportation_emissions,
            'use_phase': use_phase_emissions,
            'end_of_life': end_of_life_emissions
        }
        
        emissions_by_scope = {
            EmissionScope.SCOPE1: production_emissions,
            EmissionScope.SCOPE2: transportation_emissions,
            EmissionScope.SCOPE3: raw_material_emissions + use_phase_emissions + end_of_life_emissions
        }
        
        if product_id in self.product_footprints:
            footprint = self.product_footprints[product_id]
            production_volume = footprint.production_volume
        else:
            production_volume = 1000.0
        
        carbon_intensity = total_emissions / production_volume if production_volume > 0 else 0
        
        footprint = ProductCarbonFootprint(
            product_id=product_id,
            product_name=self.product_footprints.get(product_id, ProductCarbonFootprint(
                product_id=product_id,
                product_name="",
                production_volume=production_volume,
                total_emissions=0.0,
                emissions_by_scope={},
                emissions_by_stage={},
                carbon_intensity=0.0
            )).product_name,
            production_volume=production_volume,
            total_emissions=total_emissions,
            emissions_by_scope=emissions_by_scope,
            emissions_by_stage=emissions_by_stage,
            carbon_intensity=carbon_intensity
        )
        
        self.product_footprints[product_id] = footprint
        return footprint
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.CARBON,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化碳排放
        
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
        
        for source_id, source in self.emission_sources.items():
            hourly_emissions = source.activity_data * source.emission_factor / 24
            reduction_potential = hourly_emissions * 0.3
            schedule = []
            
            for hour in range(time_horizon):
                carbon_cost = hourly_emissions * 0.05  # 元/kg CO2
                reduction_savings = reduction_potential * 0.05
                total_cost += carbon_cost - reduction_savings
                total_carbon += hourly_emissions - reduction_potential
                
                schedule.append({
                    'hour': hour,
                    'emissions': hourly_emissions,
                    'reduction': reduction_potential,
                    'net_emissions': hourly_emissions - reduction_potential,
                    'cost': carbon_cost - reduction_savings
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.7
        
        for measure_id, measure in self.reduction_measures.items():
            utilization = 0.6 + np.random.random() * 0.3
            component_utilization[measure_id] = utilization
            
            measure_cost = measure.implementation_cost * 0.1 / time_horizon
            total_cost += measure_cost
        
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
                    'carbon_cost': total_cost * 0.6,
                    'measure_cost': total_cost * 0.4
                },
                'emission_sources': {
                    'direct_emissions': total_carbon * 0.7,
                    'indirect_emissions': total_carbon * 0.3
                }
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
        
        for source_id, source in self.emission_sources.items():
            hourly_emissions = source.activity_data * source.emission_factor / 24
            reduction_potential = hourly_emissions * 0.4
            schedule = []
            
            for hour in range(time_horizon):
                net_emissions = hourly_emissions - reduction_potential
                total_carbon += net_emissions
                
                schedule.append({
                    'hour': hour,
                    'emissions': hourly_emissions,
                    'reduction': reduction_potential,
                    'net_emissions': net_emissions
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.85
        
        for measure_id, measure in self.reduction_measures.items():
            component_utilization[measure_id] = 0.75
        
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
                    'direct_emissions': total_carbon * 0.7,
                    'indirect_emissions': total_carbon * 0.3
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
        
        for source_id, source in self.emission_sources.items():
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.9 + np.random.random() * 0.1
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'reliability': reliability
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.8
        
        for measure_id, measure in self.reduction_measures.items():
            component_utilization[measure_id] = 0.85
            reliability_score += measure.feasibility
        
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
        
        for source_id, source in self.emission_sources.items():
            hourly_emissions = source.activity_data * source.emission_factor / 24
            reduction_efficiency = 0.8 + np.random.random() * 0.15
            schedule = []
            
            for hour in range(time_horizon):
                reduction = hourly_emissions * reduction_efficiency
                efficiency_score += reduction_efficiency
                
                schedule.append({
                    'hour': hour,
                    'emissions': hourly_emissions,
                    'reduction': reduction,
                    'reduction_efficiency': reduction_efficiency
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.85
        
        for measure_id, measure in self.reduction_measures.items():
            component_utilization[measure_id] = 0.8
            efficiency_score += measure.feasibility
        
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
        weights = {'cost': 0.3, 'carbon': 0.4, 'efficiency': 0.3}
        
        cost_result = self._optimize_cost(time_horizon)
        carbon_result = self._optimize_carbon(time_horizon)
        efficiency_result = self._optimize_efficiency(time_horizon)
        
        normalized_cost = abs(cost_result.total_cost) / 10000.0
        normalized_carbon = abs(carbon_result.total_carbon_emissions) / 1000.0
        normalized_efficiency = 1.0 - (efficiency_result.objective_value / 
                                        (len(self.emission_sources) + len(self.reduction_measures)))
        
        objective_value = (
            weights['cost'] * normalized_cost +
            weights['carbon'] * normalized_carbon +
            weights['efficiency'] * normalized_efficiency
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
                    'efficiency': normalized_efficiency
                },
                'cost_components': cost_result.additional_metrics.get('cost_components', {}),
                'emission_sources': carbon_result.additional_metrics.get('emission_sources', {})
            }
        )
    
    def develop_carbon_neutral_pathway(
        self,
        baseline_year: int,
        target_year: int,
        baseline_emissions: float,
        target_emissions: float,
        budget_constraint: Optional[float] = None
    ) -> CarbonNeutralPathway:
        """开发碳中和路径
        
        Parameters
        ----------
        baseline_year : int
            基准年
        target_year : int
            目标年
        baseline_emissions : float
            基准排放量
        target_emissions : float
            目标排放量
        budget_constraint : float, optional
            预算约束
        
        Returns
        -------
        CarbonNeutralPathway
            碳中和路径
        """
        years = target_year - baseline_year
        annual_reduction_rate = (baseline_emissions - target_emissions) / years
        
        applicable_measures = [
            measure for measure in self.reduction_measures.values()
            if measure.feasibility > 0.7
        ]
        
        selected_measures = []
        total_reduction = 0.0
        total_investment = 0.0
        
        for measure in sorted(applicable_measures, key=lambda m: m.reduction_potential / m.implementation_cost, reverse=True):
            if total_reduction + measure.reduction_potential >= annual_reduction_rate:
                selected_measures.append(measure)
                total_reduction += measure.reduction_potential
                total_investment += measure.implementation_cost
                
                if budget_constraint and total_investment > budget_constraint:
                    break
        
        annual_emissions_trajectory = {}
        current_emissions = baseline_emissions
        for year in range(baseline_year, target_year + 1):
            annual_emissions_trajectory[year] = current_emissions
            current_emissions = max(target_emissions, current_emissions - annual_reduction_rate)
        
        cumulative_savings = sum(
            measure.reduction_potential * 0.05 * (target_year - baseline_year)
            for measure in selected_measures
        )
        
        achievement_probability = min(
            sum(m.feasibility for m in selected_measures) / len(selected_measures) if selected_measures else 0,
            0.95
        )
        
        pathway = CarbonNeutralPathway(
            pathway_id=f"pathway_{baseline_year}_{target_year}",
            target_year=target_year,
            baseline_emissions=baseline_emissions,
            target_emissions=target_emissions,
            reduction_measures=selected_measures,
            annual_emissions_trajectory=annual_emissions_trajectory,
            total_investment=total_investment,
            cumulative_savings=cumulative_savings,
            achievement_probability=achievement_probability
        )
        
        self.carbon_pathways[pathway.pathway_id] = pathway
        return pathway
    
    def generate_carbon_report(self) -> Dict[str, Any]:
        """生成碳排放报告
        
        Returns
        -------
        Dict[str, Any]
            碳排放报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        emission_calculation = self.calculate_emissions()
        
        report = {
            'summary': {
                'total_emission_sources': len(self.emission_sources),
                'total_product_footprints': len(self.product_footprints),
                'total_reduction_measures': len(self.reduction_measures),
                'total_carbon_pathways': len(self.carbon_pathways),
                'total_emissions': emission_calculation['total_emissions'],
                'emissions_by_scope': emission_calculation['emissions_by_scope'],
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'emission_source_details': {},
            'product_footprint_details': {},
            'reduction_measure_details': {},
            'pathway_details': {}
        }
        
        for source_id, source in self.emission_sources.items():
            emissions = source.activity_data * source.emission_factor
            report['emission_source_details'][source_id] = {
                'type': source.source_type,
                'scope': source.scope.value,
                'location': source.location,
                'activity_data': source.activity_data,
                'unit': source.unit,
                'emission_factor': source.emission_factor,
                'emissions': emissions,
                'description': source.description
            }
        
        for product_id, footprint in self.product_footprints.items():
            report['product_footprint_details'][product_id] = {
                'name': footprint.product_name,
                'production_volume': footprint.production_volume,
                'total_emissions': footprint.total_emissions,
                'carbon_intensity': footprint.carbon_intensity,
                'emissions_by_scope': {scope.value: emissions for scope, emissions in footprint.emissions_by_scope.items()},
                'emissions_by_stage': footprint.emissions_by_stage
            }
        
        for measure_id, measure in self.reduction_measures.items():
            report['reduction_measure_details'][measure_id] = {
                'strategy': measure.strategy.value,
                'description': measure.description,
                'applicable_sources': measure.applicable_sources,
                'reduction_potential': measure.reduction_potential,
                'implementation_cost': measure.implementation_cost,
                'annual_operating_cost': measure.annual_operating_cost,
                'payback_period': measure.payback_period,
                'feasibility': measure.feasibility,
                'priority': measure.priority
            }
        
        for pathway_id, pathway in self.carbon_pathways.items():
            report['pathway_details'][pathway_id] = {
                'target_year': pathway.target_year,
                'baseline_emissions': pathway.baseline_emissions,
                'target_emissions': pathway.target_emissions,
                'reduction_rate': (pathway.baseline_emissions - pathway.target_emissions) / (pathway.target_year - 2024),
                'number_of_measures': len(pathway.reduction_measures),
                'total_investment': pathway.total_investment,
                'cumulative_savings': pathway.cumulative_savings,
                'achievement_probability': pathway.achievement_probability
            }
        
        return report