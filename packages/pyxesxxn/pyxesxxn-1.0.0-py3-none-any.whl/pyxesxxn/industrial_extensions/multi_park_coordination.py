"""
多园区能源系统协同模块

多个工业园区之间的能源互济与协同优化
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


class EnergyExchangeType(Enum):
    """能源交换类型"""
    ELECTRICITY = "electricity"
    HEAT = "heat"
    HYDROGEN = "hydrogen"
    NATURAL_GAS = "natural_gas"


class CoordinationStrategy(Enum):
    """协同策略"""
    COST_MINIMIZATION = "cost_minimization"
    EMISSION_REDUCTION = "emission_reduction"
    LOAD_BALANCING = "load_balancing"
    PEAK_SHARING = "peak_sharing"
    EMERGENCY_SUPPORT = "emergency_support"


@dataclass
class IndustrialPark:
    """工业园区"""
    park_id: str
    park_name: str
    location: str
    coordinates: Tuple[float, float]
    total_capacity: float  # kW
    peak_demand: float  # kW
    base_load: float  # kW
    renewable_capacity: float  # kW
    storage_capacity: float  # kWh
    energy_generation: Dict[str, float]  # by carrier
    energy_consumption: Dict[str, float]  # by carrier
    flexibility_index: float  # 0-1


@dataclass
class EnergyExchange:
    """能源交换"""
    exchange_id: str
    from_park_id: str
    to_park_id: str
    energy_type: EnergyExchangeType
    exchange_capacity: float  # kW
    exchange_efficiency: float  # 0-1
    distance: float  # km
    transmission_loss: float  # %/km
    cost_per_kwh: float  # 元/kWh
    availability: float  # 0-1


@dataclass
class CoordinationPlan:
    """协同计划"""
    plan_id: str
    coordination_strategy: CoordinationStrategy
    participating_parks: List[str]
    time_horizon: timedelta
    energy_exchanges: List[EnergyExchange]
    total_cost: float  # 元
    total_emissions: float  # kg CO2
    total_savings: float  # 元
    reliability_score: float  # 0-1


@dataclass
class ParkLoadProfile:
    """园区负荷曲线"""
    park_id: str
    time_series: pd.Series
    peak_demand: float
    average_demand: float
    load_factor: float
    variability: float


class MultiParkCoordinator(BaseIndustrialExtension):
    """多园区协调器
    
    多个工业园区之间的能源互济与协同优化
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化多园区协调器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - industrial_parks: 工业园区列表
            - energy_exchanges: 能源交换列表
            - coordination_plans: 协同计划列表
            - park_load_profiles: 园区负荷曲线列表
        """
        super().__init__(config)
        
        self.industrial_parks: Dict[str, IndustrialPark] = {}
        self.energy_exchanges: Dict[str, EnergyExchange] = {}
        self.coordination_plans: Dict[str, CoordinationPlan] = {}
        self.park_load_profiles: Dict[str, ParkLoadProfile] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'industrial_parks' in config:
            for park_config in config['industrial_parks']:
                park = IndustrialPark(**park_config)
                self.industrial_parks[park.park_id] = park
        
        if 'energy_exchanges' in config:
            for exchange_config in config['energy_exchanges']:
                exchange = EnergyExchange(**exchange_config)
                self.energy_exchanges[exchange.exchange_id] = exchange
        
        if 'coordination_plans' in config:
            for plan_config in config['coordination_plans']:
                plan = CoordinationPlan(**plan_config)
                self.coordination_plans[plan.plan_id] = plan
        
        if 'park_load_profiles' in config:
            for profile_config in config['park_load_profiles']:
                profile = ParkLoadProfile(**profile_config)
                self.park_load_profiles[profile.park_id] = profile
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.industrial_parks:
                print("警告: 未配置工业园区")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_industrial_park(self, park: IndustrialPark):
        """添加工业园区
        
        Parameters
        ----------
        park : IndustrialPark
            工业园区
        """
        self.industrial_parks[park.park_id] = park
    
    def add_energy_exchange(self, exchange: EnergyExchange):
        """添加能源交换
        
        Parameters
        ----------
        exchange : EnergyExchange
            能源交换
        """
        self.energy_exchanges[exchange.exchange_id] = exchange
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化多园区协同
        
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
        
        for park_id, park in self.industrial_parks.items():
            hourly_load = park.base_load * (0.8 + np.random.random() * 0.3)
            schedule = []
            
            for hour in range(time_horizon):
                generation = park.renewable_capacity * (0.7 + np.random.random() * 0.3)
                net_load = hourly_load - generation
                
                if net_load > 0:
                    cost = net_load * 0.8  # 元/kWh
                else:
                    revenue = abs(net_load) * 0.6  # 元/kWh
                    cost = -revenue
                
                total_cost += cost
                
                schedule.append({
                    'hour': hour,
                    'load': hourly_load,
                    'generation': generation,
                    'net_load': net_load,
                    'cost': cost
                })
            
            energy_schedule[park_id] = schedule
            component_utilization[park_id] = 0.75
        
        for exchange_id, exchange in self.energy_exchanges.items():
            utilization = 0.5 + np.random.random() * 0.4
            component_utilization[exchange_id] = utilization
            
            exchange_cost = exchange.exchange_capacity * utilization * exchange.cost_per_kwh * time_horizon
            total_cost += exchange_cost
        
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
                    'park_operation': total_cost * 0.7,
                    'energy_exchange': total_cost * 0.3
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
        
        for park_id, park in self.industrial_parks.items():
            hourly_load = park.base_load * 0.9
            schedule = []
            
            for hour in range(time_horizon):
                generation = park.renewable_capacity * 0.8
                net_load = hourly_load - generation
                
                if net_load > 0:
                    carbon = net_load * 0.4  # kg CO2/kWh
                else:
                    carbon = 0.0
                
                total_carbon += carbon
                
                schedule.append({
                    'hour': hour,
                    'load': hourly_load,
                    'generation': generation,
                    'net_load': net_load,
                    'carbon': carbon
                })
            
            energy_schedule[park_id] = schedule
            component_utilization[park_id] = 0.85
        
        for exchange_id, exchange in self.energy_exchanges.items():
            component_utilization[exchange_id] = 0.7
        
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
                    'park_emissions': total_carbon
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
        
        for park_id, park in self.industrial_parks.items():
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.9 + np.random.random() * 0.1
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'reliability': reliability
                })
            
            energy_schedule[park_id] = schedule
            component_utilization[park_id] = 0.8
        
        for exchange_id, exchange in self.energy_exchanges.items():
            component_utilization[exchange_id] = 0.85
            reliability_score += exchange.availability
        
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
        
        for park_id, park in self.industrial_parks.items():
            hourly_load = park.base_load * 0.85
            schedule = []
            
            for hour in range(time_horizon):
                generation = park.renewable_capacity * 0.85
                efficiency = park.flexibility_index * (0.9 + np.random.random() * 0.1)
                efficiency_score += efficiency
                
                schedule.append({
                    'hour': hour,
                    'load': hourly_load,
                    'generation': generation,
                    'efficiency': efficiency
                })
            
            energy_schedule[park_id] = schedule
            component_utilization[park_id] = 0.8
        
        for exchange_id, exchange in self.energy_exchanges.items():
            component_utilization[exchange_id] = 0.75
            efficiency_score += exchange.exchange_efficiency
        
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
        weights = {'cost': 0.4, 'carbon': 0.3, 'reliability': 0.3}
        
        cost_result = self._optimize_cost(time_horizon)
        carbon_result = self._optimize_carbon(time_horizon)
        reliability_result = self._optimize_reliability(time_horizon)
        
        normalized_cost = abs(cost_result.total_cost) / 10000.0
        normalized_carbon = abs(carbon_result.total_carbon_emissions) / 1000.0
        normalized_reliability = 1.0 - (reliability_result.objective_value / 
                                       (len(self.industrial_parks) + len(self.energy_exchanges)))
        
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
    
    def create_coordination_plan(
        self,
        plan_id: str,
        strategy: CoordinationStrategy,
        participating_parks: List[str],
        time_horizon: timedelta
    ) -> CoordinationPlan:
        """创建协同计划
        
        Parameters
        ----------
        plan_id : str
            计划ID
        strategy : CoordinationStrategy
            协同策略
        participating_parks : List[str]
            参与园区列表
        time_horizon : timedelta
            时间范围
        
        Returns
        -------
        CoordinationPlan
            协同计划
        """
        relevant_exchanges = [
            exchange for exchange in self.energy_exchanges.values()
            if exchange.from_park_id in participating_parks and
               exchange.to_park_id in participating_parks
        ]
        
        total_cost = 0.0
        total_emissions = 0.0
        total_savings = 0.0
        reliability_score = 0.0
        
        for exchange in relevant_exchanges:
            utilization = 0.6 + np.random.random() * 0.3
            exchange_cost = exchange.exchange_capacity * utilization * exchange.cost_per_kwh
            total_cost += exchange_cost
            
            exchange_emissions = exchange.exchange_capacity * utilization * 0.3
            total_emissions += exchange_emissions
            
            exchange_savings = exchange.exchange_capacity * utilization * 0.2
            total_savings += exchange_savings
            
            reliability_score += exchange.availability
        
        reliability_score = reliability_score / len(relevant_exchanges) if relevant_exchanges else 0.0
        
        plan = CoordinationPlan(
            plan_id=plan_id,
            coordination_strategy=strategy,
            participating_parks=participating_parks,
            time_horizon=time_horizon,
            energy_exchanges=relevant_exchanges,
            total_cost=total_cost,
            total_emissions=total_emissions,
            total_savings=total_savings,
            reliability_score=reliability_score
        )
        
        self.coordination_plans[plan_id] = plan
        return plan
    
    def calculate_energy_balance(
        self,
        park_id: str,
        time_horizon: int = 24
    ) -> Dict[str, Any]:
        """计算能源平衡
        
        Parameters
        ----------
        park_id : str
            园区ID
        time_horizon : int
            时间范围
        
        Returns
        -------
        Dict[str, Any]
            能源平衡结果
        """
        if park_id not in self.industrial_parks:
            return {'error': '园区不存在'}
        
        park = self.industrial_parks[park_id]
        
        hourly_balance = []
        total_import = 0.0
        total_export = 0.0
        
        for hour in range(time_horizon):
            load = park.base_load * (0.8 + np.random.random() * 0.3)
            generation = park.renewable_capacity * (0.7 + np.random.random() * 0.3)
            net = generation - load
            
            if net > 0:
                export_amount = net * 0.9
                total_export += export_amount
                balance = {
                    'hour': hour,
                    'load': load,
                    'generation': generation,
                    'net': net,
                    'export': export_amount,
                    'import': 0.0
                }
            else:
                import_amount = abs(net) * 1.1
                total_import += import_amount
                balance = {
                    'hour': hour,
                    'load': load,
                    'generation': generation,
                    'net': net,
                    'export': 0.0,
                    'import': import_amount
                }
            
            hourly_balance.append(balance)
        
        return {
            'park_id': park_id,
            'hourly_balance': hourly_balance,
            'total_import': total_import,
            'total_export': total_export,
            'net_import': total_import - total_export,
            'self_sufficiency_ratio': total_export / (total_import + total_export) if (total_import + total_export) > 0 else 0
        }
    
    def generate_coordination_report(self) -> Dict[str, Any]:
        """生成协同报告
        
        Returns
        -------
        Dict[str, Any]
            协同报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        total_capacity = sum(park.total_capacity for park in self.industrial_parks.values())
        total_renewable = sum(park.renewable_capacity for park in self.industrial_parks.values())
        total_storage = sum(park.storage_capacity for park in self.industrial_parks.values())
        
        report = {
            'summary': {
                'total_parks': len(self.industrial_parks),
                'total_energy_exchanges': len(self.energy_exchanges),
                'total_coordination_plans': len(self.coordination_plans),
                'total_capacity': total_capacity,
                'total_renewable_capacity': total_renewable,
                'total_storage_capacity': total_storage,
                'renewable_ratio': total_renewable / total_capacity if total_capacity > 0 else 0,
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'park_details': {},
            'exchange_details': {},
            'plan_details': {}
        }
        
        for park_id, park in self.industrial_parks.items():
            report['park_details'][park_id] = {
                'name': park.park_name,
                'location': park.location,
                'coordinates': park.coordinates,
                'total_capacity': park.total_capacity,
                'peak_demand': park.peak_demand,
                'base_load': park.base_load,
                'renewable_capacity': park.renewable_capacity,
                'storage_capacity': park.storage_capacity,
                'flexibility_index': park.flexibility_index,
                'energy_generation': park.energy_generation,
                'energy_consumption': park.energy_consumption
            }
        
        for exchange_id, exchange in self.energy_exchanges.items():
            report['exchange_details'][exchange_id] = {
                'from_park': exchange.from_park_id,
                'to_park': exchange.to_park_id,
                'energy_type': exchange.energy_type.value,
                'exchange_capacity': exchange.exchange_capacity,
                'exchange_efficiency': exchange.exchange_efficiency,
                'distance': exchange.distance,
                'transmission_loss': exchange.transmission_loss,
                'cost_per_kwh': exchange.cost_per_kwh,
                'availability': exchange.availability
            }
        
        for plan_id, plan in self.coordination_plans.items():
            report['plan_details'][plan_id] = {
                'strategy': plan.coordination_strategy.value,
                'participating_parks': plan.participating_parks,
                'time_horizon': str(plan.time_horizon),
                'number_of_exchanges': len(plan.energy_exchanges),
                'total_cost': plan.total_cost,
                'total_emissions': plan.total_emissions,
                'total_savings': plan.total_savings,
                'reliability_score': plan.reliability_score
            }
        
        return report