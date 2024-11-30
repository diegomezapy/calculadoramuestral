import numpy as np
import pandas as pd
import plotly.graph_objs as go
import ipywidgets as widgets
from IPython.display import display, clear_output

# Definir las distribuciones disponibles
distribuciones = {
    'Normal': lambda size: np.random.normal(loc=0, scale=1, size=size),
    'Uniforme': lambda size: np.random.uniform(low=0, high=1, size=size),
    'Exponencial': lambda size: np.random.exponential(scale=1, size=size),
    'Binomial': lambda size: np.random.binomial(n=10, p=0.5, size=size),
    'Poisson': lambda size: np.random.poisson(lam=3, size=size)
}

# Crear widgets
distribucion_widget = widgets.Dropdown(
    options=list(distribuciones.keys()),
    value='Normal',
    description='Distribución:',
    disabled=False,
)

tamaño_muestra_widget = widgets.IntSlider(
    value=30,
    min=1,
    max=1000,
    step=1,
    description='Tamaño n:',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

numero_muestras_widget = widgets.IntSlider(
    value=50,
    min=1,
    max=1000,
    step=1,
    description='Número de muestras:',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

boton_simular = widgets.Button(
    description='Iniciar Simulación',
    button_style='success',
    tooltip='Haz clic para iniciar la simulación',
    icon='play'
)

boton_reiniciar = widgets.Button(
    description='Reiniciar',
    button_style='warning',
    tooltip='Haz clic para reiniciar la simulación',
    icon='refresh'
)

# Crear contenedores para los resultados
resultado_widget = widgets.Output()

# Definir la función de simulación
def simular(b):
    with resultado_widget:
        clear_output(wait=True)
        distribucion = distribucion_widget.value
        n = tamaño_muestra_widget.value
        m = numero_muestras_widget.value
        
        # Generar datos poblacionales
        datos_poblacion = distribuciones
        sigma_poblacional = np.std(datos_poblacion, ddof=1)
        
        # Generar muestras y calcular medias
        medias_muestrales = np.random.choice(datos_poblacion, size=(m, n), replace=True).mean(axis=1)
        desviacion_medias = np.std(medias_muestrales, ddof=1)
        error_estandar = sigma_poblacional / np.sqrt(n)
        
        # Mostrar métricas
        col1, col2, col3 = widgets.HBox([
            widgets.VBox([widgets.Label("Número de Muestras"), widgets.Label(str(m))]),
            widgets.VBox([widgets.Label("Desviación de las Medias"), widgets.Label(f"{desviacion_medias:.2f}")]),
            widgets.VBox([widgets.Label("Desviación Poblacional"), widgets.Label(f"{sigma_poblacional:.2f}")])
        ])
        display(col1, col2, col3)
        display(widgets.Label(f"Cociente σ/√n: {error_estandar:.2f}"))
        
        # Crear gráficos
        fig_poblacion = go.Figure()
        fig_poblacion.add_trace(go.Histogram(x=datos_poblacion, nbinsx=30, marker_color='skyblue'))
        fig_poblacion.update_layout(
            title=f"Distribución Poblacional ({distribucion})",
            xaxis_title="Valores",
            yaxis_title="Frecuencia",
            bargap=0.1
        )
        
        fig_medias = go.Figure()
        fig_medias.add_trace(go.Histogram(x=medias_muestrales, nbinsx=30, marker_color='salmon'))
        fig_medias.update_layout(
            title="Distribución de las Medias Muestrales",
            xaxis_title="Media de la Muestra",
            yaxis_title="Frecuencia",
            bargap=0.1
        )
        
        display(fig_poblacion)
        display(fig_medias)
        
        # Crear tabla de resultados
        df_resultados = pd.DataFrame({
            "N° Muestra": np.arange(1, m + 1),
            "Promedio de la Muestra": medias_muestrales
        })
        st_table = df_resultados.style.format({"Promedio de la Muestra": "{:.2f}"})
        display(st_table)

# Definir la función de reinicio
def reiniciar(b):
    with resultado_widget:
        clear_output(wait=True)
        tamaño_muestra_widget.value = 30
        numero_muestras_widget.value = 50
        distribucion_widget.value = 'Normal'

# Asignar las funciones a los botones
boton_simular.on_click(simular)
boton_reiniciar.on_click(reiniciar)

# Organizar los widgets en el notebook
configuracion = widgets.VBox([
    distribucion_widget,
    tamaño_muestra_widget,
    numero_muestras_widget,
    widgets.HBox([boton_simular, boton_reiniciar])
])

# Mostrar los widgets y el contenedor de resultados
st_header = widgets.HTML("<h2>Configuración de la Simulación</h2>")
display(st_header, configuracion, resultado_widget)
