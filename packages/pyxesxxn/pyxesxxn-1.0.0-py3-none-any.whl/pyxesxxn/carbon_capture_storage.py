"""
CCS + 熔盐储能（MSES）低碳柔性CHP模块

该模块实现了碳捕集与封存（CCS）与熔盐储能（MSES）结合的低碳柔性热电联产系统，
并构建了扩展碳流（ECEF）模型，用于追踪能量流向、碳流向和时间维度的碳分布。

主要功能：
1. CCS系统建模：锅炉排放CO₂的捕集与处理
2. MSES系统建模：跨时间热量储存与释放
3. ECEF模型：能量-碳流耦合追踪
4. 碳定价基础：基于真实碳分布的经济分析
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum


class CarbonCaptureTechnology(Enum):
    """碳捕集技术类型"""
    POST_COMBUSTION = "post_combustion"  # 燃烧后捕集
    PRE_COMBUSTION = "pre_combustion"   # 燃烧前捕集
    OXYFUEL = "oxyfuel"                 # 富氧燃烧


class MoltenSaltType(Enum):
    """熔盐类型"""
    NITRATE = "nitrate"      # 硝酸盐熔盐
    CARBONATE = "carbonate"  # 碳酸盐熔盐
    CHLORIDE = "chloride"    # 氯化物熔盐


@dataclass
class CCSConfiguration:
    """CCS系统配置"""
    capture_efficiency: float  # 捕集效率 (0-1)
    energy_penalty: float     # 能耗惩罚系数
    capital_cost: float       # 单位容量投资成本 (元/kW)
    opex_cost: float         # 单位容量运维成本 (元/kW/年)
    technology: CarbonCaptureTechnology
    storage_capacity: float   # 封存容量 (tCO₂)


@dataclass
class MSESConfiguration:
    """熔盐储能系统配置"""
    storage_capacity: float   # 储热容量 (MWh)
    charge_efficiency: float  # 充电效率
    discharge_efficiency: float  # 放电效率
    heat_loss_rate: float    # 热损失率 (%/小时)
    salt_type: MoltenSaltType
    max_temperature: float   # 最高工作温度 (°C)
    min_temperature: float   # 最低工作温度 (°C)


@dataclass
class FlexibleCHPConfiguration:
    """柔性CHP系统配置"""
    power_capacity: float    # 发电容量 (MW)
    heat_capacity: float     # 供热容量 (MW)
    fuel_type: str          # 燃料类型
    efficiency_power: float  # 发电效率
    efficiency_heat: float   # 供热效率
    carbon_intensity: float  # 碳排放强度 (tCO₂/MWh)
    ramp_rate: float        # 爬坡速率 (MW/分钟)
    min_load: float         # 最小负荷率


class ECEFModel:
    """扩展碳流（ECEF）模型
    
    追踪能量流向、碳流向和时间维度的碳分布，为碳定价提供基础。
    """
    
    def __init__(self, time_horizon: int = 8760):
        self.time_horizon = time_horizon
        self.energy_flows = {}  # 能量流向记录
        self.carbon_flows = {}  # 碳流向记录
        self.temporal_carbon_distribution = np.zeros(time_horizon)
        
    def track_energy_flow(self, timestamp: int, source: str, destination: str, 
                         energy_type: str, quantity: float):
        """追踪能量流向"""
        key = f"{timestamp}_{source}_{destination}_{energy_type}"
        self.energy_flows[key] = {
            'timestamp': timestamp,
            'source': source,
            'destination': destination,
            'energy_type': energy_type,
            'quantity': quantity
        }
    
    def track_carbon_flow(self, timestamp: int, source: str, destination: str,
                         carbon_content: float, flow_type: str):
        """追踪碳流向"""
        key = f"{timestamp}_{source}_{destination}_{flow_type}"
        self.carbon_flows[key] = {
            'timestamp': timestamp,
            'source': source,
            'destination': destination,
            'carbon_content': carbon_content,
            'flow_type': flow_type
        }
        
        # 更新时间维度碳分布
        self.temporal_carbon_distribution[timestamp] += carbon_content
    
    def calculate_carbon_intensity_timeseries(self) -> np.ndarray:
        """计算时间序列碳强度"""
        # 这里可以基于能量流和碳流计算实时碳强度
        # 简化实现：返回时间序列碳强度
        return self.temporal_carbon_distribution / (np.sum(self.temporal_carbon_distribution) + 1e-10)
    
    def get_carbon_pricing_basis(self, carbon_price: float) -> Dict:
        """获取碳定价基础数据"""
        total_carbon = np.sum(self.temporal_carbon_distribution)
        avg_intensity = total_carbon / self.time_horizon if self.time_horizon > 0 else 0
        
        return {
            'total_carbon_emissions': total_carbon,
            'average_carbon_intensity': avg_intensity,
            'peak_carbon_intensity': np.max(self.temporal_carbon_distribution),
            'carbon_price_impact': total_carbon * carbon_price,
            'temporal_distribution': self.temporal_carbon_distribution
        }


class CCSMSESFlexibleCHP:
    """CCS + 熔盐储能低碳柔性CHP系统"""
    
    def __init__(self, chp_config: FlexibleCHPConfiguration,
                 ccs_config: CCSConfiguration,
                 mses_config: MSESConfiguration,
                 time_horizon: int = 8760):
        
        self.chp_config = chp_config
        self.ccs_config = ccs_config
        self.mses_config = mses_config
        self.time_horizon = time_horizon
        
        # 初始化ECEF模型
        self.ecef_model = ECEFModel(time_horizon)
        
        # 系统状态变量
        self.power_output = np.zeros(time_horizon)
        self.heat_output = np.zeros(time_horizon)
        self.carbon_emissions = np.zeros(time_horizon)
        self.carbon_captured = np.zeros(time_horizon)
        self.mses_charge_level = np.zeros(time_horizon)
        
        # 运行参数
        self.current_time = 0
        
    def simulate_timestep(self, power_demand: float, heat_demand: float, 
                         timestamp: int) -> Dict:
        """模拟单个时间步长"""
        
        # CHP基本运行
        power_output = min(power_demand, self.chp_config.power_capacity)
        heat_output = min(heat_demand, self.chp_config.heat_capacity)
        
        # 计算燃料消耗和碳排放
        fuel_consumption_power = power_output / self.chp_config.efficiency_power
        fuel_consumption_heat = heat_output / self.chp_config.efficiency_heat
        total_fuel_consumption = fuel_consumption_power + fuel_consumption_heat
        
        carbon_emissions = total_fuel_consumption * self.chp_config.carbon_intensity
        
        # CCS碳捕集
        carbon_captured = carbon_emissions * self.ccs_config.capture_efficiency
        net_carbon_emissions = carbon_emissions - carbon_captured
        
        # MSES运行逻辑
        excess_heat = max(0, heat_output - heat_demand)
        if excess_heat > 0 and self.mses_charge_level[timestamp-1] < self.mses_config.storage_capacity:
            # 充电模式
            charge_heat = min(excess_heat * self.mses_config.charge_efficiency,
                            self.mses_config.storage_capacity - self.mses_charge_level[timestamp-1])
            self.mses_charge_level[timestamp] = self.mses_charge_level[timestamp-1] + charge_heat
        elif heat_demand > heat_output and self.mses_charge_level[timestamp-1] > 0:
            # 放电模式
            discharge_heat = min((heat_demand - heat_output) / self.mses_config.discharge_efficiency,
                               self.mses_charge_level[timestamp-1])
            self.mses_charge_level[timestamp] = self.mses_charge_level[timestamp-1] - discharge_heat
            heat_output += discharge_heat * self.mses_config.discharge_efficiency
        else:
            self.mses_charge_level[timestamp] = self.mses_charge_level[timestamp-1] * (1 - self.mses_config.heat_loss_rate/100)
        
        # 更新系统状态
        self.power_output[timestamp] = power_output
        self.heat_output[timestamp] = heat_output
        self.carbon_emissions[timestamp] = carbon_emissions
        self.carbon_captured[timestamp] = carbon_captured
        
        # ECEF模型追踪
        self.ecef_model.track_energy_flow(timestamp, "CHP", "Grid", "electricity", power_output)
        self.ecef_model.track_energy_flow(timestamp, "CHP", "Heat_Network", "heat", heat_output)
        self.ecef_model.track_carbon_flow(timestamp, "CHP", "Atmosphere", net_carbon_emissions, "emission")
        self.ecef_model.track_carbon_flow(timestamp, "CHP", "CCS_Storage", carbon_captured, "capture")
        
        return {
            'power_output': power_output,
            'heat_output': heat_output,
            'carbon_emissions': carbon_emissions,
            'carbon_captured': carbon_captured,
            'net_carbon_emissions': net_carbon_emissions,
            'mses_charge_level': self.mses_charge_level[timestamp],
            'fuel_consumption': total_fuel_consumption
        }
    
    def run_simulation(self, power_demand_profile: np.ndarray, 
                      heat_demand_profile: np.ndarray) -> Dict:
        """运行完整仿真"""
        
        if len(power_demand_profile) != self.time_horizon or len(heat_demand_profile) != self.time_horizon:
            raise ValueError("需求曲线长度必须与时间范围匹配")
        
        results = []
        for t in range(self.time_horizon):
            result = self.simulate_timestep(power_demand_profile[t], 
                                          heat_demand_profile[t], t)
            results.append(result)
        
        # 计算系统性能指标
        total_power = np.sum(self.power_output)
        total_heat = np.sum(self.heat_output)
        total_carbon = np.sum(self.carbon_emissions)
        total_captured = np.sum(self.carbon_captured)
        
        carbon_reduction_rate = total_captured / total_carbon if total_carbon > 0 else 0
        
        return {
            'hourly_results': results,
            'summary': {
                'total_power_generation': total_power,
                'total_heat_generation': total_heat,
                'total_carbon_emissions': total_carbon,
                'total_carbon_captured': total_captured,
                'carbon_reduction_rate': carbon_reduction_rate,
                'average_power_output': np.mean(self.power_output),
                'average_heat_output': np.mean(self.heat_output),
                'capacity_factor_power': total_power / (self.chp_config.power_capacity * self.time_horizon),
                'capacity_factor_heat': total_heat / (self.chp_config.heat_capacity * self.time_horizon)
            },
            'ecef_model': self.ecef_model
        }
    
    def charge_mses(self, heat_input: float, duration: int) -> Dict:
        """熔盐储能充电操作"""
        # 计算实际存储的热量
        heat_stored = heat_input * self.mses_config.charge_efficiency
        
        # 确保不超过存储容量
        if self.mses_charge_level[self.current_time] + heat_stored > self.mses_config.storage_capacity:
            heat_stored = self.mses_config.storage_capacity - self.mses_charge_level[self.current_time]
        
        # 更新存储水平
        self.mses_charge_level[self.current_time] += heat_stored
        
        return {
            'heat_stored': heat_stored,
            'charge_efficiency': self.mses_config.charge_efficiency,
            'current_storage_level': self.mses_charge_level[self.current_time],
            'storage_capacity': self.mses_config.storage_capacity
        }
    
    def discharge_mses(self, heat_demand: float, duration: int) -> Dict:
        """熔盐储能放电操作"""
        # 计算可提供的热量
        available_heat = self.mses_charge_level[self.current_time] * self.mses_config.discharge_efficiency
        heat_supplied = min(heat_demand, available_heat)
        
        # 更新存储水平
        self.mses_charge_level[self.current_time] -= heat_supplied / self.mses_config.discharge_efficiency
        
        return {
            'heat_supplied': heat_supplied,
            'discharge_efficiency': self.mses_config.discharge_efficiency,
            'current_storage_level': self.mses_charge_level[self.current_time],
            'storage_capacity': self.mses_config.storage_capacity
        }
    
    def economic_analysis(self, electricity_price: float, heat_price: float,
                         carbon_price: float, fuel_price: float) -> Dict:
        """经济性分析"""
        
        total_revenue = (np.sum(self.power_output) * electricity_price + 
                        np.sum(self.heat_output) * heat_price)
        
        total_fuel_cost = (np.sum(self.power_output) / self.chp_config.efficiency_power + 
                          np.sum(self.heat_output) / self.chp_config.efficiency_heat) * fuel_price
        
        carbon_cost = np.sum(self.carbon_emissions - self.carbon_captured) * carbon_price
        
        # CCS和MSES运维成本
        ccs_opex = self.ccs_config.opex_cost * self.chp_config.power_capacity
        mses_opex = self.mses_config.storage_capacity * 100  # 简化假设
        
        total_opex = ccs_opex + mses_opex
        
        net_profit = total_revenue - total_fuel_cost - carbon_cost - total_opex
        
        return {
            'total_revenue': total_revenue,
            'fuel_cost': total_fuel_cost,
            'carbon_cost': carbon_cost,
            'opex_cost': total_opex,
            'net_profit': net_profit,
            'carbon_price_sensitivity': self.ecef_model.get_carbon_pricing_basis(carbon_price)
        }


def create_standard_ccs_mses_chp() -> CCSMSESFlexibleCHP:
    """创建标准CCS+MSES柔性CHP系统"""
    
    chp_config = FlexibleCHPConfiguration(
        power_capacity=100,      # 100 MW
        heat_capacity=80,        # 80 MW
        fuel_type="natural_gas",
        efficiency_power=0.45,   # 45%
        efficiency_heat=0.4,     # 40%
        carbon_intensity=0.2,    # 0.2 tCO₂/MWh
        ramp_rate=5,            # 5 MW/分钟
        min_load=0.3            # 30%
    )
    
    ccs_config = CCSConfiguration(
        capture_efficiency=0.9,   # 90%
        energy_penalty=0.15,     # 15%能耗惩罚
        capital_cost=1500,       # 1500元/kW
        opex_cost=50,            # 50元/kW/年
        technology=CarbonCaptureTechnology.POST_COMBUSTION,
        storage_capacity=100000  # 10万吨CO₂
    )
    
    mses_config = MSESConfiguration(
        storage_capacity=500,     # 500 MWh
        charge_efficiency=0.95,  # 95%
        discharge_efficiency=0.9, # 90%
        heat_loss_rate=0.1,      # 0.1%/小时
        salt_type=MoltenSaltType.NITRATE,
        max_temperature=565,     # 565°C
        min_temperature=290      # 290°C
    )
    
    return CCSMSESFlexibleCHP(chp_config, ccs_config, mses_config)


# 导出主要类和函数
__all__ = [
    'CCSMSESFlexibleCHP',
    'ECEFModel', 
    'CCSConfiguration',
    'MSESConfiguration',
    'FlexibleCHPConfiguration',
    'CarbonCaptureTechnology',
    'MoltenSaltType',
    'create_standard_ccs_mses_chp'
]