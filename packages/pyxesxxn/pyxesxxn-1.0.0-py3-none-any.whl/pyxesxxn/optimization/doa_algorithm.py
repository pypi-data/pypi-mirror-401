import numpy as np
import random
import math

def doa_algorithm(pop_size, max_iter, lb, ub, dim, fobj):
    """
    Dream Optimization Algorithm (DOA) implementation in Python
    
    Args:
        pop_size: Population size
        max_iter: Maximum number of iterations
        lb: Lower bounds for variables
        ub: Upper bounds for variables
        dim: Problem dimension
        fobj: Objective function
        
    Returns:
        fbest: Best objective function value
        sbest: Best solution
        fbest_history: History of best values over iterations
    """
    # Ensure dimensions match
    lb = np.array(lb) * np.ones(dim)
    ub = np.array(ub) * np.ones(dim)
    
    # Initialize population
    x = np.zeros((pop_size, dim))
    for i in range(pop_size):
        x[i, :] = lb + (ub - lb) * np.random.rand(dim)
    
    SELECT = list(range(pop_size))
    
    # Initialize best solutions
    sbest = np.zeros(dim)
    sbestd = np.zeros((5, dim))  # Best solution for each of 5 groups
    fbest = float('inf')
    fbestd = [float('inf')] * 5  # Best value for each of 5 groups
    fbest_history = np.zeros(max_iter)
    
    # Exploration phase (first 90% of iterations)
    for i in range(int(9 * max_iter / 10)):
        for m in range(5):
            # Determine group indices
            start_idx = int((m / 5) * pop_size)
            end_idx = int(((m + 1) / 5) * pop_size)
            
            # Update group best
            for j in range(start_idx, end_idx):
                current_fitness = fobj(x[j, :])
                if current_fitness < fbestd[m]:
                    sbestd[m, :] = x[j, :].copy()
                    fbestd[m] = current_fitness
            
            # Memory strategy and forgetting/supplementation
            for j in range(start_idx, end_idx):
                x[j, :] = sbestd[m, :].copy()  # Memory strategy
                
                # Randomly select k dimensions to modify
                k = random.randint(math.ceil(dim / (8 * (m + 1))), math.ceil(dim / (3 * (m + 1))))
                in_idx = np.random.permutation(dim)[:k]
                
                if random.random() < 0.9:
                    # Forgetting and supplementation strategy
                    for h in range(k):
                        idx = in_idx[h]
                        rand_value = random.random() * (ub[idx] - lb[idx]) + lb[idx]
                        cos_term = (math.cos(((i + max_iter / 10) * math.pi) / max_iter) + 1) / 2
                        x[j, idx] += rand_value * cos_term
                        
                        # Boundary handling
                        if x[j, idx] > ub[idx] or x[j, idx] < lb[idx]:
                            if dim > 15:
                                # Select from other individuals
                                select = SELECT.copy()
                                select.remove(j)
                                sel = random.choice(select)
                                x[j, idx] = x[sel, idx]
                            else:
                                # Random value within bounds
                                x[j, idx] = random.random() * (ub[idx] - lb[idx]) + lb[idx]
                else:
                    # Random replacement from population
                    for h in range(k):
                        idx = in_idx[h]
                        random_individual = random.randint(0, pop_size - 1)
                        x[j, idx] = x[random_individual, idx]
            
            # Update global best
            if fbestd[m] < fbest:
                fbest = fbestd[m]
                sbest = sbestd[m, :].copy()
        
        fbest_history[i] = fbest
    
    # Exploitation phase (last 10% of iterations)
    for i in range(int(9 * max_iter / 10), max_iter):
        # Update global best
        for p in range(pop_size):
            current_fitness = fobj(x[p, :])
            if current_fitness < fbest:
                sbest = x[p, :].copy()
                fbest = current_fitness
        
        # Local search around best solution
        for j in range(pop_size):
            km = max(2, math.ceil(dim / 3))
            k = random.randint(2, km)
            x[j, :] = sbest.copy()
            
            in_idx = np.random.permutation(dim)[:k]
            
            for h in range(k):
                idx = in_idx[h]
                rand_value = random.random() * (ub[idx] - lb[idx]) + lb[idx]
                cos_term = (math.cos((i * math.pi) / max_iter) + 1) / 2
                x[j, idx] += rand_value * cos_term
                
                # Boundary handling
                if x[j, idx] > ub[idx] or x[j, idx] < lb[idx]:
                    if dim > 15:
                        # Select from other individuals
                        select = SELECT.copy()
                        select.remove(j)
                        sel = random.choice(select)
                        x[j, idx] = x[sel, idx]
                    else:
                        # Random value within bounds
                        x[j, idx] = random.random() * (ub[idx] - lb[idx]) + lb[idx]
        
        fbest_history[i] = fbest
    
    return fbest, sbest, fbest_history