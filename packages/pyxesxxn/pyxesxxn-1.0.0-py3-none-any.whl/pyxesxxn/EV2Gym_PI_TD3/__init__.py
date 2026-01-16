"""EV2Gym_PI_TD3 Module.

This module implements Physics-Informed Twin Delayed Deep Deterministic Policy Gradient (PI-TD3)
for electric vehicle (EV) charging management in vehicle-to-grid (V2G) systems.

The module provides:
- PI-TD3 algorithm implementation
- EV2Gym environment for EV charging simulation
- Physics-informed reinforcement learning with differentiable models
- Integration with PyXESXXN energy system framework

Reference:
    Stavros Orfanoudakis, Frans Oliehoek, Peter Palesnky, Pedro P. Vergara.
    "Physics-Informed Reinforcement Learning for Large-Scale EV Smart Charging
     Considering Distribution Network Voltage Constraints"
    arXiv:2510.12335
"""

from .ev2gym_pi_wrapper import (
    EV2GymPIWrapper,
    PI_TD3Config,
    EVChargingEnvironment,
    EVChargingConfig
)

__all__ = [
    'EV2GymPIWrapper',
    'PI_TD3Config',
    'EVChargingEnvironment',
    'EVChargingConfig'
]
