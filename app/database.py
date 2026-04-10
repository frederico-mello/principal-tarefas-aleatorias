import sqlite3
from pathlib import Path
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='listas.db'):
        # Constrói o caminho para o banco de dados na raiz do projeto
        project_root = Path(__file__).parent.parent
        self.db_path = project_root / db_name
        
        print(f"--- [Database Init] ---")
        print(f"Procurando banco de dados em: {self.db_path.resolve()}")
        if self.db_path.exists():
            print("Banco de dados encontrado!")
        else:
            print("AVISO: Banco de dados NÃO encontrado. Um novo será criado, mas pode estar vazio.")
        print(f"----------------------")

        self._create_tables()
    
    def _get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(str(self.db_path))
    
    def _create_tables(self):
        """Cria a tabela de histórico se não existir"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS itens_sorteados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        data_sorteio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Erro ao criar tabela 'itens_sorteados': {e}")
            raise

    def registrar_item_sorteado(self, item, categoria):
        """Registra um item sorteado no banco de dados"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO itens_sorteados (item, categoria) VALUES (?, ?)",
                (item, categoria)
            )
            conn.commit()

    def obter_historico_sorteios(self, limite=10):
        """Retorna o histórico de itens sorteados"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT item, categoria, datetime(data_sorteio, 'localtime') as data_formatada 
                FROM itens_sorteados 
                ORDER BY data_sorteio DESC 
                LIMIT ?
            """, (limite,))
            return cursor.fetchall()

    def get_items_from_listas(self, category_name):
        """Retorna todos os itens de uma categoria específica da tabela listas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.descricao, 15 as tempo
                FROM listas l
                JOIN categorias c ON l.categoria_id = c.id
                WHERE c.nome = ?
                ORDER BY l.descricao
            """, (category_name,))
            return dict(cursor.fetchall() or [])

    def get_items_from_dicionarios(self, category_name):
        """Retorna todos os itens de uma categoria específica da tabela dicionarios"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.nome, d.valor
                FROM dicionarios d
                JOIN categorias c ON d.categoria_id = c.id
                WHERE c.nome = ?
                ORDER BY d.nome
            """, (category_name,))
            return dict(cursor.fetchall() or [])

    def get_all_items(self, category_name):
        """Retorna todos os itens de uma categoria, tentando em ambas as tabelas"""
        # Tenta primeiro na tabela dicionarios
        items = self.get_items_from_dicionarios(category_name)
        if items:
            return items
        # Se não encontrar, tenta na tabela listas
        return self.get_items_from_listas(category_name)

    def get_all_activities(self, category_name):
        """Retorna todas as atividades de uma categoria específica da tabela listas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.descricao 
                FROM listas l
                JOIN categorias c ON l.categoria_id = c.id
                WHERE c.nome = ?
                ORDER BY l.descricao
            """, (category_name,))
            return [row[0] for row in cursor.fetchall()]

    def get_random_item(self, category_name, max_value=None):
        """Retorna um item aleatório de uma categoria, opcionalmente com valor máximo"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT d.nome, d.valor 
                FROM dicionarios d
                JOIN categorias c ON d.categoria_id = c.id
                WHERE c.nome = ?
            """
            params = [category_name]

            if max_value is not None:
                query += " AND d.valor <= ?"
                params.append(float(max_value))
            
            query += " ORDER BY RANDOM() LIMIT 1"
            
            cursor.execute(query, tuple(params))
            
            result = cursor.fetchone()
            
            if result:
                return (result[0], result[1])
            else:
                return None

    def get_random_activity(self, category_name):
        """Retorna uma atividade aleatória de uma categoria"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.descricao 
                FROM listas l
                JOIN categorias c ON l.categoria_id = c.id
                WHERE c.nome = ?
                ORDER BY RANDOM()
                LIMIT 1
            """, (category_name,))
            result = cursor.fetchone()
            return result[0] if result else None

# Instância global para ser usada em todo o aplicativo
db = Database()
