"""
Módulo de conexão e operações com o banco de dados SQLite
"""
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'chat.db')

@contextmanager
def get_db():
    """Context manager para conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    """
    Executa uma query no banco de dados
    
    Args:
        query: SQL query
        params: Parâmetros da query
        fetch_one: Retorna um único resultado
        fetch_all: Retorna todos os resultados
        commit: Faz commit das alterações
    
    Returns:
        Resultado da query ou None
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if commit:
            conn.commit()
            return cursor.lastrowid
        
        if fetch_one:
            return cursor.fetchone()
        
        if fetch_all:
            return cursor.fetchall()
        
        return None

def dict_from_row(row):
    """Converte sqlite3.Row para dicionário"""
    if row is None:
        return None
    return dict(zip(row.keys(), row))

