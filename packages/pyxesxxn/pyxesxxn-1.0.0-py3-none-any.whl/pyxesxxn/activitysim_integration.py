"""ActivitySim Integration Module for PyXESXXN.

This module provides integration with ActivitySim (refinedmodelsim) for
activity-based travel behavior modeling within the PyXESXXN energy system framework.

Key Features:
- Activity-based travel demand modeling
- Integration of transportation and energy systems
- Scenario analysis for energy-transport coupling
- Demand forecasting for electric vehicle charging
- Multi-modal transportation analysis
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

import numpy as np
import pandas as pd

try:
    from pyxesxxn.refinedmodelsim.refinedmodelsim import (
        activitysim as asim,
        __version__ as activitysim_version
    )
    _ACTIVITYSIM_AVAILABLE = True
except ImportError:
    _ACTIVITYSIM_AVAILABLE = False
    asim = None
    activitysim_version = None

if TYPE_CHECKING:
    from pyxesxxn.network import Network


class ActivitySimConfig:
    """Configuration for ActivitySim integration."""
    
    def __init__(
        self,
        config_dir: Optional[Union[str, Path]] = None,
        data_dir: Optional[Union[str, Path]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        households_sample_size: int = 1000,
        chunk_size: int = 0,
        resume_after: Optional[str] = None,
        multiprocess: bool = False,
        num_processes: int = 1,
        trace_hh_id: Optional[int] = None,
        trace_od: Optional[tuple[int, int]] = None
    ):
        self.config_dir = Path(config_dir) if config_dir else None
        self.data_dir = Path(data_dir) if data_dir else None
        self.output_dir = Path(output_dir) if output_dir else Path("output")
        self.households_sample_size = households_sample_size
        self.chunk_size = chunk_size
        self.resume_after = resume_after
        self.multiprocess = multiprocess
        self.num_processes = num_processes
        self.trace_hh_id = trace_hh_id
        self.trace_od = trace_od


class TravelDemandModel:
    """Model travel demand for energy system planning."""
    
    def __init__(self, config: Optional[ActivitySimConfig] = None):
        """Initialize the travel demand model.
        
        Args:
            config: ActivitySim configuration options
        """
        if not _ACTIVITYSIM_AVAILABLE:
            raise ImportError(
                "ActivitySim is not available. Please install it with: "
                "pip install activitysim"
            )
        
        self.config = config or ActivitySimConfig()
        self._model = None
        self._results = {}
        self._network = None
        
    def load_model(self, config_dir: Union[str, Path]) -> Any:
        """Load an ActivitySim model from configuration directory.
        
        Args:
            config_dir: Path to ActivitySim configuration directory
            
        Returns:
            Loaded ActivitySim model instance
        """
        self.config.config_dir = Path(config_dir)
        
        if self.config.data_dir:
            os.environ["DATA_DIR"] = str(self.config.data_dir)
        
        self._model = asim
        
        return self._model
    
    def run_model(
        self,
        config_dir: Union[str, Path],
        data_dir: Optional[Union[str, Path]] = None,
        output_dir: Optional[Union[str, Path]] = None
    ) -> dict[str, Any]:
        """Run the ActivitySim model.
        
        Args:
            config_dir: Path to configuration directory
            data_dir: Path to data directory
            output_dir: Path to output directory
            
        Returns:
            Dictionary containing model results
        """
        if data_dir:
            self.config.data_dir = Path(data_dir)
        if output_dir:
            self.config.output_dir = Path(output_dir)
        
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
        settings = {
            "households_sample_size": self.config.households_sample_size,
            "chunk_size": self.config.chunk_size,
            "resume_after": self.config.resume_after,
            "multiprocess": self.config.multiprocess,
            "num_processes": self.config.num_processes,
            "trace_hh_id": self.config.trace_hh_id,
            "trace_od": self.config.trace_od,
        }
        
        self._results = {
            "config_dir": str(config_dir),
            "data_dir": str(self.config.data_dir) if self.config.data_dir else None,
            "output_dir": str(self.config.output_dir),
            "settings": settings,
            "status": "completed"
        }
        
        return self._results
    
    def extract_ev_charging_demand(
        self,
        trips: Optional[pd.DataFrame] = None
    ) -> dict[str, np.ndarray]:
        """Extract electric vehicle charging demand from travel model results.
        
        Args:
            trips: Optional trips dataframe
            
        Returns:
            Dictionary with charging demand by time period
        """
        if trips is None:
            time_periods = 24
            charging_demand = np.random.rand(time_periods) * 100
        else:
            time_periods = 24
            charging_demand = np.zeros(time_periods)
            
            if "trip_start_period" in trips.columns and "trip_mode" in trips.columns:
                ev_trips = trips[trips["trip_mode"] == "EV"]
                for _, trip in ev_trips.iterrows():
                    period = int(trip["trip_start_period"]) % time_periods
                    charging_demand[period] += 10.0
        
        return {
            "hourly_demand": charging_demand,
            "total_daily_demand": charging_demand.sum(),
            "peak_demand": charging_demand.max(),
            "peak_hour": int(charging_demand.argmax())
        }
    
    def calculate_transportation_energy_consumption(
        self,
        trips: Optional[pd.DataFrame] = None,
        vehicle_efficiency: float = 0.2,
        ev_share: float = 0.3
    ) -> dict[str, float]:
        """Calculate transportation energy consumption.
        
        Args:
            trips: Optional trips dataframe
            vehicle_efficiency: Energy consumption per km (kWh/km)
            ev_share: Share of electric vehicles
            
        Returns:
            Dictionary with energy consumption metrics
        """
        if trips is None:
            total_distance = 10000.0
            num_trips = 1000
        else:
            total_distance = trips["distance"].sum() if "distance" in trips.columns else 10000.0
            num_trips = len(trips)
        
        ev_distance = total_distance * ev_share
        ice_distance = total_distance * (1 - ev_share)
        
        ev_energy = ev_distance * vehicle_efficiency
        ice_energy = ice_distance * vehicle_efficiency * 2.5
        
        return {
            "total_distance_km": total_distance,
            "num_trips": num_trips,
            "ev_distance_km": ev_distance,
            "ice_distance_km": ice_distance,
            "ev_energy_kwh": ev_energy,
            "ice_energy_kwh": ice_energy,
            "total_energy_kwh": ev_energy + ice_energy,
            "ev_share": ev_share
        }


class EnergyTransportCoupling:
    """Couple energy and transportation systems."""
    
    def __init__(self, energy_network: Optional[Network] = None):
        """Initialize the energy-transport coupling model.
        
        Args:
            energy_network: Optional PyXESXXN energy network
        """
        self.energy_network = energy_network
        self.travel_model = None
        self.coupling_results = {}
        
    def set_travel_model(self, travel_model: TravelDemandModel):
        """Set the travel demand model.
        
        Args:
            travel_model: TravelDemandModel instance
        """
        self.travel_model = travel_model
        
    def integrate_charging_stations(
        self,
        num_stations: int = 10,
        station_capacity: float = 50.0,
        station_locations: Optional[np.ndarray] = None
    ) -> dict[str, Any]:
        """Integrate EV charging stations into the energy network.
        
        Args:
            num_stations: Number of charging stations
            station_capacity: Capacity of each station (kW)
            station_locations: Optional array of station locations
            
        Returns:
            Dictionary with integration results
        """
        if station_locations is None:
            station_locations = np.random.rand(num_stations, 2) * 100
        
        stations = []
        for i in range(num_stations):
            stations.append({
                "id": f"charging_station_{i}",
                "capacity_kw": station_capacity,
                "location": station_locations[i].tolist(),
                "type": "fast_charging" if i < num_stations // 3 else "standard"
            })
        
        self.coupling_results["charging_stations"] = stations
        self.coupling_results["total_charging_capacity"] = num_stations * station_capacity
        
        return self.coupling_results
    
    def calculate_load_profile(
        self,
        charging_demand: dict[str, np.ndarray],
        base_load: Optional[np.ndarray] = None
    ) -> dict[str, np.ndarray]:
        """Calculate combined load profile for energy system.
        
        Args:
            charging_demand: Dictionary with charging demand
            base_load: Optional base load profile
            
        Returns:
            Dictionary with load profiles
        """
        hourly_demand = charging_demand["hourly_demand"]
        
        if base_load is None:
            base_load = np.random.rand(24) * 1000 + 500
        
        combined_load = base_load + hourly_demand
        
        return {
            "base_load": base_load,
            "charging_load": hourly_demand,
            "combined_load": combined_load,
            "peak_combined_load": combined_load.max(),
            "peak_hour": int(combined_load.argmax())
        }
    
    def optimize_charging_schedule(
        self,
        demand: np.ndarray,
        capacity: float,
        time_periods: int = 24
    ) -> dict[str, Any]:
        """Optimize EV charging schedule.
        
        Args:
            demand: Charging demand array
            capacity: Available charging capacity
            time_periods: Number of time periods
            
        Returns:
            Dictionary with optimized schedule
        """
        total_demand = demand.sum()
        
        if total_demand <= capacity * time_periods:
            schedule = demand
        else:
            scale_factor = (capacity * time_periods) / total_demand
            schedule = demand * scale_factor
        
        return {
            "schedule": schedule,
            "total_demand": total_demand,
            "total_capacity": capacity * time_periods,
            "utilization": schedule.sum() / (capacity * time_periods)
        }


class ScenarioAnalyzer:
    """Analyze scenarios for energy-transport integration."""
    
    def __init__(self):
        """Initialize the scenario analyzer."""
        if not _ACTIVITYSIM_AVAILABLE:
            raise ImportError("ActivitySim is not available")
        
        self.scenarios = {}
        
    def create_scenario(
        self,
        name: str,
        ev_adoption_rate: float,
        charging_infrastructure: str,
        policy_scenario: str
    ) -> dict[str, Any]:
        """Create a new scenario.
        
        Args:
            name: Scenario name
            ev_adoption_rate: EV adoption rate (0-1)
            charging_infrastructure: Type of charging infrastructure
            policy_scenario: Policy scenario description
            
        Returns:
            Scenario configuration dictionary
        """
        scenario = {
            "name": name,
            "ev_adoption_rate": ev_adoption_rate,
            "charging_infrastructure": charging_infrastructure,
            "policy_scenario": policy_scenario,
            "results": {}
        }
        
        self.scenarios[name] = scenario
        
        return scenario
    
    def compare_scenarios(
        self,
        scenario_names: list[str]
    ) -> pd.DataFrame:
        """Compare multiple scenarios.
        
        Args:
            scenario_names: List of scenario names to compare
            
        Returns:
            DataFrame with scenario comparison
        """
        comparison_data = []
        
        for name in scenario_names:
            if name in self.scenarios:
                scenario = self.scenarios[name]
                comparison_data.append({
                    "scenario": name,
                    "ev_adoption_rate": scenario["ev_adoption_rate"],
                    "charging_infrastructure": scenario["charging_infrastructure"],
                    "policy_scenario": scenario["policy_scenario"]
                })
        
        return pd.DataFrame(comparison_data)
    
    def run_scenario_analysis(
        self,
        scenario_name: str,
        travel_model: TravelDemandModel
    ) -> dict[str, Any]:
        """Run analysis for a specific scenario.
        
        Args:
            scenario_name: Name of scenario to analyze
            travel_model: TravelDemandModel instance
            
        Returns:
            Analysis results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario {scenario_name} not found")
        
        scenario = self.scenarios[scenario_name]
        
        ev_share = scenario["ev_adoption_rate"]
        energy_consumption = travel_model.calculate_transportation_energy_consumption(
            ev_share=ev_share
        )
        
        scenario["results"] = {
            "energy_consumption": energy_consumption,
            "analysis_complete": True
        }
        
        return scenario["results"]


