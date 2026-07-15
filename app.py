import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Dengue & RENIPRESS",
    page_icon="🏥",
    layout="wide"
)

st.title("📊 Panel de Control: Vigilancia de Dengue y RENIPRESS")
st.markdown("Sistema de Inteligencia de Negocios para la evaluación epidemiológica con datos integrados.")

# Cargar tu archivo CSV unificado real
@st.cache_data
def cargar_datos():
    # Lee directamente el archivo CSV que subiste a GitHub
    df = pd.read_csv("REPORTE_UNIFICADO_DENGUE_RENIPRESS.csv") 
    return df

try:
    df = cargar_datos()

    # Métricas calculadas automáticamente con tus datos reales
    total_dengue = df["CASOS_DENGUE"].sum()
    total_renipress = df["ESTABLECIMIENTOS_RENIPRESS"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Casos Dengue (Real)", f"{total_dengue:,}")
    col2.metric("Total RENIPRESS (Real)", f"{total_renipress:,}")

    # Mostrar la tabla integrada
    st.subheader("Matriz Regional Integrada")
    st.dataframe(df, use_container_width=True)

    # Gráfico de barras con tus datos
    st.subheader("Gráfico de Casos por Departamento")
    st.bar_chart(df.set_index("DEPARTAMENTO")["CASOS_DENGUE"])

except Exception as e:
    st.error(f"Error al cargar el archivo de datos: {e}. Revisa que las columnas 'CASOS_DENGUE', 'ESTABLECIMIENTOS_RENIPRESS' y 'DEPARTAMENTO' existan exactamente con esos nombres en tu CSV.")
