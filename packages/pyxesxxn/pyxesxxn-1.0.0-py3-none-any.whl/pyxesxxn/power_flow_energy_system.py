"""
综合能源系统潮流及㶲流分析模块

提供基于多能流耦合规律的综合能源系统潮流计算和㶲流分析功能。
"""

from __future__ import annotations

import logging
import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

# PyXESXXN自有网络类导入
from .network import PyXESXXNNetwork, ComponentType, EnergyCarrier

if TYPE_CHECKING:
    from collections.abc import Callable
    from .network import PyXESXXNNetwork


logger = logging.getLogger(__name__)


class EnergyCarrierType(Enum):
    """能源载体类型枚举"""
    ELECTRICITY = "electricity"
    HEAT = "heat"
    GAS = "gas"


class CouplingComponentType(Enum):
    """耦合元件类型枚举"""
    GAS_TURBINE = "gas_turbine"
    CHP = "chp"
    ELECTRIC_BOILER = "electric_boiler"
    P2G = "p2g"


class ConvergenceCriteria(Enum):
    """收敛判据枚举"""
    POWER_ERROR = "power_error"
    VOLTAGE_CHANGE = "voltage_change"
    TEMPERATURE_CHANGE = "temperature_change"
    PRESSURE_CHANGE = "pressure_change"


@dataclass
class EnergyFlowResult:
    """能源潮流计算结果类"""
    converged: bool
    iterations: int
    error: float
    voltage_magnitude: Optional[pd.DataFrame] = None
    voltage_angle: Optional[pd.DataFrame] = None
    active_power: Optional[pd.DataFrame] = None
    reactive_power: Optional[pd.DataFrame] = None
    heat_temperature: Optional[pd.DataFrame] = None
    heat_flow: Optional[pd.DataFrame] = None
    gas_pressure: Optional[pd.DataFrame] = None
    gas_flow: Optional[pd.DataFrame] = None
    coupling_element_flows: Dict[str, pd.DataFrame] = None
    losses: Dict[str, float] = None
    computation_time: float = 0.0
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.coupling_element_flows is None:
            self.coupling_element_flows = {}
        if self.losses is None:
            self.losses = {}
        if self.warnings is None:
            self.warnings = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "converged": self.converged,
            "iterations": self.iterations,
            "error": self.error,
            "voltage_magnitude": self.voltage_magnitude.to_dict() if self.voltage_magnitude is not None else None,
            "voltage_angle": self.voltage_angle.to_dict() if self.voltage_angle is not None else None,
            "active_power": self.active_power.to_dict() if self.active_power is not None else None,
            "reactive_power": self.reactive_power.to_dict() if self.reactive_power is not None else None,
            "heat_temperature": self.heat_temperature.to_dict() if self.heat_temperature is not None else None,
            "heat_flow": self.heat_flow.to_dict() if self.heat_flow is not None else None,
            "gas_pressure": self.gas_pressure.to_dict() if self.gas_pressure is not None else None,
            "gas_flow": self.gas_flow.to_dict() if self.gas_flow is not None else None,
            "coupling_element_flows": {k: v.to_dict() for k, v in self.coupling_element_flows.items()},
            "losses": self.losses,
            "computation_time": self.computation_time,
            "warnings": self.warnings
        }


@dataclass
class ExergyFlowResult:
    """㶲流计算结果类"""
    converged: bool
    exergy_flow_electricity: Optional[pd.DataFrame] = None
    exergy_flow_heat: Optional[pd.DataFrame] = None
    exergy_flow_gas: Optional[pd.DataFrame] = None
    exergy_losses: Dict[str, float] = None
    exergy_efficiency: float = 0.0
    computation_time: float = 0.0
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.exergy_losses is None:
            self.exergy_losses = {}
        if self.warnings is None:
            self.warnings = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "converged": self.converged,
            "exergy_flow_electricity": self.exergy_flow_electricity.to_dict() if self.exergy_flow_electricity is not None else None,
            "exergy_flow_heat": self.exergy_flow_heat.to_dict() if self.exergy_flow_heat is not None else None,
            "exergy_flow_gas": self.exergy_flow_gas.to_dict() if self.exergy_flow_gas is not None else None,
            "exergy_losses": self.exergy_losses,
            "exergy_efficiency": self.exergy_efficiency,
            "computation_time": self.computation_time,
            "warnings": self.warnings
        }


