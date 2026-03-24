# Tutorial completo em Markdown — projeto **Share Products**

Este tutorial mostra como montar o projeto completo em partes, do zero, até chegar em:

- tela para ver produtos;
- tela para ver carrinho;
- compartilhamento do carrinho por código/QR;
- leitura do código do carrinho;
- filtro de pesquisa na tela de produtos.

A ideia aqui é construir **na ordem**, sem misturar tudo de uma vez.

---

## O que vamos usar

### Bibliotecas

Instale estas bibliotecas antes de começar:

```bash
pip install customtkinter qrcode pillow pyperclip opencv-python pyzbar
```

### Estrutura final do projeto

No final, sua pasta vai ficar assim:

```text
share-products/
├── main.py
├── database.py
├── database.sql
├── shareproducts.db      # criado automaticamente
└── carrinhos.json        # criado automaticamente quando compartilhar um carrinho
```

---

# Parte 1 — Criação dos arquivos e estrutura do projeto

## O que vamos fazer

Aqui vamos criar **somente a estrutura** do projeto, com os arquivos vazios.
Ainda não vamos colocar lógica nenhuma.

## Estrutura inicial

Crie uma pasta chamada `share-products`.

Dentro dela, crie estes 3 arquivos vazios:

- `main.py`
- `database.py`
- `database.sql`

A estrutura fica assim:

```text
share-products/
├── main.py
├── database.py
└── database.sql
```

## Como criar os arquivos

### Opção 1 — manualmente

Crie a pasta e depois crie os três arquivos.

### Opção 2 — pelo terminal

```bash
mkdir share-products
cd share-products
copy nul main.py
copy nul database.py
copy nul database.sql
```

> No Windows, `copy nul arquivo.ext` cria um arquivo vazio.

---

# Parte 2 — Criar o banco de dados

## O que vamos fazer

Agora vamos criar:

1. o arquivo SQL com a tabela de produtos;
2. o arquivo Python que cria o banco automaticamente;
3. funções para buscar todos os produtos e buscar um produto por ID.

---

## Arquivo `database.sql`

Coloque este conteúdo no arquivo:

```sql
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
);

INSERT INTO produtos (nome, preco) VALUES
('Arroz 5kg', 25.90),
('Feijão 1kg', 8.50),
('Óleo 900ml', 7.20),
('Açúcar 1kg', 4.30),
('Café 500g', 15.80),
('Macarrão 500g', 4.90),
('Molho Tomate', 3.50),
('Leite 1L', 5.20),
('Farinha 1kg', 5.60),
('Sal 1kg', 2.10),
('Biscoito', 3.80),
('Margarina 500g', 8.90),
('Sabão 1kg', 12.50),
('Detergente 500ml', 2.30),
('Papel Higiênico', 9.80),
('Sabonete', 2.50),
('Shampoo 350ml', 11.90),
('Creme Dental', 5.40),
('Desinfetante 1L', 6.80),
('Esponja Aço', 4.20);
```

## Explicação linha por linha

`CREATE TABLE IF NOT EXISTS produtos (`
- cria a tabela chamada `produtos`.
- `IF NOT EXISTS` evita erro se a tabela já existir.

`id INTEGER PRIMARY KEY AUTOINCREMENT,`
- cria a coluna `id`.
- `INTEGER` significa número inteiro.
- `PRIMARY KEY` define essa coluna como chave principal.
- `AUTOINCREMENT` faz o SQLite gerar o próximo número automaticamente.

`nome TEXT NOT NULL,`
- cria a coluna `nome`.
- `TEXT` significa texto.
- `NOT NULL` obriga o valor a existir.

`preco REAL NOT NULL`
- cria a coluna `preco`.
- `REAL` é número decimal.
- `NOT NULL` obriga o valor a existir.

`);`
- encerra a criação da tabela.

`INSERT INTO produtos (nome, preco) VALUES`
- insere registros na tabela `produtos`.
- diz que vamos preencher as colunas `nome` e `preco`.

`('Arroz 5kg', 25.90),`
- adiciona um produto chamado `Arroz 5kg` com preço `25.90`.

As demais linhas de `INSERT` fazem exatamente a mesma coisa para os outros produtos.

---

## Arquivo `database.py`

Agora coloque este conteúdo:

```python
import sqlite3
import os

DB_PATH = "shareproducts.db"


def init_db():
    if os.path.exists(DB_PATH):
        return
    with open("database.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql)
    conn.commit()
    conn.close()


def get_produtos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
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
```

## Explicação linha por linha

`import sqlite3`
- importa o módulo padrão do Python para trabalhar com SQLite.

`import os`
- importa funções do sistema operacional.
- vamos usar para verificar se o arquivo do banco já existe.

`DB_PATH = "shareproducts.db"`
- guarda o nome do arquivo do banco.

`def init_db():`
- cria a função que inicializa o banco.

`if os.path.exists(DB_PATH):`
- verifica se o arquivo do banco já existe.

`return`
- se o banco já existir, sai da função.

`with open("database.sql", "r", encoding="utf-8") as f:`
- abre o arquivo SQL em modo leitura.
- `encoding="utf-8"` garante leitura correta de acentos.

`sql = f.read()`
- lê todo o conteúdo do arquivo SQL.

`conn = sqlite3.connect(DB_PATH)`
- cria uma conexão com o arquivo do banco.

`conn.executescript(sql)`
- executa o script SQL completo.

`conn.commit()`
- confirma as alterações no banco.

`conn.close()`
- fecha a conexão.

`def get_produtos():`
- cria a função que lista todos os produtos.

`conn = sqlite3.connect(DB_PATH)`
- abre conexão com o banco.

`conn.row_factory = sqlite3.Row`
- faz cada linha do banco poder ser acessada como dicionário.

`cur = conn.cursor()`
- cria o cursor para executar comandos SQL.

`cur.execute("SELECT * FROM produtos ORDER BY nome")`
- busca todos os produtos.
- `ORDER BY nome` ordena por nome.

`produtos = []`
- cria uma lista vazia para guardar o resultado.

`for row in cur.fetchall():`
- percorre todas as linhas retornadas.

