import streamlit as st
import pandas as pd
import plotly.express as px

def colored_card(metric_emoji, metric_label, metric_value, bg_color):
    st.markdown(
        f"""
        <div style='background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;'>
            <p style='margin:0; font-weight:bold; color:white; font-size:24px; min-height:50px'>
                <span style='font-size:36px;'>{metric_emoji}</span> {metric_label}
            </p>
            <p style='margin:0; font-size:36px; color:white; font-weight:bold;'>{metric_value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def renderizar(df_filtrado):

    st.markdown("<h1 style='text-align: center;'>📦 Análise de Cargas</h1>", unsafe_allow_html=True)
    
    # Cálculos
    distancia_total = df_filtrado['DISTÂNCIA VOADA (KM)'].sum() if 'DISTÂNCIA VOADA (KM)' in df_filtrado.columns else 0
    carga_paga_total = df_filtrado['CARGA PAGA (KG)'].sum() if 'CARGA PAGA (KG)' in df_filtrado.columns else 0
    carga_gratis_total = df_filtrado['CARGA GRÁTIS (KG)'].sum() if 'CARGA GRÁTIS (KG)' in df_filtrado.columns else 0
    carga_paga_km_total = df_filtrado['CARGA PAGA KM'].sum() if 'CARGA PAGA KM' in df_filtrado.columns else 0
    
    st.markdown('')

    # Exibindo os dados calculados
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        colored_card("📦", "Total Cargas Pagas", carga_paga_total, "#4CAF50")
    with col2:
        colored_card("🚚", "Cargas Pagas Corridas", carga_paga_km_total, "#9C27B0")
    with col3:
        colored_card("✈️", "Distância Total Voadas", distancia_total, "#FF9800")
    with col4:
        colored_card("🎁", "Total Cargas Gratis", carga_gratis_total, "#2196F3")

    st.markdown('')
         
    # Gráfico interativo para as Top 10 ou Top 5 companhias aéreas
    st.subheader("Top Companhias Aéreas com Mais Cargas Pagas (KG) 📊")

    # Agrupar por companhia aérea e somar o peso das cargas pagas
    carga_por_empresa = df_filtrado.groupby('EMPRESA (NOME)')['CARGA PAGA (KG)'].sum().sort_values(ascending=False)

    if carga_por_empresa.empty or carga_por_empresa.sum() == 0:
        st.warning("Não há dados para serem exibidos.")
    else:
        # Opção para escolher entre Top 5 e Top 10
        top_n = st.selectbox("Selecione o número de Top Empresas", [5, 10], index=1)
        
        # Selecionando os Top N
        carga_top = carga_por_empresa.head(top_n).reset_index()

        # Criando o gráfico com Plotly
        fig = px.bar(
            carga_top,
            x='EMPRESA (NOME)', 
            y='CARGA PAGA (KG)',
            title=f'Top {top_n} Companhias Aéreas com Mais Cargas Pagas (KG)',
            labels={'EMPRESA (NOME)': 'Companhia Aérea', 'CARGA PAGA (KG)': 'Carga Paga (KG)'},
            color='CARGA PAGA (KG)',
            color_continuous_scale='Viridis',
            text='CARGA PAGA (KG)',
            template='plotly_dark'
        )
        
        # Melhorando os rótulos e a formatação
        fig.update_layout(
            height=500,
            width=2000,
            title={
                'text': f'Top {top_n} Companhias Aéreas com Mais Cargas Pagas (KG)',
                'font': {'size': 24, 'family': 'Arial, sans-serif'},
                'x': 0.5,
                'xanchor': 'center',
            },
            yaxis_title={
                'text': 'Carga Paga (KG)',
                'font': {'size': 18, 'family': 'Arial, sans-serif'},
            },
            xaxis_tickangle=-45,
            xaxis={'tickmode': 'array', 'tickvals': carga_top['EMPRESA (NOME)']},
            yaxis={'tickformat': ',.0f'},
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=100)
        )
        
        # Exibindo o gráfico
        st.plotly_chart(fig)

    # Exibindo o dataframe filtrado
    st.markdown("<h1 style='text-align: center;'>Exibição da tabela</h1>", unsafe_allow_html=True)
    st.dataframe(df_filtrado[['ANO', 'MÊS', 'EMPRESA (NOME)','EMPRESA (SIGLA)', 'DISTÂNCIA VOADA (KM)','HORAS VOADAS' ,'CARGA PAGA (KG)', 'CARGA GRÁTIS (KG)',]])