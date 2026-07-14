import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Dengue & RENIPRESS",
    page_icon="🏥",
    layout="wide"
)

st.title("📊 Panel de Control: Vigilancia de Dengue y RENIPRESS")
st.markdown("Sistema de Inteligencia de Negocios para la evaluación epidemiológica.")

# Datos de prueba para verificar que encienda perfecto
@st.cache_data
def cargar_datos():
    data = {
        "DEPARTAMENTO": ["LIMA", "PIURA", "LA LIBERTAD", "ICA", "LORETO"],
        "CASOS_DENGUE": [45200, 38100, 21500, 15400, 12800],
        "ESTABLECIMIENTOS_RENIPRESS": [8450, 1200, 1600, 950, 800]
    }
    return pd.DataFrame(data)

df = cargar_datos()

# Métricas rápidas
col1, col2 = st.columns(2)
col1.metric("Total Casos Dengue", "133,000")
col2.metric("Total RENIPRESS", "13,000")

# Mostrar tabla y gráfico
st.subheader("Matriz Regional Integrada")
st.dataframe(df, use_container_width=True)

st.subheader("Gráfico de Casos")
st.bar_chart(df.set_index("DEPARTAMENTO")["CASOS_DENGUE"])
