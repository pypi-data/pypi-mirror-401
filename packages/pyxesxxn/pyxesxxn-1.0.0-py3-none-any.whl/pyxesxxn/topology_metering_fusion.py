"""配电网拓扑-量测数据融合模块 (Topology-Metering Fusion Module)

该模块将配电网拓扑结构（节点、支路、开关、中性点接地方式）与实时量测数据
（电压、电流、功率、零序电流等，采样频率≥1Hz）进行结构化融合，构建并输出
包含静态拓扑属性+动态时序特征的图数据结构，为后续GNN等模型提供输入。

核心功能：
- 支持多种中性点接地方式（不接地、消弧线圈接地等）的拓扑建模
- 处理量测噪声、数据缺失（如插值、前向填充）
- 将数据转换为图神经网络（GNN）可识别的节点/边特征格式
"""

from __future__ import annotations
from typing import Dict, List, Optional, Union, Any, Tuple
from enum import Enum
import pandas as pd
import numpy as np
from dataclasses import dataclass
import networkx as nx
from scipy import interpolate
from sklearn.preprocessing import StandardScaler


class NeutralGroundingType(Enum):
    """中性点接地方式枚举"""
    UNGROUNDED = "ungrounded"  # 不接地
    PETERSON_COIL = "peterson_coil"  # 消弧线圈接地
    RESISTANCE_GROUNDED = "resistance_grounded"  # 电阻接地
    SOLIDLY_GROUNDED = "solidly_grounded"  # 直接接地


class SwitchType(Enum):
    """开关类型枚举"""
    CIRCUIT_BREAKER = "circuit_breaker"  # 断路器
    DISCONNECTOR = "disconnector"  # 隔离开关
    LOAD_BREAK_SWITCH = "load_break_switch"  # 负荷开关
    RECLOSER = "recloser"  # 重合器


class MeasurementType(Enum):
    """量测类型枚举"""
    VOLTAGE = "voltage"  # 电压
    CURRENT = "current"  # 电流
    ACTIVE_POWER = "active_power"  # 有功功率
    REACTIVE_POWER = "reactive_power"  # 无功功率
    ZERO_SEQUENCE_CURRENT = "zero_sequence_current"  # 零序电流
    FREQUENCY = "frequency"  # 频率


@dataclass
class DistributionNode:
    """配电网节点类"""
    node_id: str
    node_type: str  # 变电站、配电变压器、负荷节点等
    voltage_level: float  # 电压等级(kV)
    coordinates: Optional[Tuple[float, float]] = None  # 地理坐标
    capacity: Optional[float] = None  # 容量(kVA)
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class DistributionBranch:
    """配电网支路类"""
    branch_id: str
    from_node: str
    to_node: str
    branch_type: str  # 架空线、电缆等
    length: float  # 长度(km)
    resistance: float  # 电阻(Ω/km)
    reactance: float  # 电抗(Ω/km)
    susceptance: float  # 电纳(S/km)
    capacity: float  # 容量(kVA)
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class DistributionSwitch:
    """配电网开关类"""
    switch_id: str
    switch_type: SwitchType
    connected_nodes: List[str]  # 连接的节点
    status: bool  # 开关状态(True=闭合, False=断开)
    location: Optional[str] = None  # 位置描述
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class MeasurementData:
    """量测数据类"""
    measurement_id: str
    measurement_type: MeasurementType
    node_id: str  # 关联的节点
    timestamp: pd.Timestamp
    value: float
    quality: float = 1.0  # 数据质量(0-1)
    unit: str = ""