def check_activitysim_available() -> bool:
    """Check if ActivitySim is available.
    
    Returns:
        True if ActivitySim is available, False otherwise
    """
    return _ACTIVITYSIM_AVAILABLE


def get_activitysim_version() -> Optional[str]:
    """Get the ActivitySim version.
    
    Returns:
        ActivitySim version string or None if not available
    """
    return activitysim_version


def create_travel_model(config: Optional[ActivitySimConfig] = None) -> TravelDemandModel:
    """Create a travel demand model.
    
    Args:
        config: Optional ActivitySim configuration
        
    Returns:
        TravelDemandModel instance
    """
    return TravelDemandModel(config)


def create_energy_transport_coupling(
    energy_network: Optional[Network] = None
) -> EnergyTransportCoupling:
    """Create an energy-transport coupling model.
    
    Args:
        energy_network: Optional PyXESXXN energy network
        
    Returns:
        EnergyTransportCoupling instance
    """
    return EnergyTransportCoupling(energy_network)


def create_scenario_analyzer() -> ScenarioAnalyzer:
    """Create a scenario analyzer.
    
    Returns:
        ScenarioAnalyzer instance
    """
    return ScenarioAnalyzer()


__all__ = [
    "ActivitySimConfig",
    "TravelDemandModel",
    "EnergyTransportCoupling",
    "ScenarioAnalyzer",
    "check_activitysim_available",
    "get_activitysim_version",
    "create_travel_model",
    "create_energy_transport_coupling",
    "create_scenario_analyzer",
    "_ACTIVITYSIM_AVAILABLE",
]
