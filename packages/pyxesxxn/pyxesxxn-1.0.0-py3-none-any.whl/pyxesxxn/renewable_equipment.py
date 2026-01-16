"""
可再生能源设备模块

该模块实现了沼气CHPP（热电联产）、地源热泵和集中式/分布式光伏等新型设备，
扩展PyXESXXN的设备库，支持低碳能源系统的建模与优化。

主要功能：
1. 沼气CHPP系统：生物质能热电联产
2. 地源热泵系统：高效地热能利用
3. 光伏发电系统：集中式与分布式光伏
4. 设备性能模型：效率曲线、运行特性
5. 经济性分析：投资成本、运维成本、收益分析
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from scipy import interpolate


class BiogasSource(Enum):
    """沼气来源类型"""
    AGRICULTURAL_WASTE = "agricultural_waste"  # 农业废弃物
    MUNICIPAL_SOLID_WASTE = "msw"             # 城市固体废物
    INDUSTRIAL_WASTE = "industrial_waste"     # 工业废物
    LANDFILL_GAS = "landfill_gas"             # 填埋气


class HeatPumpType(Enum):
    """热泵类型"""
    GROUND_SOURCE = "ground_source"    # 地源热泵
    WATER_SOURCE = "water_source"      # 水源热泵
    AIR_SOURCE = "air_source"          # 空气源热泵


class PVSystemType(Enum):
    """光伏系统类型"""
    CENTRALIZED = "centralized"        # 集中式光伏
    DISTRIBUTED = "distributed"        # 分布式光伏
    ROOFTOP = "rooftop"                # 屋顶光伏
    BUILDING_INTEGRATED = "bipv"       # 建筑一体化光伏


@dataclass
class BiogasCHPPConfiguration:
    """沼气CHPP系统配置"""
    power_capacity: float           # 发电容量 (kW)
    heat_capacity: float            # 供热容量 (kW)
    biogas_consumption_rate: float  # 沼气消耗率 (m³/kWh)
    electrical_efficiency: float    # 发电效率
    thermal_efficiency: float       # 供热效率
    biogas_source: BiogasSource     # 沼气来源
    chp_ratio: float               # 热电比
    min_load: float                # 最小负荷率
    ramp_rate: float               # 爬坡速率 (kW/分钟)
    
    # 经济参数
    capital_cost: float            # 单位容量投资成本 (元/kW)
    opex_cost: float              # 单位容量运维成本 (元/kW/年)
    biogas_cost: float            # 沼气成本 (元/m³)
    lifetime: int                 # 使用寿命 (年)


@dataclass
class GeothermalHeatPumpConfiguration:
    """地源热泵系统配置"""
    heating_capacity: float        # 制热容量 (kW)
    cooling_capacity: float        # 制冷容量 (kW)
    cop_heating: float            # 制热能效比
    cop_cooling: float            # 制冷能效比
    heat_pump_type: HeatPumpType  # 热泵类型
    ground_temperature: float     # 地温 (°C)
    
    # 地热交换系统参数
    borehole_depth: float         # 钻孔深度 (m)
    borehole_spacing: float       # 钻孔间距 (m)
    heat_exchanger_type: str      # 换热器类型
    
    # 经济参数
    capital_cost: float          # 投资成本 (元/kW)
    opex_cost: float            # 运维成本 (元/kW/年)
    drilling_cost: float        # 钻孔成本 (元/m)
    lifetime: int               # 使用寿命 (年)


@dataclass
class PVSystemConfiguration:
    """光伏系统配置"""
    installed_capacity: float     # 安装容量 (kWp)
    system_type: PVSystemType     # 系统类型
    panel_efficiency: float       # 面板效率
    inverter_efficiency: float    # 逆变器效率
    tilt_angle: float            # 倾角 (度)
    azimuth: float               # 方位角 (度)
    
    # 性能参数
    performance_ratio: float     # 性能比
    degradation_rate: float      # 年衰减率
    temperature_coefficient: float  # 温度系数
    
    # 经济参数
    capital_cost: float         # 单位容量投资成本 (元/kWp)
    opex_cost: float           # 单位容量运维成本 (元/kWp/年)
    land_cost: float           # 土地成本 (集中式光伏)
    rooftop_cost: float        # 屋顶成本 (分布式光伏)
    lifetime: int              # 使用寿命 (年)


class BiogasCHPPSystem:
    """沼气热电联产系统"""
    
    def __init__(self, config: BiogasCHPPConfiguration):
        self.config = config
        self.current_power_output = 0.0
        self.current_heat_output = 0.0
        self.biogas_consumption = 0.0
        self.operating_hours = 0
        
    def operate(self, power_demand: float, heat_demand: float, 
               ambient_temperature: float = 20.0) -> Dict:
        """运行系统"""
        
        # 考虑环境温度对效率的影响
        temperature_factor = self._calculate_temperature_factor(ambient_temperature)
        
        # 确定运行模式
        if power_demand <= 0 and heat_demand <= 0:
            # 停机模式
            power_output = 0
            heat_output = 0
            biogas_consumption = 0
            operating_mode = "shutdown"
        else:
            # 运行模式
            power_output = min(power_demand, self.config.power_capacity)
            
            # 根据热电比调整热输出
            if power_output > 0:
                max_heat_from_power = power_output * self.config.chp_ratio
                heat_output = min(heat_demand, max_heat_from_power, self.config.heat_capacity)
            else:
                heat_output = min(heat_demand, self.config.heat_capacity)
            
            # 计算沼气消耗
            electrical_energy = power_output / (self.config.electrical_efficiency * temperature_factor)
            thermal_energy = heat_output / (self.config.thermal_efficiency * temperature_factor)
            total_energy_input = electrical_energy + thermal_energy
            
            biogas_consumption = total_energy_input * self.config.biogas_consumption_rate
            operating_mode = "chp" if power_output > 0 and heat_output > 0 else "power_only"
        
        # 更新系统状态
        self.current_power_output = power_output
        self.current_heat_output = heat_output
        self.biogas_consumption = biogas_consumption
        self.operating_hours += 1 if power_output > 0 or heat_output > 0 else 0
        
        return {
            'power_output': power_output,
            'heat_output': heat_output,
            'biogas_consumption': biogas_consumption,
            'operating_mode': operating_mode,
            'efficiency_electrical': self.config.electrical_efficiency * temperature_factor,
            'efficiency_thermal': self.config.thermal_efficiency * temperature_factor,
            'carbon_emissions_saved': self._calculate_carbon_savings(biogas_consumption)
        }
    
    def _calculate_temperature_factor(self, temperature: float) -> float:
        """计算温度影响因子"""
        # 简化模型：在15-25°C范围内效率最高
        optimal_temp = 20.0
        if 15 <= temperature <= 25:
            return 1.0
        elif temperature < 15:
            return 1.0 - 0.005 * (optimal_temp - temperature)
        else:
            return 1.0 - 0.008 * (temperature - optimal_temp)
    
    def _calculate_carbon_savings(self, biogas_consumption: float) -> float:
        """计算碳减排量"""
        # 沼气替代天然气的碳减排
        # 假设：沼气碳强度为0，天然气碳强度为0.2 tCO₂/MWh
        natural_gas_intensity = 0.2  # tCO₂/MWh
        energy_equivalent = biogas_consumption * 6.0  # 假设1m³沼气≈6kWh能量
        carbon_savings = energy_equivalent * natural_gas_intensity / 1000  # 转换为吨
        
        return carbon_savings
    
    def economic_analysis(self, electricity_price: float, heat_price: float, 
                         operating_hours: int) -> Dict:
        """经济性分析"""
        annual_revenue = (self.current_power_output * electricity_price + 
                         self.current_heat_output * heat_price) * operating_hours
        
        annual_fuel_cost = self.biogas_consumption * self.config.biogas_cost * operating_hours
        annual_opex = self.config.opex_cost * self.config.power_capacity
        
        capital_recovery = (self.config.capital_cost * self.config.power_capacity * 
                          0.08)  # 8%资本回收率
        
        annual_profit = annual_revenue - annual_fuel_cost - annual_opex - capital_recovery
        payback_period = (self.config.capital_cost * self.config.power_capacity) / max(annual_profit, 1e-10)
        
        return {
            'annual_revenue': annual_revenue,
            'annual_fuel_cost': annual_fuel_cost,
            'annual_opex': annual_opex,
            'capital_recovery': capital_recovery,
            'annual_profit': annual_profit,
            'payback_period': payback_period,
            'lcoe': self._calculate_lcoe(annual_revenue, operating_hours)
        }
    
    def _calculate_lcoe(self, annual_revenue: float, operating_hours: int) -> float:
        """计算平准化能源成本"""
        total_cost = (self.config.capital_cost * self.config.power_capacity + 
                     self.config.opex_cost * self.config.lifetime)
        total_energy = (self.current_power_output + self.current_heat_output) * operating_hours * self.config.lifetime
        
        return total_cost / max(total_energy, 1e-10)


class GeothermalHeatPumpSystem:
    """地源热泵系统"""
    
    def __init__(self, config: GeothermalHeatPumpConfiguration):
        self.config = config
        self.current_heating_output = 0.0
        self.current_cooling_output = 0.0
        self.electricity_consumption = 0.0
        self.ground_temperature_history = []
        
    def operate_heating(self, heat_demand: float, ambient_temperature: float,
                       electricity_price: float = 0.0) -> Dict:
        """运行制热模式"""
        
        # 计算实际COP（考虑地温和环境温度）
        effective_cop = self._calculate_effective_cop_heating(ambient_temperature)
        
        # 确定制热输出
        heating_output = min(heat_demand, self.config.heating_capacity)
        
        # 计算电力消耗
        if heating_output > 0:
            electricity_consumption = heating_output / effective_cop
        else:
            electricity_consumption = 0
        
        # 更新系统状态
        self.current_heating_output = heating_output
        self.current_cooling_output = 0
        self.electricity_consumption = electricity_consumption
        self.ground_temperature_history.append(self.config.ground_temperature)
        
        return {
            'heating_output': heating_output,
            'electricity_consumption': electricity_consumption,
            'effective_cop': effective_cop,
            'operating_cost': electricity_consumption * electricity_price,
            'carbon_reduction': self._calculate_heating_carbon_reduction(heating_output)
        }
    
    def operate_cooling(self, cooling_demand: float, ambient_temperature: float,
                       electricity_price: float = 0.0) -> Dict:
        """运行制冷模式"""
        
        # 计算实际COP
        effective_cop = self._calculate_effective_cop_cooling(ambient_temperature)
        
        # 确定制冷输出
        cooling_output = min(cooling_demand, self.config.cooling_capacity)
        
        # 计算电力消耗
        if cooling_output > 0:
            electricity_consumption = cooling_output / effective_cop
        else:
            electricity_consumption = 0
        
        # 更新系统状态
        self.current_heating_output = 0
        self.current_cooling_output = cooling_output
        self.electricity_consumption = electricity_consumption
        
        return {
            'cooling_output': cooling_output,
            'electricity_consumption': electricity_consumption,
            'effective_cop': effective_cop,
            'operating_cost': electricity_consumption * electricity_price,
            'carbon_reduction': self._calculate_cooling_carbon_reduction(cooling_output)
        }
    
    def _calculate_effective_cop_heating(self, ambient_temperature: float) -> float:
        """计算制热有效COP"""
        # 基于地温和环境温度的COP修正
        delta_t = self.config.ground_temperature - ambient_temperature
        cop_reduction = max(0, delta_t * 0.02)  # 每度温差降低2%
        return max(1.0, self.config.cop_heating * (1 - cop_reduction))
    
    def _calculate_effective_cop_cooling(self, ambient_temperature: float) -> float:
        """计算制冷有效COP"""
        delta_t = ambient_temperature - self.config.ground_temperature
        cop_reduction = max(0, delta_t * 0.015)  # 每度温差降低1.5%
        return max(1.0, self.config.cop_cooling * (1 - cop_reduction))
    
    def _calculate_heating_carbon_reduction(self, heating_output: float) -> float:
        """计算制热碳减排"""
        # 相对于燃气锅炉的碳减排
        gas_boiler_efficiency = 0.9
        gas_carbon_intensity = 0.2  # tCO₂/MWh
        
        gas_consumption = heating_output / gas_boiler_efficiency
        carbon_emissions_gas = gas_consumption * gas_carbon_intensity / 1000
        
        # 热泵的碳排放（假设电力碳强度为0.5 tCO₂/MWh）
        electricity_carbon_intensity = 0.5
        carbon_emissions_hp = self.electricity_consumption * electricity_carbon_intensity / 1000
        
        return max(0, carbon_emissions_gas - carbon_emissions_hp)
    
    def _calculate_cooling_carbon_reduction(self, cooling_output: float) -> float:
        """计算制冷碳减排"""
        # 相对于传统空调的碳减排
        traditional_ac_cop = 3.0
        electricity_carbon_intensity = 0.5  # tCO₂/MWh
        
        electricity_traditional = cooling_output / traditional_ac_cop
        carbon_emissions_traditional = electricity_traditional * electricity_carbon_intensity / 1000
        carbon_emissions_hp = self.electricity_consumption * electricity_carbon_intensity / 1000
        
        return max(0, carbon_emissions_traditional - carbon_emissions_hp)


class PVSystem:
    """光伏发电系统"""
    
    def __init__(self, config: PVSystemConfiguration, location_lat: float, location_lon: float):
        self.config = config
        self.location_lat = location_lat
        self.location_lon = location_lon
        self.generation_profile = None
        self.energy_generated = 0.0
        self.operating_hours = 0
        
    def calculate_generation(self, solar_irradiance: np.ndarray, 
                           ambient_temperature: np.ndarray, 
                           timestamp: pd.DatetimeIndex) -> np.ndarray:
        """计算发电量"""
        
        if len(solar_irradiance) != len(ambient_temperature) != len(timestamp):
            raise ValueError("输入数据长度必须一致")
        
        generation = np.zeros(len(solar_irradiance))
        
        for i, (irradiance, temperature, time) in enumerate(zip(solar_irradiance, ambient_temperature, timestamp)):
            # 考虑温度影响
            temperature_loss = self._calculate_temperature_loss(temperature)
            
            # 考虑倾角和方位角影响
            orientation_factor = self._calculate_orientation_factor(time)
            
            # 计算实际发电量
            dc_power = (irradiance * self.config.installed_capacity * 
                       self.config.panel_efficiency * orientation_factor * 
                       (1 - temperature_loss))
            
            # 逆变器转换
            ac_power = dc_power * self.config.inverter_efficiency * self.config.performance_ratio
            
            generation[i] = max(0, ac_power)
        
        self.generation_profile = generation
        self.energy_generated = np.sum(generation)
        self.operating_hours = len([x for x in generation if x > 0])
        
        return generation
    
    def _calculate_temperature_loss(self, temperature: float) -> float:
        """计算温度损失"""
        # 标准测试条件温度
        stc_temperature = 25.0
        temperature_difference = temperature - stc_temperature
        return self.config.temperature_coefficient * temperature_difference / 100
    
    def _calculate_orientation_factor(self, timestamp: pd.Timestamp) -> float:
        """计算方位角影响因子"""
        # 简化模型：基于太阳高度角和方位角
        # 这里可以使用更精确的太阳位置算法
        
        # 计算太阳高度角（简化）
        hour = timestamp.hour
        day_of_year = timestamp.dayofyear
        
        # 太阳高度角近似计算
        solar_altitude = 90 - abs(self.location_lat - 23.5 * np.sin(2 * np.pi * (day_of_year - 81) / 365))
        solar_altitude = max(0, solar_altitude - (12 - abs(hour - 12)) * 15)
        
        if solar_altitude <= 0:
            return 0.0
        
        # 方位角匹配度
        optimal_azimuth = 180 if self.location_lat >= 0 else 0  # 北半球朝南，南半球朝北
        azimuth_diff = abs(self.config.azimuth - optimal_azimuth)
        azimuth_factor = max(0, 1 - azimuth_diff / 180)
        
        # 倾角优化
        optimal_tilt = self.location_lat
        tilt_diff = abs(self.config.tilt_angle - optimal_tilt)
        tilt_factor = max(0, 1 - tilt_diff / 90)
        
        return azimuth_factor * tilt_factor * (solar_altitude / 90)
    
    def economic_analysis(self, electricity_price: float, 
                         feed_in_tariff: float = 0.0) -> Dict:
        """经济性分析"""
        
        if self.generation_profile is None:
            raise ValueError("请先调用calculate_generation方法计算发电量")
        
        annual_energy = self.energy_generated
        
        # 收入计算
        energy_self_consumed = annual_energy * 0.3  # 假设30%自用
        energy_exported = annual_energy - energy_self_consumed
        
        annual_revenue = (energy_self_consumed * electricity_price + 
                         energy_exported * feed_in_tariff)
        
        # 成本计算
        capital_cost = self.config.capital_cost * self.config.installed_capacity
        
        if self.config.system_type == PVSystemType.CENTRALIZED:
            capital_cost += self.config.land_cost
        elif self.config.system_type in [PVSystemType.ROOFTOP, PVSystemType.BUILDING_INTEGRATED]:
            capital_cost += self.config.rooftop_cost
        
        annual_opex = self.config.opex_cost * self.config.installed_capacity
        
        # 平准化成本计算
        total_cost = capital_cost + annual_opex * self.config.lifetime
        lcoe = total_cost / (annual_energy * self.config.lifetime)
        
        # 投资回收期
        annual_profit = annual_revenue - annual_opex
        payback_period = capital_cost / max(annual_profit, 1e-10)
        
        return {
            'annual_energy_generation': annual_energy,
            'annual_revenue': annual_revenue,
            'capital_cost': capital_cost,
            'annual_opex': annual_opex,
            'lcoe': lcoe,
            'payback_period': payback_period,
            'capacity_factor': annual_energy / (self.config.installed_capacity * 8760)
        }


def create_standard_biogas_chpp() -> BiogasCHPPSystem:
    """创建标准沼气CHPP系统"""
    config = BiogasCHPPConfiguration(
        power_capacity=500,           # 500 kW
        heat_capacity=400,            # 400 kW
        biogas_consumption_rate=0.25, # 0.25 m³/kWh
        electrical_efficiency=0.35,   # 35%
        thermal_efficiency=0.45,      # 45%
        biogas_source=BiogasSource.AGRICULTURAL_WASTE,
        chp_ratio=1.2,               # 热电比1.2
        min_load=0.4,                # 40%
        ramp_rate=10,                # 10 kW/分钟
        capital_cost=8000,           # 8000元/kW
        opex_cost=200,               # 200元/kW/年
        biogas_cost=1.5,             # 1.5元/m³
        lifetime=20                  # 20年
    )
    return BiogasCHPPSystem(config)


def create_standard_geothermal_heat_pump() -> GeothermalHeatPumpSystem:
    """创建标准地源热泵系统"""
    config = GeothermalHeatPumpConfiguration(
        heating_capacity=100,         # 100 kW
        cooling_capacity=80,          # 80 kW
        cop_heating=4.0,             # COP 4.0
        cop_cooling=5.0,             # COP 5.0
        heat_pump_type=HeatPumpType.GROUND_SOURCE,
        ground_temperature=15.0,     # 15°C地温
        borehole_depth=100,          # 100米
        borehole_spacing=5,          # 5米间距
        heat_exchanger_type="U-tube",
        capital_cost=3000,           # 3000元/kW
        opex_cost=100,               # 100元/kW/年
        drilling_cost=500,           # 500元/米
        lifetime=25                  # 25年
    )
    return GeothermalHeatPumpSystem(config)


def create_standard_pv_system() -> PVSystem:
    """创建标准光伏系统"""
    config = PVSystemConfiguration(
        installed_capacity=100,       # 100 kWp
        system_type=PVSystemType.DISTRIBUTED,
        panel_efficiency=0.18,        # 18%
        inverter_efficiency=0.96,     # 96%
        tilt_angle=30,               # 30度倾角
        azimuth=180,                 # 朝南
        performance_ratio=0.85,      # 85%
        degradation_rate=0.005,      # 0.5%/年
        temperature_coefficient=0.004, # -0.4%/°C
        capital_cost=5000,           # 5000元/kWp
        opex_cost=50,                # 50元/kWp/年
        land_cost=0,                 # 分布式无土地成本
        rooftop_cost=200,            # 200元/kWp屋顶成本
        lifetime=25                  # 25年
    )
    return PVSystem(config, location_lat=39.9, location_lon=116.4)  # 北京坐标


# 导出主要类和函数
__all__ = [
    'BiogasCHPPSystem',
    'GeothermalHeatPumpSystem',
    'PVSystem',
    'BiogasCHPPConfiguration',
    'GeothermalHeatPumpConfiguration',
    'PVSystemConfiguration',
    'BiogasSource',
    'HeatPumpType',
    'PVSystemType',
    'create_standard_biogas_chpp',
    'create_standard_geothermal_heat_pump',
    'create_standard_pv_system'
]