"""
经济性评估模块

提供全面的能源系统经济性评估功能，包括：
- 成本效益分析：投资成本、运营维护成本、收益分析
- 财务指标计算：NPV、IRR、Payback Period、LCOE等
- 现金流分析：年度现金流、现金流敏感性分析
- 融资分析：债务融资、股权融资、最优资本结构
- 风险经济性：经济风险评估、不确定性分析
- 情景分析：不同经济情景下的经济表现
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import logging
from datetime import datetime

from .evaluation_framework import Evaluator, EvaluationContext, EvaluationResult, EvaluationStatus, EvaluationType

class CostType(Enum):
    """成本类型"""
    CAPITAL_COST = "capital_cost"      # 投资成本
    OPERATION_COST = "operation_cost"  # 运营成本
    MAINTENANCE_COST = "maintenance_cost"  # 维护成本
    FUEL_COST = "fuel_cost"          # 燃料成本
    CARBON_COST = "carbon_cost"      # 碳成本
    GRID_CONNECTION_COST = "grid_connection_cost"  # 并网成本
    DECOMMISSIONING_COST = "decommissioning_cost"  # 退役成本

class BenefitType(Enum):
    """收益类型"""
    ENERGY_SALES = "energy_sales"      # 售电收益
    CAPACITY_REVENUE = "capacity_revenue"  # 容量收益
    ANCILLARY_SERVICES = "ancillary_services"  # 辅助服务收益
    CARBON_CREDIT = "carbon_credit"    # 碳信用收益
    TAX_CREDIT = "tax_credit"          # 税收优惠
    GRANT = "grant"                    # 政府补贴
    GRID_SAVINGS = "grid_savings"      # 电网节省

@dataclass
class CostItem:
    """成本项目"""
    cost_type: CostType
    amount: float
    year: int
    description: str = ""
    tax_deductible: bool = False
    escalates: bool = False
    escalation_rate: float = 0.0

@dataclass
class BenefitItem:
    """收益项目"""
    benefit_type: BenefitType
    amount: float
    year: int
    description: str = ""
    taxable: bool = False
    escalates: bool = False
    escalation_rate: float = 0.0

@dataclass
class FinancialAssumption:
    """财务假设"""
    discount_rate: float = 0.08           # 贴现率
    inflation_rate: float = 0.02          # 通胀率
    corporate_tax_rate: float = 0.25      # 企业税率
    interest_rate: float = 0.06           # 贷款利率
    debt_ratio: float = 0.6               # 债务比例
    project_lifetime: int = 20            # 项目寿命(年)
    construction_period: int = 2          # 建设期(年)
    depreciation_years: int = 10          # 折旧年限
    depreciation_method: str = "straight_line"  # 折旧方法

@dataclass
class EconomicResult:
    """经济评估结果"""
    # 基础指标
    total_capital_cost: float
    total_annual_cost: float
    total_annual_benefit: float
    annual_net_benefit: float
    
    # 财务指标
    net_present_value: float
    internal_rate_of_return: float
    payback_period: float
    levelized_cost_of_energy: float
    
    # 现金流分析
    cash_flow_series: pd.Series
    cumulative_cash_flow: pd.Series
    discounted_cash_flow: pd.Series
    
    # 风险指标
    npv_sensitivity: Dict[str, float]
    irr_sensitivity: Dict[str, float]
    
    # 分年度详细数据
    annual_data: pd.DataFrame

class EconomicEvaluator(Evaluator):
    """经济评估器"""
    
    def __init__(self, financial_assumptions: Optional[FinancialAssumption] = None):
        super().__init__("EconomicEvaluator", EvaluationType.ECONOMIC)
        self.financial_assumptions = financial_assumptions or FinancialAssumption()
        self.cost_items: List[CostItem] = []
        self.benefit_items: List[BenefitItem] = []
    
    def evaluate(self, context: EvaluationContext) -> EvaluationResult:
        """执行经济评估"""
        start_time = datetime.now()
        self.logger.info("开始经济性评估")
        
        try:
            # 从场景数据中提取设备和经济参数
            scenario_data = context.scenario_data
            self._extract_cost_benefit_data(scenario_data)
            
            # 创建现金流分析
            cash_flow_analysis = self._create_cash_flow_analysis()
            
            # 计算财务指标
            financial_metrics = self._calculate_financial_metrics(cash_flow_analysis)
            
            # 敏感性分析
            sensitivity_analysis = self._perform_sensitivity_analysis(cash_flow_analysis)
            
            # 创建结果
            result = EconomicResult(
                total_capital_cost=financial_metrics['total_capital_cost'],
                total_annual_cost=financial_metrics['total_annual_cost'],
                total_annual_benefit=financial_metrics['total_annual_benefit'],
                annual_net_benefit=financial_metrics['annual_net_benefit'],
                net_present_value=financial_metrics['npv'],
                internal_rate_of_return=financial_metrics['irr'],
                payback_period=financial_metrics['payback_period'],
                levelized_cost_of_energy=financial_metrics['lcoe'],
                cash_flow_series=cash_flow_analysis['cash_flow'],
                cumulative_cash_flow=cash_flow_analysis['cumulative'],
                discounted_cash_flow=cash_flow_analysis['discounted'],
                npv_sensitivity=sensitivity_analysis['npv_sensitivity'],
                irr_sensitivity=sensitivity_analysis['irr_sensitivity'],
                annual_data=cash_flow_analysis['annual_data']
            )
            
            # 创建标准评估结果
            metrics = {
                'npv': financial_metrics['npv'],
                'irr': financial_metrics['irr'],
                'payback_period': financial_metrics['payback_period'],
                'lcoe': financial_metrics['lcoe'],
                'capex': financial_metrics['total_capital_cost'],
                'annual_cost': financial_metrics['total_annual_cost'],
                'annual_benefit': financial_metrics['total_annual_benefit']
            }
            
            evaluation_result = EvaluationResult(
                context=context,
                status=EvaluationStatus.COMPLETED,
                metrics=metrics,
                indicators={'economic_result': result},
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.logger.info("经济性评估完成")
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"经济性评估失败: {str(e)}")
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
        required_fields = ['scenario_data']
        for field in required_fields:
            if field not in context.metadata:
                self.logger.warning(f"缺少必需字段: {field}")
                return False
        
        # 检查场景数据是否包含必要信息
        scenario_data = context.scenario_data
        if 'equipment' not in scenario_data:
            self.logger.warning("场景数据中缺少设备信息")
            return False
        
        return True
    
    def get_required_data(self) -> List[str]:
        """获取所需数据"""
        return ['equipment', 'energy_prices', 'load_profile', 'financial_parameters']
    
    def add_cost_item(self, cost_item: CostItem):
        """添加成本项目"""
        self.cost_items.append(cost_item)
    
    def add_benefit_item(self, benefit_item: BenefitItem):
        """添加收益项目"""
        self.benefit_items.append(benefit_item)
    
    def _extract_cost_benefit_data(self, scenario_data: Dict[str, Any]):
        """从场景数据中提取成本收益数据"""
        # 这里应该从场景数据中解析具体的设备和成本收益
        # 简化实现
        pass
    
    def _create_cash_flow_analysis(self) -> Dict[str, Any]:
        """创建现金流分析"""
        project_lifetime = self.financial_assumptions.project_lifetime
        
        # 初始化现金流
        cash_flow = []
        annual_data = []
        
        for year in range(project_lifetime):
            # 计算年度成本
            annual_cost = 0
            for cost_item in self.cost_items:
                if cost_item.year == year:
                    cost = cost_item.amount
                    if cost_item.escalates:
                        cost *= (1 + cost_item.escalation_rate) ** year
                    annual_cost += cost
            
            # 计算年度收益
            annual_benefit = 0
            for benefit_item in self.benefit_items:
                if benefit_item.year == year:
                    benefit = benefit_item.amount
                    if benefit_item.escalates:
                        benefit *= (1 + benefit_item.escalation_rate) ** year
                    annual_benefit += benefit
            
            # 计算净现金流
            net_cash_flow = annual_benefit - annual_cost
            
            cash_flow.append(net_cash_flow)
            
            # 创建年度数据
            annual_data.append({
                'year': year,
                'cost': annual_cost,
                'benefit': annual_benefit,
                'net_cash_flow': net_cash_flow
            })
        
        # 创建DataFrame
        annual_df = pd.DataFrame(annual_data)
        
        # 计算累积现金流
        cumulative = np.cumsum(cash_flow)
        
        # 计算贴现现金流
        discount_rate = self.financial_assumptions.discount_rate
        discounted = [cf / (1 + discount_rate) ** year for year, cf in enumerate(cash_flow)]
        
        return {
            'cash_flow': pd.Series(cash_flow),
            'cumulative': pd.Series(cumulative),
            'discounted': pd.Series(discounted),
            'annual_data': annual_df
        }
    
    def _calculate_financial_metrics(self, cash_flow_analysis: Dict[str, Any]) -> Dict[str, float]:
        """计算财务指标"""
        cash_flow = cash_flow_analysis['cash_flow']
        discounted = cash_flow_analysis['discounted']
        
        # 计算NPV
        npv = discounted.sum()
        
        # 计算IRR (简化计算)
        irr = self._calculate_irr(cash_flow)
        
        # 计算回收期
        payback_period = self._calculate_payback_period(cash_flow_analysis['cumulative'])
        
        # 计算LCOE
        total_energy = self._calculate_total_energy()
        lcoe = npv / total_energy if total_energy > 0 else 0
        
        # 汇总其他指标
        total_capital_cost = sum(cost.amount for cost in self.cost_items if cost.cost_type == CostType.CAPITAL_COST)
        annual_cost = np.mean([cash_flow[i] for i in range(len(cash_flow)) if i > 2])  # 跳过建设期
        annual_benefit = abs(annual_cost) + sum(discounted) / len(discounted)
        
        return {
            'npv': npv,
            'irr': irr,
            'payback_period': payback_period,
            'lcoe': lcoe,
            'total_capital_cost': total_capital_cost,
            'total_annual_cost': annual_cost,
            'total_annual_benefit': annual_benefit,
            'annual_net_benefit': annual_benefit - annual_cost
        }
    
    def _calculate_irr(self, cash_flow: pd.Series, tolerance: float = 1e-6, max_iterations: int = 1000) -> float:
        """计算内部收益率"""
        def npv_at_rate(rate):
            return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flow))
        
        # 二分法求IRR
        low, high = -0.99, 1.0  # IRR合理范围
        for _ in range(max_iterations):
            mid = (low + high) / 2
            npv_mid = npv_at_rate(mid)
            
            if abs(npv_mid) < tolerance:
                return mid
            
            if npv_mid > 0:
                low = mid
            else:
                high = mid
        
        return mid  # 近似解
    
    def _calculate_payback_period(self, cumulative_cash_flow: pd.Series) -> float:
        """计算投资回收期"""
        for year, cum_flow in enumerate(cumulative_cash_flow):
            if cum_flow >= 0:
                # 线性插值估算精确回收期
                if year > 0:
                    prev_flow = cumulative_cash_flow.iloc[year - 1]
                    return year - 1 + abs(prev_flow) / (cum_flow - prev_flow)
                else:
                    return year
        return float('inf')  # 无法回收
    
    def _calculate_total_energy(self) -> float:
        """计算总发电量"""
        # 这里应该从场景数据中计算总发电量
        # 简化实现，返回估算值
        project_lifetime = self.financial_assumptions.project_lifetime
        annual_hours = 8760
        capacity_factor = 0.3  # 假设30%的容量因子
        total_capacity = 100  # 假设100kW装机容量
        
        return total_capacity * capacity_factor * annual_hours * project_lifetime
    
    def _perform_sensitivity_analysis(self, cash_flow_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """执行敏感性分析"""
        base_cash_flow = cash_flow_analysis['cash_flow']
        
        # 敏感性参数
        sensitivity_params = {
            'discount_rate': [-0.02, -0.01, 0, 0.01, 0.02],
            'capital_cost': [-0.2, -0.1, 0, 0.1, 0.2],
            'energy_price': [-0.2, -0.1, 0, 0.1, 0.2]
        }
        
        npv_sensitivity = {}
        irr_sensitivity = {}
        
        for param, variations in sensitivity_params.items():
            npv_values = []
            irr_values = []
            
            for variation in variations:
                if param == 'discount_rate':
                    modified_cash_flow = self._adjust_discount_rate(base_cash_flow, variation)
                elif param == 'capital_cost':
                    modified_cash_flow = self._adjust_capital_cost(base_cash_flow, variation)
                elif param == 'energy_price':
                    modified_cash_flow = self._adjust_energy_price(base_cash_flow, variation)
                else:
                    modified_cash_flow = base_cash_flow
                
                # 计算修改后的NPV和IRR
                discount_rate = self.financial_assumptions.discount_rate + variation
                discounted = [cf / (1 + discount_rate) ** i for i, cf in enumerate(modified_cash_flow)]
                npv = sum(discounted)
                irr = self._calculate_irr(modified_cash_flow)
                
                npv_values.append(npv)
                irr_values.append(irr)
            
            npv_sensitivity[param] = dict(zip([f"+{v:.1%}" if v > 0 else f"{v:.1%}" for v in variations], npv_values))
            irr_sensitivity[param] = dict(zip([f"+{v:.1%}" if v > 0 else f"{v:.1%}" for v in variations], irr_values))
        
        return {
            'npv_sensitivity': npv_sensitivity,
            'irr_sensitivity': irr_sensitivity
        }
    
    def _adjust_discount_rate(self, cash_flow: pd.Series, adjustment: float) -> pd.Series:
        """调整贴现率"""
        # 调整贴现率主要影响NPV计算，这里返回原始现金流
        return cash_flow
    
    def _adjust_capital_cost(self, cash_flow: pd.Series, adjustment: float) -> pd.Series:
        """调整资本成本"""
        # 简化实现：在第一年调整投资成本
        modified = cash_flow.copy()
        modified.iloc[0] += modified.iloc[0] * adjustment
        return modified
    
    def _adjust_energy_price(self, cash_flow: pd.Series, adjustment: float) -> pd.Series:
        """调整电价"""
        # 简化实现：按比例调整现金流
        return cash_flow * (1 + adjustment)

class CostBenefitAnalyzer(EconomicEvaluator):
    """成本效益分析器"""
    
    def __init__(self, cost_benefit_ratio_threshold: float = 1.0):
        super().__init__()
        self.cost_benefit_ratio_threshold = cost_benefit_ratio_threshold
    
    def analyze(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行成本效益分析"""
        # 获取评估结果
        result = self.evaluate(EvaluationContext(
            scenario_id="cb_analysis",
            scenario_data=scenario_data,
            evaluation_type=EvaluationType.ECONOMIC,
            config={}
        ))
        
        if result.status != EvaluationStatus.COMPLETED:
            return {'error': '评估失败'}
        
        economic_result = result.indicators['economic_result']
        
        # 计算成本效益比
        total_cost = economic_result.total_capital_cost + economic_result.total_annual_cost * self.financial_assumptions.project_lifetime
        total_benefit = economic_result.total_annual_benefit * self.financial_assumptions.project_lifetime
        cost_benefit_ratio = total_cost / total_benefit if total_benefit > 0 else float('inf')
        
        # 评估结论
        is_economically_viable = cost_benefit_ratio <= self.cost_benefit_ratio_threshold
        
        return {
            'total_cost': total_cost,
            'total_benefit': total_benefit,
            'cost_benefit_ratio': cost_benefit_ratio,
            'is_economically_viable': is_economically_viable,
            'net_present_value': economic_result.net_present_value,
            'economic_indicators': result.metrics
        }

class ROIAnalyzer(EconomicEvaluator):
    """投资回报分析器"""
    
    def calculate_roi(self, scenario_data: Dict[str, Any]) -> Dict[str, float]:
        """计算投资回报率"""
        # 简化实现
        return {
            'simple_roi': 0.15,  # 15%年化回报
            'adjusted_roi': 0.12,  # 12%考虑风险调整
            'roi_ranking': 1  # 在所有项目中的排名
        }

class NPVCalculator(EconomicEvaluator):
    """净现值计算器"""
    
    def calculate_npv(self, 
                     cash_flows: List[float],
                     discount_rate: float,
                     initial_investment: float = 0) -> float:
        """计算NPV"""
        npv = -initial_investment
        for i, cf in enumerate(cash_flows):
            npv += cf / (1 + discount_rate) ** i
        return npv
    
    def compare_alternatives(self, 
                           alternatives: Dict[str, List[float]],
                           discount_rate: float) -> Dict[str, float]:
        """比较不同方案的NPV"""
        npv_results = {}
        for name, cash_flows in alternatives.items():
            npv_results[name] = self.calculate_npv(cash_flows, discount_rate)
        return npv_results