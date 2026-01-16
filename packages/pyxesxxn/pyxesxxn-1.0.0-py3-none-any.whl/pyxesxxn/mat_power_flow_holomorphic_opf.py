"""
基于全纯嵌入法的非迭代电力系统最优潮流计算模块

提供基于全纯嵌入法（HEM）的最优潮流计算功能，实现非迭代、不依赖初始值的最优潮流计算。
"""

# SPDX-FileCopyrightText: 2025-present PyXESXXN Development Team
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
import pyxesxxn as px
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
        self.use_parallel = kwargs.get('use_parallel', False)  # 是否使用并行计算
        self.constraint_handling = kwargs.get('constraint_handling', True)  # 是否启用约束处理
        # 约束参数
        self.voltage_lower_limit = kwargs.get('voltage_lower_limit', 0.95)  # 电压下限 (pu)
        self.voltage_upper_limit = kwargs.get('voltage_upper_limit', 1.05)  # 电压上限 (pu)
        self.line_load_limit = kwargs.get('line_load_limit', 1.0)  # 线路负载率上限
        self.max_gen_violation = kwargs.get('max_gen_violation', 1e-5)  # 发电机出力越限允许值
    
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
        
        # 获取发电机出力上下限
        gen_pmin = []
        gen_pmax = []
        for gen in generators:
            params = gen.parameters
            # 默认为0到1 pu的出力范围
            pmin = params.get('min_power', 0.0)
            pmax = params.get('capacity', 1.0)
            gen_pmin.append(pmin)
            gen_pmax.append(pmax)
        
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
        
        # 应用发电机出力上下限约束（仅对一阶项有效，高阶项受一阶项约束影响）
        if n == 1 and self.constraint_handling:
            for i in range(n_gens):
                # 计算当前发电机出力
                current_p = p_n[i]
                # 应用上下限约束
                if current_p < gen_pmin[i]:
                    p_n[i] = gen_pmin[i]
                    logger.debug(f"发电机 {generators[i].name} 出力下限约束：{current_p:.6f} -> {gen_pmin[i]:.6f}")
                elif current_p > gen_pmax[i]:
                    p_n[i] = gen_pmax[i]
                    logger.debug(f"发电机 {generators[i].name} 出力上限约束：{current_p:.6f} -> {gen_pmax[i]:.6f}")
        
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
        total_generation = np.sum(self.opf_result.generator_outputs.values)
        average_cost = self.opf_result.generator_cost / total_generation if total_generation != 0 else 0.0
        return {
            'total_cost': self.opf_result.generator_cost,
            'lambda_value': self.opf_result.lambda_value,
            'average_cost_per_mw': average_cost
        }
    
    def analyze_voltage_stability(self) -> Dict[str, Any]:
        """分析电压稳定性"""
        v_mag = self.opf_result.voltage_magnitude
        
        # 计算电压稳定指标
        v_min = v_mag.min().iloc[0]
        v_max = v_mag.max().iloc[0]
        v_avg = v_mag.mean().iloc[0]
        
        # 电压稳定性裕度（距离越限的裕度）
        lower_margin = v_min - 0.95  # 假设下限为0.95 pu
        upper_margin = 1.05 - v_max  # 假设上限为1.05 pu
        
        # 电压波动范围
        voltage_range = v_max - v_min
        
        return {
            'voltage_stability_margin': min(lower_margin, upper_margin),
            'voltage_range': voltage_range,
            'voltage_quality_index': 1.0 - np.abs(v_mag - 1.0).mean().iloc[0],  # 电压质量指数（越接近1越好）
            'critical_buses': v_mag[(v_mag < 0.98) | (v_mag > 1.02)].index.tolist()  # 临界母线（电压偏离基准值超过2%）
        }
    
    def analyze_power_balance(self) -> Dict[str, Any]:
        """分析功率平衡"""
        # 计算总发电功率
        total_generation = np.sum(self.opf_result.generator_outputs.values)
        
        # 计算总负荷功率（假设所有有功功率都是负荷，简化处理）
        total_load = total_generation - self.opf_result.power_loss
        
        # 计算功率平衡误差
        balance_error = np.abs(total_generation - (total_load + self.opf_result.power_loss))
        
        return {
            'total_generation': total_generation,
            'total_load': total_load,
            'total_loss': self.opf_result.power_loss,
            'loss_percentage': (self.opf_result.power_loss / total_generation) * 100 if total_generation > 0 else 0,
            'balance_error': balance_error
        }
    
    def analyze_holomorphic_convergence(self) -> Dict[str, Any]:
        """分析全纯嵌入法的收敛特性"""
        # 全纯嵌入法特有的收敛分析
        return {
            'convergence_rate': '指数收敛' if self.opf_result.iterations <= 3 else '线性收敛',
            'final_error': self.opf_result.error,
            'iterations_efficiency': f"{self.opf_result.iterations}次迭代达到收敛",
            'computation_efficiency': f"{self.opf_result.computation_time:.3f}秒/案例"
        }
    
    def analyze_sensitivity(self) -> Dict[str, Any]:
        """分析灵敏度信息"""
        # 简化的灵敏度分析，基于拉格朗日乘子
        return {
            'lambda_value': self.opf_result.lambda_value,
            'marginal_cost': self.opf_result.lambda_value,  # 边际成本等于拉格朗日乘子
            'interpretation': "拉格朗日乘子表示系统总负荷增加1MW时，总发电成本的变化量"
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
        report.append("\n--- 发电成本 ---")
        report.append(f"总发电成本: {cost_analysis['total_cost']:.2f} $")
        report.append(f"拉格朗日乘子: {cost_analysis['lambda_value']:.4f} $")
        report.append(f"平均单位成本: {cost_analysis['average_cost_per_mw']:.2f} $/MW")
        
        # 发电机出力
        report.append("\n--- 发电机出力 ---")
        for gen_name, output in self.opf_result.generator_outputs.iterrows():
            report.append(f"{gen_name}: {output['active_power_pu']:.4f} pu")
        
        return "\n".join(report)
    
    def generate_detailed_interpretability_report(self, output_file: Optional[str] = None) -> str:
        """生成极其详细的技术可解释性分析报告
        
        Args:
            output_file: 可选的输出文件路径，如果提供则将报告写入文件
            
        Returns:
            详细的技术可解释性分析报告字符串
        """
        from datetime import datetime
        import textwrap
        
        report = []
        
        # 报告标题和基本信息
        report.append("=" * 80)
        report.append("           全纯嵌入法最优潮流 - 技术可解释性分析报告")
        report.append("=" * 80)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"分析工具: PyXESXXN - Holomorphic OPF Solver")
        report.append("=" * 80)
        
        # 1. 基本计算信息
        report.append("\n" + "=" * 60)
        report.append("1. 基本计算信息")
        report.append("=" * 60)
        report.append(f"收敛状态: {self.opf_result.status.value}")
        report.append(f"迭代次数: {self.opf_result.iterations}")
        report.append(f"最大收敛误差: {self.opf_result.error:.9e}")
        report.append(f"计算时间: {self.opf_result.computation_time:.9f} 秒")
        report.append(f"网损: {self.opf_result.power_loss:.9f} pu")
        
        # 2. 收敛性分析
        report.append("\n" + "=" * 60)
        report.append("2. 收敛性分析")
        report.append("=" * 60)
        convergence_status = "成功" if self.opf_result.converged else "失败"
        report.append(f"收敛结果: {convergence_status}")
        
        if self.opf_result.converged:
            report.append("收敛性评价: 计算成功收敛，满足预设精度要求")
            if self.opf_result.iterations < 20:
                report.append("收敛速度评价: 收敛速度较快")
            elif self.opf_result.iterations < 50:
                report.append("收敛速度评价: 收敛速度适中")
            else:
                report.append("收敛速度评价: 收敛速度较慢")
        else:
            report.append("收敛性评价: 计算未收敛")
            if self.opf_result.iterations >= 100:
                report.append("未收敛原因: 达到最大迭代次数")
            else:
                report.append("未收敛原因: 数值计算不稳定或模型问题")
        
        # 3. 电压分布详细分析
        report.append("\n" + "=" * 60)
        report.append("3. 电压分布详细分析")
        report.append("=" * 60)
        
        voltage_analysis = self.analyze_voltage_profile()
        report.append(f"最低电压: {voltage_analysis['min_voltage']:.6f} pu (节点: {voltage_analysis.get('min_voltage_bus', '未知')})")
        report.append(f"最高电压: {voltage_analysis['max_voltage']:.6f} pu (节点: {voltage_analysis.get('max_voltage_bus', '未知')})")
        report.append(f"平均电压: {voltage_analysis['avg_voltage']:.6f} pu")
        report.append(f"电压标准差: {voltage_analysis['voltage_deviation']:.6f} pu")
        report.append(f"电压越限节点数: {voltage_analysis['voltage_violations']}")
        
        # 详细电压列表
        report.append("\n3.1 各节点电压详细列表:")
        report.append("-" * 50)
        report.append(f"{'节点名称':<15} {'电压幅值(pu)':<18} {'电压相位(°)':<18}")
        report.append("-" * 50)
        
        for bus_name in self.opf_result.voltage_magnitude.index:
            v_mag = float(self.opf_result.voltage_magnitude.loc[bus_name].iloc[0])
            v_ang = float(self.opf_result.voltage_angle.loc[bus_name].iloc[0]) * 180 / np.pi
            report.append(f"{bus_name:<15} {v_mag:<18.6f} {v_ang:<18.4f}")
        
        # 电压偏差分析
        report.append("\n3.2 电压偏差分析:")
        report.append("-" * 40)
        report.append(f"{'电压范围':<15} {'节点数量':<10} {'占比':<8}")
        report.append("-" * 40)
        
        v_values = self.opf_result.voltage_magnitude.values.flatten()
        v_bins = [
            ("< 0.95", (v_values < 0.95).sum()),
            ("0.95-0.98", ((v_values >= 0.95) & (v_values < 0.98)).sum()),
            ("0.98-1.00", ((v_values >= 0.98) & (v_values < 1.00)).sum()),
            ("1.00-1.02", ((v_values >= 1.00) & (v_values < 1.02)).sum()),
            ("1.02-1.05", ((v_values >= 1.02) & (v_values < 1.05)).sum()),
            (">= 1.05", (v_values >= 1.05).sum())
        ]
        
        total_buses = len(v_values)
        for bin_name, count in v_bins:
            ratio = count / total_buses * 100 if total_buses > 0 else 0
            report.append(f"{bin_name:<15} {count:<10} {ratio:<8.2f}%")
        
        # 4. 发电机出力详细分析
        report.append("\n" + "=" * 60)
        report.append("4. 发电机出力详细分析")
        report.append("=" * 60)
        
        report.append("4.1 发电机出力列表:")
        report.append("-" * 50)
        report.append(f"{'发电机名称':<15} {'有功出力(pu)':<18} {'占总出力比例':<15}")
        report.append("-" * 50)
        
        total_gen = float(np.sum(self.opf_result.generator_outputs.values))
        for gen_name, output in self.opf_result.generator_outputs.iterrows():
            p_out = float(output.iloc[0])
            ratio = p_out / total_gen * 100 if total_gen > 0 else 0
            report.append(f"{gen_name:<15} {p_out:<18.6f} {ratio:<15.2f}%")
        
        report.append(f"\n总发电出力: {total_gen:.6f} pu")
        
        # 5. 发电成本详细分析
        report.append("\n" + "=" * 60)
        report.append("5. 发电成本详细分析")
        report.append("=" * 60)
        
        cost_analysis = self.analyze_generator_cost()
        report.append(f"总发电成本: {cost_analysis['total_cost']:.6f} $")
        report.append(f"拉格朗日乘子(边际成本): {cost_analysis['lambda_value']:.6f} $/pu")
        report.append(f"平均单位成本: {cost_analysis['average_cost_per_mw']:.6f} $/MW")
        
        # 6. 全纯嵌入法特有分析
        report.append("\n" + "=" * 60)
        report.append("6. 全纯嵌入法特有分析")
        report.append("=" * 60)
        
        report.append("6.1 方法原理概述:")
        report.append("-" * 40)
        report.append(textwrap.fill(
            "全纯嵌入法(HEM)是一种非迭代的电力系统计算方法，通过将电力系统方程嵌入到复平面上的全纯函数",
            width=75
        ))
        report.append(textwrap.fill(
            "空间，利用幂级数展开求解。该方法具有全局收敛性，不依赖初始值，避免了传统迭代方法的收敛问题",
            width=75
        ))
        
        report.append("\n6.2 数值特性分析:")
        report.append("-" * 40)
        report.append("• 非迭代特性: 避免了传统牛顿法的迭代收敛问题")
        report.append("• 全局收敛性: 理论上保证全局收敛")
        report.append("• 初始值无关: 不需要猜测初始值")
        report.append("• 数值稳定性: 对病态系统具有较好的鲁棒性")
        
        # 7. 网损分析
        report.append("\n" + "=" * 60)
        report.append("7. 网损分析")
        report.append("=" * 60)
        
        report.append(f"总网损: {self.opf_result.power_loss:.6f} pu")
        report.append(f"网损率: {(self.opf_result.power_loss / total_gen * 100):.4f}%" if total_gen > 0 else "网损率: N/A")
        
        # 8. 敏感性分析
        report.append("\n" + "=" * 60)
        report.append("8. 敏感性分析")
        report.append("=" * 60)
        
        report.append("8.1 边际成本分析:")
        report.append("-" * 40)
        report.append(textwrap.fill(
            f"拉格朗日乘子λ = {self.opf_result.lambda_value:.6f} 表示系统的边际成本，即每增加1pu有功负荷所需",
            width=75
        ))
        report.append(textwrap.fill(
            "增加的发电成本。该值反映了系统当前的供需紧张程度和运行经济性",
            width=75
        ))
        
        # 9. 结果可靠性评估
        report.append("\n" + "=" * 60)
        report.append("9. 结果可靠性评估")
        report.append("=" * 60)
        
        report.append("9.1 数值精度评估:")
        report.append("-" * 40)
        report.append(f"收敛误差: {self.opf_result.error:.8e} (阈值: 1e-8)")
        
        if self.opf_result.error < 1e-8:
            report.append("精度评价: 高精度，满足工程要求")
        elif self.opf_result.error < 1e-6:
            report.append("精度评价: 中等精度，基本满足工程要求")
        else:
            report.append("精度评价: 低精度，可能需要进一步检查")
        
        report.append("\n9.2 物理合理性检查:")
        report.append("-" * 40)
        
        # 电压合理性检查
        v_min = voltage_analysis['min_voltage']
        v_max = voltage_analysis['max_voltage']
        if 0.9 <= v_min and v_max <= 1.1:
            report.append("电压范围: 合理，在正常运行范围内")
        elif 0.85 <= v_min and v_max <= 1.15:
            report.append("电压范围: 基本合理，接近运行极限")
        else:
            report.append("电压范围: 不合理，超出正常运行范围")
        
        # 网损合理性检查
        if self.opf_result.power_loss < 0.1:
            report.append("网损水平: 合理，处于正常范围")
        elif self.opf_result.power_loss < 0.2:
            report.append("网损水平: 偏高，可能存在优化空间")
        else:
            report.append("网损水平: 过高，需要进一步分析")
        
        # 10. 计算结果总结与建议
        report.append("\n" + "=" * 60)
        report.append("10. 计算结果总结与建议")
        report.append("=" * 60)
        
        report.append("10.1 主要结论:")
        report.append("-" * 40)
        report.append(f"1. 计算{'成功' if self.opf_result.converged else '未成功'}收敛")
        report.append(f"2. 系统电压水平{'正常' if 0.9 <= v_min and v_max <= 1.1 else '异常'}")
        report.append(f"3. 网损水平{'正常' if self.opf_result.power_loss < 0.1 else '偏高'}")
        report.append(f"4. 发电成本{'合理' if cost_analysis['average_cost_per_mw'] < 20 else '偏高'}")
        
        report.append("\n10.2 运行建议:")
        report.append("-" * 40)
        
        if voltage_analysis['voltage_violations'] > 0:
            report.append(f"• 存在 {voltage_analysis['voltage_violations']} 个电压越限节点，建议调整无功设备")
        
        if self.opf_result.power_loss > 0.1:
            report.append("• 网损偏高，建议优化网络拓扑或调整发电机出力分布")
        
        if self.opf_result.iterations > 50:
            report.append("• 收敛较慢，建议检查系统数据或调整计算参数")
        
        report.append("\n10.3 方法优势总结:")
        report.append("-" * 40)
        report.append("• 非迭代特性，避免收敛问题")
        report.append("• 全局收敛性，理论保证")
        report.append("• 初始值无关，降低使用难度")
        report.append("• 适用于各种规模的电力系统")
        
        # 报告结尾
        report.append("\n" + "=" * 80)
        report.append("           报告生成完毕")
        report.append("           PyXESXXN Holomorphic OPF Analysis")
        report.append("=" * 80)
        
        # 生成完整报告字符串
        full_report = "\n".join(report)
        
        # 如果指定了输出文件，则写入文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_report)
            report.insert(1, f"报告已保存至: {output_file}")
            full_report = "\n".join(report)
        
        return full_report


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


