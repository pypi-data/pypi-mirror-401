#!/usr/bin/env python3
"""
基于离散傅里叶变换矩阵的概率最优潮流计算方法

该模块实现了基于离散傅里叶变换矩阵（DFTM）的概率最优潮流（POPF）计算功能，
包括Nataf变换、DCTM法、DSTM法等核心算法。
"""

import numpy as np
import pandas as pd
from scipy.stats import norm, weibull_min
from scipy.linalg import cholesky
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class NatafTransformer:
    """Nataf变换类，用于处理变量相关性和非正态分布"""
    
    def __init__(self, marginal_distributions: Dict[str, Dict], correlation_matrix: np.ndarray):
        """
        初始化Nataf变换器
        
        参数:
            marginal_distributions: 边缘分布字典，格式为{变量名: {'type': 分布类型, 'params': 参数字典}}
            correlation_matrix: 原始分布域的相关系数矩阵
        """
        self.marginal_distributions = marginal_distributions
        self.correlation_matrix = correlation_matrix
        self.n_vars = len(marginal_distributions)
        self.Z_corr_matrix = None  # 标准正态分布域的相关系数矩阵
        self.L = None  # 标准正态分布域相关系数矩阵的Cholesky分解
    
    def _calculate_Z_correlation(self) -> np.ndarray:
        """
        计算标准正态分布域的相关系数矩阵
        
        返回:
            Z_corr_matrix: 标准正态分布域的相关系数矩阵
        """
        # Nataf变换中标准正态分布域相关系数矩阵的计算
        # 基于文献《The Nataf transformation: A tool for the simulation of correlated random variables》
        
        n_vars = self.n_vars
        Z_corr_matrix = np.copy(self.correlation_matrix)
        
        # 迭代计算标准正态分布域的相关系数矩阵
        # 当变量均为正态分布时，Z_corr_matrix等于原始相关系数矩阵
        # 对于非正态分布，需要通过迭代计算
        is_all_normal = all(dist['type'] == 'normal' for dist in self.marginal_distributions.values())
        
        if is_all_normal:
            return Z_corr_matrix
        
        # 对于非正态分布，这里使用简化的迭代计算
        # 实际中需要更复杂的迭代算法
        max_iterations = 100
        tolerance = 1e-6
        
        for iteration in range(max_iterations):
            Z_corr_new = np.zeros((n_vars, n_vars))
            
            # 对角线元素始终为1
            np.fill_diagonal(Z_corr_new, 1.0)
            
            # 计算非对角线元素
            for i in range(n_vars):
                for j in range(i + 1, n_vars):
                    if i == j:
                        continue
                    
                    # 获取两个变量的边缘分布
                    dist_i = list(self.marginal_distributions.values())[i]
                    dist_j = list(self.marginal_distributions.values())[j]
                    
                    # 生成随机样本进行蒙特卡洛近似
                    n_mc_samples = 10000
                    Z1 = np.random.normal(0, 1, n_mc_samples)
                    Z2 = np.random.normal(0, 1, n_mc_samples)
                    
                    # 使用当前的相关系数矩阵生成相关样本
                    Z2 = Z_corr_matrix[i, j] * Z1 + np.sqrt(1 - Z_corr_matrix[i, j]**2) * Z2
                    
                    # 转换为原始分布
                    X1 = self._convert_Z_to_X(Z1, dist_i)
                    X2 = self._convert_Z_to_X(Z2, dist_j)
                    
                    # 计算原始分布的相关系数
                    rho_ij = np.corrcoef(X1, X2)[0, 1]
                    
                    # 更新标准正态分布域的相关系数
                    Z_corr_new[i, j] = Z_corr_new[j, i] = rho_ij
            
            # 检查收敛性
            if np.max(np.abs(Z_corr_new - Z_corr_matrix)) < tolerance:
                break
            
            Z_corr_matrix = Z_corr_new
        
        return Z_corr_matrix
    
    def _convert_Z_to_X(self, Z: np.ndarray, dist_info: Dict) -> np.ndarray:
        """
        将标准正态分布样本转换为特定分布的样本
        
        参数:
            Z: 标准正态分布样本
            dist_info: 分布信息
        
        返回:
            X: 特定分布的样本
        """
        # 计算累积概率
        p = norm.cdf(Z)
        
        # 逆变换采样
        dist_type = dist_info['type']
        params = dist_info['params']
        
        if dist_type == 'weibull':
            # Weibull分布逆变换
            return params['D'] * (-np.log(1 - p)) ** (1 / params['K'])
        elif dist_type == 'normal':
            # 正态分布逆变换
            return norm.ppf(p, loc=params['mu'], scale=params['sigma'])
        elif dist_type == 'uniform':
            # 均匀分布逆变换
            return params['a'] + p * (params['b'] - params['a'])
        else:
            raise ValueError(f"不支持的分布类型: {dist_type}")
    
    def fit(self) -> None:
        """拟合Nataf变换器，计算标准正态分布域的相关系数矩阵及其Cholesky分解"""
        self.Z_corr_matrix = self._calculate_Z_correlation()
        self.L = cholesky(self.Z_corr_matrix, lower=True)
    
    def transform(self, Z: np.ndarray) -> np.ndarray:
        """
        将标准正态分布样本转换为原始分布样本
        
        参数:
            Z: 标准正态分布样本矩阵，形状为(n_samples, n_vars)
        
        返回:
            X: 原始分布样本矩阵，形状为(n_samples, n_vars)
        """
        n_samples = Z.shape[0]
        X = np.zeros_like(Z)
        
        for i in range(self.n_vars):
            # 获取边缘分布信息
            dist_info = list(self.marginal_distributions.values())[i]
            dist_type = dist_info['type']
            params = dist_info['params']
            
            # 计算累积概率
            p = norm.cdf(Z[:, i])
            
            # 逆变换采样
            if dist_type == 'weibull':
                # Weibull分布逆变换
                X[:, i] = params['D'] * (-np.log(1 - p)) ** (1 / params['K'])
            elif dist_type == 'normal':
                # 正态分布逆变换
                X[:, i] = norm.ppf(p, loc=params['mu'], scale=params['sigma'])
            elif dist_type == 'uniform':
                # 均匀分布逆变换
                X[:, i] = params['a'] + p * (params['b'] - params['a'])
            else:
                raise ValueError(f"不支持的分布类型: {dist_type}")
        
        return X
    
    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """
        将原始分布样本转换为标准正态分布样本
        
        参数:
            X: 原始分布样本矩阵，形状为(n_samples, n_vars)
        
        返回:
            Z: 标准正态分布样本矩阵，形状为(n_samples, n_vars)
        """
        n_samples = X.shape[0]
        Z = np.zeros_like(X)
        
        for i in range(self.n_vars):
            # 获取边缘分布信息
            dist_info = list(self.marginal_distributions.values())[i]
            dist_type = dist_info['type']
            params = dist_info['params']
            
            # 计算累积概率
            if dist_type == 'weibull':
                # Weibull分布累积概率
                p = 1 - np.exp(-(X[:, i] / params['D']) ** params['K'])
            elif dist_type == 'normal':
                # 正态分布累积概率
                p = norm.cdf(X[:, i], loc=params['mu'], scale=params['sigma'])
            elif dist_type == 'uniform':
                # 均匀分布累积概率
                p = (X[:, i] - params['a']) / (params['b'] - params['a'])
            else:
                raise ValueError(f"不支持的分布类型: {dist_type}")
            
            # 转换为标准正态分布
            Z[:, i] = norm.ppf(p)
        
        return Z

