import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Dengue & RENIPRESS", layout="wide")

st.title("📊 Panel de Control: Vigilancia de Dengue y RENIPRESS")

# Cargar el archivo CSV
@st.cache_data
def cargar_datos():
    # Intenta leer con coma o punto y coma por si acaso
    try:
        df = pd.read_csv("REPORTE_UNIFICADO_DENGUE_RENIPRESS.csv")
    except:
        df = pd.read_csv("REPORTE_UNIFICADO_DENGUE_RENIPRESS.csv", sep=";")
    return df

try:
    df = cargar_datos()
    
    # Esto te mostrará en tu página web cuáles son los nombres exactos de tus columnas
    st.write("Columna(s) detectadas en tu CSV:", list(df.columns))
    
    # Muestra la tabla tal cual está en tu archivo
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
