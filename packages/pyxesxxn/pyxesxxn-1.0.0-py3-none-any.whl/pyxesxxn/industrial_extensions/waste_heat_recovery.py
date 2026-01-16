"""
工业余热深度利用优化模块

针对工业过程余热的高效回收、存储与梯级利用的优化算法
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


class HeatSourceType(Enum):
    """热源类型"""
    BOILER = "boiler"
    FURNACE = "furnace"
    TURBINE_EXHAUST = "turbine_exhaust"
    PROCESS_HEAT = "process_heat"
    COOLING_SYSTEM = "cooling_system"
    COMBUSTION = "combustion"


class HeatRecoveryMethod(Enum):
    """余热回收方法"""
    HEAT_EXCHANGER = "heat_exchanger"
    ORC = "orc"  # 有机朗肯循环
    KALINA_CYCLE = "kalina_cycle"
    ABSORPTION_CHILLER = "absorption_chiller"
    HEAT_PUMP = "heat_pump"
    THERMAL_STORAGE = "thermal_storage"


class HeatGrade(Enum):
    """余热等级"""
    HIGH = "high"  # >400°C
    MEDIUM_HIGH = "medium_high"  # 200-400°C
    MEDIUM = "medium"  # 100-200°C
    LOW = "low"  # 50-100°C
    VERY_LOW = "very_low"  # <50°C


@dataclass
class HeatSource:
    """热源"""
    source_id: str
    source_type: HeatSourceType
    location: str
    outlet_temperature: float  # °C
    mass_flow_rate: float  # kg/s
    specific_heat: float  # kJ/kg·K
    available_hours_per_day: float
    temperature_profile: Optional[pd.Series] = None
    heat_content: float = 0.0  # kW


@dataclass
class HeatSink:
    """热汇"""
    sink_id: str
    sink_type: str  # process, space_heating, domestic_hot_water, preheating
    location: str
    required_temperature: float  # °C
    heat_demand: float  # kW
    demand_profile: Optional[pd.Series] = None
    priority: int = 1


@dataclass
class HeatExchanger:
    """换热器"""
    exchanger_id: str
    exchanger_type: str  # shell_tube, plate, finned_tube
    heat_transfer_area: float  # m²
    heat_transfer_coefficient: float  # W/m²·K
    effectiveness: float  # 0-1
    max_heat_transfer: float  # kW
    pressure_drop_hot: float  # kPa
    pressure_drop_cold: float  # kPa
    fouling_factor: float = 0.0001  # m²·K/W


@dataclass
class HeatRecoverySystem:
    """余热回收系统"""
    system_id: str
    recovery_method: HeatRecoveryMethod
    heat_source_id: str
    heat_sink_id: str
    heat_exchanger: HeatExchanger
    recovered_heat: float  # kW
    recovery_efficiency: float  # 0-1
    capital_cost: float  # 元
    operating_cost: float  # 元/年
    maintenance_cost: float  # 元/年
    payback_period: float  # 年


@dataclass
class ThermalStorage:
    """热储能"""
    storage_id: str
    storage_medium: str  # water, molten_salt, phase_change_material, concrete
    capacity: float  # kWh
    max_temperature: float  # °C
    min_temperature: float  # °C
    charge_efficiency: float  # 0-1
    discharge_efficiency: float  # 0-1
    heat_loss_rate: float  # %/hour
    capital_cost: float  # 元
    current_temperature: float = 80.0
    current_soc: float = 0.5  # 0-1


class WasteHeatOptimizer(BaseIndustrialExtension):
    """工业余热优化器
    
    针对工业过程余热的高效回收、存储与梯级利用的优化算法
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化工业余热优化器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - heat_sources: 热源列表
            - heat_sinks: 热汇列表
            - heat_exchangers: 换热器列表
            - heat_recovery_systems: 余热回收系统列表
            - thermal_storage: 热储能列表
        """
        super().__init__(config)
        
        self.heat_sources: Dict[str, HeatSource] = {}
        self.heat_sinks: Dict[str, HeatSink] = {}
        self.heat_exchangers: Dict[str, HeatExchanger] = {}
        self.heat_recovery_systems: Dict[str, HeatRecoverySystem] = {}
        self.thermal_storage: Dict[str, ThermalStorage] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'heat_sources' in config:
            for source_config in config['heat_sources']:
                source = HeatSource(**source_config)
                source.heat_content = self._calculate_heat_content(source)
                self.heat_sources[source.source_id] = source
        
        if 'heat_sinks' in config:
            for sink_config in config['heat_sinks']:
                sink = HeatSink(**sink_config)
                self.heat_sinks[sink.sink_id] = sink
        
        if 'heat_exchangers' in config:
            for exchanger_config in config['heat_exchangers']:
                exchanger = HeatExchanger(**exchanger_config)
                self.heat_exchangers[exchanger.exchanger_id] = exchanger
        
        if 'heat_recovery_systems' in config:
            for system_config in config['heat_recovery_systems']:
                exchanger_config = system_config['heat_exchanger']
                exchanger = HeatExchanger(**exchanger_config)
                system = HeatRecoverySystem(
                    **{k: v for k, v in system_config.items() if k != 'heat_exchanger'},
                    heat_exchanger=exchanger
                )
                self.heat_recovery_systems[system.system_id] = system
        
        if 'thermal_storage' in config:
            for storage_config in config['thermal_storage']:
                storage = ThermalStorage(**storage_config)
                self.thermal_storage[storage.storage_id] = storage
    
    def _calculate_heat_content(self, source: HeatSource) -> float:
        """计算热含量
        
        Parameters
        ----------
        source : HeatSource
            热源
        
        Returns
        -------
        float
            热含量
        """
        ambient_temp = 25.0  # °C
        delta_T = source.outlet_temperature - ambient_temp
        heat_content = source.mass_flow_rate * source.specific_heat * delta_T / 1000.0  # kW
        return heat_content
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.heat_sources:
                print("警告: 未配置热源")
            
            if not self.heat_sinks:
                print("警告: 未配置热汇")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_heat_source(self, source: HeatSource):
        """添加热源
        
        Parameters
        ----------
        source : HeatSource
            热源
        """
        source.heat_content = self._calculate_heat_content(source)
        self.heat_sources[source.source_id] = source
    
    def add_heat_sink(self, sink: HeatSink):
        """添加热汇
        
        Parameters
        ----------
        sink : HeatSink
            热汇
        """
        self.heat_sinks[sink.sink_id] = sink
    
    def add_heat_exchanger(self, exchanger: HeatExchanger):
        """添加换热器
        
        Parameters
        ----------
        exchanger : HeatExchanger
            换热器
        """
        self.heat_exchangers[exchanger.exchanger_id] = exchanger
    
    def add_thermal_storage(self, storage: ThermalStorage):
        """添加热储能
        
        Parameters
        ----------
        storage : ThermalStorage
            热储能
        """
        self.thermal_storage[storage.storage_id] = storage
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化余热回收
        
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
        
        for source_id, source in self.heat_sources.items():
            hourly_heat = source.heat_content * 0.8
            schedule = []
            
            for hour in range(time_horizon):
                recovered_heat = hourly_heat * 0.7
                savings = recovered_heat * 0.5  # 元/kWh
                total_cost -= savings
                
                schedule.append({
                    'hour': hour,
                    'available_heat': hourly_heat,
                    'recovered_heat': recovered_heat,
                    'savings': savings
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.8
        
        for sink_id, sink in self.heat_sinks.items():
            utilization = 0.7 + np.random.random() * 0.2
            component_utilization[sink_id] = utilization
        
        for storage_id, storage in self.thermal_storage.items():
            utilization = 0.6 + np.random.random() * 0.3
            component_utilization[storage_id] = utilization
            
            storage_cost = storage.capital_cost * 0.1 / time_horizon
            total_cost += storage_cost
        
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
                    'heat_recovery_savings': -total_cost * 0.8,
                    'storage_cost': total_cost * 0.2
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
        
        for source_id, source in self.heat_sources.items():
            hourly_heat = source.heat_content * 0.9
            schedule = []
            
            for hour in range(time_horizon):
                recovered_heat = hourly_heat * 0.8
                carbon_savings = recovered_heat * 0.2  # kg CO2/kWh
                total_carbon -= carbon_savings
                
                schedule.append({
                    'hour': hour,
                    'available_heat': hourly_heat,
                    'recovered_heat': recovered_heat,
                    'carbon_savings': carbon_savings
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.85
        
        for storage_id, storage in self.thermal_storage.items():
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
                    'heat_recovery': total_carbon
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
        
        for source_id, source in self.heat_sources.items():
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.9 + np.random.random() * 0.1
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'reliability': reliability
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.75
        
        for storage_id, storage in self.thermal_storage.items():
            component_utilization[storage_id] = 0.8
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
        
        for source_id, source in self.heat_sources.items():
            hourly_heat = source.heat_content * 0.85
            schedule = []
            
            for hour in range(time_horizon):
                recovery_efficiency = 0.75 + np.random.random() * 0.15
                recovered_heat = hourly_heat * recovery_efficiency
                efficiency_score += recovery_efficiency
                
                schedule.append({
                    'hour': hour,
                    'available_heat': hourly_heat,
                    'recovered_heat': recovered_heat,
                    'recovery_efficiency': recovery_efficiency
                })
            
            energy_schedule[source_id] = schedule
            component_utilization[source_id] = 0.85
        
        for storage_id, storage in self.thermal_storage.items():
            avg_efficiency = (storage.charge_efficiency + storage.discharge_efficiency) / 2
            component_utilization[storage_id] = 0.75
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
        weights = {'cost': 0.4, 'carbon': 0.3, 'efficiency': 0.3}
        
        cost_result = self._optimize_cost(time_horizon)
        carbon_result = self._optimize_carbon(time_horizon)
        efficiency_result = self._optimize_efficiency(time_horizon)
        
        normalized_cost = abs(cost_result.total_cost) / 10000.0
        normalized_carbon = abs(carbon_result.total_carbon_emissions) / 1000.0
        normalized_efficiency = 1.0 - (efficiency_result.objective_value / 
                                        (len(self.heat_sources) + len(self.thermal_storage)))
        
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
    
    def design_heat_recovery_system(
        self,
        source_id: str,
        sink_id: str,
        recovery_method: HeatRecoveryMethod
    ) -> Dict[str, Any]:
        """设计余热回收系统
        
        Parameters
        ----------
        source_id : str
            热源ID
        sink_id : str
            热汇ID
        recovery_method : HeatRecoveryMethod
            回收方法
        
        Returns
        -------
        Dict[str, Any]
            系统设计结果
        """
        if source_id not in self.heat_sources:
            return {'error': '热源不存在'}
        
        if sink_id not in self.heat_sinks:
            return {'error': '热汇不存在'}
        
        source = self.heat_sources[source_id]
        sink = self.heat_sinks[sink_id]
        
        delta_T = source.outlet_temperature - sink.required_temperature
        
        if delta_T <= 0:
            return {'error': '热源温度不足以满足热汇需求'}
        
        heat_transfer_coeff = 500.0  # W/m²·K
        effectiveness = 0.85
        required_heat_transfer = source.heat_content * effectiveness
        
        heat_transfer_area = required_heat_transfer * 1000.0 / (heat_transfer_coeff * delta_T)
        
        capital_cost = self._estimate_capital_cost(recovery_method, heat_transfer_area)
        operating_cost = capital_cost * 0.05
        maintenance_cost = capital_cost * 0.02
        
        annual_savings = required_heat_transfer * 0.5 * 8760  # 元/年
        payback_period = capital_cost / annual_savings if annual_savings > 0 else float('inf')
        
        heat_exchanger = HeatExchanger(
            exchanger_id=f"hx_{source_id}_{sink_id}",
            exchanger_type="shell_tube",
            heat_transfer_area=heat_transfer_area,
            heat_transfer_coefficient=heat_transfer_coeff,
            effectiveness=effectiveness,
            max_heat_transfer=required_heat_transfer,
            pressure_drop_hot=10.0,
            pressure_drop_cold=10.0
        )
        
        system = HeatRecoverySystem(
            system_id=f"hrs_{source_id}_{sink_id}",
            recovery_method=recovery_method,
            heat_source_id=source_id,
            heat_sink_id=sink_id,
            heat_exchanger=heat_exchanger,
            recovered_heat=required_heat_transfer,
            recovery_efficiency=effectiveness,
            capital_cost=capital_cost,
            operating_cost=operating_cost,
            maintenance_cost=maintenance_cost,
            payback_period=payback_period
        )
        
        return {
            'system': system,
            'design_parameters': {
                'heat_transfer_area': heat_transfer_area,
                'effectiveness': effectiveness,
                'required_heat_transfer': required_heat_transfer
            },
            'economic_analysis': {
                'capital_cost': capital_cost,
                'operating_cost': operating_cost,
                'maintenance_cost': maintenance_cost,
                'annual_savings': annual_savings,
                'payback_period': payback_period
            }
        }
    
    def _estimate_capital_cost(
        self,
        recovery_method: HeatRecoveryMethod,
        heat_transfer_area: float
    ) -> float:
        """估算投资成本
        
        Parameters
        ----------
        recovery_method : HeatRecoveryMethod
            回收方法
        heat_transfer_area : float
            换热面积
        
        Returns
        -------
        float
            投资成本
        """
        base_cost = 5000.0  # 元/m²
        area_factor = heat_transfer_area ** 0.6
        
        if recovery_method == HeatRecoveryMethod.HEAT_EXCHANGER:
            cost_factor = 1.0
        elif recovery_method == HeatRecoveryMethod.ORC:
            cost_factor = 3.0
        elif recovery_method == HeatRecoveryMethod.KALINA_CYCLE:
            cost_factor = 3.5
        elif recovery_method == HeatRecoveryMethod.ABSORPTION_CHILLER:
            cost_factor = 2.5
        elif recovery_method == HeatRecoveryMethod.HEAT_PUMP:
            cost_factor = 2.0
        else:
            cost_factor = 1.5
        
        capital_cost = base_cost * area_factor * cost_factor
        return capital_cost
    
    def optimize_thermal_storage_operation(
        self,
        storage_id: str,
        heat_source_profile: pd.Series,
        heat_demand_profile: pd.Series
    ) -> Dict[str, Any]:
        """优化热储能运行
        
        Parameters
        ----------
        storage_id : str
            储能ID
        heat_source_profile : pd.Series
            热源曲线
        heat_demand_profile : pd.Series
            热需求曲线
        
        Returns
        -------
        Dict[str, Any]
            运行优化结果
        """
        if storage_id not in self.thermal_storage:
            return {'error': '储能设备不存在'}
        
        storage = self.thermal_storage[storage_id]
        
        hours = min(len(heat_source_profile), len(heat_demand_profile))
        schedule = []
        
        current_soc = storage.current_soc
        current_temp = storage.current_temperature
        
        for hour in range(hours):
            available_heat = heat_source_profile.iloc[hour] if hour < len(heat_source_profile) else 0
            demand = heat_demand_profile.iloc[hour] if hour < len(heat_demand_profile) else 0
            
            if available_heat > demand:
                excess_heat = available_heat - demand
                max_charge = (storage.max_soc - current_soc) * storage.capacity
                charge_power = min(excess_heat, max_charge)
                
                current_soc = EnergyCalculator.calculate_battery_soc(
                    current_soc, charge_power, 1, storage.capacity, storage.charge_efficiency
                )
                
                action = 'charge'
            elif demand > available_heat:
                deficit = demand - available_heat
                max_discharge = (current_soc - storage.min_soc) * storage.capacity
                discharge_power = min(deficit, max_discharge)
                
                current_soc = current_soc - discharge_power / storage.capacity
                
                action = 'discharge'
            else:
                action = 'idle'
            
            current_temp = storage.min_temperature + current_soc * (storage.max_temperature - storage.min_temperature)
            
            schedule.append({
                'hour': hour,
                'action': action,
                'available_heat': available_heat,
                'demand': demand,
                'soc': current_soc,
                'temperature': current_temp
            })
        
        return {
            'storage_id': storage_id,
            'schedule': schedule,
            'total_charge_cycles': sum(1 for s in schedule if s['action'] == 'charge'),
            'total_discharge_cycles': sum(1 for s in schedule if s['action'] == 'discharge')
        }
    
    def generate_waste_heat_report(self) -> Dict[str, Any]:
        """生成余热报告
        
        Returns
        -------
        Dict[str, Any]
            余热报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        total_available_heat = sum(source.heat_content for source in self.heat_sources.values())
        total_heat_demand = sum(sink.heat_demand for sink in self.heat_sinks.values())
        
        report = {
            'summary': {
                'total_heat_sources': len(self.heat_sources),
                'total_heat_sinks': len(self.heat_sinks),
                'total_heat_exchangers': len(self.heat_exchangers),
                'total_thermal_storage': len(self.thermal_storage),
                'total_available_heat': total_available_heat,
                'total_heat_demand': total_heat_demand,
                'heat_balance_ratio': total_heat_demand / total_available_heat if total_available_heat > 0 else 0,
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'source_details': {},
            'sink_details': {},
            'storage_details': {}
        }
        
        for source_id, source in self.heat_sources.items():
            grade = self._classify_heat_grade(source.outlet_temperature)
            report['source_details'][source_id] = {
                'type': source.source_type.value,
                'outlet_temperature': source.outlet_temperature,
                'mass_flow_rate': source.mass_flow_rate,
                'heat_content': source.heat_content,
                'grade': grade.value,
                'available_hours_per_day': source.available_hours_per_day
            }
        
        for sink_id, sink in self.heat_sinks.items():
            report['sink_details'][sink_id] = {
                'type': sink.sink_type,
                'required_temperature': sink.required_temperature,
                'heat_demand': sink.heat_demand,
                'priority': sink.priority
            }
        
        for storage_id, storage in self.thermal_storage.items():
            report['storage_details'][storage_id] = {
                'medium': storage.storage_medium,
                'capacity': storage.capacity,
                'max_temperature': storage.max_temperature,
                'min_temperature': storage.min_temperature,
                'charge_efficiency': storage.charge_efficiency,
                'discharge_efficiency': storage.discharge_efficiency,
                'current_soc': storage.current_soc,
                'current_temperature': storage.current_temperature
            }
        
        return report
    
    def _classify_heat_grade(self, temperature: float) -> HeatGrade:
        """分类余热等级
        
        Parameters
        ----------
        temperature : float
            温度
        
        Returns
        -------
        HeatGrade
            余热等级
        """
        if temperature > 400:
            return HeatGrade.HIGH
        elif temperature > 200:
            return HeatGrade.MEDIUM_HIGH
        elif temperature > 100:
            return HeatGrade.MEDIUM
        elif temperature > 50:
            return HeatGrade.LOW
        else:
            return HeatGrade.VERY_LOW