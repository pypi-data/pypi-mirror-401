"""Thermodynamic constants for energy system calculations."""

from typing import Dict

# Universal gas constant (J/(mol·K))
UNIVERSAL_GAS_CONSTANT = 8.314462618  # J/(mol·K)

# Gas-specific constants
GAS_CONSTANTS: Dict[str, float] = {
    "hydrogen": 4124.2,      # J/(kg·K)
    "natural_gas": 518.3,    # J/(kg·K)
    "air": 287.1,           # J/(kg·K)
    "co2": 188.9,           # J/(kg·K)
    "methane": 518.3,       # J/(kg·K)
    "ethane": 276.5,        # J/(kg·K)
    "propane": 188.6,       # J/(kg·K)
    "nitrogen": 296.8,      # J/(kg·K)
    "oxygen": 259.8,        # J/(kg·K)
}

# Specific heat ratios (gamma = cp/cv)
SPECIFIC_HEAT_RATIOS: Dict[str, float] = {
    "hydrogen": 1.4,
    "natural_gas": 1.3,
    "air": 1.4,
    "co2": 1.28,
    "methane": 1.3,
    "ethane": 1.18,
    "propane": 1.13,
    "nitrogen": 1.4,
    "oxygen": 1.4,
}

# Molar masses (kg/mol)
MOLAR_MASSES: Dict[str, float] = {
    "hydrogen": 0.002016,
    "natural_gas": 0.01604,  # Approx for methane
    "air": 0.02897,
    "co2": 0.04401,
    "methane": 0.01604,
    "ethane": 0.03007,
    "propane": 0.04410,
    "nitrogen": 0.02801,
    "oxygen": 0.03200,
}

# Critical properties
CRITICAL_TEMPERATURES: Dict[str, float] = {
    "hydrogen": 33.19,      # K
    "natural_gas": 190.56,  # K (methane)
    "air": 132.5,          # K
    "co2": 304.13,         # K
    "methane": 190.56,     # K
    "ethane": 305.3,       # K
    "propane": 369.8,      # K
    "nitrogen": 126.2,     # K
    "oxygen": 154.6,       # K
}

CRITICAL_PRESSURES: Dict[str, float] = {
    "hydrogen": 13.13e5,    # Pa
    "natural_gas": 45.99e5, # Pa (methane)
    "air": 37.7e5,         # Pa
    "co2": 73.8e5,         # Pa
    "methane": 45.99e5,    # Pa
    "ethane": 48.72e5,     # Pa
    "propane": 42.48e5,    # Pa
    "nitrogen": 33.9e5,    # Pa
    "oxygen": 50.43e5,     # Pa
}

# Standard conditions
STANDARD_TEMPERATURE = 293.15  # K (20°C)
STANDARD_PRESSURE = 101325.0   # Pa (1 atm)

# Conversion factors
BAR_TO_PA = 1e5
PSI_TO_PA = 6894.76
ATM_TO_PA = 101325.0

# Thermodynamic constants for water
WATER_SPECIFIC_HEAT = 4186.0      # J/(kg·K)
WATER_LATENT_HEAT_VAPORIZATION = 2.257e6  # J/kg
WATER_LATENT_HEAT_FUSION = 3.34e5         # J/kg