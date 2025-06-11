import streamlit as st
from modules.database import initialize_database

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

def renderizar (df_filtrado):
    st.markdown("<h1 style='text-align:center;'>📦 Dashboard Cargas</h1>", unsafe_allow_html=True)
    #BIGNUMBERS
    #- Distância Total Voada (KM) ✈️ – Mostra quantos quilômetros foram percorridos no transporte de cargas.
    #- Total de Carga Paga (KG) 📦 – Exibe o volume total de carga paga transportada.
    #- Total de Carga Grátis (KG) 🎁 – Indica o peso total da carga gratuita transportada.

    #GRAFICOS top #5 aviações com mais cargas
    


    # Big Numbers
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        conn, cursor = initialize_database()
        cursor.execute("SELECT SUM(carga_paga_kg) FROM voos_completos")
        total_carga_paga = cursor.fetchone()[0]
        colored_card("📦", "Total Cargas Pagas", total_carga_paga, "#4CAF50")
    with coluna2:
        cursor.execute("SELECT SUM(carga_paga_km) FROM voos_completos")
        total_distancia_voada = cursor.fetchone()[0]
        colored_card("✈️", "Distancia total Cargas Pagas", total_distancia_voada, "#FF9800")
    with coluna3:
        cursor.execute("SELECT SUM(carga_paga_kg)/SUM(carga_paga_km) FROM voos_completos")
        media_carga_por_km = cursor.fetchone()[0]
        colored_card("🎁", "Peso total de Cargas transportadas", media_carga_por_km, "#2196F3")