`produtos.append(dict(row))`
- converte a linha para dicionário e adiciona na lista.

`conn.close()`
- fecha a conexão.

`return produtos`
- devolve a lista de produtos.

`def get_produto(produto_id):`
- cria a função para buscar um produto específico.

`cur.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))`
- busca o produto com o ID informado.
- o `?` evita montar SQL manualmente.

`row = cur.fetchone()`
- pega uma única linha.

`if row:`
- verifica se encontrou produto.

`return dict(row)`
- devolve o produto como dicionário.

`return {}`
- se não encontrou, devolve dicionário vazio.

---

# Parte 3 — Criar a Tela 1 para ver produtos

## O que vamos fazer

Agora vamos criar a primeira tela da aplicação:

- abre a janela;
- carrega os produtos do banco;
- mostra um botão para adicionar produto no carrinho;
- mostra no topo quantos itens existem no carrinho.

> Aqui **ainda não vamos criar o filtro de pesquisa**. Isso fica só na Parte 7.

---

## Arquivo `main.py`

Coloque este conteúdo:

```python
import customtkinter as ctk

from database import init_db, get_produtos

carrinho = {}
root = None
btn_carrinho = None


def atualizar_botao_carrinho():
    if btn_carrinho:
        btn_carrinho.configure(text=f"🛒 Carrinho ({len(carrinho)})")


def adicionar(p):
    if p["id"] in carrinho:
        carrinho[p["id"]]["qtd"] += 1
    else:
        carrinho[p["id"]] = {"produto": p, "qtd": 1}
    atualizar_botao_carrinho()


def tela_produtos():
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    header = ctk.CTkFrame(frame)
    header.pack(fill="x", pady=10)

    ctk.CTkLabel(
        header,
        text="📦 Share Products",
        font=("Arial", 24, "bold"),
    ).pack(side="left")

    global btn_carrinho
    btn_carrinho = ctk.CTkButton(
        header,
        text=f"🛒 Carrinho ({len(carrinho)})",
    )
    btn_carrinho.pack(side="right", padx=5)

    lista = ctk.CTkScrollableFrame(frame)
    lista.pack(fill="both", expand=True)

    for produto in get_produtos():
        card = ctk.CTkFrame(lista, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(
            card,
            text=f"{produto['nome']} - R$ {produto['preco']:.2f}",
            font=("Arial", 12),
        ).pack(side="left", padx=10, pady=8)

        ctk.CTkButton(
            card,
            text="🛒 Adicionar",
            width=100,
            command=lambda p=produto: adicionar(p),
        ).pack(side="right", padx=5, pady=5)


def main():
    global root
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Share Products")
    root.geometry("800x600")
    init_db()
    tela_produtos()
    root.mainloop()


if __name__ == "__main__":
    main()
```

## Explicação linha por linha

`import customtkinter as ctk`
- importa a biblioteca da interface.
- `as ctk` cria um apelido menor para usar no código.

`from database import init_db, get_produtos`
- importa as funções do arquivo `database.py`.
- `init_db` cria o banco.
- `get_produtos` busca os produtos.

`carrinho = {}`
- cria um dicionário vazio para guardar os itens adicionados.

`root = None`
- cria a variável principal da janela.

`btn_carrinho = None`
- cria a variável do botão do carrinho.
- ela começa vazia e depois vai receber o botão real.

`def atualizar_botao_carrinho():`
- cria a função para atualizar o texto do botão do carrinho.

`if btn_carrinho:`
- verifica se o botão já foi criado.

`btn_carrinho.configure(text=f"🛒 Carrinho ({len(carrinho)})")`
- troca o texto do botão.
- `len(carrinho)` mostra quantos produtos diferentes existem no carrinho.

`def adicionar(p):`
- cria a função para adicionar produto no carrinho.
- `p` é o produto recebido.

`if p["id"] in carrinho:`
- verifica se o ID do produto já existe no carrinho.

`carrinho[p["id"]]["qtd"] += 1`
- se já existe, soma mais 1 na quantidade.

`else:`
- entra aqui se ainda não existir no carrinho.

`carrinho[p["id"]] = {"produto": p, "qtd": 1}`
- cria um novo item no carrinho.
- salva o produto e começa com quantidade 1.

`atualizar_botao_carrinho()`
- atualiza o contador do carrinho na tela.

`def tela_produtos():`
- cria a função da tela de produtos.

`frame = ctk.CTkFrame(root)`
- cria um container dentro da janela principal.

`frame.pack(fill="both", expand=True, padx=10, pady=10)`
- desenha o container.
- `fill="both"` ocupa largura e altura.
- `expand=True` faz crescer junto com a janela.
- `padx` e `pady` criam espaçamento.

`header = ctk.CTkFrame(frame)`
- cria a faixa superior da tela.

`header.pack(fill="x", pady=10)`
- faz o cabeçalho ocupar toda a largura.

`ctk.CTkLabel(`
- começa a criação do texto do título.

`header,`
- diz que o título fica dentro do cabeçalho.

`text="📦 Share Products",`
- define o texto exibido.

`font=("Arial", 24, "bold"),`
- define fonte, tamanho e negrito.

`).pack(side="left")`
- desenha o título alinhado à esquerda.

`global btn_carrinho`
- avisa que a função vai usar a variável global `btn_carrinho`.

`btn_carrinho = ctk.CTkButton(`
- cria o botão do carrinho.

`header,`
- coloca o botão dentro do cabeçalho.

`text=f"🛒 Carrinho ({len(carrinho)})",`
- já mostra a quantidade inicial no texto.

`)`
- encerra a criação do botão.

`btn_carrinho.pack(side="right", padx=5)`
- desenha o botão do lado direito.

`lista = ctk.CTkScrollableFrame(frame)`
- cria uma área rolável para os produtos.

`lista.pack(fill="both", expand=True)`
- faz a lista ocupar o espaço restante.

`for produto in get_produtos():`
- percorre todos os produtos do banco.

`card = ctk.CTkFrame(lista, corner_radius=10)`
- cria um card para cada produto.
- `corner_radius=10` arredonda as bordas.

`card.pack(fill="x", padx=5, pady=5)`
- desenha o card ocupando a largura.

