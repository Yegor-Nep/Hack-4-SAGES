import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

class Parametrs(Enum):
    mass = 1
    radius = 2
    albedo = 3
    emissivity = 4
    heat_capacity = 5
    base_diffusion = 6
    base_pressure = 7
    stellar_flux = 8
    
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