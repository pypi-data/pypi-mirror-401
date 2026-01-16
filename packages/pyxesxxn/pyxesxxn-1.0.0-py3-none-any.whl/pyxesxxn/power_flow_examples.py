"""
潮流计算示例和测试用例

提供潮流计算功能的完整示例和测试用例，展示专业潮流计算功能的使用方法。
"""

# SPDX-FileCopyrightText: 2024-present PyXESXXN Development Team
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .power_flow_enhanced import (
    PowerFlowMethod, 
    NewtonRaphsonSolver, 
    PowerFlowResult,
    EnhancedPowerFlowSolver
)

if TYPE_CHECKING:
    from .network import PyXESXXNNetwork
    from .power_flow_reliability import (
        PowerFlowReliabilityAnalyzer,
        ReliabilityLevel
    )


logger = logging.getLogger(__name__)


class PowerFlowExample:
    """潮流计算示例基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.network = None
        self.results = {}
    
    def setup_network(self) -> PyXESXXNNetwork:
        """设置网络模型"""
        raise NotImplementedError("子类必须实现此方法")
    
    def run_power_flow(self, method: PowerFlowMethod = PowerFlowMethod.NEWTON_RAPHSON) -> PowerFlowResult:
        """运行潮流计算"""
        if self.network is None:
            self.network = self.setup_network()
        
        solver = NewtonRaphsonSolver(self.network)
        result = solver.solve()
        
        self.results[method.value] = result
        return result
    
    def analyze_reliability(self, result: PowerFlowResult) -> Tuple[Dict[str, Any], str]:
        """分析可靠性"""
        from .power_flow_reliability import PowerFlowReliabilityAnalyzer
        
        analyzer = PowerFlowReliabilityAnalyzer(self.network, result)
        metrics = analyzer.analyze_reliability()
        report = analyzer.generate_reliability_report()
        
        return metrics.to_dict(), report
    
    def run_example(self) -> Dict[str, Any]:
        """运行完整示例"""
        print(f"=== 运行示例: {self.name} ===")
        print(f"描述: {self.description}")
        
        # 设置网络
        print("\n1. 设置网络模型...")
        self.setup_network()
        
        # 运行潮流计算
        print("2. 运行潮流计算...")
        result = self.run_power_flow()
        
        # 分析可靠性
        print("3. 分析可靠性...")
        metrics, report = self.analyze_reliability(result)
        
        # 输出结果
        print("4. 生成报告...")
        print(f"\n潮流计算结果:")
        print(f"收敛状态: {'收敛' if result.converged else '不收敛'}")
        print(f"迭代次数: {result.iterations}")
        print(f"最大误差: {result.error:.6e}")
        
        print(f"\n可靠性报告:")
        print(report)
        
        return {
            'network': self.network,
            'result': result,
            'metrics': metrics,
            'report': report
        }


class Simple3BusExample(PowerFlowExample):
    """简单3节点系统示例"""
    
    def __init__(self):
        super().__init__(
            name="简单3节点系统",
            description="展示基本潮流计算功能的简单3节点电力系统示例"
        )
    
    def setup_network(self) -> PyXESXXNNetwork:
        """设置3节点测试网络"""
        from .network_new import PyXESXXNNetwork, ComponentType, EnergyCarrier
        
        # 创建网络
        network = PyXESXXNNetwork()
        
        # 添加节点
        network.add_bus("Bus1", voltage=110.0, carrier=EnergyCarrier.ELECTRICITY)
        network.add_bus("Bus2", voltage=110.0, carrier=EnergyCarrier.ELECTRICITY)
        network.add_bus("Bus3", voltage=110.0, carrier=EnergyCarrier.ELECTRICITY)
        
        # 添加发电机
        network.add_generator("Gen1", bus="Bus1", capacity=100, carrier="electricity")
        network.add_generator("Gen2", bus="Bus2", capacity=80, carrier="electricity")
        
        # 添加负荷
        network.add_load("Load1", bus="Bus2", carrier="electricity", demand=40)
        network.add_load("Load2", bus="Bus3", carrier="electricity", demand=60)
        
        # 添加线路
        network.add_line("Line1-2", from_bus="Bus1", to_bus="Bus2", carrier="electricity",
                        capacity=100, resistance=0.01, reactance=0.1)
        network.add_line("Line2-3", from_bus="Bus2", to_bus="Bus3", carrier="electricity",
                        capacity=100, resistance=0.02, reactance=0.15)
        
        return network
    
    def run_wind_power_analysis(self) -> Dict[str, Any]:
        """运行风电接入分析"""
        if self.network is None:
            self.network = self.setup_network()
        
        # 运行基础潮流计算
        print("1. 基础潮流计算...")
        base_result = self.run_power_flow()
        
        # 分析风电接入影响
        print("2. 风电接入影响分析...")
        
        # 计算风电渗透率
        total_generation = sum(gen.capacity for gen in self.network.generators.values())
        wind_generation = sum(gen.capacity for name, gen in self.network.generators.items() 
                            if 'Wind' in name)
        wind_penetration = wind_generation / total_generation * 100
        
        # 分析电压稳定性
        voltage_stability = {}
        for bus_name, bus_result in base_result.bus_results.items():
            voltage_stability[bus_name] = {
                'voltage': bus_result.voltage_magnitude,
                'angle': bus_result.voltage_angle
            }
        
        # 分析线路负载率
        line_loading = {}
        for line_name, line_result in base_result.line_results.items():
            if hasattr(line_result, 'loading'):
                line_loading[line_name] = line_result.loading
        
        return {
            'base_result': base_result,
            'wind_penetration': wind_penetration,
            'voltage_stability': voltage_stability,
            'line_loading': line_loading,
            'analysis': {
                'total_generation': total_generation,
                'wind_generation': wind_generation,
                'penetration_rate': f"{wind_penetration:.1f}%"
            }
        }


class IEEE14BusExample(PowerFlowExample):
    """IEEE 14节点系统示例"""
    
    def __init__(self):
        super().__init__(
            name="IEEE 14节点系统",
            description="标准IEEE 14节点测试系统的潮流计算示例"
        )
    
    def setup_network(self) -> PyXESXXNNetwork:
        """设置IEEE 14节点网络"""
        from .network_new import PyXESXXNNetwork, ComponentType, EnergyCarrier
        
        # 创建网络
        network = PyXESXXNNetwork()
        
        # 添加节点 (基于IEEE 14节点标准数据)
        buses = [
            ("Bus1", 69.0, "Slack"),
            ("Bus2", 69.0, "PV"),
            ("Bus3", 69.0, "PV"),
            ("Bus4", 69.0, "PQ"),
            ("Bus5", 69.0, "PQ"),
            ("Bus6", 13.8, "PQ"),
            ("Bus7", 13.8, "PQ"),
            ("Bus8", 18.0, "PQ"),
            ("Bus9", 13.8, "PQ"),
            ("Bus10", 13.8, "PQ"),
            ("Bus11", 13.8, "PQ"),
            ("Bus12", 13.8, "PQ"),
            ("Bus13", 13.8, "PQ"),
            ("Bus14", 13.8, "PQ")
        ]
        
        for name, v_nom, bus_type in buses:
            network.add_bus(name, voltage=v_nom, frequency=50, carrier=EnergyCarrier.ELECTRICITY)
        
        # 添加发电机
        generators = [
            ("Gen1", "Bus1", 232.4, None, "Slack"),
            ("Gen2", "Bus2", 40.0, 42.4, "PV"),
            ("Gen3", "Bus3", 0.0, 23.4, "PV"),
            ("Gen6", "Bus6", 0.0, 12.2, "PV"),
            ("Gen8", "Bus8", 0.0, 17.4, "PV")
        ]
        
        for name, bus, p_set, q_set, control in generators:
            network.add_generator(name, bus=bus, capacity=p_set * 1.5, carrier="electricity")
        
        # 添加负荷
        loads = [
            ("Load2", "Bus2", 21.7, 12.7),
            ("Load3", "Bus3", 94.2, 19.0),
            ("Load4", "Bus4", 47.8, -3.9),
            ("Load5", "Bus5", 7.6, 1.6),
            ("Load6", "Bus6", 11.2, 7.5),
            ("Load9", "Bus9", 29.5, 16.6),
            ("Load10", "Bus10", 9.0, 5.8),
            ("Load11", "Bus11", 3.5, 1.8),
            ("Load12", "Bus12", 6.1, 1.6),
            ("Load13", "Bus13", 13.5, 5.8),
            ("Load14", "Bus14", 14.9, 5.0)
        ]
        
        for name, bus, p_set, q_set in loads:
            network.add_load(name, bus=bus, carrier="electricity", demand=p_set)
        
        # 添加线路 (简化版本)
        lines = [
            ("Line1-2", "Bus1", "Bus2", 0.01938, 0.05917),
            ("Line1-5", "Bus1", "Bus5", 0.05403, 0.22304),
            ("Line2-3", "Bus2", "Bus3", 0.04699, 0.19797),
            ("Line2-4", "Bus2", "Bus4", 0.05811, 0.17632),
            ("Line2-5", "Bus2", "Bus5", 0.05695, 0.17388),
            ("Line3-4", "Bus3", "Bus4", 0.06701, 0.17103),
            ("Line4-5", "Bus4", "Bus5", 0.01335, 0.04211),
            ("Line4-7", "Bus4", "Bus7", 0.0, 0.20912),
            ("Line4-9", "Bus4", "Bus9", 0.0, 0.55618),
            ("Line5-6", "Bus5", "Bus6", 0.0, 0.25202),
            ("Line6-11", "Bus6", "Bus11", 0.09498, 0.1989),
            ("Line6-12", "Bus6", "Bus12", 0.12291, 0.25581),
            ("Line6-13", "Bus6", "Bus13", 0.06615, 0.13027),
            ("Line7-8", "Bus7", "Bus8", 0.0, 0.17615),
            ("Line7-9", "Bus7", "Bus9", 0.0, 0.11001),
            ("Line9-10", "Bus9", "Bus10", 0.03181, 0.0845),
            ("Line9-14", "Bus9", "Bus14", 0.12711, 0.27038),
            ("Line10-11", "Bus10", "Bus11", 0.08205, 0.19207),
            ("Line12-13", "Bus12", "Bus13", 0.22092, 0.19988),
            ("Line13-14", "Bus13", "Bus14", 0.17093, 0.34802)
        ]
        
        for name, bus0, bus1, r, x in lines:
            network.add_line(name, from_bus=bus0, to_bus=bus1, carrier="electricity",
                           capacity=100, resistance=r, reactance=x)
        
        return network


class WindPowerIntegrationExample(PowerFlowExample):
    """风电接入潮流计算示例"""
    
    def __init__(self):
        super().__init__(
            name="风电接入系统",
            description="展示风电接入对潮流计算影响的示例"
        )
    
    def setup_network(self) -> PyXESXXNNetwork:
        """设置风电接入网络"""
        from .network_new import PyXESXXNNetwork, ComponentType, EnergyCarrier
        
        # 创建网络
        network = PyXESXXNNetwork()
        
        # 添加节点
        buses = [
            ("Bus1", 110, "Slack"),
            ("Bus2", 110, "PQ"),
            ("Bus3", 110, "PQ"),
            ("Bus4", 110, "PQ"),
            ("Bus5", 110, "PQ")
        ]
        
        for name, v_nom, bus_type in buses:
            network.add_bus(name, voltage=v_nom, carrier=EnergyCarrier.ELECTRICITY)
        
        # 添加传统发电机
        network.add_generator("Gen1", bus="Bus1", capacity=150, carrier="electricity")
        network.add_generator("Gen2", bus="Bus2", capacity=75, carrier="electricity")
        
        # 添加风电
        network.add_generator("Wind1", bus="Bus3", capacity=45, carrier="electricity")
        network.add_generator("Wind2", bus="Bus4", capacity=30, carrier="electricity")
        
        # 添加负荷
        network.add_load("Load1", bus="Bus2", carrier="electricity", demand=40)
        network.add_load("Load2", bus="Bus3", carrier="electricity", demand=35)
        network.add_load("Load3", bus="Bus4", carrier="electricity", demand=25)
        network.add_load("Load4", bus="Bus5", carrier="electricity", demand=30)
        
        # 添加线路
        lines = [
            ("Line1-2", "Bus1", "Bus2", 0.02, 0.08),
            ("Line2-3", "Bus2", "Bus3", 0.03, 0.12),
            ("Line3-4", "Bus3", "Bus4", 0.025, 0.1),
            ("Line4-5", "Bus4", "Bus5", 0.015, 0.06),
            ("Line2-5", "Bus2", "Bus5", 0.035, 0.14)
        ]
        
        for name, bus0, bus1, r, x in lines:
            network.add_line(name, from_bus=bus0, to_bus=bus1, carrier="electricity",
                           capacity=100, resistance=r, reactance=x)
        
        return network

    def run_wind_power_analysis(self) -> Dict[str, Any]:
        """运行风电接入分析"""
        if self.network is None:
            self.network = self.setup_network()
        
        # 基础潮流计算
        print("1. 基础潮流计算...")
        base_result = self.run_power_flow()
        
        # 风电渗透率分析
        print("2. 风电渗透率分析...")
        total_generation = sum(gen.parameters.get('capacity', 0) for gen in self.network.generators.values())
        wind_generation = sum(gen.parameters.get('capacity', 0) for name, gen in self.network.generators.items() 
                             if name.startswith('Wind'))
        wind_penetration = wind_generation / total_generation if total_generation > 0 else 0
        
        # 电压稳定性分析
        print("3. 电压稳定性分析...")
        voltage_stability = {}
        if base_result.converged:
            for bus_name, voltage in base_result.voltage_magnitude.items():
                voltage_stability[bus_name] = {
                    'voltage': voltage.iloc[0],
                    'stable': 0.95 <= voltage.iloc[0] <= 1.05
                }
        
        # 线路负载率分析
        print("4. 线路负载率分析...")
        line_loading = {}
        if hasattr(base_result, 'line_flows') and base_result.line_flows:
            for line_name, flow in base_result.line_flows.items():
                if line_name in self.network.lines:
                    capacity = self.network.lines[line_name].parameters.get('capacity', 100)
                    loading = abs(flow.iloc[0]) / capacity if capacity > 0 else 0
                    line_loading[line_name] = {
                        'flow': flow.iloc[0],
                        'loading': loading,
                        'overloaded': loading > 0.8
                    }
        
        return {
            'base_case': {
                'result': base_result,
                'wind_penetration': wind_penetration,
                'voltage_stability': voltage_stability,
                'line_loading': line_loading
            },
            'wind_scenarios': {
                'current': wind_penetration,
                'high_wind': min(wind_penetration * 1.5, 0.8),  # 模拟高风电场景
                'low_wind': max(wind_penetration * 0.5, 0.1)    # 模拟低风电场景
            }
        }


class ContingencyAnalysisExample(PowerFlowExample):
    """故障分析潮流计算示例"""
    
    def __init__(self):
        super().__init__(
            name="故障分析",
            description="展示N-1故障分析的潮流计算示例"
        )
    
    def setup_network(self) -> PyXESXXNNetwork:
        """设置故障分析网络"""
        from .network_new import PyXESXXNNetwork, ComponentType, EnergyCarrier
        
        # 创建网络
        network = PyXESXXNNetwork()
        
        # 添加节点
        buses = [
            ("Bus1", 220, "Slack"),
            ("Bus2", 220, "PQ"),
            ("Bus3", 110, "PQ"),
            ("Bus4", 110, "PQ"),
            ("Bus5", 110, "PQ")
        ]
        
        for name, v_nom, bus_type in buses:
            network.add_bus(name, voltage=v_nom, carrier=EnergyCarrier.ELECTRICITY)
        
        # 添加发电机
        network.add_generator("Gen1", bus="Bus1", capacity=300, carrier="electricity")
        network.add_generator("Gen2", bus="Bus3", capacity=120, carrier="electricity")
        
        # 添加负荷
        network.add_load("Load1", bus="Bus2", carrier="electricity", demand=60)
        network.add_load("Load2", bus="Bus3", carrier="electricity", demand=40)
        network.add_load("Load3", bus="Bus4", carrier="electricity", demand=50)
        network.add_load("Load4", bus="Bus5", carrier="electricity", demand=30)
        
        # 添加线路
        lines = [
            ("Line1-2", "Bus1", "Bus2", 0.01, 0.04),
            ("Line2-3", "Bus2", "Bus3", 0.015, 0.06),
            ("Line3-4", "Bus3", "Bus4", 0.02, 0.08),
            ("Line4-5", "Bus4", "Bus5", 0.025, 0.1),
            ("Line2-4", "Bus2", "Bus4", 0.03, 0.12)
        ]
        
        for name, bus0, bus1, r, x in lines:
            network.add_line(name, from_bus=bus0, to_bus=bus1, carrier="electricity",
                           capacity=100, resistance=r, reactance=x)
        
        # 注意：PyXESXXN当前版本不支持变压器，暂时跳过
        # 添加变压器
        # network.add("Transformer", "Trafo2-3", bus0="Bus2", bus1="Bus3", 
        #            x=0.1, s_nom=100)
        
        return network
    
    def run_contingency_analysis(self) -> Dict[str, Any]:
        """运行故障分析"""
        if self.network is None:
            self.network = self.setup_network()
        
        # 正常运行状态
        print("1. 正常运行状态分析...")
        normal_result = self.run_power_flow()
        normal_metrics, normal_report = self.analyze_reliability(normal_result)
        
        # 线路故障分析
        print("\n2. 线路故障分析...")
        contingency_results = {}
        
        # 模拟线路故障
        for line_name in ["Line1-2", "Line2-3", "Line2-4"]:
            print(f"  分析线路 {line_name} 故障...")
            
            # 创建故障网络 - 由于PyXESXXN网络类没有copy方法，重新创建网络
            from .network_new import PyXESXXNNetwork, ComponentType, EnergyCarrier
            contingency_network = PyXESXXNNetwork()
            
            # 复制所有组件，但排除故障线路
            for bus_name, bus in self.network.buses.items():
                contingency_network.add_bus(bus_name, voltage=bus.parameters.get('voltage', 110), 
                                         frequency=bus.parameters.get('frequency', 50), carrier=bus.config.carrier)
            
            for gen_name, gen in self.network.generators.items():
                contingency_network.add_generator(gen_name, bus=gen.bus.name, capacity=gen.parameters.get('capacity', 100), carrier="electricity")
            
            for load_name, load in self.network.loads.items():
                contingency_network.add_load(load_name, bus=load.bus.name, carrier="electricity", demand=load.parameters.get('demand', 0))
            
            for line_name_copy, line in self.network.lines.items():
                if line_name_copy != line_name:  # 排除故障线路
                    contingency_network.add_line(line_name_copy, from_bus=line.from_bus.name, to_bus=line.to_bus.name, carrier="electricity",
                                               capacity=line.parameters.get('capacity', 100), 
                                               resistance=line.parameters.get('resistance', 0.01), 
                                               reactance=line.parameters.get('reactance', 0.1))
            
            # 运行故障状态潮流计算
            from .power_flow_enhanced import NewtonRaphsonSolver
            solver = NewtonRaphsonSolver(contingency_network)
            contingency_result = solver.solve()
            
            # 分析可靠性
            try:
                from .power_flow_reliability import PowerFlowReliabilityAnalyzer
                analyzer = PowerFlowReliabilityAnalyzer(contingency_network, contingency_result)
                contingency_metrics = analyzer.analyze_reliability()
                contingency_metrics_dict = contingency_metrics.to_dict()
            except Exception as e:
                print(f"    可靠性分析失败: {e}")
                contingency_metrics_dict = {}
            
            contingency_results[line_name] = {
                'result': contingency_result,
                'metrics': contingency_metrics_dict
            }
        
        return {
            'normal': {
                'result': normal_result,
                'metrics': normal_metrics,
                'report': normal_report
            },
            'contingencies': contingency_results
        }


class PowerFlowTestSuite:
    """潮流计算测试套件"""
    
    def __init__(self):
        self.examples = [
            Simple3BusExample(),
            IEEE14BusExample(),
            WindPowerIntegrationExample(),
            ContingencyAnalysisExample()
        ]
        self.test_results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("=== 潮流计算测试套件 ===")
        print(f"运行 {len(self.examples)} 个测试用例...\n")
        
        results = {}
        
        for i, example in enumerate(self.examples, 1):
            print(f"测试 {i}/{len(self.examples)}: {example.name}")
            
            try:
                if isinstance(example, ContingencyAnalysisExample):
                    result = example.run_contingency_analysis()
                else:
                    result = example.run_example()
                
                results[example.name] = {
                    'status': 'PASS',
                    'result': result
                }
                print(f"  [OK] 测试通过\n")
                
            except Exception as e:
                results[example.name] = {
                    'status': 'FAIL',
                    'error': str(e)
                }
                print(f"  [ERROR] 测试失败: {e}\n")
        
        # 统计结果
        passed = sum(1 for r in results.values() if r['status'] == 'PASS')
        failed = len(results) - passed
        
        print(f"=== 测试结果汇总 ===")
        print(f"总测试数: {len(results)}")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        print(f"通过率: {passed/len(results)*100:.1f}%")
        
        self.test_results = results
        return results
    
    def generate_test_report(self) -> str:
        """生成测试报告"""
        if not self.test_results:
            self.run_all_tests()
        
        report = []
        report.append("=== 潮流计算测试报告 ===")
        report.append("")
        
        for name, result in self.test_results.items():
            status_icon = "[OK]" if result['status'] == 'PASS' else "[ERROR]"
            report.append(f"{status_icon} {name}: {result['status']}")
            
            if result['status'] == 'FAIL':
                report.append(f"   错误: {result['error']}")
        
        # 统计信息
        passed = sum(1 for r in self.test_results.values() if r['status'] == 'PASS')
        total = len(self.test_results)
        
        report.append("")
        report.append("=== 统计信息 ===")
        report.append(f"总测试数: {total}")
        report.append(f"通过: {passed}")
        report.append(f"失败: {total - passed}")
        report.append(f"通过率: {passed/total*100:.1f}%")
        
        return "\n".join(report)


# 实用函数
def run_quick_example() -> None:
    """运行快速示例"""
    print("=== 潮流计算快速示例 ===")
    
    example = Simple3BusExample()
    result = example.run_example()
    
    print("\n示例运行完成!")


def run_comprehensive_test() -> None:
    """运行全面测试"""
    test_suite = PowerFlowTestSuite()
    results = test_suite.run_all_tests()
    
    report = test_suite.generate_test_report()
    print("\n" + report)


def create_custom_example(network_config: Dict[str, Any]) -> PowerFlowExample:
    """创建自定义示例"""
    class CustomExample(PowerFlowExample):
        def __init__(self, config):
            super().__init__(
                name=config.get('name', '自定义示例'),
                description=config.get('description', '用户自定义潮流计算示例')
            )
            self.config = config
        
        def setup_network(self) -> PyXESXXNNetwork:
            from .network_new import PyXESXXNNetwork, ComponentType, EnergyCarrier
            
            network = PyXESXXNNetwork()
            
            # 根据配置设置网络
            buses = self.config.get('buses', [])
            generators = self.config.get('generators', [])
            loads = self.config.get('loads', [])
            lines = self.config.get('lines', [])
            
            # 添加节点
            for bus in buses:
                network.add_bus(bus['name'], voltage=bus.get('v_nom', 110), 
                              carrier=EnergyCarrier.ELECTRICITY)
            
            # 添加发电机
            for gen in generators:
                network.add_generator(gen['name'], bus=gen['bus'], carrier="electricity",
                                   capacity=gen.get('p_set', 0) * 1.5)
            
            # 添加负荷
            for load in loads:
                network.add_load(load['name'], bus=load['bus'], carrier="electricity",
                              demand=load.get('p_set', 0))
            
            # 添加线路
            for line in lines:
                network.add_line(line['name'], from_bus=line['bus0'], to_bus=line['bus1'], carrier="electricity",
                               capacity=line.get('s_nom', 100), resistance=line.get('r', 0.01), reactance=line.get('x', 0.1))
            
            return network
    
    return CustomExample(network_config)


# 导出公共API
__all__ = [
    'PowerFlowExample',
    'Simple3BusExample',
    'IEEE14BusExample',
    'WindPowerIntegrationExample',
    'ContingencyAnalysisExample',
    'PowerFlowTestSuite',
    'run_quick_example',
    'run_comprehensive_test',
    'create_custom_example'
]


if __name__ == "__main__":
    # 当直接运行此文件时，执行快速示例
    run_quick_example()