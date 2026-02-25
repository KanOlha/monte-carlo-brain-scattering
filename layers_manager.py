# ---------------------------------------------------------------------------
# Copyright (c) 2025 Olha Kanikovska. All Rights Reserved.
# Project: Statistical Analysis of Infrared Signal Scattering in Inhomogeneous Brain Structures - Medical Study Research
# Part of Master's Thesis at Lviv Polytechnic National University
# ---------------------------------------------------------------------------

import numpy as np

# 1. This class manages how we simplify or "group" the original 4 tissue layers into fewer layers for testing.
class LayersManager:
    def __init__(self, input_data):
        """
        Initializes with a dictionary of parameters (from config or user input).
        """
        self.data = input_data

    def _extract_initial_properties(self):
        """Helper to get clean references to the base data."""
        d = self.data
        return (
            np.array(d['n']), np.array(d['mua']), np.array(d['mus']), 
            np.array(d['g']), np.array(d['d']), d['np'], 
            d['dz'], d['dr'], d['nz'], d['nr'], d['na']
        )

    def make_one_layer(self):
        """Aggregates 4 tissue layers into one effective layer."""
        n_full, mua_f, mus_f, g_f, d_f, np_val, dz, dr, nz, nr, na = self._extract_initial_properties()

        # Logic: Average n, mua, mus, g; Sum depths
        n_layer = np.mean(n_full[1:4])
        mua_layer = np.mean(mua_f)
        mus_layer = np.mean(mus_f)
        g_layer = np.mean(g_f)
        d_layer = np.sum(d_f)

        return {
            "np": np_val, "dz": dz, "dr": dr, "nz": nz, "nr": nr, "na": na, "nl": 1,
            "n": [n_full[0], n_layer, n_full[5]],
            "mua": [mua_layer], "mus": [mus_layer], "g": [g_layer], "d": [d_layer]
        }

    def make_two_layers(self, scheme='2-2'):
        """Aggregates 4 tissue layers into two effective layers based on scheme."""
        n_f, mua_f, mus_f, g_f, d_f, np_val, dz, dr, nz, nr, na = self._extract_initial_properties()

        if scheme == '2-2':
            # Layer 1 (Orig 1+2), Layer 2 (Orig 3+4)
            n1, n2 = np.mean(n_f[1:3]), np.mean(n_f[3:5])
            mua1, mua2 = np.mean(mua_f[0:2]), np.mean(mua_f[2:4])
            mus1, mus2 = np.mean(mus_f[0:2]), np.mean(mus_f[2:4])
            g1, g2 = np.mean(g_f[0:2]), np.mean(g_f[2:4])
            d1, d2 = np.sum(d_f[0:2]), np.sum(d_f[2:4])
        
        elif scheme == '1-3':
            # Layer 1 (Orig 1), Layer 2 (Orig 2+3+4)
            n1, n2 = n_f[1], np.mean(n_f[2:5])
            mua1, mua2 = mua_f[0], np.mean(mua_f[1:4])
            mus1, mus2 = mus_f[0], np.mean(mus_f[1:4])
            g1, g2 = g_f[0], np.mean(g_f[1:4])
            d1, d2 = d_f[0], np.sum(d_f[1:4])

        elif scheme == '3-1':
            # Layer 1 (Orig 1+2+3), Layer 2 (Orig 4)
            n1, n2 = np.mean(n_f[1:4]), n_f[4]
            mua1, mua2 = np.mean(mua_f[0:3]), mua_f[3]
            mus1, mus2 = np.mean(mus_f[0:3]), mus_f[3]
            g1, g2 = np.mean(g_f[0:3]), g_f[3]
            d1, d2 = np.sum(d_f[0:3]), d_f[3]
        else:
            raise ValueError("Invalid scheme. Use '2-2', '1-3', or '3-1'.")

        return {
            "np": np_val, "dz": dz, "dr": dr, "nz": nz, "nr": nr, "na": na, "nl": 2,
            "n": [n_f[0], n1, n2, n_f[5]],
            "mua": [mua1, mua2], "mus": [mus1, mus2], "g": [g1, g2], "d": [d1, d2]
        }
    
    def make_three_layers(self, scheme='1-1-2'):
        """Aggregates 4 tissue layers into three effective layers based on scheme."""
        n_f, mua_f, mus_f, g_f, d_f, np_val, dz, dr, nz, nr, na = self._extract_initial_properties()

        if scheme == '1-1-2':
            # Layer 1 (Orig 1), Layer 2 (Orig 2), Layer 3 (Orig 3+4)
            n1, n2, n3 = n_f[1], n_f[2], np.mean(n_f[3:5])
            mua1, mua2, mua3 = mua_f[0], mua_f[1], np.mean(mua_f[2:4])
            mus1, mus2, mus3 = mus_f[0], mus_f[1], np.mean(mus_f[2:4])
            g1, g2, g3 = g_f[0], g_f[1], np.mean(g_f[2:4])
            d1, d2, d3 = d_f[0], d_f[1], np.sum(d_f[2:4])
        
        elif scheme == '1-2-1':
            # Layer 1 (Orig 1), Layer 2 (Orig 2-3), Layer 3 (Orig 4)
            n1, n2, n3 = np.mean(n_f[1]), np.mean(n_f[2:4]), np.mean(n_f[4])
            mua1, mua2, mua3 = mua_f[0], np.mean(mua_f[1:3]), mua_f[3]
            mus1, mus2, mus3 = mus_f[0], np.mean(mus_f[1:3]), mus_f[3]
            g1, g2, g3 = g_f[0], np.mean(g_f[1:3]), g_f[3]
            d1, d2, d3 = d_f[0], np.sum(d_f[1:3]), d_f[3]

        elif scheme == '2-1-1':
            # Layer 1 (Orig 1+2), Layer 2 (Orig 3), Layer 3 (Orig 4)
            n1, n2, n3 = np.mean(n_f[1:3]), n_f[3], n_f[4]
            mua1, mua2, mua3 = np.mean(mua_f[0:2]), mua_f[2], mua_f[3]
            mus1, mus2, mus3 = np.mean(mus_f[0:2]), mus_f[2], mus_f[3]
            g1, g2, g3 = np.mean(g_f[0:2]), g_f[2], g_f[3]
            d1, d2, d3 = np.sum(d_f[0:2]), d_f[2], d_f[3]
        else:
            raise ValueError("Invalid scheme. Use '1-1-2', '1-2-1', or '2-1-1'.")

        return {
            "np": np_val, "dz": dz, "dr": dr, "nz": nz, "nr": nr, "na": na, "nl": 3,
            "n": [n_f[0], n1, n2, n3, n_f[5]],
            "mua": [mua1, mua2, mua3], "mus": [mus1, mus2, mus3], "g": [g1, g2, g3], "d": [d1, d2, d3]
        }