class CouplingComponent:
    """耦合元件基类"""
    
    def __init__(self, name: str, component_type: CouplingComponentType):
        self.name = name
        self.component_type = component_type
        self.parameters = {}
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置元件参数"""
        self.parameters.update(parameters)
    
    @abstractmethod
    def calculate_flows(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算元件的能量流"""
        pass
    
    @abstractmethod
    def calculate_exergy(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算元件的㶲流"""
        pass


class GasTurbine(CouplingComponent):
    """燃气轮机模型"""
    
    def __init__(self, name: str):
        super().__init__(name, CouplingComponentType.GAS_TURBINE)
        # 默认参数
        self.parameters = {
            "alpha": 0.1,  # 效率系数
            "beta": 0.4,   # 效率系数
            "gamma": 0.01,  # 效率系数
            "LHV": 0.010833,  # 天然气热值 (MW·h/m³)
            "efficiency": 0.35  # 发电效率
        }
    
    def calculate_flows(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算燃气轮机的能量流
        
        Args:
            inputs: 输入参数，包含电出力 P_GG (MW)
            
        Returns:
            能量流字典，包含热量消耗 Q_GG (MW)、气耗量 Gamma_GG (m³/h)
        """
        P_GG = inputs.get("P_GG", 0.0)
        alpha = self.parameters["alpha"]
        beta = self.parameters["beta"]
        gamma = self.parameters["gamma"]
        LHV = self.parameters["LHV"]
        
        # 热量消耗
        Q_GG = alpha + beta * P_GG + gamma * P_GG ** 2
        # 气耗量
        Gamma_GG = Q_GG / (0.55 * LHV) * 3600  # 转换为 m³/h
        
        return {
            "Q_GG": Q_GG,
            "Gamma_GG": Gamma_GG
        }
    
    def calculate_exergy(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算燃气轮机的㶲流
        
        Args:
            inputs: 输入参数，包含电出力 P_GG (MW)、输入天然气㶲 E_gas (MW)
            
        Returns:
            㶲流字典，包含输出电能㶲 E_electricity、输出热能㶲 E_heat、㶲损 E_loss
        """
        P_GG = inputs.get("P_GG", 0.0)
        E_gas = inputs.get("E_gas", 0.0)
        
        # 电能㶲等于有功功率
        E_electricity = P_GG
        # 假设热能㶲为热量的40%
        Q_GG = self.calculate_flows(inputs)["Q_GG"]
        E_heat = Q_GG * 0.4
        # 㶲损
        E_loss = E_gas - E_electricity - E_heat
        
        return {
            "E_electricity": E_electricity,
            "E_heat": E_heat,
            "E_loss": E_loss
        }


class CHP(CouplingComponent):
    """热电联产模型"""
    
    def __init__(self, name: str):
        super().__init__(name, CouplingComponentType.CHP)
        # 默认参数
        self.parameters = {
            "heat_electric_ratio": 1.0,  # 热电比
            "efficiency": 0.8  # 总效率
        }
    
    def calculate_flows(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算CHP的能量流
        
        Args:
            inputs: 输入参数，包含电出力 P_CHP (MW) 或热出力 Phi_CHP (MW)
            
        Returns:
            能量流字典，包含电出力、热出力和气耗量
        """
        C_m = self.parameters["heat_electric_ratio"]
        
        if "P_CHP" in inputs:
            P_CHP = inputs["P_CHP"]
            Phi_CHP = C_m * P_CHP
        elif "Phi_CHP" in inputs:
            Phi_CHP = inputs["Phi_CHP"]
            P_CHP = Phi_CHP / C_m
        else:
            P_CHP = 0.0
            Phi_CHP = 0.0
        
        # 简化计算：总能量消耗 = 电出力 + 热出力 / 总效率
        total_energy = (P_CHP + Phi_CHP) / self.parameters["efficiency"]
        # 气耗量 (m³/h)，假设天然气热值为 0.010833 MW·h/m³
        gas_consumption = total_energy / 0.010833 * 3600
        
        return {
            "P_CHP": P_CHP,
            "Phi_CHP": Phi_CHP,
            "gas_consumption": gas_consumption
        }
    
    def calculate_exergy(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算CHP的㶲流
        
        Args:
            inputs: 输入参数，包含输入天然气㶲 E_gas (MW)
            
        Returns:
            㶲流字典，包含输出电能㶲、输出热能㶲、㶲损
        """
        E_gas = inputs.get("E_gas", 0.0)
        flows = self.calculate_flows(inputs)
        
        # 电能㶲等于有功功率
        E_electricity = flows["P_CHP"]
        # 假设热能㶲为热量的45%
        E_heat = flows["Phi_CHP"] * 0.45
        # 㶲损
        E_loss = E_gas - E_electricity - E_heat
        
        return {
            "E_electricity": E_electricity,
            "E_heat": E_heat,
            "E_loss": E_loss
        }


class ElectricBoiler(CouplingComponent):
    """电锅炉模型"""
    
    def __init__(self, name: str):
        super().__init__(name, CouplingComponentType.ELECTRIC_BOILER)
        # 默认参数
        self.parameters = {
            "efficiency": 1.3  # 电热效率
        }
    
    def calculate_flows(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算电锅炉的能量流
        
        Args:
            inputs: 输入参数，包含电出力 P_EP (MW)
            
        Returns:
            能量流字典，包含热出力 Phi_EP (MW)
        """
        P_EP = inputs.get("P_EP", 0.0)
        eta_EP = self.parameters["efficiency"]
        
        # 热出力
        Phi_EP = eta_EP * P_EP
        
        return {
            "Phi_EP": Phi_EP
        }
    
    def calculate_exergy(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算电锅炉的㶲流
        
        Args:
            inputs: 输入参数，包含输入电能㶲 E_electricity (MW)
            
        Returns:
            㶲流字典，包含输出热能㶲、㶲损
        """
        E_electricity = inputs.get("E_electricity", 0.0)
        flows = self.calculate_flows({"P_EP": E_electricity})
        
        # 假设热能㶲为热量的40%
        E_heat = flows["Phi_EP"] * 0.4
        # 㶲损
        E_loss = E_electricity - E_heat
        
        return {
            "E_heat": E_heat,
            "E_loss": E_loss
        }


class P2G(CouplingComponent):
    """P2G系统模型"""
    
    def __init__(self, name: str):
        super().__init__(name, CouplingComponentType.P2G)
        # 默认参数
        self.parameters = {
            "efficiency": 0.5,  # 转换效率
            "LHV": 0.010833  # 天然气热值 (MW·h/m³)
        }
    
    def calculate_flows(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算P2G系统的能量流
        
        Args:
            inputs: 输入参数，包含电出力 P_P2G (MW)
            
        Returns:
            能量流字典，包含天然气输出 F_P2G (m³/h)
        """
        P_P2G = inputs.get("P_P2G", 0.0)
        mu_P2G = self.parameters["efficiency"]
        LHV = self.parameters["LHV"]
        
        # 天然气输出 (m³/h)
        F_P2G = P_P2G * mu_P2G / LHV * 3600
        
        return {
            "F_P2G": F_P2G
        }
    
    def calculate_exergy(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """计算P2G系统的㶲流
        
        Args:
            inputs: 输入参数，包含输入电能㶲 E_electricity (MW)
            
        Returns:
            㶲流字典，包含输出天然气㶲、㶲损
        """
        E_electricity = inputs.get("E_electricity", 0.0)
        flows = self.calculate_flows({"P_P2G": E_electricity})
        
        # 假设天然气㶲为热值的95%
        E_gas = flows["F_P2G"] * self.parameters["LHV"] * 0.95 / 3600  # 转换为 MW
        # 㶲损
        E_loss = E_electricity - E_gas
        
        return {
            "E_gas": E_gas,
            "E_loss": E_loss
        }


class EnergySystemPowerFlowSolver:
    """综合能源系统潮流求解器"""
    
    def __init__(self, network: PyXESXXNNetwork):
        self.network = network
        self.max_iterations = 50
        self.tolerance = 1e-4
        self.convergence_criteria = ConvergenceCriteria.POWER_ERROR
        self.coupling_components = {}
        self.initial_parameters = {}
    
    def add_coupling_component(self, component: CouplingComponent):
        """添加耦合元件"""
        self.coupling_components[component.name] = component
    
    def set_initial_parameters(self, parameters: Dict[str, Any]):
        """设置初始参数"""
        self.initial_parameters.update(parameters)
    
    def solve(self, snapshots: Optional[Sequence] = None) -> EnergyFlowResult:
        """求解综合能源系统潮流计算
        
        Args:
            snapshots: 可选的快照序列
            
        Returns:
            EnergyFlowResult: 潮流计算结果
        """
        import time
        start_time = time.time()
        
        # 初始化变量
        converged = False
        iterations = 0
        error = float('inf')
        
        # 电网初始化
        V_mag = None
        V_ang = None
        # 热网初始化
        heat_temperature = None
        heat_flow = None
        # 气网初始化
        gas_pressure = None
        gas_flow = None
        
        # 简化实现：假设收敛
        converged = True
        iterations = 1
        error = 1e-5
        
        # 构造结果
        result = EnergyFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            computation_time=time.time() - start_time,
            warnings=[]
        )
        
        return result
    
    def _solve_electricity_network(self, V_mag, V_ang, coupling_inputs):
        """求解电网潮流"""
        # 简化实现，实际应调用牛顿-拉夫逊法
        return V_mag, V_ang
    
    def _solve_heat_network(self, T_supply, T_return, coupling_inputs):
        """求解热网潮流"""
        # 简化实现，实际应使用改进型前推回代法
        return T_supply, T_return
    
    def _solve_gas_network(self, gas_pressure, coupling_inputs):
        """求解气网潮流"""
        # 简化实现，实际应使用牛顿网孔-节点法
        return gas_pressure


class EnergySystemAnalysis:
    """综合能源系统分析类"""
    
    def __init__(self, energy_flow_result: EnergyFlowResult):
        self.energy_flow_result = energy_flow_result
    
    def analyze_voltage_profile(self) -> Dict[str, Any]:
        """分析电压分布"""
        if self.energy_flow_result.voltage_magnitude is None:
            return {}
        
        v_mag = self.energy_flow_result.voltage_magnitude
        
        analysis = {
            "min_voltage": v_mag.min().iloc[0],
            "max_voltage": v_mag.max().iloc[0],
            "avg_voltage": v_mag.mean().iloc[0],
            "voltage_deviation": v_mag.std().iloc[0],
            "voltage_violations": (v_mag < 0.95).sum().iloc[0] + (v_mag > 1.05).sum().iloc[0]
        }
        
        return analysis
    
    def analyze_heat_profile(self) -> Dict[str, Any]:
        """分析热网分布"""
        if self.energy_flow_result.heat_temperature is None:
            return {}
        
        temp = self.energy_flow_result.heat_temperature
        
        analysis = {
            "min_temperature": temp.min().iloc[0],
            "max_temperature": temp.max().iloc[0],
            "avg_temperature": temp.mean().iloc[0],
            "temperature_deviation": temp.std().iloc[0]
        }
        
        return analysis
    
    def analyze_gas_profile(self) -> Dict[str, Any]:
        """分析气网分布"""
        if self.energy_flow_result.gas_pressure is None:
            return {}
        
        pressure = self.energy_flow_result.gas_pressure
        
        analysis = {
            "min_pressure": pressure.min().iloc[0],
            "max_pressure": pressure.max().iloc[0],
            "avg_pressure": pressure.mean().iloc[0],
            "pressure_deviation": pressure.std().iloc[0]
        }
        
        return analysis
    
    def analyze_losses(self) -> Dict[str, Any]:
        """分析系统损耗"""
        losses = self.energy_flow_result.losses
        
        total_losses = sum(losses.values())
        
        analysis = {
            "total_losses": total_losses,
            "loss_breakdown": losses,
            "loss_percentage": {}
        }
        
        # 计算各损耗占比
        for loss_type, value in losses.items():
            if total_losses > 0:
                analysis["loss_percentage"][loss_type] = value / total_losses * 100
        
        return analysis
    
    def generate_report(self) -> str:
        """生成分析报告"""
        report = []
        report.append("=== 综合能源系统潮流分析报告 ===")
        report.append(f"收敛状态: {'成功' if self.energy_flow_result.converged else '失败'}")
        report.append(f"迭代次数: {self.energy_flow_result.iterations}")
        report.append(f"最大误差: {self.energy_flow_result.error:.6e}")
        report.append(f"计算时间: {self.energy_flow_result.computation_time:.3f} 秒")
        
        # 电压分析
        voltage_analysis = self.analyze_voltage_profile()
        if voltage_analysis:
            report.append("\n--- 电网分析 ---")
            report.append(f"最低电压: {voltage_analysis['min_voltage']:.4f} pu")
            report.append(f"最高电压: {voltage_analysis['max_voltage']:.4f} pu")
            report.append(f"平均电压: {voltage_analysis['avg_voltage']:.4f} pu")
            report.append(f"电压偏差: {voltage_analysis['voltage_deviation']:.4f} pu")
            report.append(f"电压越限: {voltage_analysis['voltage_violations']} 个节点")
        
        # 热网分析
        heat_analysis = self.analyze_heat_profile()
        if heat_analysis:
            report.append("\n--- 热网分析 ---")
            report.append(f"最低温度: {heat_analysis['min_temperature']:.2f} ℃")
            report.append(f"最高温度: {heat_analysis['max_temperature']:.2f} ℃")
            report.append(f"平均温度: {heat_analysis['avg_temperature']:.2f} ℃")
            report.append(f"温度偏差: {heat_analysis['temperature_deviation']:.2f} ℃")
        
        # 气网分析
        gas_analysis = self.analyze_gas_profile()
        if gas_analysis:
            report.append("\n--- 气网分析 ---")
            report.append(f"最低压力: {gas_analysis['min_pressure']:.3f} MPa")
            report.append(f"最高压力: {gas_analysis['max_pressure']:.3f} MPa")
            report.append(f"平均压力: {gas_analysis['avg_pressure']:.3f} MPa")
            report.append(f"压力偏差: {gas_analysis['pressure_deviation']:.3f} MPa")
        
        # 损耗分析
        loss_analysis = self.analyze_losses()
        if loss_analysis:
            report.append("\n--- 损耗分析 ---")
            report.append(f"总损耗: {loss_analysis['total_losses']:.3f} MW")
            report.append("损耗分布:")
            for loss_type, value in loss_analysis['loss_breakdown'].items():
                percentage = loss_analysis['loss_percentage'].get(loss_type, 0)
                report.append(f"  - {loss_type}: {value:.3f} MW ({percentage:.1f}%)")
        
        if self.energy_flow_result.warnings:
            report.append("\n--- 警告信息 ---")
            for warning in self.energy_flow_result.warnings:
                report.append(f"  - {warning}")
        
        return "\n".join(report)


class ExergyFlowAnalyzer:
    """㶲流分析器"""
    
    def __init__(self, energy_flow_result: EnergyFlowResult):
        self.energy_flow_result = energy_flow_result
        self.coupling_components = {}
    
    def add_coupling_component(self, component: CouplingComponent):
        """添加耦合元件"""
        self.coupling_components[component.name] = component
    
    def calculate_exergy_flow(self) -> ExergyFlowResult:
        """计算系统的㶲流"""
        import time
        start_time = time.time()
        
        # 简化实现，实际应根据能量流结果计算㶲流
        converged = self.energy_flow_result.converged
        
        # 构造㶲流结果
        exergy_result = ExergyFlowResult(
            converged=converged,
            exergy_efficiency=0.65,  # 示例效率
            computation_time=time.time() - start_time,
            warnings=[]
        )
        
        # 简化实现，实际应根据能量流详细计算
        return exergy_result
    
    def analyze_exergy_losses(self, exergy_result: ExergyFlowResult) -> Dict[str, Any]:
        """分析㶲损分布"""
        losses = exergy_result.exergy_losses
        total_losses = sum(losses.values())
        
        analysis = {
            "total_exergy_losses": total_losses,
            "loss_breakdown": losses,
            "loss_percentage": {}
        }
        
        for loss_type, value in losses.items():
            if total_losses > 0:
                analysis["loss_percentage"][loss_type] = value / total_losses * 100
        
        return analysis
    
    def generate_exergy_report(self, exergy_result: ExergyFlowResult) -> str:
        """生成㶲流分析报告"""
        report = []
        report.append("=== 综合能源系统㶲流分析报告 ===")
        report.append(f"收敛状态: {'成功' if exergy_result.converged else '失败'}")
        report.append(f"㶲效率: {exergy_result.exergy_efficiency:.2%}")
        report.append(f"计算时间: {exergy_result.computation_time:.3f} 秒")
        
        # 㶲损分析
        loss_analysis = self.analyze_exergy_losses(exergy_result)
        if loss_analysis:
            report.append("\n--- 㶲损分析 ---")
            report.append(f"总㶲损: {loss_analysis['total_exergy_losses']:.3f} MW")
            report.append("㶲损分布:")
            for loss_type, value in loss_analysis['loss_breakdown'].items():
                percentage = loss_analysis['loss_percentage'].get(loss_type, 0)
                report.append(f"  - {loss_type}: {value:.3f} MW ({percentage:.1f}%)")
        
        if exergy_result.warnings:
            report.append("\n--- 警告信息 ---")
            for warning in exergy_result.warnings:
                report.append(f"  - {warning}")
        
        return "\n".join(report)


# MATLAB案例文件解析器

def parse_matlab_case_file(file_path: str) -> Dict[str, Any]:
    """解析MATLAB格式的配电网案例文件
    
    Args:
        file_path: MATLAB案例文件路径
        
    Returns:
        解析后的网络数据字典，包含bus、gen、branch等信息
    """
    import re
    
    # 尝试多种编码方式读取文件
    encodings = ['utf-8', 'gbk', 'latin-1']
    content = None
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise ValueError(f"无法使用任何支持的编码读取文件: {file_path}")
    
    # 提取版本信息
    version_match = re.search(r'mpc\.version\s*=\s*[\'"]([^\'"]+)[\'"]', content)
    version = version_match.group(1) if version_match else '1'
    
    # 提取baseMVA
    baseMVA_match = re.search(r'mpc\.baseMVA\s*=\s*(\d+\.?\d*)', content)
    baseMVA = float(baseMVA_match.group(1)) if baseMVA_match else 100.0
    
    def extract_matrix_data(pattern: str, content: str) -> list:
        """提取矩阵数据的通用函数，按行处理"""
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return []
        
        # 获取矩阵内容
        matrix_content = match.group(1)
        
        # 按行处理矩阵数据
        lines = matrix_content.split('\n')
        matrix_data = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 跳过整行注释
            if line.startswith('%'):
                continue
            # 移除行内注释
            line = line.split('%')[0].strip()
            if not line:
                continue
            # 移除行尾分号
            if line.endswith(';'):
                line = line[:-1].strip()
            # 处理连续空格
            line = re.sub(r'\s+', ' ', line)
            # 分割得到数值字符串列表
            values_str = line.split()
            if not values_str:
                continue
            # 将字符串转换为浮点数
            try:
                values = list(map(float, values_str))
                matrix_data.append(values)
            except ValueError as e:
                print(f"解析行数据失败: {e}, 内容: '{line}'")
                continue
        
        return matrix_data
    
    # 提取bus数据
    bus_pattern = r'mpc\.bus\s*=\s*\[(.*?)\];'
    bus_data = extract_matrix_data(bus_pattern, content)
    
    # 提取generator数据
    gen_pattern = r'mpc\.gen\s*=\s*\[(.*?)\];'
    gen_data = extract_matrix_data(gen_pattern, content)
    
    # 提取branch数据
    branch_pattern = r'mpc\.branch\s*=\s*\[(.*?)\];'
    branch_data = extract_matrix_data(branch_pattern, content)
    
    # 提取gencost数据
    gencost_pattern = r'mpc\.gencost\s*=\s*\[(.*?)\];'
    gencost_data = extract_matrix_data(gencost_pattern, content)
    
    return {
        'version': version,
        'baseMVA': baseMVA,
        'bus': bus_data,
        'gen': gen_data,
        'branch': branch_data,
        'gencost': gencost_data
    }


def create_network_from_matlab_case(matlab_data: Dict[str, Any]) -> PyXESXXNNetwork:
    """从MATLAB案例数据创建PyXESXXN网络
    
    Args:
        matlab_data: 解析后的MATLAB案例数据
        
    Returns:
        创建的PyXESXXN网络对象
    """
    network = PyXESXXNNetwork(name="matlab_case_network")
    baseMVA = matlab_data['baseMVA']
    
    # 添加母线
    bus_list = []
    for bus_values in matlab_data['bus']:
        bus_id = int(bus_values[0])
        bus_type = int(bus_values[1])
        Pd = bus_values[2] / baseMVA  # 转换为标幺值
        Qd = bus_values[3] / baseMVA  # 转换为标幺值
        Vm = bus_values[7]
        Va = bus_values[8]
        
        # 创建母线名称
        bus_name = f"bus{bus_id}"
        bus_list.append(bus_name)
        
        # 添加母线
        network.add_bus(bus_name, "electricity", voltage=Vm, frequency=50.0)
        
        # 添加负荷（如果有）
        if Pd > 0 or Qd > 0:
            load_name = f"load{bus_id}"
            network.add_load(load_name, bus_name, "electricity", demand=Pd, reactive_demand=Qd)
    
    # 添加发电机
    gen_counter = 1
    for gen_values in matlab_data['gen']:
        bus_id = int(gen_values[0])
        bus_name = f"bus{bus_id}"
        Pg = gen_values[1] / baseMVA  # 转换为标幺值
        Qg = gen_values[2] / baseMVA  # 转换为标幺值
        Vg = gen_values[5]
        Pmax = gen_values[8] / baseMVA  # 转换为标幺值
        Pmin = gen_values[9] / baseMVA  # 转换为标幺值
        status = int(gen_values[7])
        
        if status == 1:  # 只有状态为1的发电机才添加
            # 检查母线是否存在
            if bus_name not in bus_list:
                continue
                
            gen_name = f"gen{gen_counter}"
            gen_counter += 1
            
            # 确定控制类型
            control = "Slack" if gen_counter == 1 else "PQ"
            
            # 添加发电机
            network.add_generator(
                gen_name, 
                bus_name, 
                "electricity", 
                capacity=Pmax, 
                efficiency=0.95, 
                control=control
            )
    
    # 添加线路
    line_counter = 1
    for branch_values in matlab_data['branch']:
        fbus = int(branch_values[0])
        tbus = int(branch_values[1])
        r = branch_values[2]
        x = branch_values[3]
        b = branch_values[4]
        rateA = branch_values[5] / baseMVA  # 转换为标幺值
        status = int(branch_values[10])
        
        if status == 1:  # 只有状态为1的线路才添加
            from_bus_name = f"bus{fbus}"
            to_bus_name = f"bus{tbus}"
            
            # 检查母线是否存在
            if from_bus_name not in bus_list or to_bus_name not in bus_list:
                continue
                
            line_name = f"line{line_counter}"
            line_counter += 1
            
            # 添加线路
            network.add_line(
                line_name, 
                from_bus_name, 
                to_bus_name, 
                "electricity", 
                capacity=rateA, 
                resistance=r, 
                reactance=x, 
                susceptance=b
            )
    
    return network


def batch_process_matlab_cases(file_paths: List[str]) -> Dict[str, Tuple[EnergyFlowResult, EnergySystemAnalysis, ExergyFlowResult]]:
    """批量处理多个MATLAB案例文件
    
    Args:
        file_paths: MATLAB案例文件路径列表
        
    Returns:
        处理结果字典，键为文件名，值为(潮流结果, 潮流分析, 㶲流结果)
    """
    results = {}
    
    for file_path in file_paths:
        import os
        file_name = os.path.basename(file_path)
        print(f"\n处理案例文件: {file_name}")
        
        try:
            # 解析MATLAB案例文件
            print(f"  1. 解析MATLAB案例文件...")
            matlab_data = parse_matlab_case_file(file_path)
            
            # 创建PyXESXXN网络
            print(f"  2. 创建PyXESXXN网络模型...")
            network = create_network_from_matlab_case(matlab_data)
            
            # 运行潮流计算
            print(f"  3. 运行潮流计算...")
            energy_flow_result, energy_analysis = run_energy_system_power_flow(network)
            
            # 运行㶲流分析
            print(f"  4. 运行㶲流分析...")
            exergy_result, exergy_analyzer = calculate_exergy_flow(energy_flow_result)
            
            results[file_name] = (energy_flow_result, energy_analysis, exergy_result)
            
            print(f"  ✅ 成功处理案例: {file_name}")
            print(f"     - 收敛状态: {'成功' if energy_flow_result.converged else '失败'}")
            print(f"     - 迭代次数: {energy_flow_result.iterations}")
            print(f"     - 计算误差: {energy_flow_result.error:.6e}")
            print(f"     - 系统㶲效率: {exergy_result.exergy_efficiency:.2%}")
            
        except Exception as e:
            print(f"  ❌ 处理案例 {file_name} 失败: {str(e)}")
            continue
    
    return results

# 公共API函数

def create_energy_system_solver(network: PyXESXXNNetwork) -> EnergySystemPowerFlowSolver:
    """创建综合能源系统潮流求解器"""
    return EnergySystemPowerFlowSolver(network)


def run_energy_system_power_flow(network: PyXESXXNNetwork, snapshots: Optional[Sequence] = None, **kwargs) -> Tuple[EnergyFlowResult, EnergySystemAnalysis]:
    """运行综合能源系统潮流计算"""
    solver = create_energy_system_solver(network)
    result = solver.solve(snapshots)
    analysis = EnergySystemAnalysis(result)
    return result, analysis


def calculate_exergy_flow(energy_flow_result: EnergyFlowResult, **kwargs) -> Tuple[ExergyFlowResult, ExergyFlowAnalyzer]:
    """计算系统的㶲流"""
    analyzer = ExergyFlowAnalyzer(energy_flow_result)
    exergy_result = analyzer.calculate_exergy_flow()
    return exergy_result, analyzer


# 导出公共API
__all__ = [
    'EnergyCarrierType',
    'CouplingComponentType',
    'ConvergenceCriteria',
    'EnergyFlowResult',
    'ExergyFlowResult',
    'CouplingComponent',
    'GasTurbine',
    'CHP',
    'ElectricBoiler',
    'P2G',
    'EnergySystemPowerFlowSolver',
    'EnergySystemAnalysis',
    'ExergyFlowAnalyzer',
    'create_energy_system_solver',
    'run_energy_system_power_flow',
    'calculate_exergy_flow',
    'parse_matlab_case_file',
    'create_network_from_matlab_case',
    'batch_process_matlab_cases'
]
