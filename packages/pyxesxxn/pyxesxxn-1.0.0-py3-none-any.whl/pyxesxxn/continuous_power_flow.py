#!/usr/bin/env python3
"""
基于改进Chord法的电力系统连续潮流计算新方法

该模块实现了基于改进Chord法的连续潮流（CPF）计算功能，用于分析电力系统静态电压稳定和传输能力。
"""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, csc_matrix, dok_matrix
from scipy.sparse.linalg import spsolve
from typing import Dict, List, Optional, Tuple, Any, Sequence
import logging
import time

from .power_flow_enhanced import (
    EnhancedPowerFlowSolver,
    PowerFlowMethod,
    PowerFlowResult,
    ConvergenceStatus,
    NewtonRaphsonSolver
)
from .network import PyXESXXNNetwork

logger = logging.getLogger(__name__)


class ContinuousPowerFlowResult:
    """连续潮流计算结果类"""
    def __init__(self):
        self.v_angles: List[np.ndarray] = []  # 电压相角序列
        self.v_magnitudes: List[np.ndarray] = []  # 电压幅值序列
        self.lambdas: List[float] = []  # 负荷增长参数序列
        self.solution_path: List[np.ndarray] = []  # 完整解路径
        self.critical_point: Optional[Dict[str, Any]] = None  # 临界点信息
        self.converged: bool = False  # 计算是否收敛
        self.iterations: int = 0  # 总迭代次数
        self.computation_time: float = 0.0  # 计算时间
        self.warnings: List[str] = []  # 警告信息
        self.method_switches: int = 0  # 方法切换次数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "v_angles": [list(va) for va in self.v_angles],
            "v_magnitudes": [list(vm) for vm in self.v_magnitudes],
            "lambdas": self.lambdas,
            "solution_path": [list(sp) for sp in self.solution_path],
            "critical_point": self.critical_point,
            "converged": self.converged,
            "iterations": self.iterations,
            "computation_time": self.computation_time,
            "warnings": self.warnings,
            "method_switches": self.method_switches
        }
    
    def get_pv_curve(self) -> Tuple[List[float], Dict[str, List[float]]]:
        """获取P-V曲线数据"""
        lambdas = self.lambdas
        
        # 检查v_magnitudes是否为空
        if not self.v_magnitudes or len(self.v_magnitudes[0]) == 0:
            return lambdas, {}
        
        v_magnitudes = {
            f"bus_{i}": [vm[i] for vm in self.v_magnitudes]
            for i in range(len(self.v_magnitudes[0]))
        }
        return lambdas, v_magnitudes


