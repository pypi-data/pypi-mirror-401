"""CHP and gas system components."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

from pyxesxxn.energy_components.base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    register_component_factory,
    calculate_carnot_efficiency,
    calculate_thermodynamic_state
)


@dataclass
class CHPGasSystemConfig(ExtendedEquipmentConfig):
    """Configuration for CHP and gas system components."""
    pass


class NaturalGasICECHP(ExtendedEnergyComponent):
    """天然气内燃机热电联产物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'electrical_efficiency': 0.40,
            'thermal_efficiency': 0.45,
            'total_efficiency': 0.85,
            'natural_gas_lhv': 53.5,  # MJ/kg
            'max_power_output': 100.0,  # kW
            'operating_temperature': 85.0  # °C (排烟温度)
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算天然气内燃机热电联产的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h)
        gas_input = input_power
        
        # 计算总能量输入 (kW)
        total_energy = gas_input * params.get('natural_gas_lhv', 53.5) * 1000 / 3600
        
        # 计算电输出功率 (kW)
        elec_eff = params.get('electrical_efficiency', 0.40)
        power_output = total_energy * elec_eff
        
        # 计算热输出功率 (kW)
        thermal_eff = params.get('thermal_efficiency', 0.45)
        heat_output = total_energy * thermal_eff
        
        return {
            'natural_gas_input': gas_input,
            'power_output': power_output,
            'heat_output': heat_output,
            'electrical_efficiency': elec_eff,
            'thermal_efficiency': thermal_eff,
            'total_efficiency': params.get('total_efficiency', 0.85),
            'temperature': params.get('operating_temperature', 85.0),
            'pressure': 1.0
        }


class MicroGasTurbineCHP(ExtendedEnergyComponent):
    """微型燃气轮机热电联产物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'electrical_efficiency': 0.30,
            'thermal_efficiency': 0.55,
            'total_efficiency': 0.85,
            'turbine_inlet_temp': 950.0,  # °C
            'compression_ratio': 4.5,
            'max_power_output': 50.0,  # kW
            'natural_gas_lhv': 53.5  # MJ/kg
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算微型燃气轮机热电联产的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h)
        gas_input = input_power
        
        # 计算总能量输入 (kW)
        total_energy = gas_input * params.get('natural_gas_lhv', 53.5) * 1000 / 3600
        
        # 计算电输出功率 (kW)
        elec_eff = params.get('electrical_efficiency', 0.30)
        power_output = total_energy * elec_eff
        
        # 计算热输出功率 (kW)
        thermal_eff = params.get('thermal_efficiency', 0.55)
        heat_output = total_energy * thermal_eff
        
        # 计算卡诺效率
        t_high = params.get('turbine_inlet_temp', 950.0) + 273.15  # K
        t_low = 300.0  # K (环境温度)
        carnot_eff = calculate_carnot_efficiency(t_high, t_low)
        
        return {
            'natural_gas_input': gas_input,
            'power_output': power_output,
            'heat_output': heat_output,
            'electrical_efficiency': elec_eff,
            'thermal_efficiency': thermal_eff,
            'total_efficiency': params.get('total_efficiency', 0.85),
            'carnot_efficiency': carnot_eff,
            'temperature': params.get('turbine_inlet_temp', 950.0),
            'pressure': 1.0
        }


class IndustrialGasTurbineCHP(ExtendedEnergyComponent):
    """工业级燃气轮机热电联产物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'electrical_efficiency': 0.38,
            'thermal_efficiency': 0.50,
            'total_efficiency': 0.88,
            'turbine_inlet_temp': 1300.0,  # °C
            'compression_ratio': 15.0,
            'max_power_output': 5000.0,  # kW
            'natural_gas_lhv': 53.5  # MJ/kg
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算工业级燃气轮机热电联产的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h)
        gas_input = input_power
        
        # 计算总能量输入 (kW)
        total_energy = gas_input * params.get('natural_gas_lhv', 53.5) * 1000 / 3600
        
        # 计算电输出功率 (kW)
        elec_eff = params.get('electrical_efficiency', 0.38)
        power_output = total_energy * elec_eff
        
        # 计算热输出功率 (kW)
        thermal_eff = params.get('thermal_efficiency', 0.50)
        heat_output = total_energy * thermal_eff
        
        # 计算卡诺效率
        t_high = params.get('turbine_inlet_temp', 1300.0) + 273.15  # K
        t_low = 300.0  # K (环境温度)
        carnot_eff = calculate_carnot_efficiency(t_high, t_low)
        
        return {
            'natural_gas_input': gas_input,
            'power_output': power_output,
            'heat_output': heat_output,
            'electrical_efficiency': elec_eff,
            'thermal_efficiency': thermal_eff,
            'total_efficiency': params.get('total_efficiency', 0.88),
            'carnot_efficiency': carnot_eff,
            'temperature': params.get('turbine_inlet_temp', 1300.0),
            'pressure': 1.0
        }


