import streamlit as st
import pydeck as pdk
import airportsdata as air

# Carrega dados ICAO automaticamente
icao_dict = air.Airport["ICAO"]



def renderizar(df_filtrado):
    rotas_com_coords = []

    icao_dict = air.load()  # chave padrão é 'ICAO'
    for _, row in df_filtrado.iterrows():
        origem = str(row["AEROPORTO DE ORIGEM (SIGLA)"]).strip().upper()
        destino = str(row["AEROPORTO DE DESTINO (SIGLA)"]).strip().upper()




        if origem in icao_dict and destino in icao_dict:
            lat_o = icao_dict[origem]["lat"]
            lon_o = icao_dict[origem]["lon"]
            lat_d = icao_dict[destino]["lat"]
            lon_d = icao_dict[destino]["lon"]
            rotas_com_coords.append({
                "origem": origem,
                "destino": destino,
                "source_position": [lon_o, lat_o],
                "target_position": [lon_d, lat_d],
                "NUM_VOOS": row.get("DECOLAGENS", 1)
            })

    if not rotas_com_coords:
        st.warning("Nenhuma rota com coordenadas conhecidas foi encontrada.")
        return

    layer = pdk.Layer(
        "ArcLayer",
        data=rotas_com_coords,
        get_source_position="source_position",
        get_target_position="target_position",
        get_source_color=[255, 140, 0],
        get_target_color=[0, 191, 255],
        get_width=1,
        pickable=True,
        auto_highlight=True,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(latitude=-15, longitude=-55, zoom=4),
        tooltip={"text": "{origem} → {destino}"}
    ))