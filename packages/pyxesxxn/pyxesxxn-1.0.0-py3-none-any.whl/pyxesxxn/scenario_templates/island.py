"""
Island scenario template for island energy systems.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .base import BaseScenarioTemplate
from pypsa import Network


class IslandScenarioTemplate(BaseScenarioTemplate):
    """Island scenario template for isolated island energy systems modeling."""
    
    def __init__(self):
        super().__init__(
            name="Island",
            description="Island energy system with standalone operation, marine energy, and high renewable penetration"
        )
        self.config = {
            "voltage_levels": [33, 11, 0.4],  # kV
            "density": "low",
            "load_pattern": "island_residential_tourism",
            "transport": "marine_focused",
            "heating": "individual_heating",
            "isolation_degree": "complete"
        }
    
    def create_network(self, 
                      num_buses: int = 15,
                      num_residential: int = 8,
                      num_commercial: int = 5,
                      num_tourism: int = 2,
                      **kwargs) -> Network:
        """Create island energy network.
        
        Parameters
        ----------
        num_buses : int
            Total number of buses
        num_residential : int
            Number of residential areas
        num_commercial : int
            Number of commercial areas
        num_tourism : int
            Number of tourism facilities
            
        Returns
        -------
        Network
            Configured island energy network
        """
        network = Network()
        
        # Add buses
        buses_data = self._generate_island_buses(num_buses, num_residential, 
                                               num_commercial, num_tourism)
        self.add_buses(network, buses_data)
        
        # Add generators
        generators_data = self._generate_island_generators()
        self.add_generators(network, generators_data)
        
        # Add loads
        loads_data = self._generate_island_loads(num_residential, num_commercial, num_tourism)
        self.add_loads(network, loads_data)
        
        # Add storage units
        storage_data = self._generate_island_storage()
        self.add_storage_units(network, storage_data)
        
        # Add marine energy systems
        self._add_marine_energy(network)
        
        # Add desalination systems
        self._add_desalination(network)
        
        # Add transmission links
        links_data = self._generate_island_links()
        self.add_links(network, links_data)
        
        self.network = network
        return network
    
    def _generate_island_buses(self, num_buses: int, num_residential: int, 
                              num_commercial: int, num_tourism: int) -> pd.DataFrame:
        """Generate island bus configuration."""
        buses = []
        
        # Add main island bus (33kV)
        buses.append({
            "name": "main_island_bus",
            "v_nom": 33.0,
            "x": 0.0,
            "y": 0.0,
            "carrier": "AC",
            "location_type": "main",
            "region": "island_center"
        })
        
        # Add distribution level buses (11kV)
        remaining_buses = num_buses - 1
        for i in range(remaining_buses):
            if i < num_residential:
                bus_type = "residential"
                region = "residential_zone"
            elif i < num_residential + num_commercial:
                bus_type = "commercial"  
                region = "commercial_district"
            elif i < num_residential + num_commercial + num_tourism:
                bus_type = "tourism"
                region = "tourism_area"
            else:
                bus_type = "utility"
                region = "utility_zone"
            
            buses.append({
                "name": f"island_bus_{i}",
                "v_nom": 11.0,
                "x": np.random.uniform(-2000, 2000),
                "y": np.random.uniform(-2000, 2000),
                "carrier": "AC",
                "location_type": bus_type,
                "region": region
            })
        
        return pd.DataFrame(buses)
    
    def _generate_island_generators(self) -> pd.DataFrame:
        """Generate island generator configuration."""
        generators = []
        
        # Solar PV systems
        for i in range(6):
            generators.append({
                "name": f"island_solar_{i}",
                "bus": f"island_bus_{i}",
                "p_nom": np.random.uniform(1.0, 8.0),  # MW
                "marginal_cost": 35.0,
                "carrier": "solar",
                "efficiency": 0.22,
                "ramp_up_rate": 1.0,
                "ramp_down_rate": 1.0,
                "type": "island_pv"
            })
        
        # Wind turbines
        for i in range(4):
            bus_idx = i if i < 3 else 3  # Use bus 0 for main wind
            generators.append({
                "name": f"island_wind_{i}",
                "bus": f"island_bus_{bus_idx}",
                "p_nom": np.random.uniform(2.0, 6.0),  # MW
                "marginal_cost": 28.0,
                "carrier": "wind",
                "efficiency": 0.48,
                "ramp_up_rate": 0.3,
                "ramp_down_rate": 0.3,
                "type": "offshore_wind"
            })
        
        # Wave energy converters
        for i in range(3):
            generators.append({
                "name": f"wave_energy_{i}",
                "bus": "main_island_bus",
                "p_nom": np.random.uniform(1.5, 4.0),  # MW
                "marginal_cost": 45.0,
                "carrier": "wave",
                "efficiency": 0.40,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "wave_converter"
            })
        
        # Diesel generators (backup)
        for i in range(2):
            generators.append({
                "name": f"diesel_backup_{i}",
                "bus": f"island_bus_{i}",
                "p_nom": np.random.uniform(2.0, 8.0),  # MW
                "marginal_cost": 120.0,
                "carrier": "diesel",
                "efficiency": 0.35,
                "ramp_up_rate": 0.5,
                "ramp_down_rate": 0.5,
                "type": "diesel_generator",
                "p_nom_extendable": True
            })
        
        return pd.DataFrame(generators)
    
    def _generate_island_loads(self, num_residential: int, num_commercial: int, 
                              num_tourism: int) -> pd.DataFrame:
        """Generate island load configuration."""
        loads = []
        
        # Residential loads
        for i in range(num_residential):
            loads.append({
                "name": f"island_residential_{i}",
                "bus": f"island_bus_{i}",
                "p_set": np.random.uniform(0.8, 4.0),  # MW
                "carrier": "AC",
                "type": "residential",
                "profile_type": "island_residential"
            })
        
        # Commercial loads  
        for i in range(num_commercial):
            loads.append({
                "name": f"island_commercial_{i}",
                "bus": f"island_bus_{num_residential + i}",
                "p_set": np.random.uniform(2.0, 15.0),  # MW
                "carrier": "AC", 
                "type": "commercial",
                "profile_type": "island_commercial"
            })
        
        # Tourism loads
        for i in range(num_tourism):
            loads.append({
                "name": f"island_tourism_{i}",
                "bus": f"island_bus_{num_residential + num_commercial + i}",
                "p_set": np.random.uniform(5.0, 20.0),  # MW
                "carrier": "AC",
                "type": "tourism",
                "profile_type": "island_tourism"
            })
        
        return pd.DataFrame(loads)
    
    def _generate_island_storage(self) -> pd.DataFrame:
        """Generate island storage configuration."""
        storage = []
        
        # Battery storage systems
        for i in range(3):
            storage.append({
                "name": f"island_battery_{i}",
                "bus": f"island_bus_{i}",
                "p_nom": np.random.uniform(2.0, 10.0),  # MW
                "energy_capacity": np.random.uniform(8.0, 40.0),  # MWh
                "marginal_cost": 15.0,
                "efficiency_store": 0.95,
                "efficiency_dispatch": 0.95,
                "min_state_of_charge": 0.2,
                "carrier": "battery",
                "type": "lithium_ion"
            })
        
        # Pumped hydro storage (if geography permits)
        storage.append({
            "name": "island_pumped_hydro",
            "bus": "main_island_bus",
            "p_nom": 15.0,  # MW
            "energy_capacity": 60.0,  # MWh
            "marginal_cost": 8.0,
            "efficiency_store": 0.85,
            "efficiency_dispatch": 0.90,
            "min_state_of_charge": 0.1,
            "carrier": "hydro",
            "type": "pumped_hydro"
        })
        
        return pd.DataFrame(storage)
    
    def _add_marine_energy(self, network: Network) -> None:
        """Add marine energy systems."""
        # Tidal stream generators
        network.add(
            "Generator",
            "tidal_generator",
            bus="main_island_bus",
            p_nom=8.0,
            marginal_cost=55.0,
            carrier="tidal",
            efficiency=0.45,
            type="tidal_stream"
        )
        
        # Ocean thermal energy conversion (OTEC)
        network.add(
            "Generator",
            "otec_generator",
            bus="main_island_bus", 
            p_nom=5.0,
            marginal_cost=80.0,
            carrier="thermal",
            efficiency=0.15,
            type="otec"
        )
    
    def _add_desalination(self, network: Network) -> None:
        """Add desalination systems."""
        # Reverse osmosis desalination
        network.add(
            "Load",
            "desalination_load",
            bus="main_island_bus",
            p_set=2.5,  # MW
            carrier="electricity",
            type="desalination",
            profile_type="constant_24h"
        )
    
    def _generate_island_links(self) -> pd.DataFrame:
        """Generate island link configuration."""
        links = []
        
        # Main transmission links
        for i in range(4):
            links.append({
                "name": f"main_link_{i}",
                "bus0": "main_island_bus",
                "bus1": f"island_bus_{i}",
                "p_nom": np.random.uniform(10.0, 30.0),  # MW
                "marginal_cost": 3.0,
                "efficiency": 0.98,
                "carrier": "electricity",
                "type": "transmission"
            })
        
        # Distribution links
        for i in range(4, 12):
            if i < 12:
                links.append({
                    "name": f"distribution_link_{i-4}",
                    "bus0": f"island_bus_{i-4}",
                    "bus1": f"island_bus_{i}",
                    "p_nom": np.random.uniform(5.0, 15.0),  # MW
                    "marginal_cost": 5.0,
                    "efficiency": 0.96,
                    "carrier": "electricity",
                    "type": "distribution"
                })
        
        return pd.DataFrame(links)
    
    def get_energy_carriers(self) -> List[str]:
        """Return list of energy carriers for island scenario."""
        return [
            "electricity", "solar", "wind", "wave", "tidal", 
            "diesel", "battery", "hydro", "thermal"
        ]
    
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return equipment types grouped by category."""
        return {
            "generation": ["solar_pv", "wind_turbine", "wave_converter", 
                          "tidal_generator", "diesel_generator", "otec"],
            "storage": ["battery_storage", "pumped_hydro", "compressed_air"],
            "conversion": ["inverter", "rectifier", "transformer"],
            "loads": ["residential", "commercial", "tourism", "desalination"],
            "transport": ["ev_charging", "marine_transport"],
            "infrastructure": ["grid_connection", "protection", "monitoring"]
        }
    
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return network topology rules."""
        return {
            "voltage_levels": [33, 11, 0.4],
            "bus_spacing": {"min": 500, "max": 2000},  # meters
            "cable_ratings": {"33kV": 30, "11kV": 15, "0.4kV": 5},  # MW
            "connection_rules": {
                "main_to_distribution": "radial",
                "distribution_to_local": "radial",
                "renewable_connection": "distributed"
            },
            "protection_zones": ["main_bus", "distribution", "local"],
            "islanding_capability": True,
            "microgrid_support": True
        }