"""
Optimizer module for PyXESXXN multi-carrier energy system optimization.

This module provides optimization algorithms and solvers for energy hub models.
"""

from typing import Dict, List, Any, Optional, Union
import numpy as np
import pandas as pd
from dataclasses import dataclass
from enum import Enum

from .energy_hub import EnergyHubModel


class OptimizationObjective(Enum):
    """Enumeration of optimization objectives."""
    COST = "cost"
    EMISSIONS = "emissions"
    EFFICIENCY = "efficiency"
    RELIABILITY = "reliability"
    MULTI_OBJECTIVE = "multi_objective"
    ROBUST = "robust"


@dataclass
class OptimizationConfig:
    """Configuration for optimization."""
    solver: str = "glpk"
    time_horizon: int = 24
    time_step: int = 1
    objective: OptimizationObjective = OptimizationObjective.COST
    weights: Optional[Dict[str, float]] = None
    risk_tolerance: float = 0.1
    uncertainty_scenarios: Optional[List[Dict[str, Any]]] = None
    verbose: bool = False


class HubOptimizer:
    """Optimizer for energy hub models."""
    
    def __init__(self, hub: EnergyHubModel):
        """Initialize optimizer with energy hub.
        
        Parameters
        ----------
        hub : EnergyHubModel
            Energy hub model to optimize
        """
        self.hub = hub
        self.optimization_history = []
    
    def optimize(self, config: OptimizationConfig) -> Dict[str, Any]:
        """Optimize energy hub based on configuration.
        
        Parameters
        ----------
        config : OptimizationConfig
            Optimization configuration
            
        Returns
        -------
        Dict[str, Any]
            Optimization results
        """
        if config.objective == OptimizationObjective.MULTI_OBJECTIVE:
            return self.multi_objective_optimization(
                objectives=[OptimizationObjective.COST, OptimizationObjective.EMISSIONS],
                weights=config.weights
            )
        elif config.objective == OptimizationObjective.ROBUST:
            return self.robust_optimization(
                uncertainty_scenarios=config.uncertainty_scenarios,
                risk_tolerance=config.risk_tolerance
            )
        else:
            return self.hub.optimize_energy_flow(objective=config.objective.value)
    
    def multi_objective_optimization(self, 
                                   objectives: List[Union[str, OptimizationObjective]],
                                   weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Perform multi-objective optimization.
        
        Parameters
        ----------
        objectives : List[Union[str, OptimizationObjective]]
            List of optimization objectives
        weights : Optional[Dict[str, float]], optional
            Weights for each objective
            
        Returns
        -------
        Dict[str, Any]
            Multi-objective optimization results
        """
        # Convert objectives to strings if needed
        objective_strings = []
        for obj in objectives:
            if isinstance(obj, OptimizationObjective):
                objective_strings.append(obj.value)
            else:
                objective_strings.append(obj)
        
        # Normalize weights
        normalized_weights = {}
        if weights:
            total_weight = sum(weights.values())
            if total_weight > 0:
                normalized_weights = {k: v/total_weight for k, v in weights.items()}
        else:
            # Equal weights if not specified
            normalized_weights = {obj: 1.0/len(objective_strings) for obj in objective_strings}
        
        # Perform weighted optimization
        results = {}
        
        for objective in objective_strings:
            result = self.hub.optimize_energy_flow(objective=objective)
            if result['success']:
                results[objective] = result
        
        # Combine results using weights
        combined_results = self._combine_weighted_results(results, normalized_weights)
        
        # Store optimization history
        self.optimization_history.append({
            'type': 'multi_objective',
            'objectives': objective_strings,
            'weights': normalized_weights,
            'results': combined_results
        })
        
        return combined_results
    
    def robust_optimization(self, 
                          uncertainty_scenarios: Optional[List[Dict[str, Any]]] = None,
                          risk_tolerance: float = 0.1) -> Dict[str, Any]:
        """Perform robust optimization considering uncertainties.
        
        Parameters
        ----------
        uncertainty_scenarios : Optional[List[Dict[str, Any]]], optional
            List of uncertainty scenarios
        risk_tolerance : float
            Risk tolerance level (0-1)
            
        Returns
        -------
        Dict[str, Any]
            Robust optimization results
        """
        # Generate default uncertainty scenarios if not provided
        if uncertainty_scenarios is None:
            uncertainty_scenarios = self._generate_uncertainty_scenarios()
        
        scenario_results = []
        
        # Optimize for each scenario
        for scenario in uncertainty_scenarios:
            # Apply scenario to hub configuration
            self._apply_uncertainty_scenario(scenario)
            
            # Run optimization
            result = self.hub.optimize_energy_flow()
            if result['success']:
                scenario_results.append(result)
        
        # Aggregate robust solution
        robust_result = self._aggregate_robust_solution(scenario_results, risk_tolerance)
        
        return robust_result
    
    def _generate_uncertainty_scenarios(self) -> List[Dict[str, Any]]:
        """Generate uncertainty scenarios for robust optimization.
        
        Returns
        -------
        List[Dict[str, Any]]
            List of uncertainty scenarios
        """
        scenarios = []
        
        # Load uncertainty scenarios
        base_loads = {}
        for load_id, load_config in self.hub.config.loads.items():
            if 'profile' in load_config:
                base_loads[load_id] = load_config['profile']
        
        # Generate scenarios with different load variations
        for load_factor in [0.8, 1.0, 1.2]:  # -20%, base, +20%
            scenario = {
                'load_multiplier': load_factor,
                'renewable_variability': 0.15,  # 15% variability
                'price_volatility': 0.1,  # 10% price volatility
                'component_efficiency_variation': 0.05  # 5% efficiency variation
            }
            scenarios.append(scenario)
        
        return scenarios
    
    def _apply_uncertainty_scenario(self, scenario: Dict[str, Any]) -> None:
        """Apply uncertainty scenario to hub.
        
        Parameters
        ----------
        scenario : Dict[str, Any]
            Uncertainty scenario to apply
        """
        # Apply load variations
        if 'load_multiplier' in scenario:
            multiplier = scenario['load_multiplier']
            for load_id, load_config in self.hub.config.loads.items():
                if 'profile' in load_config:
                    original_profile = load_config['profile']
                    load_config['profile'] = original_profile * multiplier
                    # Update network load
                    if load_id in self.hub.network.loads.index:
                        self.hub.network.loads.loc[load_id, 'p_set'] *= multiplier
    
    def _combine_weighted_results(self, 
                                results: Dict[str, Dict[str, Any]], 
                                weights: Dict[str, float]) -> Dict[str, Any]:
        """Combine weighted optimization results.
        
        Parameters
        ----------
        results : Dict[str, Dict[str, Any]]
            Optimization results for each objective
        weights : Dict[str, float]
            Objective weights
            
        Returns
        -------
        Dict[str, Any]
            Combined weighted results
        """
        combined = {
            'type': 'multi_objective_combined',
            'individual_results': results,
            'weighted_objective': 0,
            'combined_solution': {},
            'pareto_analysis': {}
        }
        
        # Calculate weighted objective value
        weighted_objective = 0
        for objective, result in results.items():
            if result['success'] and 'objective_value' in result:
                weighted_objective += weights.get(objective, 0) * result['objective_value']
        
        combined['weighted_objective'] = weighted_objective
        
        # Combine energy flows
        combined['energy_flows'] = {}
        for objective, result in results.items():
            if result['success'] and 'energy_flows' in result:
                for flow_type, flows in result['energy_flows'].items():
                    if flow_type not in combined['energy_flows']:
                        combined['energy_flows'][flow_type] = {}
                    
                    weight = weights.get(objective, 0)
                    for component, flow_values in flows.items():
                        if isinstance(flow_values, dict):
                            weighted_flow = {}
                            for time_period, flow in flow_values.items():
                                weighted_flow[time_period] = weight * flow
                            combined['energy_flows'][flow_type][component] = weighted_flow
        
        return combined
    
    def _aggregate_robust_solution(self, 
                                 scenario_results: List[Dict[str, Any]], 
                                 risk_tolerance: float) -> Dict[str, Any]:
        """Aggregate robust solution across scenarios.
        
        Parameters
        ----------
        scenario_results : List[Dict[str, Any]]
            Results from all uncertainty scenarios
        risk_tolerance : float
            Risk tolerance level
            
        Returns
        -------
        Dict[str, Any]
            Robust optimization result
        """
        if not scenario_results:
            return {'success': False, 'error': 'No scenario results available'}
        
        robust_result = {
            'type': 'robust_optimization',
            'num_scenarios': len(scenario_results),
            'risk_tolerance': risk_tolerance,
            'scenario_analysis': {},
            'robust_solution': {},
            'risk_assessment': {}
        }
        
        # Analyze each scenario
        for i, scenario_result in enumerate(scenario_results):
            scenario_id = f"scenario_{i}"
            robust_result['scenario_analysis'][scenario_id] = {
                'objective_value': scenario_result.get('objective_value'),
                'success': scenario_result.get('success'),
                'efficiency_metrics': scenario_result.get('efficiency_metrics', {})
            }
        
        # Calculate robust solution (e.g., worst-case, average-case, or percentile-based)
        if risk_tolerance > 0.5:
            # Conservative solution - use worst case
            robust_objective = max(r.get('objective_value', float('inf')) 
                                 for r in scenario_results if r.get('success'))
        else:
            # Aggressive solution - use average case
            successful_objectives = [r.get('objective_value', 0) 
                                   for r in scenario_results if r.get('success')]
            robust_objective = np.mean(successful_objectives) if successful_objectives else None
        
        robust_result['robust_solution']['objective_value'] = robust_objective
        
        # Risk assessment
        successful_results = [r for r in scenario_results if r.get('success')]
        if successful_results:
            objective_values = [r.get('objective_value', 0) for r in successful_results]
            robust_result['risk_assessment'] = {
                'objective_mean': np.mean(objective_values),
                'objective_std': np.std(objective_values),
                'objective_range': [min(objective_values), max(objective_values)],
                'success_rate': len(successful_results) / len(scenario_results)
            }
        
        return robust_result
