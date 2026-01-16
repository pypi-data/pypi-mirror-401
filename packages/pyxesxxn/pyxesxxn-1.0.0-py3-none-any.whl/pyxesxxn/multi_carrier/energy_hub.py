"""
Energy Hub Models for Multi-Carrier Energy Systems.

This module provides comprehensive energy hub modeling capabilities including:
- Energy hub configuration and optimization
- Multi-input/multi-output energy conversion systems
- Coupled optimization constraints
- Energy flow optimization
- Hub performance assessment
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
import warnings

try:
    import pypsa
    PYPSA_AVAILABLE = True
except ImportError:
    warnings.warn("PyPSA not available", UserWarning)
    PYPSA_AVAILABLE = False

# Import base modules  
from .base import (
    MultiCarrierConverter, 
    EnergyCarrier, 
    ConverterConfiguration, 
    ConverterType
)
from .converters import ElectrolyzerConverter, FuelCellConverter, HeatPumpConverter


class HubConfiguration:
    """Configuration for energy hub components and constraints."""
    
    def __init__(self, 
                 hub_id: str,
                 location: Optional[str] = None,
                 coordinate: Optional[Tuple[float, float]] = None,
                 operating_horizon: Optional[pd.DatetimeIndex] = None):
        """Initialize hub configuration.
        
        Parameters
        ----------
        hub_id : str
            Unique hub identifier
        location : str, optional
            Physical location description
        coordinate : Tuple[float, float], optional
            Geographic coordinates (lat, lon)
        operating_horizon : pd.DatetimeIndex, optional
            Operating time periods
        """
        self.hub_id = hub_id
        self.location = location
        self.coordinate = coordinate
        self.operating_horizon = operating_horizon
        
        # Hub components
        self.converters: List[MultiCarrierConverter] = []
        self.storage_units: Dict[str, Any] = {}
        self.renewable_sources: Dict[str, Any] = {}
        self.loads: Dict[str, Any] = {}
        self.sensors: Dict[str, Any] = {}
        
        # Hub constraints
        self.power_limits: Dict[str, float] = {}
        self.energy_limits: Dict[str, float] = {}
        self.emission_limits: Optional[Dict[str, float]] = None
        self.cost_limits: Optional[Dict[str, float]] = None
        
        # Hub operating parameters
        self.dispatch_strategy = "economic"  # economic, environmental, reliability
        self.response_time = 1.0  # seconds
        self.efficiency_threshold = 0.7
        self.availability_requirement = 0.95
    
    def add_converter(self, converter: MultiCarrierConverter) -> None:
        """Add converter to hub.
        
        Parameters
        ----------
        converter : MultiCarrierConverter
            Converter to add to hub
        """
        self.converters.append(converter)
    
    def add_storage(self, storage_id: str, storage_config: Dict[str, Any]) -> None:
        """Add storage unit to hub.
        
        Parameters
        ----------
        storage_id : str
            Storage unit identifier
        storage_config : Dict[str, Any]
            Storage configuration
        """
        self.storage_units[storage_id] = storage_config
    
    def add_load(self, load_id: str, load_profile: Union[pd.Series, np.ndarray]) -> None:
        """Add load to hub.
        
        Parameters
        ----------
        load_id : str
            Load identifier
        load_profile : Union[pd.Series, np.ndarray]
            Load profile over time
        """
        self.loads[load_id] = {
            'profile': load_profile,
            'type': 'time_varying',
            'priority': 'normal'
        }
    
    def add_renewable_source(self, source_id: str, source_config: Dict[str, Any]) -> None:
        """Add renewable source to hub.
        
        Parameters
        ----------
        source_id : str
            Renewable source identifier
        source_config : Dict[str, Any]
            Source configuration and parameters
        """
        self.renewable_sources[source_id] = source_config
    
    def set_emission_limits(self, emission_limits: Dict[str, float]) -> None:
        """Set emission limits for hub.
        
        Parameters
        ----------
        emission_limits : Dict[str, float]
            Emission limits by carrier type (kg CO2eq/MWh)
        """
        self.emission_limits = emission_limits
    
    def set_cost_limits(self, cost_limits: Dict[str, float]) -> None:
        """Set cost limits for hub.
        
        Parameters
        ----------
        cost_limits : Dict[str, float]
            Cost limits (€/MWh)
        """
        self.cost_limits = cost_limits


class EnergyHubModel:
    """Energy Hub Model for multi-carrier energy system optimization."""
    
    def __init__(self, 
                 configuration: HubConfiguration,
                 network: Optional['pypsa.Network'] = None):
        """Initialize energy hub model.
        
        Parameters
        ----------
        configuration : HubConfiguration
            Hub configuration
        network : pypsa.Network, optional
            PyPSA network to integrate with
        """
        self.config = configuration
        self.network = network
        
        # Hub state
        self.energy_balance = {}
        self.power_flows = {}
        self.operating_state = {}
        self.performance_metrics = {}
        
        # Optimization results
        self.optimization_results = {}
        self.dispatch_schedule = {}
        self.cost_analysis = {}
        
        # Initialize model
        self._initialize_hub_model()
    
    def _initialize_hub_model(self) -> None:
        """Initialize internal hub model components."""
        # Create internal network if not provided
        if self.network is None:
            self.network = pypsa.Network()
            self._create_internal_network()
        
        # Add converters to network
        for converter in self.config.converters:
            self._add_converter_to_network(converter)
        
        # Add storage units
        for storage_id, storage_config in self.config.storage_units.items():
            self._add_storage_to_network(storage_id, storage_config)
        
        # Add loads
        for load_id, load_config in self.config.loads.items():
            self._add_load_to_network(load_id, load_config)
    
    def _create_internal_network(self) -> None:
        """Create internal energy hub network."""
        # Add bus for each energy carrier
        carriers = self._get_hub_energy_carriers()
        for carrier in carriers:
            bus_id = f"{carrier.value}_bus"
            self.network.add("Bus", 
                           bus_id,
                           v_nom=1.0,  # Normalized voltage
                           carrier=carrier.value)
    
    def _get_hub_energy_carriers(self) -> List[EnergyCarrier]:
        """Get all energy carriers present in hub."""
        carriers = set()
        for converter in self.config.converters:
            carriers.add(converter.input_carrier)
            carriers.add(converter.output_carrier)
        return list(carriers)
    
    def _add_converter_to_network(self, converter: MultiCarrierConverter) -> None:
        """Add converter to internal network.
        
        Parameters
        ----------
        converter : MultiCarrierConverter
            Converter to add
        """
        # Create buses for converter
        input_bus = f"{converter.input_carrier.value}_bus"
        output_bus = f"{converter.output_carrier.value}_bus"
        
        # Ensure buses exist
        if input_bus not in self.network.buses.index:
            self.network.add("Bus", input_bus, v_nom=1.0, carrier=converter.input_carrier.value)
        
        if output_bus not in self.network.buses.index:
            self.network.add("Bus", output_bus, v_nom=1.0, carrier=converter.output_carrier.value)
        
        # Add converter as link
        self.network.add("Link",
                        converter.converter_id,
                        bus0=input_bus,
                        bus1=output_bus,
                        efficiency=converter.config.get_efficiency(),
                        p_nom=converter.config.power_rating,
                        carrier_in=converter.input_carrier.value,
                        carrier_out=converter.output_carrier.value)
    
    def _add_storage_to_network(self, storage_id: str, storage_config: Dict[str, Any]) -> None:
        """Add storage unit to internal network.
        
        Parameters
        ----------
        storage_id : str
            Storage unit identifier
        storage_config : Dict[str, Any]
            Storage configuration
        """
        carrier = storage_config.get('carrier', 'electricity')
        bus_id = f"{carrier}_bus"
        
        # Ensure bus exists
        if bus_id not in self.network.buses.index:
            self.network.add("Bus", bus_id, v_nom=1.0, carrier=carrier)
        
        # Add storage unit
        self.network.add("StorageUnit",
                        storage_id,
                        bus=bus_id,
                        p_nom=storage_config.get('power_rating', 100),  # kW
                        energy_capacity=storage_config.get('energy_capacity', 400),  # kWh
                        efficiency_store=storage_config.get('efficiency_store', 0.9),
                        efficiency_dispatch=storage_config.get('efficiency_dispatch', 0.9),
                        marginal_cost=storage_config.get('marginal_cost', 0),
                        carrier=carrier)
    
    def _add_load_to_network(self, load_id: str, load_config: Dict[str, Any]) -> None:
        """Add load to internal network.
        
        Parameters
        ----------
        load_id : str
            Load identifier
        load_config : Dict[str, Any]
            Load configuration
        """
        carrier = load_config.get('carrier', 'electricity')
        bus_id = f"{carrier}_bus"
        
        # Ensure bus exists
        if bus_id not in self.network.buses.index:
            self.network.add("Bus", bus_id, v_nom=1.0, carrier=carrier)
        
        # Add load
        load_profile = load_config.get('profile', np.zeros(24))  # Default 24h profile
        p_set = np.mean(load_profile)  # Use average as set point
        
        self.network.add("Load",
                        load_id,
                        bus=bus_id,
                        p_set=p_set,
                        carrier=carrier)
        
        # Store load profile for time-series optimization
        load_config['time_series'] = load_profile
    
    def optimize_energy_flow(self, 
                           objective: str = "cost",
                           time_periods: Optional[List[str]] = None,
                           constraints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Optimize energy flow within hub.
        
        Parameters
        ----------
        objective : str
            Optimization objective: "cost", "emissions", "efficiency", "reliability"
        time_periods : List[str], optional
            Time periods to optimize
        constraints : Dict[str, Any], optional
            Additional constraints
            
        Returns
        -------
        Dict[str, Any]
            Optimization results
        """
        # Set up optimization
        if time_periods is not None:
            self._setup_time_series_optimization(time_periods)
        
        # Apply objective function
        self._set_optimization_objective(objective)
        
        # Apply constraints
        if constraints:
            self._apply_additional_constraints(constraints)
        
        # Run optimization
        try:
            self.network.optimize()
            optimization_success = True
        except Exception as e:
            optimization_success = False
            optimization_error = str(e)
            return {
                'success': False,
                'error': optimization_error,
                'hub_id': self.config.hub_id
            }
        
        # Extract results
        self.optimization_results = self._extract_optimization_results()
        
        return {
            'success': True,
            'hub_id': self.config.hub_id,
            'objective_value': self.optimization_results.get('objective_value'),
            'energy_flows': self.optimization_results.get('energy_flows'),
            'converter_utilization': self.optimization_results.get('converter_utilization'),
            'storage_operations': self.optimization_results.get('storage_operations'),
            'cost_breakdown': self.optimization_results.get('cost_breakdown'),
            'emissions': self.optimization_results.get('emissions'),
            'efficiency_metrics': self.optimization_results.get('efficiency_metrics')
        }
    
    def _setup_time_series_optimization(self, time_periods: List[str]) -> None:
        """Set up time series optimization.
        
        Parameters
        ----------
        time_periods : List[str]
            Time periods for optimization
        """
        # Set up time index
        self.network.set_snapshots(pd.DatetimeIndex(time_periods))
        
        # Add time series data for loads
        for load_id, load_config in self.config.loads.items():
            if 'time_series' in load_config:
                # Extend or repeat time series to match time periods
                time_series = load_config['time_series']
                if len(time_series) < len(time_periods):
                    # Repeat pattern if needed
                    repeats = int(np.ceil(len(time_periods) / len(time_series)))
                    extended_series = np.tile(time_series, repeats)[:len(time_periods)]
                else:
                    extended_series = time_series[:len(time_periods)]
                
                # Update load time series in network
                if load_id in self.network.loads.index:
                    self.network.loads_t.p_set.loc[time_periods, load_id] = extended_series
    
    def _set_optimization_objective(self, objective: str) -> None:
        """Set optimization objective function.
        
        Parameters
        ----------
        objective : str
            Optimization objective
        """
        if objective == "cost":
            # Minimize total system cost
            pass  # PyPSA minimizes marginal costs by default
        
        elif objective == "emissions":
            # Add emission costs to marginal costs
            emission_factors = self._get_emission_factors()
            for comp_type in ['generators', 'links', 'storage_units']:
                if comp_type in self.network.components:
                    comp_df = getattr(self.network, comp_type)
                    if not comp_df.empty and 'marginal_cost' in comp_df.columns:
                        for idx in comp_df.index:
                            carrier = comp_df.loc[idx, 'carrier']
                            if carrier in emission_factors:
                                emission_cost = emission_factors[carrier] * 50  # €50/tonne CO2
                                comp_df.loc[idx, 'marginal_cost'] += emission_cost
        
        elif objective == "efficiency":
            # Favor high efficiency operations
            # This would require custom objective function
            pass
        
        elif objective == "reliability":
            # Add reliability costs/constraints
            pass
    
    def _get_emission_factors(self) -> Dict[str, float]:
        """Get emission factors for different energy carriers.
        
        Returns
        -------
        Dict[str, float]
            Emission factors in kg CO2eq/kWh
        """
        return {
            'electricity': 0.4,  # Grid electricity
            'natural_gas': 0.2,
            'hydrogen': 0.0,    # Green hydrogen
            'solar': 0.0,
            'wind': 0.0,
            'biomass': 0.05,
            'coal': 0.8
        }
    
    def _apply_additional_constraints(self, constraints: Dict[str, Any]) -> None:
        """Apply additional constraints to optimization.
        
        Parameters
        ----------
        constraints : Dict[str, Any]
            Additional constraints
        """
        # Emission limits
        if 'max_emissions' in constraints:
            max_emissions = constraints['max_emissions']
            # This would require custom constraint implementation
            pass
        
        # Power limits
        if 'max_power' in constraints:
            for converter_id, max_power in constraints['max_power'].items():
                if converter_id in self.network.links.index:
                    self.network.links.loc[converter_id, 'p_nom'] = max_power
        
        # Storage limits
        if 'storage_limits' in constraints:
            for storage_id, limits in constraints['storage_limits'].items():
                if storage_id in self.network.storage_units.index:
                    if 'max_capacity' in limits:
                        self.network.storage_units.loc[storage_id, 'energy_capacity'] = limits['max_capacity']
    
    def _extract_optimization_results(self) -> Dict[str, Any]:
        """Extract and process optimization results.
        
        Returns
        -------
        Dict[str, Any]
            Processed optimization results
        """
        results = {}
        
        # Extract objective value
        if hasattr(self.network, 'objective_value'):
            results['objective_value'] = self.network.objective_value
        
        # Extract energy flows
        results['energy_flows'] = self._extract_energy_flows()
        
        # Extract converter utilization
        results['converter_utilization'] = self._extract_converter_utilization()
        
        # Extract storage operations
        results['storage_operations'] = self._extract_storage_operations()
        
        # Calculate cost breakdown
        results['cost_breakdown'] = self._calculate_cost_breakdown()
        
        # Calculate emissions
        results['emissions'] = self._calculate_emissions()
        
        # Calculate efficiency metrics
        results['efficiency_metrics'] = self._calculate_efficiency_metrics()
        
        return results
    
    def _extract_energy_flows(self) -> Dict[str, Any]:
        """Extract energy flow results."""
        flows = {}
        
        # Link flows (converters)
        if not self.network.links_t.p0.empty:
            flows['converter_flows'] = self.network.links_t.p0.to_dict()
        
        # Generator outputs
        if not self.network.generators_t.p.empty:
            flows['generator_outputs'] = self.network.generators_t.p.to_dict()
        
        # Storage flows
        if not self.network.storage_units_t.p0.empty:
            flows['storage_flows'] = self.network.storage_units_t.p0.to_dict()
        
        return flows
    
    def _extract_converter_utilization(self) -> Dict[str, float]:
        """Extract converter utilization rates."""
        utilization = {}
        
        for converter in self.config.converters:
            if converter.converter_id in self.network.links.index:
                rated_power = self.network.links.loc[converter.converter_id, 'p_nom']
                avg_flow = self.network.links_t.p0[converter.converter_id].mean()
                utilization[converter.converter_id] = avg_flow / rated_power if rated_power > 0 else 0
        
        return utilization
    
    def _extract_storage_operations(self) -> Dict[str, Any]:
        """Extract storage operation results."""
        storage_ops = {}
        
        for storage_id in self.network.storage_units.index:
            storage_ops[storage_id] = {
                'charge_power': self.network.storage_units_t.p0[storage_id].to_dict(),
                'discharge_power': self.network.storage_units_t.p1[storage_id].to_dict(),
                'state_of_charge': self.network.storage_units_t.state_of_charge[storage_id].to_dict(),
                'capacity_utilization': (
                    self.network.storage_units_t.state_of_charge[storage_id].std() / 
                    self.network.storage_units.loc[storage_id, 'energy_capacity']
                ) if storage_id in self.network.storage_units_t.state_of_charge.columns else 0
            }
        
        return storage_ops
    
    def _calculate_cost_breakdown(self) -> Dict[str, float]:
        """Calculate cost breakdown by component."""
        cost_breakdown = {}
        
        # Operational costs
        total_cost = 0
        for comp_type in ['generators', 'links', 'storage_units']:
            if comp_type in self.network.components:
                comp_df = getattr(self.network, comp_type)
                if not comp_df.empty and 'marginal_cost' in comp_df.columns:
                    for idx in comp_df.index:
                        if comp_type == 'generators':
                            flow = self.network.generators_t.p[idx].sum()
                        elif comp_type == 'links':
                            flow = self.network.links_t.p0[idx].sum()
                        elif comp_type == 'storage_units':
                            flow = abs(self.network.storage_units_t.p0[idx].sum())
                        
                        cost = comp_df.loc[idx, 'marginal_cost'] * flow
                        component_name = f"{comp_type}_{idx}"
                        cost_breakdown[component_name] = cost
                        total_cost += cost
        
        cost_breakdown['total'] = total_cost
        return cost_breakdown
    
    def _calculate_emissions(self) -> Dict[str, float]:
        """Calculate emissions by carrier."""
        emissions = {}
        emission_factors = self._get_emission_factors()
        
        # Calculate emissions from generator outputs
        if not self.network.generators_t.p.empty:
            for generator in self.network.generators.index:
                carrier = self.network.generators.loc[generator, 'carrier']
                if carrier in emission_factors:
                    energy_output = self.network.generators_t.p[generator].sum()
                    emission_factor = emission_factors[carrier]
                    emissions[generator] = energy_output * emission_factor / 1000  # Convert to tonnes
        
        return emissions
    
    def _calculate_efficiency_metrics(self) -> Dict[str, float]:
        """Calculate system efficiency metrics."""
        metrics = {}
        
        # Overall system efficiency
        total_input_energy = 0.0
        total_output_energy = 0.0
        total_converter_loss = 0.0
        
        # Calculate input/output energies from converters with proper energy accounting
        for converter in self.config.converters:
            if converter.converter_id in self.network.links.index:
                # Get converter efficiency
                efficiency = self.network.links.loc[converter.converter_id, 'efficiency']
                metrics[f"{converter.converter_id}_efficiency"] = efficiency
                
                # Calculate actual input and output energies
                if not self.network.links_t.p0.empty:
                    input_energy = self.network.links_t.p0[converter.converter_id].sum()
                    output_energy = self.network.links_t.p1[converter.converter_id].sum()
                    
                    # Proper energy accounting: converters consume energy (negative p0)
                    if input_energy < 0:  # Energy consumption
                        total_input_energy += abs(input_energy)
                    if output_energy > 0:  # Energy production
                        total_output_energy += output_energy
                    
                    # Calculate converter losses
                    converter_loss = abs(input_energy) - output_energy
                    if converter_loss > 0:
                        total_converter_loss += converter_loss
                    
                    metrics[f"{converter.converter_id}_input_energy"] = abs(input_energy)
                    metrics[f"{converter.converter_id}_output_energy"] = output_energy
                    metrics[f"{converter.converter_id}_loss"] = converter_loss
        
        # Calculate storage energy flows
        storage_charging = 0
        storage_discharging = 0
        for storage_id in self.network.storage_units.index:
            if not self.network.storage_units_t.p0.empty:
                storage_charging += abs(self.network.storage_units_t.p0[storage_id].sum())
                storage_discharging += self.network.storage_units_t.p1[storage_id].sum()
        
        # Calculate hub-level efficiency with proper energy accounting
        if total_input_energy > 0:
            metrics['overall_efficiency'] = total_output_energy / total_input_energy
            # Energy utilization ratio
            metrics['energy_utilization_ratio'] = (total_output_energy + storage_charging) / total_input_energy
            # Storage efficiency
            if storage_charging > 0:
                metrics['storage_efficiency'] = storage_discharging / storage_charging
            else:
                metrics['storage_efficiency'] = 0
            # Energy balance ratio (should be close to 1 for balanced systems)
            metrics['energy_balance_ratio'] = (total_output_energy + storage_charging + total_converter_loss) / total_input_energy
        else:
            metrics['overall_efficiency'] = 0.0
            metrics['energy_utilization_ratio'] = 0.0
            metrics['storage_efficiency'] = 0.0
            metrics['energy_balance_ratio'] = 0.0
            
        # Add energy balance metrics
        metrics['total_input_energy'] = total_input_energy
        metrics['total_output_energy'] = total_output_energy
        metrics['energy_loss'] = total_converter_loss
        metrics['storage_charging'] = storage_charging
        metrics['storage_discharging'] = storage_discharging
        
        return metrics
    
    def get_hub_status(self) -> Dict[str, Any]:
        """Get current hub operational status.
        
        Returns
        -------
        Dict[str, Any]
            Current hub status
        """
        status = {
            'hub_id': self.config.hub_id,
            'location': self.config.location,
            'operating_horizon': len(self.config.operating_horizon) if self.config.operating_horizon else 'continuous',
            'components': {
                'converters': len(self.config.converters),
                'storage_units': len(self.config.storage_units),
                'loads': len(self.config.loads),
                'renewable_sources': len(self.config.renewable_sources)
            },
            'constraints': {
                'power_limits': len(self.config.power_limits),
                'energy_limits': len(self.config.energy_limits),
                'has_emission_limits': self.config.emission_limits is not None,
                'has_cost_limits': self.config.cost_limits is not None
            },
            'network_components': {
                'buses': len(self.network.buses),
                'links': len(self.network.links),
                'generators': len(self.network.generators),
                'storage_units': len(self.network.storage_units),
                'loads': len(self.network.loads)
            }
        }
        
        # Add current energy balances if available
        if self.optimization_results:
            status['last_optimization'] = {
                'success': True,
                'objective_value': self.optimization_results.get('objective_value'),
                'conversion_efficiency': self.optimization_results.get('efficiency_metrics', {})
            }
        
        return status
    
    def export_configuration(self) -> Dict[str, Any]:
        """Export hub configuration.
        
        Returns
        -------
        Dict[str, Any]
            Hub configuration for serialization
        """
        config_export = {
            'hub_id': self.config.hub_id,
            'location': self.config.location,
            'coordinate': self.config.coordinate,
            'operating_horizon': self.config.operating_horizon.tolist() if self.config.operating_horizon is not None else None,
            'converters': [],
            'storage_units': self.config.storage_units,
            'loads': {k: {'type': v['type'], 'priority': v['priority']} for k, v in self.config.loads.items()},
            'renewable_sources': self.config.renewable_sources,
            'constraints': {
                'power_limits': self.config.power_limits,
                'energy_limits': self.config.energy_limits,
                'emission_limits': self.config.emission_limits,
                'cost_limits': self.config.cost_limits
            },
            'operating_parameters': {
                'dispatch_strategy': self.config.dispatch_strategy,
                'response_time': self.config.response_time,
                'efficiency_threshold': self.config.efficiency_threshold,
                'availability_requirement': self.config.availability_requirement
            }
        }
        
        # Export converter configurations
        for converter in self.config.converters:
            converter_export = {
                'converter_id': converter.converter_id,
                'converter_type': converter.config.converter_type.value,
                'power_rating': converter.config.power_rating,
                'efficiency': converter.config.get_efficiency(),
                'input_carrier': converter.input_carrier.value,
                'output_carrier': converter.output_carrier.value,
                'location': converter.location,
                'investment_costs': converter.config.investment_costs,
                'lifetime': converter.config.lifetime
            }
            config_export['converters'].append(converter_export)
        
        return config_export


