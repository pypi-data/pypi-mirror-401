"""Ammonia and alcohol-based energy system components."""

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
class AmmoniaAlcoholConfig(ExtendedEquipmentConfig):
    """Configuration for ammonia and alcohol-based energy components."""
    pass


class HaberBoschAmmoniaSynthesis(ExtendedEnergyComponent):
    """哈伯法合成氨装置物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'pressure': 200.0,  # 合成压力 (bar)
            'temperature': 450.0,  # 合成温度 (°C)
            'catalyst_efficiency': 0.85,
            'h2_n2_ratio': 3.0,
            'conversion_rate': 0.15,
            'energy_consumption': 33.0  # kWh/kg NH3
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算哈伯法合成氨装置的物理性能"""
        # 获取物理参数
        params = self.config.physical_parameters
        
        # 计算氨产量 (kg/h)
        ammonia_production = (input_power / params.get('energy_consumption', 33.0)) * time_step
        
        # 计算H2和N2消耗量
        h2_consumption = ammonia_production * (3/2) * 2.016 / 17.031  # kg H2
        n2_consumption = ammonia_production * (1/2) * 28.013 / 17.031  # kg N2
        
        # 计算效率
        theoretical_energy = 31.0  # kWh/kg NH3 (理论值)
        efficiency = theoretical_energy / params.get('energy_consumption', 33.0)
        
        return {
            'power_input': input_power,
            'ammonia_production': ammonia_production,
            'h2_consumption': h2_consumption,
            'n2_consumption': n2_consumption,
            'efficiency': efficiency,
            'temperature': params.get('temperature', 450.0),
            'pressure': params.get('pressure', 200.0),
            'conversion_rate': params.get('conversion_rate', 0.15),
            'catalyst_efficiency': params.get('catalyst_efficiency', 0.85)
        }


class ElectrocatalyticAmmoniaSynthesis(ExtendedEnergyComponent):
    """电催化合成氨装置物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'cell_voltage': 2.5,  # V
            'current_density': 0.1,  # A/cm²
            'faradaic_efficiency': 0.3,
            'selectivity': 0.9,
            'operating_pressure': 1.0,  # bar
            'operating_temperature': 25.0  # °C
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算电催化合成氨装置的物理性能"""
        params = self.config.physical_parameters
        
        # 计算电流 (A)
        current = input_power * 1000 / params.get('cell_voltage', 2.5)
        
        # 计算氨产量 (kg/h) - 基于法拉第定律
        # 合成1mol NH3需要3mol电子
        faradaic_eff = params.get('faradaic_efficiency', 0.3)
        nh3_molar_mass = 17.031  # g/mol
        ammonia_production = (current * faradaic_eff * time_step * 3600 * nh3_molar_mass) / (3 * 96485 * 1000)
        
        # 计算效率
        # 理论能量: N2 + 3H2 → 2NH3, ΔH = -46.11 kJ/mol
        theoretical_energy = (46.11 * 1000) / (2 * 17.031)  # kJ/kg NH3
        actual_energy = input_power * time_step * 3600 / ammonia_production if ammonia_production > 0 else 0  # kJ/kg NH3
        efficiency = theoretical_energy / actual_energy if actual_energy > 0 else 0
        
        return {
            'power_input': input_power,
            'ammonia_production': ammonia_production,
            'current': current,
            'cell_voltage': params.get('cell_voltage', 2.5),
            'faradaic_efficiency': faradaic_eff,
            'selectivity': params.get('selectivity', 0.9),
            'efficiency': efficiency,
            'temperature': params.get('operating_temperature', 25.0),
            'pressure': params.get('operating_pressure', 1.0)
        }


class AmmoniaStorageTank(ExtendedEnergyComponent):
    """氨储罐物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['ammonia_level'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'capacity': 10000.0,  # kg
            'max_pressure': 10.0,  # bar
            'operating_temperature': -33.0,  # °C (液氨沸点)
            'heat_loss_rate': 0.01  # 热损失率 (1%/h)
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算氨储罐的物理性能"""
        params = self.config.physical_parameters
        capacity = params.get('capacity', 10000.0)
        
        # input_power表示氨的输入/输出速率 (kg/h)
        ammonia_flow = input_power
        
        # 计算新的氨水平
        current_level = self._current_state.get('ammonia_level', 0.0)
        new_level = max(0.0, min(capacity, current_level + ammonia_flow * time_step))
        
        # 计算填充率
        fill_rate = new_level / capacity
        
        # 计算热损失
        heat_loss = params.get('heat_loss_rate', 0.01) * time_step
        
        return {
            'ammonia_flow': ammonia_flow,
            'ammonia_level': new_level,
            'fill_rate': fill_rate,
            'temperature': params.get('operating_temperature', -33.0),
            'pressure': params.get('max_pressure', 10.0) * fill_rate,
            'heat_loss': heat_loss,
            'efficiency': 0.99  # 存储效率
        }


