import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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
    st.markdown("""
        <h1 style='text-align:center; margin-bottom:10px;'>✈️ Dashboard de Aeroporto</h1>
        <p style='text-align:center; font-size:18px;'>Análise completa do Balanço</p>
    """, unsafe_allow_html=True)

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
        st.markdown("### 🥧 Distribuição de Passageiros: Pagantes vs Não Pagantes")
        
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
                colors=['#02413C', '#2196F3'])
            ax.set_title("Distribuição por Tipo de Passageiro", pad=15, fontsize=14, fontweight='bold')

            st.pyplot(fig)
        else:
            st.warning("Não há dados para serem exibidos.")

    with col2:
        st.markdown("### 🏆 Top 5 Empresas por Total de Passageiros")
        
        # Gráfico de barras simples: Top 5 empresas
        top_empresas = df_filtrado.groupby('EMPRESA (NOME)').agg({
            'PASSAGEIROS PAGOS': 'sum',
            'PASSAGEIROS GRÁTIS': 'sum'
        }).reset_index()
        
        top_empresas['TOTAL_PASSAGEIROS'] = (
            top_empresas['PASSAGEIROS PAGOS'] + top_empresas['PASSAGEIROS GRÁTIS']
        )
        
        # Pegar apenas top 5
        top_empresas = top_empresas.nlargest(5, 'TOTAL_PASSAGEIROS')
        
        if not top_empresas.empty and top_empresas['TOTAL_PASSAGEIROS'].sum() > 0:
            # Criar gráfico de barras simples com gradiente de cores
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            bars = ax.bar(
                range(len(top_empresas)), 
                top_empresas['TOTAL_PASSAGEIROS'],
                color=cores[:len(top_empresas)],
                edgecolor='white',
                linewidth=2
            )
            
            # Adicionar valores nas barras
            for i, (bar, valor) in enumerate(zip(bars, top_empresas['TOTAL_PASSAGEIROS'])):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{formatar_valor(valor)}',
                       ha='center', va='bottom', fontweight='bold', fontsize=11)
            
            # Personalizar o gráfico
            ax.set_xlabel('Empresas', fontweight='bold', fontsize=12)
            ax.set_ylabel('Total de Passageiros', fontweight='bold', fontsize=12)
            ax.set_title('Ranking das 5 Maiores Empresas', fontweight='bold', fontsize=14, pad=20)
            
            # Configurar eixo X com nomes das empresas
            empresa_names = [nome[:15] + '...' if len(nome) > 15 else nome 
                           for nome in top_empresas['EMPRESA (NOME)']]
            ax.set_xticks(range(len(top_empresas)))
            ax.set_xticklabels(empresa_names, rotation=45, ha='right')
            
            # Remover bordas superiores e direitas
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Adicionar grid sutil
            ax.grid(True, linestyle='--', alpha=0.3, axis='y')
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Não há dados para serem exibidos.")

    # Exibindo o dataframe filtrado
    if not df_filtrado.empty:
        st.markdown("<h1 style='text-align: center;'>📋 Tabela de Dados Filtrados</h1>", unsafe_allow_html=True)
        st.dataframe(df_filtrado)
    else:
        st.warning("Não há dados para serem exibidos.")