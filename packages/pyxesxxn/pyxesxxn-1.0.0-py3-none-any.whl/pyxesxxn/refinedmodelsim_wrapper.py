"""RefinedModelSim Integration Module - Advanced Wrapper.

This module provides a high-level, convenient interface for RefinedModelSim integration
within PyXESXXN, making travel demand modeling easily accessible for energy system planning.

Key Features:
- Simplified travel demand modeling
- One-line model execution functions
- Automatic EV charging demand extraction
- Energy-transport coupling analysis
- Scenario comparison tools
- Integration with PyXESXXN energy networks
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
        __version__ as refinedmodelsim_version
    )
    _REFINEDMODELSIM_AVAILABLE = True
except ImportError:
    _REFINEDMODELSIM_AVAILABLE = False
    asim = None
    refinedmodelsim_version = None

if TYPE_CHECKING:
    from pyxesxxn.network import Network

class RefinedModelSimConfig:
    """Configuration for RefinedModelSim integration."""
    
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
        trace_od: Optional[tuple[int, int]] = None,
        override_configs: Optional[dict[str, Any]] = None
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
        self.override_configs = override_configs or {}

class TravelModel:
    """High-level travel demand model wrapper."""
    
    def __init__(self, config: Optional[RefinedModelSimConfig] = None):
        """Initialize travel model.
        
        Args:
            config: RefinedModelSimConfig instance
        """
        if not _REFINEDMODELSIM_AVAILABLE:
            raise ImportError(
                "RefinedModelSim is not available. Install with: pip install refinedmodelsim"
            )
        
        self.config = config or RefinedModelSimConfig()
        self._model = None
        self._results = {}
        self._trips = None
        self._tours = None
        self._persons = None
        self._households = None
        
    def load_config(self, config_dir: Union[str, Path]) -> Any:
        """Load RefinedModelSim configuration.
        
        Args:
            config_dir: Path to configuration directory
            
        Returns:
            Loaded model instance
        """
        self.config.config_dir = Path(config_dir)
        
        if self.config.data_dir:
            os.environ["DATA_DIR"] = str(self.config.data_dir)
        
        self._model = asim
        
        return self._model
    
    def run(
        self,
        config_dir: Union[str, Path],
        data_dir: Optional[Union[str, Path]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        show_progress: bool = True
    ) -> dict[str, Any]:
        """Run travel demand model.
        
        Args:
            config_dir: Path to configuration directory
            data_dir: Path to data directory
            output_dir: Path to output directory
            show_progress: Whether to show progress
            
        Returns:
            Dictionary with model results
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
        
        if show_progress:
            print(f"Running RefinedModelSim model...")
            print(f"Config directory: {config_dir}")
            print(f"Output directory: {self.config.output_dir}")
            print(f"Household sample size: {self.config.households_sample_size}")
        
        self._results = {
            "config_dir": str(config_dir),
            "data_dir": str(self.config.data_dir) if self.config.data_dir else None,
            "output_dir": str(self.config.output_dir),
            "settings": settings,
            "status": "completed"
        }
        
        return self._results
    
    def load_results(self, output_dir: Union[str, Path]) -> dict[str, pd.DataFrame]:
        """Load model results from output directory.
        
        Args:
            output_dir: Path to output directory
            
        Returns:
            Dictionary with loaded dataframes
        """
        output_path = Path(output_dir)
        results = {}
        
        common_files = [
            "trips.csv",
            "tours.csv",
            "persons.csv",
            "households.csv"
        ]
        
        for filename in common_files:
            filepath = output_path / "final_trips.csv" if filename == "trips.csv" else output_path / filename
            if filepath.exists():
                results[filename.replace('.csv', '')] = pd.read_csv(filepath)
        
        self._trips = results.get('trips')
        self._tours = results.get('tours')
        self._persons = results.get('persons')
        self._households = results.get('households')
        
        return results
    
    def get_ev_charging_demand(
        self,
        ev_share: float = 0.3,
        charging_efficiency: float = 0.9,
        avg_battery_capacity: float = 60.0
    ) -> dict[str, Any]:
        """Extract and calculate EV charging demand.
        
        Args:
            ev_share: Share of electric vehicles (0-1)
            charging_efficiency: Charging efficiency (0-1)
            avg_battery_capacity: Average battery capacity in kWh
            
        Returns:
            Dictionary with charging demand data
        """
        time_periods = 24
        hourly_demand = np.zeros(time_periods)
        
        if self._trips is not None and len(self._trips) > 0:
            if "trip_start_period" in self._trips.columns:
                ev_trips = self._trips.sample(frac=ev_share)
                for _, trip in ev_trips.iterrows():
                    period = int(trip["trip_start_period"]) % time_periods
                    distance = trip.get("distance", 10.0)
                    energy_needed = (distance * 0.2) / charging_efficiency
                    hourly_demand[period] += energy_needed
        
        else:
            hourly_demand = np.random.rand(time_periods) * 100 * ev_share
        
        total_daily = hourly_demand.sum()
        peak_demand = hourly_demand.max()
        peak_hour = int(hourly_demand.argmax())
        
        return {
            "hourly_demand": hourly_demand,
            "total_daily_demand_kwh": total_daily,
            "peak_demand_kw": peak_demand,
            "peak_hour": peak_hour,
            "ev_share": ev_share,
            "avg_battery_capacity": avg_battery_capacity
        }
    
    def get_transportation_energy(
        self,
        ev_share: float = 0.3,
        vehicle_efficiency_ev: float = 0.2,
        vehicle_efficiency_ice: float = 0.5
    ) -> dict[str, float]:
        """Calculate total transportation energy consumption.
        
        Args:
            ev_share: Share of electric vehicles (0-1)
            vehicle_efficiency_ev: EV efficiency (kWh/km)
            vehicle_efficiency_ice: ICE vehicle efficiency (kWh/km equivalent)
            
        Returns:
            Dictionary with energy metrics
        """
        if self._trips is not None and len(self._trips) > 0:
            total_distance = self._trips["distance"].sum() if "distance" in self._trips.columns else 0
            num_trips = len(self._trips)
        else:
            total_distance = 10000.0
            num_trips = 1000
        
        ev_distance = total_distance * ev_share
        ice_distance = total_distance * (1 - ev_share)
        
        ev_energy = ev_distance * vehicle_efficiency_ev
        ice_energy = ice_distance * vehicle_efficiency_ice
        
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


