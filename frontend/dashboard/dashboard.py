import streamlit as st

class Data:
    def __init__(self, mass, radius, albedo, emissivity, heat_capacity, base_diffusion, base_pressure, stellar_flux):
        self.mass = mass
        self.radius = radius
        self.albedo = albedo
        self.emissivity = emissivity
        self.heat_capacity = heat_capacity
        self.base_diffusion = base_diffusion
        self.base_pressure = base_pressure
        self.stellar_flux = stellar_flux 

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
    tab1, tab2 = st.tabs(["Dashboard", "Graphs"])

with tab1:
    col_obrazek, col1 = st.columns([1, 2])

    # with col_obrazek:
        # st.subheader("Widok projektu")
        # st.image("", caption="Twój obrazek")

    with col1:
        st.subheader("Parameters")

        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            with st.container(border=True):
                mass = slider_with_input("Mass", 0.1, 10.0, 5.0, "mass")
                radius = slider_with_input("radius", 0.5, 2.5, 1.5, "radius")
                albedo = slider_with_input("albedo", 0.0, 1.0, 0.5, "albedo")
                emissivity = slider_with_input("emissivity", 0.01, 1.0, 0.5, "emissivity")

        with sub_col2:
            with st.container(border=True):
                heat_capacity = slider_with_input("heat capacity", 1000000, 100000000, 50500000, "heat_capacity")
                base_diffusion = slider_with_input("base diffusion", 0.0, 10.0, 5.0, "base_diffusion")
                base_pressure = slider_with_input("base pressure", 0.01, 100.0, 50.0, "base_pressure")
                stellar_flux = slider_with_input("stellar flux", 100.0, 3000.0, 1550.0, "stellar_flux")
        
        st.write("---")
        
        if st.button("Generate"):
            st.success("Przetwarzanie danych")
            sliders_data = Data(mass, radius, albedo, emissivity, heat_capacity, base_diffusion, base_pressure, stellar_flux)