"""
内存管理模块

提供高效的内存管理功能，包括：
- 内存池管理：减少内存分配开销
- 大数组处理：分块处理和流式计算
- 内存监控：实时监控内存使用情况
- 垃圾回收优化：主动内存清理
- 缓存管理：LRU缓存和内存映射文件
"""

import gc
import os
import sys
import psutil
import threading
import time
import numpy as np
import logging
from typing import Any, Dict, List, Optional, Tuple, Callable, Union, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
from collections import OrderedDict
from abc import ABC, abstractmethod
import weakref
import pickle
import mmap

class MemoryLevel(Enum):
    """内存层级"""
    L1_CACHE = "l1_cache"      # CPU L1缓存
    L2_CACHE = "l2_cache"      # CPU L2缓存
    L3_CACHE = "l3_cache"      # CPU L3缓存
    RAM = "ram"                # 内存
    SSD = "ssd"                # 固态硬盘
    HDD = "hdd"                # 机械硬盘

@dataclass
class MemoryInfo:
    """内存信息"""
    total: int                 # 总内存(字节)
    available: int             # 可用内存(字节)
    used: int                  # 已使用内存(字节)
    percentage: float          # 使用百分比
    level: MemoryLevel = MemoryLevel.RAM
    
    @property
    def free(self) -> int:
        """空闲内存"""
        return self.total - self.used

@dataclass
class MemoryBlock:
    """内存块"""
    block_id: str
    start_address: int
    size: int
    level: MemoryLevel
    access_count: int = 0
    last_access_time: float = field(default_factory=time.time)
    data: Optional[Any] = None
    
    def access(self):
        """访问内存块"""
        self.access_count += 1
        self.last_access_time = time.time()

class MemoryPool(ABC):
    """内存池抽象基类"""
    
    @abstractmethod
    def allocate(self, size: int) -> MemoryBlock:
        """分配内存"""
        pass
    
    @abstractmethod
    def deallocate(self, block: MemoryBlock):
        """释放内存"""
        pass
    
    @abstractmethod
    def get_info(self) -> MemoryInfo:
        """获取内存池信息"""
        pass

class FixedSizeMemoryPool(MemoryPool):
    """固定大小内存池"""
    
    def __init__(self, block_size: int, num_blocks: int, level: MemoryLevel = MemoryLevel.RAM):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.level = level
        
        self.free_blocks: List[MemoryBlock] = []
        self.allocated_blocks: Dict[str, MemoryBlock] = {}
        self.block_counter = 0
        
        # 预分配内存块
        for i in range(num_blocks):
            block = MemoryBlock(
                block_id=f"block_{i}",
                start_address=0,  # 在真实实现中这里应该是实际地址
                size=block_size,
                level=level
            )
            self.free_blocks.append(block)
    
    def allocate(self, size: int) -> MemoryBlock:
        """分配内存块"""
        if size > self.block_size:
            raise ValueError(f"请求大小 {size} 超过块大小 {self.block_size}")
        
        if not self.free_blocks:
            raise MemoryError("内存池已满")
        
        block = self.free_blocks.pop(0)
        self.allocated_blocks[block.block_id] = block
        
        return block
    
    def deallocate(self, block: MemoryBlock):
        """释放内存块"""
        if block.block_id in self.allocated_blocks:
            del self.allocated_blocks[block.block_id]
            self.free_blocks.append(block)
        else:
            raise ValueError(f"内存块 {block.block_id} 不存在或未分配")
    
    def get_info(self) -> MemoryInfo:
        """获取内存池信息"""
        total_size = self.block_size * self.num_blocks
        used_size = self.block_size * (self.num_blocks - len(self.free_blocks))
        
        return MemoryInfo(
            total=total_size,
            used=used_size,
            available=total_size - used_size,
            percentage=used_size / total_size * 100,
            level=self.level
        )

