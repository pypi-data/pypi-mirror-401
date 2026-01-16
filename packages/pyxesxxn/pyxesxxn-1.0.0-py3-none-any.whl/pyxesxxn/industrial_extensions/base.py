"""
工业扩展模块基础框架

提供所有工业扩展模块的基础类和通用功能
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class MachineryType(Enum):
    """工程机械类型枚举"""
    EXCAVATOR = "excavator"
    LOADER = "loader"
    CRANE = "crane"
    BULLDOZER = "bulldozer"
    DUMP_TRUCK = "dump_truck"
    CONCRETE_MIXER = "concrete_mixer"
    ROLLER = "roller"
    FORKLIFT = "forklift"


class EnergySource(Enum):
    """能源类型枚举"""
    ELECTRICITY = "electricity"
    HYDROGEN = "hydrogen"
    DIESEL = "diesel"
    NATURAL_GAS = "natural_gas"
    BATTERY = "battery"
    HYBRID = "hybrid"


class OptimizationObjective(Enum):
    """优化目标枚举"""
    COST = "cost"
    CARBON = "carbon"
    RELIABILITY = "reliability"
    EFFICIENCY = "efficiency"
    MULTI_OBJECTIVE = "multi_objective"


@dataclass
class MachineryConfig:
    """工程机械配置"""
    machinery_id: str
    machinery_type: MachineryType
    power_rating: float  # kW
    energy_source: EnergySource
    battery_capacity: Optional[float] = None  # kWh
    hydrogen_capacity: Optional[float] = None  # kg
    fuel_consumption_rate: Optional[float] = None  # L/h or kg/h
    operating_hours_per_day: float = 8.0
    daily_energy_demand: Optional[float] = None  # kWh/day
    location: Optional[str] = None
    coordinates: Optional[tuple] = None


@dataclass
class EnergyPriceProfile:
    """能源价格配置"""
    electricity_price: Dict[str, float] = field(default_factory=dict)  # 元/kWh by time period
    hydrogen_price: float = 30.0  # 元/kg
    diesel_price: float = 8.0  # 元/L
    natural_gas_price: float = 4.0  # 元/m³
    peak_hours: List[str] = field(default_factory=lambda: ["08:00-12:00", "18:00-22:00"])


@dataclass
class CarbonEmissionFactors:
    """碳排放因子配置"""
    electricity: float = 0.4  # kg CO2/kWh
    hydrogen: float = 0.0  # kg CO2/kg (green hydrogen)
    diesel: float = 2.68  # kg CO2/L
    natural_gas: float = 2.0  # kg CO2/m³


@dataclass
class OptimizationResult:
    """优化结果"""
    success: bool
    objective_value: float
    total_cost: float
    total_carbon_emissions: float
    energy_schedule: Dict[str, Any]
    component_utilization: Dict[str, float]
    convergence_time: float
    error_message: Optional[str] = None
    additional_metrics: Dict[str, Any] = field(default_factory=dict)


class BaseIndustrialExtension(ABC):
    """工业扩展模块基类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化基类
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数
        """
        self.config = config or {}
        self.initialized = False
        self.results = {}
        self.metadata = {
            'created_at': datetime.now(),
            'version': '1.0.0',
            'module_name': self.__class__.__name__
        }
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        pass
    
    @abstractmethod
    def optimize(self, **kwargs) -> OptimizationResult:
        """执行优化
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        pass
    
    def get_results(self) -> Dict[str, Any]:
        """获取结果
        
        Returns
        -------
        Dict[str, Any]
            结果字典
        """
        return self.results
    
    def get_metadata(self) -> Dict[str, Any]:
        """获取元数据
        
        Returns
        -------
        Dict[str, Any]
            元数据字典
        """
        return self.metadata
    
    def validate_config(self) -> bool:
        """验证配置
        
        Returns
        -------
        bool
            配置是否有效
        """
        return True
    
    def reset(self):
        """重置模块状态"""
        self.results = {}
        self.initialized = False


