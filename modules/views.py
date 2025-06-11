import sqlite3
from modules.database import initialize_database

conn, cursor = initialize_database()

def paying_public(mes=None, empresa=None, uf=None):
    query = '''
        SELECT SUM(vc."passageiros_pagos")
        FROM voos_completos vc
        INNER JOIN empresas e ON vc.empresa_id = e.id
        WHERE 1=1
    '''
    params = []

    if mes:
        query += ' AND vc.mes = ?'
        params.append(mes)
    if empresa:
        query += f" AND e.nome IN ({','.join(['?'] * len(empresa))})"
        params.extend(empresa)
    if uf:
        query += f" AND vc.aeroporto_origem_uf IN ({','.join(['?'] * len(uf))})"
        params.extend(uf)

    cursor.execute(query, params)
    resultado = cursor.fetchone()[0]

    return resultado[0] if resultado and resultado[0] is not None else 0

def non_paying_public(mes=None, empresa=None, uf=None):
    query = '''
        SELECT SUM(vc."passageiros_gratis")
        FROM voos_completos vc
        INNER JOIN empresas e ON vc.empresa_id = e.id
        WHERE 1=1
    '''
    params = []

    if mes:
        query += ' AND vc.mes = ?'
        params.append(mes)
    if empresa:
        query += f" AND e.nome IN ({','.join(['?'] * len(empresa))})"
        params.extend(empresa)
    if uf:
        query += f" AND vc.aeroporto_origem_uf IN ({','.join(['?'] * len(uf))})"
        params.extend(uf)

    cursor.execute(query, params)
    resultado = cursor.fetchone()[0]

    return resultado[0] if resultado and resultado[0] is not None else 0

def total_carga_paga(mes=None, empresa=None, uf=None):
    query = '''
        SELECT SUM(vc."carga_paga_kg")
        FROM voos_completos vc
        INNER JOIN empresas e ON vc.empresa_id = e.id
        WHERE 1 = 1
    '''
    
    params = []
    
    if mes:
        query += ' AND vc.mes = ?'
        params.append(mes)

    if empresa:
        query += ' AND e.nome = ?'
        params.append(empresa)

    if uf:
        query += ' AND vc.aeroporto_origem_sigla = ?'
        params.append(uf)
    
    cursor.execute(query, params)
    resultado = cursor.fetchone()[0]
    
    return resultado

def distancia_total_voada(mes=None, empresa=None, uf=None):
    query = '''
        SELECT SUM(vc."carga_paga_km")
        FROM voos_completos vc
        INNER JOIN empresas e ON vc.empresa_id = e.id
        WHERE 1 = 1
    '''
    
    params = []

    if mes:
        query += ' AND vc.mes = ?'
        params.append(mes)

    if empresa:
        query += ' AND e.nome = ?'
        params.append(empresa)

    if uf:
        query += ' AND vc.aeroporto_origem_sigla = ?'
        params.append(uf)

    cursor.execute(query, params)
    resultado = cursor.fetchone()[0]
    
    return resultado

def carga_por_km(mes=None, empresa=None, uf=None):
    query = '''
        SELECT SUM(vc.carga_paga_kg) / SUM(vc.carga_paga_km)
        FROM voos_completos vc
        INNER JOIN empresas e ON vc.empresa_id = e.id
        WHERE 1 = 1
    '''
    
    params = []

    if mes:
        query += ' AND vc.mes = ?'
        params.append(mes)

    if empresa:
        query += ' AND e.nome = ?'
        params.append(empresa)

    if uf:
        query += ' AND vc.aeroporto_origem_sigla = ?'
        params.append(uf)

    cursor.execute(query, params)
    resultado = cursor.fetchone()[0]
    
    return resultado