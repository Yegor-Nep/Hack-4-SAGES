import matplotlib.pyplot as plt
from enum import Enum
import numpy as np 
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

class ChartType(Enum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"


def generate_water_map(graph_data):
    if not graph_data:
        return None

    theta = np.array(graph_data.get('theta_angles', []))
    phases = graph_data.get('water_phases', [])

    if len(theta) == 0 or len(phases) == 0:
        return None

    phase_dict = {'Solid': 0, 'Liquid': 1, 'Gas': 2}
    num_phases = np.array([phase_dict.get(p, 1) for p in phases]) 

    lon = np.linspace(-np.pi, np.pi, 100)
    lat = np.linspace(-np.pi/2, np.pi/2, 100)
    Lon, Lat = np.meshgrid(lon, lat)

    cos_c = np.cos(Lat) * np.cos(Lon)
    cos_c = np.clip(cos_c, -1.0, 1.0)
    c_degrees = np.degrees(np.arccos(cos_c))

    Grid_Phases = np.round(np.interp(c_degrees, theta, num_phases))

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax = fig.add_subplot(111, projection='mollweide')
    ax.set_facecolor('#0e1117')

    cmap = mcolors.ListedColormap(['#e0f7fa', '#0277bd', '#ffb74d'])
    bounds = [-0.5, 0.5, 1.5, 2.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    mesh = ax.pcolormesh(Lon, Lat, Grid_Phases, cmap=cmap, norm=norm, shading='nearest')

    ax.grid(True, color='white', linestyle='--', alpha=0.3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title("Global Surface Phase Map", color='white', pad=20)

    ice_patch = mpatches.Patch(color='#e0f7fa', label='Ice (Solid)')
    water_patch = mpatches.Patch(color='#0277bd', label='Ocean (Liquid)')
    gas_patch = mpatches.Patch(color='#ffb74d', label='Steam/Desert (Gas)')
    
    ax.legend(handles=[ice_patch, water_patch, gas_patch], loc='lower center', 
              bbox_to_anchor=(0.5, -0.15), ncol=3, facecolor='#0e1117', 
              edgecolor='none', labelcolor='white')

    return fig

def generate_graph_from_facade(graph_data):
    if not graph_data:
        return None

    x_values = graph_data.get('theta_angles', [])
    y_values = graph_data.get('temperatures', [])
    habitability = graph_data.get('habitability', 0.0)

    if not x_values or not y_values:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    ax.plot(x_values, y_values, color='#ff4b4b', linestyle='-', linewidth=2.5)
    ax.fill_between(x_values, y_values, color='#ff4b4b', alpha=0.15)

    ax.set_title(f"Surface Temperature (Habitability: {habitability:.2f}%)", color='white', pad=15)
    ax.set_xlabel("Planetary Angle (Theta)", color='white')
    ax.set_ylabel("Temperature (Kelvin)", color='white')
    ax.tick_params(colors='white', which='both')

    for spine in ax.spines.values():
        spine.set_edgecolor('#444444')

    ax.grid(True, color='white', linestyle='--', alpha=0.1)

    return fig

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
    cos_c = np.clip(cos_c, -1.0, 1.0) 
    c_degrees = np.degrees(np.arccos(cos_c))

    Grid_Temps = np.interp(c_degrees, theta, temps)

    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117') 
    
    ax = fig.add_subplot(111, projection='mollweide')
    ax.set_facecolor('#0e1117')

    mesh = ax.pcolormesh(Lon, Lat, Grid_Temps, cmap='inferno', shading='auto')

    ax.grid(True, color='white', linestyle='--', alpha=0.3)
    ax.set_xticklabels([]) 
    ax.set_yticklabels([])
    ax.set_title("Global Temperature Map (Spitzer Projection)", color='white', pad=20)

    cbar = plt.colorbar(mesh, orientation='horizontal', pad=0.05, aspect=40)
    cbar.set_label('Temperature (Kelvin)', color='white')
    cbar.ax.xaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='white')

    return fig

