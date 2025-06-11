import streamlit as st
import pandas as pd
from modules.data import dados_tratados
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

# Filtros aplicáveis a todas as páginas
mes_unicos = st.sidebar.selectbox("Mês", sorted(dados["MÊS"].unique()))
empresa_unicas = st.sidebar.multiselect("Empresa Aérea", dados["EMPRESA (NOME)"].unique())
uf_origem_unicos = st.sidebar.multiselect("UF Origem", dados["AEROPORTO DE ORIGEM (UF)"].unique())

# Aplicar os filtros aos dados
filtro = dados.copy() # cópia do dados
if mes_unicos:
    filtro = filtro[filtro["MÊS"] == mes_unicos]
if empresa_unicas:
    filtro = filtro[filtro["EMPRESA (NOME)"].isin(empresa_unicas)]
if uf_origem_unicos:
    filtro = filtro[filtro["AEROPORTO DE ORIGEM (UF)"].isin(uf_origem_unicos)]

# ADICIONAR BOTÃO DE RESETAR TODOS OS FILTROS -----

# Navegação dentro das páginas principais
abas = st.tabs(["🏠 Visão Geral", "🗺️ Regiões", "✈️ Aeroportos", "📦 Cargas", "🔁 Rotas"])

with abas[0]:
    dashboard.renderizar(filtro, mes_unicos, empresa_unicas, uf_origem_unicos)

with abas[1]:
    regioes.renderizar(filtro, mes_unicos, empresa_unicas, uf_origem_unicos)

with abas[2]:
    aeroportos.renderizar(filtro, mes_unicos, empresa_unicas, uf_origem_unicos)

with abas[3]:
    cargas.renderizar(filtro, mes_unicos, empresa_unicas, uf_origem_unicos)

with abas[4]:
    rotas.renderizar(filtro, mes_unicos, empresa_unicas, uf_origem_unicos)