`ctk.CTkLabel(`
- começa a criação do texto do produto.

`card,`
- diz que o texto fica dentro do card.

`text=f"{produto['nome']} - R$ {produto['preco']:.2f}",`
- mostra nome e preço com duas casas decimais.

`font=("Arial", 12),`
- define o estilo da fonte.

`).pack(side="left", padx=10, pady=8)`
- desenha o texto do lado esquerdo com espaçamento.

`ctk.CTkButton(`
- começa a criação do botão de adicionar.

`card,`
- o botão fica dentro do card.

`text="🛒 Adicionar",`
- texto do botão.

`width=100,`
- largura do botão.

`command=lambda p=produto: adicionar(p),`
- quando clicar, chama a função `adicionar`.
- `lambda p=produto` guarda o produto certo daquela linha.

`).pack(side="right", padx=5, pady=5)`
- desenha o botão do lado direito.

`def main():`
- cria a função principal do programa.

`global root`
- avisa que vai usar a variável global `root`.

`ctk.set_appearance_mode("dark")`
- define o tema escuro.

`ctk.set_default_color_theme("blue")`
- define o tema de cores azul.

`root = ctk.CTk()`
- cria a janela principal.

`root.title("Share Products")`
- define o título da janela.

`root.geometry("800x600")`
- define largura e altura da janela.

`init_db()`
- cria o banco e insere os produtos, se ainda não existir.

`tela_produtos()`
- abre a tela de produtos.

`root.mainloop()`
- inicia o loop da interface.

`if __name__ == "__main__":`
- garante que o programa rode só quando esse arquivo for executado diretamente.

`main()`
- chama a função principal.

---

# Parte 4 — Criar a Tela 2 para ver carrinho

## O que vamos fazer

Agora vamos adicionar:

- segunda tela para ver o carrinho;
- botão voltar;
- aumentar quantidade;
- diminuir quantidade;
- remover item;
- limpar carrinho;
- atualizar só os números da tela, sem recriar tudo a cada clique.

---

## Substitua o conteúdo de `main.py` por este

```python
import customtkinter as ctk
from tkinter import messagebox

from database import init_db, get_produtos

carrinho = {}
root = tela_atual = btn_carrinho = label_total = None
itens_carrinho = {}


def limpar_tela():
    global tela_atual, btn_carrinho, label_total, itens_carrinho
    if tela_atual:
        tela_atual.destroy()
    tela_atual = btn_carrinho = label_total = None
    itens_carrinho = {}


def total_carrinho():
    total = 0
    for item in carrinho.values():
        total += item["qtd"] * item["produto"]["preco"]
    return total


def atualizar_botao_carrinho():
    if btn_carrinho and btn_carrinho.winfo_exists():
        btn_carrinho.configure(text=f"🛒 Carrinho ({len(carrinho)})")


def atualizar_total_carrinho():
    if label_total and label_total.winfo_exists():
        label_total.configure(text=f"Total: R$ {total_carrinho():.2f}")


def atualizar_item_carrinho(pid):
    if pid in carrinho and pid in itens_carrinho:
        item = carrinho[pid]
        itens_carrinho[pid][1].configure(text=str(item["qtd"]))
        itens_carrinho[pid][2].configure(
            text=f"Total: R$ {item['qtd'] * item['produto']['preco']:.2f}"
        )
    atualizar_total_carrinho()
    atualizar_botao_carrinho()


def adicionar(p):
    if p["id"] in carrinho:
        carrinho[p["id"]]["qtd"] += 1
    else:
        carrinho[p["id"]] = {"produto": p, "qtd": 1}
    atualizar_botao_carrinho()


def alterar_qtd(pid, delta):
    if pid in carrinho:
        carrinho[pid]["qtd"] += delta
        if carrinho[pid]["qtd"] <= 0:
            remover(pid)
        else:
            atualizar_item_carrinho(pid)


def remover(pid):
    if pid in carrinho:
        del carrinho[pid]
        atualizar_botao_carrinho()
        if pid in itens_carrinho:
            itens_carrinho[pid][0].destroy()
            del itens_carrinho[pid]
            if carrinho:
                atualizar_total_carrinho()
            else:
                tela_carrinho()


def limpar_carrinho():
    if messagebox.askyesno("Confirmar", "Limpar carrinho?"):
        carrinho.clear()
        atualizar_botao_carrinho()
        tela_carrinho()


def tela_produtos():
    global tela_atual, btn_carrinho
    limpar_tela()

    tela_atual = ctk.CTkFrame(root)
    tela_atual.pack(fill="both", expand=True, padx=10, pady=10)

    header = ctk.CTkFrame(tela_atual)
    header.pack(fill="x", pady=10)

    ctk.CTkLabel(
        header,
        text="📦 Share Products",
        font=("Arial", 24, "bold"),
    ).pack(side="left")

    btn_carrinho = ctk.CTkButton(
        header,
        text=f"🛒 Carrinho ({len(carrinho)})",
        command=tela_carrinho,
    )
    btn_carrinho.pack(side="right", padx=5)

    lista = ctk.CTkScrollableFrame(tela_atual)
    lista.pack(fill="both", expand=True)

    for produto in get_produtos():
        card = ctk.CTkFrame(lista, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(
            card,
            text=f"{produto['nome']} - R$ {produto['preco']:.2f}",
            font=("Arial", 12),
        ).pack(side="left", padx=10, pady=8)

        ctk.CTkButton(
            card,
            text="🛒 Adicionar",
            width=100,
            command=lambda p=produto: adicionar(p),
        ).pack(side="right", padx=5, pady=5)


def tela_carrinho():
    global tela_atual, label_total, itens_carrinho
    limpar_tela()

    tela_atual = ctk.CTkFrame(root)
    tela_atual.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkButton(tela_atual, text="← Voltar", command=tela_produtos).pack(pady=10)
    ctk.CTkLabel(
        tela_atual,
        text="🛒 Meu Carrinho",
        font=("Arial", 20, "bold"),
    ).pack()

    if not carrinho:
        ctk.CTkLabel(
            tela_atual,
            text="Carrinho vazio :(",
            font=("Arial", 14),
        ).pack(pady=50)
        return

    scroll = ctk.CTkScrollableFrame(tela_atual)
    scroll.pack(fill="both", expand=True, pady=10)

    for pid, item in carrinho.items():
        p = item["produto"]
        card = ctk.CTkFrame(scroll, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            info,
            text=f"{p['nome']} - R$ {p['preco']:.2f}",
            font=("Arial", 12),
        ).pack(anchor="w")

        ctrl = ctk.CTkFrame(info, fg_color="transparent")
        ctrl.pack(fill="x", pady=5)

        ctk.CTkButton(
            ctrl,
            text="-",
            width=30,
            command=lambda pid=pid: alterar_qtd(pid, -1),
        ).pack(side="left", padx=2)

        qtd = ctk.CTkLabel(ctrl, text=str(item["qtd"]), font=("Arial", 12))
        qtd.pack(side="left", padx=10)

        ctk.CTkButton(
            ctrl,
            text="+",
            width=30,
            command=lambda pid=pid: alterar_qtd(pid, 1),
        ).pack(side="left", padx=2)

        total_item = ctk.CTkLabel(
            ctrl,
            text=f"Total: R$ {item['qtd'] * p['preco']:.2f}",
            font=("Arial", 12, "bold"),
        )
        total_item.pack(side="right")

        ctk.CTkButton(
            ctrl,
            text="🗑️",
            width=30,
            command=lambda pid=pid: remover(pid),
        ).pack(side="right", padx=5)

        itens_carrinho[pid] = card, qtd, total_item

    label_total = ctk.CTkLabel(
        tela_atual,
        text=f"Total: R$ {total_carrinho():.2f}",
        font=("Arial", 16, "bold"),
    )
    label_total.pack(pady=10)

    footer = ctk.CTkFrame(tela_atual)
    footer.pack(fill="x", pady=10)

    ctk.CTkButton(
        footer,
        text="🗑️ Limpar",
        command=limpar_carrinho,
    ).pack(side="right", padx=5)


def main():
    global root
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Share Products")
    root.geometry("800x600")
    init_db()
    tela_produtos()
    root.mainloop()


if __name__ == "__main__":
    main()
```

