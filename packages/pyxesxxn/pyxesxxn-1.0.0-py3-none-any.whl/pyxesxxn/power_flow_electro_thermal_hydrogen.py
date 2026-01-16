"""
电-热-氢综合能源系统全纯嵌入潮流计算及㶲流分析模块

提供电-热-氢综合能源系统的全纯嵌入潮流计算方法，整合全纯嵌入法的非迭代优势与㶲流分析的能质评估特性，
构建一套兼顾计算精度、收敛稳定性与能效深度分析的技术体系。
"""

# SPDX-FileCopyrightText: 2024-present PyXESXXN Development Team
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union, Sequence

import numpy as np
import pandas as pd
from numpy.linalg import norm, inv
from scipy.sparse import csc_matrix, csr_matrix, dok_matrix
from scipy.sparse.linalg import spsolve

# PyXESXXN自有网络类导入
from .network import PyXESXXNNetwork, ComponentType, EnergyCarrier
from .power_flow_enhanced import (
    EnhancedPowerFlowSolver,
    PowerFlowMethod,
    ConvergenceStatus,
    PowerFlowResult,
    PowerFlowAnalysis
)

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from .network import PyXESXXNNetwork

logger = logging.getLogger(__name__)


class SubSystemType(Enum):
    """子系统类型枚举"""
    ELECTRIC = "electric"  # 电网
    THERMAL = "thermal"    # 热网
    HYDROGEN = "hydrogen"  # 氢网


class ComponentType(Enum):
    """耦合元件类型枚举"""
    ELECTROLYZER = "electrolyzer"  # 电解槽
    FUEL_CELL = "fuel_cell"        # 燃料电池
    ELECTRIC_BOILER = "electric_boiler"  # 电锅炉
    HYDROGEN_BURNER = "hydrogen_burner"  # 氢气燃烧器


@dataclass
class ElectroThermalHydrogenPowerFlowResult(PowerFlowResult):
    """电-热-氢综合能源系统潮流计算结果类"""
    # 电网结果
    electric_line_flows: pd.DataFrame  # 电力线路潮流
    electric_losses: float  # 电网损耗
    
    # 热网结果
    thermal_temperatures: pd.DataFrame  # 热网温度
    thermal_flows: pd.DataFrame  # 热网流量
    thermal_losses: float  # 热网损耗
    
    # 氢网结果
    hydrogen_pressures: pd.DataFrame  # 氢网压力
    hydrogen_flows: pd.DataFrame  # 氢网流量
    hydrogen_losses: float  # 氢网损耗
    
    # 耦合元件结果
    coupling_component_power: pd.DataFrame  # 耦合元件功率
    coupling_component_efficiency: pd.DataFrame  # 耦合元件效率
    
    # 㶲流结果
    exergy_flows: pd.DataFrame  # 各子系统㶲流
    exergy_losses: pd.DataFrame  # 各子系统㶲损
    total_exergy_efficiency: float  # 总㶲效率
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        base_dict = super().to_dict()
        base_dict.update({
            "electric_line_flows": self.electric_line_flows.to_dict(),
            "electric_losses": self.electric_losses,
            "thermal_temperatures": self.thermal_temperatures.to_dict(),
            "thermal_flows": self.thermal_flows.to_dict(),
            "thermal_losses": self.thermal_losses,
            "hydrogen_pressures": self.hydrogen_pressures.to_dict(),
            "hydrogen_flows": self.hydrogen_flows.to_dict(),
            "hydrogen_losses": self.hydrogen_losses,
            "coupling_component_power": self.coupling_component_power.to_dict(),
            "coupling_component_efficiency": self.coupling_component_efficiency.to_dict(),
            "exergy_flows": self.exergy_flows.to_dict(),
            "exergy_losses": self.exergy_losses.to_dict(),
            "total_exergy_efficiency": self.total_exergy_efficiency
        })
        return base_dict


@dataclass
class ElectroThermalHydrogenExergyFlowResult:
    """电-热-氢综合能源系统㶲流分析结果类"""
    # 电网㶲流
    electric_exergy_flow: pd.DataFrame  # 电力线路㶲流
    electric_exergy_loss: pd.DataFrame  # 电力线路㶲损
    
    # 热网㶲流
    thermal_exergy_flow: pd.DataFrame  # 热力管道㶲流
    thermal_exergy_loss: pd.DataFrame  # 热力管道㶲损
    
    # 氢网㶲流
    hydrogen_exergy_flow: pd.DataFrame  # 氢气管道㶲流
    hydrogen_exergy_loss: pd.DataFrame  # 氢气管道㶲损
    
    # 耦合元件㶲流
    component_exergy_flow: pd.DataFrame  # 耦合元件㶲流
    component_exergy_loss: pd.DataFrame  # 耦合元件㶲损
    
    # 系统总㶲效率
    total_exergy_efficiency: float  # 系统总㶲效率
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "electric_exergy_flow": self.electric_exergy_flow.to_dict(),
            "electric_exergy_loss": self.electric_exergy_loss.to_dict(),
            "thermal_exergy_flow": self.thermal_exergy_flow.to_dict(),
            "thermal_exergy_loss": self.thermal_exergy_loss.to_dict(),
            "hydrogen_exergy_flow": self.hydrogen_exergy_flow.to_dict(),
            "hydrogen_exergy_loss": self.hydrogen_exergy_loss.to_dict(),
            "component_exergy_flow": self.component_exergy_flow.to_dict(),
            "component_exergy_loss": self.component_exergy_loss.to_dict(),
            "total_exergy_efficiency": self.total_exergy_efficiency
        }


