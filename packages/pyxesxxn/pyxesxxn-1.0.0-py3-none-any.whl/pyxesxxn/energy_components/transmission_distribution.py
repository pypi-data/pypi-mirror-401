"""Transmission and distribution network components."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

from pyxesxxn.energy_components.base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    register_component_factory
)


@dataclass
class TransmissionDistributionConfig(ExtendedEquipmentConfig):
    """Configuration for transmission and distribution network components."""
    pass


class ACGridLine(ExtendedEnergyComponent):
    """交流配电网线路（架空/电缆）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[TransmissionDistributionConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'resistance': 0.1,  # Ω/km
            'reactance': 0.3,  # Ω/km
            'susceptance': 3.0,  # μS/km
            'length': 1.0,  # km
            'max_current': 500.0,  # A
            'voltage_level': 10.0,  # kV
            'conductor_type': 'aluminum',
            'temperature_coefficient': 0.004  # 1/°C
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算交流配电网线路的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示线路电流 (A)
        current = input_power
        
        # 获取线路参数
        r = params.get('resistance', 0.1) * params.get('length', 1.0)
        x = params.get('reactance', 0.3) * params.get('length', 1.0)
        voltage = params.get('voltage_level', 10.0) * 1000  # V
        
        # 计算线路阻抗 (Ω)
        impedance = np.sqrt(r**2 + x**2)
        
        # 计算功率损耗 (kW)
        power_loss = 3 * (current**2) * r / 1000  # 3相
        
        # 计算电压降 (V)
        voltage_drop = 3**0.5 * current * impedance
        voltage_drop_pct = (voltage_drop / voltage) * 100  # %
        
        # 计算热损失
        temperature_rise = current**2 * r * params.get('temperature_coefficient', 0.004) * time_step
        
        # 计算潮流
        active_power = 3**0.5 * voltage * current * 0.9 / 1000  # kW, 假设功率因数0.9
        reactive_power = 3**0.5 * voltage * current * np.sin(np.arccos(0.9)) / 1000  # kVar
        
        return {
            'current': current,
            'power_loss': power_loss,
            'voltage_drop': voltage_drop,
            'voltage_drop_pct': voltage_drop_pct,
            'temperature_rise': temperature_rise,
            'active_power_flow': active_power,
            'reactive_power_flow': reactive_power,
            'impedance': impedance,
            'resistance': r,
            'reactance': x
        }


class DCCable(ExtendedEnergyComponent):
    """直流配电网线路物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[TransmissionDistributionConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'resistance': 0.08,  # Ω/km
            'length': 1.0,  # km
            'max_current': 1000.0,  # A
            'voltage_level': 30.0,  # kV DC
            'cable_type': 'XLPE',
            'insulation_resistance': 100.0  # MΩ·km
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算直流配电网线路的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示线路电流 (A)
        current = input_power
        
        # 获取线路参数
        r = params.get('resistance', 0.08) * params.get('length', 1.0)
        voltage = params.get('voltage_level', 30.0) * 1000  # V
        
        # 计算功率损耗 (kW)
        power_loss = 2 * (current**2) * r / 1000  # 2导体
        
        # 计算电压降 (V)
        voltage_drop = 2 * current * r
        voltage_drop_pct = (voltage_drop / voltage) * 100  # %
        
        # 计算功率传输
        power_flow = voltage * current / 1000  # kW
        
        # 计算绝缘损耗
        insulation_resistance = params.get('insulation_resistance', 100.0) * 10**6 / params.get('length', 1.0)  # Ω
        insulation_loss = (voltage**2) / insulation_resistance / 1000  # kW
        
        return {
            'current': current,
            'power_loss': power_loss + insulation_loss,
            'conduction_loss': power_loss,
            'insulation_loss': insulation_loss,
            'voltage_drop': voltage_drop,
            'voltage_drop_pct': voltage_drop_pct,
            'power_flow': power_flow,
            'resistance': r,
            'voltage': voltage
        }


class ACToDCConverter(ExtendedEnergyComponent):
    """交流/直流换流器物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[TransmissionDistributionConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'max_power': 1000.0,  # kW
            'efficiency': 0.98,
            'ac_voltage': 10.0,  # kV
            'dc_voltage': 30.0,  # kV
            'switching_frequency': 2000.0,  # Hz
            'power_factor': 0.98
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算交流/直流换流器的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示交流输入功率 (kW)
        ac_power = input_power
        
        # 计算直流输出功率 (kW)
        efficiency = params.get('efficiency', 0.98)
        dc_power = ac_power * efficiency
        
        # 计算功率损耗 (kW)
        power_loss = ac_power - dc_power
        
        # 计算交流电流 (A)
        ac_voltage = params.get('ac_voltage', 10.0) * 1000  # V
        ac_current = ac_power * 1000 / (3**0.5 * ac_voltage * params.get('power_factor', 0.98))
        
        # 计算直流电流 (A)
        dc_voltage = params.get('dc_voltage', 30.0) * 1000  # V
        dc_current = dc_power * 1000 / dc_voltage
        
        return {
            'ac_power': ac_power,
            'dc_power': dc_power,
            'power_loss': power_loss,
            'efficiency': efficiency,
            'ac_current': ac_current,
            'dc_current': dc_current,
            'ac_voltage': ac_voltage,
            'dc_voltage': dc_voltage
        }


class LoadTapChangerTransformer(ExtendedEnergyComponent):
    """变压器（有载调压）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[TransmissionDistributionConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['tap_position'] = 0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'power_rating': 5000.0,  # kVA
            'primary_voltage': 110.0,  # kV
            'secondary_voltage': 10.0,  # kV
            'tap_range': [-10, 10],  # %
            'tap_step': 1.0,  # %
            'resistance': 0.5,  # %
            'reactance': 5.0,  # %
            'no_load_loss': 5.0,  # kW
            'load_loss': 50.0,  # kW at rated load
            'efficiency': 0.98
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算有载调压变压器的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示负载率 (0-1)
        load_factor = input_power
        
        # 获取当前抽头位置
        tap_position = self._current_state.get('tap_position', 0)
        tap_percent = tap_position * params.get('tap_step', 1.0)
        
        # 计算实际负载功率 (kVA)
        rated_power = params.get('power_rating', 5000.0)
        actual_power = rated_power * load_factor
        
        # 计算负载损耗 (kW)
        load_loss = params.get('load_loss', 50.0) * (load_factor**2)
        
        # 计算总损耗 (kW)
        total_loss = params.get('no_load_loss', 5.0) + load_loss
        
        # 计算效率
        efficiency = (actual_power - total_loss) / actual_power if actual_power > 0 else 0
        
        # 计算电压比
        voltage_ratio = (params.get('primary_voltage', 110.0) * (1 + tap_percent/100)) / params.get('secondary_voltage', 10.0)
        
        # 计算短路阻抗 (Ω)
        short_circuit_impedance_pct = np.sqrt(params.get('resistance', 0.5)**2 + params.get('reactance', 5.0)**2)
        
        return {
            'load_factor': load_factor,
            'actual_power': actual_power,
            'total_loss': total_loss,
            'no_load_loss': params.get('no_load_loss', 5.0),
            'load_loss': load_loss,
            'efficiency': efficiency,
            'tap_position': tap_position,
            'tap_percent': tap_percent,
            'voltage_ratio': voltage_ratio,
            'short_circuit_impedance_pct': short_circuit_impedance_pct
        }


class StaticVarCompensator(ExtendedEnergyComponent):
    """静态无功补偿器（SVC）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[TransmissionDistributionConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'max_reactive_power': 1000.0,  # kVar
            'min_reactive_power': -1000.0,  # kVar
            'response_time': 0.1,  # s
            'efficiency': 0.99,
            'voltage_level': 10.0,  # kV
            'control_mode': 'voltage'
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算静态无功补偿器的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示无功功率指令 (kVar)
        reactive_power = input_power
        
        # 限制无功功率在范围内
        limited_reactive = max(
            params.get('min_reactive_power', -1000.0),
            min(reactive_power, params.get('max_reactive_power', 1000.0))
        )
        
        # 计算功率损耗 (kW)
        efficiency = params.get('efficiency', 0.99)
        power_loss = abs(limited_reactive) * (1 - efficiency) / 1000  # kW
        
        # 计算响应时间
        response_time = params.get('response_time', 0.1)
        
        return {
            'reactive_power': limited_reactive,
            'power_loss': power_loss,
            'efficiency': efficiency,
            'response_time': response_time,
            'available_capacity_up': params.get('max_reactive_power', 1000.0) - limited_reactive,
            'available_capacity_down': limited_reactive - params.get('min_reactive_power', -1000.0),
            'voltage_level': params.get('voltage_level', 10.0)
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.AC_GRID_LINE, ACGridLine)
register_component_factory(ExtendedEquipmentType.DC_GRID_LINE, DCCable)
register_component_factory(ExtendedEquipmentType.AC_TO_DC_CONVERTER, ACToDCConverter)
register_component_factory(ExtendedEquipmentType.LOAD_TAP_CHANGER_TRANSFORMER, LoadTapChangerTransformer)
register_component_factory(ExtendedEquipmentType.STATIC_VAR_COMPENSATOR, StaticVarCompensator)
register_component_factory(ExtendedEquipmentType.SOLID_STATE_TRANSFORMER, ACToDCConverter)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.PV_INVERTER, ACToDCConverter)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.ENERGY_STORAGE_CONVERTER, ACToDCConverter)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.NATURAL_GAS_DISTRIBUTION_NETWORK, ACGridLine)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.NATURAL_GAS_COMPRESSOR_STATION, ACToDCConverter)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.NATURAL_GAS_GATE_STATION, LoadTapChangerTransformer)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.HYDROGEN_NATURAL_GAS_BLEND_PIPELINE, DCCable)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.THERMAL_NETWORK_HYDRAULIC_MODEL, ACGridLine)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.MULTI_ENERGY_HUB, ACToDCConverter)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.ENERGY_ROUTER, ACToDCConverter)  # 暂时使用相似模型


# 模块导出
__all__ = [
    'ACGridLine',
    'DCCable',
    'ACToDCConverter',
    'LoadTapChangerTransformer',
    'StaticVarCompensator'
]