import sqlite3
import streamlit as st
from modules.database import initialize_database

conn, cursor = initialize_database()

# Queries para o Dashboard Principal
def paying_public (mes=None, empresa=None, uf=None):   
    query = '''
        SELECT SUM(vc.PASSAGEIROS PAGOS)
        FROM voos_completos vc
        INNER JOIN empresas e ON vc.empresa_id = e.id
        WHERE 1 = 1 
    '''

    params = []

    if mes:
        query += ' AND vc.mes = ?'
        params.append(mes)

    if empresa:
        query += ' AND vc.EMPRESA (NOME) = ?'
        params.append(empresa)

    if uf:
        query += ' AND vc.AEROPORTO DE ORIGEM (UF) = ?'
        params.append(uf)

    cursor.execute(query, params)
    resultado = cursor.fetchone()[0]

    return resultado

def non_paying_public ():
    pass