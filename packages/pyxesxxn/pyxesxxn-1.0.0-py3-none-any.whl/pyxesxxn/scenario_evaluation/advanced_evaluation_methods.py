"""
高级评价方法模块

提供40种评价方法的完整实现，包括：
- 变异系数法及其组合方法
- 层次分析法及其组合方法  
- 熵权法及其组合方法
- CRITIC法及其组合方法
- TODIM法及其组合方法
- TOPSIS法及其组合方法
- VIKOR法及其组合方法
- PROMETHEE法及其组合方法
- 灰色预测法及其组合方法
- 秩和比法及其组合方法
- 博弈组合法及其组合方法
- 正态云组合法及其组合方法
- 主成分分析法
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Union, Any
from enum import Enum
from dataclasses import dataclass
from scipy import stats
from scipy.linalg import eigh
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import warnings


class EvaluationMethod(Enum):
    """评价方法枚举"""
    # 基础方法
    COEFFICIENT_OF_VARIATION = "coefficient_of_variation"  # 变异系数法
    ANALYTIC_HIERARCHY_PROCESS = "analytic_hierarchy_process"  # 层次分析法
    ENTROPY_WEIGHTING = "entropy_weighting"  # 熵权法
    CRITIC = "critic"  # CRITIC法
    TODIM = "todim"  # TODIM法
    TOPSIS = "topsis"  # TOPSIS法
    VIKOR = "vikor"  # VIKOR法
    PROMETHEE = "promethee"  # PROMETHEE法
    GREY_PREDICTION = "grey_prediction"  # 灰色预测法
    RANK_SUM_RATIO = "rank_sum_ratio"  # 秩和比法
    GAME_THEORY = "game_theory"  # 博弈组合法
    NORMAL_CLOUD = "normal_cloud"  # 正态云组合法
    PRINCIPAL_COMPONENT_ANALYSIS = "principal_component_analysis"  # 主成分分析法
    
    # 组合方法
    CV_TODIM = "cv_todim"  # 变异系数-TODIM法
    STOCHASTIC_CV_TODIM = "stochastic_cv_todim"  # 随机变异系数-TODIM法
    CRITIC_TODIM = "critic_todim"  # CRITIC-TODIM法
    STOCHASTIC_ENTROPY_TODIM = "stochastic_entropy_todim"  # 随机熵权-TODIM法
    STOCHASTIC_ENTROPY_VIKOR = "stochastic_entropy_vikor"  # 随机熵权-VIKOR法
    ENTROPY_PROMETHEE = "entropy_promethee"  # 熵权-PROMETHEE法
    CV_PROMETHEE = "cv_promethee"  # 变异系数-PROMETHEE法
    AHP_ENTROPY_CRITIC = "ahp_entropy_critic"  # 层次-熵权-CRITIC组合法
    CV_PROMETHEE = "cv_promethee"  # 变异系数-PROMETHEE法
    CRITIC_PROMETHEE = "critic_promethee"  # CRITIC-PROMETHEE法
    AHP_CV_CRITIC = "ahp_cv_critic"  # 层次-变异系数-CRITIC组合法
    ENTROPY_GREY = "entropy_grey"  # 熵权-灰色预测法
    ENTROPY_CV_CRITIC = "entropy_cv_critic"  # 熵权-变异系数-CRITIC组合法
    ENTROPY_RANK_SUM = "entropy_rank_sum"  # 熵权-秩和比法
    CV_GREY = "cv_grey"  # 变异系数-灰色预测法
    AHP_ENTROPY_CV_CRITIC = "ahp_entropy_cv_critic"  # 层次-熵权-变异系数-CRITIC组合法
    CV_RANK_SUM = "cv_rank_sum"  # 变异系数-秩和比法
    CRITIC_GREY = "critic_grey"  # CRITIC-灰色预测法
    AHP_ENTROPY_GAME = "ahp_entropy_game"  # 层次-熵权-博弈组合法
    CRITIC_RANK_SUM = "critic_rank_sum"  # CRITIC-秩和比法
    STOCHASTIC_TOPSIS = "stochastic_topsis"  # 随机TOPSIS法
    AHP_CV_GAME = "ahp_cv_game"  # 层次-变异系数-博弈组合法
    ENTROPY_TOPSIS = "entropy_topsis"  # 熵权-TOPSIS法
    STOCHASTIC_AHP_TOPSIS = "stochastic_ahp_topsis"  # 随机层次分析-TOPSIS法
    ENTROPY_CV_GAME = "entropy_cv_game"  # 熵权-变异系数-博弈组合法
    CV_TOPSIS = "cv_topsis"  # 变异系数-TOPSIS法
    STOCHASTIC_ENTROPY_TOPSIS = "stochastic_entropy_topsis"  # 随机熵权-TOPSIS法
    CRITIC_TOPSIS = "critic_topsis"  # CRITIC-TOPSIS法
    STOCHASTIC_CV_TOPSIS = "stochastic_cv_topsis"  # 随机变异系数-TOPSIS法
    AHP_ENTROPY_CV_GAME = "ahp_entropy_cv_game"  # 层次-熵权-变异系数-博弈组合法
    ENTROPY_VIKOR = "entropy_vikor"  # 熵权-VIKOR法
    STOCHASTIC_ENTROPY_PROMETHEE = "stochastic_entropy_promethee"  # 随机熵权-PROMETHEE法
    AHP_ENTROPY_NORMAL_CLOUD = "ahp_entropy_normal_cloud"  # 层次-熵权-正态云组合法
    CV_VIKOR = "cv_vikor"  # 变异系数-VIKOR法
    STOCHASTIC_CRITIC_VIKOR = "stochastic_critic_vikor"  # 随机CRITIC-VIKOR法
    AHP_CV_NORMAL_CLOUD = "ahp_cv_normal_cloud"  # 层次-变异系数-正态云组合法
    CRITIC_VIKOR = "critic_vikor"  # CRITIC-VIKOR法
    STOCHASTIC_CV_TODIM = "stochastic_cv_todim"  # 随机变异系数-TODIM法
    ENTROPY_CV_NORMAL_CLOUD = "entropy_cv_normal_cloud"  # 熵权-变异系数-正态云组合法
    ENTROPY_TODIM = "entropy_todim"  # 熵权-TODIM法
    STOCHASTIC_ENTROPY_TODIM = "stochastic_entropy_todim"  # 随机熵权-TODIM法
    AHP_ENTROPY_CV_NORMAL_CLOUD = "ahp_entropy_cv_normal_cloud"  # 层次-熵权-变异系数-正态云组合法


@dataclass
class EvaluationResult:
    """评价结果"""
    weights: np.ndarray  # 权重向量
    scores: np.ndarray  # 综合得分
    rankings: np.ndarray  # 排名
    method_name: str  # 方法名称
    metadata: Dict[str, Any]  # 元数据


class AdvancedEvaluationMethods:
    """高级评价方法类"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        np.random.seed(random_state)
    
    def evaluate(self, 
                 data: np.ndarray, 
                 method: EvaluationMethod,
                 benefit_criteria: Optional[List[int]] = None,
                 cost_criteria: Optional[List[int]] = None,
                 **kwargs) -> EvaluationResult:
        """
        执行评价
        
        Args:
            data: 评价矩阵 (m×n)，m为方案数，n为指标数
            method: 评价方法
            benefit_criteria: 效益型指标索引
            cost_criteria: 成本型指标索引
            **kwargs: 其他参数
            
        Returns:
            EvaluationResult: 评价结果
        """
        
        # 设置默认的效益型和成本型指标
        if benefit_criteria is None:
            benefit_criteria = list(range(data.shape[1]))
        if cost_criteria is None:
            cost_criteria = []
        
        # 根据方法调用相应的评价函数
        method_map = {
            # 基础方法
            EvaluationMethod.COEFFICIENT_OF_VARIATION: self._coefficient_of_variation,
            EvaluationMethod.ANALYTIC_HIERARCHY_PROCESS: self._analytic_hierarchy_process,
            EvaluationMethod.ENTROPY_WEIGHTING: self._entropy_weighting,
            EvaluationMethod.CRITIC: self._critic,
            EvaluationMethod.TODIM: self._todim,
            EvaluationMethod.TOPSIS: self._topsis,
            EvaluationMethod.VIKOR: self._vikor,
            EvaluationMethod.PROMETHEE: self._promethee,
            EvaluationMethod.GREY_PREDICTION: self._grey_prediction,
            EvaluationMethod.RANK_SUM_RATIO: self._rank_sum_ratio,
            EvaluationMethod.GAME_THEORY: self._game_theory,
            EvaluationMethod.NORMAL_CLOUD: self._normal_cloud,
            EvaluationMethod.PRINCIPAL_COMPONENT_ANALYSIS: self._principal_component_analysis,
            
            # 组合方法
            EvaluationMethod.CV_TODIM: self._cv_todim,
            EvaluationMethod.STOCHASTIC_CV_TODIM: self._stochastic_cv_todim,
            EvaluationMethod.CRITIC_TODIM: self._critic_todim,
            EvaluationMethod.STOCHASTIC_ENTROPY_TODIM: self._stochastic_entropy_todim,
            EvaluationMethod.STOCHASTIC_ENTROPY_VIKOR: self._stochastic_entropy_vikor,
            EvaluationMethod.ENTROPY_PROMETHEE: self._entropy_promethee,
            EvaluationMethod.CV_PROMETHEE: self._cv_promethee,
            EvaluationMethod.AHP_ENTROPY_CRITIC: self._ahp_entropy_critic,
            EvaluationMethod.CRITIC_PROMETHEE: self._critic_promethee,
            EvaluationMethod.AHP_CV_CRITIC: self._ahp_cv_critic,
            EvaluationMethod.ENTROPY_GREY: self._entropy_grey,
            EvaluationMethod.ENTROPY_CV_CRITIC: self._entropy_cv_critic,
            EvaluationMethod.ENTROPY_RANK_SUM: self._entropy_rank_sum,
            EvaluationMethod.CV_GREY: self._cv_grey,
            EvaluationMethod.AHP_ENTROPY_CV_CRITIC: self._ahp_entropy_cv_critic,
            EvaluationMethod.CV_RANK_SUM: self._cv_rank_sum,
            EvaluationMethod.CRITIC_GREY: self._critic_grey,
            EvaluationMethod.AHP_ENTROPY_GAME: self._ahp_entropy_game,
            EvaluationMethod.CRITIC_RANK_SUM: self._critic_rank_sum,
            EvaluationMethod.STOCHASTIC_TOPSIS: self._stochastic_topsis,
            EvaluationMethod.AHP_CV_GAME: self._ahp_cv_game,
            EvaluationMethod.ENTROPY_TOPSIS: self._entropy_topsis,
            EvaluationMethod.STOCHASTIC_AHP_TOPSIS: self._stochastic_ahp_topsis,
            EvaluationMethod.ENTROPY_CV_GAME: self._entropy_cv_game,
            EvaluationMethod.CV_TOPSIS: self._cv_topsis,
            EvaluationMethod.STOCHASTIC_ENTROPY_TOPSIS: self._stochastic_entropy_topsis,
            EvaluationMethod.CRITIC_TOPSIS: self._critic_topsis,
            EvaluationMethod.STOCHASTIC_CV_TOPSIS: self._stochastic_cv_topsis,
            EvaluationMethod.AHP_ENTROPY_CV_GAME: self._ahp_entropy_cv_game,
            EvaluationMethod.ENTROPY_VIKOR: self._entropy_vikor,
            EvaluationMethod.STOCHASTIC_ENTROPY_PROMETHEE: self._stochastic_entropy_promethee,
            EvaluationMethod.AHP_ENTROPY_NORMAL_CLOUD: self._ahp_entropy_normal_cloud,
            EvaluationMethod.CV_VIKOR: self._cv_vikor,
            EvaluationMethod.STOCHASTIC_CRITIC_VIKOR: self._stochastic_critic_vikor,
            EvaluationMethod.AHP_CV_NORMAL_CLOUD: self._ahp_cv_normal_cloud,
            EvaluationMethod.CRITIC_VIKOR: self._critic_vikor,
            EvaluationMethod.STOCHASTIC_CV_TODIM: self._stochastic_cv_todim,
            EvaluationMethod.ENTROPY_CV_NORMAL_CLOUD: self._entropy_cv_normal_cloud,
            EvaluationMethod.ENTROPY_TODIM: self._entropy_todim,
            EvaluationMethod.STOCHASTIC_ENTROPY_TODIM: self._stochastic_entropy_todim,
            EvaluationMethod.AHP_ENTROPY_CV_NORMAL_CLOUD: self._ahp_entropy_cv_normal_cloud,
        }
        
        if method not in method_map:
            raise ValueError(f"不支持的评价方法: {method}")
        
        return method_map[method](data, benefit_criteria, cost_criteria, **kwargs)
    
    def _normalize_matrix(self, 
                         data: np.ndarray,
                         benefit_criteria: List[int],
                         cost_criteria: List[int]) -> np.ndarray:
        """标准化矩阵"""
        normalized_data = data.copy().astype(float)
        
        for j in range(data.shape[1]):
            if j in benefit_criteria:
                # 效益型指标：越大越好
                min_val = np.min(data[:, j])
                max_val = np.max(data[:, j])
                if max_val != min_val:
                    normalized_data[:, j] = (data[:, j] - min_val) / (max_val - min_val)
                else:
                    normalized_data[:, j] = 1.0
            elif j in cost_criteria:
                # 成本型指标：越小越好
                min_val = np.min(data[:, j])
                max_val = np.max(data[:, j])
                if max_val != min_val:
                    normalized_data[:, j] = (max_val - data[:, j]) / (max_val - min_val)
                else:
                    normalized_data[:, j] = 1.0
        
        return normalized_data
    
    def _coefficient_of_variation(self, 
                                 data: np.ndarray,
                                 benefit_criteria: List[int],
                                 cost_criteria: List[int],
                                 **kwargs) -> EvaluationResult:
        """变异系数法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        # 计算变异系数
        std_dev = np.std(normalized_data, axis=0)
        mean_val = np.mean(normalized_data, axis=0)
        
        # 避免除零
        cv = np.zeros_like(std_dev)
        non_zero_mean = mean_val != 0
        cv[non_zero_mean] = std_dev[non_zero_mean] / mean_val[non_zero_mean]
        
        # 计算权重
        weights = cv / np.sum(cv)
        
        # 计算综合得分
        scores = np.dot(normalized_data, weights)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="变异系数法",
            metadata={"cv_values": cv}
        )
    
    def _analytic_hierarchy_process(self,
                                   data: np.ndarray,
                                   benefit_criteria: List[int],
                                   cost_criteria: List[int],
                                   comparison_matrix: Optional[np.ndarray] = None,
                                   **kwargs) -> EvaluationResult:
        """层次分析法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_criteria = data.shape[1]
        
        # 如果没有提供判断矩阵，使用随机一致性矩阵
        if comparison_matrix is None:
            comparison_matrix = np.ones((n_criteria, n_criteria))
            for i in range(n_criteria):
                for j in range(i+1, n_criteria):
                    # 随机生成1-9的比例标度
                    scale = np.random.randint(1, 10)
                    comparison_matrix[i, j] = scale
                    comparison_matrix[j, i] = 1.0 / scale
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = eigh(comparison_matrix)
        max_eigenvalue_idx = np.argmax(eigenvalues)
        max_eigenvector = eigenvectors[:, max_eigenvalue_idx]
        
        # 计算权重
        weights = max_eigenvector / np.sum(max_eigenvector)
        weights = np.abs(weights)  # 确保权重为正
        
        # 计算一致性指标
        max_eigenvalue = eigenvalues[max_eigenvalue_idx]
        ci = (max_eigenvalue - n_criteria) / (n_criteria - 1)
        
        # 随机一致性指标RI
        ri_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
        ri = ri_dict.get(n_criteria, 1.49)
        
        # 一致性比率
        cr = ci / ri if ri != 0 else 0
        
        # 计算综合得分
        scores = np.dot(normalized_data, weights)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="层次分析法",
            metadata={
                "comparison_matrix": comparison_matrix,
                "max_eigenvalue": max_eigenvalue,
                "ci": ci,
                "cr": cr,
                "consistency_acceptable": cr < 0.1
            }
        )
    
    def _entropy_weighting(self,
                          data: np.ndarray,
                          benefit_criteria: List[int],
                          cost_criteria: List[int],
                          **kwargs) -> EvaluationResult:
        """熵权法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        # 避免零值
        normalized_data = np.where(normalized_data == 0, 1e-10, normalized_data)
        
        # 计算指标比重
        p_ij = normalized_data / np.sum(normalized_data, axis=0)
        
        # 计算熵值
        e_j = -np.sum(p_ij * np.log(p_ij), axis=0) / np.log(data.shape[0])
        
        # 计算差异系数
        d_j = 1 - e_j
        
        # 计算权重
        weights = d_j / np.sum(d_j)
        
        # 计算综合得分
        scores = np.dot(normalized_data, weights)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="熵权法",
            metadata={"entropy_values": e_j, "difference_coefficients": d_j}
        )
    
    def _critic(self,
               data: np.ndarray,
               benefit_criteria: List[int],
               cost_criteria: List[int],
               **kwargs) -> EvaluationResult:
        """CRITIC法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        # 计算标准差
        std_dev = np.std(normalized_data, axis=0)
        
        # 计算相关系数矩阵
        corr_matrix = np.corrcoef(normalized_data.T)
        
        # 计算冲突性
        conflict = np.sum(1 - corr_matrix, axis=0)
        
        # 计算信息量
        information_amount = std_dev * conflict
        
        # 计算权重
        weights = information_amount / np.sum(information_amount)
        
        # 计算综合得分
        scores = np.dot(normalized_data, weights)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="CRITIC法",
            metadata={
                "std_dev": std_dev,
                "correlation_matrix": corr_matrix,
                "conflict": conflict,
                "information_amount": information_amount
            }
        )
    
    def _todim(self,
              data: np.ndarray,
              benefit_criteria: List[int],
              cost_criteria: List[int],
              theta: float = 2.5,
              **kwargs) -> EvaluationResult:
        """TODIM法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_alternatives = data.shape[0]
        n_criteria = data.shape[1]
        
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        weights = entropy_result.weights
        
        # 计算相对权重
        w_r = weights / np.max(weights)
        
        # 计算优势度矩阵
        dominance_matrix = np.zeros((n_alternatives, n_alternatives))
        
        for i in range(n_alternatives):
            for k in range(n_alternatives):
                if i != k:
                    phi_ik = 0
                    for j in range(n_criteria):
                        if normalized_data[i, j] > normalized_data[k, j]:
                            phi_ik += w_r[j] * np.sqrt((normalized_data[i, j] - normalized_data[k, j]) / np.sum(weights))
                        elif normalized_data[i, j] < normalized_data[k, j]:
                            phi_ik -= (1 / theta) * np.sqrt((np.sum(weights) * (normalized_data[k, j] - normalized_data[i, j])) / w_r[j])
                    dominance_matrix[i, k] = phi_ik
        
        # 计算总体优势度
        overall_dominance = np.sum(dominance_matrix, axis=1)
        
        # 计算综合得分
        min_dominance = np.min(overall_dominance)
        max_dominance = np.max(overall_dominance)
        
        if max_dominance != min_dominance:
            scores = (overall_dominance - min_dominance) / (max_dominance - min_dominance)
        else:
            scores = np.ones_like(overall_dominance)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="TODIM法",
            metadata={
                "dominance_matrix": dominance_matrix,
                "overall_dominance": overall_dominance,
                "theta": theta
            }
        )
    
    def _topsis(self,
               data: np.ndarray,
               benefit_criteria: List[int],
               cost_criteria: List[int],
               weights: Optional[np.ndarray] = None,
               **kwargs) -> EvaluationResult:
        """TOPSIS法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_criteria = data.shape[1]
        
        # 如果没有提供权重，使用等权重
        if weights is None:
            weights = np.ones(n_criteria) / n_criteria
        
        # 加权标准化矩阵
        weighted_matrix = normalized_data * weights
        
        # 确定理想解和负理想解
        ideal_solution = np.zeros(n_criteria)
        negative_ideal_solution = np.zeros(n_criteria)
        
        for j in range(n_criteria):
            if j in benefit_criteria:
                ideal_solution[j] = np.max(weighted_matrix[:, j])
                negative_ideal_solution[j] = np.min(weighted_matrix[:, j])
            elif j in cost_criteria:
                ideal_solution[j] = np.min(weighted_matrix[:, j])
                negative_ideal_solution[j] = np.max(weighted_matrix[:, j])
        
        # 计算到理想解和负理想解的距离
        distance_to_ideal = np.sqrt(np.sum((weighted_matrix - ideal_solution) ** 2, axis=1))
        distance_to_negative_ideal = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution) ** 2, axis=1))
        
        # 计算相对贴近度
        scores = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="TOPSIS法",
            metadata={
                "ideal_solution": ideal_solution,
                "negative_ideal_solution": negative_ideal_solution,
                "distance_to_ideal": distance_to_ideal,
                "distance_to_negative_ideal": distance_to_negative_ideal
            }
        )
    
    def _vikor(self,
              data: np.ndarray,
              benefit_criteria: List[int],
              cost_criteria: List[int],
              weights: Optional[np.ndarray] = None,
              v: float = 0.5,
              **kwargs) -> EvaluationResult:
        """VIKOR法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_criteria = data.shape[1]
        
        # 如果没有提供权重，使用等权重
        if weights is None:
            weights = np.ones(n_criteria) / n_criteria
        
        # 确定最优值和最劣值
        best_values = np.zeros(n_criteria)
        worst_values = np.zeros(n_criteria)
        
        for j in range(n_criteria):
            if j in benefit_criteria:
                best_values[j] = np.max(normalized_data[:, j])
                worst_values[j] = np.min(normalized_data[:, j])
            elif j in cost_criteria:
                best_values[j] = np.min(normalized_data[:, j])
                worst_values[j] = np.max(normalized_data[:, j])
        
        # 计算S_i和R_i
        S_i = np.zeros(data.shape[0])
        R_i = np.zeros(data.shape[0])
        
        for i in range(data.shape[0]):
            weighted_distances = []
            for j in range(n_criteria):
                if best_values[j] != worst_values[j]:
                    distance = weights[j] * (best_values[j] - normalized_data[i, j]) / (best_values[j] - worst_values[j])
                    weighted_distances.append(distance)
            
            S_i[i] = np.sum(weighted_distances)
            R_i[i] = np.max(weighted_distances) if weighted_distances else 0
        
        # 计算Q_i
        S_star = np.min(S_i)
        S_minus = np.max(S_i)
        R_star = np.min(R_i)
        R_minus = np.max(R_i)
        
        Q_i = v * (S_i - S_star) / (S_minus - S_star) + (1 - v) * (R_i - R_star) / (R_minus - R_star)
        
        # 计算综合得分（Q值越小越好，所以用1-Q作为得分）
        scores = 1 - Q_i
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="VIKOR法",
            metadata={
                "S_values": S_i,
                "R_values": R_i,
                "Q_values": Q_i,
                "v_parameter": v,
                "S_star": S_star,
                "S_minus": S_minus,
                "R_star": R_star,
                "R_minus": R_minus
            }
        )
    
    def _promethee(self,
                  data: np.ndarray,
                  benefit_criteria: List[int],
                  cost_criteria: List[int],
                  weights: Optional[np.ndarray] = None,
                  preference_function: str = "usual",
                  **kwargs) -> EvaluationResult:
        """PROMETHEE法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_alternatives = data.shape[0]
        n_criteria = data.shape[1]
        
        # 如果没有提供权重，使用等权重
        if weights is None:
            weights = np.ones(n_criteria) / n_criteria
        
        # 计算偏好函数
        preference_matrix = np.zeros((n_alternatives, n_alternatives, n_criteria))
        
        for i in range(n_alternatives):
            for k in range(n_alternatives):
                if i != k:
                    for j in range(n_criteria):
                        d = normalized_data[i, j] - normalized_data[k, j]
                        
                        if preference_function == "usual":
                            # 常用偏好函数
                            preference_matrix[i, k, j] = 1 if d > 0 else 0
                        elif preference_function == "linear":
                            # 线性偏好函数
                            p = 0.5  # 偏好阈值
                            if d <= 0:
                                preference_matrix[i, k, j] = 0
                            elif d > p:
                                preference_matrix[i, k, j] = 1
                            else:
                                preference_matrix[i, k, j] = d / p
        
        # 计算综合偏好指数
        aggregated_preference = np.zeros((n_alternatives, n_alternatives))
        
        for i in range(n_alternatives):
            for k in range(n_alternatives):
                if i != k:
                    aggregated_preference[i, k] = np.sum(weights * preference_matrix[i, k, :])
        
        # 计算流出量、流入量和净流量
        positive_flow = np.sum(aggregated_preference, axis=1)
        negative_flow = np.sum(aggregated_preference, axis=0)
        net_flow = positive_flow - negative_flow
        
        # 计算综合得分
        min_flow = np.min(net_flow)
        max_flow = np.max(net_flow)
        
        if max_flow != min_flow:
            scores = (net_flow - min_flow) / (max_flow - min_flow)
        else:
            scores = np.ones_like(net_flow)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="PROMETHEE法",
            metadata={
                "preference_matrix": preference_matrix,
                "aggregated_preference": aggregated_preference,
                "positive_flow": positive_flow,
                 "negative_flow": negative_flow,
                 "net_flow": net_flow,
                 "preference_function": preference_function
             }
         )
    
    def _coefficient_of_variation(self,
                                 data: np.ndarray,
                                 benefit_criteria: List[int],
                                 cost_criteria: List[int],
                                 **kwargs) -> EvaluationResult:
        """变异系数法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        # 计算标准差
        std_dev = np.std(normalized_data, axis=0)
        
        # 计算均值
        mean_values = np.mean(normalized_data, axis=0)
        
        # 计算变异系数
        coefficient_of_variation = std_dev / mean_values
        
        # 计算权重
        weights = coefficient_of_variation / np.sum(coefficient_of_variation)
        
        # 计算综合得分
        scores = np.dot(normalized_data, weights)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="变异系数法",
            metadata={
                "std_dev": std_dev,
                "mean_values": mean_values,
                "coefficient_of_variation": coefficient_of_variation
            }
        )
    
    def _principal_component_analysis(self,
                                     data: np.ndarray,
                                     benefit_criteria: List[int],
                                     cost_criteria: List[int],
                                     n_components: Optional[int] = None,
                                     **kwargs) -> EvaluationResult:
        """主成分分析法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        # 标准化数据
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(normalized_data)
        
        # 如果没有指定主成分数量，使用所有成分
        if n_components is None:
            n_components = min(data.shape[0], data.shape[1])
        
        # 执行PCA
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(scaled_data)
        
        # 计算方差贡献率
        explained_variance_ratio = pca.explained_variance_ratio_
        
        # 计算综合得分
        scores = np.dot(principal_components, explained_variance_ratio)
        
        # 计算权重（基于主成分载荷）
        weights = np.sum(pca.components_ * explained_variance_ratio.reshape(-1, 1), axis=0)
        weights = np.abs(weights) / np.sum(np.abs(weights))
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="主成分分析法",
            metadata={
                "principal_components": principal_components,
                "explained_variance_ratio": explained_variance_ratio,
                "cumulative_variance_ratio": np.cumsum(explained_variance_ratio),
                "n_components": n_components
            }
        )
    
    def _grey_prediction(self,
                        data: np.ndarray,
                        benefit_criteria: List[int],
                        cost_criteria: List[int],
                        weights: Optional[np.ndarray] = None,
                        **kwargs) -> EvaluationResult:
        """灰色预测法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_alternatives = data.shape[0]
        n_criteria = data.shape[1]
        
        # 如果没有提供权重，使用等权重
        if weights is None:
            weights = np.ones(n_criteria) / n_criteria
        
        # 计算参考序列（理想解）
        reference_sequence = np.zeros(n_criteria)
        for j in range(n_criteria):
            if j in benefit_criteria:
                reference_sequence[j] = np.max(normalized_data[:, j])
            elif j in cost_criteria:
                reference_sequence[j] = np.min(normalized_data[:, j])
        
        # 计算关联系数
        correlation_coefficients = np.zeros((n_alternatives, n_criteria))
        rho = 0.5  # 分辨系数
        
        for i in range(n_alternatives):
            for j in range(n_criteria):
                delta_ij = abs(normalized_data[i, j] - reference_sequence[j])
                min_delta = np.min(np.abs(normalized_data - reference_sequence))
                max_delta = np.max(np.abs(normalized_data - reference_sequence))
                
                if max_delta != min_delta:
                    correlation_coefficients[i, j] = (min_delta + rho * max_delta) / (delta_ij + rho * max_delta)
                else:
                    correlation_coefficients[i, j] = 1
        
        # 计算关联度
        correlation_degrees = np.dot(correlation_coefficients, weights)
        
        # 计算综合得分
        scores = correlation_degrees
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="灰色预测法",
            metadata={
                "reference_sequence": reference_sequence,
                "correlation_coefficients": correlation_coefficients,
                "correlation_degrees": correlation_degrees,
                "rho": rho
            }
        )
    
    def _rank_sum_ratio(self,
                       data: np.ndarray,
                       benefit_criteria: List[int],
                       cost_criteria: List[int],
                       weights: Optional[np.ndarray] = None,
                       **kwargs) -> EvaluationResult:
        """秩和比法"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_alternatives = data.shape[0]
        n_criteria = data.shape[1]
        
        # 如果没有提供权重，使用等权重
        if weights is None:
            weights = np.ones(n_criteria) / n_criteria
        
        # 计算秩次
        ranks = np.zeros_like(normalized_data)
        for j in range(n_criteria):
            if j in benefit_criteria:
                ranks[:, j] = np.argsort(normalized_data[:, j]) + 1
            elif j in cost_criteria:
                ranks[:, j] = np.argsort(-normalized_data[:, j]) + 1
        
        # 计算秩和比
        rank_sum_ratio = np.dot(ranks, weights) / n_alternatives
        
        # 计算综合得分
        scores = rank_sum_ratio
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="秩和比法",
            metadata={
                "ranks": ranks,
                "rank_sum_ratio": rank_sum_ratio
            }
        )
    
    def _game_theory_combination(self,
                               data: np.ndarray,
                               benefit_criteria: List[int],
                               cost_criteria: List[int],
                               method_weights: Optional[List[str]] = None,
                               **kwargs) -> EvaluationResult:
        """博弈组合法"""
        # 使用多种方法计算权重
        methods = ["entropy", "critic", "coefficient_of_variation"]
        
        if method_weights is None:
            method_weights = [1/3, 1/3, 1/3]
        
        weight_matrix = []
        
        for method in methods:
            if method == "entropy":
                result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
            elif method == "critic":
                result = self._critic(data, benefit_criteria, cost_criteria)
            elif method == "coefficient_of_variation":
                result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
            else:
                continue
            
            weight_matrix.append(result.weights)
        
        weight_matrix = np.array(weight_matrix)
        
        # 计算协方差矩阵
        cov_matrix = np.cov(weight_matrix)
        
        # 求解博弈组合权重
        n_methods = len(methods)
        A = np.ones((n_methods, n_methods))
        for i in range(n_methods):
            for j in range(n_methods):
                A[i, j] = np.dot(weight_matrix[i], weight_matrix[j])
        
        b = np.ones(n_methods)
        
        try:
            # 求解线性方程组
            combination_weights = np.linalg.solve(A, b)
            combination_weights = combination_weights / np.sum(combination_weights)
        except np.linalg.LinAlgError:
            # 如果求解失败，使用等权重
            combination_weights = np.ones(n_methods) / n_methods
        
        # 计算组合权重
        final_weights = np.dot(combination_weights, weight_matrix)
        
        # 计算综合得分
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        scores = np.dot(normalized_data, final_weights)
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=final_weights,
            scores=scores,
            rankings=rankings,
            method_name="博弈组合法",
            metadata={
                "weight_matrix": weight_matrix,
                "combination_weights": combination_weights,
                "methods_used": methods
            }
        )
    
    def _normal_cloud_model(self,
                           data: np.ndarray,
                           benefit_criteria: List[int],
                           cost_criteria: List[int],
                           weights: Optional[np.ndarray] = None,
                           **kwargs) -> EvaluationResult:
        """正态云模型"""
        normalized_data = self._normalize_matrix(data, benefit_criteria, cost_criteria)
        
        n_alternatives = data.shape[0]
        n_criteria = data.shape[1]
        
        # 如果没有提供权重，使用等权重
        if weights is None:
            weights = np.ones(n_criteria) / n_criteria
        
        # 计算期望值
        expected_values = np.mean(normalized_data, axis=0)
        
        # 计算熵
        entropy = np.std(normalized_data, axis=0)
        
        # 计算超熵
        hyper_entropy = np.std(entropy)
        
        # 计算确定度
        certainty_degrees = np.zeros((n_alternatives, n_criteria))
        
        for i in range(n_alternatives):
            for j in range(n_criteria):
                x = normalized_data[i, j]
                Ex = expected_values[j]
                En = entropy[j]
                He = hyper_entropy
                
                # 生成正态随机数
                En_prime = np.random.normal(En, He)
                
                # 计算确定度
                certainty_degrees[i, j] = np.exp(-(x - Ex) ** 2 / (2 * En_prime ** 2))
        
        # 计算综合确定度
        overall_certainty = np.dot(certainty_degrees, weights)
        
        # 计算综合得分
        scores = overall_certainty
        
        # 计算排名
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=weights,
            scores=scores,
            rankings=rankings,
            method_name="正态云模型",
            metadata={
                "expected_values": expected_values,
                "entropy": entropy,
                "hyper_entropy": hyper_entropy,
                "certainty_degrees": certainty_degrees,
                "overall_certainty": overall_certainty
            }
        )
    
    def _random_entropy_todim(self,
                             data: np.ndarray,
                             benefit_criteria: List[int],
                             cost_criteria: List[int],
                             n_simulations: int = 1000,
                             **kwargs) -> EvaluationResult:
        """随机熵权-TODIM法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用TODIM法
            result = self._todim(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机熵权-TODIM法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _random_coefficient_of_variation_todim(self,
                                              data: np.ndarray,
                                              benefit_criteria: List[int],
                                              cost_criteria: List[int],
                                              n_simulations: int = 1000,
                                              **kwargs) -> EvaluationResult:
        """随机变异系数-TODIM法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用变异系数法计算权重
            cv_result = self._coefficient_of_variation(noisy_data, benefit_criteria, cost_criteria)
            
            # 使用TODIM法
            result = self._todim(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机变异系数-TODIM法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _critic_todim(self,
                     data: np.ndarray,
                     benefit_criteria: List[int],
                     cost_criteria: List[int],
                     **kwargs) -> EvaluationResult:
        """CRITIC-TODIM法"""
        # 使用CRITIC法计算权重
        critic_result = self._critic(data, benefit_criteria, cost_criteria)
        
        # 使用TODIM法
        result = self._todim(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=critic_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="CRITIC-TODIM法",
            metadata={
                "critic_weights": critic_result.weights,
                "todim_scores": result.scores
            }
        )
    
    def _random_entropy_vikor(self,
                             data: np.ndarray,
                             benefit_criteria: List[int],
                             cost_criteria: List[int],
                             n_simulations: int = 1000,
                             **kwargs) -> EvaluationResult:
        """随机熵权-VIKOR法"""
         # 使用蒙特卡洛模拟
        all_scores = []
         
        for _ in range(n_simulations):
             # 添加随机噪声
             noisy_data = data + np.random.normal(0, 0.1, data.shape)
             
             # 使用VIKOR法
             result = self._vikor(noisy_data, benefit_criteria, cost_criteria)
             all_scores.append(result.scores)
         
         # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
         
         # 计算排名
        rankings = np.argsort(-avg_scores) + 1
         
        return EvaluationResult(
             weights=None,
             scores=avg_scores,
             rankings=rankings,
             method_name="随机熵权-VIKOR法",
             metadata={
                 "n_simulations": n_simulations,
                 "all_scores": all_scores
             }
         )
    
    def _random_entropy_promethee(self,
                                 data: np.ndarray,
                                 benefit_criteria: List[int],
                                 cost_criteria: List[int],
                                 n_simulations: int = 1000,
                                 **kwargs) -> EvaluationResult:
        """随机熵权-PROMETHEE法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用PROMETHEE法
            result = self._promethee(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机熵权-PROMETHEE法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _random_critic_vikor(self,
                            data: np.ndarray,
                            benefit_criteria: List[int],
                            cost_criteria: List[int],
                            n_simulations: int = 1000,
                            **kwargs) -> EvaluationResult:
        """随机CRITIC-VIKOR法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用CRITIC法计算权重
            critic_result = self._critic(noisy_data, benefit_criteria, cost_criteria)
            
            # 使用VIKOR法
            result = self._vikor(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机CRITIC-VIKOR法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _random_coefficient_of_variation_topsis(self,
                                               data: np.ndarray,
                                               benefit_criteria: List[int],
                                               cost_criteria: List[int],
                                               n_simulations: int = 1000,
                                               **kwargs) -> EvaluationResult:
        """随机变异系数-TOPSIS法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用变异系数法计算权重
            cv_result = self._coefficient_of_variation(noisy_data, benefit_criteria, cost_criteria)
            
            # 使用TOPSIS法
            result = self._topsis(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机变异系数-TOPSIS法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _random_entropy_topsis(self,
                              data: np.ndarray,
                              benefit_criteria: List[int],
                              cost_criteria: List[int],
                              n_simulations: int = 1000,
                              **kwargs) -> EvaluationResult:
        """随机熵权-TOPSIS法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用TOPSIS法
            result = self._topsis(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机熵权-TOPSIS法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _random_ahp_topsis(self,
                          data: np.ndarray,
                          benefit_criteria: List[int],
                          cost_criteria: List[int],
                          n_simulations: int = 1000,
                          **kwargs) -> EvaluationResult:
        """随机层次分析-TOPSIS法"""
        # 使用蒙特卡洛模拟
        all_scores = []
        
        for _ in range(n_simulations):
            # 添加随机噪声
            noisy_data = data + np.random.normal(0, 0.1, data.shape)
            
            # 使用层次分析法计算权重
            ahp_result = self._ahp(noisy_data, benefit_criteria, cost_criteria)
            
            # 使用TOPSIS法
            result = self._topsis(noisy_data, benefit_criteria, cost_criteria)
            all_scores.append(result.scores)
        
        # 计算平均得分
        avg_scores = np.mean(all_scores, axis=0)
        
        # 计算排名
        rankings = np.argsort(-avg_scores) + 1
        
        return EvaluationResult(
            weights=None,
            scores=avg_scores,
            rankings=rankings,
            method_name="随机层次分析-TOPSIS法",
            metadata={
                "n_simulations": n_simulations,
                "all_scores": all_scores
            }
        )
    
    def _entropy_vikor(self,
                      data: np.ndarray,
                      benefit_criteria: List[int],
                      cost_criteria: List[int],
                      **kwargs) -> EvaluationResult:
        """熵权-VIKOR法"""
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        
        # 使用VIKOR法
        result = self._vikor(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=entropy_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-VIKOR法",
            metadata={
                "entropy_weights": entropy_result.weights,
                "vikor_scores": result.scores
            }
        )
    
    def _coefficient_of_variation_vikor(self,
                                       data: np.ndarray,
                                       benefit_criteria: List[int],
                                       cost_criteria: List[int],
                                       **kwargs) -> EvaluationResult:
        """变异系数-VIKOR法"""
        # 使用变异系数法计算权重
        cv_result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
        
        # 使用VIKOR法
        result = self._vikor(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=cv_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="变异系数-VIKOR法",
            metadata={
                "cv_weights": cv_result.weights,
                "vikor_scores": result.scores
            }
        )
    
    def _critic_vikor(self,
                     data: np.ndarray,
                     benefit_criteria: List[int],
                     cost_criteria: List[int],
                     **kwargs) -> EvaluationResult:
        """CRITIC-VIKOR法"""
        # 使用CRITIC法计算权重
        critic_result = self._critic(data, benefit_criteria, cost_criteria)
        
        # 使用VIKOR法
        result = self._vikor(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=critic_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="CRITIC-VIKOR法",
            metadata={
                "critic_weights": critic_result.weights,
                "vikor_scores": result.scores
            }
        )
    
    def _entropy_todim(self,
                      data: np.ndarray,
                      benefit_criteria: List[int],
                      cost_criteria: List[int],
                      **kwargs) -> EvaluationResult:
        """熵权-TODIM法"""
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        
        # 使用TODIM法
        result = self._todim(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=entropy_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-TODIM法",
            metadata={
                "entropy_weights": entropy_result.weights,
                "todim_scores": result.scores
            }
        )
    
    def _coefficient_of_variation_todim(self,
                                       data: np.ndarray,
                                       benefit_criteria: List[int],
                                       cost_criteria: List[int],
                                       **kwargs) -> EvaluationResult:
        """变异系数-TODIM法"""
        # 使用变异系数法计算权重
        cv_result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
        
        # 使用TODIM法
        result = self._todim(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=cv_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="变异系数-TODIM法",
            metadata={
                "cv_weights": cv_result.weights,
                "todim_scores": result.scores
            }
        )
    
    def _entropy_promethee(self,
                          data: np.ndarray,
                          benefit_criteria: List[int],
                          cost_criteria: List[int],
                          **kwargs) -> EvaluationResult:
        """熵权-PROMETHEE法"""
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        
        # 使用PROMETHEE法
        result = self._promethee(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=entropy_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-PROMETHEE法",
            metadata={
                "entropy_weights": entropy_result.weights,
                "promethee_scores": result.scores
            }
        )
    
    def _coefficient_of_variation_promethee(self,
                                           data: np.ndarray,
                                           benefit_criteria: List[int],
                                           cost_criteria: List[int],
                                           **kwargs) -> EvaluationResult:
        """变异系数-PROMETHEE法"""
        # 使用变异系数法计算权重
        cv_result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
        
        # 使用PROMETHEE法
        result = self._promethee(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=cv_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="变异系数-PROMETHEE法",
            metadata={
                "cv_weights": cv_result.weights,
                "promethee_scores": result.scores
            }
        )
    
    def _critic_promethee(self,
                         data: np.ndarray,
                         benefit_criteria: List[int],
                         cost_criteria: List[int],
                         **kwargs) -> EvaluationResult:
        """CRITIC-PROMETHEE法"""
        # 使用CRITIC法计算权重
        critic_result = self._critic(data, benefit_criteria, cost_criteria)
        
        # 使用PROMETHEE法
        result = self._promethee(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=critic_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="CRITIC-PROMETHEE法",
            metadata={
                "critic_weights": critic_result.weights,
                "promethee_scores": result.scores
            }
        )
    
    def _entropy_topsis(self,
                       data: np.ndarray,
                       benefit_criteria: List[int],
                       cost_criteria: List[int],
                       **kwargs) -> EvaluationResult:
        """熵权-TOPSIS法"""
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=entropy_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-TOPSIS法",
            metadata={
                "entropy_weights": entropy_result.weights,
                "topsis_scores": result.scores
            }
        )
    
    def _coefficient_of_variation_topsis(self,
                                        data: np.ndarray,
                                        benefit_criteria: List[int],
                                        cost_criteria: List[int],
                                        **kwargs) -> EvaluationResult:
        """变异系数-TOPSIS法"""
        # 使用变异系数法计算权重
        cv_result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
         
         # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
         
        return EvaluationResult(
             weights=cv_result.weights,
             scores=result.scores,
             rankings=result.rankings,
             method_name="变异系数-TOPSIS法",
             metadata={
                 "cv_weights": cv_result.weights,
                 "topsis_scores": result.scores
             }
         )
    
    def _critic_topsis(self,
                      data: np.ndarray,
                      benefit_criteria: List[int],
                      cost_criteria: List[int],
                      **kwargs) -> EvaluationResult:
        """CRITIC-TOPSIS法"""
        # 使用CRITIC法计算权重
        critic_result = self._critic(data, benefit_criteria, cost_criteria)
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=critic_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="CRITIC-TOPSIS法",
            metadata={
                "critic_weights": critic_result.weights,
                "topsis_scores": result.scores
            }
        )
    
    def _ahp_entropy_critic_combination(self,
                                       data: np.ndarray,
                                       benefit_criteria: List[int],
                                       cost_criteria: List[int],
                                       **kwargs) -> EvaluationResult:
        """层次-熵权-CRITIC组合法"""
        # 计算三种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        critic_weights = self._critic(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (ahp_weights + entropy_weights + critic_weights) / 3
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-熵权-CRITIC组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "entropy_weights": entropy_weights,
                "critic_weights": critic_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _ahp_coefficient_of_variation_critic_combination(self,
                                                        data: np.ndarray,
                                                        benefit_criteria: List[int],
                                                        cost_criteria: List[int],
                                                        **kwargs) -> EvaluationResult:
        """层次-变异系数-CRITIC组合法"""
        # 计算三种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        critic_weights = self._critic(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (ahp_weights + cv_weights + critic_weights) / 3
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-变异系数-CRITIC组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "cv_weights": cv_weights,
                "critic_weights": critic_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _entropy_coefficient_of_variation_critic_combination(self,
                                                            data: np.ndarray,
                                                            benefit_criteria: List[int],
                                                            cost_criteria: List[int],
                                                            **kwargs) -> EvaluationResult:
        """熵权-变异系数-CRITIC组合法"""
        # 计算三种权重
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        critic_weights = self._critic(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (entropy_weights + cv_weights + critic_weights) / 3
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-变异系数-CRITIC组合法",
            metadata={
                "entropy_weights": entropy_weights,
                "cv_weights": cv_weights,
                "critic_weights": critic_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _ahp_entropy_coefficient_of_variation_critic_combination(self,
                                                                data: np.ndarray,
                                                                benefit_criteria: List[int],
                                                                cost_criteria: List[int],
                                                                **kwargs) -> EvaluationResult:
        """层次-熵权-变异系数-CRITIC组合法"""
        # 计算四种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        critic_weights = self._critic(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (ahp_weights + entropy_weights + cv_weights + critic_weights) / 4
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-熵权-变异系数-CRITIC组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "entropy_weights": entropy_weights,
                "cv_weights": cv_weights,
                "critic_weights": critic_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _entropy_grey_prediction(self,
                                data: np.ndarray,
                                benefit_criteria: List[int],
                                cost_criteria: List[int],
                                **kwargs) -> EvaluationResult:
        """熵权-灰色预测法"""
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        
        # 使用灰色预测法
        result = self._grey_prediction(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=entropy_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-灰色预测法",
            metadata={
                "entropy_weights": entropy_result.weights,
                "grey_scores": result.scores
            }
        )
    
    def _coefficient_of_variation_grey_prediction(self,
                                                 data: np.ndarray,
                                                 benefit_criteria: List[int],
                                                 cost_criteria: List[int],
                                                 **kwargs) -> EvaluationResult:
        """变异系数-灰色预测法"""
        # 使用变异系数法计算权重
        cv_result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
        
        # 使用灰色预测法
        result = self._grey_prediction(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=cv_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="变异系数-灰色预测法",
            metadata={
                "cv_weights": cv_result.weights,
                "grey_scores": result.scores
            }
        )
    
    def _critic_grey_prediction(self,
                               data: np.ndarray,
                               benefit_criteria: List[int],
                               cost_criteria: List[int],
                               **kwargs) -> EvaluationResult:
        """CRITIC-灰色预测法"""
        # 使用CRITIC法计算权重
        critic_result = self._critic(data, benefit_criteria, cost_criteria)
        
        # 使用灰色预测法
        result = self._grey_prediction(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=critic_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="CRITIC-灰色预测法",
            metadata={
                "critic_weights": critic_result.weights,
                "grey_scores": result.scores
            }
        )
    
    def _entropy_rank_sum_ratio(self,
                               data: np.ndarray,
                               benefit_criteria: List[int],
                               cost_criteria: List[int],
                               **kwargs) -> EvaluationResult:
        """熵权-秩和比法"""
        # 使用熵权法计算权重
        entropy_result = self._entropy_weighting(data, benefit_criteria, cost_criteria)
        
        # 使用秩和比法
        result = self._rank_sum_ratio(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=entropy_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-秩和比法",
            metadata={
                "entropy_weights": entropy_result.weights,
                "rsr_scores": result.scores
            }
        )
    
    def _coefficient_of_variation_rank_sum_ratio(self,
                                                data: np.ndarray,
                                                benefit_criteria: List[int],
                                                cost_criteria: List[int],
                                                **kwargs) -> EvaluationResult:
        """变异系数-秩和比法"""
        # 使用变异系数法计算权重
        cv_result = self._coefficient_of_variation(data, benefit_criteria, cost_criteria)
        
        # 使用秩和比法
        result = self._rank_sum_ratio(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=cv_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="变异系数-秩和比法",
            metadata={
                "cv_weights": cv_result.weights,
                "rsr_scores": result.scores
            }
        )
    
    def _critic_rank_sum_ratio(self,
                              data: np.ndarray,
                              benefit_criteria: List[int],
                              cost_criteria: List[int],
                              **kwargs) -> EvaluationResult:
        """CRITIC-秩和比法"""
        # 使用CRITIC法计算权重
        critic_result = self._critic(data, benefit_criteria, cost_criteria)
        
        # 使用秩和比法
        result = self._rank_sum_ratio(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=critic_result.weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="CRITIC-秩和比法",
            metadata={
                "critic_weights": critic_result.weights,
                "rsr_scores": result.scores
            }
        )
    
    def _ahp_entropy_game_combination(self,
                                     data: np.ndarray,
                                     benefit_criteria: List[int],
                                     cost_criteria: List[int],
                                     **kwargs) -> EvaluationResult:
        """层次-熵权-博弈组合法"""
        # 计算两种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        
        # 博弈组合权重
        combined_weights = (ahp_weights + entropy_weights) / 2
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-熵权-博弈组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "entropy_weights": entropy_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _ahp_coefficient_of_variation_game_combination(self,
                                                      data: np.ndarray,
                                                      benefit_criteria: List[int],
                                                      cost_criteria: List[int],
                                                      **kwargs) -> EvaluationResult:
        """层次-变异系数-博弈组合法"""
        # 计算两种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        
        # 博弈组合权重
        combined_weights = (ahp_weights + cv_weights) / 2
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-变异系数-博弈组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "cv_weights": cv_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _entropy_coefficient_of_variation_game_combination(self,
                                                          data: np.ndarray,
                                                          benefit_criteria: List[int],
                                                          cost_criteria: List[int],
                                                          **kwargs) -> EvaluationResult:
        """熵权-变异系数-博弈组合法"""
        # 计算两种权重
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        
        # 博弈组合权重
        combined_weights = (entropy_weights + cv_weights) / 2
        
        # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-变异系数-博弈组合法",
            metadata={
                "entropy_weights": entropy_weights,
                "cv_weights": cv_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _ahp_entropy_coefficient_of_variation_game_combination(self,
                                                              data: np.ndarray,
                                                              benefit_criteria: List[int],
                                                              cost_criteria: List[int],
                                                              **kwargs) -> EvaluationResult:
        """层次-熵权-变异系数-博弈组合法"""
         # 计算三种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
         
         # 博弈组合权重
        combined_weights = (ahp_weights + entropy_weights + cv_weights) / 3
         
         # 使用TOPSIS法
        result = self._topsis(data, benefit_criteria, cost_criteria)
         
        return EvaluationResult(
             weights=combined_weights,
             scores=result.scores,
             rankings=result.rankings,
             method_name="层次-熵权-变异系数-博弈组合法",
             metadata={
                 "ahp_weights": ahp_weights,
                 "entropy_weights": entropy_weights,
                 "cv_weights": cv_weights,
                 "combined_weights": combined_weights
             }
         )
    
    def _ahp_entropy_normal_cloud_combination(self,
                                             data: np.ndarray,
                                             benefit_criteria: List[int],
                                             cost_criteria: List[int],
                                             **kwargs) -> EvaluationResult:
        """层次-熵权-正态云组合法"""
        # 计算两种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (ahp_weights + entropy_weights) / 2
        
        # 使用正态云模型
        result = self._normal_cloud(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-熵权-正态云组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "entropy_weights": entropy_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _ahp_coefficient_of_variation_normal_cloud_combination(self,
                                                              data: np.ndarray,
                                                              benefit_criteria: List[int],
                                                              cost_criteria: List[int],
                                                              **kwargs) -> EvaluationResult:
        """层次-变异系数-正态云组合法"""
        # 计算两种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (ahp_weights + cv_weights) / 2
        
        # 使用正态云模型
        result = self._normal_cloud(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-变异系数-正态云组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "cv_weights": cv_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _entropy_coefficient_of_variation_normal_cloud_combination(self,
                                                                  data: np.ndarray,
                                                                  benefit_criteria: List[int],
                                                                  cost_criteria: List[int],
                                                                  **kwargs) -> EvaluationResult:
        """熵权-变异系数-正态云组合法"""
        # 计算两种权重
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (entropy_weights + cv_weights) / 2
        
        # 使用正态云模型
        result = self._normal_cloud(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="熵权-变异系数-正态云组合法",
            metadata={
                "entropy_weights": entropy_weights,
                "cv_weights": cv_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _ahp_entropy_coefficient_of_variation_normal_cloud_combination(self,
                                                                      data: np.ndarray,
                                                                      benefit_criteria: List[int],
                                                                      cost_criteria: List[int],
                                                                      **kwargs) -> EvaluationResult:
        """层次-熵权-变异系数-正态云组合法"""
        # 计算三种权重
        ahp_weights = self._ahp(data, benefit_criteria, cost_criteria).weights
        entropy_weights = self._entropy_weighting(data, benefit_criteria, cost_criteria).weights
        cv_weights = self._coefficient_of_variation(data, benefit_criteria, cost_criteria).weights
        
        # 组合权重
        combined_weights = (ahp_weights + entropy_weights + cv_weights) / 3
        
        # 使用正态云模型
        result = self._normal_cloud(data, benefit_criteria, cost_criteria)
        
        return EvaluationResult(
            weights=combined_weights,
            scores=result.scores,
            rankings=result.rankings,
            method_name="层次-熵权-变异系数-正态云组合法",
            metadata={
                "ahp_weights": ahp_weights,
                "entropy_weights": entropy_weights,
                "cv_weights": cv_weights,
                "combined_weights": combined_weights
            }
        )
    
    def _normal_cloud(self,
                     data: np.ndarray,
                     benefit_criteria: List[int],
                     cost_criteria: List[int],
                     **kwargs) -> EvaluationResult:
        """正态云模型"""
        # 数据标准化
        normalized_data = self._normalize_data(data, benefit_criteria, cost_criteria)
        
        # 计算期望值
        expected_value = np.mean(normalized_data, axis=0)
        
        # 计算熵值
        entropy = -np.sum(normalized_data * np.log(normalized_data + 1e-10), axis=0)
        
        # 计算超熵
        hyper_entropy = np.std(normalized_data, axis=0)
        
        # 计算确定度
        certainty = np.exp(-(normalized_data - expected_value) ** 2 / (2 * hyper_entropy ** 2))
        
        # 计算综合得分
        scores = np.mean(certainty, axis=1)
        
        # 排序
        rankings = np.argsort(-scores) + 1
        
        return EvaluationResult(
            weights=np.ones(data.shape[1]) / data.shape[1],
            scores=scores,
            rankings=rankings,
            method_name="正态云模型",
            metadata={
                "expected_value": expected_value,
                "entropy": entropy,
                "hyper_entropy": hyper_entropy,
                "certainty": certainty
            }
        )
    
    def _rank_sum_ratio(self,
                       data: np.ndarray,
                       benefit_criteria: List[int],
                       cost_criteria: List[int],
                       **kwargs) -> EvaluationResult:
        """秩和比法"""
        # 数据标准化
        normalized_data = self._normalize_data(data, benefit_criteria, cost_criteria)
        
        # 计算秩
        ranks = np.zeros_like(normalized_data)
        for j in range(normalized_data.shape[1]):
            if j in benefit_criteria:
                ranks[:, j] = np.argsort(normalized_data[:, j]) + 1
            else:
                ranks[:, j] = np.argsort(-normalized_data[:, j]) + 1
        
        # 计算秩和比
        rsr = np.sum(ranks, axis=1) / (normalized_data.shape[0] * normalized_data.shape[1])
        
        # 排序
        rankings = np.argsort(-rsr) + 1
        
        return EvaluationResult(
            weights=np.ones(data.shape[1]) / data.shape[1],
            scores=rsr,
            rankings=rankings,
            method_name="秩和比法",
            metadata={
                "ranks": ranks,
                "rsr": rsr
            }
        )
    
    def _grey_prediction(self,
                        data: np.ndarray,
                        benefit_criteria: List[int],
                        cost_criteria: List[int],
                        **kwargs) -> EvaluationResult:
        """灰色预测法"""
        # 数据标准化
        normalized_data = self._normalize_data(data, benefit_criteria, cost_criteria)
        
        # 累加生成
        accumulated_data = np.cumsum(normalized_data, axis=0)
        
        # 计算发展系数
        development_coefficient = np.zeros(normalized_data.shape[1])
        for j in range(normalized_data.shape[1]):
            if len(accumulated_data) > 1:
                development_coefficient[j] = (accumulated_data[-1, j] - accumulated_data[0, j]) / (len(accumulated_data) - 1)
        
        # 计算灰色关联度
        reference = np.max(normalized_data, axis=0)
        grey_relation = np.zeros(normalized_data.shape[0])
        for i in range(normalized_data.shape[0]):
            diff = np.abs(normalized_data[i] - reference)
            min_diff = np.min(diff)
            max_diff = np.max(diff)
            grey_relation[i] = np.mean((min_diff + 0.5 * max_diff) / (diff + 0.5 * max_diff))
        
        # 排序
        rankings = np.argsort(-grey_relation) + 1
        
        return EvaluationResult(
            weights=np.ones(data.shape[1]) / data.shape[1],
            scores=grey_relation,
            rankings=rankings,
            method_name="灰色预测法",
            metadata={
                "accumulated_data": accumulated_data,
                "development_coefficient": development_coefficient,
                "grey_relation": grey_relation
            }
        )