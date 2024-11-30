# Paso 1: Instalar las dependencias
#!pip install streamlit
#!pip install pyngrok

# Paso 2: Escribir el código de la aplicación en app.py
#%%writefile app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Título de la Aplicación
st.title("Simulación de Distribución Muestral de Medias")

# Sección de Configuración
st.sidebar.header("Configuración de la Simulación")

# Selección de la Distribución Poblacional
distribucion = st.sidebar.selectbox(
    "Distribución Poblacional:",
    ("Normal", "Uniforme", "Exponencial", "Binomial", "Poisson")
)

# Tamaño de la Muestra (n)
tamaño_muestra = st.sidebar.number_input(
    "Tamaño de la Muestra (n):",
    min_value=1,
    value=30,
    step=1
)

# Número de Muestras
numero_muestras = st.sidebar.number_input(
    "Número de Muestras:",
    min_value=1,
    value=50,
    step=1
)

# Botón para Iniciar la Simulación
if st.sidebar.button("Iniciar Simulación"):
    # Generar Datos Poblacionales
    if distribucion == "Normal":
        datos_poblacion = np.random.normal(loc=0, scale=1, size=10000)
        sigma_poblacional = 1
    elif distribucion == "Uniforme":
        datos_poblacion = np.random.uniform(low=0, high=1, size=10000)
        sigma_poblacional = np.std(datos_poblacion)
    elif distribucion == "Exponencial":
        datos_poblacion = np.random.exponential(scale=1, size=10000)
        sigma_poblacional = np.std(datos_poblacion)
    elif distribucion == "Binomial":
        datos_poblacion = np.random.binomial(n=10, p=0.5, size=10000)
        sigma_poblacional = np.std(datos_poblacion)
    elif distribucion == "Poisson":
        datos_poblacion = np.random.poisson(lam=3, size=10000)
        sigma_poblacional = np.std(datos_poblacion)
    else:
        st.error("Distribución no soportada.")
        st.stop()

    # Función para Generar Muestras y Calcular Promedios
    def generar_muestras(datos, n, m):
        medias = []
        for _ in range(m):
            muestra = np.random.choice(datos, size=n, replace=True)
            media = np.mean(muestra)
            medias.append(media)
        return medias

    # Generar las Medias Muestrales
    medias_muestrales = generar_muestras(datos_poblacion, tamaño_muestra, numero_muestras)

    # Cálculos de Resultados
    desviacion_medias = np.std(medias_muestrales, ddof=1)
    error_estandar = sigma_poblacional / np.sqrt(tamaño_muestra)

    # Mostrar Resultados
    st.subheader("Resultados de la Simulación")
    col1, col2, col3 = st.columns(3)
    col1.metric("Número de Muestras", numero_muestras)
    col2.metric("Desviación de las Medias", f"{desviacion_medias:.2f}")
    col3.metric("Desviación Poblacional", f"{sigma_poblacional:.2f}")
    st.metric("Cociente σ/√n", f"{error_estandar:.2f}")

    # Gráficos
    st.subheader("Visualización de Resultados")

    # Gráfico de la Distribución Poblacional
    fig1, ax1 = plt.subplots()
    ax1.hist(datos_poblacion, bins=30, color='skyblue', edgecolor='black')
    ax1.set_title(f"Distribución Poblacional ({distribucion})")
    ax1.set_xlabel("Valores")
    ax1.set_ylabel("Frecuencia")
    st.pyplot(fig1)

    # Gráfico de la Distribución de las Medias Muestrales
    fig2, ax2 = plt.subplots()
    ax2.hist(medias_muestrales, bins=30, color='salmon', edgecolor='black')
    ax2.set_title("Distribución de las Medias Muestrales")
    ax2.set_xlabel("Media de la Muestra")
    ax2.set_ylabel("Frecuencia")
    st.pyplot(fig2)

    # Tabla de Resultados
    st.subheader("Tabla de Medias Muestrales")
    df = pd.DataFrame({
        "N° Muestra": np.arange(1, numero_muestras + 1),
        "Promedio de la Muestra": medias_muestrales
    })
    st.dataframe(df.style.format({"Promedio de la Muestra": "{:.2f}"}))

# Paso 3: Importar pyngrok y configurar
from pyngrok import ngrok
import os
import time
import threading
import sys

# Configurar el puerto para Streamlit
port = 8501

# Iniciar el túnel de ngrok
public_url = ngrok.connect(port)
print(f"La aplicación está disponible en: {public_url}")

# Función para ejecutar Streamlit
def run_streamlit():
    # Ejecutar Streamlit y redirigir la salida para evitar que se muestre en Colab
    os.system(f"streamlit run app.py --server.port {port} --server.enableCORS false")

# Ejecutar Streamlit en un hilo separado
threading.Thread(target=run_streamlit).start()

# Mantener la ejecución del notebook abierta mientras la aplicación está en funcionamiento
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
        break
