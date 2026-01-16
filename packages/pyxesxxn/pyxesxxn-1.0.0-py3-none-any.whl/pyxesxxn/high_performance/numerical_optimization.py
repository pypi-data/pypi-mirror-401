"""
数值优化模块

提供高效的数值优化算法，包括：
- 经典优化算法：梯度下降、牛顿法、BFGS等
- 进化算法：遗传算法、粒子群优化、差分进化等  
- 约束优化：序列二次规划(SQP)、内点法等
- 多目标优化：NSGA-II、SPEA2等
- 随机优化：模拟退火、随机梯度下降等
"""

import numpy as np
import time
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import random

class OptimizationAlgorithm(Enum):
    """优化算法类型"""
    # 经典算法
    GRADIENT_DESCENT = "gradient_descent"
    NEWTON = "newton"
    BFGS = "bfgs"
    LBFGS = "lbfgs"
    
    # 进化算法
    GENETIC_ALGORITHM = "genetic_algorithm"
    PARTICLE_SWARM = "particle_swarm"
    DIFFERENTIAL_EVOLUTION = "differential_evolution"
    
    # 约束优化
    SQP = "sqp"
    INTERIOR_POINT = "interior_point"
    
    # 多目标优化
    NSGA2 = "nsga2"
    SPEA2 = "spea2"
    
    # 随机优化
    SIMULATED_ANNEALING = "simulated_annealing"
    SGD = "stochastic_gradient_descent"