class VariableSizeMemoryPool(MemoryPool):
    """可变大小内存池"""
    
    def __init__(self, total_size: int, level: MemoryLevel = MemoryLevel.RAM):
        self.total_size = total_size
        self.level = level
        self.free_memory = total_size
        self.allocated_blocks: Dict[str, MemoryBlock] = {}
        self.block_counter = 0
    
    def allocate(self, size: int) -> MemoryBlock:
        """分配内存"""
        if size > self.free_memory:
            raise MemoryError(f"内存不足: 需要 {size}, 可用 {self.free_memory}")
        
        block = MemoryBlock(
            block_id=f"block_{self.block_counter}",
            start_address=0,  # 简化实现
            size=size,
            level=self.level
        )
        
        self.block_counter += 1
        self.allocated_blocks[block.block_id] = block
        self.free_memory -= size
        
        return block
    
    def deallocate(self, block: MemoryBlock):
        """释放内存"""
        if block.block_id in self.allocated_blocks:
            self.free_memory += block.size
            del self.allocated_blocks[block.block_id]
        else:
            raise ValueError(f"内存块 {block.block_id} 不存在或未分配")
    
    def get_info(self) -> MemoryInfo:
        """获取内存池信息"""
        used_size = self.total_size - self.free_memory
        
        return MemoryInfo(
            total=self.total_size,
            used=used_size,
            available=self.free_memory,
            percentage=used_size / self.total_size * 100,
            level=self.level
        )

class LRUCache:
    """LRU缓存"""
    
    def __init__(self, max_size: int = 1000, max_memory: int = 100 * 1024 * 1024):  # 100MB
        self.max_size = max_size
        self.max_memory = max_memory
        self.cache: OrderedDict[str, Tuple[Any, int]] = OrderedDict()  # value, size
        self.current_memory = 0
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        with self.lock:
            if key in self.cache:
                value, size = self.cache[key]
                # 移动到末尾(LRU)
                del self.cache[key]
                self.cache[key] = (value, size)
                self.hit_count += 1
                return value
            else:
                self.miss_count += 1
                return None
    
    def put(self, key: str, value: Any, size: Optional[int] = None):
        """放入缓存项"""
        with self.lock:
            # 计算大小（简化实现）
            if size is None:
                try:
                    size = sys.getsizeof(value)
                except:
                    size = 64  # 默认大小
            
            # 如果键已存在，删除旧值
            if key in self.cache:
                old_size = self.cache[key][1]
                self.current_memory -= old_size
                del self.cache[key]
            
            # 如果缓存满，删除最久未使用的项
            while (len(self.cache) >= self.max_size or 
                   self.current_memory + size > self.max_memory):
                oldest_key, (oldest_value, oldest_size) = self.cache.popitem(last=False)
                self.current_memory -= oldest_size
            
            self.cache[key] = (value, size)
            self.current_memory += size
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.current_memory = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self.hit_count + self.miss_count
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'memory_usage': self.current_memory,
            'max_memory': self.max_memory,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': self.hit_count / total_requests if total_requests > 0 else 0,
            'utilization': self.current_memory / self.max_memory
        }

class MemoryMappedFile:
    """内存映射文件"""
    
    def __init__(self, file_path: str, size: int, mode: str = 'r+'):
        self.file_path = file_path
        self.size = size
        self.mode = mode
        
        # 创建文件
        with open(file_path, 'wb') as f:
            f.seek(size - 1)
            f.write(b'\0')
        
        # 打开内存映射
        self.file = open(file_path, mode)
        self.mapped_memory = mmap.mmap(self.file.fileno(), size)
    
    def read(self, offset: int, size: int) -> bytes:
        """读取数据"""
        return self.mapped_memory[offset:offset + size]
    
    def write(self, offset: int, data: bytes):
        """写入数据"""
        self.mapped_memory[offset:offset + len(data)] = data
    
    def close(self):
        """关闭映射"""
        self.mapped_memory.close()
        self.file.close()
        os.unlink(self.file_path)

