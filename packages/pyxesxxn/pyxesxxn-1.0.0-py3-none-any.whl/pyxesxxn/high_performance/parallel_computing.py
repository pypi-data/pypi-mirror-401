"""
并行计算模块

提供多线程和多进程计算功能，支持：
- 多进程计算池 (ProcessPool)
- 多线程计算池 (ThreadPool)  
- 任务调度和负载均衡
- 计算结果收集和错误处理
"""

import multiprocessing as mp
import threading
import concurrent.futures
import queue
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import Future, ThreadPoolExecutor, ProcessPoolExecutor

T = TypeVar('T')
R = TypeVar('R')

class PoolType(Enum):
    """计算池类型"""
    THREAD = "thread"
    PROCESS = "process"

class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Task(Generic[T]):
    """计算任务"""
    id: str
    func: Callable[[T], R]
    args: T
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    callback: Optional[Callable[[Future[R]], None]] = None
    created_at: float = field(default_factory=time.time)
    
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority.value > other.priority.value
        return self.created_at < other.created_at

@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    result: Any
    success: bool
    execution_time: float
    error: Optional[Exception] = None
    worker_id: Optional[str] = None

class ParallelComputator:
    """并行计算管理器"""
    
    def __init__(self, 
                 pool_type: PoolType = PoolType.PROCESS,
                 max_workers: Optional[int] = None,
                 chunk_size: int = 1000,
                 timeout: float = 3600,
                 enable_logging: bool = True):
        """
        初始化并行计算管理器
        
        Args:
            pool_type: 计算池类型
            max_workers: 最大工作进程/线程数
            chunk_size: 任务分块大小
            timeout: 默认超时时间
            enable_logging: 是否启用日志
        """
        self.pool_type = pool_type
        self.max_workers = max_workers or mp.cpu_count()
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.enable_logging = enable_logging
        
        if enable_logging:
            self.logger = logging.getLogger(__name__)
        
        self._executor: Optional[Union[ThreadPoolExecutor, ProcessPoolExecutor]] = None
        self._task_queue = queue.PriorityQueue()
        self._running_tasks: Dict[str, Future] = {}
        self._completed_tasks: Dict[str, TaskResult] = {}
        self._shutdown = False
        
    def start(self):
        """启动计算池"""
        if self._executor is not None:
            raise RuntimeError("计算池已经启动")
            
        if self.pool_type == PoolType.THREAD:
            self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        else:
            self._executor = ProcessPoolExecutor(max_workers=self.max_workers)
            
        if self.enable_logging:
            self.logger.info(f"启动{self.pool_type.value}计算池，工作进程数: {self.max_workers}")
    
    def stop(self):
        """停止计算池"""
        if self._executor is not None:
            self._executor.shutdown(wait=True)
            self._executor = None
            if self.enable_logging:
                self.logger.info("计算池已停止")
    
    def submit_task(self, 
                   task_id: str,
                   func: Callable[[T], R], 
                   args: T,
                   priority: TaskPriority = TaskPriority.NORMAL,
                   timeout: Optional[float] = None,
                   callback: Optional[Callable[[Future[R]], None]] = None) -> Future[R]:
        """
        提交计算任务
        
        Args:
            task_id: 任务ID
            func: 计算函数
            args: 函数参数
            priority: 任务优先级
            timeout: 超时时间
            callback: 结果回调函数
            
        Returns:
            任务Future对象
        """
        if self._executor is None:
            raise RuntimeError("计算池未启动，请先调用start()方法")
            
        if self._shutdown:
            raise RuntimeError("计算管理器已关闭")
            
        task = Task(
            id=task_id,
            func=func,
            args=args,
            priority=priority,
            timeout=timeout or self.timeout,
            callback=callback
        )
        
        future = self._executor.submit(self._execute_task, task)
        self._running_tasks[task_id] = future
        
        if self.enable_logging:
            self.logger.debug(f"提交任务: {task_id}, 优先级: {priority.name}")
        
        return future
    
    def _execute_task(self, task: Task[T]) -> R:
        """执行单个任务"""
        start_time = time.time()
        worker_id = f"{self.pool_type.value}_{threading.get_ident()}"
        
        try:
            # 应用超时
            if task.timeout:
                result = self._execute_with_timeout(task.func, task.args, task.timeout)
            else:
                result = task.func(task.args)
                
            execution_time = time.time() - start_time
            
            task_result = TaskResult(
                task_id=task.id,
                result=result,
                success=True,
                execution_time=execution_time,
                worker_id=worker_id
            )
            
            self._completed_tasks[task.id] = task_result
            
            if self.enable_logging:
                self.logger.debug(f"任务完成: {task.id}, 耗时: {execution_time:.2f}s")
                
            # 执行回调函数
            if task.callback:
                future = Future()
                future.set_result(result)
                task.callback(future)
                
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            task_result = TaskResult(
                task_id=task.id,
                result=None,
                success=False,
                execution_time=execution_time,
                error=e,
                worker_id=worker_id
            )
            
            self._completed_tasks[task.id] = task_result
            
            if self.enable_logging:
                self.logger.error(f"任务失败: {task.id}, 错误: {str(e)}")
                
            # 重试机制
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                if self.enable_logging:
                    self.logger.info(f"重试任务: {task.id}, 重试次数: {task.retry_count}")
                return self._execute_task(task)
            else:
                raise e
    
    def _execute_with_timeout(self, func: Callable, args, timeout: float) -> Any:
        """带超时执行"""
        result_queue = queue.Queue()
        
        def target():
            try:
                result = func(args)
                result_queue.put(('success', result))
            except Exception as e:
                result_queue.put(('error', e))
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout)
        
        if thread.is_alive():
            raise TimeoutError(f"任务执行超时 ({timeout}s)")
        
        status, result = result_queue.get()
        if status == 'error':
            raise result
        return result
    
    def map_async(self, 
                 func: Callable[[T], R], 
                 data_list: List[T],
                 chunk_size: Optional[int] = None) -> List[R]:
        """
        异步映射执行
        
        Args:
            func: 计算函数
            data_list: 数据列表
            chunk_size: 分块大小
            
        Returns:
            结果列表
        """
        if self._executor is None:
            raise RuntimeError("计算池未启动")
            
        chunk_size = chunk_size or self.chunk_size
        
        if self.enable_logging:
            self.logger.info(f"开始并行映射执行，任务数: {len(data_list)}, 分块大小: {chunk_size}")
        
        futures = []
        for i, data in enumerate(data_list):
            task_id = f"map_task_{i}"
            future = self.submit_task(task_id, func, data)
            futures.append(future)
        
        # 等待所有任务完成
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
        
        if self.enable_logging:
            self.logger.info(f"并行映射执行完成，处理了 {len(results)} 个任务")
        
        return results
    
    def get_task_status(self, task_id: str) -> Optional[TaskResult]:
        """获取任务状态"""
        if task_id in self._completed_tasks:
            return self._completed_tasks[task_id]
        elif task_id in self._running_tasks:
            future = self._running_tasks[task_id]
            if future.done():
                # 任务已完成，移动到已完成列表
                try:
                    result = future.result()
                    task_result = TaskResult(
                        task_id=task_id,
                        result=result,
                        success=True,
                        execution_time=0.0  # 实际执行时间需要从其他地方获取
                    )
                    self._completed_tasks[task_id] = task_result
                    del self._running_tasks[task_id]
                    return task_result
                except Exception as e:
                    task_result = TaskResult(
                        task_id=task_id,
                        result=None,
                        success=False,
                        execution_time=0.0,
                        error=e
                    )
                    self._completed_tasks[task_id] = task_result
                    del self._running_tasks[task_id]
                    return task_result
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        completed_count = len(self._completed_tasks)
        running_count = len(self._running_tasks)
        
        if self._completed_tasks:
            execution_times = [task.execution_time for task in self._completed_tasks.values()]
            avg_time = sum(execution_times) / len(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
        else:
            avg_time = min_time = max_time = 0.0
        
        return {
            'pool_type': self.pool_type.value,
            'max_workers': self.max_workers,
            'running_tasks': running_count,
            'completed_tasks': completed_count,
            'total_tasks': running_count + completed_count,
            'avg_execution_time': avg_time,
            'min_execution_time': min_time,
            'max_execution_time': max_time,
            'success_rate': completed_count / (running_count + completed_count) if (running_count + completed_count) > 0 else 0
        }
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

class ProcessPool(ParallelComputator):
    """进程池"""
    
    def __init__(self, **kwargs):
        super().__init__(pool_type=PoolType.PROCESS, **kwargs)

class ThreadPool(ParallelComputator):
    """线程池"""
    
    def __init__(self, **kwargs):
        super().__init__(pool_type=PoolType.THREAD, **kwargs)