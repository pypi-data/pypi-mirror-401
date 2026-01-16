"""Base classes and utilities for extended energy components.

This module provides the foundation for all extended energy components, including:
- Extended equipment type and category enumerations
- Base classes for extended components
- Factory functions for component creation
- Configuration management
"""

import abc
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Type, Callable, TypeVar

import numpy as np

# Import PyXESXXN core components to extend
from pyxesxxn.equipment_library.base import (
    EquipmentType as PyXESXXNEquipmentType,
    EquipmentCategory as PyXESXXNEquipmentCategory,
    EnergyCarrier as PyXESXXNEnergyCarrier,
    EquipmentConfig as PyXESXXNEquipmentConfig,
    BaseEquipment as PyXESXXNBaseEquipment
)
from pyxesxxn.network import PyXESXXNNetwork


class ExtendedEquipmentCategory(Enum):
    """Extended equipment category enumeration with additional categories."""
    # Original categories from PyXESXXN
    GENERATION = "generation"
    STORAGE = "storage"
    CONVERSION = "conversion"
    TRANSPORT = "transport"
    LOADS = "loads"
    INFRASTRUCTURE = "infrastructure"
    CONTROL = "control"
    MEASUREMENT = "measurement"
    
    # Additional categories for extended components
    HYDROGEN_SYSTEMS = "hydrogen_systems"
    AMMONIA_ALCOHOL = "ammonia_alcohol"
    CARBON_MANAGEMENT = "carbon_management"
    MULTI_ENERGY = "multi_energy"
    EMERGING_TECH = "emerging_tech"
    FORECASTING = "forecasting"
    CARBON_TRACKING = "carbon_tracking"


