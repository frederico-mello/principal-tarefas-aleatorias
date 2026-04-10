#!/usr/bin/env python3
"""
Script para criar o banco de dados SQLite com todos os dados.
Execute: python inicializar_banco.py

Para clonar o repositório e criar o banco localmente:
1. Clone o repositório
2. Execute: python inicializar_banco.py
3. O banco listas.db será criado automaticamente
"""

import sqlite3
import json
import os

# Schema do banco de dados
SCHEMAS = {
    "categorias": """
        CREATE TABLE categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT
        )
    """,
    "listas": """
        CREATE TABLE listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            UNIQUE(categoria_id, descricao)
        )
    """,
    "dicionarios": """
        CREATE TABLE dicionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            valor REAL,
            CONSTRAINT FK_dicionarios_categorias FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """,
    "itens_sorteados": """
        CREATE TABLE itens_sorteados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            categoria TEXT NOT NULL,
            data_sorteio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
}

def main():
    # Usa nome diferente para evitar conflito com banco em uso
    banco_destino = 'listas.db'
    if os.path.exists(banco_destino):
        os.remove(banco_destino)
        print(f"Banco '{banco_destino}' antigo removido.")
    
    # Carrega dados do JSON
    print("Carregando dados do arquivo JSON...")
    with open('dados.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Cria banco e tabelas
    conn = sqlite3.connect(banco_destino)
    cursor = conn.cursor()
    
    print("Criando tabelas...")
    for tabela, schema in SCHEMAS.items():
        cursor.execute(schema)
        print(f"  - Tabela '{tabela}' criada")
    
    # Insere dados em cada tabela
    print("Inserindo dados...")
    for tabela_json, info in dados.items():
        # Normaliza nome da tabela para minúsculas
        tabela = tabela_json.lower()
        colunas = info['colunas']
        registros = info['dados']
        
        placeholders = ', '.join(['?'] * len(colunas))
        colunas_str = ', '.join(colunas)
        sql = f"INSERT INTO {tabela} ({colunas_str}) VALUES ({placeholders})"
        
        cursor.executemany(sql, registros)
        print(f"  - {tabela}: {len(registros)} registros inseridos")
    
    conn.commit()
    
    # Verifica resultado
    print("\nVerificando banco criado:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for (tabela,) in cursor.fetchall():
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cursor.fetchone()[0]
        print(f"  - {tabela}: {count} registros")
    
    conn.close()
    print(f"\nBanco '{banco_destino}' criado com sucesso!")
    print("\nPara usar o banco, renomeie para 'listas.db' ou atualize a referência no código.")

if __name__ == '__main__':
    main()
