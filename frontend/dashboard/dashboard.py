import streamlit as st

st.set_page_config(layout="wide")

tab1, tab3 = st.tabs(["Dashboard", "Graphs"])

with tab1:
    col_obrazek, col1 = st.columns([1, 2])

    # with col_obrazek:
        # st.subheader("Widok projektu")
        # st.image("", caption="Twój obrazek")

    with col1:
        st.subheader("Parametry")

        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            mass = st.slider("mass", 0.1, 10.0, 5.0)
            radius = st.slider("radius", 0.5, 2.5, 1.5)
            albedo = st.slider("albedo", 0.0, 1.0, 0.5)
            emissivity = st.slider("emissivity", 0.01, 1.0, 0.5)

        with sub_col2:
            heat_capacity = st.slider("heat capacity", 1000000, 100000000, 50500000)
            base_diffusion = st.slider("base diffusion", 0.0, 10.0, 5.0)
            base_pressure = st.slider("base pressure", 0.01, 100.0, 50.0)
            stellar_flux = st.slider("stellar flux", 100.0, 3000.0, 1550.0)
        
        st.write("---")
        
        if st.button("Generate"):
            st.success("Przetwarzanie danych: {mass}, {radius}, {albedo}, {emissivity}, {heat_capacity}, {base_diffusion}, {base_pressure}, {stellar_flux}")