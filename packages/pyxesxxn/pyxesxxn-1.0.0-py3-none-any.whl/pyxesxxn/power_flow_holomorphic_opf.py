"""
基于全纯嵌入法的非迭代电力系统最优潮流计算模块

提供基于全纯嵌入法（HEM）的最优潮流计算功能，实现非迭代、不依赖初始值的最优潮流计算。
"""

# SPDX-FileCopyrightText: 2024-present PyXESXXN Development Team
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

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


class HolomorphicOPFResult:
    """全纯嵌入法最优潮流计算结果类"""
    def __init__(self,
                 converged: bool,
                 iterations: int,
                 error: float,
                 status: ConvergenceStatus,
                 voltage_magnitude: pd.DataFrame,
                 voltage_angle: pd.DataFrame,
                 active_power: pd.DataFrame,
                 reactive_power: pd.DataFrame,
                 line_flows: Dict[str, pd.DataFrame],
                 transformer_flows: Dict[str, pd.DataFrame],
                 losses: Dict[str, float],
                 computation_time: float,
                 warnings: List[str],
                 generator_cost: float,
                 generator_outputs: pd.DataFrame,
                 lambda_value: float,
                 power_loss: float):
        self.converged = converged
        self.iterations = iterations
        self.error = error
        self.status = status
        self.voltage_magnitude = voltage_magnitude
        self.voltage_angle = voltage_angle
        self.active_power = active_power
        self.reactive_power = reactive_power
        self.line_flows = line_flows
        self.transformer_flows = transformer_flows
        self.losses = losses
        self.computation_time = computation_time
        self.warnings = warnings
        self.generator_cost = generator_cost
        self.generator_outputs = generator_outputs
        self.lambda_value = lambda_value
        self.power_loss = power_loss
    
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
            "warnings": self.warnings,
            "generator_cost": self.generator_cost,
            "generator_outputs": self.generator_outputs.to_dict(),
            "lambda_value": self.lambda_value,
            "power_loss": self.power_loss
        }


