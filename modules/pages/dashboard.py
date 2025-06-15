import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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

def colored_card(metric_emoji, metric_label, metric_value, bg_color):
    valor_formatado = formatar_valor(metric_value)
    st.markdown(
        f"""
        <div style='background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;'>
            <p style='margin:0; font-weight:bold; color:white; font-size:24px; min-height:50px'>
                <span style='font-size:36px;'>{metric_emoji}</span> {metric_label}
            </p>
            <p style='margin:0; font-size:36px; color:white; font-weight:bold;'>{valor_formatado}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def renderizar (df_filtrado):
    st.title("✈️ Dashboard de Aeroporto")
    st.markdown("### Análise completa do Balanço")
    st.markdown("---")

    # Cálculos
    passageiros_pagaram = int(df_filtrado['PASSAGEIROS PAGOS'].sum())
    passageiros_nao_pagaram = int(df_filtrado['PASSAGEIROS GRÁTIS'].sum())
    total_carga_paga = int(df_filtrado['CARGA PAGA (KG)'].sum())
    total_voos = len(df_filtrado)
    total_horas_voadas = int(df_filtrado['HORAS VOADAS'].sum())
    
    st.markdown('')

   # Big Numbers
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        colored_card("👥", "Total Passag. Pagantes", passageiros_pagaram, "#02413C")
    with col2:
        colored_card("🎫", "Total Passg. Não Pagantes", passageiros_nao_pagaram, "#2196F3")
    with col3:
        colored_card("📦", "Total Carga Paga", total_carga_paga, "#5B9004")
    with col4:
        colored_card("✈️", "Total de Voos", total_voos, "#9C27B0")
    with col5:
        colored_card("🕑", "Horas Voadas", total_horas_voadas, "#FF5722")

    st.markdown('<br><br>', unsafe_allow_html=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de pizza mostrando a porcentagem em comparação aos pagantes e não pagantes
        porcentagem_pagante = df_filtrado['PASSAGEIROS PAGOS'].sum()
        porcentagem_nao_pagante = df_filtrado['PASSAGEIROS GRÁTIS'].sum()

        valores = [porcentagem_pagante, porcentagem_nao_pagante]
        total = porcentagem_pagante + porcentagem_nao_pagante

        if total > 0:
            rotulos = ['Pagantes', 'Não Pagantes']
            fig, ax = plt.subplots(figsize=(8, 5))

            ax.pie(valores,
                labels=rotulos,
                autopct='%1.1f%%',
                startangle=90,
                colors=sns.color_palette("pastel"))
            ax.set_title("Distribuição por Pessoas Pagantes", pad=15, fontsize=12)

            st.pyplot(fig)
        else:
            st.warning("Não há dados para serem exibidos.")

    with col2:
        # Novo gráfico: Top 5 empresas por passageiros
        st.subheader("Top 5 Empresas por Passageiros 📊")
        
        passageiros_por_empresa = df_filtrado.groupby('EMPRESA (NOME)').agg({
            'PASSAGEIROS PAGOS': 'sum',
            'PASSAGEIROS GRÁTIS': 'sum'
        }).reset_index()
        
        passageiros_por_empresa['TOTAL_PASSAGEIROS'] = (
            passageiros_por_empresa['PASSAGEIROS PAGOS'] + 
            passageiros_por_empresa['PASSAGEIROS GRÁTIS']
        )
        
        top_empresas = passageiros_por_empresa.nlargest(5, 'TOTAL_PASSAGEIROS')
        
        if not top_empresas.empty and top_empresas['TOTAL_PASSAGEIROS'].sum() > 0:
            fig = px.bar(
                top_empresas,
                x='EMPRESA (NOME)',
                y='TOTAL_PASSAGEIROS',
                title='Top 5 Empresas por Total de Passageiros',
                labels={'EMPRESA (NOME)': 'Empresa', 'TOTAL_PASSAGEIROS': 'Total de Passageiros'},
                color='TOTAL_PASSAGEIROS',
                color_continuous_scale='Blues',
                template='plotly_white'
            )
            
            fig.update_layout(
                height=400,
                xaxis_tickangle=-45,
                title={'x': 0.5, 'xanchor': 'center'},
                margin=dict(l=40, r=40, t=60, b=100)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados para serem exibidos.")

    # Exibindo o dataframe filtrado
    if not df_filtrado.empty:
        st.markdown("<h1 style='text-align: center;'>Exibição da tabela</h1>", unsafe_allow_html=True)
        st.dataframe(df_filtrado)
    else:
        st.warning("Não há dados para serem exibidos.")