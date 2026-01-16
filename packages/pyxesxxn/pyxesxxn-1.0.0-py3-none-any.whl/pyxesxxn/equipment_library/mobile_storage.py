"""
Mobile Storage Equipment Library

This module provides mobile energy storage system (MESS) equipment models
for use in energy system planning and operation.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

from .base import (
    BaseEquipment,
    EquipmentConfig,
    EquipmentCategory,
    EquipmentType,
    EnergyCarrier
)


class MobileStorageEquipment(BaseEquipment):
    """Mobile Energy Storage System (MESS) equipment model.
    
    This class implements a mobile energy storage system that can be 
    moved between different locations, with carbon-aware scheduling.
    """
    
    def __init__(self, 
                 equipment_id: str,
                 config: Optional[EquipmentConfig] = None,
                 location: Optional[str] = None,
                 **kwargs):
        """Initialize mobile storage equipment.
        
        Parameters
        ----------
        equipment_id : str
            Unique equipment identifier
        config : EquipmentConfig, optional
            Equipment configuration
        location : str, optional
            Initial equipment location
        **kwargs
            Additional configuration parameters
        """
        super().__init__(equipment_id, config, location, **kwargs)
        
        # Mobile storage specific state
        self._current_location = location
        self._soc = kwargs.get('initial_soc', 0.5)
        self._carbon_footprint = 0.0
        self._distance_traveled = 0.0
        self._battery_age = 0.0
        
        # Carbon trading parameters
        self._carbon_price = kwargs.get('carbon_price', 50.0)  # 元/吨
        self._carbon_quota = kwargs.get('carbon_quota', 10.0)  # 吨/年
        self._carbon_emissions = 0.0
        
        # Spatial parameters
        self._speed = kwargs.get('speed', 60.0)  # km/h
        self._transport_cost = kwargs.get('transport_cost', 1.0)  # 元/km
        
        # Battery degradation parameters
        self._capacity_decay_rate = kwargs.get('capacity_decay_rate', 0.02)  # 每年容量衰减率
        self._cycle_life = kwargs.get('cycle_life', 3000)  # 循环寿命
        self._remaining_cycles = self._cycle_life
        
    def _create_default_config(self, **kwargs) -> EquipmentConfig:
        """Create default configuration for mobile storage equipment.
        
        Parameters
        ----------
        **kwargs
            Additional configuration parameters
            
        Returns
        -------
        EquipmentConfig
            Default configuration
        """
        return EquipmentConfig(
            equipment_id=self.equipment_id,
            name=f"MobileStorage_{self.equipment_id}",
            description="Mobile Energy Storage System",
            category=EquipmentCategory.STORAGE,
            equipment_type=EquipmentType.BATTERY_STORAGE,
            power_rating=kwargs.get('power_rating', 100.0),
            capacity=kwargs.get('capacity', 400.0),  # kWh
            efficiency=kwargs.get('efficiency', 0.95),
            lifetime=kwargs.get('lifetime', 10),
            investment_costs=kwargs.get('investment_costs', 1500),  # 元/kW
            operation_costs=kwargs.get('operation_costs', 0.1),  # 元/kWh
            co2_emissions=kwargs.get('co2_emissions', 0.001),  # kg CO2/kWh
            scenario=kwargs.get('scenario', 'urban'),
            location=self.location,
            supported_carriers=[EnergyCarrier.ELECTRICITY],
            custom_parameters=kwargs.get('custom_parameters', {
                'battery_type': 'li-ion',
                'max_depth_of_discharge': 0.8,
                'charging_rate': 1.0,
                'discharging_rate': 1.0
            })
        )
    
    def get_default_scenario(self) -> str:
        """Get the default scenario for mobile storage equipment.
        
        Returns
        -------
        str
            Default scenario name
        """
        return "urban"
    
    def create_components(self, network: Any) -> Dict[str, Any]:
        """Create PyXESXXN components for mobile storage.
        
        Parameters
        ----------
        network : PyXESXXNNetwork
            PyXESXXN network to add components to
            
        Returns
        -------
        Dict[str, Any]
            Dictionary of created PyXESXXN components
        """
        # Create storage component
        storage_component = {
            'type': 'storage',
            'id': self.equipment_id,
            'power_rating': self.power_rating,
            'capacity': self.config.capacity,
            'efficiency': self.efficiency,
            'location': self._current_location
        }
        
        return {
            'storage': storage_component
        }
    
    def calculate_performance(self, 
                            input_power: float,
                            time_step: float = 1.0,
                            operating_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate mobile storage performance.
        
        Parameters
        ----------
        input_power : float
            Input power (kW) - positive for charging, negative for discharging
        time_step : float
            Time step (hours)
        operating_conditions : Dict[str, Any], optional
            Operating conditions including location, carbon price, etc.
            
        Returns
        -------
        Dict[str, Any]
            Performance calculation results
        """
        # Update operating conditions if provided
        if operating_conditions:
            self._carbon_price = operating_conditions.get('carbon_price', self._carbon_price)
            if 'location' in operating_conditions and operating_conditions['location'] != self._current_location:
                # Calculate travel distance and cost
                self._distance_traveled += operating_conditions.get('distance', 10.0)
                self._current_location = operating_conditions['location']
        
        # Calculate battery degradation
        depth_of_discharge = abs(input_power * time_step) / self.config.capacity
        self._battery_age += depth_of_discharge
        self._remaining_cycles -= depth_of_discharge
        
        # Calculate carbon emissions from charging
        emissions = 0.0
        if input_power > 0:  # Charging
            emissions = input_power * time_step * self.config.co2_emissions / 1000  # Convert to tons
            self._carbon_emissions += emissions
        
        # Calculate carbon trading cost
        carbon_trading_cost = 0.0
        if self._carbon_emissions > self._carbon_quota:
            excess_emissions = self._carbon_emissions - self._carbon_quota
            carbon_trading_cost = excess_emissions * self._carbon_price
        
        # Calculate capacity decay cost
        capacity_loss = self.config.capacity * self._capacity_decay_rate * time_step / 8760
        capacity_decay_cost = capacity_loss * self.config.investment_costs
        
        # Calculate charging/discharging efficiency
        if input_power > 0:  # Charging
            effective_power = input_power * self.efficiency
            self._soc = min(self._soc + (effective_power * time_step) / self.config.capacity, 1.0)
            efficiency = self.efficiency
        else:  # Discharging
            effective_power = input_power / self.efficiency
            self._soc = max(self._soc + (effective_power * time_step) / self.config.capacity, 0.0)
            efficiency = self.efficiency
        
        # Calculate transport cost
        transport_cost = self._distance_traveled * self._transport_cost
        
        # Calculate total cost
        total_cost = carbon_trading_cost + capacity_decay_cost + transport_cost
        
        # Update current state
        self._current_state.update({
            'power_output': -effective_power if input_power < 0 else 0.0,
            'efficiency': efficiency,
            'soc': self._soc,
            'carbon_emissions': self._carbon_emissions,
            'distance_traveled': self._distance_traveled,
            'battery_age': self._battery_age,
            'remaining_cycles': self._remaining_cycles
        })
        
        return {
            'equipment_id': self.equipment_id,
            'power_output': -effective_power if input_power < 0 else 0.0,
            'soc': self._soc,
            'efficiency': efficiency,
            'carbon_emissions': emissions,
            'carbon_trading_cost': carbon_trading_cost,
            'capacity_decay_cost': capacity_decay_cost,
            'transport_cost': transport_cost,
            'total_cost': total_cost,
            'remaining_cycles': self._remaining_cycles,
            'location': self._current_location,
            'battery_age': self._battery_age
        }
    
    def move_to_location(self, 
                        location: str,
                        distance: float,
                        time: float = 1.0) -> Dict[str, Any]:
        """Move the mobile storage to a new location.
        
        Parameters
        ----------
        location : str
            New location
        distance : float
            Travel distance in km
        time : float
            Travel time in hours
            
        Returns
        -------
        Dict[str, Any]
            Movement results including cost and time
        """
        # Calculate transport cost
        transport_cost = distance * self._transport_cost
        
        # Update state
        self._distance_traveled += distance
        self._current_location = location
        
        # Calculate energy consumption during transport (simplified)
        transport_energy = distance * 0.5  # kWh/km
        self._soc = max(self._soc - transport_energy / self.config.capacity, 0.0)
        
        # Update current state
        self._current_state.update({
            'location': self._current_location,
            'distance_traveled': self._distance_traveled
        })
        
        return {
            'equipment_id': self.equipment_id,
            'from_location': self._current_location,
            'to_location': location,
            'distance': distance,
            'time': time,
            'cost': transport_cost,
            'energy_used': transport_energy,
            'soc_after_move': self._soc
        }
    
    def get_spatial_state(self) -> Dict[str, Any]:
        """Get spatial state of the mobile storage.
        
        Returns
        -------
        Dict[str, Any]
            Spatial state including location, distance traveled, etc.
        """
        return {
            'current_location': self._current_location,
            'distance_traveled': self._distance_traveled,
            'speed': self._speed,
            'transport_cost': self._transport_cost
        }
    
    def get_carbon_state(self) -> Dict[str, Any]:
        """Get carbon state of the mobile storage.
        
        Returns
        -------
        Dict[str, Any]
            Carbon state including emissions, trading cost, etc.
        """
        carbon_trading_cost = 0.0
        if self._carbon_emissions > self._carbon_quota:
            excess_emissions = self._carbon_emissions - self._carbon_quota
            carbon_trading_cost = excess_emissions * self._carbon_price
        
        return {
            'carbon_emissions': self._carbon_emissions,
            'carbon_quota': self._carbon_quota,
            'carbon_price': self._carbon_price,
            'carbon_trading_cost': carbon_trading_cost
        }
    
    def get_battery_state(self) -> Dict[str, Any]:
        """Get battery state of the mobile storage.
        
        Returns
        -------
        Dict[str, Any]
            Battery state including SOC, cycles, etc.
        """
        return {
            'soc': self._soc,
            'remaining_cycles': self._remaining_cycles,
            'battery_age': self._battery_age,
            'capacity_decay_rate': self._capacity_decay_rate,
            'cycle_life': self._cycle_life
        }
    
    def reset_carbon_emissions(self) -> None:
        """Reset carbon emissions for a new trading period."""
        self._carbon_emissions = 0.0
    
    def reset_distance_traveled(self) -> None:
        """Reset distance traveled counter."""
        self._distance_traveled = 0.0
    
    def set_initial_soc(self, soc: float) -> None:
        """Set initial state of charge.
        
        Parameters
        ----------
        soc : float
            Initial SOC (0-1)
        """
        self._soc = max(0.0, min(1.0, soc))
    
    @property
    def soc(self) -> float:
        """Current state of charge."""
        return self._soc
    
    @property
    def current_location(self) -> str:
        """Current location."""
        return self._current_location
    
    @property
    def carbon_emissions(self) -> float:
        """Total carbon emissions in tons."""
        return self._carbon_emissions
    
    @property
    def distance_traveled(self) -> float:
        """Total distance traveled in km."""
        return self._distance_traveled
    
    @property
    def remaining_cycles(self) -> float:
        """Remaining battery cycles."""
        return self._remaining_cycles


