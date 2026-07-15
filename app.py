import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# 1. Configuración de página limpia
st.set_page_config(
    page_title="Vigilancia Dengue & RENIPRESS",
    page_icon="🏥",
    layout="wide"
)

# 2. Estilos personalizados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: var(--text-color);
    }

    /* Fondo general (se adapta solo a modo claro/oscuro de Streamlit) */
    [data-testid="stAppViewContainer"] {
        background-color: var(--secondary-background-color);
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* Quita el padding superior por defecto de Streamlit para que el header pegue arriba */
    .block-container {
        padding-top: 1rem;
    }

    /* --- SIDEBAR DIFERENCIADO DEL CONTENIDO --- */
    /* Apuntamos a TODOS los contenedores internos, no solo al externo,
       porque Streamlit anida varios divs y algunos quedaban transparentes */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        background-color: var(--background-color) !important;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(99, 102, 241, 0.15);
        box-shadow: 4px 0 18px rgba(79, 70, 229, 0.06);
        padding-top: 10px;
        z-index: 999999 !important;
        min-height: 100vh;
    }

    /* En mobile, el sidebar se abre como panel flotante: aseguramos que
       cubra todo el alto y quede siempre por encima de todo el contenido */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            z-index: 999999 !important;
            min-height: 100vh !important;
            box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
        }
        [data-testid="stSidebarContent"] {
            min-height: 100vh !important;
        }
    }

    [data-testid="stSidebar"] h2 {
        color: #6366f1 !important;
        font-size: 20px !important;
        font-weight: 700;
    }

    /* Estilo del option_menu (nav-pills) */
    [data-testid="stSidebar"] nav {
        background-color: transparent !important;
    }

    /* --- HEADER SUPERIOR (índigo -> violeta) --- */
    .top-header {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        padding: 18px 28px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
    }
    .top-header-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
        margin: 0;
    }
    .top-header-badge {
        color: #ede9fe;
        font-size: 13px;
        font-weight: 500;
    }

    /* Título de sección (debajo del header) */
    .header-title {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #6366f1;
        margin-bottom: 0px;
    }
    .header-subtitle {
        font-size: 15px;
        color: var(--text-color);
        opacity: 0.65;
        margin-bottom: 25px;
    }

    /* Los 3 cuadrados de colores arriba */
    .card-blue {
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
        padding: 16px 20px; border-radius: 14px; color: white; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .card-green {
        background: linear-gradient(135deg, #2dd4bf 0%, #0f766e 100%);
        padding: 16px 20px; border-radius: 14px; color: white; box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
    }
    .card-red {
        background: linear-gradient(135deg, #fb7185 0%, #be123c 100%);
        padding: 16px 20px; border-radius: 14px; color: white; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.3);
    }
    .card-title {
        font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9; margin-bottom: 4px;
    }
    .card-value {
        font-size: 26px; font-weight: 700; margin: 0;
    }

    /* Contenedor redondeado con relieve (efecto tarjeta) exclusivo para los gráficos */
    .grafico-card {
        background: var(--background-color);
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 12px 28px -6px rgba(79, 70, 229, 0.12), 0 4px 10px -4px rgba(79, 70, 229, 0.06);
        border: 1px solid rgba(99, 102, 241, 0.10);
        margin-bottom: 20px;
    }

    /* --- LISTA DE REGIONES (Reportes por Región) --- */
    .region-list-title {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-color);
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 10px;
    }
    /* Botones normales de la lista (no seleccionados) */
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"] {
        text-align: left !important;
        justify-content: flex-start !important;
        background-color: transparent !important;
        color: var(--text-color) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500;
        padding: 8px 12px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"]:hover {
        background-color: rgba(99, 102, 241, 0.12) !important;
        color: #6366f1 !important;
    }
    /* Botón seleccionado (activo, resaltado en índigo) */
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="primary"] {
        text-align: left !important;
        justify-content: flex-start !important;
        background-color: #6366f1 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600;
        padding: 8px 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar datos reales
@st.cache_data
def cargar_datos():
    df = pd.read_excel("REPORTE UNIFICADO DENGUE RENIPRESS.xlsx")
    df.columns = df.columns.str.strip().str.upper()
    return df

try:
    df = cargar_datos()

    total_dengue = int(df["CASOS_DENGUE_2024"].sum()) if "CASOS_DENGUE_2024" in df.columns else 0
    total_renipress = int(df["TOTAL_ESTABLECIMIENTOS_SALUD"].sum()) if "TOTAL_ESTABLECIMIENTOS_SALUD" in df.columns else 0
    total_regiones = df["DEPARTAMENTO"].nunique() if "DEPARTAMENTO" in df.columns else 0

    # ----------------------------------------------------
    # MENÚ LATERAL ESTILO IMAGEN 2 (sidebar blanco + iconos)
    # ----------------------------------------------------
    with st.sidebar:
        st.markdown("## 🏥 Menú Principal")
        st.markdown("---")
        menu = option_menu(
            menu_title=None,
            options=["Dashboard General", "Reportes por Región", "Base de Datos"],
            icons=["bar-chart-fill", "geo-alt-fill", "database-fill"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#6366f1", "font-size": "16px"},
                "nav-link": {
                    "font-size": "15px",
                    "font-weight": "500",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "10px 14px",
                    "border-radius": "10px",
                    "color": "var(--text-color)",
                    "--hover-color": "rgba(99, 102, 241, 0.12)",
                },
                "nav-link-selected": {
                    "background-color": "#6366f1",
                    "color": "white",
                    "font-weight": "600",
                },
            }
        )

    # ----------------------------------------------------
    # HEADER AZUL SUPERIOR (visible en todas las pestañas)
    # ----------------------------------------------------
    st.markdown(f"""
        <div class="top-header">
            <p class="top-header-title">🏥 Vigilancia Dengue & RENIPRESS</p>
            <p class="top-header-badge">Dataset Local Integrado</p>
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # DASHBOARD GENERAL
    # ----------------------------------------------------
    if menu == "Dashboard General":
        st.markdown("<div class='header-title'>📊 Dashboard de Vigilancia Epidemiológica</div>", unsafe_allow_html=True)
        st.markdown("<div class='header-subtitle'>Monitoreo en tiempo real de Casos de Dengue y Capacidad Hospitalaria (RENIPRESS)</div>", unsafe_allow_html=True)

        # Los 3 cuadrados de colores arriba
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class='card-blue'>
                    <div class='card-title'>Total Casos Dengue</div>
                    <div class='card-value'>{total_dengue:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class='card-green'>
                    <div class='card-title'>Establecimientos RENIPRESS</div>
                    <div class='card-value'>{total_renipress:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class='card-red'>
                    <div class='card-title'>Regiones Evaluadas</div>
                    <div class='card-value'>{total_regiones}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_izq, col_der = st.columns([1.4, 0.6])

        with col_izq:
            st.markdown("<div class='grafico-card'>", unsafe_allow_html=True)
            st.subheader("Casos de Dengue por Departamento")
            if "DEPARTAMENTO" in df.columns and "CASOS_DENGUE_2024" in df.columns:
                df_ordenado = df.sort_values("CASOS_DENGUE_2024", ascending=False)

                fig_bar = px.bar(
                    df_ordenado, x="DEPARTAMENTO", y="CASOS_DENGUE_2024",
                    color_discrete_sequence=["#6366f1"],
                    text="CASOS_DENGUE_2024"
                )
                fig_bar.update_traces(
                    texttemplate='%{text:,}',
                    textposition='outside',
                    textfont=dict(size=10, color="#818cf8"),
                    cliponaxis=False,
                    marker=dict(line=dict(width=0))
                )
                fig_bar.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=40, b=20, l=10, r=10),
                    xaxis=dict(tickangle=-45, title="", tickfont=dict(size=10, color="#94a3b8"), fixedrange=True),
                    yaxis=dict(title="", gridcolor="rgba(148, 163, 184, 0.3)", tickfont=dict(color="#94a3b8"), fixedrange=True),
                    height=430,
                    bargap=0.3,
                    dragmode=False
                )

                st.plotly_chart(
                    fig_bar, use_container_width=True,
                    config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False}
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_der:
            st.markdown("<div class='grafico-card'>", unsafe_allow_html=True)
            st.subheader("Distribución por Edades")
            columnas_edades = [c for c in ["NIÑOS (0-11)", "ADOLESCENTES (12-17)", "ADULTOS (18-59)", "ADULTOS MAYORES (60+)"] if c in df.columns]
            if columnas_edades:
                df_edades = df[columnas_edades].sum().reset_index()
                df_edades.columns = ['Grupo Etario', 'Casos']

                fig_pie = px.pie(
                    df_edades, values='Casos', names='Grupo Etario', hole=0.45,
                    color_discrete_sequence=["#6366f1", "#2dd4bf", "#f59e0b", "#fb7185"]
                )
                fig_pie.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=380,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94a3b8"))
                )
                st.plotly_chart(
                    fig_pie, use_container_width=True,
                    config={"displayModeBar": False, "scrollZoom": False}
                )
            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # REPORTES POR REGIÓN
    # ----------------------------------------------------
    elif menu == "Reportes por Región":
        st.markdown("<div class='header-title'>🔍 Análisis Comparativo por Región</div>", unsafe_allow_html=True)
        st.markdown("<div class='header-subtitle'>Seleccione un departamento para evaluar su capacidad hospitalaria frente al dengue.</div>", unsafe_allow_html=True)

        if "DEPARTAMENTO" in df.columns:
            lista_departamentos = sorted(df["DEPARTAMENTO"].dropna().unique().tolist())

            # Estado persistente de la región seleccionada
            if "region_seleccionada" not in st.session_state:
                st.session_state.region_seleccionada = lista_departamentos[0]

            col_lista, col_grafico = st.columns([1, 2.2])

            # ---------- COLUMNA IZQUIERDA: buscador + lista de regiones ----------
            with col_lista:
                st.markdown("<div class='grafico-card' style='padding:18px;'>", unsafe_allow_html=True)
                st.markdown("<div class='region-list-title'>Región</div>", unsafe_allow_html=True)
                busqueda = st.text_input(
                    "Buscar región", "", placeholder="🔍 Buscar región...", label_visibility="collapsed"
                )
                filtrados = (
                    [d for d in lista_departamentos if busqueda.upper() in d.upper()]
                    if busqueda else lista_departamentos
                )

                with st.container(height=320):
                    for depto in filtrados:
                        es_activo = (depto == st.session_state.region_seleccionada)
                        if st.button(
                            depto,
                            key=f"btn_region_{depto}",
                            use_container_width=True,
                            type="primary" if es_activo else "secondary"
                        ):
                            st.session_state.region_seleccionada = depto
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            region_seleccionada = st.session_state.region_seleccionada
            df_reg = df[df["DEPARTAMENTO"] == region_seleccionada].iloc[0]
            casos_reg = df_reg.get("CASOS_DENGUE_2024", 0)
            renipress_reg = df_reg.get("TOTAL_ESTABLECIMIENTOS_SALUD", 0)

            # ---------- COLUMNA DERECHA: gráfico de la región seleccionada ----------
            with col_grafico:
                st.markdown("<div class='grafico-card'>", unsafe_allow_html=True)
                st.markdown(f"#### {region_seleccionada}")
                st.caption("Casos de Dengue vs. Establecimientos RENIPRESS")

                df_comparativa = pd.DataFrame({
                    "Indicador": ["Casos de Dengue", "Establecimientos RENIPRESS"],
                    "Valor": [casos_reg, renipress_reg]
                })

                fig_reg = px.bar(
                    df_comparativa, x="Indicador", y="Valor", text="Valor",
                    color="Indicador",
                    color_discrete_map={"Casos de Dengue": "#fb7185", "Establecimientos RENIPRESS": "#6366f1"}
                )
                fig_reg.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=20, b=10, l=10, r=10),
                    height=380,
                    showlegend=False,
                    xaxis=dict(title="", tickfont=dict(size=14, color="#94a3b8"), fixedrange=True),
                    yaxis=dict(title="", gridcolor="rgba(148, 163, 184, 0.3)", tickfont=dict(color="#94a3b8"), fixedrange=True),
                    dragmode=False
                )
                st.plotly_chart(
                    fig_reg, use_container_width=True,
                    config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False}
                )
                st.markdown("</div>", unsafe_allow_html=True)

            # ---------- TABLA COMPARATIVA COMPLETA (todas las regiones) ----------
            st.markdown("<div class='grafico-card'>", unsafe_allow_html=True)
            st.markdown("##### 📋 Desglose Analítico por Región")
            columnas_tabla = [c for c in ["DEPARTAMENTO", "CASOS_DENGUE_2024", "TOTAL_ESTABLECIMIENTOS_SALUD"] if c in df.columns]
            df_tabla = df[columnas_tabla].rename(columns={
                "DEPARTAMENTO": "Región",
                "CASOS_DENGUE_2024": "Casos de Dengue",
                "TOTAL_ESTABLECIMIENTOS_SALUD": "Establecimientos RENIPRESS"
            })
            if "Casos de Dengue" in df_tabla.columns:
                df_tabla = df_tabla.sort_values("Casos de Dengue", ascending=False)
            st.dataframe(df_tabla, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # BASE DE DATOS
    # ----------------------------------------------------
    elif menu == "Base de Datos":
        st.markdown("<div class='header-title'>🗄️ Base de Datos Integrada</div>", unsafe_allow_html=True)
        st.markdown("<div class='header-subtitle'>Matriz completa de registros procesados.</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Ocurrió un error al cargar la aplicación: {e}")
