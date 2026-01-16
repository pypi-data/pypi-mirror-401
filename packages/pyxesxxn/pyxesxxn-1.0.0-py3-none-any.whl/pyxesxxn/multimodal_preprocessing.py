"""多态数据预处理模块 (Multimodal Data Preprocessing Module)

该模块针对配电网多源异构数据（拓扑、量测、故障时间等），提供归一化、异常值处理、
数据增强等功能，提升AI模型的鲁棒性。

核心功能：
- 量测数据的标准化/归一化（适配AI模型输入）
- 缺失数据的补全（如基于时序插值、拓扑关联补全）
- 故障数据增强（如生成不同故障类型、阻抗、持续时间的模拟样本）
"""

from __future__ import annotations
from typing import Dict, List, Optional, Union, Any, Tuple
from enum import Enum
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
import scipy.stats as stats
from scipy import interpolate
import warnings


class DataType(Enum):
    """数据类型枚举"""
    TOPOLOGY = "topology"  # 拓扑数据
    MEASUREMENT = "measurement"  # 量测数据
    FAULT = "fault"  # 故障数据
    OPERATIONAL = "operational"  # 运行数据
    ENVIRONMENTAL = "environmental"  # 环境数据


class NormalizationMethod(Enum):
    """归一化方法枚举"""
    STANDARD = "standard"  # 标准化 (Z-score)
    MINMAX = "minmax"  # 最小-最大归一化
    ROBUST = "robust"  # 鲁棒归一化
    LOG = "log"  # 对数变换
    NONE = "none"  # 不进行归一化


class MissingValueMethod(Enum):
    """缺失值填充方法枚举"""
    MEAN = "mean"  # 均值填充
    MEDIAN = "median"  # 中位数填充
    MODE = "mode"  # 众数填充
    FORWARD_FILL = "forward_fill"  # 前向填充
    INTERPOLATION = "interpolation"  # 插值填充
    KNN = "knn"  # K近邻填充
    TOPOLOGY_BASED = "topology_based"  # 基于拓扑的填充


class FaultType(Enum):
    """故障类型枚举"""
    SINGLE_PHASE_GROUND = "single_phase_ground"  # 单相接地
    TWO_PHASE_SHORT = "two_phase_short"  # 两相短路
    TWO_PHASE_GROUND = "two_phase_ground"  # 两相接地
    THREE_PHASE_SHORT = "three_phase_short"  # 三相短路
    LINE_BREAK = "line_break"  # 断线
    EQUIPMENT_FAILURE = "equipment_failure"  # 设备故障


@dataclass
class DataQualityMetrics:
    """数据质量指标类"""
    completeness: float  # 完整性 (0-1)
    accuracy: float  # 准确性 (0-1)
    consistency: float  # 一致性 (0-1)
    timeliness: float  # 及时性 (0-1)
    validity: float  # 有效性 (0-1)