class GasSteamCombinedCyclePlant(ExtendedEnergyComponent):
    """燃气-蒸汽联合循环机组物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'gas_turbine_efficiency': 0.38,
            'steam_turbine_efficiency': 0.30,
            'total_efficiency': 0.68,
            'turbine_inlet_temp': 1400.0,  # °C
            'compression_ratio': 18.0,
            'max_power_output': 30000.0,  # kW
            'natural_gas_lhv': 53.5  # MJ/kg
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算燃气-蒸汽联合循环机组的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h)
        gas_input = input_power
        
        # 计算总能量输入 (kW)
        total_energy = gas_input * params.get('natural_gas_lhv', 53.5) * 1000 / 3600
        
        # 计算燃气轮机输出 (kW)
        gt_eff = params.get('gas_turbine_efficiency', 0.38)
        gt_power = total_energy * gt_eff
        
        # 计算余热锅炉回收能量 (kW)
        exhaust_energy = total_energy * (1 - gt_eff) * 0.85  # 85%热回收效率
        
        # 计算蒸汽轮机输出 (kW)
        st_eff = params.get('steam_turbine_efficiency', 0.30)
        st_power = exhaust_energy * st_eff
        
        # 总输出功率
        power_output = gt_power + st_power
        
        # 计算总效率
        total_eff = power_output / total_energy
        
        return {
            'natural_gas_input': gas_input,
            'power_output': power_output,
            'gas_turbine_power': gt_power,
            'steam_turbine_power': st_power,
            'total_efficiency': total_eff,
            'gas_turbine_efficiency': gt_eff,
            'steam_turbine_efficiency': st_eff,
            'temperature': params.get('turbine_inlet_temp', 1400.0),
            'pressure': 1.0
        }


class StirlingEngine(ExtendedEnergyComponent):
    """斯特林发动机物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'efficiency': 0.35,
            'hot_source_temperature': 650.0,  # °C
            'cold_source_temperature': 30.0,  # °C
            'max_power_output': 10.0,  # kW
            'natural_gas_lhv': 53.5  # MJ/kg
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算斯特林发动机的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h)
        gas_input = input_power
        
        # 计算总能量输入 (kW)
        total_energy = gas_input * params.get('natural_gas_lhv', 53.5) * 1000 / 3600
        
        # 计算输出功率 (kW)
        eff = params.get('efficiency', 0.35)
        power_output = total_energy * eff
        
        # 计算卡诺效率
        t_high = params.get('hot_source_temperature', 650.0) + 273.15  # K
        t_low = params.get('cold_source_temperature', 30.0) + 273.15  # K
        carnot_eff = calculate_carnot_efficiency(t_high, t_low)
        
        return {
            'natural_gas_input': gas_input,
            'power_output': power_output,
            'efficiency': eff,
            'carnot_efficiency': carnot_eff,
            'hot_temperature': params.get('hot_source_temperature', 650.0),
            'cold_temperature': params.get('cold_source_temperature', 30.0),
            'pressure': 1.0
        }


