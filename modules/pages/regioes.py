import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def renderizar (df_filtrado):
    st.title("Análise das Regiões")
    st.markdown("---")

    # Big Numbers
    coluna1, coluna2, coluna3 = st.columns(3)

    

    st.markdown("---")

    # Gráfico da distribuição de passageiros por região
    df_filtrado['TOTAL_PASSAGEIROS'] = df_filtrado['PASSAGEIROS PAGOS'] + df_filtrado['PASSAGEIROS GRÁTIS']
    passageiros_regioes = df_filtrado.groupby('AEROPORTO DE ORIGEM (REGIÃO)')['TOTAL_PASSAGEIROS'].sum().reset_index()
    
    st.markdown("Distribuiçõa de Passageiros por Região")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(passageiros_regioes['TOTAL_PASSAGEIROS'],
        labels=passageiros_regioes['AEROPORTO DE ORIGEM (REGIÃO)'],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"))
    
    ax.set_title("Distribuição por Pagantes", pad=15, fontsize=12)
    
    st.pyplot(fig)