class ImprovedChordMethodSolver(EnhancedPowerFlowSolver):
    """基于改进Chord法的连续潮流求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        """
        初始化改进Chord法连续潮流求解器
        
        参数:
            network: PyXESXXN网络对象
            **kwargs: 其他配置参数
        """
        super().__init__(network, PowerFlowMethod.NEWTON_RAPHSON)
        self.max_iterations = kwargs.get('max_iterations', 100)
        self.tolerance = kwargs.get('tolerance', 1e-8)
        self.chord_tolerance = kwargs.get('chord_tolerance', 1e-6)
        self.step_size = kwargs.get('step_size', 0.05)  # 负荷增长步长
        self.min_step_size = kwargs.get('min_step_size', 0.001)  # 最小步长
        self.max_lambda = kwargs.get('max_lambda', 3.0)  # 最大负荷增长参数
        self.criticality_threshold = kwargs.get('criticality_threshold', 100.0)  # 临界点判定阈值
        self.use_improved_chord = kwargs.get('use_improved_chord', True)  # 是否使用改进Chord法
        self.verbose = kwargs.get('verbose', False)
        self.damping_factor = kwargs.get('damping_factor', 0.8)  # 添加阻尼因子，默认0.8
        
        # 存储迭代历史
        self.iteration_history = []
    
    def solve(self, snapshots: Optional[Sequence] = None) -> ContinuousPowerFlowResult:
        """
        求解连续潮流计算
        
        参数:
            snapshots: 快照序列（未使用）
            
        返回:
            ContinuousPowerFlowResult: 连续潮流计算结果
        """
        start_time = time.time()
        result = ContinuousPowerFlowResult()
        
        try:
            # 验证网络数据
            if not self.validate_inputs():
                result.converged = False
                result.warnings.append("网络数据验证失败")
                result.computation_time = time.time() - start_time
                return result
            
            # 准备网络数据
            network_data = self._prepare_network_data()
            n_buses = len(network_data['bus_names'])
            
            # 首先运行常规牛顿-拉夫逊潮流计算，获取可靠的初始点
            logger.info("运行初始牛顿-拉夫逊潮流计算，获取可靠初始点...")
            
            # 初始化电压：平衡节点为1.0∠0°，其他节点为0.95∠-0.1°
            V_mag_initial = np.ones(n_buses) * 0.95  # 电压幅值初始化为0.95 pu
            V_ang_initial = np.zeros(n_buses) - 0.1   # 电压相角初始化为-0.1 rad
            
            # 识别平衡节点
            slack_bus_idx = self._find_slack_bus(network_data)
            
            # 平衡节点保持1.0∠0°
            if slack_bus_idx is not None:
                V_mag_initial[slack_bus_idx] = 1.0
                V_ang_initial[slack_bus_idx] = 0.0
            
            # 运行初始牛顿-拉夫逊迭代，获取可靠的初始点
            initial_iterations = 0
            max_initial_iterations = 10
            initial_tolerance = 1e-6
            
            # 计算导纳矩阵
            Y = self._calculate_admittance_matrix(network_data)
            
            # 初始潮流计算
            V_mag = V_mag_initial.copy()
            V_ang = V_ang_initial.copy()
            initial_converged = False
            
            for initial_iter in range(max_initial_iterations):
                # 计算功率不平衡
                P, Q = self._calculate_power_injection(V_mag, V_ang, Y)
                P_mismatch, Q_mismatch = self._calculate_power_mismatch(P, Q, 0.0, network_data)
                
                # 计算误差
                mismatch = np.concatenate([P_mismatch, Q_mismatch])
                error = np.max(np.abs(mismatch))
                
                if error < initial_tolerance:
                    initial_converged = True
                    break
                
                # 计算雅可比矩阵
                J = self._calculate_jacobian(V_mag, V_ang, Y, network_data)
                
                # 求解修正方程
                dx = spsolve(J, -mismatch)
                
                # 应用阻尼因子
                dx *= 0.9
                
                # 更新电压
                V_ang += dx[:n_buses]
                V_mag += dx[n_buses:]
                
                # 限制电压幅值
                V_mag = np.clip(V_mag, 0.5, 1.5)
                
                initial_iterations += 1
            
            if initial_converged:
                logger.info(f"初始潮流计算收敛，迭代次数: {initial_iterations}")
                V_mag_initial = V_mag.copy()
                V_ang_initial = V_ang.copy()
            else:
                logger.warning(f"初始潮流计算未完全收敛，使用近似解作为初始点")
            
            logger.info(f"使用初始电压值: V_mag={V_mag_initial[:3]}..., V_ang={V_ang_initial[:3]}...")
            
            # 初始化连续潮流计算
            lambda_current = 0.0
            V_mag_current = V_mag_initial.copy()
            V_ang_current = V_ang_initial.copy()
            
            # 存储初始解
            result.v_angles.append(V_ang_current.copy())
            result.v_magnitudes.append(V_mag_current.copy())
            result.lambdas.append(lambda_current)
            result.solution_path.append(np.concatenate([V_ang_current, V_mag_current]))
            
            # 计算导纳矩阵
            Y = self._calculate_admittance_matrix(network_data)
            
            # 识别平衡节点
            slack_bus_idx = self._find_slack_bus(network_data)
            
            # 主循环：追踪连续潮流曲线
            converged = True
            while converged and lambda_current < self.max_lambda:
                # 预测下一个解点
                dlambda, V_mag_pred, V_ang_pred = self._predict_next_step(
                    V_mag_current, V_ang_current, lambda_current, Y, network_data
                )
                
                # 修正预测点
                converged, V_mag_corrected, V_ang_corrected, lambda_corrected = self._correct_step(
                    V_mag_pred, V_ang_pred, lambda_current + dlambda, Y, network_data
                )
                
                if converged:
                    # 检查是否到达临界点
                    is_critical = self._check_critical_point(
                        V_mag_current, V_ang_current, lambda_current,
                        V_mag_corrected, V_ang_corrected, lambda_corrected,
                        Y, network_data
                    )
                    
                    # 更新当前解
                    V_mag_current = V_mag_corrected.copy()
                    V_ang_current = V_ang_corrected.copy()
                    lambda_current = lambda_corrected
                    
                    # 存储解
                    result.v_angles.append(V_ang_current.copy())
                    result.v_magnitudes.append(V_mag_current.copy())
                    result.lambdas.append(lambda_current)
                    result.solution_path.append(np.concatenate([V_ang_current, V_mag_current]))
                    result.iterations += 1
                    
                    # 记录迭代历史，用于调整步长
                    self.iteration_history.append({
                        "iterations": result.iterations,
                        "lambda": lambda_current,
                        "error": np.max(np.abs(np.concatenate([
                            self._calculate_power_mismatch(
                                *self._calculate_power_injection(V_mag_current, V_ang_current, Y),
                                lambda_current, network_data
                            )
                        ])))
                    })
                    
                    if is_critical:
                        # 记录临界点
                        result.critical_point = {
                            "lambda": lambda_current,
                            "v_angles": V_ang_current.copy().tolist(),
                            "v_magnitudes": V_mag_current.copy().tolist()
                        }
                        result.warnings.append(f"已到达临界点，λ={lambda_current:.4f}")
                        break
                    
                    # 调整步长
                    self._adjust_step_size()
            
            result.converged = converged
        except Exception as e:
            logger.error(f"连续潮流计算失败: {e}")
            result.converged = False
            result.warnings.append(f"计算失败: {str(e)}")
        
        result.computation_time = time.time() - start_time
        return result
    
    def _prepare_network_data(self) -> Dict[str, Any]:
        """
        准备网络数据
        
        返回:
            Dict[str, Any]: 网络数据字典，与NewtonRaphsonSolver兼容
        """
        # 直接返回与NewtonRaphsonSolver兼容的数据格式
        # 收集母线数据（列表格式）
        buses = list(self.network.buses.values())
        bus_names = list(self.network.buses.keys())
        
        # 收集发电机数据（列表格式）
        generators = list(self.network.generators.values())
        
        # 收集负荷数据（列表格式）
        loads = list(self.network.loads.values())
        
        # 收集线路数据（列表格式）
        lines = list(self.network.lines.values())
        
        return {
            'buses': buses,
            'bus_names': bus_names,
            'generators': generators,
            'loads': loads,
            'lines': lines
        }
    
    def _calculate_admittance_matrix(self, network_data: Dict[str, Any]) -> csr_matrix:
        """
        计算导纳矩阵
        
        参数:
            network_data: 网络数据字典
            
        返回:
            csr_matrix: 导纳矩阵
        """
        bus_names = network_data['bus_names']
        n_buses = len(bus_names)
        Y = dok_matrix((n_buses, n_buses), dtype=np.complex128)
        
        # 初始化导纳矩阵
        for line in network_data['lines']:
            # Line对象是对象，不是字典，应该使用属性访问
            from_bus_name = line.from_bus.name
            to_bus_name = line.to_bus.name
            params = line.parameters
            r = params.get('resistance', 0.0)
            x = params.get('reactance', 0.0)
            
            # 计算线路导纳
            y_line = 1 / (r + 1j * x) if (r + 1j * x) != 0 else 0
            
            # 自导纳
            Y[bus_names.index(from_bus_name), bus_names.index(from_bus_name)] += y_line
            Y[bus_names.index(to_bus_name), bus_names.index(to_bus_name)] += y_line
            
            # 互导纳
            Y[bus_names.index(from_bus_name), bus_names.index(to_bus_name)] -= y_line
            Y[bus_names.index(to_bus_name), bus_names.index(from_bus_name)] -= y_line
        
        return Y.tocsr()
    
    def _find_slack_bus(self, network_data: Dict[str, Any]) -> Optional[int]:
        """
        查找平衡节点
        
        参数:
            network_data: 网络数据字典
            
        返回:
            Optional[int]: 平衡节点索引
        """
        for gen in network_data['generators']:
            # Generator对象是对象，不是字典，应该使用属性访问
            control = getattr(gen, 'control', '') or gen.parameters.get('control', '')
            # 不区分大小写比较
            if control.upper() in ['SLACK', 'BALANCE']:
                return network_data['bus_names'].index(gen.bus.name)
        
        # 如果没有找到平衡节点，返回第一个母线作为平衡节点
        logger.warning("未找到平衡节点，使用第一个母线作为平衡节点")
        return 0
    
    def _predict_next_step(self, V_mag: np.ndarray, V_ang: np.ndarray, 
                          lambda_current: float, Y: csr_matrix, 
                          network_data: Dict[str, Any]) -> Tuple[float, np.ndarray, np.ndarray]:
        """
        预测下一个解点

        参数:
            V_mag: 当前电压幅值
            V_ang: 当前电压相角
            lambda_current: 当前负荷增长参数
            Y: 导纳矩阵
            network_data: 网络数据字典
            
        返回:
            Tuple[float, np.ndarray, np.ndarray]: (步长, 预测电压幅值, 预测电压相角)
        """
        # 使用线性化方法预测下一个解点
        n_buses = len(V_mag)
        
        # 计算当前功率不平衡量
        P, Q = self._calculate_power_injection(V_mag, V_ang, Y)
        P_mismatch, Q_mismatch = self._calculate_power_mismatch(P, Q, lambda_current, network_data)
        mismatch = np.concatenate([P_mismatch, Q_mismatch])
        
        # 计算当前雅可比矩阵
        J = self._calculate_jacobian(V_mag, V_ang, Y, network_data)
        
        # 计算参数化的雅可比矩阵（添加lambda维度）
        # 首先计算功率对lambda的偏导数
        dP_dlambda, dQ_dlambda = self._calculate_power_lambda_derivative(network_data)
        dS_dlambda = np.concatenate([dP_dlambda, dQ_dlambda])
        
        # 构建参数化雅可比矩阵 [J | -dS_dlambda]
        # 计算预测方向向量
        direction = np.zeros(2 * n_buses + 1)
        direction[-1] = 1.0  # 沿着lambda增加的方向
        
        # 计算参数化方程的解，得到预测方向
        try:
            # 构建扩展雅可比矩阵
            J_extended = dok_matrix((2 * n_buses + 1, 2 * n_buses + 1))
            J_extended[:2*n_buses, :2*n_buses] = J
            J_extended[:2*n_buses, -1] = -dS_dlambda
            
            # 添加参数化约束（弧长约束）
            # 这里使用简化的弧长约束
            J_extended[-1, :] = direction
            
            # 求解扩展系统
            dx = spsolve(J_extended.tocsr(), np.zeros(2 * n_buses + 1))
            
            # 计算步长
            dlambda = self.step_size
            
            # 计算预测的电压变化
            V_ang_pred = V_ang + dx[:n_buses] * dlambda
            V_mag_pred = V_mag + dx[n_buses:2*n_buses] * dlambda
        except Exception as e:
            logger.warning(f"预测步骤中发生错误，使用简化预测: {e}")
            # 如果参数化求解失败，使用简化的线性预测
            dlambda = self.step_size
            V_mag_pred = V_mag.copy()
            V_ang_pred = V_ang.copy()
        
        return dlambda, V_mag_pred, V_ang_pred
    
    def _correct_step(self, V_mag_pred: np.ndarray, V_ang_pred: np.ndarray, 
                     lambda_pred: float, Y: csr_matrix, 
                     network_data: Dict[str, Any]) -> Tuple[bool, np.ndarray, np.ndarray, float]:
        """
        修正预测点
        
        参数:
            V_mag_pred: 预测电压幅值
            V_ang_pred: 预测电压相角
            lambda_pred: 预测负荷增长参数
            Y: 导纳矩阵
            network_data: 网络数据字典
            
        返回:
            Tuple[bool, np.ndarray, np.ndarray, float]: (是否收敛, 修正后电压幅值, 修正后电压相角, 修正后负荷增长参数)
        """
        n_buses = len(V_mag_pred)
        slack_bus_idx = self._find_slack_bus(network_data)
        
        # 初始化修正后的解
        V_mag_corrected = V_mag_pred.copy()
        V_ang_corrected = V_ang_pred.copy()
        lambda_corrected = lambda_pred
        
        # 计算初始功率不平衡
        P, Q = self._calculate_power_injection(V_mag_corrected, V_ang_corrected, Y)
        P_mismatch, Q_mismatch = self._calculate_power_mismatch(P, Q, lambda_corrected, network_data)
        
        # 计算初始误差
        error = np.max(np.abs(np.concatenate([P_mismatch, Q_mismatch]))) 
        
        # 判断是否需要使用改进Chord法
        use_chord_method = False
        try:
            # 计算雅可比矩阵
            J = self._calculate_jacobian(V_mag_corrected, V_ang_corrected, Y, network_data)
            
            # 检查雅可比矩阵条件数，判断是否接近临界点
            cond_number = np.linalg.cond(J.toarray())
            if cond_number > self.criticality_threshold:
                use_chord_method = True
        except np.linalg.LinAlgError:
            # 雅可比矩阵奇异，使用改进Chord法
            use_chord_method = True
        
        if use_chord_method:
            # 使用改进Chord法修正
            logger.info(f"使用改进Chord法，当前λ={lambda_corrected:.4f}")
            return self._improve_chord_correction(V_mag_corrected, V_ang_corrected, lambda_corrected, Y, network_data)
        else:
            # 使用牛顿法修正
            return self._newton_correction(V_mag_corrected, V_ang_corrected, lambda_corrected, Y, network_data)
    
    def _newton_correction(self, V_mag: np.ndarray, V_ang: np.ndarray, 
                          lambda_current: float, Y: csr_matrix, 
                          network_data: Dict[str, Any]) -> Tuple[bool, np.ndarray, np.ndarray, float]:
        """
        使用牛顿法修正预测点
        
        参数:
            V_mag: 初始电压幅值
            V_ang: 初始电压相角
            lambda_current: 初始负荷增长参数
            Y: 导纳矩阵
            network_data: 网络数据字典
            
        返回:
            Tuple[bool, np.ndarray, np.ndarray, float]: (是否收敛, 修正后电压幅值, 修正后电压相角, 修正后负荷增长参数)
        """
        converged = False
        iterations = 0
        
        while iterations < self.max_iterations:
            # 计算功率不平衡
            P, Q = self._calculate_power_injection(V_mag, V_ang, Y)
            P_mismatch, Q_mismatch = self._calculate_power_mismatch(P, Q, lambda_current, network_data)
            
            # 计算误差
            mismatch = np.concatenate([P_mismatch, Q_mismatch])
            error = np.max(np.abs(mismatch))
            
            if error < self.tolerance:
                converged = True
                break
            
            # 计算雅可比矩阵
            J = self._calculate_jacobian(V_mag, V_ang, Y, network_data)
            
            # 求解修正方程
            try:
                dx = spsolve(J, -mismatch)
                
                # 更新电压
                V_ang += dx[:len(V_ang)]
                V_mag += dx[len(V_ang):]
                
                iterations += 1
            except Exception as e:
                logger.error(f"牛顿法修正失败: {e}")
                break
        
        return converged, V_mag, V_ang, lambda_current
    
    def _improve_chord_correction(self, V_mag: np.ndarray, V_ang: np.ndarray, 
                                 lambda_current: float, Y: csr_matrix, 
                                 network_data: Dict[str, Any]) -> Tuple[bool, np.ndarray, np.ndarray, float]:
        """
        使用改进Chord法修正预测点
        
        参数:
            V_mag: 初始电压幅值
            V_ang: 初始电压相角
            lambda_current: 初始负荷增长参数
            Y: 导纳矩阵
            network_data: 网络数据字典
            
        返回:
            Tuple[bool, np.ndarray, np.ndarray, float]: (是否收敛, 修正后电压幅值, 修正后电压相角, 修正后负荷增长参数)
        """
        converged = False
        iterations = 0
        
        # 保存初始雅可比矩阵
        J_initial = self._calculate_jacobian(V_mag, V_ang, Y, network_data)
        
        # 计算初始功率不平衡
        P_initial, Q_initial = self._calculate_power_injection(V_mag, V_ang, Y)
        P_mismatch_initial, Q_mismatch_initial = self._calculate_power_mismatch(P_initial, Q_initial, lambda_current, network_data)
        
        # 初始化迭代变量
        V_mag_prev = V_mag.copy()
        V_ang_prev = V_ang.copy()
        
        while iterations < self.max_iterations:
            # 计算当前功率不平衡
            P, Q = self._calculate_power_injection(V_mag, V_ang, Y)
            P_mismatch, Q_mismatch = self._calculate_power_mismatch(P, Q, lambda_current, network_data)
            
            # 计算误差
            mismatch = np.concatenate([P_mismatch, Q_mismatch])
            error = np.max(np.abs(mismatch))
            
            if error < self.chord_tolerance:
                converged = True
                break
            
            try:
                # 使用固定的初始雅可比矩阵求解修正量
                dx = spsolve(J_initial, -mismatch)
                
                # 应用阻尼因子，平滑电压变化
                dx *= self.damping_factor
                
                # 更新电压
                V_ang_new = V_ang + dx[:len(V_ang)]
                V_mag_new = V_mag + dx[len(V_ang):]
                
                # 限制电压幅值在合理范围内
                V_mag_new = np.clip(V_mag_new, 0.5, 1.5)
                
                if self.use_improved_chord:
                    # 使用外推公式优化迭代结果，添加安全检查
                    if iterations > 0:
                        # 计算外推值
                        V_ang_extrap = (iterations + 1) * V_ang_new - iterations * V_ang_prev
                        V_mag_extrap = (iterations + 1) * V_mag_new - iterations * V_mag_prev
                        
                        # 检查外推值是否合理，否则使用普通更新
                        if np.all(np.isfinite(V_ang_extrap)) and np.all(np.isfinite(V_mag_extrap)):
                            V_ang_new = V_ang_extrap
                            V_mag_new = V_mag_extrap
                
                # 更新迭代变量
                V_ang_prev = V_ang.copy()
                V_mag_prev = V_mag.copy()
                V_ang = V_ang_new.copy()
                V_mag = V_mag_new.copy()
                
                iterations += 1
            except Exception as e:
                logger.error(f"改进Chord法修正失败: {e}")
                break
        
        return converged, V_mag, V_ang, lambda_current
    
    def _calculate_power_injection(self, V_mag: np.ndarray, V_ang: np.ndarray, Y: csr_matrix) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算节点注入功率
        
        参数:
            V_mag: 电压幅值
            V_ang: 电压相角
            Y: 导纳矩阵
            
        返回:
            Tuple[np.ndarray, np.ndarray]: (有功注入功率, 无功注入功率)
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
    
    def _calculate_power_mismatch(self, P: np.ndarray, Q: np.ndarray, 
                                 lambda_current: float, network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算功率不平衡量
        
        参数:
            P: 注入有功功率
            Q: 注入无功功率
            lambda_current: 负荷增长参数
            network_data: 网络数据字典
            
        返回:
            Tuple[np.ndarray, np.ndarray]: (有功不平衡量, 无功不平衡量)
        """
        n_buses = len(P)
        P_mismatch = np.zeros(n_buses)
        Q_mismatch = np.zeros(n_buses)
        
        # 计算指定功率（考虑负荷增长）
        P_specified, Q_specified = self._calculate_specified_power(network_data, lambda_current)
        
        # 计算不平衡量
        P_mismatch = P_specified - P
        Q_mismatch = Q_specified - Q
        
        # 平衡节点的有功功率不平衡量应该为0（电压幅值和相角固定）
        slack_bus_idx = self._find_slack_bus(network_data)
        if slack_bus_idx is not None:
            P_mismatch[slack_bus_idx] = 0
            Q_mismatch[slack_bus_idx] = 0
        
        return P_mismatch, Q_mismatch
    
    def _calculate_specified_power(self, network_data: Dict[str, Any], lambda_current: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算指定功率（考虑负荷增长）

        参数:
            network_data: 网络数据字典
            lambda_current: 负荷增长参数
            
        返回:
            Tuple[np.ndarray, np.ndarray]: (指定有功功率, 指定无功功率)
        """
        buses = network_data['buses']
        bus_names = network_data['bus_names']
        generators = network_data['generators']
        loads = network_data['loads']
        
        n_buses = len(buses)
        P_specified = np.zeros(n_buses)
        Q_specified = np.zeros(n_buses)
        
        # 创建母线名称到索引的映射
        bus_name_to_idx = {name: idx for idx, name in enumerate(bus_names)}
        
        # 发电机功率（正方向）
        for gen in generators:
            bus_name = gen.bus.name
            if bus_name in bus_name_to_idx:
                bus_idx = bus_name_to_idx[bus_name]
                params = gen.parameters
                P_specified[bus_idx] += params.get('power_set', 0)
                Q_specified[bus_idx] += params.get('reactive_power_set', 0)
        
        # 负荷功率（负方向，考虑负荷增长）
        for load in loads:
            bus_name = load.bus.name
            if bus_name in bus_name_to_idx:
                bus_idx = bus_name_to_idx[bus_name]
                params = load.parameters
                # 获取负荷增长速率
                growth_rate = params.get('growth_rate', 1.0)
                # 计算考虑增长后的负荷功率
                P_specified[bus_idx] -= params.get('demand', 0) * (1 + lambda_current * growth_rate)
                Q_specified[bus_idx] -= params.get('reactive_demand', 0) * (1 + lambda_current * growth_rate)
        
        return P_specified, Q_specified
    
    def _calculate_power_lambda_derivative(self, network_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算功率对lambda的偏导数

        参数:
            network_data: 网络数据字典
            
        返回:
            Tuple[np.ndarray, np.ndarray]: (有功功率对lambda的偏导数, 无功功率对lambda的偏导数)
        """
        buses = network_data['buses']
        bus_names = network_data['bus_names']
        loads = network_data['loads']
        
        n_buses = len(buses)
        dP_dlambda = np.zeros(n_buses)
        dQ_dlambda = np.zeros(n_buses)
        
        # 创建母线名称到索引的映射
        bus_name_to_idx = {name: idx for idx, name in enumerate(bus_names)}
        
        # 只考虑负荷对lambda的导数，发电机功率对lambda的导数为0
        for load in loads:
            bus_name = load.bus.name
            if bus_name in bus_name_to_idx:
                bus_idx = bus_name_to_idx[bus_name]
                params = load.parameters
                # 获取负荷增长速率
                growth_rate = params.get('growth_rate', 1.0)
                # 计算功率对lambda的偏导数
                dP_dlambda[bus_idx] -= params.get('demand', 0) * growth_rate
                dQ_dlambda[bus_idx] -= params.get('reactive_demand', 0) * growth_rate
        
        return dP_dlambda, dQ_dlambda
    
    def _calculate_jacobian(self, V_mag: np.ndarray, V_ang: np.ndarray, 
                           Y: csr_matrix, network_data: Dict[str, Any]) -> csr_matrix:
        """
        计算雅可比矩阵
        
        参数:
            V_mag: 电压幅值
            V_ang: 电压相角
            Y: 导纳矩阵
            network_data: 网络数据字典
            
        返回:
            csr_matrix: 雅可比矩阵
        """
        n_buses = len(V_mag)
        J = dok_matrix((2 * n_buses, 2 * n_buses))
        
        # 计算注入功率
        V = V_mag * np.exp(1j * V_ang)
        S_injected = V * np.conj(Y @ V)
        P_injected = S_injected.real
        Q_injected = S_injected.imag
        
        # 计算指定功率
        P_specified, Q_specified = self._calculate_specified_power(network_data, 0.0)
        
        # 计算雅可比矩阵
        for i in range(n_buses):
            for j in range(n_buses):
                # 计算导纳矩阵元素
                G_ij = Y[i, j].real
                B_ij = Y[i, j].imag
                
                # 计算电压角度差
                theta_ij = V_ang[i] - V_ang[j]
                
                if i == j:
                    # 对角线元素
                    # dP/dθ_i
                    J[i, i] = -Q_injected[i] - V_mag[i]**2 * B_ij
                    # dP/dV_i
                    J[i, i + n_buses] = P_injected[i] + V_mag[i]**2 * G_ij
                    # dQ/dθ_i
                    J[i + n_buses, i] = P_injected[i] - V_mag[i]**2 * G_ij
                    # dQ/dV_i
                    J[i + n_buses, i + n_buses] = Q_injected[i] - V_mag[i]**2 * B_ij
                else:
                    # 非对角线元素
                    # dP_i/dθ_j
                    J[i, j] = V_mag[i] * V_mag[j] * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))
                    # dP_i/dV_j
                    J[i, j + n_buses] = V_mag[i] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                    # dQ_i/dθ_j
                    J[i + n_buses, j] = -V_mag[i] * V_mag[j] * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                    # dQ_i/dV_j
                    J[i + n_buses, j + n_buses] = V_mag[i] * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))
        
        return J.tocsr()
    
    def _check_critical_point(self, V_mag_prev: np.ndarray, V_ang_prev: np.ndarray, lambda_prev: float,
                             V_mag_curr: np.ndarray, V_ang_curr: np.ndarray, lambda_curr: float,
                             Y: csr_matrix, network_data: Dict[str, Any]) -> bool:
        """
        检查是否到达临界点
        
        参数:
            V_mag_prev: 前一电压幅值
            V_ang_prev: 前一电压相角
            lambda_prev: 前一负荷增长参数
            V_mag_curr: 当前电压幅值
            V_ang_curr: 当前电压相角
            lambda_curr: 当前负荷增长参数
            Y: 导纳矩阵
            network_data: 网络数据字典
            
        返回:
            bool: 是否为临界点
        """
        # 计算导数符号变化，判断是否为临界点
        try:
            # 计算前一雅可比矩阵
            J_prev = self._calculate_jacobian(V_mag_prev, V_ang_prev, Y, network_data)
            J_prev_det = np.linalg.det(J_prev.toarray())
            
            # 计算当前雅可比矩阵
            J_curr = self._calculate_jacobian(V_mag_curr, V_ang_curr, Y, network_data)
            J_curr_det = np.linalg.det(J_curr.toarray())
            
            # 如果行列式符号变化，说明接近临界点
            if J_prev_det * J_curr_det < 0:
                return True
        except Exception as e:
            logger.error(f"临界点判定失败: {e}")
        
        return False
    
    def _adjust_step_size(self) -> None:
        """
        调整步长
        """
        # 简化的步长调整策略
        if len(self.iteration_history) > 5:
            # 如果最近迭代收敛较慢，减小步长
            if any(iter_info['iterations'] > 10 for iter_info in self.iteration_history[-5:]):
                self.step_size = max(self.step_size * 0.8, self.min_step_size)
            else:
                # 否则增大步长
                self.step_size = min(self.step_size * 1.2, 0.2)


def create_continuous_power_flow_solver(network: PyXESXXNNetwork, **kwargs) -> ImprovedChordMethodSolver:
    """
    创建连续潮流计算求解器
    
    参数:
        network: PyXESXXN网络对象
        **kwargs: 其他配置参数
        
    返回:
        ImprovedChordMethodSolver: 连续潮流计算求解器
    """
    return ImprovedChordMethodSolver(network, **kwargs)


def run_continuous_power_flow_analysis(network: PyXESXXNNetwork, **kwargs) -> Tuple[ContinuousPowerFlowResult, Any]:
    """
    运行连续潮流计算分析
    
    参数:
        network: PyXESXXN网络对象
        **kwargs: 其他配置参数
        
    返回:
        Tuple[ContinuousPowerFlowResult, Any]: (连续潮流计算结果, 分析对象)
    """
    solver = create_continuous_power_flow_solver(network, **kwargs)
    result = solver.solve()
    
    # 这里可以添加分析对象
    analysis = None
    
    return result, analysis


# 导出公共API
__all__ = [
    'ContinuousPowerFlowResult',
    'ImprovedChordMethodSolver',
    'create_continuous_power_flow_solver',
    'run_continuous_power_flow_analysis'
]