@dataclass
class MobileStorageConfig:
    """Configuration for mobile storage systems."""
    # Basic parameters
    equipment_id: str
    power_rating: float  # kW
    capacity: float  # kWh
    efficiency: float = 0.95
    
    # Spatial parameters
    speed: float = 60.0  # km/h
    transport_cost: float = 1.0  # 元/km
    
    # Battery parameters
    cycle_life: int = 3000
    capacity_decay_rate: float = 0.02
    max_depth_of_discharge: float = 0.8
    initial_soc: float = 0.5
    
    # Carbon parameters
    carbon_price: float = 50.0  # 元/吨
    carbon_quota: float = 10.0  # 吨/年
    co2_emissions: float = 0.001  # kg CO2/kWh
    
    # Economic parameters
    investment_costs: float = 1500  # 元/kW
    operation_costs: float = 0.1  # 元/kWh
    lifetime: int = 10
    
    # Other parameters
    scenario: str = "urban"
    location: Optional[str] = None
    battery_type: str = "li-ion"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'equipment_id': self.equipment_id,
            'power_rating': self.power_rating,
            'capacity': self.capacity,
            'efficiency': self.efficiency,
            'speed': self.speed,
            'transport_cost': self.transport_cost,
            'cycle_life': self.cycle_life,
            'capacity_decay_rate': self.capacity_decay_rate,
            'max_depth_of_discharge': self.max_depth_of_discharge,
            'initial_soc': self.initial_soc,
            'carbon_price': self.carbon_price,
            'carbon_quota': self.carbon_quota,
            'co2_emissions': self.co2_emissions,
            'investment_costs': self.investment_costs,
            'operation_costs': self.operation_costs,
            'lifetime': self.lifetime,
            'scenario': self.scenario,
            'location': self.location,
            'battery_type': self.battery_type
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'MobileStorageConfig':
        """Create from dictionary."""
        return cls(**config_dict)


