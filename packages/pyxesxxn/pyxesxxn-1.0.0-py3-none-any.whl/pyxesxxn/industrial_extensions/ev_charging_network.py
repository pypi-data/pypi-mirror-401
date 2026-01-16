"""
电动工程机械充换电网络规划模块

城市/工业园区内电动工程机械充换电设施的优化布局与容量规划
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import math

from .base import (
    BaseIndustrialExtension,
    OptimizationObjective,
    OptimizationResult,
    EnergyCalculator,
    TimeSeriesGenerator,
    ResultAnalyzer
)


class ChargingStationType(Enum):
    """充电站类型"""
    FAST_CHARGING = "fast_charging"
    NORMAL_CHARGING = "normal_charging"
    WIRELESS_CHARGING = "wireless_charging"
    SWAP_STATION = "swap_station"


class ServiceLevel(Enum):
    """服务等级"""
    HIGH = "high"  # <10分钟等待
    MEDIUM = "medium"  # 10-30分钟等待
    LOW = "low"  # >30分钟等待


@dataclass
class ChargingStation:
    """充电站"""
    station_id: str
    station_type: ChargingStationType
    location: str
    coordinates: Tuple[float, float]  # (latitude, longitude)
    charging_power: float  # kW
    number_of_chargers: int
    charging_efficiency: float = 0.95
    operating_hours: List[str] = field(default_factory=lambda: ["00:00-24:00"])
    service_level: ServiceLevel = ServiceLevel.MEDIUM
    land_cost: float = 0.0  # 元/m²
    construction_cost: float = 0.0  # 元
    annual_maintenance_cost: float = 0.0  # 元/年


@dataclass
class BatterySwapStation:
    """换电站"""
    station_id: str
    location: str
    coordinates: Tuple[float, float]
    swap_capacity: int  # 每日可换电池数量
    battery_capacity: float  # kWh per battery
    charging_power: float  # kW per battery
    number_of_batteries: int
    charging_efficiency: float = 0.95
    swap_time: float = 5.0  # 分钟
    land_cost: float = 0.0
    construction_cost: float = 0.0
    annual_maintenance_cost: float = 0.0


@dataclass
class EVChargingDemand:
    """电动工程机械充电需求"""
    demand_id: str
    machinery_type: str
    location: str
    coordinates: Tuple[float, float]
    battery_capacity: float  # kWh
    current_soc: float  # 0-1
    target_soc: float  # 0-1
    required_energy: float  # kWh
    arrival_time: datetime
    departure_time: datetime
    charging_preference: str  # fast, normal, swap
    priority: int = 1


@dataclass
class ChargingNetwork:
    """充电网络"""
    network_id: str
    charging_stations: Dict[str, ChargingStation] = field(default_factory=dict)
    swap_stations: Dict[str, BatterySwapStation] = field(default_factory=dict)
    total_capacity: float = 0.0  # kW
    coverage_area: float = 0.0  # km²


class EVChargingNetworkPlanner(BaseIndustrialExtension):
    """电动工程机械充电网络规划器
    
    城市/工业园区内电动工程机械充换电设施的优化布局与容量规划
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化充电网络规划器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - charging_stations: 充电站列表
            - swap_stations: 换电站列表
            - charging_demands: 充电需求列表
            - charging_network: 充电网络配置
        """
        super().__init__(config)
        
        self.charging_stations: Dict[str, ChargingStation] = {}
        self.swap_stations: Dict[str, BatterySwapStation] = {}
        self.charging_demands: Dict[str, EVChargingDemand] = {}
        self.charging_network: Optional[ChargingNetwork] = None
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'charging_stations' in config:
            for station_config in config['charging_stations']:
                station = ChargingStation(**station_config)
                self.charging_stations[station.station_id] = station
        
        if 'swap_stations' in config:
            for swap_config in config['swap_stations']:
                swap = BatterySwapStation(**swap_config)
                self.swap_stations[swap.station_id] = swap
        
        if 'charging_demands' in config:
            for demand_config in config['charging_demands']:
                demand = EVChargingDemand(**demand_config)
                self.charging_demands[demand.demand_id] = demand
        
        if 'charging_network' in config:
            network_config = config['charging_network']
            self.charging_network = ChargingNetwork(**network_config)
            self.charging_network.charging_stations = self.charging_stations
            self.charging_network.swap_stations = self.swap_stations
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.charging_stations and not self.swap_stations:
                print("警告: 未配置充电站或换电站")
            
            if not self.charging_demands:
                print("警告: 未配置充电需求")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_charging_station(self, station: ChargingStation):
        """添加充电站
        
        Parameters
        ----------
        station : ChargingStation
            充电站
        """
        self.charging_stations[station.station_id] = station
    
    def add_swap_station(self, station: BatterySwapStation):
        """添加换电站
        
        Parameters
        ----------
        station : BatterySwapStation
            换电站
        """
        self.swap_stations[station.station_id] = station
    
    def add_charging_demand(self, demand: EVChargingDemand):
        """添加充电需求
        
        Parameters
        ----------
        demand : EVChargingDemand
            充电需求
        """
        self.charging_demands[demand.demand_id] = demand
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化充电网络
        
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
        
        for station_id, station in self.charging_stations.items():
            total_capacity = station.charging_power * station.number_of_chargers
            hourly_utilization = 0.6 + np.random.random() * 0.3
            schedule = []
            
            for hour in range(time_horizon):
                charged_energy = total_capacity * hourly_utilization
                revenue = charged_energy * 1.5  # 元/kWh
                total_cost -= revenue
                
                schedule.append({
                    'hour': hour,
                    'charged_energy': charged_energy,
                    'revenue': revenue,
                    'utilization': hourly_utilization
                })
            
            energy_schedule[station_id] = schedule
            component_utilization[station_id] = hourly_utilization
            
            annual_cost = station.construction_cost * 0.1 + station.annual_maintenance_cost
            total_cost += annual_cost / 365 * time_horizon
        
        for swap_id, swap in self.swap_stations.items():
            utilization = 0.5 + np.random.random() * 0.4
            component_utilization[swap_id] = utilization
            
            daily_swaps = swap.swap_capacity * utilization
            revenue = daily_swaps * 50  # 元/次
            total_cost -= revenue
            
            annual_cost = swap.construction_cost * 0.1 + swap.annual_maintenance_cost
            total_cost += annual_cost / 365 * time_horizon
        
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
                    'construction_cost': total_cost * 0.3,
                    'maintenance_cost': total_cost * 0.2,
                    'revenue': -total_cost * 0.5
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
        
        for station_id, station in self.charging_stations.items():
            total_capacity = station.charging_power * station.number_of_chargers
            hourly_utilization = 0.7 + np.random.random() * 0.2
            schedule = []
            
            for hour in range(time_horizon):
                charged_energy = total_capacity * hourly_utilization
                carbon_savings = charged_energy * 0.3  # kg CO2/kWh
                total_carbon -= carbon_savings
                
                schedule.append({
                    'hour': hour,
                    'charged_energy': charged_energy,
                    'carbon_savings': carbon_savings
                })
            
            energy_schedule[station_id] = schedule
            component_utilization[station_id] = hourly_utilization
        
        for swap_id, swap in self.swap_stations.items():
            component_utilization[swap_id] = 0.7
        
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
                    'ev_charging': total_carbon
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
        
        for station_id, station in self.charging_stations.items():
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.9 + np.random.random() * 0.1
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'reliability': reliability
                })
            
            energy_schedule[station_id] = schedule
            component_utilization[station_id] = 0.75
        
        for swap_id, swap in self.swap_stations.items():
            component_utilization[swap_id] = 0.8
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
        
        for station_id, station in self.charging_stations.items():
            schedule = []
            
            for hour in range(time_horizon):
                efficiency = station.charging_efficiency * (0.9 + np.random.random() * 0.1)
                efficiency_score += efficiency
                
                schedule.append({
                    'hour': hour,
                    'efficiency': efficiency
                })
            
            energy_schedule[station_id] = schedule
            component_utilization[station_id] = 0.8
        
        for swap_id, swap in self.swap_stations.items():
            component_utilization[swap_id] = 0.75
            efficiency_score += swap.charging_efficiency
        
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
                                       (len(self.charging_stations) + len(self.swap_stations)))
        
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
    
    def calculate_distance(
        self,
        point1: Tuple[float, float],
        point2: Tuple[float, float]
    ) -> float:
        """计算两点间距离（Haversine公式）
        
        Parameters
        ----------
        point1 : Tuple[float, float]
            点1坐标 (latitude, longitude)
        point2 : Tuple[float, float]
            点2坐标 (latitude, longitude)
        
        Returns
        -------
        float
            距离
        """
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        R = 6371.0  # 地球半径
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat / 2) ** 2 +
              math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
              math.sin(dlon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def optimize_station_location(
        self,
        demand_points: List[Tuple[float, float]],
        max_distance: float = 5.0,
        min_capacity: float = 100.0
    ) -> Dict[str, Any]:
        """优化充电站位置
        
        Parameters
        ----------
        demand_points : List[Tuple[float, float]]
            需求点坐标列表
        max_distance : float
            最大服务距离
        min_capacity : float
            最小容量
        
        Returns
        -------
        Dict[str, Any]
            位置优化结果
        """
        if not demand_points:
            return {'error': '无需求点'}
        
        n_stations = max(1, len(demand_points) // 10)
        
        latitudes = [point[0] for point in demand_points]
        longitudes = [point[1] for point in demand_points]
        
        optimal_locations = []
        
        for i in range(n_stations):
            cluster_size = len(demand_points) // n_stations
            start_idx = i * cluster_size
            end_idx = min((i + 1) * cluster_size, len(demand_points))
            
            cluster_points = demand_points[start_idx:end_idx]
            
            if cluster_points:
                avg_lat = sum(point[0] for point in cluster_points) / len(cluster_points)
                avg_lon = sum(point[1] for point in cluster_points) / len(cluster_points)
                
                optimal_locations.append((avg_lat, avg_lon))
        
        coverage_analysis = []
        for location in optimal_locations:
            covered_demands = 0
            for demand_point in demand_points:
                distance = self.calculate_distance(location, demand_point)
                if distance <= max_distance:
                    covered_demands += 1
            
            coverage_analysis.append({
                'location': location,
                'covered_demands': covered_demands,
                'coverage_ratio': covered_demands / len(demand_points)
            })
        
        return {
            'optimal_locations': optimal_locations,
            'number_of_stations': n_stations,
            'coverage_analysis': coverage_analysis,
            'total_coverage': sum(ca['covered_demands'] for ca in coverage_analysis),
            'average_coverage_ratio': sum(ca['coverage_ratio'] for ca in coverage_analysis) / len(coverage_analysis) if coverage_analysis else 0
        }
    
    def calculate_charging_schedule(
        self,
        demand_id: str,
        station_id: str
    ) -> Dict[str, Any]:
        """计算充电计划
        
        Parameters
        ----------
        demand_id : str
            需求ID
        station_id : str
            充电站ID
        
        Returns
        -------
        Dict[str, Any]
            充电计划
        """
        if demand_id not in self.charging_demands:
            return {'error': '充电需求不存在'}
        
        if station_id not in self.charging_stations:
            return {'error': '充电站不存在'}
        
        demand = self.charging_demands[demand_id]
        station = self.charging_stations[station_id]
        
        distance = self.calculate_distance(demand.coordinates, station.coordinates)
        
        required_energy = demand.required_energy
        charging_power = station.charging_power
        charging_time = required_energy / (charging_power * station.charging_efficiency)
        
        travel_time = distance / 30.0  # 假设平均速度30km/h
        
        total_time = travel_time + charging_time
        
        available_time = (demand.departure_time - demand.arrival_time).total_seconds() / 3600
        
        if total_time > available_time:
            feasible = False
            actual_soc = demand.current_soc
        else:
            feasible = True
            actual_soc = demand.target_soc
        
        cost = required_energy * 1.2  # 元/kWh
        
        return {
            'demand_id': demand_id,
            'station_id': station_id,
            'distance': distance,
            'travel_time': travel_time,
            'charging_time': charging_time,
            'total_time': total_time,
            'required_energy': required_energy,
            'charging_power': charging_power,
            'cost': cost,
            'feasible': feasible,
            'actual_soc': actual_soc
        }
    
    def generate_charging_network_report(self) -> Dict[str, Any]:
        """生成充电网络报告
        
        Returns
        -------
        Dict[str, Any]
            充电网络报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        total_charging_capacity = sum(
            station.charging_power * station.number_of_chargers
            for station in self.charging_stations.values()
        )
        
        total_swap_capacity = sum(
            swap.swap_capacity for swap in self.swap_stations.values()
        )
        
        report = {
            'summary': {
                'total_charging_stations': len(self.charging_stations),
                'total_swap_stations': len(self.swap_stations),
                'total_charging_demands': len(self.charging_demands),
                'total_charging_capacity': total_charging_capacity,
                'total_swap_capacity': total_swap_capacity,
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'charging_station_details': {},
            'swap_station_details': {},
            'demand_summary': {}
        }
        
        for station_id, station in self.charging_stations.items():
            report['charging_station_details'][station_id] = {
                'type': station.station_type.value,
                'location': station.location,
                'coordinates': station.coordinates,
                'charging_power': station.charging_power,
                'number_of_chargers': station.number_of_chargers,
                'total_capacity': station.charging_power * station.number_of_chargers,
                'service_level': station.service_level.value,
                'construction_cost': station.construction_cost,
                'annual_maintenance_cost': station.annual_maintenance_cost
            }
        
        for swap_id, swap in self.swap_stations.items():
            report['swap_station_details'][swap_id] = {
                'location': swap.location,
                'coordinates': swap.coordinates,
                'swap_capacity': swap.swap_capacity,
                'battery_capacity': swap.battery_capacity,
                'charging_power': swap.charging_power,
                'number_of_batteries': swap.number_of_batteries,
                'swap_time': swap.swap_time,
                'construction_cost': swap.construction_cost,
                'annual_maintenance_cost': swap.annual_maintenance_cost
            }
        
        machinery_types = {}
        for demand in self.charging_demands.values():
            if demand.machinery_type not in machinery_types:
                machinery_types[demand.machinery_type] = {
                    'count': 0,
                    'total_energy_demand': 0.0,
                    'total_battery_capacity': 0.0
                }
            
            machinery_types[demand.machinery_type]['count'] += 1
            machinery_types[demand.machinery_type]['total_energy_demand'] += demand.required_energy
            machinery_types[demand.machinery_type]['total_battery_capacity'] += demand.battery_capacity
        
        report['demand_summary'] = machinery_types
        
        return report