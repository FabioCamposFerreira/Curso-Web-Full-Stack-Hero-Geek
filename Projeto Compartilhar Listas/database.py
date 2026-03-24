import sqlite3
import hashlib
import time
import os
import json

DB_PATH = "shareproducts.db"
CARRINHOS_FILE = "carrinhos.json"

def init_db():
    """Inicializa o banco de dados"""
    if os.path.exists("database.sql"):
        with open("database.sql", 'r', encoding='utf-8') as f:
            sql = f.read()
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(sql)
        conn.commit()
        conn.close()

def get_produtos(filtro=""):
    """Retorna lista de produtos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if filtro:
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome", (f"%{filtro}%",))
    else:
        cursor.execute("SELECT * FROM produtos ORDER BY nome")
    
    produtos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return produtos

def get_produto(produto_id):
    """Retorna um produto pelo ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = dict(cursor.fetchone() or {})
    conn.close()
    return produto

def gerar_codigo():
    """Gera código único para compartilhamento"""
    return hashlib.md5(str(time.time()).encode()).hexdigest()[:12].upper()

def salvar_carrinho(itens):
    """Salva carrinho em JSON e retorna código"""
    codigo = gerar_codigo()
    carrinhos = {}
    if os.path.exists(CARRINHOS_FILE):
        with open(CARRINHOS_FILE, 'r') as f:
            carrinhos = json.load(f)
    
    carrinhos[codigo] = {"itens": itens, "total": sum(i["qty"] * get_produto(i["id"])["preco"] for i in itens)}
    
    with open(CARRINHOS_FILE, 'w') as f:
        json.dump(carrinhos, f)
    
    return codigo

def carregar_carrinho(codigo):
    """Carrega carrinho pelo código"""
    if not os.path.exists(CARRINHOS_FILE):
        return None
    
    with open(CARRINHOS_FILE, 'r') as f:
        carrinhos = json.load(f)
    
    return carrinhos.get(codigo)
