"""
高性能计算模块

该模块提供PyPSA能源系统建模和分析的高性能计算功能，包括：
- 并行计算：多线程和多进程计算支持
- 分布式计算：集群和云计算环境支持
- 数值优化：高效求解算法
- 内存管理：大数据处理优化

主要组件：
- ParallelComputator: 并行计算管理器
- DistributedComputator: 分布式计算管理器  
- NumericalOptimizer: 数值优化器
- MemoryManager: 内存管理器
"""

from .parallel_computing import ParallelComputator, ProcessPool, ThreadPool
from .distributed_computing import DistributedComputator, ClusterManager
from .numerical_optimization import NumericalOptimizer, OptimizationAlgorithm
from .memory_management import MemoryManager

__all__ = [
    'ParallelComputator',
    'ProcessPool', 
    'ThreadPool',
    'DistributedComputator',
    'ClusterManager',
    'NumericalOptimizer',
    'OptimizationAlgorithm',
    'MemoryManager'
]

# 默认配置
DEFAULT_PARALLEL_CONFIG = {
    'max_workers': None,  # 自动检测CPU核心数
    'chunk_size': 1000,
    'timeout': 3600
}

DEFAULT_DISTRIBUTED_CONFIG = {
    'cluster_type': 'local',
    'worker_count': 4,
    'memory_limit': '8GB',
    'timeout': 7200
}

DEFAULT_OPTIMIZATION_CONFIG = {
    'algorithm': 'scipy_lbfgs',
    'tolerance': 1e-6,
    'max_iterations': 1000,
    'parallel_evaluation': True
}