class OrganicRankineCycleWasteHeatRecovery(ExtendedEnergyComponent):
    """有机朗肯循环余热发电物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'efficiency': 0.15,
            'heat_source_temperature': 200.0,  # °C
            'heat_sink_temperature': 30.0,  # °C
            'max_power_output': 500.0,  # kW
            'working_fluid': 'R245fa'
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算有机朗肯循环余热发电的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示余热输入速率 (kW)
        heat_input = input_power
        
        # 计算输出功率 (kW)
        eff = params.get('efficiency', 0.15)
        power_output = heat_input * eff
        
        # 计算卡诺效率
        t_high = params.get('heat_source_temperature', 200.0) + 273.15  # K
        t_low = params.get('heat_sink_temperature', 30.0) + 273.15  # K
        carnot_eff = calculate_carnot_efficiency(t_high, t_low)
        
        # 计算热力学状态
        thermo_state = calculate_thermodynamic_state(
            params.get('heat_source_temperature', 200.0),
            1.0,
            {'cp': 1.0, 'density': 1.0}
        )
        
        return {
            'heat_input': heat_input,
            'power_output': power_output,
            'efficiency': eff,
            'carnot_efficiency': carnot_eff,
            'thermodynamic_state': thermo_state,
            'temperature': params.get('heat_source_temperature', 200.0),
            'pressure': 1.0
        }


class AbsorptionChiller(ExtendedEnergyComponent):
    """吸收式制冷机（溴化锂）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'cop': 1.2,  # 制冷系数
            'heat_source_temperature': 85.0,  # °C
            'chilled_water_temperature': 7.0,  # °C
            'cooling_water_temperature': 32.0,  # °C
            'max_cooling_capacity': 1000.0,  # kW
            'natural_gas_lhv': 53.5  # MJ/kg
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算吸收式制冷机的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h) 或 热输入 (kW)
        # 假设input_power为热输入 (kW)
        heat_input = input_power
        
        # 计算制冷量 (kW)
        cop = params.get('cop', 1.2)
        cooling_output = heat_input * cop
        
        # 计算需要的冷却水量 (kg/s) - 假设冷却水温升5°C
        cooling_water_flow = cooling_output / (4.186 * 5) if cooling_output > 0 else 0
        
        return {
            'heat_input': heat_input,
            'cooling_output': cooling_output,
            'cop': cop,
            'chilled_water_temperature': params.get('chilled_water_temperature', 7.0),
            'cooling_water_temperature': params.get('cooling_water_temperature', 32.0),
            'cooling_water_flow': cooling_water_flow,
            'temperature': params.get('heat_source_temperature', 85.0),
            'pressure': 1.0
        }


class NaturalGasBoiler(ExtendedEnergyComponent):
    """天然气锅炉物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'efficiency': 0.92,
            'max_heat_output': 5000.0,  # kW
            'natural_gas_lhv': 53.5,  # MJ/kg
            'flue_gas_temperature': 150.0,  # °C
            'nox_emission_factor': 0.005  # kg/kWh
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算天然气锅炉的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示天然气输入速率 (kg/h)
        gas_input = input_power
        
        # 计算总能量输入 (kW)
        total_energy = gas_input * params.get('natural_gas_lhv', 53.5) * 1000 / 3600
        
        # 计算热输出功率 (kW)
        eff = params.get('efficiency', 0.92)
        heat_output = total_energy * eff
        
        # 计算NOx排放
        nox_emissions = heat_output * params.get('nox_emission_factor', 0.005)
        
        return {
            'natural_gas_input': gas_input,
            'heat_output': heat_output,
            'efficiency': eff,
            'flue_gas_temperature': params.get('flue_gas_temperature', 150.0),
            'nox_emissions': nox_emissions,
            'temperature': params.get('flue_gas_temperature', 150.0),
            'pressure': 1.0
        }


class AirSourceHeatPump(ExtendedEnergyComponent):
    """空气源热泵物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'cop_heating': 3.0,
            'cop_cooling': 2.5,
            'max_heating_capacity': 100.0,  # kW
            'max_cooling_capacity': 80.0,  # kW
            'ambient_temperature': 10.0,  # °C
            'water_temperature': 50.0  # °C (供热)
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算空气源热泵的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示电力输入 (kW)
        power_input = input_power
        
        # 计算供热输出 (kW)
        cop_heating = params.get('cop_heating', 3.0)
        heating_output = power_input * cop_heating
        
        # 计算制冷输出 (kW)
        cop_cooling = params.get('cop_cooling', 2.5)
        cooling_output = power_input * cop_cooling
        
        return {
            'power_input': power_input,
            'heating_output': heating_output,
            'cooling_output': cooling_output,
            'cop_heating': cop_heating,
            'cop_cooling': cop_cooling,
            'ambient_temperature': params.get('ambient_temperature', 10.0),
            'water_temperature': params.get('water_temperature', 50.0),
            'pressure': 1.0
        }


