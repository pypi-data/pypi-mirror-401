"""
基于时域差分运算的配电网多分支线路故障定位模块

该模块实现了基于时域差分运算的单端/双端定位方案，通过时域差分消除正弦分量，
将故障行波转化为脉冲信号实现波头精准标定，结合反射波时序约束与极性判别，
仅需主干线路配置检测装置即可完成多分支故障定位。
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Set, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass
import numpy as np
import pandas as pd
from pyxesxxn.topology_metering_fusion import TopologyMeteringFusion, DistributionNode, DistributionBranch, DistributionSwitch, MeasurementType


class FaultLocatorType(Enum):
    """故障定位器类型枚举"""
    SINGLE_END = 0  # 单端定位
    DOUBLE_END = 1  # 双端定位


class LineType(Enum):
    """线路类型枚举"""
    MAIN_LINE = 0  # 主干线路
    BRANCH_LINE = 1  # 分支线路


@dataclass
class WavefrontInfo:
    """行波波头信息类"""
    arrival_time: float  # 波头到达时间(ms)
    polarity: int  # 波头极性(1: 正向, -1: 反向)
    amplitude: float  # 波头幅值
    confidence: float  # 标定置信度


@dataclass
class TimeDomainFaultLocationResult:
    """时域差分故障定位结果类"""
    fault_distance: float  # 故障距离(km)
    fault_line_type: LineType  # 故障线路类型
    fault_branch: str  # 故障分支ID
    wavefronts: List[WavefrontInfo]  # 检测到的波头信息
    confidence: float  # 定位置信度
    calculation_time: float  # 计算时间(ms)
    locator_type: FaultLocatorType  # 定位器类型


class TimeDomainFaultLocator:
    """基于时域差分运算的配电网多分支线路故障定位器"""
    
    def __init__(self, fusion_module: TopologyMeteringFusion):
        """初始化时域差分故障定位器
        
        Parameters
        ----------
        fusion_module : TopologyMeteringFusion
            拓扑-量测数据融合模块实例
        """
        self.fusion_module = fusion_module
        self.locator_type: FaultLocatorType = FaultLocatorType.SINGLE_END
        self.wave_speed: float = 2.99792458e5  # 行波波速(km/s，默认光速，可根据实际线路调整)
        self.sampling_rate: float = 1e6  # 采样率(Hz)
        self.window_size: int = 100  # 短时窗长度(采样点)
        
        # 差分运算参数
        self.lambda_param: float = 0.0  # 脉冲优化系数
        self.alpha: float = 0.1  # 衰减系数
        
        # 滤波参数
        self.kalman_process_noise: float = 1e-5  # 卡尔曼滤波过程噪声
        self.kalman_measurement_noise: float = 1e-3  # 卡尔曼滤波测量噪声
        
        # 波头检测参数
        self.wavefront_threshold: float = 0.1  # 波头检测阈值
        self.polarity_threshold: float = 0.05  # 极性判别阈值
        
        # 定位结果
        self.fault_location_result: Optional[TimeDomainFaultLocationResult] = None
    
    def set_locator_type(self, locator_type: FaultLocatorType) -> None:
        """设置定位器类型
        
        Parameters
        ----------
        locator_type : FaultLocatorType
            定位器类型(SINGLE_END/DOUBLE_END)
        """
        self.locator_type = locator_type
    
    def set_wave_speed(self, wave_speed: float) -> None:
        """设置行波波速
        
        Parameters
        ----------
        wave_speed : float
            行波波速(km/s)
        """
        self.wave_speed = wave_speed
    
    def set_sampling_rate(self, sampling_rate: float) -> None:
        """设置采样率
        
        Parameters
        ----------
        sampling_rate : float
            采样率(Hz)
        """
        self.sampling_rate = sampling_rate
    
    def _time_domain_model(self, t: float, ta: float, A: float, tau: float, B: float, C: float) -> float:
        """故障行波时域模型
        
        Parameters
        ----------
        t : float
            时间(s)
        ta : float
            故障起始时间(s)
        A : float
            幅值系数
        tau : float
            衰减时间常数(s)
        B : float
            线性系数
        C : float
            常数项
        
        Returns
        -------
        float
            故障行波信号值
        """
        if t < ta:
            return B * t + C
        else:
            exponential_term = A * np.exp(-(t - ta) / tau)
            return exponential_term + B * t + C
    
    def _single_difference(self, signal: np.ndarray) -> np.ndarray:
        """一次差分运算
        
        Parameters
        ----------
        signal : np.ndarray
            原始信号
        
        Returns
        -------
        np.ndarray
            一次差分结果
        """
        diff = np.diff(signal)
        return np.concatenate(([0], diff))
    
    def _double_difference(self, signal: np.ndarray) -> np.ndarray:
        """二次差分运算
        
        Parameters
        ----------
        signal : np.ndarray
            原始信号
        
        Returns
        -------
        np.ndarray
            二次差分结果
        """
        single_diff = self._single_difference(signal)
        double_diff = self._single_difference(single_diff)
        return double_diff
    
    def _pulse_optimization(self, double_diff_signal: np.ndarray) -> np.ndarray:
        """脉冲优化
        
        Parameters
        ----------
        double_diff_signal : np.ndarray
            二次差分信号
        
        Returns
        -------
        np.ndarray
            优化后的脉冲信号
        """
        # 计算lambda系数
        if len(double_diff_signal) < 2:
            return double_diff_signal
        
        x = double_diff_signal[1:]
        y = double_diff_signal[:-1]
        
        if np.sum(y ** 2) == 0:
            self.lambda_param = 0.0
        else:
            self.lambda_param = np.sum(x * y) / np.sum(y ** 2)
        
        # 应用脉冲优化
        optimized = np.zeros_like(double_diff_signal)
        optimized[0] = double_diff_signal[0]
        for i in range(1, len(double_diff_signal)):
            optimized[i] = double_diff_signal[i] - self.lambda_param * double_diff_signal[i-1]
        
        return optimized
    
    def _improved_kalman_filter(self, signal: np.ndarray) -> np.ndarray:
        """改进卡尔曼滤波
        
        Parameters
        ----------
        signal : np.ndarray
            原始信号
        
        Returns
        -------
        np.ndarray
            滤波后的信号
        """
        if len(signal) == 0:
            return signal
        
        # 初始化卡尔曼滤波参数
        n = len(signal)
        filtered = np.zeros(n)
        P = 1.0  # 估计误差协方差
        
        # 初始值
        filtered[0] = signal[0]
        
        # 卡尔曼滤波迭代
        for k in range(1, n):
            # 预测
            x_pred = filtered[k-1]
            P_pred = P + self.kalman_process_noise
            
            # 更新
            K = P_pred / (P_pred + self.kalman_measurement_noise)
            filtered[k] = x_pred + K * (signal[k] - x_pred)
            P = (1 - K) * P_pred
        
        return filtered
    
    def _detect_wavefronts(self, signal: np.ndarray) -> List[WavefrontInfo]:
        """检测行波波头
        
        Parameters
        ----------
        signal : np.ndarray
            优化后的脉冲信号
        
        Returns
        -------
        List[WavefrontInfo]
            检测到的波头信息列表
        """
        wavefronts = []
        sample_interval = 1.0 / self.sampling_rate * 1000  # 采样间隔(ms)
        
        # 查找超过阈值的峰值
        for i in range(1, len(signal)-1):
            # 检测峰值
            if ((signal[i] > signal[i-1] and signal[i] > signal[i+1]) or 
                (signal[i] < signal[i-1] and signal[i] < signal[i+1])):
                
                # 检查是否超过阈值
                if abs(signal[i]) > self.wavefront_threshold:
                    # 计算波头到达时间
                    arrival_time = i * sample_interval
                    
                    # 计算极性
                    polarity = 1 if signal[i] > 0 else -1
                    
                    # 计算置信度
                    confidence = min(1.0, abs(signal[i]) / self.wavefront_threshold)
                    
                    wavefront = WavefrontInfo(
                        arrival_time=arrival_time,
                        polarity=polarity,
                        amplitude=signal[i],
                        confidence=confidence
                    )
                    wavefronts.append(wavefront)
        
        # 按到达时间排序
        wavefronts.sort(key=lambda x: x.arrival_time)
        
        return wavefronts
    
    def _wavefront_calibration(self, voltage_signal: np.ndarray) -> List[WavefrontInfo]:
        """行波波头标定
        
        Parameters
        ----------
        voltage_signal : np.ndarray
            电压信号
        
        Returns
        -------
        List[WavefrontInfo]
            标定后的波头信息列表
        """
        # 应用改进卡尔曼滤波
        filtered_signal = self._improved_kalman_filter(voltage_signal)
        
        # 执行时域差分运算
        double_diff = self._double_difference(filtered_signal)
        
        # 脉冲优化
        optimized_pulse = self._pulse_optimization(double_diff)
        
        # 检测波头
        wavefronts = self._detect_wavefronts(optimized_pulse)
        
        return wavefronts
    
    def _main_line_location(self, wavefronts_m: List[WavefrontInfo], wavefronts_n: List[WavefrontInfo], line_length: float) -> float:
        """主干线路故障定位
        
        Parameters
        ----------
        wavefronts_m : List[WavefrontInfo]
            M端检测到的波头信息
        wavefronts_n : List[WavefrontInfo]
            N端检测到的波头信息
        line_length : float
            线路长度(km)
        
        Returns
        -------
        float
            故障距离(km)
        """
        if len(wavefronts_m) < 2 or len(wavefronts_n) < 2:
            return 0.0
        
        # 获取初始行波和反射波到达时间
        t_m1 = wavefronts_m[0].arrival_time  # M端初始行波到达时间
        t_m2 = wavefronts_m[1].arrival_time  # M端反射波到达时间
        t_n1 = wavefronts_n[0].arrival_time  # N端初始行波到达时间
        t_n2 = wavefronts_n[1].arrival_time  # N端反射波到达时间
        
        # 计算时间差
        delta_t_m = t_m2 - t_m1
        delta_t_n = t_n2 - t_n1
        
        # 应用定位公式
        if delta_t_m + delta_t_n == 0:
            return line_length / 2
        
        # M端定位距离
        d_mf = (delta_t_m / (delta_t_m + delta_t_n)) * line_length
        
        # N端定位距离
        d_nf = (delta_t_n / (delta_t_n + delta_t_m)) * line_length
        
        # 返回平均值
        return (d_mf + d_nf) / 2
    
    def _branch_line_location(self, wavefronts: List[WavefrontInfo], line_length: float, branch_point_distance: float) -> float:
        """分支线路故障定位
        
        Parameters
        ----------
        wavefronts : List[WavefrontInfo]
            检测到的波头信息
        line_length : float
            线路长度(km)
        branch_point_distance : float
            分支点距离(km)
        
        Returns
        -------
        float
            故障距离(km)
        """
        if len(wavefronts) < 3:
            return branch_point_distance
        
        # 获取波头到达时间
        t_m1 = wavefronts[0].arrival_time  # 初始行波到达时间
        t_m2 = wavefronts[1].arrival_time  # 反射波到达时间1
        t_m3 = wavefronts[2].arrival_time  # 反射波到达时间2
        
        # 计算距离
        l_mp1 = branch_point_distance
        l_p1q1 = line_length - branch_point_distance
        
        # 公式1: l_MF' = l_MP1 + (t_M2 - t_M1) * v / 2
        l_mf_prime = l_mp1 + (t_m2 - t_m1) * 1e-3 * self.wave_speed / 2
        
        # 公式2: l_MF'' = l_MP1 + l_P1Q1 - (t_M3 - t_M1) * v / 2
        l_mf_double_prime = l_mp1 + l_p1q1 - (t_m3 - t_m1) * 1e-3 * self.wave_speed / 2
        
        # 返回平均值
        return (l_mf_prime + l_mf_double_prime) / 2
    
    def _identify_fault_branch(self, wavefronts: List[WavefrontInfo]) -> Tuple[str, LineType]:
        """识别故障分支
        
        Parameters
        ----------
        wavefronts : List[WavefrontInfo]
            检测到的波头信息
        
        Returns
        -------
        Tuple[str, LineType]
            故障分支ID和线路类型
        """
        # 简化实现：基于波头数量和时序关系判断
        if len(wavefronts) < 3:
            # 波头数量较少，可能是主干线路故障
            return "main", LineType.MAIN_LINE
        else:
            # 波头数量较多，可能是分支线路故障
            # 这里需要根据实际网络拓扑进行更复杂的判断
            # 简化实现：返回第一个分支
            if self.fusion_module.branches:
                first_branch = list(self.fusion_module.branches.keys())[0]
                return first_branch, LineType.BRANCH_LINE
            else:
                return "main", LineType.MAIN_LINE
    
    def locate_fault(self, voltage_signal_m: np.ndarray, voltage_signal_n: Optional[np.ndarray] = None) -> TimeDomainFaultLocationResult:
        """执行故障定位
        
        Parameters
        ----------
        voltage_signal_m : np.ndarray
            M端电压信号
        voltage_signal_n : Optional[np.ndarray], default=None
            N端电压信号(双端定位时使用)
        
        Returns
        -------
        TimeDomainFaultLocationResult
            故障定位结果
        """
        import time
        start_time = time.time()
        
        # 默认值
        fault_distance = 0.0
        fault_line_type = LineType.MAIN_LINE
        fault_branch = "main"
        confidence = 0.0
        
        # 标定波头
        wavefronts_m = self._wavefront_calibration(voltage_signal_m)
        wavefronts_n = []
        
        if voltage_signal_n is not None:
            # 双端定位
            self.locator_type = FaultLocatorType.DOUBLE_END
            wavefronts_n = self._wavefront_calibration(voltage_signal_n)
        else:
            # 单端定位
            self.locator_type = FaultLocatorType.SINGLE_END
        
        # 获取线路长度
        main_line_length = 0.0
        if self.fusion_module.branches:
            # 简化实现：使用第一个支路的长度作为主干线路长度
            first_branch = list(self.fusion_module.branches.values())[0]
            main_line_length = first_branch.length
        
        # 识别故障分支
        fault_branch, fault_line_type = self._identify_fault_branch(wavefronts_m)
        
        # 根据线路类型执行定位
        if fault_line_type == LineType.MAIN_LINE:
            if self.locator_type == FaultLocatorType.DOUBLE_END and wavefronts_n:
                # 双端主干线路定位
                fault_distance = self._main_line_location(wavefronts_m, wavefronts_n, main_line_length)
            else:
                # 单端主干线路定位
                if len(wavefronts_m) >= 2:
                    t_m1 = wavefronts_m[0].arrival_time
                    t_m2 = wavefronts_m[1].arrival_time
                    fault_distance = (t_m2 - t_m1) * 1e-3 * self.wave_speed / 2
        else:
            # 分支线路定位
            fault_distance = self._branch_line_location(wavefronts_m, main_line_length, main_line_length / 2)
        
        # 计算置信度
        confidence = min(1.0, 0.5 + 0.5 * len(wavefronts_m) / 5)
        
        # 计算耗时
        calculation_time = (time.time() - start_time) * 1000  # 转换为ms
        
        # 构建结果
        result = TimeDomainFaultLocationResult(
            fault_distance=fault_distance,
            fault_line_type=fault_line_type,
            fault_branch=fault_branch,
            wavefronts=wavefronts_m,
            confidence=confidence,
            calculation_time=calculation_time,
            locator_type=self.locator_type
        )
        
        return result
    
    def run_location(self, voltage_signal_m: np.ndarray, voltage_signal_n: Optional[np.ndarray] = None) -> TimeDomainFaultLocationResult:
        """运行故障定位
        
        Parameters
        ----------
        voltage_signal_m : np.ndarray
            M端电压信号
        voltage_signal_n : Optional[np.ndarray], default=None
            N端电压信号(双端定位时使用)
        
        Returns
        -------
        TimeDomainFaultLocationResult
            故障定位结果
        """
        return self.locate_fault(voltage_signal_m, voltage_signal_n)


# 工具函数
def create_sample_time_domain_locator() -> TimeDomainFaultLocator:
    """创建示例时域差分故障定位器
    
    Returns
    -------
    TimeDomainFaultLocator
        示例故障定位器
    """
    # 创建拓扑-量测融合模块
    from pyxesxxn.topology_metering_fusion import create_sample_distribution_network
    fusion = create_sample_distribution_network()
    
    # 创建故障定位器
    locator = TimeDomainFaultLocator(fusion)
    
    # 设置参数
    locator.set_wave_speed(2.5e5)  # 设置行波波速为250000 km/s
    locator.set_sampling_rate(1e6)  # 设置采样率为1 MHz
    
    return locator


def generate_test_voltage_signal(duration: float = 0.01, fault_time: float = 0.001) -> np.ndarray:
    """生成测试电压信号
    
    Parameters
    ----------
    duration : float, default=0.01
        信号持续时间(s)
    fault_time : float, default=0.001
        故障发生时间(s)
    
    Returns
    -------
    np.ndarray
        测试电压信号
    """
    # 采样点数
    sampling_rate = 1e6
    n_points = int(duration * sampling_rate)
    
    # 生成时间轴
    t = np.linspace(0, duration, n_points)
    
    # 生成原始电压信号
    voltage = np.zeros(n_points)
    
    # 添加故障行波
    for i in range(n_points):
        if t[i] >= fault_time:
            # 故障行波时域模型
            exponential_term = 1000 * np.exp(-(t[i] - fault_time) / 0.0001)  # 指数衰减分量
            linear_term = 0.1 * t[i]  # 线性趋势项
            voltage[i] = exponential_term + linear_term
        else:
            # 正常电压
            voltage[i] = 0.1 * t[i] + 100  # 线性趋势
    
    # 添加噪声
    noise = np.random.normal(0, 5, n_points)
    voltage += noise
    
    return voltage
