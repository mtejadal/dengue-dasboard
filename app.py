import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de pantalla completa
st.set_page_config(page_title="SIS-POL - Analítica Regional", layout="wide")

# ==========================================
# 🎨 ESTILOS CSS (DISEÑO GIGANTE E INTERFAZ LIMPIA)
# ==========================================
st.markdown("""
    <style>
    .block-container { padding: 0rem 1rem !important; max-width: 100% !important; }
    
    .main-banner {
        background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%);
        padding: 20px; border-radius: 4px; margin-top: 15px; margin-bottom: 25px; 
        display: flex; justify-content: space-between; align-items: center; color: white;
    }
    
    /* DISEÑO GIGANTE PARA LAS TARJETAS DE REPORTES (KPI CARDS) */
    .card { 
        background-color: #1e293b; 
        padding: 35px 20px; 
        border-radius: 10px; 
        border: 2px solid #334155; 
        margin-bottom: 15px; 
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-val { 
        font-size: 42px; 
        font-weight: 800; 
        color: #38bdf8; 
        line-height: 1.2;
    }
    .metric-lbl { 
        font-size: 16px; 
        color: #94a3b8; 
        font-weight: 600; 
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    /* INYECCIÓN CSS PARA EL SELECTOR GIGANTE */
    div[data-baseweb="select"] {
        font-size: 22px !important; 
    }
    .stSelectbox label p {
        font-size: 20px !important; 
        font-weight: bold !important;
        color: #38bdf8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Banner Principal
st.markdown("""
    <div class="main-banner">
        <span style="font-weight: bold; font-size: 22px;">⚕️ Sistema Analítico SIS - SALUDPOL</span>
        <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">📊 CONFIGURADOR REGIONAL INTERACTIVO • JUNIO 2026</span>
    </div>
""", unsafe_allow_html=True)

# Verificación de datos
if os.path.exists('data_noviembre_2025.csv'):
    df = pd.read_csv('data_noviembre_2025.csv')
else:
    st.error("Por favor, ejecuta primero 'procesar_datos.py' para generar la data base.")
    st.stop()

# ==========================================
# 🔍 PANEL DE CONTROL: SELECTOR (DISEÑO AMPLIO)
# ==========================================
st.write("### 🔍 Panel de Control: Selección de Cobertura Geográfica")
lista_regiones = sorted(df['Region'].unique())

region_seleccionada = st.selectbox(
    "Selecciona un departamento para filtrar todo el análisis estadístico:",
    options=lista_regiones,
    index=0
)

# Filtrado de datos en vivo
df_filtrado = df[df['Region'] == region_seleccionada].iloc[0]
tabla_region_individual = df[df['Region'] == region_seleccionada][['Region', 'Afiliados', 'Atenciones', 'Reembolsos']]

st.markdown("---")
st.write(f"## 📍 Reporte Consolidado: Región {region_seleccionada.upper()}")
st.write("##### *Los siguientes indicadores y gráficos corresponden exclusivamente a la zona seleccionada.*")

# ==========================================
# 📊 TARJETAS DE MÉTRICAS CLAVE (EXPANDIDAS)
# ==========================================
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""<div class='card'><div class='metric-lbl'>POBLACIÓN AFILIADA ACTIVA</div><div class='metric-val'>{int(df_filtrado['Afiliados']):,}</div></div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class='card'><div class='metric-lbl'>TOTAL ATENCIONES REALIZADAS</div><div class='metric-val'>{int(df_filtrado['Atenciones']):,}</div></div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class='card'><div class='metric-lbl'>MONTO TOTAL REEMBOLSADO</div><div class='metric-val'>S/. {df_filtrado['Reembolsos']:,.2f}</div></div>""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 🎨 GRÁFICOS ESPECÍFICOS
# ==========================================
col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.write("#### 🚻 Perfil Demográfico por Sexo")
    data_sexo = pd.DataFrame({
        'Sexo': ['Masculino', 'Femenino'],
        'Cantidad': [int(df_filtrado['Masc']), int(df_filtrado['Fem'])]
    })
    
    # 🔥 SOLUCIÓN AL ERROR DE COLOR: Mapeamos explícitamente qué color le toca a cada categoría
    fig_sexo = px.pie(
        data_sexo, 
        values='Cantidad', 
        names='Sexo', 
        hole=.4,
        color='Sexo',
        color_discrete_map={'Masculino': '#38bdf8', 'Femenino': '#f472b6'}
    )
    fig_sexo.update_layout(template="plotly_dark", height=320, margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig_sexo, use_container_width=True)

with col_der:
    st.write("#### 🎂 Distribución por Grupos de Edad")
    # Cambiamos el nombre de la columna de 'Total Evaluados' a 'Afiliados Activos'
    data_edad = pd.DataFrame({
        'Rango de Edad': ['Niños (0-11)', 'Jóvenes (12-25)', 'Adultos (26-59)', 'Ancianos (60+)'],
        'Afiliados Activos': [int(df_filtrado['Ninos']), int(df_filtrado['Jov']), int(df_filtrado['Adul']), int(df_filtrado['Anc'])]
    })
    
    # Al usar 'Afiliados Activos' en el eje Y, Plotly lo usará automáticamente en el cartel flotante
    fig_edad = px.bar(
        data_edad, 
        x='Rango de Edad', 
        y='Afiliados Activos', 
        color='Rango de Edad', 
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    # Forzamos a que el cartel flotante sea súper limpio y profesional
    fig_edad.update_traces(
        hovertemplate="<b>%{x}</b><br>Afiliados Activos: %{y:,.0f}<extra></extra>"
    )
    
    fig_edad.update_layout(
        template="plotly_dark", 
        height=320, 
        showlegend=False, 
        xaxis_title="Grupos Generacionales", 
        yaxis_title="Cantidad de Personas"
    )
    st.plotly_chart(fig_edad, use_container_width=True)
# ==========================================
