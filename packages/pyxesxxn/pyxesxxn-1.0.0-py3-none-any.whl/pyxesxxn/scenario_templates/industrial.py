"""
Industrial scenario template for industrial energy systems.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .base import BaseScenarioTemplate
from pypsa import Network


class IndustrialScenarioTemplate(BaseScenarioTemplate):
    """Industrial scenario template for industrial energy systems modeling."""
    
    def __init__(self):
        super().__init__(
            name="Industrial",
            description="Industrial energy system with process heat, manufacturing loads, and industrial processes"
        )
        self.config = {
            "voltage_levels": [110, 20, 10, 0.4],  # kV
            "density": "medium",
            "load_pattern": "industrial_continuous",
            "transport": "industrial_vehicles",
            "heating": "process_heating",
            "industry_type": "manufacturing"
        }
    
    def create_network(self, 
                      num_buses: int = 25,
                      num_heavy_industry: int = 8,
                      num_light_industry: int = 10,
                      num_process_heat: int = 7,
                      **kwargs) -> Network:
        """Create industrial energy network.
        
        Parameters
        ----------
        num_buses : int
            Total number of buses
        num_heavy_industry : int
            Number of heavy industry facilities
        num_light_industry : int
            Number of light industry facilities
        num_process_heat : int
            Number of process heating systems
            
        Returns
        -------
        Network
            Configured industrial energy network
        """
        network = Network()
        
        # Add buses
        buses_data = self._generate_industrial_buses(num_buses, num_heavy_industry, 
                                                   num_light_industry, num_process_heat)
        self.add_buses(network, buses_data)
        
        # Add generators
        generators_data = self._generate_industrial_generators()
        self.add_generators(network, generators_data)
        
        # Add loads
        loads_data = self._generate_industrial_loads(num_heavy_industry, num_light_industry, num_process_heat)
        self.add_loads(network, loads_data)
        
        # Add storage units
        storage_data = self._generate_industrial_storage()
        self.add_storage_units(network, storage_data)
        
        # Add industrial processes
        self._add_industrial_processes(network)
        
        # Add process heating systems
        self._add_process_heating(network)
        
        # Add transmission links
        links_data = self._generate_industrial_links()
        self.add_links(network, links_data)
        
        self.network = network
        return network
    
    def _generate_industrial_buses(self, num_buses: int, num_heavy_industry: int, 
                                  num_light_industry: int, num_process_heat: int) -> pd.DataFrame:
        """Generate industrial bus configuration."""
        buses = []
        
        # Add transmission level buses (110kV)
        for i in range(min(3, num_buses // 8)):
            buses.append({
                "name": f"industrial_transmission_{i}",
                "v_nom": 110.0,
                "x": np.random.uniform(-5000, 5000),
                "y": np.random.uniform(-5000, 5000),
                "carrier": "AC",
                "location_type": "transmission",
                "region": "industrial_zone"
            })
        
        # Add medium voltage buses (20kV)
        remaining_buses = num_buses - len(buses)
        for i in range(remaining_buses):
            if i < num_heavy_industry:
                bus_type = "heavy_industry"
                region = "heavy_industrial_area"
            elif i < num_heavy_industry + num_light_industry:
                bus_type = "light_industry"
                region = "light_industrial_area"
            else:
                bus_type = "process_heat"
                region = "process_heating_zone"
            
            buses.append({
                "name": f"industrial_bus_{i}",
                "v_nom": 20.0,
                "x": np.random.uniform(-3000, 3000),
                "y": np.random.uniform(-3000, 3000),
                "carrier": "AC",
                "location_type": bus_type,
                "region": region
            })
        
        return pd.DataFrame(buses)
    
    def _generate_industrial_generators(self) -> pd.DataFrame:
        """Generate industrial generator configuration."""
        generators = []
        
        # Combined Heat and Power (CHP) units for industrial processes
        for i in range(6):
            generators.append({
                "name": f"industrial_chp_{i}",
                "bus": f"industrial_bus_{i}",
                "p_nom": np.random.uniform(10.0, 50.0),  # MW
                "marginal_cost": 55.0,
                "carrier": "natural_gas",
                "efficiency": 0.85,  # Total efficiency (electric + heat)
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "industrial_chp"
            })
        
        # Waste heat recovery generators
        for i in range(4):
            generators.append({
                "name": f"waste_heat_gen_{i}",
                "bus": f"industrial_bus_{num_heavy_industry + i}",
                "p_nom": np.random.uniform(3.0, 15.0),  # MW
                "marginal_cost": 15.0,
                "carrier": "waste_heat",
                "efficiency": 0.25,
                "ramp_up_rate": 0.5,
                "ramp_down_rate": 0.5,
                "type": "waste_heat_recovery"
            })
        
        # Solar PV for industrial rooftops
        for i in range(8):
            generators.append({
                "name": f"industrial_solar_{i}",
                "bus": f"industrial_bus_{num_heavy_industry + num_light_industry + i}",
                "p_nom": np.random.uniform(2.0, 12.0),  # MW
                "marginal_cost": 25.0,
                "carrier": "solar",
                "efficiency": 0.20,
                "ramp_up_rate": 1.0,
                "ramp_down_rate": 1.0,
                "type": "industrial_solar"
            })
        
        # Industrial wind turbines
        for i in range(3):
            generators.append({
                "name": f"industrial_wind_{i}",
                "bus": f"industrial_transmission_{i}",
                "p_nom": np.random.uniform(5.0, 20.0),  # MW
                "marginal_cost": 30.0,
                "carrier": "wind",
                "efficiency": 0.45,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "industrial_wind"
            })
        
        return pd.DataFrame(generators)
    
    def _generate_industrial_loads(self, num_heavy_industry: int, num_light_industry: int, 
                                  num_process_heat: int) -> pd.DataFrame:
        """Generate industrial load configuration."""
        loads = []
        
        # Heavy industry loads (steel, chemicals, etc.)
        for i in range(num_heavy_industry):
            loads.append({
                "name": f"heavy_industry_load_{i}",
                "bus": f"industrial_bus_{i}",
                "p_set": np.random.uniform(20.0, 100.0),  # MW
                "carrier": "AC",
                "type": "heavy_industry",
                "profile_type": "continuous_24h"
            })
        
        # Light industry loads (manufacturing, assembly, etc.)
        for i in range(num_light_industry):
            loads.append({
                "name": f"light_industry_load_{i}",
                "bus": f"industrial_bus_{num_heavy_industry + i}",
                "p_set": np.random.uniform(5.0, 30.0),  # MW
                "carrier": "AC",
                "type": "light_industry",
                "profile_type": "industrial_day_shift"
            })
        
        # Process heating loads
        for i in range(num_process_heat):
            loads.append({
                "name": f"process_heat_load_{i}",
                "bus": f"industrial_bus_{num_heavy_industry + num_light_industry + i}",
                "p_set": np.random.uniform(10.0, 50.0),  # MW
                "carrier": "heat",
                "type": "process_heating",
                "profile_type": "continuous_24h"
            })
        
        return pd.DataFrame(loads)
    
    def _generate_industrial_storage(self) -> pd.DataFrame:
        """Generate industrial storage configuration."""
        storage = []
        
        # Industrial battery storage for peak shaving
        for i in range(4):
            storage.append({
                "name": f"industrial_battery_{i}",
                "bus": f"industrial_bus_{i}",
                "p_nom": np.random.uniform(5.0, 25.0),  # MW
                "energy_capacity": np.random.uniform(20.0, 100.0),  # MWh
                "marginal_cost": 20.0,
                "efficiency_store": 0.92,
                "efficiency_dispatch": 0.95,
                "min_state_of_charge": 0.1,
                "carrier": "battery",
                "type": "industrial_battery"
            })
        
        # Thermal storage for process heat
        storage.append({
            "name": "thermal_storage",
            "bus": "industrial_bus_0",
            "p_nom": 30.0,  # MW thermal
            "energy_capacity": 200.0,  # MWh thermal
            "marginal_cost": 5.0,
            "efficiency_store": 0.98,
            "efficiency_dispatch": 0.98,
            "min_state_of_charge": 0.1,
            "carrier": "thermal",
            "type": "industrial_thermal"
        })
        
        return pd.DataFrame(storage)
    
    def _add_industrial_processes(self, network: Network) -> None:
        """Add industrial process equipment."""
        # Electrolysis for hydrogen production
        network.add(
            "Link",
            "industrial_electrolyzer",
            bus0="industrial_bus_0",
            bus1="hydrogen_bus",
            p_nom=20.0,
            efficiency=0.65,  # kWh/kg H2
            marginal_cost=25.0,
            carrier="electricity_to_hydrogen",
            type="industrial_electrolyzer"
        )
        
        # Hydrogen storage
        network.add(
            "StorageUnit",
            "industrial_hydrogen_storage",
            bus="hydrogen_bus",
            p_nom=15.0,
            energy_capacity=1000.0,  # kg H2
            marginal_cost=2.0,
            efficiency_store=0.98,
            efficiency_dispatch=0.98,
            carrier="hydrogen",
            type="compressed_gas"
        )
        
        # Industrial air compression
        network.add(
            "Link",
            "air_compressor",
            bus0="industrial_bus_1",
            bus1="compressed_air_bus",
            p_nom=8.0,
            efficiency=0.88,
            marginal_cost=8.0,
            carrier="electricity_to_compressed_air",
            type="industrial_compressor"
        )
    
    def _add_process_heating(self, network: Network) -> None:
        """Add process heating systems."""
        # High temperature heat pumps
        for i in range(3):
            network.add(
                "Link",
                f"heat_pump_{i}",
                bus0=f"industrial_bus_{num_process_heat + i}",
                bus1=f"process_heat_bus_{i}",
                p_nom=np.random.uniform(15.0, 40.0),
                efficiency=3.5,  # COP
                marginal_cost=12.0,
                carrier="electricity_to_heat",
                type="high_temp_heat_pump"
            )
        
        # Industrial boilers (backup)
        for i in range(2):
            network.add(
                "Link",
                f"industrial_boiler_{i}",
                bus0="natural_gas_bus",
                bus1=f"process_heat_bus_{i}",
                p_nom=np.random.uniform(20.0, 60.0),
                efficiency=0.90,
                marginal_cost=35.0,
                carrier="natural_gas_to_heat",
                type="industrial_boiler"
            )
    
    def _generate_industrial_links(self) -> pd.DataFrame:
        """Generate industrial link configuration."""
        links = []
        
        # Transmission links
        for i in range(3):
            for j in range(8):
                bus_idx = i * 8 + j
                if bus_idx < 20:
                    links.append({
                        "name": f"transmission_link_{bus_idx}",
                        "bus0": f"industrial_transmission_{i}",
                        "bus1": f"industrial_bus_{bus_idx}",
                        "p_nom": np.random.uniform(20.0, 80.0),  # MW
                        "marginal_cost": 4.0,
                        "efficiency": 0.97,
                        "carrier": "electricity",
                        "type": "industrial_transmission"
                    })
        
        # Process heat distribution links
        for i in range(7):
            links.append({
                "name": f"process_heat_link_{i}",
                "bus0": f"industrial_bus_{num_heavy_industry + num_light_industry + i}",
                "bus1": f"process_heat_bus_{i}",
                "p_nom": np.random.uniform(5.0, 30.0),  # MW thermal
                "marginal_cost": 2.0,
                "efficiency": 0.95,
                "carrier": "heat",
                "type": "heat_distribution"
            })
        
        return pd.DataFrame(links)
    
    def get_energy_carriers(self) -> List[str]:
        """Return list of energy carriers for industrial scenario."""
        return [
            "electricity", "natural_gas", "hydrogen", "process_heat", 
            "compressed_air", "solar", "wind", "waste_heat", "battery", "thermal"
        ]
    
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return equipment types grouped by category."""
        return {
            "generation": ["chp", "waste_heat_recovery", "solar_pv", "wind_turbine"],
            "storage": ["industrial_battery", "thermal_storage", "hydrogen_storage"],
            "conversion": ["electrolyzer", "heat_pump", "compressor", "boiler"],
            "loads": ["heavy_industry", "light_industry", "process_heating"],
            "transport": ["industrial_vehicles", "forklift", "heavy_trucks"],
            "infrastructure": ["industrial_transformer", "process_control", "ems"]
        }
    
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return network topology rules."""
        return {
            "voltage_levels": [110, 20, 10, 0.4],
            "bus_spacing": {"min": 200, "max": 1000},  # meters
            "cable_ratings": {"110kV": 100, "20kV": 50, "10kV": 25, "0.4kV": 10},  # MW
            "connection_rules": {
                "heavy_industry": "dual_feed",
                "light_industry": "radial",
                "process_heat": "radial"
            },
            "power_quality": {
                "harmonic_limits": "IEEE_519",
                "voltage_fluctuation": "IEC_61000",
                "power_factor": "0.95_leading_lagging"
            },
            "process_integration": True,
            "cogeneration_support": True,
            "demand_response": True
        }