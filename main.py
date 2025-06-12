import streamlit as st
import pandas as pd
from modules.data import dados_tratados, ordem_meses
from modules.database import initialize_database
from modules.pages import dashboard, cargas, aeroportos, regioes, rotas

# Inicializar o banco de dados
conn, cursor = initialize_database()

dados = dados_tratados()

# Streamlit

# Configurações Gerais da Página
st.set_page_config(page_title="Dashboard ANAC", layout="wide")

# Sidebar - Filtros Globais
# st.sidebar.image("img/logo_anac.png", width=180)
st.sidebar.markdown("### Agência Nacional de Aviação Civil")
meses_ordenados = [m for m in ordem_meses if m in dados["MÊS"].unique()]
# Filtros aplicáveis a todas as páginas
mes_unicos = st.sidebar.selectbox("Mês", meses_ordenados)
empresa_unicas = st.sidebar.multiselect("Empresa Aérea", dados["EMPRESA (NOME)"].unique())
uf_origem_unicos = st.sidebar.multiselect("UF Origem", dados["AEROPORTO DE ORIGEM (UF)"].unique())

filtro = dados.copy()
if mes_unicos:
    filtro = filtro[filtro["MÊS"] == mes_unicos]
if empresa_unicas:
    filtro = filtro[filtro["EMPRESA (NOME)"].isin(empresa_unicas)]
if uf_origem_unicos:
    filtro = filtro[filtro["AEROPORTO DE ORIGEM (UF)"].isin(uf_origem_unicos)]
# ADICIONAR BOTÃO DE RESETAR TODOS OS FILTROS -----

# Navegação dentro das páginas principais
abas = st.tabs(["🏠 Visão Geral", "🗺️ Regiões", "✈️ Aeroportos", "📦 Cargas", "🔁 Rotas"])

with abas[1]:
    regioes.renderizar(filtro)

with abas[2]:
    aeroportos.renderizar(filtro)

with abas[3]:
    cargas.renderizar(filtro)

with abas[4]:
    rotas.renderizar(filtro)