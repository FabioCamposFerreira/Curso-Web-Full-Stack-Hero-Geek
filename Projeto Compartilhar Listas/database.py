"""
Módulo de gerenciamento do banco de dados SQLite
"""
import sqlite3
import os
from typing import List, Dict, Optional
import hashlib
import time


class Database:
    def __init__(self, db_path: str = "shareproducts.db"):
        self.db_path = db_path
        self.initialize_database()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Inicializa o banco de dados com o schema"""
        # Lê o arquivo SQL e executa
        sql_file = "database.sql"
        if os.path.exists(sql_file):
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()
            conn.close()
    
    # ===== PRODUTOS =====
    
    def get_produtos(self, filtro: str = "") -> List[Dict]:
        """Retorna todos os produtos ativos, com filtro opcional"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if filtro:
            cursor.execute("""
                SELECT * FROM produtos 
                WHERE ativo = 1 AND nome LIKE ?
                ORDER BY nome
            """, (f"%{filtro}%",))
        else:
            cursor.execute("""
                SELECT * FROM produtos 
                WHERE ativo = 1
                ORDER BY nome
            """)
        
        produtos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return produtos
    
    def get_produto_by_id(self, produto_id: int) -> Optional[Dict]:
        """Retorna um produto pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # ===== CARRINHOS =====
    
    def gerar_codigo_compartilhamento(self) -> str:
        """Gera um código único para compartilhamento"""
        timestamp = str(time.time())
        hash_obj = hashlib.md5(timestamp.encode())
        return hash_obj.hexdigest()[:12].upper()
    
    def salvar_carrinho(self, itens: List[Dict], nome_carrinho: str = "") -> str:
        """
        Salva um carrinho e retorna o código de compartilhamento
        itens: [{"produto_id": int, "quantidade": int, "preco_unitario": float}]
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Calcula valor total
        valor_total = sum(item["quantidade"] * item["preco_unitario"] for item in itens)
        
        # Gera código único
        codigo = self.gerar_codigo_compartilhamento()
        
        # Insere carrinho
        cursor.execute("""
            INSERT INTO carrinhos (codigo_compartilhamento, nome_carrinho, valor_total)
            VALUES (?, ?, ?)
        """, (codigo, nome_carrinho, valor_total))
        
        carrinho_id = cursor.lastrowid
        
        # Insere itens do carrinho
        for item in itens:
            valor_item = item["quantidade"] * item["preco_unitario"]
            cursor.execute("""
                INSERT INTO carrinho_itens 
                (carrinho_id, produto_id, quantidade, preco_unitario, valor_total)
                VALUES (?, ?, ?, ?, ?)
            """, (carrinho_id, item["produto_id"], item["quantidade"], 
                  item["preco_unitario"], valor_item))
        
        conn.commit()
        conn.close()
        
        return codigo
    
    def carregar_carrinho(self, codigo: str) -> Optional[Dict]:
        """Carrega um carrinho pelo código de compartilhamento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Busca o carrinho
        cursor.execute("""
            SELECT * FROM carrinhos 
            WHERE codigo_compartilhamento = ?
        """, (codigo,))
        
        carrinho_row = cursor.fetchone()
        
        if not carrinho_row:
            conn.close()
            return None
        
        carrinho = dict(carrinho_row)
        
        # Busca os itens do carrinho com informações do produto
        cursor.execute("""
            SELECT ci.*, p.nome, p.descricao
            FROM carrinho_itens ci
            JOIN produtos p ON ci.produto_id = p.id
            WHERE ci.carrinho_id = ?
        """, (carrinho["id"],))
        
        itens = [dict(row) for row in cursor.fetchall()]
        carrinho["itens"] = itens
        
        conn.close()
        return carrinho
    
    def verificar_codigo_existe(self, codigo: str) -> bool:
        """Verifica se um código de compartilhamento existe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) as count FROM carrinhos 
            WHERE codigo_compartilhamento = ?
        """, (codigo,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result["count"] > 0
