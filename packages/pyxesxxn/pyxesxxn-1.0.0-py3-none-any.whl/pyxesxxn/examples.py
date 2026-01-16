# SPDX-FileCopyrightText: PyXESXXN Contributors
#
# SPDX-License-Identifier: MIT

"""Example networks and usage patterns for PyXESXXN."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .network import PyXESXXNNetwork


def create_simple_network() -> PyXESXXNNetwork:
    """Create a simple multi-carrier energy system example.
    
    This example demonstrates basic PyXESXXN functionality with a simple
    electricity and heat network.
    
    Returns
    -------
    PyXESXXNNetwork
        A simple multi-carrier energy system
    """
    from .network import PyXESXXNNetwork
    
    # Create network
    network = PyXESXXNNetwork("Simple Multi-Carrier Network")
    
    # Add buses
    elec_bus = network.add_bus("electricity_bus", "electricity")
    heat_bus = network.add_bus("heat_bus", "heat")
    
    # Add components
    solar_pv = network.add_generator("solar_pv", elec_bus, "electricity", capacity=100, efficiency=0.95)
    gas_boiler = network.add_generator("gas_boiler", heat_bus, "heat", capacity=50, efficiency=0.85)
    
    elec_load = network.add_load("electricity_load", elec_bus, "electricity", demand=80)
    heat_load = network.add_load("heat_load", heat_bus, "heat", demand=30)
    
    return network


def create_urban_energy_system() -> PyXESXXNNetwork:
    """Create an urban energy system example with multiple energy carriers.
    
    This example demonstrates a more complex urban energy system with
    electricity, heat, and hydrogen carriers.
    
    Returns
    -------
    PyXESXXNNetwork
        An urban energy system with multiple carriers
    """
    from .network import PyXESXXNNetwork
    
    network = PyXESXXNNetwork("Urban Multi-Carrier System")
    
    # Add buses for different energy carriers
    elec_bus = network.add_bus("urban_electricity", "electricity")
    heat_bus = network.add_bus("district_heating", "heat")
    hydrogen_bus = network.add_bus("hydrogen_supply", "hydrogen")
    
    # Add generation components
    wind_farm = network.add_generator("wind_farm", elec_bus, "electricity", capacity=200, efficiency=0.98)
    solar_farm = network.add_generator("solar_farm", elec_bus, "electricity", capacity=150, efficiency=0.95)
    chp_plant = network.add_generator("chp_plant", elec_bus, "electricity", capacity=100, efficiency=0.85)
    
    # Add storage components
    battery = network.add_storage_unit("battery_storage", elec_bus, "electricity", capacity=50, efficiency=0.92)
    thermal_storage = network.add_storage_unit("thermal_storage", heat_bus, "heat", capacity=100, efficiency=0.85)
    
    # Add loads
    residential_load = network.add_load("residential_electricity", elec_bus, "electricity", demand=120)
    commercial_load = network.add_load("commercial_electricity", elec_bus, "electricity", demand=80)
    heating_load = network.add_load("district_heating_load", heat_bus, "heat", demand=60)
    
    return network


def create_renewable_integration_model() -> PyXESXXNNetwork:
    """Create a renewable energy integration example.
    
    This example focuses on high renewable penetration with storage
    and flexible loads.
    
    Returns
    -------
    PyXESXXNNetwork
        A renewable integration model
    """
    from .network import PyXESXXNNetwork
    
    network = PyXESXXNNetwork("Renewable Integration Model")
    
    elec_bus = network.add_bus("renewable_grid", "electricity")
    
    # High renewable generation
    offshore_wind = network.add_generator("offshore_wind", elec_bus, "electricity", capacity=500, efficiency=0.98)
    onshore_wind = network.add_generator("onshore_wind", elec_bus, "electricity", capacity=300, efficiency=0.97)
    utility_solar = network.add_generator("utility_solar", elec_bus, "electricity", capacity=400, efficiency=0.95)
    
    # Large-scale storage
    pumped_hydro = network.add_storage_unit("pumped_hydro", elec_bus, "electricity", capacity=200, efficiency=0.80)
    battery_farm = network.add_storage_unit("battery_farm", elec_bus, "electricity", capacity=100, efficiency=0.92)
    
    # Flexible loads
    ev_charging = network.add_load("ev_charging", elec_bus, "electricity", demand=150, flexible=True)
    industrial_load = network.add_load("industrial_load", elec_bus, "electricity", demand=200, flexible=True)
    
    return network


def create_multi_carrier_hub() -> PyXESXXNNetwork:
    """Create a multi-carrier energy hub example.
    
    This example demonstrates an energy hub with conversion between
    multiple energy carriers.
    
    Returns
    -------
    PyXESXXNNetwork
        A multi-carrier energy hub
    """
    from .network import PyXESXXNNetwork
    
    network = PyXESXXNNetwork("Multi-Carrier Energy Hub")
    
    # Energy carrier buses
    elec_bus = network.add_bus("electricity_hub", "electricity")
    gas_bus = network.add_bus("natural_gas_hub", "natural_gas")
    heat_bus = network.add_bus("heat_hub", "heat")
    hydrogen_bus = network.add_bus("hydrogen_hub", "hydrogen")
    
    # Generation and loads
    renewable_gen = network.add_generator("renewable_generation", elec_bus, "electricity", capacity=100)
    gas_supply = network.add_generator("gas_supply", gas_bus, "natural_gas", capacity=80)
    
    elec_load = network.add_load("electricity_demand", elec_bus, "electricity", demand=60)
    heat_load = network.add_load("heat_demand", heat_bus, "heat", demand=40)
    hydrogen_load = network.add_load("hydrogen_demand", hydrogen_bus, "hydrogen", demand=20)
    
    return network