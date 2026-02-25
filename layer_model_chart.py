# ---------------------------------------------------------------------------
# Copyright (c) 2025 Olha Kanikovska. All Rights Reserved.
# Project: Statistical Analysis of Infrared Signal Scattering in Inhomogeneous Brain Structures - Medical Study Research
# Part of Master's Thesis at Lviv Polytechnic National University
# ---------------------------------------------------------------------------

import plotly.graph_objects as go

# 1. This function creates a 3D picture of head layers based on the user's selection.
def create_layer_diagram(input_data, selected_scheme):
    """
    Dynamically generates a 3D block diagram for any aggregation scheme.
    """
    fig = go.Figure()
    
    # 2. These are the colors for each part: 0: Scalp, 1: Skull, 2: CSF, 3: Gray Matter
    base_colors = ['#F5B08F', '#A0A0A0', '#AED6F1', '#F7DC6F']
    
    depths = input_data['d']
    num_layers = len(depths)
    current_z = 0

    # 3. This loop goes through each layer and gives it the right name and color depending on the chosen scheme.
    for i in range(num_layers):
        thickness = depths[i]
        opacity = 1.0 
        
        if "Baseline" in selected_scheme:
            label = f"Layer {i+1}: {['Scalp', 'Skull', 'CSF', 'Gray Matter'][i]}"
            color = base_colors[i]
        
        elif "1-Layer" in selected_scheme:
            label = "Layer 1:<br>Scalp + Skull +<br>+ CSF + Gray Matter"
            color = '#F5B08F'
            
        elif "2-Layer" in selected_scheme:
            if "2-2" in selected_scheme:
                label = "Layers 1+2:<br>Scalp + Skull" if i == 0 else "Layers 3+4:<br>CSF + Gray Matter"
                color = base_colors[0] if i == 0 else base_colors[2]
            elif "1-3" in selected_scheme:
                label = "Layer 1: Scalp" if i == 0 else "Layers 2+3+4:<br>Skull + CSF + <br> + Gray Matter"
                color = base_colors[0] if i == 0 else base_colors[1]
            else: # 3-1
                label = "Layers 1+2+3:<br>Scalp + Skull + CSF" if i == 0 else "Layer 4: Gray Matter"
                color = base_colors[0] if i == 0 else base_colors[3]

        elif "3-Layer" in selected_scheme:
            if "1-1-2" in selected_scheme:
                labels = ["Layer 1: Scalp", "Layer 2: Skull", "Layers 3+4:<br>CSF + Gray Matter"]
                colors = [base_colors[0], base_colors[1], base_colors[2]]
                label = labels[i]
                color = colors[i]
            elif "1-2-1" in selected_scheme:
                labels = ["Layer 1: Scalp", "Layers 2+3:<br>Skull + CSF", "Layer 4: Gray Matter"]
                colors = [base_colors[0], base_colors[1], base_colors[3]]
                label = labels[i]
                color = colors[i]
            else: # 2-1-1
                labels = ["Layers 1+2:<br>Scalp + Skull", "Layer 3: CSF", "Layer 4: Gray Matter"]
                colors = [base_colors[0], base_colors[2], base_colors[3]]
            label = labels[i]
            color = colors[i]
        
        # 4. This part builds the actual 3D boxes.
        """Adds a 3D block and its black wireframe edges."""
        x = [0, 14, 14, 0, 0, 14, 14, 0]
        y = [0, 0, 14, 14, 0, 0, 14, 14]
        z = [current_z, current_z, current_z, current_z, 
            current_z + thickness, current_z + thickness, current_z + thickness, current_z + thickness]
        
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            alphahull=0,
            color=color,
            opacity=opacity,
            name=label,
            legendgroup=label,
            showlegend=True
        ))

        edges_x, edges_y, edges_z = [], [], []
        for bz in [current_z, current_z + thickness]:
            edges_x += [0, 14, 14, 0, 0, None]; edges_y += [0, 0, 14, 14, 0, None]; edges_z += [bz, bz, bz, bz, bz, None]
        for bx, by in [(0,0), (14,0), (14,14), (0,14)]:
            edges_x += [bx, bx, None]; edges_y += [by, by, None]; edges_z += [current_z, current_z + thickness, None]

        fig.add_trace(go.Scatter3d(
            x=edges_x, y=edges_y, z=edges_z, mode='lines',
            line=dict(color='black', width=4), showlegend=False, legendgroup=label
        ))
        
        current_z += thickness

    # 5. Finally, I set the chart to dark mode and adjust the camera angle.
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            zaxis=dict(autorange="reversed", title="Depth (z) mm"),
            xaxis_title="X (mm)",
            yaxis_title="Y (mm)",
            aspectmode='manual', 
            aspectratio=dict(x=1, y=1, z=1), 
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.5),
                center=dict(x=0, y=0, z=0),
                up=dict(x=0, y=0, z=1)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=50),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05,
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            alphahull=0,
            color=color,
            opacity=opacity,
            name=label,
            legendgroup=label,
        ))
    
    return fig