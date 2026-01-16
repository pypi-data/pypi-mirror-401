#!/usr/bin/env python3
"""
基于牛顿-拉夫逊法的潮流计算实现

这个模块重新实现了基于牛顿-拉夫逊法的潮流计算，确保计算的准确性和收敛性。
"""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, lil_matrix
from typing import Dict, List, Optional, Tuple, Any, Sequence
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PowerFlowMethod(Enum):
    """潮流计算方法枚举"""
    NEWTON_RAPHSON = "newton_raphson"
    FAST_DECOUPLED = "fast_decoupled"
    GAUSS_SEIDEL = "gauss_seidel"


class ConvergenceStatus(Enum):
    """收敛状态枚举"""
    CONVERGED = "converged"
    DIVERGED = "diverged"
    MAX_ITERATIONS_REACHED = "max_iterations_reached"
    NUMERICAL_ERROR = "numerical_error"


class PowerFlowResult:
    """潮流计算结果类"""
    def __init__(self, converged: bool, iterations: int, error: float,
                 voltage_magnitude: Optional[pd.DataFrame] = None,
                 voltage_angle: Optional[pd.DataFrame] = None,
                 active_power: Optional[pd.DataFrame] = None,
                 reactive_power: Optional[pd.DataFrame] = None,
                 line_flows: Optional[Dict] = None,
                 losses: Optional[Dict] = None,
                 status: ConvergenceStatus = ConvergenceStatus.DIVERGED):
        self.converged = converged
        self.iterations = iterations
        self.error = error
        self.voltage_magnitude = voltage_magnitude
        self.voltage_angle = voltage_angle
        self.active_power = active_power
        self.reactive_power = reactive_power
        self.line_flows = line_flows
        self.losses = losses if losses is not None else {}
        self.status = status


