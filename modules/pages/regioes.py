import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk

def renderizar (df_filtrado):
    st.title("Análise das Regiões")
    st.markdown("---")

    # Big Numbers
    coluna1, coluna2, coluna3 = st.columns(3)

    

    st.markdown("---")

    # Gráfico da distribuição de passageiros por região
    df_filtrado['TOTAL_PASSAGEIROS'] = df_filtrado['PASSAGEIROS PAGOS'] + df_filtrado['PASSAGEIROS GRÁTIS']
    passageiros_regioes = df_filtrado.groupby('AEROPORTO DE ORIGEM (REGIÃO)')['TOTAL_PASSAGEIROS'].sum().reset_index()
    
    st.markdown("Distribuição de Passageiros por Região")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(passageiros_regioes['TOTAL_PASSAGEIROS'],
        labels=passageiros_regioes['AEROPORTO DE ORIGEM (REGIÃO)'],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"))
    
    ax.set_title("Distribuição por Pagantes", pad=15, fontsize=12)
    st.pyplot(fig)

    # Gráfico interativo para as regiões mais visitadas
    

    # Gráfico interativo para as regiões mais visitadas
    st.subheader("Regiões mais Visitadas")
    regioes = df_filtrado['AEROPORTO DE DESTINO (REGIÃO)'].value_counts().reset_index()
    regioes.columns = ['REGIAO', 'QUANTIDADE']

    # Coordenadas corrigidas (longitude, latitude)
    coords = {
        'Norte': [-62.2, -3.5],
        'Nordeste': [-34.9, -8.0],
        'Centro-Oeste': [-47.9, -15.8],
        'Sudeste': [-46.6, -23.5],
        'Sul': [-51.2, -30.0]
    }

    # Remover regiões não mapeadas
    regioes = regioes[regioes['REGIAO'].isin(coords.keys())]

    # Adicionar lat/lon
    regioes['longitude'] = regioes['REGIAO'].map(lambda x: coords[x][0])
    regioes['latitude'] = regioes['REGIAO'].map(lambda x: coords[x][1])

    # Criar camada
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=regioes,
        get_position='[longitude, latitude]',
        get_radius='QUANTIDADE * 5000',
        get_fill_color='[255, 140, 0]',
        pickable=True
    )

    # Exibir o mapa
    view_state = pdk.ViewState(latitude=-15.8, longitude=-47.9, zoom=4)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{REGIAO}: {QUANTIDADE}"})
    st.pydeck_chart(deck)

    # Exibindo o dataframe filtrado
    st.markdown("<h1 style='text-align: center;'>Exibição da tabela</h1>", unsafe_allow_html=True)
    colunas = ['EMPRESA (NACIONALIDADE)', 'AEROPORTO DE ORIGEM (SIGLA)', 'AEROPORTO DE ORIGEM (NOME)', 'AEROPORTO DE ORIGEM (REGIÃO)', 'AEROPORTO DE ORIGEM (PAÍS)', 'AEROPORTO DE ORIGEM (CONTINENTE)', 'AEROPORTO DE DESTINO (SIGLA)', 'AEROPORTO DE DESTINO (NOME)', 'AEROPORTO DE DESTINO (UF)', 'AEROPORTO DE DESTINO (REGIÃO)', 'AEROPORTO DE DESTINO (PAÍS)', 'AEROPORTO DE DESTINO (CONTINENTE)', 'NATUREZA', 'GRUPO DE VOO']
    st.dataframe(df_filtrado[colunas])