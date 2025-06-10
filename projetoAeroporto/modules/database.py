import sqlite3
import pandas as pd

# Fazer a conexão
def getConnection ():
    conn = sqlite3.connect('projetoAeroporto')
    cursor = conn.cursor()

# Inicializar o Banco de Dados
def initialize_database ():
    conn, cursor = getConnection()
    createTables(conn, cursor)

# Criação de Tabelas
def createTables ():


# Inserção de dados
def populateTables ():