## Explicação das partes novas

### Controle de tela atual

`root = tela_atual = btn_carrinho = label_total = None`
- cria várias variáveis globais de uma vez.
- `tela_atual` vai guardar a tela visível.
- `label_total` vai guardar o texto do total do carrinho.

`itens_carrinho = {}`
- guarda referências visuais de cada item na tela do carrinho.
- isso permite atualizar só aquele item, sem redesenhar tudo.

### Limpar a tela antes de abrir outra

`def limpar_tela():`
- cria a função que fecha a tela atual.

`if tela_atual:`
- verifica se já existe uma tela aberta.

`tela_atual.destroy()`
- remove a tela da interface.

`tela_atual = btn_carrinho = label_total = None`
- limpa as referências visuais.

`itens_carrinho = {}`
- limpa o dicionário com os widgets dos itens.

### Calcular o total

`def total_carrinho():`
- cria a função que soma o total do carrinho.

`for item in carrinho.values():`
- percorre os itens do carrinho.

`total += item["qtd"] * item["produto"]["preco"]`
- multiplica quantidade por preço e soma no total.

### Atualizar só a linha do item

`def atualizar_item_carrinho(pid):`
- cria a função que atualiza apenas um item da tela.

`if pid in carrinho and pid in itens_carrinho:`
- garante que o item existe no carrinho e também na tela.

`item = carrinho[pid]`
- pega o item atualizado.

`itens_carrinho[pid][1].configure(text=str(item["qtd"]))`
- atualiza o texto da quantidade.

`itens_carrinho[pid][2].configure(...)`
- atualiza o total daquela linha.

`atualizar_total_carrinho()`
- atualiza o total geral.

`atualizar_botao_carrinho()`
- atualiza o botão do topo.

### Alterar quantidade

`def alterar_qtd(pid, delta):`
- cria a função que soma ou subtrai quantidade.
- `delta` recebe `1` ou `-1`.

`carrinho[pid]["qtd"] += delta`
- altera a quantidade.

`if carrinho[pid]["qtd"] <= 0:`
- se a quantidade chegar em zero ou menos, remove o item.

`remover(pid)`
- chama a função de remoção.

`else:`
- se ainda existir quantidade positiva.

`atualizar_item_carrinho(pid)`
- atualiza só aquela linha da tela.

### Remover item

`def remover(pid):`
- cria a função que remove um item.

`del carrinho[pid]`
- exclui o item do dicionário do carrinho.

`itens_carrinho[pid][0].destroy()`
- destrói o card visual desse item.

`del itens_carrinho[pid]`
- remove a referência do dicionário visual.

`if carrinho:`
- verifica se ainda sobrou item no carrinho.

`atualizar_total_carrinho()`
- atualiza o total se ainda houver itens.

`else:`
- se o carrinho ficou vazio.

`tela_carrinho()`
- recria a tela do carrinho para mostrar a mensagem de vazio.

### Limpar tudo

`messagebox.askyesno("Confirmar", "Limpar carrinho?")`
- abre uma caixa de confirmação com Sim/Não.

`carrinho.clear()`
- remove todos os itens do carrinho.

`tela_carrinho()`
- recarrega a tela do carrinho já vazia.

### Abrir a tela do carrinho

`command=tela_carrinho`
- faz o botão do carrinho abrir a segunda tela.

### Guardar widgets do item

`itens_carrinho[pid] = card, qtd, total_item`
- salva os elementos visuais do item.
- `card` é o container da linha.
- `qtd` é o texto da quantidade.
- `total_item` é o texto do total da linha.

---

# Parte 5 — Compartilhar carrinho

## O que vamos fazer

Agora vamos permitir:

- salvar o carrinho em arquivo JSON;
- gerar um código único;
- mostrar esse código;
- gerar o QR Code;
- copiar o código;
- começar um novo carrinho.

---

## Primeiro: atualize `database.py`

Substitua por este conteúdo:

```python
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
```

## Explicação das partes novas do `database.py`

