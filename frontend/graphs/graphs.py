import matplotlib.pyplot as plt
from enum import Enum

class ChartType(Enum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"

def generate_graph_from_facade(graph_data):
    if not graph_data:
        return None

    x_values = graph_data.get('theta_angles', [])
    y_values = graph_data.get('temperatures', [])
    habitability = graph_data.get('habitability', 0.0)

    if not x_values or not y_values:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x_values, y_values, color='red', linestyle='-', linewidth=2)
    ax.fill_between(x_values, y_values, color='red', alpha=0.1)

    ax.set_title(f"Surface Temperature (Habitability: {habitability:.2f}%)")
    ax.set_xlabel("Planetary Angle (Theta)")
    ax.set_ylabel("Temperature (Kelvin)")
    ax.grid(True, linestyle='--', alpha=0.5)

    return fig



import numpy as np 

def generate_global_map(graph_data):
    if not graph_data:
        return None

    theta = np.array(graph_data.get('theta_angles', []))
    temps = np.array(graph_data.get('temperatures', []))

    if len(theta) == 0 or len(temps) == 0:
        return None

    lon = np.linspace(-np.pi, np.pi, 100)
    lat = np.linspace(-np.pi/2, np.pi/2, 100)
    Lon, Lat = np.meshgrid(lon, lat)

    cos_c = np.cos(Lat) * np.cos(Lon)
    cos_c = np.clip(cos_c, -1.0, 1.0) # Prevent math errors
    c_degrees = np.degrees(np.arccos(cos_c))

    Grid_Temps = np.interp(c_degrees, theta, temps)

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117') # Match Streamlit dark mode
    
    ax = fig.add_subplot(111, projection='mollweide')
    ax.set_facecolor('#0e1117')

    mesh = ax.pcolormesh(Lon, Lat, Grid_Temps, cmap='inferno', shading='auto')

    ax.grid(True, color='white', linestyle='--', alpha=0.3)
    ax.set_xticklabels([]) # Hide the default coordinates for a cleaner look
    ax.set_yticklabels([])
    ax.set_title("Global Temperature Map (Spitzer Projection)", color='white', pad=20)

    cbar = plt.colorbar(mesh, orientation='horizontal', pad=0.05, aspect=40)
    cbar.set_label('Temperature (Kelvin)', color='white')
    cbar.ax.xaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='white')

    return fig


"""
def generate_graph_from_facade(graph_data):
    if not graph_data:
        return None

    chart_type = graph_data.get('type')
    x_values = graph_data.get('theta_angles', [])
    y_values = graph_data.get('temperatures', [])
    title = graph_data.get('title', 'temperatura na kątach')

    if not x_values or not y_values:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    if chart_type == ChartType.BAR:
        ax.bar(x_values, y_values, color='skyblue', edgecolor='black')
        
    elif chart_type == ChartType.LINE:
        ax.plot(x_values, y_values, marker='o', color='green', linestyle='-')
        
    elif chart_type == ChartType.SCATTER:
        ax.scatter(x_values, y_values, color='red', alpha=0.7)
        
    else:
        plt.close(fig) 
        return None

    ax.set_title(title)
    ax.set_xlabel("Oś X")
    ax.set_ylabel("Oś Y")
    ax.grid(True, linestyle='--', alpha=0.5)

    print(fig)

    plt.close(fig)

    return fig
"""