class AmmoniaCrackingSystem(ExtendedEnergyComponent):
    """氨裂解制氢装置物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'temperature': 800.0,  # 裂解温度 (°C)
            'pressure': 3.0,  # 裂解压力 (bar)
            'catalyst_efficiency': 0.95,
            'conversion_rate': 0.98,
            'energy_consumption': 2.5  # kWh/kg NH3
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算氨裂解制氢装置的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示氨输入速率 (kg/h)
        ammonia_input = input_power
        
        # 计算H2产量 (kg/h)
        # NH3 → 1.5H2 + 0.5N2
        conversion = params.get('conversion_rate', 0.98)
        h2_production = ammonia_input * conversion * (3/2) * 2.016 / 17.031
        n2_production = ammonia_input * conversion * (1/2) * 28.013 / 17.031
        
        # 计算所需能量 (kW)
        energy_required = ammonia_input * params.get('energy_consumption', 2.5)
        
        # 计算效率
        efficiency = 0.95  # 裂解效率
        
        return {
            'ammonia_input': ammonia_input,
            'h2_production': h2_production,
            'n2_production': n2_production,
            'energy_required': energy_required,
            'conversion_rate': conversion,
            'efficiency': efficiency,
            'temperature': params.get('temperature', 800.0),
            'pressure': params.get('pressure', 3.0)
        }


class DirectAmmoniaFuelCell(ExtendedEnergyComponent):
    """直接氨燃料电池物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'operating_temperature': 600.0,  # °C
            'operating_pressure': 1.0,  # bar
            'nominal_voltage': 0.8,  # V
            'max_power_density': 0.3,  # W/cm²
            'efficiency': 0.55
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算直接氨燃料电池的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示氨输入速率 (kg/h)
        ammonia_input = input_power
        
        # 计算电输出功率 (kW)
        # 1kg NH3的理论能量: 18.6 kWh/kg
        theoretical_energy = 18.6  # kWh/kg
        power_output = ammonia_input * theoretical_energy * params.get('efficiency', 0.55)
        
        # 计算效率
        efficiency = params.get('efficiency', 0.55)
        
        return {
            'ammonia_input': ammonia_input,
            'power_output': power_output,
            'efficiency': efficiency,
            'temperature': params.get('operating_temperature', 600.0),
            'pressure': params.get('operating_pressure', 1.0),
            'voltage': params.get('nominal_voltage', 0.8)
        }


class AmmoniaFuelGasTurbine(ExtendedEnergyComponent):
    """氨燃料燃气轮机物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'turbine_inlet_temp': 1400.0,  # °C
            'compression_ratio': 15.0,
            'efficiency': 0.38,
            'ammonia_lhv': 18.6,  # kWh/kg
            'nox_emission_factor': 0.01  # kg/kWh
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算氨燃料燃气轮机的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示氨输入速率 (kg/h)
        ammonia_input = input_power
        
        # 计算电输出功率 (kW)
        lhv = params.get('ammonia_lhv', 18.6)
        efficiency = params.get('efficiency', 0.38)
        power_output = ammonia_input * lhv * efficiency
        
        # 计算热输出功率 (kW)
        heat_output = ammonia_input * lhv * (1 - efficiency) * 0.8  # 80%热回收
        
        # 计算NOx排放
        nox_emissions = power_output * params.get('nox_emission_factor', 0.01)
        
        return {
            'ammonia_input': ammonia_input,
            'power_output': power_output,
            'heat_output': heat_output,
            'efficiency': efficiency,
            'temperature': params.get('turbine_inlet_temp', 1400.0),
            'nox_emissions': nox_emissions
        }


class MethanolSynthesisSystem(ExtendedEnergyComponent):
    """甲醇合成装置物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'pressure': 80.0,  # bar
            'temperature': 250.0,  # °C
            'catalyst_efficiency': 0.85,
            'h2_co_ratio': 2.0,
            'conversion_rate': 0.25,
            'energy_consumption': 8.5  # kWh/kg CH3OH
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算甲醇合成装置的物理性能"""
        params = self.config.physical_parameters
        
        # 计算甲醇产量 (kg/h)
        methanol_production = (input_power / params.get('energy_consumption', 8.5)) * time_step
        
        # 计算H2和CO消耗量
        h2_consumption = methanol_production * (2/1) * 2.016 / 32.042  # kg H2
        co_consumption = methanol_production * (1/1) * 28.010 / 32.042  # kg CO
        
        # 计算效率
        theoretical_energy = 7.5  # kWh/kg CH3OH (理论值)
        efficiency = theoretical_energy / params.get('energy_consumption', 8.5)
        
        return {
            'power_input': input_power,
            'methanol_production': methanol_production,
            'h2_consumption': h2_consumption,
            'co_consumption': co_consumption,
            'efficiency': efficiency,
            'temperature': params.get('temperature', 250.0),
            'pressure': params.get('pressure', 80.0),
            'conversion_rate': params.get('conversion_rate', 0.25)
        }


class DirectMethanolFuelCell(ExtendedEnergyComponent):
    """直接甲醇燃料电池物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'operating_temperature': 80.0,  # °C
            'operating_pressure': 1.0,  # bar
            'nominal_voltage': 0.65,  # V
            'max_power_density': 0.15,  # W/cm²
            'efficiency': 0.45
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算直接甲醇燃料电池的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示甲醇输入速率 (kg/h)
        methanol_input = input_power
        
        # 计算电输出功率 (kW)
        # 1kg CH3OH的理论能量: 6.4 kWh/kg
        theoretical_energy = 6.4  # kWh/kg
        power_output = methanol_input * theoretical_energy * params.get('efficiency', 0.45)
        
        # 计算效率
        efficiency = params.get('efficiency', 0.45)
        
        return {
            'methanol_input': methanol_input,
            'power_output': power_output,
            'efficiency': efficiency,
            'temperature': params.get('operating_temperature', 80.0),
            'pressure': params.get('operating_pressure', 1.0),
            'voltage': params.get('nominal_voltage', 0.65)
        }


