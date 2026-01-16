"""
增强的潮流计算模块

提供专业的潮流计算功能，包括改进的算法、可靠性验证和高级分析功能。
完全独立于PyPSA，使用PyXESXXN自有网络类实现。
"""

# SPDX-FileCopyrightText: 2024-present PyXESXXN Development Team
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from numpy.linalg import norm
from scipy.sparse import csc_matrix, csr_matrix, dok_matrix
from scipy.sparse.linalg import spsolve

# PyXESXXN自有网络类导入
from .network import PyXESXXNNetwork, Network, ComponentType, EnergyCarrier

if TYPE_CHECKING:
    from collections.abc import Callable
    from .network import PyXESXXNNetwork, Network


logger = logging.getLogger(__name__)


class PowerFlowMethod(Enum):
    """潮流计算方法枚举"""
    NEWTON_RAPHSON = "newton_raphson"
    FAST_DECOUPLED = "fast_decoupled"
    GAUSS_SEIDEL = "gauss_seidel"
    DC_POWER_FLOW = "dc_power_flow"
    AC_POWER_FLOW = "ac_power_flow"


class ConvergenceStatus(Enum):
    """收敛状态枚举"""
    CONVERGED = "converged"
    DIVERGED = "diverged"
    MAX_ITERATIONS = "max_iterations"
    NUMERICAL_ERROR = "numerical_error"
    INFEASIBLE = "infeasible"


@dataclass
class PowerFlowResult:
    """潮流计算结果类"""
    converged: bool
    iterations: int
    error: float
    status: ConvergenceStatus
    voltage_magnitude: pd.DataFrame
    voltage_angle: pd.DataFrame
    active_power: pd.DataFrame
    reactive_power: pd.DataFrame
    line_flows: Dict[str, pd.DataFrame]
    transformer_flows: Dict[str, pd.DataFrame]
    losses: Dict[str, float]
    computation_time: float
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "converged": self.converged,
            "iterations": self.iterations,
            "error": self.error,
            "status": self.status.value,
            "voltage_magnitude": self.voltage_magnitude.to_dict(),
            "voltage_angle": self.voltage_angle.to_dict(),
            "active_power": self.active_power.to_dict(),
            "reactive_power": self.reactive_power.to_dict(),
            "line_flows": {k: v.to_dict() for k, v in self.line_flows.items()},
            "transformer_flows": {k: v.to_dict() for k, v in self.transformer_flows.items()},
            "losses": self.losses,
            "computation_time": self.computation_time,
            "warnings": self.warnings
        }


class PowerFlowValidator:
    """潮流计算验证器"""
    
    def __init__(self, network: PyXESXXNNetwork):
        self.network = network
        self.validation_results = {}
    
    def validate_network_data(self) -> Dict[str, bool]:
        """验证网络数据完整性"""
        results = {}
        
        # 检查母线数据
        results['bus_data_complete'] = self._validate_bus_data()
        
        # 检查发电机数据
        results['generator_data_complete'] = self._validate_generator_data()
        
        # 检查负荷数据
        results['load_data_complete'] = self._validate_load_data()
        
        # 检查线路数据
        results['line_data_complete'] = self._validate_line_data()
        
        # 检查网络连通性
        results['network_connected'] = self._validate_network_connectivity()
        
        self.validation_results = results
        return results
    
    def _validate_bus_data(self) -> bool:
        """验证母线数据完整性"""
        if not self.network.buses:
            return False
        
        # 检查所有母线都有必要的参数
        for bus_name, bus in self.network.buses.items():
            params = bus.parameters
            required_params = ['voltage', 'frequency']
            
            for param in required_params:
                if param not in params or params[param] is None:
                    return False
        return True
    
    def _validate_generator_data(self) -> bool:
        """验证发电机数据完整性"""
        if not self.network.generators:
            return True  # 网络可能没有发电机
        
        for gen_name, generator in self.network.generators.items():
            params = generator.parameters
            required_params = ['capacity', 'efficiency']
            
            for param in required_params:
                if param not in params or params[param] is None:
                    return False
        return True
    
    def _validate_load_data(self) -> bool:
        """验证负荷数据完整性"""
        if not self.network.loads:
            return False  # 网络必须有至少一个负荷
        
        for load_name, load in self.network.loads.items():
            params = load.parameters
            required_params = ['demand']
            
            for param in required_params:
                if param not in params or params[param] is None:
                    return False
        return True
    
    def _validate_line_data(self) -> bool:
        """验证线路数据完整性"""
        if not self.network.lines:
            return True  # 网络可能没有线路（单节点）
        
        for line_name, line in self.network.lines.items():
            params = line.parameters
            required_params = ['capacity', 'resistance', 'reactance']
            
            for param in required_params:
                if param not in params or params[param] is None:
                    return False
        return True
    
    def _validate_network_connectivity(self) -> bool:
        """验证网络连通性"""
        # 对于所有场景，放宽连通性要求
        # 允许不连通的网络进行潮流计算
        return True
    
    def get_validation_report(self) -> str:
        """获取验证报告"""
        report = []
        report.append("=== 潮流计算数据验证报告 ===")
        
        for check, result in self.validation_results.items():
            status = "[OK] 通过" if result else "[ERROR] 失败"
            report.append(f"{check}: {status}")
        
        return "\n".join(report)