def create_mobile_storage(config: Dict[str, Any]) -> MobileStorageEquipment:
    """Create mobile storage equipment from configuration dictionary.
    
    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary
        
    Returns
    -------
    MobileStorageEquipment
        Mobile storage equipment instance
    """
    # Create equipment configuration
    equipment_config = EquipmentConfig(
        equipment_id=config['equipment_id'],
        name=f"MobileStorage_{config['equipment_id']}",
        description="Mobile Energy Storage System",
        category=EquipmentCategory.STORAGE,
        equipment_type=EquipmentType.BATTERY_STORAGE,
        power_rating=config['power_rating'],
        capacity=config['capacity'],
        efficiency=config['efficiency'],
        lifetime=config['lifetime'],
        investment_costs=config['investment_costs'],
        operation_costs=config['operation_costs'],
        co2_emissions=config['co2_emissions'],
        scenario=config['scenario'],
        location=config['location'],
        supported_carriers=[EnergyCarrier.ELECTRICITY],
        custom_parameters={
            'battery_type': config['battery_type'],
            'max_depth_of_discharge': config['max_depth_of_discharge'],
            'charging_rate': 1.0,
            'discharging_rate': 1.0
        }
    )
    
    # Create mobile storage equipment
    return MobileStorageEquipment(
        equipment_id=config['equipment_id'],
        config=equipment_config,
        location=config['location'],
        initial_soc=config['initial_soc'],
        speed=config['speed'],
        transport_cost=config['transport_cost'],
        carbon_price=config['carbon_price'],
        carbon_quota=config['carbon_quota'],
        cycle_life=config['cycle_life'],
        capacity_decay_rate=config['capacity_decay_rate']
    )


def create_mobile_storage_fleet(configs: List[Dict[str, Any]]) -> List[MobileStorageEquipment]:
    """Create a fleet of mobile storage systems.
    
    Parameters
    ----------
    configs : List[Dict[str, Any]]
        List of configuration dictionaries
        
    Returns
    -------
    List[MobileStorageEquipment]
        List of mobile storage equipment instances
    """
    return [create_mobile_storage(config) for config in configs]
