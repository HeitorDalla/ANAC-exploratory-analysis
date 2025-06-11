import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from modules.views import paying_public, non_paying_public

def renderizar (df_filtrado):
    st.title("✈️ Dashboard de Aeroporto")
    st.markdown("### Análise completa do Balanço")
    st.markdown("---")

    # Big Numbers
    coluna1, coluna2, coluna3 = st.columns(3)

    with coluna1:
        passageiros_pagaram = df_filtrado['PASSAGEIROS PAGOS'].sum()
        st.metric("Total Passag. Pagantes", passageiros_pagaram) 

    with coluna2:
        passageiros_nao_pagaram = df_filtrado['PASSAGEIROS GRÁTIS'].sum()
        st.metric("Total Passg. Não Pagantes", passageiros_nao_pagaram)

    with coluna3:
        total_carga_paga = df_filtrado['CARGA PAGA (KG)'].sum()
        st.metric("Total Carga Paga", total_carga_paga)

    st.markdown("---")

    # Gráficos

    # Gráfico de pizza mostrando a porcentagem em comparação aos pagantes e não pagantes
    porcentagem_pagante = paying_public()
    porcentagem_nao_pagante = non_paying_public()

    valores = [porcentagem_pagante, porcentagem_nao_pagante]
    rotulos = ['Pagantes', 'Não Pagantes']

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(valores,
           labels=rotulos,
           autopct='%1.1f%%',
           startangle=90,
           colors=sns.color_palette("pastel")
    )

    ax.set_title("Distribuiçõa por Pagantes", pad=15, fontsize=12)
    st.pyplot(fig)