class ExtendedEquipmentType(Enum):
    """Extended equipment type enumeration with all 130+ energy components."""
    # =========================================================================
    # 一、可再生能源发电
    # =========================================================================
    # 1. 光伏发电系统（固定倾角）
    FIXED_TILT_PV = "fixed_tilt_pv"
    # 2. 光伏发电系统（单轴/双轴跟踪）
    SINGLE_AXIS_TRACKING_PV = "single_axis_tracking_pv"
    DUAL_AXIS_TRACKING_PV = "dual_axis_tracking_pv"
    # 3. 分布式屋顶光伏
    DISTRIBUTED_ROOF_PV = "distributed_roof_pv"
    # 4. 集中式光伏电站
    CONCENTRATED_SOLAR_POWER_PLANT = "concentrated_solar_power_plant"
    # 5. 风力发电机（陆上，定速）
    FIXED_SPEED_WIND_TURBINE = "fixed_speed_wind_turbine"
    # 6. 风力发电机（陆上，变速双馈）
    VARIABLE_SPEED_DFIG_WIND_TURBINE = "variable_speed_dfig_wind_turbine"
    # 7. 风力发电机（海上直驱）
    OFFSHORE_DIRECT_DRIVE_WIND_TURBINE = "offshore_direct_drive_wind_turbine"
    # 8. 小型垂直轴风机
    SMALL_VERTICAL_AXIS_WIND_TURBINE = "small_vertical_axis_wind_turbine"
    # 9. 潮汐发电机组
    TIDAL_POWER_GENERATOR = "tidal_power_generator"
    # 10. 波浪能发电装置
    WAVE_ENERGY_CONVERTER = "wave_energy_converter"
    # 11. 小水电机组（径流式）
    RUN_OF_RIVER_HYDRO_GENERATOR = "run_of_river_hydro_generator"
    # 12. 小水电机组（水库式）
    RESERVOIR_HYDRO_GENERATOR = "reservoir_hydro_generator"
    # 13. 生物质直燃发电机组
    BIOMASS_DIRECT_COMBUSTION_GENERATOR = "biomass_direct_combustion_generator"
    # 14. 生物质气化发电系统
    BIOMASS_GASIFICATION_POWER_SYSTEM = "biomass_gasification_power_system"
    # 15. 地热发电（有机朗肯循环）
    GEOTHERMAL_ORC_POWER_PLANT = "geothermal_orc_power_plant"
    # 16. 聚光太阳能热发电（CSP，塔式）
    CSP_TOWER_SYSTEM = "csp_tower_system"
    # 17. 聚光太阳能热发电（槽式）
    CSP_TROUGH_SYSTEM = "csp_trough_system"
    # 18. 太阳能温差发电（热电偶）
    SOLAR_THERMOELECTRIC_GENERATOR = "solar_thermoelectric_generator"
    
    # =========================================================================
    # 二、电化学储能
    # =========================================================================
    # 19. 锂离子电池（磷酸铁锂）
    LITHIUM_IRON_PHOSPHATE_BATTERY = "lithium_iron_phosphate_battery"
    # 20. 锂离子电池（三元材料）
    NMC_BATTERY = "nmc_battery"
    # 21. 铅碳电池
    LEAD_CARBON_BATTERY = "lead_carbon_battery"
    # 22. 液流电池（全钒）
    VANADIUM_REDOX_FLOW_BATTERY = "vanadium_redox_flow_battery"
    # 23. 钠硫电池
    SODIUM_SULFUR_BATTERY = "sodium_sulfur_battery"
    # 24. 钠离子电池
    SODIUM_ION_BATTERY = "sodium_ion_battery"
    # 25. 固态电池
    SOLID_STATE_BATTERY = "solid_state_battery"
    # 26. 超级电容器
    SUPERCAPACITOR = "supercapacitor"
    # 27. 飞轮储能
    FLYWHEEL_ENERGY_STORAGE = "flywheel_energy_storage"
    # 28. 压缩空气储能（传统）
    TRADITIONAL_COMPRESSED_AIR_STORAGE = "traditional_compressed_air_storage"
    # 29. 压缩空气储能（绝热/等温）
    ADIABATIC_COMPRESSED_AIR_STORAGE = "adiabatic_compressed_air_storage"
    # 30. 抽水蓄能（大型）
    LARGE_PUMPED_HYDRO_STORAGE = "large_pumped_hydro_storage"
    # 31. 抽水蓄能（小型模块化）
    SMALL_MODULAR_PUMPED_HYDRO_STORAGE = "small_modular_pumped_hydro_storage"
    
    # =========================================================================
    # 三、氢能系统
    # =========================================================================
    # 32. 碱性电解槽（AEC）
    ALKALINE_ELECTROLYZER = "alkaline_electrolyzer"
    # 33. 质子交换膜电解槽（PEMEC）
    PEM_ELECTROLYZER = "pem_electrolyzer"
    # 34. 固体氧化物电解槽（SOEC）
    SOLID_OXIDE_ELECTROLYZER = "solid_oxide_electrolyzer"
    # 35. 高压气态储氢罐（35/70 MPa）
    HIGH_PRESSURE_HYDROGEN_TANK = "high_pressure_hydrogen_tank"
    # 36. 液态储氢罐
    LIQUID_HYDROGEN_TANK = "liquid_hydrogen_tank"
    # 37. 固态储氢（金属氢化物）
    METAL_HYDRIDE_HYDROGEN_STORAGE = "metal_hydride_hydrogen_storage"
    # 38. 地下储氢（盐穴）
    SALT_CAVERN_HYDROGEN_STORAGE = "salt_cavern_hydrogen_storage"
    # 39. 质子交换膜燃料电池（PEMFC）
    PEM_FUEL_CELL = "pem_fuel_cell"
    # 40. 固体氧化物燃料电池（SOFC）
    SOLID_OXIDE_FUEL_CELL = "solid_oxide_fuel_cell"
    # 41. 磷酸燃料电池（PAFC）
    PHOSPHORIC_ACID_FUEL_CELL = "phosphoric_acid_fuel_cell"
    # 42. 氢气压缩机（往复/离子）
    HYDROGEN_COMPRESSOR = "hydrogen_compressor"
    # 43. 氢气纯化装置（PSA）
    HYDROGEN_PURIFICATION_PSA = "hydrogen_purification_psa"
    # 44. 氢气加注站
    HYDROGEN_REFUELING_STATION = "hydrogen_refueling_station"
    # 45. 氢气输送管道（纯氢/掺氢）
    HYDROGEN_PIPELINE = "hydrogen_pipeline"
    
    # =========================================================================
    # 四、氨/醇基能源
    # =========================================================================
    # 46. 哈伯法合成氨装置
    HABER_BOSCH_AMMONIA_SYNTHESIS = "haber_bosch_ammonia_synthesis"
    # 47. 电催化合成氨装置
    ELECTROCATALYTIC_AMMONIA_SYNTHESIS = "electrocatalytic_ammonia_synthesis"
    # 48. 氨储罐（低温/加压）
    AMMONIA_STORAGE_TANK = "ammonia_storage_tank"
    # 49. 氨裂解制氢装置
    AMMONIA_CRACKING_SYSTEM = "ammonia_cracking_system"
    # 50. 直接氨燃料电池（DAFC）
    DIRECT_AMMONIA_FUEL_CELL = "direct_ammonia_fuel_cell"
    # 51. 氨燃料燃气轮机
    AMMONIA_FUEL_GAS_TURBINE = "ammonia_fuel_gas_turbine"
    # 52. 氨燃料内燃机
    AMMONIA_FUEL_INTERNAL_COMBUSTION_ENGINE = "ammonia_fuel_internal_combustion_engine"
    # 53. 甲醇合成装置（CO₂加氢）
    CO2_HYDROGENATION_METHANOL_SYNTHESIS = "co2_hydrogenation_methanol_synthesis"
    # 54. 生物质制甲醇装置
    BIOMASS_TO_METHANOL_SYSTEM = "biomass_to_methanol_system"
    # 55. 甲醇储罐
    METHANOL_STORAGE_TANK = "methanol_storage_tank"
    # 56. 甲醇重整制氢装置
    METHANOL_REFORMING_SYSTEM = "methanol_reforming_system"
    # 57. 直接甲醇燃料电池（DMFC）
    DIRECT_METHANOL_FUEL_CELL = "direct_methanol_fuel_cell"
    # 58. 甲醇燃料内燃机
    METHANOL_FUEL_INTERNAL_COMBUSTION_ENGINE = "methanol_fuel_internal_combustion_engine"
    # 59. 乙醇发酵与精馏装置
    ETHANOL_FERMENTATION_DISTILLATION = "ethanol_fermentation_distillation"
    # 60. 乙醇储罐
    ETHANOL_STORAGE_TANK = "ethanol_storage_tank"
    # 61. 乙醇燃料电池
    ETHANOL_FUEL_CELL = "ethanol_fuel_cell"
    
    # =========================================================================
    # 五、热电联产与燃气系统
    # =========================================================================
    # 62. 天然气内燃机热电联产
    NATURAL_GAS_IC_ENGINE_CHP = "natural_gas_ic_engine_chp"
    # 63. 燃气轮机热电联产（微型）
    MICRO_GAS_TURBINE_CHP = "micro_gas_turbine_chp"
    # 64. 燃气轮机热电联产（工业级）
    INDUSTRIAL_GAS_TURBINE_CHP = "industrial_gas_turbine_chp"
    # 65. 燃气-蒸汽联合循环机组
    GAS_STEAM_COMBINED_CYCLE_PLANT = "gas_steam_combined_cycle_plant"
    # 66. 斯特林发动机
    STIRLING_ENGINE = "stirling_engine"
    # 67. 有机朗肯循环余热发电
    ORGANIC_RANKINE_CYCLE_WASTE_HEAT_RECOVERY = "organic_rankine_cycle_waste_heat_recovery"
    # 68. 吸收式制冷机（溴化锂）
    ABSORPTION_CHILLER = "absorption_chiller"
    # 69. 吸附式制冷机
    ADSORPTION_CHILLER = "adsorption_chiller"
    # 70. 天然气锅炉
    NATURAL_GAS_BOILER = "natural_gas_boiler"
    # 71. 生物质锅炉
    BIOMASS_BOILER = "biomass_boiler"
    # 72. 热泵（空气源）
    AIR_SOURCE_HEAT_PUMP = "air_source_heat_pump"
    # 73. 热泵（地源）
    GROUND_SOURCE_HEAT_PUMP = "ground_source_heat_pump"
    # 74. 储热罐（显热，水基）
    SENSIBLE_HEAT_STORAGE_TANK = "sensible_heat_storage_tank"
    # 75. 储热罐（潜热，相变材料）
    PHASE_CHANGE_MATERIAL_HEAT_STORAGE = "phase_change_material_heat_storage"
    # 76. 储热罐（热化学）
    THERMOCHEMICAL_HEAT_STORAGE = "thermochemical_heat_storage"
    # 77. 区域供热管网
    DISTRICT_HEATING_NETWORK = "district_heating_network"
    # 78. 区域供冷管网
    DISTRICT_COOLING_NETWORK = "district_cooling_network"
    
    # =========================================================================
    # 六、碳管理系统
    # =========================================================================
    # 79. 燃烧后碳捕集（胺吸收）
    POST_COMBUSTION_CARBON_CAPTURE = "post_combustion_carbon_capture"
    # 80. 燃烧前碳捕集（重整气）
    PRE_COMBUSTION_CARBON_CAPTURE = "pre_combustion_carbon_capture"
    # 81. 富氧燃烧碳捕集
    OXY_FUEL_COMBUSTION_CARBON_CAPTURE = "oxy_fuel_combustion_carbon_capture"
    # 82. 直接空气捕集（DAC）
    DIRECT_AIR_CAPTURE = "direct_air_capture"
    # 83. 二氧化碳压缩机
    CO2_COMPRESSOR = "co2_compressor"
    # 84. 二氧化碳储罐（液态）
    LIQUID_CO2_STORAGE_TANK = "liquid_co2_storage_tank"
    # 85. 二氧化碳输送管道
    CO2_PIPELINE = "co2_pipeline"
    # 86. 地质封存系统（枯竭油气田）
    GEOLOGIC_CO2_STORAGE = "geologic_co2_storage"
    # 87. 二氧化碳利用系统（微藻培养）
    ALGAE_CULTIVATION_CO2_UTILIZATION = "algae_cultivation_co2_utilization"
    # 88. 二氧化碳利用系统（矿物碳化）
    MINERAL_CARBONATION_CO2_UTILIZATION = "mineral_carbonation_co2_utilization"
    
    # =========================================================================
    # 七、柔性负荷与终端
    # =========================================================================
    # 89. 商业楼宇负荷（空调、照明、插座）
    COMMERCIAL_BUILDING_LOAD = "commercial_building_load"
    # 90. 工业过程可调节负荷
    INDUSTRIAL_ADJUSTABLE_LOAD = "industrial_adjustable_load"
    # 91. 居民需求响应负荷
    RESIDENTIAL_DEMAND_RESPONSE_LOAD = "residential_demand_response_load"
    # 92. 电动汽车充电桩（交流慢充）
    AC_LEVEL2_EV_CHARGER = "ac_level2_ev_charger"
    # 93. 电动汽车充电桩（直流快充）
    DC_FAST_EV_CHARGER = "dc_fast_ev_charger"
    # 94. 电动汽车换电站
    EV_BATTERY_SWAP_STATION = "ev_battery_swap_station"
    # 95. 电动卡车充电桩（大功率）
    HIGH_POWER_ELECTRIC_TRUCK_CHARGERS = "high_power_electric_truck_chargers"
    # 96. 船舶岸电系统
    SHORE_POWER_SYSTEM = "shore_power_system"
    # 97. 电制氢装置（与电网交互）
    POWER_TO_GAS_FLEXIBLE_OPERATION = "power_to_gas_flexible_operation"
    # 98. 电制氨装置（柔性运行）
    POWER_TO_AMMONIA_FLEXIBLE_OPERATION = "power_to_ammonia_flexible_operation"
    # 99. 数据中心负荷（可调节IT负载）
    DATA_CENTER_ADJUSTABLE_LOAD = "data_center_adjustable_load"
    # 100. 空调系统虚拟储能模型
    AIR_CONDITIONING_VIRTUAL_STORAGE = "air_conditioning_virtual_storage"
    
    # =========================================================================
    # 八、输配网络与耦合节点
    # =========================================================================
    # 101. 交流配电网线路（架空/电缆）
    AC_GRID_LINE = "ac_grid_line"
    # 102. 直流配电网线路
    DC_GRID_LINE = "dc_grid_line"
    # 103. 交流/直流换流器
    AC_TO_DC_CONVERTER = "ac_to_dc_converter"
    # 104. 变压器（有载调压）
    LOAD_TAP_CHANGER_TRANSFORMER = "load_tap_changer_transformer"
    # 105. 静态无功补偿器（SVC）
    STATIC_VAR_COMPENSATOR = "static_var_compensator"
    # 106. 固态变压器（SST）
    SOLID_STATE_TRANSFORMER = "solid_state_transformer"
    # 107. 电力电子接口（光伏逆变器）
    PV_INVERTER = "pv_inverter"
    # 108. 电力电子接口（储能变流器）
    ENERGY_STORAGE_CONVERTER = "energy_storage_converter"
    # 109. 天然气输配管网
    NATURAL_GAS_DISTRIBUTION_NETWORK = "natural_gas_distribution_network"
    # 110. 天然气压缩机站
    NATURAL_GAS_COMPRESSOR_STATION = "natural_gas_compressor_station"
    # 111. 天然气门站
    NATURAL_GAS_GATE_STATION = "natural_gas_gate_station"
    # 112. 氢气-天然气混合输送管段
    HYDROGEN_NATURAL_GAS_BLEND_PIPELINE = "hydrogen_natural_gas_blend_pipeline"
    # 113. 热力管网水力模型
    THERMAL_NETWORK_HYDRAULIC_MODEL = "thermal_network_hydraulic_model"
    # 114. 多能源枢纽（电-热-气耦合）
    MULTI_ENERGY_HUB = "multi_energy_hub"
    # 115. 能源路由器（信息物理系统）
    ENERGY_ROUTER = "energy_router"
    
    # =========================================================================
    # 九、控制与辅助系统
    # =========================================================================
    # 116. 能量管理系统（EMS）
    ENERGY_MANAGEMENT_SYSTEM = "energy_management_system"
    # 117. 分布式协同控制器
    DISTRIBUTED_COORDINATED_CONTROLLER = "distributed_coordinated_controller"
    # 118. 频率调节备用系统
    FREQUENCY_REGULATION_RESERVE_SYSTEM = "frequency_regulation_reserve_system"
    # 119. 黑启动电源
    BLACK_START_POWER_SUPPLY = "black_start_power_supply"
    # 120. 并网同步装置
    GRID_SYNCHRONIZATION_DEVICE = "grid_synchronization_device"
    # 121. 故障限流器
    FAULT_CURRENT_LIMITER = "fault_current_limiter"
    # 122. 电能质量治理装置（APF）
    POWER_QUALITY_IMPROVEMENT_DEVICE = "power_quality_improvement_device"
    # 123. 气象预测模块（风光功率预测）
    WEATHER_FORECASTING_MODULE = "weather_forecasting_module"
    # 124. 负荷预测模块
    LOAD_FORECASTING_MODULE = "load_forecasting_module"
    # 125. 碳流追踪模块
    CARBON_FLOW_TRACKING_MODULE = "carbon_flow_tracking_module"
    
    # =========================================================================
    # 十、新兴技术组件
    # =========================================================================
    # 126. 磁约束核聚变实验堆（概念）
    MAGNETIC_CONFINEMENT_FUSION_REACTOR = "magnetic_confinement_fusion_reactor"
    # 127. 空间光伏电站（微波输电）
    SPACE_SOLAR_POWER_STATION = "space_solar_power_station"
    # 128. 海洋温差发电
    OCEAN_THERMAL_ENERGY_CONVERSION = "ocean_thermal_energy_conversion"
    # 129. 人工光合作用装置
    ARTIFICIAL_PHOTOSYNTHESIS_DEVICE = "artificial_photosynthesis_device"
    # 130. 超导储能（SMES）
    SUPERCONDUCTING_MAGNETIC_ENERGY_STORAGE = "superconducting_magnetic_energy_storage"
    # 131. 重力储能（斜坡重块）
    GRAVITY_ENERGY_STORAGE = "gravity_energy_storage"
    # 132. 热声发电装置
    THERMOACOUSTIC_POWER_GENERATOR = "thermoacoustic_power_generator"
    # 133. 放射性同位素热电发电机
    RADIOISOTOPE_THERMOELECTRIC_GENERATOR = "radioisotope_thermoelectric_generator"


