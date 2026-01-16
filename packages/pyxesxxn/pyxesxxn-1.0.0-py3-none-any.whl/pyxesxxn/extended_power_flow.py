#!/usr/bin/env python3
"""
基于功率下垂节点与两步式分析的扩展潮流计算模型

该模块实现了针对大电网潮流计算无解场景的扩展潮流计算模型，通过定义功率下垂节点（KV节点）、
两步式子网分析方法及状态回溯机制，实现潮流无解时的可靠调整与收敛。
"""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, csc_matrix, dok_matrix
from scipy.sparse.linalg import spsolve
from scipy.linalg import eig, eigh
from typing import Dict, List, Optional, Tuple, Any
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


class ExtendedPowerFlowResult:
    """扩展潮流计算结果类"""
    def __init__(self):
        self.converged: bool = False  # 计算是否收敛
        self.iterations: int = 0  # 总迭代次数
        self.computation_time: float = 0.0  # 计算时间
        self.warnings: List[str] = []  # 警告信息
        
        # 潮流结果
        self.power_flow_result: Optional[PowerFlowResult] = None  # 最终潮流计算结果
        
        # KV节点信息
        self.kv_nodes: List[Dict[str, Any]] = []  # 转换为KV节点的信息
        self.kv_conversion_count: int = 0  # KV节点转换次数
        
        # 子网分析结果
        self.pq_subnet_result: Dict[str, Any] = {}  # PQ子网分析结果
        self.pv_subnet_result: Dict[str, Any] = {}  # PV子网分析结果
        
        # 状态回溯结果
        self.state_backtracking: Dict[str, Any] = {}  # 状态回溯信息
        self.generator_adjustments: Dict[str, float] = {}  # 发电机出力调整量
        self.reactive_compensation: Dict[str, float] = {}  # 无功补偿量
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "converged": self.converged,
            "iterations": self.iterations,
            "computation_time": self.computation_time,
            "warnings": self.warnings,
            "power_flow_result": self.power_flow_result.to_dict() if self.power_flow_result else None,
            "kv_nodes": self.kv_nodes,
            "kv_conversion_count": self.kv_conversion_count,
            "pq_subnet_result": self.pq_subnet_result,
            "pv_subnet_result": self.pv_subnet_result,
            "state_backtracking": self.state_backtracking,
            "generator_adjustments": self.generator_adjustments,
            "reactive_compensation": self.reactive_compensation
        }


class PowerSagNode:
    """功率下垂节点（KV节点）类"""
    
    def __init__(self, node_name: str, node_type: str, 
                 k_coefficient: float, u_set: float,
                 p_c: float = 0.0, q_c: float = 0.0):
        """
        初始化功率下垂节点
        
        参数:
            node_name: 节点名称
            node_type: 原节点类型 ('PQ' 或 'PV')
            k_coefficient: 功率比例系数
            u_set: 电压设定值
            p_c: 有功修正系数
            q_c: 无功修正系数
        """
        self.node_name = node_name
        self.node_type = node_type
        self.k_coefficient = k_coefficient
        self.u_set = u_set
        self.p_c = p_c
        self.q_c = q_c
        self.is_converted = False  # 是否已转换
    
    def calculate_power_imbalance(self, p_injected: float, q_injected: float) -> float:
        """
        计算功率不平衡量
        
        参数:
            p_injected: 注入有功功率
            q_injected: 注入无功功率
            
        返回:
            float: 功率不平衡量
        """
        return p_injected - self.p_c - self.k_coefficient * (q_injected - self.q_c)
    
    def get_equation(self) -> str:
        """获取KV节点的方程表示"""
        return f"f_Pd - {self.p_c} - {self.k_coefficient}(f_Qd - {self.q_c}) = 0, U = {self.u_set}"