class EnergyCalculator:
    """能源计算工具类"""
    
    @staticmethod
    def calculate_energy_consumption(
        power_rating: float,
        operating_hours: float,
        efficiency: float = 0.85
    ) -> float:
        """计算能源消耗
        
        Parameters
        ----------
        power_rating : float
            额定功率 (kW)
        operating_hours : float
            运行小时数
        efficiency : float
            效率
        
        Returns
        -------
        float
            能源消耗 (kWh)
        """
        return power_rating * operating_hours / efficiency
    
    @staticmethod
    def calculate_carbon_emissions(
        energy_consumption: float,
        emission_factor: float
    ) -> float:
        """计算碳排放
        
        Parameters
        ----------
        energy_consumption : float
            能源消耗
        emission_factor : float
            排放因子
        
        Returns
        -------
        float
            碳排放量 (kg CO2)
        """
        return energy_consumption * emission_factor
    
    @staticmethod
    def calculate_cost(
        energy_consumption: float,
        price: float
    ) -> float:
        """计算成本
        
        Parameters
        ----------
        energy_consumption : float
            能源消耗
        price : float
            单价
        
        Returns
        -------
        float
            成本
        """
        return energy_consumption * price
    
    @staticmethod
    def calculate_battery_soc(
        current_soc: float,
        charging_power: float,
        charging_time: float,
        battery_capacity: float,
        efficiency: float = 0.95
    ) -> float:
        """计算电池荷电状态
        
        Parameters
        ----------
        current_soc : float
            当前SOC (0-1)
        charging_power : float
            充电功率 (kW)
        charging_time : float
            充电时间 (h)
        battery_capacity : float
            电池容量 (kWh)
        efficiency : float
            充电效率
        
        Returns
        -------
        float
            新的SOC (0-1)
        """
        energy_charged = charging_power * charging_time * efficiency
        new_soc = current_soc + energy_charged / battery_capacity
        return min(max(new_soc, 0.0), 1.0)


class TimeSeriesGenerator:
    """时间序列生成器"""
    
    @staticmethod
    def generate_hourly_profile(
        base_value: float,
        variation: float = 0.2,
        days: int = 1
    ) -> pd.Series:
        """生成小时级时间序列
        
        Parameters
        ----------
        base_value : float
            基准值
        variation : float
            变化幅度
        days : int
            天数
        
        Returns
        -------
        pd.Series
            时间序列
        """
        hours = days * 24
        np.random.seed(42)
        values = base_value * (1 + np.random.uniform(-variation, variation, hours))
        index = pd.date_range(start='2024-01-01', periods=hours, freq='H')
        return pd.Series(values, index=index)
    
    @staticmethod
    def generate_daily_profile(
        base_value: float,
        variation: float = 0.15,
        days: int = 30
    ) -> pd.Series:
        """生成日级时间序列
        
        Parameters
        ----------
        base_value : float
            基准值
        variation : float
            变化幅度
        days : int
            天数
        
        Returns
        -------
        pd.Series
            时间序列
        """
        np.random.seed(42)
        values = base_value * (1 + np.random.uniform(-variation, variation, days))
        index = pd.date_range(start='2024-01-01', periods=days, freq='D')
        return pd.Series(values, index=index)


class ResultAnalyzer:
    """结果分析器"""
    
    @staticmethod
    def analyze_cost_breakdown(
        optimization_result: OptimizationResult
    ) -> Dict[str, Any]:
        """分析成本分解
        
        Parameters
        ----------
        optimization_result : OptimizationResult
            优化结果
        
        Returns
        -------
        Dict[str, Any]
            成本分解分析
        """
        return {
            'total_cost': optimization_result.total_cost,
            'cost_per_kwh': optimization_result.total_cost / 
                          sum(optimization_result.energy_schedule.values()) if 
                          optimization_result.energy_schedule else 0,
            'cost_components': optimization_result.additional_metrics.get('cost_components', {})
        }
    
    @staticmethod
    def analyze_carbon_emissions(
        optimization_result: OptimizationResult
    ) -> Dict[str, Any]:
        """分析碳排放
        
        Parameters
        ----------
        optimization_result : OptimizationResult
            优化结果
        
        Returns
        -------
        Dict[str, Any]
            碳排放分析
        """
        return {
            'total_emissions': optimization_result.total_carbon_emissions,
            'emission_intensity': optimization_result.total_carbon_emissions / 
                                 optimization_result.total_cost if 
                                 optimization_result.total_cost > 0 else 0,
            'emission_sources': optimization_result.additional_metrics.get('emission_sources', {})
        }
    
    @staticmethod
    def analyze_utilization(
        optimization_result: OptimizationResult
    ) -> Dict[str, Any]:
        """分析设备利用率
        
        Parameters
        ----------
        optimization_result : OptimizationResult
            优化结果
        
        Returns
        -------
        Dict[str, Any]
            利用率分析
        """
        utilization = optimization_result.component_utilization
        return {
            'average_utilization': np.mean(list(utilization.values())) if utilization else 0,
            'min_utilization': min(utilization.values()) if utilization else 0,
            'max_utilization': max(utilization.values()) if utilization else 0,
            'utilization_by_component': utilization
        }