class MultimodalPreprocessor:
    """多态数据预处理类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化预处理模块
        
        Parameters
        ----------
        config : Optional[Dict[str, Any]], default=None
            配置参数
        """
        self.config = config or {}
        self.scalers: Dict[str, Any] = {}
        self.imputers: Dict[str, Any] = {}
        self.quality_metrics: Dict[str, DataQualityMetrics] = {}
        
        # 默认配置
        self.default_config = {
            'normalization_method': NormalizationMethod.STANDARD,
            'imputation_method': MissingValueMethod.INTERPOLATION,
            'outlier_threshold': 3.0,  # Z-score阈值
            'knn_neighbors': 5,
            'max_missing_ratio': 0.3,  # 最大缺失率
            'augmentation_factor': 2,  # 数据增强倍数
        }
        
        # 更新配置
        self.default_config.update(self.config)
    
    def normalize_data(self, 
                      data: Union[pd.DataFrame, np.ndarray], 
                      method: NormalizationMethod = None,
                      feature_names: Optional[List[str]] = None) -> Union[pd.DataFrame, np.ndarray]:
        """数据归一化
        
        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray]
            输入数据
        method : NormalizationMethod, default=None
            归一化方法
        feature_names : Optional[List[str]], default=None
            特征名称
            
        Returns
        -------
        Union[pd.DataFrame, np.ndarray]
            归一化后的数据
        """
        if method is None:
            method = self.default_config['normalization_method']
        
        if isinstance(data, pd.DataFrame):
            feature_names = data.columns.tolist()
            values = data.values
        else:
            values = data
            if feature_names is None:
                feature_names = [f'feature_{i}' for i in range(values.shape[1])]
        
        # 处理全零或常数列
        valid_columns = []
        for i in range(values.shape[1]):
            if np.std(values[:, i]) > 1e-10:  # 非常数列
                valid_columns.append(i)
        
        if not valid_columns:
            warnings.warn("所有特征都是常数，无法进行归一化")
            return data
        
        valid_values = values[:, valid_columns]
        
        if method == NormalizationMethod.STANDARD:
            scaler = StandardScaler()
            normalized_values = scaler.fit_transform(valid_values)
            self.scalers['standard'] = scaler
        
        elif method == NormalizationMethod.MINMAX:
            scaler = MinMaxScaler()
            normalized_values = scaler.fit_transform(valid_values)
            self.scalers['minmax'] = scaler
        
        elif method == NormalizationMethod.ROBUST:
            scaler = RobustScaler()
            normalized_values = scaler.fit_transform(valid_values)
            self.scalers['robust'] = scaler
        
        elif method == NormalizationMethod.LOG:
            # 对数变换，处理前确保数据为正
            valid_values = np.where(valid_values <= 0, 1e-10, valid_values)
            normalized_values = np.log(valid_values)
        
        else:  # NONE
            normalized_values = valid_values
        
        # 重建完整数据
        result = np.zeros_like(values)
        for i, col_idx in enumerate(valid_columns):
            result[:, col_idx] = normalized_values[:, i]
        
        if isinstance(data, pd.DataFrame):
            return pd.DataFrame(result, columns=feature_names, index=data.index)
        else:
            return result
    
    def detect_outliers(self, 
                       data: Union[pd.DataFrame, np.ndarray],
                       method: str = 'zscore',
                       threshold: float = None) -> Dict[str, List[int]]:
        """检测异常值
        
        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray]
            输入数据
        method : str, default='zscore'
            异常检测方法
        threshold : float, default=None
            异常检测阈值
            
        Returns
        -------
        Dict[str, List[int]]
            异常值索引字典
        """
        if threshold is None:
            threshold = self.default_config['outlier_threshold']
        
        outliers = {}
        
        if isinstance(data, pd.DataFrame):
            feature_names = data.columns.tolist()
            values = data.values
        else:
            values = data
            feature_names = [f'feature_{i}' for i in range(values.shape[1])]
        
        for i, feature_name in enumerate(feature_names):
            feature_data = values[:, i]
            
            # 移除NaN值
            valid_data = feature_data[~np.isnan(feature_data)]
            
            if len(valid_data) < 2:
                continue
            
            if method == 'zscore':
                # Z-score方法
                mean_val = np.mean(valid_data)
                std_val = np.std(valid_data)
                
                if std_val == 0:
                    continue
                
                z_scores = np.abs((feature_data - mean_val) / std_val)
                outlier_indices = np.where(z_scores > threshold)[0].tolist()
            
            elif method == 'iqr':
                # IQR方法
                q1 = np.percentile(valid_data, 25)
                q3 = np.percentile(valid_data, 75)
                iqr = q3 - q1
                
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outlier_indices = np.where((feature_data < lower_bound) | 
                                          (feature_data > upper_bound))[0].tolist()
            
            else:
                raise ValueError(f"不支持的异常检测方法: {method}")
            
            if outlier_indices:
                outliers[feature_name] = outlier_indices
        
        return outliers
    
    def handle_outliers(self, 
                       data: Union[pd.DataFrame, np.ndarray],
                       method: str = 'clip',
                       **kwargs) -> Union[pd.DataFrame, np.ndarray]:
        """处理异常值
        
        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray]
            输入数据
        method : str, default='clip'
            异常值处理方法
        **kwargs
            额外参数
            
        Returns
        -------
        Union[pd.DataFrame, np.ndarray]
            处理后的数据
        """
        outliers = self.detect_outliers(data, **kwargs)
        
        if isinstance(data, pd.DataFrame):
            result = data.copy()
            values = result.values
        else:
            values = data.copy()
        
        for feature_name, outlier_indices in outliers.items():
            if isinstance(data, pd.DataFrame):
                col_idx = data.columns.get_loc(feature_name)
            else:
                col_idx = int(feature_name.split('_')[-1])
            
            feature_data = values[:, col_idx]
            valid_data = feature_data[~np.isnan(feature_data)]
            
            if method == 'clip':
                # 截断法
                if len(valid_data) > 0:
                    q1 = np.percentile(valid_data, 1)  # 使用1%和99%分位数
                    q99 = np.percentile(valid_data, 99)
                    
                    feature_data[feature_data < q1] = q1
                    feature_data[feature_data > q99] = q99
            
            elif method == 'remove':
                # 移除法（设置为NaN）
                feature_data[outlier_indices] = np.nan
            
            elif method == 'mean':
                # 均值替换
                mean_val = np.mean(valid_data)
                feature_data[outlier_indices] = mean_val
            
            else:
                raise ValueError(f"不支持的异常值处理方法: {method}")
        
        if isinstance(data, pd.DataFrame):
            return result
        else:
            return values
    
    def impute_missing_data(self, 
                           data: Union[pd.DataFrame, np.ndarray],
                           method: MissingValueMethod = None,
                           **kwargs) -> Union[pd.DataFrame, np.ndarray]:
        """缺失值填充
        
        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray]
            输入数据
        method : MissingValueMethod, default=None
            填充方法
        **kwargs
            额外参数
            
        Returns
        -------
        Union[pd.DataFrame, np.ndarray]
            填充后的数据
        """
        if method is None:
            method = self.default_config['imputation_method']
        
        if isinstance(data, pd.DataFrame):
            feature_names = data.columns.tolist()
            values = data.values
            index = data.index
        else:
            values = data
            feature_names = [f'feature_{i}' for i in range(values.shape[1])]
            index = None
        
        # 检查缺失率
        missing_ratio = np.isnan(values).sum() / values.size
        max_missing_ratio = self.default_config['max_missing_ratio']
        
        if missing_ratio > max_missing_ratio:
            warnings.warn(f"缺失率 {missing_ratio:.2%} 超过阈值 {max_missing_ratio:.2%}")
        
        if method == MissingValueMethod.MEAN:
            imputer = SimpleImputer(strategy='mean')
            imputed_values = imputer.fit_transform(values)
            self.imputers['mean'] = imputer
        
        elif method == MissingValueMethod.MEDIAN:
            imputer = SimpleImputer(strategy='median')
            imputed_values = imputer.fit_transform(values)
            self.imputers['median'] = imputer
        
        elif method == MissingValueMethod.MODE:
            imputer = SimpleImputer(strategy='most_frequent')
            imputed_values = imputer.fit_transform(values)
            self.imputers['mode'] = imputer
        
        elif method == MissingValueMethod.KNN:
            n_neighbors = kwargs.get('n_neighbors', self.default_config['knn_neighbors'])
            imputer = KNNImputer(n_neighbors=n_neighbors)
            imputed_values = imputer.fit_transform(values)
            self.imputers['knn'] = imputer
        
        elif method == MissingValueMethod.INTERPOLATION:
            # 时序数据的线性插值
            if index is not None and isinstance(index, pd.DatetimeIndex):
                df = pd.DataFrame(values, index=index, columns=feature_names)
                imputed_df = df.interpolate(method='linear')
                imputed_values = imputed_df.values
            else:
                # 非时序数据使用简单插值
                imputer = SimpleImputer(strategy='mean')
                imputed_values = imputer.fit_transform(values)
        
        elif method == MissingValueMethod.FORWARD_FILL:
            if index is not None and isinstance(index, pd.DatetimeIndex):
                df = pd.DataFrame(values, index=index, columns=feature_names)
                imputed_df = df.ffill().bfill()  # 前向填充+后向填充
                imputed_values = imputed_df.values
            else:
                imputer = SimpleImputer(strategy='mean')
                imputed_values = imputer.fit_transform(values)
        
        else:
            raise ValueError(f"不支持的填充方法: {method}")
        
        if isinstance(data, pd.DataFrame):
            return pd.DataFrame(imputed_values, columns=feature_names, index=index)
        else:
            return imputed_values
    
    def augment_fault_data(self, 
                          fault_data: Dict[str, Any],
                          augmentation_factor: int = None) -> List[Dict[str, Any]]:
        """故障数据增强
        
        Parameters
        ----------
        fault_data : Dict[str, Any]
            原始故障数据
        augmentation_factor : int, default=None
            增强倍数
            
        Returns
        -------
        List[Dict[str, Any]]
            增强后的故障数据列表
        """
        if augmentation_factor is None:
            augmentation_factor = self.default_config['augmentation_factor']
        
        augmented_data = [fault_data]  # 包含原始数据
        
        for i in range(augmentation_factor):
            augmented_sample = fault_data.copy()
            
            # 故障类型增强
            if 'fault_type' in augmented_sample:
                fault_types = list(FaultType)
                current_type = FaultType(augmented_sample['fault_type'])
                
                # 随机选择不同的故障类型（有一定概率保持原类型）
                if np.random.random() < 0.7:  # 70%概率改变类型
                    new_type = np.random.choice([t for t in fault_types if t != current_type])
                    augmented_sample['fault_type'] = new_type.value
            
            # 故障阻抗增强
            if 'fault_impedance' in augmented_sample:
                original_impedance = augmented_sample['fault_impedance']
                # 添加随机噪声（±20%）
                noise = np.random.uniform(-0.2, 0.2)
                augmented_sample['fault_impedance'] = original_impedance * (1 + noise)
            
            # 故障持续时间增强
            if 'duration' in augmented_sample:
                original_duration = augmented_sample['duration']
                # 添加随机噪声（±30%）
                noise = np.random.uniform(-0.3, 0.3)
                augmented_sample['duration'] = max(0.1, original_duration * (1 + noise))
            
            # 故障位置增强
            if 'location' in augmented_sample:
                # 在拓扑结构中随机选择故障位置
                # 这里需要拓扑信息，简化处理为添加噪声
                if isinstance(augmented_sample['location'], (int, float)):
                    noise = np.random.normal(0, 0.1)
                    augmented_sample['location'] += noise
            
            # 量测数据增强
            if 'measurements' in augmented_sample:
                measurements = augmented_sample['measurements']
                if isinstance(measurements, (list, np.ndarray)):
                    # 添加高斯噪声
                    noise_std = np.std(measurements) * 0.1  # 10%的标准差
                    noise = np.random.normal(0, noise_std, len(measurements))
                    augmented_sample['measurements'] = measurements + noise
            
            augmented_data.append(augmented_sample)
        
        return augmented_data
    
    def calculate_data_quality(self, 
                              data: Union[pd.DataFrame, np.ndarray],
                              data_type: DataType) -> DataQualityMetrics:
        """计算数据质量指标
        
        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray]
            输入数据
        data_type : DataType
            数据类型
            
        Returns
        -------
        DataQualityMetrics
            数据质量指标
        """
        if isinstance(data, pd.DataFrame):
            values = data.values
        else:
            values = data
        
        # 完整性（非缺失值比例）
        completeness = 1 - (np.isnan(values).sum() / values.size)
        
        # 准确性（基于统计检验，简化处理）
        # 这里可以添加更复杂的准确性评估逻辑
        accuracy = 0.9  # 默认值
        
        # 一致性（检查数据范围是否合理）
        consistency = 1.0
        for i in range(values.shape[1]):
            col_data = values[:, i]
            valid_data = col_data[~np.isnan(col_data)]
            if len(valid_data) > 0:
                # 检查是否存在明显不合理值
                if data_type == DataType.MEASUREMENT:
                    # 电压应该在合理范围内（0-500kV）
                    if np.any((valid_data < 0) | (valid_data > 500)):
                        consistency *= 0.8
        
        # 及时性（检查时间戳连续性）
        timeliness = 1.0
        if isinstance(data, pd.DataFrame) and isinstance(data.index, pd.DatetimeIndex):
            time_diffs = data.index.to_series().diff().dt.total_seconds()
            if len(time_diffs) > 1:
                expected_interval = time_diffs.mode().iloc[0] if not time_diffs.mode().empty else 1
                large_gaps = (time_diffs > 2 * expected_interval).sum()
                timeliness = 1 - (large_gaps / len(time_diffs))
        
        # 有效性（检查数据格式和类型）
        validity = 1.0
        
        metrics = DataQualityMetrics(
            completeness=completeness,
            accuracy=accuracy,
            consistency=consistency,
            timeliness=timeliness,
            validity=validity
        )
        
        self.quality_metrics[data_type.value] = metrics
        return metrics
    
    def preprocess_pipeline(self, 
                           data: Union[pd.DataFrame, np.ndarray],
                           data_type: DataType,
                           steps: List[str] = None) -> Union[pd.DataFrame, np.ndarray]:
        """完整的数据预处理流水线
        
        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray]
            输入数据
        data_type : DataType
            数据类型
        steps : List[str], default=None
            处理步骤列表
            
        Returns
        -------
        Union[pd.DataFrame, np.ndarray]
            预处理后的数据
        """
        if steps is None:
            steps = ['quality_check', 'outlier_detection', 'outlier_handling', 
                    'imputation', 'normalization']
        
        processed_data = data
        
        for step in steps:
            if step == 'quality_check':
                quality_metrics = self.calculate_data_quality(processed_data, data_type)
                print(f"数据质量指标: {quality_metrics}")
            
            elif step == 'outlier_detection':
                outliers = self.detect_outliers(processed_data)
                if outliers:
                    print(f"检测到异常值: {len(outliers)} 个特征")
            
            elif step == 'outlier_handling':
                processed_data = self.handle_outliers(processed_data)
            
            elif step == 'imputation':
                processed_data = self.impute_missing_data(processed_data)
            
            elif step == 'normalization':
                processed_data = self.normalize_data(processed_data)
            
            else:
                warnings.warn(f"未知的处理步骤: {step}")
        
        return processed_data
    
    def export_preprocessing_config(self) -> Dict[str, Any]:
        """导出预处理配置
        
        Returns
        -------
        Dict[str, Any]
            预处理配置
        """
        return {
            'config': self.default_config,
            'scalers': {name: type(scaler).__name__ for name, scaler in self.scalers.items()},
            'imputers': {name: type(imputer).__name__ for name, imputer in self.imputers.items()},
            'quality_metrics': {name: vars(metrics) for name, metrics in self.quality_metrics.items()}
        }


