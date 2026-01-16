"""Emerging technology components."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

from pyxesxxn.energy_components.base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    register_component_factory,
    calculate_carnot_efficiency
)


@dataclass
class EmergingTechnologyConfig(ExtendedEquipmentConfig):
    """Configuration for emerging technology components."""
    pass


class MagneticConfinementFusionReactor(ExtendedEnergyComponent):
    """磁约束核聚变实验堆（概念）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[EmergingTechnologyConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['plasma_temperature'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'fusion_power': 500.0,  # MW
            'q_ratio': 10.0,  # 能量增益比
            'plasma_temperature': 150.0,  # 百万°C
            'magnetic_field_strength': 5.0,  # T
            'plasma_density': 1.0e20,  # m⁻³
            'confinement_time': 5.0,  # s
            'energy_injection_power': 50.0,  # MW
            'coolant_type': 'water'
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算磁约束核聚变实验堆的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示等离子体温度（百万°C）
        plasma_temp = input_power
        
        # 获取当前等离子体温度
        current_temp = self._current_state.get('plasma_temperature', 0.0)
        new_temp = plasma_temp
        
        # 计算能量增益比
        q_ratio = params.get('q_ratio', 10.0)
        
        # 计算输入能量（MW）
        energy_injection = params.get('energy_injection_power', 50.0)
        
        # 计算输出能量（MW）
        fusion_power = energy_injection * q_ratio
        
        # 计算热效率
        thermal_efficiency = 0.4  # 假设
        electrical_power = fusion_power * thermal_efficiency
        
        # 计算冷却需求
        heat_to_cool = fusion_power * (1 - thermal_efficiency)
        
        # 计算能量平衡
        energy_balance = fusion_power - energy_injection
        
        return {
            'plasma_temperature': new_temp,
            'fusion_power': fusion_power,
            'energy_injection': energy_injection,
            'electrical_power': electrical_power,
            'energy_balance': energy_balance,
            'q_ratio': q_ratio,
            'thermal_efficiency': thermal_efficiency,
            'heat_to_cool': heat_to_cool,
            'magnetic_field_strength': params.get('magnetic_field_strength', 5.0)
        }


class SpaceSolarPowerStation(ExtendedEnergyComponent):
    """空间光伏电站（微波输电）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[EmergingTechnologyConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'solar_panel_area': 10000.0,  # m²
            'solar_irradiance': 1367.0,  # W/m² (太空)
            'panel_efficiency': 0.35,  # 35%
            'microwave_conversion_efficiency': 0.85,  # 85%
            'transmission_efficiency': 0.90,  # 90%
            'rectenna_efficiency': 0.80,  # 80%
            'operating_orbit': 'geostationary',
            'microwave_frequency': 2.45,  # GHz
            'beam_divergence': 0.01  # rad
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算空间光伏电站的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示太阳辐照度变化系数 (0-2)
        irradiance_factor = input_power
        
        # 计算太阳能收集功率 (kW)
        irradiance = params.get('solar_irradiance', 1367.0) * irradiance_factor
        panel_area = params.get('panel_efficiency', 0.35)
        panel_eff = params.get('panel_efficiency', 0.35)
        solar_power = irradiance * panel_area * panel_eff / 1000  # kW
        
        # 计算微波转换功率 (kW)
        microwave_eff = params.get('microwave_conversion_efficiency', 0.85)
        microwave_power = solar_power * microwave_eff
        
        # 计算传输功率 (kW)
        transmission_eff = params.get('transmission_efficiency', 0.90)
        transmitted_power = microwave_power * transmission_eff
        
        # 计算接收功率 (kW)
        rectenna_eff = params.get('rectenna_efficiency', 0.80)
        received_power = transmitted_power * rectenna_eff
        
        # 计算总效率
        total_efficiency = panel_eff * microwave_eff * transmission_eff * rectenna_eff
        
        return {
            'solar_power': solar_power,
            'microwave_power': microwave_power,
            'transmitted_power': transmitted_power,
            'received_power': received_power,
            'total_efficiency': total_efficiency,
            'panel_efficiency': panel_eff,
            'microwave_conversion_efficiency': microwave_eff,
            'transmission_efficiency': transmission_eff,
            'rectenna_efficiency': rectenna_eff,
            'irradiance_factor': irradiance_factor
        }


class OceanThermalEnergyConversion(ExtendedEnergyComponent):
    """海洋温差发电物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[EmergingTechnologyConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'warm_water_temperature': 25.0,  # °C
            'cold_water_temperature': 5.0,  # °C
            'working_fluid': 'ammonia',
            'turbine_efficiency': 0.85,
            'pump_efficiency': 0.75,
            'heat_exchanger_efficiency': 0.80,
            'max_power_output': 1000.0,  # kW
            'flow_rate': 10000.0,  # m³/h
            'plant_type': 'closed_cycle'
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算海洋温差发电的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示温差 (°C)
        temp_diff = input_power
        
        # 获取温海水和冷海水温度
        warm_temp = params.get('warm_water_temperature', 25.0)
        cold_temp = warm_temp - temp_diff
        
        # 计算卡诺效率
        t_high = warm_temp + 273.15  # K
        t_low = cold_temp + 273.15  # K
        carnot_eff = calculate_carnot_efficiency(t_high, t_low)
        
        # 计算实际效率
        turbine_eff = params.get('turbine_efficiency', 0.85)
        pump_eff = params.get('pump_efficiency', 0.75)
        heat_exchanger_eff = params.get('heat_exchanger_efficiency', 0.80)
        actual_efficiency = carnot_eff * turbine_eff * pump_eff * heat_exchanger_eff
        
        # 计算功率输出
        flow_rate = params.get('flow_rate', 10000.0)  # m³/h
        water_density = 1000.0  # kg/m³
        water_cp = 4.186  # kJ/kg·°C
        
        # 计算热流量 (kW)
        heat_flow = (flow_rate * water_density * water_cp * temp_diff) / 3600
        
        # 计算功率输出 (kW)
        power_output = heat_flow * actual_efficiency
        
        return {
            'power_output': power_output,
            'warm_water_temperature': warm_temp,
            'cold_water_temperature': cold_temp,
            'temperature_difference': temp_diff,
            'carnot_efficiency': carnot_eff,
            'actual_efficiency': actual_efficiency,
            'heat_flow': heat_flow,
            'turbine_efficiency': turbine_eff,
            'pump_efficiency': pump_eff
        }


class SuperconductingMagneticEnergyStorage(ExtendedEnergyComponent):
    """超导储能（SMES）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[EmergingTechnologyConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['stored_energy'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'max_energy_storage': 100.0,  # kWh
            'power_capacity': 500.0,  # kW
            'charge_efficiency': 0.98,
            'discharge_efficiency': 0.98,
            'round_trip_efficiency': 0.96,
            'response_time': 0.01,  # s
            'operating_temperature': -269.0,  # °C (氦温)
            'magnetic_field_strength': 2.0,  # T
            'superconductor_type': 'NbTi'
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算超导储能的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示充放电功率 (kW)
        power = input_power
        
        # 获取当前存储能量
        current_energy = self._current_state.get('stored_energy', 0.0)
        max_energy = params.get('max_energy_storage', 100.0)
        
        # 计算新的存储能量
        if power > 0:  # 充电
            charge_eff = params.get('charge_efficiency', 0.98)
            energy_added = power * time_step * charge_eff
            new_energy = min(current_energy + energy_added, max_energy)
        else:  # 放电
            discharge_eff = params.get('discharge_efficiency', 0.98)
            energy_removed = abs(power) * time_step / discharge_eff
            new_energy = max(0.0, current_energy - energy_removed)
        
        # 计算实际充放电功率
        actual_power = (new_energy - current_energy) / time_step
        
        # 计算充放电效率
        efficiency = params.get('charge_efficiency', 0.98) if power > 0 else params.get('discharge_efficiency', 0.98)
        
        # 更新状态
        self._current_state['stored_energy'] = new_energy
        
        return {
            'stored_energy': new_energy,
            'input_power': power,
            'actual_power': actual_power,
            'efficiency': efficiency,
            'max_energy_storage': max_energy,
            'state_of_charge': new_energy / max_energy,
            'response_time': params.get('response_time', 0.01)
        }


class GravityEnergyStorage(ExtendedEnergyComponent):
    """重力储能（斜坡重块）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[EmergingTechnologyConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['height'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'max_energy_storage': 500.0,  # kWh
            'power_capacity': 250.0,  # kW
            'charge_efficiency': 0.90,
            'discharge_efficiency': 0.90,
            'round_trip_efficiency': 0.81,
            'mass': 100000.0,  # kg
            'max_height': 200.0,  # m
            'ramp_rate': 100.0,  # kW/s
            'friction_loss': 0.05
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算重力储能的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示充放电功率 (kW)
        power = input_power
        
        # 获取当前高度
        current_height = self._current_state.get('height', 0.0)
        max_height = params.get('max_height', 200.0)
        mass = params.get('mass', 100000.0)
        g = 9.81  # m/s²
        
        # 计算势能变化
        if power > 0:  # 充电（提升重物）
            charge_eff = params.get('charge_efficiency', 0.90)
            energy_added = power * time_step * charge_eff
            height_increase = energy_added * 3600 / (mass * g)  # m
            new_height = min(current_height + height_increase, max_height)
        else:  # 放电（下降重物）
            discharge_eff = params.get('discharge_efficiency', 0.90)
            energy_removed = abs(power) * time_step / discharge_eff
            height_decrease = energy_removed * 3600 / (mass * g)  # m
            new_height = max(0.0, current_height - height_decrease)
        
        # 计算实际充放电功率
        height_change = new_height - current_height
        energy_change = mass * g * height_change / 3600  # kWh
        actual_power = energy_change / time_step
        
        # 计算充放电效率
        efficiency = params.get('charge_efficiency', 0.90) if power > 0 else params.get('discharge_efficiency', 0.90)
        
        # 计算存储容量
        stored_energy = mass * g * new_height / 3600  # kWh
        
        # 更新状态
        self._current_state['height'] = new_height
        
        return {
            'stored_energy': stored_energy,
            'height': new_height,
            'input_power': power,
            'actual_power': actual_power,
            'efficiency': efficiency,
            'max_energy_storage': params.get('max_energy_storage', 500.0),
            'state_of_charge': stored_energy / params.get('max_energy_storage', 500.0)
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.MAGNETIC_CONFINEMENT_FUSION_REACTOR, MagneticConfinementFusionReactor)
register_component_factory(ExtendedEquipmentType.SPACE_SOLAR_POWER_STATION, SpaceSolarPowerStation)
register_component_factory(ExtendedEquipmentType.OCEAN_THERMAL_ENERGY_CONVERSION, OceanThermalEnergyConversion)
register_component_factory(ExtendedEquipmentType.ARTIFICIAL_PHOTOSYNTHESIS_DEVICE, OceanThermalEnergyConversion)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.SUPERCONDUCTING_MAGNETIC_ENERGY_STORAGE, SuperconductingMagneticEnergyStorage)
register_component_factory(ExtendedEquipmentType.GRAVITY_ENERGY_STORAGE, GravityEnergyStorage)
register_component_factory(ExtendedEquipmentType.THERMOACOUSTIC_POWER_GENERATOR, OceanThermalEnergyConversion)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.RADIOISOTOPE_THERMOELECTRIC_GENERATOR, OceanThermalEnergyConversion)  # 暂时使用相似模型


# 模块导出
__all__ = [
    'MagneticConfinementFusionReactor',
    'SpaceSolarPowerStation',
    'OceanThermalEnergyConversion',
    'SuperconductingMagneticEnergyStorage',
    'GravityEnergyStorage'
]