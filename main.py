import streamlit as st
from modules.data import dados_tratados
from modules.database import initialize_database
from modules.pages import dashboard, cargas, regioes, rotas

# Configurações Gerais da Página
st.set_page_config(page_title="Dashboard ANAC", layout="wide")

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

ordem_meses = [
    "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]

# Inicializar o banco de dados
conn, cursor = initialize_database()

dados = dados_tratados()

# Streamlit
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-size: 1.5rem !important;
        padding: 1.2rem 2rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Agência Nacional de Aviação Civil")
meses_ordenados = [m for m in ordem_meses if m in dados["MÊS"].unique()]

# Filtros aplicáveis a todas as páginas
opcoes_meses = ["Todos os Meses"] + meses_ordenados
mes_selecionado = st.sidebar.selectbox("Mês", opcoes_meses)

empresa_unicas = st.sidebar.multiselect("Empresa Aérea", dados["EMPRESA (NOME)"].unique())
ufs_disponiveis = dados["AEROPORTO DE ORIGEM (UF)"].unique()
uf_origem_unicos = st.sidebar.multiselect("UF Origem", ufs_disponiveis if "PR" in ufs_disponiveis else [])

# Aplicação dos filtros
filtro = dados.copy()

if mes_selecionado != 'Todos os Meses':
    filtro = filtro[filtro["MÊS"] == mes_selecionado]
if empresa_unicas:
    filtro = filtro[filtro["EMPRESA (NOME)"].isin(empresa_unicas)]
if uf_origem_unicos:
    filtro = filtro[filtro["AEROPORTO DE ORIGEM (UF)"].isin(uf_origem_unicos)]

# Navegação dentro das páginas principais
abas = st.tabs(["🏠 Visão Geral", "🗺️ Regiões", "📦 Cargas", "🔁 Rotas"])

with abas[0]:
    dashboard.renderizar(filtro)

with abas[1]:
    regioes.renderizar(filtro)

with abas[2]:
    cargas.renderizar(filtro)

with abas[3]:
    rotas.renderizar(filtro)