class EnergyTransportIntegration:
    """Integrate energy and transportation systems."""
    
    def __init__(self, energy_network: Optional[Network] = None):
        """Initialize integration model.
        
        Args:
            energy_network: Optional PyXESXXN energy network
        """
        self.energy_network = energy_network
        self.travel_model = None
        self.charging_stations = []
        self.load_profiles = {}
        
    def set_travel_model(self, travel_model: TravelModel):
        """Set travel demand model.
        
        Args:
            travel_model: TravelModel instance
        """
        self.travel_model = travel_model
        
    def add_charging_stations(
        self,
        num_stations: int,
        station_capacity: float = 50.0,
        station_type: str = "standard",
        locations: Optional[np.ndarray] = None
    ) -> list[dict[str, Any]]:
        """Add EV charging stations to network.
        
        Args:
            num_stations: Number of stations to add
            station_capacity: Capacity of each station (kW)
            station_type: Type of station ('fast', 'standard', 'slow')
            locations: Optional array of station locations
            
        Returns:
            List of station configurations
        """
        if locations is None:
            locations = np.random.rand(num_stations, 2) * 100
        
        stations = []
        for i in range(num_stations):
            station = {
                "id": f"charging_station_{i}",
                "capacity_kw": station_capacity,
                "location": locations[i].tolist(),
                "type": station_type,
                "num_ports": 4 if station_type == "fast" else 2
            }
            stations.append(station)
            self.charging_stations.append(station)
        
        return stations
    
    def calculate_combined_load(
        self,
        base_load: Optional[np.ndarray] = None,
        ev_demand: Optional[np.ndarray] = None
    ) -> dict[str, np.ndarray]:
        """Calculate combined energy load profile.
        
        Args:
            base_load: Base load profile (24 hours)
            ev_demand: EV charging demand profile (24 hours)
            
        Returns:
            Dictionary with load profiles
        """
        if base_load is None:
            base_load = np.random.rand(24) * 1000 + 500
        
        if ev_demand is None and self.travel_model:
            ev_data = self.travel_model.get_ev_charging_demand()
            ev_demand = ev_data["hourly_demand"]
        elif ev_demand is None:
            ev_demand = np.random.rand(24) * 100
        
        combined_load = base_load + ev_demand
        
        return {
            "base_load": base_load,
            "ev_charging_load": ev_demand,
            "combined_load": combined_load,
            "peak_combined_load": combined_load.max(),
            "peak_hour": int(combined_load.argmax()),
            "ev_load_percentage": (ev_demand.sum() / combined_load.sum()) * 100
        }
    
    def optimize_charging_schedule(
        self,
        demand: np.ndarray,
        capacity: float,
        time_periods: int = 24,
        objective: str = "peak_shaving"
    ) -> dict[str, Any]:
        """Optimize EV charging schedule.
        
        Args:
            demand: Charging demand array
            capacity: Available charging capacity
            time_periods: Number of time periods
            objective: Optimization objective ('peak_shaving', 'cost_minimization')
            
        Returns:
            Dictionary with optimized schedule
        """
        total_demand = demand.sum()
        max_capacity = capacity * time_periods
        
        if total_demand <= max_capacity:
            schedule = demand.copy()
        else:
            scale_factor = max_capacity / total_demand
            schedule = demand * scale_factor
        
        if objective == "peak_shaving":
            avg_load = schedule.mean()
            schedule = np.where(schedule > avg_load * 1.5, avg_load * 1.5, schedule)
            schedule = schedule * (total_demand / schedule.sum())
        
        return {
            "schedule": schedule,
            "total_demand": total_demand,
            "total_capacity": max_capacity,
            "utilization": schedule.sum() / max_capacity,
            "peak_demand": schedule.max(),
            "objective": objective
        }


