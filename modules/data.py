import pandas as pd

# Função para tratar os dados do CSV
def dados_tratados():
    meses = {
        1: "JANEIRO",
        2: "FEVEREIRO",
        3: "MARÇO",
        4: "ABRIL",
        5: "MAIO",
        6: "JUNHO",
        7: "JULHO",
        8: "AGOSTO",
        9: "SETEMBRO",
        10: "OUTUBRO",
        11: "NOVEMBRO",
        12: "DEZEMBRO"
    }
    
    df = pd.read_csv("csv/resumo_anual_2025.csv", delimiter=';', encoding='latin-1')

    df['HORAS VOADAS'] = df['HORAS VOADAS'].str.replace(',', '.', regex=False)
    df['HORAS VOADAS'] = pd.to_numeric(df['HORAS VOADAS'], errors='coerce')
    df['ANO'] = df['ANO'].astype(str)

    df = df.where(pd.notnull(df), None) # para compatibilidade com o sqlite
    df["MÊS"] = df["MÊS"].map(meses)

    return df