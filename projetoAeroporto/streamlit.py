import streamlit as st
import pandas as pd
from datetime import date, datetime


df = pd.read_csv("projetoAeroporto\csv\resumo_anual_2025.csv", encoding='latin-1', delimiter=';')

# C:\Users\Aluno\Desktop\projeto-final\projeto-aeroporto\projetoAeroporto\csv\resumo_anual_2025.csv
# Configurações Gerais da Página
st.set_page_config(
    page_title='',
    page_icon='',
    layout=''
)


# Página

# Header
st.title("✈️ Dashboard de Aeroporto")
st.markdown("### Análise completa do Balanço")
st.markdown("---")

# Filtros Laterais