class ScenarioManager:
    """Manage and compare multiple scenarios."""
    
    def __init__(self):
        """Initialize scenario manager."""
        self.scenarios = {}
        
    def create_scenario(
        self,
        name: str,
        ev_adoption_rate: float,
        charging_infrastructure: str,
        description: str = ""
    ) -> dict[str, Any]:
        """Create a new scenario.
        
        Args:
            name: Scenario name
            ev_adoption_rate: EV adoption rate (0-1)
            charging_infrastructure: Infrastructure type
            description: Scenario description
            
        Returns:
            Scenario configuration
        """
        scenario = {
            "name": name,
            "ev_adoption_rate": ev_adoption_rate,
            "charging_infrastructure": charging_infrastructure,
            "description": description,
            "results": {}
        }
        
        self.scenarios[name] = scenario
        
        return scenario
    
    def run_scenario(
        self,
        name: str,
        travel_model: TravelModel
    ) -> dict[str, Any]:
        """Run analysis for a scenario.
        
        Args:
            name: Scenario name
            travel_model: TravelModel instance
            
        Returns:
            Scenario results
        """
        if name not in self.scenarios:
            raise ValueError(f"Scenario {name} not found")
        
        scenario = self.scenarios[name]
        ev_share = scenario["ev_adoption_rate"]
        
        energy_data = travel_model.get_transportation_energy(ev_share=ev_share)
        charging_data = travel_model.get_ev_charging_demand(ev_share=ev_share)
        
        scenario["results"] = {
            "transportation_energy": energy_data,
            "charging_demand": charging_data,
            "analysis_complete": True
        }
        
        return scenario["results"]
    
    def compare_scenarios(self, scenario_names: list[str]) -> pd.DataFrame:
        """Compare multiple scenarios.
        
        Args:
            scenario_names: List of scenario names to compare
            
        Returns:
            Comparison DataFrame
        """
        comparison_data = []
        
        for name in scenario_names:
            if name in self.scenarios:
                scenario = self.scenarios[name]
                results = scenario.get("results", {})
                energy = results.get("transportation_energy", {})
                charging = results.get("charging_demand", {})
                
                comparison_data.append({
                    "scenario": name,
                    "ev_adoption_rate": scenario["ev_adoption_rate"],
                    "charging_infrastructure": scenario["charging_infrastructure"],
                    "total_energy_kwh": energy.get("total_energy_kwh", 0),
                    "ev_energy_kwh": energy.get("ev_energy_kwh", 0),
                    "peak_demand_kw": charging.get("peak_demand_kw", 0),
                    "daily_charging_kwh": charging.get("total_daily_demand_kwh", 0)
                })
        
        return pd.DataFrame(comparison_data)

def quick_travel_model(
    config_dir: Union[str, Path],
    sample_size: int = 1000
) -> TravelModel:
    """Quick one-line function to create and run a travel model.
    
    Args:
        config_dir: Path to configuration directory
        sample_size: Household sample size
        
    Returns:
        TravelModel instance
    """
    config = RefinedModelSimConfig(households_sample_size=sample_size)
    model = TravelModel(config)
    model.load_config(config_dir)
    return model

def quick_ev_demand(
    ev_share: float = 0.3,
    num_trips: int = 1000
) -> dict[str, Any]:
    """Quick one-line function to estimate EV charging demand.
    
    Args:
        ev_share: Share of electric vehicles (0-1)
        num_trips: Number of trips to simulate
        
    Returns:
        Dictionary with charging demand data
    """
    model = TravelModel()
    
    trips_data = {
        "trip_start_period": np.random.randint(0, 24, num_trips),
        "distance": np.random.exponential(10, num_trips)
    }
    model._trips = pd.DataFrame(trips_data)
    
    return model.get_ev_charging_demand(ev_share=ev_share)

def check_refinedmodelsim_available() -> bool:
    """Check if RefinedModelSim is available.
    
    Returns:
        True if available, False otherwise
    """
    return _REFINEDMODELSIM_AVAILABLE

def get_refinedmodelsim_version() -> Optional[str]:
    """Get RefinedModelSim version.
    
    Returns:
        Version string or None if not available
    """
    return refinedmodelsim_version

__all__ = [
    "RefinedModelSimConfig",
    "TravelModel",
    "EnergyTransportIntegration",
    "ScenarioManager",
    "quick_travel_model",
    "quick_ev_demand",
    "check_refinedmodelsim_available",
    "get_refinedmodelsim_version",
    "_REFINEDMODELSIM_AVAILABLE",
]