"""
Port scenario template for port and maritime energy systems.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from .base import BaseScenarioTemplate
from pypsa import Network


class PortScenarioTemplate(BaseScenarioTemplate):
    """Port scenario template for port and maritime energy systems modeling."""
    
    def __init__(self):
        super().__init__(
            name="Port",
            description="Port energy system with container terminals, ship-to-shore power, hydrogen production"
        )
        self.config = {
            "voltage_levels": [110, 20, 6.6, 0.4],  # kV
            "density": "medium",
            "load_pattern": "port_operations_heavy_industry",
            "transport": "ship_shore_power",
            "heating": "industrial_processing"
        }
    
    def create_network(self, 
                      num_buses: int = 18,
                      num_terminals: int = 6,
                      num_marine: int = 4,
                      num_industrial: int = 4,
                      num_offshore: int = 2,
                      **kwargs) -> Network:
        """Create port energy network.
        
        Parameters
        ----------
        num_buses : int
            Total number of buses
        num_terminals : int
            Number of container terminals
        num_marine : int
            Number of marine/quay side connections
        num_industrial : int
            Number of port industrial facilities
        num_offshore : int
            Number of offshore wind connections
            
        Returns
        -------
        Network
            Configured port energy network
        """
        network = Network()
        
        # Add buses
        buses_data = self._generate_port_buses(num_buses, num_terminals, 
                                             num_marine, num_industrial, num_offshore)
        self.add_buses(network, buses_data)
        
        # Add generators
        generators_data = self._generate_port_generators()
        self.add_generators(network, generators_data)
        
        # Add loads
        loads_data = self._generate_port_loads(num_terminals, num_marine, num_industrial)
        self.add_loads(network, loads_data)
        
        # Add storage units
        storage_data = self._generate_port_storage()
        self.add_storage_units(network, storage_data)
        
        # Add port specific equipment
        self._add_port_specific_equipment(network)
        
        # Add transmission links
        links_data = self._generate_port_links()
        self.add_links(network, links_data)
        
        # Add hydrogen infrastructure
        self._add_hydrogen_infrastructure(network)
        
        self.network = network
        return network
    
    def _generate_port_buses(self, num_buses: int, num_terminals: int, 
                            num_marine: int, num_industrial: int, num_offshore: int) -> pd.DataFrame:
        """Generate port bus configuration."""
        buses = []
        
        # Add transmission level buses (110kV)
        for i in range(min(2, num_buses // 9)):
            buses.append({
                "name": f"port_transmission_bus_{i}",
                "v_nom": 110.0,
                "x": np.random.uniform(-5000, 5000),
                "y": np.random.uniform(-2000, 2000),
                "carrier": "AC",
                "location_type": "transmission",
                "region": "port_transmission"
            })
        
        # Add main port substation buses (20kV)
        for i in range(min(3, num_buses // 6)):
            buses.append({
                "name": f"port_substation_bus_{i}",
                "v_nom": 20.0,
                "x": np.random.uniform(-3000, 3000),
                "y": np.random.uniform(-1500, 1500),
                "carrier": "AC",
                "location_type": "substation",
                "region": "port_substation"
            })
        
        # Add terminal buses (6.6kV)
        terminal_buses = min(num_terminals, 6)
        for i in range(terminal_buses):
            buses.append({
                "name": f"terminal_bus_{i}",
                "v_nom": 6.6,
                "x": np.random.uniform(-2000, 2000),
                "y": np.random.uniform(-1000, 1000),
                "carrier": "AC",
                "location_type": "terminal",
                "region": f"terminal_{i}"
            })
        
        # Add marine/quay side buses (6.6kV)
        marine_buses = min(num_marine, 4)
        for i in range(marine_buses):
            buses.append({
                "name": f"marine_bus_{i}",
                "v_nom": 6.6,
                "x": np.random.uniform(-1000, 1000),
                "y": np.random.uniform(-500, 500),
                "carrier": "AC",
                "location_type": "marine",
                "region": f"quay_{i}"
            })
        
        # Add industrial area buses (20kV)
        industrial_buses = min(num_industrial, 4)
        for i in range(industrial_buses):
            buses.append({
                "name": f"port_industrial_bus_{i}",
                "v_nom": 20.0,
                "x": np.random.uniform(-1500, 1500),
                "y": np.random.uniform(-800, 800),
                "carrier": "AC",
                "location_type": "industrial",
                "region": f"industrial_area_{i}"
            })
        
        # Add offshore connection buses
        offshore_buses = min(num_offshore, 2)
        for i in range(offshore_buses):
            buses.append({
                "name": f"offshore_bus_{i}",
                "v_nom": 33.0,  # Typical offshore voltage
                "x": np.random.uniform(-3000, -1000),  # Offshore location
                "y": np.random.uniform(-500, 500),
                "carrier": "AC",
                "location_type": "offshore",
                "region": f"offshore_{i}"
            })
        
        # Add hydrogen system buses
        for i in range(2):
            buses.append({
                "name": f"hydrogen_bus_{i}",
                "v_nom": 1.0,  # Low pressure hydrogen
                "x": np.random.uniform(-1000, 1000),
                "y": np.random.uniform(-500, 500),
                "carrier": "hydrogen",
                "location_type": "hydrogen",
                "region": "hydrogen_system"
            })
        
        return pd.DataFrame(buses)
    
    def _generate_port_generators(self) -> pd.DataFrame:
        """Generate port generator configuration."""
        generators = []
        
        # Port PV systems
        for i in range(8):
            bus_name = f"terminal_bus_{i}" if i < 6 else f"port_substation_bus_{i-6}"
            generators.append({
                "name": f"port_pv_{i}",
                "bus": bus_name,
                "p_nom": np.random.uniform(1.0, 8.0),  # MW
                "marginal_cost": 32.0,
                "carrier": "solar",
                "efficiency": 0.20,
                "ramp_up_rate": 0.3,
                "ramp_down_rate": 0.3,
                "type": "port_rooftop_pv"
            })
        
        # Offshore wind connections
        for i in range(2):
            generators.append({
                "name": f"offshore_wind_{i}",
                "bus": f"offshore_bus_{i}",
                "p_nom": np.random.uniform(50.0, 150.0),  # MW
                "marginal_cost": 60.0,
                "carrier": "wind",
                "efficiency": 0.45,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "offshore_wind_farm"
            })
        
        # Port gas turbines (backup/peak)
        for i in range(3):
            generators.append({
                "name": f"port_gas_turbine_{i}",
                "bus": f"port_substation_bus_{i}",
                "p_nom": np.random.uniform(20.0, 50.0),  # MW
                "marginal_cost": 80.0,
                "carrier": "gas",
                "efficiency": 0.35,
                "ramp_up_rate": 0.05,
                "ramp_down_rate": 0.05,
                "type": "port_gas_turbine",
                "fuel_cost": 0.06  # €/kWh
            })
        
        # Emergency diesel generators
        for i in range(4):
            bus_name = f"terminal_bus_{i}" if i < 6 else f"marine_bus_{i-4}"
            generators.append({
                "name": f"emergency_diesel_{i}",
                "bus": bus_name,
                "p_nom": np.random.uniform(2.0, 8.0),  # MW
                "marginal_cost": 120.0,
                "carrier": "diesel",
                "efficiency": 0.40,
                "ramp_up_rate": 0.02,
                "ramp_down_rate": 0.02,
                "type": "emergency_diesel"
            })
        
        # Hydrogen fuel cells (for clean energy)
        for i in range(2):
            generators.append({
                "name": f"hydrogen_fuel_cell_{i}",
                "bus": f"hydrogen_bus_{i}",
                "p_nom": np.random.uniform(3.0, 10.0),  # MW
                "marginal_cost": 85.0,
                "carrier": "hydrogen",
                "efficiency": 0.55,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "hydrogen_fuel_cell"
            })
        
        return pd.DataFrame(generators)
    
    def _generate_port_loads(self, num_terminals: int, num_marine: int, 
                            num_industrial: int) -> pd.DataFrame:
        """Generate port load configuration."""
        loads = []
        
        # Container terminal loads
        for i in range(min(num_terminals, 6)):
            loads.append({
                "name": f"container_terminal_{i}",
                "bus": f"terminal_bus_{i}",
                "p_set": np.random.uniform(5.0, 25.0),  # MW
                "carrier": "AC",
                "type": "container_terminal",
                "profile_type": "port_terminal_operations"
            })
        
        # Ship-to-shore (STS) crane loads
        for i in range(min(num_marine * 2, 8)):
            crane_bus = f"marine_bus_{i // 2}" if i // 2 < num_marine else f"terminal_bus_{i // 2}"
            loads.append({
                "name": f"sts_crane_{i}",
                "bus": crane_bus,
                "p_set": np.random.uniform(1.0, 5.0),  # MW per crane
                "carrier": "AC",
                "type": "sts_crane",
                "profile_type": "port_crane_operations"
            })
        
        # Quay crane loads
        for i in range(min(num_marine * 3, 12)):
            crane_bus = f"marine_bus_{i // 3}" if i // 3 < num_marine else f"terminal_bus_{i // 3}"
            loads.append({
                "name": f"quay_crane_{i}",
                "bus": crane_bus,
                "p_set": np.random.uniform(0.5, 2.0),  # MW per crane
                "carrier": "AC",
                "type": "quay_crane",
                "profile_type": "port_crane_operations"
            })
        
        # Port industrial loads
        for i in range(min(num_industrial, 4)):
            loads.append({
                "name": f"port_industrial_{i}",
                "bus": f"port_industrial_bus_{i}",
                "p_set": np.random.uniform(10.0, 50.0),  # MW
                "carrier": "AC",
                "type": "port_industrial",
                "profile_type": "port_industrial_processing"
            })
        
        # Ship shore power connections
        for i in range(min(num_marine, 4)):
            loads.append({
                "name": f"ship_shore_power_{i}",
                "bus": f"marine_bus_{i}",
                "p_set": np.random.uniform(0.0, 15.0),  # MW (when ships connected)
                "carrier": "AC",
                "type": "ship_shore_power",
                "profile_type": "ship_shore_power"
            })
        
        return pd.DataFrame(loads)
    
    def _generate_port_storage(self) -> pd.DataFrame:
        """Generate port storage configuration."""
        storage = []
        
        # Large scale port battery storage
        for i in range(4):
            storage.append({
                "name": f"port_battery_{i}",
                "bus": f"port_substation_bus_{i}",
                "p_nom": np.random.uniform(5.0, 25.0),  # MW
                "energy_capacity": np.random.uniform(20.0, 100.0),  # MWh
                "marginal_cost": 10.0,
                "efficiency_store": 0.94,
                "efficiency_dispatch": 0.94,
                "min_state_of_charge": 0.2,
                "carrier": "battery",
                "type": "port_scale_battery"
            })
        
        # Terminal-level battery storage
        for i in range(min(num_terminals, 6)):
            storage.append({
                "name": f"terminal_battery_{i}",
                "bus": f"terminal_bus_{i}",
                "p_nom": np.random.uniform(1.0, 5.0),  # MW
                "energy_capacity": np.random.uniform(4.0, 20.0),  # MWh
                "marginal_cost": 15.0,
                "efficiency_store": 0.92,
                "efficiency_dispatch": 0.92,
                "min_state_of_charge": 0.3,
                "carrier": "battery",
                "type": "terminal_battery"
            })
        
        # Hydrogen storage
        for i in range(2):
            storage.append({
                "name": f"hydrogen_storage_{i}",
                "bus": f"hydrogen_bus_{i}",
                "p_nom": np.random.uniform(2.0, 8.0),  # MW (electrolyzer capacity)
                "energy_capacity": np.random.uniform(100.0, 500.0),  # MWh H2
                "marginal_cost": 20.0,
                "efficiency_store": 0.70,  # Electrolysis efficiency
                "efficiency_dispatch": 0.50,  # Fuel cell efficiency
                "min_state_of_charge": 0.1,
                "carrier": "hydrogen",
                "type": "compressed_hydrogen"
            })
        
        return pd.DataFrame(storage)
    
    def _generate_port_links(self) -> pd.DataFrame:
        """Generate port transmission links."""
        links = []
        
        # Transmission to substation connections
        for i in range(2):
            for j in range(3):
                links.append({
                    "name": f"transmission_to_port_sub_{i}_{j}",
                    "bus0": f"port_transmission_bus_{i}",
                    "bus1": f"port_substation_bus_{j}",
                    "p_nom": np.random.uniform(100.0, 300.0),  # MW
                    "marginal_cost": 2.0,
                    "efficiency": 0.98,
                    "carrier": "electricity",
                    "type": "port_transmission",
                    "s_nom": np.random.uniform(150.0, 400.0)  # MVA
                })
        
        # Substation to terminal connections
        for i in range(6):
            terminal_bus_idx = i % 6
            substation_bus_idx = i // 2
            links.append({
                "name": f"substation_to_terminal_{i}",
                "bus0": f"port_substation_bus_{substation_bus_idx}",
                "bus1": f"terminal_bus_{terminal_bus_idx}",
                "p_nom": np.random.uniform(20.0, 60.0),  # MW
                "marginal_cost": 8.0,
                "efficiency": 0.96,
                "carrier": "electricity",
                "type": "port_distribution",
                "s_nom": np.random.uniform(30.0, 80.0)  # MVA
            })
        
        # Substation to marine connections
        for i in range(4):
            marine_bus_idx = i
            substation_bus_idx = i // 2
            links.append({
                "name": f"substation_to_marine_{i}",
                "bus0": f"port_substation_bus_{substation_bus_idx}",
                "bus1": f"marine_bus_{marine_bus_idx}",
                "p_nom": np.random.uniform(15.0, 40.0),  # MW
                "marginal_cost": 10.0,
                "efficiency": 0.95,
                "carrier": "electricity",
                "type": "port_marine_distribution",
                "s_nom": np.random.uniform(20.0, 50.0)  # MVA
            })
        
        # Offshore connections
        for i in range(2):
            offshore_idx = i
            substation_bus_idx = i
            links.append({
                "name": f"offshore_connection_{i}",
                "bus0": f"offshore_bus_{offshore_idx}",
                "bus1": f"port_substation_bus_{substation_bus_idx}",
                "p_nom": np.random.uniform(50.0, 150.0),  # MW
                "marginal_cost": 5.0,
                "efficiency": 0.94,
                "carrier": "electricity",
                "type": "offshore_submarine_cable",
                "s_nom": np.random.uniform(80.0, 200.0)  # MVA
            })
        
        return pd.DataFrame(links)
    
    def _add_port_specific_equipment(self, network: Network) -> None:
        """Add port specific equipment."""
        # Reefer (refrigerated container) loads
        reefer_loads = []
        for i in range(8):
            reefer_loads.append({
                "name": f"reefer_plug_{i}",
                "bus": f"terminal_bus_{i % 6}",
                "p_set": np.random.uniform(0.01, 0.05),  # MW per reefer
                "carrier": "AC",
                "type": "reefer_container",
                "profile_type": "reefer_plug_operations"
            })
        
        for load_data in reefer_loads:
            network.add(
                "Load",
                load_data["name"],
                bus=load_data["bus"],
                p_set=load_data["p_set"],
                carrier=load_data["carrier"],
                type=load_data["type"],
                profile_type=load_data["profile_type"]
            )
        
        # Port service vehicles (electric)
        service_vehicle_loads = []
        for i in range(6):
            service_vehicle_loads.append({
                "name": f"port_service_vehicle_{i}",
                "bus": f"terminal_bus_{i % 6}",
                "p_set": np.random.uniform(0.1, 0.5),  # MW charging
                "carrier": "electricity",
                "type": "port_service_vehicle",
                "profile_type": "port_fleet_charging"
            })
        
        for load_data in service_vehicle_loads:
            network.add(
                "Load",
                load_data["name"],
                bus=load_data["bus"],
                p_set=load_data["p_set"],
                carrier=load_data["carrier"],
                type=load_data["type"],
                profile_type=load_data["profile_type"]
            )
    
    def _add_hydrogen_infrastructure(self, network: Network) -> None:
        """Add hydrogen production and distribution infrastructure."""
        # Electrolyzers
        electrolyzers = []
        for i in range(3):
            electrolyzers.append({
                "name": f"port_electrolyzer_{i}",
                "bus0": f"port_substation_bus_{i}",
                "bus1": f"hydrogen_bus_{i % 2}",
                "p_nom": np.random.uniform(2.0, 8.0),  # MW
                "marginal_cost": 5.0,
                "efficiency": 0.70,  # kWh/kg H2
                "carrier": "hydrogen_production",
                "type": "pem_electrolyzer"
            })
        
        for link_data in electrolyzers:
            network.add(
                "Link",
                link_data["name"],
                bus0=link_data["bus0"],
                bus1=link_data["bus1"],
                p_nom=link_data["p_nom"],
                marginal_cost=link_data["marginal_cost"],
                efficiency=link_data["efficiency"],
                carrier=link_data["carrier"],
                type=link_data["type"]
            )
        
        # Hydrogen pipeline connections
        pipeline_links = []
        for i in range(1):
            pipeline_links.append({
                "name": "hydrogen_pipeline",
                "bus0": "hydrogen_bus_0",
                "bus1": "hydrogen_bus_1",
                "p_nom": np.random.uniform(1.0, 5.0),  # MW H2 flow
                "marginal_cost": 2.0,
                "efficiency": 0.98,
                "carrier": "hydrogen",
                "type": "hydrogen_pipeline"
            })
        
        for link_data in pipeline_links:
            network.add(
                "Link",
                link_data["name"],
                bus0=link_data["bus0"],
                bus1=link_data["bus1"],
                p_nom=link_data["p_nom"],
                marginal_cost=link_data["marginal_cost"],
                efficiency=link_data["efficiency"],
                carrier=link_data["carrier"],
                type=link_data["type"]
            )
        
        # Hydrogen refueling stations for port vehicles
        refueling_loads = []
        for i in range(2):
            refueling_loads.append({
                "name": f"hydrogen_refuel_station_{i}",
                "bus": f"hydrogen_bus_{i}",
                "p_set": np.random.uniform(0.0, 2.0),  # MW H2 compression
                "carrier": "hydrogen",
                "type": "hydrogen_refueling",
                "profile_type": "hydrogen_refueling_station"
            })
        
        for load_data in refueling_loads:
            network.add(
                "Load",
                load_data["name"],
                bus=load_data["bus"],
                p_set=load_data["p_set"],
                carrier=load_data["carrier"],
                type=load_data["type"],
                profile_type=load_data["profile_type"]
            )
    
    def get_energy_carriers(self) -> List[str]:
        """Return port energy carriers."""
        return [
            "electricity", "solar", "wind", "offshore_wind", "gas", "diesel",
            "hydrogen", "battery", "port_operations", "marine_power"
        ]
    
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return port equipment types."""
        return {
            "generation": ["port_pv", "offshore_wind_farm", "port_gas_turbine", "emergency_diesel", "hydrogen_fuel_cell"],
            "terminal": ["container_terminal", "sts_crane", "quay_crane", "reefer_plug"],
            "marine": ["ship_shore_power", "marine_power_connection"],
            "hydrogen": ["pem_electrolyzer", "hydrogen_fuel_cell", "hydrogen_storage", "hydrogen_refueling"],
            "storage": ["port_scale_battery", "terminal_battery", "hydrogen_storage"],
            "transport": ["port_service_vehicle", "ship_shore_power"],
            "industrial": ["port_industrial", "hydrogen_production"]
        }
    
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return port topology rules."""
        return {
            "voltage_levels": [110, 33, 20, 6.6, 0.4],  # kV
            "connection_rules": {
                "terminal_to_substation": "20kV to 6.6kV",
                "marine_to_substation": "20kV to 6.6kV",
                "offshore_connection": "33kV submarine cable",
                "hydrogen_system": "Low pressure hydrogen network"
            },
            "redundancy": "high",
            "density": "medium",
            "grid_structure": "mesh_radial_hybrid",
            "renewable_integration": "very_high",
            "port_specific_features": [
                "ship_to_shore_power",
                "container_terminal_operations", 
                "hydrogen_production",
                "offshore_wind_connection",
                "reefer_container_management"
            ]
        }