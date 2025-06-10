import sqlite3
import pandas as pd

# Função para fazer a conexão com o banco
def getConnection():
    conn = sqlite3.connect('banco_de_dados.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    return conn, cursor

# Criação das tabelas no banco
def createTables(conn, cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla TEXT UNIQUE,
        nome TEXT,
        nacionalidade TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS voos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa_id INTEGER,
        ano INTEGER,
        mes INTEGER,
        aeroporto_origem_sigla TEXT,
        aeroporto_origem_nome TEXT,
        aeroporto_destino_nome TEXT,
        natureza TEXT,
        FOREIGN KEY (empresa_id) REFERENCES empresas(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS desempenho_voos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voo_id INTEGER,
        passageiros_pagos INTEGER,
        passageiros_gratis INTEGER,
        carga_paga_kg INTEGER,
        ask REAL,
        rpk REAL,
        atk REAL,
        rtk REAL,
        distancia_voada_km REAL,
        decolagens REAL,
        correio_km REAL,
        horas_voadas REAL,
        FOREIGN KEY (voo_id) REFERENCES voos(id)
    )
    ''')

    conn.commit()

def populate_tables(conn, cursor):
    # Popula a tabela 'empresas' se não houver dados nela
    cursor.execute("SELECT COUNT(*) FROM empresas")
    if cursor.fetchone()[0] == 0: 
        df_empresas = pd.read_csv('csv/empresas.csv')
        df_empresas.columns = ['sigla', 'nome', 'nacionalidade']
        df_empresas.to_sql('empresas', conn, if_exists='append', index=False)

    # Popula a tabela 'voos' se não houver dados nela
    cursor.execute("SELECT COUNT(*) FROM voos")
    if cursor.fetchone()[0] == 0:
        df_voos = pd.read_csv('csv/voos.csv')
        df_voos.rename(columns={'MÊS': 'mes'}, inplace=True)
        df_voos.rename(columns={'AEROPORTO DE ORIGEM (SIGLA)': 'aeroporto_origem_sigla'}, inplace=True)
        df_voos.rename(columns={'AEROPORTO DE ORIGEM (NOME)': 'aeroporto_origem_nome'}, inplace=True)
        df_voos.rename(columns={'AEROPORTO DE DESTINO (NOME)': 'aeroporto_destino_nome'}, inplace=True)
        df_voos.to_sql('voos', conn, if_exists='append', index=False)

    # Popula a tabela 'desempenho_voos' se não houver dados nela
    cursor.execute("SELECT COUNT(*) FROM desempenho_voos")
    if cursor.fetchone()[0] == 0:
        df_desempenho_voos = pd.read_csv('csv/desempenho_voos.csv')
        df_desempenho_voos.rename(columns={'PASSAGEIROS GRÁTIS': 'passageiros_gratis'}, inplace=True)
        df_desempenho_voos.rename(columns={'CARGA PAGA (KG)': 'carga_paga_kg'}, inplace=True)
        df_desempenho_voos.rename(columns={'DISTÂNCIA VOADA (KM)': 'distancia_voada_km'}, inplace=True)
        df_desempenho_voos.rename(columns={'CORREIO KM': 'correio_km'}, inplace=True)
        df_desempenho_voos.rename(columns={'HORAS VOADAS': 'horas_voadas'}, inplace=True)
        df_desempenho_voos.rename(columns={'PASSAGEIROS PAGOS': 'passageiros_pagos'}, inplace=True)
        df_desempenho_voos.to_sql('desempenho_voos', conn, if_exists='append', index=False)
        
    conn.commit()

# Função para inicializar o banco de dados
def initialize_database():
    conn, cursor = getConnection()
    createTables(conn, cursor)
    populate_tables(conn, cursor)

    return conn, cursor