`import hashlib`
- importa a biblioteca para gerar hash.

`import time`
- importa funções de tempo.

`import json`
- importa o módulo para ler e salvar JSON.

`CARRINHOS_FILE = "carrinhos.json"`
- define o nome do arquivo onde os carrinhos serão salvos.

`def gerar_codigo():`
- cria a função que gera um código único.

`str(time.time()).encode()`
- pega o horário atual, transforma em texto e depois em bytes.

`hashlib.md5(...).hexdigest()`
- gera um hash em texto.

`[:12]`
- pega apenas os 12 primeiros caracteres.

`.upper()`
- converte para maiúsculo.

`def salvar_carrinho(itens):`
- cria a função que salva os itens do carrinho.

`codigo = gerar_codigo()`
- gera o código do carrinho.

`carrinhos = {}`
- começa com um dicionário vazio.

`if os.path.exists(CARRINHOS_FILE):`
- verifica se o arquivo JSON já existe.

`carrinhos = json.load(f)`
- lê os carrinhos já salvos.

`total = 0`
- inicia o total em zero.

`for item in itens:`
- percorre os itens recebidos.

`total += item["qty"] * item["preco"]`
- soma quantidade vezes preço.

`carrinhos[codigo] = {"itens": itens, "total": total}`
- grava o novo carrinho no dicionário.

`json.dump(carrinhos, f)`
- salva tudo no arquivo JSON.

`return codigo`
- devolve o código gerado.

---

## Agora atualize `main.py`

Substitua por este conteúdo:

```python
import customtkinter as ctk
from tkinter import messagebox

import qrcode
import pyperclip
from PIL import ImageTk

from database import init_db, get_produtos, salvar_carrinho

carrinho = {}
root = tela_atual = btn_carrinho = label_total = None
itens_carrinho = {}


def limpar_tela():
    global tela_atual, btn_carrinho, label_total, itens_carrinho
    if tela_atual:
        tela_atual.destroy()
    tela_atual = btn_carrinho = label_total = None
    itens_carrinho = {}


def total_carrinho():
    total = 0
    for item in carrinho.values():
        total += item["qtd"] * item["produto"]["preco"]
    return total


def atualizar_botao_carrinho():
    if btn_carrinho and btn_carrinho.winfo_exists():
        btn_carrinho.configure(text=f"🛒 Carrinho ({len(carrinho)})")


def atualizar_total_carrinho():
    if label_total and label_total.winfo_exists():
        label_total.configure(text=f"Total: R$ {total_carrinho():.2f}")


def atualizar_item_carrinho(pid):
    if pid in carrinho and pid in itens_carrinho:
        item = carrinho[pid]
        itens_carrinho[pid][1].configure(text=str(item["qtd"]))
        itens_carrinho[pid][2].configure(
            text=f"Total: R$ {item['qtd'] * item['produto']['preco']:.2f}"
        )
    atualizar_total_carrinho()
    atualizar_botao_carrinho()


def adicionar(p):
    if p["id"] in carrinho:
        carrinho[p["id"]]["qtd"] += 1
    else:
        carrinho[p["id"]] = {"produto": p, "qtd": 1}
    atualizar_botao_carrinho()


def alterar_qtd(pid, delta):
    if pid in carrinho:
        carrinho[pid]["qtd"] += delta
        if carrinho[pid]["qtd"] <= 0:
            remover(pid)
        else:
            atualizar_item_carrinho(pid)


def remover(pid):
    if pid in carrinho:
        del carrinho[pid]
        atualizar_botao_carrinho()
        if pid in itens_carrinho:
            itens_carrinho[pid][0].destroy()
            del itens_carrinho[pid]
            if carrinho:
                atualizar_total_carrinho()
            else:
                tela_carrinho()


def limpar_carrinho():
    if messagebox.askyesno("Confirmar", "Limpar carrinho?"):
        carrinho.clear()
        atualizar_botao_carrinho()
        tela_carrinho()


def tela_produtos():
    global tela_atual, btn_carrinho
    limpar_tela()
    tela_atual = ctk.CTkFrame(root)
    tela_atual.pack(fill="both", expand=True, padx=10, pady=10)

    header = ctk.CTkFrame(tela_atual)
    header.pack(fill="x", pady=10)

    ctk.CTkLabel(
        header,
        text="📦 Share Products",
        font=("Arial", 24, "bold"),
    ).pack(side="left")

    btn_carrinho = ctk.CTkButton(
        header,
        text=f"🛒 Carrinho ({len(carrinho)})",
        command=tela_carrinho,
    )
    btn_carrinho.pack(side="right", padx=5)

    lista = ctk.CTkScrollableFrame(tela_atual)
    lista.pack(fill="both", expand=True)

    for produto in get_produtos():
        card = ctk.CTkFrame(lista, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(
            card,
            text=f"{produto['nome']} - R$ {produto['preco']:.2f}",
            font=("Arial", 12),
        ).pack(side="left", padx=10, pady=8)

        ctk.CTkButton(
            card,
            text="🛒 Adicionar",
            width=100,
            command=lambda p=produto: adicionar(p),
        ).pack(side="right", padx=5, pady=5)


def tela_carrinho():
    global tela_atual, label_total, itens_carrinho
    limpar_tela()
    tela_atual = ctk.CTkFrame(root)
    tela_atual.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkButton(tela_atual, text="← Voltar", command=tela_produtos).pack(pady=10)
    ctk.CTkLabel(
        tela_atual,
        text="🛒 Meu Carrinho",
        font=("Arial", 20, "bold"),
    ).pack()

    if not carrinho:
        ctk.CTkLabel(
            tela_atual,
            text="Carrinho vazio :(",
            font=("Arial", 14),
        ).pack(pady=50)
        return

    scroll = ctk.CTkScrollableFrame(tela_atual)
    scroll.pack(fill="both", expand=True, pady=10)

    for pid, item in carrinho.items():
        p = item["produto"]
        card = ctk.CTkFrame(scroll, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            info,
            text=f"{p['nome']} - R$ {p['preco']:.2f}",
            font=("Arial", 12),
        ).pack(anchor="w")

        ctrl = ctk.CTkFrame(info, fg_color="transparent")
        ctrl.pack(fill="x", pady=5)

        ctk.CTkButton(
            ctrl,
            text="-",
            width=30,
            command=lambda pid=pid: alterar_qtd(pid, -1),
        ).pack(side="left", padx=2)

        qtd = ctk.CTkLabel(ctrl, text=str(item["qtd"]), font=("Arial", 12))
        qtd.pack(side="left", padx=10)

        ctk.CTkButton(
            ctrl,
            text="+",
            width=30,
            command=lambda pid=pid: alterar_qtd(pid, 1),
        ).pack(side="left", padx=2)

        total_item = ctk.CTkLabel(
            ctrl,
            text=f"Total: R$ {item['qtd'] * p['preco']:.2f}",
            font=("Arial", 12, "bold"),
        )
        total_item.pack(side="right")

        ctk.CTkButton(
            ctrl,
            text="🗑️",
            width=30,
            command=lambda pid=pid: remover(pid),
        ).pack(side="right", padx=5)

        itens_carrinho[pid] = card, qtd, total_item

    label_total = ctk.CTkLabel(
        tela_atual,
        text=f"Total: R$ {total_carrinho():.2f}",
        font=("Arial", 16, "bold"),
    )
    label_total.pack(pady=10)

    footer = ctk.CTkFrame(tela_atual)
    footer.pack(fill="x", pady=10)

    ctk.CTkButton(
        footer,
        text="🗑️ Limpar",
        command=limpar_carrinho,
    ).pack(side="right", padx=5)

    ctk.CTkButton(
        footer,
        text="📤 Compartilhar",
        command=tela_qr,
    ).pack(side="right", padx=5)


def tela_qr():
    global tela_atual
    limpar_tela()
    tela_atual = ctk.CTkFrame(root)
    tela_atual.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkButton(tela_atual, text="← Voltar", command=tela_carrinho).pack(pady=10)
    ctk.CTkLabel(
        tela_atual,
        text="📤 Compartilhar",
        font=("Arial", 20, "bold"),
    ).pack(pady=20)
    ctk.CTkLabel(tela_atual, text="✅ Carrinho salvo!", font=("Arial", 14)).pack()

    itens = []
    for pid, item in carrinho.items():
        itens.append({
            "id": pid,
            "qty": item["qtd"],
            "preco": item["produto"]["preco"],
        })

    codigo = salvar_carrinho(itens)

    ctk.CTkLabel(
        tela_atual,
        text=codigo,
        font=("Arial", 16, "bold"),
    ).pack(pady=20)

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(codigo)
    qr.make(fit=True)

    photo = ImageTk.PhotoImage(
        qr.make_image(fill_color="black", back_color="white").resize((250, 250))
    )

    qr_label = ctk.CTkLabel(tela_atual, text="", image=photo)
    qr_label.image = photo
    qr_label.pack(pady=20)

    ctk.CTkButton(
        tela_atual,
        text="📋 Copiar",
        command=lambda: pyperclip.copy(codigo),
    ).pack(pady=5)

    ctk.CTkButton(
        tela_atual,
        text="🛒 Novo Carrinho",
        command=lambda: (carrinho.clear(), tela_produtos()),
    ).pack(pady=5)


def main():
    global root
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Share Products")
    root.geometry("800x600")
    init_db()
    tela_produtos()
    root.mainloop()


if __name__ == "__main__":
    main()
```