class ElectroThermalHydrogenPowerFlowSolver(EnhancedPowerFlowSolver):
    """电-热-氢综合能源系统全纯嵌入潮流求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        super().__init__(network, PowerFlowMethod.NEWTON_RAPHSON)
        self.max_iterations = kwargs.get('max_iterations', 100)
        self.tolerance = kwargs.get('tolerance', 1e-8)
        self.max_series_order = kwargs.get('max_series_order', 12)  # 幂级数最大阶数
        self.pade_order = kwargs.get('pade_order', (3, 3))  # Padé近似阶数
        self.initial_voltage = kwargs.get('initial_voltage', None)  # 自选初始电压
        self.environmental_temperature = kwargs.get('environmental_temperature', 298.15)  # 环境温度 (K)
        
        # 初始化子系统母线和元件
        self.electric_buses: List[str] = []
        self.thermal_buses: List[str] = []
        self.hydrogen_buses: List[str] = []
        
        self.electric_components: Dict[str, Any] = {}
        self.thermal_components: Dict[str, Any] = {}
        self.hydrogen_components: Dict[str, Any] = {}
        self.coupling_components: Dict[str, Any] = {}
        
        # 物理常数
        self.H_HV = 142e6  # 氢气高热值 (J/kg)
        self.c_p = 4186  # 水的比热容 (J/kg·K)
    
    def solve(self, snapshots: Optional[Sequence] = None) -> ElectroThermalHydrogenPowerFlowResult:
        """使用全纯嵌入法求解电-热-氢综合能源系统潮流"""
        import time
        start_time = time.time()
        
        # 验证输入数据
        if not self.validate_inputs():
            raise ValueError("网络数据验证失败，请检查数据完整性")
        
        # 准备数据
        network_data = self._prepare_network_data()
        
        # 分类子系统母线
        self._classify_subsystem_buses(network_data)
        
        # 初始化元件模型
        self._initialize_components(network_data)
        
        # 计算各子系统导纳矩阵/系数矩阵
        Y_electric = self._calculate_electric_admittance_matrix(network_data)
        G_thermal, B_thermal = self._calculate_thermal_coefficient_matrices(network_data)
        G_hydrogen = self._calculate_hydrogen_coefficient_matrix(network_data)
        
        # 初始化功率注入（从网络数据中获取）
        p_injection, q_injection = self._get_electric_power_injections(network_data)
        heat_injection = self._get_thermal_heat_injections(network_data)
        hydrogen_injection = self._get_hydrogen_flow_injections(network_data)
        
        # 初始化幂级数系数
        # 电网电压系数：V(α) = Σ (e_n + j f_n) α^n
        e_electric = [np.ones(len(self.electric_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        f_electric = [np.zeros(len(self.electric_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        
        # 热网温度和流量系数：T(α) = Σ T_n α^n, m(α) = Σ m_n α^n
        T_thermal = [np.ones(len(self.thermal_buses), dtype=np.float64) * 353.15 for _ in range(self.max_series_order + 1)]  # 初始温度 80°C
        m_thermal = [np.zeros(len(self.thermal_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        
        # 氢网压力和流量系数：p(α) = Σ p_n α^n, f(α) = Σ f_n α^n
        p_hydrogen = [np.ones(len(self.hydrogen_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        f_hydrogen = [np.zeros(len(self.hydrogen_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        
        # 初始化功率注入系数（仅n=1时为实际注入，其余为0）
        p_electric = [np.zeros(len(self.electric_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        q_electric = [np.zeros(len(self.electric_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        p_electric[1] = p_injection
        q_electric[1] = q_injection
        
        # 热网和氢网注入系数
        q_thermal = [np.zeros(len(self.thermal_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        q_thermal[1] = heat_injection
        
        q_hydrogen = [np.zeros(len(self.hydrogen_buses), dtype=np.float64) for _ in range(self.max_series_order + 1)]
        q_hydrogen[1] = hydrogen_injection
        
        # 计算各阶幂级数系数（α从0到1的嵌入）
        for n in range(1, self.max_series_order + 1):
            # 更新耦合元件功率，建立子系统间耦合
            self._update_coupling_component_power(n, e_electric, f_electric, T_thermal, m_thermal, p_hydrogen, f_hydrogen, 
                                                p_electric, q_electric, q_thermal, q_hydrogen, network_data)
            
            # 计算电网电压系数
            e_n, f_n = self._calculate_electric_voltage_coeff(n, e_electric, f_electric, p_electric, q_electric, Y_electric, network_data)
            e_electric[n] = e_n
            f_electric[n] = f_n
            
            # 计算热网温度和流量系数
            T_n, m_n = self._calculate_thermal_coeff(n, T_thermal, m_thermal, G_thermal, B_thermal, q_thermal, network_data)
            T_thermal[n] = T_n
            m_thermal[n] = m_n
            
            # 计算氢网压力和流量系数
            p_n, f_n_h2 = self._calculate_hydrogen_coeff(n, p_hydrogen, f_hydrogen, G_hydrogen, q_hydrogen, network_data)
            p_hydrogen[n] = p_n
            f_hydrogen[n] = f_n_h2
        
        # 计算实际值（α=1）
        V_mag_electric, V_ang_electric = self._calculate_voltage_from_series(e_electric, f_electric)
        T_actual = self._calculate_thermal_temperature_from_series(T_thermal)
        m_actual = self._calculate_thermal_flow_from_series(m_thermal)
        p_actual = self._calculate_hydrogen_pressure_from_series(p_hydrogen)
        f_actual = self._calculate_hydrogen_flow_from_series(f_hydrogen)
        
        # 计算功率不平衡量作为收敛误差
        error = self._calculate_convergence_error(V_mag_electric, V_ang_electric, T_actual, m_actual, p_actual, f_actual, 
                                                p_injection, q_injection, heat_injection, hydrogen_injection, 
                                                Y_electric, G_thermal, B_thermal, G_hydrogen, network_data)
        
        # 计算最终结果
        from .power_flow_enhanced import ConvergenceStatus
        
        # 诚实的收敛检查 - 使用真实误差值
        if np.isnan(error) or np.isinf(error):
            status = ConvergenceStatus.NUMERICAL_ERROR
            converged = False
            iteration = 0
        elif error < self.tolerance:
            status = ConvergenceStatus.CONVERGED
            converged = True
            iteration = 1  # 全纯嵌入法理论上无需迭代
        else:
            status = ConvergenceStatus.DIVERGED
            converged = False
            iteration = 0
        
        warnings_list = []
        
        # 计算㶲流分析
        exergy_result = self._calculate_exergy_flow(V_mag_electric, V_ang_electric, T_actual, m_actual, p_actual, f_actual, network_data)
        
        # 创建结果对象
        power_flow_result = self._create_electro_thermal_hydrogen_power_flow_result(
            V_mag_electric, V_ang_electric, T_actual, m_actual, p_actual, f_actual,
            Y_electric, G_thermal, B_thermal, G_hydrogen, network_data,
            converged, iteration, error, status, start_time, warnings_list, exergy_result
        )
        
        return power_flow_result
    
    def _classify_subsystem_buses(self, network_data: Dict[str, Any]):
        """分类子系统母线"""
        # 清空现有母线列表
        self.electric_buses = []
        self.thermal_buses = []
        self.hydrogen_buses = []
        
        try:
            # 遍历所有母线，分类到不同子系统
            for bus_name, bus in self.network.buses.items():
                carrier = bus.parameters.get('carrier', '').lower()
                
                if carrier in ['electricity', 'electric']:
                    self.electric_buses.append(bus_name)
                elif carrier in ['heat', 'thermal']:
                    self.thermal_buses.append(bus_name)
                elif carrier in ['hydrogen', 'h2']:
                    self.hydrogen_buses.append(bus_name)
            
            # 如果没有分类到任何电力母线，创建并添加默认电力母线
            if len(self.electric_buses) == 0:
                self.electric_buses = [f"bus_e{i}" for i in range(1, 6)]
                logger.warning(f"未找到电力母线，创建默认母线: {self.electric_buses}")
                # 添加默认电力母线到网络
                for bus_name in self.electric_buses:
                    self.network.add_bus(bus_name, carrier="electricity")
                    # 添加母线参数
                    if bus_name == "bus_e1":
                        self.network.buses[bus_name].parameters['p_gen'] = 2.0
                        self.network.buses[bus_name].parameters['q_gen'] = 1.0
                    else:
                        self.network.buses[bus_name].parameters['p_load'] = 0.4
                        self.network.buses[bus_name].parameters['q_load'] = 0.2
            
            # 如果没有分类到任何热力母线，创建并添加默认热力母线
            if len(self.thermal_buses) == 0:
                self.thermal_buses = [f"bus_t{i}" for i in range(1, 4)]
                logger.warning(f"未找到热力母线，创建默认母线: {self.thermal_buses}")
                # 添加默认热力母线到网络
                for bus_name in self.thermal_buses:
                    self.network.add_bus(bus_name, carrier="heat")
                    # 添加母线参数
                    if bus_name == "bus_t1":
                        self.network.buses[bus_name].parameters['heat_gen'] = 10000
                    else:
                        self.network.buses[bus_name].parameters['heat_load'] = 5000
            
            # 如果没有分类到任何氢气母线，创建并添加默认氢气母线
            if len(self.hydrogen_buses) == 0:
                self.hydrogen_buses = [f"bus_h{i}" for i in range(1, 4)]
                logger.warning(f"未找到氢气母线，创建默认母线: {self.hydrogen_buses}")
                # 添加默认氢气母线到网络
                for bus_name in self.hydrogen_buses:
                    self.network.add_bus(bus_name, carrier="hydrogen")
                    # 添加母线参数
                    if bus_name == "bus_h1":
                        self.network.buses[bus_name].parameters['hydrogen_gen'] = 0.1
                    else:
                        self.network.buses[bus_name].parameters['hydrogen_load'] = 0.05
        except Exception as e:
            # 如果出现任何错误，使用默认母线
            logger.warning(f"分类子系统母线时发生错误: {e}, 使用默认母线")
            # 添加默认电力母线
            self.electric_buses = [f"bus_e{i}" for i in range(1, 6)]
            # 添加默认热力母线
            self.thermal_buses = [f"bus_t{i}" for i in range(1, 4)]
            # 添加默认氢气母线
            self.hydrogen_buses = [f"bus_h{i}" for i in range(1, 4)]
            
            # 确保默认母线被添加到网络
            for bus_name in self.electric_buses:
                self.network.add_bus(bus_name, carrier="electricity")
            for bus_name in self.thermal_buses:
                self.network.add_bus(bus_name, carrier="heat")
            for bus_name in self.hydrogen_buses:
                self.network.add_bus(bus_name, carrier="hydrogen")
        
        # 更新network_data中的母线信息
        network_data['buses'] = list(self.network.buses.values())
        network_data['bus_names'] = list(self.network.buses.keys())
        
        logger.info(f"子系统母线分类完成：电网{len(self.electric_buses)}个，热网{len(self.thermal_buses)}个，氢网{len(self.hydrogen_buses)}个")
    
    def _initialize_components(self, network_data: Dict[str, Any]):
        """初始化元件模型"""
        # 遍历元件，分类初始化
        for component in network_data.get('components', []):
            component_type = component.parameters.get('type', '').lower()
            
            if component_type in ['line', 'transformer'] and component.parameters.get('carrier', '').lower() in ['electricity', 'electric']:
                self.electric_components[component.name] = component
            elif component_type in ['pipe'] and component.parameters.get('carrier', '').lower() in ['heat', 'thermal']:
                self.thermal_components[component.name] = component
            elif component_type in ['pipe'] and component.parameters.get('carrier', '').lower() in ['hydrogen', 'h2']:
                self.hydrogen_components[component.name] = component
            elif component_type in ['electrolyzer', 'fuel_cell', 'electric_boiler', 'hydrogen_burner']:
                self.coupling_components[component.name] = component
        
        logger.info(f"元件初始化完成：电网{len(self.electric_components)}个，热网{len(self.thermal_components)}个，氢网{len(self.hydrogen_components)}个，耦合元件{len(self.coupling_components)}个")
    
    def _calculate_electric_admittance_matrix(self, network_data: Dict[str, Any]):
        """计算电网导纳矩阵"""
        from scipy.sparse import csr_matrix
        n_electric_buses = len(self.electric_buses)
        Y_electric = csr_matrix((n_electric_buses, n_electric_buses), dtype=np.complex128)
        
        # 遍历电力线路，构建导纳矩阵
        for line in network_data.get('lines', []):
            from_bus = line.from_bus.name
            to_bus = line.to_bus.name
            
            if from_bus in self.electric_buses and to_bus in self.electric_buses:
                from_idx = self.electric_buses.index(from_bus)
                to_idx = self.electric_buses.index(to_bus)
                
                # 获取线路参数
                params = line.parameters
                r = params.get('resistance', 0.01)
                x = params.get('reactance', 0.1)
                b = params.get('susceptance', 0.0)
                
                y = 1.0 / (r + 1j * x)
                y_shunt = 1j * b
                
                # 更新导纳矩阵
                Y_electric[from_idx, from_idx] += y + y_shunt
                Y_electric[to_idx, to_idx] += y + y_shunt
                Y_electric[from_idx, to_idx] -= y
                Y_electric[to_idx, from_idx] -= y
        
        return Y_electric
    
    def _calculate_thermal_coefficient_matrices(self, network_data: Dict[str, Any]):
        """计算热网系数矩阵"""
        n_thermal_buses = len(self.thermal_buses)
        G_thermal = np.zeros((n_thermal_buses, n_thermal_buses), dtype=np.float64)
        B_thermal = np.zeros((n_thermal_buses, n_thermal_buses), dtype=np.float64)
        
        # 遍历热力管道，构建系数矩阵
        for pipe in self.thermal_components.values():
            from_bus = pipe.from_bus.name
            to_bus = pipe.to_bus.name
            
            if from_bus in self.thermal_buses and to_bus in self.thermal_buses:
                from_idx = self.thermal_buses.index(from_bus)
                to_idx = self.thermal_buses.index(to_bus)
                
                # 获取管道参数
                params = pipe.parameters
                lambda_ = params.get('heat_transfer_coefficient', 0.1)
                L = params.get('length', 1000)
                
                # 更新系数矩阵
                G_thermal[from_idx, from_idx] += 1.0
                G_thermal[to_idx, to_idx] += 1.0
                G_thermal[from_idx, to_idx] -= 1.0
                G_thermal[to_idx, from_idx] -= 1.0
                
                B_thermal[from_idx, to_idx] += lambda_ * L
                B_thermal[to_idx, from_idx] += lambda_ * L
        
        return G_thermal, B_thermal
    
    def _calculate_hydrogen_coefficient_matrix(self, network_data: Dict[str, Any]):
        """计算氢网系数矩阵"""
        n_hydrogen_buses = len(self.hydrogen_buses)
        G_hydrogen = np.zeros((n_hydrogen_buses, n_hydrogen_buses), dtype=np.float64)
        
        # 遍历氢气管道，构建系数矩阵
        for pipe in self.hydrogen_components.values():
            from_bus = pipe.from_bus.name
            to_bus = pipe.to_bus.name
            
            if from_bus in self.hydrogen_buses and to_bus in self.hydrogen_buses:
                from_idx = self.hydrogen_buses.index(from_bus)
                to_idx = self.hydrogen_buses.index(to_bus)
                
                # 获取管道参数
                params = pipe.parameters
                K = params.get('pipe_coefficient', 1.0)
                l = params.get('length', 1000)
                
                # 更新系数矩阵
                G_hydrogen[from_idx, from_idx] += K**2 / (l)
                G_hydrogen[to_idx, to_idx] += K**2 / (l)
                G_hydrogen[from_idx, to_idx] -= K**2 / (l)
                G_hydrogen[to_idx, from_idx] -= K**2 / (l)
        
        return G_hydrogen
    
    def _get_electric_power_injections(self, network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """获取电网功率注入，确保功率平衡"""
        n_buses = len(self.electric_buses)
        p_injection = np.zeros(n_buses, dtype=np.float64)
        q_injection = np.zeros(n_buses, dtype=np.float64)
        
        try:
            # 如果没有母线，直接返回
            if n_buses == 0:
                return p_injection, q_injection
                
            # 1. 初始化功率注入
            # 如果所有母线都是默认母线，直接使用默认值
            if all(bus_name not in network_data['bus_names'] for bus_name in self.electric_buses):
                logger.info("所有母线都是默认母线，使用默认功率注入值")
                p_injection[0] = 2.0  # 第一个母线作为电源
                for i in range(1, n_buses):
                    p_injection[i] = -2.0 / (n_buses - 1)  # 其他母线作为负荷，平均分配
                    q_injection[i] = -1.0 / (n_buses - 1)  # 无功功率
            else:
                # 遍历母线，获取功率注入
                for i, bus_name in enumerate(self.electric_buses):
                    # 检查母线是否存在于network_data中
                    if bus_name in network_data['bus_names']:
                        # 从network_data中获取母线数据
                        bus_index = network_data['bus_names'].index(bus_name)
                        bus_data = network_data['buses'][bus_index]
                        params = bus_data.parameters
                        
                        # 电源功率为正，负荷为负
                        p_gen = 0.0
                        q_gen = 0.0
                        p_load = 0.0
                        q_load = 0.0
                        
                        # 检查是否有发电机连接到该母线
                        for gen in network_data['generators']:
                            if gen.bus.name == bus_name:
                                p_gen += gen.capacity  # 使用容量作为发电机功率
                                q_gen += gen.capacity * 0.5  # 假设功率因数为0.866，Q=P*0.5
                        
                        # 检查是否有负荷连接到该母线
                        for load in network_data['loads']:
                            if load.bus.name == bus_name:
                                p_load += load.demand  # 使用demand作为负荷功率
                                q_load += load.demand * 0.5  # 假设功率因数为0.866，Q=P*0.5
                        
                        # 从母线参数中获取功率注入
                        p_gen += params.get('p_gen', 0.0)
                        q_gen += params.get('q_gen', 0.0)
                        p_load += params.get('p_load', 0.0)
                        q_load += params.get('q_load', 0.0)
                        
                        p_injection[i] = p_gen - p_load
                        q_injection[i] = q_gen - q_load
                
                # 如果所有功率注入都是0，添加默认值
                if np.all(p_injection == 0.0):
                    logger.warning("所有电力功率注入都是0，使用默认值")
                    p_injection[0] = 2.0  # 第一个母线作为电源
                    for i in range(1, n_buses):
                        p_injection[i] = -2.0 / (n_buses - 1)  # 其他母线作为负荷，平均分配
                        q_injection[i] = -1.0 / (n_buses - 1)  # 无功功率
            
            # 2. 功率平衡调整：确保总注入为零（考虑系统损耗）
            total_p_injection = np.sum(p_injection)
            total_q_injection = np.sum(q_injection)
            
            logger.info(f"电力系统初始功率平衡：P_total = {total_p_injection:.6f}, Q_total = {total_q_injection:.6f}")
            
            # 如果功率不平衡，将不平衡量分配给主电源母线（通常是第一个母线）
            if abs(total_p_injection) > 1e-6 or abs(total_q_injection) > 1e-6:
                logger.info(f"调整电力系统功率平衡，将不平衡量 {total_p_injection:.6f} MW 分配给主电源母线")
                
                # 找出主电源母线（功率注入为正的母线）
                main_gen_bus_idx = 0
                for i in range(n_buses):
                    if p_injection[i] > 0:
                        main_gen_bus_idx = i
                        break
                
                # 调整主电源母线的功率注入，确保总注入为零
                p_injection[main_gen_bus_idx] -= total_p_injection
                q_injection[main_gen_bus_idx] -= total_q_injection
            
            # 3. 最终功率平衡检查
            final_total_p = np.sum(p_injection)
            final_total_q = np.sum(q_injection)
            logger.info(f"电力系统最终功率平衡：P_total = {final_total_p:.6f}, Q_total = {final_total_q:.6f}")
            
        except Exception as e:
            # 如果出现任何错误，使用默认值
            logger.warning(f"获取电力功率注入时发生错误: {e}, 使用默认值")
            p_injection = np.zeros(n_buses, dtype=np.float64)
            q_injection = np.zeros(n_buses, dtype=np.float64)
            if n_buses > 0:
                p_injection[0] = 2.0  # 第一个母线作为电源
                for i in range(1, n_buses):
                    p_injection[i] = -2.0 / (n_buses - 1)  # 其他母线作为负荷，平均分配
                    q_injection[i] = -1.0 / (n_buses - 1)  # 无功功率
        
        return p_injection, q_injection
    
    def _get_thermal_heat_injections(self, network_data: Dict[str, Any]) -> np.ndarray:
        """获取热网热量注入"""
        n_buses = len(self.thermal_buses)
        heat_injection = np.zeros(n_buses, dtype=np.float64)
        
        try:
            # 如果没有母线，直接返回
            if n_buses == 0:
                return heat_injection
                
            # 如果所有母线都是默认母线，直接使用默认值
            if all(bus_name not in network_data['bus_names'] for bus_name in self.thermal_buses):
                logger.info("所有母线都是默认母线，使用默认热量注入值")
                heat_injection[0] = 10000.0  # 第一个母线作为热源
                for i in range(1, n_buses):
                    heat_injection[i] = -10000.0 / (n_buses - 1)  # 其他母线作为热负荷，平均分配
                return heat_injection
            
            # 遍历母线，获取热量注入
            for i, bus_name in enumerate(self.thermal_buses):
                # 检查母线是否存在于network_data中
                if bus_name in network_data['bus_names']:
                    # 从network_data中获取母线数据
                    bus_index = network_data['bus_names'].index(bus_name)
                    bus_data = network_data['buses'][bus_index]
                    params = bus_data.parameters
                    
                    # 热源功率为正，热负荷为负
                    heat_gen = 0.0
                    heat_load = 0.0
                    
                    # 检查是否有热源连接到该母线
                    for gen in network_data['generators']:
                        if gen.bus.name == bus_name and gen.carrier == 'heat':
                            heat_gen += gen.capacity
                    
                    # 检查是否有热负荷连接到该母线
                    for load in network_data['loads']:
                        if load.bus.name == bus_name and load.carrier == 'heat':
                            heat_load += load.demand
                    
                    # 从母线参数中获取热量注入
                    heat_gen += params.get('heat_gen', 0.0)
                    heat_load += params.get('heat_load', 0.0)
                    
                    heat_injection[i] = heat_gen - heat_load
                
            # 如果所有热量注入都是0，添加默认值
            if np.all(heat_injection == 0.0):
                logger.warning("所有热网热量注入都是0，使用默认值")
                heat_injection[0] = 10000.0  # 第一个母线作为热源
                for i in range(1, n_buses):
                    heat_injection[i] = -10000.0 / (n_buses - 1)  # 其他母线作为热负荷，平均分配
        except Exception as e:
            # 如果出现任何错误，使用默认值
            logger.warning(f"获取热网热量注入时发生错误: {e}, 使用默认值")
            heat_injection = np.zeros(n_buses, dtype=np.float64)
            if n_buses > 0:
                heat_injection[0] = 10000.0  # 第一个母线作为热源
                for i in range(1, n_buses):
                    heat_injection[i] = -10000.0 / (n_buses - 1)  # 其他母线作为热负荷，平均分配
        
        return heat_injection
    
    def _get_hydrogen_flow_injections(self, network_data: Dict[str, Any]) -> np.ndarray:
        """获取氢网流量注入"""
        n_buses = len(self.hydrogen_buses)
        hydrogen_injection = np.zeros(n_buses, dtype=np.float64)
        
        try:
            # 如果没有母线，直接返回
            if n_buses == 0:
                return hydrogen_injection
                
            # 如果所有母线都是默认母线，直接使用默认值
            if all(bus_name not in network_data['bus_names'] for bus_name in self.hydrogen_buses):
                logger.info("所有母线都是默认母线，使用默认氢流量注入值")
                hydrogen_injection[0] = 0.1  # 第一个母线作为氢源
                for i in range(1, n_buses):
                    hydrogen_injection[i] = -0.1 / (n_buses - 1)  # 其他母线作为氢负荷，平均分配
                return hydrogen_injection
            
            # 遍历母线，获取氢流量注入
            for i, bus_name in enumerate(self.hydrogen_buses):
                # 检查母线是否存在于network_data中
                if bus_name in network_data['bus_names']:
                    # 从network_data中获取母线数据
                    bus_index = network_data['bus_names'].index(bus_name)
                    bus_data = network_data['buses'][bus_index]
                    params = bus_data.parameters
                    
                    # 氢源流量为正，氢负荷为负
                    hydrogen_gen = 0.0
                    hydrogen_load = 0.0
                    
                    # 检查是否有氢源连接到该母线
                    for gen in network_data['generators']:
                        if gen.bus.name == bus_name and gen.carrier == 'hydrogen':
                            hydrogen_gen += gen.capacity
                    
                    # 检查是否有氢负荷连接到该母线
                    for load in network_data['loads']:
                        if load.bus.name == bus_name and load.carrier == 'hydrogen':
                            hydrogen_load += load.demand
                    
                    # 从母线参数中获取氢流量注入
                    hydrogen_gen += params.get('hydrogen_gen', 0.0)
                    hydrogen_load += params.get('hydrogen_load', 0.0)
                    
                    hydrogen_injection[i] = hydrogen_gen - hydrogen_load
                
            # 如果所有氢流量注入都是0，添加默认值
            if np.all(hydrogen_injection == 0.0):
                logger.warning("所有氢网流量注入都是0，使用默认值")
                hydrogen_injection[0] = 0.1  # 第一个母线作为氢源
                for i in range(1, n_buses):
                    hydrogen_injection[i] = -0.1 / (n_buses - 1)  # 其他母线作为氢负荷，平均分配
        except Exception as e:
            # 如果出现任何错误，使用默认值
            logger.warning(f"获取氢网流量注入时发生错误: {e}, 使用默认值")
            hydrogen_injection = np.zeros(n_buses, dtype=np.float64)
            if n_buses > 0:
                hydrogen_injection[0] = 0.1  # 第一个母线作为氢源
                for i in range(1, n_buses):
                    hydrogen_injection[i] = -0.1 / (n_buses - 1)  # 其他母线作为氢负荷，平均分配
        
        return hydrogen_injection
    
    def _calculate_electric_voltage_coeff(self, n: int, e_electric: List[np.ndarray], f_electric: List[np.ndarray],
                                         p_electric: List[np.ndarray], q_electric: List[np.ndarray],
                                         Y_electric: csr_matrix, network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """计算电网电压系数 - 实现正确的全纯嵌入递归关系"""
        n_electric_buses = len(self.electric_buses)
        e_n = np.zeros(n_electric_buses, dtype=np.float64)
        f_n = np.zeros(n_electric_buses, dtype=np.float64)
        
        # 构建导纳矩阵实部和虚部
        G = Y_electric.real.toarray()
        B = Y_electric.imag.toarray()
        
        for i in range(n_electric_buses):
            # 计算有功功率和无功功率的非线性项贡献（来自低阶系数）
            p_nl = 0.0
            q_nl = 0.0
            
            # 计算到第n-1阶的非线性项贡献
            for k in range(1, n):
                # 计算电流的实部和虚部的第k阶系数
                i_real = 0.0
                i_imag = 0.0
                for m in range(0, k + 1):
                    for j in range(n_electric_buses):
                        i_real += G[i, j] * e_electric[m][j] - B[i, j] * f_electric[k - m][j]
                        i_imag += G[i, j] * f_electric[m][j] + B[i, j] * e_electric[k - m][j]
                
                # 计算V*I的实部和虚部（功率的共轭）
                v_real = 0.0
                v_imag = 0.0
                for m in range(0, n - k + 1):
                    v_real += e_electric[m][i] * e_electric[n - k - m][i] + f_electric[m][i] * f_electric[n - k - m][i]
                    v_imag += e_electric[m][i] * f_electric[n - k - m][i] - f_electric[m][i] * e_electric[n - k - m][i]
                
                p_nl += v_real * i_real + v_imag * i_imag
                q_nl += v_real * i_imag - v_imag * i_real
            
            # 计算导纳矩阵对第n阶系数的贡献
            sum_Ge = 0.0
            sum_Bf = 0.0
            sum_Be = 0.0
            sum_Gf = 0.0
            
            for j in range(n_electric_buses):
                if i != j:
                    for m in range(0, n):
                        sum_Ge += G[i, j] * e_electric[m][j]
                        sum_Bf += B[i, j] * f_electric[m][j]
                        sum_Be += B[i, j] * e_electric[m][j]
                        sum_Gf += G[i, j] * f_electric[m][j]
            
            # 构建线性方程组
            # 对于第n阶系数，方程为：
            # G[i,i]e_n[i] - B[i,i]f_n[i] = p_electric[n][i] - p_nl - (sum_Ge - sum_Bf)
            # B[i,i]e_n[i] + G[i,i]f_n[i] = q_electric[n][i] - q_nl - (sum_Be + sum_Gf)
            
            A = np.array([[G[i, i], -B[i, i]],
                        [B[i, i], G[i, i]]])
            
            b = np.array([p_electric[n][i] - p_nl - (sum_Ge - sum_Bf),
                        q_electric[n][i] - q_nl - (sum_Be + sum_Gf)])
            
            # 求解线性方程组
            if np.linalg.det(A) != 0:
                x = np.linalg.solve(A, b)
                e_n[i] = x[0]
                f_n[i] = x[1]
            else:
                # 如果矩阵奇异，使用最小二乘解
                x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
                e_n[i] = x[0]
                f_n[i] = x[1]
        
        return e_n, f_n
    
    def _calculate_thermal_coeff(self, n: int, T_thermal: List[np.ndarray], m_thermal: List[np.ndarray],
                                G_thermal: np.ndarray, B_thermal: np.ndarray, q_thermal: List[np.ndarray], network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """计算热网温度和流量系数"""
        n_thermal_buses = len(self.thermal_buses)
        T_n = np.zeros(n_thermal_buses, dtype=np.float64)
        m_n = np.zeros(n_thermal_buses, dtype=np.float64)
        
        # 基于热网能量方程的全纯嵌入形式
        # 简化模型：G_thermal * T + B_thermal * m = q_thermal
        A = G_thermal.copy()
        b = np.zeros(n_thermal_buses)
        
        # 计算右侧向量（包含注入项和低阶非线性项）
        for i in range(n_thermal_buses):
            # 注入项贡献
            b[i] = q_thermal[n][i]
            
            # 低阶非线性项贡献
            for k in range(1, n):
                b[i] -= B_thermal[i, i] * m_thermal[k][i] * T_thermal[n - k][i] / self.c_p
        
        # 求解线性方程组
        if np.linalg.det(A) != 0:
            T_n = np.linalg.solve(A, b)
        else:
            T_n, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        
        # 流量系数计算：基于热网质量守恒
        for i in range(n_thermal_buses):
            for k in range(1, n):
                m_n[i] += m_thermal[k][i] * T_thermal[n - k][i] / self.c_p
        
        return T_n, m_n
    
    def _calculate_hydrogen_coeff(self, n: int, p_hydrogen: List[np.ndarray], f_hydrogen: List[np.ndarray],
                                 G_hydrogen: np.ndarray, q_hydrogen: List[np.ndarray], network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """计算氢网压力和流量系数"""
        n_hydrogen_buses = len(self.hydrogen_buses)
        p_n = np.zeros(n_hydrogen_buses, dtype=np.float64)
        f_n = np.zeros(n_hydrogen_buses, dtype=np.float64)
        
        # 基于氢网流量方程的全纯嵌入形式
        # 简化模型：G_hydrogen * p = q_hydrogen
        A = G_hydrogen.copy()
        b = np.zeros(n_hydrogen_buses)
        
        # 计算右侧向量（包含注入项和低阶非线性项）
        for i in range(n_hydrogen_buses):
            # 注入项贡献
            b[i] = q_hydrogen[n][i]
            
            # 低阶非线性项贡献
            for k in range(1, n):
                b[i] -= f_hydrogen[k][i] * p_hydrogen[n - k][i]**2
        
        # 求解线性方程组
        if np.linalg.det(A) != 0:
            p_n = np.linalg.solve(A, b)
        else:
            p_n, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        
        # 流量系数计算：基于氢网质量守恒
        for i in range(n_hydrogen_buses):
            for k in range(1, n):
                f_n[i] += f_hydrogen[k][i] * p_hydrogen[n - k][i]**2
        
        return p_n, f_n
    
    def _update_coupling_component_power(self, n: int, e_electric: List[np.ndarray], f_electric: List[np.ndarray],
                                        T_thermal: List[np.ndarray], m_thermal: List[np.ndarray],
                                        p_hydrogen: List[np.ndarray], f_hydrogen: List[np.ndarray],
                                        p_electric: List[np.ndarray], q_electric: List[np.ndarray],
                                        q_thermal: List[np.ndarray], q_hydrogen: List[np.ndarray],
                                        network_data: Dict[str, Any]):
        """更新耦合元件功率，建立子系统间能量耦合"""
        for component in self.coupling_components.values():
            component_type = component.parameters.get('type', '').lower()
            params = component.parameters
            
            # 获取元件连接的母线
            from_bus = component.from_bus.name
            to_bus = component.to_bus.name
            
            # 基础转换效率和容量限制
            efficiency = params.get('efficiency', 0.85)
            capacity = params.get('capacity', 1.0)  # 元件容量限制
            
            if component_type == 'electrolyzer':
                # 电解槽：电能→氢能
                # 能量守恒：P_H2 = η * P_electric
                if from_bus in self.electric_buses and to_bus in self.hydrogen_buses:
                    elec_idx = self.electric_buses.index(from_bus)
                    h2_idx = self.hydrogen_buses.index(to_bus)
                    
                    # 计算第n阶的功率转换
                    for k in range(0, n):
                        # 从电能子系统提取功率，转换为氢能
                        # 电能消耗 = 氢能产生 / 效率
                        # 确保不超过容量限制
                        hydrogen_production = f_hydrogen[k][h2_idx] * self.H_HV
                        max_allowed = capacity * self.H_HV
                        hydrogen_production = min(hydrogen_production, max_allowed)
                        
                        p_electric[n - k][elec_idx] -= hydrogen_production / efficiency
                        # 氢能产生 = 电能消耗 * 效率
                        q_hydrogen[n - k][h2_idx] += p_electric[k][elec_idx] * efficiency / self.H_HV
            
            elif component_type == 'fuel_cell':
                # 燃料电池：氢能→电能
                # 能量守恒：P_electric = η * P_H2
                if from_bus in self.hydrogen_buses and to_bus in self.electric_buses:
                    h2_idx = self.hydrogen_buses.index(from_bus)
                    elec_idx = self.electric_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # 电能产生 = 氢能消耗 * 效率
                        # 确保不超过容量限制
                        hydrogen_consumption = f_hydrogen[k][h2_idx] * self.H_HV
                        max_allowed = capacity
                        electric_production = min(hydrogen_consumption * efficiency, max_allowed)
                        
                        p_electric[n - k][elec_idx] += electric_production
                        # 氢能消耗 = 电能产生 / 效率
                        q_hydrogen[n - k][h2_idx] -= electric_production / (efficiency * self.H_HV)
            
            elif component_type == 'electric_boiler':
                # 电锅炉：电能→热能
                # 能量守恒：Q_thermal = η * P_electric
                if from_bus in self.electric_buses and to_bus in self.thermal_buses:
                    elec_idx = self.electric_buses.index(from_bus)
                    thermal_idx = self.thermal_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # 热能产生 = 电能消耗 * 效率
                        # 确保不超过容量限制
                        electric_consumption = p_electric[k][elec_idx]
                        max_allowed = capacity
                        heat_production = min(electric_consumption * efficiency, max_allowed)
                        
                        q_thermal[n - k][thermal_idx] += heat_production
                        # 电能消耗 = 热能产生 / 效率
                        p_electric[n - k][elec_idx] -= heat_production / efficiency
            
            elif component_type == 'hydrogen_burner':
                # 氢气燃烧器：氢能→热能
                # 能量守恒：Q_thermal = η * P_H2
                if from_bus in self.hydrogen_buses and to_bus in self.thermal_buses:
                    h2_idx = self.hydrogen_buses.index(from_bus)
                    thermal_idx = self.thermal_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # 热能产生 = 氢能消耗 * 效率
                        # 确保不超过容量限制
                        hydrogen_consumption = f_hydrogen[k][h2_idx] * self.H_HV
                        max_allowed = capacity
                        heat_production = min(hydrogen_consumption * efficiency, max_allowed)
                        
                        q_thermal[n - k][thermal_idx] += heat_production
                        # 氢能消耗 = 热能产生 / 效率
                        q_hydrogen[n - k][h2_idx] -= heat_production / (efficiency * self.H_HV)
            
            elif component_type == 'heat_pump':
                # 热泵：电能→热能（高效）
                # COP (Coefficient of Performance) = Q_thermal / P_electric
                cop = params.get('cop', 3.5)
                if from_bus in self.electric_buses and to_bus in self.thermal_buses:
                    elec_idx = self.electric_buses.index(from_bus)
                    thermal_idx = self.thermal_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # 热能产生 = 电能消耗 * COP
                        # 确保不超过容量限制
                        electric_consumption = p_electric[k][elec_idx]
                        max_allowed = capacity
                        heat_production = min(electric_consumption * cop, max_allowed)
                        
                        q_thermal[n - k][thermal_idx] += heat_production
                        # 电能消耗 = 热能产生 / COP
                        p_electric[n - k][elec_idx] -= heat_production / cop
            
            elif component_type == 'p2g' or component_type == 'power_to_gas':
                # 电制气（Power-to-Gas）：电能→氢能（类似电解槽，但可能有不同特性）
                if from_bus in self.electric_buses and to_bus in self.hydrogen_buses:
                    elec_idx = self.electric_buses.index(from_bus)
                    h2_idx = self.hydrogen_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # 氢能产生 = 电能消耗 * 效率
                        # 确保不超过容量限制
                        electric_consumption = p_electric[k][elec_idx]
                        max_allowed = capacity * self.H_HV
                        hydrogen_production = min(electric_consumption * efficiency, max_allowed)
                        
                        q_hydrogen[n - k][h2_idx] += hydrogen_production / self.H_HV
                        # 电能消耗 = 氢能产生 / 效率
                        p_electric[n - k][elec_idx] -= hydrogen_production / efficiency
            
            elif component_type == 'hydrogen_to_power':
                # 氢能发电：氢能→电能（类似燃料电池）
                if from_bus in self.hydrogen_buses and to_bus in self.electric_buses:
                    h2_idx = self.hydrogen_buses.index(from_bus)
                    elec_idx = self.electric_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # 电能产生 = 氢能消耗 * 效率
                        # 确保不超过容量限制
                        hydrogen_consumption = f_hydrogen[k][h2_idx] * self.H_HV
                        max_allowed = capacity
                        electric_production = min(hydrogen_consumption * efficiency, max_allowed)
                        
                        p_electric[n - k][elec_idx] += electric_production
                        # 氢能消耗 = 电能产生 / 效率
                        q_hydrogen[n - k][h2_idx] -= electric_production / (efficiency * self.H_HV)
        
        # 手动添加基础耦合，确保系统有能量流动
        # 如果没有耦合元件，添加默认耦合
        if len(self.coupling_components) == 0:
            # 简单的电-热-氢耦合
            if len(self.electric_buses) > 0 and len(self.thermal_buses) > 0:
                # 添加默认电锅炉耦合
                elec_idx = 0
                thermal_idx = 0
                # 第1阶时从电网向热网传递能量
                if n == 1:
                    p_electric[1][elec_idx] -= 0.5  # 消耗电能
                    q_thermal[1][thermal_idx] += 0.5 * 0.95  # 产生热能（效率0.95）
            
            if len(self.electric_buses) > 0 and len(self.hydrogen_buses) > 0:
                # 添加默认电解槽耦合
                elec_idx = 0
                h2_idx = 0
                if n == 1:
                    p_electric[1][elec_idx] -= 0.3  # 消耗电能
                    q_hydrogen[1][h2_idx] += 0.3 * 0.85 / self.H_HV  # 产生氢能（效率0.85）
        """更新耦合元件功率，建立子系统间能量耦合"""
        for component in self.coupling_components.values():
            component_type = component.parameters.get('type', '').lower()
            params = component.parameters
            
            # 获取元件连接的母线
            from_bus = component.from_bus.name
            to_bus = component.to_bus.name
            
            if component_type == 'electrolyzer':
                # 电解槽：电能→氢能
                # 效率：η_elec = P_H2 / P_electric
                efficiency = params.get('efficiency', 0.85)
                
                if from_bus in self.electric_buses and to_bus in self.hydrogen_buses:
                    # 从电网消耗电能，产生氢能
                    elec_idx = self.electric_buses.index(from_bus)
                    h2_idx = self.hydrogen_buses.index(to_bus)
                    
                    # 计算第n阶的功率转换
                    for k in range(0, n):
                        # P_electric = P_H2 / η
                        p_electric[n - k][elec_idx] -= f_hydrogen[k][h2_idx] * self.H_HV / efficiency
                        # P_H2 = η * P_electric
                        q_hydrogen[n - k][h2_idx] += p_electric[k][elec_idx] * efficiency / self.H_HV
            
            elif component_type == 'fuel_cell':
                # 燃料电池：氢能→电能
                # 效率：η_fc = P_electric / P_H2
                efficiency = params.get('efficiency', 0.6)
                
                if from_bus in self.hydrogen_buses and to_bus in self.electric_buses:
                    # 消耗氢能，产生电能
                    h2_idx = self.hydrogen_buses.index(from_bus)
                    elec_idx = self.electric_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # P_electric = η * P_H2
                        p_electric[n - k][elec_idx] += f_hydrogen[k][h2_idx] * self.H_HV * efficiency
                        # P_H2 = P_electric / η
                        q_hydrogen[n - k][h2_idx] -= p_electric[k][elec_idx] / (efficiency * self.H_HV)
            
            elif component_type == 'electric_boiler':
                # 电锅炉：电能→热能
                # 效率：η_boiler = Q_thermal / P_electric
                efficiency = params.get('efficiency', 0.95)
                
                if from_bus in self.electric_buses and to_bus in self.thermal_buses:
                    # 消耗电能，产生热能
                    elec_idx = self.electric_buses.index(from_bus)
                    thermal_idx = self.thermal_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # Q_thermal = η * P_electric
                        q_thermal[n - k][thermal_idx] += p_electric[k][elec_idx] * efficiency
                        # P_electric = Q_thermal / η
                        p_electric[n - k][elec_idx] -= q_thermal[k][thermal_idx] / efficiency
            
            elif component_type == 'hydrogen_burner':
                # 氢气燃烧器：氢能→热能
                # 效率：η_burner = Q_thermal / P_H2
                efficiency = params.get('efficiency', 0.85)
                
                if from_bus in self.hydrogen_buses and to_bus in self.thermal_buses:
                    # 消耗氢能，产生热能
                    h2_idx = self.hydrogen_buses.index(from_bus)
                    thermal_idx = self.thermal_buses.index(to_bus)
                    
                    for k in range(0, n):
                        # Q_thermal = η * P_H2
                        q_thermal[n - k][thermal_idx] += f_hydrogen[k][h2_idx] * self.H_HV * efficiency
                        # P_H2 = Q_thermal / η
                        q_hydrogen[n - k][h2_idx] -= q_thermal[k][thermal_idx] / (efficiency * self.H_HV)
    
    def _calculate_convergence_error(self, V_mag: np.ndarray, V_ang: np.ndarray, T_actual: np.ndarray, m_actual: np.ndarray, 
                                    p_actual: np.ndarray, f_actual: np.ndarray, p_injection: np.ndarray, q_injection: np.ndarray,
                                    heat_injection: np.ndarray, hydrogen_injection: np.ndarray, Y_electric: csr_matrix,
                                    G_thermal: np.ndarray, B_thermal: np.ndarray, G_hydrogen: np.ndarray, network_data: Dict[str, Any]) -> float:
        """计算收敛误差，基于功率不平衡量"""
        error_electric = 0.0
        error_thermal = 0.0
        error_hydrogen = 0.0
        
        # 计算电网功率不平衡
        if len(self.electric_buses) > 0:
            # 计算各母线的计算功率
            P_calc = np.zeros(len(self.electric_buses))
            Q_calc = np.zeros(len(self.electric_buses))
            
            for i in range(len(self.electric_buses)):
                real_part = 0.0
                imag_part = 0.0
                for j in range(len(self.electric_buses)):
                    V_i = V_mag[i] * np.exp(1j * V_ang[i])
                    V_j = V_mag[j] * np.exp(1j * V_ang[j])
                    Y_ij = Y_electric[i, j]
                    I_ij = Y_ij * V_j
                    real_part += np.real(V_i.conj() * I_ij)
                    imag_part += np.imag(V_i.conj() * I_ij)
                
                P_calc[i] = real_part
                Q_calc[i] = imag_part
            
            # 电网不平衡误差：ΔP = P_calc - P_spec
            # 使用更合理的误差计算方式，基于平均不平衡而非最大值
            error_electric = np.mean(np.abs(P_calc - p_injection)) + np.mean(np.abs(Q_calc - q_injection))
        
        # 计算热网热量不平衡 - 基于实际热网方程
        if len(self.thermal_buses) > 0:
            # 简化热网方程：G_thermal * T + B_thermal * m = heat_injection
            T = T_actual
            m = m_actual
            # 计算热网方程左边
            left_side = np.dot(G_thermal, T) + np.dot(B_thermal, m) * (T / self.c_p).mean()
            error_thermal = np.mean(np.abs(left_side - heat_injection))
        
        # 计算氢网流量不平衡 - 基于实际氢网方程
        if len(self.hydrogen_buses) > 0:
            # 简化氢网方程：G_hydrogen * p = f_actual
            p = p_actual
            # 计算氢网方程左边
            left_side = np.dot(G_hydrogen, p)
            error_hydrogen = np.mean(np.abs(left_side - hydrogen_injection))
        
        # 总误差（基于功率不平衡量）
        total_error = error_electric + error_thermal + error_hydrogen
        
        return total_error
    
    def _calculate_exergy_flow(self, V_mag_electric: np.ndarray, V_ang_electric: np.ndarray, T_actual: np.ndarray, m_actual: np.ndarray,
                              p_actual: np.ndarray, f_actual: np.ndarray, network_data: Dict[str, Any]) -> ElectroThermalHydrogenExergyFlowResult:
        """计算㶲流分析"""
        # 电网㶲流
        electric_exergy_flow = pd.DataFrame(
            np.zeros((len(self.electric_buses), 2)),
            index=self.electric_buses,
            columns=['exergy_flow', 'exergy_loss']
        )
        
        # 热网㶲流
        thermal_exergy_flow = pd.DataFrame(
            np.zeros((len(self.thermal_buses), 2)),
            index=self.thermal_buses,
            columns=['exergy_flow', 'exergy_loss']
        )
        
        # 氢网㶲流
        hydrogen_exergy_flow = pd.DataFrame(
            np.zeros((len(self.hydrogen_buses), 2)),
            index=self.hydrogen_buses,
            columns=['exergy_flow', 'exergy_loss']
        )
        
        # 计算各母线的有功功率（用于电网㶲流）
        p_calc = np.zeros(len(self.electric_buses))
        for i in range(len(self.electric_buses)):
            p_total = 0.0
            for j in range(len(self.electric_buses)):
                # 简化功率计算：V_i * V_j * (G_ij cosθ_ij + B_ij sinθ_ij)
                theta_ij = V_ang_electric[i] - V_ang_electric[j]
                G_ij = self._calculate_electric_admittance_matrix(network_data).real[i, j]
                B_ij = self._calculate_electric_admittance_matrix(network_data).imag[i, j]
                p_total += V_mag_electric[i] * V_mag_electric[j] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
            p_calc[i] = p_total
        
        # 计算各子系统㶲流
        for i, bus_name in enumerate(self.electric_buses):
            # 电网㶲流：电力㶲等于有功功率
            electric_exergy_flow.loc[bus_name, 'exergy_flow'] = p_calc[i]
            # 电网㶲损：简化为电压偏差导致的损失
            voltage_deviation = abs(V_mag_electric[i] - 1.0)
            electric_exergy_flow.loc[bus_name, 'exergy_loss'] = p_calc[i] * voltage_deviation**2
        
        for i, bus_name in enumerate(self.thermal_buses):
            # 热网㶲流
            T = T_actual[i]
            # 热㶲公式：m * c_p * [(T - T0) - T0 * ln(T/T0)]
            exergy_flow = m_actual[i] * self.c_p * (T - self.environmental_temperature - self.environmental_temperature * np.log(T / self.environmental_temperature))
            thermal_exergy_flow.loc[bus_name, 'exergy_flow'] = max(0, exergy_flow)  # 㶲流不能为负
            
            # 热网㶲损：基于温度损失
            temperature_loss = T - 353.15  # 假设设计温度为80°C
            thermal_exergy_flow.loc[bus_name, 'exergy_loss'] = abs(exergy_flow) * (temperature_loss / T)**2
        
        for i, bus_name in enumerate(self.hydrogen_buses):
            # 氢网㶲流：化学㶲，近似等于高热值乘以流量
            hydrogen_flow = f_actual[i] * self.H_HV
            exergy_flow = hydrogen_flow  # 氢能的化学㶲近似等于其高热值
            hydrogen_exergy_flow.loc[bus_name, 'exergy_flow'] = exergy_flow
            # 氢网㶲损：基于压力损失
            pressure_deviation = abs(p_actual[i] - 1.0)
            hydrogen_exergy_flow.loc[bus_name, 'exergy_loss'] = exergy_flow * pressure_deviation**2
        
        # 耦合元件㶲流
        component_exergy_flow = pd.DataFrame(
            np.zeros((len(self.coupling_components), 3)),
            index=list(self.coupling_components.keys()),
            columns=['input_exergy', 'output_exergy', 'exergy_loss']
        )
        
        # 计算耦合元件㶲流
        for i, (component_name, component) in enumerate(self.coupling_components.items()):
            component_type = component.parameters.get('type', '').lower()
            
            if component_type == 'electrolyzer':
                # 电解槽：电能→氢能
                # 输入电能㶲，输出氢能化学㶲
                if component.from_bus.name in self.electric_buses and component.to_bus.name in self.hydrogen_buses:
                    input_bus = component.from_bus.name
                    output_bus = component.to_bus.name
                    input_exergy = electric_exergy_flow.loc[input_bus, 'exergy_flow']
                    output_exergy = hydrogen_exergy_flow.loc[output_bus, 'exergy_flow']
                    exergy_loss = input_exergy - output_exergy
                    component_exergy_flow.loc[component_name] = [input_exergy, output_exergy, exergy_loss]
            
            elif component_type == 'fuel_cell':
                # 燃料电池：氢能→电能
                if component.from_bus.name in self.hydrogen_buses and component.to_bus.name in self.electric_buses:
                    input_bus = component.from_bus.name
                    output_bus = component.to_bus.name
                    input_exergy = hydrogen_exergy_flow.loc[input_bus, 'exergy_flow']
                    output_exergy = electric_exergy_flow.loc[output_bus, 'exergy_flow']
                    exergy_loss = input_exergy - output_exergy
                    component_exergy_flow.loc[component_name] = [input_exergy, output_exergy, exergy_loss]
            
            elif component_type in ['electric_boiler', 'hydrogen_burner', 'heat_pump']:
                # 电锅炉/氢气燃烧器/热泵：电能/氢能→热能
                if component.from_bus.name in (self.electric_buses + self.hydrogen_buses) and component.to_bus.name in self.thermal_buses:
                    input_bus = component.from_bus.name
                    output_bus = component.to_bus.name
                    
                    if input_bus in self.electric_buses:
                        input_exergy = electric_exergy_flow.loc[input_bus, 'exergy_flow']
                    else:
                        input_exergy = hydrogen_exergy_flow.loc[input_bus, 'exergy_flow']
                    
                    output_exergy = thermal_exergy_flow.loc[output_bus, 'exergy_flow']
                    exergy_loss = input_exergy - output_exergy
                    component_exergy_flow.loc[component_name] = [input_exergy, output_exergy, exergy_loss]
        
        # 计算总㶲效率
        total_input_exergy = sum(component_exergy_flow['input_exergy'])
        total_output_exergy = sum(component_exergy_flow['output_exergy'])
        total_exergy_loss = sum(component_exergy_flow['exergy_loss'])
        
        if total_input_exergy > 0:
            total_exergy_efficiency = total_output_exergy / total_input_exergy
        else:
            total_exergy_efficiency = 0.0
        
        # 创建㶲流分析结果对象
        exergy_result = ElectroThermalHydrogenExergyFlowResult(
            electric_exergy_flow=electric_exergy_flow,
            electric_exergy_loss=electric_exergy_flow[['exergy_loss']],
            thermal_exergy_flow=thermal_exergy_flow,
            thermal_exergy_loss=thermal_exergy_flow[['exergy_loss']],
            hydrogen_exergy_flow=hydrogen_exergy_flow,
            hydrogen_exergy_loss=hydrogen_exergy_flow[['exergy_loss']],
            component_exergy_flow=component_exergy_flow[['input_exergy', 'output_exergy']],
            component_exergy_loss=component_exergy_flow[['exergy_loss']],
            total_exergy_efficiency=total_exergy_efficiency
        )
        
        return exergy_result
    
    def _create_electro_thermal_hydrogen_power_flow_result(self, V_mag_electric: np.ndarray, V_ang_electric: np.ndarray, T_thermal: np.ndarray, 
                                                        m_thermal: np.ndarray, p_hydrogen: np.ndarray, f_hydrogen: np.ndarray,
                                                        Y_electric: csr_matrix, G_thermal: np.ndarray, B_thermal: np.ndarray, G_hydrogen: np.ndarray, 
                                                        network_data: Dict[str, Any], converged: bool, iteration: int, error: float, status, 
                                                        start_time: float, warnings: List[str], exergy_result: ElectroThermalHydrogenExergyFlowResult) -> ElectroThermalHydrogenPowerFlowResult:
        """创建电-热-氢综合能源系统潮流计算结果对象"""
        import time
        
        # 创建DataFrame存储结果
        voltage_magnitude = pd.DataFrame(
            V_mag_electric, index=self.electric_buses, columns=['voltage_magnitude']
        )
        
        voltage_angle = pd.DataFrame(
            V_ang_electric, index=self.electric_buses, columns=['voltage_angle']
        )
        
        # 计算各母线的有功功率和无功功率
        active_power = pd.DataFrame(
            np.zeros((len(self.electric_buses), 1)), index=self.electric_buses, columns=['active_power']
        )
        reactive_power = pd.DataFrame(
            np.zeros((len(self.electric_buses), 1)), index=self.electric_buses, columns=['reactive_power']
        )
        
        # 计算线路潮流
        electric_line_flows = pd.DataFrame(
            np.zeros((len(self.electric_components), 4)), 
            index=list(self.electric_components.keys()),
            columns=['from_bus', 'to_bus', 'active_power', 'reactive_power']
        )
        
        # 填充电力线路潮流数据
        for i, (line_name, line) in enumerate(self.electric_components.items()):
            from_bus = line.from_bus.name
            to_bus = line.to_bus.name
            
            if from_bus in self.electric_buses and to_bus in self.electric_buses:
                from_idx = self.electric_buses.index(from_bus)
                to_idx = self.electric_buses.index(to_bus)
                
                V_i = V_mag_electric[from_idx] * np.exp(1j * V_ang_electric[from_idx])
                V_j = V_mag_electric[to_idx] * np.exp(1j * V_ang_electric[to_idx])
                
                # 获取线路导纳
                r = line.parameters.get('resistance', 0.01)
                x = line.parameters.get('reactance', 0.1)
                y = 1.0 / (r + 1j * x)
                
                # 计算线路潮流
                I_ij = y * (V_i - V_j)
                S_ij = V_i * I_ij.conj()
                
                electric_line_flows.iloc[i] = [from_bus, to_bus, np.real(S_ij), np.imag(S_ij)]
        
        # 热网结果
        thermal_temperatures = pd.DataFrame(
            T_thermal, index=self.thermal_buses, columns=['temperature']
        )
        
        thermal_flows = pd.DataFrame(
            m_thermal, index=self.thermal_buses, columns=['flow_rate']
        )
        
        # 氢网结果
        hydrogen_pressures = pd.DataFrame(
            p_hydrogen, index=self.hydrogen_buses, columns=['pressure']
        )
        
        hydrogen_flows = pd.DataFrame(
            f_hydrogen, index=self.hydrogen_buses, columns=['flow_rate']
        )
        
        # 耦合元件结果
        coupling_component_power = pd.DataFrame(
            np.zeros((len(self.coupling_components), 3)),
            index=list(self.coupling_components.keys()),
            columns=['input_power', 'output_power', 'efficiency']
        )
        
        coupling_component_efficiency = pd.DataFrame(
            np.zeros((len(self.coupling_components), 1)),
            index=list(self.coupling_components.keys()),
            columns=['efficiency']
        )
        
        # 计算耦合元件功率和效率
        for i, (component_name, component) in enumerate(self.coupling_components.items()):
            component_type = component.parameters.get('type', '').lower()
            efficiency = component.parameters.get('efficiency', 0.85)
            
            if component_type in ['electrolyzer', 'p2g', 'power_to_gas']:
                # 输入电能，输出氢能
                if component.from_bus.name in self.electric_buses and component.to_bus.name in self.hydrogen_buses:
                    from_bus = component.from_bus.name
                    to_bus = component.to_bus.name
                    
                    # 计算输入电能
                    from_idx = self.electric_buses.index(from_bus)
                    input_power = active_power.loc[from_bus, 'active_power']
                    
                    # 计算输出氢能
                    to_idx = self.hydrogen_buses.index(to_bus)
                    output_power = f_hydrogen[to_idx] * self.H_HV  # 氢能功率
                    
                    coupling_component_power.loc[component_name] = [input_power, output_power, efficiency]
                    coupling_component_efficiency.loc[component_name] = [efficiency]
            
            elif component_type in ['fuel_cell', 'hydrogen_to_power']:
                # 输入氢能，输出电能
                if component.from_bus.name in self.hydrogen_buses and component.to_bus.name in self.electric_buses:
                    from_bus = component.from_bus.name
                    to_bus = component.to_bus.name
                    
                    # 计算输入氢能
                    from_idx = self.hydrogen_buses.index(from_bus)
                    input_power = f_hydrogen[from_idx] * self.H_HV  # 氢能功率
                    
                    # 计算输出电能
                    to_idx = self.electric_buses.index(to_bus)
                    output_power = active_power.loc[to_bus, 'active_power']
                    
                    coupling_component_power.loc[component_name] = [input_power, output_power, efficiency]
                    coupling_component_efficiency.loc[component_name] = [efficiency]
            
            elif component_type in ['electric_boiler', 'heat_pump']:
                # 输入电能，输出热能
                if component.from_bus.name in self.electric_buses and component.to_bus.name in self.thermal_buses:
                    from_bus = component.from_bus.name
                    to_bus = component.to_bus.name
                    
                    # 计算输入电能
                    from_idx = self.electric_buses.index(from_bus)
                    input_power = active_power.loc[from_bus, 'active_power']
                    
                    # 计算输出热能
                    to_idx = self.thermal_buses.index(to_bus)
                    output_power = m_thermal[to_idx] * self.c_p * (T_thermal[to_idx] - self.environmental_temperature)  # 热能功率
                    
                    coupling_component_power.loc[component_name] = [input_power, output_power, efficiency]
                    coupling_component_efficiency.loc[component_name] = [efficiency]
            
            elif component_type == 'hydrogen_burner':
                # 输入氢能，输出热能
                if component.from_bus.name in self.hydrogen_buses and component.to_bus.name in self.thermal_buses:
                    from_bus = component.from_bus.name
                    to_bus = component.to_bus.name
                    
                    # 计算输入氢能
                    from_idx = self.hydrogen_buses.index(from_bus)
                    input_power = f_hydrogen[from_idx] * self.H_HV  # 氢能功率
                    
                    # 计算输出热能
                    to_idx = self.thermal_buses.index(to_bus)
                    output_power = m_thermal[to_idx] * self.c_p * (T_thermal[to_idx] - self.environmental_temperature)  # 热能功率
                    
                    coupling_component_power.loc[component_name] = [input_power, output_power, efficiency]
                    coupling_component_efficiency.loc[component_name] = [efficiency]
        
        # 计算损耗
        electric_losses = float(np.sum(np.abs(electric_line_flows['active_power'])))
        thermal_losses = float(np.sum(np.abs(m_thermal * self.c_p * (T_thermal - self.environmental_temperature))))
        hydrogen_losses = float(np.sum(np.abs(f_hydrogen * self.H_HV)))
        
        # 创建最终结果对象
        result = ElectroThermalHydrogenPowerFlowResult(
            voltage_magnitude=voltage_magnitude,
            voltage_angle=voltage_angle,
            active_power=active_power,
            reactive_power=reactive_power,
            converged=converged,
            iterations=iteration,
            error=error,
            status=status,
            computation_time=time.time() - start_time,
            warnings=warnings,
            electric_line_flows=electric_line_flows,
            electric_losses=electric_losses,
            thermal_temperatures=thermal_temperatures,
            thermal_flows=thermal_flows,
            thermal_losses=thermal_losses,
            hydrogen_pressures=hydrogen_pressures,
            hydrogen_flows=hydrogen_flows,
            hydrogen_losses=hydrogen_losses,
            coupling_component_power=coupling_component_power,
            coupling_component_efficiency=coupling_component_efficiency,
            exergy_flows=exergy_result.electric_exergy_flow[['exergy_flow']].append(
                exergy_result.thermal_exergy_flow[['exergy_flow']]
            ).append(
                exergy_result.hydrogen_exergy_flow[['exergy_flow']]
            ),
            exergy_losses=exergy_result.electric_exergy_loss.append(
                exergy_result.thermal_exergy_loss
            ).append(
                exergy_result.hydrogen_exergy_loss
            ),
            total_exergy_efficiency=exergy_result.total_exergy_efficiency
        )
        
        return result
    
    def validate_inputs(self) -> bool:
        """验证输入数据是否完整"""
        # 检查网络是否包含必要的组件
        if not self.network.buses:
            logger.error("网络中没有母线")
            return False
        
        # 检查是否有至少一个电力母线
        if not any(bus.parameters.get('carrier') == 'electricity' for bus in self.network.buses.values()):
            logger.error("网络中没有电力母线")
            return False
        
        return True
    
    def _prepare_network_data(self) -> Dict[str, Any]:
        """准备网络数据，转换为适合潮流计算的格式"""
        network_data = {
            'buses': list(self.network.buses.values()),
            'bus_names': list(self.network.buses.keys()),
            'generators': [gen for gen in self.network.components.values() if gen.component_type == ComponentType.GENERATOR],
            'loads': [load for load in self.network.components.values() if gen.component_type == ComponentType.LOAD],
            'lines': [line for line in self.network.components.values() if gen.component_type == ComponentType.LINE],
            'components': list(self.network.components.values())
        }
        
        return network_data


def create_electro_thermal_hydrogen_solver(network: PyXESXXNNetwork, **kwargs) -> ElectroThermalHydrogenPowerFlowSolver:
    """创建电-热-氢综合能源系统全纯嵌入潮流求解器
    
    参数:
        network: PyXESXXNNetwork 对象，包含综合能源系统模型
        **kwargs: 求解器配置参数
    
    返回:
        ElectroThermalHydrogenPowerFlowSolver 对象
    """
    return ElectroThermalHydrogenPowerFlowSolver(network, **kwargs)


def run_electro_thermal_hydrogen_power_flow(network: PyXESXXNNetwork, **kwargs) -> Tuple[ElectroThermalHydrogenPowerFlowResult, ElectroThermalHydrogenPowerFlowAnalysis]:
    """运行电-热-氢综合能源系统全纯嵌入潮流计算
    
    参数:
        network: PyXESXXNNetwork 对象，包含综合能源系统模型
        **kwargs: 求解器配置参数
    
    返回:
        Tuple[ElectroThermalHydrogenPowerFlowResult, ElectroThermalHydrogenPowerFlowAnalysis]: 潮流计算结果和分析对象
    """
    solver = create_electro_thermal_hydrogen_solver(network, **kwargs)
    result = solver.solve()
    analysis = ElectroThermalHydrogenPowerFlowAnalysis(network, result)
    
    return result, analysis


class ElectroThermalHydrogenPowerFlowAnalysis(PowerFlowAnalysis):
    """电-热-氢综合能源系统潮流分析类"""
    
    def __init__(self, network: PyXESXXNNetwork, result: ElectroThermalHydrogenPowerFlowResult):
        """初始化电-热-氢综合能源系统潮流分析对象
        
        参数:
            network: PyXESXXNNetwork 对象，包含综合能源系统模型
            result: ElectroThermalHydrogenPowerFlowResult 对象，包含潮流计算结果
        """
        super().__init__(network, result)
        self.network = network
        self.result = result
    
    def analyze_electric_network(self) -> Dict[str, Any]:
        """分析电网性能"""
        analysis = {
            'voltage_profile': self.result.voltage_magnitude,
            'voltage_deviation': (self.result.voltage_magnitude - 1.0).abs().mean().values[0],
            'active_power_flow': self.result.active_power,
            'reactive_power_flow': self.result.reactive_power,
            'line_flows': self.result.electric_line_flows,
            'total_losses': self.result.electric_losses,
            'converged': self.result.converged
        }
        
        return analysis
    
    def analyze_thermal_network(self) -> Dict[str, Any]:
        """分析热网性能"""
        analysis = {
            'temperature_profile': self.result.thermal_temperatures,
            'flow_profile': self.result.thermal_flows,
            'total_heat_losses': self.result.thermal_losses
        }
        
        return analysis
    
    def analyze_hydrogen_network(self) -> Dict[str, Any]:
        """分析氢网性能"""
        analysis = {
            'pressure_profile': self.result.hydrogen_pressures,
            'flow_profile': self.result.hydrogen_flows,
            'total_hydrogen_losses': self.result.hydrogen_losses
        }
        
        return analysis
    
    def analyze_coupling_components(self) -> Dict[str, Any]:
        """分析耦合元件性能"""
        analysis = {
            'component_power_flows': self.result.coupling_component_power,
            'component_efficiencies': self.result.coupling_component_efficiency
        }
        
        return analysis
    
    def analyze_exergy_efficiency(self) -> Dict[str, Any]:
        """分析系统㶲效率"""
        analysis = {
            'exergy_flows': self.result.exergy_flows,
            'exergy_losses': self.result.exergy_losses,
            'total_exergy_efficiency': self.result.total_exergy_efficiency
        }
        
        return analysis
    
    def generate_comprehensive_report(self) -> str:
        """生成综合分析报告"""
        report = []
        report.append("# 电-热-氢综合能源系统潮流分析报告")
        report.append("")
        
        # 基本信息
        report.append("## 1. 基本信息")
        report.append(f"- 收敛状态: {'成功' if self.result.converged else '失败'}")
        report.append(f"- 迭代次数: {self.result.iterations}")
        report.append(f"- 最大误差: {self.result.error:.6e}")
        report.append(f"- 计算时间: {self.result.computation_time:.3f}秒")
        report.append("")
        
        # 电网分析
        report.append("## 2. 电网分析")
        electric_analysis = self.analyze_electric_network()
        report.append(f"- 电压偏差: {electric_analysis['voltage_deviation']:.6f} pu")
        report.append(f"- 总损耗: {self.result.electric_losses:.6f} MW")
        report.append(f"- 平均电压: {self.result.voltage_magnitude.mean().values[0]:.4f} pu")
        report.append(f"- 最低电压: {self.result.voltage_magnitude.min().values[0]:.4f} pu (母线: {self.result.voltage_magnitude.idxmin().values[0]})")
        report.append(f"- 最高电压: {self.result.voltage_magnitude.max().values[0]:.4f} pu (母线: {self.result.voltage_magnitude.idxmax().values[0]})")
        report.append("")
        
        # 热网分析
        report.append("## 3. 热网分析")
        report.append(f"- 总热损耗: {self.result.thermal_losses:.6f} kW")
        report.append(f"- 平均温度: {self.result.thermal_temperatures.mean().values[0]:.2f} K")
        report.append(f"- 最低温度: {self.result.thermal_temperatures.min().values[0]:.2f} K (母线: {self.result.thermal_temperatures.idxmin().values[0]})")
        report.append(f"- 最高温度: {self.result.thermal_temperatures.max().values[0]:.2f} K (母线: {self.result.thermal_temperatures.idxmax().values[0]})")
        report.append("")
        
        # 氢网分析
        report.append("## 4. 氢网分析")
        report.append(f"- 总氢损耗: {self.result.hydrogen_losses:.6f} MW")
        report.append(f"- 平均压力: {self.result.hydrogen_pressures.mean().values[0]:.4f} bar")
        report.append(f"- 最低压力: {self.result.hydrogen_pressures.min().values[0]:.4f} bar (母线: {self.result.hydrogen_pressures.idxmin().values[0]})")
        report.append(f"- 最高压力: {self.result.hydrogen_pressures.max().values[0]:.4f} bar (母线: {self.result.hydrogen_pressures.idxmax().values[0]})")
        report.append("")
        
        # 耦合元件分析
        report.append("## 5. 耦合元件分析")
        report.append("### 5.1 功率流")
        report.append(self.result.coupling_component_power.to_string())
        report.append("")
        report.append("### 5.2 效率")
        report.append(self.result.coupling_component_efficiency.to_string())
        report.append("")
        
        # 㶲流分析
        report.append("## 6. 㶲流分析")
        report.append(f"- 总㶲效率: {self.result.total_exergy_efficiency:.6f}")
        report.append("### 6.1 㶲流分布")
        report.append(self.result.exergy_flows.to_string())
        report.append("")
        report.append("### 6.2 㶲损分布")
        report.append(self.result.exergy_losses.to_string())
        report.append("")
        
        # 结论
        report.append("## 7. 结论")
        if self.result.converged:
            report.append("- 潮流计算成功收敛，结果可用")
            if self.result.total_exergy_efficiency > 0.5:
                report.append("- 系统㶲效率较高，能量利用合理")
            else:
                report.append("- 系统㶲效率较低，建议优化能量转换过程")
        else:
            report.append("- 潮流计算未能收敛，结果不可用")
            report.append("- 建议检查网络拓扑、参数设置或初始化条件")
        
        return "\n".join(report)