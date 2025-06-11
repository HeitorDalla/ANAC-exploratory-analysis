import streamlit as st
from modules.database import initialize_database
from modules.views import total_carga_paga, distancia_total_voada, carga_por_km

def colored_card(metric_emoji, metric_label, metric_value, bg_color):
    st.markdown(
        f"""
        <div style='background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;'>
            <p style='margin:0; font-weight:bold; color:white; font-size:24px;'>
                <span style='font-size:36px;'>{metric_emoji}</span> {metric_label}
            </p>
            <p style='margin:0; font-size:36px; color:white; font-weight:bold;'>{metric_value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def renderizar(mes, empresa, uf):
    st.markdown("<h1 style='text-align:center;'>📦 Dashboard Cargas</h1>", unsafe_allow_html=True)

    conn, cursor = initialize_database()

    # Aplicação dos filtros nos Big Numbers
    coluna1, coluna2, coluna3 = st.columns(3)
    
    with coluna1:
        total_carga = total_carga_paga(mes, empresa, uf)
        colored_card("📦", "Total Cargas Pagas", total_carga, "#4CAF50")
    
    with coluna2:
        total_distancia_voada = distancia_total_voada(mes, empresa, uf)
        colored_card("✈️", "Distância Total Voada", total_distancia_voada, "#FF9800")

    with coluna3:
        media_carga_por_km = carga_por_km(mes, empresa, uf)
        colored_card("🎁", "Carga Paga por KM", media_carga_por_km, "#2196F3")