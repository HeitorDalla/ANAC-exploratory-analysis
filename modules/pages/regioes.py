import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.express as px

def renderizar(df_filtrado):
    st.title("Análise das Regiões")
    st.markdown("---")

    # Big Numbers
    coluna1, coluna2, coluna3 = st.columns(3)
    
    with coluna1:
        total_passageiros = (df_filtrado['PASSAGEIROS PAGOS'].fillna(0) + df_filtrado['PASSAGEIROS GRÁTIS'].fillna(0)).sum()
        st.metric("Total Passageiros", f"{int(total_passageiros):,}")
    
    with coluna2:
        total_voos = len(df_filtrado)
        st.metric("Total Voos", f"{total_voos:,}")
    
    with coluna3:
        regioes_count = df_filtrado['AEROPORTO DE DESTINO (REGIÃO)'].nunique()
        st.metric("Regiões Atendidas", regioes_count)

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    # Gráfico 1: Passageiros por Região
    with col1:
        st.subheader("📊 Passageiros por Região")
        
        dados_regiao = df_filtrado.groupby('AEROPORTO DE DESTINO (REGIÃO)').agg({
            'PASSAGEIROS PAGOS': 'sum',
            'PASSAGEIROS GRÁTIS': 'sum'
        }).reset_index()

        dados_regiao['TOTAL'] = dados_regiao['PASSAGEIROS PAGOS'] + dados_regiao['PASSAGEIROS GRÁTIS']

        if dados_regiao['TOTAL'].sum() == 0 or dados_regiao.empty:
            st.warning("Não há dados para serem exibidos.")
        else:
            fig1 = px.bar(dados_regiao, x='AEROPORTO DE DESTINO (REGIÃO)', y='TOTAL',
                        title='Total de Passageiros por Região')
            
            st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Distribuição de Voos por Região (Pizza)
    with col2:
        st.subheader("🥧 Distribuição de Voos por Região")
        
        voos_regiao = df_filtrado["AEROPORTO DE DESTINO (REGIÃO)"].value_counts().reset_index()
        voos_regiao.columns = ['Região', 'Voos']

        if not voos_regiao.empty:
            fig2 = px.pie(voos_regiao, values='Voos', names='Região',
                        title='Distribuição de Voos por Região')
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Não há dados para serem exibidos.")

    # Exibindo o dataframe filtrado
    if not df_filtrado.empty:
        st.markdown("<h1 style='text-align: center;'>Exibição da tabela</h1>", unsafe_allow_html=True)
        st.dataframe(df_filtrado[['AEROPORTO DE ORIGEM (SIGLA)', 'AEROPORTO DE ORIGEM (NOME)', 'AEROPORTO DE ORIGEM (UF)', 'AEROPORTO DE ORIGEM (REGIÃO)','AEROPORTO DE ORIGEM (PAÍS)', 'AEROPORTO DE ORIGEM (CONTINENTE)', 'AEROPORTO DE DESTINO (SIGLA)', 'AEROPORTO DE DESTINO (NOME)', 'AEROPORTO DE DESTINO (UF)', 'AEROPORTO DE DESTINO (REGIÃO)', 'AEROPORTO DE DESTINO (PAÍS)', 'AEROPORTO DE DESTINO (CONTINENTE)', 'NATUREZA', 'GRUPO DE VOO']])
    else:
        st.warning("Não há dados para serem exibidos.")