class TopologyMeteringFusion:
    """配电网拓扑-量测数据融合类"""
    
    def __init__(self, network_name: str = "Distribution Network"):
        """初始化融合模块
        
        Parameters
        ----------
        network_name : str, default="Distribution Network"
            网络名称
        """
        self.network_name = network_name
        self.nodes: Dict[str, DistributionNode] = {}
        self.branches: Dict[str, DistributionBranch] = {}
        self.switches: Dict[str, DistributionSwitch] = {}
        self.measurements: List[MeasurementData] = []
        self.grounding_type: NeutralGroundingType = NeutralGroundingType.UNGROUNDED
        self.graph: Optional[nx.Graph] = None
        
        # 数据预处理工具
        self.scaler = StandardScaler()
        self.interpolation_method = 'linear'
    
    def add_node(self, node: DistributionNode) -> None:
        """添加节点
        
        Parameters
        ----------
        node : DistributionNode
            配电网节点
        """
        if node.node_id in self.nodes:
            raise ValueError(f"节点 {node.node_id} 已存在")
        self.nodes[node.node_id] = node
    
    def add_branch(self, branch: DistributionBranch) -> None:
        """添加支路
        
        Parameters
        ----------
        branch : DistributionBranch
            配电网支路
        """
        if branch.branch_id in self.branches:
            raise ValueError(f"支路 {branch.branch_id} 已存在")
        
        # 验证节点存在性
        if branch.from_node not in self.nodes:
            raise ValueError(f"起始节点 {branch.from_node} 不存在")
        if branch.to_node not in self.nodes:
            raise ValueError(f"终止节点 {branch.to_node} 不存在")
        
        self.branches[branch.branch_id] = branch
    
    def add_switch(self, switch: DistributionSwitch) -> None:
        """添加开关
        
        Parameters
        ----------
        switch : DistributionSwitch
            配电网开关
        """
        if switch.switch_id in self.switches:
            raise ValueError(f"开关 {switch.switch_id} 已存在")
        
        # 验证节点存在性
        for node_id in switch.connected_nodes:
            if node_id not in self.nodes:
                raise ValueError(f"节点 {node_id} 不存在")
        
        self.switches[switch.switch_id] = switch
    
    def add_measurement(self, measurement: MeasurementData) -> None:
        """添加量测数据
        
        Parameters
        ----------
        measurement : MeasurementData
            量测数据
        """
        if measurement.node_id not in self.nodes:
            raise ValueError(f"节点 {measurement.node_id} 不存在")
        
        self.measurements.append(measurement)
    
    def set_grounding_type(self, grounding_type: NeutralGroundingType) -> None:
        """设置中性点接地方式
        
        Parameters
        ----------
        grounding_type : NeutralGroundingType
            接地方式
        """
        self.grounding_type = grounding_type
    
    def build_topology_graph(self) -> nx.Graph:
        """构建拓扑图结构
        
        Returns
        -------
        nx.Graph
            网络拓扑图
        """
        graph = nx.Graph(name=self.network_name)
        
        # 添加节点
        for node_id, node in self.nodes.items():
            graph.add_node(
                node_id,
                node_type=node.node_type,
                voltage_level=node.voltage_level,
                capacity=node.capacity,
                coordinates=node.coordinates,
                parameters=node.parameters or {}
            )
        
        # 添加支路
        for branch_id, branch in self.branches.items():
            graph.add_edge(
                branch.from_node,
                branch.to_node,
                branch_id=branch_id,
                branch_type=branch.branch_type,
                length=branch.length,
                resistance=branch.resistance,
                reactance=branch.reactance,
                susceptance=branch.susceptance,
                capacity=branch.capacity,
                parameters=branch.parameters or {}
            )
        
        # 处理开关状态
        for switch_id, switch in self.switches.items():
            if len(switch.connected_nodes) >= 2:
                # 对于闭合的开关，合并节点或添加虚拟连接
                if switch.status:
                    for i in range(len(switch.connected_nodes) - 1):
                        node1 = switch.connected_nodes[i]
                        node2 = switch.connected_nodes[i + 1]
                        if graph.has_edge(node1, node2):
                            # 更新现有边的属性
                            graph.edges[node1, node2]['switch_id'] = switch_id
                            graph.edges[node1, node2]['switch_status'] = switch.status
                        else:
                            # 添加虚拟连接
                            graph.add_edge(
                                node1, node2,
                                switch_id=switch_id,
                                switch_status=switch.status,
                                is_virtual=True
                            )
        
        self.graph = graph
        return graph
    
    def process_measurement_data(self, 
                                start_time: pd.Timestamp,
                                end_time: pd.Timestamp,
                                sampling_rate: str = '1S') -> pd.DataFrame:
        """处理量测数据，生成时序特征
        
        Parameters
        ----------
        start_time : pd.Timestamp
            开始时间
        end_time : pd.Timestamp
            结束时间
        sampling_rate : str, default='1S'
            采样频率
            
        Returns
        -------
        pd.DataFrame
            处理后的量测数据
        """
        if not self.measurements:
            raise ValueError("没有量测数据可供处理")
        
        # 创建时间序列索引
        time_index = pd.date_range(start=start_time, end=end_time, freq=sampling_rate)
        
        # 按节点和量测类型组织数据
        measurement_dict = {}
        for measurement in self.measurements:
            key = (measurement.node_id, measurement.measurement_type.value)
            if key not in measurement_dict:
                measurement_dict[key] = []
            measurement_dict[key].append((measurement.timestamp, measurement.value, measurement.quality))
        
        # 创建数据框
        df_list = []
        for (node_id, meas_type), data in measurement_dict.items():
            # 转换为DataFrame
            temp_df = pd.DataFrame(data, columns=['timestamp', 'value', 'quality'])
            temp_df.set_index('timestamp', inplace=True)
            
            # 重采样到统一时间序列
            resampled = temp_df['value'].resample(sampling_rate).mean()
            
            # 数据插值处理缺失值
            if len(resampled) < len(time_index):
                # 创建插值函数
                valid_times = resampled.index
                valid_values = resampled.values
                
                if len(valid_values) > 1:
                    # 使用线性插值
                    interp_func = interpolate.interp1d(
                        valid_times.astype(np.int64), 
                        valid_values, 
                        kind=self.interpolation_method,
                        bounds_error=False,
                        fill_value="extrapolate"
                    )
                    
                    # 插值到目标时间序列
                    interp_values = interp_func(time_index.astype(np.int64))
                    
                    # 创建最终序列
                    final_series = pd.Series(interp_values, index=time_index, name=f"{node_id}_{meas_type}")
                    df_list.append(final_series)
                else:
                    # 如果只有一个数据点，使用前向填充
                    single_value = valid_values[0] if len(valid_values) > 0 else 0.0
                    final_series = pd.Series([single_value] * len(time_index), index=time_index, name=f"{node_id}_{meas_type}")
                    df_list.append(final_series)
            else:
                # 直接使用重采样数据
                final_series = resampled.reindex(time_index, method='ffill')
                final_series.name = f"{node_id}_{meas_type}"
                df_list.append(final_series)
        
        # 合并所有数据
        if df_list:
            result_df = pd.concat(df_list, axis=1)
            
            # 数据标准化
            result_df = pd.DataFrame(
                self.scaler.fit_transform(result_df),
                columns=result_df.columns,
                index=result_df.index
            )
            
            return result_df
        else:
            return pd.DataFrame(index=time_index)
    
    def create_gnn_input_features(self, 
                                 time_window: pd.Timedelta = pd.Timedelta(hours=1),
                                 feature_dim: int = 10) -> Dict[str, np.ndarray]:
        """创建GNN输入特征
        
        Parameters
        ----------
        time_window : pd.Timedelta, default=1小时
            时间窗口长度
        feature_dim : int, default=10
            特征维度
            
        Returns
        -------
        Dict[str, np.ndarray]
            GNN输入特征字典
        """
        if self.graph is None:
            self.build_topology_graph()
        
        if not self.measurements:
            raise ValueError("没有量测数据")
        
        # 获取时间范围
        timestamps = [m.timestamp for m in self.measurements]
        if not timestamps:
            raise ValueError("没有有效的时间戳")
        
        start_time = min(timestamps)
        end_time = max(timestamps)
        
        # 处理量测数据
        measurement_df = self.process_measurement_data(start_time, end_time)
        
        # 创建节点特征
        node_features = {}
        for node_id in self.nodes.keys():
            # 静态特征
            node = self.nodes[node_id]
            static_features = [
                node.voltage_level,
                node.capacity or 0.0,
                1.0 if node.node_type == "substation" else 0.0,  # 是否为变电站
                1.0 if node.node_type == "transformer" else 0.0,  # 是否为变压器
            ]
            
            # 动态特征（量测数据）
            dynamic_features = []
            for meas_type in MeasurementType:
                col_name = f"{node_id}_{meas_type.value}"
                if col_name in measurement_df.columns:
                    # 取时间窗口内的统计特征
                    window_data = measurement_df[col_name].iloc[-min(len(measurement_df), feature_dim):]
                    dynamic_features.extend([
                        window_data.mean(),
                        window_data.std(),
                        window_data.max(),
                        window_data.min(),
                    ])
                else:
                    # 填充零值
                    dynamic_features.extend([0.0, 0.0, 0.0, 0.0])
            
            # 组合特征
            all_features = static_features + dynamic_features
            
            # 确保特征维度一致
            if len(all_features) > feature_dim:
                all_features = all_features[:feature_dim]
            elif len(all_features) < feature_dim:
                all_features.extend([0.0] * (feature_dim - len(all_features)))
            
            node_features[node_id] = np.array(all_features, dtype=np.float32)
        
        # 创建边特征
        edge_features = {}
        edge_index = []
        
        for edge in self.graph.edges(data=True):
            node1, node2, edge_data = edge
            
            # 边特征
            edge_feature = [
                edge_data.get('length', 0.0),
                edge_data.get('resistance', 0.0),
                edge_data.get('reactance', 0.0),
                edge_data.get('capacity', 0.0),
                1.0 if edge_data.get('is_virtual', False) else 0.0,  # 是否为虚拟边
                1.0 if edge_data.get('switch_status', False) else 0.0,  # 开关状态
            ]
            
            # 确保特征维度一致
            if len(edge_feature) > 6:
                edge_feature = edge_feature[:6]
            elif len(edge_feature) < 6:
                edge_feature.extend([0.0] * (6 - len(edge_feature)))
            
            edge_key = (node1, node2)
            edge_features[edge_key] = np.array(edge_feature, dtype=np.float32)
            edge_index.append([list(self.nodes.keys()).index(node1), 
                             list(self.nodes.keys()).index(node2)])
        
        return {
            'node_features': node_features,
            'edge_features': edge_features,
            'edge_index': np.array(edge_index, dtype=np.int64).T,
            'node_mapping': {node_id: idx for idx, node_id in enumerate(self.nodes.keys())}
        }
    
    def detect_anomalies(self, 
                        method: str = 'zscore',
                        threshold: float = 3.0) -> Dict[str, List[Tuple[pd.Timestamp, float]]]:
        """检测量测数据异常
        
        Parameters
        ----------
        method : str, default='zscore'
            异常检测方法
        threshold : float, default=3.0
            异常检测阈值
            
        Returns
        -------
        Dict[str, List[Tuple[pd.Timestamp, float]]]
            异常检测结果
        """
        if not self.measurements:
            return {}
        
        anomalies = {}
        
        # 按节点和量测类型分组
        measurement_groups = {}
        for measurement in self.measurements:
            key = (measurement.node_id, measurement.measurement_type.value)
            if key not in measurement_groups:
                measurement_groups[key] = []
            measurement_groups[key].append(measurement)
        
        for (node_id, meas_type), measurements in measurement_groups.items():
            values = [m.value for m in measurements]
            timestamps = [m.timestamp for m in measurements]
            
            if len(values) < 2:
                continue
            
            if method == 'zscore':
                # Z-score异常检测
                mean_val = np.mean(values)
                std_val = np.std(values)
                
                if std_val == 0:
                    continue
                
                z_scores = [(val - mean_val) / std_val for val in values]
                
                anomaly_points = []
                for i, z_score in enumerate(z_scores):
                    if abs(z_score) > threshold:
                        anomaly_points.append((timestamps[i], values[i]))
                
                if anomaly_points:
                    key = f"{node_id}_{meas_type}"
                    anomalies[key] = anomaly_points
        
        return anomalies
    
    def export_to_pyg_format(self) -> Dict[str, Any]:
        """导出为PyTorch Geometric格式
        
        Returns
        -------
        Dict[str, Any]
            PyG格式数据
        """
        gnn_features = self.create_gnn_input_features()
        
        return {
            'x': np.array([gnn_features['node_features'][node_id] 
                          for node_id in self.nodes.keys()]),
            'edge_index': gnn_features['edge_index'],
            'edge_attr': np.array([gnn_features['edge_features'][edge_key] 
                                 for edge_key in gnn_features['edge_features'].keys()]),
            'y': np.zeros(len(self.nodes)),  # 标签（可根据实际任务设置）
            'node_ids': list(self.nodes.keys())
        }
    
    def summary(self) -> Dict[str, Any]:
        """生成网络摘要
        
        Returns
        -------
        Dict[str, Any]
            网络统计信息
        """
        return {
            'network_name': self.network_name,
            'node_count': len(self.nodes),
            'branch_count': len(self.branches),
            'switch_count': len(self.switches),
            'measurement_count': len(self.measurements),
            'grounding_type': self.grounding_type.value,
            'graph_edges': len(self.graph.edges) if self.graph else 0,
            'measurement_types': list(set(m.measurement_type.value for m in self.measurements))
        }


