import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from dataclasses import dataclass

class Parametrs(Enum):
    mass = 1
    radius = 2
    albedo = 3
    emissivity = 4
    heat_capacity = 5
    base_diffusion = 6
    base_pressure = 7
    stellar_flux = 8

@dataclass
class PlanetParameters:
    data: dict[Parametrs, float]  

def sync_input_to_slider(key):
    st.session_state[f"{key}_input"] = str(st.session_state[f"{key}_slider"])

def sync_slider_to_input(key, min_v, max_v):
    try:
        val = float(st.session_state[f"{key}_input"])
        if min_v <= val <= max_v:
            st.session_state[f"{key}_slider"] = val
        else:
            st.session_state[f"{key}_input"] = str(st.session_state[f"{key}_slider"])
    except ValueError:
        st.session_state[f"{key}_input"] = str(st.session_state[f"{key}_slider"])
        pass

def slider_with_input(label, min_val, max_val, default_val, key):
    if f"{key}_slider" not in st.session_state:
        st.session_state[f"{key}_slider"] = float(default_val)
    if f"{key}_input" not in st.session_state:
        st.session_state[f"{key}_input"] = str(default_val)

    col_l, col_r = st.columns([4, 1])

    with col_l:
        st.slider(label, min_val, max_val, 
                  key=f"{key}_slider", 
                  on_change=sync_input_to_slider, 
                  args=(key,))

    with col_r:
        st.text_input(label, 
                      key=f"{key}_input", 
                      on_change=sync_slider_to_input, 
                      args=(key, min_val, max_val), 
                      label_visibility="collapsed")

    return st.session_state[f"{key}_slider"]

def get_planet_preview(radius, albedo, flux, pressure, emissivity):
    sigma_pseudo = 0.0000000567 
    
    safe_emissivity = max(0.01, emissivity)
    
    t_fourth = (flux * (1 - albedo)) / (4 * sigma_pseudo * safe_emissivity)
    approx_temp_k = t_fourth**0.25
    
    approx_temp_k = approx_temp_k * (1 + (pressure / 100) * 0.5)
    
    temp_c = approx_temp_k - 273.15

    if temp_c < 0:
        mix = min(1.0, abs(temp_c) / 100)
        base = np.array([173, 216, 230]) / 255.0 
        white = np.array([255, 255, 255]) / 255.0
        final_color = base * mix + white * (1 - mix)
        
    elif temp_c < 100:
        mix = temp_c / 100
        ocean = np.array([30, 144, 255]) / 255.0  
        forest = np.array([34, 139, 34]) / 255.0  
        final_color = ocean * (1 - mix) + forest * mix
        
    elif temp_c < 500:
        mix = (temp_c - 100) / 400
        yellow = np.array([255, 215, 0]) / 255.0   
        orange = np.array([255, 140, 0]) / 255.0   
        final_color = yellow * (1 - mix) + orange * mix
        
    else:
        mix = min(1.0, (temp_c - 500) / 1000)
        red = np.array([255, 69, 0]) / 255.0      
        dark_red = np.array([139, 0, 0]) / 255.0  
        final_color = red * (1 - mix) + dark_red * mix

    return final_color, approx_temp_k

def generate_planet_visual(params):
    rad = params[Parametrs.radius]
    alb = params[Parametrs.albedo]
    flux = params[Parametrs.stellar_flux]
    press = params[Parametrs.base_pressure]
    emiss = params[Parametrs.emissivity] 
    
    p_color, p_temp = get_planet_preview(rad, alb, flux, press, emiss)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    ax.axis('off')
    
    flux_mult = max(0.2, min(1.0, flux / 2000)) 

    press_factor = press / 100
    for i in range(15):
        glow_rad = rad * (1 + i * 0.03)
        alpha = (1 - i/15) * 0.15 * press_factor * flux_mult
        glow = plt.Circle((0, 0), glow_rad, color=p_color, alpha=alpha, lw=0)
        ax.add_patch(glow)

    base = plt.Circle((0, 0), rad, color='#050505', zorder=2)
    ax.add_patch(base)

    for i in range(30):
        step_rad = rad * (1 - i/45)
        offset = i * 0.012 * rad
        alpha = (1 - i/30) * 0.9 * flux_mult 
        
        light_layer = plt.Circle((offset, offset), step_rad, color=p_color, alpha=alpha, lw=0, zorder=3)
        ax.add_patch(light_layer)

    rim = plt.Circle((0,0), rad, color=p_color, fill=False, lw=1, alpha=0.1 * flux_mult, zorder=4)
    ax.add_patch(rim)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    
    return fig, p_temp

# # Ukrywanie elementów interfejsu Streamlit
# hide_ui_style = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_ui_style, unsafe_allow_html=True)

st.set_page_config(layout="wide")

with st.container(border=True):
    tab_d, tab_g = st.tabs(["Dashboard", "Graphs"])

with tab_d:
    col_img, col1 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")

        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            results = {}
            with st.container(border=True):
                results[Parametrs.mass] = slider_with_input("Mass", 0.1, 10.0, 5.0, "mass")
                results[Parametrs.radius] = slider_with_input("radius", 0.5, 2.5, 1.5, "radius")
                results[Parametrs.albedo] = slider_with_input("albedo", 0.0, 1.0, 0.5, "albedo")
                results[Parametrs.emissivity] = slider_with_input("emissivity", 0.01, 1.0, 0.5, "emissivity")

        with sub_col2:
            with st.container(border=True):
                results[Parametrs.heat_capacity] = slider_with_input("heat capacity", 1000000, 100000000, 50500000, "heat_capacity")
                results[Parametrs.base_diffusion] = slider_with_input("base diffusion", 0.0, 100.0, 50.0, "base_diffusion")
                results[Parametrs.base_pressure] = slider_with_input("base pressure", 0.01, 100.0, 50.0, "base_pressure")
                results[Parametrs.stellar_flux] = slider_with_input("stellar flux", 100.0, 3000.0, 1550.0, "stellar_flux")
        
        st.write("---")
        
        if st.button("Generate"):
            forBackend = PlanetParameters(data=results)

    with col_img:
        st.subheader("Planetary Simulation")

        with st.spinner("Rendering planetary model..."):
            fig_planet, current_temp_k = generate_planet_visual(results)
            
            st.pyplot(fig_planet)

with tab_g:
    col_l, col_r = st.columns([1,1])

    with col_l:
        st.header("wykres 1.")
    
    with col_r:
        st.header("wykres 2.")