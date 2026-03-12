import streamlit as st
from dataclasses import dataclass
from planet_visual import generate_planet_visual
import sys
sys.path.insert(1, '..')
sys.path.insert(1, '../graphs/')
sys.path.insert(1, '../../facade/')
from facade import Facade
from params_enum import Parametrs
from graphs import generate_graph_from_facade, generate_global_map, generate_water_map

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

st.set_page_config(layout="wide")

hide_ui_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_ui_style, unsafe_allow_html=True)

if 'sim' not in st.session_state:
    st.session_state.sim = Facade()

if 'generated_chart' not in st.session_state:
    st.session_state['generated_chart'] = None
    
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
                results[Parametrs.heat_capacity] = slider_with_input("heat capacity", 100000000, 1000000000, 505000000, "heat_capacity")
                results[Parametrs.base_diffusion] = slider_with_input("base diffusion", 0.0, 100.0, 1.5, "base_diffusion")
                results[Parametrs.base_pressure] = slider_with_input("base pressure", 0.01, 100.0, 50.0, "base_pressure")
                results[Parametrs.stellar_flux] = slider_with_input("stellar flux", 100.0, 3000.0, 1550.0, "stellar_flux")
        
        st.write("---")
        fig = None 
        if st.button("Generate"):
            st.session_state.sim.set_data(results)
            final_data = st.session_state.sim.run_simulation()
            print(final_data)
            fig = generate_graph_from_facade(final_data)
            fig1 = generate_global_map(final_data)
            fig2 = generate_water_map(final_data)

            # forBackend = PlanetParameters(results)
            # st.success("data processed successfully")
            
            # facade_singleton.set_data(forBackend)
            # facade_singleton.run_simulation()
            # fig = generate_graph_from_facade()

            if fig is not None:
                st.session_state['current_fig'] = fig
                st.session_state['global_map_fig'] = fig1
                st.session_state['water_map_fig'] = fig2
                st.session_state['generated_chart'] = True
                st.success("Chart generated")
            else:
                st.error("Facade is broken lol")
    
    with col_img:
        st.subheader("Planetary Simulation")

        with st.spinner("Rendering planetary model..."):
            fig_planet, current_temp_k = generate_planet_visual(results)
            
            st.pyplot(fig_planet)

with tab_g:
    st.subheader("1D Temperature Gradient")
    if st.session_state['generated_chart'] is not None:
        col_center = st.columns([1, 2, 1])
        with col_center[1]:
            st.pyplot(st.session_state['current_fig']) 
    else:
        st.info("Click 'Generate' in Dashboard, to see charts.")
        
    st.write("---") 
    
    col_map1, col_map2 = st.columns(2)
    
    with col_map1:
        st.subheader("2D Global Thermal Map")
        if st.session_state['generated_chart'] is not None:
            st.pyplot(st.session_state['global_map_fig'])
            
    with col_map2:
        st.subheader("2D Surface Phase Map")
        if st.session_state['generated_chart'] is not None:
            st.pyplot(st.session_state['water_map_fig'])

