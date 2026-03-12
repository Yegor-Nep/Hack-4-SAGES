import matplotlib.pyplot as plt
from enum import Enum

# Importujemy instancję fasady
from facade import facade_singleton 

class ChartType(Enum):
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"

def generate_graph_from_facade():
    """
    Pobiera dane z Fasady, generuje obiekt wykresu i go ZWRACA.
    Nie wyświetla wykresu samodzielnie.
    """
    # 1. Pobranie danych z fasady
    graph_data = facade_singleton.get_data()
    
    # Jeśli nie ma danych, zwracamy None, żeby dashboard wiedział, że nie ma co rysować
    if not graph_data:
        return None

    # Wyciągnięcie danych ze słownika
    chart_type = graph_data.get('type')
    x_values = graph_data.get('x', [])
    y_values = graph_data.get('y', [])
    title = graph_data.get('title', 'Brak tytułu')

    if not x_values or not y_values:
        return None

    # 2. Podejście obiektowe: tworzymy 'Figure' (całe okno/płótno) i 'Axes' (właściwy wykres)
    fig, ax = plt.subplots(figsize=(8, 5))

    # 3. Rysowanie danych na obiekcie 'ax' (a nie bezpośrednio w plt)
    if chart_type == ChartType.BAR:
        ax.bar(x_values, y_values, color='skyblue', edgecolor='black')
        
    elif chart_type == ChartType.LINE:
        ax.plot(x_values, y_values, marker='o', color='green', linestyle='-')
        
    elif chart_type == ChartType.SCATTER:
        ax.scatter(x_values, y_values, color='red', alpha=0.7)
        
    else:
        # Jeśli typ jest zły, zamykamy pusty wykres w pamięci i zwracamy None
        plt.close(fig) 
        return None

    # 4. Konfiguracja osi i tytułów na obiekcie 'ax'
    ax.set_title(title)
    ax.set_xlabel("Oś X")
    ax.set_ylabel("Oś Y")
    ax.grid(True, linestyle='--', alpha=0.5)

    # Zamykamy wykres dla wewnętrznego silnika matplotlib, żeby nie renderował się w tle
    # (Dashboard sam go wyrenderuje używając obiektu fig)
    plt.close(fig)

    # 5. ZWRACAMY GOTOWY OBIEKT WYKRESU
    return fig