-- Share Products Database Schema
-- SQLite Database Structure

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco_unitario REAL NOT NULL,
    imagem TEXT,
    ativo INTEGER DEFAULT 1,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Carrinhos Salvos (para compartilhamento)
CREATE TABLE IF NOT EXISTS carrinhos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_compartilhamento TEXT UNIQUE NOT NULL,
    nome_carrinho TEXT,
    valor_total REAL NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Itens do Carrinho
CREATE TABLE IF NOT EXISTS carrinho_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carrinho_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    valor_total REAL NOT NULL,
    FOREIGN KEY (carrinho_id) REFERENCES carrinhos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Inserindo produtos de exemplo
INSERT INTO produtos (nome, descricao, preco_unitario) VALUES
('Arroz Branco 5kg', 'Arroz tipo 1, pacote de 5kg', 25.90),
('Feijão Preto 1kg', 'Feijão preto tipo 1', 8.50),
('Óleo de Soja 900ml', 'Óleo de soja refinado', 7.20),
('Açúcar Cristal 1kg', 'Açúcar cristal', 4.30),
('Café Torrado 500g', 'Café torrado e moído', 15.80),
('Macarrão Espaguete 500g', 'Massa de sêmola', 4.90),
('Molho de Tomate 340g', 'Molho de tomate tradicional', 3.50),
('Leite Integral 1L', 'Leite UHT integral', 5.20),
('Farinha de Trigo 1kg', 'Farinha de trigo tipo 1', 5.60),
('Sal Refinado 1kg', 'Sal refinado iodado', 2.10),
('Biscoito Cream Cracker', 'Biscoito salgado 200g', 3.80),
('Margarina 500g', 'Margarina com sal', 8.90),
('Sabão em Pó 1kg', 'Sabão em pó para roupas', 12.50),
('Detergente 500ml', 'Detergente líquido neutro', 2.30),
('Papel Higiênico 4un', 'Papel higiênico folha dupla', 9.80),
('Sabonete 90g', 'Sabonete em barra', 2.50),
('Shampoo 350ml', 'Shampoo hidratante', 11.90),
('Creme Dental 90g', 'Creme dental branqueador', 5.40),
('Desinfetante 1L', 'Desinfetante multiuso', 6.80),
('Esponja de Aço', 'Esponja de aço pacote com 8', 4.20);