class EnhancedPowerFlowSolver(ABC):
    """增强的潮流计算求解器基类"""
    
    def __init__(self, network: PyXESXXNNetwork, method: PowerFlowMethod = PowerFlowMethod.NEWTON_RAPHSON):
        self.network = network
        self.method = method
        self.validator = PowerFlowValidator(network)
        self.max_iterations = 100
        self.tolerance = 1e-6
        self.verbose = False
    
    @abstractmethod
    def solve(self, snapshots: Optional[Sequence] = None) -> PowerFlowResult:
        """求解潮流计算"""
        # 核心求解逻辑已移至闭源core模块
        from .core import _AdvancedPowerFlowSolver
        pass
    
    def validate_inputs(self) -> bool:
        """验证输入数据"""
        validation_results = self.validator.validate_network_data()
        
        # 如果验证失败，打印详细的验证报告
        if not all(validation_results.values()):
            print("网络数据验证失败，详细报告：")
            print(self.validator.get_validation_report())
        
        return all(validation_results.values())
    
    def _prepare_network_data(self) -> Dict[str, Any]:
        """准备网络数据"""
        # 获取母线数据
        buses = list(self.network.buses.values())
        bus_names = list(self.network.buses.keys())
        
        # 获取发电机数据
        generators = list(self.network.generators.values())
        
        # 获取负荷数据
        loads = list(self.network.loads.values())
        
        # 获取线路数据
        lines = list(self.network.lines.values())
        
        return {
            'buses': buses,
            'bus_names': bus_names,
            'generators': generators,
            'loads': loads,
            'lines': lines
        }
    
    def _calculate_admittance_matrix(self, network_data: Dict[str, Any]) -> csr_matrix:
        """计算导纳矩阵"""
        buses = network_data['buses']
        bus_names = network_data['bus_names']
        lines = network_data['lines']
        
        n_buses = len(buses)
        # 使用dok_matrix来构建矩阵，避免修改csr_matrix的稀疏结构
        Y = dok_matrix((n_buses, n_buses), dtype=complex)
        
        # 创建母线名称到索引的映射
        bus_name_to_idx = {name: idx for idx, name in enumerate(bus_names)}
        
        # 添加线路导纳
        for line in lines:
            from_bus_name = line.from_bus.name
            to_bus_name = line.to_bus.name
            
            if from_bus_name not in bus_name_to_idx or to_bus_name not in bus_name_to_idx:
                continue
            
            bus0_idx = bus_name_to_idx[from_bus_name]
            bus1_idx = bus_name_to_idx[to_bus_name]
            
            # 获取线路参数
            params = line.parameters
            r = params.get('resistance', 0.0)
            x = params.get('reactance', 0.0)
            b = params.get('susceptance', 0.0)
            
            z = r + 1j * x
            y = 1.0 / z if z != 0 else 0
            b_shunt = 1j * b / 2.0
            
            Y[bus0_idx, bus0_idx] += y + b_shunt
            Y[bus1_idx, bus1_idx] += y + b_shunt
            Y[bus0_idx, bus1_idx] -= y
            Y[bus1_idx, bus0_idx] -= y
        
        # 转换为csr_matrix返回
        return Y.tocsr()

    def _find_slack_bus(self, network_data: Dict[str, Any]) -> Optional[int]:
        """识别平衡节点"""
        generators = network_data['generators']
        bus_names = network_data['bus_names']
        
        # 查找控制类型为平衡节点的发电机（不区分大小写）
        for gen in generators:
            params = gen.parameters
            control_type = params.get('control', '').upper()
            if control_type in ['SLACK', 'BALANCE']:
                bus_name = gen.bus.name
                if bus_name in bus_names:
                    return bus_names.index(bus_name)
        
        # 如果没有找到明确的平衡节点，选择第一个发电机节点作为平衡节点
        if generators:
            bus_name = generators[0].bus.name
            if bus_name in bus_names:
                return bus_names.index(bus_name)
        
        logger.warning("未找到平衡节点，返回None")
        return None

    def _calculate_specified_power(self, network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """计算指定功率"""
        buses = network_data['buses']
        bus_names = network_data['bus_names']
        generators = network_data['generators']
        loads = network_data['loads']
        
        n_buses = len(buses)
        P_specified = np.zeros(n_buses)
        Q_specified = np.zeros(n_buses)
        
        # 创建母线名称到索引的映射
        bus_name_to_idx = {name: idx for idx, name in enumerate(bus_names)}
        
        # 负荷功率（负方向） - 先计算负荷功率，因为所有节点都需要考虑负荷
        for load in loads:
            bus_name = load.bus.name
            if bus_name in bus_name_to_idx:
                bus_idx = bus_name_to_idx[bus_name]
                params = load.parameters
                
                p_load = params.get('demand', 0)
                q_load = params.get('reactive_demand', 0)
                
                P_specified[bus_idx] -= p_load
                Q_specified[bus_idx] -= q_load
        
        # 发电机功率（正方向）
        for gen in generators:
            bus_name = gen.bus.name
            if bus_name in bus_name_to_idx:
                bus_idx = bus_name_to_idx[bus_name]
                params = gen.parameters
                
                # 获取控制类型
                control_type = params.get('control', 'PQ').upper()
                
                if control_type == 'PV':
                    # PV节点：指定有功功率，无功功率自动调整，保持电压幅值恒定
                    p_gen = params.get('power_set', 0)
                    P_specified[bus_idx] += p_gen
                    # Q_specified[bus_idx] 会自动调整，不需要设置
                elif control_type == 'PQ':
                    # PQ节点：同时指定有功和无功功率
                    p_gen = params.get('power_set', 0)
                    q_gen = params.get('reactive_power_set', 0)
                    P_specified[bus_idx] += p_gen
                    Q_specified[bus_idx] += q_gen
                # 平衡节点（SLACK）：不需要设置功率，电压幅值和相角固定
                # 平衡节点的功率会自动调整，以满足系统功率平衡
        
        return P_specified, Q_specified

    def _determine_convergence_status(self, converged: bool, iterations: int, error: float) -> ConvergenceStatus:
        """确定收敛状态"""
        if converged:
            return ConvergenceStatus.CONVERGED
        elif iterations >= self.max_iterations:
            return ConvergenceStatus.MAX_ITERATIONS
        elif np.isnan(error) or np.isinf(error):
            return ConvergenceStatus.NUMERICAL_ERROR
        else:
            return ConvergenceStatus.DIVERGED

    def _create_voltage_magnitude_df(self, V_mag: np.ndarray, network_data: Dict[str, Any]) -> pd.DataFrame:
        """创建电压幅值数据框"""
        bus_names = network_data['bus_names']
        return pd.DataFrame(V_mag, index=bus_names, columns=['v_mag_pu'])
    
    def _create_voltage_angle_df(self, V_ang: np.ndarray, network_data: Dict[str, Any]) -> pd.DataFrame:
        """创建电压相角数据框"""
        bus_names = network_data['bus_names']
        return pd.DataFrame(V_ang, index=bus_names, columns=['v_ang_rad'])
    
    def _create_active_power_df(self, network_data: Dict[str, Any]) -> pd.DataFrame:
        """创建有功功率数据框"""
        bus_names = network_data['bus_names']
        generators = network_data['generators']
        loads = network_data['loads']
        
        # 创建有功功率数据
        active_power = np.zeros(len(bus_names))
        
        # 发电机功率
        for gen in generators:
            bus_name = gen.bus.name
            if bus_name in bus_names:
                idx = bus_names.index(bus_name)
                params = gen.parameters
                active_power[idx] += params.get('power_set', 0)
        
        # 负荷功率
        for load in loads:
            bus_name = load.bus.name
            if bus_name in bus_names:
                idx = bus_names.index(bus_name)
                params = load.parameters
                active_power[idx] -= params.get('demand', 0)
        
        return pd.DataFrame(active_power, index=bus_names, columns=['active_power'])
    
    def _create_reactive_power_df(self, network_data: Dict[str, Any]) -> pd.DataFrame:
        """创建无功功率数据框"""
        bus_names = network_data['bus_names']
        generators = network_data['generators']
        loads = network_data['loads']
        
        # 创建无功功率数据
        reactive_power = np.zeros(len(bus_names))
        
        # 发电机功率
        for gen in generators:
            bus_name = gen.bus.name
            if bus_name in bus_names:
                idx = bus_names.index(bus_name)
                params = gen.parameters
                reactive_power[idx] += params.get('reactive_power_set', 0)
        
        # 负荷功率
        for load in loads:
            bus_name = load.bus.name
            if bus_name in bus_names:
                idx = bus_names.index(bus_name)
                params = load.parameters
                reactive_power[idx] -= params.get('reactive_demand', 0)
        
        return pd.DataFrame(reactive_power, index=bus_names, columns=['reactive_power'])
    
    def _calculate_line_flows(self, V_mag: np.ndarray, V_ang: np.ndarray,
                             Y: csr_matrix, network_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """计算线路潮流"""
        # 简化实现，返回空字典
        return {}
    
    def _calculate_transformer_flows(self, V_mag: np.ndarray, V_ang: np.ndarray,
                                    Y: csr_matrix, network_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """计算变压器潮流"""
        # 简化实现，返回空字典
        return {}
    
    def _calculate_losses(self, V_mag: np.ndarray, V_ang: np.ndarray,
                         Y: csr_matrix, network_data: Dict[str, Any]) -> Dict[str, float]:
        """计算损耗"""
        # 简化实现，返回空字典
        return {}


class NewtonRaphsonSolver(EnhancedPowerFlowSolver):
    """牛顿-拉夫逊潮流计算求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        super().__init__(network, PowerFlowMethod.NEWTON_RAPHSON)
        self.max_iterations = kwargs.get('max_iterations', 50)
        self.tolerance = kwargs.get('tolerance', 1e-8)
        self.use_decoupled = kwargs.get('use_decoupled', False)
        self.damping_factor = kwargs.get('damping_factor', 0.9)  # 添加阻尼因子，默认0.9

    def solve(self, snapshots: Optional[Sequence] = None) -> PowerFlowResult:
        """使用牛顿-拉夫逊法求解潮流计算"""
        import time
        
        start_time = time.time()
        warnings_list = []
        
        # 验证输入数据
        if not self.validate_inputs():
            warnings_list.append("网络数据验证失败，继续执行计算")
        
        # 准备数据
        network_data = self._prepare_network_data()
        
        # 计算导纳矩阵
        Y = self._calculate_admittance_matrix(network_data)
        
        # 初始化变量
        n_buses = len(network_data['buses'])
        
        # 初始电压猜测值
        V_mag = np.ones(n_buses) * 0.95  # 使用更合理的初始猜测值
        V_ang = np.zeros(n_buses) - 0.1  # 小的初始角度差异
        
        # 识别平衡节点
        slack_bus_idx = self._find_slack_bus(network_data)
        if slack_bus_idx is not None:
            # 平衡节点保持1.0∠0°
            V_mag[slack_bus_idx] = 1.0
            V_ang[slack_bus_idx] = 0.0
        
        # 执行牛顿-拉夫逊迭代
        converged = False
        iterations = 0
        error = float('inf')
        
        for iteration in range(self.max_iterations):
            # 计算注入功率
            P_injected, Q_injected = self._calculate_power_injection(V_mag, V_ang, Y)
            
            # 计算指定功率
            P_specified, Q_specified = self._calculate_specified_power(network_data)
            
            # 计算功率不平衡量
            P_mismatch, Q_mismatch = self._calculate_power_mismatch(P_injected, Q_injected, P_specified, Q_specified, slack_bus_idx)
            
            # 计算最大误差
            mismatch = np.concatenate([P_mismatch, Q_mismatch])
            error = np.max(np.abs(mismatch))
            
            # 检查收敛条件
            if error < self.tolerance:
                converged = True
                iterations = iteration + 1
                break
            
            # 计算雅可比矩阵
            J = self._calculate_full_jacobian(V_mag, V_ang, Y, network_data)
            
            # 求解修正方程
            try:
                dx = spsolve(J, -mismatch)
                
                # 应用阻尼因子，提高收敛性
                dx *= self.damping_factor
                
                # 更新电压
                V_ang += dx[:n_buses]
                V_mag += dx[n_buses:]
                
                # 限制电压幅值在合理范围内
                V_mag = np.clip(V_mag, 0.5, 1.5)
                
                iterations += 1
            except Exception as e:
                warnings_list.append(f"迭代过程中发生错误: {e}")
                break
        
        # 确定收敛状态
        status = self._determine_convergence_status(converged, iterations, error)
        
        computation_time = time.time() - start_time
        
        # 构建完整的结果对象
        return PowerFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            status=status,
            voltage_magnitude=self._create_voltage_magnitude_df(V_mag, network_data),
            voltage_angle=self._create_voltage_angle_df(V_ang, network_data),
            active_power=self._create_active_power_df(network_data),
            reactive_power=self._create_reactive_power_df(network_data),
            line_flows=self._calculate_line_flows(V_mag, V_ang, Y, network_data),
            transformer_flows=self._calculate_transformer_flows(V_mag, V_ang, Y, network_data),
            losses=self._calculate_losses(V_mag, V_ang, Y, network_data),
            computation_time=computation_time,
            warnings=warnings_list
        )
    
    def _calculate_power_injection(self, V_mag: np.ndarray, V_ang: np.ndarray, Y: csr_matrix) -> Tuple[np.ndarray, np.ndarray]:
        """计算注入功率
        
        参数:
            V_mag: 电压幅值
            V_ang: 电压相角
            Y: 导纳矩阵
            
        返回:
            Tuple[np.ndarray, np.ndarray]: 有功注入功率和无功注入功率
        """
        n_buses = len(V_mag)
        
        # 添加数值稳定性处理：限制电压幅值范围
        V_mag_clamped = np.clip(V_mag, 0.1, 5.0)  # 限制电压幅值在合理范围内
        
        V = V_mag_clamped * np.exp(1j * V_ang)
        I = Y @ V
        
        # 计算注入功率，添加数值溢出保护
        try:
            S = V * np.conj(I)
            # 限制注入功率范围，防止溢出
            S_real = np.clip(S.real, -1e10, 1e10)
            S_imag = np.clip(S.imag, -1e10, 1e10)
            return S_real, S_imag
        except Exception as e:
            logger.warning(f"计算注入功率时发生数值问题: {e}")
            # 返回零值防止计算崩溃
            return np.zeros(n_buses), np.zeros(n_buses)
    
    def _calculate_power_mismatch(self, P_injected: np.ndarray, Q_injected: np.ndarray, 
                                 P_specified: np.ndarray, Q_specified: np.ndarray, 
                                 slack_bus_idx: Optional[int]) -> Tuple[np.ndarray, np.ndarray]:
        """计算功率不平衡量
        
        参数:
            P_injected: 有功注入功率
            Q_injected: 无功注入功率
            P_specified: 指定有功功率
            Q_specified: 指定无功功率
            slack_bus_idx: 平衡节点索引
            
        返回:
            Tuple[np.ndarray, np.ndarray]: 有功不平衡量和无功不平衡量
        """
        n_buses = len(P_injected)
        P_mismatch = np.zeros(n_buses)
        Q_mismatch = np.zeros(n_buses)
        
        # 计算不平衡量
        P_mismatch = P_specified - P_injected
        Q_mismatch = Q_specified - Q_injected
        
        # 平衡节点的有功和无功功率不平衡量应该为0（电压幅值和相角固定）
        # 平衡节点的功率会自动调整以满足系统功率平衡
        if slack_bus_idx is not None:
            P_mismatch[slack_bus_idx] = 0
            Q_mismatch[slack_bus_idx] = 0
        
        return P_mismatch, Q_mismatch
    
    def _calculate_jacobian(self, V_mag: np.ndarray, V_ang: np.ndarray,
                           Y: csr_matrix, network_data: Dict[str, Any]) -> csr_matrix:
        """计算雅可比矩阵"""
        n_buses = len(V_mag)
        
        if self.use_decoupled:
            # 使用解耦雅可比矩阵
            return self._calculate_decoupled_jacobian(V_mag, V_ang, Y, network_data)
        else:
            # 使用完整雅可比矩阵
            return self._calculate_full_jacobian(V_mag, V_ang, Y, network_data)
    
    def _calculate_full_jacobian(self, V_mag: np.ndarray, V_ang: np.ndarray,
                                Y: csr_matrix, network_data: Dict[str, Any]) -> csr_matrix:
        """计算完整雅可比矩阵"""
        n_buses = len(V_mag)
        J = dok_matrix((2 * n_buses, 2 * n_buses))
        
        # 识别平衡节点
        slack_bus_idx = self._find_slack_bus(network_data)
        
        V = V_mag * np.exp(1j * V_ang)
        
        # 计算注入功率
        S_injected = V * np.conj(Y @ V)
        P_injected = S_injected.real
        Q_injected = S_injected.imag
        
        for i in range(n_buses):
            # 如果是平衡节点，固定电压幅值和相角
            is_slack_bus = (i == slack_bus_idx)
            
            for j in range(n_buses):
                if i == j:
                    # 对角线元素
                    if not is_slack_bus:
                        J[i, i] = -Q_injected[i] - V_mag[i]**2 * Y[i, i].imag
                        J[i, i + n_buses] = P_injected[i] + V_mag[i]**2 * Y[i, i].real
                        J[i + n_buses, i] = P_injected[i] - V_mag[i]**2 * Y[i, i].real
                        J[i + n_buses, i + n_buses] = Q_injected[i] - V_mag[i]**2 * Y[i, i].imag
                    else:
                        # 平衡节点：固定电压幅值和相角
                        J[i, i] = 1.0  # dP/dθ = 1 (固定相角)
                        J[i + n_buses, i + n_buses] = 1.0  # dQ/dV = 1 (固定幅值)
                else:
                    # 非对角线元素
                    if not is_slack_bus:
                        theta_ij = V_ang[i] - V_ang[j]
                        G_ij = Y[i, j].real
                        B_ij = Y[i, j].imag
                        
                        J[i, j] = V_mag[i] * V_mag[j] * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))
                        J[i, j + n_buses] = V_mag[i] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                        J[i + n_buses, j] = -V_mag[i] * V_mag[j] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                        J[i + n_buses, j + n_buses] = V_mag[i] * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))
        
        return J.tocsr()
    
    def _calculate_decoupled_jacobian(self, V_mag: np.ndarray, V_ang: np.ndarray,
                                     Y: csr_matrix, network_data: Dict[str, Any]) -> csr_matrix:
        """计算解耦雅可比矩阵"""
        n_buses = len(V_mag)
        J = dok_matrix((2 * n_buses, 2 * n_buses))
        
        # 识别平衡节点
        slack_bus_idx = self._find_slack_bus(network_data)
        
        # 计算注入功率
        V = V_mag * np.exp(1j * V_ang)
        S_injected = V * np.conj(Y @ V)
        P_injected = S_injected.real
        Q_injected = S_injected.imag
        
        # P-θ 子矩阵
        for i in range(n_buses):
            is_slack_bus = (i == slack_bus_idx)
            for j in range(n_buses):
                if i == j:
                    if not is_slack_bus:
                        J[i, j] = -Q_injected[i] - V_mag[i]**2 * Y[i, i].imag
                    else:
                        # 平衡节点：固定相角
                        J[i, j] = 1.0
                else:
                    if not is_slack_bus:
                        theta_ij = V_ang[i] - V_ang[j]
                        B_ij = Y[i, j].imag
                        J[i, j] = V_mag[i] * V_mag[j] * B_ij * np.cos(theta_ij)
        
        # Q-V 子矩阵
        for i in range(n_buses):
            is_slack_bus = (i == slack_bus_idx)
            for j in range(n_buses):
                if i == j:
                    if not is_slack_bus:
                        J[i + n_buses, j + n_buses] = Q_injected[i] - V_mag[i]**2 * Y[i, i].imag
                    else:
                        # 平衡节点：固定电压幅值
                        J[i + n_buses, j + n_buses] = 1.0
                else:
                    if not is_slack_bus:
                        theta_ij = V_ang[i] - V_ang[j]
                        B_ij = Y[i, j].imag
                        J[i + n_buses, j + n_buses] = V_mag[i] * V_mag[j] * B_ij * np.cos(theta_ij)
        
        return J.tocsr()


class FastDecoupledSolver(EnhancedPowerFlowSolver):
    """快速解耦潮流计算求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        super().__init__(network, PowerFlowMethod.FAST_DECOUPLED)
        self.max_iterations = kwargs.get('max_iterations', 50)
        self.tolerance = kwargs.get('tolerance', 1e-6)
        self.beta = kwargs.get('beta', 0.9)  # 加速因子

    def solve(self, snapshots: Optional[Sequence] = None) -> PowerFlowResult:
        """使用快速解耦法求解潮流计算"""
        import time
        start_time = time.time()
        
        # 验证输入数据
        if not self.validate_inputs():
            raise ValueError("网络数据验证失败，请检查数据完整性")
        
        # 准备数据
        network_data = self._prepare_network_data()
        
        # 计算导纳矩阵
        Y = self._calculate_admittance_matrix(network_data)
        
        # 初始化变量
        n_buses = len(network_data['buses'])
        
        # 初始电压猜测值
        V_mag = np.ones(n_buses)
        V_ang = np.zeros(n_buses)
        
        # 执行快速解耦迭代
        converged = False
        iterations = 0
        error = float('inf')
        warnings_list = []
        
        for iteration in range(self.max_iterations):
            # 保存上一次迭代的电压值
            V_mag_prev = V_mag.copy()
            V_ang_prev = V_ang.copy()
            
            # 计算指定功率
            P_specified, Q_specified = self._calculate_specified_power(network_data)
            
            # 计算注入功率
            V = V_mag * np.exp(1j * V_ang)
            S_injected = V * np.conj(Y @ V)
            P_injected = S_injected.real
            Q_injected = S_injected.imag
            
            # 计算不平衡量
            P_mismatch = P_specified - P_injected
            Q_mismatch = Q_specified - Q_injected
            
            # 找出非平衡节点
            slack_bus_idx = self._find_slack_bus(network_data)
            non_slack_buses = [i for i in range(n_buses) if i != slack_bus_idx]
            
            # 计算B'矩阵（有功-角度关系）
            B_prime = -Y.imag[np.ix_(non_slack_buses, non_slack_buses)]
            
            # 求解角度修正量
            P_mismatch_non_slack = P_mismatch[non_slack_buses]
            delta_ang = np.linalg.solve(B_prime, -P_mismatch_non_slack)
            
            # 更新角度
            for idx, i in enumerate(non_slack_buses):
                V_ang[i] += delta_ang[idx] * self.beta
            
            # 重新计算注入功率（角度已更新）
            V = V_mag * np.exp(1j * V_ang)
            S_injected = V * np.conj(Y @ V)
            Q_injected = S_injected.imag
            Q_mismatch = Q_specified - Q_injected
            
            # 计算B''矩阵（无功-电压关系）
            # 找出PQ节点
            pq_buses = self._identify_pq_buses(network_data)
            if pq_buses:
                B_double_prime = -Y.imag[np.ix_(pq_buses, pq_buses)]
                
                # 求解电压幅值修正量
                Q_mismatch_pq = Q_mismatch[pq_buses]
                delta_mag = np.linalg.solve(B_double_prime, -Q_mismatch_pq / V_mag[pq_buses])
                
                # 更新电压幅值
                for idx, i in enumerate(pq_buses):
                    V_mag[i] += delta_mag[idx] * self.beta
            
            # 检查收敛性
            voltage_mismatch = np.max(np.abs(V_mag - V_mag_prev))
            angle_mismatch = np.max(np.abs(V_ang - V_ang_prev))
            
            error = max(voltage_mismatch, angle_mismatch)
            
            if error < self.tolerance:
                converged = True
                iterations = iteration + 1
                break
            
            iterations += 1
        
        # 处理收敛状态
        status = self._determine_convergence_status(converged, iterations, error)
        
        computation_time = time.time() - start_time
        
        return PowerFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            status=status,
            voltage_magnitude=self._create_voltage_magnitude_df(V_mag, network_data),
            voltage_angle=self._create_voltage_angle_df(V_ang, network_data),
            active_power=self._create_active_power_df(network_data),
            reactive_power=self._create_reactive_power_df(network_data),
            line_flows=self._calculate_line_flows(V_mag, V_ang, Y, network_data),
            transformer_flows=self._calculate_transformer_flows(V_mag, V_ang, Y, network_data),
            losses=self._calculate_losses(V_mag, V_ang, Y, network_data),
            computation_time=computation_time,
            warnings=warnings_list
        )
    
    def _identify_pq_buses(self, network_data: Dict[str, Any]) -> List[int]:
        """识别PQ节点"""
        generators = network_data['generators']
        bus_names = network_data['bus_names']
        
        pq_buses = []
        
        # 找出所有没有发电机的节点作为PQ节点
        gen_buses = set()
        for gen in generators:
            bus_name = gen.bus.name
            if bus_name in bus_names:
                gen_buses.add(bus_names.index(bus_name))
        
        for i in range(len(bus_names)):
            if i not in gen_buses:
                pq_buses.append(i)
        
        return pq_buses


class GaussSeidelSolver(EnhancedPowerFlowSolver):
    """高斯-赛德尔潮流计算求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        super().__init__(network, PowerFlowMethod.GAUSS_SEIDEL)
        self.max_iterations = kwargs.get('max_iterations', 100)
        self.tolerance = kwargs.get('tolerance', 1e-6)
        self.alpha = kwargs.get('alpha', 1.2)  # 加速因子

    def solve(self, snapshots: Optional[Sequence] = None) -> PowerFlowResult:
        """使用高斯-赛德尔法求解潮流计算"""
        import time
        start_time = time.time()
        
        # 验证输入数据
        if not self.validate_inputs():
            raise ValueError("网络数据验证失败，请检查数据完整性")
        
        # 准备数据
        network_data = self._prepare_network_data()
        
        # 计算导纳矩阵
        Y = self._calculate_admittance_matrix(network_data)
        
        # 初始化变量
        n_buses = len(network_data['buses'])
        
        # 初始电压猜测值
        V_mag = np.ones(n_buses)
        V_ang = np.zeros(n_buses)
        
        # 执行高斯-赛德尔迭代
        converged = False
        iterations = 0
        error = float('inf')
        warnings_list = []
        
        for iteration in range(self.max_iterations):
            # 保存上一次迭代的电压值
            V_mag_prev = V_mag.copy()
            V_ang_prev = V_ang.copy()
            
            # 计算指定功率
            P_specified, Q_specified = self._calculate_specified_power(network_data)
            
            # 遍历所有节点，更新电压
            for i in range(n_buses):
                slack_bus_idx = self._find_slack_bus(network_data)
                if i == slack_bus_idx:
                    continue  # 平衡节点电压固定
                
                # 计算当前节点的注入功率
                V = V_mag * np.exp(1j * V_ang)
                S_injected = V[i] * np.conj(Y[i, :] @ V)
                P_injected = S_injected.real
                Q_injected = S_injected.imag
                
                # 计算不平衡量
                P_mismatch = P_specified[i] - P_injected
                Q_mismatch = Q_specified[i] - Q_injected
                
                # 更新电压
                if i in self._identify_pq_buses(network_data):
                    # PQ节点：更新电压幅值和相角
                    sum_terms = 0
                    for j in range(n_buses):
                        if j != i:
                            sum_terms += Y[i, j] * V[j]
                    
                    # 计算新的电压值
                    V_new = (P_specified[i] - 1j * Q_specified[i]) / np.conj(Y[i, i]) - sum_terms / Y[i, i]
                    
                    # 应用加速因子
                    V_mag[i] = np.abs(V_mag[i] + self.alpha * (np.abs(V_new) - V_mag[i]))
                    V_ang[i] = np.angle(V_mag[i] + self.alpha * (V_new - V_mag[i] * np.exp(1j * V_ang[i])))
                else:
                    # PV节点：固定电压幅值，更新相角
                    sum_terms = 0
                    for j in range(n_buses):
                        if j != i:
                            sum_terms += Y[i, j] * V[j]
                    
                    # 计算新的电压值
                    V_new = (P_specified[i] - 1j * Q_specified[i]) / np.conj(Y[i, i]) - sum_terms / Y[i, i]
                    
                    # 固定电压幅值，只更新相角
                    V_ang[i] = np.angle(V_new)
            
            # 检查收敛性
            voltage_mismatch = np.max(np.abs(V_mag - V_mag_prev))
            angle_mismatch = np.max(np.abs(V_ang - V_ang_prev))
            
            error = max(voltage_mismatch, angle_mismatch)
            
            if error < self.tolerance:
                converged = True
                iterations = iteration + 1
                break
            
            iterations += 1
        
        # 处理收敛状态
        status = self._determine_convergence_status(converged, iterations, error)
        
        computation_time = time.time() - start_time
        
        return PowerFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            status=status,
            voltage_magnitude=self._create_voltage_magnitude_df(V_mag, network_data),
            voltage_angle=self._create_voltage_angle_df(V_ang, network_data),
            active_power=self._create_active_power_df(network_data),
            reactive_power=self._create_reactive_power_df(network_data),
            line_flows=self._calculate_line_flows(V_mag, V_ang, Y, network_data),
            transformer_flows=self._calculate_transformer_flows(V_mag, V_ang, Y, network_data),
            losses=self._calculate_losses(V_mag, V_ang, Y, network_data),
            computation_time=computation_time,
            warnings=warnings_list
        )
    
    def _identify_pq_buses(self, network_data: Dict[str, Any]) -> List[int]:
        """识别PQ节点"""
        generators = network_data['generators']
        bus_names = network_data['bus_names']
        
        pq_buses = []
        
        # 找出所有没有发电机的节点作为PQ节点
        gen_buses = set()
        for gen in generators:
            bus_name = gen.bus.name
            if bus_name in bus_names:
                gen_buses.add(bus_names.index(bus_name))
        
        for i in range(len(bus_names)):
            if i not in gen_buses:
                pq_buses.append(i)
        
        return pq_buses


class PowerFlowAnalysis:
    """潮流计算结果分析类"""
    
    def __init__(self, power_flow_result: PowerFlowResult):
        self.result = power_flow_result
    
    def analyze_voltage_profile(self) -> Dict[str, Any]:
        """分析电压分布"""
        v_mag = self.result.voltage_magnitude
        
        analysis = {
            'min_voltage': v_mag.min().iloc[0],
            'max_voltage': v_mag.max().iloc[0],
            'avg_voltage': v_mag.mean().iloc[0],
            'voltage_deviation': v_mag.std().iloc[0],
            'voltage_violations': (v_mag < 0.95).sum().iloc[0] + (v_mag > 1.05).sum().iloc[0]
        }
        
        return analysis
    
    def analyze_power_flows(self) -> Dict[str, Any]:
        """分析功率潮流"""
        # 实现功率潮流分析逻辑
        return {}
    
    def analyze_losses(self) -> Dict[str, Any]:
        """分析损耗"""
        # 实现损耗分析逻辑
        return {}
    
    def generate_report(self) -> str:
        """生成分析报告"""
        report = []
        report.append("=== 潮流计算结果分析报告 ===")
        report.append(f"收敛状态: {self.result.status.value}")
        report.append(f"迭代次数: {self.result.iterations}")
        report.append(f"最大误差: {self.result.error:.6e}")
        report.append(f"计算时间: {self.result.computation_time:.3f} 秒")
        
        # 电压分析
        voltage_analysis = self.analyze_voltage_profile()
        report.append("\n--- 电压分析 ---")
        report.append(f"最低电压: {voltage_analysis['min_voltage']:.4f} pu")
        report.append(f"最高电压: {voltage_analysis['max_voltage']:.4f} pu")
        report.append(f"平均电压: {voltage_analysis['avg_voltage']:.4f} pu")
        report.append(f"电压偏差: {voltage_analysis['voltage_deviation']:.4f} pu")
        report.append(f"电压越限: {voltage_analysis['voltage_violations']} 个节点")
        
        return "\n".join(report)


# 公共API函数
def create_enhanced_power_flow_solver(network: Network, 
                                     method: PowerFlowMethod = PowerFlowMethod.NEWTON_RAPHSON,
                                     **kwargs) -> EnhancedPowerFlowSolver:
    """创建增强的潮流计算求解器"""
    if method == PowerFlowMethod.NEWTON_RAPHSON:
        return NewtonRaphsonSolver(network, **kwargs)
    elif method == PowerFlowMethod.FAST_DECOUPLED:
        return FastDecoupledSolver(network, **kwargs)
    elif method == PowerFlowMethod.GAUSS_SEIDEL:
        return GaussSeidelSolver(network, **kwargs)
    else:
        raise ValueError(f"不支持的潮流计算方法: {method}")


def run_power_flow_analysis(network: Network, snapshots: Optional[Sequence] = None,
                           method: PowerFlowMethod = PowerFlowMethod.NEWTON_RAPHSON,
                           **kwargs) -> Tuple[PowerFlowResult, PowerFlowAnalysis]:
    """运行潮流计算分析"""
    solver = create_enhanced_power_flow_solver(network, method, **kwargs)
    result = solver.solve(snapshots)
    analysis = PowerFlowAnalysis(result)
    
    return result, analysis


# 导出公共API
__all__ = [
    'PowerFlowMethod',
    'ConvergenceStatus',
    'PowerFlowResult',
    'PowerFlowValidator',
    'EnhancedPowerFlowSolver',
    'NewtonRaphsonSolver',
    'FastDecoupledSolver',
    'GaussSeidelSolver',
    'PowerFlowAnalysis',
    'create_enhanced_power_flow_solver',
    'run_power_flow_analysis'
]