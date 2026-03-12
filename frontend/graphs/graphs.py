import matplotlib.pyplot as plt
from enum import Enum

from facade import facade_singleton 

class ChartType(Enum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"

def generate_graph_from_facade():

    graph_data = facade_singleton.get_output()
    
    if not graph_data:
        return None

    chart_type = graph_data.get('type')
    x_values = graph_data.get('x', [])
    y_values = graph_data.get('y', [])
    title = graph_data.get('title', 'Brak tytułu')

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

    plt.close(fig)

    return fig