class EthanolFuelCell(ExtendedEnergyComponent):
    """乙醇燃料电池物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[AmmoniaAlcoholConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'operating_temperature': 120.0,  # °C
            'operating_pressure': 1.0,  # bar
            'nominal_voltage': 0.7,  # V
            'max_power_density': 0.12,  # W/cm²
            'efficiency': 0.48
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算乙醇燃料电池的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示乙醇输入速率 (kg/h)
        ethanol_input = input_power
        
        # 计算电输出功率 (kW)
        # 1kg C2H5OH的理论能量: 8.0 kWh/kg
        theoretical_energy = 8.0  # kWh/kg
        power_output = ethanol_input * theoretical_energy * params.get('efficiency', 0.48)
        
        # 计算效率
        efficiency = params.get('efficiency', 0.48)
        
        return {
            'ethanol_input': ethanol_input,
            'power_output': power_output,
            'efficiency': efficiency,
            'temperature': params.get('operating_temperature', 120.0),
            'pressure': params.get('operating_pressure', 1.0),
            'voltage': params.get('nominal_voltage', 0.7)
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.HABER_BOSCH_AMMONIA_SYNTHESIS, HaberBoschAmmoniaSynthesis)
register_component_factory(ExtendedEquipmentType.ELECTROCATALYTIC_AMMONIA_SYNTHESIS, ElectrocatalyticAmmoniaSynthesis)
register_component_factory(ExtendedEquipmentType.AMMONIA_STORAGE_TANK, AmmoniaStorageTank)
register_component_factory(ExtendedEquipmentType.AMMONIA_CRACKING_SYSTEM, AmmoniaCrackingSystem)
register_component_factory(ExtendedEquipmentType.DIRECT_AMMONIA_FUEL_CELL, DirectAmmoniaFuelCell)
register_component_factory(ExtendedEquipmentType.AMMONIA_FUEL_GAS_TURBINE, AmmoniaFuelGasTurbine)
register_component_factory(ExtendedEquipmentType.AMMONIA_FUEL_INTERNAL_COMBUSTION_ENGINE, AmmoniaFuelGasTurbine)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.CO2_HYDROGENATION_METHANOL_SYNTHESIS, MethanolSynthesisSystem)
register_component_factory(ExtendedEquipmentType.BIOMASS_TO_METHANOL_SYSTEM, MethanolSynthesisSystem)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.METHANOL_STORAGE_TANK, AmmoniaStorageTank)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.METHANOL_REFORMING_SYSTEM, AmmoniaCrackingSystem)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.DIRECT_METHANOL_FUEL_CELL, DirectMethanolFuelCell)
register_component_factory(ExtendedEquipmentType.METHANOL_FUEL_INTERNAL_COMBUSTION_ENGINE, AmmoniaFuelGasTurbine)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.ETHANOL_FERMENTATION_DISTILLATION, MethanolSynthesisSystem)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.ETHANOL_STORAGE_TANK, AmmoniaStorageTank)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.ETHANOL_FUEL_CELL, EthanolFuelCell)


# 模块导出
__all__ = [
    'HaberBoschAmmoniaSynthesis',
    'ElectrocatalyticAmmoniaSynthesis',
    'AmmoniaStorageTank',
    'AmmoniaCrackingSystem',
    'DirectAmmoniaFuelCell',
    'AmmoniaFuelGasTurbine',
    'MethanolSynthesisSystem',
    'DirectMethanolFuelCell',
    'EthanolFuelCell'
]