@dataclass
class ExtendedEquipmentConfig(PyXESXXNEquipmentConfig):
    """Extended equipment configuration with additional parameters."""
    # Additional parameters for physical modeling
    physical_parameters: Dict[str, Any] = field(default_factory=dict)
    thermodynamic_parameters: Dict[str, Any] = field(default_factory=dict)
    efficiency_map: Optional[Dict[str, Any]] = field(default_factory=dict)
    environmental_parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary with extended parameters."""
        config_dict = super().to_dict()
        
        # Add extended parameters
        config_dict.update({
            'physical_parameters': self.physical_parameters.copy(),
            'thermodynamic_parameters': self.thermodynamic_parameters.copy(),
            'efficiency_map': self.efficiency_map.copy() if self.efficiency_map else {},
            'environmental_parameters': self.environmental_parameters.copy()
        })
            
        
        return config_dict
        
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ExtendedEquipmentConfig':
        """Create configuration from dictionary with extended parameters."""
        # Extract extended parameters
        physical_params = config_dict.pop('physical_parameters', {})
        thermodynamic_params = config_dict.pop('thermodynamic_parameters', {})
        efficiency_map = config_dict.pop('efficiency_map', {})
        environmental_params = config_dict.pop('environmental_parameters', {})
        
        # Create base configuration
        base_config = super().from_dict(config_dict)
        
        # Create extended configuration
        return cls(
            **base_config.__dict__,
            physical_parameters=physical_params,
            thermodynamic_parameters=thermodynamic_params,
            efficiency_map=efficiency_map,
            environmental_parameters=environmental_params
        )


class ExtendedEnergyComponent(PyXESXXNBaseEquipment, abc.ABC):
    """Base class for all extended energy components."""
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[ExtendedEquipmentConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize an extended energy component."""
        # Call parent constructor first to ensure all attributes are initialized
        super().__init__(equipment_id=equipment_id, config=config, location=location)
        
        # Initialize component-specific state
        self._physical_state = {
            'temperature': 25.0,
            'pressure': 1.0,
            'flow_rate': 0.0,
            'internal_state': {},
            'thermodynamic_state': {}
        }
    
    def get_default_scenario(self) -> str:
        """Get the default scenario for this equipment type."""
        return "universal"
    
    def _create_default_config(self, **kwargs) -> ExtendedEquipmentConfig:
        """Create default configuration for the extended component."""
        # Get default config from parent
        base_config = super()._create_default_config(**kwargs)
        
        # Convert to extended config and add default parameters
        return ExtendedEquipmentConfig(
            **base_config.__dict__,
            physical_parameters=self._get_default_physical_parameters(),
            thermodynamic_parameters=self._get_default_thermodynamic_parameters(),
            efficiency_map=self._get_default_efficiency_map(),
            environmental_parameters=self._get_default_environmental_parameters()
        )
    
    def _get_default_physical_parameters(self) -> Dict[str, Any]:
        """Get default physical parameters for the component."""
        return {
            'temperature': 25.0,
            'pressure': 1.0,
            'density': 1.0,
            'specific_heat': 1.0,
            'thermal_conductivity': 1.0
        }
    
    def _get_default_thermodynamic_parameters(self) -> Dict[str, Any]:
        """Get default thermodynamic parameters for the component."""
        return {
            'isentropic_efficiency': 0.85,
            'thermal_efficiency': 0.8,
            'carnot_efficiency': 0.5
        }
    
    def _get_default_efficiency_map(self) -> Dict[str, Any]:
        """Get default efficiency map for the component."""
        return {
            'efficiency_vs_load': [(0.0, 0.0), (0.5, 0.85), (1.0, 0.8)]
        }
    
    def _get_default_environmental_parameters(self) -> Dict[str, Any]:
        """Get default environmental parameters for the component."""
        return {
            'co2_emissions': 0.0,
            'nox_emissions': 0.0,
            'sox_emissions': 0.0,
            'water_consumption': 0.0
        }
    
    @abc.abstractmethod
    def calculate_physical_performance(self, 
                                      input_power: float,
                                      time_step: float = 1.0,
                                      operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate physical performance of the component.
        
        Args:
            input_power: Input power (kW)
            time_step: Time step (hours)
            operating_conditions: Operating conditions (temperature, pressure, etc.)
            
        Returns:
            Dictionary containing physical performance metrics
        """
        pass
    
    def calculate_performance(self, 
                            input_power: float,
                            time_step: float = 1.0,
                            operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate component performance (overrides parent method)."""
        # Calculate physical performance
        physical_perf = self.calculate_physical_performance(
            input_power, time_step, operating_conditions
        )
        
        # Update component state
        self._current_state.update({
            'power_output': physical_perf.get('power_output', 0.0),
            'efficiency': physical_perf.get('efficiency', self.config.efficiency or 0.0),
            'temperature': physical_perf.get('temperature', self._physical_state['temperature']),
            'pressure': physical_perf.get('pressure', self._physical_state['pressure'])
        })
        
        self._physical_state.update({
            'temperature': physical_perf.get('temperature', 25.0),
            'pressure': physical_perf.get('pressure', 1.0),
            'flow_rate': physical_perf.get('flow_rate', 0.0),
            'internal_state': physical_perf.get('internal_state', {}),
            'thermodynamic_state': physical_perf.get('thermodynamic_state', {})
        })
        
        # Update operational hours
        if self._is_operational:
            self._current_state['operational_hours'] += time_step
        
        return physical_perf
    
    def create_components(self, network: PyXESXXNNetwork) -> Dict[str, Any]:
        """Create PyXESXXN components for this equipment."""
        # Default implementation - should be overridden by subclasses
        components = {}
        
        # Create a basic bus if needed
        bus_id = f"bus_{self.equipment_id}"
        if not hasattr(network, 'buses') or bus_id not in network.buses:
            network.add_bus(
                bus_id,
                self.config.supported_carriers[0].value if self.config.supported_carriers else "electricity"
            )
            components['bus'] = bus_id
        
        return components
    
    def get_physical_state(self) -> Dict[str, Any]:
        """Get the current physical state of the component."""
        return self._physical_state.copy()
    
    def update_physical_state(self, **kwargs) -> None:
        """Update the physical state of the component."""
        self._physical_state.update(kwargs)
    
    def get_comprehensive_performance(self, 
                                    input_power: float,
                                    time_step: float = 1.0,
                                    operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get comprehensive performance including physical, thermodynamic, and economic metrics."""
        # Calculate basic performance
        perf = self.calculate_performance(input_power, time_step, operating_conditions)
        
        # Add economic metrics
        costs = self.estimate_costs()
        perf.update(costs)
        
        # Add physical state
        perf['physical_state'] = self.get_physical_state()
        
        # Add environmental metrics
        perf['environmental_impact'] = self.config.environmental_parameters
        
        return perf


# =============================================================================
# Component Factory System
# =============================================================================

_ComponentFactory = Callable[..., ExtendedEnergyComponent]
_component_factories: Dict[ExtendedEquipmentType, _ComponentFactory] = {}


def register_component_factory(component_type: ExtendedEquipmentType, factory: _ComponentFactory) -> None:
    """Register a component factory for a specific equipment type."""
    _component_factories[component_type] = factory


def get_component_factory(component_type: ExtendedEquipmentType) -> Optional[_ComponentFactory]:
    """Get the component factory for a specific equipment type."""
    return _component_factories.get(component_type)


def create_extended_component(component_type: ExtendedEquipmentType, 
                              equipment_id: str, 
                              **kwargs) -> ExtendedEnergyComponent:
    """Create an extended energy component from the given type and parameters.
    
    Args:
        component_type: Type of component to create
        equipment_id: Unique identifier for the component
        **kwargs: Additional parameters for component creation
        
    Returns:
        ExtendedEnergyComponent instance
        
    Raises:
        ValueError: If no factory is registered for the given component type
    """
    factory = get_component_factory(component_type)
    if factory is None:
        raise ValueError(f"No factory registered for component type: {component_type}")
    
    return factory(equipment_id=equipment_id, **kwargs)


# =============================================================================
# Energy Carrier Enumeration Extension
# =============================================================================

# Create a dictionary with original PyXESXXN EnergyCarrier values
extended_energy_carriers = {
    carrier.value: carrier for carrier in PyXESXXNEnergyCarrier
}

# Add additional energy carriers as strings (not Enum members)
additional_carriers = [
    "ammonia", "methanol", "ethanol", "hydrogen_mix",
    "liquid_co2", "compressed_co2", "molten_salt", "synfuel"
]

for carrier in additional_carriers:
    extended_energy_carriers[carrier] = carrier


# =============================================================================
# Utility Functions for Physical Modeling
# =============================================================================

def calculate_carnot_efficiency(t_high: float, t_low: float) -> float:
    """Calculate Carnot efficiency for a heat engine.
    
    Args:
        t_high: High temperature in Kelvin
        t_low: Low temperature in Kelvin
        
    Returns:
        Carnot efficiency (0-1)
    """
    return 1.0 - (t_low / t_high)


def calculate_exergy(energy: float, exergy_efficiency: float = 0.8) -> float:
    """Calculate exergy from energy.
    
    Args:
        energy: Energy in kWh
        exergy_efficiency: Exergy efficiency (0-1)
        
    Returns:
        Exergy in kWh
    """
    return energy * exergy_efficiency


def calculate_thermodynamic_state(temperature: float, pressure: float, 
                                  fluid_properties: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate thermodynamic state of a fluid.
    
    Args:
        temperature: Temperature in °C
        pressure: Pressure in bar
        fluid_properties: Fluid properties dictionary
        
    Returns:
        Thermodynamic state dictionary
    """
    t_kelvin = temperature + 273.15
    
    return {
        'temperature_k': t_kelvin,
        'pressure_bar': pressure,
        'specific_enthalpy': fluid_properties.get('cp', 1.0) * t_kelvin,
        'specific_entropy': fluid_properties.get('cp', 1.0) * np.log(t_kelvin / 298.15),
        'density': fluid_properties.get('density', 1.0) * (pressure / 1.0) * (298.15 / t_kelvin)
    }


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Extended enumerations
    'ExtendedEquipmentType',
    'ExtendedEquipmentCategory',
    
    # Base classes for extended components
    'ExtendedEnergyComponent',
    'ExtendedEquipmentConfig',
    
    # Utility functions
    'create_extended_component',
    'register_component_factory',
    'get_component_factory',
    'calculate_carnot_efficiency',
    'calculate_exergy',
    'calculate_thermodynamic_state'
]
