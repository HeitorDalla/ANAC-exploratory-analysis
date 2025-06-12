import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk

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

    # Gráfico da distribuição de passageiros por região
    df_filtrado['TOTAL_PASSAGEIROS'] = df_filtrado['PASSAGEIROS PAGOS'].fillna(0) + df_filtrado['PASSAGEIROS GRÁTIS'].fillna(0)
    passageiros_regioes = df_filtrado.groupby('AEROPORTO DE DESTINO (REGIÃO)')['TOTAL_PASSAGEIROS'].sum().reset_index()
    
    # Remover valores NaN e zeros
    passageiros_regioes = passageiros_regioes.dropna()
    passageiros_regioes = passageiros_regioes[passageiros_regioes['TOTAL_PASSAGEIROS'] > 0]
    
    st.markdown("Distribuição de Passageiros por Região")

    if len(passageiros_regioes) > 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(passageiros_regioes['TOTAL_PASSAGEIROS'],
            labels=passageiros_regioes['AEROPORTO DE DESTINO (REGIÃO)'],
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette("pastel"))
        
        ax.set_title("Densidade de Passageiros por Região", pad=15, fontsize=12)
        st.pyplot(fig)
    else:
        st.warning("Não há dados para serem exibidos.")

    # Mapa de densidade de passageiros por região
    st.subheader("Densidade de Passageiros por Região")
    
    # Coordenadas corrigidas (longitude, latitude)
    coords = {
        'Norte': [-62.2, -3.5],
        'Nordeste': [-34.9, -8.0],
        'Centro-Oeste': [-47.9, -15.8],
        'Sudeste': [-46.6, -23.5],
        'Sul': [-51.2, -30.0]
    }

    # Usar dados de passageiros ao invés de contagem de voos
    densidade_regioes = passageiros_regioes.copy()
    densidade_regioes.columns = ['REGIAO', 'TOTAL_PASSAGEIROS']
    
    # Remover regiões não mapeadas
    densidade_regioes = densidade_regioes[densidade_regioes['REGIAO'].isin(coords.keys())]

    # Adicionar lat/lon
    densidade_regioes['longitude'] = densidade_regioes['REGIAO'].map(lambda x: coords[x][0])
    densidade_regioes['latitude'] = densidade_regioes['REGIAO'].map(lambda x: coords[x][1])

    # Normalizar o raio baseado no número de passageiros
    max_passageiros = densidade_regioes['TOTAL_PASSAGEIROS'].max()
    densidade_regioes['radius'] = (densidade_regioes['TOTAL_PASSAGEIROS'] / max_passageiros) * 100000 + 20000

    # Criar camada com cores baseadas na densidade
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=densidade_regioes,
        get_position='[longitude, latitude]',
        get_radius='radius',
        get_fill_color='[255, 140, 0, 180]',
        pickable=True
    )

    # Exibir o mapa
    view_state = pdk.ViewState(latitude=-15.8, longitude=-47.9, zoom=4)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, 
                   tooltip={"text": "Região: {REGIAO}\nPassageiros: {TOTAL_PASSAGEIROS:,}"})
    st.pydeck_chart(deck)

    # Exibindo o dataframe filtrado
    st.markdown("<h1 style='text-align: center;'>Exibição da tabela</h1>", unsafe_allow_html=True)
    colunas = ['EMPRESA (NACIONALIDADE)', 'AEROPORTO DE ORIGEM (SIGLA)', 'AEROPORTO DE ORIGEM (NOME)', 'AEROPORTO DE ORIGEM (REGIÃO)', 'AEROPORTO DE ORIGEM (PAÍS)', 'AEROPORTO DE ORIGEM (CONTINENTE)', 'AEROPORTO DE DESTINO (SIGLA)', 'AEROPORTO DE DESTINO (NOME)', 'AEROPORTO DE DESTINO (UF)', 'AEROPORTO DE DESTINO (REGIÃO)', 'AEROPORTO DE DESTINO (PAÍS)', 'AEROPORTO DE DESTINO (CONTINENTE)', 'NATUREZA', 'GRUPO DE VOO']
    st.dataframe(df_filtrado[colunas])