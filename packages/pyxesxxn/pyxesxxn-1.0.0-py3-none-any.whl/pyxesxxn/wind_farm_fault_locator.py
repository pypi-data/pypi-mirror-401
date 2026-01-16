"""
基于双层负序差值与负序测距的风电场集电线不对称故障定位模块

该模块实现了针对风电场集电线不对称故障的定位功能，通过风机负序建模与网络等效，
利用双层负序差值识别故障区域，再基于双端负序量推导测距公式，实现各类不对称故障的精准定位。
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Set, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass
import numpy as np
import pandas as pd
from pyxesxxn.topology_metering_fusion import TopologyMeteringFusion, DistributionNode, DistributionBranch, DistributionSwitch


class FaultType(Enum):
    """故障类型枚举"""
    SINGLE_PHASE_TO_GROUND = 0  # 单相接地故障
    TWO_PHASE_SHORT_CIRCUIT = 1  # 两相短路故障
    TWO_PHASE_TO_GROUND = 2  # 两相接地故障
    UNKNOWN = 3  # 未知故障


class WindTurbineType(Enum):
    """风机类型枚举"""
    DFIG = 0  # 双馈风机
    PMSG = 1  # 永磁直驱风机
    SCSG = 2  # 鼠笼式异步风机


@dataclass
class WindTurbine:
    """风机类"""
    wt_id: str
    node_id: str  # 连接的节点
    capacity: float  # 容量(kW)
    wt_type: WindTurbineType  # 风机类型
    negative_sequence_impedance: complex  # 负序阻抗(Ω)
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class NegativeSequenceMeasurement:
    """负序量测数据类"""
    node_id: str  # 节点ID
    voltage: complex  # 负序电压(V)
    current: complex  # 负序电流(A)
    timestamp: pd.Timestamp  # 量测时间
    quality: float = 1.0  # 数据质量(0-1)


@dataclass
class FaultLocationResult:
    """故障定位结果类"""
    fault_distance: float  # 故障距离(km)
    fault_nodes: Tuple[str, str]  # 故障区域的两个节点
    fault_type: FaultType  # 故障类型
    confidence: float  # 定位置信度
    calculation_time: float  # 计算时间(ms)
    first_node_confidence: float  # 第一节点识别置信度
    second_node_confidence: float  # 第二节点识别置信度


class WindFarmNegativeSequenceNetwork:
    """风电场负序网络类"""
    
    def __init__(self, fusion_module: TopologyMeteringFusion):
        """初始化风电场负序网络
        
        Parameters
        ----------
        fusion_module : TopologyMeteringFusion
            拓扑-量测数据融合模块实例
        """
        self.fusion_module = fusion_module
        self.wind_turbines: Dict[str, WindTurbine] = {}  # 风机字典
        self.negative_sequence_measurements: List[NegativeSequenceMeasurement] = []  # 负序量测数据
        self.node_impedance_matrix: Optional[np.ndarray] = None  # 节点阻抗矩阵
        self.node_mapping: Dict[str, int] = {}  # 节点ID到矩阵索引的映射
        
        # 网络等效参数
        self.equivalent_impedance: float = 100.0  # 等效阻抗(Ω)
        
    def add_wind_turbine(self, wt: WindTurbine) -> None:
        """添加风机
        
        Parameters
        ----------
        wt : WindTurbine
            风机实例
        """
        if wt.wt_id in self.wind_turbines:
            raise ValueError(f"风机 {wt.wt_id} 已存在")
        if wt.node_id not in self.fusion_module.nodes:
            raise ValueError(f"节点 {wt.node_id} 不存在")
        self.wind_turbines[wt.wt_id] = wt
    
    def add_negative_sequence_measurement(self, measurement: NegativeSequenceMeasurement) -> None:
        """添加负序量测数据
        
        Parameters
        ----------
        measurement : NegativeSequenceMeasurement
            负序量测数据实例
        """
        if measurement.node_id not in self.fusion_module.nodes:
            raise ValueError(f"节点 {measurement.node_id} 不存在")
        self.negative_sequence_measurements.append(measurement)
    
    def build_negative_sequence_network(self) -> None:
        """构建负序网络"""
        # 构建节点映射
        nodes = list(self.fusion_module.nodes.keys())
        self.node_mapping = {node_id: idx for idx, node_id in enumerate(nodes)}
        
        # 初始化节点阻抗矩阵
        n_nodes = len(nodes)
        self.node_impedance_matrix = np.zeros((n_nodes, n_nodes), dtype=complex)
        
        # 添加线路阻抗
        for branch_id, branch in self.fusion_module.branches.items():
            from_idx = self.node_mapping[branch.from_node]
            to_idx = self.node_mapping[branch.to_node]
            
            # 计算线路阻抗（简化实现：使用电阻和电抗）
            line_impedance = complex(branch.resistance * branch.length, branch.reactance * branch.length)
            
            # 更新节点阻抗矩阵
            self.node_impedance_matrix[from_idx, to_idx] += line_impedance
            self.node_impedance_matrix[to_idx, from_idx] += line_impedance
            self.node_impedance_matrix[from_idx, from_idx] += line_impedance
            self.node_impedance_matrix[to_idx, to_idx] += line_impedance
        
        # 添加风机负序阻抗（等效到节点）
        for wt_id, wt in self.wind_turbines.items():
            node_idx = self.node_mapping[wt.node_id]
            self.node_impedance_matrix[node_idx, node_idx] += wt.negative_sequence_impedance
    
    def calculate_negative_sequence_voltage(self, currents: np.ndarray) -> np.ndarray:
        """计算负序网络电压
        
        Parameters
        ----------
        currents : np.ndarray
            注入电流数组
        
        Returns
        -------
        np.ndarray
            节点负序电压数组
        """
        if self.node_impedance_matrix is None:
            self.build_negative_sequence_network()
        
        return np.dot(self.node_impedance_matrix, currents)
    
    def equivalent_network(self, region_nodes: List[str]) -> complex:
        """网络等效
        
        Parameters
        ----------
        region_nodes : List[str]
            区域节点列表
        
        Returns
        -------
        complex
            等效阻抗
        """
        # 简化实现：返回等效阻抗
        return complex(self.equivalent_impedance, 0.0)


class FaultRegionIdentifier:
    """故障区域识别类"""
    
    def __init__(self, negative_sequence_network: WindFarmNegativeSequenceNetwork):
        """初始化故障区域识别器
        
        Parameters
        ----------
        negative_sequence_network : WindFarmNegativeSequenceNetwork
            风电场负序网络实例
        """
        self.network = negative_sequence_network
    
    def identify_first_node(self) -> Tuple[str, float]:
        """识别第一节点
        
        Returns
        -------
        Tuple[str, float]
            第一节点ID和置信度
        """
        if not self.network.negative_sequence_measurements:
            raise ValueError("没有负序量测数据")
        
        # 获取实际故障负序电压
        actual_voltages = {}
        for measurement in self.network.negative_sequence_measurements:
            actual_voltages[measurement.node_id] = measurement.voltage
        
        # 模拟各节点故障，计算负序电压差值
        min_norm = float('inf')
        first_node = list(self.network.fusion_module.nodes.keys())[0]
        
        for node_id in self.network.fusion_module.nodes.keys():
            # 模拟该节点发生故障
            simulated_voltages = self._simulate_fault(node_id)
            
            # 计算负序电压差值
            delta_u = []
            for measurement in self.network.negative_sequence_measurements:
                if measurement.node_id in simulated_voltages and simulated_voltages[measurement.node_id] != 0:
                    diff = (actual_voltages[measurement.node_id] - simulated_voltages[measurement.node_id]) / simulated_voltages[measurement.node_id]
                    delta_u.append(diff)
            
            # 计算2范数
            norm = np.linalg.norm(delta_u)
            
            # 更新最小范数和第一节点
            if norm < min_norm:
                min_norm = norm
                first_node = node_id
        
        # 计算置信度（范数越小，置信度越高）
        confidence = 1.0 / (1.0 + min_norm)
        
        return first_node, confidence
    
    def identify_second_node(self, first_node: str) -> Tuple[str, float]:
        """识别第二节点
        
        Parameters
        ----------
        first_node : str
            第一节点ID
        
        Returns
        -------
        Tuple[str, float]
            第二节点ID和置信度
        """
        if not self.network.negative_sequence_measurements:
            raise ValueError("没有负序量测数据")
        
        # 获取相邻节点
        adjacent_nodes = self._get_adjacent_nodes(first_node)
        if not adjacent_nodes:
            # 没有相邻节点，返回自身
            return first_node, 1.0
        
        # 计算负序电压比差值
        min_ratio_diff = float('inf')
        second_node = adjacent_nodes[0]
        
        for node in adjacent_nodes:
            # 计算负序电压比差值
            ratio_diff = self._calculate_voltage_ratio_diff(first_node, node)
            
            # 更新最小比值差和第二节点
            if ratio_diff < min_ratio_diff:
                min_ratio_diff = ratio_diff
                second_node = node
        
        # 计算置信度
        confidence = 1.0 / (1.0 + min_ratio_diff)
        
        return second_node, confidence
    
    def _simulate_fault(self, fault_node: str) -> Dict[str, complex]:
        """模拟故障
        
        Parameters
        ----------
        fault_node : str
            故障节点ID
        
        Returns
        -------
        Dict[str, complex]
            模拟故障后的负序电压
        """
        # 简化实现：假设故障电流为100A
        fault_current = 100.0
        
        # 构建注入电流数组
        n_nodes = len(self.network.node_mapping)
        currents = np.zeros(n_nodes, dtype=complex)
        fault_idx = self.network.node_mapping[fault_node]
        currents[fault_idx] = complex(fault_current, 0.0)
        
        # 计算负序电压
        voltages = self.network.calculate_negative_sequence_voltage(currents)
        
        # 转换为字典
        voltage_dict = {}
        for node_id, idx in self.network.node_mapping.items():
            voltage_dict[node_id] = voltages[idx]
        
        return voltage_dict
    
    def _get_adjacent_nodes(self, node_id: str) -> List[str]:
        """获取相邻节点
        
        Parameters
        ----------
        node_id : str
            节点ID
        
        Returns
        -------
        List[str]
            相邻节点列表
        """
        adjacent_nodes = []
        
        # 遍历所有支路，查找相邻节点
        for branch_id, branch in self.network.fusion_module.branches.items():
            if branch.from_node == node_id:
                adjacent_nodes.append(branch.to_node)
            elif branch.to_node == node_id:
                adjacent_nodes.append(branch.from_node)
        
        return adjacent_nodes
    
    def _calculate_voltage_ratio_diff(self, node1: str, node2: str) -> float:
        """计算负序电压比差值
        
        Parameters
        ----------
        node1 : str
            节点1 ID
        node2 : str
            节点2 ID
        
        Returns
        -------
        float
            负序电压比差值
        """
        # 获取实际量测数据
        actual_voltages = {}
        for measurement in self.network.negative_sequence_measurements:
            actual_voltages[measurement.node_id] = measurement.voltage
        
        # 模拟故障
        simulated_voltages_node1 = self._simulate_fault(node1)
        simulated_voltages_node2 = self._simulate_fault(node2)
        
        # 计算实际电压比和模拟电压比
        if node1 in actual_voltages and node2 in actual_voltages and actual_voltages[node2] != 0:
            actual_ratio = actual_voltages[node1] / actual_voltages[node2]
        else:
            actual_ratio = 1.0
        
        if node1 in simulated_voltages_node1 and node2 in simulated_voltages_node1 and simulated_voltages_node1[node2] != 0:
            simulated_ratio = simulated_voltages_node1[node1] / simulated_voltages_node1[node2]
        else:
            simulated_ratio = 1.0
        
        # 计算差值
        ratio_diff = abs(actual_ratio - simulated_ratio)
        
        return ratio_diff
    
    def identify_fault_region(self) -> Tuple[Tuple[str, str], float, float]:
        """识别故障区域
        
        Returns
        -------
        Tuple[Tuple[str, str], float, float]
            故障区域的两个节点ID，第一节点置信度和第二节点置信度
        """
        # 识别第一节点
        first_node, first_confidence = self.identify_first_node()
        
        # 识别第二节点
        second_node, second_confidence = self.identify_second_node(first_node)
        
        # 处理故障点接近分支引出点的情况
        if first_node == second_node:
            # 在第一节点附近搜索故障
            adjacent_nodes = self._get_adjacent_nodes(first_node)
            if adjacent_nodes:
                second_node = adjacent_nodes[0]
        
        return (first_node, second_node), first_confidence, second_confidence


class FaultDistanceCalculator:
    """故障测距类"""
    
    def __init__(self, negative_sequence_network: WindFarmNegativeSequenceNetwork):
        """初始化故障测距器
        
        Parameters
        ----------
        negative_sequence_network : WindFarmNegativeSequenceNetwork
            风电场负序网络实例
        """
        self.network = negative_sequence_network
        self.wave_speed: float = 2.5e5  # 行波波速(km/s)
    
    def calculate_fault_distance(self, fault_nodes: Tuple[str, str]) -> float:
        """计算故障距离
        
        Parameters
        ----------
        fault_nodes : Tuple[str, str]
            故障区域的两个节点
        
        Returns
        -------
        float
            故障距离(km)
        """
        node1, node2 = fault_nodes
        
        # 获取这两个节点的负序量测数据
        measurements = {}
        for measurement in self.network.negative_sequence_measurements:
            if measurement.node_id in fault_nodes:
                measurements[measurement.node_id] = measurement
        
        if len(measurements) < 2:
            # 简化实现：返回两个节点之间距离的一半
            branch_length = self._get_branch_length(node1, node2)
            return branch_length / 2
        
        # 获取双端负序电压和电流
        u2 = measurements[node1].voltage
        i2 = measurements[node1].current
        u4 = measurements[node2].voltage
        i4 = measurements[node2].current
        
        # 获取线路阻抗参数
        branch_length = self._get_branch_length(node1, node2)
        branch = self._get_branch(node1, node2)
        
        if branch is None:
            return branch_length / 2
        
        # 计算单位长度线路阻抗
        z = complex(branch.resistance, branch.reactance)  # Ω/km
        
        # 构建测距方程：|U2 - I2 * l * z|² = |U4 + I4 * (L - l) * z|²
        # 展开并求解一元二次方程
        L = branch_length
        
        # 计算各项系数
        a = abs(i2 * z + i4 * z) ** 2
        b = -2 * np.real( (u2 - u4 - i4 * L * z) * np.conj(i2 * z + i4 * z) )
        c = abs(u2 - u4 - i4 * L * z) ** 2
        
        # 求解一元二次方程 ax² + bx + c = 0
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            # 无实数解，返回两个节点之间距离的一半
            return branch_length / 2
        
        # 计算两个解
        sqrt_discriminant = np.sqrt(discriminant)
        l1 = (-b + sqrt_discriminant) / (2*a)
        l2 = (-b - sqrt_discriminant) / (2*a)
        
        # 选择在0到L之间的解
        valid_solutions = [l for l in [l1, l2] if 0 <= l <= L]
        
        if valid_solutions:
            return min(valid_solutions)
        else:
            # 没有有效解，返回两个节点之间距离的一半
            return branch_length / 2
    
    def _get_branch_length(self, node1: str, node2: str) -> float:
        """获取两个节点之间的支路长度
        
        Parameters
        ----------
        node1 : str
            节点1 ID
        node2 : str
            节点2 ID
        
        Returns
        -------
        float
            支路长度(km)
        """
        branch = self._get_branch(node1, node2)
        if branch:
            return branch.length
        else:
            return 0.0
    
    def _get_branch(self, node1: str, node2: str) -> Optional[DistributionBranch]:
        """获取两个节点之间的支路
        
        Parameters
        ----------
        node1 : str
            节点1 ID
        node2 : str
            节点2 ID
        
        Returns
        -------
        Optional[DistributionBranch]
            支路对象
        """
        for branch_id, branch in self.network.fusion_module.branches.items():
            if (branch.from_node == node1 and branch.to_node == node2) or \
               (branch.from_node == node2 and branch.to_node == node1):
                return branch
        return None


class WindFarmFaultLocator:
    """风电场集电线故障定位器"""
    
    def __init__(self, fusion_module: TopologyMeteringFusion):
        """初始化风电场故障定位器
        
        Parameters
        ----------
        fusion_module : TopologyMeteringFusion
            拓扑-量测数据融合模块实例
        """
        self.fusion_module = fusion_module
        self.negative_sequence_network = WindFarmNegativeSequenceNetwork(fusion_module)
        self.region_identifier = FaultRegionIdentifier(self.negative_sequence_network)
        self.distance_calculator = FaultDistanceCalculator(self.negative_sequence_network)
        self.fault_type: FaultType = FaultType.UNKNOWN
    
    def add_wind_turbine(self, wt: WindTurbine) -> None:
        """添加风机
        
        Parameters
        ----------
        wt : WindTurbine
            风机实例
        """
        self.negative_sequence_network.add_wind_turbine(wt)
    
    def add_negative_sequence_measurement(self, measurement: NegativeSequenceMeasurement) -> None:
        """添加负序量测数据
        
        Parameters
        ----------
        measurement : NegativeSequenceMeasurement
            负序量测数据实例
        """
        self.negative_sequence_network.add_negative_sequence_measurement(measurement)
    
    def set_fault_type(self, fault_type: FaultType) -> None:
        """设置故障类型
        
        Parameters
        ----------
        fault_type : FaultType
            故障类型
        """
        self.fault_type = fault_type
    
    def locate_fault(self) -> FaultLocationResult:
        """执行故障定位
        
        Returns
        -------
        FaultLocationResult
            故障定位结果
        """
        import time
        start_time = time.time()
        
        # 构建负序网络
        self.negative_sequence_network.build_negative_sequence_network()
        
        # 识别故障区域
        fault_nodes, first_confidence, second_confidence = self.region_identifier.identify_fault_region()
        
        # 计算故障距离
        fault_distance = self.distance_calculator.calculate_fault_distance(fault_nodes)
        
        # 计算总置信度
        confidence = (first_confidence + second_confidence) / 2
        
        # 计算耗时
        calculation_time = (time.time() - start_time) * 1000  # 转换为ms
        
        # 构建结果
        result = FaultLocationResult(
            fault_distance=fault_distance,
            fault_nodes=fault_nodes,
            fault_type=self.fault_type,
            confidence=confidence,
            calculation_time=calculation_time,
            first_node_confidence=first_confidence,
            second_node_confidence=second_confidence
        )
        
        return result


# 工具函数
def create_sample_wind_farm_locator() -> WindFarmFaultLocator:
    """创建示例风电场故障定位器
    
    Returns
    -------
    WindFarmFaultLocator
        示例故障定位器
    """
    # 创建拓扑-量测融合模块
    from pyxesxxn.topology_metering_fusion import create_sample_distribution_network
    fusion = create_sample_distribution_network()
    
    # 创建故障定位器
    locator = WindFarmFaultLocator(fusion)
    
    # 添加风机
    from pyxesxxn.wind_farm_fault_locator import WindTurbine, WindTurbineType
    
    # 添加双馈风机
    locator.add_wind_turbine(WindTurbine(
        wt_id="wt1",
        node_id="load1",
        capacity=2000.0,
        wt_type=WindTurbineType.DFIG,
        negative_sequence_impedance=complex(100.0, 50.0)
    ))
    
    locator.add_wind_turbine(WindTurbine(
        wt_id="wt2",
        node_id="load2",
        capacity=2000.0,
        wt_type=WindTurbineType.DFIG,
        negative_sequence_impedance=complex(100.0, 50.0)
    ))
    
    # 添加负序量测数据
    from pyxesxxn.wind_farm_fault_locator import NegativeSequenceMeasurement
    import pandas as pd
    
    # 创建示例负序量测数据
    timestamp = pd.Timestamp.now()
    
    # 添加节点1的量测数据
    locator.add_negative_sequence_measurement(NegativeSequenceMeasurement(
        node_id="transformer1",
        voltage=complex(100.0, 50.0),
        current=complex(10.0, 5.0),
        timestamp=timestamp
    ))
    
    # 添加节点2的量测数据
    locator.add_negative_sequence_measurement(NegativeSequenceMeasurement(
        node_id="load1",
        voltage=complex(80.0, 40.0),
        current=complex(8.0, 4.0),
        timestamp=timestamp
    ))
    
    # 添加节点3的量测数据
    locator.add_negative_sequence_measurement(NegativeSequenceMeasurement(
        node_id="load2",
        voltage=complex(60.0, 30.0),
        current=complex(6.0, 3.0),
        timestamp=timestamp
    ))
    
    # 设置故障类型
    locator.set_fault_type(FaultType.SINGLE_PHASE_TO_GROUND)
    
    return locator


def generate_sample_negative_sequence_measurements() -> List[NegativeSequenceMeasurement]:
    """生成示例负序量测数据
    
    Returns
    -------
    List[NegativeSequenceMeasurement]
        示例负序量测数据列表
    """
    from pyxesxxn.wind_farm_fault_locator import NegativeSequenceMeasurement
    import pandas as pd
    
    timestamp = pd.Timestamp.now()
    
    # 创建示例负序量测数据
    measurements = [
        NegativeSequenceMeasurement(
            node_id="node1",
            voltage=complex(100.0, 50.0),
            current=complex(10.0, 5.0),
            timestamp=timestamp
        ),
        NegativeSequenceMeasurement(
            node_id="node2",
            voltage=complex(80.0, 40.0),
            current=complex(8.0, 4.0),
            timestamp=timestamp
        ),
        NegativeSequenceMeasurement(
            node_id="node3",
            voltage=complex(60.0, 30.0),
            current=complex(6.0, 3.0),
            timestamp=timestamp
        )
    ]
    
    return measurements
