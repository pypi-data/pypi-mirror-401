"""
Scenario-Specific Equipment Library Module.

This module provides specialized equipment configurations for different
scenario types including urban, rural, port, island, industrial, and
railway scenarios.
"""

from .universal import UniversalEquipmentLibrary
from .urban import UrbanEquipmentLibrary
from .rural import RuralEquipmentLibrary
from .port import PortEquipmentLibrary
from .island import IslandEquipmentLibrary
from .industrial import IndustrialEquipmentLibrary
from .railway import RailwayEquipmentLibrary

__all__ = [
    'UniversalEquipmentLibrary',
    'UrbanEquipmentLibrary',
    'RuralEquipmentLibrary',
    'PortEquipmentLibrary',
    'IslandEquipmentLibrary',
    'IndustrialEquipmentLibrary',
    'RailwayEquipmentLibrary'
]