## Explicação das partes novas do `main.py`

### Importações novas

`import qrcode`
- importa a biblioteca que gera QR Code.

`import pyperclip`
- importa a biblioteca que copia texto para a área de transferência.

`from PIL import ImageTk`
- importa a parte do Pillow que transforma imagem em objeto exibível no Tkinter.

`from database import init_db, get_produtos, salvar_carrinho`
- adiciona a função `salvar_carrinho` importada do banco.

### Botão compartilhar

`text="📤 Compartilhar"`
- define o texto do botão.

`command=tela_qr`
- ao clicar, abre a tela de compartilhamento.

### Montar a lista de itens para salvar

`itens = []`
- cria uma lista vazia.

`for pid, item in carrinho.items():`
- percorre todos os itens do carrinho.

`itens.append({...})`
- adiciona cada item em formato simples para salvar.

`"id": pid`
- salva o ID do produto.

`"qty": item["qtd"]`
- salva a quantidade.

`"preco": item["produto"]["preco"]`
- salva o preço.

### Salvar e exibir código

`codigo = salvar_carrinho(itens)`
- salva o carrinho no JSON e recebe o código gerado.

`text=codigo`
- mostra o código na tela.

### Gerar QR

`qr = qrcode.QRCode(version=1, box_size=10, border=2)`
- cria o objeto QR Code.
- `version=1` define um tamanho base.
- `box_size=10` define o tamanho dos quadrados.
- `border=2` define a borda do QR.

`qr.add_data(codigo)`
- coloca o código dentro do QR.

`qr.make(fit=True)`
- monta o QR final, ajustando tamanho se precisar.

`qr.make_image(fill_color="black", back_color="white")`
- gera a imagem do QR com fundo branco e conteúdo preto.

`.resize((250, 250))`
- redimensiona a imagem para 250x250.

`photo = ImageTk.PhotoImage(...)`
- transforma a imagem em objeto aceito pelo Tkinter.

`qr_label = ctk.CTkLabel(tela_atual, text="", image=photo)`
- cria um label que mostra a imagem.

`qr_label.image = photo`
- mantém referência da imagem para ela não sumir da tela.

### Copiar código

`command=lambda: pyperclip.copy(codigo)`
- quando clicar, copia o código para a área de transferência.

### Novo carrinho

`command=lambda: (carrinho.clear(), tela_produtos())`
- limpa o carrinho e volta para a tela de produtos.

---

# Parte 6 — Ler código do carrinho

## O que vamos fazer

Agora vamos permitir recuperar um carrinho de 3 formas:

- digitando o código manualmente;
- lendo uma imagem com QR Code;
- usando a câmera.

---

## Primeiro: atualize `database.py`

Adicione esta função no final do arquivo:

