# ---------------------------------------------------------------------------
# Copyright (c) 2025 Olha Kanikovska. All Rights Reserved.
# Project: Statistical Analysis of Infrared Signal Scattering in Inhomogeneous Brain Structures - Medical Study Research
# Part of Master's Thesis at Lviv Polytechnic National University
# ---------------------------------------------------------------------------

DEFAULT_INPUT_DATA = {
    "np": 50000,          # Number of photons
    "dz": 0.2,            # Grid z [cm]
    "dr": 0.2,            # Grid r [cm]
    "nz": 10,             # Grids in z
    "nr": 20,             # Grids in r
    "na": 30,             # Grids in alpha
    "nl": 4,              # Number of original layers
    "n": [1.0, 1.37, 1.43, 1.33, 1.37, 1.0], #Refractive index
    "mua": [0.018, 0.016, 0.004, 0.036],  # Absorption coefficients
    "mus": [19.0, 16.0, 2.4, 22.0],       # Scattering coefficients
    "g": [0.9, 0.9, 0.9, 0.9],            # Anisotropy factor
    "d": [0.3, 0.5, 0.2, 0.4]             # Depths [cm]
}