class ExtendedPowerFlowSolver(EnhancedPowerFlowSolver):
    """扩展潮流计算求解器"""
    
    def __init__(self, network: PyXESXXNNetwork, **kwargs):
        """
        初始化扩展潮流计算求解器
        
        参数:
            network: PyXESXXN网络对象
            **kwargs: 其他配置参数
        """
        super().__init__(network, method=PowerFlowMethod.NEWTON_RAPHSON)
        self.max_iterations = kwargs.get('max_iterations', 100)
        self.tolerance = kwargs.get('tolerance', 1e-6)
        self.kv_k_pq = kwargs.get('kv_k_pq', 0.5)  # PQ节点转换为KV节点的功率比例系数
        self.kv_k_pv = kwargs.get('kv_k_pv', 0.3)  # PV节点转换为KV节点的功率比例系数
        self.u_set_default = kwargs.get('u_set_default', 1.0)  # 默认电压设定值
        self.max_kv_conversions = kwargs.get('max_kv_conversions', 10)  # 最大KV节点转换次数
        self.verbose = kwargs.get('verbose', False)
        
        # 存储KV节点
        self.kv_nodes: List[PowerSagNode] = []
        
        # 子网分析结果
        self.pq_subnet: Dict[str, Any] = {}
        self.pv_subnet: Dict[str, Any] = {}
        
        # 状态回溯结果
        self.generator_adjustments: Dict[str, float] = {}
        self.reactive_compensation: Dict[str, float] = {}
    
    def solve(self, snapshots: Optional[Any] = None) -> ExtendedPowerFlowResult:
        """
        求解扩展潮流计算
        
        参数:
            snapshots: 快照序列（未使用）
            
        返回:
            ExtendedPowerFlowResult: 扩展潮流计算结果
        """
        start_time = time.time()
        result = ExtendedPowerFlowResult()
        
        try:
            # 1. 数据初始化
            logger.info("扩展潮流计算：数据初始化...")
            
            # 2. 尝试常规潮流计算
            logger.info("扩展潮流计算：尝试常规潮流计算...")
            newton_solver = NewtonRaphsonSolver(self.network)
            try:
                power_flow_result = newton_solver.solve()
                if power_flow_result.converged:
                    logger.info("常规潮流计算收敛，无需扩展计算")
                    result.converged = True
                    result.power_flow_result = power_flow_result
                    result.computation_time = time.time() - start_time
                    return result
            except Exception as e:
                logger.info(f"常规潮流计算失败，开始扩展计算: {e}")
            
            # 3. 两步式分析
            logger.info("扩展潮流计算：开始两步式分析...")
            
            # 3.1 子网拆分
            self._split_subnets()
            
            # 3.2 识别薄弱节点
            weak_pv_nodes = self._identify_weak_pv_nodes()
            weak_pq_nodes = self._identify_weak_pq_nodes()
            
            # 4. KV节点转换与潮流计算
            logger.info("扩展潮流计算：KV节点转换与潮流计算...")
            
            converged = False
            conversion_count = 0
            
            while not converged and conversion_count < self.max_kv_conversions:
                # 转换薄弱节点为KV节点
                if weak_pv_nodes and conversion_count % 2 == 0:
                    # 优先转换PV节点
                    node_name = weak_pv_nodes.pop(0)
                    self._convert_to_kv_node(node_name, 'PV')
                    result.kv_conversion_count += 1
                elif weak_pq_nodes:
                    # 转换PQ节点
                    node_name = weak_pq_nodes.pop(0)
                    self._convert_to_kv_node(node_name, 'PQ')
                    result.kv_conversion_count += 1
                else:
                    # 没有更多薄弱节点可转换
                    break
                
                conversion_count += 1
                
                # 尝试求解扩展潮流
                try:
                    extended_result = self._solve_extended_power_flow()
                    if extended_result.converged:
                        converged = True
                        result.power_flow_result = extended_result
                        break
                except Exception as e:
                    logger.warning(f"扩展潮流计算失败: {e}")
            
            # 5. 状态回溯
            if converged:
                logger.info("扩展潮流计算：状态回溯...")
                self._state_backtracking()
            
            # 6. 结果整理
            result.converged = converged
            result.iterations = conversion_count
            result.kv_nodes = [{
                'node_name': kv_node.node_name,
                'node_type': kv_node.node_type,
                'k_coefficient': kv_node.k_coefficient,
                'u_set': kv_node.u_set
            } for kv_node in self.kv_nodes]
            
        except Exception as e:
            logger.error(f"扩展潮流计算失败: {e}")
            import traceback
            traceback.print_exc()
            result.converged = False
            result.warnings.append(f"计算失败: {str(e)}")
        
        result.computation_time = time.time() - start_time
        return result
    
    def _split_subnets(self) -> None:
        """
        拆分PQ子网与PV子网
        """
        # 准备网络数据
        network_data = self._prepare_network_data()
        buses = network_data['buses']
        generators = network_data['generators']
        loads = network_data['loads']
        
        # 分类节点
        pq_nodes = []
        pv_nodes = []
        slack_nodes = []
        
        for bus_name, bus in zip(network_data['bus_names'], buses):
            # 判断节点类型
            is_slack = any(gen.bus.name == bus_name and gen.parameters.get('control', '') == 'SLACK' for gen in generators)
            is_pv = any(gen.bus.name == bus_name and gen.parameters.get('control', '') == 'PV' for gen in generators)
            is_pq = any(load.bus.name == bus_name for load in loads)
            
            if is_slack:
                slack_nodes.append(bus_name)
            elif is_pv:
                pv_nodes.append(bus_name)
            elif is_pq:
                pq_nodes.append(bus_name)
        
        # 存储子网信息
        self.pq_subnet = {
            'nodes': pq_nodes,
            'size': len(pq_nodes)
        }
        
        self.pv_subnet = {
            'nodes': pv_nodes,
            'size': len(pv_nodes)
        }
        
        logger.info(f"子网拆分结果：PQ子网 {len(pq_nodes)} 个节点，PV子网 {len(pv_nodes)} 个节点，平衡节点 {len(slack_nodes)} 个")
    
    def _identify_weak_pv_nodes(self) -> List[str]:
        """
        识别薄弱PV节点
        
        返回:
            List[str]: 薄弱PV节点列表（按薄弱程度排序）
        """
        # 简化实现：基于发电机出力裕度识别薄弱节点
        weak_nodes = []
        
        for gen in self.network.generators.values():
            control = gen.parameters.get('control', '')
            if control == 'PV':
                capacity = gen.parameters.get('capacity', 1.0)
                power_set = gen.parameters.get('power_set', 0.0)
                
                # 计算出力裕度
                margin = capacity - power_set
                # 裕度越小，节点越薄弱
                weak_nodes.append((gen.bus.name, margin))
        
        # 按裕度从小到大排序（薄弱程度从高到低）
        weak_nodes.sort(key=lambda x: x[1])
        
        return [node_name for node_name, margin in weak_nodes]
    
    def _identify_weak_pq_nodes(self) -> List[str]:
        """
        识别薄弱PQ节点
        
        返回:
            List[str]: 薄弱PQ节点列表（按薄弱程度排序）
        """
        # 简化实现：基于负荷大小识别薄弱节点
        weak_nodes = []
        
        for load in self.network.loads.values():
            demand = load.parameters.get('demand', 0.0)
            # 负荷越大，节点越薄弱
            weak_nodes.append((load.bus.name, demand))
        
        # 按负荷从大到小排序（薄弱程度从高到低）
        weak_nodes.sort(key=lambda x: x[1], reverse=True)
        
        return [node_name for node_name, demand in weak_nodes]
    
    def _convert_to_kv_node(self, node_name: str, node_type: str) -> None:
        """
        将节点转换为KV节点
        
        参数:
            node_name: 节点名称
            node_type: 原节点类型 ('PQ' 或 'PV')
        """
        # 确定功率比例系数
        if node_type == 'PQ':
            k_coefficient = self.kv_k_pq
        else:  # PV
            k_coefficient = self.kv_k_pv
        
        # 创建KV节点
        kv_node = PowerSagNode(
            node_name=node_name,
            node_type=node_type,
            k_coefficient=k_coefficient,
            u_set=self.u_set_default
        )
        
        self.kv_nodes.append(kv_node)
        logger.info(f"转换节点 {node_name} 为KV节点，类型: {node_type}，K系数: {k_coefficient}")
    
    def _solve_extended_power_flow(self) -> PowerFlowResult:
        """
        求解扩展潮流模型
        
        返回:
            PowerFlowResult: 潮流计算结果
        """
        from .power_flow_enhanced import PowerFlowResult, ConvergenceStatus
        
        logger.info("开始求解扩展潮流模型...")
        
        # 准备网络数据
        network_data = self._prepare_network_data()
        bus_names = network_data['bus_names']
        n_buses = len(bus_names)
        
        # 初始化电压幅值和相角
        v_mag = np.ones(n_buses)
        v_ang = np.zeros(n_buses)
        
        # 确定节点类型
        node_types = []
        for bus_name in bus_names:
            # 检查是否为KV节点
            is_kv_node = any(kv_node.node_name == bus_name for kv_node in self.kv_nodes)
            if is_kv_node:
                node_types.append('KV')
            # 检查是否为平衡节点
            elif any(gen.bus.name == bus_name and gen.parameters.get('control', '') == 'SLACK' for gen in network_data['generators']):
                node_types.append('SLACK')
            # 检查是否为PV节点
            elif any(gen.bus.name == bus_name and gen.parameters.get('control', '') == 'PV' for gen in network_data['generators']):
                node_types.append('PV')
            else:
                node_types.append('PQ')
        
        # 计算导纳矩阵
        Y = self._calculate_admittance_matrix(network_data)
        
        # 开始牛顿迭代
        converged = False
        iterations = 0
        error = float('inf')
        
        while iterations < self.max_iterations and error > self.tolerance:
            iterations += 1
            
            # 计算功率不平衡量
            p_mismatch, q_mismatch = self._calculate_power_mismatch(Y, v_mag, v_ang, network_data, node_types)
            
            # 计算雅可比矩阵
            J = self._calculate_extended_jacobian(Y, v_mag, v_ang, network_data, node_types)
            
            # 计算修正量
            delta = np.linalg.solve(J, np.concatenate([p_mismatch, q_mismatch]))
            
            # 更新电压幅值和相角
            delta_ang = delta[:n_buses]
            delta_mag = delta[n_buses:]
            
            for i in range(n_buses):
                if node_types[i] != 'SLACK':  # 平衡节点相角不变
                    v_ang[i] += delta_ang[i]
                if node_types[i] in ['PQ', 'KV']:  # PV节点电压幅值不变
                    v_mag[i] += delta_mag[i]
            
            # 计算误差
            error = np.max(np.abs(delta))
            
            if self.verbose:
                logger.info(f"迭代 {iterations}: 最大误差 = {error:.6e}")
        
        # 构建结果
        if converged or error <= self.tolerance:
            status = ConvergenceStatus.CONVERGED
            converged = True
        else:
            status = ConvergenceStatus.MAX_ITERATIONS
        
        # 创建结果数据框
        voltage_magnitude = pd.DataFrame(v_mag.reshape(-1, 1), index=bus_names, columns=['v_mag_pu'])
        voltage_angle = pd.DataFrame(v_ang.reshape(-1, 1), index=bus_names, columns=['v_ang_rad'])
        
        # 计算注入功率
        p_inj, q_inj = self._calculate_injected_power(Y, v_mag, v_ang)
        active_power = pd.DataFrame(p_inj.reshape(-1, 1), index=bus_names, columns=['p_mw'])
        reactive_power = pd.DataFrame(q_inj.reshape(-1, 1), index=bus_names, columns=['q_mvar'])
        
        return PowerFlowResult(
            converged=converged,
            iterations=iterations,
            error=error,
            status=status,
            voltage_magnitude=voltage_magnitude,
            voltage_angle=voltage_angle,
            active_power=active_power,
            reactive_power=reactive_power,
            line_flows={},
            transformer_flows={},
            losses={'p': np.sum(p_inj), 'q': np.sum(q_inj)},
            computation_time=0.0,
            warnings=[]
        )
    
    def _state_backtracking(self) -> None:
        """
        状态回溯机制
        """
        # 计算SNB点及左特征向量
        snb_result = self._calculate_snb_point()
        
        if snb_result:
            logger.info(f"SNB点计算结果：{snb_result}")
            
            # 确定发电机出力调整量
            self._calculate_generator_adjustments(snb_result['left_eigenvector'])
            
            # 确定无功补偿量
            self._calculate_reactive_compensation(snb_result['voltage_profile'])
    
    def _calculate_snb_point(self) -> Dict[str, Any]:
        """
        计算鞍节分岔点（SNB点）
        
        返回:
            Dict[str, Any]: SNB点计算结果
        """
        logger.info("计算SNB点及左特征向量...")
        
        # 准备网络数据
        network_data = self._prepare_network_data()
        bus_names = network_data['bus_names']
        n_buses = len(bus_names)
        
        # 计算导纳矩阵
        Y = self._calculate_admittance_matrix(network_data)
        
        # 初始化电压幅值和相角（使用扩展潮流计算的结果）
        v_mag = np.ones(n_buses)
        v_ang = np.zeros(n_buses)
        
        # 确定节点类型
        node_types = []
        for bus_name in bus_names:
            is_kv_node = any(kv_node.node_name == bus_name for kv_node in self.kv_nodes)
            if is_kv_node:
                node_types.append('KV')
            elif any(gen.bus.name == bus_name and gen.parameters.get('control', '') == 'SLACK' for gen in network_data['generators']):
                node_types.append('SLACK')
            elif any(gen.bus.name == bus_name and gen.parameters.get('control', '') == 'PV' for gen in network_data['generators']):
                node_types.append('PV')
            else:
                node_types.append('PQ')
        
        # 计算实际的雅可比矩阵
        J = self._calculate_extended_jacobian(Y, v_mag, v_ang, network_data, node_types)
        
        # 计算雅可比矩阵的特征值和左特征向量
        eigenvalues, eigenvectors = eig(J)
        
        # 找到最小实部的特征值
        min_idx = np.argmin(eigenvalues.real)
        left_eigenvector = eigenvectors[:, min_idx].real
        
        # 单位化左特征向量
        left_eigenvector = left_eigenvector / np.linalg.norm(left_eigenvector)
        
        # 计算实际的电压分布
        _, q_inj = self._calculate_injected_power(Y, v_mag, v_ang)
        voltage_profile = v_mag.tolist()
        
        return {
            'eigenvalues': eigenvalues.tolist(),
            'left_eigenvector': left_eigenvector.tolist(),
            'voltage_profile': voltage_profile
        }
    
    def _calculate_generator_adjustments(self, left_eigenvector: List[float]) -> None:
        """
        计算发电机出力调整量
        
        参数:
            left_eigenvector: 左特征向量
        """
        network_data = self._prepare_network_data()
        
        # 识别实际的发电机节点
        generator_nodes = []
        generator_names = []
        for gen in network_data['generators']:
            control = gen.parameters.get('control', '')
            if control in ['PV', 'SLACK']:  # 只考虑PV和平衡节点的发电机
                bus_name = gen.bus.name
                bus_idx = network_data['bus_names'].index(bus_name)
                generator_nodes.append(bus_idx)
                generator_names.append(gen.name)
        
        # 计算总有功缺额（基于KV节点的功率调整）
        total_p_need = 0.0
        for kv_node in self.kv_nodes:
            # 简化计算，假设每个KV节点贡献1 MW的有功缺额
            total_p_need += 1.0
        
        # 基于左特征向量计算发电机出力调整量
        for i, (gen_name, bus_idx) in enumerate(zip(generator_names, generator_nodes)):
            if bus_idx < len(left_eigenvector):
                # 使用左特征向量对应位置的分量
                weight = left_eigenvector[bus_idx] ** 2
                adjustment = weight * total_p_need
                self.generator_adjustments[gen_name] = adjustment
                logger.info(f"发电机 {gen_name} 出力调整量: {adjustment:.2f} MW")
    
    def _calculate_reactive_compensation(self, voltage_profile: List[float]) -> None:
        """
        计算无功补偿量
        
        参数:
            voltage_profile: 电压分布
        """
        network_data = self._prepare_network_data()
        bus_names = network_data['bus_names']
        
        # 基于实际电压分布计算无功补偿量
        for bus_idx, (bus_name, voltage) in enumerate(zip(bus_names, voltage_profile)):
            # 低于0.95 pu的节点需要无功补偿
            if voltage < 0.95:
                # 每0.01 pu电压需要10 MVar补偿
                compensation = (0.95 - voltage) * 1000  # 转换为每0.01 pu对应10 MVar
                self.reactive_compensation[bus_name] = compensation
                logger.info(f"母线 {bus_name} 电压: {voltage:.3f} pu, 无功补偿量: {compensation:.2f} MVar")
            elif voltage > 1.05:
                # 高于1.05 pu的节点需要减少无功补偿
                compensation = (1.05 - voltage) * 1000
                self.reactive_compensation[bus_name] = compensation
                logger.info(f"母线 {bus_name} 电压: {voltage:.3f} pu, 无功调整量: {compensation:.2f} MVar")
    
    def _prepare_network_data(self) -> Dict[str, Any]:
        """
        准备网络数据
        
        返回:
            Dict[str, Any]: 网络数据字典
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
    
    def _calculate_power_mismatch(self, Y: csr_matrix, v_mag: np.ndarray, v_ang: np.ndarray, 
                                 network_data: Dict[str, Any], node_types: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算功率不平衡量
        
        参数:
            Y: 导纳矩阵
            v_mag: 电压幅值向量
            v_ang: 电压相角向量
            network_data: 网络数据字典
            node_types: 节点类型列表
            
        返回:
            Tuple[np.ndarray, np.ndarray]: 有功功率不平衡量和无功功率不平衡量
        """
        n_buses = len(v_mag)
        p_mismatch = np.zeros(n_buses)
        q_mismatch = np.zeros(n_buses)
        
        # 计算各节点的注入功率
        p_inj, q_inj = self._calculate_injected_power(Y, v_mag, v_ang)
        
        # 计算各节点的有功和无功功率设定值
        p_set = np.zeros(n_buses)
        q_set = np.zeros(n_buses)
        
        for gen in network_data['generators']:
            bus_idx = network_data['bus_names'].index(gen.bus.name)
            p_set[bus_idx] += gen.parameters.get('power_set', 0.0)
        
        for load in network_data['loads']:
            bus_idx = network_data['bus_names'].index(load.bus.name)
            demand = load.parameters.get('demand', 0.0)
            p_set[bus_idx] -= demand
            # 简化处理，假设功率因数为1
            q_set[bus_idx] -= demand * 0.2
        
        # 计算功率不平衡量
        for i in range(n_buses):
            bus_name = network_data['bus_names'][i]
            node_type = node_types[i]
            
            if node_type == 'KV':
                # KV节点：使用功率下垂方程
                kv_node = next(kv for kv in self.kv_nodes if kv.node_name == bus_name)
                # 计算KV节点的功率不平衡量
                p_mismatch[i] = p_inj[i] - kv_node.p_c - kv_node.k_coefficient * (q_inj[i] - kv_node.q_c)
                # KV节点的电压设定值
                q_mismatch[i] = v_mag[i] - kv_node.u_set
            elif node_type == 'PQ':
                # PQ节点：有功和无功都不平衡
                p_mismatch[i] = p_inj[i] - p_set[i]
                q_mismatch[i] = q_inj[i] - q_set[i]
            elif node_type == 'PV':
                # PV节点：只有有功不平衡，无功由系统决定
                p_mismatch[i] = p_inj[i] - p_set[i]
                # PV节点的电压设定值（假设为1.0）
                q_mismatch[i] = v_mag[i] - 1.0
            elif node_type == 'SLACK':
                # 平衡节点：有功和无功都不参与不平衡计算
                p_mismatch[i] = 0.0
                q_mismatch[i] = 0.0
        
        return p_mismatch, q_mismatch
    
    def _calculate_extended_jacobian(self, Y: csr_matrix, v_mag: np.ndarray, v_ang: np.ndarray, 
                                   network_data: Dict[str, Any], node_types: List[str]) -> np.ndarray:
        """
        计算扩展雅可比矩阵
        
        参数:
            Y: 导纳矩阵
            v_mag: 电压幅值向量
            v_ang: 电压相角向量
            network_data: 网络数据字典
            node_types: 节点类型列表
            
        返回:
            np.ndarray: 扩展雅可比矩阵
        """
        n_buses = len(v_mag)
        J = np.zeros((2 * n_buses, 2 * n_buses))
        
        # 构建导纳矩阵的实部和虚部
        Y_real = Y.real
        Y_imag = Y.imag
        
        for i in range(n_buses):
            for j in range(n_buses):
                if i == j:
                    # 自导纳项
                    H_ii = -v_mag[i] ** 2 * Y_imag[i, i]
                    N_ii = v_mag[i] ** 2 * Y_real[i, i]
                    J_ii = -v_mag[i] * Y_imag[i, i]
                    L_ii = v_mag[i] * Y_real[i, i]
                else:
                    # 互导纳项
                    delta_ang = v_ang[i] - v_ang[j]
                    Y_ij = Y[i, j]
                    Y_mag = np.abs(Y_ij)
                    Y_ang = np.angle(Y_ij)
                    
                    H_ij = v_mag[i] * v_mag[j] * Y_mag * np.sin(Y_ang - delta_ang)
                    N_ij = -v_mag[i] * v_mag[j] * Y_mag * np.cos(Y_ang - delta_ang)
                    J_ij = v_mag[i] * Y_mag * np.sin(Y_ang - delta_ang)
                    L_ij = v_mag[i] * Y_mag * np.cos(Y_ang - delta_ang)
                
                # 填充雅可比矩阵
                if i != j:
                    J[i, j] = H_ij  # dP_i/dθ_j
                    J[i, n_buses + j] = J_ij  # dP_i/dV_j
                    J[n_buses + i, j] = N_ij  # dQ_i/dθ_j
                    J[n_buses + i, n_buses + j] = L_ij  # dQ_i/dV_j
                else:
                    J[i, i] = H_ii  # dP_i/dθ_i
                    J[i, n_buses + i] = J_ii  # dP_i/dV_i
                    J[n_buses + i, i] = N_ii  # dQ_i/dθ_i
                    J[n_buses + i, n_buses + i] = L_ii  # dQ_i/dV_i
        
        # 修改KV节点的雅可比矩阵项
        for i in range(n_buses):
            bus_name = network_data['bus_names'][i]
            if node_types[i] == 'KV':
                kv_node = next(kv for kv in self.kv_nodes if kv.node_name == bus_name)
                k = kv_node.k_coefficient
                
                # KV节点的有功方程：d(P - KQ)/dθ 和 d(P - KQ)/dV
                for j in range(n_buses):
                    J[i, j] = J[i, j] - k * J[n_buses + i, j]  # d(P-KQ)/dθ_j = dP/dθ_j - K*dQ/dθ_j
                    J[i, n_buses + j] = J[i, n_buses + j] - k * J[n_buses + i, n_buses + j]  # d(P-KQ)/dV_j = dP/dV_j - K*dQ/dV_j
                
                # KV节点的无功方程：d(U - U_set)/dθ 和 d(U - U_set)/dV
                for j in range(n_buses):
                    J[n_buses + i, j] = 0.0  # dU/dθ_j = 0
                J[n_buses + i, n_buses + i] = 1.0  # dU/dV_i = 1
        
        return J
    
    def _calculate_injected_power(self, Y: csr_matrix, v_mag: np.ndarray, v_ang: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算节点注入功率
        
        参数:
            Y: 导纳矩阵
            v_mag: 电压幅值向量
            v_ang: 电压相角向量
            
        返回:
            Tuple[np.ndarray, np.ndarray]: 有功功率和无功功率注入向量
        """
        n_buses = len(v_mag)
        p_inj = np.zeros(n_buses)
        q_inj = np.zeros(n_buses)
        
        for i in range(n_buses):
            p = 0.0
            q = 0.0
            for j in range(n_buses):
                delta_ang = v_ang[i] - v_ang[j]
                Y_ij = Y[i, j]
                Y_mag = np.abs(Y_ij)
                Y_ang = np.angle(Y_ij)
                
                p += v_mag[i] * v_mag[j] * Y_mag * np.cos(Y_ang - delta_ang)
                q += v_mag[i] * v_mag[j] * Y_mag * np.sin(Y_ang - delta_ang)
            
            p_inj[i] = p
            q_inj[i] = q
        
        return p_inj, q_inj
    
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


def create_extended_power_flow_solver(network: PyXESXXNNetwork, **kwargs) -> ExtendedPowerFlowSolver:
    """
    创建扩展潮流计算求解器
    
    参数:
        network: PyXESXXN网络对象
        **kwargs: 其他配置参数
        
    返回:
        ExtendedPowerFlowSolver: 扩展潮流计算求解器
    """
    return ExtendedPowerFlowSolver(network, **kwargs)


def run_extended_power_flow_analysis(network: PyXESXXNNetwork, **kwargs) -> Tuple[ExtendedPowerFlowResult, Any]:
    """
    运行扩展潮流计算分析
    
    参数:
        network: PyXESXXN网络对象
        **kwargs: 其他配置参数
        
    返回:
        Tuple[ExtendedPowerFlowResult, Any]: (扩展潮流计算结果, 分析对象)
    """
    solver = create_extended_power_flow_solver(network, **kwargs)
    result = solver.solve()
    
    # 这里可以添加分析对象
    analysis = None
    
    return result, analysis


# 导出公共API
__all__ = [
    'ExtendedPowerFlowResult',
    'PowerSagNode',
    'ExtendedPowerFlowSolver',
    'create_extended_power_flow_solver',
    'run_extended_power_flow_analysis'
]