"""
Railway scenario template for railway transportation energy systems.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .base import BaseScenarioTemplate
from pypsa import Network


class RailwayScenarioTemplate(BaseScenarioTemplate):
    """Railway scenario template for railway transportation energy systems modeling."""
    
    def __init__(self):
        super().__init__(
            name="Railway",
            description="Railway transportation energy system with overhead catenary, traction substations, and regenerative braking"
        )
        self.config = {
            "voltage_levels": [110, 25, 15, 1.5, 0.75, 0.75],  # kV (including DC levels)
            "density": "linear",
            "load_pattern": "railway_movement",
            "transport": "train_operation",
            "heating": "traction_resistors"
        }
    
    def create_network(self, 
                      num_buses: int = 30,
                      num_traction_substations: int = 8,
                      num_feeder_stations: int = 6,
                      num_regeneration_points: int = 12,
                      num_hydrogen_stations: int = 3,
                      **kwargs) -> Network:
        """Create railway energy network.
        
        Parameters
        ----------
        num_buses : int
            Total number of buses
        num_traction_substations : int
            Number of traction substations
        num_feeder_stations : int
            Number of feeder/sub-feeder stations
        num_regeneration_points : int
            Number of regenerative braking capture points
        num_hydrogen_stations : int
            Number of hydrogen refueling stations
            
        Returns
        -------
        Network
            Configured railway energy network
        """
        network = Network()
        
        # Add buses
        buses_data = self._generate_railway_buses(num_buses, num_traction_substations, 
                                                num_feeder_stations, num_regeneration_points, num_hydrogen_stations)
        self.add_buses(network, buses_data)
        
        # Add generators
        generators_data = self._generate_railway_generators()
        self.add_generators(network, generators_data)
        
        # Add loads
        loads_data = self._generate_railway_loads(num_traction_substations, num_feeder_stations)
        self.add_loads(network, loads_data)
        
        # Add storage units
        storage_data = self._generate_railway_storage()
        self.add_storage_units(network, storage_data)
        
        # Add railway specific equipment
        self._add_railway_equipment(network)
        
        # Add transmission links
        links_data = self._generate_railway_links()
        self.add_links(network, links_data)
        
        # Add hydrogen infrastructure
        self._add_hydrogen_infrastructure(network)
        
        self.network = network
        return network
    
    def _generate_railway_buses(self, num_buses: int, num_traction_substations: int, 
                               num_feeder_stations: int, num_regeneration_points: int, 
                               num_hydrogen_stations: int) -> pd.DataFrame:
        """Generate railway bus configuration."""
        buses = []
        
        # Add transmission level buses (110kV)
        for i in range(min(3, num_buses // 10)):
            buses.append({
                "name": f"railway_transmission_{i}",
                "v_nom": 110.0,
                "x": np.random.uniform(-20000, 20000),
                "y": np.random.uniform(-5000, 5000),
                "carrier": "AC",
                "location_type": "transmission",
                "region": "railway_transmission"
            })
        
        # Add traction substation buses (25kV AC)
        traction_buses = min(num_traction_substations, 8)
        for i in range(traction_buses):
            buses.append({
                "name": f"traction_substation_{i}",
                "v_nom": 25.0,
                "x": np.random.uniform(-15000, 15000) + i * 2000,  # Along railway line
                "y": np.random.uniform(-2000, 2000),
                "carrier": "AC_25kV",
                "location_type": "traction_substation",
                "region": f"substation_{i}"
            })
        
        # Add feeder station buses (15kV AC for some European systems)
        feeder_buses = min(num_feeder_stations, 6)
        for i in range(feeder_buses):
            buses.append({
                "name": f"feeder_station_{i}",
                "v_nom": 15.0,
                "x": np.random.uniform(-10000, 10000) + i * 3000,
                "y": np.random.uniform(-1500, 1500),
                "carrier": "AC_15kV",
                "location_type": "feeder_station",
                "region": f"feeder_{i}"
            })
        
        # Add DC traction buses (1.5kV DC)
        dc_bus_count = min(num_traction_substations // 2, 4)
        for i in range(dc_bus_count):
            buses.append({
                "name": f"dc_traction_bus_{i}",
                "v_nom": 1.5,
                "x": np.random.uniform(-8000, 8000) + i * 4000,
                "y": np.random.uniform(-1000, 1000),
                "carrier": "DC_1.5kV",
                "location_type": "dc_traction",
                "region": f"dc_substation_{i}"
            })
        
        # Add regenerative braking capture points
        regen_buses = min(num_regeneration_points, 12)
        for i in range(regen_buses):
            buses.append({
                "name": f"regeneration_point_{i}",
                "v_nom": 0.75,  # Lower voltage for regen capture
                "x": np.random.uniform(-12000, 12000) + i * 2000,
                "y": np.random.uniform(-800, 800),
                "carrier": "DC_750V",
                "location_type": "regeneration",
                "region": f"regen_point_{i}"
            })
        
        # Add hydrogen refueling station buses
        h2_bus_count = min(num_hydrogen_stations, 3)
        for i in range(h2_bus_count):
            buses.append({
                "name": f"hydrogen_station_{i}",
                "v_nom": 1.0,
                "x": np.random.uniform(-5000, 5000),
                "y": np.random.uniform(-1000, 1000),
                "carrier": "hydrogen",
                "location_type": "hydrogen_station",
                "region": f"hydrogen_facility_{i}"
            })
        
        return pd.DataFrame(buses)
    
    def _generate_railway_generators(self) -> pd.DataFrame:
        """Generate railway generator configuration."""
        generators = []
        
        # Traction substation generators (AC feeds)
        for i in range(8):
            generators.append({
                "name": f"traction_substation_gen_{i}",
                "bus": f"traction_substation_{i}",
                "p_nom": np.random.uniform(15.0, 50.0),  # MW
                "marginal_cost": 45.0,
                "carrier": "grid_electricity",
                "efficiency": 0.92,
                "ramp_up_rate": 0.2,
                "ramp_down_rate": 0.2,
                "type": "traction_feeder"
            })
        
        # Solar PV installations near railway stations
        for i in range(10):
            if i < 8:
                bus_name = f"feeder_station_{i}" if i < 6 else f"traction_substation_{i-6}"
            else:
                bus_name = f"railway_transmission_{i-8}"
            
            generators.append({
                "name": f"railway_solar_{i}",
                "bus": bus_name,
                "p_nom": np.random.uniform(2.0, 10.0),  # MW
                "marginal_cost": 28.0,
                "carrier": "solar",
                "efficiency": 0.20,
                "ramp_up_rate": 0.5,
                "ramp_down_rate": 0.5,
                "type": "railway_solar"
            })
        
        # Wind generators along railway corridors
        for i in range(4):
            generators.append({
                "name": f"railway_wind_{i}",
                "bus": f"railway_transmission_{i}",
                "p_nom": np.random.uniform(5.0, 25.0),  # MW
                "marginal_cost": 32.0,
                "carrier": "wind",
                "efficiency": 0.45,
                "ramp_up_rate": 0.1,
                "ramp_down_rate": 0.1,
                "type": "railway_wind"
            })
        
        # Hydrogen generators for hydrogen trains
        for i in range(3):
            generators.append({
                "name": f"hydrogen_generator_{i}",
                "bus": f"hydrogen_station_{i}",
                "p_nom": np.random.uniform(2.0, 8.0),  # MW
                "marginal_cost": 60.0,  # Higher cost for hydrogen generation
                "carrier": "hydrogen",
                "efficiency": 0.65,
                "ramp_up_rate": 0.3,
                "ramp_down_rate": 0.3,
                "type": "hydrogen_production"
            })
        
        return pd.DataFrame(generators)
    
    def _generate_railway_loads(self, num_traction_substations: int, num_feeder_stations: int) -> pd.DataFrame:
        """Generate railway load configuration."""
        loads = []
        
        # Traction loads (train operation)
        for i in range(num_traction_substations):
            loads.append({
                "name": f"traction_load_{i}",
                "bus": f"traction_substation_{i}",
                "p_set": np.random.uniform(10.0, 40.0),  # MW
                "carrier": "AC_25kV",
                "type": "traction_load",
                "profile_type": "railway_hourly"
            })
        
        # Feeder station loads
        for i in range(min(num_feeder_stations, 6)):
            loads.append({
                "name": f"feeder_load_{i}",
                "bus": f"feeder_station_{i}",
                "p_set": np.random.uniform(5.0, 20.0),  # MW
                "carrier": "AC_15kV",
                "type": "feeder_load",
                "profile_type": "railway_hourly"
            })
        
        # Station auxiliary loads
        for i in range(6):
            loads.append({
                "name": f"station_aux_load_{i}",
                "bus": f"feeder_station_{i}" if i < 6 else f"traction_substation_{i-6}",
                "p_set": np.random.uniform(0.5, 3.0),  # MW
                "carrier": "AC",
                "type": "station_auxiliary",
                "profile_type": "station_operations"
            })
        
        # Maintenance facility loads
        for i in range(3):
            loads.append({
                "name": f"maintenance_load_{i}",
                "bus": f"railway_transmission_{i}",
                "p_set": np.random.uniform(2.0, 8.0),  # MW
                "carrier": "AC",
                "type": "maintenance_facility",
                "profile_type": "industrial_day_shift"
            })
        
        return pd.DataFrame(loads)
    
    def _generate_railway_storage(self) -> pd.DataFrame:
        """Generate railway storage configuration."""
        storage = []
        
        # Battery storage at regenerative braking points
        for i in range(8):
            storage.append({
                "name": f"regen_battery_{i}",
                "bus": f"regeneration_point_{i}",
                "p_nom": np.random.uniform(5.0, 20.0),  # MW
                "energy_capacity": np.random.uniform(15.0, 80.0),  # MWh
                "marginal_cost": 25.0,
                "efficiency_store": 0.90,
                "efficiency_dispatch": 0.92,
                "min_state_of_charge": 0.1,
                "carrier": "battery",
                "type": "regeneration_battery"
            })
        
        # Super capacitor banks for rapid regen capture
        for i in range(4):
            storage.append({
                "name": f"supercap_bank_{i}",
                "bus": f"regeneration_point_{i}",
                "p_nom": np.random.uniform(10.0, 30.0),  # MW
                "energy_capacity": np.random.uniform(2.0, 10.0),  # MWh (short duration)
                "marginal_cost": 15.0,
                "efficiency_store": 0.95,
                "efficiency_dispatch": 0.98,
                "min_state_of_charge": 0.1,
                "carrier": "supercapacitor",
                "type": "rapid_regen_storage"
            })
        
        # Hydrogen storage for hydrogen trains
        for i in range(3):
            storage.append({
                "name": f"railway_h2_storage_{i}",
                "bus": f"hydrogen_station_{i}",
                "p_nom": 5.0,  # MW (for dispensing)
                "energy_capacity": np.random.uniform(500.0, 2000.0),  # kg H2
                "marginal_cost": 3.0,
                "efficiency_store": 0.99,
                "efficiency_dispatch": 0.99,
                "min_state_of_charge": 0.1,
                "carrier": "hydrogen",
                "type": "railway_hydrogen_storage"
            })
        
        return pd.DataFrame(storage)
    
    def _add_railway_equipment(self, network: Network) -> None:
        """Add railway specific equipment."""
        # Traction transformers
        for i in range(8):
            network.add(
                "Link",
                f"traction_transformer_{i}",
                bus0=f"railway_transmission_{i//3}",  # Connect to transmission
                bus1=f"traction_substation_{i}",
                p_nom=np.random.uniform(30.0, 100.0),
                efficiency=0.98,
                marginal_cost=2.0,
                carrier="AC_to_AC_25kV",
                type="traction_transformer"
            )
        
        # AC-DC converters for DC traction
        for i in range(4):
            network.add(
                "Link",
                f"ac_dc_converter_{i}",
                bus0=f"traction_substation_{i}",
                bus1=f"dc_traction_bus_{i}",
                p_nom=np.random.uniform(20.0, 60.0),
                efficiency=0.95,
                marginal_cost=8.0,
                carrier="AC_25kV_to_DC_1.5kV",
                type="traction_rectifier"
            )
        
        # Traction inverters for regenerative braking
        for i in range(8):
            network.add(
                "Link",
                f"traction_inverter_{i}",
                bus0=f"regeneration_point_{i}",
                bus1=f"traction_substation_{i//2}",
                p_nom=np.random.uniform(10.0, 30.0),
                efficiency=0.93,
                marginal_cost=10.0,
                carrier="DC_750V_to_AC_25kV",
                type="regeneration_inverter"
            )
        
        # Traction resistors for dynamic braking
        for i in range(6):
            network.add(
                "Link",
                f"braking_resistor_{i}",
                bus0=f"regeneration_point_{i}",
                bus1="resistive_heat_bus",
                p_nom=np.random.uniform(15.0, 40.0),
                efficiency=0.0,  # Dissipates as heat
                marginal_cost=0.5,
                carrier="electric_to_heat",
                type="dynamic_braking_resistor"
            )
    
    def _add_hydrogen_infrastructure(self, network: Network) -> None:
        """Add hydrogen infrastructure for hydrogen trains."""
        # Electrolyzers at hydrogen stations
        for i in range(3):
            network.add(
                "Link",
                f"railway_electrolyzer_{i}",
                bus0=f"hydrogen_station_{i}",
                bus1="electricity_bus",
                p_nom=np.random.uniform(3.0, 10.0),
                efficiency=0.68,  # kWh/kg H2
                marginal_cost=25.0,
                carrier="electricity_to_hydrogen",
                type="railway_electrolyzer"
            )
        
        # Hydrogen compressors
        for i in range(3):
            network.add(
                "Link",
                f"hydrogen_compressor_{i}",
                bus0="low_pressure_hydrogen_bus",
                bus1=f"high_pressure_hydrogen_bus_{i}",
                p_nom=2.0,
                efficiency=0.85,
                marginal_cost=5.0,
                carrier="hydrogen_compression",
                type="hydrogen_compressor"
            )
                
    
    def _generate_railway_links(self) -> pd.DataFrame:
        """Generate railway link configuration."""
        links = []
        
        # Transmission links between substations
        for i in range(7):
            links.append({
                "name": f"catenary_link_{i}",
                "bus0": f"traction_substation_{i}",
                "bus1": f"traction_substation_{i+1}",
                "p_nom": np.random.uniform(25.0, 80.0),  # MW
                "marginal_cost": 3.0,
                "efficiency": 0.97,
                "carrier": "AC_25kV",
                "type": "catenary_line"
            })
        
        # DC traction connections
        for i in range(3):
            links.append({
                "name": f"dc_traction_link_{i}",
                "bus0": f"dc_traction_bus_{i}",
                "bus1": f"dc_traction_bus_{i+1}",
                "p_nom": np.random.uniform(15.0, 50.0),  # MW
                "marginal_cost": 2.0,
                "efficiency": 0.98,
                "carrier": "DC_1.5kV",
                "type": "dc_traction_line"
            })
        
        # Regeneration capture links
        for i in range(8):
            links.append({
                "name": f"regen_capture_link_{i}",
                "bus0": f"regeneration_point_{i}",
                "bus1": f"traction_substation_{i//2}",
                "p_nom": np.random.uniform(8.0, 25.0),  # MW
                "marginal_cost": 1.0,
                "efficiency": 0.95,
                "carrier": "DC_750V",
                "type": "regeneration_feeder"
            })
        
        return pd.DataFrame(links)
    
    def get_energy_carriers(self) -> List[str]:
        """Return list of energy carriers for railway scenario."""
        return [
            "electricity", "AC_25kV", "AC_15kV", "DC_1.5kV", "DC_750V", 
            "hydrogen", "solar", "wind", "battery", "supercapacitor"
        ]
    
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return equipment types grouped by category."""
        return {
            "generation": ["traction_feeder", "railway_solar", "railway_wind", "hydrogen_production"],
            "storage": ["regeneration_battery", "rapid_regen_storage", "railway_hydrogen_storage"],
            "conversion": ["traction_transformer", "traction_rectifier", "regeneration_inverter", 
                         "dynamic_braking_resistor", "railway_electrolyzer", "hydrogen_compressor"],
            "loads": ["traction_load", "feeder_load", "station_auxiliary", "maintenance_facility"],
            "transport": ["electric_train", "hydrogen_train", "diesel_train", "maintenance_vehicle"],
            "infrastructure": ["catenary_system", "railway_substation", "track_feeder", "signaling_system"]
        }
    
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return network topology rules."""
        return {
            "voltage_levels": [110, 25, 15, 1.5, 0.75],
            "bus_spacing": {"min": 1000, "max": 5000},  # meters along railway
            "cable_ratings": {"110kV": 100, "25kV": 50, "15kV": 30, "1.5kV": 25, "0.75kV": 15},  # MW
            "connection_rules": {
                "traction_substation": "dual_feed",
                "feeder_station": "radial",
                "regeneration_point": "bidirectional"
            },
            "railway_specific": {
                "catenary_system": True,
                "regenerative_braking": True,
                "traction_power_quality": "EN_50163",
                "harmonics": "IEC_61000_3_6",
                "voltage_variations": "IEC_61000_3_7"
            },
            "power_quality": {
                "harmonic_limits": "EN_50160",
                "voltage_fluctuation": "IEC_61000_3_7",
                "power_factor": "0.95_leading_lagging"
            },
            "transport_integration": True,
            "regeneration_support": True,
            "hydrogen_infrastructure": True
        }