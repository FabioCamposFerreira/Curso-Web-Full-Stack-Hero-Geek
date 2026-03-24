import sqlite3
import hashlib
import time
import os
import json

DB_PATH = "shareproducts.db"
CARRINHOS_FILE = "carrinhos.json"


def init_db():
    if os.path.exists(DB_PATH):
        return
    with open("database.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql)
    conn.commit()
    conn.close()


def get_produtos(filtro=""):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if filtro:
        cur.execute(
            "SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome",
            (f"%{filtro}%",),
        )
    else:
        cur.execute("SELECT * FROM produtos ORDER BY nome")
    produtos = []
    for row in cur.fetchall():
        produtos.append(dict(row))
    conn.close()
    return produtos


def get_produto(produto_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {}


def gerar_codigo():
    return hashlib.md5(str(time.time()).encode()).hexdigest()[:12].upper()


def salvar_carrinho(itens):
    codigo = gerar_codigo()
    carrinhos = {}
    if os.path.exists(CARRINHOS_FILE):
        with open(CARRINHOS_FILE, "r", encoding="utf-8") as f:
            carrinhos = json.load(f)
    total = 0
    for item in itens:
        total += item["qty"] * item["preco"]
    carrinhos[codigo] = {"itens": itens, "total": total}
    with open(CARRINHOS_FILE, "w", encoding="utf-8") as f:
        json.dump(carrinhos, f)
    return codigo


def carregar_carrinho(codigo):
    if not os.path.exists(CARRINHOS_FILE):
        return None
    with open(CARRINHOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get(codigo)
