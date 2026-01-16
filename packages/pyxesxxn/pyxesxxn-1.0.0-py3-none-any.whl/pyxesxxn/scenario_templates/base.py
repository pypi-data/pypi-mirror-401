"""
Base classes for scenario templates.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from pypsa import Network


class BaseScenarioTemplate(ABC):
    """Base class for all scenario templates."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize base scenario template.
        
        Parameters
        ----------
        name : str
            Name of the scenario template
        description : str
            Description of the scenario
        """
        self.name = name
        self.description = description
        self.network = None
        self.config = {}
    
    @abstractmethod
    def create_network(self, **kwargs) -> Network:
        """Create the network for this scenario template."""
        pass
    
    @abstractmethod
    def get_energy_carriers(self) -> List[str]:
        """Return list of energy carriers for this scenario."""
        pass
    
    @abstractmethod
    def get_equipment_types(self) -> Dict[str, List[str]]:
        """Return equipment types grouped by category."""
        pass
    
    @abstractmethod
    def get_topology_rules(self) -> Dict[str, Any]:
        """Return network topology rules."""
        pass
    
    def add_buses(self, network: Network, buses_data: pd.DataFrame) -> None:
        """Add buses to the network."""
        for _, bus in buses_data.iterrows():
            network.add(
                "Bus",
                bus.get("name", f"bus_{len(network.buses)}"),
                v_nom=bus.get("v_nom", 110.0),
                x=bus.get("x", 0.0),
                y=bus.get("y", 0.0),
                carrier=bus.get("carrier", "AC"),
                location_type=bus.get("location_type", "urban"),
                region=bus.get("region", "default"),
            )
    
    def add_generators(self, network: Network, generators_data: pd.DataFrame) -> None:
        """Add generators to the network."""
        for _, gen in generators_data.iterrows():
            network.add(
                "Generator",
                gen.get("name", f"gen_{len(network.generators)}"),
                bus=gen["bus"],
                p_nom=gen.get("p_nom", 100.0),
                marginal_cost=gen.get("marginal_cost", 50.0),
                carrier=gen.get("carrier", "solar"),
                efficiency=gen.get("efficiency", 1.0),
                ramp_up_rate=gen.get("ramp_up_rate", 0.1),
                ramp_down_rate=gen.get("ramp_down_rate", 0.1),
                type=gen.get("type", "PV"),
            )
    
    def add_loads(self, network: Network, loads_data: pd.DataFrame) -> None:
        """Add loads to the network."""
        for _, load in loads_data.iterrows():
            network.add(
                "Load",
                load.get("name", f"load_{len(network.loads)}"),
                bus=load["bus"],
                p_set=load.get("p_set", 50.0),
                carrier=load.get("carrier", "AC"),
                type=load.get("type", "residential"),
                profile_type=load.get("profile_type", "residential_annual"),
            )
    
    def add_storage_units(self, network: Network, storage_data: pd.DataFrame) -> None:
        """Add storage units to the network."""
        for _, storage in storage_data.iterrows():
            network.add(
                "StorageUnit",
                storage.get("name", f"storage_{len(network.storage_units)}"),
                bus=storage["bus"],
                p_nom=storage.get("p_nom", 50.0),
                energy_capacity=storage.get("energy_capacity", 200.0),
                marginal_cost=storage.get("marginal_cost", 10.0),
                efficiency_store=storage.get("efficiency_store", 0.95),
                efficiency_dispatch=storage.get("efficiency_dispatch", 0.95),
                min_state_of_charge=storage.get("min_state_of_charge", 0.1),
                carrier=storage.get("carrier", "battery"),
                type=storage.get("type", "lithium_ion"),
            )
    
    def add_links(self, network: Network, links_data: pd.DataFrame) -> None:
        """Add links to the network."""
        for _, link in links_data.iterrows():
            network.add(
                "Link",
                link.get("name", f"link_{len(network.links)}"),
                bus0=link["bus0"],
                bus1=link["bus1"],
                p_nom=link.get("p_nom", 100.0),
                marginal_cost=link.get("marginal_cost", 5.0),
                efficiency=link.get("efficiency", 0.95),
                carrier=link.get("carrier", "electricity"),
                type=link.get("type", "transmission"),
                s_nom=link.get("s_nom", 100.0),
            )
    
    def add_charging_stations(self, network: Network, charging_data: pd.DataFrame) -> None:
        """Add EV charging stations to the network."""
        for _, station in charging_data.iterrows():
            network.add(
                "Load",
                station.get("name", f"charging_{len(network.loads)}"),
                bus=station["bus"],
                p_set=station.get("p_set", 0.0),
                carrier="electricity",
                type="ev_charging",
                profile_type="ev_charging_peak",
            )
    
    def validate_network(self, network: Network) -> bool:
        """Validate the created network."""
        required_components = ["Bus"]
        for comp in required_components:
            if len(getattr(network, comp.lower() + "s")) == 0:
                return False
        return True