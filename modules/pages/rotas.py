import streamlit as st
import pydeck as pdk
import airportsdata as air
import plotly.express as px
import numpy as np

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-size: 1.5rem !important;
        padding: 1.2rem 2rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Componente visual de destaque com cor personalizada
def colored_card(metric_emoji, metric_label,metric_value, metric_type ,bg_color):
    valor_formatado = formatar_valor(metric_value)
    st.markdown(
        f"""
        <div style='background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;'>
            <p style='margin:0; font-weight:bold; color:white; font-size:24px; min-height:50px'>
                <span style='font-size:36px;'>{metric_emoji}</span> {metric_label}
            </p>
            <p style='margin:0; font-size:36px; color:white; font-weight:bold;'>{valor_formatado} {metric_type}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para formatar grandes números
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



# Gráfico de pizza nacional/internacional
def grafico_rotas_nacionais_internacionais(df):
    df["TIPO ROTA"] = df["AEROPORTO DE DESTINO (PAÍS)"].apply(
        lambda x: "Nacional" if str(x).strip().upper() == "BRASIL" else "Internacional"
    )
    resumo = df["TIPO ROTA"].value_counts().reset_index()
    resumo.columns = ["Tipo", "Total"]

    fig = px.pie(
        resumo,
        names="Tipo",
        values="Total",
        color_discrete_sequence=["#00796B", "#FBC02D"],
        title="Rotas Internacionais vs Nacionais"
    )
    fig.update_layout(
        width=700,
        height=500,
        font=dict(size=16),
        title=dict(font=dict(size=22), x=0.5),
        margin=dict(t=50, b=20, l=20, r=20)
    )
    fig.update_traces(textinfo="percent+label", pull=[0.04, 0.04])
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersão passageiros vs distância
def grafico_dispercao_passageiros_distancia(df):
    rotas = df.groupby([
        "AEROPORTO DE ORIGEM (SIGLA)", "AEROPORTO DE DESTINO (SIGLA)"
    ]).agg({
        "DISTÂNCIA VOADA (KM)": "sum",
        "PASSAGEIROS PAGOS": "sum",
        "DECOLAGENS": "sum"
    }).reset_index()

    rotas["ROTA"] = rotas["AEROPORTO DE ORIGEM (SIGLA)"] + " → " + rotas["AEROPORTO DE DESTINO (SIGLA)"]

    fig = px.scatter(
        rotas,
        x="DISTÂNCIA VOADA (KM)",
        y="PASSAGEIROS PAGOS",
        size="DECOLAGENS",
        hover_name="ROTA",
        title="Passageiros vs Distância por Rota",
        labels={
            "DISTÂNCIA VOADA (KM)": "Distância (KM)",
            "PASSAGEIROS PAGOS": "Passageiros"
        },
        template="plotly_white",
        color_discrete_sequence=["#0288D1"]
    )
    fig.update_layout(margin=dict(t=50, b=20, l=10, r=10))
    fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color='DarkSlateGrey')))
    st.plotly_chart(fig, use_container_width=True)

# Página principal de renderização
def renderizar(df_filtrado):
    st.markdown("""
        <h1 style='text-align:center; margin-bottom:10px;'>✈️ Análise de Rotas Aéreas</h1>
        <p style='text-align:center; font-size:18px;'>Resumo interativo de voos, passageiros e trajetos nacionais/internacionais</p>
    """, unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("Nenhum dado disponível para a seleção atual.")
        return

    total_rotas_unicas = df_filtrado.groupby([
        "AEROPORTO DE ORIGEM (SIGLA)", "AEROPORTO DE DESTINO (SIGLA)"
    ]).ngroups
    total_decolagens = int(df_filtrado["DECOLAGENS"].sum())

    passageiros_por_rota = df_filtrado.groupby([
        "AEROPORTO DE ORIGEM (SIGLA)", "AEROPORTO DE DESTINO (SIGLA)"
    ])["PASSAGEIROS PAGOS"].sum()
    media_passageiros_por_rota = passageiros_por_rota.mean() or 0

    distancia_mais_longa = 0
    if not df_filtrado.empty:
        rota_longa_df = df_filtrado.groupby([
            "AEROPORTO DE ORIGEM (SIGLA)", "AEROPORTO DE DESTINO (SIGLA)"
        ])["DISTÂNCIA VOADA (KM)"].sum().reset_index()

        if not rota_longa_df.empty:
            rota_longa = rota_longa_df.sort_values(by="DISTÂNCIA VOADA (KM)", ascending=False).iloc[0]
            distancia_mais_longa = int(rota_longa["DISTÂNCIA VOADA (KM)"])

    total_horas_voadas = int(df_filtrado["HORAS VOADAS"].sum())

    aba = st.tabs(["📊 Indicadores", "📈 Gráficos"])

    with aba[0]:
        st.markdown("### 📊 Indicadores de Desempenho de Rotas")
        col1, col2, col3 = st.columns(3)
        with col1:
            colored_card("🔁", "Rotas Únicas", total_rotas_unicas, "", "#294273")
        with col2:
            colored_card("✈️", "Total de Decolagens", total_decolagens, "", "#26658C")
        with col3:
            colored_card("📐", "Média Passageiros/Rota", int(media_passageiros_por_rota), "", "#307322")

        st.markdown('')

        col4, col5 = st.columns(2)
        with col4:
            colored_card("🛬", "Rota Mais Longa (km)", distancia_mais_longa, "", "#468C5F")
        with col5:
            colored_card("⏱️", "Horas Totais Voada", total_horas_voadas, "", "#D9A714")

    with aba[1]:
        grafico_rotas_nacionais_internacionais(df_filtrado)

    st.markdown('<br><br>', unsafe_allow_html=True)

    st.markdown("## 🌐 Mapa de Rotas com Coordenadas")
    icao_dict = air.load()
    rotas_com_coords = []

    for _, row in df_filtrado.iterrows():
        origem = str(row["AEROPORTO DE ORIGEM (SIGLA)"]).strip().upper()
        destino = str(row["AEROPORTO DE DESTINO (SIGLA)"]).strip().upper()

        if origem in icao_dict and destino in icao_dict:
            lat_o = icao_dict[origem]["lat"]
            lon_o = icao_dict[origem]["lon"]
            lat_d = icao_dict[destino]["lat"]
            lon_d = icao_dict[destino]["lon"]
            num_voos = row.get("DECOLAGENS", 1)
            origem_nome = row.get("AEROPORTO DE ORIGEM (NOME)", "")
            destino_nome = row.get("AEROPORTO DE DESTINO (NOME)", "")

            rotas_com_coords.append({
                "origem": origem,
                "destino": destino,
                "origem_nome": origem_nome,
                "destino_nome": destino_nome,
                "source_position": [lon_o, lat_o],
                "target_position": [lon_d, lat_d],
                "NUM_VOOS": num_voos
            })

    if not rotas_com_coords:
        st.warning("Nenhuma rota com coordenadas conhecidas foi encontrada.")
        return

    max_voos = max(r["NUM_VOOS"] for r in rotas_com_coords)
    for r in rotas_com_coords:
        r["WIDTH"] = np.interp(r["NUM_VOOS"], [0, max_voos], [1, 6])

    layer = pdk.Layer(
        "ArcLayer",
        data=rotas_com_coords,
        get_source_position="source_position",
        get_target_position="target_position",
        get_source_color=[255, 87, 34],
        get_target_color=[0, 188, 212],
        get_width="WIDTH",
        pickable=True,
        auto_highlight=True,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(latitude=-14.235, longitude=-51.9253, zoom=4),
        tooltip={
            "html": "<b>🛫 {origem_nome}</b><br>→<br><b>🛬 {destino_nome}</b>",
            "style": {"color": "white"}
        },
        map_style="dark"
    ))