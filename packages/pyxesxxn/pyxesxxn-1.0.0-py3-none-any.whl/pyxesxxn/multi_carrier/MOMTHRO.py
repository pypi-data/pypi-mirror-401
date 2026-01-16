"""
MOMTHRO (Multi-Objective Modified Tianji Horse Racing Optimization) Algorithm

This module implements the MOMTHRO algorithm for multi-objective optimization problems.
The algorithm is based on the Tianji Horse Racing strategy with non-dominated sorting
and crowding distance calculation for maintaining diversity in Pareto fronts.

Key Features:
- Non-dominated sorting and crowding distance calculation
- Adaptive parameter control for exploration and exploitation
- Levy flight for global search capability
- Hypervolume-based performance metrics
- Diversity preservation mechanisms
"""

from __future__ import annotations
from typing import Callable, Tuple, List, Optional, Dict, Any
import numpy as np
from scipy.special import gamma
from scipy.spatial.distance import cdist
from scipy.optimize import minimize
from scipy.stats import norm
import warnings
import random
import time
from collections import deque
from itertools import combinations
import logging

# Import qmc conditionally
try:
    from scipy.stats import qmc
    QMC_AVAILABLE = True
except ImportError:
    qmc = None
    QMC_AVAILABLE = False


class MOMTHROOptimizer:
    """Multi-Objective Modified Tianji Horse Racing Optimization Algorithm."""
    
    def __init__(
        self,
        population_size: int = 100,
        max_iterations: int = 200,
        mutation_rate: float = 0.1,
        alpha: float = 1.0,
        beta: float = 0.5
    ):
        """Initialize the MOMTHRO optimizer.
        
        Parameters
        ----------
        population_size : int, default=100
            Total population size (divided equally between Tianji and King populations)
        max_iterations : int, default=200
            Maximum number of iterations
        mutation_rate : float, default=0.1
            Mutation rate for diversity preservation
        alpha : float, default=1.0
            Exploration parameter
        beta : float, default=0.5
            Exploitation parameter
        """
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.mutation_rate = mutation_rate
        self.alpha = alpha
        self.beta = beta
        
        # Optimization history
        self.history: List[Dict[str, Any]] = []
        self.pareto_front: Optional[np.ndarray] = None
        self.pareto_set: Optional[np.ndarray] = None
        
    def optimize(
        self,
        objective_function: Callable,
        lower_bounds: np.ndarray,
        upper_bounds: np.ndarray,
        dimension: int,
        num_objectives: int = 2
    ) -> Tuple[np.ndarray, np.ndarray, List[float]]:
        """Execute the MOMTHRO optimization algorithm.
        
        Parameters
        ----------
        objective_function : Callable
            Multi-objective function to minimize
        lower_bounds : np.ndarray
            Lower bounds for each dimension
        upper_bounds : np.ndarray
            Upper bounds for each dimension
        dimension : int
            Problem dimension
        num_objectives : int, default=2
            Number of objective functions
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray, List[float]]
            Pareto front, Pareto set, and hypervolume history
        """
        # Validate inputs
        self._validate_inputs(lower_bounds, upper_bounds, dimension, num_objectives)
        
        # Initialize populations
        n_pop = max(2, self.population_size // 2)
        
        # Initialize Tianji and King populations using Latin Hypercube Sampling
        tianji_pop = self._lhs_design_modified(n_pop, lower_bounds, upper_bounds)
        king_pop = self._lhs_design_modified(n_pop, lower_bounds, upper_bounds)
        
        # Evaluate initial populations
        tianji_fitness = np.array([objective_function(ind) for ind in tianji_pop])
        king_fitness = np.array([objective_function(ind) for ind in king_pop])
        
        # Initialize Pareto front
        all_positions = np.vstack([tianji_pop, king_pop])
        all_fitness = np.vstack([tianji_fitness, king_fitness])
        
        self.pareto_front, self.pareto_set = self._find_pareto_front(all_fitness, all_positions)
        best_hypervolume = self._calculate_hypervolume(self.pareto_front)
        
        hypervolume_history = [best_hypervolume]
        
        # Adaptive parameters
        adaptive_params = {'alpha': self.alpha, 'beta': self.beta}
        
        print(f"Starting MOMTHRO optimization: Population={self.population_size}, "
              f"Iterations={self.max_iterations}, Dimension={dimension}")
        
        for iteration in range(self.max_iterations):
            # Check diversity status for adaptive parameter control
            diversity_status = self._check_diversity_loss(tianji_pop, king_pop, lower_bounds, upper_bounds)
            
            # Update adaptive parameters with enhanced multi-dimensional feedback
            adaptive_params = self._update_adaptive_params(
                adaptive_params, iteration, self.max_iterations, 
                hypervolume_history, len(self.pareto_set), diversity_status
            )
            
            # Random reassignment for diversity
            tianji_pop, tianji_fitness, king_pop, king_fitness = self._random_reassignment(
                tianji_pop, tianji_fitness, king_pop, king_fitness
            )
            
            # Non-dominated sorting
            tianji_ranks, tianji_crowding = self._non_dominated_sort(tianji_fitness)
            king_ranks, king_crowding = self._non_dominated_sort(king_fitness)
            
            # Sort populations based on Pareto rank and crowding distance
            tianji_pop, tianji_fitness = self._sort_by_rank_and_crowding(
                tianji_pop, tianji_fitness, tianji_ranks, tianji_crowding
            )
            king_pop, king_fitness = self._sort_by_rank_and_crowding(
                king_pop, king_fitness, king_ranks, king_crowding
            )
            
            # Tianji Horse Racing strategy
            for i in range(n_pop):
                if self._dominates(tianji_fitness[i], king_fitness[i]):
                    # Tianji dominates King
                    tianji_pop, tianji_fitness = self._update_solution_improved(
                        tianji_pop, tianji_fitness, i, tianji_pop[0],
                        king_pop, upper_bounds, lower_bounds, objective_function,
                        iteration, self.max_iterations, adaptive_params
                    )
                elif self._dominates(king_fitness[i], tianji_fitness[i]):
                    # King dominates Tianji
                    king_pop, king_fitness = self._update_solution_improved(
                        king_pop, king_fitness, i, king_pop[0],
                        tianji_pop, upper_bounds, lower_bounds, objective_function,
                        iteration, self.max_iterations, adaptive_params
                    )
                else:
                    # Non-dominated - use crowding distance
                    if tianji_crowding[i] > king_crowding[i]:
                        tianji_pop, tianji_fitness = self._update_solution_improved(
                            tianji_pop, tianji_fitness, i, tianji_pop[0],
                            king_pop, upper_bounds, lower_bounds, objective_function,
                            iteration, self.max_iterations, adaptive_params
                        )
                    else:
                        king_pop, king_fitness = self._update_solution_improved(
                            king_pop, king_fitness, i, king_pop[0],
                            tianji_pop, upper_bounds, lower_bounds, objective_function,
                            iteration, self.max_iterations, adaptive_params
                        )
            
            # Enhanced adaptive mutation for diversity maintenance
            current_mutation_rate = self._calculate_adaptive_mutation_rate(
                iteration, self.max_iterations, hypervolume_history, len(self.pareto_set)
            )
            
            # Apply mutation with adaptive frequency
            mutation_frequency = self._calculate_mutation_frequency(iteration, self.max_iterations, hypervolume_history)
            if iteration % mutation_frequency == 0:
                tianji_pop = self._apply_enhanced_mutation(tianji_pop, lower_bounds, upper_bounds, current_mutation_rate, iteration)
                king_pop = self._apply_enhanced_mutation(king_pop, lower_bounds, upper_bounds, current_mutation_rate, iteration)
                
                # Re-evaluate fitness
                tianji_fitness = np.array([objective_function(ind) for ind in tianji_pop])
                king_fitness = np.array([objective_function(ind) for ind in king_pop])
            
            # Diversity maintenance: inject new solutions if diversity is low
            if iteration % 20 == 0 and diversity_status['diversity_low']:
                tianji_pop, king_pop = self._inject_diversity(tianji_pop, king_pop, lower_bounds, upper_bounds, diversity_status)
                tianji_fitness = np.array([objective_function(ind) for ind in tianji_pop])
                king_fitness = np.array([objective_function(ind) for ind in king_pop])
            
            # Update Pareto front
            all_positions = np.vstack([tianji_pop, king_pop])
            all_fitness = np.vstack([tianji_fitness, king_fitness])
            
            # Merge with historical Pareto front
            if self.pareto_set is not None and len(self.pareto_set) > 0:
                all_positions = np.vstack([all_positions, self.pareto_set])
                all_fitness = np.vstack([all_fitness, self.pareto_front])
            
            new_pareto_front, new_pareto_set = self._find_pareto_front(all_fitness, all_positions)
            
            # Convergence detection and restart mechanism
            if iteration > 50 and iteration % 10 == 0:
                convergence_status = self._check_convergence(hypervolume_history, iteration, 
                                                           pareto_size=len(self.pareto_set))
                if convergence_status['stagnant']:
                    print(f"Iteration {iteration}: Convergence stagnation detected. Applying restart mechanism...")
                    
                    # Apply restart mechanism
                    if convergence_status['severity'] == 'mild':
                        # Mild stagnation: inject diversity
                        diversity_status = self._check_diversity_loss(tianji_pop, king_pop, lower_bounds, upper_bounds)
                        tianji_pop, king_pop = self._inject_diversity(tianji_pop, king_pop, lower_bounds, upper_bounds, diversity_status)
                        tianji_fitness = np.array([objective_function(ind) for ind in tianji_pop])
                        king_fitness = np.array([objective_function(ind) for ind in king_pop])
                    elif convergence_status['severity'] == 'moderate':
                        # Moderate stagnation: partial restart
                        tianji_pop, king_pop = self._partial_restart(tianji_pop, king_pop, lower_bounds, upper_bounds, n_pop)
                        tianji_fitness = np.array([objective_function(ind) for ind in tianji_pop])
                        king_fitness = np.array([objective_function(ind) for ind in king_pop])
                    else:
                        # Severe stagnation: full restart
                        tianji_pop, king_pop = self._full_restart(lower_bounds, upper_bounds, n_pop)
                        tianji_fitness = np.array([objective_function(ind) for ind in tianji_pop])
                        king_fitness = np.array([objective_function(ind) for ind in king_pop])
                        
                    # Recalculate Pareto front after restart
                    all_positions = np.vstack([tianji_pop, king_pop])
                    all_fitness = np.vstack([tianji_fitness, king_fitness])
                    if self.pareto_set is not None and len(self.pareto_set) > 0:
                        all_positions = np.vstack([all_positions, self.pareto_set])
                        all_fitness = np.vstack([all_fitness, self.pareto_front])
                    new_pareto_front, new_pareto_set = self._find_pareto_front(all_fitness, all_positions)
            
            # Maintain Pareto front size
            if len(new_pareto_set) > n_pop:
                new_pareto_front, new_pareto_set = self._select_diverse_solutions(
                    new_pareto_front, new_pareto_set, n_pop
                )
            
            self.pareto_front = new_pareto_front
            self.pareto_set = new_pareto_set
            
            # Calculate hypervolume
            current_hypervolume = self._calculate_hypervolume(self.pareto_front)
            if current_hypervolume > best_hypervolume:
                best_hypervolume = current_hypervolume
            
            # Record current hypervolume for convergence detection
            hypervolume_history.append(current_hypervolume)
            
            # Progress reporting
            if iteration % max(1, self.max_iterations // 10) == 0 or iteration in [0, self.max_iterations - 1]:
                print(f"Iteration {iteration + 1}/{self.max_iterations}, "
                      f"Hypervolume = {best_hypervolume:.6f}, "
                      f"Pareto solutions = {len(self.pareto_set)}")
            
            # Store iteration history
            self.history.append({
                'iteration': iteration,
                'hypervolume': best_hypervolume,
                'pareto_size': len(self.pareto_set),
                'adaptive_alpha': adaptive_params['alpha'],
                'adaptive_beta': adaptive_params['beta']
            })
        
        print(f"Optimization completed. Final Pareto solutions: {len(self.pareto_set)}, "
              f"Final hypervolume: {best_hypervolume:.6f}")
        
        return self.pareto_front, self.pareto_set, hypervolume_history
    
    def _validate_inputs(self, lower_bounds: np.ndarray, upper_bounds: np.ndarray, 
                        dimension: int, num_objectives: int) -> None:
        """Validate input parameters."""
        if len(lower_bounds) != dimension:
            raise ValueError(f"Lower bounds dimension ({len(lower_bounds)}) "
                           f"does not match problem dimension ({dimension})")
        
        if len(upper_bounds) != dimension:
            raise ValueError(f"Upper bounds dimension ({len(upper_bounds)}) "
                           f"does not match problem dimension ({dimension})")
        
        if np.any(lower_bounds >= upper_bounds):
            raise ValueError("Lower bounds must be strictly less than upper bounds")
        
        if num_objectives < 2:
            raise ValueError("Number of objectives must be at least 2 for multi-objective optimization")
    
    def _lhs_design_modified(self, n: int, lower_bounds: np.ndarray, 
                           upper_bounds: np.ndarray) -> np.ndarray:
        """Intelligent population initialization with enhanced diversity and coverage strategies."""
        dim = len(lower_bounds)
        
        # Adaptive strategy selection based on problem characteristics
        if dim <= 5:
            # Low-dimensional problems: emphasize space-filling
            strategy_ratios = [0.4, 0.3, 0.2, 0.1]  # LHS, Sobol, Random, Halton
        elif dim <= 15:
            # Medium-dimensional problems: balanced approach
            strategy_ratios = [0.35, 0.25, 0.25, 0.15]
        else:
            # High-dimensional problems: emphasize diversity
            strategy_ratios = [0.3, 0.2, 0.3, 0.2]
        
        # Strategy 1: Enhanced Latin Hypercube Sampling
        lhs_samples = self._lhs_enhanced(int(n * strategy_ratios[0]), dim)
        
        # Strategy 2: Sobol sequence with enhanced scrambling
        sobol_samples = self._generate_sobol_sequence_enhanced(int(n * strategy_ratios[1]), dim)
        
        # Strategy 3: Adaptive random sampling with intelligent distribution
        random_samples = self._adaptive_random_sampling(int(n * strategy_ratios[2]), dim, lower_bounds, upper_bounds)
        
        # Strategy 4: Halton sequence for additional diversity
        halton_samples = self._generate_halton_sequence(int(n * strategy_ratios[3]), dim)
        
        # Combine all strategies with intelligent merging
        combined_samples = np.vstack([lhs_samples, sobol_samples, random_samples, halton_samples])
        
        # Ensure exact population size with intelligent sampling
        if len(combined_samples) > n:
            # Select most diverse subset using max-min distance
            combined_samples = self._select_diverse_subset(combined_samples, n)
        elif len(combined_samples) < n:
            # Add intelligent additional samples
            additional_needed = n - len(combined_samples)
            additional_samples = self._generate_intelligent_samples(additional_needed, dim, lower_bounds, upper_bounds, combined_samples)
            combined_samples = np.vstack([combined_samples, additional_samples])
        
        # Intelligent scaling with adaptive boundary emphasis
        population = np.zeros((n, dim))
        for i in range(dim):
            range_size = upper_bounds[i] - lower_bounds[i]
            # Adaptive scaling based on dimension importance
            scale_factor = 1.0 + 0.1 * np.random.randn()
            population[:, i] = lower_bounds[i] + combined_samples[:, i] * range_size * scale_factor
        
        # Enhanced diversity perturbation with multi-scale adaptive scaling
        for i in range(n):
            # Multi-scale perturbation based on solution density
            density_factor = self._calculate_solution_density(population, i, dim)
            
            # Adaptive perturbation scaling
            base_scale = 0.06 * (upper_bounds - lower_bounds)
            adaptive_factor = 1.0 + 0.3 * np.random.randn(dim) * density_factor
            perturbation_scale = base_scale * adaptive_factor
            
            # Multi-modal perturbation (Gaussian + Uniform)
            gaussian_perturbation = perturbation_scale * np.random.randn(dim)
            uniform_perturbation = 0.3 * perturbation_scale * (2 * np.random.random(dim) - 1)
            perturbation = gaussian_perturbation + uniform_perturbation
            
            population[i] += perturbation
            population[i] = np.clip(population[i], lower_bounds, upper_bounds)
        
        # Intelligent boundary emphasis with adaptive coverage
        boundary_coverage = self._calculate_boundary_coverage(population, lower_bounds, upper_bounds)
        
        # Adaptive boundary solution generation
        if boundary_coverage < 0.8:  # If boundary coverage is insufficient
            boundary_indices = np.random.choice(n, int(n * 0.2), replace=False)
            for idx in boundary_indices:
                # Adaptive number of boundary dimensions
                num_boundary_dims = max(1, int(dim * (0.2 + 0.3 * np.random.random())))
                boundary_dims = np.random.choice(dim, num_boundary_dims, replace=False)
                
                for dim_choice in boundary_dims:
                    # Intelligent boundary positioning
                    boundary_type = np.random.choice(['near_lower', 'near_upper', 'corner'], p=[0.4, 0.4, 0.2])
                    
                    if boundary_type == 'near_lower':
                        offset = 0.01 + 0.04 * np.random.random()
                        population[idx, dim_choice] = lower_bounds[dim_choice] + offset * (upper_bounds[dim_choice] - lower_bounds[dim_choice])
                    elif boundary_type == 'near_upper':
                        offset = 0.01 + 0.04 * np.random.random()
                        population[idx, dim_choice] = upper_bounds[dim_choice] - offset * (upper_bounds[dim_choice] - lower_bounds[dim_choice])
                    else:  # corner
                        if np.random.random() < 0.5:
                            population[idx, dim_choice] = lower_bounds[dim_choice]
                        else:
                            population[idx, dim_choice] = upper_bounds[dim_choice]
        
        # Enhanced corner and edge solutions for extreme exploration
        corner_count = min(max(3, n // 15), 8)
        corner_indices = np.random.choice(n, corner_count, replace=False)
        
        for idx in corner_indices:
            # Adaptive corner strategy
            corner_strategy = np.random.choice(['full_corner', 'partial_corner', 'edge'], p=[0.3, 0.4, 0.3])
            
            if corner_strategy == 'full_corner':
                # Full corner solution
                for dim_choice in range(dim):
                    if np.random.random() < 0.5:
                        population[idx, dim_choice] = lower_bounds[dim_choice]
                    else:
                        population[idx, dim_choice] = upper_bounds[dim_choice]
            elif corner_strategy == 'partial_corner':
                # Partial corner (some dimensions at boundaries)
                num_corner_dims = max(1, int(dim * 0.6))
                corner_dims = np.random.choice(dim, num_corner_dims, replace=False)
                for dim_choice in corner_dims:
                    if np.random.random() < 0.5:
                        population[idx, dim_choice] = lower_bounds[dim_choice]
                    else:
                        population[idx, dim_choice] = upper_bounds[dim_choice]
            else:  # edge
                # Edge solution (one dimension at boundary, others random)
                edge_dim = np.random.randint(dim)
                if np.random.random() < 0.5:
                    population[idx, edge_dim] = lower_bounds[edge_dim]
                else:
                    population[idx, edge_dim] = upper_bounds[edge_dim]
        
        # Final diversity enhancement with intelligent mixing
        population = self._enhance_diversity_mixing(population, lower_bounds, upper_bounds)
        
        return population
    
    def _generate_sobol_sequence(self, n_samples: int, dim: int) -> np.ndarray:
        """Generate Sobol sequence for quasi-random sampling."""
        try:
            from scipy.stats import qmc
            sobol = qmc.Sobol(d=dim, scramble=True)
            return sobol.random(n=n_samples)
        except ImportError:
            # Fallback to improved LHS if scipy not available
            return self._lhs_original(n_samples, dim)
    
    def _lhs_original(self, n: int, dim: int) -> np.ndarray:
        """Original Latin Hypercube Sampling implementation."""
        samples = np.zeros((n, dim))
        
        for i in range(dim):
            edges = np.linspace(0, 1, n + 1)
            points = edges[:-1] + np.random.random(n) * (edges[1:] - edges[:-1])
            samples[:, i] = np.random.permutation(points)
        
        return samples
    
    def _lhs_enhanced(self, n: int, dim: int) -> np.ndarray:
        """Enhanced Latin Hypercube Sampling with improved stratification."""
        samples = np.zeros((n, dim))
        
        for i in range(dim):
            # Enhanced stratification with overlapping intervals
            edges = np.linspace(0, 1, n + 1)
            # Add small random overlap for better coverage
            overlap_factor = 0.05 * np.random.random()
            edges = edges * (1 - overlap_factor) + overlap_factor * np.random.random(n + 1)
            
            points = edges[:-1] + np.random.random(n) * (edges[1:] - edges[:-1])
            samples[:, i] = np.random.permutation(points)
        
        return samples
    
    def _generate_sobol_sequence_enhanced(self, n_samples: int, dim: int) -> np.ndarray:
        """Generate enhanced Sobol sequence with multiple scrambling techniques."""
        if QMC_AVAILABLE:
            sobol = qmc.Sobol(d=dim, scramble=True)
            # Generate multiple sequences and select best coverage
            sequences = []
            for _ in range(3):
                seq = sobol.random(n=n_samples)
                sequences.append(seq)
            
            # Select sequence with best space-filling properties
            best_sequence = sequences[0]
            best_discrepancy = float('inf')
            for seq in sequences:
                try:
                    disc = qmc.discrepancy(seq)
                    if disc < best_discrepancy:
                        best_discrepancy = disc
                        best_sequence = seq
                except:
                    continue
            
            return best_sequence
        else:
            # Fallback to enhanced LHS
            return self._lhs_enhanced(n_samples, dim)
    
    def _adaptive_random_sampling(self, n_samples: int, dim: int, 
                                 lower_bounds: np.ndarray, upper_bounds: np.ndarray) -> np.ndarray:
        """Adaptive random sampling with intelligent distribution."""
        samples = np.random.random((n_samples, dim))
        
        # Apply adaptive distribution based on dimension importance
        for i in range(dim):
            range_size = upper_bounds[i] - lower_bounds[i]
            # More samples in regions likely to contain optima
            if range_size > np.mean(upper_bounds - lower_bounds):
                # Wider ranges get more uniform distribution
                pass
            else:
                # Narrower ranges get more concentrated distribution
                samples[:, i] = 0.3 + 0.4 * samples[:, i]
        
        return samples
    
    def _generate_halton_sequence(self, n_samples: int, dim: int) -> np.ndarray:
        """Generate Halton sequence for quasi-random sampling."""
        if QMC_AVAILABLE:
            halton = qmc.Halton(d=dim, scramble=True)
            return halton.random(n=n_samples)
        else:
            # Fallback to random sampling
            return np.random.random((n_samples, dim))
    
    def _select_diverse_subset(self, samples: np.ndarray, n: int) -> np.ndarray:
        """Select most diverse subset using max-min distance criterion."""
        if len(samples) <= n:
            return samples
        
        # Initialize with random sample
        selected_indices = [np.random.randint(len(samples))]
        
        while len(selected_indices) < n:
            # Calculate minimum distance to selected points for each candidate
            min_distances = []
            for i in range(len(samples)):
                if i not in selected_indices:
                    distances = cdist([samples[i]], samples[selected_indices])
                    min_distances.append((i, np.min(distances)))
            
            # Select point with maximum minimum distance
            if min_distances:
                max_dist_idx = max(min_distances, key=lambda x: x[1])[0]
                selected_indices.append(max_dist_idx)
            else:
                break
        
        return samples[selected_indices]
    
    def _generate_intelligent_samples(self, n_needed: int, dim: int, 
                                     lower_bounds: np.ndarray, upper_bounds: np.ndarray,
                                     existing_samples: np.ndarray) -> np.ndarray:
        """Generate intelligent additional samples to fill gaps."""
        if n_needed <= 0:
            return np.array([])
        
        new_samples = []
        
        for _ in range(n_needed):
            # Find region with least coverage
            if len(existing_samples) > 0:
                # Generate candidate in sparse region
                candidate = np.random.random(dim)
                
                # Adjust towards sparse regions
                if len(existing_samples) > 1:
                    distances = cdist([candidate], existing_samples)
                    min_dist = np.min(distances)
                    # Move candidate towards sparse regions
                    if min_dist < 0.3:
                        # Find direction to sparse region
                        sparse_direction = np.random.random(dim) - 0.5
                        sparse_direction = sparse_direction / np.linalg.norm(sparse_direction)
                        candidate = candidate + 0.2 * sparse_direction
                        candidate = np.clip(candidate, 0, 1)
            else:
                candidate = np.random.random(dim)
            
            new_samples.append(candidate)
        
        return np.array(new_samples)
    
    def _calculate_solution_density(self, population: np.ndarray, idx: int, dim: int) -> float:
        """Calculate solution density around a given solution."""
        if len(population) <= 1:
            return 1.0
        
        # Calculate distances to other solutions
        distances = cdist([population[idx]], population)
        distances = distances[distances > 0]  # Exclude self-distance
        
        if len(distances) == 0:
            return 1.0
        
        # Calculate density as inverse of average distance
        avg_distance = np.mean(distances)
        density = 1.0 / (1.0 + avg_distance)
        
        return min(2.0, max(0.5, density))
    
    def _calculate_boundary_coverage(self, population: np.ndarray, 
                                    lower_bounds: np.ndarray, upper_bounds: np.ndarray) -> float:
        """Calculate how well the boundaries are covered by the population."""
        dim = len(lower_bounds)
        boundary_threshold = 0.05  # 5% from boundaries
        
        boundary_coverage = 0
        total_boundary_points = 2 * dim  # Lower and upper boundaries for each dimension
        
        for i in range(dim):
            range_size = upper_bounds[i] - lower_bounds[i]
            lower_threshold = lower_bounds[i] + boundary_threshold * range_size
            upper_threshold = upper_bounds[i] - boundary_threshold * range_size
            
            # Check if any solution is near lower boundary
            if np.any(population[:, i] <= lower_threshold):
                boundary_coverage += 0.5
            
            # Check if any solution is near upper boundary
            if np.any(population[:, i] >= upper_threshold):
                boundary_coverage += 0.5
        
        return boundary_coverage / total_boundary_points
    
    def _enhance_diversity_mixing(self, population: np.ndarray,
                                 lower_bounds: np.ndarray, upper_bounds: np.ndarray) -> np.ndarray:
        """Enhance diversity through intelligent mixing of solutions."""
        n, dim = population.shape
        
        if n <= 1:
            return population
        
        # Apply small random perturbations to enhance diversity
        for i in range(n):
            perturbation_scale = 0.02 * (upper_bounds - lower_bounds)
            perturbation = perturbation_scale * np.random.randn(dim)
            population[i] += perturbation
            population[i] = np.clip(population[i], lower_bounds, upper_bounds)
        
        return population
    
    def _update_adaptive_params(self, params: Dict[str, float], 
                              iteration: int, max_iterations: int,
                              hypervolume_history: List[float] = None,
                              pareto_size: int = None,
                              diversity_status: Dict[str, Any] = None) -> Dict[str, float]:
        """Enhanced intelligent adaptive parameter control with multi-dimensional feedback."""
        progress = iteration / max_iterations
        
        # Multi-dimensional feedback-based parameter adjustment
        
        # 1. Progress-based adjustment (smooth exploration to exploitation transition)
        progress_factor = progress
        
        # 2. Hypervolume improvement-based adjustment (enhanced with multiple time windows)
        improvement_factor = 1.0
        if hypervolume_history and len(hypervolume_history) > 10:
            # Multi-window improvement analysis
            windows = [3, 5, 8, 10, 15]
            window_factors = []
            
            for window_size in windows:
                if len(hypervolume_history) >= window_size:
                    window_improvement = (hypervolume_history[-1] - hypervolume_history[-window_size]) / max(hypervolume_history[-window_size], 1e-10)
                    # Weighted normalization based on window size
                    weight = min(1.0, window_size / 10.0)
                    window_factor = min(2.0, max(0.5, 1.0 + 8 * weight * window_improvement))
                    window_factors.append(window_factor)
            
            if window_factors:
                # Weighted average with more emphasis on recent improvements
                weights = [0.3, 0.25, 0.2, 0.15, 0.1][:len(window_factors)]
                improvement_factor = np.average(window_factors, weights=weights)
        
        # 3. Diversity-based adjustment (new feature)
        diversity_factor = 1.0
        if diversity_status:
            severity = diversity_status.get('severity', 'normal')
            diversity_score = diversity_status.get('score', 1.0)
            
            if severity == 'critical':
                diversity_factor = 1.8  # Strong exploration boost for critical diversity loss
            elif severity == 'severe':
                diversity_factor = 1.5  # Moderate exploration boost
            elif severity == 'moderate':
                diversity_factor = 1.2  # Mild exploration boost
            elif severity == 'normal':
                # Fine-tune based on diversity score
                if diversity_score < 0.3:
                    diversity_factor = 1.1
                elif diversity_score > 0.7:
                    diversity_factor = 0.9  # Slightly reduce exploration for high diversity
        
        # 4. Pareto front size-based adjustment (new feature)
        pareto_factor = 1.0
        if pareto_size is not None:
            if pareto_size < 10:
                pareto_factor = 1.3  # Increase exploration for small Pareto front
            elif pareto_size > 30:
                pareto_factor = 0.8  # Reduce exploration for large Pareto front
            elif pareto_size > 50:
                pareto_factor = 0.7  # Further reduce for very large Pareto front
        
        # 5. Stagnation detection-based adjustment (enhanced)
        stagnation_factor = 1.0
        if hypervolume_history and len(hypervolume_history) > 15:
            convergence_result = self._check_convergence(hypervolume_history, iteration)
            if convergence_result['stagnant']:
                if convergence_result['severity'] == 'severe':
                    stagnation_factor = 2.0  # Stronger exploration boost
                elif convergence_result['severity'] == 'moderate':
                    stagnation_factor = 1.6  # Moderate exploration boost
                elif convergence_result['severity'] == 'mild':
                    stagnation_factor = 1.2  # Mild exploration boost
                
                # Additional boost based on stagnation duration
                if convergence_result.get('stagnation_duration', 0) > 0.3 * max_iterations:
                    stagnation_factor *= 1.3
        
        # 6. Adaptive parameter calculation with multi-factor integration
        
        # Alpha (exploration parameter): composite adjustment
        base_alpha = 1.2 * (1 - 0.4 * progress_factor)
        
        # Multi-factor adjustment for alpha
        alpha_adjustment = improvement_factor * diversity_factor * pareto_factor * stagnation_factor
        params['alpha'] = base_alpha * alpha_adjustment
        
        # Beta (exploitation parameter): inverse relationship with alpha
        base_beta = 0.3 * (1 + 0.6 * progress_factor)
        
        # Inverse adjustment for balanced exploration/exploitation
        beta_adjustment = 1.0 / alpha_adjustment
        params['beta'] = base_beta * beta_adjustment
        
        # 7. Dynamic parameter bounds based on problem characteristics and progress
        if progress < 0.2:
            # Early exploration phase: aggressive exploration
            params['alpha'] = min(3.0, max(0.8, params['alpha']))
            params['beta'] = min(1.0, max(0.1, params['beta']))
        elif progress < 0.5:
            # Transition phase: balanced approach
            params['alpha'] = min(2.5, max(0.6, params['alpha']))
            params['beta'] = min(1.2, max(0.2, params['beta']))
        elif progress < 0.8:
            # Exploitation phase: refined search
            params['alpha'] = min(2.0, max(0.4, params['alpha']))
            params['beta'] = min(1.4, max(0.3, params['beta']))
        else:
            # Final phase: intensive exploitation
            params['alpha'] = min(1.5, max(0.3, params['alpha']))
            params['beta'] = min(1.6, max(0.4, params['beta']))
        
        # 8. Intelligent perturbations with adaptive strength
        perturbation_strength = 0.1 * (1 - 0.7 * progress)
        
        # Adaptive perturbation based on convergence state
        if hypervolume_history and len(hypervolume_history) > 8:
            recent_volatility = np.std(hypervolume_history[-8:]) / max(np.mean(hypervolume_history[-8:]), 1e-10)
            if recent_volatility < 0.0005:  # Very low volatility indicates strong stagnation
                perturbation_strength *= 2.0
            elif recent_volatility < 0.001:
                perturbation_strength *= 1.5
            elif recent_volatility > 0.01:  # High volatility indicates active search
                perturbation_strength *= 0.5
        
        # Apply intelligent perturbations
        params['alpha'] *= (1 + perturbation_strength * np.random.randn())
        params['beta'] *= (1 + perturbation_strength * np.random.randn())
        
        # 9. Final parameter bounds for stability and convergence
        params['alpha'] = max(0.2, min(3.5, params['alpha']))
        params['beta'] = max(0.05, min(2.0, params['beta']))
        
        # 10. Adaptive parameter smoothing for stable convergence
        if hasattr(self, '_previous_alpha'):
            # Smooth parameter transitions to avoid oscillations
            smoothing_factor = max(0.3, 0.7 * (1 - progress))  # More smoothing in early stages
            params['alpha'] = smoothing_factor * self._previous_alpha + (1 - smoothing_factor) * params['alpha']
            params['beta'] = smoothing_factor * self._previous_beta + (1 - smoothing_factor) * params['beta']
        
        # Store current parameters for next iteration smoothing
        self._previous_alpha = params['alpha']
        self._previous_beta = params['beta']
        
        return params
    
    def _calculate_adaptive_mutation_rate(self, iteration: int, max_iterations: int, 
                                        hypervolume_history: List[float], pareto_size: int) -> float:
        """Calculate adaptive mutation rate based on convergence state."""
        progress = iteration / max_iterations
        
        # Base mutation rate decreases with progress
        base_rate = max(0.05, 0.3 * (1 - progress))
        
        # Adjust based on hypervolume improvement
        if len(hypervolume_history) > 10:
            recent_improvement = hypervolume_history[-1] - hypervolume_history[-10]
            avg_improvement = np.mean(np.diff(hypervolume_history[-10:]))
            
            if recent_improvement < 0.001 * hypervolume_history[-10]:
                # Stagnation - increase mutation rate
                base_rate *= 1.5
            elif avg_improvement > 0.005 * hypervolume_history[-10]:
                # Good progress - reduce mutation rate
                base_rate *= 0.7
        
        # Adjust based on Pareto front diversity
        if pareto_size < 10:
            # Low diversity - increase mutation
            base_rate *= 1.3
        elif pareto_size > 30:
            # High diversity - reduce mutation
            base_rate *= 0.8
        
        return min(0.5, max(0.05, base_rate))
    
    def _calculate_mutation_frequency(self, iteration: int, max_iterations: int, 
                                    hypervolume_history: List[float]) -> int:
        """Calculate adaptive mutation frequency."""
        progress = iteration / max_iterations
        
        # Base frequency: more frequent in early stages
        base_frequency = max(3, int(15 * (1 - progress)))
        
        # Adjust based on convergence state
        if len(hypervolume_history) > 15:
            recent_improvement = hypervolume_history[-1] - hypervolume_history[-15]
            if recent_improvement < 0.002 * hypervolume_history[-15]:
                # Stagnation - increase frequency
                base_frequency = max(2, base_frequency // 2)
        
        return base_frequency
    
    def _apply_enhanced_mutation(self, population: np.ndarray, lower_bounds: np.ndarray,
                               upper_bounds: np.ndarray, mutation_rate: float, 
                               iteration: int) -> np.ndarray:
        """Apply enhanced mutation with multiple strategies."""
        n, dim = population.shape
        mutated_pop = population.copy()
        
        for i in range(n):
            if np.random.random() < mutation_rate:
                mutation_type = np.random.choice(['gaussian', 'polynomial', 'boundary'])
                
                if mutation_type == 'gaussian':
                    # Gaussian mutation with adaptive scale
                    scale = 0.1 * (upper_bounds - lower_bounds) * (1 - iteration / self.max_iterations)
                    mutation = np.random.randn(dim) * scale
                    mutated_pop[i] += mutation
                    
                elif mutation_type == 'polynomial':
                    # Polynomial mutation for better exploration
                    eta = 20 + 10 * np.random.random()
                    for j in range(dim):
                        if np.random.random() < 0.5:
                            delta = 2 * np.random.random() - 1
                            if delta < 0:
                                delta_q = (2 * np.random.random() + (1 - 2 * np.random.random()) * 
                                         (1 - delta) ** (eta + 1)) ** (1 / (eta + 1)) - 1
                            else:
                                delta_q = 1 - (2 * np.random.random() + (1 - 2 * np.random.random()) * 
                                             (1 - delta) ** (eta + 1)) ** (1 / (eta + 1))
                            
                            mutated_pop[i, j] += delta_q * (upper_bounds[j] - lower_bounds[j])
                            
                elif mutation_type == 'boundary':
                    # Boundary mutation for extreme exploration
                    j = np.random.randint(dim)
                    if np.random.random() < 0.5:
                        mutated_pop[i, j] = lower_bounds[j]
                    else:
                        mutated_pop[i, j] = upper_bounds[j]
        
        # Apply boundary constraints
        mutated_pop = np.clip(mutated_pop, lower_bounds, upper_bounds)
        return mutated_pop
    
    def _check_diversity_loss(self, tianji_pop: np.ndarray, king_pop: np.ndarray,
                            lower_bounds: np.ndarray, upper_bounds: np.ndarray) -> Dict[str, Any]:
        """Enhanced diversity assessment with multiple metrics."""
        all_pop = np.vstack([tianji_pop, king_pop])
        n = len(all_pop)
        
        if n < 2:
            return {'diversity_low': True, 'severity': 'critical', 'metrics': {}}
        
        # Multiple diversity metrics
        
        # 1. Spatial diversity: average pairwise distances
        distances = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(all_pop[i] - all_pop[j])
                distances.append(dist)
        
        avg_distance = np.mean(distances) if distances else 0
        max_possible_distance = np.linalg.norm(upper_bounds - lower_bounds)
        spatial_diversity = avg_distance / max_possible_distance if max_possible_distance > 0 else 0
        
        # 2. Cluster analysis: check if solutions are clustered
        if n >= 3:
            # Calculate cluster density using k-means silhouette score approximation
            from sklearn.metrics import pairwise_distances
            dist_matrix = pairwise_distances(all_pop)
            cluster_density = np.mean(np.min(dist_matrix + np.eye(n) * np.max(dist_matrix), axis=1))
            cluster_diversity = cluster_density / max_possible_distance
        else:
            cluster_diversity = spatial_diversity
        
        # 3. Entropy-based diversity: measure solution distribution uniformity
        if n >= 5 and len(lower_bounds) <= 32:  # Only use histogramdd for dimensions <= 32
            # Simple entropy approximation using grid-based partitioning
            n_bins = min(10, n)
            hist, _ = np.histogramdd(all_pop, bins=n_bins, 
                                   range=[(lb, ub) for lb, ub in zip(lower_bounds, upper_bounds)])
            hist = hist[hist > 0]  # Remove empty bins
            if len(hist) > 0:
                prob = hist / np.sum(hist)
                entropy = -np.sum(prob * np.log(prob))
                max_entropy = np.log(len(hist))
                entropy_diversity = entropy / max_entropy if max_entropy > 0 else 0
            else:
                entropy_diversity = 0
        else:
            # For high-dimensional problems, use PCA-based entropy approximation
            if n >= 5 and len(lower_bounds) > 32:
                # Use first 10 principal components for entropy calculation
                from sklearn.decomposition import PCA
                pca = PCA(n_components=min(10, len(lower_bounds)))
                try:
                    pca_features = pca.fit_transform(all_pop)
                    # Calculate entropy on PCA features
                    n_bins = min(5, n)  # Fewer bins for high-dimensional data
                    hist, _ = np.histogramdd(pca_features, bins=n_bins)
                    hist = hist[hist > 0]
                    if len(hist) > 0:
                        prob = hist / np.sum(hist)
                        entropy = -np.sum(prob * np.log(prob))
                        max_entropy = np.log(len(hist))
                        entropy_diversity = entropy / max_entropy if max_entropy > 0 else 0
                    else:
                        entropy_diversity = 0
                except:
                    entropy_diversity = spatial_diversity
            else:
                entropy_diversity = spatial_diversity
        
        # 4. Solution uniqueness: percentage of unique solutions
        unique_pop = np.unique(all_pop, axis=0)
        uniqueness_ratio = len(unique_pop) / n
        
        # Combined diversity score (weighted average)
        diversity_score = (0.4 * spatial_diversity + 0.3 * cluster_diversity + 
                         0.2 * entropy_diversity + 0.1 * uniqueness_ratio)
        
        # Adaptive thresholds based on population size
        base_threshold = 0.15
        size_adjustment = max(0.5, min(1.5, n / 50))  # Adjust for population size
        threshold = base_threshold * size_adjustment
        
        # Determine diversity status
        diversity_low = diversity_score < threshold
        
        # Severity classification
        if diversity_score < 0.5 * threshold:
            severity = 'critical'
        elif diversity_score < 0.8 * threshold:
            severity = 'severe'
        elif diversity_score < threshold:
            severity = 'moderate'
        else:
            severity = 'normal'
        
        return {
            'diversity_low': diversity_low,
            'severity': severity,
            'score': diversity_score,
            'metrics': {
                'spatial': spatial_diversity,
                'cluster': cluster_diversity,
                'entropy': entropy_diversity,
                'uniqueness': uniqueness_ratio
            }
        }
    
    def _inject_diversity(self, tianji_pop: np.ndarray, king_pop: np.ndarray,
                        lower_bounds: np.ndarray, upper_bounds: np.ndarray, 
                        diversity_status: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """Enhanced diversity injection with intelligent adaptive strategies."""
        all_pop = np.vstack([tianji_pop, king_pop])
        n = len(all_pop)
        severity = diversity_status.get('severity', 'moderate')
        metrics = diversity_status.get('metrics', {})
        
        # Adaptive injection strategy based on severity and specific diversity metrics
        if severity == 'critical':
            # Critical: aggressive replacement (40-60%) with multiple strategies
            replace_ratio = 0.5
            strategy = 'aggressive'
        elif severity == 'severe':
            # Severe: moderate replacement (25-40%) with targeted strategies
            replace_ratio = 0.35
            strategy = 'moderate'
        elif severity == 'moderate':
            # Moderate: conservative replacement (15-25%) with quality preservation
            replace_ratio = 0.2
            strategy = 'conservative'
        else:
            # Normal: minimal injection (5-15%) for maintenance
            replace_ratio = 0.1
            strategy = 'minimal'
        
        # Adjust replacement ratio based on specific diversity metrics
        if 'spatial' in metrics and metrics['spatial'] < 0.1:
            # Very low spatial diversity: increase replacement
            replace_ratio = min(0.7, replace_ratio * 1.3)
        if 'uniqueness' in metrics and metrics['uniqueness'] < 0.7:
            # Low uniqueness: increase replacement
            replace_ratio = min(0.8, replace_ratio * 1.2)
        
        replace_count = max(1, int(replace_ratio * n))
        
        # Intelligent strategy selection based on diversity metrics
        if strategy == 'aggressive':
            # Aggressive: multiple generation methods with emphasis on spatial diversity
            if metrics.get('spatial', 1) < 0.2:
                # Very low spatial diversity: focus on boundary and random solutions
                boundary_count = max(1, int(0.5 * replace_count))
                random_count = max(1, int(0.3 * replace_count))
                lhs_count = replace_count - boundary_count - random_count
            else:
                # Balanced approach
                lhs_count = max(1, int(0.4 * replace_count))
                random_count = max(1, int(0.3 * replace_count))
                boundary_count = replace_count - lhs_count - random_count
            
            new_individuals_lhs = self._lhs_design_modified(lhs_count, lower_bounds, upper_bounds)
            new_individuals_random = self._generate_random_solutions(random_count, lower_bounds, upper_bounds)
            new_individuals_boundary = self._generate_boundary_solutions(boundary_count, lower_bounds, upper_bounds)
            
            new_individuals = np.vstack([new_individuals_lhs, new_individuals_random, new_individuals_boundary])
            
        elif strategy == 'moderate':
            # Moderate: LHS + boundary with adaptive ratios
            if metrics.get('cluster', 1) < 0.3:
                # Low cluster diversity: more boundary solutions
                boundary_count = max(1, int(0.4 * replace_count))
                lhs_count = replace_count - boundary_count
            else:
                # Standard approach
                lhs_count = max(1, int(0.7 * replace_count))
                boundary_count = replace_count - lhs_count
            
            new_individuals_lhs = self._lhs_design_modified(lhs_count, lower_bounds, upper_bounds)
            new_individuals_boundary = self._generate_boundary_solutions(boundary_count, lower_bounds, upper_bounds)
            
            new_individuals = np.vstack([new_individuals_lhs, new_individuals_boundary])
            
        elif strategy == 'conservative':
            # Conservative: LHS + intelligent perturbation
            lhs_count = max(1, int(0.8 * replace_count))
            perturbed_count = replace_count - lhs_count
            
            new_individuals_lhs = self._lhs_design_modified(lhs_count, lower_bounds, upper_bounds)
            
            # Intelligent perturbation based on diversity metrics
            if perturbed_count > 0 and n > 0:
                # Select elite solutions for perturbation
                elite_count = min(perturbed_count, max(1, int(0.2 * n)))
                elite_solutions = all_pop[:elite_count]
                
                # Adaptive perturbation strength based on diversity status
                if metrics.get('entropy', 1) < 0.3:
                    # Low entropy: stronger perturbation
                    perturbation_strength = 0.15
                else:
                    perturbation_strength = 0.1
                
                perturbations = np.random.uniform(-perturbation_strength, perturbation_strength, 
                                                 (elite_count, len(lower_bounds)))
                
                # Scale perturbations by variable ranges
                ranges = upper_bounds - lower_bounds
                scaled_perturbations = perturbations * ranges
                
                new_individuals_perturbed = elite_solutions + scaled_perturbations
                
                # Ensure boundaries
                new_individuals_perturbed = np.clip(new_individuals_perturbed, lower_bounds, upper_bounds)
                
                new_individuals = np.vstack([new_individuals_lhs, new_individuals_perturbed])
            else:
                new_individuals = new_individuals_lhs
                
        else:  # minimal strategy
            # Only LHS with small perturbation
            new_individuals = self._lhs_design_modified(replace_count, lower_bounds, upper_bounds)
            
            # Add small random noise
            noise = np.random.normal(0, 0.01, new_individuals.shape)
            new_individuals = np.clip(new_individuals + noise, lower_bounds, upper_bounds)
        
        # Replace worst individuals based on dummy objective
        all_fitness = np.array([self._dummy_objective(ind) for ind in all_pop])
        worst_indices = np.argsort(all_fitness)[-replace_count:]
        all_pop[worst_indices] = new_individuals
        
        # Split back into tianji and king populations
        tianji_size = len(tianji_pop)
        tianji_pop_new = all_pop[:tianji_size]
        king_pop_new = all_pop[tianji_size:]
        
        return tianji_pop_new, king_pop_new
    
    def _dummy_objective(self, individual: np.ndarray) -> float:
        """Dummy objective function for diversity injection."""
        # Simple distance-based objective to identify worst solutions
        return np.sum(individual ** 2)
    
    def _generate_random_solutions(self, n: int, lower_bounds: np.ndarray, 
                                 upper_bounds: np.ndarray) -> np.ndarray:
        """Generate random solutions within bounds."""
        dim = len(lower_bounds)
        solutions = np.random.uniform(lower_bounds, upper_bounds, (n, dim))
        return solutions
    
    def _generate_boundary_solutions(self, n: int, lower_bounds: np.ndarray, 
                                   upper_bounds: np.ndarray) -> np.ndarray:
        """Generate solutions near the boundaries to explore extreme regions."""
        dim = len(lower_bounds)
        solutions = []
        
        for _ in range(n):
            # Choose which boundaries to explore
            boundary_type = np.random.choice(['lower', 'upper', 'mixed'])
            solution = np.zeros(dim)
            
            if boundary_type == 'lower':
                # Near lower bounds
                for j in range(dim):
                    solution[j] = lower_bounds[j] + np.random.uniform(0, 0.1) * (upper_bounds[j] - lower_bounds[j])
            elif boundary_type == 'upper':
                # Near upper bounds
                for j in range(dim):
                    solution[j] = upper_bounds[j] - np.random.uniform(0, 0.1) * (upper_bounds[j] - lower_bounds[j])
            else:  # mixed
                # Mix of lower and upper boundaries
                for j in range(dim):
                    if np.random.random() < 0.5:
                        solution[j] = lower_bounds[j] + np.random.uniform(0, 0.1) * (upper_bounds[j] - lower_bounds[j])
                    else:
                        solution[j] = upper_bounds[j] - np.random.uniform(0, 0.1) * (upper_bounds[j] - lower_bounds[j])
            
            solutions.append(solution)
        
        return np.array(solutions)
    
    def _random_reassignment(self, tianji_pop: np.ndarray, tianji_fitness: np.ndarray,
                           king_pop: np.ndarray, king_fitness: np.ndarray):
        """Randomly reassign populations to increase diversity."""
        all_pop = np.vstack([tianji_pop, king_pop])
        all_fitness = np.vstack([tianji_fitness, king_fitness])
        
        n_pop = len(tianji_pop)
        random_indices = np.random.permutation(len(all_pop))
        
        tianji_pop_new = all_pop[random_indices[:n_pop]]
        tianji_fitness_new = all_fitness[random_indices[:n_pop]]
        king_pop_new = all_pop[random_indices[n_pop:]]
        king_fitness_new = all_fitness[random_indices[n_pop:]]
        
        return tianji_pop_new, tianji_fitness_new, king_pop_new, king_fitness_new
    
    def _non_dominated_sort(self, fitness: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Perform non-dominated sorting and calculate crowding distances."""
        n = len(fitness)
        if n == 0:
            return np.array([]), np.array([])
        
        ranks = np.zeros(n, dtype=int)
        crowding = np.zeros(n)
        
        # Initialize domination relationships
        S = [[] for _ in range(n)]  # Solutions dominated by each solution
        n_dominated = np.zeros(n, dtype=int)  # Number of solutions dominating each solution
        fronts = [[] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if self._dominates(fitness[i], fitness[j]):
                    S[i].append(j)
                elif self._dominates(fitness[j], fitness[i]):
                    n_dominated[i] += 1
            
            if n_dominated[i] == 0:
                ranks[i] = 1
                fronts[0].append(i)
        
        # Calculate subsequent fronts
        current_front = 0
        while fronts[current_front]:
            Q = []
            for i in fronts[current_front]:
                for j in S[i]:
                    n_dominated[j] -= 1
                    if n_dominated[j] == 0:
                        ranks[j] = current_front + 2  # +1 for 0-index, +1 for next front
                        Q.append(j)
            current_front += 1
            # 确保fronts列表有足够的空间
            if current_front >= len(fronts):
                fronts.append([])
            fronts[current_front] = Q
        
        # Calculate crowding distances for all fronts
        for front_idx in range(current_front):
            if fronts[front_idx]:
                front_indices = np.array(fronts[front_idx])
                crowding_subset = self._calculate_crowding_distance(fitness[front_indices])
                crowding[front_indices] = crowding_subset
        
        return ranks, crowding
    
    def _calculate_crowding_distance(self, fitness_subset: np.ndarray) -> np.ndarray:
        """Calculate crowding distance for a subset of solutions."""
        n, m = fitness_subset.shape
        crowding = np.zeros(n)
        
        if n <= 2:
            crowding[:] = np.inf
            return crowding
        
        for obj in range(m):
            order = np.argsort(fitness_subset[:, obj])
            sorted_vals = fitness_subset[order, obj]
            
            # Endpoints get infinite crowding distance
            crowding[order[0]] = np.inf
            crowding[order[-1]] = np.inf
            
            f_max = sorted_vals[-1]
            f_min = sorted_vals[0]
            
            if f_max == f_min:
                continue
            
            # Calculate crowding for intermediate points
            for i in range(1, n - 1):
                crowding[order[i]] += (sorted_vals[i + 1] - sorted_vals[i - 1]) / (f_max - f_min)
        
        return crowding
    
    def _dominates(self, a: np.ndarray, b: np.ndarray) -> bool:
        """Check if solution a dominates solution b."""
        not_worse = np.all(a <= b)
        strictly_better = np.any(a < b)
        return not_worse and strictly_better
    
    def _sort_by_rank_and_crowding(self, population: np.ndarray, fitness: np.ndarray,
                                 ranks: np.ndarray, crowding: np.ndarray):
        """Sort population by Pareto rank and crowding distance."""
        if len(population) == 0:
            return population, fitness
        
        # Sort by rank (ascending) and crowding (descending)
        indices = np.lexsort([-crowding, ranks])
        return population[indices], fitness[indices]
    
    def _select_diverse_solutions(self, front: np.ndarray, positions: np.ndarray, 
                                k: int, diversity_status: Dict[str, Any] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Enhanced elite selection with adaptive diversity preservation."""
        if len(front) == 0:
            return front, positions
        
        n = min(len(front), len(positions))
        if n == 0:
            return np.array([]), np.array([])
        
        front = front[:n]
        positions = positions[:n]
        
        # Adaptive selection strategy based on diversity status
        if diversity_status and diversity_status.get('diversity_low', False):
            severity = diversity_status.get('severity', 'moderate')
            
            if severity == 'critical':
                # Critical diversity loss: prioritize diversity over crowding
                return self._select_by_diversity_metric(front, positions, k)
            elif severity == 'severe':
                # Severe: balance diversity and crowding
                return self._select_by_balanced_criteria(front, positions, k, diversity_weight=0.6)
            elif severity == 'moderate':
                # Moderate: slight preference for diversity
                return self._select_by_balanced_criteria(front, positions, k, diversity_weight=0.3)
        
        # Normal diversity: traditional crowding-based selection
        crowding = self._calculate_crowding_distance(front)
        indices = np.argsort(-crowding)[:min(k, n)]
        
        return front[indices], positions[indices]
    
    def _select_by_diversity_metric(self, front: np.ndarray, positions: np.ndarray, 
                                  k: int) -> Tuple[np.ndarray, np.ndarray]:
        """Select solutions based on spatial diversity metrics."""
        n = len(front)
        if k >= n:
            return front, positions
        
        # Calculate pairwise distances
        from sklearn.metrics import pairwise_distances
        dist_matrix = pairwise_distances(front)
        
        # Greedy selection: maximize minimum distance to selected solutions
        selected_indices = []
        
        # Start with the solution that has maximum average distance
        avg_distances = np.mean(dist_matrix, axis=1)
        start_idx = np.argmax(avg_distances)
        selected_indices.append(start_idx)
        
        # Greedily add solutions that maximize minimum distance to selected set
        for _ in range(1, k):
            min_distances = []
            for i in range(n):
                if i not in selected_indices:
                    min_dist = np.min([dist_matrix[i, j] for j in selected_indices])
                    min_distances.append(min_dist)
                else:
                    min_distances.append(-np.inf)
            
            next_idx = np.argmax(min_distances)
            selected_indices.append(next_idx)
        
        return front[selected_indices], positions[selected_indices]
    
    def _select_by_balanced_criteria(self, front: np.ndarray, positions: np.ndarray, 
                                   k: int, diversity_weight: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
        """Select solutions balancing crowding distance and spatial diversity."""
        n = len(front)
        if k >= n:
            return front, positions
        
        # Calculate crowding distances
        crowding = self._calculate_crowding_distance(front)
        
        # Calculate spatial diversity scores
        from sklearn.metrics import pairwise_distances
        dist_matrix = pairwise_distances(front)
        diversity_scores = np.mean(dist_matrix, axis=1)
        
        # Normalize both metrics
        crowding_norm = (crowding - np.min(crowding)) / (np.max(crowding) - np.min(crowding) + 1e-10)
        diversity_norm = (diversity_scores - np.min(diversity_scores)) / (np.max(diversity_scores) - np.min(diversity_scores) + 1e-10)
        
        # Combined score
        combined_scores = (1 - diversity_weight) * crowding_norm + diversity_weight * diversity_norm
        
        # Select top k solutions
        indices = np.argsort(-combined_scores)[:k]
        
        return front[indices], positions[indices]
    
    def _calculate_hypervolume(self, front: np.ndarray) -> float:
        """Calculate hypervolume metric for Pareto front with enhanced precision and maximization focus."""
        if len(front) == 0:
            return 0.0
        
        n, m = front.shape
        
        # Enhanced duplicate removal with tolerance-based comparison
        front_rounded = np.round(front, 8)  # Increased precision
        _, unique_idx = np.unique(front_rounded, axis=0, return_index=True)
        front = front[unique_idx]
        
        if len(front) == 0:
            return 0.0
        
        # Enhanced reference point selection for hypervolume maximization
        ref_point = self._select_reference_point_maximization(front)
        
        # Use appropriate hypervolume calculation method based on dimension
        if m == 2:
            return self._hv2d_maximization(front, ref_point)
        elif m == 3:
            return self._hv3d_maximization(front, ref_point)
        elif m <= 5:
            return self._hv_nd_maximization(front, ref_point)
        else:
            return self._hv_monte_carlo_maximization(front, ref_point)
    
    def _select_reference_point(self, front: np.ndarray) -> np.ndarray:
        """Select reference point for hypervolume calculation."""
        max_point = np.max(front, axis=0)
        min_point = np.min(front, axis=0)
        
        # Reference point is 15% beyond maximum values
        ref_point = max_point + 0.15 * (max_point - min_point)
        
        # Ensure reference point is sufficiently far
        for i in range(len(ref_point)):
            if np.any(front[:, i] >= ref_point[i]):
                ref_point[i] = max_point[i] + 0.1 * abs(max_point[i])
        
        # Prevent extreme reference points
        ref_point = np.minimum(ref_point, max_point * 1.5)
        return ref_point
    
    def _select_reference_point_maximization(self, front: np.ndarray) -> np.ndarray:
        """Optimized reference point selection specifically for hypervolume maximization."""
        if len(front) == 0:
            return np.array([])
        
        n, m = front.shape
        
        # For hypervolume maximization, we need a reference point that is worse than all solutions
        # This ensures all solutions dominate the reference point, maximizing the hypervolume
        min_point = np.min(front, axis=0)
        max_point = np.max(front, axis=0)
        
        # Calculate the spread of the Pareto front
        spread = max_point - min_point
        
        # Adaptive reference point selection based on front characteristics
        if n <= 5:
            # Small front: use conservative reference point
            ref_point = min_point - 0.15 * spread
        else:
            # Larger front: use more aggressive reference point to maximize hypervolume
            # Consider the density and distribution of solutions
            density_factor = min(1.0, 10.0 / n)  # Higher density allows more aggressive reference
            ref_point = min_point - (0.1 + 0.1 * density_factor) * spread
        
        # Ensure reference point is strictly dominated by all solutions
        for i in range(m):
            # Add a small safety margin to ensure dominance
            safety_margin = 0.01 * abs(min_point[i])
            if np.any(front[:, i] <= ref_point[i] + safety_margin):
                ref_point[i] = min_point[i] - 0.05 * abs(min_point[i])
        
        # Prevent extreme reference points that could cause numerical issues
        ref_point = np.maximum(ref_point, min_point * 0.5)
        
        # Additional safety: ensure reference point is not too close to zero for positive objectives
        for i in range(m):
            if min_point[i] > 0 and ref_point[i] < 0.01 * min_point[i]:
                ref_point[i] = 0.01 * min_point[i]
        
        return ref_point
    
    def _hv2d(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Calculate 2D hypervolume."""
        if len(front) == 0:
            return 0.0
        
        # Sort by first objective ascending, second objective descending
        sorted_front = front[np.lexsort([-front[:, 1], front[:, 0]])]
        
        hv = 0.0
        prev_y = ref_point[1]
        
        for i in range(len(sorted_front)):
            current_x = sorted_front[i, 0]
            current_y = sorted_front[i, 1]
            
            if current_y < prev_y:
                width = ref_point[0] - current_x
                height = prev_y - current_y
                hv += width * height
                prev_y = current_y
        
        return hv
    
    def _hv2d_maximization(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Optimized 2D hypervolume calculation for maximization problems with guaranteed accuracy."""
        if len(front) == 0:
            return 0.0
        
        # Filter solutions that strictly dominate the reference point
        valid_indices = np.all(front > ref_point, axis=1)
        front = front[valid_indices]
        
        if len(front) == 0:
            return 0.0
        
        # Sort by first objective in descending order, then by second objective in ascending order
        # This ensures we cover the maximum hypervolume efficiently
        sorted_indices = np.lexsort([front[:, 1], -front[:, 0]])
        sorted_front = front[sorted_indices]
        
        # Initialize hypervolume calculation
        hv = 0.0
        prev_y = ref_point[1]
        
        # Calculate the hypervolume using an efficient sweep-line algorithm
        for i in range(len(sorted_front)):
            current_x = sorted_front[i, 0]
            current_y = sorted_front[i, 1]
            
            # Calculate the area contribution of this solution
            if i == 0:
                # First solution contributes the full rectangle from reference point
                hv += (current_x - ref_point[0]) * (current_y - ref_point[1])
            else:
                # Subsequent solutions contribute the area between current and previous y-values
                if current_y > prev_y:
                    hv += (current_x - ref_point[0]) * (current_y - prev_y)
            
            prev_y = max(prev_y, current_y)
        
        # Additional optimization: check for overlapping areas and ensure no double-counting
        # This is particularly important for crowded Pareto fronts
        if len(sorted_front) > 1:
            # Verify that the calculated hypervolume is reasonable
            max_possible = (np.max(sorted_front[:, 0]) - ref_point[0]) * (np.max(sorted_front[:, 1]) - ref_point[1])
            if hv > max_possible:
                # Use a more conservative approach if there's potential overestimation
                hv = self._hv2d_conservative(sorted_front, ref_point)
        
        return hv
    
    def _hv2d_conservative(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Conservative 2D hypervolume calculation using the standard inclusion-exclusion method."""
        if len(front) == 0:
            return 0.0
        
        # Sort by first objective in descending order
        sorted_indices = np.argsort(-front[:, 0])
        sorted_front = front[sorted_indices]
        
        hv = 0.0
        prev_y = ref_point[1]
        
        for i in range(len(sorted_front)):
            current_x = sorted_front[i, 0]
            current_y = sorted_front[i, 1]
            
            # Only add area if this solution improves the second objective
            if current_y > prev_y:
                hv += (current_x - ref_point[0]) * (current_y - prev_y)
                prev_y = current_y
        
        return hv
    
    def _hv3d(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Calculate 3D hypervolume using slicing method."""
        if len(front) == 0:
            return 0.0
        
        # Sort by first objective
        sorted_front = front[np.argsort(front[:, 0])]
        
        # Remove solutions dominated by reference point
        valid_indices = np.all(sorted_front < ref_point, axis=1)
        sorted_front = sorted_front[valid_indices]
        
        if len(sorted_front) == 0:
            return 0.0
        
        hv = 0.0
        prev_x = ref_point[0]
        
        for i in range(len(sorted_front)):
            current_x = sorted_front[i, 0]
            
            # Calculate current slice
            slice_points = sorted_front[i:, 1:3]
            slice_ref = ref_point[1:3]
            
            slice_hv = self._hv2d(slice_points, slice_ref)
            width = prev_x - current_x
            hv += width * slice_hv
            
            prev_x = current_x
        
        return hv
    
    def _hv3d_maximization(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Optimized 3D hypervolume calculation for maximization with guaranteed accuracy."""
        if len(front) == 0:
            return 0.0
        
        # Filter solutions that strictly dominate the reference point
        valid_indices = np.all(front > ref_point, axis=1)
        front = front[valid_indices]
        
        if len(front) == 0:
            return 0.0
        
        # Sort by first objective in ascending order for efficient slicing
        sorted_indices = np.argsort(front[:, 0])
        sorted_front = front[sorted_indices]
        
        hv = 0.0
        prev_x = ref_point[0]
        
        for i in range(len(sorted_front)):
            current_x = sorted_front[i, 0]
            
            # Calculate 2D hypervolume for current slice using maximization method
            slice_points = sorted_front[i:, 1:3]
            slice_ref = ref_point[1:3]
            
            slice_hv = self._hv2d_maximization(slice_points, slice_ref)
            width = current_x - prev_x
            hv += width * slice_hv
            
            prev_x = current_x
        
        # Validation: ensure the calculated hypervolume is reasonable
        if len(sorted_front) > 0:
            max_possible = (np.max(sorted_front[:, 0]) - ref_point[0]) * \
                          (np.max(sorted_front[:, 1]) - ref_point[1]) * \
                          (np.max(sorted_front[:, 2]) - ref_point[2])
            if hv > max_possible:
                # Fall back to a more conservative method
                hv = self._hv3d_conservative(sorted_front, ref_point)
        
        return hv
    
    def _hv3d_conservative(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Conservative 3D hypervolume calculation using slice-based approach."""
        if len(front) == 0:
            return 0.0
        
        # Sort by third objective in descending order for slicing
        sorted_indices = np.argsort(-front[:, 2])
        sorted_front = front[sorted_indices]
        
        hv = 0.0
        prev_z = ref_point[2]
        
        # Slice-based approach: calculate 2D hypervolume for each z-slice
        for i in range(len(sorted_front)):
            current_z = sorted_front[i, 2]
            if current_z > prev_z:
                # Extract solutions that have z >= current_z
                slice_front = sorted_front[:i+1, :2]
                slice_ref = ref_point[:2]
                
                # Calculate 2D hypervolume for this slice
                slice_hv = self._hv2d_conservative(slice_front, slice_ref)
                
                # Add the volume contribution
                hv += slice_hv * (current_z - prev_z)
                prev_z = current_z
        
        return hv
    
    def _hv_nd_maximization(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Calculate hypervolume for dimensions 3-5 using recursive slicing method.
        
        Parameters
        ----------
        front : np.ndarray
            Pareto front
        ref_point : np.ndarray
            Reference point
            
        Returns
        -------
        float
            Hypervolume value
        """
        if len(front) == 0:
            return 0.0
        
        # Filter solutions that strictly dominate the reference point
        valid_indices = np.all(front > ref_point, axis=1)
        front = front[valid_indices]
        
        if len(front) == 0:
            return 0.0
        
        # For dimensions 3-5, use the existing WFG algorithm
        return self._hv_nd_wfg(front, ref_point)
    
    def _hv_monte_carlo_maximization(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Calculate hypervolume for dimensions >5 using enhanced Monte Carlo method.
        
        Parameters
        ----------
        front : np.ndarray
            Pareto front
        ref_point : np.ndarray
            Reference point
            
        Returns
        -------
        float
            Hypervolume value
        """
        if len(front) == 0:
            return 0.0
        
        # Filter solutions that strictly dominate the reference point
        valid_indices = np.all(front > ref_point, axis=1)
        front = front[valid_indices]
        
        if len(front) == 0:
            return 0.0
        
        # For high dimensions, use the enhanced Monte Carlo method
        return self._hv_monte_carlo_enhanced(front, ref_point)
    
    def _hv_nd_wfg(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Calculate hypervolume for 4-5 dimensions using WFG algorithm for maximization."""
        if len(front) == 0:
            return 0.0
        
        # Filter solutions that dominate the reference point (maximization case)
        valid_indices = np.all(front > ref_point, axis=1)
        front = front[valid_indices]
        
        if len(front) == 0:
            return 0.0
        
        # Use recursive slicing approach for moderate dimensions
        return self._hv_nd_recursive(front, ref_point)
    
    def _hv_nd_recursive(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Recursive hypervolume calculation for moderate dimensions with maximization support."""
        if len(front) == 0:
            return 0.0
        
        m = front.shape[1]
        
        if m == 1:
            # 1D case: simple calculation for maximization
            return np.max(front[:, 0]) - ref_point[0]
        elif m == 2:
            return self._hv2d_maximization(front, ref_point)
        elif m == 3:
            return self._hv3d_maximization(front, ref_point)
        else:
            # Recursive slicing for higher dimensions - sort by ascending for maximization
            sorted_indices = np.argsort(front[:, 0])
            sorted_front = front[sorted_indices]
            
            hv = 0.0
            prev_x = ref_point[0]
            
            for i in range(len(sorted_front)):
                current_x = sorted_front[i, 0]
                
                # Calculate hypervolume for lower-dimensional slice
                slice_points = sorted_front[i:, 1:]
                slice_ref = ref_point[1:]
                
                slice_hv = self._hv_nd_recursive(slice_points, slice_ref)
                width = current_x - prev_x
                hv += width * slice_hv
                
                prev_x = current_x
            
            return hv
    
    def _hv_monte_carlo_improved(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Calculate hypervolume for high-dimensional problems using Monte Carlo."""
        n_samples = 10000
        n, m = front.shape
        
        if n == 0:
            return 0.0
        
        # For minimization problems, use the origin as minimum point
        min_point = np.zeros(m)
        
        # Generate random samples
        samples = np.random.random((n_samples, m))
        for i in range(m):
            samples[:, i] = min_point[i] + (ref_point[i] - min_point[i]) * samples[:, i]
        
        # Count dominated samples
        dominated_count = 0
        for sample in samples:
            if self._is_dominated_by_any(sample, front):
                dominated_count += 1
        
        # Calculate hypervolume
        total_volume = np.prod(ref_point - min_point)
        return total_volume * dominated_count / n_samples
    
    def _hv_monte_carlo_enhanced(self, front: np.ndarray, ref_point: np.ndarray) -> float:
        """Enhanced Monte Carlo hypervolume calculation with adaptive sampling."""
        n, m = front.shape
        
        if n == 0:
            return 0.0
        
        # Adaptive sample size based on dimension
        base_samples = 5000
        dimension_factor = 2 ** m  # Exponential increase with dimension
        n_samples = min(100000, base_samples * dimension_factor)
        
        # For minimization problems, use the origin as minimum point
        min_point = np.zeros(m)
        
        # Use Latin Hypercube Sampling for better coverage
        try:
            from scipy.stats import qmc
            sampler = qmc.LatinHypercube(d=m)
            samples = sampler.random(n=n_samples)
            # Scale to the hypervolume space
            for i in range(m):
                samples[:, i] = min_point[i] + (ref_point[i] - min_point[i]) * samples[:, i]
        except ImportError:
            # Fallback to uniform random sampling
            samples = np.random.random((n_samples, m))
            for i in range(m):
                samples[:, i] = min_point[i] + (ref_point[i] - min_point[i]) * samples[:, i]
        
        # Vectorized dominance checking for better performance
        dominated_count = 0
        batch_size = 1000
        
        for i in range(0, n_samples, batch_size):
            batch_end = min(i + batch_size, n_samples)
            batch_samples = samples[i:batch_end]
            
            # Check if any solution in front dominates each sample
            for j in range(len(batch_samples)):
                sample = batch_samples[j]
                for solution in front:
                    if np.all(solution <= sample):
                        dominated_count += 1
                        break
        
        # Calculate hypervolume with confidence interval estimation
        total_volume = np.prod(ref_point - min_point)
        hv_estimate = total_volume * dominated_count / n_samples
        
        # Estimate standard error for quality assessment
        p = dominated_count / n_samples
        std_error = total_volume * np.sqrt(p * (1 - p) / n_samples)
        
        # Return estimate with quality indicator (can be used for convergence detection)
        return hv_estimate
    
    def _is_dominated_by_any(self, point: np.ndarray, front: np.ndarray) -> bool:
        """Check if point is dominated by any solution in the front."""
        for solution in front:
            if self._dominates(solution, point):
                return True
        return False
    
    def _update_solution_improved(self, pop_pos: np.ndarray, pop_fit: np.ndarray, 
                                idx: int, best_pos: np.ndarray, opponent_pop: np.ndarray,
                                upper_bounds: np.ndarray, lower_bounds: np.ndarray,
                                objective_function: Callable, iteration: int, 
                                max_iterations: int, params: Dict[str, float]):
        """Enhanced solution update strategy with intelligent crossover and mutation."""
        p = 1 - iteration / max_iterations  # Linear decrease
        dim = len(pop_pos[0])
        
        # Adaptive strategy selection based on convergence state
        strategy_choice = np.random.choice(['crossover', 'mutation', 'hybrid'], 
                                          p=[0.4, 0.4, 0.2])
        
        if strategy_choice == 'crossover':
            # Intelligent crossover strategy
            new_pos = self._intelligent_crossover(pop_pos, idx, best_pos, opponent_pop, 
                                                 p, params, dim)
        elif strategy_choice == 'mutation':
            # Enhanced mutation strategy
            new_pos = self._enhanced_mutation_strategy(pop_pos, idx, best_pos, 
                                                      p, params, dim, iteration, max_iterations)
        else:
            # Hybrid strategy combining both
            new_pos = self._hybrid_strategy(pop_pos, idx, best_pos, opponent_pop, 
                                          p, params, dim, iteration, max_iterations)
        
        # Boundary handling
        new_pos = self._space_bound_improved(new_pos, upper_bounds, lower_bounds)
        
        # Evaluate new solution
        new_fit = objective_function(new_pos)
        
        # Enhanced acceptance criteria with simulated annealing
        if self._should_accept_solution(new_fit, pop_fit[idx], iteration, max_iterations):
            pop_pos[idx] = new_pos
            pop_fit[idx] = new_fit
        
        return pop_pos, pop_fit
    
    def _intelligent_crossover(self, pop_pos: np.ndarray, idx: int, best_pos: np.ndarray,
                             opponent_pop: np.ndarray, p: float, params: Dict[str, float],
                             dim: int) -> np.ndarray:
        """Intelligent crossover strategy with multiple operators."""
        current_pos = pop_pos[idx]
        
        # Select crossover partner
        if np.random.random() < 0.7:
            # Crossover with best solution
            partner = best_pos
        else:
            # Crossover with random opponent
            partner_idx = np.random.randint(len(opponent_pop))
            partner = opponent_pop[partner_idx]
        
        # Adaptive crossover operator selection
        crossover_type = np.random.choice(['sbx', 'blx', 'arithmetic'])
        
        if crossover_type == 'sbx':
            # Simulated Binary Crossover
            eta = 20 + 10 * np.random.random()
            new_pos = self._simulated_binary_crossover_single(current_pos, partner, eta)
        elif crossover_type == 'blx':
            # BLX-alpha crossover
            alpha = 0.3 + 0.2 * np.random.random()
            new_pos = self._blx_alpha_crossover(current_pos, partner, alpha)
        else:
            # Arithmetic crossover
            weight = 0.3 + 0.4 * np.random.random()
            new_pos = weight * current_pos + (1 - weight) * partner
        
        # Add small perturbation
        perturbation = params['beta'] * np.random.randn(dim) * p
        new_pos += perturbation
        
        return new_pos
    
    def _enhanced_mutation_strategy(self, pop_pos: np.ndarray, idx: int, best_pos: np.ndarray,
                                  p: float, params: Dict[str, float], dim: int,
                                  iteration: int, max_iterations: int) -> np.ndarray:
        """Enhanced mutation strategy with adaptive operators."""
        current_pos = pop_pos[idx]
        
        # Adaptive mutation operator selection
        mutation_type = np.random.choice(['gaussian', 'polynomial', 'levy', 'boundary'])
        
        if mutation_type == 'gaussian':
            # Gaussian mutation with adaptive scale
            scale = 0.1 * (1 - iteration / max_iterations)
            mutation = np.random.randn(dim) * scale
            new_pos = current_pos + mutation
            
        elif mutation_type == 'polynomial':
            # Polynomial mutation
            eta = 20 + 10 * np.random.random()
            new_pos = self._polynomial_mutation_single(current_pos, eta)
            
        elif mutation_type == 'levy':
            # Levy flight mutation
            R = self._levy_improved(dim)
            new_pos = current_pos + R * (best_pos - current_pos) * params['alpha']
            
        else:
            # Boundary mutation
            j = np.random.randint(dim)
            new_pos = current_pos.copy()
            if np.random.random() < 0.5:
                new_pos[j] = lower_bounds[j] if 'lower_bounds' in locals() else 0
            else:
                new_pos[j] = upper_bounds[j] if 'upper_bounds' in locals() else 1
        
        return new_pos
    
    def _hybrid_strategy(self, pop_pos: np.ndarray, idx: int, best_pos: np.ndarray,
                        opponent_pop: np.ndarray, p: float, params: Dict[str, float],
                        dim: int, iteration: int, max_iterations: int) -> np.ndarray:
        """Hybrid strategy combining crossover and mutation."""
        # First apply crossover
        temp_pos = self._intelligent_crossover(pop_pos, idx, best_pos, opponent_pop, 
                                             p, params, dim)
        
        # Then apply mutation
        new_pos = self._enhanced_mutation_strategy(np.array([temp_pos]), 0, best_pos,
                                                 p, params, dim, iteration, max_iterations)
        
        return new_pos[0]
    
    def _should_accept_solution(self, new_fit: np.ndarray, current_fit: np.ndarray,
                              iteration: int, max_iterations: int) -> bool:
        """Enhanced acceptance criteria with simulated annealing."""
        if self._dominates(new_fit, current_fit):
            return True
        elif not self._dominates(current_fit, new_fit):
            # Non-dominated solutions: accept with probability
            temperature = 1.0 - iteration / max_iterations
            acceptance_prob = 0.1 * temperature
            return np.random.random() < acceptance_prob
        else:
            # Dominated solution: accept with very low probability
            return np.random.random() < 0.01
    
    def _simulated_binary_crossover_single(self, parent1: np.ndarray, parent2: np.ndarray,
                                         eta: float) -> np.ndarray:
        """Single offspring SBX crossover."""
        u = np.random.random(len(parent1))
        child = np.zeros(len(parent1))
        
        for i in range(len(parent1)):
            if u[i] <= 0.5:
                beta = (2 * u[i]) ** (1 / (eta + 1))
            else:
                beta = (1 / (2 * (1 - u[i]))) ** (1 / (eta + 1))
            
            child[i] = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
        
        return child
    
    def _blx_alpha_crossover(self, parent1: np.ndarray, parent2: np.ndarray,
                           alpha: float) -> np.ndarray:
        """BLX-alpha crossover."""
        child = np.zeros(len(parent1))
        
        for i in range(len(parent1)):
            d = abs(parent1[i] - parent2[i])
            min_val = min(parent1[i], parent2[i]) - alpha * d
            max_val = max(parent1[i], parent2[i]) + alpha * d
            child[i] = min_val + np.random.random() * (max_val - min_val)
        
        return child
    
    def _polynomial_mutation_single(self, individual: np.ndarray, eta: float) -> np.ndarray:
        """Single individual polynomial mutation."""
        mutated = individual.copy()
        
        for i in range(len(individual)):
            if np.random.random() < 0.1:  # Mutation probability
                u = np.random.random()
                if u <= 0.5:
                    delta = (2 * u) ** (1 / (eta + 1)) - 1
                else:
                    delta = 1 - (2 * (1 - u)) ** (1 / (eta + 1))
                
                mutated[i] += delta
        
        return mutated
    
    def _check_convergence(self, hypervolume_history: List[float], iteration: int, 
                          best_fitness_history: List[float] = None, pareto_size: int = 0) -> Dict[str, Any]:
        """Intelligent convergence detection with multi-dimensional analysis and adaptive restart strategies."""
        if len(hypervolume_history) < 15:
            return {'stagnant': False, 'severity': 'none', 'confidence': 0.0, 'restart_type': 'none'}
        
        # Intelligent convergence detection with enhanced multi-dimensional criteria
        
        # 1. Multi-window improvement analysis
        windows = [5, 10, 15, 20]  # Multiple time scales
        improvement_metrics = {}
        
        for window_size in windows:
            if len(hypervolume_history) >= window_size:
                window_improvement = (hypervolume_history[-1] - hypervolume_history[-window_size]) / max(hypervolume_history[-window_size], 1e-10)
                improvement_metrics[f'improvement_{window_size}'] = window_improvement
        
        # 2. Advanced variance and trend analysis with adaptive windows
        recent_window = min(10, len(hypervolume_history))
        recent_values = hypervolume_history[-recent_window:]
        
        # Dynamic variance analysis
        recent_variance = np.var(recent_values) / max(np.mean(recent_values), 1e-10)
        
        # Multi-scale trend analysis with polynomial fitting
        trend_scores = []
        for window_size in [8, 12, 16, 20]:
            if len(hypervolume_history) >= window_size:
                x = np.arange(window_size)
                y = np.array(hypervolume_history[-window_size:])
                # Use quadratic fitting for better trend detection
                coeffs = np.polyfit(x, y, 2)
                trend_score = coeffs[0] / max(y[0], 1e-10) if y[0] != 0 else 0
                trend_scores.append(trend_score)
        
        trend_improvement = np.mean(trend_scores) if trend_scores else 0
        
        # 3. Plateau detection with adaptive range analysis
        recent_range = (max(recent_values) - min(recent_values)) / max(np.mean(recent_values), 1e-10)
        
        # 4. Oscillation detection with enhanced pattern recognition
        oscillation_score = 0
        if len(hypervolume_history) >= 12:
            osc_window = min(12, len(hypervolume_history))
            osc_values = hypervolume_history[-osc_window:]
            # Enhanced oscillation detection using autocorrelation
            diffs = np.diff(osc_values)
            autocorr = np.correlate(diffs, diffs, mode='full')
            if len(autocorr) > 0:
                oscillation_score = np.max(np.abs(autocorr[len(autocorr)//2:])) / (np.var(diffs) + 1e-10)
        
        # 5. Pareto front size-based convergence assessment
        pareto_factor = 1.0
        if pareto_size > 0:
            # Adjust thresholds based on Pareto front size
            if pareto_size < 10:
                pareto_factor = 0.7  # More sensitive for small fronts
            elif pareto_size > 30:
                pareto_factor = 1.3  # Less sensitive for large fronts
        
        # 6. Adaptive thresholds with intelligent scaling
        iteration_factor = min(iteration / 150, 1.0)  # More responsive scaling
        problem_factor = 1.0
        
        # Dynamic threshold adjustment based on multiple factors
        base_threshold = 0.0001
        recent_threshold = base_threshold * (1 - 0.6 * iteration_factor) * problem_factor * pareto_factor
        medium_threshold = base_threshold * 1.5 * (1 - 0.5 * iteration_factor) * problem_factor * pareto_factor
        variance_threshold = 0.00008 * (1 + 0.7 * iteration_factor) * problem_factor
        plateau_threshold = 0.00015 * (1 - 0.3 * iteration_factor) * problem_factor * pareto_factor
        oscillation_threshold = 0.4 * (1 - 0.15 * iteration_factor)
        
        # 7. Multi-criteria decision making with adaptive weights
        criteria_weights = {
            'recent_improvement': 2.0,  # Most important
            'medium_improvement': 1.5,
            'variance': 0.9,
            'trend': 1.2,
            'plateau': 1.0,
            'oscillation': 0.8
        }
        
        # Adjust weights based on iteration progress
        if iteration_factor > 0.7:
            criteria_weights['trend'] *= 1.3  # Emphasize trends in later iterations
            criteria_weights['variance'] *= 0.8  # Reduce variance importance
        
        weighted_score = 0
        total_weight = sum(criteria_weights.values())
        
        # Multi-criteria evaluation with adaptive logic
        if 'improvement_10' in improvement_metrics and abs(improvement_metrics['improvement_10']) < recent_threshold:
            weighted_score += criteria_weights['recent_improvement']
        if 'improvement_20' in improvement_metrics and abs(improvement_metrics['improvement_20']) < medium_threshold:
            weighted_score += criteria_weights['medium_improvement']
        if recent_variance < variance_threshold:
            weighted_score += criteria_weights['variance']
        if abs(trend_improvement) < recent_threshold * 1.2:
            weighted_score += criteria_weights['trend']
        if recent_range < plateau_threshold:
            weighted_score += criteria_weights['plateau']
        if oscillation_score > oscillation_threshold:
            weighted_score += criteria_weights['oscillation']
        
        # Calculate confidence level with normalization
        confidence = min(1.0, weighted_score / total_weight)
        
        # Intelligent restart strategy selection
        if weighted_score >= 0.75 * total_weight:
            # Severe stagnation: strong evidence of convergence
            if 'improvement_10' in improvement_metrics and abs(improvement_metrics['improvement_10']) < 0.05 * recent_threshold:
                return {'stagnant': True, 'severity': 'severe', 'confidence': confidence, 'restart_type': 'full'}
            else:
                return {'stagnant': True, 'severity': 'moderate', 'confidence': confidence, 'restart_type': 'partial'}
        elif weighted_score >= 0.45 * total_weight:
            # Mild stagnation: moderate evidence of convergence
            return {'stagnant': True, 'severity': 'mild', 'confidence': confidence, 'restart_type': 'diversity_injection'}
        
        return {'stagnant': False, 'severity': 'none', 'confidence': confidence, 'restart_type': 'none'}
    
    def _partial_restart(self, tianji_pop: np.ndarray, king_pop: np.ndarray,
                        lower_bounds: np.ndarray, upper_bounds: np.ndarray,
                        n_pop: int, iteration: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        """Enhanced partial restart with adaptive diversity injection and intelligent replacement."""
        # Adaptive keep ratio based on iteration progress
        iteration_factor = min(iteration / 200, 1.0)
        keep_ratio = 0.6 - 0.2 * iteration_factor  # More aggressive replacement early on
        keep_count = max(1, int(n_pop * keep_ratio))
        
        # Enhanced fitness evaluation for multi-objective optimization
        tianji_fitness = np.array([self._dummy_objective(ind) for ind in tianji_pop])
        king_fitness = np.array([self._dummy_objective(ind) for ind in king_pop])
        
        # Sort by hypervolume contribution (for maximization)
        tianji_indices = np.argsort(-tianji_fitness)[:keep_count]
        king_indices = np.argsort(-king_fitness)[:keep_count]
        
        # Keep best individuals
        new_tianji_pop = tianji_pop[tianji_indices]
        new_king_pop = king_pop[king_indices]
        
        # Generate new individuals with enhanced diversity strategies
        new_tianji_count = n_pop - keep_count
        new_king_count = n_pop - keep_count
        
        # Use multiple sampling strategies for diversity
        if iteration_factor < 0.5:
            # Early iterations: focus on exploration
            new_tianji_samples = self._lhs_design_modified(new_tianji_count, lower_bounds, upper_bounds)
            new_king_samples = self._lhs_design_modified(new_king_count, lower_bounds, upper_bounds)
        else:
            # Later iterations: balance exploration and exploitation
            new_tianji_samples = self._hybrid_sampling(new_tianji_count, lower_bounds, upper_bounds, 
                                                      new_tianji_pop, iteration)
            new_king_samples = self._hybrid_sampling(new_king_count, lower_bounds, upper_bounds,
                                                   new_king_pop, iteration)
        
        new_tianji_pop = np.vstack([new_tianji_pop, new_tianji_samples])
        new_king_pop = np.vstack([new_king_pop, new_king_samples])
        
        # Apply small perturbations to maintain diversity
        perturbation_strength = 0.05 * (1 - 0.3 * iteration_factor)
        for i in range(keep_count, n_pop):
            perturbation = perturbation_strength * (upper_bounds - lower_bounds) * np.random.randn(len(lower_bounds))
            new_tianji_pop[i] = np.clip(new_tianji_pop[i] + perturbation, lower_bounds, upper_bounds)
            new_king_pop[i] = np.clip(new_king_pop[i] + perturbation, lower_bounds, upper_bounds)
        
        return new_tianji_pop, new_king_pop
    
    def _hybrid_sampling(self, n_samples: int, lower_bounds: np.ndarray, upper_bounds: np.ndarray,
                        existing_pop: np.ndarray = None, iteration: int = 0) -> np.ndarray:
        """Hybrid sampling strategy combining multiple methods for enhanced diversity."""
        iteration_factor = min(iteration / 200, 1.0)
        samples = []
        
        # Use multiple sampling methods based on iteration progress
        if iteration_factor < 0.3:
            # Early stage: focus on exploration
            lhs_samples = self._lhs_design_modified(n_samples, lower_bounds, upper_bounds)
            samples = lhs_samples
        elif iteration_factor < 0.7:
            # Middle stage: balanced approach
            lhs_count = int(n_samples * 0.6)
            random_count = n_samples - lhs_count
            
            lhs_samples = self._lhs_design_modified(lhs_count, lower_bounds, upper_bounds)
            random_samples = np.random.uniform(lower_bounds, upper_bounds, (random_count, len(lower_bounds)))
            samples = np.vstack([lhs_samples, random_samples])
        else:
            # Late stage: exploitation with some exploration
            if existing_pop is not None and len(existing_pop) > 0:
                # Use existing population as base for exploitation
                exploitation_count = int(n_samples * 0.4)
                exploration_count = n_samples - exploitation_count
                
                # Exploitation: sample around existing good solutions
                exploitation_samples = []
                for _ in range(exploitation_count):
                    base_solution = existing_pop[np.random.randint(len(existing_pop))]
                    perturbation = 0.1 * (upper_bounds - lower_bounds) * np.random.randn(len(lower_bounds))
                    new_sample = np.clip(base_solution + perturbation, lower_bounds, upper_bounds)
                    exploitation_samples.append(new_sample)
                
                # Exploration: use LHS for diversity
                exploration_samples = self._lhs_design_modified(exploration_count, lower_bounds, upper_bounds)
                samples = np.vstack([exploitation_samples, exploration_samples])
            else:
                samples = self._lhs_design_modified(n_samples, lower_bounds, upper_bounds)
        
        return samples
    
    def _full_restart(self, lower_bounds: np.ndarray, upper_bounds: np.ndarray,
                     n_pop: int, iteration: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        """Enhanced full restart with adaptive diversity strategies and boundary exploration."""
        iteration_factor = min(iteration / 200, 1.0)
        
        # Generate new populations using hybrid sampling
        new_tianji_pop = self._hybrid_sampling(n_pop, lower_bounds, upper_bounds, None, iteration)
        new_king_pop = self._hybrid_sampling(n_pop, lower_bounds, upper_bounds, None, iteration)
        
        # Enhanced perturbation strategies
        perturbation_probability = 0.4 * (1 - 0.5 * iteration_factor)  # Higher early on
        perturbation_strength = 0.15 * (1 - 0.3 * iteration_factor)
        
        for i in range(n_pop):
            if np.random.random() < perturbation_probability:
                # Adaptive perturbation based on iteration progress
                perturbation = perturbation_strength * (upper_bounds - lower_bounds) * np.random.randn(len(lower_bounds))
                new_tianji_pop[i] = np.clip(new_tianji_pop[i] + perturbation, lower_bounds, upper_bounds)
                new_king_pop[i] = np.clip(new_king_pop[i] + perturbation, lower_bounds, upper_bounds)
        
        # Add boundary solutions to ensure exploration of search space edges
        if iteration_factor < 0.5:
            boundary_count = min(3, n_pop // 5)
            for i in range(boundary_count):
                # Add solutions at different boundaries
                boundary_solution = lower_bounds.copy()
                boundary_solution[i % len(lower_bounds)] = upper_bounds[i % len(lower_bounds)]
                new_tianji_pop[i] = boundary_solution
                
                # Opposite boundary
                boundary_solution = upper_bounds.copy()
                boundary_solution[i % len(lower_bounds)] = lower_bounds[i % len(lower_bounds)]
                new_king_pop[i] = boundary_solution
        
        return new_tianji_pop, new_king_pop
    
    def _space_bound_improved(self, x: np.ndarray, upper_bounds: np.ndarray, 
                             lower_bounds: np.ndarray) -> np.ndarray:
        """Improved boundary handling with reflection."""
        # Ensure x is a 1D array
        x = np.asarray(x).flatten()
        
        for i in range(len(x)):
            if x[i] > upper_bounds[i]:
                x[i] = upper_bounds[i] - (x[i] - upper_bounds[i])
                if x[i] < lower_bounds[i]:
                    x[i] = lower_bounds[i]
            elif x[i] < lower_bounds[i]:
                x[i] = lower_bounds[i] + (lower_bounds[i] - x[i])
                if x[i] > upper_bounds[i]:
                    x[i] = upper_bounds[i]
        
        # Final boundary enforcement
        return np.clip(x, lower_bounds, upper_bounds)
    
    def _levy_improved(self, dim: int) -> np.ndarray:
        """Improved Levy flight step generation."""
        beta = 1.5
        sigma = (gamma(1 + beta) * np.sin(np.pi * beta / 2) / 
                (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        
        u = np.random.randn(dim) * sigma
        v = np.random.randn(dim)
        
        step = u / (np.abs(v) ** (1 / beta))
        
        # Improved step scaling
        L = 0.01 * step / (1 + np.log(1 + np.linalg.norm(step)))
        
        return L
    
    def _tournament_selection(self, population: np.ndarray, fitness: np.ndarray, 
                            tournament_size: int = 2) -> np.ndarray:
        """Perform tournament selection on a population."""
        n = len(population)
        selected_indices = []
        
        for _ in range(n):
            # Randomly select tournament participants
            participants = np.random.choice(n, tournament_size, replace=False)
            
            # Find the best participant
            best_idx = participants[0]
            for idx in participants[1:]:
                if self._dominates(fitness[idx], fitness[best_idx]):
                    best_idx = idx
                elif not self._dominates(fitness[best_idx], fitness[idx]):
                    # If non-dominated, choose randomly
                    if np.random.random() < 0.5:
                        best_idx = idx
            
            selected_indices.append(best_idx)
        
        return population[selected_indices]
    
    def _simulated_binary_crossover(self, parent1: np.ndarray, parent2: np.ndarray, 
                                  eta: float = 20) -> Tuple[np.ndarray, np.ndarray]:
        """Perform simulated binary crossover."""
        u = np.random.random(len(parent1))
        beta = np.zeros(len(parent1))
        
        for i in range(len(parent1)):
            if u[i] <= 0.5:
                beta[i] = (2 * u[i]) ** (1 / (eta + 1))
            else:
                beta[i] = (1 / (2 * (1 - u[i]))) ** (1 / (eta + 1))
        
        child1 = 0.5 * ((1 + beta) * parent1 + (1 - beta) * parent2)
        child2 = 0.5 * ((1 - beta) * parent1 + (1 + beta) * parent2)
        
        return child1, child2
    
    def _polynomial_mutation(self, individual: np.ndarray, lower_bounds: np.ndarray,
                           upper_bounds: np.ndarray, eta: float = 20) -> np.ndarray:
        """Perform polynomial mutation."""
        mutated = individual.copy()
        
        for i in range(len(individual)):
            if np.random.random() < self.mutation_rate:
                u = np.random.random()
                delta = 0.0
                
                if u <= 0.5:
                    delta = (2 * u) ** (1 / (eta + 1)) - 1
                else:
                    delta = 1 - (2 * (1 - u)) ** (1 / (eta + 1))
                
                mutated[i] = individual[i] + delta * (upper_bounds[i] - lower_bounds[i])
                mutated[i] = np.clip(mutated[i], lower_bounds[i], upper_bounds[i])
        
        return mutated
    
    def _select_diverse_solutions(self, front: np.ndarray, positions: np.ndarray, 
                                max_solutions: int) -> Tuple[np.ndarray, np.ndarray]:
        """Select diverse solutions from Pareto front using crowding distance."""
        if len(front) <= max_solutions:
            return front, positions
        
        # Calculate crowding distances
        distances = self._calculate_crowding_distance(front)
        
        # Select solutions with highest crowding distances
        selected_indices = np.argsort(distances)[-max_solutions:]
        
        return front[selected_indices], positions[selected_indices]
    
    def _apply_mutation(self, population: np.ndarray, lower_bounds: np.ndarray,
                       upper_bounds: np.ndarray, mutation_rate: float) -> np.ndarray:
        """Apply Gaussian mutation to population."""
        mutated_pop = population.copy()
        n, dim = population.shape
        
        for i in range(n):
            if np.random.random() < mutation_rate:
                # Gaussian mutation
                mutation_strength = 0.1 * (upper_bounds - lower_bounds)
                mutation = mutation_strength * np.random.randn(dim)
                mutated_pop[i] = population[i] + mutation
                
                # Boundary handling
                mutated_pop[i] = np.clip(mutated_pop[i], lower_bounds, upper_bounds)
        
        return mutated_pop
    
    def _find_pareto_front(self, fitness: np.ndarray, positions: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Find Pareto front and corresponding solution set."""
        if len(fitness) == 0:
            return np.array([]), np.array([])
        
        n = len(fitness)
        is_dominated = np.zeros(n, dtype=bool)
        
        for i in range(n):
            for j in range(n):
                if i != j and self._dominates(fitness[j], fitness[i]):
                    is_dominated[i] = True
                    break
        
        pareto_front = fitness[~is_dominated]
        pareto_set = positions[~is_dominated]
        
        return pareto_front, pareto_set


def dominates(a: np.ndarray, b: np.ndarray) -> bool:
    """Check if solution a dominates solution b.
    
    Parameters
    ----------
    a : np.ndarray
        First solution's objective values
    b : np.ndarray
        Second solution's objective values
        
    Returns
    -------
    bool
        True if a dominates b
    """
    not_worse = np.all(a <= b)
    strictly_better = np.any(a < b)
    return not_worse and strictly_better


def update_pareto_front(current_front: np.ndarray, new_solutions: np.ndarray) -> np.ndarray:
    """Update Pareto front with new solutions.
    
    Parameters
    ----------
    current_front : np.ndarray
        Current Pareto front
    new_solutions : np.ndarray
        New candidate solutions
        
    Returns
    -------
    np.ndarray
        Updated Pareto front
    """
    if len(current_front) == 0:
        return new_solutions
    
    if len(new_solutions) == 0:
        return current_front
    
    all_solutions = np.vstack([current_front, new_solutions])
    is_dominated = np.zeros(len(all_solutions), dtype=bool)
    
    for i in range(len(all_solutions)):
        for j in range(len(all_solutions)):
            if i != j and dominates(all_solutions[j], all_solutions[i]):
                is_dominated[i] = True
                break
    
    return all_solutions[~is_dominated]


def calculate_crowding_distance(fitness: np.ndarray) -> np.ndarray:
    """Calculate crowding distance for a set of solutions.
    
    Parameters
    ----------
    fitness : np.ndarray
        Objective function values for solutions
        
    Returns
    -------
    np.ndarray
        Crowding distances for each solution
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._calculate_crowding_distance(fitness)


def select_nondominated_solutions(fitness: np.ndarray, positions: np.ndarray, 
                                max_solutions: int) -> Tuple[np.ndarray, np.ndarray]:
    """Select non-dominated solutions with diversity preservation.
    
    Parameters
    ----------
    fitness : np.ndarray
        Objective function values
    positions : np.ndarray
        Decision variable values
    max_solutions : int
        Maximum number of solutions to select
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Selected fitness and positions
    """
    optimizer = MOMTHROOptimizer()
    pareto_front, pareto_set = optimizer._find_pareto_front(fitness, positions)
    
    if len(pareto_set) > max_solutions:
        selected_front, selected_set = optimizer._select_diverse_solutions(
            pareto_front, pareto_set, max_solutions
        )
        return selected_front, selected_set
    
    return pareto_front, pareto_set


def non_dominated_sort(fitness: np.ndarray) -> List[List[int]]:
    """Perform non-dominated sorting on a population.
    
    Parameters
    ----------
    fitness : np.ndarray
        Objective function values for the population
        
    Returns
    -------
    List[List[int]]
        List of fronts, each containing indices of solutions in that front
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._non_dominated_sort(fitness)[0]


def crowding_distance(fitness: np.ndarray) -> np.ndarray:
    """Calculate crowding distance for a set of solutions.
    
    Parameters
    ----------
    fitness : np.ndarray
        Objective function values
        
    Returns
    -------
    np.ndarray
        Crowding distances for each solution
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._calculate_crowding_distance(fitness)


def calculate_hypervolume(fitness: np.ndarray, reference_point: Optional[np.ndarray] = None) -> float:
    """Calculate hypervolume metric for a Pareto front.
    
    Parameters
    ----------
    fitness : np.ndarray
        Pareto front objective values
    reference_point : Optional[np.ndarray], default=None
        Reference point for hypervolume calculation (ignored, auto-selected)
        
    Returns
    -------
    float
        Hypervolume value
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._calculate_hypervolume(fitness)


def lhsdesign_modified(n: int, lower_bounds: np.ndarray, upper_bounds: np.ndarray) -> np.ndarray:
    """Generate Latin Hypercube Sample with improved space-filling properties.
    
    Parameters
    ----------
    n : int
        Number of samples
    lower_bounds : np.ndarray
        Lower bounds for each dimension
    upper_bounds : np.ndarray
        Upper bounds for each dimension
        
    Returns
    -------
    np.ndarray
        Generated samples
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._lhs_design_modified(n, lower_bounds, upper_bounds)


def tournament_selection(population: np.ndarray, fitness: np.ndarray, 
                       tournament_size: int = 2) -> np.ndarray:
    """Perform tournament selection on a population.
    
    Parameters
    ----------
    population : np.ndarray
        Population of solutions
    fitness : np.ndarray
        Objective function values
    tournament_size : int, default=2
        Size of tournament
        
    Returns
    -------
    np.ndarray
        Selected individuals
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._tournament_selection(population, fitness, tournament_size)


def simulated_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, 
                              eta: float = 20) -> Tuple[np.ndarray, np.ndarray]:
    """Perform simulated binary crossover.
    
    Parameters
    ----------
    parent1 : np.ndarray
        First parent
    parent2 : np.ndarray
        Second parent
    eta : float, default=20
        Distribution index
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Two offspring
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._simulated_binary_crossover(parent1, parent2, eta)


def polynomial_mutation(individual: np.ndarray, lower_bounds: np.ndarray,
                       upper_bounds: np.ndarray, eta: float = 20) -> np.ndarray:
    """Perform polynomial mutation.
    
    Parameters
    ----------
    individual : np.ndarray
        Individual to mutate
    lower_bounds : np.ndarray
        Lower bounds
    upper_bounds : np.ndarray
        Upper bounds
    eta : float, default=20
        Distribution index
        
    Returns
    -------
    np.ndarray
        Mutated individual
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._polynomial_mutation(individual, lower_bounds, upper_bounds, eta)


def adaptive_parameters(iteration: int, max_iterations: int, 
                       initial_params: Dict[str, float]) -> Dict[str, float]:
    """Update adaptive parameters based on iteration progress.
    
    Parameters
    ----------
    iteration : int
        Current iteration
    max_iterations : int
        Maximum iterations
    initial_params : Dict[str, float]
        Initial parameter values
        
    Returns
    -------
    Dict[str, float]
        Updated parameters
    """
    optimizer = MOMTHROOptimizer()
    return optimizer._update_adaptive_params(initial_params, iteration, max_iterations)


