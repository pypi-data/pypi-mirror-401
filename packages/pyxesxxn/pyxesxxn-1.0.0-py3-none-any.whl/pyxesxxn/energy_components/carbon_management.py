"""Carbon management system components."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

from pyxesxxn.energy_components.base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    register_component_factory,
    calculate_thermodynamic_state
)


@dataclass
class CarbonManagementConfig(ExtendedEquipmentConfig):
    """Configuration for carbon management system components."""
    pass


class PostCombustionCarbonCapture(ExtendedEnergyComponent):
    """燃烧后碳捕集（胺吸收）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CarbonManagementConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'capture_efficiency': 0.90,
            'energy_consumption': 3.0,  # MJ/kg CO2
            'amine_concentration': 0.3,  # MEA浓度 (30%)
            'operating_temperature': 40.0,  # °C (吸收塔)
            'regenerator_temperature': 120.0,  # °C (再生塔)
            'pressure': 1.0  # bar
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算燃烧后碳捕集装置的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示烟气流量 (kg/h)，假设烟气中CO2浓度为15%
        flue_gas_flow = input_power
        co2_concentration = 0.15  # 15%
        
        # 计算CO2输入量 (kg/h)
        co2_input = flue_gas_flow * co2_concentration
        
        # 计算捕集的CO2量 (kg/h)
        capture_eff = params.get('capture_efficiency', 0.90)
        co2_captured = co2_input * capture_eff
        
        # 计算能量消耗 (kW)
        energy_per_kg = params.get('energy_consumption', 3.0)
        energy_consumed = (co2_captured * energy_per_kg * 1000) / 3600
        
        # 计算热力学状态
        thermo_state = calculate_thermodynamic_state(
            params.get('operating_temperature', 40.0),
            params.get('pressure', 1.0),
            {'cp': 1.0, 'density': 1.0}
        )
        
        return {
            'flue_gas_flow': flue_gas_flow,
            'co2_input': co2_input,
            'co2_captured': co2_captured,
            'capture_efficiency': capture_eff,
            'energy_consumed': energy_consumed,
            'energy_per_kg_co2': energy_per_kg,
            'temperature': params.get('operating_temperature', 40.0),
            'pressure': params.get('pressure', 1.0),
            'thermodynamic_state': thermo_state
        }


class DirectAirCapture(ExtendedEnergyComponent):
    """直接空气捕集（DAC）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CarbonManagementConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'capture_efficiency': 0.95,
            'energy_consumption': 9.0,  # MJ/kg CO2
            'air_flow_rate': 10000.0,  # m³/h
            'co2_concentration_in_air': 0.0004,  # 400 ppm
            'operating_temperature': 50.0,  # °C
            'pressure': 1.0  # bar
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算直接空气捕集装置的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示电力输入 (kW)
        power_input = input_power
        
        # 计算CO2捕集量 (kg/h)
        energy_per_kg = params.get('energy_consumption', 9.0)
        co2_captured = (power_input * 3600) / (energy_per_kg * 1000)
        
        # 计算所需空气流量 (m³/h)
        co2_air = params.get('co2_concentration_in_air', 0.0004)
        air_flow_needed = (co2_captured / co2_air) / 1.225  # 1.225 kg/m³ 空气密度
        
        # 计算捕集效率
        capture_eff = params.get('capture_efficiency', 0.95)
        
        return {
            'power_input': power_input,
            'co2_captured': co2_captured,
            'air_flow_needed': air_flow_needed,
            'capture_efficiency': capture_eff,
            'energy_consumed': power_input,
            'energy_per_kg_co2': energy_per_kg,
            'temperature': params.get('operating_temperature', 50.0),
            'pressure': params.get('pressure', 1.0)
        }


class CO2Compressor(ExtendedEnergyComponent):
    """二氧化碳压缩机物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CarbonManagementConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'efficiency': 0.75,
            'inlet_pressure': 1.0,  # bar
            'outlet_pressure': 150.0,  # bar
            'inlet_temperature': 40.0,  # °C
            'co2_isentropic_exponent': 1.28,
            'co2_molar_mass': 44.01  # g/mol
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算二氧化碳压缩机的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示CO2流量 (kg/h)
        co2_flow = input_power
        
        # 计算等熵压缩功 (kJ/kg)
        p1 = params.get('inlet_pressure', 1.0)
        p2 = params.get('outlet_pressure', 150.0)
        k = params.get('co2_isentropic_exponent', 1.28)
        t1 = params.get('inlet_temperature', 40.0) + 273.15  # K
        
        # 等熵压缩功公式: w_isentropic = (k/(k-1)) * R * T1 * [(p2/p1)^((k-1)/k) - 1]
        R = 8.314 / (params.get('co2_molar_mass', 44.01) / 1000)  # J/kg·K
        pressure_ratio = p2 / p1
        w_isentropic = (k / (k - 1)) * R * t1 * (pressure_ratio ** ((k - 1) / k) - 1) / 1000  # kJ/kg
        
        # 计算实际功 (kJ/kg)
        eff = params.get('efficiency', 0.75)
        w_actual = w_isentropic / eff
        
        # 计算功率消耗 (kW)
        power_consumed = (co2_flow * w_actual) / 3.6  # kW = (kg/h * kJ/kg) / 3.6
        
        # 计算出口温度 (K)
        t2 = t1 * (pressure_ratio ** ((k - 1) / k)) / eff
        outlet_temperature = t2 - 273.15  # °C
        
        return {
            'co2_flow': co2_flow,
            'power_consumed': power_consumed,
            'efficiency': eff,
            'inlet_pressure': p1,
            'outlet_pressure': p2,
            'inlet_temperature': params.get('inlet_temperature', 40.0),
            'outlet_temperature': outlet_temperature,
            'pressure_ratio': pressure_ratio
        }