class PowerFlowAnalysis:
    """潮流计算分析类"""
    def __init__(self, result: PowerFlowResult):
        self.result = result

    def get_voltage_profile(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """获取电压分布"""
        return self.result.voltage_magnitude, self.result.voltage_angle

    def get_line_flows(self) -> Dict:
        """获取线路潮流"""
        return self.result.line_flows

    def get_losses(self) -> Dict:
        """获取损耗"""
        return self.result.losses


class NewtonRaphsonPowerFlow:
    """基于牛顿-拉夫逊法的潮流计算求解器"""
    
    def __init__(self, network):
        self.network = network
        self.max_iterations = 50
        self.tolerance = 1e-8
        self.damping_factor = 0.8
    
    def solve(self, snapshots=None):
        """求解潮流计算"""
        import time
        start_time = time.time()
        
        # 准备网络数据
        network_data = self._prepare_network_data()
        buses = network_data['buses']
        bus_names = network_data['bus_names']
        generators = network_data['generators']
        loads = network_data['loads']
        lines = network_data['lines']
        
        n_buses = len(buses)
        
        # 识别平衡节点、PQ节点和PV节点
        slack_bus = None
        pv_buses = []
        pq_buses = []
        
        for bus in buses:
            bus_type = self._get_bus_type(bus, generators)
            if bus_type == 'SLACK':
                slack_bus = bus
            elif bus_type == 'PV':
                pv_buses.append(bus)
            elif bus_type == 'PQ':
                pq_buses.append(bus)
        
        if not slack_bus:
            logger.warning("未找到平衡节点，使用第一个母线作为平衡节点")
            slack_bus = buses[0]
        
        # 初始化电压
        V_mag = np.ones(n_buses)
        V_ang = np.zeros(n_buses)
        
        # 计算导纳矩阵
        Y = self._calculate_admittance_matrix(buses, lines)
        
        # 执行牛顿-拉夫逊迭代
        converged = False
        iterations = 0
        error = float('inf')
        
        for iteration in range(self.max_iterations):
            # 计算功率不平衡量
            P_mismatch, Q_mismatch = self._calculate_power_mismatch(
                V_mag, V_ang, Y, buses, generators, loads, slack_bus
            )
            
            # 计算雅可比矩阵
            J = self._calculate_jacobian(
                V_mag, V_ang, Y, buses, slack_bus, pv_buses, pq_buses
            )
            
            # 构建修正方程
            mismatch = []
            for bus in buses:
                if bus != slack_bus:
                    mismatch.append(P_mismatch[bus])
            for bus in pq_buses:
                mismatch.append(Q_mismatch[bus])
            mismatch = np.array(mismatch)
            
            # 检查收敛
            error = np.max(np.abs(mismatch))
            if error < self.tolerance:
                converged = True
                iterations = iteration + 1
                break
            
            # 求解修正方程
            delta = np.linalg.solve(J, -mismatch)
            
            # 应用阻尼因子
            delta *= self.damping_factor
            
            # 更新电压
            delta_idx = 0
            for bus in buses:
                if bus != slack_bus:
                    bus_idx = buses.index(bus)
                    V_ang[bus_idx] += delta[delta_idx]
                    delta_idx += 1
            for bus in pq_buses:
                bus_idx = buses.index(bus)
                V_mag[bus_idx] += delta[delta_idx]
                delta_idx += 1
            
            # 限制电压幅值范围
            V_mag = np.clip(V_mag, 0.5, 1.5)
        
        # 计算最终结果
        voltage_magnitude = pd.DataFrame({
            'v_mag_pu': V_mag
        }, index=bus_names)
        
        voltage_angle = pd.DataFrame({
            'v_ang_deg': np.rad2deg(V_ang)
        }, index=bus_names)
        
        # 计算线路潮流和损耗
        line_flows = self._calculate_line_flows(V_mag, V_ang, Y, buses, lines)
        losses = self._calculate_losses(line_flows)
        
        status = ConvergenceStatus.CONVERGED if converged else ConvergenceStatus.MAX_ITERATIONS_REACHED
        
        result = PowerFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            voltage_magnitude=voltage_magnitude,
            voltage_angle=voltage_angle,
            line_flows=line_flows,
            losses=losses,
            status=status
        )
        
        analysis = PowerFlowAnalysis(result)
        
        return result, analysis
    
    def _prepare_network_data(self):
        """准备网络数据"""
        buses = list(self.network.buses.values())
        bus_names = list(self.network.buses.keys())
        generators = list(self.network.generators.values())
        loads = list(self.network.loads.values())
        lines = list(self.network.lines.values())
        
        return {
            'buses': buses,
            'bus_names': bus_names,
            'generators': generators,
            'loads': loads,
            'lines': lines
        }
    
    def _get_bus_type(self, bus, generators):
        """获取母线类型"""
        # 检查是否为平衡节点
        for gen in generators:
            if gen.bus == bus:
                control_type = gen.parameters.get('control', 'PV').upper()
                return control_type
        
        # 默认是PQ节点
        return 'PQ'
    
    def _calculate_admittance_matrix(self, buses, lines):
        """计算导纳矩阵"""
        n_buses = len(buses)
        Y = np.zeros((n_buses, n_buses), dtype=np.complex128)
        
        for line in lines:
            from_bus = line.from_bus
            to_bus = line.to_bus
            from_idx = buses.index(from_bus)
            to_idx = buses.index(to_bus)
            
            # 获取线路参数
            r = line.parameters.get('resistance', 0.0)
            x = line.parameters.get('reactance', 0.0)
            b = line.parameters.get('susceptance', 0.0)
            
            # 计算线路阻抗和导纳
            z = r + 1j * x
            y = 1.0 / z if z != 0 else 0
            y_shunt = 1j * b
            
            # 更新导纳矩阵
            Y[from_idx, from_idx] += y + y_shunt / 2
            Y[to_idx, to_idx] += y + y_shunt / 2
            Y[from_idx, to_idx] -= y
            Y[to_idx, from_idx] -= y
        
        return Y
    
    def _calculate_power_mismatch(self, V_mag, V_ang, Y, buses, generators, loads, slack_bus):
        """计算功率不平衡量"""
        n_buses = len(buses)
        P_calculated = np.zeros(n_buses)
        Q_calculated = np.zeros(n_buses)
        P_specified = np.zeros(n_buses)
        Q_specified = np.zeros(n_buses)
        
        # 计算指定功率
        for gen in generators:
            bus_idx = buses.index(gen.bus)
            P_specified[bus_idx] += gen.parameters.get('power_set', 0.0)
            Q_specified[bus_idx] += gen.parameters.get('reactive_power_set', 0.0)
        
        for load in loads:
            bus_idx = buses.index(load.bus)
            P_specified[bus_idx] -= load.parameters.get('demand', 0.0)
            Q_specified[bus_idx] -= load.parameters.get('reactive_demand', 0.0)
        
        # 计算实际注入功率
        for i in range(n_buses):
            S_i = 0
            for j in range(n_buses):
                theta_ij = V_ang[i] - V_ang[j]
                Y_ij = Y[i, j]
                G_ij = Y_ij.real
                B_ij = Y_ij.imag
                S_i += V_mag[i] * V_mag[j] * (G_ij + 1j * B_ij) * np.exp(1j * theta_ij)
            P_calculated[i] = S_i.real
            Q_calculated[i] = S_i.imag
        
        # 计算不平衡量
        P_mismatch = {}
        Q_mismatch = {}
        for bus in buses:
            bus_idx = buses.index(bus)
            P_mismatch[bus] = P_specified[bus_idx] - P_calculated[bus_idx]
            Q_mismatch[bus] = Q_specified[bus_idx] - Q_calculated[bus_idx]
        
        # 平衡节点的不平衡量设为0
        P_mismatch[slack_bus] = 0.0
        Q_mismatch[slack_bus] = 0.0
        
        return P_mismatch, Q_mismatch
    
    def _calculate_jacobian(self, V_mag, V_ang, Y, buses, slack_bus, pv_buses, pq_buses):
        """计算雅可比矩阵"""
        n_buses = len(buses)
        n_pv = len(pv_buses)
        n_pq = len(pq_buses)
        n_vars = (n_buses - 1) + n_pq
        
        J = np.zeros((n_vars, n_vars))
        
        # 构建行索引映射
        row_map = {}
        row_idx = 0
        for bus in buses:
            if bus != slack_bus:
                row_map[('P', bus)] = row_idx
                row_idx += 1
        for bus in pq_buses:
            row_map[('Q', bus)] = row_idx
            row_idx += 1
        
        # 构建列索引映射
        col_map = {}
        col_idx = 0
        for bus in buses:
            if bus != slack_bus:
                col_map[('theta', bus)] = col_idx
                col_idx += 1
        for bus in pq_buses:
            col_map[('V', bus)] = col_idx
            col_idx += 1
        
        # 计算雅可比矩阵元素
        for bus_i in buses:
            i = buses.index(bus_i)
            if bus_i != slack_bus:
                # 计算dP_i/dtheta_j
                for bus_j in buses:
                    j = buses.index(bus_j)
                    if bus_j != slack_bus:
                        if i == j:
                            # 对角线元素
                            sum_val = 0
                            for k in range(n_buses):
                                if k != i:
                                    theta_ik = V_ang[i] - V_ang[k]
                                    Y_ik = Y[i, k]
                                    G_ik = Y_ik.real
                                    B_ik = Y_ik.imag
                                    sum_val += V_mag[i] * V_mag[k] * (G_ik * np.sin(theta_ik) - B_ik * np.cos(theta_ik))
                            J[row_map[('P', bus_i)], col_map[('theta', bus_j)]] = -sum_val
                        else:
                            # 非对角线元素
                            theta_ij = V_ang[i] - V_ang[j]
                            Y_ij = Y[i, j]
                            G_ij = Y_ij.real
                            B_ij = Y_ij.imag
                            J[row_map[('P', bus_i)], col_map[('theta', bus_j)]] = V_mag[i] * V_mag[j] * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))
                
                # 计算dP_i/dV_j
                for bus_j in pq_buses:
                    j = buses.index(bus_j)
                    if i == j:
                        # 对角线元素
                        sum_val = 0
                        for k in range(n_buses):
                            theta_ik = V_ang[i] - V_ang[k]
                            Y_ik = Y[i, k]
                            G_ik = Y_ik.real
                            B_ik = Y_ik.imag
                            sum_val += V_mag[k] * (G_ik * np.cos(theta_ik) + B_ik * np.sin(theta_ik))
                        J[row_map[('P', bus_i)], col_map[('V', bus_j)]] = V_mag[i] * Y[i, i].real + sum_val
                    else:
                        # 非对角线元素
                        theta_ij = V_ang[i] - V_ang[j]
                        Y_ij = Y[i, j]
                        G_ij = Y_ij.real
                        B_ij = Y_ij.imag
                        J[row_map[('P', bus_i)], col_map[('V', bus_j)]] = V_mag[i] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
            
            # 计算dQ_i/dtheta_j 和 dQ_i/dV_j（仅PQ节点）
            if bus_i in pq_buses:
                # 计算dQ_i/dtheta_j
                for bus_j in buses:
                    j = buses.index(bus_j)
                    if bus_j != slack_bus:
                        if i == j:
                            # 对角线元素
                            sum_val = 0
                            for k in range(n_buses):
                                if k != i:
                                    theta_ik = V_ang[i] - V_ang[k]
                                    Y_ik = Y[i, k]
                                    G_ik = Y_ik.real
                                    B_ik = Y_ik.imag
                                    sum_val += V_mag[i] * V_mag[k] * (G_ik * np.cos(theta_ik) + B_ik * np.sin(theta_ik))
                            J[row_map[('Q', bus_i)], col_map[('theta', bus_j)]] = sum_val
                        else:
                            # 非对角线元素
                            theta_ij = V_ang[i] - V_ang[j]
                            Y_ij = Y[i, j]
                            G_ij = Y_ij.real
                            B_ij = Y_ij.imag
                            J[row_map[('Q', bus_i)], col_map[('theta', bus_j)]] = -V_mag[i] * V_mag[j] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                
                # 计算dQ_i/dV_j
                for bus_j in pq_buses:
                    j = buses.index(bus_j)
                    if i == j:
                        # 对角线元素
                        sum_val = 0
                        for k in range(n_buses):
                            theta_ik = V_ang[i] - V_ang[k]
                            Y_ik = Y[i, k]
                            G_ik = Y_ik.real
                            B_ik = Y_ik.imag
                            sum_val += V_mag[k] * (G_ik * np.sin(theta_ik) - B_ik * np.cos(theta_ik))
                        J[row_map[('Q', bus_i)], col_map[('V', bus_j)]] = V_mag[i] * Y[i, i].imag + sum_val
                    else:
                        # 非对角线元素
                        theta_ij = V_ang[i] - V_ang[j]
                        Y_ij = Y[i, j]
                        G_ij = Y_ij.real
                        B_ij = Y_ij.imag
                        J[row_map[('Q', bus_i)], col_map[('V', bus_j)]] = V_mag[i] * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))
        
        return J
    
    def _calculate_line_flows(self, V_mag, V_ang, Y, buses, lines):
        """计算线路潮流"""
        line_flows = {}
        
        for line in lines:
            from_bus = line.from_bus
            to_bus = line.to_bus
            from_idx = buses.index(from_bus)
            to_idx = buses.index(to_bus)
            
            # 计算线路始端和末端的电压
            V_from = V_mag[from_idx] * np.exp(1j * V_ang[from_idx])
            V_to = V_mag[to_idx] * np.exp(1j * V_ang[to_idx])
            
            # 获取线路参数
            r = line.parameters.get('resistance', 0.0)
            x = line.parameters.get('reactance', 0.0)
            b = line.parameters.get('susceptance', 0.0)
            
            # 计算线路阻抗和导纳
            z = r + 1j * x
            y = 1.0 / z if z != 0 else 0
            y_shunt = 1j * b
            
            # 计算线路潮流
            I_from = (V_from - V_to) * y + V_from * y_shunt / 2
            I_to = (V_to - V_from) * y + V_to * y_shunt / 2
            
            S_from = V_from * np.conj(I_from)
            S_to = V_to * np.conj(I_to)
            
            line_flows[line.name] = {
                'from_bus': from_bus.name,
                'to_bus': to_bus.name,
                'P_from': S_from.real,
                'Q_from': S_from.imag,
                'P_to': S_to.real,
                'Q_to': S_to.imag,
                'loss_P': S_from.real + S_to.real,
                'loss_Q': S_from.imag + S_to.imag
            }
        
        return line_flows
    
    def _calculate_losses(self, line_flows):
        """计算总损耗"""
        total_real_loss = 0
        total_reactive_loss = 0
        
        for line_name, flow in line_flows.items():
            total_real_loss += flow['loss_P']
            total_reactive_loss += flow['loss_Q']
        
        return {
            'p': total_real_loss,
            'q': total_reactive_loss
        }


def run_power_flow_analysis(network, method=PowerFlowMethod.NEWTON_RAPHSON, **kwargs):
    """运行潮流计算分析"""
    if method == PowerFlowMethod.NEWTON_RAPHSON:
        solver = NewtonRaphsonPowerFlow(network)
    else:
        raise NotImplementedError(f"不支持的潮流计算方法: {method}")
    
    result, analysis = solver.solve()
    return result, analysis