```python
def carregar_carrinho(codigo):
    if not os.path.exists(CARRINHOS_FILE):
        return None
    with open(CARRINHOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get(codigo)
```

## Explicação linha por linha

`def carregar_carrinho(codigo):`
- cria a função que busca um carrinho salvo pelo código.

`if not os.path.exists(CARRINHOS_FILE):`
- verifica se o arquivo JSON existe.

`return None`
- se não existir, devolve `None`.

`with open(CARRINHOS_FILE, "r", encoding="utf-8") as f:`
- abre o arquivo JSON para leitura.

`return json.load(f).get(codigo)`
- lê o JSON.
- busca a chave com o código informado.
- se não existir, devolve `None`.

---

## Agora atualize `main.py`

Substitua pelos imports abaixo no topo:

```python
import customtkinter as ctk
from tkinter import messagebox, filedialog

import qrcode
import pyperclip
import cv2
from PIL import ImageTk

from database import (
    init_db,
    get_produtos,
    get_produto,
    salvar_carrinho,
    carregar_carrinho,
)
```

## Explicação das importações novas

`from tkinter import messagebox, filedialog`
- `messagebox` mostra caixas de mensagem.
- `filedialog` abre seletor de arquivo.

`import cv2`
- importa o OpenCV para ler imagem e câmera.

`get_produto`
- será usado para buscar os dados completos de um produto salvo no carrinho.

`carregar_carrinho`
- será usado para recuperar um carrinho pelo código.

---

## Agora adicione estas funções em `main.py`

### 1) botão para abrir leitor na tela de produtos

Dentro de `tela_produtos()`, logo antes do botão do carrinho, adicione:

```python
ctk.CTkButton(
    header,
    text="📷 Ler QR",
    command=tela_qr_reader,
).pack(side="right", padx=5)
```

## Explicação linha por linha

`ctk.CTkButton(`
- começa a criação do botão.

`header,`
- o botão ficará no cabeçalho.

`text="📷 Ler QR",`
- define o texto do botão.

`command=tela_qr_reader,`
- ao clicar, abre a tela de leitura.

`).pack(side="right", padx=5)`
- desenha o botão do lado direito.

---

### 2) tela para ler QR

Adicione esta função:

```python
def tela_qr_reader():
    global tela_atual
    limpar_tela()
    tela_atual = ctk.CTkFrame(root)
    tela_atual.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkButton(tela_atual, text="← Voltar", command=tela_produtos).pack(pady=10)
    ctk.CTkLabel(
        tela_atual,
        text="📷 Ler QR Code",
        font=("Arial", 20, "bold"),
    ).pack(pady=20)
    ctk.CTkLabel(tela_atual, text="Digite o código:", font=("Arial", 14)).pack()

    codigo_input = ctk.CTkEntry(tela_atual, width=250)
    codigo_input.pack(pady=10)

    ctk.CTkButton(
        tela_atual,
        text="📥 Carregar",
        command=lambda: carregar_qr(codigo_input.get()),
    ).pack(pady=5)

    ctk.CTkLabel(tela_atual, text="─── OU ───").pack(pady=20)

    ctk.CTkButton(
        tela_atual,
        text="📁 Abrir Imagem",
        command=ler_imagem,
    ).pack(pady=5)

    ctk.CTkButton(
        tela_atual,
        text="📷 Usar Câmera",
        command=ler_camera,
    ).pack(pady=5)
```

## Explicação linha por linha

`codigo_input = ctk.CTkEntry(tela_atual, width=250)`
- cria o campo onde o usuário pode digitar o código.

`command=lambda: carregar_qr(codigo_input.get())`
- quando clicar no botão, pega o texto digitado e chama a função de carregamento.

`text="─── OU ───"`
- mostra uma separação visual entre as opções.

`command=ler_imagem`
- ao clicar, abre um arquivo de imagem.

`command=ler_camera`
- ao clicar, abre a câmera.

---

### 3) função para carregar o carrinho pelo código

Adicione esta função:

```python
def carregar_qr(codigo):
    c = carregar_carrinho(codigo.strip().upper())
    if not c:
        messagebox.showerror("Erro", "Carrinho não encontrado!")
        return

    carrinho.clear()
    for item in c["itens"]:
        p = get_produto(item["id"])
        if p:
            carrinho[p["id"]] = {"produto": p, "qtd": item["qty"]}

    tela_carrinho()
```

## Explicação linha por linha

`codigo.strip().upper()`
- `strip()` remove espaços antes e depois.
- `upper()` converte para maiúsculo.

`c = carregar_carrinho(...)`
- tenta buscar o carrinho salvo.

`if not c:`
- verifica se não encontrou resultado.

`messagebox.showerror("Erro", "Carrinho não encontrado!")`
- mostra mensagem de erro.

`return`
- encerra a função.

`carrinho.clear()`
- limpa o carrinho atual antes de carregar o novo.

`for item in c["itens"]:`
- percorre os itens do carrinho salvo.

`p = get_produto(item["id"])`
- busca o produto completo no banco.

`if p:`
- garante que o produto existe no banco.

`carrinho[p["id"]] = {"produto": p, "qtd": item["qty"]}`
- recria o item no carrinho da aplicação.

`tela_carrinho()`
- abre a tela do carrinho já carregado.

---

### 4) ler QR de uma imagem

Adicione esta função:

```python
def ler_imagem():
    f = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg")])
    if f:
        try:
            from pyzbar.pyzbar import decode

            d = decode(cv2.imread(f))
            if d:
                carregar_qr(d[0].data.decode())
            else:
                messagebox.showerror("Erro", "QR Code não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
```

## Explicação linha por linha

`filedialog.askopenfilename(...)`
- abre a janela para escolher arquivo.

`filetypes=[("Imagens", "*.png *.jpg")]`
- limita a seleção para PNG e JPG.

`if f:`
- verifica se o usuário escolheu algum arquivo.

`from pyzbar.pyzbar import decode`
- importa a função que lê QR Code.

`cv2.imread(f)`
- abre a imagem usando OpenCV.

`d = decode(...)`
- tenta decodificar o QR Code da imagem.

`if d:`
- verifica se encontrou algum QR.

