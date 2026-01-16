"""Flexible loads and terminals components."""

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
class FlexibleLoadConfig(ExtendedEquipmentConfig):
    """Configuration for flexible load and terminal components."""
    pass


class CommercialBuildingLoad(ExtendedEnergyComponent):
    """商业楼宇负荷（空调、照明、插座）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[FlexibleLoadConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['temperature'] = 24.0  # 初始室温
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'building_area': 1000.0,  # m²
            'max_cooling_load': 200.0,  # kW
            'max_heating_load': 150.0,  # kW
            'max_elec_load': 100.0,  # kW
            'thermal_mass': 100000.0,  # kJ/°C
            'setpoint_temperature': 24.0,  # °C
            'occupancy_schedule': [0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 0.8, 0.9, 0.9, 0.8, 0.9, 0.9, 0.8, 0.8, 0.7, 0.6, 0.5, 0.7, 0.8, 0.6, 0.4, 0.2, 0.1, 0.1]  # 24小时 occupancy
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算商业楼宇负荷的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示环境温度 (°C)
        ambient_temp = input_power
        
        # 获取当前室温
        current_temp = self._current_state.get('temperature', 24.0)
        setpoint = params.get('setpoint_temperature', 24.0)
        thermal_mass = params.get('thermal_mass', 100000.0)
        
        # 计算热增益/损失 (kW)
        heat_transfer_coef = 50.0  # kW/°C (简化模型)
        heat_gain = heat_transfer_coef * (ambient_temp - current_temp) * time_step
        
        # 计算温度变化 (°C)
        temp_change = heat_gain / thermal_mass * 1000  # 转换为 °C
        new_temp = current_temp + temp_change
        
        # 计算空调负荷
        cooling_load = max(0.0, (new_temp - setpoint) * heat_transfer_coef)
        heating_load = max(0.0, (setpoint - new_temp) * heat_transfer_coef)
        
        # 计算照明和插座负荷 (基于occupancy)
        hour = int(time_step % 24)  # 简化的小时计算
        occupancy = params.get('occupancy_schedule', [0.5] * 24)[hour]
        elec_load = params.get('max_elec_load', 100.0) * occupancy
        
        # 总负荷
        total_load = cooling_load + heating_load + elec_load
        
        # 更新状态
        self._current_state['temperature'] = new_temp
        
        return {
            'ambient_temperature': ambient_temp,
            'room_temperature': new_temp,
            'cooling_load': cooling_load,
            'heating_load': heating_load,
            'electrical_load': elec_load,
            'total_load': total_load,
            'occupancy': occupancy,
            'setpoint_temperature': setpoint
        }


class IndustrialAdjustableLoad(ExtendedEnergyComponent):
    """工业过程可调节负荷物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[FlexibleLoadConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'base_load': 500.0,  # kW
            'max_adjustment': 200.0,  # kW (可调节范围)
            'min_load': 300.0,  # kW (最小负荷)
            'ramp_rate': 50.0,  # kW/min
            'process_efficiency': 0.85,
            'energy_storage_capacity': 1000.0  # kWh
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算工业过程可调节负荷的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示功率调整指令 (kW)
        power_adjustment = input_power
        
        # 获取当前负荷
        current_load = self._current_state.get('current_load', params.get('base_load', 500.0))
        
        # 计算新负荷
        new_load = max(
            params.get('min_load', 300.0),
            min(
                current_load + power_adjustment * time_step,
                params.get('base_load', 500.0) + params.get('max_adjustment', 200.0)
            )
        )
        
        # 计算效率
        efficiency = params.get('process_efficiency', 0.85)
        
        # 计算能量消耗 (kWh)
        energy_consumed = new_load * time_step
        
        # 计算可用调节容量
        available_up = params.get('base_load', 500.0) + params.get('max_adjustment', 200.0) - new_load
        available_down = new_load - params.get('min_load', 300.0)
        
        # 更新状态
        self._current_state['current_load'] = new_load
        
        return {
            'current_load': new_load,
            'energy_consumed': energy_consumed,
            'efficiency': efficiency,
            'available_up_adjustment': available_up,
            'available_down_adjustment': available_down,
            'ramp_rate': params.get('ramp_rate', 50.0),
            'process_output': new_load * efficiency
        }


class ResidentialDemandResponseLoad(ExtendedEnergyComponent):
    """居民需求响应负荷物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[FlexibleLoadConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'base_elec_load': 5.0,  # kW
            'max_elec_load': 10.0,  # kW
            'thermostat_setpoint': 24.0,  # °C
            'water_heater_capacity': 50.0,  # gallons
            'water_heater_setpoint': 60.0,  # °C
            'water_heater_standby_loss': 0.5,  # kW
            'dishwasher_power': 2.0,  # kW
            'clothes_washer_power': 1.5,  # kW
            'clothes_dryer_power': 3.0  # kW
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算居民需求响应负荷的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示需求响应信号 (0-1, 1表示最大削减)
        dr_signal = input_power
        
        # 基础负荷
        base_load = params.get('base_elec_load', 5.0)
        
        # 计算可削减负荷
        max_reducible = 3.0  # kW (简化模型)
        reducible_load = max_reducible * dr_signal
        
        # 计算实际负荷
        actual_load = base_load - reducible_load
        
        # 计算能量消耗 (kWh)
        energy_consumed = actual_load * time_step
        
        return {
            'base_load': base_load,
            'actual_load': actual_load,
            'reducible_load': reducible_load,
            'dr_signal': dr_signal,
            'energy_consumed': energy_consumed,
            'max_elec_load': params.get('max_elec_load', 10.0)
        }


class DCFastEVCharger(ExtendedEnergyComponent):
    """电动汽车充电桩（直流快充）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[FlexibleLoadConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'max_power_output': 150.0,  # kW
            'efficiency': 0.95,
            'voltage_range': [500, 1000],  # V
            'current_range': [0, 300],  # A
            'charging_curve': [(0, 1.0), (0.2, 0.95), (0.4, 0.9), (0.6, 0.8), (0.8, 0.6), (1.0, 0.3)]  # SOC vs C-rate
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算直流快充充电桩的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示电动汽车的SOC (0-1)
        soc = input_power
        
        # 根据SOC确定充电功率
        charging_curve = params.get('charging_curve', [(0, 1.0), (0.2, 0.95), (0.4, 0.9), (0.6, 0.8), (0.8, 0.6), (1.0, 0.3)])
        
        # 线性插值获取C-rate
        c_rate = 0.0
        for i in range(len(charging_curve) - 1):
            soc1, c1 = charging_curve[i]
            soc2, c2 = charging_curve[i + 1]
            if soc1 <= soc <= soc2:
                c_rate = c1 + (c2 - c1) * (soc - soc1) / (soc2 - soc1)
                break
        
        # 计算充电功率 (kW)
        battery_capacity = 80.0  # kWh (假设)
        charging_power = min(
            params.get('max_power_output', 150.0),
            battery_capacity * c_rate
        )
        
        # 计算电网输入功率 (kW)
        efficiency = params.get('efficiency', 0.95)
        grid_power = charging_power / efficiency
        
        # 计算充电电量 (kWh)
        energy_delivered = charging_power * time_step
        
        return {
            'charging_power': charging_power,
            'grid_power': grid_power,
            'efficiency': efficiency,
            'soc': soc,
            'c_rate': c_rate,
            'energy_delivered': energy_delivered,
            'max_power_output': params.get('max_power_output', 150.0)
        }


class DataCenterAdjustableLoad(ExtendedEnergyComponent):
    """数据中心负荷（可调节IT负载）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[FlexibleLoadConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'total_servers': 1000,
            'base_power_per_server': 0.5,  # kW/server
            'max_power_per_server': 1.0,  # kW/server
            'pue': 1.2,  # Power Usage Effectiveness
            'max_cooling_load': 200.0,  # kW
            'thermal_inertia': 50000.0,  # kJ/°C
            'setpoint_temperature': 22.0  # °C
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算数据中心可调节IT负载的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示负载调节因子 (0-1, 1表示满负载)
        load_factor = input_power
        
        # 计算IT负载
        total_servers = params.get('total_servers', 1000)
        base_power = params.get('base_power_per_server', 0.5)
        max_power = params.get('max_power_per_server', 1.0)
        
        it_load = total_servers * (base_power + (max_power - base_power) * load_factor)
        
        # 计算冷却负荷 (基于PUE)
        pue = params.get('pue', 1.2)
        cooling_load = it_load * (pue - 1.0)
        
        # 计算总功率消耗
        total_power = it_load * pue
        
        # 计算可用调节容量
        available_reduction = it_load - (total_servers * base_power)
        available_increase = (total_servers * max_power) - it_load
        
        return {
            'it_load': it_load,
            'cooling_load': cooling_load,
            'total_power': total_power,
            'load_factor': load_factor,
            'pue': pue,
            'available_reduction': available_reduction,
            'available_increase': available_increase,
            'total_servers': total_servers
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.COMMERCIAL_BUILDING_LOAD, CommercialBuildingLoad)
register_component_factory(ExtendedEquipmentType.INDUSTRIAL_ADJUSTABLE_LOAD, IndustrialAdjustableLoad)
register_component_factory(ExtendedEquipmentType.RESIDENTIAL_DEMAND_RESPONSE_LOAD, ResidentialDemandResponseLoad)
register_component_factory(ExtendedEquipmentType.AC_LEVEL2_EV_CHARGER, DCFastEVCharger)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.DC_FAST_EV_CHARGER, DCFastEVCharger)
register_component_factory(ExtendedEquipmentType.EV_BATTERY_SWAP_STATION, DCFastEVCharger)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.HIGH_POWER_ELECTRIC_TRUCK_CHARGERS, DCFastEVCharger)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.SHORE_POWER_SYSTEM, DCFastEVCharger)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.POWER_TO_GAS_FLEXIBLE_OPERATION, DCFastEVCharger)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.POWER_TO_AMMONIA_FLEXIBLE_OPERATION, DCFastEVCharger)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.DATA_CENTER_ADJUSTABLE_LOAD, DataCenterAdjustableLoad)
register_component_factory(ExtendedEquipmentType.AIR_CONDITIONING_VIRTUAL_STORAGE, CommercialBuildingLoad)  # 暂时使用相似模型


# 模块导出
__all__ = [
    'CommercialBuildingLoad',
    'IndustrialAdjustableLoad',
    'ResidentialDemandResponseLoad',
    'DCFastEVCharger',
    'DataCenterAdjustableLoad'
]