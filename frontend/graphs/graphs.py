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