class ChunkedArrayProcessor:
    """分块数组处理器"""
    
    def __init__(self, chunk_size: int = 1024 * 1024):  # 1MB
        self.chunk_size = chunk_size
        self.temp_files: List[str] = []
    
    def process_large_array(self, 
                          array: np.ndarray, 
                          process_func: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
        """分块处理大数组"""
        total_size = array.size
        result_chunks = []
        
        for start_idx in range(0, total_size, self.chunk_size):
            end_idx = min(start_idx + self.chunk_size, total_size)
            chunk = array.flat[start_idx:end_idx]
            
            # 处理块
            processed_chunk = process_func(chunk)
            result_chunks.append(processed_chunk)
        
        # 合并结果
        return np.concatenate(result_chunks)
    
    def create_temp_file(self) -> str:
        """创建临时文件"""
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        temp_path = temp_file.name
        self.temp_files.append(temp_path)
        return temp_path
    
    def cleanup_temp_files(self):
        """清理临时文件"""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except OSError:
                pass
        self.temp_files.clear()

class MemoryMonitor:
    """内存监控器"""
    
    def __init__(self, check_interval: float = 1.0):
        self.check_interval = check_interval
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.memory_history: List[Tuple[float, MemoryInfo]] = []
        self.warning_callbacks: List[Callable[[MemoryInfo], None]] = []
        self.critical_callbacks: List[Callable[[MemoryInfo], None]] = []
        
        self.enable_logging = True
        if self.enable_logging:
            self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self):
        """开始监控"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        if self.enable_logging:
            self.logger.info("内存监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        if self.enable_logging:
            self.logger.info("内存监控已停止")
    
    def add_warning_callback(self, callback: Callable[[MemoryInfo], None]):
        """添加警告回调"""
        self.warning_callbacks.append(callback)
    
    def add_critical_callback(self, callback: Callable[[MemoryInfo], None]):
        """添加严重警告回调"""
        self.critical_callbacks.append(callback)
    
    def get_current_memory_info(self) -> MemoryInfo:
        """获取当前内存信息"""
        memory = psutil.virtual_memory()
        return MemoryInfo(
            total=memory.total,
            available=memory.available,
            used=memory.used,
            percentage=memory.percent,
            level=MemoryLevel.RAM
        )
    
    def _monitor_loop(self):
        """监控循环"""
        while self.is_monitoring:
            try:
                memory_info = self.get_current_memory_info()
                self.memory_history.append((time.time(), memory_info))
                
                # 保留最近1小时的数据
                current_time = time.time()
                self.memory_history = [
                    (timestamp, info) for timestamp, info in self.memory_history
                    if current_time - timestamp < 3600
                ]
                
                # 检查内存使用情况
                if memory_info.percentage > 90:  # 严重警告
                    for callback in self.critical_callbacks:
                        try:
                            callback(memory_info)
                        except Exception as e:
                            if self.enable_logging:
                                self.logger.error(f"严重警告回调错误: {str(e)}")
                    
                    if self.enable_logging:
                        self.logger.critical(f"内存使用率严重过高: {memory_info.percentage:.1f}%")
                
                elif memory_info.percentage > 80:  # 警告
                    for callback in self.warning_callbacks:
                        try:
                            callback(memory_info)
                        except Exception as e:
                            if self.enable_logging:
                                self.logger.error(f"警告回调错误: {str(e)}")
                    
                    if self.enable_logging:
                        self.logger.warning(f"内存使用率过高: {memory_info.percentage:.1f}%")
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                if self.enable_logging:
                    self.logger.error(f"内存监控错误: {str(e)}")
                time.sleep(self.check_interval)
    
    def get_memory_statistics(self, duration: float = 300) -> Dict[str, Any]:
        """获取内存统计信息"""
        current_time = time.time()
        recent_history = [
            info for timestamp, info in self.memory_history
            if current_time - timestamp <= duration
        ]
        
        if not recent_history:
            return {}
        
        percentages = [info.percentage for info in recent_history]
        usages = [info.used for info in recent_history]
        
        return {
            'duration': duration,
            'data_points': len(recent_history),
            'avg_usage_percent': np.mean(percentages),
            'max_usage_percent': np.max(percentages),
            'min_usage_percent': np.min(percentages),
            'std_usage_percent': np.std(percentages),
            'avg_used_bytes': np.mean(usages),
            'max_used_bytes': np.max(usages),
            'min_used_bytes': np.min(usages)
        }

class MemoryManager:
    """内存管理器"""
    
    def __init__(self, 
                 total_memory_gb: float = 8.0,
                 cache_size_mb: int = 100,
                 enable_monitoring: bool = True):
        self.total_memory = int(total_memory_gb * 1024 * 1024 * 1024)
        self.cache = LRUCache(max_memory=cache_size_mb * 1024 * 1024)
        self.monitor = MemoryMonitor() if enable_monitoring else None
        
        # 内存池
        self.pools: Dict[MemoryLevel, MemoryPool] = {
            MemoryLevel.RAM: VariableSizeMemoryPool(self.total_memory, MemoryLevel.RAM)
        }
        
        # 垃圾回收设置
        gc.set_threshold(700, 10, 10)  # 调整GC阈值
        
        self.enable_logging = True
        if self.enable_logging:
            self.logger = logging.getLogger(__name__)
        
        # 添加内存监控回调
        if self.monitor:
            self.monitor.add_warning_callback(self._handle_memory_warning)
            self.monitor.add_critical_callback(self._handle_memory_critical)
    
    def start_monitoring(self):
        """开始内存监控"""
        if self.monitor:
            self.monitor.start_monitoring()
    
    def stop_monitoring(self):
        """停止内存监控"""
        if self.monitor:
            self.monitor.stop_monitoring()
    
    def allocate_memory(self, size: int, level: MemoryLevel = MemoryLevel.RAM) -> MemoryBlock:
        """分配内存"""
        if level not in self.pools:
            raise ValueError(f"不支持的内存层级: {level}")
        
        return self.pools[level].allocate(size)
    
    def deallocate_memory(self, block: MemoryBlock):
        """释放内存"""
        if block.level not in self.pools:
            raise ValueError(f"不支持的内存层级: {block.level}")
        
        self.pools[block.level].deallocate(block)
    
    def cache_data(self, key: str, data: Any):
        """缓存数据"""
        self.cache.put(key, data)
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        return self.cache.get(key)
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
    
    def process_large_array(self, 
                          array: np.ndarray, 
                          process_func: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
        """处理大数组"""
        # 检查是否需要分块处理
        array_size_bytes = array.nbytes
        memory_threshold = self.total_memory * 0.5  # 使用50%内存作为阈值
        
        if array_size_bytes > memory_threshold:
            # 分块处理
            processor = ChunkedArrayProcessor()
            try:
                result = processor.process_large_array(array, process_func)
                return result
            finally:
                processor.cleanup_temp_files()
        else:
            # 直接处理
            return process_func(array)
    
    def optimize_memory(self):
        """优化内存"""
        # 强制垃圾回收
        collected = gc.collect()
        
        # 清理缓存
        old_cache_stats = self.cache.get_stats()
        self.clear_cache()
        
        # 获取当前内存状态
        memory_info = self.get_memory_info()
        
        if self.enable_logging:
            self.logger.info(f"内存优化完成: 回收对象 {collected} 个")
            self.logger.info(f"清理缓存: 释放 {old_cache_stats['memory_usage']} 字节")
            self.logger.info(f"当前内存使用: {memory_info.percentage:.1f}%")
        
        return {
            'collected_objects': collected,
            'released_cache_bytes': old_cache_stats['memory_usage'],
            'current_memory_percent': memory_info.percentage
        }
    
    def get_memory_info(self) -> MemoryInfo:
        """获取内存信息"""
        return self.monitor.get_current_memory_info() if self.monitor else psutil.virtual_memory()
    
    def get_memory_statistics(self, duration: float = 300) -> Dict[str, Any]:
        """获取内存统计"""
        if self.monitor:
            return self.monitor.get_memory_statistics(duration)
        else:
            return {}
    
    def get_pools_info(self) -> Dict[str, Any]:
        """获取内存池信息"""
        info = {}
        for level, pool in self.pools.items():
            info[level.value] = pool.get_info()
        return info
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return self.cache.get_stats()
    
    def _handle_memory_warning(self, memory_info: MemoryInfo):
        """处理内存警告"""
        # 自动清理缓存
        self.clear_cache()
        
        # 强制垃圾回收
        gc.collect()
        
        if self.enable_logging:
            self.logger.warning("自动内存优化完成")
    
    def _handle_memory_critical(self, memory_info: MemoryInfo):
        """处理严重内存警告"""
        # 激进清理
        self.clear_cache()
        gc.collect()
        gc.collect()  # 多次GC
        
        if self.enable_logging:
            self.logger.critical("激进内存清理完成")
    
    def __enter__(self):
        self.start_monitoring()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_monitoring()

# 便捷函数
def create_memory_manager(total_memory_gb: float = 8.0,
                        cache_size_mb: int = 100) -> MemoryManager:
    """创建内存管理器"""
    return MemoryManager(total_memory_gb, cache_size_mb)

def monitor_memory_usage(callback: Callable[[MemoryInfo], None],
                       check_interval: float = 1.0):
    """监控内存使用"""
    manager = MemoryManager(enable_monitoring=True)
    manager.monitor.add_warning_callback(callback)
    manager.monitor.start_monitoring()
    return manager