class SensibleHeatStorageTank(ExtendedEnergyComponent):
    """显热储热罐（水基）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[CHPGasSystemConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['temperature'] = 20.0  # 初始水温
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'capacity': 100.0,  # m³
            'max_temperature': 90.0,  # °C
            'min_temperature': 20.0,  # °C
            'heat_loss_rate': 0.005,  # 热损失率 (0.5%/h)
            'water_density': 1000.0,  # kg/m³
            'water_specific_heat': 4.186  # kJ/kg·°C
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算显热储热罐的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示热输入/输出速率 (kW)
        heat_flow = input_power
        
        # 获取当前状态
        current_temp = self._current_state.get('temperature', 20.0)
        capacity = params.get('capacity', 100.0)
        density = params.get('water_density', 1000.0)
        specific_heat = params.get('water_specific_heat', 4.186)
        
        # 计算热容量 (kJ/°C)
        heat_capacity = capacity * density * specific_heat
        
        # 计算温度变化
        temp_change = (heat_flow * time_step * 3600) / heat_capacity
        
        # 计算新温度
        new_temp = max(
            params.get('min_temperature', 20.0),
            min(params.get('max_temperature', 90.0),
                current_temp + temp_change)
        )
        
        # 计算实际存储的热量
        actual_heat_change = (new_temp - current_temp) * heat_capacity / 3600
        
        # 计算热损失
        heat_loss = params.get('heat_loss_rate', 0.005) * time_step * ((current_temp + new_temp) / 2 - 20.0) * heat_capacity / 3600
        
        # 更新状态
        self._current_state['temperature'] = new_temp
        
        return {
            'heat_flow': heat_flow,
            'temperature': new_temp,
            'heat_stored': actual_heat_change,
            'heat_loss': heat_loss,
            'efficiency': 1.0 - heat_loss / abs(heat_flow) if heat_flow != 0 else 1.0,
            'fill_rate': (new_temp - params.get('min_temperature', 20.0)) / 
                        (params.get('max_temperature', 90.0) - params.get('min_temperature', 20.0)),
            'pressure': 1.0
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.NATURAL_GAS_IC_ENGINE_CHP, NaturalGasICECHP)
register_component_factory(ExtendedEquipmentType.MICRO_GAS_TURBINE_CHP, MicroGasTurbineCHP)
register_component_factory(ExtendedEquipmentType.INDUSTRIAL_GAS_TURBINE_CHP, IndustrialGasTurbineCHP)
register_component_factory(ExtendedEquipmentType.GAS_STEAM_COMBINED_CYCLE_PLANT, GasSteamCombinedCyclePlant)
register_component_factory(ExtendedEquipmentType.STIRLING_ENGINE, StirlingEngine)
register_component_factory(ExtendedEquipmentType.ORGANIC_RANKINE_CYCLE_WASTE_HEAT_RECOVERY, OrganicRankineCycleWasteHeatRecovery)
register_component_factory(ExtendedEquipmentType.ABSORPTION_CHILLER, AbsorptionChiller)
register_component_factory(ExtendedEquipmentType.ADSORPTION_CHILLER, AbsorptionChiller)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.NATURAL_GAS_BOILER, NaturalGasBoiler)
register_component_factory(ExtendedEquipmentType.BIOMASS_BOILER, NaturalGasBoiler)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.AIR_SOURCE_HEAT_PUMP, AirSourceHeatPump)
register_component_factory(ExtendedEquipmentType.GROUND_SOURCE_HEAT_PUMP, AirSourceHeatPump)  # 暂时使用相同模型
register_component_factory(ExtendedEquipmentType.SENSIBLE_HEAT_STORAGE_TANK, SensibleHeatStorageTank)
register_component_factory(ExtendedEquipmentType.PHASE_CHANGE_MATERIAL_HEAT_STORAGE, SensibleHeatStorageTank)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.THERMOCHEMICAL_HEAT_STORAGE, SensibleHeatStorageTank)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.DISTRICT_HEATING_NETWORK, SensibleHeatStorageTank)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.DISTRICT_COOLING_NETWORK, SensibleHeatStorageTank)  # 暂时使用相似模型


# 模块导出
__all__ = [
    'NaturalGasICECHP',
    'MicroGasTurbineCHP',
    'IndustrialGasTurbineCHP',
    'GasSteamCombinedCyclePlant',
    'StirlingEngine',
    'OrganicRankineCycleWasteHeatRecovery',
    'AbsorptionChiller',
    'NaturalGasBoiler',
    'AirSourceHeatPump',
    'SensibleHeatStorageTank'
]