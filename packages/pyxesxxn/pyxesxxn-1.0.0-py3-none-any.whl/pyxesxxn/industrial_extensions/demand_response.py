"""
需求侧响应与虚拟电厂集成模块

提供工业负荷的需求响应能力评估、聚合与虚拟电厂参与机制
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from .base import (
    BaseIndustrialExtension,
    OptimizationObjective,
    OptimizationResult,
    EnergyCalculator,
    TimeSeriesGenerator,
    ResultAnalyzer
)


@dataclass
class FlexibleLoad:
    """可调节负荷"""
    load_id: str
    load_type: str  # industrial, commercial, residential
    base_power: float  # kW
    flexibility: float  # 可调节比例 (0-1)
    response_time: float  # 响应时间 (分钟)
    max_reduction: float  # 最大削减功率 (kW)
    max_increase: float  # 最大增加功率 (kW)
    priority: int  # 优先级 (1-5, 1为最高)
    location: Optional[str] = None
    participation_rate: float = 0.8  # 参与率


@dataclass
class DistributedResource:
    """分布式资源"""
    resource_id: str
    resource_type: str  # solar, wind, storage, ev_charging
    capacity: float  # kW
    availability: float  # 可用性 (0-1)
    response_time: float  # 响应时间 (分钟)
    location: Optional[str] = None


@dataclass
class DemandResponseEvent:
    """需求响应事件"""
    event_id: str
    start_time: str
    end_time: str
    event_type: str  # peak_shaving, load_shifting, emergency
    target_reduction: float  # 目标削减量 (kW)
    price_signal: float  # 价格信号 (元/kWh)
    notification_time: int  # 提前通知时间 (分钟)


@dataclass
class VirtualPowerPlant:
    """虚拟电厂"""
    vpp_id: str
    name: str
    total_capacity: float  # kW
    flexible_loads: Dict[str, FlexibleLoad] = field(default_factory=dict)
    distributed_resources: Dict[str, DistributedResource] = field(default_factory=dict)
    aggregation_capability: float = 0.9  # 聚合能力
    market_participation: bool = True


class DemandResponseManager(BaseIndustrialExtension):
    """需求响应管理器
    
    提供工业负荷的需求响应能力评估、聚合与虚拟电厂参与机制
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化需求响应管理器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - flexible_loads: 可调节负荷列表
            - distributed_resources: 分布式资源列表
            - virtual_power_plants: 虚拟电厂列表
            - demand_response_events: 需求响应事件列表
            - price_profile: 价格配置
        """
        super().__init__(config)
        
        self.flexible_loads: Dict[str, FlexibleLoad] = {}
        self.distributed_resources: Dict[str, DistributedResource] = {}
        self.virtual_power_plants: Dict[str, VirtualPowerPlant] = {}
        self.demand_response_events: List[DemandResponseEvent] = []
        self.price_profile: Dict[str, float] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'flexible_loads' in config:
            for load_config in config['flexible_loads']:
                load = FlexibleLoad(**load_config)
                self.flexible_loads[load.load_id] = load
        
        if 'distributed_resources' in config:
            for resource_config in config['distributed_resources']:
                resource = DistributedResource(**resource_config)
                self.distributed_resources[resource.resource_id] = resource
        
        if 'virtual_power_plants' in config:
            for vpp_config in config['virtual_power_plants']:
                vpp = VirtualPowerPlant(**vpp_config)
                self.virtual_power_plants[vpp.vpp_id] = vpp
        
        if 'demand_response_events' in config:
            for event_config in config['demand_response_events']:
                event = DemandResponseEvent(**event_config)
                self.demand_response_events.append(event)
        
        if 'price_profile' in config:
            self.price_profile = config['price_profile']
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.flexible_loads:
                print("警告: 未配置可调节负荷")
            
            if not self.distributed_resources:
                print("警告: 未配置分布式资源")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_flexible_load(self, load: FlexibleLoad):
        """添加可调节负荷
        
        Parameters
        ----------
        load : FlexibleLoad
            可调节负荷
        """
        self.flexible_loads[load.load_id] = load
    
    def add_distributed_resource(self, resource: DistributedResource):
        """添加分布式资源
        
        Parameters
        ----------
        resource : DistributedResource
            分布式资源
        """
        self.distributed_resources[resource.resource_id] = resource
    
    def add_virtual_power_plant(self, vpp: VirtualPowerPlant):
        """添加虚拟电厂
        
        Parameters
        ----------
        vpp : VirtualPowerPlant
            虚拟电厂
        """
        self.virtual_power_plants[vpp.vpp_id] = vpp
    
    def add_demand_response_event(self, event: DemandResponseEvent):
        """添加需求响应事件
        
        Parameters
        ----------
        event : DemandResponseEvent
            需求响应事件
        """
        self.demand_response_events.append(event)
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化需求响应
        
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
        
        for load_id, load in self.flexible_loads.items():
            hourly_reduction = load.max_reduction * load.flexibility * load.participation_rate
            schedule = []
            
            for hour in range(time_horizon):
                price = self.price_profile.get(f"hour_{hour}", 0.8)
                
                if price > 1.0:
                    reduction = hourly_reduction
                    revenue = reduction * price * 0.5
                    total_cost -= revenue
                else:
                    reduction = 0
                    revenue = 0
                
                schedule.append({
                    'hour': hour,
                    'reduction': reduction,
                    'revenue': revenue,
                    'price': price
                })
            
            energy_schedule[load_id] = schedule
            component_utilization[load_id] = 0.7
        
        for resource_id, resource in self.distributed_resources.items():
            utilization = 0.6 + np.random.random() * 0.3
            component_utilization[resource_id] = utilization
            
            output = resource.capacity * utilization * resource.availability
            cost = output * 0.1
            total_cost += cost
        
        for vpp_id, vpp in self.virtual_power_plants.items():
            vpp_utilization = 0.75 + np.random.random() * 0.2
            component_utilization[vpp_id] = vpp_utilization
            
            vpp_output = vpp.total_capacity * vpp_utilization * vpp.aggregation_capability
            revenue = vpp_output * 0.6
            total_cost -= revenue
        
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
                    'load_reduction': -total_cost * 0.6,
                    'resource_output': total_cost * 0.4
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
        
        for load_id, load in self.flexible_loads.items():
            hourly_reduction = load.max_reduction * load.flexibility
            schedule = []
            
            for hour in range(time_horizon):
                carbon_reduction = hourly_reduction * 0.4
                total_carbon -= carbon_reduction
                
                schedule.append({
                    'hour': hour,
                    'reduction': hourly_reduction,
                    'carbon_reduction': carbon_reduction
                })
            
            energy_schedule[load_id] = schedule
            component_utilization[load_id] = 0.8
        
        for resource_id, resource in self.distributed_resources.items():
            component_utilization[resource_id] = 0.7
        
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
                    'load_reduction': total_carbon
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
        
        for load_id, load in self.flexible_loads.items():
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.9 + np.random.random() * 0.1
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'reliability': reliability
                })
            
            energy_schedule[load_id] = schedule
            component_utilization[load_id] = 0.85
        
        for resource_id, resource in self.distributed_resources.items():
            component_utilization[resource_id] = 0.8
            reliability_score += resource.availability
        
        for vpp_id, vpp in self.virtual_power_plants.items():
            component_utilization[vpp_id] = 0.9
            reliability_score += vpp.aggregation_capability
        
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
        
        for load_id, load in self.flexible_loads.items():
            schedule = []
            
            for hour in range(time_horizon):
                efficiency = load.flexibility * (0.9 + np.random.random() * 0.1)
                efficiency_score += efficiency
                
                schedule.append({
                    'hour': hour,
                    'efficiency': efficiency
                })
            
            energy_schedule[load_id] = schedule
            component_utilization[load_id] = 0.75
        
        for resource_id, resource in self.distributed_resources.items():
            component_utilization[resource_id] = 0.7
            efficiency_score += resource.availability
        
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
                                       (len(self.flexible_loads) + 
                                        len(self.distributed_resources) + 
                                        len(self.virtual_power_plants)))
        
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
    
    def assess_demand_response_capability(
        self,
        load_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """评估需求响应能力
        
        Parameters
        ----------
        load_id : str, optional
            负荷ID，如果为None则评估所有负荷
        
        Returns
        -------
        Dict[str, Any]
            需求响应能力评估结果
        """
        if load_id:
            if load_id not in self.flexible_loads:
                return {'error': '负荷不存在'}
            loads_to_assess = {load_id: self.flexible_loads[load_id]}
        else:
            loads_to_assess = self.flexible_loads
        
        assessment = {
            'total_flexible_power': 0.0,
            'total_reduction_capacity': 0.0,
            'total_increase_capacity': 0.0,
            'average_response_time': 0.0,
            'load_details': {}
        }
        
        for lid, load in loads_to_assess.items():
            flexible_power = load.base_power * load.flexibility * load.participation_rate
            assessment['total_flexible_power'] += flexible_power
            assessment['total_reduction_capacity'] += load.max_reduction * load.participation_rate
            assessment['total_increase_capacity'] += load.max_increase * load.participation_rate
            assessment['average_response_time'] += load.response_time
            
            assessment['load_details'][lid] = {
                'base_power': load.base_power,
                'flexibility': load.flexibility,
                'flexible_power': flexible_power,
                'max_reduction': load.max_reduction,
                'max_increase': load.max_increase,
                'response_time': load.response_time,
                'priority': load.priority,
                'participation_rate': load.participation_rate
            }
        
        if loads_to_assess:
            assessment['average_response_time'] /= len(loads_to_assess)
        
        return assessment
    
    def create_virtual_power_plant(
        self,
        vpp_id: str,
        name: str,
        load_ids: List[str],
        resource_ids: List[str]
    ) -> Dict[str, Any]:
        """创建虚拟电厂
        
        Parameters
        ----------
        vpp_id : str
            虚拟电厂ID
        name : str
            虚拟电厂名称
        load_ids : List[str]
            负荷ID列表
        resource_ids : List[str]
            资源ID列表
        
        Returns
        -------
        Dict[str, Any]
            虚拟电厂创建结果
        """
        flexible_loads = {}
        for load_id in load_ids:
            if load_id in self.flexible_loads:
                flexible_loads[load_id] = self.flexible_loads[load_id]
        
        distributed_resources = {}
        for resource_id in resource_ids:
            if resource_id in self.distributed_resources:
                distributed_resources[resource_id] = self.distributed_resources[resource_id]
        
        total_capacity = sum(r.capacity for r in distributed_resources.values())
        
        vpp = VirtualPowerPlant(
            vpp_id=vpp_id,
            name=name,
            total_capacity=total_capacity,
            flexible_loads=flexible_loads,
            distributed_resources=distributed_resources
        )
        
        self.virtual_power_plants[vpp_id] = vpp
        
        return {
            'vpp_id': vpp_id,
            'name': name,
            'total_capacity': total_capacity,
            'number_of_loads': len(flexible_loads),
            'number_of_resources': len(distributed_resources),
            'status': 'created'
        }
    
    def optimize_virtual_power_plant(
        self,
        vpp_id: str,
        time_horizon: int = 24
    ) -> Dict[str, Any]:
        """优化虚拟电厂运行
        
        Parameters
        ----------
        vpp_id : str
            虚拟电厂ID
        time_horizon : int
            时间范围
        
        Returns
        -------
        Dict[str, Any]
            优化结果
        """
        if vpp_id not in self.virtual_power_plants:
            return {'error': '虚拟电厂不存在'}
        
        vpp = self.virtual_power_plants[vpp_id]
        
        schedule = []
        total_output = 0.0
        total_revenue = 0.0
        
        for hour in range(time_horizon):
            price = self.price_profile.get(f"hour_{hour % 24}", 0.8)
            
            resource_output = sum(
                resource.capacity * resource.availability * (0.7 + np.random.random() * 0.3)
                for resource in vpp.distributed_resources.values()
            )
            
            load_reduction = sum(
                load.max_reduction * load.flexibility * load.participation_rate
                for load in vpp.flexible_loads.values()
            ) if price > 1.0 else 0.0
            
            total_output = resource_output + load_reduction
            revenue = total_output * price
            total_revenue += revenue
            
            schedule.append({
                'hour': hour,
                'resource_output': resource_output,
                'load_reduction': load_reduction,
                'total_output': total_output,
                'price': price,
                'revenue': revenue
            })
        
        return {
            'vpp_id': vpp_id,
            'schedule': schedule,
            'total_output': total_output,
            'total_revenue': total_revenue,
            'average_output': total_output / time_horizon if time_horizon > 0 else 0
        }
    
    def generate_demand_response_report(self) -> Dict[str, Any]:
        """生成需求响应报告
        
        Returns
        -------
        Dict[str, Any]
            需求响应报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        carbon_analysis = ResultAnalyzer.analyze_carbon_emissions(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        capability_assessment = self.assess_demand_response_capability()
        
        report = {
            'summary': {
                'total_flexible_loads': len(self.flexible_loads),
                'total_distributed_resources': len(self.distributed_resources),
                'total_virtual_power_plants': len(self.virtual_power_plants),
                'total_flexible_power': capability_assessment['total_flexible_power'],
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'capability_assessment': capability_assessment,
            'cost_analysis': cost_analysis,
            'carbon_analysis': carbon_analysis,
            'utilization_analysis': utilization_analysis,
            'load_details': {},
            'resource_details': {},
            'vpp_details': {}
        }
        
        for load_id, load in self.flexible_loads.items():
            report['load_details'][load_id] = {
                'type': load.load_type,
                'base_power': load.base_power,
                'flexibility': load.flexibility,
                'max_reduction': load.max_reduction,
                'max_increase': load.max_increase,
                'response_time': load.response_time,
                'priority': load.priority,
                'participation_rate': load.participation_rate
            }
        
        for resource_id, resource in self.distributed_resources.items():
            report['resource_details'][resource_id] = {
                'type': resource.resource_type,
                'capacity': resource.capacity,
                'availability': resource.availability,
                'response_time': resource.response_time
            }
        
        for vpp_id, vpp in self.virtual_power_plants.items():
            report['vpp_details'][vpp_id] = {
                'name': vpp.name,
                'total_capacity': vpp.total_capacity,
                'number_of_loads': len(vpp.flexible_loads),
                'number_of_resources': len(vpp.distributed_resources),
                'aggregation_capability': vpp.aggregation_capability,
                'market_participation': vpp.market_participation
            }
        
        return report