import pandas as pd

# Função para tratar os dados do CSV
def dados_tratados():
    df = pd.read_csv("csv/resumo_anual_2025.csv", delimiter=';', encoding='latin-1')

    df['HORAS VOADAS'] = df['HORAS VOADAS'].str.replace(',', '.', regex=False)
    df['HORAS VOADAS'] = pd.to_numeric(df['HORAS VOADAS'], errors='coerce')

    df = df.where(pd.notnull(df), None) # para compatibilidade com o sqlite

    return df