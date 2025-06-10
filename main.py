import streamlit as st
import pandas as pd
from modules.database import initialize_database, dados_tratados
from modules.pages import dashboard, graficos

# Configurações Gerais da Página
st.set_page_config(page_title="Dashboard ANAC", layout="wide")

# Inicializar o banco de dados
conn, cursor = initialize_database()

# Página Principal
# Sidebar
st.sidebar.title("🔧 Filtros")
st.sidebar.markdown("## Personalize a sua Análise")

st.sidebar.markdown("#### Período")

with st.sidebar:
    ano_selecionado = st.selectbox(
        'Selecione o ano:',
        options = [2020, 2021, 2022, 2023, 2024, 2025],
        index = 0
    )

    if "menu_ativo" not in st.session_state:
        st.session_state.menu_ativo = "Dashboard"

    if st.sidebar.button("Dashboard", type='tertiary'):
        st.session_state.menu_ativo = "Dashboard"
        
    if st.sidebar.button("Dados Estatisticos", type='tertiary'):
        st.session_state.menu_ativo = "Dados Estatisticos"

    menu = st.session_state.menu_ativo

# Página Principal
dados = dados_tratados()

if menu == "Dashboard":
    dashboard(dados)
elif menu == "Dados Estatisticos":
    graficos(dados) 