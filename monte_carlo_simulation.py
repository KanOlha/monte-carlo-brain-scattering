# ---------------------------------------------------------------------------
# Copyright (c) 2025 Olha Kanikovska. All Rights Reserved.
# Project: Statistical Analysis of Infrared Signal Scattering in Inhomogeneous Brain Structures - Medical Study Research
# Part of Master's Thesis at Lviv Polytechnic National University
# ---------------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from types import SimpleNamespace

# 1. This class is the "brain" of our project that handles all the physics math for light moving through layers.
class SimulationMonteCarlo:
    def __init__(self, input_data, model_name):
        """
        Constructor to initialize with a Python dictionary
        input_data: Dictionary containing simulation parameters
        model_name: String name for the model
        """
        self.input = self.initialize_input(input_data)
        self.output = None
        self.model_name = model_name

    # 2. This part organizes the raw data into a list of layers and calculates light properties like critical angles.
    def initialize_input(self, data):
        """Processes the raw dictionary into a structured object with layer properties"""
        np_sim = data["np"]
        dz = data["dz"]
        dr = data["dr"]
        nz, nr, na, nl = data["nz"], data["nr"], data["na"], data["nl"]
        
        n = data["n"]
        mua, mus, g, d = data["mua"], data["mus"], data["g"], data["d"]

        layers = []
        # Logic: n[0] is ambient top, n[1...nl] are layers, n[nl+1] is ambient bottom
        for ilayer in range(nl):
            z1 = sum(d[:ilayer+1])
            z0 = z1 - d[ilayer]
            n0 = n[ilayer]      # Index of medium above
            n1 = n[ilayer + 1]  # Index of current layer
           
            cos_crit0 = np.sqrt(1 - (n0**2) / (n1**2)) if n1 > n0 else 0.0
            
            layer = {
                'n': n1,
                'mua': mua[ilayer],
                'mus': mus[ilayer],
                'g': g[ilayer],
                'z0': z0,
                'z1': z1,
                'cos_crit0': cos_crit0
            }
            layers.append(layer)

        return SimpleNamespace(
            np=np_sim, dz=dz, dr=dr, da=0.5 * np.pi / na,
            nz=nz, nr=nr, na=na, nl=nl, 
            n_above=n[0], n_below=n[-1], 
            layers=layers
        )

    def run_simulation(self):
        """Calls the MC method to perform the simulation"""
        self.output = self.mc(self.input)

    # 3. Raw results are just counts; this function rescales them into real physical units like reflectance and absorption.
    def process_output(self, input_data, output):
        """Calculates totals and applies physical scaling to the raw counts"""
        # Basic Normalization by photon count
        output.rd_ra /= input_data.np
        output.ab_rz /= input_data.np
        output.tt_ra /= input_data.np

        # Summing across dimensions for 1D profiles
        output.rd_r = np.sum(output.rd_ra, axis=1)
        output.rd_a = np.sum(output.rd_ra, axis=0)
        output.ab_r = np.sum(output.ab_rz, axis=1)
        output.ab_z = np.sum(output.ab_rz, axis=0)
        output.tt_r = np.sum(output.tt_ra, axis=1)
        output.tt_a = np.sum(output.tt_ra, axis=0)
        
        output.rd = np.sum(output.rd_ra)
        output.ab = np.sum(output.ab_rz)
        output.tt = np.sum(output.tt_ra)

        # Geometric Rescaling (Vectorized)
        dr, da, dz = input_data.dr, input_data.da, input_data.dz
        nr, na, nz = input_data.nr, input_data.na, input_data.nz
        
        scale1 = 4.0 * np.pi**2 * dr * np.sin(da / 2) * dr
        ir = np.arange(1, nr + 1).reshape(-1, 1)
        ia = np.arange(1, na + 1).reshape(1, -1)
        
        # Scale 2D arrays
        scale2_ra = 1.0 / ((ir - 0.5) * np.sin(2.0 * (ia - 0.5) * da) * scale1)
        output.rd_ra *= scale2_ra
        output.tt_ra *= scale2_ra

        # Scale Radial Vectors
        scale1_r = 2.0 * np.pi * dr**2
        r_indices = np.arange(1, nr + 1)
        output.rd_r *= (1.0 / ((r_indices - 0.5) * scale1_r))
        output.tt_r *= (1.0 / ((r_indices - 0.5) * scale1_r))

        # Scale Angular Vectors
        scale1_a = 4.0 * np.pi * np.sin(da / 2)
        a_indices = np.arange(1, na + 1)
        output.rd_a *= (1.0 / (np.sin(a_indices * da) * scale1_a))
        output.tt_a *= (1.0 / (np.sin(a_indices * da) * scale1_a))
        
        # Scale Absorption
        output.ab_rz *= (1.0 / (r_indices.reshape(-1, 1) * scale1_a * dz))
        output.ab_z *= (1.0 / dz)
        
        return output

    def mc(self, input_data):
        """Simulate Monte Carlo results (Placeholder)"""
        output = SimpleNamespace()
        output.rd_ra = np.random.rand(input_data.nr, input_data.na)
        output.ab_rz = np.random.rand(input_data.nr, input_data.nz)
        output.tt_ra = np.random.rand(input_data.nr, input_data.na)
        
        return self.process_output(input_data, output)

    # 4. This final part lets us pick a specific distance range, calculates the values there, and saves it all to a .txt file.
    def get_analysis_data(self, start_dist, end_dist, step):
        dr, nr = self.input.dr, self.input.nr
        rindex = (np.arange(1, nr + 1) * dr) - dr / 2
        
        i_distances = np.arange(start_dist, end_dist + step, step)
        
        interp_func = PchipInterpolator(rindex, self.output.rd_r, extrapolate=False)
        p_reflectance = np.nan_to_num(interp_func(i_distances), nan=0.0)
        
        df_p_only = pd.DataFrame({
            'i_value': i_distances,
            'P_reflectance': p_reflectance
        }).set_index('i_value')

        p_sorted = np.sort(p_reflectance)
        file_name = f"P_reflectance.txt"
        df_save = pd.DataFrame({'P_reflectance': p_sorted})
        df_save.to_csv(file_name, sep='\t', index=False, float_format='%.12f')
        
        return df_p_only, rindex, self.output.rd_r
