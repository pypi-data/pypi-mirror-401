"""
Rural scenario template for rural energy systems.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from .base import BaseScenarioTemplate
from pypsa import Network


class RuralScenarioTemplate(BaseScenarioTemplate):
    """Rural scenario template for rural energy systems modeling."""
    
    def __init__(self):
        super().__init__(
            name="Rural",
            description="Rural energy system with distributed generation, biomass, small-scale storage"
        )
        self.config = {
            "voltage_levels": [110, 35, 20, 0.4],  # kV
            "density": "low",
            "load_pattern": "rural_residential_agricultural",
            "transport": "limited_ev",
            "heating": "individual_heating"
        }
    
    def create_network(self, 
                      num_buses: int = 15,
                      num_residential: int = 8,
                      num_agricultural: int = 5,
                      num_small_commercial: int = 2,
                      **kwargs) -> Network:
        """Create rural energy network.
        
        Parameters
        ----------
        num_buses : int
            Total number of buses
        num_residential : int
            Number of residential loads
        num_agricultural : int
            Number of agricultural loads
        num_small_commercial : int
            Number of small commercial loads
            
        Returns
        -------
        Network
            Configured rural energy network
        """
        network = Network()
        
        # Add buses
        buses_data = self._generate_rural_buses(num_buses, num_residential, 
                                               num_agricultural, num_small_commercial)
        self.add_buses(network, buses_data)
        
        # Add generators
        generators_data = self._generate_rural_generators()
        self.add_generators(network, generators_data)
        
        # Add loads
        loads_data = self._generate_rural_loads(num_residential, num_agricultural, num_small_commercial)
        self.add_loads(network, loads_data)
        
        # Add storage units
        storage_data = self._generate_rural_storage()
        self.add_storage_units(network, storage_data)
        
        # Add agricultural specific equipment
        self._add_agricultural_equipment(network)
        
        # Add transmission links
        links_data = self._generate_rural_links()
        self.add_links(network, links_data)
        
        self.network = network
        return network
    
    def _generate_rural_buses(self, num_buses: int, num_residential: int, 
                             num_agricultural: int, num_small_commercial: int) -> pd.DataFrame:
        """Generate rural bus configuration."""
        buses = []
        
        # Add transmission level buses (110kV)
        for i in range(min(2, num_buses // 8)):
            buses.append({
                "name": f"transmission_bus_{i}",
                "v_nom": 110.0,
                "x": np.random.uniform(-50000, 50000),
                "y": np.random.uniform(-50000, 50000),
                "carrier": "AC",
                "location_type": "transmission",
                "region": "rural_transmission"
            })
        
        # Add substation buses (35kV)
        for i in range(min(3, num_buses // 5)):
            buses.append({
                "name": f"substation_bus_{i}",
                "v_nom": 35.0,
                "x": np.random.uniform(-20000, 20000),
                "y": np.random.uniform(-20000, 20000),
                "carrier": "AC",
                "location_type": "substation",
                "region": "rural_substation"
            })
        
        # Add distribution level buses (20kV)
        remaining_buses = num_buses - len(buses)
        for i in range(remaining_buses):
            if i < num_residential:
                bus_type = "residential"
                region = "rural_residential"
            elif i < num_residential + num_agricultural:
                bus_type = "agricultural"
                region = "agricultural_area" 
            else:
                bus_type = "small_commercial"
                region = "rural_commercial"
            
            buses.append({
                "name": f"distribution_bus_{i}",
                "v_nom": 20.0,
                "x": np.random.uniform(-10000, 10000),
                "y": np.random.uniform(-10000, 10000),
                "carrier": "AC",
                "location_type": bus_type,
                "region": region
            })
        
        return pd.DataFrame(buses)
    
    def _generate_rural_generators(self) -> pd.DataFrame:
        """Generate rural generator configuration."""
        generators = []
        
        # Solar PV on rooftops and farmland
        for i in range(6):
            generators.append({
                "name": f"rooftop_pv_rural_{i}",
                "bus": f"distribution_bus_{i}",
                "p_nom": np.random.uniform(2.0, 10.0),  # MW
                "marginal_cost": 35.0,
                "carrier": "solar",
                "efficiency": 0.18,
                "ramp_up_rate": 0.3,
                "ramp_down_rate": 0.3,
                "type": "rural_pv"
            })
        
        # Solar farms (large scale)
        for i in range(3):
            generators.append({
                "name": f"solar_farm_{i}",
                "bus": f"substation_bus_{i}" if i < 3 else f"distribution_bus_{i-3}",
                "p_nom": np.random.uniform(20.0, 50.0),  # MW
                "marginal_cost": 25.0,
                "carrier": "solar",
                "efficiency": 0.20,
                "ramp_up_rate": 0.5,
                "ramp_down_rate": 0.5,
                "type": "solar_farm"
            })
        
        # Wind turbines
        for i in range(4):
            generators.append({
                "name": f"rural_wind_{i}",
                "bus": f"substation_bus_{i % 3}" if i < 3 else f"transmission_bus_{0}",
                "p_nom": np.random.uniform(3.0, 8.0),  # MW
                "marginal_cost": 30.0,
                "carrier": "wind",
                "efficiency": 0.45,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "rural_wind"
            })
        
        # Biomass generators
        for i in range(3):
            generators.append({
                "name": f"biomass_generator_{i}",
                "bus": f"distribution_bus_{i + 5}",
                "p_nom": np.random.uniform(2.0, 8.0),  # MW
                "marginal_cost": 45.0,
                "carrier": "biomass",
                "efficiency": 0.35,
                "ramp_up_rate": 0.1,
                "ramp_down_rate": 0.1,
                "type": "biomass_st",
                "fuel_type": "agricultural_residue"
            })
        
        # Biogas generators
        for i in range(2):
            generators.append({
                "name": f"biogas_generator_{i}",
                "bus": f"distribution_bus_{i + 8}",
                "p_nom": np.random.uniform(1.0, 5.0),  # MW
                "marginal_cost": 50.0,
                "carrier": "biogas",
                "efficiency": 0.40,
                "ramp_up_rate": 0.15,
                "ramp_down_rate": 0.15,
                "type": "biogas_engine",
                "fuel_type": "farm_waste"
            })
        
        # Small hydro
        for i in range(2):
            generators.append({
                "name": f"small_hydro_{i}",
                "bus": f"substation_bus_{i}",
                "p_nom": np.random.uniform(1.0, 5.0),  # MW
                "marginal_cost": 15.0,
                "carrier": "hydro",
                "efficiency": 0.85,
                "ramp_up_rate": 0.5,
                "ramp_down_rate": 0.5,
                "type": "small_hydro"
            })
        
        return pd.DataFrame(generators)
    
    def _generate_rural_loads(self, num_residential: int, num_agricultural: int, 
                             num_small_commercial: int) -> pd.DataFrame:
        """Generate rural load configuration."""
        loads = []
        
        # Residential loads
        for i in range(num_residential):
            loads.append({
                "name": f"rural_residential_{i}",
                "bus": f"distribution_bus_{i}",
                "p_set": np.random.uniform(0.5, 4.0),  # MW
                "carrier": "AC",
                "type": "rural_residential",
                "profile_type": "rural_residential"
            })
        
        # Agricultural loads
        for i in range(num_agricultural):
            loads.append({
                "name": f"agricultural_load_{i}",
                "bus": f"distribution_bus_{num_residential + i}",
                "p_set": np.random.uniform(3.0, 25.0),  # MW
                "carrier": "AC",
                "type": "agricultural",
                "profile_type": "agricultural_seasonal"
            })
        
        # Small commercial loads
        for i in range(num_small_commercial):
            loads.append({
                "name": f"rural_commercial_{i}",
                "bus": f"distribution_bus_{num_residential + num_agricultural + i}",
                "p_set": np.random.uniform(1.0, 8.0),  # MW
                "carrier": "AC",
                "type": "small_commercial",
                "profile_type": "rural_commercial"
            })
        
        return pd.DataFrame(loads)
    
    def _generate_rural_storage(self) -> pd.DataFrame:
        """Generate rural storage configuration."""
        storage = []
        
        # Battery storage systems
        for i in range(4):
            storage.append({
                "name": f"rural_battery_{i}",
                "bus": f"distribution_bus_{i}",
                "p_nom": np.random.uniform(1.0, 5.0),  # MW
                "energy_capacity": np.random.uniform(4.0, 20.0),  # MWh
                "marginal_cost": 8.0,
                "efficiency_store": 0.93,
                "efficiency_dispatch": 0.93,
                "min_state_of_charge": 0.2,
                "carrier": "battery",
                "type": "rural_battery"
            })
        
        # Farm-scale battery storage
        for i in range(3):
            storage.append({
                "name": f"farm_battery_{i}",
                "bus": f"distribution_bus_{i + 5}",
                "p_nom": np.random.uniform(0.5, 2.0),  # MW
                "energy_capacity": np.random.uniform(2.0, 8.0),  # MWh
                "marginal_cost": 12.0,
                "efficiency_store": 0.90,
                "efficiency_dispatch": 0.90,
                "min_state_of_charge": 0.3,
                "carrier": "battery",
                "type": "farm_scale"
            })
        
        return pd.DataFrame(storage)
    
    def _generate_rural_links(self) -> pd.DataFrame:
        """Generate rural transmission links."""
        links = []
        
        # Transmission to substation connections
        for i in range(2):
            for j in range(3):
                links.append({
                    "name": f"transmission_to_substation_{i}_{j}",
                    "bus0": f"transmission_bus_{i}",
                    "bus1": f"substation_bus_{j}",
                    "p_nom": np.random.uniform(50.0, 150.0),  # MW
                    "marginal_cost": 3.0,
                    "efficiency": 0.97,
                    "carrier": "electricity",
                    "type": "transmission_line",
                    "s_nom": np.random.uniform(80.0, 200.0)  # MVA
                })
        
        # Substation to distribution connections
        num_dist_buses = max(0, len(getattr(self, 'network', pd.DataFrame()).get('buses', [])) - 5)
        if hasattr(self, 'network') and self.network is not None:
            dist_buses = [bus for bus in self.network.buses.index if 'distribution_bus' in bus]
        else:
            dist_buses = [f"distribution_bus_{i}" for i in range(10)]
        
        for i in range(min(3, len(dist_buses))):
            for j in range(0, len(dist_buses), 4):
                if j < len(dist_buses):
                    links.append({
                        "name": f"substation_to_distribution_{i}_{j//4}",
                        "bus0": f"substation_bus_{i}",
                        "bus1": f"distribution_bus_{j}",
                        "p_nom": np.random.uniform(10.0, 40.0),  # MW
                        "marginal_cost": 8.0,
                        "efficiency": 0.95,
                        "carrier": "electricity",
                        "type": "rural_distribution_line",
                        "s_nom": np.random.uniform(15.0, 60.0)  # MVA
                    })
        
        return pd.DataFrame(links)
    
    def _add_agricultural_equipment(self, network: Network) -> None:
        """Add agricultural specific equipment."""
        # Agricultural processing loads
        agricultural_loads = []
        for i in range(3):
            agricultural_loads.append({
                "name": f"agricultural_processing_{i}",
                "bus": f"distribution_bus_{i + 5}",
                "p_set": np.random.uniform(2.0, 15.0),  # MW
                "carrier": "AC",
                "type": "agricultural_processing",
                "profile_type": "agricultural_processing"
            })
        
        for load_data in agricultural_loads:
            network.add(
                "Load",
                load_data["name"],
                bus=load_data["bus"],
                p_set=load_data["p_set"],
                carrier=load_data["carrier"],
                type=load_data["type"],
                profile_type=load_data["profile_type"]
            )
        
        # Irrigation pumps
        irrigation_loads = []
        for i in range(4):
            irrigation_loads.append({
                "name": f"irrigation_pump_{i}",
                "bus": f"distribution_bus_{i + 2}",
                "p_set": np.random.uniform(0.1, 1.0),  # MW
                "carrier": "AC",
                "type": "irrigation",
                "profile_type": "irrigation_seasonal"
            })
        
        for load_data in irrigation_loads:
            network.add(
                "Load",
                load_data["name"],
                bus=load_data["bus"],
                p_set=load_data["p_set"],
                carrier=load_data["carrier"],
                type=load_data["type"],
                profile_type=load_data["profile_type"]
            )
        
        # Biomass storage
        for i in range(2):
            network.add(
                "Store",
                f"biomass_storage_{i}",
                bus=f"distribution_bus_{i + 8}",
                e_nom=np.random.uniform(100.0, 500.0),  # MWh biomass
                carrier="biomass",
                type="agricultural_residue",
                marginal_cost=0.0
            )
    
    def get_energy_carriers(self) -> List[str]:
        """Return rural energy carriers."""
        return [
            "electricity", "solar", "wind", "biomass", "biogas", "hydro", 
            "battery", "agricultural_waste", "rural_heating"
        ]
    
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return rural equipment types."""
        return {
            "generation": ["rural_pv", "solar_farm", "rural_wind", "biomass_st", "biogas_engine", "small_hydro"],
            "storage": ["rural_battery", "farm_scale_battery"],
            "agricultural": ["irrigation_pump", "agricultural_processing", "grain_drying"],
            "residential": ["rural_heating", "residential_pv"],
            "transport": ["farm_vehicle_charging", "agricultural_equipment"]
        }
    
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return rural topology rules."""
        return {
            "voltage_levels": [110, 35, 20, 0.4],  # kV
            "connection_rules": {
                "residential_to_distribution": "20kV",
                "agricultural_to_distribution": "20kV",
                "substation_to_distribution": "35kV",
                "transmission_to_substation": "110kV"
            },
            "redundancy": "low",
            "density": "low",
            "grid_structure": "radial_distribution",
            "renewable_integration": "high_penetration",
            "storage_deployment": "distributed"
        }