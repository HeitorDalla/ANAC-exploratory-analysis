import streamlit as st
from modules.database import initialize_database

    #- Distância Total Voada (KM) ✈️ – Mostra quantos quilômetros foram percorridos no transporte de cargas.Add commentMore actions
    #- Total de Carga Paga (KG) 📦 – Exibe o volume total de carga paga transportada.
    #- Total de Carga Grátis (KG) 🎁 – Indica o peso total da carga gratuita transportada.

    #GRAFICOS top #5 aviações com mais cargas

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

def renderizar(df_filtrado):
    # Título da página
    st.title("Análise de Cargas")
    
    # Cálculos
    distancia_total = df_filtrado['DISTÂNCIA'].sum() if 'DISTÂNCIA' in df_filtrado.columns else 0
    carga_paga_total = df_filtrado['PESO_CARGA_PAGA'].sum() if 'PESO_CARGA_PAGA' in df_filtrado.columns else 0
    carga_gratis_total = df_filtrado['PESO_CARGA_GRATIS'].sum() if 'PESO_CARGA_GRATIS' in df_filtrado.columns else 0
    
    # Exibindo os dados calculados
    st.write(f"**Distância Total Voada (KM) ✈️**: {distancia_total} km")
    st.write(f"**Total de Carga Paga (KG) 📦**: {carga_paga_total} kg")
    st.write(f"**Total de Carga Grátis (KG) 🎁**: {carga_gratis_total} kg")
    
    # Exibindo o dataframe filtrado
    st.write("Exibindo dados filtrados:")
    st.dataframe(df_filtrado)
    