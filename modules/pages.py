import streamlit as st

def dashboard(df):
    st.title("✈️ Dashboard de Aeroporto")
    st.markdown("### Análise completa do Balanço")
    st.markdown("---")

    # Big Numbers
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)

    with coluna1:
        passageiros_pagaram = df['PASSAGEIROS PAGOS'].sum()
        st.metric("Total Passag. Pagantes", passageiros_pagaram) 

    with coluna2:
        passageiros_nao_pagaram = df['PASSAGEIROS GRÁTIS'].sum()
        st.metric("Total Passg. Não Pagantes", passageiros_nao_pagaram)

    with coluna3:
        total_carga_paga = df['CARGA PAGA (KG)'].sum()
        st.metric("Total Carga Paga", total_carga_paga)

    st.markdown("---")

    # Gráficos

def graficos(df):
    pass