class OptimizationStatus(Enum):
    """优化状态"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    CONVERGED = "converged"
    FAILED = "failed"
    TERMINATED = "terminated"

@dataclass
class OptimizationConfig:
    """优化配置"""
    algorithm: OptimizationAlgorithm
    max_iterations: int = 1000
    tolerance: float = 1e-6
    step_size: float = 0.01
    learning_rate: float = 0.01
    
    # 约束参数
    penalty_factor: float = 1000.0
    barrier_parameter: float = 0.1
    
    # 进化算法参数
    population_size: int = 50
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    elite_ratio: float = 0.1
    
    # 多目标参数
    num_objectives: int = 1
    
    # 收敛参数
    patience: int = 50
    min_improvement: float = 1e-8
    
    # 计算参数
    parallel_evaluation: bool = True
    use_gradient: bool = True
    
    # 随机种子
    random_seed: Optional[int] = None

@dataclass
class OptimizationResult:
    """优化结果"""
    algorithm: OptimizationAlgorithm
    best_solution: np.ndarray
    best_fitness: float
    convergence_history: List[float] = field(default_factory=list)
    execution_time: float = 0.0
    iterations: int = 0
    status: OptimizationStatus = OptimizationStatus.INITIALIZED
    message: str = ""
    
    @property
    def is_successful(self) -> bool:
        """检查是否成功收敛"""
        return self.status == OptimizationStatus.CONVERGED

@dataclass
class MultiObjectiveResult:
    """多目标优化结果"""
    algorithm: OptimizationAlgorithm
    pareto_front: np.ndarray = field(default_factory=lambda: np.array([]))
    pareto_solutions: List[np.ndarray] = field(default_factory=list)
    convergence_history: List[List[float]] = field(default_factory=list)
    execution_time: float = 0.0
    iterations: int = 0
    status: OptimizationStatus = OptimizationStatus.INITIALIZED
    num_objectives: int = 1

class OptimizationProblem(ABC):
    """优化问题抽象基类"""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.lower_bounds = np.full(dimension, -np.inf)
        self.upper_bounds = np.full(dimension, np.inf)
    
    @abstractmethod
    def evaluate(self, x: np.ndarray) -> Union[float, np.ndarray]:
        """评估目标函数"""
        pass
    
    @abstractmethod
    def gradient(self, x: np.ndarray) -> Optional[np.ndarray]:
        """计算梯度（可选）"""
        pass
    
    def constraints(self, x: np.ndarray) -> Optional[np.ndarray]:
        """约束函数（可选）"""
        return None
    
    def bounds_check(self, x: np.ndarray) -> bool:
        """检查边界约束"""
        return np.all(x >= self.lower_bounds) and np.all(x <= self.upper_bounds)

class BaseOptimizer(ABC):
    """优化器基类"""
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.problem: Optional[OptimizationProblem] = None
        self.current_iteration = 0
        self.best_solution = None
        self.best_fitness = np.inf
        self.convergence_history = []
        self.start_time = 0.0
        
        # 设置随机种子
        if config.random_seed is not None:
            np.random.seed(config.random_seed)
            random.seed(config.random_seed)
        
        self.enable_logging = True
        if self.enable_logging:
            self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """执行优化"""
        pass
    
    def _initialize_optimization(self, problem: OptimizationProblem):
        """初始化优化"""
        self.problem = problem
        self.current_iteration = 0
        self.best_solution = None
        self.best_fitness = np.inf
        self.convergence_history = []
        self.start_time = time.time()
        
        if self.enable_logging:
            self.logger.info(f"开始优化算法: {self.config.algorithm.value}")
    
    def _check_convergence(self, current_fitness: float) -> bool:
        """检查收敛条件"""
        self.convergence_history.append(current_fitness)
        
        if current_fitness < self.best_fitness:
            self.best_fitness = current_fitness
            self.best_improvement_iteration = self.current_iteration
        
        # 检查是否达到最大迭代次数
        if self.current_iteration >= self.config.max_iterations:
            return True
        
        # 检查容忍度
        if self.convergence_history:
            recent_history = self.convergence_history[-min(10, len(self.convergence_history)):]
            if len(recent_history) > 1:
                improvement = recent_history[0] - recent_history[-1]
                if abs(improvement) < self.config.tolerance:
                    return True
        
        # 检查早停
        if hasattr(self, 'best_improvement_iteration'):
            iterations_since_improvement = self.current_iteration - self.best_improvement_iteration
            if iterations_since_improvement > self.config.patience:
                if self.enable_logging:
                    self.logger.info(f"早停: {iterations_since_improvement} 次迭代无改进")
                return True
        
        return False
    
    def _create_result(self, status: OptimizationStatus, message: str = "") -> OptimizationResult:
        """创建优化结果"""
        execution_time = time.time() - self.start_time
        
        return OptimizationResult(
            algorithm=self.config.algorithm,
            best_solution=self.best_solution.copy() if self.best_solution is not None else np.array([]),
            best_fitness=self.best_fitness,
            convergence_history=self.convergence_history.copy(),
            execution_time=execution_time,
            iterations=self.current_iteration,
            status=status,
            message=message
        )

class GradientDescentOptimizer(BaseOptimizer):
    """梯度下降优化器"""
    
    def __init__(self, config: OptimizationConfig):
        super().__init__(config)
        
        if config.algorithm != OptimizationAlgorithm.GRADIENT_DESCENT:
            raise ValueError(f"算法不匹配: {config.algorithm}")
    
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """执行梯度下降优化"""
        self._initialize_optimization(problem)
        
        # 初始化解
        x = np.random.uniform(
            problem.lower_bounds,
            problem.upper_bounds,
            problem.dimension
        )
        
        if self.enable_logging:
            self.logger.info(f"初始解: {x}, 初始目标值: {problem.evaluate(x)}")
        
        try:
            while True:
                current_fitness = problem.evaluate(x)
                
                if current_fitness < self.best_fitness:
                    self.best_fitness = current_fitness
                    self.best_solution = x.copy()
                
                if self._check_convergence(current_fitness):
                    break
                
                # 计算梯度
                gradient = problem.gradient(x)
                if gradient is None:
                    # 数值梯度
                    gradient = self._numerical_gradient(problem, x)
                
                # 更新解
                x = x - self.config.learning_rate * gradient
                
                # 边界投影
                x = np.clip(x, problem.lower_bounds, problem.upper_bounds)
                
                self.current_iteration += 1
                
                if self.enable_logging and self.current_iteration % 100 == 0:
                    self.logger.info(f"迭代 {self.current_iteration}: 目标值 = {current_fitness}")
            
            return self._create_result(OptimizationStatus.CONVERGED, "梯度下降收敛")
            
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"梯度下降失败: {str(e)}")
            return self._create_result(OptimizationStatus.FAILED, str(e))
    
    def _numerical_gradient(self, problem: OptimizationProblem, x: np.ndarray) -> np.ndarray:
        """数值梯度计算"""
        eps = 1e-8
        gradient = np.zeros_like(x)
        
        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += eps
            x_minus = x.copy()
            x_minus[i] -= eps
            
            gradient[i] = (problem.evaluate(x_plus) - problem.evaluate(x_minus)) / (2 * eps)
        
        return gradient

class GeneticAlgorithmOptimizer(BaseOptimizer):
    """遗传算法优化器"""
    
    def __init__(self, config: OptimizationConfig):
        super().__init__(config)
        
        if config.algorithm != OptimizationAlgorithm.GENETIC_ALGORITHM:
            raise ValueError(f"算法不匹配: {config.algorithm}")
    
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """执行遗传算法优化"""
        self._initialize_optimization(problem)
        
        # 初始化种群
        population = self._initialize_population(problem)
        fitness_scores = self._evaluate_population(problem, population)
        
        if self.enable_logging:
            self.logger.info(f"初始种群: {len(population)} 个个体")
            self.logger.info(f"初始最佳适应度: {min(fitness_scores)}")
        
        generation = 0
        while True:
            # 选择
            selected = self._selection(population, fitness_scores)
            
            # 交叉
            offspring = self._crossover(selected)
            
            # 变异
            mutated = self._mutation(offspring, problem)
            
            # 合并种群
            population = population + mutated
            
            # 评估新种群
            new_fitness_scores = self._evaluate_population(problem, population)
            
            # 精英保留
            population, fitness_scores = self._elitism(population, new_fitness_scores)
            
            # 更新最佳解
            best_idx = np.argmin(fitness_scores)
            current_best = population[best_idx]
            current_best_fitness = fitness_scores[best_idx]
            
            if current_best_fitness < self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_solution = current_best.copy()
            
            self.current_iteration = generation + 1
            
            if self.enable_logging and generation % 50 == 0:
                self.logger.info(f"第 {generation} 代: 最佳适应度 = {current_best_fitness}")
            
            if self._check_convergence(current_best_fitness):
                break
            
            generation += 1
        
        return self._create_result(OptimizationStatus.CONVERGED, "遗传算法收敛")
    
    def _initialize_population(self, problem: OptimizationProblem) -> List[np.ndarray]:
        """初始化种群"""
        population = []
        for _ in range(self.config.population_size):
            individual = np.random.uniform(
                problem.lower_bounds,
                problem.upper_bounds,
                problem.dimension
            )
            population.append(individual)
        return population
    
    def _evaluate_population(self, problem: OptimizationProblem, population: List[np.ndarray]) -> np.ndarray:
        """评估种群"""
        fitness_scores = []
        for individual in population:
            try:
                fitness = problem.evaluate(individual)
                fitness_scores.append(fitness)
            except:
                fitness_scores.append(np.inf)  # 不可行的解给予极差适应度
        return np.array(fitness_scores)
    
    def _selection(self, population: List[np.ndarray], fitness_scores: np.ndarray) -> List[np.ndarray]:
        """选择操作（轮盘赌选择）"""
        # 适应度越小越好，所以需要取倒数
        scores = 1.0 / (1.0 + fitness_scores)
        scores = np.maximum(scores, 1e-10)  # 避免除零
        
        probabilities = scores / np.sum(scores)
        
        selected = []
        for _ in range(self.config.population_size):
            idx = np.random.choice(len(population), p=probabilities)
            selected.append(population[idx].copy())
        
        return selected
    
    def _crossover(self, population: List[np.ndarray]) -> List[np.ndarray]:
        """交叉操作（单点交叉）"""
        offspring = []
        for i in range(0, len(population), 2):
            if i + 1 < len(population):
                parent1 = population[i]
                parent2 = population[i + 1]
                
                if np.random.random() < self.config.crossover_rate:
                    # 单点交叉
                    crossover_point = np.random.randint(1, len(parent1))
                    
                    child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
                    child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
                    
                    offspring.append(child1)
                    offspring.append(child2)
                else:
                    offspring.append(parent1.copy())
                    offspring.append(parent2.copy())
        
        return offspring
    
    def _mutation(self, population: List[np.ndarray], problem: OptimizationProblem) -> List[np.ndarray]:
        """变异操作"""
        mutated = []
        
        for individual in population:
            mutated_individual = individual.copy()
            
            for i in range(len(individual)):
                if np.random.random() < self.config.mutation_rate:
                    # 高斯变异
                    mutated_individual[i] += np.random.normal(0, 0.1)
                    
                    # 边界检查
                    mutated_individual[i] = np.clip(
                        mutated_individual[i],
                        problem.lower_bounds[i],
                        problem.upper_bounds[i]
                    )
            
            mutated.append(mutated_individual)
        
        return mutated
    
    def _elitism(self, population: List[np.ndarray], fitness_scores: np.ndarray) -> Tuple[List[np.ndarray], np.ndarray]:
        """精英保留"""
        # 排序
        sorted_indices = np.argsort(fitness_scores)
        
        # 选择精英
        elite_count = int(self.config.elite_ratio * self.config.population_size)
        elite_indices = sorted_indices[:elite_count]
        
        # 选择其余个体
        remaining_count = self.config.population_size - elite_count
        remaining_indices = sorted_indices[elite_count:elite_count + remaining_count]
        
        # 构建新种群
        new_population = []
        new_fitness_scores = []
        
        for idx in elite_indices:
            new_population.append(population[idx])
            new_fitness_scores.append(fitness_scores[idx])
        
        for idx in remaining_indices:
            new_population.append(population[idx])
            new_fitness_scores.append(fitness_scores[idx])
        
        return new_population, np.array(new_fitness_scores)

class ParticleSwarmOptimizer(BaseOptimizer):
    """粒子群优化算法"""
    
    def __init__(self, config: OptimizationConfig):
        super().__init__(config)
        
        if config.algorithm != OptimizationAlgorithm.PARTICLE_SWARM:
            raise ValueError(f"算法不匹配: {config.algorithm}")
    
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        """执行粒子群优化"""
        self._initialize_optimization(problem)
        
        # 初始化粒子
        positions = self._initialize_particles(problem)
        velocities = np.zeros_like(positions)
        
        # 个体最佳
        personal_best_positions = positions.copy()
        personal_best_scores = np.array([problem.evaluate(pos) for pos in positions])
        
        # 全局最佳
        global_best_idx = np.argmin(personal_best_scores)
        global_best_position = personal_best_positions[global_best_idx].copy()
        global_best_score = personal_best_scores[global_best_idx]
        
        if self.enable_logging:
            self.logger.info(f"粒子群初始化完成，初始全局最佳: {global_best_score}")
        
        try:
            while True:
                # 更新粒子速度和位置
                for i in range(len(positions)):
                    # 更新速度
                    r1, r2 = np.random.random(2)
                    
                    velocities[i] = (self.config.inertia_weight * velocities[i] +
                                   self.config.cognitive_factor * r1 * (personal_best_positions[i] - positions[i]) +
                                   self.config.social_factor * r2 * (global_best_position - positions[i]))
                    
                    # 限制速度
                    max_velocity = 0.2 * (problem.upper_bounds - problem.lower_bounds)
                    velocities[i] = np.clip(velocities[i], -max_velocity, max_velocity)
                    
                    # 更新位置
                    positions[i] += velocities[i]
                    
                    # 边界检查
                    positions[i] = np.clip(positions[i], problem.lower_bounds, problem.upper_bounds)
                
                # 评估新位置
                current_scores = np.array([problem.evaluate(pos) for pos in positions])
                
                # 更新个体最佳
                for i in range(len(positions)):
                    if current_scores[i] < personal_best_scores[i]:
                        personal_best_scores[i] = current_scores[i]
                        personal_best_positions[i] = positions[i].copy()
                
                # 更新全局最佳
                global_best_idx = np.argmin(personal_best_scores)
                if personal_best_scores[global_best_idx] < global_best_score:
                    global_best_score = personal_best_scores[global_best_idx]
                    global_best_position = personal_best_positions[global_best_idx].copy()
                
                # 更新最佳解
                if global_best_score < self.best_fitness:
                    self.best_fitness = global_best_score
                    self.best_solution = global_best_position.copy()
                
                self.current_iteration += 1
                
                if self.enable_logging and self.current_iteration % 100 == 0:
                    self.logger.info(f"迭代 {self.current_iteration}: 全局最佳 = {global_best_score}")
                
                if self._check_convergence(global_best_score):
                    break
            
            return self._create_result(OptimizationStatus.CONVERGED, "粒子群优化收敛")
            
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"粒子群优化失败: {str(e)}")
            return self._create_result(OptimizationStatus.FAILED, str(e))
    
    def _initialize_particles(self, problem: OptimizationProblem) -> np.ndarray:
        """初始化粒子位置"""
        particles = np.random.uniform(
            problem.lower_bounds,
            problem.upper_bounds,
            (self.config.population_size, problem.dimension)
        )
        return particles

class NumericalOptimizer:
    """数值优化器主类"""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        self.config = config or OptimizationConfig(algorithm=OptimizationAlgorithm.GRADIENT_DESCENT)
        self.optimizers = {
            OptimizationAlgorithm.GRADIENT_DESCENT: GradientDescentOptimizer,
            OptimizationAlgorithm.GENETIC_ALGORITHM: GeneticAlgorithmOptimizer,
            OptimizationAlgorithm.PARTICLE_SWARM: ParticleSwarmOptimizer,
        }
        
        self.enable_logging = True
        if self.enable_logging:
            self.logger = logging.getLogger(__name__)
    
    def optimize(self, 
                problem: OptimizationProblem,
                algorithm: Optional[OptimizationAlgorithm] = None) -> OptimizationResult:
        """
        执行优化
        
        Args:
            problem: 优化问题
            algorithm: 优化算法
            
        Returns:
            优化结果
        """
        algorithm = algorithm or self.config.algorithm
        
        if algorithm not in self.optimizers:
            raise ValueError(f"不支持的算法: {algorithm}")
        
        optimizer_class = self.optimizers[algorithm]
        
        # 创建配置
        config = OptimizationConfig(
            algorithm=algorithm,
            max_iterations=self.config.max_iterations,
            tolerance=self.config.tolerance,
            step_size=self.config.step_size,
            learning_rate=self.config.learning_rate,
            population_size=self.config.population_size,
            mutation_rate=self.config.mutation_rate,
            crossover_rate=self.config.crossover_rate,
            elite_ratio=self.config.elite_ratio,
            random_seed=self.config.random_seed
        )
        
        # 特殊参数处理
        if algorithm == OptimizationAlgorithm.PARTICLE_SWARM:
            config.inertia_weight = 0.7
            config.cognitive_factor = 1.5
            config.social_factor = 1.5
        
        optimizer = optimizer_class(config)
        
        if self.enable_logging:
            self.logger.info(f"使用算法: {algorithm.value}")
        
        return optimizer.optimize(problem)
    
    def multi_objective_optimize(self, 
                               problem: OptimizationProblem,
                               algorithm: Optional[OptimizationAlgorithm] = None) -> MultiObjectiveResult:
        """
        多目标优化
        
        Args:
            problem: 优化问题
            algorithm: 优化算法
            
        Returns:
            多目标优化结果
        """
        if algorithm is None:
            algorithm = OptimizationAlgorithm.NSGA2
        
        if algorithm not in [OptimizationAlgorithm.NSGA2, OptimizationAlgorithm.SPEA2]:
            raise ValueError(f"不支持的算法: {algorithm}")
        
        # 初始化结果
        result = MultiObjectiveResult(
            algorithm=algorithm,
            num_objectives=self.config.num_objectives
        )
        
        start_time = time.time()
        
        try:
            if algorithm == OptimizationAlgorithm.NSGA2:
                self._nsga2_optimize(problem, result)
            elif algorithm == OptimizationAlgorithm.SPEA2:
                self._spea2_optimize(problem, result)
        except Exception as e:
            result.status = OptimizationStatus.FAILED
            if self.enable_logging:
                self.logger.error(f"多目标优化失败: {e}")
        
        result.execution_time = time.time() - start_time
        return result
    
    def _nsga2_optimize(self, problem: OptimizationProblem, result: MultiObjectiveResult):
        """NSGA-II算法实现"""
        population_size = self.config.population_size
        max_iterations = self.config.max_iterations
        
        # 初始化种群
        population = self._initialize_population(problem, population_size)
        
        for iteration in range(max_iterations):
            # 评估种群
            fitness = self._evaluate_population(problem, population)
            
            # 非支配排序和拥挤度计算
            fronts = self._non_dominated_sort(fitness)
            crowding_distances = self._calculate_crowding_distance(fitness, fronts)
            
            # 选择父代
            parents = self._tournament_selection(population, fitness, fronts, crowding_distances)
            
            # 交叉和变异
            offspring = self._crossover_and_mutation(parents, problem)
            
            # 合并父代和子代
            combined_population = np.vstack([population, offspring])
            combined_fitness = self._evaluate_population(problem, combined_population)
            
            # 环境选择
            population = self._environmental_selection(
                combined_population, combined_fitness, population_size
            )
            
            # 记录收敛历史
            if iteration % 10 == 0:
                current_pareto = self._extract_pareto_front(population, fitness)
                result.convergence_history.append(current_pareto.tolist())
            
            # 检查收敛
            if self._check_multi_objective_convergence(result.convergence_history):
                break
        
        # 提取帕累托前沿
        final_fitness = self._evaluate_population(problem, population)
        pareto_front = self._extract_pareto_front(population, final_fitness)
        
        result.pareto_front = pareto_front
        result.pareto_solutions = population.tolist()
        result.iterations = iteration + 1
        result.status = OptimizationStatus.CONVERGED
    
    def _spea2_optimize(self, problem: OptimizationProblem, result: MultiObjectiveResult):
        """SPEA2算法实现"""
        population_size = self.config.population_size
        archive_size = population_size // 2
        max_iterations = self.config.max_iterations
        
        # 初始化种群和档案
        population = self._initialize_population(problem, population_size)
        archive = np.empty((0, problem.dimension))
        
        for iteration in range(max_iterations):
            # 评估种群
            fitness = self._evaluate_population(problem, population)
            
            # 计算适应度值
            strengths = self._calculate_strengths(fitness)
            raw_fitness = self._calculate_raw_fitness(fitness, strengths)
            density = self._calculate_density(fitness)
            
            # 环境选择
            archive = self._environmental_selection_spea2(
                population, fitness, raw_fitness, density, archive_size
            )
            
            # 选择父代
            parents = self._selection_spea2(archive, population_size)
            
            # 交叉和变异
            population = self._crossover_and_mutation(parents, problem)
            
            # 记录收敛历史
            if iteration % 10 == 0:
                current_pareto = self._extract_pareto_front(archive, fitness)
                result.convergence_history.append(current_pareto.tolist())
            
            # 检查收敛
            if self._check_multi_objective_convergence(result.convergence_history):
                break
        
        # 提取帕累托前沿
        final_fitness = self._evaluate_population(problem, archive)
        pareto_front = self._extract_pareto_front(archive, final_fitness)
        
        result.pareto_front = pareto_front
        result.pareto_solutions = archive.tolist()
        result.iterations = iteration + 1
        result.status = OptimizationStatus.CONVERGED
    
    def _initialize_population(self, problem: OptimizationProblem, size: int) -> np.ndarray:
        """初始化种群"""
        population = np.random.uniform(
            problem.lower_bounds,
            problem.upper_bounds,
            (size, problem.dimension)
        )
        return population
    
    def _evaluate_population(self, problem: OptimizationProblem, population: np.ndarray) -> np.ndarray:
        """评估种群"""
        fitness = []
        for individual in population:
            if problem.bounds_check(individual):
                fitness.append(problem.evaluate(individual))
            else:
                # 违反边界约束的个体给予惩罚
                fitness.append(np.full(self.config.num_objectives, np.inf))
        return np.array(fitness)
    
    def _non_dominated_sort(self, fitness: np.ndarray) -> List[List[int]]:
        """非支配排序"""
        fronts = [[]]
        domination_counts = [0] * len(fitness)
        dominated_solutions = [[] for _ in range(len(fitness))]
        
        for i in range(len(fitness)):
            for j in range(len(fitness)):
                if i == j:
                    continue
                
                if self._dominates(fitness[i], fitness[j]):
                    dominated_solutions[i].append(j)
                elif self._dominates(fitness[j], fitness[i]):
                    domination_counts[i] += 1
            
            if domination_counts[i] == 0:
                fronts[0].append(i)
        
        current_front = 0
        while fronts[current_front]:
            next_front = []
            for i in fronts[current_front]:
                for j in dominated_solutions[i]:
                    domination_counts[j] -= 1
                    if domination_counts[j] == 0:
                        next_front.append(j)
            
            if next_front:
                fronts.append(next_front)
            current_front += 1
        
        return fronts
    
    def _dominates(self, a: np.ndarray, b: np.ndarray) -> bool:
        """检查a是否支配b"""
        return np.all(a <= b) and np.any(a < b)
    
    def _calculate_crowding_distance(self, fitness: np.ndarray, fronts: List[List[int]]) -> np.ndarray:
        """计算拥挤度"""
        crowding_distances = np.zeros(len(fitness))
        
        for front in fronts:
            if not front:
                continue
            
            front_fitness = fitness[front]
            for obj_idx in range(front_fitness.shape[1]):
                sorted_indices = np.argsort(front_fitness[:, obj_idx])
                crowding_distances[front[sorted_indices[0]]] = np.inf
                crowding_distances[front[sorted_indices[-1]]] = np.inf
                
                for i in range(1, len(sorted_indices) - 1):
                    idx = front[sorted_indices[i]]
                    crowding_distances[idx] += (
                        front_fitness[sorted_indices[i + 1], obj_idx] - 
                        front_fitness[sorted_indices[i - 1], obj_idx]
                    )
        
        return crowding_distances
    
    def _tournament_selection(self, population: np.ndarray, fitness: np.ndarray, 
                            fronts: List[List[int]], crowding_distances: np.ndarray) -> np.ndarray:
        """锦标赛选择"""
        parents = []
        tournament_size = 2
        
        for _ in range(len(population)):
            candidates = np.random.choice(len(population), tournament_size, replace=False)
            
            # 比较候选个体
            best_candidate = candidates[0]
            for candidate in candidates[1:]:
                if self._compare_individuals(
                    best_candidate, candidate, fronts, crowding_distances
                ):
                    best_candidate = candidate
            
            parents.append(population[best_candidate])
        
        return np.array(parents)
    
    def _compare_individuals(self, idx1: int, idx2: int, fronts: List[List[int]], 
                           crowding_distances: np.ndarray) -> bool:
        """比较两个个体"""
        # 找到个体所在的层级
        front1 = self._find_front(idx1, fronts)
        front2 = self._find_front(idx2, fronts)
        
        if front1 < front2:
            return False  # idx1更好
        elif front1 > front2:
            return True   # idx2更好
        else:
            # 同一层级，比较拥挤度
            return crowding_distances[idx1] < crowding_distances[idx2]
    
    def _find_front(self, idx: int, fronts: List[List[int]]) -> int:
        """找到个体所在的层级"""
        for front_idx, front in enumerate(fronts):
            if idx in front:
                return front_idx
        return len(fronts)
    
    def _crossover_and_mutation(self, parents: np.ndarray, problem: OptimizationProblem) -> np.ndarray:
        """交叉和变异"""
        offspring = []
        
        for i in range(0, len(parents), 2):
            if i + 1 >= len(parents):
                break
            
            parent1 = parents[i]
            parent2 = parents[i + 1]
            
            # 模拟二进制交叉
            child1, child2 = self._simulated_binary_crossover(parent1, parent2)
            
            # 多项式变异
            child1 = self._polynomial_mutation(child1, problem)
            child2 = self._polynomial_mutation(child2, problem)
            
            offspring.extend([child1, child2])
        
        return np.array(offspring)
    
    def _simulated_binary_crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """模拟二进制交叉"""
        eta_c = 20  # 分布指数
        child1 = np.copy(parent1)
        child2 = np.copy(parent2)
        
        for i in range(len(parent1)):
            if np.random.random() < self.config.crossover_rate:
                u = np.random.random()
                if u <= 0.5:
                    beta = (2 * u) ** (1 / (eta_c + 1))
                else:
                    beta = (1 / (2 * (1 - u))) ** (1 / (eta_c + 1))
                
                child1[i] = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
                child2[i] = 0.5 * ((1 - beta) * parent1[i] + (1 + beta) * parent2[i])
        
        return child1, child2
    
    def _polynomial_mutation(self, individual: np.ndarray, problem: OptimizationProblem) -> np.ndarray:
        """多项式变异"""
        eta_m = 20  # 分布指数
        mutated = np.copy(individual)
        
        for i in range(len(individual)):
            if np.random.random() < self.config.mutation_rate:
                u = np.random.random()
                if u < 0.5:
                    delta = (2 * u) ** (1 / (eta_m + 1)) - 1
                else:
                    delta = 1 - (2 * (1 - u)) ** (1 / (eta_m + 1))
                
                mutated[i] += delta * (problem.upper_bounds[i] - problem.lower_bounds[i])
                # 边界检查
                mutated[i] = np.clip(mutated[i], problem.lower_bounds[i], problem.upper_bounds[i])
        
        return mutated
    
    def _environmental_selection(self, population: np.ndarray, fitness: np.ndarray, 
                               target_size: int) -> np.ndarray:
        """环境选择"""
        fronts = self._non_dominated_sort(fitness)
        selected = []
        
        for front in fronts:
            if len(selected) + len(front) <= target_size:
                selected.extend(front)
            else:
                # 需要部分选择
                front_fitness = fitness[front]
                crowding_distances = self._calculate_crowding_distance(fitness, [front])
                
                # 按拥挤度排序
                sorted_indices = np.argsort(crowding_distances[front])[::-1]
                remaining = target_size - len(selected)
                selected.extend([front[i] for i in sorted_indices[:remaining]])
                break
        
        return population[selected]
    
    def _extract_pareto_front(self, population: np.ndarray, fitness: np.ndarray) -> np.ndarray:
        """提取帕累托前沿"""
        pareto_indices = []
        
        for i in range(len(fitness)):
            is_pareto = True
            for j in range(len(fitness)):
                if i == j:
                    continue
                if self._dominates(fitness[j], fitness[i]):
                    is_pareto = False
                    break
            
            if is_pareto:
                pareto_indices.append(i)
        
        return fitness[pareto_indices]
    
    def _calculate_strengths(self, fitness: np.ndarray) -> np.ndarray:
        """计算强度值（SPEA2）"""
        strengths = np.zeros(len(fitness))
        
        for i in range(len(fitness)):
            for j in range(len(fitness)):
                if i == j:
                    continue
                if self._dominates(fitness[i], fitness[j]):
                    strengths[i] += 1
        
        return strengths
    
    def _calculate_raw_fitness(self, fitness: np.ndarray, strengths: np.ndarray) -> np.ndarray:
        """计算原始适应度（SPEA2）"""
        raw_fitness = np.zeros(len(fitness))
        
        for i in range(len(fitness)):
            for j in range(len(fitness)):
                if i == j:
                    continue
                if self._dominates(fitness[j], fitness[i]):
                    raw_fitness[i] += strengths[j]
        
        return raw_fitness
    
    def _calculate_density(self, fitness: np.ndarray) -> np.ndarray:
        """计算密度（SPEA2）"""
        k = int(np.sqrt(len(fitness)))
        distances = np.zeros((len(fitness), len(fitness)))
        
        # 计算欧几里得距离
        for i in range(len(fitness)):
            for j in range(len(fitness)):
                if i != j:
                    distances[i, j] = np.linalg.norm(fitness[i] - fitness[j])
        
        # 对每个个体，找到第k个最近邻的距离
        densities = np.zeros(len(fitness))
        for i in range(len(fitness)):
            sorted_distances = np.sort(distances[i])
            kth_distance = sorted_distances[k]
            densities[i] = 1.0 / (kth_distance + 2.0)  # 避免除零
        
        return densities
    
    def _environmental_selection_spea2(self, population: np.ndarray, fitness: np.ndarray,
                                     raw_fitness: np.ndarray, density: np.ndarray,
                                     archive_size: int) -> np.ndarray:
        """SPEA2环境选择"""
        # 计算总适应度
        total_fitness = raw_fitness + density
        
        # 选择非支配解
        pareto_indices = []
        for i in range(len(fitness)):
            is_pareto = True
            for j in range(len(fitness)):
                if i == j:
                    continue
                if self._dominates(fitness[j], fitness[i]):
                    is_pareto = False
                    break
            
            if is_pareto:
                pareto_indices.append(i)
        
        # 如果非支配解数量小于等于档案大小，全部选择
        if len(pareto_indices) <= archive_size:
            # 还需要添加一些支配解来填满档案
            remaining = archive_size - len(pareto_indices)
            if remaining > 0:
                # 选择总适应度最好的支配解
                dominated_indices = [i for i in range(len(fitness)) if i not in pareto_indices]
                dominated_fitness = total_fitness[dominated_indices]
                best_dominated = np.argsort(dominated_fitness)[:remaining]
                selected_indices = pareto_indices + [dominated_indices[i] for i in best_dominated]
            else:
                selected_indices = pareto_indices
        else:
            # 非支配解过多，需要截断
            # 使用聚类方法选择代表性解
            selected_indices = self._truncate_by_clustering(
                population[pareto_indices], fitness[pareto_indices], archive_size
            )
            selected_indices = [pareto_indices[i] for i in selected_indices]
        
        return population[selected_indices]
    
    def _selection_spea2(self, archive: np.ndarray, population_size: int) -> np.ndarray:
        """SPEA2选择操作"""
        if len(archive) == 0:
            return np.empty((0, archive.shape[1]))
        
        # 如果档案大小小于种群大小，需要重复选择
        if len(archive) < population_size:
            indices = np.random.choice(len(archive), population_size, replace=True)
        else:
            indices = np.random.choice(len(archive), population_size, replace=False)
        
        return archive[indices]
    
    def _truncate_by_clustering(self, population: np.ndarray, fitness: np.ndarray, 
                               target_size: int) -> List[int]:
        """通过聚类截断解集"""
        if len(population) <= target_size:
            return list(range(len(population)))
        
        # 简单的距离聚类
        selected_indices = list(range(len(population)))
        
        while len(selected_indices) > target_size:
            # 找到距离最近的两个解
            min_distance = np.inf
            to_remove = -1
            
            for i in range(len(selected_indices)):
                for j in range(i + 1, len(selected_indices)):
                    idx1, idx2 = selected_indices[i], selected_indices[j]
                    distance = np.linalg.norm(fitness[idx1] - fitness[idx2])
                    if distance < min_distance:
                        min_distance = distance
                        # 移除拥挤度较小的解
                        crowding1 = self._calculate_crowding_distance(
                            fitness[selected_indices], [[i]]
                        )[i]
                        crowding2 = self._calculate_crowding_distance(
                            fitness[selected_indices], [[j]]
                        )[j]
                        
                        if crowding1 < crowding2:
                            to_remove = i
                        else:
                            to_remove = j
            
            if to_remove != -1:
                selected_indices.pop(to_remove)
        
        return selected_indices
    
    def _check_multi_objective_convergence(self, convergence_history: List[List[List[float]]]) -> bool:
        """检查多目标优化收敛"""
        if len(convergence_history) < 3:
            return False
        
        # 检查最近几次迭代的帕累托前沿变化
        recent_fronts = convergence_history[-3:]
        
        # 计算前沿之间的平均距离
        distances = []
        for i in range(len(recent_fronts) - 1):
            front1 = np.array(recent_fronts[i])
            front2 = np.array(recent_fronts[i + 1])
            
            # 计算两个前沿之间的Hausdorff距离
            distance = self._hausdorff_distance(front1, front2)
            distances.append(distance)
        
        # 如果距离变化很小，认为收敛
        if len(distances) >= 2:
            avg_distance = np.mean(distances)
            if avg_distance < 1e-6:
                return True
        
        return False
    
    def _hausdorff_distance(self, set1: np.ndarray, set2: np.ndarray) -> float:
        """计算两个集合之间的Hausdorff距离"""
        if len(set1) == 0 or len(set2) == 0:
            return np.inf
        
        # 计算从set1到set2的距离
        dist1 = []
        for point1 in set1:
            min_dist = np.inf
            for point2 in set2:
                dist = np.linalg.norm(point1 - point2)
                if dist < min_dist:
                    min_dist = dist
            dist1.append(min_dist)
        
        # 计算从set2到set1的距离
        dist2 = []
        for point2 in set2:
            min_dist = np.inf
            for point1 in set1:
                dist = np.linalg.norm(point2 - point1)
                if dist < min_dist:
                    min_dist = dist
            dist2.append(min_dist)
        
        # Hausdorff距离是两个方向最大距离的最大值
        return max(np.max(dist1), np.max(dist2))

# 便捷函数
def create_optimizer(algorithm: OptimizationAlgorithm,
                    **kwargs) -> NumericalOptimizer:
    """创建优化器"""
    config = OptimizationConfig(algorithm=algorithm, **kwargs)
    return NumericalOptimizer(config)

def minimize(objective_func: Callable,
           bounds: List[Tuple[float, float]],
           algorithm: OptimizationAlgorithm = OptimizationAlgorithm.GRADIENT_DESCENT,
           **kwargs) -> OptimizationResult:
    """
    最小化目标函数
    
    Args:
        objective_func: 目标函数
        bounds: 变量边界
        algorithm: 优化算法
        **kwargs: 其他参数
        
    Returns:
        优化结果
    """
    from functools import partial
    
    class SimpleProblem(OptimizationProblem):
        def evaluate(self, x):
            return objective_func(x)
        
        def gradient(self, x):
            return None
    
    problem = SimpleProblem(len(bounds))
    problem.lower_bounds = np.array([b[0] for b in bounds])
    problem.upper_bounds = np.array([b[1] for b in bounds])
    
    optimizer = create_optimizer(algorithm, **kwargs)
    return optimizer.optimize(problem)