import sqlite3
import pandas as pd
from modules.data import dados_tratados

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
        nome TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS voos_completos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa_id INTEGER,
        ano INTEGER,
        mes INTEGER,
        aeroporto_origem_sigla TEXT,
        passageiros_pagos INTEGER,
        passageiros_gratis INTEGER,
        carga_paga_kg REAL,
        horas_voadas REAL,
        carga_paga_km REAL,
        rpk REAL,
        atk REAL,
        rtk REAL,
        FOREIGN KEY (empresa_id) REFERENCES empresas(id)
    )
    ''')
    
    conn.commit()

def populate_tables(conn, cursor):
    cursor.execute("SELECT COUNT(*) FROM voos_completos")
    if cursor.fetchone()[0] > 0:
        return
    
    dados = dados_tratados()

    # Inserir empresas únicas
    empresas_unicas = dados[['EMPRESA (SIGLA)', 'EMPRESA (NOME)']].drop_duplicates()
    
    for _, empresa in empresas_unicas.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO empresas (sigla, nome) 
            VALUES (?, ?)
        ''', (empresa['EMPRESA (SIGLA)'], empresa['EMPRESA (NOME)']))
    
    # Inserir dados de voos
    for _, row in dados.iterrows():
        # Buscar ID da empresa
        cursor.execute('SELECT id FROM empresas WHERE sigla = ?', (row['EMPRESA (SIGLA)'],))
        empresa_id = cursor.fetchone()[0]
        
        # Converter valores para tipos apropriados
        passageiros_pagos = int(row['PASSAGEIROS PAGOS']) if pd.notna(row['PASSAGEIROS PAGOS']) else 0
        passageiros_gratis = int(row['PASSAGEIROS GRÁTIS']) if pd.notna(row['PASSAGEIROS GRÁTIS']) else 0
        carga_paga_kg = float(row['CARGA PAGA (KG)']) if pd.notna(row['CARGA PAGA (KG)']) else 0.0
        horas_voadas = float(row['HORAS VOADAS']) if pd.notna(row['HORAS VOADAS']) else 0.0
        carga_paga_km = int(row['CARGA PAGA KM']) if pd.notna(row['CARGA PAGA KM']) else 0.0
        rpk = int(row['RPK']) if pd.notna(row['RPK']) else 0.0
        atk = int(row['ATK']) if pd.notna(row['ATK']) else 0.0
        rtk = int(row['RTK']) if pd.notna(row['RTK']) else 0.0
        
        cursor.execute('''
            INSERT INTO voos_completos 
            (empresa_id, ano, mes, aeroporto_origem_sigla, passageiros_pagos, 
             passageiros_gratis, carga_paga_kg, horas_voadas, carga_paga_km, rpk, atk, rtk)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            empresa_id,
            int(row['ANO']),
            int(row['MÊS']),
            row['AEROPORTO DE ORIGEM (SIGLA)'],
            passageiros_pagos,
            passageiros_gratis,
            carga_paga_kg,
            horas_voadas,
            carga_paga_km,
            rpk,
            atk,
            rtk
        ))
    
    conn.commit()

# Função para inicializar o banco de dados
def initialize_database():
    conn, cursor = getConnection()
    createTables(conn, cursor)
    populate_tables(conn, cursor)

    return conn, cursor
