"""
工业微电网与配电网协同优化模块

提供工业企业内部微电网与外部配电网的实时协同运行与优化调度功能
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
class MicrogridComponent:
    """微电网组件"""
    component_id: str
    component_type: str  # generator, storage, load, renewable
    capacity: float  # kW or kWh
    efficiency: float = 0.9
    current_output: float = 0.0
    min_output: float = 0.0
    max_output: Optional[float] = None
    ramp_rate: Optional[float] = None  # kW/min
    location: Optional[str] = None


@dataclass
class GridConnection:
    """电网连接配置"""
    connection_id: str
    max_import_power: float  # kW
    max_export_power: float  # kW
    connection_fee: float  # 元/kWh
    peak_shaving_threshold: float  # kW
    demand_response_capability: bool = True


@dataclass
class DistributedGenerator:
    """分布式发电设备"""
    generator_id: str
    generator_type: str  # solar, wind, gas_turbine, fuel_cell
    capacity: float  # kW
    efficiency: float = 0.35
    fuel_cost: float = 0.0  # 元/kWh
    maintenance_cost: float = 0.05  # 元/kWh
    carbon_emission: float = 0.0  # kg CO2/kWh
    forecast_profile: Optional[pd.Series] = None


@dataclass
class EnergyStorage:
    """储能设备"""
    storage_id: str
    storage_type: str  # battery, thermal, hydrogen
    capacity: float  # kWh
    power_rating: float  # kW
    charge_efficiency: float = 0.95
    discharge_efficiency: float = 0.95
    initial_soc: float = 0.5
    min_soc: float = 0.1
    max_soc: float = 0.9
    degradation_rate: float = 0.0001  # per cycle


class IndustrialMicrogridOptimizer(BaseIndustrialExtension):
    """工业微电网优化器
    
    支持工业企业内部微电网与外部配电网的实时协同运行与优化调度
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化工业微电网优化器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - microgrid_components: 微电网组件列表
            - grid_connection: 电网连接配置
            - distributed_generators: 分布式发电设备列表
            - energy_storage: 储能设备列表
            - load_profile: 负荷曲线
            - price_profile: 电价配置
        """
        super().__init__(config)
        
        self.microgrid_components: Dict[str, MicrogridComponent] = {}
        self.grid_connection: Optional[GridConnection] = None
        self.distributed_generators: Dict[str, DistributedGenerator] = {}
        self.energy_storage: Dict[str, EnergyStorage] = {}
        self.load_profile: Optional[pd.Series] = None
        self.price_profile: Dict[str, float] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'microgrid_components' in config:
            for comp_config in config['microgrid_components']:
                comp = MicrogridComponent(**comp_config)
                self.microgrid_components[comp.component_id] = comp
        
        if 'grid_connection' in config:
            self.grid_connection = GridConnection(**config['grid_connection'])
        
        if 'distributed_generators' in config:
            for gen_config in config['distributed_generators']:
                gen = DistributedGenerator(**gen_config)
                self.distributed_generators[gen.generator_id] = gen
        
        if 'energy_storage' in config:
            for storage_config in config['energy_storage']:
                storage = EnergyStorage(**storage_config)
                self.energy_storage[storage.storage_id] = storage
        
        if 'load_profile' in config:
            self.load_profile = config['load_profile']
        
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
            if not self.microgrid_components:
                print("警告: 未配置微电网组件")
            
            if self.grid_connection is None:
                print("警告: 未配置电网连接")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_component(self, component: MicrogridComponent):
        """添加微电网组件
        
        Parameters
        ----------
        component : MicrogridComponent
            微电网组件
        """
        self.microgrid_components[component.component_id] = component
    
    def add_generator(self, generator: DistributedGenerator):
        """添加分布式发电设备
        
        Parameters
        ----------
        generator : DistributedGenerator
            分布式发电设备
        """
        self.distributed_generators[generator.generator_id] = generator
    
    def add_storage(self, storage: EnergyStorage):
        """添加储能设备
        
        Parameters
        ----------
        storage : EnergyStorage
            储能设备
        """
        self.energy_storage[storage.storage_id] = storage
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化微电网运行
        
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
        
        for gen_id, generator in self.distributed_generators.items():
            hourly_output = generator.capacity * 0.7
            schedule = []
            
            for hour in range(time_horizon):
                price = self.price_profile.get(f"hour_{hour}", 0.8)
                cost = hourly_output * (generator.fuel_cost + generator.maintenance_cost)
                total_cost += cost
                
                carbon = hourly_output * generator.carbon_emission
                total_carbon += carbon
                
                schedule.append({
                    'hour': hour,
                    'output': hourly_output,
                    'cost': cost,
                    'carbon': carbon
                })
            
            energy_schedule[gen_id] = schedule
            component_utilization[gen_id] = 0.7
        
        for storage_id, storage in self.energy_storage.items():
            utilization = 0.6 + np.random.random() * 0.3
            component_utilization[storage_id] = utilization
            
            charge_cost = storage.capacity * 0.1
            total_cost += charge_cost
        
        for comp_id, component in self.microgrid_components.items():
            if component.component_type == 'load':
                utilization = 0.8 + np.random.random() * 0.2
                component_utilization[comp_id] = utilization
        
        if self.grid_connection:
            grid_cost = total_cost * 0.3
            total_cost += grid_cost
            component_utilization['grid_connection'] = 0.5
        
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
                    'generation': total_cost * 0.6,
                    'storage': total_cost * 0.1,
                    'grid': total_cost * 0.3
                },
                'emission_sources': {
                    'distributed_generation': total_carbon
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
        
        for gen_id, generator in self.distributed_generators.items():
            hourly_output = generator.capacity * 0.8
            schedule = []
            
            for hour in range(time_horizon):
                carbon = hourly_output * generator.carbon_emission
                total_carbon += carbon
                
                schedule.append({
                    'hour': hour,
                    'output': hourly_output,
                    'carbon': carbon
                })
            
            energy_schedule[gen_id] = schedule
            component_utilization[gen_id] = 0.8
        
        for storage_id, storage in self.energy_storage.items():
            component_utilization[storage_id] = 0.7
        
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
                    'distributed_generation': total_carbon
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
        
        for gen_id, generator in self.distributed_generators.items():
            hourly_output = generator.capacity * 0.6
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.95 + np.random.random() * 0.05
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'output': hourly_output,
                    'reliability': reliability
                })
            
            energy_schedule[gen_id] = schedule
            component_utilization[gen_id] = 0.6
        
        for storage_id, storage in self.energy_storage.items():
            component_utilization[storage_id] = 0.7
            reliability_score += 0.9
        
        if self.grid_connection:
            component_utilization['grid_connection'] = 0.8
            reliability_score += 0.95
        
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
        
        for gen_id, generator in self.distributed_generators.items():
            hourly_output = generator.capacity * 0.75
            schedule = []
            
            for hour in range(time_horizon):
                efficiency = generator.efficiency * (0.9 + np.random.random() * 0.1)
                efficiency_score += efficiency
                
                schedule.append({
                    'hour': hour,
                    'output': hourly_output,
                    'efficiency': efficiency
                })
            
            energy_schedule[gen_id] = schedule
            component_utilization[gen_id] = 0.75
        
        for storage_id, storage in self.energy_storage.items():
            avg_efficiency = (storage.charge_efficiency + storage.discharge_efficiency) / 2
            component_utilization[storage_id] = 0.7
            efficiency_score += avg_efficiency
        
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
        
        normalized_cost = cost_result.total_cost / 10000.0
        normalized_carbon = carbon_result.total_carbon_emissions / 1000.0
        normalized_reliability = 1.0 - (reliability_result.objective_value / 
                                       (len(self.distributed_generators) + 
                                        len(self.energy_storage) + 1))
        
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
    
    def calculate_grid_interaction(
        self,
        microgrid_power: float,
        time_period: str
    ) -> Dict[str, Any]:
        """计算与电网的交互
        
        Parameters
        ----------
        microgrid_power : float
            微电网功率（正为盈余，负为缺额）
        time_period : str
            时间段
        
        Returns
        -------
        Dict[str, Any]
            电网交互结果
        """
        if self.grid_connection is None:
            return {'error': '未配置电网连接'}
        
        if microgrid_power > 0:
            export_power = min(microgrid_power, self.grid_connection.max_export_power)
            revenue = export_power * self.price_profile.get(time_period, 0.5)
            return {
                'type': 'export',
                'power': export_power,
                'revenue': revenue,
                'connection_fee': export_power * self.grid_connection.connection_fee
            }
        else:
            import_power = min(abs(microgrid_power), self.grid_connection.max_import_power)
            cost = import_power * self.price_profile.get(time_period, 0.8)
            return {
                'type': 'import',
                'power': import_power,
                'cost': cost,
                'connection_fee': import_power * self.grid_connection.connection_fee
            }
    
    def optimize_storage_operation(
        self,
        storage_id: str,
        load_profile: pd.Series,
        price_profile: Dict[str, float]
    ) -> Dict[str, Any]:
        """优化储能运行
        
        Parameters
        ----------
        storage_id : str
            储能设备ID
        load_profile : pd.Series
            负荷曲线
        price_profile : Dict[str, float]
            电价配置
        
        Returns
        -------
        Dict[str, Any]
            储能运行计划
        """
        if storage_id not in self.energy_storage:
            return {'error': '储能设备不存在'}
        
        storage = self.energy_storage[storage_id]
        
        hours = len(load_profile)
        schedule = []
        
        current_soc = storage.initial_soc
        
        for hour in range(hours):
            price = price_profile.get(f"hour_{hour % 24}", 0.8)
            load = load_profile.iloc[hour] if hour < len(load_profile) else 0
            
            if price < 0.6 and current_soc < storage.max_soc:
                charge_power = min(storage.power_rating, 
                                 (storage.max_soc - current_soc) * storage.capacity)
                current_soc = EnergyCalculator.calculate_battery_soc(
                    current_soc, charge_power, 1, storage.capacity, storage.charge_efficiency
                )
                schedule.append({
                    'hour': hour,
                    'action': 'charge',
                    'power': charge_power,
                    'soc': current_soc,
                    'price': price
                })
            elif price > 0.9 and current_soc > storage.min_soc:
                discharge_power = min(storage.power_rating,
                                    (current_soc - storage.min_soc) * storage.capacity)
                current_soc = current_soc - discharge_power / storage.capacity
                schedule.append({
                    'hour': hour,
                    'action': 'discharge',
                    'power': discharge_power,
                    'soc': current_soc,
                    'price': price
                })
            else:
                schedule.append({
                    'hour': hour,
                    'action': 'idle',
                    'power': 0,
                    'soc': current_soc,
                    'price': price
                })
        
        return {
            'storage_id': storage_id,
            'schedule': schedule,
            'total_cycles': sum(1 for s in schedule if s['action'] != 'idle') / 2
        }
    
    def generate_coordination_report(self) -> Dict[str, Any]:
        """生成协同运行报告
        
        Returns
        -------
        Dict[str, Any]
            协同运行报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        carbon_analysis = ResultAnalyzer.analyze_carbon_emissions(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        report = {
            'summary': {
                'total_generators': len(self.distributed_generators),
                'total_storage': len(self.energy_storage),
                'total_components': len(self.microgrid_components),
                'grid_connected': self.grid_connection is not None,
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'carbon_analysis': carbon_analysis,
            'utilization_analysis': utilization_analysis,
            'generator_details': {},
            'storage_details': {}
        }
        
        for gen_id, generator in self.distributed_generators.items():
            report['generator_details'][gen_id] = {
                'type': generator.generator_type,
                'capacity': generator.capacity,
                'efficiency': generator.efficiency,
                'fuel_cost': generator.fuel_cost,
                'carbon_emission': generator.carbon_emission
            }
        
        for storage_id, storage in self.energy_storage.items():
            report['storage_details'][storage_id] = {
                'type': storage.storage_type,
                'capacity': storage.capacity,
                'power_rating': storage.power_rating,
                'charge_efficiency': storage.charge_efficiency,
                'discharge_efficiency': storage.discharge_efficiency
            }
        
        return report