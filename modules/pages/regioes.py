import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.express as px

def formatar_valor(valor):
    if valor >= 2_000_000:
        return f"{valor/1_000_000:.1f} milhões"
    elif valor >= 1_000_000:
        return f"{valor/1_000_000:.1f} milhão"
    elif valor >= 2_000:
        return f"{valor/1_000:.1f} mil"
    elif valor >= 1_000:
        return f"{valor/1_000:.1f} mil"
    return str(valor)

def colored_card(metric_emoji, metric_label, metric_value, bg_color):
    valor_formatado = formatar_valor(metric_value)
    st.markdown(
        f"""
        <div style='background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;'>
            <p style='margin:0; font-weight:bold; color:white; font-size:24px; min-height:50px'>
                <span style='font-size:36px;'>{metric_emoji}</span> {metric_label}
            </p>
            <p style='margin:0; font-size:36px; color:white; font-weight:bold;'>{valor_formatado}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def renderizar(df_filtrado):
    st.title("Análise das Regiões")
    st.markdown("---")

   # Cálculos
    total_passageiros = int((df_filtrado['PASSAGEIROS PAGOS'].fillna(0) + df_filtrado['PASSAGEIROS GRÁTIS'].fillna(0)).sum())
    total_voos = len(df_filtrado)
    regioes_count = df_filtrado['AEROPORTO DE DESTINO (REGIÃO)'].nunique()

    # Big Numbers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        colored_card("👥", "Total Passageiros", total_passageiros, "#02413C")
    
    with col2:
        colored_card("✈️", "Total Voos", total_voos, "#2196F3")
    
    with col3:
        colored_card("🌍", "Regiões Atendidas", regioes_count, "#5B9004")

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