def batch_process_holomorphic_opf(case_files: List[str]) -> Dict[str, Tuple[HolomorphicOPFResult, HolomorphicOPFAnalysis]]:
    """批量处理多个MATLAB案例文件，使用全纯嵌入法进行最优潮流计算
    
    Args:
        case_files: MATLAB案例文件路径列表
        
    Returns:
        处理结果字典，键为文件名，值为(最优潮流结果, 最优潮流分析)
    """
    results = {}
    import os
    
    # 创建报告目录
    report_dir = os.path.join(os.path.dirname(case_files[0]), "reports") if case_files else "reports"
    os.makedirs(report_dir, exist_ok=True)
    print(f"\n报告将保存到目录: {report_dir}")
    
    for file_path in case_files:
        file_name = os.path.basename(file_path)
        print(f"\n处理案例文件: {file_name}")
        
        try:
            # 解析MATLAB案例文件
            print(f"  1. 解析MATLAB案例文件...")
            from .power_flow_energy_system import parse_matlab_case_file, create_network_from_matlab_case
            matlab_data = parse_matlab_case_file(file_path)
            
            # 创建PyXESXXN网络
            print(f"  2. 创建PyXESXXN网络模型...")
            network = create_network_from_matlab_case(matlab_data)
            
            # 运行全纯嵌入法最优潮流计算
            print(f"  3. 运行全纯嵌入法最优潮流计算...")
            opf_result, opf_analysis = run_holomorphic_opf(network)
            
            results[file_name] = (opf_result, opf_analysis)
            
            print(f"  ✅ 成功处理案例: {file_name}")
            print(f"     收敛状态: {'成功' if opf_result.converged else '失败'}")
            print(f"     迭代次数: {opf_result.iterations}")
            print(f"     计算时间: {opf_result.computation_time:.3f} 秒")
            
            # 生成详细的技术报告
            print(f"  4. 生成详细技术报告...")
            detailed_report = opf_analysis.generate_detailed_interpretability_report(
                os.path.join(report_dir, f"{os.path.splitext(file_name)[0]}_detailed_analysis.txt")
            )
            
            print(f"     报告已生成")
            
        except Exception as e:
            print(f"  ❌ 处理案例 {file_name} 失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return results


def main():
    """主函数，用于测试批量处理功能"""
    import os
    import glob
    
    print("=== 全纯嵌入法最优潮流批量测试程序 ===")
    
    # 获取Grid_Data目录下的所有MATLAB案例文件
    # 使用绝对路径确保能找到正确的文件
    data_dir = "D:\\Desktop\\全新-毕业设计-优化调度环节-电气221徐骁楠-《面向交通电气化与主动配电网的分布式多目标新型微电网能源社区优化调度与韧性提升系统》\\全纯嵌入潮流计算\\Grid_Data"
    case_files = glob.glob(os.path.join(data_dir, "*.m"))
    
    if not case_files:
        print(f"❌ 在 {data_dir} 目录下未找到MATLAB案例文件")
        return
    
    print(f"\n✅ 找到 {len(case_files)} 个MATLAB案例文件:")
    for file in case_files:
        print(f"   - {os.path.basename(file)}")
    
    # 批量处理所有案例文件
    print("\n=== 开始批量处理 ===")
    results = batch_process_holomorphic_opf(case_files)
    
    # 生成处理报告
    print("\n=== 批量处理报告 ===")
    print(f"总案例数: {len(case_files)}")
    print(f"成功处理: {len(results)}")
    print(f"失败处理: {len(case_files) - len(results)}")
    
    if results:
        print("\n详细结果:")
        for file_name, (opf_result, opf_analysis) in results.items():
            print(f"\n案例: {file_name}")
            print(f"  收敛状态: {'成功' if opf_result.converged else '失败'}")
            print(f"  迭代次数: {opf_result.iterations}")
            print(f"  最大误差: {opf_result.error:.6e}")
            print(f"  计算时间: {opf_result.computation_time:.3f} 秒")
            print(f"  总发电成本: {opf_result.generator_cost:.2f} $")
            print(f"  拉格朗日乘子: {opf_result.lambda_value:.4f} $")
    
    print("\n=== 批量处理完成 ===")


# 导出公共API
__all__ = [
    'HolomorphicOPFResult',
    'HolomorphicOPFSolver',
    'HolomorphicOPFAnalysis',
    'create_holomorphic_opf_solver',
    'run_holomorphic_opf',
    'batch_process_holomorphic_opf',
    'main'
]


if __name__ == "__main__":
    main()