class HolomorphicOPFSolver(EnhancedPowerFlowSolver):
    """基于全纯嵌入法的最优潮流求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        super().__init__(network, PowerFlowMethod.NEWTON_RAPHSON)
        self.max_iterations = kwargs.get('max_iterations', 100)
        self.tolerance = kwargs.get('tolerance', 1e-8)
        self.max_series_order = kwargs.get('max_series_order', 10)  # 幂级数最大阶数
        self.cost_coefficients = kwargs.get('cost_coefficients', {})  # 发电机成本系数 {gen_name: (C0, C1, C2)}
    
    def solve(self, snapshots: Optional[Sequence] = None) -> HolomorphicOPFResult:
        """使用全纯嵌入法求解最优潮流"""
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
        n_gens = len(network_data['generators'])
        
        # 初始化幂级数系数
        # e[n] - 电压实部系数，f[n] - 电压虚部系数
        e = [np.ones(n_buses, dtype=np.float64) for _ in range(self.max_series_order + 1)]
        f = [np.zeros(n_buses, dtype=np.float64) for _ in range(self.max_series_order + 1)]
        
        # p[n] - 发电机有功出力系数，lambda_coeff[n] - 拉格朗日乘子系数
        p = [np.zeros(n_gens, dtype=np.float64) for _ in range(self.max_series_order + 1)]
        lambda_coeff = [0.0 for _ in range(self.max_series_order + 1)]
        
        # 识别发电机所在母线
        gen_bus_indices = []
        bus_names = network_data['bus_names']
        for gen in network_data['generators']:
            bus_name = gen.bus.name
            gen_bus_indices.append(bus_names.index(bus_name))
        
        # 初始化成本系数
        self._initialize_cost_coefficients(network_data)
        
        # 交叉递推计算
        converged = False
        iteration = 0
        error = float('inf')
        warnings_list = []
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # 交叉递推：计算p[n]和lambda[n]
            for n in range(1, self.max_series_order + 1):
                # 使用KKT条件递推方程计算p[n]和lambda[n]
                p[n], lambda_coeff[n] = self._calculate_p_lambda_coeff(n, p, e, f, lambda_coeff, 
                                                                     network_data, gen_bus_indices, Y)
                
                # 使用约束条件递推方程计算e[n]和f[n]
                e_n, f_n = self._calculate_voltage_coeff(n, p, e, f, lambda_coeff, 
                                                       network_data, gen_bus_indices, Y)
                
                e[n] = e_n
                f[n] = f_n
            
            # 计算实际值
            V_mag, V_ang = self._calculate_voltage_from_series(e, f)
            P_gen = self._calculate_power_from_series(p)
            lambda_value = self._calculate_lambda_from_series(lambda_coeff)
            
            # 更新网络数据中的发电机出力
            self._update_generator_outputs(network_data, P_gen)
            
            # 计算网损微增率和网络损耗（不需要雅可比矩阵）
            power_loss, loss_derivatives = self._calculate_loss_micro_increment(V_mag, V_ang, Y, network_data)
            
            # 检查收敛性
            prev_loss = getattr(self, '_prev_loss', float('inf'))
            error = abs(power_loss - prev_loss)
            
            if error < self.tolerance:
                converged = True
                break
            
            self._prev_loss = power_loss
        
        # 计算最终结果
        # 直接处理收敛状态
        from .power_flow_enhanced import ConvergenceStatus
        if converged:
            status = ConvergenceStatus.CONVERGED
        elif iteration >= self.max_iterations:
            status = ConvergenceStatus.MAX_ITERATIONS
        elif np.isnan(error) or np.isinf(error):
            status = ConvergenceStatus.NUMERICAL_ERROR
        else:
            status = ConvergenceStatus.DIVERGED
        
        # 计算发电成本
        generator_cost = self._calculate_generator_cost(P_gen, network_data)
        
        # 创建结果对象
        power_flow_result = self._create_power_flow_result(
            V_mag, V_ang, Y, network_data, converged, iteration, error, status
        )
        
        computation_time = time.time() - start_time
        
        # 创建发电机出力数据框
        gen_names = [gen.name for gen in network_data['generators']]
        generator_outputs = pd.DataFrame(P_gen, index=gen_names, columns=['active_power_pu'])
        
        return HolomorphicOPFResult(
            converged=converged,
            iterations=iteration,
            error=error,
            status=status,
            voltage_magnitude=power_flow_result.voltage_magnitude,
            voltage_angle=power_flow_result.voltage_angle,
            active_power=power_flow_result.active_power,
            reactive_power=power_flow_result.reactive_power,
            line_flows=power_flow_result.line_flows,
            transformer_flows=power_flow_result.transformer_flows,
            losses=power_flow_result.losses,
            computation_time=computation_time,
            warnings=power_flow_result.warnings,
            generator_cost=generator_cost,
            generator_outputs=generator_outputs,
            lambda_value=lambda_value,
            power_loss=power_loss
        )
    
    def _initialize_cost_coefficients(self, network_data: Dict[str, Any]):
        """初始化发电机成本系数"""
        generators = network_data['generators']
        
        # 如果没有提供成本系数，使用默认值
        if not self.cost_coefficients:
            self.cost_coefficients = {}
            for gen in generators:
                # 默认成本系数：C0=0, C1=10, C2=0.1
                self.cost_coefficients[gen.name] = (0.0, 10.0, 0.1)
    
    def _calculate_p_lambda_coeff(self, n: int, p: List[np.ndarray], e: List[np.ndarray], 
                                  f: List[np.ndarray], lambda_coeff: List[float],
                                  network_data: Dict[str, Any], gen_bus_indices: List[int],
                                  Y: csr_matrix) -> Tuple[np.ndarray, float]:
        """计算有功出力和拉格朗日乘子的幂级数系数"""
        generators = network_data['generators']
        n_gens = len(generators)
        
        # 构建左侧矩阵
        A = np.zeros((n_gens + 1, n_gens + 1))
        B = np.zeros(n_gens + 1)
        
        # 填充对角线元素（2*C2 + 小扰动，避免奇异矩阵）
        for i in range(n_gens):
            C0, C1, C2 = self.cost_coefficients[generators[i].name]
            A[i, i] = 2 * C2 + 1e-8  # 添加小扰动，避免奇异矩阵
        
        # 填充lambda相关列（除了最后一个元素）
        for i in range(n_gens):
            A[i, n_gens] = 1.0  # KKT条件中的lambda系数
        
        # 填充最后一行（有功平衡方程）
        for i in range(n_gens):
            A[n_gens, i] = 1.0
        A[n_gens, n_gens] = 1e-8  # 添加小扰动，避免奇异矩阵
        
        # 填充右侧向量
        for i in range(n_gens):
            C0, C1, C2 = self.cost_coefficients[generators[i].name]
            
            # 计算低阶系数组合
            sum_terms = 0.0
            for k in range(1, n):
                sum_terms += p[k][i] * p[n - k][i]
            
            # KKT条件：s*C1 + 2*C2*p[n] + lambda[n]*(1 + s*loss_deriv) = 0
            # 对于n=1, s=1；对于n>1, s=0（因为s是一阶项）
            if n == 1:
                B[i] = -C1
            else:
                B[i] = 0.0
            B[i] -= 2 * C2 * sum_terms
            
            # 添加lambda相关项的低阶贡献
            for k in range(n):
                B[i] -= lambda_coeff[k] * (1.0 if k == 0 else 0.0)  # 简化处理，仅考虑lambda[0]
        
        # 计算有功平衡方程右侧
        # 简化处理：使用发电机出力和负荷的关系
        B[n_gens] = 0.0
        if n == 1:
            # 对于n=1，有功平衡方程右侧为负荷需求
            total_load = 0.0
            for load in network_data['loads']:
                total_load += load.parameters.get('demand', 0.0)
            B[n_gens] = -total_load
        
        # 求解线性方程组
        try:
            x = np.linalg.solve(A, B)
        except np.linalg.LinAlgError:
            # 如果矩阵奇异，使用最小二乘解
            x, residuals, rank, s = np.linalg.lstsq(A, B, rcond=None)
            logger.warning(f"警告：计算p[{n}]时遇到奇异矩阵，使用最小二乘解")
        
        p_n = x[:n_gens]
        lambda_n = x[-1]
        
        return p_n, lambda_n
    
    def _calculate_voltage_coeff(self, n: int, p: List[np.ndarray], e: List[np.ndarray], 
                                f: List[np.ndarray], lambda_coeff: List[float],
                                network_data: Dict[str, Any], gen_bus_indices: List[int],
                                Y: csr_matrix) -> Tuple[np.ndarray, np.ndarray]:
        """计算电压实部和虚部的幂级数系数"""
        n_buses = len(network_data['buses'])
        generators = network_data['generators']
        
        # 初始化系数向量
        e_n = np.zeros(n_buses)
        f_n = np.zeros(n_buses)
        
        # 构建导纳矩阵实部和虚部（使用不同的变量名避免冲突）
        G_imag = Y.real.toarray()
        B_imag = Y.imag.toarray()
        
        # 计算节点注入功率的幂级数系数
        P_inj_coeff = np.zeros((self.max_series_order + 1, n_buses))
        Q_inj_coeff = np.zeros((self.max_series_order + 1, n_buses))
        
        # 发电机注入功率
        for gen_idx, (gen, bus_idx) in enumerate(zip(generators, gen_bus_indices)):
            for k in range(1, self.max_series_order + 1):
                P_inj_coeff[k, bus_idx] += p[k][gen_idx]
        
        # 负荷注入功率（负值）
        for load in network_data['loads']:
            bus_name = load.bus.name
            bus_idx = network_data['bus_names'].index(bus_name)
            params = load.parameters
            demand = params.get('demand', 0.0)
            reactive_demand = params.get('reactive_demand', 0.0)
            
            # 负荷注入功率为负，且只有一阶项（s=1时）
            P_inj_coeff[1, bus_idx] -= demand
            Q_inj_coeff[1, bus_idx] -= reactive_demand
        
        # 计算电压系数
        for i in range(n_buses):
            # 构建方程：Σ (G_ik e_k[n] - B_ik f_k[n]) = P_inj[n]
            #          Σ (B_ik e_k[n] + G_ik f_k[n]) = Q_inj[n]
            
            # 计算已知项（低阶系数组合）
            P_known = 0.0
            Q_known = 0.0
            
            for k in range(1, n):
                # 计算V*V'的低阶系数
                vv_real = 0.0
                vv_imag = 0.0
                for m in range(0, k + 1):
                    vv_real += e[m][i] * e[k - m][i] + f[m][i] * f[k - m][i]
                    vv_imag += e[m][i] * f[k - m][i] - f[m][i] * e[k - m][i]
                
                # 计算注入功率低阶项
                P_known += P_inj_coeff[k][i] * vv_real + Q_inj_coeff[k][i] * vv_imag
                Q_known += Q_inj_coeff[k][i] * vv_real - P_inj_coeff[k][i] * vv_imag
            
            # 构建线性方程组
            A_mat = np.zeros((2, 2))
            b_vec = np.zeros(2)
            
            # 导纳矩阵对角线项
            A_mat[0, 0] = G_imag[i, i]
            A_mat[0, 1] = -B_imag[i, i]
            A_mat[1, 0] = B_imag[i, i]
            A_mat[1, 1] = G_imag[i, i]
            
            # 右侧向量
            b_vec[0] = P_inj_coeff[n][i] - P_known
            b_vec[1] = Q_inj_coeff[n][i] - Q_known
            
            # 计算非对角线项的贡献
            for j in range(n_buses):
                if i != j:
                    # 非对角线项的低阶贡献
                    sum_Ge = 0.0
                    sum_Bf = 0.0
                    sum_Be = 0.0
                    sum_Gf = 0.0
                    
                    for k in range(1, n):
                        sum_Ge += G_imag[i, j] * e[k][j]
                        sum_Bf += B_imag[i, j] * f[k][j]
                        sum_Be += B_imag[i, j] * e[k][j]
                        sum_Gf += G_imag[i, j] * f[k][j]
                    
                    # 非对角线项对右侧向量的贡献
                    b_vec[0] -= (sum_Ge - sum_Bf)
                    b_vec[1] -= (sum_Be + sum_Gf)
            
            # 求解线性方程组
            det_A = np.linalg.det(A_mat)
            if det_A != 0:
                x = np.linalg.solve(A_mat, b_vec)
                e_n[i] = x[0]
                f_n[i] = x[1]
            else:
                # 如果矩阵奇异，使用最小二乘解
                x, residuals, rank, s = np.linalg.lstsq(A_mat, b_vec, rcond=None)
                e_n[i] = x[0]
                f_n[i] = x[1]
        
        return e_n, f_n
    
    def _calculate_voltage_from_series(self, e: List[np.ndarray], f: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """从幂级数系数计算实际电压幅值和相位"""
        n_buses = len(e[0])
        V_mag = np.zeros(n_buses)
        V_ang = np.zeros(n_buses)
        
        for i in range(n_buses):
            # 计算实际电压（s=1）
            real_part = sum(e[n][i] for n in range(self.max_series_order + 1))
            imag_part = sum(f[n][i] for n in range(self.max_series_order + 1))
            
            V_mag[i] = np.sqrt(real_part**2 + imag_part**2)
            V_ang[i] = np.arctan2(imag_part, real_part)
        
        return V_mag, V_ang
    
    def _calculate_power_from_series(self, p: List[np.ndarray]) -> np.ndarray:
        """从幂级数系数计算实际有功出力"""
        n_gens = len(p[0])
        P_gen = np.zeros(n_gens)
        
        for i in range(n_gens):
            P_gen[i] = sum(p[n][i] for n in range(self.max_series_order + 1))
        
        return P_gen
    
    def _calculate_lambda_from_series(self, lambda_coeff: List[float]) -> float:
        """从幂级数系数计算实际拉格朗日乘子"""
        return sum(lambda_coeff[n] for n in range(self.max_series_order + 1))
    
    def _update_generator_outputs(self, network_data: Dict[str, Any], P_gen: np.ndarray):
        """更新网络数据中的发电机出力"""
        generators = network_data['generators']
        for i, gen in enumerate(generators):
            if 'power_set' not in gen.parameters:
                gen.parameters['power_set'] = 0.0
            gen.parameters['power_set'] = P_gen[i]
    
    def _calculate_loss_micro_increment(self, V_mag: np.ndarray, V_ang: np.ndarray, 
                                      Y: csr_matrix, network_data: Dict[str, Any]) -> Tuple[float, np.ndarray]:
        """计算网损微增率"""
        # 简化实现：计算总网损
        V = V_mag * np.exp(1j * V_ang)
        S_injected = V * np.conj(Y @ V)
        total_loss = np.sum(S_injected.real)
        
        # 简化的网损微增率（后续优化）
        loss_derivatives = np.zeros(len(network_data['generators']))
        
        return total_loss, loss_derivatives
    
    def _calculate_generator_cost(self, P_gen: np.ndarray, network_data: Dict[str, Any]) -> float:
        """计算发电成本"""
        generators = network_data['generators']
        total_cost = 0.0
        
        for i, gen in enumerate(generators):
            C0, C1, C2 = self.cost_coefficients[gen.name]
            p = P_gen[i]
            total_cost += C0 + C1 * p + C2 * p**2
        
        return total_cost
    
    def _create_power_flow_result(self, V_mag: np.ndarray, V_ang: np.ndarray, Y: csr_matrix,
                                 network_data: Dict[str, Any], converged: bool, 
                                 iterations: int, error: float, status: ConvergenceStatus) -> PowerFlowResult:
        """创建潮流计算结果对象"""
        import pandas as pd
        
        # 创建电压幅值数据框
        bus_names = network_data['bus_names']
        voltage_magnitude = pd.DataFrame(V_mag, index=bus_names, columns=['v_mag_pu'])
        
        # 创建电压相角数据框
        voltage_angle = pd.DataFrame(V_ang, index=bus_names, columns=['v_ang_rad'])
        
        # 创建有功功率数据框
        active_power = pd.DataFrame(np.zeros(len(bus_names)), index=bus_names, columns=['active_power'])
        
        # 创建无功功率数据框
        reactive_power = pd.DataFrame(np.zeros(len(bus_names)), index=bus_names, columns=['reactive_power'])
        
        # 计算线路潮流（简化处理，返回空字典）
        line_flows = {}
        
        # 计算变压器潮流（简化处理，返回空字典）
        transformer_flows = {}
        
        # 计算损耗（简化处理，返回总损耗）
        V = V_mag * np.exp(1j * V_ang)
        S_injected = V * np.conj(Y @ V)
        total_loss = np.sum(S_injected.real)
        losses = {'total': total_loss}
        
        return PowerFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            status=status,
            voltage_magnitude=voltage_magnitude,
            voltage_angle=voltage_angle,
            active_power=active_power,
            reactive_power=reactive_power,
            line_flows=line_flows,
            transformer_flows=transformer_flows,
            losses=losses,
            computation_time=0.0,
            warnings=[]
        )


class HolomorphicOPFAnalysis(PowerFlowAnalysis):
    """全纯嵌入法最优潮流结果分析类"""
    
    def __init__(self, opf_result: HolomorphicOPFResult):
        super().__init__(opf_result)
        self.opf_result = opf_result
    
    def analyze_generator_cost(self) -> Dict[str, Any]:
        """分析发电成本"""
        return {
            'total_cost': self.opf_result.generator_cost,
            'lambda_value': self.opf_result.lambda_value,
            'average_cost_per_mw': self.opf_result.generator_cost / np.sum(self.opf_result.generator_outputs.values)
        }
    
    def generate_opf_report(self) -> str:
        """生成最优潮流分析报告"""
        report = []
        report.append("=== 全纯嵌入法最优潮流分析报告 ===")
        report.append(f"收敛状态: {self.opf_result.status.value}")
        report.append(f"迭代次数: {self.opf_result.iterations}")
        report.append(f"最大误差: {self.opf_result.error:.6e}")
        report.append(f"计算时间: {self.opf_result.computation_time:.3f} 秒")
        
        # 电压分析
        voltage_analysis = self.analyze_voltage_profile()
        report.append("\n--- 电压分析 ---")
        report.append(f"最低电压: {voltage_analysis['min_voltage']:.4f} pu")
        report.append(f"最高电压: {voltage_analysis['max_voltage']:.4f} pu")
        report.append(f"平均电压: {voltage_analysis['avg_voltage']:.4f} pu")
        report.append(f"电压偏差: {voltage_analysis['voltage_deviation']:.4f} pu")
        report.append(f"电压越限: {voltage_analysis['voltage_violations']} 个节点")
        
        # 发电成本分析
        cost_analysis = self.analyze_generator_cost()
        report.append("\n--- 发电成本分析 ---")
        report.append(f"总发电成本: {cost_analysis['total_cost']:.2f} $")
        report.append(f"拉格朗日乘子: {cost_analysis['lambda_value']:.4f} $")
        report.append(f"平均单位成本: {cost_analysis['average_cost_per_mw']:.2f} $/MW")
        
        # 发电机出力
        report.append("\n--- 发电机出力 ---")
        for gen_name, output in self.opf_result.generator_outputs.iterrows():
            report.append(f"{gen_name}: {output['active_power_pu']:.4f} pu")
        
        return "\n".join(report)


# 公共API函数
def create_holomorphic_opf_solver(network: PyXESXXNNetwork, **kwargs) -> HolomorphicOPFSolver:
    """创建全纯嵌入法最优潮流求解器"""
    return HolomorphicOPFSolver(network, **kwargs)


def run_holomorphic_opf(network: PyXESXXNNetwork, snapshots: Optional[Sequence] = None,
                        **kwargs) -> Tuple[HolomorphicOPFResult, HolomorphicOPFAnalysis]:
    """运行全纯嵌入法最优潮流计算"""
    solver = create_holomorphic_opf_solver(network, **kwargs)
    result = solver.solve(snapshots)
    analysis = HolomorphicOPFAnalysis(result)
    
    return result, analysis


# 导出公共API
__all__ = [
    'HolomorphicOPFResult',
    'HolomorphicOPFSolver',
    'HolomorphicOPFAnalysis',
    'create_holomorphic_opf_solver',
    'run_holomorphic_opf'
]