# 工具函数
def create_sample_distribution_network() -> TopologyMeteringFusion:
    """创建示例配电网
    
    Returns
    -------
    TopologyMeteringFusion
        示例配电网融合对象
    """
    fusion = TopologyMeteringFusion("示例配电网")
    
    # 添加节点
    nodes = [
        DistributionNode("substation", "substation", 110.0, (0, 0), 50000),
        DistributionNode("transformer1", "transformer", 10.0, (1, 1), 10000),
        DistributionNode("load1", "load", 10.0, (2, 2), 5000),
        DistributionNode("load2", "load", 10.0, (3, 1), 3000),
    ]
    
    for node in nodes:
        fusion.add_node(node)
    
    # 添加支路
    branches = [
        DistributionBranch("line1", "substation", "transformer1", "overhead", 5.0, 0.1, 0.2, 0.001, 20000),
        DistributionBranch("line2", "transformer1", "load1", "cable", 2.0, 0.05, 0.1, 0.002, 10000),
        DistributionBranch("line3", "transformer1", "load2", "overhead", 3.0, 0.08, 0.15, 0.001, 8000),
    ]
    
    for branch in branches:
        fusion.add_branch(branch)
    
    # 添加开关
    switches = [
        DistributionSwitch("sw1", SwitchType.CIRCUIT_BREAKER, ["transformer1", "load1"], True),
    ]
    
    for switch in switches:
        fusion.add_switch(switch)
    
    # 设置接地方式
    fusion.set_grounding_type(NeutralGroundingType.PETERSON_COIL)
    
    return fusion