class CO2StorageTank(ExtendedEnergyComponent):
    """二氧化碳储罐（液态）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CarbonManagementConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['fill_level'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'capacity': 1000.0,  # m³
            'operating_pressure': 200.0,  # bar
            'operating_temperature': -20.0,  # °C
            'co2_density': 770.0,  # kg/m³ (液态CO2)
            'heat_loss_rate': 0.01,  # 热损失率 (1%/h)
            'max_fill_rate': 0.95,
            'min_fill_rate': 0.05
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算二氧化碳储罐的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示CO2输入/输出速率 (kg/h)
        co2_flow = input_power
        
        # 获取当前状态
        current_fill = self._current_state.get('fill_level', 0.0)
        capacity = params.get('capacity', 1000.0)
        density = params.get('co2_density', 770.0)
        
        # 计算当前存储量 (kg)
        current_stored = current_fill * capacity * density
        
        # 计算新存储量 (kg)
        new_stored = max(
            params.get('min_fill_rate', 0.05) * capacity * density,
            min(params.get('max_fill_rate', 0.95) * capacity * density,
                current_stored + co2_flow * time_step)
        )
        
        # 计算新填充率
        new_fill = new_stored / (capacity * density)
        
        # 计算热损失 (kW)
        heat_loss_rate = params.get('heat_loss_rate', 0.01)
        heat_loss = heat_loss_rate * (new_stored * 1.0)  # 假设比热为1.0 kJ/kg·°C
        
        # 更新状态
        self._current_state['fill_level'] = new_fill
        
        return {
            'co2_flow': co2_flow,
            'fill_level': new_fill,
            'co2_stored': new_stored,
            'heat_loss': heat_loss,
            'temperature': params.get('operating_temperature', -20.0),
            'pressure': params.get('operating_pressure', 200.0),
            'efficiency': 0.99  # 存储效率
        }


class GeologicCO2Storage(ExtendedEnergyComponent):
    """地质封存系统（枯竭油气田）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CarbonManagementConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['storage_level'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'storage_capacity': 1000000.0,  # 10^6 tons CO2
            'injectivity': 1000.0,  # tons CO2/day
            'storage_efficiency': 0.98,
            'leakage_rate': 0.0001,  # 泄漏率 (0.01%/year)
            'formation_pressure': 200.0,  # bar
            'formation_temperature': 60.0  # °C
        }
    
    def calculate_physical_performance(self, input_power: float, operating_conditions: Optional[Dict[str, Any]] = None, time_step: float = 1.0) -> Dict[str, Any]:
        """计算地质封存系统的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示CO2注入速率 (kg/h)
        co2_injection = input_power
        
        # 转换为吨/年
        co2_injection_tpy = (co2_injection * 24 * 365) / 1000
        
        # 获取当前存储量 (tons)
        current_storage = self._current_state.get('storage_level', 0.0)
        max_capacity = params.get('storage_capacity', 1000000.0)
        
        # 计算新存储量 (tons)
        new_storage = max(
            0.0,
            min(max_capacity,
                current_storage + (co2_injection * time_step) / 1000  # 转换为吨
            )
        )
        
        # 计算存储率
        storage_rate = new_storage / max_capacity
        
        # 计算泄漏量 (kg/h)
        leakage_rate = params.get('leakage_rate', 0.0001)
        leakage = (current_storage * 1000 * leakage_rate) / (365 * 24)  # kg/h
        
        # 更新状态
        self._current_state['storage_level'] = new_storage
        
        return {
            'co2_injection': co2_injection,
            'storage_level': new_storage,
            'storage_rate': storage_rate,
            'leakage': leakage,
            'max_capacity': max_capacity,
            'injectivity': params.get('injectivity', 1000.0),
            'storage_efficiency': params.get('storage_efficiency', 0.98),
            'temperature': params.get('formation_temperature', 60.0),
            'pressure': params.get('formation_pressure', 200.0)
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.POST_COMBUSTION_CARBON_CAPTURE, PostCombustionCarbonCapture)
register_component_factory(ExtendedEquipmentType.PRE_COMBUSTION_CARBON_CAPTURE, PostCombustionCarbonCapture)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.OXY_FUEL_COMBUSTION_CARBON_CAPTURE, PostCombustionCarbonCapture)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.DIRECT_AIR_CAPTURE, DirectAirCapture)
register_component_factory(ExtendedEquipmentType.CO2_COMPRESSOR, CO2Compressor)
register_component_factory(ExtendedEquipmentType.LIQUID_CO2_STORAGE_TANK, CO2StorageTank)
register_component_factory(ExtendedEquipmentType.CO2_PIPELINE, CO2StorageTank)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.GEOLOGIC_CO2_STORAGE, GeologicCO2Storage)
register_component_factory(ExtendedEquipmentType.ALGAE_CULTIVATION_CO2_UTILIZATION, PostCombustionCarbonCapture)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.MINERAL_CARBONATION_CO2_UTILIZATION, PostCombustionCarbonCapture)  # 暂时使用相似模型


# 模块导出
__all__ = [
    'PostCombustionCarbonCapture',
    'DirectAirCapture',
    'CO2Compressor',
    'CO2StorageTank',
    'GeologicCO2Storage'
]