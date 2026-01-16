"""
分布式计算模块

提供集群和云计算环境下的分布式计算功能，支持：
- 本地集群管理器 (LocalClusterManager)
- 云端集群管理器 (CloudClusterManager)
- 任务分发和结果收集
- 动态资源管理和负载均衡
"""

import os
import json
import time
import logging
import threading
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import socket
import psutil
import requests

class ClusterType(Enum):
    """集群类型"""
    LOCAL = "local"
    KUBERNETES = "kubernetes"
    SLURM = "slurm"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"

class JobStatus(Enum):
    """作业状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ResourceType(Enum):
    """资源类型"""
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    STORAGE = "storage"

@dataclass
class WorkerNode:
    """工作节点"""
    node_id: str
    hostname: str
    ip_address: str
    cpu_count: int
    memory_gb: float
    gpu_count: int = 0
    status: str = "active"
    load: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    
    def is_healthy(self) -> bool:
        """检查节点健康状态"""
        current_time = time.time()
        return (current_time - self.last_heartbeat) < 300  # 5分钟超时

@dataclass
class ComputeJob:
    """计算作业"""
    job_id: str
    command: str
    args: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    resource_request: Dict[ResourceType, float] = field(default_factory=dict)
    priority: int = 0
    max_runtime: float = 3600
    max_retries: int = 3
    created_at: float = field(default_factory=time.time)
    status: JobStatus = JobStatus.PENDING
    assigned_node: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    exit_code: Optional[int] = None
    output_file: Optional[str] = None
    error_file: Optional[str] = None
    retry_count: int = 0
    
    @property
    def runtime(self) -> float:
        """计算运行时间"""
        if self.start_time is None:
            return 0.0
        end_time = self.end_time or time.time()
        return end_time - self.start_time

@dataclass
class ClusterConfig:
    """集群配置"""
    cluster_type: ClusterType
    master_url: str
    worker_nodes: List[str] = field(default_factory=list)
    max_workers: int = 100
    cpu_per_worker: int = 1
    memory_per_worker: float = 4.0  # GB
    gpu_per_worker: int = 0
    timeout: float = 7200
    max_concurrent_jobs: int = 1000
    queue_size: int = 10000

class ClusterManager:
    """集群管理器基类"""
    
    def __init__(self, config: ClusterConfig):
        self.config = config
        self.workers: Dict[str, WorkerNode] = {}
        self.jobs: Dict[str, ComputeJob] = {}
        self.job_queue: List[ComputeJob] = []
        self.running_jobs: Dict[str, ComputeJob] = {}
        self.completed_jobs: Dict[str, ComputeJob] = {}
        self.failed_jobs: Dict[str, ComputeJob] = {}
        self.enable_logging = True
        
        if self.enable_logging:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
    
    def start(self):
        """启动集群管理器"""
        self._initialize_cluster()
        self._start_heartbeat_monitor()
        self._start_job_scheduler()
        
        if self.enable_logging:
            self.logger.info(f"集群管理器已启动，类型: {self.config.cluster_type.value}")
    
    def stop(self):
        """停止集群管理器"""
        self._stop_job_scheduler()
        self._stop_heartbeat_monitor()
        self._cleanup_cluster()
        
        if self.enable_logging:
            self.logger.info("集群管理器已停止")
    
    def submit_job(self, 
                   job_id: str,
                   command: str,
                   args: Optional[List[str]] = None,
                   environment: Optional[Dict[str, str]] = None,
                   resource_request: Optional[Dict[ResourceType, float]] = None,
                   priority: int = 0,
                   max_runtime: float = 3600) -> ComputeJob:
        """
        提交计算作业
        
        Args:
            job_id: 作业ID
            command: 执行命令
            args: 命令参数
            environment: 环境变量
            resource_request: 资源请求
            priority: 优先级
            max_runtime: 最大运行时间
            
        Returns:
            计算作业对象
        """
        args = args or []
        environment = environment or {}
        resource_request = resource_request or {}
        
        job = ComputeJob(
            job_id=job_id,
            command=command,
            args=args,
            environment=environment,
            resource_request=resource_request,
            priority=priority,
            max_runtime=max_runtime
        )
        
        self.jobs[job_id] = job
        self.job_queue.append(job)
        self.job_queue.sort(key=lambda x: x.priority, reverse=True)
        
        if self.enable_logging:
            self.logger.info(f"作业已提交: {job_id}, 优先级: {priority}")
        
        return job
    
    def cancel_job(self, job_id: str) -> bool:
        """取消作业"""
        if job_id not in self.jobs:
            return False
            
        job = self.jobs[job_id]
        job.status = JobStatus.CANCELLED
        
        # 从队列中移除
        if job in self.job_queue:
            self.job_queue.remove(job)
        
        # 如果正在运行，强制终止
        if job_id in self.running_jobs:
            self._terminate_job(job)
            del self.running_jobs[job_id]
        
        if self.enable_logging:
            self.logger.info(f"作业已取消: {job_id}")
        
        return True
    
    def get_job_status(self, job_id: str) -> Optional[ComputeJob]:
        """获取作业状态"""
        return self.jobs.get(job_id)
    
    def get_cluster_status(self) -> Dict[str, Any]:
        """获取集群状态"""
        active_workers = sum(1 for worker in self.workers.values() if worker.is_healthy())
        
        return {
            'cluster_type': self.config.cluster_type.value,
            'total_workers': len(self.workers),
            'active_workers': active_workers,
            'running_jobs': len(self.running_jobs),
            'pending_jobs': len(self.job_queue),
            'completed_jobs': len(self.completed_jobs),
            'failed_jobs': len(self.failed_jobs),
            'total_jobs': len(self.jobs),
            'utilization': active_workers / max(1, len(self.workers))
        }
    
    def get_worker_status(self, worker_id: str) -> Optional[WorkerNode]:
        """获取工作节点状态"""
        return self.workers.get(worker_id)
    
    def _initialize_cluster(self):
        """初始化集群"""
        if self.config.cluster_type == ClusterType.LOCAL:
            self._initialize_local_cluster()
        elif self.config.cluster_type == ClusterType.KUBERNETES:
            self._initialize_kubernetes_cluster()
        elif self.config.cluster_type == ClusterType.SLURM:
            self._initialize_slurm_cluster()
        elif self.config.cluster_type in [ClusterType.AWS, ClusterType.AZURE, ClusterType.GCP]:
            self._initialize_cloud_cluster()
    
    def _initialize_local_cluster(self):
        """初始化本地集群"""
        # 获取本地系统资源
        cpu_count = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # 创建本地工作节点
        worker_id = f"local_worker_{socket.gethostname()}"
        worker = WorkerNode(
            node_id=worker_id,
            hostname=socket.gethostname(),
            ip_address='127.0.0.1',
            cpu_count=cpu_count,
            memory_gb=memory_gb
        )
        
        self.workers[worker_id] = worker
        
        if self.enable_logging:
            self.logger.info(f"本地集群初始化完成: {cpu_count} CPU, {memory_gb:.1f}GB 内存")
    
    def _initialize_kubernetes_cluster(self):
        """初始化Kubernetes集群"""
        try:
            # 使用kubectl获取工作节点
            result = subprocess.run(['kubectl', 'get', 'nodes', '-o', 'json'],
                                  capture_output=True, text=True, check=True)
            nodes_info = json.loads(result.stdout)
            
            for node_info in nodes_info.get('items', []):
                node_name = node_info['metadata']['name']
                worker_id = f"k8s_worker_{node_name}"
                
                # 解析节点资源
                cpu_count = node_info['status']['capacity'].get('cpu', '1')
                memory = node_info['status']['capacity'].get('memory', '4Gi')
                
                # 转换内存单位
                if 'Gi' in memory:
                    memory_gb = float(memory.replace('Gi', ''))
                elif 'Mi' in memory:
                    memory_gb = float(memory.replace('Mi', '')) / 1024
                else:
                    memory_gb = 4.0
                
                worker = WorkerNode(
                    node_id=worker_id,
                    hostname=node_name,
                    ip_address='',
                    cpu_count=int(cpu_count),
                    memory_gb=memory_gb
                )
                
                self.workers[worker_id] = worker
            
            if self.enable_logging:
                self.logger.info(f"Kubernetes集群初始化完成，节点数: {len(self.workers)}")
                
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            if self.enable_logging:
                self.logger.error(f"Kubernetes集群初始化失败: {str(e)}")
    
    def _initialize_slurm_cluster(self):
        """初始化Slurm集群"""
        try:
            # 使用sinfo获取节点信息
            result = subprocess.run(['sinfo', '-h', '-o', '%n,%c,%m'],
                                  capture_output=True, text=True, check=True)
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        node_name = parts[0]
                        cpu_count = int(parts[1])
                        memory_mb = int(parts[2])
                        memory_gb = memory_mb / 1024
                        
                        worker_id = f"slurm_worker_{node_name}"
                        worker = WorkerNode(
                            node_id=worker_id,
                            hostname=node_name,
                            ip_address='',
                            cpu_count=cpu_count,
                            memory_gb=memory_gb
                        )
                        
                        self.workers[worker_id] = worker
            
            if self.enable_logging:
                self.logger.info(f"Slurm集群初始化完成，节点数: {len(self.workers)}")
                
        except (subprocess.CalledProcessError, ValueError) as e:
            if self.enable_logging:
                self.logger.error(f"Slurm集群初始化失败: {str(e)}")
    
    def _initialize_cloud_cluster(self):
        """初始化云端集群"""
        # 云端集群初始化逻辑
        if self.enable_logging:
            self.logger.info(f"云端集群初始化: {self.config.cluster_type.value}")
    
    def _start_heartbeat_monitor(self):
        """启动心跳监控"""
        def heartbeat_worker():
            while not self._shutdown:
                current_time = time.time()
                for worker in self.workers.values():
                    if not worker.is_healthy():
                        if self.enable_logging:
                            self.logger.warning(f"工作节点无响应: {worker.node_id}")
                
                time.sleep(60)  # 每分钟检查一次
        
        self._heartbeat_thread = threading.Thread(target=heartbeat_worker, daemon=True)
        self._heartbeat_thread.start()
    
    def _stop_heartbeat_monitor(self):
        """停止心跳监控"""
        if hasattr(self, '_heartbeat_thread'):
            self._shutdown = True
            self._heartbeat_thread.join(timeout=5)
    
    def _start_job_scheduler(self):
        """启动作业调度器"""
        def scheduler_worker():
            while not self._shutdown:
                try:
                    self._schedule_jobs()
                    time.sleep(5)  # 每5秒调度一次
                except Exception as e:
                    if self.enable_logging:
                        self.logger.error(f"作业调度器错误: {str(e)}")
                    time.sleep(10)
        
        self._scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
        self._scheduler_thread.start()
    
    def _stop_job_scheduler(self):
        """停止作业调度器"""
        if hasattr(self, '_scheduler_thread'):
            self._shutdown = True
            self._scheduler_thread.join(timeout=5)
    
    def _schedule_jobs(self):
        """调度作业"""
        while (self.job_queue and 
               len(self.running_jobs) < self.config.max_concurrent_jobs and
               self._get_available_worker() is not None):
            
            job = self.job_queue.pop(0)
            worker = self._get_available_worker()
            
            if worker:
                self._launch_job(job, worker)
    
    def _get_available_worker(self) -> Optional[WorkerNode]:
        """获取可用工作节点"""
        for worker in self.workers.values():
            if (worker.is_healthy() and 
                worker.node_id not in [job.assigned_node for job in self.running_jobs.values()]):
                return worker
        return None
    
    def _launch_job(self, job: ComputeJob, worker: WorkerNode):
        """启动作业"""
        job.status = JobStatus.RUNNING
        job.assigned_node = worker.node_id
        job.start_time = time.time()
        
        self.running_jobs[job.job_id] = job
        
        # 在新线程中执行作业
        def job_worker():
            try:
                self._execute_job(job)
            except Exception as e:
                if self.enable_logging:
                    self.logger.error(f"作业执行错误: {job.job_id}, 错误: {str(e)}")
                job.status = JobStatus.FAILED
                self.failed_jobs[job.job_id] = job
        
        threading.Thread(target=job_worker, daemon=True).start()
        
        if self.enable_logging:
            self.logger.info(f"作业已启动: {job.job_id} 在节点 {worker.node_id}")
    
    def _execute_job(self, job: ComputeJob):
        """执行作业"""
        try:
            # 准备环境
            env = os.environ.copy()
            env.update(job.environment)
            
            # 执行命令
            process = subprocess.Popen(
                [job.command] + job.args,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待完成或超时
            try:
                stdout, stderr = process.communicate(timeout=job.max_runtime)
                job.exit_code = process.returncode
                
                # 保存输出
                if job.output_file:
                    with open(job.output_file, 'w') as f:
                        f.write(stdout.decode())
                
                if job.error_file:
                    with open(job.error_file, 'w') as f:
                        f.write(stderr.decode())
                
                if job.exit_code == 0:
                    job.status = JobStatus.COMPLETED
                    self.completed_jobs[job.job_id] = job
                else:
                    job.status = JobStatus.FAILED
                    self.failed_jobs[job.job_id] = job
                    
            except subprocess.TimeoutExpired:
                process.kill()
                job.status = JobStatus.FAILED
                self.failed_jobs[job.job_id] = job
                
        except Exception as e:
            job.status = JobStatus.FAILED
            self.failed_jobs[job.job_id] = job
            
        finally:
            job.end_time = time.time()
            
            # 从运行作业中移除
            if job.job_id in self.running_jobs:
                del self.running_jobs[job.job_id]
            
            if self.enable_logging:
                self.logger.info(f"作业执行完成: {job.job_id}, 状态: {job.status.value}")
    
    def _terminate_job(self, job: ComputeJob):
        """终止作业"""
        # 实现作业终止逻辑
        if self.enable_logging:
            self.logger.info(f"作业已终止: {job.job_id}")
    
    def _cleanup_cluster(self):
        """清理集群"""
        # 清理资源
        self.workers.clear()
        self.jobs.clear()

class DistributedComputator:
    """分布式计算管理器"""
    
    def __init__(self, config: ClusterConfig):
        self.cluster_manager = None
        self.config = config
        self.enable_logging = True
        
        if self.enable_logging:
            self.logger = logging.getLogger(__name__)
    
    def start(self):
        """启动分布式计算"""
        self.cluster_manager = ClusterManager(self.config)
        self.cluster_manager.start()
        
        if self.enable_logging:
            self.logger.info("分布式计算管理器已启动")
    
    def stop(self):
        """停止分布式计算"""
        if self.cluster_manager:
            self.cluster_manager.stop()
            self.cluster_manager = None
        
        if self.enable_logging:
            self.logger.info("分布式计算管理器已停止")
    
    def run_distributed_task(self,
                           task_func: Callable,
                           data_list: List[Any],
                           job_name: str = "distributed_task") -> List[Any]:
        """
        运行分布式任务
        
        Args:
            task_func: 任务函数
            data_list: 数据列表
            job_name: 作业名称
            
        Returns:
            结果列表
        """
        if self.cluster_manager is None:
            raise RuntimeError("分布式计算管理器未启动")
        
        job_id = f"{job_name}_{int(time.time())}"
        
        # 创建临时Python脚本
        script_content = f"""
