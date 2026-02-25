# ---------------------------------------------------------------------------
# Copyright (c) 2025 Olha Kanikovska. All Rights Reserved.
# Project: Statistical Analysis of Infrared Signal Scattering in Inhomogeneous Brain Structures - Medical Study Research
# Part of Master's Thesis at Lviv Polytechnic National University
# ---------------------------------------------------------------------------

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats
import plotly.graph_objects as go

# 1. This class takes our simulation results and calculates the statistic
class StatisticalAnalyzer:
    def __init__(self, data, model_name="Current Scheme"):
        self.graphic_values = np.array(data)
        self.model_name = model_name
        self.N = len(self.graphic_values)
        self.x_min = np.min(self.graphic_values)
        self.x_max = np.max(self.graphic_values)
        
        # Sturges' rule for interval step
        self.h = (self.x_max - self.x_min) / (1 + 3.322 * np.log(self.N))

    def calculate(self):
        if self.h <= 0: return
        
        # 1. Intervals and Frequencies
        x_start = self.x_min - self.h / 2
        bins = np.arange(x_start, self.x_max + self.h * 1.5, self.h)
        self.ni_values, self.edges = np.histogram(self.graphic_values, bins=bins)
        self.xi_values = (self.edges[:-1] + self.edges[1:]) / 2
        
        # 2. Mean (average) and Variance
        self.m = np.sum(self.xi_values * self.ni_values) / self.N
        self.d = np.sum(((self.xi_values - self.m)**2) * self.ni_values) / (self.N - 1)
        self.o = np.sqrt(self.d)
        
        # 3. Confidence Intervals (alpha=0.05)
        alpha = 0.05
        t_crit = stats.t.ppf(1 - alpha/2, self.N - 1)
        margin = t_crit * (self.o / np.sqrt(self.N))
        self.m_ci = (self.m - margin, self.m + margin)
        
        chi2_low = stats.chi2.ppf(alpha/2, self.N - 1)
        chi2_high = stats.chi2.ppf(1 - alpha/2, self.N - 1)
        self.d_ci = ((self.N - 1) * self.d / chi2_high, (self.N - 1) * self.d / chi2_low)
        
        # 4. Pearson Tests
        self._run_pearson_tests(alpha)

    def _merge_intervals(self, ni_obs, ni_exp):
        obs_m, exp_m = [], []
        c_obs, c_exp = 0, 0
        for o, e in zip(ni_obs, ni_exp):
            c_obs += o
            c_exp += e
            if c_exp >= 5:
                obs_m.append(c_obs); exp_m.append(c_exp)
                c_obs, c_exp = 0, 0
        if c_exp > 0 and exp_m:
            obs_m[-1] += c_obs; exp_m[-1] += c_exp
        return np.array(obs_m), np.array(exp_m)

    def _run_pearson_tests(self, alpha):
        # Normal
        p_i = stats.norm.cdf(self.edges[1:], self.m, self.o) - stats.norm.cdf(self.edges[:-1], self.m, self.o)
        obs, exp = self._merge_intervals(self.ni_values, self.N * p_i)
        df_n = max(1, len(exp) - 3)
        self.chi2_n = np.sum((obs - exp)**2 / exp) if len(exp) >= 3 else np.nan
        self.p_n = 1 - stats.chi2.cdf(self.chi2_n, df_n)
        self.res_n = "Accepted" if self.p_n >= alpha else "Rejected"

        # Exponential
        lambd = 1 / self.m
        p_i_e = stats.expon.cdf(self.edges[1:], scale=1/lambd) - stats.expon.cdf(self.edges[:-1], scale=1/lambd)
        obs_e, exp_e = self._merge_intervals(self.ni_values, self.N * p_i_e)
        df_e = max(1, len(exp_e) - 2)
        self.chi2_e = np.sum((obs_e - exp_e)**2 / exp_e) if len(exp_e) >= 2 else np.nan
        self.p_e = 1 - stats.chi2.cdf(self.chi2_e, df_e)
        self.res_e = "Accepted" if self.p_e >= alpha else "Rejected"
    
    def tableA(self):
        stats_data = pd.DataFrame({
            "Statistic": ["Mean", "Variance", "Min Value", "Max Value", "Step (h)"],
                "Value": [f"{self.m:.7f}", f"{self.d:.10f}", f"{self.x_min:.10f}", f"{self.x_max:.10f}", f"{self.h:.10f}"],
                "95% Conf. Interval": [f"[{self.m_ci[0]:.10f}, {self.m_ci[1]:.10f}]", 
                                       f"[{self.d_ci[0]:.10f}, {self.d_ci[1]:.10f}]", "-", "-", "-"]
        })
        stats_data.set_index("Statistic", inplace=True)
        st.table(stats_data)

    def tableB(self):
        pearson_data = pd.DataFrame({
            "Distribution": ["Normal (Gaussian)", "Exponential"],
            "Chi² Calculated": [f"{self.chi2_n:.4f}", f"{self.chi2_e:.4f}"],
            "p-value": [f"{self.p_n:.7f}", f"{self.p_e:.7f}"],
            "Result (α=0.05)": [self.res_n, self.res_e]
        })
        pearson_data.set_index("Distribution", inplace=True)
        st.table(pearson_data)

    def barGraph(self):
        bg_color = '#0B0F19'      
        text_color = '#E1E7EF'    
        bar_color = '#3B82F6' 
        grid_color = '#1F2937'    

        fig = go.Figure()

        # Add the Bar Diagram
        fig.add_trace(go.Bar(
            x=self.xi_values,
            y=self.ni_values,
            name='Observed Ni',
            marker_color=bar_color,
            opacity=0.6,
            hovertemplate="<b>Value:</b> %{x:.4e}<br><b>Frequency:</b> %{y}<extra></extra>"
        ))

        # Add Theoretical Fits (Scaling PDF to match Frequency)
        x_smooth = np.linspace(self.x_min, self.x_max, 100)
        scale = self.N * self.h

        # Normal Fit (Red)
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=stats.norm.pdf(x_smooth, self.m, self.o) * scale,
            mode='lines',
            name='Normal Fit',
            line=dict(color='#EF4444', width=3)
        ))

        # Exponential Fit (Yellow/Gold)
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=stats.expon.pdf(x_smooth, scale=self.m) * scale,
            mode='lines',
            name='Exponential Fit',
            line=dict(color='#F59E0B', width=3)
        ))

        fig.update_layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color),
            xaxis=dict(
                title="Interval Midpoints (Xi)",
                gridcolor=grid_color,
                linecolor=grid_color,
                zeroline=False
            ),
            yaxis=dict(
                title="Observed Frequency (Ni)",
                gridcolor=grid_color,
                linecolor=grid_color,
                zeroline=False
            ),
            hoverlabel=dict(bgcolor="#1F2937", font_size=14),
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            bargap=0.05 
        )

        st.plotly_chart(fig, width="stretch")