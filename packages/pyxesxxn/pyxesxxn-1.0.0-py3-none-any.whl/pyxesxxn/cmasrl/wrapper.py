"""
Multi-agent Safe Reinforcement Learning module for PyXESXXN

This module provides a clean interface to the CMASRL functionality for multi-agent safe reinforcement learning.
"""

# MO-LS-Mstar-main: Multi-Objective Loosely Synchronized Search for Multi-Objective Multi-Agent Path Finding with Asynchronous Actions
# from .MO_LS_Mstar_main.MO_LS_Mstar_main.libmomapf import MO_LS_Mstar_Agent

# SMARL-MAFOA-main: Safe Multi-Agent Reinforcement Learning for Multi-Agent Formation Obstacle Avoidance
# from .SMARL_MAFOA_main.SMARL_MAFOA_main import SMARL_MAFOA_Agent

# SS-MARL-main: Scalable Safe Multi-Agent Reinforcement Learning
# from .SS_MARL_main.SS_MARL_main.ssmarl.algorithms import SS_MARL_Agent

# Mock implementation for demonstration purposes
class MO_LS_Mstar_Agent:
    """Multi-Objective Loosely Synchronized Search Agent"""
    def __init__(self):
        self.name = "MO-LS-Mstar Agent"
        self.type = "multi_objective_path_finding"

class SMARL_MAFOA_Agent:
    """Safe Multi-Agent Reinforcement Learning for Multi-Agent Formation Obstacle Avoidance"""
    def __init__(self):
        self.name = "SMARL-MAFOA Agent"
        self.type = "formation_obstacle_avoidance"

class SS_MARL_Agent:
    """Scalable Safe Multi-Agent Reinforcement Learning"""
    def __init__(self):
        self.name = "SS-MARL Agent"
        self.type = "scalable_safe_marl"

__all__ = ['MO_LS_Mstar_Agent', 'SMARL_MAFOA_Agent', 'SS_MARL_Agent']

cmasrl_wrapper = {
    'mo_ls_mstar': MO_LS_Mstar_Agent,
    'smarl_mafoa': SMARL_MAFOA_Agent,
    'ss_marl': SS_MARL_Agent
}