`d[0].data.decode()`
- pega o texto do primeiro QR encontrado.

`carregar_qr(...)`
- usa o texto lido para carregar o carrinho.

`messagebox.showerror(...)`
- mostra erro se não encontrar QR ou se acontecer exceção.

---

### 5) ler QR pela câmera

Adicione esta função:

```python
def ler_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Câmera não disponível!")
        return

    try:
        from pyzbar.pyzbar import decode

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            d = decode(frame)
            if d:
                cap.release()
                cv2.destroyAllWindows()
                carregar_qr(d[0].data.decode())
                return

            cv2.imshow("Câmera - ESC para sair", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cap.release()
        cv2.destroyAllWindows()
```

## Explicação linha por linha

`cap = cv2.VideoCapture(0)`
- abre a câmera padrão do computador.

`if not cap.isOpened():`
- verifica se a câmera abriu corretamente.

`while True:`
- cria um loop contínuo para ler os frames da câmera.

`ok, frame = cap.read()`
- captura um frame da câmera.

`if not ok:`
- se falhar, sai do loop.

`d = decode(frame)`
- tenta ler QR Code naquele frame.

`if d:`
- se encontrou QR Code.

`cap.release()`
- libera a câmera.

`cv2.destroyAllWindows()`
- fecha a janela da câmera.

`carregar_qr(d[0].data.decode())`
- pega o texto lido e carrega o carrinho.

`cv2.imshow("Câmera - ESC para sair", frame)`
- mostra o vídeo da câmera.

`if cv2.waitKey(1) & 0xFF == 27:`
- fecha ao apertar `ESC`.
- `27` é o código da tecla ESC.

`finally:`
- garante fechamento da câmera, mesmo se der erro.

---

# Parte 7 — Adicionar filtro de pesquisa na tela 1

## O que vamos fazer

Agora sim vamos adicionar o filtro de pesquisa na tela de produtos.
Essa parte fica separada de propósito, como você pediu.

---

## Ajuste no `database.py`

A função `get_produtos` deve ficar assim:

```python
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
```

## Explicação linha por linha

`def get_produtos(filtro=""):`
- agora a função recebe um filtro opcional.
- se nada for enviado, o valor padrão é texto vazio.

`if filtro:`
- verifica se o usuário digitou algo.

`"SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome"`
- busca produtos cujo nome contenha o texto digitado.

`(f"%{filtro}%",),`
- monta o padrão do `LIKE`.
- `%texto%` significa “contém texto em qualquer posição”.

`else:`
- se o filtro estiver vazio.

`cur.execute("SELECT * FROM produtos ORDER BY nome")`
- busca todos os produtos normalmente.

---

## Ajuste no `main.py`

Dentro da função `tela_produtos()`, troque a parte da lista de produtos por esta:

```python
filtro_var = ctk.StringVar()

ctk.CTkEntry(
    tela_atual,
    textvariable=filtro_var,
    placeholder_text="🔍 Filtrar...",
).pack(fill="x", pady=5)

frame_produtos = ctk.CTkScrollableFrame(tela_atual)
frame_produtos.pack(fill="both", expand=True)


def atualizar_produtos(*args):
    for w in frame_produtos.winfo_children():
        w.destroy()

    for produto in get_produtos(filtro_var.get()):
        card = ctk.CTkFrame(frame_produtos, corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(
            card,
            text=f"{produto['nome']} - R$ {produto['preco']:.2f}",
            font=("Arial", 12),
        ).pack(side="left", padx=10, pady=8)

        ctk.CTkButton(
            card,
            text="🛒 Adicionar",
            width=100,
            command=lambda p=produto: adicionar(p),
        ).pack(side="right", padx=5, pady=5)


filtro_var.trace_add("write", atualizar_produtos)
atualizar_produtos()
```

## Explicação linha por linha

`filtro_var = ctk.StringVar()`
- cria uma variável de texto ligada ao campo de pesquisa.

`textvariable=filtro_var`
- conecta o campo visual com a variável.

`placeholder_text="🔍 Filtrar..."`
- mostra um texto de dica quando o campo está vazio.

`frame_produtos = ctk.CTkScrollableFrame(tela_atual)`
- cria a área onde os produtos serão desenhados.

`def atualizar_produtos(*args):`
- cria a função que atualiza a lista conforme o usuário digita.
- `*args` existe porque o `trace_add` envia argumentos automáticos.

`for w in frame_produtos.winfo_children():`
- percorre todos os widgets atuais da lista.

`w.destroy()`
- remove os widgets antigos da lista.

`for produto in get_produtos(filtro_var.get()):`
- busca os produtos já filtrados pelo texto digitado.

`filtro_var.get()`
- pega o texto atual da pesquisa.

`filtro_var.trace_add("write", atualizar_produtos)`
- toda vez que o texto mudar, chama `atualizar_produtos`.

`atualizar_produtos()`
- executa uma vez logo no início para já mostrar os produtos.

---

# Resultado final

Ao final, o projeto terá:

- `database.sql` com os produtos iniciais;
- `database.py` para criar o banco, listar produtos, buscar produto, salvar carrinho e carregar carrinho;
- `main.py` com:
  - tela de produtos;
  - tela de carrinho;
  - compartilhamento por QR/código;
  - leitura de QR por texto, imagem ou câmera;
  - filtro de pesquisa.

---

# Observações importantes

## 1) Arquivos gerados automaticamente

Quando rodar o projeto, estes arquivos aparecem sozinhos:

- `shareproducts.db`
- `carrinhos.json`

Você **não precisa criar esses dois manualmente**.

## 2) Como executar

Na pasta do projeto:

```bash
python main.py
```

## 3) Se a leitura de QR não funcionar

Normalmente o problema é dependência do `pyzbar` ou acesso à câmera.
Nesse caso, teste primeiro a leitura digitando o código manualmente.

---

# Resumo da ordem certa

1. criar a pasta e os arquivos vazios;
2. montar o banco com `database.sql` e `database.py`;
3. criar a tela de produtos;
4. criar a tela do carrinho;
5. adicionar compartilhamento;
6. adicionar leitura do código/QR;
7. por último, adicionar o filtro de pesquisa.

