"""
氢能工程机械能源系统模块

燃料电池工程机械的氢能供应链建模、加氢站网络规划与氢储能系统优化
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


class HydrogenProductionMethod(Enum):
    """制氢方法"""
    ELECTROLYSIS = "electrolysis"
    SMR = "smr"  # 蒸汽甲烷重整
    BIOMASS = "biomass"
    SOLAR_THERMAL = "solar_thermal"


class HydrogenStorageType(Enum):
    """储氢类型"""
    COMPRESSED_GAS = "compressed_gas"
    LIQUID = "liquid"
    METAL_HYDRIDE = "metal_hydride"
    UNDERGROUND = "underground"


@dataclass
class HydrogenProductionFacility:
    """制氢设施"""
    facility_id: str
    location: str
    production_method: HydrogenProductionMethod
    production_capacity: float  # kg/h
    energy_consumption: float  # kWh/kg H2
    efficiency: float  # 0-1
    carbon_emission: float  # kg CO2/kg H2
    operating_hours_per_day: float
    capital_cost: float  # 元
    operating_cost: float  # 元/kg H2
    water_consumption: float  # L/kg H2


@dataclass
class HydrogenStorage:
    """储氢设施"""
    storage_id: str
    location: str
    storage_type: HydrogenStorageType
    capacity: float  # kg
    current_level: float  # kg
    pressure: float  # bar (for compressed gas)
    temperature: float  # °C
    charge_efficiency: float  # 0-1
    discharge_efficiency: float  # 0-1
    capital_cost: float  # 元
    annual_maintenance_cost: float  # 元/年


@dataclass
class HydrogenRefuelingStation:
    """加氢站"""
    station_id: str
    location: str
    coordinates: Tuple[float, float]
    refueling_capacity: float  # kg/h
    storage_capacity: float  # kg
    number_of_dispensers: int
    refueling_pressure: float  # bar
    operating_hours: List[str]
    service_level: str  # high, medium, low
    land_cost: float  # 元
    construction_cost: float  # 元
    annual_maintenance_cost: float  # 元/年


@dataclass
class FuelCellMachinery:
    """燃料电池工程机械"""
    machinery_id: str
    machinery_type: str
    location: str
    fuel_cell_power: float  # kW
    hydrogen_consumption_rate: float  # kg/h
    fuel_cell_efficiency: float  # 0-1
    hydrogen_tank_capacity: float  # kg
    current_hydrogen_level: float  # kg
    operating_hours_per_day: float
    daily_energy_demand: float  # kWh


@dataclass
class HydrogenSupplyChain:
    """氢能供应链"""
    chain_id: str
    production_facilities: Dict[str, HydrogenProductionFacility]
    storage_facilities: Dict[str, HydrogenStorage]
    refueling_stations: Dict[str, HydrogenRefuelingStation]
    transport_network: Dict[str, Any]
    total_capacity: float  # kg/day
    total_demand: float  # kg/day


class HydrogenMachinerySystem(BaseIndustrialExtension):
    """氢能工程机械能源系统
    
    燃料电池工程机械的氢能供应链建模、加氢站网络规划与氢储能系统优化
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化氢能工程机械能源系统
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - production_facilities: 制氢设施列表
            - storage_facilities: 储氢设施列表
            - refueling_stations: 加氢站列表
            - fuel_cell_machinery: 燃料电池工程机械列表
            - hydrogen_supply_chain: 氢能供应链配置
        """
        super().__init__(config)
        
        self.production_facilities: Dict[str, HydrogenProductionFacility] = {}
        self.storage_facilities: Dict[str, HydrogenStorage] = {}
        self.refueling_stations: Dict[str, HydrogenRefuelingStation] = {}
        self.fuel_cell_machinery: Dict[str, FuelCellMachinery] = {}
        self.hydrogen_supply_chain: Optional[HydrogenSupplyChain] = None
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'production_facilities' in config:
            for facility_config in config['production_facilities']:
                facility = HydrogenProductionFacility(**facility_config)
                self.production_facilities[facility.facility_id] = facility
        
        if 'storage_facilities' in config:
            for storage_config in config['storage_facilities']:
                storage = HydrogenStorage(**storage_config)
                self.storage_facilities[storage.storage_id] = storage
        
        if 'refueling_stations' in config:
            for station_config in config['refueling_stations']:
                station = HydrogenRefuelingStation(**station_config)
                self.refueling_stations[station.station_id] = station
        
        if 'fuel_cell_machinery' in config:
            for machinery_config in config['fuel_cell_machinery']:
                machinery = FuelCellMachinery(**machinery_config)
                self.fuel_cell_machinery[machinery.machinery_id] = machinery
        
        if 'hydrogen_supply_chain' in config:
            chain_config = config['hydrogen_supply_chain']
            self.hydrogen_supply_chain = HydrogenSupplyChain(
                **chain_config,
                production_facilities=self.production_facilities,
                storage_facilities=self.storage_facilities,
                refueling_stations=self.refueling_stations
            )
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if not self.production_facilities:
                print("警告: 未配置制氢设施")
            
            if not self.refueling_stations:
                print("警告: 未配置加氢站")
            
            if not self.fuel_cell_machinery:
                print("警告: 未配置燃料电池工程机械")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_production_facility(self, facility: HydrogenProductionFacility):
        """添加制氢设施
        
        Parameters
        ----------
        facility : HydrogenProductionFacility
            制氢设施
        """
        self.production_facilities[facility.facility_id] = facility
    
    def add_storage_facility(self, storage: HydrogenStorage):
        """添加储氢设施
        
        Parameters
        ----------
        storage : HydrogenStorage
            储氢设施
        """
        self.storage_facilities[storage.storage_id] = storage
    
    def add_refueling_station(self, station: HydrogenRefuelingStation):
        """添加加氢站
        
        Parameters
        ----------
        station : HydrogenRefuelingStation
            加氢站
        """
        self.refueling_stations[station.station_id] = station
    
    def add_fuel_cell_machinery(self, machinery: FuelCellMachinery):
        """添加燃料电池工程机械
        
        Parameters
        ----------
        machinery : FuelCellMachinery
            燃料电池工程机械
        """
        self.fuel_cell_machinery[machinery.machinery_id] = machinery
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化氢能系统
        
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
        
        for facility_id, facility in self.production_facilities.items():
            hourly_production = facility.production_capacity * 0.8
            schedule = []
            
            for hour in range(time_horizon):
                production = hourly_production
                energy_cost = production * facility.energy_consumption * 0.8  # 元/kWh
                production_cost = production * facility.operating_cost
                total_cost += energy_cost + production_cost
                
                carbon = production * facility.carbon_emission
                total_carbon += carbon
                
                schedule.append({
                    'hour': hour,
                    'production': production,
                    'energy_cost': energy_cost,
                    'production_cost': production_cost,
                    'carbon': carbon
                })
            
            energy_schedule[facility_id] = schedule
            component_utilization[facility_id] = 0.8
        
        for storage_id, storage in self.storage_facilities.items():
            utilization = 0.6 + np.random.random() * 0.3
            component_utilization[storage_id] = utilization
            
            storage_cost = storage.capital_cost * 0.1 / time_horizon
            total_cost += storage_cost
        
        for station_id, station in self.refueling_stations.items():
            utilization = 0.5 + np.random.random() * 0.4
            component_utilization[station_id] = utilization
            
            station_cost = station.construction_cost * 0.1 / time_horizon
            total_cost += station_cost
        
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
                    'production_cost': total_cost * 0.5,
                    'storage_cost': total_cost * 0.2,
                    'refueling_cost': total_cost * 0.3
                },
                'emission_sources': {
                    'hydrogen_production': total_carbon
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
        
        for facility_id, facility in self.production_facilities.items():
            hourly_production = facility.production_capacity * 0.9
            schedule = []
            
            for hour in range(time_horizon):
                production = hourly_production
                carbon = production * facility.carbon_emission
                total_carbon += carbon
                
                schedule.append({
                    'hour': hour,
                    'production': production,
                    'carbon': carbon
                })
            
            energy_schedule[facility_id] = schedule
            component_utilization[facility_id] = 0.9
        
        for storage_id, storage in self.storage_facilities.items():
            component_utilization[storage_id] = 0.7
        
        for station_id, station in self.refueling_stations.items():
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
                    'hydrogen_production': total_carbon
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
        
        for facility_id, facility in self.production_facilities.items():
            schedule = []
            
            for hour in range(time_horizon):
                reliability = 0.9 + np.random.random() * 0.1
                reliability_score += reliability
                
                schedule.append({
                    'hour': hour,
                    'reliability': reliability
                })
            
            energy_schedule[facility_id] = schedule
            component_utilization[facility_id] = 0.75
        
        for storage_id, storage in self.storage_facilities.items():
            component_utilization[storage_id] = 0.8
            reliability_score += 0.95
        
        for station_id, station in self.refueling_stations.items():
            component_utilization[station_id] = 0.85
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
        
        for facility_id, facility in self.production_facilities.items():
            hourly_production = facility.production_capacity * 0.85
            schedule = []
            
            for hour in range(time_horizon):
                efficiency = facility.efficiency * (0.9 + np.random.random() * 0.1)
                efficiency_score += efficiency
                
                schedule.append({
                    'hour': hour,
                    'production': hourly_production,
                    'efficiency': efficiency
                })
            
            energy_schedule[facility_id] = schedule
            component_utilization[facility_id] = 0.85
        
        for storage_id, storage in self.storage_facilities.items():
            avg_efficiency = (storage.charge_efficiency + storage.discharge_efficiency) / 2
            component_utilization[storage_id] = 0.75
            efficiency_score += avg_efficiency
        
        for machinery_id, machinery in self.fuel_cell_machinery.items():
            component_utilization[machinery_id] = 0.8
            efficiency_score += machinery.fuel_cell_efficiency
        
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
        
        normalized_cost = cost_result.total_cost / 10000.0
        normalized_carbon = carbon_result.total_carbon_emissions / 1000.0
        normalized_efficiency = 1.0 - (efficiency_result.objective_value / 
                                        (len(self.production_facilities) + 
                                         len(self.storage_facilities) + 
                                         len(self.fuel_cell_machinery)))
        
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
    
    def calculate_refueling_schedule(
        self,
        machinery_id: str,
        station_id: str
    ) -> Dict[str, Any]:
        """计算加氢计划
        
        Parameters
        ----------
        machinery_id : str
            工程机械ID
        station_id : str
            加氢站ID
        
        Returns
        -------
        Dict[str, Any]
            加氢计划
        """
        if machinery_id not in self.fuel_cell_machinery:
            return {'error': '工程机械不存在'}
        
        if station_id not in self.refueling_stations:
            return {'error': '加氢站不存在'}
        
        machinery = self.fuel_cell_machinery[machinery_id]
        station = self.refueling_stations[station_id]
        
        required_hydrogen = machinery.hydrogen_tank_capacity - machinery.current_hydrogen_level
        refueling_time = required_hydrogen / station.refueling_capacity * 60  # 分钟
        
        cost = required_hydrogen * 30.0  # 元/kg
        
        return {
            'machinery_id': machinery_id,
            'station_id': station_id,
            'required_hydrogen': required_hydrogen,
            'refueling_time': refueling_time,
            'cost': cost,
            'refueling_pressure': station.refueling_pressure,
            'current_level': machinery.current_hydrogen_level,
            'target_level': machinery.hydrogen_tank_capacity
        }
    
    def optimize_hydrogen_storage_operation(
        self,
        storage_id: str,
        production_profile: pd.Series,
        demand_profile: pd.Series
    ) -> Dict[str, Any]:
        """优化储氢设施运行
        
        Parameters
        ----------
        storage_id : str
            储氢设施ID
        production_profile : pd.Series
            生产曲线
        demand_profile : pd.Series
            需求曲线
        
        Returns
        -------
        Dict[str, Any]
            运行优化结果
        """
        if storage_id not in self.storage_facilities:
            return {'error': '储氢设施不存在'}
        
        storage = self.storage_facilities[storage_id]
        
        hours = min(len(production_profile), len(demand_profile))
        schedule = []
        
        current_level = storage.current_level
        
        for hour in range(hours):
            production = production_profile.iloc[hour] if hour < len(production_profile) else 0
            demand = demand_profile.iloc[hour] if hour < len(demand_profile) else 0
            
            if production > demand:
                excess = production - demand
                max_charge = storage.capacity - current_level
                charge_amount = min(excess, max_charge)
                
                current_level = current_level + charge_amount * storage.charge_efficiency
                action = 'charge'
            elif demand > production:
                deficit = demand - production
                max_discharge = current_level - (storage.capacity * 0.1)
                discharge_amount = min(deficit, max_discharge)
                
                current_level = current_level - discharge_amount / storage.discharge_efficiency
                action = 'discharge'
            else:
                action = 'idle'
            
            schedule.append({
                'hour': hour,
                'action': action,
                'production': production,
                'demand': demand,
                'current_level': current_level,
                'capacity_utilization': current_level / storage.capacity
            })
        
        return {
            'storage_id': storage_id,
            'schedule': schedule,
            'total_charge_cycles': sum(1 for s in schedule if s['action'] == 'charge'),
            'total_discharge_cycles': sum(1 for s in schedule if s['action'] == 'discharge')
        }
    
    def generate_hydrogen_system_report(self) -> Dict[str, Any]:
        """生成氢能系统报告
        
        Returns
        -------
        Dict[str, Any]
            氢能系统报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        total_production_capacity = sum(
            facility.production_capacity * facility.operating_hours_per_day
            for facility in self.production_facilities.values()
        )
        
        total_storage_capacity = sum(
            storage.capacity for storage in self.storage_facilities.values()
        )
        
        total_refueling_capacity = sum(
            station.refueling_capacity * 24
            for station in self.refueling_stations.values()
        )
        
        total_hydrogen_demand = sum(
            machinery.hydrogen_consumption_rate * machinery.operating_hours_per_day
            for machinery in self.fuel_cell_machinery.values()
        )
        
        report = {
            'summary': {
                'total_production_facilities': len(self.production_facilities),
                'total_storage_facilities': len(self.storage_facilities),
                'total_refueling_stations': len(self.refueling_stations),
                'total_fuel_cell_machinery': len(self.fuel_cell_machinery),
                'total_production_capacity': total_production_capacity,
                'total_storage_capacity': total_storage_capacity,
                'total_refueling_capacity': total_refueling_capacity,
                'total_hydrogen_demand': total_hydrogen_demand,
                'supply_demand_ratio': total_production_capacity / total_hydrogen_demand if total_hydrogen_demand > 0 else 0,
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'production_facility_details': {},
            'storage_facility_details': {},
            'refueling_station_details': {},
            'machinery_details': {}
        }
        
        for facility_id, facility in self.production_facilities.items():
            report['production_facility_details'][facility_id] = {
                'method': facility.production_method.value,
                'location': facility.location,
                'production_capacity': facility.production_capacity,
                'energy_consumption': facility.energy_consumption,
                'efficiency': facility.efficiency,
                'carbon_emission': facility.carbon_emission,
                'operating_hours_per_day': facility.operating_hours_per_day,
                'capital_cost': facility.capital_cost,
                'operating_cost': facility.operating_cost
            }
        
        for storage_id, storage in self.storage_facilities.items():
            report['storage_facility_details'][storage_id] = {
                'type': storage.storage_type.value,
                'location': storage.location,
                'capacity': storage.capacity,
                'current_level': storage.current_level,
                'pressure': storage.pressure,
                'temperature': storage.temperature,
                'charge_efficiency': storage.charge_efficiency,
                'discharge_efficiency': storage.discharge_efficiency,
                'capital_cost': storage.capital_cost
            }
        
        for station_id, station in self.refueling_stations.items():
            report['refueling_station_details'][station_id] = {
                'location': station.location,
                'coordinates': station.coordinates,
                'refueling_capacity': station.refueling_capacity,
                'storage_capacity': station.storage_capacity,
                'number_of_dispensers': station.number_of_dispensers,
                'refueling_pressure': station.refueling_pressure,
                'service_level': station.service_level,
                'construction_cost': station.construction_cost,
                'annual_maintenance_cost': station.annual_maintenance_cost
            }
        
        for machinery_id, machinery in self.fuel_cell_machinery.items():
            report['machinery_details'][machinery_id] = {
                'type': machinery.machinery_type,
                'location': machinery.location,
                'fuel_cell_power': machinery.fuel_cell_power,
                'hydrogen_consumption_rate': machinery.hydrogen_consumption_rate,
                'fuel_cell_efficiency': machinery.fuel_cell_efficiency,
                'hydrogen_tank_capacity': machinery.hydrogen_tank_capacity,
                'current_hydrogen_level': machinery.current_hydrogen_level,
                'operating_hours_per_day': machinery.operating_hours_per_day,
                'daily_energy_demand': machinery.daily_energy_demand
            }
        
        return report