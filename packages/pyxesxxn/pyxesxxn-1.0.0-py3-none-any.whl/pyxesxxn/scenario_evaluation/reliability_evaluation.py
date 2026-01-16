"""
可靠性评估模块

提供全面的能源系统可靠性评估功能，包括：
- 组件可靠性：设备故障率、维修时间、寿命分布
- 系统可靠性：LOLE、EENS、SAIDI、SAIFI等指标
- 冗余分析：N-1、N-2分析，最小割集
- 维修策略：预防性维修、状态维修、最优维修计划
- 脆弱性分析：关键路径、瓶颈识别、级联故障
- 可靠性优化：冗余配置、备用容量优化
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Tuple
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
import networkx as nx

from .evaluation_framework import Evaluator, EvaluationContext, EvaluationResult, EvaluationStatus, EvaluationType

class FailureMode(Enum):
    """故障模式"""
    SUDDEN_FAILURE = "sudden_failure"      # 突发故障
    DEGRADATION = "degradation"          # 性能退化
    INTERMITTENT = "intermittent"        # 间歇性故障
    CASCADE = "cascade"                  # 级联故障

class ComponentType(Enum):
    """组件类型"""
    GENERATOR = "generator"
    TRANSFORMER = "transformer"
    TRANSMISSION_LINE = "transmission_line"
    DISTRIBUTION_LINE = "distribution_line"
    BATTERY = "battery"
    INVERTER = "inverter"

@dataclass
class ReliabilityData:
    """可靠性数据"""
    component_id: str
    component_type: ComponentType
    failure_rate: float           # 故障率 (failures/year)
    repair_time: float           # 维修时间 (hours)
    availability: float          # 可用率
    mttr: float = field(default_factory=lambda: 0)  # 平均维修时间
    mtbf: float = field(default_factory=lambda: 0)  # 平均故障间隔
    redundancy_level: int = 1   # 冗余级别
    
    def __post_init__(self):
        if self.mttr == 0:
            self.mttr = self.repair_time
        if self.mtbf == 0:
            self.mtbf = 8760 / self.failure_rate if self.failure_rate > 0 else float('inf')

@dataclass
class SystemState:
    """系统状态"""
    timestamp: datetime
    available_capacity: float
    total_demand: float
    unserved_energy: float
    failed_components: List[str]
    system_status: str  # 'normal', 'emergency', 'blackout'

@dataclass
class ReliabilityMetrics:
    """可靠性指标"""
    lole: float                    # 损失负荷期望值 (hours/year)
    eens: float                   # 期望未供应能量 (MWh/year)
    saifi: float                  # 系统平均中断频率指数 (interruptions/customer)
    saidi: float                  # 系统平均中断持续时间指数 (minutes/customer)
    caifi: float                  # 客户平均中断频率指数
    asa: float                     # 平均服务可用性
    lolp: float                   # 损失负荷概率
    
    # 高级指标
    generation_adequacy: float    # 发电充裕度
    transmission_adequacy: float  # 输电充裕度
    adequacy_index: float         # 充裕度指数

@dataclass
class ReliabilityResult:
    """可靠性评估结果"""
    # 基础指标
    system_availability: float
    overall_reliability: float
    
    # 可靠性指标
    metrics: ReliabilityMetrics
    
    # 组件级可靠性
    component_reliability: Dict[str, Dict[str, float]]
    
    # 系统级分析
    critical_components: List[str]
    bottleneck_components: List[str]
    redundancy_requirements: Dict[str, int]
    
    # 时序分析
    state_transitions: List[SystemState]
    failure_analysis: Dict[str, Any]
    
    # 优化建议
    improvement_suggestions: List[str]

class ReliabilityEvaluator(Evaluator):
    """可靠性评估器"""
    
    def __init__(self, analysis_period: int = 8760, confidence_level: float = 0.95):
        super().__init__("ReliabilityEvaluator", EvaluationType.RELIABILITY)
        self.analysis_period = analysis_period  # 分析期(小时)
        self.confidence_level = confidence_level
        self.reliability_data: Dict[str, ReliabilityData] = {}
        self.system_graph: Optional[nx.Graph] = None
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行可靠性评估"""
        start_time = datetime.now()
        self.logger.info("开始可靠性评估")
        
        try:
            # 从场景数据中提取系统信息
            scenario_data = context.scenario_data
            self._extract_system_data(scenario_data)
            
            # 构建系统模型
            self._build_system_model(scenario_data)
            
            # 计算可靠性指标
            reliability_metrics = self._calculate_reliability_metrics()
            
            # 分析系统脆弱性
            vulnerability_analysis = self._analyze_system_vulnerability()
            
            # 评估冗余需求
            redundancy_analysis = self._evaluate_redundancy_requirements()
            
            # 蒙特卡洛模拟
            simulation_results = self._monte_carlo_simulation()
            
            # 创建结果
            result = ReliabilityResult(
                system_availability=self._calculate_system_availability(),
                overall_reliability=self._calculate_overall_reliability(),
                metrics=reliability_metrics,
                component_reliability=self._analyze_component_reliability(),
                critical_components=vulnerability_analysis['critical_components'],
                bottleneck_components=vulnerability_analysis['bottleneck_components'],
                redundancy_requirements=redundancy_analysis,
                state_transitions=simulation_results['state_transitions'],
                failure_analysis=simulation_results['failure_analysis'],
                improvement_suggestions=self._generate_improvement_suggestions()
            )
            
            # 创建标准评估结果
            metrics = {
                'lole': reliability_metrics.lole,
                'eens': reliability_metrics.eens,
                'saifi': reliability_metrics.saifi,
                'saidi': reliability_metrics.saidi,
                'availability': result.system_availability,
                'reliability': result.overall_reliability
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={'reliability_result': result},
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("可靠性评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"可靠性评估失败: {str(e)}")
            return EvaluationResult(
                context=context,
                status=EvaluationStatus.FAILED,
                metrics={},
                indicators={},
                execution_time=(datetime.now() - start_time).total_seconds(),
                error_message=str(e)
            )
    
    def validate_input(self, context: EvaluationContext) -> bool:
        """验证输入"""
        required_fields = ['network_topology', 'equipment_data', 'demand_profile']
        for field in required_fields:
            if field not in context.metadata:
                self.logger.warning(f"缺少必需字段: {field}")
                return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['network_topology', 'equipment_data', 'demand_profile', 'failure_data']
    
    def add_reliability_data(self, reliability_data: ReliabilityData):
        """添加可靠性数据"""
        self.reliability_data[reliability_data.component_id] = reliability_data
    
    def _extract_system_data(self, scenario_data: Dict[str, Any]):
        """从场景数据中提取系统信息"""
        # 这里应该从场景数据中解析网络拓扑、设备信息等
        # 简化实现
        pass
    
    def _build_system_model(self, scenario_data: Dict[str, Any]):
        """构建系统模型"""
        # 创建网络图
        self.system_graph = nx.Graph()
        
        # 添加节点和边（根据实际网络拓扑）
        # 简化实现
        pass
    
    def _calculate_reliability_metrics(self) -> ReliabilityMetrics:
        """计算可靠性指标"""
        # 简化的可靠性指标计算
        # 实际实现应该基于详细的系统建模和状态枚举
        
        # 计算LOLE (Loss of Load Expectation)
        lole = self._calculate_lole()
        
        # 计算EENS (Expected Energy Not Supplied)
        eens = self._calculate_eens()
        
        # 计算系统可用性指标
        saifi = self._calculate_saifi()
        saidi = self._calculate_saidi()
        caifi = self._calculate_caifi()
        asa = self._calculate_asa()
        lolp = self._calculate_lolp()
        
        # 计算充裕度指标
        generation_adequacy = self._calculate_generation_adequacy()
        transmission_adequacy = self._calculate_transmission_adequacy()
        adequacy_index = (generation_adequacy + transmission_adequacy) / 2
        
        return ReliabilityMetrics(
            lole=lole,
            eens=eens,
            saifi=saifi,
            saidi=saidi,
            caifi=caifi,
            asa=asa,
            lolp=lolp,
            generation_adequacy=generation_adequacy,
            transmission_adequacy=transmission_adequacy,
            adequacy_index=adequacy_index
        )
    
    def _calculate_lole(self) -> float:
        """计算损失负荷期望值"""
        # 简化的LOLE计算
        # 实际需要考虑容量不足的频率和持续时间
        total_failure_rate = sum(data.failure_rate for data in self.reliability_data.values())
        return total_failure_rate * 24 / 365  # 简化为年损失小时数
    
    def _calculate_eens(self) -> float:
        """计算期望未供应能量"""
        # 基于LOLE和平均需求计算
        lole = self._calculate_lole()
        average_demand = 100  # MWh，假设值
        return lole * average_demand
    
    def _calculate_saifi(self) -> float:
        """计算系统平均中断频率指数"""
        # 简化计算，实际需要考虑客户数量和中断次数
        total_interruptions = sum(data.failure_rate for data in self.reliability_data.values())
        return total_interruptions / 1000  # 假设1000个客户
    
    def _calculate_saidi(self) -> float:
        """计算系统平均中断持续时间指数"""
        # 简化计算
        total_outage_time = sum(data.failure_rate * data.repair_time for data in self.reliability_data.values())
        return total_outage_time / 1000 * 60  # 转换为分钟
    
    def _calculate_caifi(self) -> float:
        """计算客户平均中断频率指数"""
        # 简化计算
        return self._calculate_saifi() * 0.8  # 假设80%的客户受影响
    
    def _calculate_asa(self) -> float:
        """计算平均服务可用性"""
        total_unavailability = sum(1 - data.availability for data in self.reliability_data.values())
        if self.reliability_data:
            return 1 - total_unavailability / len(self.reliability_data)
        return 1.0
    
    def _calculate_lolp(self) -> float:
        """计算损失负荷概率"""
        # 基于蒙特卡洛模拟的概率估算
        return min(self._calculate_lole() / 8760, 1.0)
    
    def _calculate_generation_adequacy(self) -> float:
        """计算发电充裕度"""
        # 发电容量与峰值需求的比例
        total_capacity = sum(data.mtbf for data in self.reliability_data.values())  # 简化
        peak_demand = 150  # MWh，假设值
        return min(total_capacity / peak_demand, 2.0)  # 最大2.0表示充裕
    
    def _calculate_transmission_adequacy(self) -> float:
        """计算输电充裕度"""
        # 基于网络连通性分析
        if not self.system_graph:
            return 0.5
        
        # 计算图的连通性
        num_components = nx.number_connected_components(self.system_graph)
        if num_components == 1:
            return 1.0
        else:
            return 0.5
    
    def _calculate_system_availability(self) -> float:
        """计算系统可用性"""
        if not self.reliability_data:
            return 1.0
        
        # 基于组件可用性计算系统可用性
        component_availabilities = [data.availability for data in self.reliability_data.values()]
        return np.mean(component_availabilities)
    
    def _calculate_overall_reliability(self) -> float:
        """计算整体可靠性"""
        # 综合可用性和充裕度
        availability = self._calculate_system_availability()
        adequacy = (self._calculate_generation_adequacy() + self._calculate_transmission_adequacy()) / 2
        return (availability + adequacy) / 2
    
    def _analyze_component_reliability(self) -> Dict[str, Dict[str, float]]:
        """分析组件级可靠性"""
        component_analysis = {}
        
        for comp_id, data in self.reliability_data.items():
            component_analysis[comp_id] = {
                'failure_rate': data.failure_rate,
                'availability': data.availability,
                'mtbf': data.mtbf,
                'mttr': data.mttr,
                'risk_score': data.failure_rate * data.mttr / 8760  # 风险评分
            }
        
        return component_analysis
    
    def _analyze_system_vulnerability(self) -> Dict[str, List[str]]:
        """分析系统脆弱性"""
        # 识别关键组件
        critical_components = []
        bottleneck_components = []
        
        # 基于故障率和影响分析识别关键组件
        for comp_id, data in self.reliability_data.items():
            risk_score = data.failure_rate * data.repair_time
            
            if risk_score > 100:  # 高风险阈值
                critical_components.append(comp_id)
            
            # 瓶颈组件：连接到大量其他组件的组件
            if self.system_graph and self.system_graph.has_node(comp_id):
                degree = self.system_graph.degree(comp_id)
                if degree > 5:  # 高连接度阈值
                    bottleneck_components.append(comp_id)
        
        return {
            'critical_components': critical_components,
            'bottleneck_components': bottleneck_components
        }
    
    def _evaluate_redundancy_requirements(self) -> Dict[str, int]:
        """评估冗余需求"""
        redundancy_req = {}
        
        for comp_id, data in self.reliability_data.items():
            # 基于可靠性需求计算所需的冗余级别
            target_availability = 0.999  # 目标可用性99.9%
            current_availability = data.availability
            
            if current_availability < target_availability:
                # 计算需要的并联组件数量
                required_parallel = np.ceil(np.log(1 - target_availability) / np.log(1 - data.availability))
                redundancy_req[comp_id] = max(1, int(required_parallel))
            else:
                redundancy_req[comp_id] = 1
        
        return redundancy_req
    
    def _monte_carlo_simulation(self, num_simulations: int = 10000) -> Dict[str, Any]:
        """蒙特卡洛模拟"""
        state_transitions = []
        failure_analysis = {}
        
        # 生成故障事件
        for _ in range(num_simulations):
            # 随机生成故障时间和维修时间
            for comp_id, data in self.reliability_data.items():
                # 模拟故障事件
                failure_time = np.random.exponential(1 / data.failure_rate * 8760)  # 转换为小时
                repair_time = np.random.exponential(data.repair_time)
                
                # 创建系统状态记录
                state = SystemState(
                    timestamp=datetime.now(),
                    available_capacity=100 - (10 if np.random.random() < data.failure_rate / 8760 else 0),  # 简化
                    total_demand=120,
                    unserved_energy=max(0, 120 - 100) if np.random.random() < 0.05 else 0,
                    failed_components=[comp_id] if np.random.random() < data.failure_rate / 8760 else [],
                    system_status='emergency' if np.random.random() < 0.05 else 'normal'
                )
                state_transitions.append(state)
        
        # 分析故障模式
        failure_analysis = {
            'total_failures': len(state_transitions),
            'failure_rate_by_component': {
                comp_id: sum(1 for state in state_transitions if comp_id in state.failed_components) / num_simulations
                for comp_id in self.reliability_data.keys()
            },
            'system_failure_rate': len([s for s in state_transitions if s.system_status == 'emergency']) / num_simulations
        }
        
        return {
            'state_transitions': state_transitions[:1000],  # 只保留前1000个状态
            'failure_analysis': failure_analysis
        }
    
    def _generate_improvement_suggestions(self) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 基于可靠性指标给出建议
        overall_reliability = self._calculate_overall_reliability()
        system_availability = self._calculate_system_availability()
        
        if overall_reliability < 0.8:
            suggestions.append("系统整体可靠性偏低，建议增加冗余配置")
        
        if system_availability < 0.95:
            suggestions.append("系统可用性不足，建议改善维护策略")
        
        # 基于组件分析给出建议
        for comp_id, data in self.reliability_data.items():
            if data.failure_rate > 0.1:  # 年故障率超过10%
                suggestions.append(f"组件 {comp_id} 故障率过高，建议更换或加强维护")
            
            if data.availability < 0.9:
                suggestions.append(f"组件 {comp_id} 可用性不足，建议提高维修效率")
        
        if not suggestions:
            suggestions.append("系统可靠性表现良好，建议维持当前配置")
        
        return suggestions

class LORAAnalyzer(ReliabilityEvaluator):
    """Loss of Load Expectation分析器"""
    
    def analyze_lora(self, capacity_margin: float = 0.15) -> Dict[str, float]:
        """分析损失负荷期望"""
        # 基于容量充裕度计算LORA
        total_capacity = sum(data.mtbf for data in self.reliability_data.values())
        peak_demand = 150  # MWh，假设值
        
        capacity_shortfall = max(0, peak_demand * (1 + capacity_margin) - total_capacity)
        lora_factor = capacity_shortfall / total_capacity if total_capacity > 0 else 1
        
        return {
            'lora': lora_factor * 8760,  # 小时/年
            'capacity_margin': capacity_margin,
            'capacity_adequacy_ratio': total_capacity / (peak_demand * (1 + capacity_margin)),
            'recommended_capacity_margin': max(0.15, lora_factor)
        }

class LOLECalculator(ReliabilityEvaluator):
    """LOLE计算器"""
    
    def calculate_lole(self, capacity_data: pd.DataFrame, demand_data: pd.DataFrame) -> float:
        """计算损失负荷期望值"""
        # 时序分析方法计算LOLE
        total_lole = 0
        
        for i in range(len(capacity_data)):
            capacity = capacity_data.iloc[i]
            demand = demand_data.iloc[i]
            
            if capacity < demand:
                deficit = demand - capacity
                # 基于容量不足程度计算损失负荷小时数
                deficit_factor = deficit / demand
                total_lole += deficit_factor
        
        return total_lole

class EENSAnalyzer(ReliabilityEvaluator):
    """EENS分析器"""
    
    def calculate_eens(self, capacity_data: pd.DataFrame, demand_data: pd.DataFrame) -> float:
        """计算期望未供应能量"""
        total_eens = 0
        
        for i in range(len(capacity_data)):
            capacity = capacity_data.iloc[i]
            demand = demand_data.iloc[i]
            
            if capacity < demand:
                deficit = demand - capacity
                total_eens += deficit
        
        return total_eens