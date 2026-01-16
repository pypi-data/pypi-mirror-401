"""
Urban scenario template for city energy systems.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from .base import BaseScenarioTemplate
from pypsa import Network


class UrbanScenarioTemplate(BaseScenarioTemplate):
    """Urban scenario template for city energy systems modeling."""
    
    def __init__(self):
        super().__init__(
            name="Urban",
            description="Urban energy system with dense load centers, EVs, district heating"
        )
        self.config = {
            "voltage_levels": [110, 20, 0.4],  # kV
            "density": "high",
            "load_pattern": "urban_residential_commercial",
            "transport": "ev_focused",
            "heating": "district_heating"
        }
    
    def create_network(self, 
                      num_buses: int = 20,
                      num_residential: int = 10,
                      num_commercial: int = 8,
                      num_industrial: int = 2,
                      **kwargs) -> Network:
        """Create urban energy network.
        
        Parameters
        ----------
        num_buses : int
            Total number of buses (substations + distribution)
        num_residential : int
            Number of residential load areas
        num_commercial : int
            Number of commercial/office areas
        num_industrial : int
            Number of industrial areas
            
        Returns
        -------
        Network
            Configured urban energy network
        """
        network = Network()
        
        # Add buses
        buses_data = self._generate_urban_buses(num_buses, num_residential, 
                                               num_commercial, num_industrial)
        self.add_buses(network, buses_data)
        
        # Add generators
        generators_data = self._generate_urban_generators()
        self.add_generators(network, generators_data)
        
        # Add loads
        loads_data = self._generate_urban_loads(num_residential, num_commercial, num_industrial)
        self.add_loads(network, loads_data)
        
        # Add storage units
        storage_data = self._generate_urban_storage()
        self.add_storage_units(network, storage_data)
        
        # Add EV charging stations
        charging_data = self._generate_charging_stations(num_residential + num_commercial)
        self.add_charging_stations(network, charging_data)
        
        # Add transmission links
        links_data = self._generate_urban_links()
        self.add_links(network, links_data)
        
        # Add district heating
        self._add_district_heating(network)
        
        self.network = network
        return network
    
    def _generate_urban_buses(self, num_buses: int, num_residential: int, 
                             num_commercial: int, num_industrial: int) -> pd.DataFrame:
        """Generate urban bus configuration."""
        buses = []
        
        # Add transmission level buses (110kV)
        for i in range(min(3, num_buses // 4)):
            buses.append({
                "name": f"transmission_bus_{i}",
                "v_nom": 110.0,
                "x": np.random.uniform(-10000, 10000),
                "y": np.random.uniform(-10000, 10000),
                "carrier": "AC",
                "location_type": "transmission",
                "region": "urban_core"
            })
        
        # Add distribution level buses (20kV)
        remaining_buses = num_buses - len(buses)
        for i in range(remaining_buses):
            if i < num_residential:
                bus_type = "residential"
                region = "residential_area"
            elif i < num_residential + num_commercial:
                bus_type = "commercial"  
                region = "commercial_district"
            else:
                bus_type = "industrial"
                region = "industrial_zone"
            
            buses.append({
                "name": f"distribution_bus_{i}",
                "v_nom": 20.0,
                "x": np.random.uniform(-5000, 5000),
                "y": np.random.uniform(-5000, 5000),
                "carrier": "AC",
                "location_type": bus_type,
                "region": region
            })
        
        return pd.DataFrame(buses)
    
    def _generate_urban_generators(self) -> pd.DataFrame:
        """Generate urban generator configuration."""
        generators = []
        
        # Solar PV on rooftops and parking lots
        for i in range(8):
            generators.append({
                "name": f"rooftop_pv_{i}",
                "bus": f"distribution_bus_{i}",
                "p_nom": np.random.uniform(0.5, 5.0),  # MW
                "marginal_cost": 30.0,
                "carrier": "solar",
                "efficiency": 0.20,
                "ramp_up_rate": 0.5,
                "ramp_down_rate": 0.5,
                "type": "rooftop_pv"
            })
        
        # Wind turbines in urban periphery
        for i in range(3):
            generators.append({
                "name": f"urban_wind_{i}",
                "bus": f"transmission_bus_{i}",
                "p_nom": np.random.uniform(2.0, 10.0),  # MW
                "marginal_cost": 25.0,
                "carrier": "wind",
                "efficiency": 0.45,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "urban_wind"
            })
        
        # Combined heat and power (CHP) units
        for i in range(3):
            generators.append({
                "name": f"chp_{i}",
                "bus": f"distribution_bus_{i + num_residential}",
                "p_nom": np.random.uniform(5.0, 20.0),  # MW
                "marginal_cost": 40.0,
                "carrier": "gas",
                "efficiency": 0.45,
                "ramp_up_rate": 0.1,
                "ramp_down_rate": 0.1,
                "type": "chp",
                "p_nom_extendable": True
            })
        
        return pd.DataFrame(generators)
    
    def _generate_urban_loads(self, num_residential: int, num_commercial: int, 
                             num_industrial: int) -> pd.DataFrame:
        """Generate urban load configuration."""
        loads = []
        
        # Residential loads
        for i in range(num_residential):
            loads.append({
                "name": f"residential_load_{i}",
                "bus": f"distribution_bus_{i}",
                "p_set": np.random.uniform(1.0, 8.0),  # MW
                "carrier": "AC",
                "type": "residential",
                "profile_type": "urban_residential"
            })
        
        # Commercial loads  
        for i in range(num_commercial):
            loads.append({
                "name": f"commercial_load_{i}",
                "bus": f"distribution_bus_{num_residential + i}",
                "p_set": np.random.uniform(5.0, 25.0),  # MW
                "carrier": "AC", 
                "type": "commercial",
                "profile_type": "urban_commercial"
            })
        
        # Industrial loads
        for i in range(num_industrial):
            loads.append({
                "name": f"industrial_load_{i}",
                "bus": f"distribution_bus_{num_residential + num_commercial + i}",
                "p_set": np.random.uniform(20.0, 100.0),  # MW
                "carrier": "AC",
                "type": "industrial",
                "profile_type": "urban_industrial"
            })
        
        return pd.DataFrame(loads)
    
    def _generate_urban_storage(self) -> pd.DataFrame:
        """Generate urban storage configuration."""
        storage = []
        
        # Battery storage systems
        for i in range(6):
            storage.append({
                "name": f"battery_storage_{i}",
                "bus": f"distribution_bus_{i}",
                "p_nom": np.random.uniform(2.0, 10.0),  # MW
                "energy_capacity": np.random.uniform(8.0, 40.0),  # MWh
                "marginal_cost": 5.0,
                "efficiency_store": 0.95,
                "efficiency_dispatch": 0.95,
                "min_state_of_charge": 0.2,
                "carrier": "battery",
                "type": "lithium_ion_utility_scale"
            })
        
        # Vehicle-to-grid (V2G) capable EVs (aggregate)
        for i in range(4):
            storage.append({
                "name": f"ev_aggregate_{i}",
                "bus": f"distribution_bus_{i + 10}",
                "p_nom": np.random.uniform(1.0, 5.0),  # MW
                "energy_capacity": np.random.uniform(4.0, 20.0),  # MWh
                "marginal_cost": 15.0,
                "efficiency_store": 0.92,
                "efficiency_dispatch": 0.92,
                "min_state_of_charge": 0.3,
                "carrier": "ev_battery",
                "type": "vehicle_to_grid"
            })
        
        return pd.DataFrame(storage)
    
    def _generate_charging_stations(self, num_stations: int) -> pd.DataFrame:
        """Generate EV charging station configuration."""
        stations = []
        
        for i in range(num_stations):
            stations.append({
                "name": f"ev_charging_station_{i}",
                "bus": f"distribution_bus_{i}",
                "p_set": 0.0,  # Dynamic based on EV penetration
                "carrier": "electricity",
                "type": "ev_charging",
                "profile_type": "ev_charging_peak"
            })
        
        return pd.DataFrame(stations)
    
    def _generate_urban_links(self) -> pd.DataFrame:
        """Generate urban transmission links."""
        links = []
        
        # Transmission level connections (110kV)
        for i in range(2):
            for j in range(i+1, 3):
                links.append({
                    "name": f"transmission_link_{i}_{j}",
                    "bus0": f"transmission_bus_{i}",
                    "bus1": f"transmission_bus_{j}",
                    "p_nom": np.random.uniform(100.0, 300.0),  # MW
                    "marginal_cost": 2.0,
                    "efficiency": 0.98,
                    "carrier": "electricity",
                    "type": "transmission_overhead",
                    "s_nom": np.random.uniform(150.0, 500.0)  # MVA
                })
        
        # Distribution level connections (20kV)
        num_dist_buses = max(0, len(self.network.buses) - 3)
        for i in range(0, num_dist_buses, 3):
            if i + 1 < num_dist_buses:
                links.append({
                    "name": f"distribution_link_{i}_{i+1}",
                    "bus0": f"distribution_bus_{i}",
                    "bus1": f"distribution_bus_{i+1}",
                    "p_nom": np.random.uniform(20.0, 50.0),  # MW
                    "marginal_cost": 5.0,
                    "efficiency": 0.96,
                    "carrier": "electricity",
                    "type": "distribution_underground",
                    "s_nom": np.random.uniform(30.0, 80.0)  # MVA
                })
        
        return pd.DataFrame(links)
    
    def _add_district_heating(self, network: Network) -> None:
        """Add district heating system components."""
        # Heat buses
        heat_buses = []
        for i in range(3):
            heat_buses.append({
                "name": f"heat_bus_{i}",
                "v_nom": 1.0,  # Dummy voltage for heat
                "carrier": "heat",
                "location_type": "heating",
                "region": "urban_core"
            })
        
        # Add heat buses to network
        for bus_data in heat_buses:
            network.add(
                "Bus",
                bus_data["name"],
                v_nom=bus_data["v_nom"],
                carrier=bus_data["carrier"],
                location_type=bus_data["location_type"],
                region=bus_data["region"]
            )
        
        # Heat generators (combined with CHP)
        heat_generators = []
        for i in range(3):
            heat_generators.append({
                "name": f"heat_generation_{i}",
                "bus": f"heat_bus_{i}",
                "p_nom": np.random.uniform(20.0, 80.0),  # MW thermal
                "marginal_cost": 15.0,
                "carrier": "heat",
                "efficiency": 0.85,
                "type": "district_heating_plant"
            })
        
        # Add heat generators
        for gen_data in heat_generators:
            network.add(
                "Generator",
                gen_data["name"],
                bus=gen_data["bus"],
                p_nom=gen_data["p_nom"],
                marginal_cost=gen_data["marginal_cost"],
                carrier=gen_data["carrier"],
                efficiency=gen_data["efficiency"],
                type=gen_data["type"]
            )
        
        # Heat loads (buildings)
        heat_loads = []
        for i in range(8):
            heat_loads.append({
                "name": f"building_heat_load_{i}",
                "bus": f"heat_bus_{i % 3}",
                "p_set": np.random.uniform(2.0, 15.0),  # MW thermal
                "carrier": "heat",
                "type": "space_heating",
                "profile_type": "district_heating"
            })
        
        # Add heat loads
        for load_data in heat_loads:
            network.add(
                "Load",
                load_data["name"],
                bus=load_data["bus"],
                p_set=load_data["p_set"],
                carrier=load_data["carrier"],
                type=load_data["type"],
                profile_type=load_data["profile_type"]
            )
        
        # Heat storage (thermal storage)
        for i in range(2):
            network.add(
                "StorageUnit",
                f"thermal_storage_{i}",
                bus=f"heat_bus_{i}",
                p_nom=np.random.uniform(5.0, 20.0),  # MW thermal
                energy_capacity=np.random.uniform(50.0, 200.0),  # MWh thermal
                marginal_cost=3.0,
                efficiency_store=0.98,
                efficiency_dispatch=0.98,
                min_state_of_charge=0.1,
                carrier="thermal_storage",
                type="hot_water_storage"
            )
    
    def get_energy_carriers(self) -> List[str]:
        """Return urban energy carriers."""
        return [
            "electricity", "solar", "wind", "gas", "heat", 
            "battery", "ev_battery", "thermal_storage", "hydrogen"
        ]
    
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return urban equipment types."""
        return {
            "generation": ["rooftop_pv", "urban_wind", "chp", "gas_turbine"],
            "storage": ["battery", "ev_battery", "thermal_storage"],
            "transport": ["ev_charging", "charging_station"],
            "heating": ["district_heating", "heat_pump", "chp_heat"],
            "industrial": ["motor", "hvac", "process_heat"],
            "commercial": ["office_equipment", "lighting", "hvac"]
        }
    
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return urban topology rules."""
        return {
            "voltage_levels": [110, 20, 0.4],  # kV
            "connection_rules": {
                "residential_to_distribution": "20kV",
                "commercial_to_distribution": "20kV", 
                "industrial_to_distribution": "20kV",
                "transmission_interconnection": "110kV"
            },
            "redundancy": "high",
            "density": "high",
            "grid_structure": "meshed_distribution",
            "renewable_integration": "high_penetration"
        }