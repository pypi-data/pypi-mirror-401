"""
工程机械专用能源系统建模模块

提供针对电动/混合动力工程机械的充电、换电、能量管理系统的专用建模工具
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from .base import (
    BaseIndustrialExtension,
    MachineryConfig,
    EnergySource,
    OptimizationObjective,
    OptimizationResult,
    EnergyCalculator,
    TimeSeriesGenerator,
    ResultAnalyzer
)


@dataclass
class ChargingStationConfig:
    """充电站配置"""
    station_id: str
    location: str
    charging_power: float  # kW
    charging_efficiency: float = 0.95
    number_of_chargers: int = 1
    available_hours: List[str] = field(default_factory=lambda: ["00:00-24:00"])
    grid_connection_capacity: float = 500.0  # kW


@dataclass
class BatterySwapStationConfig:
    """换电站配置"""
    station_id: str
    location: str
    swap_capacity: int  # 每日可换电池数量
    battery_capacity: float  # kWh per battery
    charging_power: float  # kW per battery
    charging_efficiency: float = 0.95
    number_of_batteries: int = 10


@dataclass
class MachineryOperatingSchedule:
    """工程机械运行计划"""
    machinery_id: str
    start_time: str
    end_time: str
    energy_demand: float  # kWh
    location: str
    priority: int = 1  # 1-5, 1为最高优先级


class ConstructionMachineryEnergySystem(BaseIndustrialExtension):
    """工程机械能源系统
    
    支持电动/混合动力工程机械的能源管理、充电调度、换电优化等功能
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化工程机械能源系统
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - machinery_list: 工程机械列表
            - charging_stations: 充电站列表
            - swap_stations: 换电站列表
            - price_profile: 能源价格配置
            - carbon_factors: 碳排放因子
        """
        super().__init__(config)
        
        self.machinery_list: Dict[str, MachineryConfig] = {}
        self.charging_stations: Dict[str, ChargingStationConfig] = {}
        self.swap_stations: Dict[str, BatterySwapStationConfig] = {}
        self.operating_schedules: Dict[str, MachineryOperatingSchedule] = {}
        
        self.price_profile = EnergyPriceProfile()
        self.carbon_factors = CarbonEmissionFactors()
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'machinery_list' in config:
            for mach_config in config['machinery_list']:
                mach = MachineryConfig(**mach_config)
                self.machinery_list[mach.machinery_id] = mach
        
        if 'charging_stations' in config:
            for station_config in config['charging_stations']:
                station = ChargingStationConfig(**station_config)
                self.charging_stations[station.station_id] = station
        
        if 'swap_stations' in config:
            for swap_config in config['swap_stations']:
                swap = BatterySwapStationConfig(**swap_config)
                self.swap_stations[swap.station_id] = swap
        
        if 'price_profile' in config:
            price_dict = config['price_profile']
            self.price_profile = EnergyPriceProfile(**price_dict)
        
        if 'carbon_factors' in config:
            carbon_dict = config['carbon_factors']
            self.carbon_factors = CarbonEmissionFactors(**carbon_dict)
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.machinery_list:
                print("警告: 未配置工程机械")
            
            if not self.charging_stations and not self.swap_stations:
                print("警告: 未配置充电站或换电站")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_machinery(self, machinery: MachineryConfig):
        """添加工程机械
        
        Parameters
        ----------
        machinery : MachineryConfig
            工程机械配置
        """
        self.machinery_list[machinery.machinery_id] = machinery
    
    def add_charging_station(self, station: ChargingStationConfig):
        """添加充电站
        
        Parameters
        ----------
        station : ChargingStationConfig
            充电站配置
        """
        self.charging_stations[station.station_id] = station
    
    def add_swap_station(self, station: BatterySwapStationConfig):
        """添加换电站
        
        Parameters
        ----------
        station : BatterySwapStationConfig
            换电站配置
        """
        self.swap_stations[station.station_id] = station
    
    def add_operating_schedule(self, schedule: MachineryOperatingSchedule):
        """添加运行计划
        
        Parameters
        ----------
        schedule : MachineryOperatingSchedule
            运行计划
        """
        self.operating_schedules[schedule.machinery_id] = schedule
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化工程机械能源系统
        
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
        
        for mach_id, machinery in self.machinery_list.items():
            if machinery.energy_source == EnergySource.ELECTRICITY:
                daily_energy = machinery.daily_energy_demand or \
                              EnergyCalculator.calculate_energy_consumption(
                                  machinery.power_rating,
                                  machinery.operating_hours_per_day
                              )
                
                hourly_energy = daily_energy / 24
                schedule = []
                
                for hour in range(time_horizon):
                    if hour < 24:
                        time_period = f"{hour:02d}:00"
                        price = self.price_profile.electricity_price.get(time_period, 0.8)
                        cost = hourly_energy * price
                        total_cost += cost
                        schedule.append({
                            'hour': hour,
                            'energy': hourly_energy,
                            'price': price,
                            'cost': cost
                        })
                
                energy_schedule[mach_id] = schedule
                component_utilization[mach_id] = 0.75
                
                carbon = EnergyCalculator.calculate_carbon_emissions(
                    daily_energy,
                    self.carbon_factors.electricity
                )
                total_carbon += carbon
        
        for station_id, station in self.charging_stations.items():
            utilization = 0.6 + np.random.random() * 0.3
            component_utilization[station_id] = utilization
        
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
                    'electricity': total_cost * 0.9,
                    'charging_infrastructure': total_cost * 0.1
                },
                'emission_sources': {
                    'electricity': total_carbon
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
        
        for mach_id, machinery in self.machinery_list.items():
            if machinery.energy_source == EnergySource.ELECTRICITY:
                daily_energy = machinery.daily_energy_demand or \
                              EnergyCalculator.calculate_energy_consumption(
                                  machinery.power_rating,
                                  machinery.operating_hours_per_day
                              )
                
                hourly_energy = daily_energy / 24
                schedule = []
                
                for hour in range(time_horizon):
                    if hour < 24:
                        carbon = hourly_energy * self.carbon_factors.electricity
                        total_carbon += carbon
                        schedule.append({
                            'hour': hour,
                            'energy': hourly_energy,
                            'carbon': carbon
                        })
                
                energy_schedule[mach_id] = schedule
                component_utilization[mach_id] = 0.8
        
        for station_id, station in self.charging_stations.items():
            component_utilization[station_id] = 0.7
        
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
                    'electricity': total_carbon
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
        
        for mach_id, machinery in self.machinery_list.items():
            if machinery.energy_source == EnergySource.ELECTRICITY:
                daily_energy = machinery.daily_energy_demand or \
                              EnergyCalculator.calculate_energy_consumption(
                                  machinery.power_rating,
                                  machinery.operating_hours_per_day
                              )
                
                schedule = []
                
                for hour in range(time_horizon):
                    if hour < 24:
                        schedule.append({
                            'hour': hour,
                            'energy': daily_energy / 24,
                            'reliability': 0.95 + np.random.random() * 0.05
                        })
                
                energy_schedule[mach_id] = schedule
                component_utilization[mach_id] = 0.85
                reliability_score += 0.95
        
        for station_id, station in self.charging_stations.items():
            component_utilization[station_id] = 0.8
            reliability_score += 0.9
        
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
        
        for mach_id, machinery in self.machinery_list.items():
            if machinery.energy_source == EnergySource.ELECTRICITY:
                daily_energy = machinery.daily_energy_demand or \
                              EnergyCalculator.calculate_energy_consumption(
                                  machinery.power_rating,
                                  machinery.operating_hours_per_day
                              )
                
                schedule = []
                
                for hour in range(time_horizon):
                    if hour < 24:
                        efficiency = 0.85 + np.random.random() * 0.1
                        schedule.append({
                            'hour': hour,
                            'energy': daily_energy / 24,
                            'efficiency': efficiency
                        })
                        efficiency_score += efficiency
                
                energy_schedule[mach_id] = schedule
                component_utilization[mach_id] = 0.8
        
        for station_id, station in self.charging_stations.items():
            component_utilization[station_id] = 0.75
            efficiency_score += station.charging_efficiency
        
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
                                       (len(self.machinery_list) + len(self.charging_stations)))
        
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
    
    def calculate_charging_schedule(
        self,
        machinery_id: str,
        initial_soc: float = 0.2,
        target_soc: float = 0.9,
        available_time: int = 8
    ) -> Dict[str, Any]:
        """计算充电计划
        
        Parameters
        ----------
        machinery_id : str
            工程机械ID
        initial_soc : float
            初始SOC
        target_soc : float
            目标SOC
        available_time : int
            可用时间（小时）
        
        Returns
        -------
        Dict[str, Any]
            充电计划
        """
        if machinery_id not in self.machinery_list:
            return {'error': '工程机械不存在'}
        
        machinery = self.machinery_list[machinery_id]
        if machinery.battery_capacity is None:
            return {'error': '该工程机械未配置电池容量'}
        
        battery_capacity = machinery.battery_capacity
        energy_needed = (target_soc - initial_soc) * battery_capacity
        
        if not self.charging_stations:
            return {'error': '未配置充电站'}
        
        station = list(self.charging_stations.values())[0]
        charging_power = station.charging_power
        efficiency = station.charging_efficiency
        
        charging_time = energy_needed / (charging_power * efficiency)
        
        if charging_time > available_time:
            actual_soc = initial_soc + (charging_power * available_time * efficiency) / battery_capacity
            charging_time = available_time
        else:
            actual_soc = target_soc
        
        schedule = {
            'machinery_id': machinery_id,
            'initial_soc': initial_soc,
            'target_soc': target_soc,
            'actual_soc': actual_soc,
            'energy_needed': energy_needed,
            'charging_power': charging_power,
            'charging_time': charging_time,
            'charging_cost': energy_needed * 0.8,
            'station_id': station.station_id
        }
        
        return schedule
    
    def generate_energy_report(self) -> Dict[str, Any]:
        """生成能源报告
        
        Returns
        -------
        Dict[str, Any]
            能源报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        carbon_analysis = ResultAnalyzer.analyze_carbon_emissions(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        report = {
            'summary': {
                'total_machinery': len(self.machinery_list),
                'total_charging_stations': len(self.charging_stations),
                'total_swap_stations': len(self.swap_stations),
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'carbon_analysis': carbon_analysis,
            'utilization_analysis': utilization_analysis,
            'machinery_details': {},
            'charging_stations': {}
        }
        
        for mach_id, machinery in self.machinery_list.items():
            report['machinery_details'][mach_id] = {
                'type': machinery.machinery_type.value,
                'power_rating': machinery.power_rating,
                'energy_source': machinery.energy_source.value,
                'battery_capacity': machinery.battery_capacity,
                'daily_energy_demand': machinery.daily_energy_demand
            }
        
        for station_id, station in self.charging_stations.items():
            report['charging_stations'][station_id] = {
                'location': station.location,
                'charging_power': station.charging_power,
                'number_of_chargers': station.number_of_chargers
            }
        
        return report


class EnergyPriceProfile:
    """能源价格配置"""
    
    def __init__(
        self,
        electricity_price: Dict[str, float] = None,
        hydrogen_price: float = 30.0,
        diesel_price: float = 8.0,
        natural_gas_price: float = 4.0,
        peak_hours: List[str] = None
    ):
        self.electricity_price = electricity_price or {}
        self.hydrogen_price = hydrogen_price
        self.diesel_price = diesel_price
        self.natural_gas_price = natural_gas_price
        self.peak_hours = peak_hours or ["08:00-12:00", "18:00-22:00"]


class CarbonEmissionFactors:
    """碳排放因子配置"""
    
    def __init__(
        self,
        electricity: float = 0.4,
        hydrogen: float = 0.0,
        diesel: float = 2.68,
        natural_gas: float = 2.0
    ):
        self.electricity = electricity
        self.hydrogen = hydrogen
        self.diesel = diesel
        self.natural_gas = natural_gas