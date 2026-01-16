"""Control and auxiliary system components."""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import numpy as np

from pyxesxxn.energy_components.base import (
    ExtendedEnergyComponent,
    ExtendedEquipmentConfig,
    ExtendedEquipmentType,
    register_component_factory
)


@dataclass
class ControlAuxiliaryConfig(ExtendedEquipmentConfig):
    """Configuration for control and auxiliary system components."""
    pass


class EnergyManagementSystem(ExtendedEnergyComponent):
    """能量管理系统（EMS）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[ControlAuxiliaryConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['optimization_status'] = 'idle'
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'computational_power': 100.0,  # GFLOPS
            'optimization_time': 5.0,  # s
            'communication_delay': 0.1,  # s
            'control_update_rate': 1.0,  # Hz
            'number_of_controlled_devices': 100,
            'optimization_algorithm': 'linear_programming'
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算能量管理系统的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示受控设备数量
        num_devices = input_power
        
        # 计算计算时间
        base_time = params.get('optimization_time', 5.0)
        comp_time = base_time * (1 + 0.01 * num_devices)  # 每增加1个设备增加1%时间
        
        # 计算通信延迟
        comm_delay = params.get('communication_delay', 0.1) * (1 + 0.005 * num_devices)
        
        # 计算能耗
        power_consumption = params.get('computational_power', 100.0) * 0.001  # 假设100 GFLOPS对应100 W
        energy_consumed = power_consumption * time_step
        
        # 计算优化效率
        optimization_efficiency = max(0.5, 1.0 - 0.001 * num_devices)  # 设备越多效率越低
        
        return {
            'number_of_controlled_devices': num_devices,
            'computation_time': comp_time,
            'communication_delay': comm_delay,
            'power_consumption': power_consumption,
            'energy_consumed': energy_consumed,
            'optimization_efficiency': optimization_efficiency,
            'control_update_rate': params.get('control_update_rate', 1.0),
            'optimization_algorithm': params.get('optimization_algorithm', 'linear_programming')
        }


class DistributedCoordinatedController(ExtendedEnergyComponent):
    """分布式协同控制器物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[ControlAuxiliaryConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['coordination_status'] = 'active'
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'number_of_agents': 10,
            'communication_bandwidth': 100.0,  # Mbps
            'consensus_time': 2.0,  # s
            'fault_tolerance': 0.3,  # 30%容错率
            'control_strategy': 'consensus_based',
            'latency': 0.05  # s
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算分布式协同控制器的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示代理数量
        num_agents = input_power
        
        # 计算共识时间
        base_consensus = params.get('consensus_time', 2.0)
        consensus_time = base_consensus * (1 + 0.02 * num_agents)  # 代理越多共识时间越长
        
        # 计算通信带宽需求
        data_per_agent = 1.0  # Mbps
        bandwidth_usage = min(params.get('communication_bandwidth', 100.0), num_agents * data_per_agent)
        bandwidth_utilization = (bandwidth_usage / params.get('communication_bandwidth', 100.0)) * 100  # %
        
        # 计算能耗
        power_per_agent = 5.0  # W per agent
        power_consumption = num_agents * power_per_agent / 1000  # kW
        energy_consumed = power_consumption * time_step
        
        # 计算容错能力
        fault_tolerance = params.get('fault_tolerance', 0.3)
        max_faults = int(num_agents * fault_tolerance)
        
        return {
            'number_of_agents': num_agents,
            'consensus_time': consensus_time,
            'communication_bandwidth_usage': bandwidth_usage,
            'bandwidth_utilization_pct': bandwidth_utilization,
            'power_consumption': power_consumption,
            'energy_consumed': energy_consumed,
            'max_tolerable_faults': max_faults,
            'latency': params.get('latency', 0.05)
        }


class FrequencyRegulationReserveSystem(ExtendedEnergyComponent):
    """频率调节备用系统物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[ControlAuxiliaryConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['frequency'] = 50.0  # Hz
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'regulation_capacity': 100.0,  # kW
            'response_time': 0.2,  # s
            'deadband': 0.05,  # Hz
            'droop_coefficient': 5.0,  # %
            'operating_frequency': 50.0,  # Hz
            'max_deviation': 0.5  # Hz
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算频率调节备用系统的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示频率偏差 (Hz)
        freq_deviation = input_power
        
        # 获取当前频率
        current_freq = self._current_state.get('frequency', 50.0)
        nominal_freq = params.get('operating_frequency', 50.0)
        
        # 计算新频率
        new_freq = current_freq + freq_deviation
        
        # 限制频率在允许范围内
        new_freq = max(
            nominal_freq - params.get('max_deviation', 0.5),
            min(new_freq, nominal_freq + params.get('max_deviation', 0.5))
        )
        
        # 计算需要的调节功率
        droop = params.get('droop_coefficient', 5.0)
        regulation_power = (freq_deviation / droop) * params.get('regulation_capacity', 100.0)
        
        # 限制调节功率
        regulation_power = max(
            -params.get('regulation_capacity', 100.0),
            min(regulation_power, params.get('regulation_capacity', 100.0))
        )
        
        # 计算调节效率
        efficiency = 0.98 - abs(freq_deviation) * 0.02  # 偏差越大效率越低
        
        # 更新状态
        self._current_state['frequency'] = new_freq
        
        return {
            'frequency': new_freq,
            'frequency_deviation': new_freq - nominal_freq,
            'regulation_power': regulation_power,
            'response_time': params.get('response_time', 0.2),
            'efficiency': efficiency,
            'regulation_capacity': params.get('regulation_capacity', 100.0),
            'droop_coefficient': droop
        }


class WeatherForecastingModule(ExtendedEnergyComponent):
    """气象预测模块（风光功率预测）物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[ControlAuxiliaryConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'forecast_horizon': 24.0,  # hours
            'forecast_resolution': 1.0,  # hours
            'solar_forecast_accuracy': 0.90,  # 90% accuracy
            'wind_forecast_accuracy': 0.85,  # 85% accuracy
            'update_frequency': 1.0,  # hours
            'data_sources': ['satellite', 'ground_station', 'numerical_weather_prediction'],
            'computational_load': 50.0  # GFLOPS
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算气象预测模块的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示预测误差水平 (0-1)
        error_level = input_power
        
        # 计算预测准确率
        base_solar_acc = params.get('solar_forecast_accuracy', 0.90)
        base_wind_acc = params.get('wind_forecast_accuracy', 0.85)
        
        solar_accuracy = max(0.5, base_solar_acc - error_level * 0.5)
        wind_accuracy = max(0.5, base_wind_acc - error_level * 0.5)
        
        # 计算计算时间
        comp_load = params.get('computational_load', 50.0)
        comp_time = (comp_load * 0.1) * (1 + error_level)  # 误差越大需要更多计算
        
        # 计算能耗
        power_consumption = comp_load * 0.001  # 假设100 GFLOPS对应100 W
        energy_consumed = power_consumption * time_step
        
        # 计算预测值（示例）
        solar_forecast = 1000.0 * (1 - error_level * 0.3)  # kW
        wind_forecast = 1500.0 * (1 - error_level * 0.4)  # kW
        
        return {
            'solar_forecast_accuracy': solar_accuracy,
            'wind_forecast_accuracy': wind_accuracy,
            'solar_forecast_value': solar_forecast,
            'wind_forecast_value': wind_forecast,
            'computation_time': comp_time,
            'power_consumption': power_consumption,
            'energy_consumed': energy_consumed,
            'forecast_horizon': params.get('forecast_horizon', 24.0),
            'forecast_resolution': params.get('forecast_resolution', 1.0)
        }


class LoadForecastingModule(ExtendedEnergyComponent):
    """负荷预测模块物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[ControlAuxiliaryConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'forecast_horizon': 24.0,  # hours
            'forecast_resolution': 1.0,  # hours
            'forecast_accuracy': 0.95,  # 95% accuracy
            'update_frequency': 1.0,  # hours
            'load_types': ['residential', 'commercial', 'industrial'],
            'historical_data_length': 365,  # days
            'computational_load': 30.0  # GFLOPS
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算负荷预测模块的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示预测误差水平 (0-1)
        error_level = input_power
        
        # 计算预测准确率
        base_acc = params.get('forecast_accuracy', 0.95)
        forecast_accuracy = max(0.6, base_acc - error_level * 0.4)
        
        # 计算计算时间
        comp_load = params.get('computational_load', 30.0)
        comp_time = (comp_load * 0.05) * (1 + error_level)  # 误差越大需要更多计算
        
        # 计算能耗
        power_consumption = comp_load * 0.001  # 假设100 GFLOPS对应100 W
        energy_consumed = power_consumption * time_step
        
        # 计算预测负荷（示例）
        total_forecast = 5000.0 * (1 + error_level * 0.2)  # kW
        
        return {
            'forecast_accuracy': forecast_accuracy,
            'total_load_forecast': total_forecast,
            'computation_time': comp_time,
            'power_consumption': power_consumption,
            'energy_consumed': energy_consumed,
            'forecast_horizon': params.get('forecast_horizon', 24.0),
            'forecast_resolution': params.get('forecast_resolution', 1.0),
            'historical_data_length': params.get('historical_data_length', 365)
        }


class CarbonFlowTrackingModule(ExtendedEnergyComponent):
    """碳流追踪模块物理建模"""
    
    def __init__(self, equipment_id: str, config: Optional[ControlAuxiliaryConfig] = None, **kwargs):
        super().__init__(equipment_id, config, **kwargs)
        self._current_state['total_carbon_emissions'] = 0.0
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        return {
            'tracking_resolution': 1.0,  # hours
            'emission_factor_resolution': 0.1,  # kg CO2/kWh
            'data_collection_frequency': 5.0,  # minutes
            'network_complexity': 100,  # number of nodes
            'accuracy': 0.98,  # 98% accuracy
            'reporting_horizon': 24.0  # hours
        }
    
    def calculate_physical_performance(self, input_power: float, time_step: float = 1.0, 
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """计算碳流追踪模块的物理性能"""
        params = self.config.physical_parameters
        
        # input_power表示能源消耗 (kWh)
        energy_consumed = input_power
        
        # 获取当前总排放
        current_emissions = self._current_state.get('total_carbon_emissions', 0.0)
        
        # 计算排放因子（假设）
        emission_factor = 0.4  # kg CO2/kWh
        
        # 计算碳排放
        carbon_emitted = energy_consumed * emission_factor
        new_total_emissions = current_emissions + carbon_emitted
        
        # 计算追踪误差
        tracking_accuracy = params.get('accuracy', 0.98)
        tracking_error = carbon_emitted * (1 - tracking_accuracy)
        
        # 计算能耗
        power_consumption = 0.1  # kW
        module_energy_consumed = power_consumption * time_step
        
        # 更新状态
        self._current_state['total_carbon_emissions'] = new_total_emissions
        
        return {
            'energy_consumed': energy_consumed,
            'carbon_emitted': carbon_emitted,
            'total_carbon_emissions': new_total_emissions,
            'emission_factor': emission_factor,
            'tracking_accuracy': tracking_accuracy,
            'tracking_error': tracking_error,
            'power_consumption': power_consumption,
            'module_energy_consumed': module_energy_consumed,
            'tracking_resolution': params.get('tracking_resolution', 1.0)
        }


# 注册组件工厂
register_component_factory(ExtendedEquipmentType.ENERGY_MANAGEMENT_SYSTEM, EnergyManagementSystem)
register_component_factory(ExtendedEquipmentType.DISTRIBUTED_COORDINATED_CONTROLLER, DistributedCoordinatedController)
register_component_factory(ExtendedEquipmentType.FREQUENCY_REGULATION_RESERVE_SYSTEM, FrequencyRegulationReserveSystem)
register_component_factory(ExtendedEquipmentType.BLACK_START_POWER_SUPPLY, EnergyManagementSystem)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.GRID_SYNCHRONIZATION_DEVICE, FrequencyRegulationReserveSystem)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.FAULT_CURRENT_LIMITER, FrequencyRegulationReserveSystem)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.POWER_QUALITY_IMPROVEMENT_DEVICE, FrequencyRegulationReserveSystem)  # 暂时使用相似模型
register_component_factory(ExtendedEquipmentType.WEATHER_FORECASTING_MODULE, WeatherForecastingModule)
register_component_factory(ExtendedEquipmentType.LOAD_FORECASTING_MODULE, LoadForecastingModule)
register_component_factory(ExtendedEquipmentType.CARBON_FLOW_TRACKING_MODULE, CarbonFlowTrackingModule)


# 模块导出
__all__ = [
    'EnergyManagementSystem',
    'DistributedCoordinatedController',
    'FrequencyRegulationReserveSystem',
    'WeatherForecastingModule',
    'LoadForecastingModule',
    'CarbonFlowTrackingModule'
]