class HubOptimizer:
    """Advanced optimization algorithms for energy hubs."""
    
    def __init__(self, hub_model: EnergyHubModel):
        """Initialize hub optimizer.
        
        Parameters
        ----------
        hub_model : EnergyHubModel
            Energy hub model to optimize
        """
        self.hub = hub_model
        self.optimization_history = []
        self.performance_metrics = {}
    
    def multi_objective_optimization(self, 
                                   objectives: List[str] = None,
                                   weights: Dict[str, float] = None) -> Dict[str, Any]:
        """Perform multi-objective optimization.
        
        Parameters
        ----------
        objectives : List[str], optional
            List of objectives to optimize
        weights : Dict[str, float], optional
            Weights for each objective
            
        Returns
        -------
        Dict[str, Any]
            Multi-objective optimization results
        """
        if objectives is None:
            objectives = ["cost", "efficiency", "emissions"]
        
        if weights is None:
            weights = {"cost": 0.4, "efficiency": 0.3, "emissions": 0.3}
        
        # Normalize weights
        total_weight = sum(weights.values())
        normalized_weights = {obj: w/total_weight for obj, w in weights.items()}
        
        # Perform weighted optimization
        results = {}
        
        for objective in objectives:
            result = self.hub.optimize_energy_flow(objective=objective)
            if result['success']:
                results[objective] = result
        
        # Combine results using weights
        combined_results = self._combine_weighted_results(results, normalized_weights)
        
        # Store optimization history
        self.optimization_history.append({
            'type': 'multi_objective',
            'objectives': objectives,
            'weights': normalized_weights,
            'results': combined_results
        })
        
        return combined_results
    
    def robust_optimization(self, 
                          uncertainty_scenarios: List[Dict[str, Any]] = None,
                          risk_tolerance: float = 0.1) -> Dict[str, Any]:
        """Perform robust optimization considering uncertainties.
        
        Parameters
        ----------
        uncertainty_scenarios : List[Dict[str, Any]], optional
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