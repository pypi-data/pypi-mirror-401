"""
Scenario Templates Module for Multi-Scenario Energy System Modeling.

This module provides predefined network templates for different scenarios
including urban, rural, port, and other energy system configurations.
"""

from .urban import UrbanScenarioTemplate
from .rural import RuralScenarioTemplate  
from .port import PortScenarioTemplate
from .island import IslandScenarioTemplate
from .industrial import IndustrialScenarioTemplate
from .railway import RailwayScenarioTemplate
from .template_manager import ScenarioTemplateManager

__all__ = [
    "UrbanScenarioTemplate",
    "RuralScenarioTemplate", 
    "PortScenarioTemplate",
    "IslandScenarioTemplate",
    "IndustrialScenarioTemplate",
    "RailwayScenarioTemplate",
    "ScenarioTemplateManager"
]