import pickle
import sys

def main():
    # 加载任务函数
    {pickle.dumps(task_func)}
    
    # 读取数据
    with open('input_data.pkl', 'rb') as f:
        data = pickle.load(f)
    
    # 执行任务
    results = []
    for item in data:
        try:
            result = task_func(item)
            results.append({{'success': True, 'result': result}})
        except Exception as e:
            results.append({{'success': False, 'error': str(e)}})
    
    # 保存结果
    with open('output_data.pkl', 'wb') as f:
        pickle.dump(results, f)

if __name__ == '__main__':
    main()
"""
        
        # 提交作业
        job = self.cluster_manager.submit_job(
            job_id=job_id,
            command="python",
            args=["distributed_task.py"]
        )
        
        # 等待作业完成
        while job.status in [JobStatus.PENDING, JobStatus.RUNNING]:
            time.sleep(10)
            job = self.cluster_manager.get_job_status(job_id)
        
        if job.status == JobStatus.COMPLETED:
            # 收集结果
            results = []
            # TODO: 实现结果收集逻辑
            return results
        else:
            raise RuntimeError(f"分布式作业失败: {job.status.value}")

# 便捷函数
def create_local_cluster(max_workers: Optional[int] = None,
                        cpu_per_worker: int = 1,
                        memory_per_worker: float = 4.0) -> DistributedComputator:
    """创建本地集群"""
    config = ClusterConfig(
        cluster_type=ClusterType.LOCAL,
        master_url='localhost:8080',
        max_workers=max_workers or psutil.cpu_count(),
        cpu_per_worker=cpu_per_worker,
        memory_per_worker=memory_per_worker
    )
    
    return DistributedComputator(config)

def create_cloud_cluster(cloud_provider: ClusterType,
                        instance_type: str = "m5.large") -> DistributedComputator:
    """创建云端集群"""
    config = ClusterConfig(
        cluster_type=cloud_provider,
        master_url=f'{cloud_provider.value}-master:8080',
        worker_nodes=[],
        max_workers=100,
        cpu_per_worker=4,
        memory_per_worker=16.0
    )
    
    return DistributedComputator(config)