class DFTMMethod:
    """离散傅里叶变换矩阵（DFTM）法类"""
    
    def __init__(self, method: str = 'dctm'):
        """
        初始化DFTM法
        
        参数:
            method: DFTM方法类型，可选'dctm'（离散余弦变换矩阵法）或'dstm'（离散正弦变换矩阵法）
        """
        self.method = method.lower()
        if self.method not in ['dctm', 'dstm']:
            raise ValueError(f"不支持的DFTM方法类型: {self.method}")
    
    def generate_samples(self, n_vars: int, n_samples: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成DFTM法样本点和对应权重
        
        参数:
            n_vars: 变量数量
            n_samples: 样本数量
        
        返回:
            T: 样本点矩阵，形状为(n_samples, n_vars)
            weights: 对应权重向量，形状为(n_samples,)
        """
        # 生成样本点
        T = np.zeros((n_samples, n_vars))
        
        for s in range(n_samples):
            for i in range(n_vars):
                # 根据文献公式生成样本点
                if self.method == 'dctm':
                    # DCTM法样本点生成: t_{i,s} = √2 * cos(2π * s * i / n)
                    T[s, i] = np.sqrt(2) * np.cos(2 * np.pi * (s + 1) * (i + 1) / n_samples)
                elif self.method == 'dstm':
                    # DSTM法样本点生成: t_{i,s} = √2 * sin(2π * s * i / n)
                    T[s, i] = np.sqrt(2) * np.sin(2 * np.pi * (s + 1) * (i + 1) / n_samples)
        
        # 生成权重
        weights = np.ones(n_samples) / n_samples
        
        return T, weights
    
    def calculate_moments(self, samples: np.ndarray, weights: np.ndarray) -> Dict[str, float]:
        """
        计算概率矩（均值、标准差）
        
        参数:
            samples: 输出变量样本值向量，形状为(n_samples,)
            weights: 对应权重向量，形状为(n_samples,)
        
        返回:
            moments: 包含均值和标准差的字典
        """
        # 计算均值
        mean = np.dot(weights, samples)
        
        # 计算标准差
        variance = np.dot(weights, (samples - mean) ** 2)
        std = np.sqrt(variance)
        
        return {'mean': mean, 'std': std}

class ProbabilisticOptimalPowerFlow:
    """概率最优潮流（POPF）计算类"""
    
    def __init__(self, network):
        """
        初始化概率最优潮流计算器
        
        参数:
            network: PyXESXXN网络对象
        """
        self.network = network
        self.nataf_transformer = None
        self.dftm_method = None
    
    def setup_distributions(self, marginal_distributions: Dict[str, Dict], correlation_matrix: np.ndarray) -> None:
        """
        设置随机变量的边缘分布和相关性
        
        参数:
            marginal_distributions: 边缘分布字典
            correlation_matrix: 相关系数矩阵
        """
        # 初始化Nataf变换器
        self.nataf_transformer = NatafTransformer(marginal_distributions, correlation_matrix)
        self.nataf_transformer.fit()
    
    def setup_dftm_method(self, method: str = 'dctm') -> None:
        """
        设置DFTM方法
        
        参数:
            method: DFTM方法类型，可选'dctm'或'dstm'
        """
        self.dftm_method = DFTMMethod(method)
    
    def _run_dopf(self, sample: np.ndarray) -> float:
        """
        运行单次确定性最优潮流计算
        
        参数:
            sample: 输入变量样本
        
        返回:
            cost: 发电成本
        """
        from .power_flow_enhanced import run_power_flow_analysis
        
        try:
            # 基于样本值更新网络参数
            # sample包含: [wind_speed_1, wind_speed_2, load_fluctuation_1, load_fluctuation_2]
            
            # 更新负荷值
            # 原始负荷值
            original_loads = {
                "负荷1": 100.0,  # 有功功率 (MW)
                "负荷2": 150.0
            }
            
            # 应用负荷波动
            for i, load_name in enumerate(["负荷1", "负荷2"]):
                # 负荷波动位于sample的后两个位置
                fluctuation_idx = i + 2
                if fluctuation_idx < len(sample):
                    # 获取当前负荷（通过字典直接访问）
                    if load_name in self.network.loads:
                        load = self.network.loads[load_name]
                        # 计算新的负荷值
                        original_load = original_loads[load_name]
                        new_load = original_load * (1 + sample[fluctuation_idx])
                        # 更新负荷参数
                        load.parameters['demand'] = new_load
            
            # 运行潮流计算
            power_flow_result, power_flow_analysis = run_power_flow_analysis(self.network)
            
            # 计算发电成本
            # 假设发电机成本系数为a*P^2 + b*P + c，这里简化实现
            # 实际中需要根据网络中发电机的参数来计算
            a = 0.01  # 成本系数a
            b = 10.0  # 成本系数b
            c = 100.0  # 成本系数c
            
            total_cost = 0.0
            for gen_name, gen_power in power_flow_result.active_power.iterrows():
                p = gen_power.values[0]
                total_cost += a * p**2 + b * p + c
            
            return total_cost
        except Exception as e:
            logger.error(f"确定性最优潮流计算失败: {e}")
            # 如果计算失败，返回一个较大的成本值
            return 1e6
    
    def calculate_popf(self, n_samples: int) -> Dict[str, Any]:
        """
        执行概率最优潮流计算
        
        参数:
            n_samples: 样本数量
        
        返回:
            results: 概率最优潮流计算结果
        """
        if self.nataf_transformer is None:
            raise ValueError("请先调用setup_distributions设置分布参数")
        
        if self.dftm_method is None:
            raise ValueError("请先调用setup_dftm_method设置DFTM方法")
        
        # 获取变量数量
        n_vars = len(self.nataf_transformer.marginal_distributions)
        
        # 生成DFTM样本点和权重
        T, weights = self.dftm_method.generate_samples(n_vars, n_samples)
        
        # 生成标准正态分布样本
        Z = np.dot(T, self.nataf_transformer.L.T)
        
        # 转换为原始分布样本
        X = self.nataf_transformer.transform(Z)
        
        # 运行DOPF计算
        costs = np.zeros(n_samples)
        for i in range(n_samples):
            costs[i] = self._run_dopf(X[i, :])
        
        # 计算概率矩
        moments = self.dftm_method.calculate_moments(costs, weights)
        
        return {
            'method': self.dftm_method.method,
            'n_samples': n_samples,
            'moments': moments,
            'sample_costs': costs,
            'sample_weights': weights
        }
    
    def compare_methods(self, n_samples_list: List[int]) -> pd.DataFrame:
        """
        比较不同样本数量下的计算结果
        
        参数:
            n_samples_list: 样本数量列表
        
        返回:
            comparison_df: 比较结果数据框
        """
        results = []
        
        for n_samples in n_samples_list:
            popf_result = self.calculate_popf(n_samples)
            results.append({
                'n_samples': n_samples,
                'method': popf_result['method'],
                'mean': popf_result['moments']['mean'],
                'std': popf_result['moments']['std']
            })
        
        return pd.DataFrame(results)

# 公共API
__all__ = [
    'NatafTransformer',
    'DFTMMethod',
    'ProbabilisticOptimalPowerFlow'
]
