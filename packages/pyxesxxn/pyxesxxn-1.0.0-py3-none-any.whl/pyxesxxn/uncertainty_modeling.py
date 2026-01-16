"""
基于PDF置信带的高阶不确定性建模模块

该模块实现了基于概率密度函数（PDF）置信带的高阶不确定性建模方法，
能够表示一系列可能分布，反映形状变化（偏态/尾部），适合长期规划场景。

主要功能：
1. PDF置信带估计：基于样本数据构建置信区间
2. 非参数分布建模：不依赖特定分布假设
3. 形状变化分析：捕捉偏态和尾部特征
4. 保守性评估：样本量对决策保守性的影响
5. 长期规划支持：适合能源系统长期不确定性分析
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from scipy import stats
from scipy.interpolate import interp1d
import warnings


@dataclass
class ConfidenceBandConfig:
    """置信带配置参数"""
    confidence_level: float = 0.95  # 置信水平
    bandwidth_method: str = "scott"  # 带宽选择方法
    num_bootstrap: int = 1000       # 自助法重采样次数
    grid_size: int = 100            # PDF网格点数
    adaptive_bandwidth: bool = True # 自适应带宽
    sample_size: int = 1000         # 样本大小
    kernel_type: str = "gaussian"   # 核函数类型


class PDFConfidenceBand:
    """PDF置信带建模类
    
    基于样本数据构建概率密度函数的置信带，能够表示分布的不确定性范围。
    """
    
    def __init__(self, config: ConfidenceBandConfig = None):
        self.config = config or ConfidenceBandConfig()
        self.sample_data = None
        self.sample_size = 0
        self.pdf_estimates = []
        self.confidence_band = None
        self.support_range = None
        
    def fit(self, data: np.ndarray) -> 'PDFConfidenceBand':
        """基于样本数据拟合PDF置信带"""
        self.sample_data = data
        self.sample_size = len(data)
        
        if self.sample_size < 10:
            warnings.warn("样本量较小，置信带估计可能不稳定")
        
        # 计算支持范围
        data_min, data_max = np.min(data), np.max(data)
        margin = 0.1 * (data_max - data_min)  # 10%边界
        self.support_range = (data_min - margin, data_max + margin)
        
        # 使用自助法估计PDF置信带
        self._bootstrap_pdf_estimation()
        
        return self
    
    def _bootstrap_pdf_estimation(self):
        """自助法PDF估计"""
        n_samples = self.sample_size
        n_bootstrap = self.config.num_bootstrap
        
        # 生成网格点
        x_grid = np.linspace(self.support_range[0], self.support_range[1], 
                            self.config.grid_size)
        
        # 存储所有自助样本的PDF估计
        pdf_estimates = []
        
        for i in range(n_bootstrap):
            # 自助重采样
            bootstrap_sample = np.random.choice(self.sample_data, size=n_samples, 
                                              replace=True)
            
            # 核密度估计 - 处理小样本情况
            try:
                if self.config.adaptive_bandwidth:
                    # 自适应带宽选择
                    kde = stats.gaussian_kde(bootstrap_sample, 
                                           bw_method=self.config.bandwidth_method)
                else:
                    # 固定带宽，对小样本使用更保守的带宽
                    if n_samples < 10:
                        # 小样本时使用更大的带宽避免数值问题
                        kde = stats.gaussian_kde(bootstrap_sample, bw_method='scott')
                    else:
                        kde = stats.gaussian_kde(bootstrap_sample)
                
                pdf_estimate = kde(x_grid)
                pdf_estimates.append(pdf_estimate)
            except (np.linalg.LinAlgError, ValueError) as e:
                # 处理数值不稳定性：使用简化方法
                if n_samples < 5:
                    # 极小样本：使用均匀分布近似
                    pdf_estimate = np.ones_like(x_grid) / (self.support_range[1] - self.support_range[0])
                else:
                    # 小样本：使用直方图平滑
                    hist, bin_edges = np.histogram(bootstrap_sample, bins=min(5, n_samples), 
                                                 density=True, range=self.support_range)
                    # 线性插值到网格点
                    pdf_estimate = np.interp(x_grid, 
                                           (bin_edges[:-1] + bin_edges[1:]) / 2, 
                                           hist, 
                                           left=0, right=0)
                pdf_estimates.append(pdf_estimate)
        
        self.pdf_estimates = np.array(pdf_estimates)
        
        # 计算置信带
        alpha = 1 - self.config.confidence_level
        lower_quantile = alpha / 2
        upper_quantile = 1 - alpha / 2
        
        self.confidence_band = {
            'x_grid': x_grid,
            'lower_bound': np.quantile(self.pdf_estimates, lower_quantile, axis=0),
            'upper_bound': np.quantile(self.pdf_estimates, upper_quantile, axis=0),
            'median_pdf': np.median(self.pdf_estimates, axis=0),
            'mean_pdf': np.mean(self.pdf_estimates, axis=0)
        }
    
    def get_confidence_band_width(self) -> np.ndarray:
        """获取置信带宽度"""
        if self.confidence_band is None:
            raise ValueError("请先调用fit方法拟合数据")
        
        return self.confidence_band['upper_bound'] - self.confidence_band['lower_bound']
    
    def assess_conservatism(self) -> Dict:
        """评估决策保守性"""
        band_width = self.get_confidence_band_width()
        avg_width = np.mean(band_width)
        max_width = np.max(band_width)
        
        # 保守性指标：置信带越宽，决策越保守
        conservatism_index = avg_width / (np.max(self.confidence_band['median_pdf']) + 1e-10)
        
        return {
            'average_band_width': avg_width,
            'max_band_width': max_width,
            'conservatism_index': conservatism_index,
            'sample_size_impact': self._assess_sample_size_impact(),
            'decision_confidence': 1 - conservatism_index  # 决策置信度
        }
    
    def _assess_sample_size_impact(self) -> Dict:
        """评估样本量对置信带的影响"""
        # 模拟不同样本量下的置信带宽度变化
        sample_sizes = [10, 30, 50, 100, 200, 500, 1000]
        band_widths = []
        
        for size in sample_sizes:
            if size > self.sample_size:
                # 使用现有数据外推
                simulated_data = np.random.choice(self.sample_data, size=size, 
                                                replace=True)
            else:
                simulated_data = self.sample_data[:size]
            
            # 简化估计：置信带宽度与1/sqrt(n)成正比
            base_width = np.mean(self.get_confidence_band_width())
            estimated_width = base_width * np.sqrt(self.sample_size / size)
            band_widths.append(estimated_width)
        
        return {
            'sample_sizes': sample_sizes,
            'estimated_band_widths': band_widths,
            'convergence_rate': self._estimate_convergence_rate(band_widths)
        }
    
    def _estimate_convergence_rate(self, band_widths: List[float]) -> float:
        """估计收敛速率"""
        if len(band_widths) < 2:
            return 0.5  # 默认收敛速率
        
        # 使用对数线性回归估计收敛速率
        sample_sizes = [10, 30, 50, 100, 200, 500, 1000]  # 直接定义样本量序列
        log_sizes = np.log([max(s, 1) for s in sample_sizes])
        log_widths = np.log([max(w, 1e-10) for w in band_widths])
        
        if len(log_sizes) > 1 and len(log_widths) > 1:
            slope, _ = np.polyfit(log_sizes, log_widths, 1)
            return -slope  # 理论收敛速率为-0.5
        
        return 0.5
    
    def detect_shape_changes(self) -> Dict:
        """检测分布形状变化"""
        if self.confidence_band is None:
            raise ValueError("请先调用fit方法拟合数据")
        
        median_pdf = self.confidence_band['median_pdf']
        x_grid = self.confidence_band['x_grid']
        
        # 计算偏度
        mean_val = np.average(x_grid, weights=median_pdf)
        std_val = np.sqrt(np.average((x_grid - mean_val)**2, weights=median_pdf))
        skewness = np.average(((x_grid - mean_val) / std_val)**3, weights=median_pdf)
        
        # 计算峰度（尾部特征）
        kurtosis = np.average(((x_grid - mean_val) / std_val)**4, weights=median_pdf) - 3
        
        # 检测多峰性
        peaks = self._find_peaks(median_pdf)
        multimodality = len(peaks) > 1
        
        return {
            'skewness': skewness,
            'kurtosis': kurtosis,
            'is_multimodal': multimodality,
            'num_peaks': len(peaks),
            'tail_behavior': self._assess_tail_behavior(),
            'shape_uncertainty': self._assess_shape_uncertainty()
        }
    
    def _find_peaks(self, pdf: np.ndarray) -> List[int]:
        """查找PDF的峰值点"""
        peaks = []
        for i in range(1, len(pdf) - 1):
            if pdf[i] > pdf[i-1] and pdf[i] > pdf[i+1]:
                peaks.append(i)
        return peaks
    
    def _assess_tail_behavior(self) -> Dict:
        """评估尾部行为"""
        lower_tail = self.confidence_band['lower_bound'][:10]  # 左尾
        upper_tail = self.confidence_band['upper_bound'][-10:]  # 右尾
        
        lower_tail_thickness = np.mean(lower_tail)
        upper_tail_thickness = np.mean(upper_tail)
        
        return {
            'left_tail_thickness': lower_tail_thickness,
            'right_tail_thickness': upper_tail_thickness,
            'tail_asymmetry': upper_tail_thickness - lower_tail_thickness,
            'has_heavy_tails': lower_tail_thickness > 0.01 or upper_tail_thickness > 0.01
        }
    
    def _assess_shape_uncertainty(self) -> float:
        """评估形状不确定性"""
        # 使用置信带上下界的差异度量形状不确定性
        shape_variation = np.mean(np.abs(self.confidence_band['upper_bound'] - 
                                       self.confidence_band['lower_bound']))
        return shape_variation


class AdvancedUncertaintyModel:
    """高级不确定性模型
    
    集成PDF置信带分析，提供完整的不确定性建模框架。
    """
    
    def __init__(self, config: ConfidenceBandConfig = None):
        self.config = config or ConfidenceBandConfig()
        self.pdf_bands = {}
        self.uncertainty_sources = {}
        
    def add_uncertainty_source(self, name: str, data: np.ndarray, 
                             config: ConfidenceBandConfig = None):
        """添加不确定性源"""
        pdf_band = PDFConfidenceBand(config)
        pdf_band.fit(data)
        
        self.pdf_bands[name] = pdf_band
        self.uncertainty_sources[name] = {
            'data': data,
            'sample_size': len(data),
            'statistics': self._compute_basic_statistics(data)
        }
    
    def estimate_confidence_band(self, data: np.ndarray, uncertainty_type: str = 'additive', 
                              uncertainty_level: float = 0.1) -> Dict:
        """估计置信带
        
        Args:
            data: 输入数据
            uncertainty_type: 不确定性类型 ('additive' 或 'multiplicative')
            uncertainty_level: 不确定性水平 (0-1)
        
        Returns:
            置信带信息字典
        """
        # 根据不确定性类型调整数据
        if uncertainty_type == 'multiplicative':
            # 乘性不确定性：数据乘以随机因子
            adjusted_data = data * (1 + np.random.normal(0, uncertainty_level, len(data)))
        else:
            # 加性不确定性（默认）：数据加上随机噪声
            adjusted_data = data + np.random.normal(0, uncertainty_level * np.std(data), len(data))
        
        pdf_band = PDFConfidenceBand(self.config)
        pdf_band.fit(adjusted_data)
        
        return {
            'lower_bound': pdf_band.confidence_band['lower_bound'],
            'upper_bound': pdf_band.confidence_band['upper_bound'],
            'median_pdf': pdf_band.confidence_band['median_pdf'],
            'mean_pdf': pdf_band.confidence_band['mean_pdf'],
            'x_grid': pdf_band.confidence_band['x_grid'],
            'bandwidth': np.mean(pdf_band.get_confidence_band_width()),
            'lower_bound_mean': np.mean(pdf_band.confidence_band['lower_bound']),
            'upper_bound_mean': np.mean(pdf_band.confidence_band['upper_bound']),
            'mean': np.mean(adjusted_data)
        }
    
    def analyze_distribution_shape(self, data: np.ndarray) -> Dict:
        """分析分布形状"""
        pdf_band = PDFConfidenceBand(self.config)
        pdf_band.fit(data)
        
        shape_analysis = pdf_band.detect_shape_changes()
        
        return {
            'skewness': shape_analysis['skewness'],
            'kurtosis': shape_analysis['kurtosis'],
            'is_multimodal': shape_analysis['is_multimodal'],
            'num_peaks': shape_analysis['num_peaks'],
            'tail_behavior': shape_analysis['tail_behavior'],
            'shape_uncertainty': shape_analysis['shape_uncertainty']
        }
    
    def _compute_basic_statistics(self, data: np.ndarray) -> Dict:
        """计算基本统计量"""
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'min': np.min(data),
            'max': np.max(data),
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data)
        }
    
    def comprehensive_uncertainty_analysis(self) -> Dict:
        """综合不确定性分析"""
        analysis_results = {}
        
        for name, pdf_band in self.pdf_bands.items():
            analysis_results[name] = {
                'confidence_band': pdf_band.confidence_band,
                'conservatism_assessment': pdf_band.assess_conservatism(),
                'shape_analysis': pdf_band.detect_shape_changes(),
                'sample_characteristics': self.uncertainty_sources[name]['statistics']
            }
        
        # 交叉不确定性分析
        analysis_results['cross_uncertainty'] = self._analyze_cross_uncertainties()
        
        return analysis_results
    
    def _analyze_cross_uncertainties(self) -> Dict:
        """分析交叉不确定性"""
        if len(self.pdf_bands) < 2:
            return {'message': '需要至少两个不确定性源进行交叉分析'}
        
        names = list(self.pdf_bands.keys())
        correlations = {}
        
        for i, name1 in enumerate(names):
            for j, name2 in enumerate(names):
                if i < j:
                    data1 = self.uncertainty_sources[name1]['data']
                    data2 = self.uncertainty_sources[name2]['data']
                    
                    # 确保数据长度一致
                    min_len = min(len(data1), len(data2))
                    corr = np.corrcoef(data1[:min_len], data2[:min_len])[0, 1]
                    
                    correlations[f"{name1}_{name2}"] = {
                        'correlation': corr,
                        'significance': self._assess_correlation_significance(corr, min_len)
                    }
        
        return correlations
    
    def _assess_correlation_significance(self, correlation: float, sample_size: int) -> str:
        """评估相关性显著性"""
        if sample_size < 30:
            return "样本量较小，显著性评估可能不准确"
        
        # 简化显著性检验
        t_stat = correlation * np.sqrt((sample_size - 2) / (1 - correlation**2))
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), sample_size - 2))
        
        if p_value < 0.01:
            return "高度显著"
        elif p_value < 0.05:
            return "显著"
        else:
            return "不显著"
    
    def generate_scenarios(self, num_scenarios: int = 100) -> Dict:
        """生成不确定性场景"""
        scenarios = {}
        
        for name, pdf_band in self.pdf_bands.items():
            # 从置信带中随机采样场景
            scenarios[name] = self._sample_from_confidence_band(
                pdf_band, num_scenarios)
        
        return scenarios
    
    def _sample_from_confidence_band(self, pdf_band: PDFConfidenceBand, 
                                   num_scenarios: int) -> np.ndarray:
        """从置信带中采样"""
        x_grid = pdf_band.confidence_band['x_grid']
        lower_bound = pdf_band.confidence_band['lower_bound']
        upper_bound = pdf_band.confidence_band['upper_bound']
        
        # 在置信带范围内均匀采样
        samples = []
        for _ in range(num_scenarios):
            # 随机选择PDF曲线
            random_pdf = np.random.uniform(lower_bound, upper_bound)
            
            # 归一化并采样
            random_pdf_normalized = random_pdf / np.sum(random_pdf)
            sample_idx = np.random.choice(len(x_grid), p=random_pdf_normalized)
            samples.append(x_grid[sample_idx])
        
        return np.array(samples)


def create_energy_demand_uncertainty_model() -> AdvancedUncertaintyModel:
    """创建能源需求不确定性模型示例"""
    
    # 生成示例数据：电力需求的不确定性
    np.random.seed(42)  # 可重复性
    
    # 基础需求模式（季节性+日变化）
    hours = 8760  # 一年小时数
    base_demand = 100 + 20 * np.sin(2 * np.pi * np.arange(hours) / 24) + \
                  30 * np.sin(2 * np.pi * np.arange(hours) / (24 * 365))
    
    # 添加不确定性（正态分布+偏态分布混合）
    normal_uncertainty = np.random.normal(0, 10, hours)
    skewed_uncertainty = stats.skewnorm.rvs(5, loc=0, scale=5, size=hours)
    
    total_demand = base_demand + 0.7 * normal_uncertainty + 0.3 * skewed_uncertainty
    
    # 创建不确定性模型
    model = AdvancedUncertaintyModel()
    
    config = ConfidenceBandConfig(
        confidence_level=0.9,
        num_bootstrap=500,
        adaptive_bandwidth=True
    )
    
    model.add_uncertainty_source("electricity_demand", total_demand, config)
    
    return model


# 导出主要类和函数
__all__ = [
    'PDFConfidenceBand',
    'AdvancedUncertaintyModel',
    'ConfidenceBandConfig',
    'create_energy_demand_uncertainty_model'
]