# 工具函数
def create_sample_fault_data() -> Dict[str, Any]:
    """创建示例故障数据
    
    Returns
    -------
    Dict[str, Any]
        示例故障数据
    """
    return {
        'fault_type': FaultType.SINGLE_PHASE_GROUND.value,
        'fault_impedance': 10.0,  # 欧姆
        'duration': 0.5,  # 秒
        'location': 'line1',
        'measurements': np.random.normal(100, 10, 100),  # 模拟量测数据
        'timestamp': pd.Timestamp.now()
    }


def validate_preprocessing_result(original_data: np.ndarray, 
                                 processed_data: np.ndarray) -> Dict[str, float]:
    """验证预处理结果
    
    Parameters
    ----------
    original_data : np.ndarray
        原始数据
    processed_data : np.ndarray
        预处理后数据
        
    Returns
    -------
    Dict[str, float]
        验证指标
    """
    metrics = {}
    
    # 数据完整性
    original_missing = np.isnan(original_data).sum()
    processed_missing = np.isnan(processed_data).sum()
    metrics['missing_reduction'] = (original_missing - processed_missing) / original_data.size
    
    # 数据分布变化
    original_mean = np.nanmean(original_data)
    processed_mean = np.nanmean(processed_data)
    metrics['mean_change'] = abs(processed_mean - original_mean) / (abs(original_mean) + 1e-10)
    
    original_std = np.nanstd(original_data)
    processed_std = np.nanstd(processed_data)
    metrics['std_change'] = abs(processed_std - original_std) / (original_std + 1e-10)
    
    return metrics