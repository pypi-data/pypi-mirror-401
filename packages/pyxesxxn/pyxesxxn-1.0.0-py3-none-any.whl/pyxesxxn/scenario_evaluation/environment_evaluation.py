"""
环境评估模块

提供能源系统的环境影响评估功能，包括：
- 排放评估：CO2、SO2、NOx、颗粒物等污染物排放
- 生命周期评估：LCA分析、环境足迹
- 碳足迹计算：全生命周期碳排放
- 环境影响指标：酸化潜力、富营养化、光化学烟雾
- 资源消耗：水、土地、原材料使用
- 可再生能源比例：清洁能源占比分析
- 环境经济效益：减排成本效益分析
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

class PollutantType(Enum):
    """污染物类型"""
    CO2 = "co2"                      # 二氧化碳
    SO2 = "so2"                      # 二氧化硫
    NOX = "nox"                      # 氮氧化物
    PM25 = "pm25"                    # PM2.5
    PM10 = "pm10"                    # PM10
    CH4 = "ch4"                      # 甲烷
    N2O = "n2o"                      # 氧化亚氮
    VOC = "voc"                      # 挥发性有机化合物

class EmissionSource(Enum):
    """排放源类型"""
    COAL_PLANT = "coal_plant"
    GAS_PLANT = "gas_plant"
    OIL_PLANT = "oil_plant"
    NUCLEAR_PLANT = "nuclear_plant"
    HYDRO_PLANT = "hydro_plant"
    WIND_PLANT = "wind_plant"
    SOLAR_PLANT = "solar_plant"
    BIOMASS_PLANT = "biomass_plant"
    GEOTHERMAL_PLANT = "geothermal_plant"
    BATTERY_STORAGE = "battery_storage"

class ImpactCategory(Enum):
    """环境影响类别"""
    GLOBAL_WARMING = "global_warming"      # 全球变暖
    ACIDIFICATION = "acidification"        # 酸化
    EUTROPHICATION = "eutrophication"      # 富营养化
    PHOTOCHEMICAL_SMOG = "photochemical_smog"  # 光化学烟雾
    WATER_DEPLETION = "water_depletion"    # 水资源消耗
    LAND_USE = "land_use"                  # 土地利用
    RESOURCE_DEPLETION = "resource_depletion"  # 资源消耗

@dataclass
class EmissionFactor:
    """排放因子"""
    pollutant_type: PollutantType
    emission_source: EmissionSource
    factor_value: float                    # kg/MWh
    factor_unit: str                       # 排放因子单位
    technology_specific: bool = False      # 是否技术特定
    fuel_quality_factor: float = 1.0      # 燃料质量因子

@dataclass
class EnvironmentalData:
    """环境数据"""
    component_id: str
    component_type: str
    capacity_mw: float
    annual_generation_mwh: float
    emission_factors: Dict[PollutantType, EmissionFactor]
    water_consumption: float = 0          # m³/MWh
    land_use: float = 0                   # km²
    material_consumption: Dict[str, float] = field(default_factory=dict)  # 材料消耗 (kg/MWh)
    noise_level: float = 0                # dB
    
@dataclass
class LifecycleData:
    """生命周期数据"""
    component_id: str
    manufacturing_emissions: Dict[PollutantType, float]  # 制造阶段排放 (kg/MWh)
    construction_emissions: Dict[PollutantType, float]   # 建设阶段排放
    operation_emissions: Dict[PollutantType, float]      # 运营阶段排放
    decommission_emissions: Dict[PollutantType, float]   # 退役阶段排放
    manufacturing_energy: float = 0         # MJ/MWh
    construction_energy: float = 0          # MJ/MWh
    lifetime_years: float = 25              # 预期寿命 (年)
    
@dataclass
class CarbonFootprintResult:
    """碳足迹结果"""
    total_co2_equivalent: float            # 总CO2当量 (kg/MWh)
    scope1_emissions: float                # 范围1排放 (直接排放)
    scope2_emissions: float                # 范围2排放 (电力消耗)
    scope3_emissions: float                # 范围3排放 (其他间接排放)
    manufacturing_footprint: float         # 制造阶段碳足迹
    operation_footprint: float             # 运营阶段碳足迹
    end_of_life_footprint: float          # 报废阶段碳足迹
    renewable_fraction: float              # 可再生能源比例
    offset_potential: float                # 碳抵消潜力

@dataclass
class EnvironmentalImpactMetrics:
    """环境影响指标"""
    # 气候变化
    global_warming_potential: float        # 全球变暖潜势 (kg CO2-eq/MWh)
    
    # 酸化潜势
    acidification_potential: float         # 酸化潜势 (kg SO2-eq/MWh)
    
    # 富营养化潜势
    eutrophication_potential: float        # 富营养化潜势 (kg PO4-eq/MWh)
    
    # 光化学烟雾潜势
    photochemical_smog_potential: float    # 光化学烟雾潜势 (kg NMVOC-eq/MWh)
    
    # 水资源影响
    water_consumption_total: float         # 总水消耗 (L/MWh)
    water_depletion_index: float           # 水资源消耗指数
    
    # 土地利用
    land_use_total: float                  # 总土地利用 (m²/MWh)
    land_use_change_impact: float          # 土地利用变化影响
    
    # 资源消耗
    resource_depletion_index: float        # 资源消耗指数
    critical_material_usage: float         # 关键材料使用量
    
    # 环境经济效益
    abatement_cost: float                  # 减排成本 ($/tCO2-eq)
    environmental_benefit_value: float     # 环境效益价值 ($/MWh)

@dataclass
class EnvironmentalResult:
    """环境评估结果"""
    # 基础排放
    total_emissions: Dict[PollutantType, float]
    emissions_by_source: Dict[str, Dict[PollutantType, float]]
    emissions_intensity: float             # kg CO2-eq/MWh
    
    # 生命周期评估
    lifecycle_emissions: Dict[str, Dict[PollutantType, float]]
    carbon_footprint: CarbonFootprintResult
    
    # 环境影响指标
    impact_metrics: EnvironmentalImpactMetrics
    
    # 资源使用
    resource_consumption: Dict[str, float]
    water_footprint: float                # 水足迹
    material_footprint: float             # 材料足迹
    
    # 可再生能源分析
    renewable_energy_fraction: float      # 可再生能源比例
    clean_energy_benefits: Dict[str, float]
    
    # 比较分析
    benchmark_comparison: Dict[str, float]
    improvement_potential: Dict[str, float]
    
    # 政策建议
    policy_recommendations: List[str]

class EnvironmentalEvaluator(Evaluator):
    """环境评估器"""
    
    def __init__(self, assessment_period: int = 365, carbon_price: float = 50.0):
        super().__init__("EnvironmentalEvaluator", EvaluationType.ENVIRONMENTAL)
        self.assessment_period = assessment_period  # 评估期(天)
        self.carbon_price = carbon_price           # 碳价格 ($/tCO2)
        self.environmental_data: Dict[str, EnvironmentalData] = {}
        self.lifecycle_data: Dict[str, LifecycleData] = {}
        self.emission_factors_db: Dict[EmissionSource, Dict[PollutantType, EmissionFactor]] = {}
        self._initialize_emission_factors()
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行环境评估"""
        start_time = datetime.now()
        self.logger.info("开始环境评估")
        
        try:
            # 从场景数据中提取环境信息
            scenario_data = context.scenario_data
            self._extract_environmental_data(scenario_data)
            
            # 计算排放
            emission_results = self._calculate_emissions()
            
            # 执行生命周期评估
            lca_results = self._perform_lifecycle_assessment()
            
            # 计算环境影响指标
            impact_metrics = self._calculate_impact_metrics()
            
            # 分析资源消耗
            resource_analysis = self._analyze_resource_consumption()
            
            # 计算碳足迹
            carbon_footprint = self._calculate_carbon_footprint()
            
            # 创建结果
            result = EnvironmentalResult(
                total_emissions=emission_results['total_emissions'],
                emissions_by_source=emission_results['emissions_by_source'],
                emissions_intensity=emission_results['emissions_intensity'],
                lifecycle_emissions=lca_results,
                carbon_footprint=carbon_footprint,
                impact_metrics=impact_metrics,
                resource_consumption=resource_analysis,
                water_footprint=self._calculate_water_footprint(),
                material_footprint=self._calculate_material_footprint(),
                renewable_energy_fraction=self._calculate_renewable_fraction(),
                clean_energy_benefits=self._calculate_clean_energy_benefits(),
                benchmark_comparison=self._compare_with_benchmarks(),
                improvement_potential=self._identify_improvement_potential(),
                policy_recommendations=self._generate_policy_recommendations()
            )
            
            # 创建标准评估结果
            metrics = {
                'total_co2_emissions': result.total_emissions.get(PollutantType.CO2, 0),
                'emissions_intensity': result.emissions_intensity,
                'renewable_fraction': result.renewable_energy_fraction,
                'carbon_footprint': result.carbon_footprint.total_co2_equivalent,
                'water_consumption': result.impact_metrics.water_consumption_total,
                'land_use': result.impact_metrics.land_use_total
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={'environmental_result': result},
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("环境评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"环境评估失败: {str(e)}")
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
        required_fields = ['generation_mix', 'emission_factors', 'operational_data']
        for field in required_fields:
            if field not in context.metadata:
                self.logger.warning(f"缺少必需字段: {field}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['generation_mix', 'emission_factors', 'operational_data', 'lifecycle_data']
    
    def add_environmental_data(self, env_data: EnvironmentalData):
        """添加环境数据"""
        self.environmental_data[env_data.component_id] = env_data
    
    def add_lifecycle_data(self, lca_data: LifecycleData):
        """添加生命周期数据"""
        self.lifecycle_data[lca_data.component_id] = lca_data
    
    def _initialize_emission_factors(self):
        """初始化排放因子数据库"""
        # 简化版排放因子数据 (kg/MWh)
        default_factors = {
            EmissionSource.COAL_PLANT: {
                PollutantType.CO2: EmissionFactor(PollutantType.CO2, EmissionSource.COAL_PLANT, 950, "kg/MWh"),
                PollutantType.SO2: EmissionFactor(PollutantType.SO2, EmissionSource.COAL_PLANT, 1.2, "kg/MWh"),
                PollutantType.NOX: EmissionFactor(PollutantType.NOX, EmissionSource.COAL_PLANT, 0.6, "kg/MWh"),
                PollutantType.PM25: EmissionFactor(PollutantType.PM25, EmissionSource.COAL_PLANT, 0.08, "kg/MWh"),
            },
            EmissionSource.GAS_PLANT: {
                PollutantType.CO2: EmissionFactor(PollutantType.CO2, EmissionSource.GAS_PLANT, 400, "kg/MWh"),
                PollutantType.NOX: EmissionFactor(PollutantType.NOX, EmissionSource.GAS_PLANT, 0.1, "kg/MWh"),
                PollutantType.SO2: EmissionFactor(PollutantType.SO2, EmissionSource.GAS_PLANT, 0.0, "kg/MWh"),
            },
            EmissionSource.WIND_PLANT: {
                PollutantType.CO2: EmissionFactor(PollutantType.CO2, EmissionSource.WIND_PLANT, 10, "kg/MWh"),
            },
            EmissionSource.SOLAR_PLANT: {
                PollutantType.CO2: EmissionFactor(PollutantType.CO2, EmissionSource.SOLAR_PLANT, 40, "kg/MWh"),
            },
            EmissionSource.HYDRO_PLANT: {
                PollutantType.CO2: EmissionFactor(PollutantType.CO2, EmissionSource.HYDRO_PLANT, 20, "kg/MWh"),
            },
            EmissionSource.NUCLEAR_PLANT: {
                PollutantType.CO2: EmissionFactor(PollutantType.CO2, EmissionSource.NUCLEAR_PLANT, 12, "kg/MWh"),
            }
        }
        
        self.emission_factors_db = default_factors
    
    def _extract_environmental_data(self, scenario_data: Dict[str, Any]):
        """从场景数据中提取环境信息"""
        # 这里应该从场景数据中解析发电组合、排放因子等
        # 简化实现
        if 'generation_mix' in scenario_data:
            generation_mix = scenario_data['generation_mix']
            for comp_id, data in generation_mix.items():
                if comp_id not in self.environmental_data:
                    # 创建默认环境数据
                    env_data = EnvironmentalData(
                        component_id=comp_id,
                        component_type=data.get('type', 'unknown'),
                        capacity_mw=data.get('capacity', 0),
                        annual_generation_mwh=data.get('generation', 0),
                        emission_factors=self._get_emission_factors_for_type(data.get('type'))
                    )
                    self.environmental_data[comp_id] = env_data
    
    def _get_emission_factors_for_type(self, comp_type: str) -> Dict[PollutantType, EmissionFactor]:
        """根据组件类型获取排放因子"""
        # 映射组件类型到排放源
        type_to_source = {
            'coal': EmissionSource.COAL_PLANT,
            'gas': EmissionSource.GAS_PLANT,
            'wind': EmissionSource.WIND_PLANT,
            'solar': EmissionSource.SOLAR_PLANT,
            'hydro': EmissionSource.HYDRO_PLANT,
            'nuclear': EmissionSource.NUCLEAR_PLANT
        }
        
        source = type_to_source.get(comp_type.lower(), EmissionSource.GAS_PLANT)
        return self.emission_factors_db.get(source, {})
    
    def _calculate_emissions(self) -> Dict[str, Any]:
        """计算排放"""
        total_emissions = {pollutant: 0.0 for pollutant in PollutantType}
        emissions_by_source = {}
        total_generation = 0
        
        for comp_id, env_data in self.environmental_data.items():
            source_emissions = {}
            
            # 计算该组件的排放
            for pollutant, factor in env_data.emission_factors.items():
                # 排放 = 发电量 × 排放因子
                emissions = env_data.annual_generation_mwh * factor.factor_value
                total_emissions[pollutant] += emissions
                source_emissions[pollutant] = emissions
            
            emissions_by_source[comp_id] = source_emissions
            total_generation += env_data.annual_generation_mwh
        
        # 计算排放强度 (kg CO2-eq/MWh)
        co2_emissions = total_emissions[PollutantType.CO2]
        emissions_intensity = co2_emissions / total_generation if total_generation > 0 else 0
        
        return {
            'total_emissions': total_emissions,
            'emissions_by_source': emissions_by_source,
            'emissions_intensity': emissions_intensity
        }
    
    def _perform_lifecycle_assessment(self) -> Dict[str, Dict[PollutantType, float]]:
        """执行生命周期评估"""
        lifecycle_emissions = {
            'manufacturing': {pollutant: 0.0 for pollutant in PollutantType},
            'construction': {pollutant: 0.0 for pollutant in PollutantType},
            'operation': {pollutant: 0.0 for pollutant in PollutantType},
            'decommission': {pollutant: 0.0 for pollutant in PollutantType}
        }
        
        # 如果有生命周期数据，计算各阶段排放
        for comp_id, lca_data in self.lifecycle_data.items():
            for phase, emissions in [
                ('manufacturing', lca_data.manufacturing_emissions),
                ('construction', lca_data.construction_emissions),
                ('operation', lca_data.operation_emissions),
                ('decommission', lca_data.decommission_emissions)
            ]:
                for pollutant, amount in emissions.items():
                    lifecycle_emissions[phase][pollutant] += amount
        
        return lifecycle_emissions
    
    def _calculate_impact_metrics(self) -> EnvironmentalImpactMetrics:
        """计算环境影响指标"""
        total_emissions = {pollutant: 0.0 for pollutant in PollutantType}
        
        # 汇总所有排放
        for env_data in self.environmental_data.values():
            for pollutant, factor in env_data.emission_factors.items():
                emissions = env_data.annual_generation_mwh * factor.factor_value
                total_emissions[pollutant] += emissions
        
        total_generation = sum(env.annual_generation_mwh for env in self.environmental_data.values())
        
        # 计算各项指标
        co2 = total_emissions[PollutantType.CO2]
        so2 = total_emissions[PollutantType.SO2]
        nox = total_emissions[PollutantType.NOX]
        pm25 = total_emissions[PollutantType.PM25]
        
        # 环境影响指标 (简化计算)
        global_warming_potential = co2 / total_generation if total_generation > 0 else 0
        acidification_potential = (so2 + 0.7 * nox) / total_generation if total_generation > 0 else 0
        eutrophication_potential = (0.1 * nox + 0.02 * pm25) / total_generation if total_generation > 0 else 0
        photochemical_smog_potential = nox / total_generation if total_generation > 0 else 0
        
        # 资源使用指标
        total_water = sum(env.water_consumption * env.annual_generation_mwh for env in self.environmental_data.values())
        total_land = sum(env.land_use for env in self.environmental_data.values())
        
        return EnvironmentalImpactMetrics(
            global_warming_potential=global_warming_potential,
            acidification_potential=acidification_potential,
            eutrophication_potential=eutrophication_potential,
            photochemical_smog_potential=photochemical_smog_potential,
            water_consumption_total=total_water,
            water_depletion_index=total_water / total_generation if total_generation > 0 else 0,
            land_use_total=total_land,
            land_use_change_impact=0,  # 简化
            resource_depletion_index=0,  # 简化
            critical_material_usage=0,   # 简化
            abatement_cost=self._calculate_abatement_cost(global_warming_potential),
            environmental_benefit_value=self._calculate_environmental_benefit_value()
        )
    
    def _analyze_resource_consumption(self) -> Dict[str, float]:
        """分析资源消耗"""
        resource_consumption = {
            'water_total': 0,
            'land_total': 0,
            'materials_total': 0,
            'energy_total': 0
        }
        
        for env_data in self.environmental_data.values():
            resource_consumption['water_total'] += env_data.water_consumption * env_data.annual_generation_mwh
            resource_consumption['land_total'] += env_data.land_use
            resource_consumption['materials_total'] += sum(env_data.material_consumption.values())
        
        return resource_consumption
    
    def _calculate_carbon_footprint(self) -> CarbonFootprintResult:
        """计算碳足迹"""
        total_co2 = 0
        scope1 = 0
        scope2 = 0
        scope3 = 0
        
        renewable_generation = 0
        fossil_generation = 0
        
        for env_data in self.environmental_data.values():
            co2_emissions = 0
            
            # 计算直接排放 (范围1)
            for pollutant, factor in env_data.emission_factors.items():
                if pollutant == PollutantType.CO2:
                    co2_emissions = env_data.annual_generation_mwh * factor.factor_value
                    total_co2 += co2_emissions
                    scope1 += co2_emissions
                    break
            
            # 判断是否为可再生能源
            is_renewable = any(source in [EmissionSource.WIND_PLANT, EmissionSource.SOLAR_PLANT, 
                                       EmissionSource.HYDRO_PLANT, EmissionSource.BIOMASS_PLANT]
                             for source in env_data.emission_factors.values())
            
            if is_renewable:
                renewable_generation += env_data.annual_generation_mwh
            else:
                fossil_generation += env_data.annual_generation_mwh
        
        total_generation = renewable_generation + fossil_generation
        
        # 计算生命周期碳足迹
        manufacturing_footprint = self._calculate_manufacturing_footprint()
        operation_footprint = scope1
        end_of_life_footprint = self._calculate_end_of_life_footprint()
        
        # 计算可再生能源比例
        renewable_fraction = renewable_generation / total_generation if total_generation > 0 else 0
        
        # 计算碳抵消潜力
        offset_potential = renewable_generation * 0.4  # 假设可再生能源的抵消潜力
        
        return CarbonFootprintResult(
            total_co2_equivalent=total_co2,
            scope1_emissions=scope1,
            scope2_emissions=scope2,
            scope3_emissions=scope3,
            manufacturing_footprint=manufacturing_footprint,
            operation_footprint=operation_footprint,
            end_of_life_footprint=end_of_life_footprint,
            renewable_fraction=renewable_fraction,
            offset_potential=offset_potential
        )
    
    def _calculate_water_footprint(self) -> float:
        """计算水足迹"""
        total_water = 0
        
        for env_data in self.environmental_data.values():
            water_usage = env_data.water_consumption * env_data.annual_generation_mwh
            total_water += water_usage
        
        return total_water
    
    def _calculate_material_footprint(self) -> float:
        """计算材料足迹"""
        total_materials = 0
        
        for env_data in self.environmental_data.values():
            materials = sum(env_data.material_consumption.values())
            total_materials += materials
        
        return total_materials
    
    def _calculate_renewable_fraction(self) -> float:
        """计算可再生能源比例"""
        total_generation = sum(env.annual_generation_mwh for env in self.environmental_data.values())
        if total_generation == 0:
            return 0
        
        renewable_generation = 0
        
        for env_data in self.environmental_data.values():
            # 检查是否为可再生能源
            is_renewable = self._check_if_renewable(env_data.component_type)
            if is_renewable:
                renewable_generation += env_data.annual_generation_mwh
        
        return renewable_generation / total_generation
    
    def _check_if_renewable(self, comp_type: str) -> bool:
        """检查是否为可再生能源"""
        renewable_types = ['wind', 'solar', 'hydro', 'biomass', 'geothermal']
        return comp_type.lower() in renewable_types
    
    def _calculate_clean_energy_benefits(self) -> Dict[str, float]:
        """计算清洁能源效益"""
        renewable_fraction = self._calculate_renewable_fraction()
        total_generation = sum(env.annual_generation_mwh for env in self.environmental_data.values())
        
        # 计算减排效益
        avoided_emissions = renewable_fraction * total_generation * 0.4  # 假设减排因子
        
        # 计算健康效益
        health_benefits = avoided_emissions * 0.05  # 假设每吨CO2的健康效益
        
        # 计算生态效益
        ecological_benefits = avoided_emissions * 0.02  # 假设每吨CO2的生态效益
        
        return {
            'avoided_co2_emissions': avoided_emissions,
            'health_benefits': health_benefits,
            'ecological_benefits': ecological_benefits,
            'total_environmental_benefits': health_benefits + ecological_benefits
        }
    
    def _calculate_manufacturing_footprint(self) -> float:
        """计算制造阶段碳足迹"""
        manufacturing_co2 = 0
        
        for comp_id, lca_data in self.lifecycle_data.items():
            manufacturing_co2 += lca_data.manufacturing_emissions.get(PollutantType.CO2, 0)
        
        return manufacturing_co2
    
    def _calculate_end_of_life_footprint(self) -> float:
        """计算报废阶段碳足迹"""
        decommission_co2 = 0
        
        for comp_id, lca_data in self.lifecycle_data.items():
            decommission_co2 += lca_data.decommission_emissions.get(PollutantType.CO2, 0)
        
        return decommission_co2
    
    def _compare_with_benchmarks(self) -> Dict[str, float]:
        """与基准进行比较"""
        current_emissions_intensity = self._calculate_emissions()['emissions_intensity']
        
        # 国际基准值 (kg CO2-eq/MWh)
        benchmarks = {
            'global_average': 475,
            'eu_average': 275,
            'us_average': 400,
            'china_average': 580,
            'renewable_ideal': 50
        }
        
        comparison = {}
        for benchmark_name, benchmark_value in benchmarks.items():
            comparison[benchmark_name] = current_emissions_intensity / benchmark_value
        
        return comparison
    
    def _identify_improvement_potential(self) -> Dict[str, float]:
        """识别改进潜力"""
        current_emissions_intensity = self._calculate_emissions()['emissions_intensity']
        
        # 计算减排潜力
        potential_reduction = max(0, current_emissions_intensity - 200)  # 目标强度200 kg/MWh
        reduction_percentage = potential_reduction / current_emissions_intensity if current_emissions_intensity > 0 else 0
        
        # 计算成本效益
        abatement_cost_per_ton = self.carbon_price
        total_abatement_potential = potential_reduction * self._get_total_annual_generation()
        
        return {
            'emission_reduction_potential': potential_reduction,
            'reduction_percentage': reduction_percentage,
            'total_abatement_potential_tons': total_abatement_potential / 1000,
            'estimated_abatement_cost': total_abatement_potential * abatement_cost_per_ton / 1000
        }
    
    def _get_total_annual_generation(self) -> float:
        """获取总年发电量"""
        return sum(env.annual_generation_mwh for env in self.environmental_data.values())
    
    def _calculate_abatement_cost(self, emissions_intensity: float) -> float:
        """计算减排成本"""
        if emissions_intensity <= 200:
            return 0
        
        # 简化的减排成本计算
        excess_emissions = emissions_intensity - 200
        return excess_emissions * self.carbon_price / 1000  # $/tCO2
    
    def _calculate_environmental_benefit_value(self) -> float:
        """计算环境效益价值"""
        renewable_fraction = self._calculate_renewable_fraction()
        total_generation = self._get_total_annual_generation()
        
        # 环境效益估值
        carbon_value = renewable_fraction * total_generation * 0.4 * self.carbon_price / 1000
        health_value = carbon_value * 0.1  # 健康效益
        ecosystem_value = carbon_value * 0.05  # 生态系统效益
        
        return carbon_value + health_value + ecosystem_value
    
    def _generate_policy_recommendations(self) -> List[str]:
        """生成政策建议"""
        recommendations = []
        
        current_intensity = self._calculate_emissions()['emissions_intensity']
        renewable_fraction = self._calculate_renewable_fraction()
        
        if current_intensity > 500:
            recommendations.append("排放强度过高，建议大幅提升清洁能源比例")
        
        if renewable_fraction < 0.3:
            recommendations.append("可再生能源比例偏低，建议增加风光等可再生能源装机")
        
        if current_intensity > 300:
            recommendations.append("实施碳定价机制，提高高碳排放技术的经济成本")
        
        recommendations.append("加强能源效率管理，减少无效能耗")
        recommendations.append("推动储能技术发展，提高可再生能源消纳能力")
        
        return recommendations

class LCACalculator(EnvironmentalEvaluator):
    """生命周期评估计算器"""
    
    def calculate_lca_results(self, system_boundary: str = "cradle_to_gate") -> Dict[str, Any]:
        """计算LCA结果"""
        if system_boundary == "cradle_to_gate":
            return self._cradle_to_gate_analysis()
        elif system_boundary == "cradle_to_grave":
            return self._cradle_to_grave_analysis()
        elif system_boundary == "cradle_to_cradle":
            return self._cradle_to_cradle_analysis()
        else:
            raise ValueError(f"未知的系统边界: {system_boundary}")
    
    def _cradle_to_gate_analysis(self) -> Dict[str, Any]:
        """从摇篮到大门分析"""
        manufacturing_emissions = self._sum_lifecycle_phase('manufacturing')
        construction_emissions = self._sum_lifecycle_phase('construction')
        
        return {
            'total_emissions': manufacturing_emissions,
            'construction_emissions': construction_emissions,
            'boundary': 'cradle_to_gate'
        }
    
    def _cradle_to_grave_analysis(self) -> Dict[str, Any]:
        """从摇篮到坟墓分析"""
        return {
            'manufacturing_emissions': self._sum_lifecycle_phase('manufacturing'),
            'construction_emissions': self._sum_lifecycle_phase('construction'),
            'operation_emissions': self._sum_lifecycle_phase('operation'),
            'decommission_emissions': self._sum_lifecycle_phase('decommission'),
            'boundary': 'cradle_to_grave'
        }
    
    def _cradle_to_cradle_analysis(self) -> Dict[str, Any]:
        """从摇篮到摇篮分析"""
        cradle_to_grave = self._cradle_to_grave_analysis()
        recycling_benefits = self._calculate_recycling_benefits()
        
        cradle_to_grave.update({
            'recycling_benefits': recycling_benefits,
            'net_emissions': self._calculate_net_emissions(recycling_benefits),
            'boundary': 'cradle_to_cradle'
        })
        
        return cradle_to_grave
    
    def _sum_lifecycle_phase(self, phase: str) -> Dict[PollutantType, float]:
        """汇总生命周期阶段排放"""
        phase_emissions = {pollutant: 0.0 for pollutant in PollutantType}
        
        for lca_data in self.lifecycle_data.values():
            if phase == 'manufacturing':
                emissions = lca_data.manufacturing_emissions
            elif phase == 'construction':
                emissions = lca_data.construction_emissions
            elif phase == 'operation':
                emissions = lca_data.operation_emissions
            elif phase == 'decommission':
                emissions = lca_data.decommission_emissions
            else:
                continue
            
            for pollutant, amount in emissions.items():
                phase_emissions[pollutant] += amount
        
        return phase_emissions
    
    def _calculate_recycling_benefits(self) -> Dict[str, float]:
        """计算回收效益"""
        # 简化计算
        total_generation = self._get_total_annual_generation()
        recycling_rate = 0.7  # 假设回收率70%
        
        benefits = {
            'material_savings': total_generation * 0.1 * recycling_rate,  # 节省材料
            'energy_savings': total_generation * 0.05 * recycling_rate,   # 节省能源
            'emission_reduction': total_generation * 0.02 * recycling_rate  # 减排
        }
        
        return benefits
    
    def _calculate_net_emissions(self, recycling_benefits: Dict[str, float]) -> Dict[PollutantType, float]:
        """计算净排放"""
        cradle_to_grave = self._cradle_to_grave_analysis()
        
        # 简化：假设回收效益主要减少CO2排放
        co2_reduction = recycling_benefits.get('emission_reduction', 0)
        
        total_co2 = (cradle_to_grave['manufacturing_emissions'].get(PollutantType.CO2, 0) +
                    cradle_to_grave['operation_emissions'].get(PollutantType.CO2, 0))
        
        net_co2 = max(0, total_co2 - co2_reduction)
        
        return {PollutantType.CO2: net_co2}

class CarbonFootprintAnalyzer(EnvironmentalEvaluator):
    """碳足迹分析器"""
    
    def analyze_carbon_footprint(self, scope: str = "full") -> Dict[str, Any]:
        """分析碳足迹"""
        if scope == "scope1":
            return self._analyze_scope1()
        elif scope == "scope2":
            return self._analyze_scope2()
        elif scope == "scope3":
            return self._analyze_scope3()
        elif scope == "full":
            return self._analyze_full_scope()
        else:
            raise ValueError(f"未知的范围: {scope}")
    
    def _analyze_scope1(self) -> Dict[str, Any]:
        """分析范围1排放（直接排放）"""
        scope1_emissions = 0
        
        for env_data in self.environmental_data.values():
            for pollutant, factor in env_data.emission_factors.items():
                if pollutant == PollutantType.CO2:
                    emissions = env_data.annual_generation_mwh * factor.factor_value
                    scope1_emissions += emissions
                    break
        
        return {
            'scope': 'scope1',
            'total_emissions': scope1_emissions,
            'main_sources': [comp_id for comp_id, data in self.environmental_data.items()
                           if any(factor.pollutant_type == PollutantType.CO2 for factor in data.emission_factors.values())],
            'reduction_potential': scope1_emissions * 0.5  # 假设50%减排潜力
        }
    
    def _analyze_scope2(self) -> Dict[str, Any]:
        """分析范围2排放（电力消费）"""
        # 简化：假设电力消费相关的间接排放
        scope2_emissions = self._get_total_annual_generation() * 0.1  # 假设电力消费系数
        
        return {
            'scope': 'scope2',
            'total_emissions': scope2_emissions,
            'main_sources': ['auxiliary_power', 'grid_losses'],
            'reduction_potential': scope2_emissions * 0.3
        }
    
    def _analyze_scope3(self) -> Dict[str, Any]:
        """分析范围3排放（其他间接排放）"""
        # 包括设备制造、运输、燃料生产等
        manufacturing_emissions = self._calculate_manufacturing_footprint()
        
        return {
            'scope': 'scope3',
            'total_emissions': manufacturing_emissions,
            'main_sources': ['equipment_manufacturing', 'fuel_production', 'transport'],
            'reduction_potential': manufacturing_emissions * 0.2
        }
    
    def _analyze_full_scope(self) -> Dict[str, Any]:
        """分析完整范围"""
        scope1 = self._analyze_scope1()
        scope2 = self._analyze_scope2()
        scope3 = self._analyze_scope3()
        
        total_emissions = (scope1['total_emissions'] + 
                          scope2['total_emissions'] + 
                          scope3['total_emissions'])
        
        return {
            'scope': 'full',
            'total_emissions': total_emissions,
            'scope_breakdown': {
                'scope1': scope1['total_emissions'],
                'scope2': scope2['total_emissions'],
                'scope3': scope3['total_emissions']
            },
            'main_emission_sources': list(self.environmental_data.keys()),
            'reduction_potential': total_emissions * 0.4
        }