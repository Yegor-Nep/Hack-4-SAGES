import subprocess
import json
import plotly.graph_objects as go
from planet_visual import Parametrs 

def generate_temperature_plot(params_dict):
    # Wyciąganie danych podanych z dashboardu kolegi
    mass = params_dict[Parametrs.mass]
    radius = params_dict[Parametrs.radius]
    albedo = params_dict[Parametrs.albedo]
    emissivity = params_dict[Parametrs.emissivity]
    heat_capacity = params_dict[Parametrs.heat_capacity]
    base_pressure = params_dict[Parametrs.base_pressure]
    base_diffusion = params_dict[Parametrs.base_diffusion]
    stellar_flux = params_dict[Parametrs.stellar_flux]
    
    # Wywołanie skompilowanego programu C++ za pomocą subprocess
    # Ścieżka musi zgadzać się z miejscem gdzie Linux zbuduje Twój 'test_run'
    try:
        process = subprocess.run(
            ["./backend/test_run", 
             str(mass), str(radius), str(albedo), str(emissivity), 
             str(heat_capacity), str(base_pressure), str(base_diffusion), str(stellar_flux)],
            capture_output=True, text=True, check=True
        )
        
        # Odbiór danych (magia JSON-a!)
        data = json.loads(process.stdout)
        theta_angles = data["theta"]
        temperatures = data["temp"]
        
    except subprocess.CalledProcessError as e:
        print(f"Błąd C++: {e.stderr}")
        return go.Figure() # W razie błędu omijamy zepsucie całej aplikacji
    except json.JSONDecodeError:
        print("Nie udało się odczytać JSON z backendu.")
        return go.Figure()

    # Tworzenie wykresu Plotly!
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=theta_angles,
        y=temperatures,
        mode='lines',
        name='Temperatura',
        line=dict(color='firebrick', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title='Symulowana Temperatura Powierzchni (Tidally Locked)',
        xaxis_title='Kąt Theta (°)',
        yaxis_title='Temperatura [K]'
    )
    
    return fig
