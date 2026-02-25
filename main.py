# ---------------------------------------------------------------------------
# Copyright (c) 2025 Olha Kanikovska. All Rights Reserved.
# Project: Statistical Analysis of Infrared Signal Scattering in Inhomogeneous Brain Structures - Medical Study Research
# Part of Master's Thesis at Lviv Polytechnic National University
# ---------------------------------------------------------------------------

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

from config import DEFAULT_INPUT_DATA
from layers_manager import LayersManager
from layer_model_chart import create_layer_diagram
from monte_carlo_simulation import SimulationMonteCarlo
from statistic import StatisticalAnalyzer

# 1. This part sets up the main dashboard layout, including the title, description, and input filters for the user.
def display_structure_table(data):
    """Renders the simulation parameters and the layer table in Streamlit."""
    
    df = pd.DataFrame({
        "n": input_data["n"][1:-1],
        "$\mu_a$": input_data["mua"],
        "$\mu_s$": input_data["mus"],
        "g": input_data["g"],
        "Thickness (d)": input_data["d"]
    })
    df.index = df.index + 1
    st.table(df)

st.set_page_config(layout="wide", page_title="Affiliate Performance Dashboard")

col_title, col_filter1, col_filter2, button = st.columns([3.5, 1.2, 1.2, 1])
with col_title:
    st.title("🔬 Multilayer Tissue Monte Carlo Analysis")

    st.markdown("""An interactive simulation tool that utilizes Monte Carlo modeling 
               to analyze the statistical distribution and scattering behavior of infrared signals within inhomogeneous, 
               multi-layered brain structures.\nCreated by Olha Kanikovska""")

with col_filter1:
    scheme_options = [
        "Baseline (Original 4-Layer)",
        "1-Layer (Average)",
        "2-Layer (2-2)",
        "2-Layer (1-3)",
        "2-Layer (3-1)",
        "3-Layer (1-2-1)",
        "3-Layer (2-1-1)",
        "3-Layer (1-1-2)"
    ]
    selected_scheme = st.selectbox("Aggregation Scheme", scheme_options)
    

with col_filter2:
    step = st.number_input("Distance Step (cm)", value=0.05, format="%.2f")

with button:
    st.write("")
    run_sim = st.button("🚀 RUN ANALYSIS", width="stretch")

# 2. This logic block connects the UI to the backend: it takes the user's choice and tells the LayersManager how to group the tissues.
if run_sim:
    layer_mgr = LayersManager(DEFAULT_INPUT_DATA)
    
    if "Baseline" in selected_scheme:
        input_data = layer_mgr.data # Original
    elif "1-Layer" in selected_scheme:
        input_data = layer_mgr.make_one_layer()
    elif "2-Layer" in selected_scheme:
        scheme_code = selected_scheme.split("(")[1].replace(")", "")
        input_data = layer_mgr.make_two_layers(scheme_code)
    elif "3-Layer" in selected_scheme:
        scheme_code = selected_scheme.split("(")[1].replace(")", "")
        input_data = layer_mgr.make_three_layers(scheme_code)

    # 3. Here, we trigger the actual Monte Carlo simulation and pass the results to the StatisticalAnalyzer for math checks.
    mcs = SimulationMonteCarlo(input_data, selected_scheme)
    mcs.run_simulation()
    df_p_only, r_axis, rd_values = mcs.get_analysis_data(0.5, 3.5, step)
    analysis_data = df_p_only["P_reflectance"].values
    analyzer = StatisticalAnalyzer(analysis_data, selected_scheme)
    analyzer.calculate()
    
    # 4. I used a 3-column layout here to show the 3D model, the line graph, and the raw data table all at once for easy comparison.
    col_left, col_mid, col_right = st.columns([1.3, 2.5, 0.5])

    with col_left:
        st.subheader("🧠 Brain model scheme")
        fig = create_layer_diagram(input_data, f"{selected_scheme}")
        
        st.plotly_chart(fig, width="stretch")
        
        st.markdown(f"**Current Scheme:** `{selected_scheme}`")
        display_structure_table(input_data)

    with col_mid:
        st.subheader("Simulation Diagram")

        bg_color = '#0B0F19'      
        text_color = '#E1E7EF'    
        line_color = '#3B82F6'    
        grid_color = '#1F2937'    

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=r_axis,
            y=rd_values,
            mode='lines',
            name=selected_scheme,
            line=dict(color=line_color, width=3),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.15)',
            hovertemplate=(
                "<b>Distance:</b> %{x:.2f} cm<br>" +
                "<b>Reflectance:</b> %{y:.8f}<br>" +
                "<extra></extra>"
            )
        ))

        fig.update_layout(
            height=500,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color),
            xaxis=dict(
                title="Distance r [cm]",
                gridcolor=grid_color,
                zeroline=False,
                showgrid=True,
                linecolor=grid_color
            ),
            yaxis=dict(
                title="Log Reflectance Rd(r)",
                type="log",
                gridcolor=grid_color,
                zeroline=False,
                showgrid=True,
                linecolor=grid_color,
                exponentformat="power"
            ),
            margin=dict(l=40, r=40, t=20, b=40),
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="#1F2937",
                font_size=14,
                font_family="Inter, sans-serif"
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor="rgba(0,0,0,0)"
            )
        )

        st.plotly_chart(fig, width="stretch")

    with col_right:
        st.subheader("Simulation values")
        precision = 10 
    
        st.dataframe(
        df_p_only, 
        column_config={
            "_index": st.column_config.NumberColumn(
                "Distance"
            ),
            "P_reflectance": st.column_config.NumberColumn(
                "Reflectance",
                format="%.8f"
            )
        },
        height=450, 
        width="stretch"
    )

    # 5. At the bottom, the app displays the final "Report Card"—the statistics tables and the histogram with distribution fits.
    st.divider()
    b_left, b_right = st.columns([1.1, 2])

    with b_left:
        st.subheader("Descriptive Statistics")
        analyzer.tableA()

        st.subheader("Pearson Chi-Squared Test")
        analyzer.tableB()

    with b_right:
        st.subheader("D. Histogram & Distribution Fits")
        analyzer.barGraph()
