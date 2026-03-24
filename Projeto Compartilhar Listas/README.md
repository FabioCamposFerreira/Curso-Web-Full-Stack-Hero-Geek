# 📦 Share Products - Versão Simplificada# 📦 Share Products



> Aplicação para compartilhar listas de compras via QR CodeSistema de compartilhamento de produtos via QR Code desenvolvido em Python com CustomTkinter.



**Status**: ✅ Totalmente Funcional | **Redução**: 69% de código | **Python**: 3.8+## 🎯 Funcionalidades



---### ✅ Implementado



## ✨ Características1. **Tela Principal (Listagem de Produtos)**

   - ✓ Exibição de todos os produtos cadastrados

✅ **Listagem de produtos** com filtro em tempo real     - ✓ Filtro de pesquisa por nome

✅ **Carrinho de compras** - Adicionar, remover, alterar quantidade     - ✓ Botão para adicionar produtos ao carrinho

✅ **Compartilhamento via QR Code** - Gera código único     - ✓ Indicador visual de produtos já adicionados

✅ **Leitura de QR Code** - 3 formas: código, arquivo ou câmera     - ✓ Contador de itens no carrinho

✅ **Interface moderna** - Tema escuro com customtkinter  

✅ **Código simplificado** - Sem classes, apenas funções  2. **Tela do Carrinho**

   - ✓ Lista de produtos selecionados

---   - ✓ Controles de quantidade (+ / - / edição manual)

   - ✓ Cálculo automático de valores (unitário, total por produto, total geral)

## 🚀 Início Rápido   - ✓ Botão para remover itens

   - ✓ Botão para limpar carrinho

### 1. Instalar Dependências   - ✓ Botão para compartilhar via QR Code



```bash3. **Tela de QR Code**

cd "Projeto Compartilhar Listas"   - ✓ Geração de código único de compartilhamento

pip install -r requirements.txt   - ✓ Exibição do QR Code visual

```   - ✓ Botão para copiar código

   - ✓ Opção de criar novo carrinho

### 2. Executar Aplicação

4. **Tela de Leitura de QR Code**

```bash   - ✓ Input para digitar código manualmente

python main.py   - ✓ Leitura de QR Code de imagem

```   - ✓ Leitura de QR Code via câmera

   - ✓ Carregamento automático do carrinho compartilhado

### 3. Executar Testes (opcional)

## 🛠️ Tecnologias Utilizadas

```bash

python test_funcionalidades.py- **Python 3.10+** - Linguagem de programação

```- **CustomTkinter** - Interface gráfica moderna

- **SQLite** - Banco de dados

---- **qrcode** - Geração de QR Codes

- **OpenCV + pyzbar** - Leitura de QR Codes

## 📊 Arquitetura- **PyInstaller** - Conversão para executável



### Comparação: Antes vs Depois## 📋 Pré-requisitos



| Métrica | Antes | Depois | Mudança |### Windows

|---------|-------|--------|---------|```bash

| Linhas de código | 1.088 | 336 | -69% ✓ |# Python 3.10 ou superior

| Classes | 1 | 0 | -100% ✓ |# Git (opcional)

| Tabelas SQL | 3 | 1 | -67% ✓ |```

| Complexidade | Alta | Baixa | +70% ✓ |

| Funcionalidades | 100% | 100% | 0% ✓ |### Linux/Mac

```bash

### Estrutura de Dados# Python 3.10 ou superior

# zbar (para leitura de QR Code)

```sudo apt-get install libzbar0  # Ubuntu/Debian

database.sql (18 linhas)brew install zbar  # macOS

  ↓```

  └─→ Tabela: produtos (id, nome, preco)

## 🚀 Instalação

main.py (250 linhas)

  ├─→ database.py (68 linhas)### 1. Clone o repositório (ou baixe os arquivos)

  │    ├─ get_produtos()```bash

  │    ├─ get_produto()git clone <url-do-repositorio>

  │    ├─ salvar_carrinho()cd share-products

  │    └─ carregar_carrinho()```

  │

  ├─→ carrinhos.json (auto-criado)### 2. Crie um ambiente virtual (recomendado)

  │    └─ {"CODIGO": {"itens": [...], "total": 0.00}}```bash

  │python -m venv venv

  └─→ shareproducts.db (SQLite, auto-criado)

       └─ produtos table# Windows

```venv\Scripts\activate



---# Linux/Mac

source venv/bin/activate

## 🎯 Como Usar```



### Tela Principal### 3. Instale as dependências

```bash

1. **Filtrar Produtos** 🔍pip install -r requirements.txt

   - Digite na barra de pesquisa```

   - Atualiza em tempo real

### 4. Inicialize o banco de dados

2. **Adicionar ao Carrinho** 🛒O banco de dados será criado automaticamente na primeira execução.

   - Clique em "Adicionar"

   - Notificação de confirmação## ▶️ Como Executar



3. **Ver Carrinho**### Modo Desenvolvimento

   - Botão no header mostra quantidade```bash

   - "🛒 Carrinho (2)"python main.py

```

### Gerenciar Carrinho

### Gerar Executável

1. **Aumentar/Diminuir Quantidade**```bash

   - Use botões + e -# Windows

   - Ou digite manualmentepyinstaller --onefile --windowed --name="ShareProducts" --icon=icon.ico main.py



2. **Remover Item** 🗑️# Linux/Mac

   - Clique no ícone de lixeirapyinstaller --onefile --windowed --name="ShareProducts" main.py

```

3. **Ver Total**

   - Mostrado em verde na parte inferiorO executável será gerado na pasta `dist/`.



### Compartilhar## 📖 Como Usar



1. **Clique em "📤 Compartilhar"**### 1. Adicionar Produtos ao Carrinho

   - Gera código único de 12 caracteres1. Na tela principal, navegue pelos produtos

   - Cria QR Code visual2. Use o filtro para buscar produtos específicos

3. Clique em "🛒 Adicionar" para adicionar ao carrinho

2. **Copiar Código**4. Clique em "🛒 Carrinho (X)" para ver seu carrinho

   - "📋 Copiar" para compartilhar texto

   - Salve a imagem do QR Code### 2. Gerenciar Carrinho

1. No carrinho, ajuste as quantidades usando +/- ou editando diretamente

3. **Novo Carrinho**2. Veja os valores individuais e o total geral

   - Clique em "🛒 Novo Carrinho"3. Remova itens com o botão 🗑️

   - Volta à tela principal4. Limpe todo o carrinho com "🗑️ Limpar Carrinho"



### Carregar Carrinho Compartilhado### 3. Compartilhar Carrinho

1. No carrinho, clique em "📤 Compartilhar"

**Opção 1: Digitando Código**2. Um código único será gerado

1. Clique em "📷 Ler QR"3. Compartilhe o código ou o QR Code com outros usuários

2. Cole o código de 12 caracteres

3. Clique em "📥 Carregar"### 4. Importar Carrinho Compartilhado

1. Na tela principal, clique em "📷 Ler QR Code"

**Opção 2: De Arquivo**2. Escolha uma das opções:

1. Clique em "📁 Abrir Imagem"   - **Digite o código**: Cole ou digite o código manualmente

2. Selecione imagem com QR Code   - **Abrir Imagem**: Selecione uma imagem do QR Code

3. Carregado automaticamente   - **Usar Câmera**: Use a webcam para escanear o QR Code



**Opção 3: De Câmera**## 🗂️ Estrutura do Projeto

1. Clique em "📷 Usar Câmera"

2. Aponte para QR Code```

3. Detecta automaticamenteshare-products/

│

---├── main.py              # Aplicação principal com interface

├── database.py          # Gerenciamento do banco de dados

## 📁 Estrutura de Arquivos├── database.sql         # Schema do banco de dados

├── requirements.txt     # Dependências do projeto

```├── README.md           # Este arquivo

Projeto Compartilhar Listas/│

├── main.py                      # Interface gráfica (funções)└── shareproducts.db    # Banco de dados (criado automaticamente)

├── database.py                  # Banco de dados (funções)```

├── database.sql                 # Schema SQL (1 tabela)

├── requirements.txt             # Dependências Python## 💾 Banco de Dados

├── README.md                    # Este arquivo

├── SIMPLIFICACAO.md             # Documento de mudanças### Tabelas

├── test_funcionalidades.py      # Suite de testes

├── test_db.py                   # Teste de BD#### produtos

│- `id`: ID único do produto

├── shareproducts.db             # SQLite (auto-criado)- `nome`: Nome do produto

└── carrinhos.json               # Carrinhos (auto-criado)- `descricao`: Descrição do produto

```- `preco_unitario`: Preço unitário

- `imagem`: Caminho da imagem (futuro)

---- `ativo`: Status do produto (1 = ativo)

- `data_criacao`: Data de criação

## 📦 Dependências

#### carrinhos

```bash- `id`: ID único do carrinho

# Instaladas via requirements.txt- `codigo_compartilhamento`: Código único para compartilhamento

- `nome_carrinho`: Nome do carrinho

customtkinter>=5.2.0      # Interface gráfica moderna- `valor_total`: Valor total do carrinho

qrcode[pil]>=8.0          # Geração de QR Code- `data_criacao`: Data de criação

Pillow>=10.4.0            # Manipulação de imagens

opencv-python>=4.10.0     # Câmera e processamento#### carrinho_itens

pyzbar==0.1.9             # Decodificação de QR- `id`: ID único do item

pyperclip>=1.9.0          # Clipboard- `carrinho_id`: Referência ao carrinho

numpy>=1.26.0             # Arrays (requerido por OpenCV)- `produto_id`: Referência ao produto

```- `quantidade`: Quantidade do produto

- `preco_unitario`: Preço unitário no momento da compra

---- `valor_total`: Valor total do item



## 🧪 Testes## 🎨 Capturas de Tela



### Executar Suite de Testes### Tela Principal

- Lista de produtos com filtro

```bash- Cards com nome, descrição e preço

python test_funcionalidades.py- Botão de adicionar ao carrinho

```

### Tela do Carrinho

Testa:- Lista de itens selecionados

- ✓ Inicialização do banco- Controles de quantidade

- ✓ Listagem de produtos- Valores calculados automaticamente

- ✓ Filtro de produtos- Total geral destacado

- ✓ Busca por ID

- ✓ Geração de código### Tela de QR Code

- ✓ Salvamento de carrinho- Código de compartilhamento

- ✓ Carregamento de carrinho- QR Code visual

- ✓ Arquivo JSON- Botão de copiar



### Teste Manual de BD### Tela de Leitura

- Input manual de código

```bash- Upload de imagem

python test_db.py- Scanner via câmera

```

## 🔧 Configurações

---

### Tema

## 🔧 ConfiguraçãoO aplicativo usa tema escuro por padrão. Para alterar, modifique em `main.py`:

```python

### Alterar Temactk.set_appearance_mode("light")  # ou "dark" ou "system"

```

Em `main.py`, na função `main()`:

### Cores

```pythonAs cores podem ser personalizadas modificando os parâmetros `fg_color` e `hover_color` nos botões.

ctk.set_appearance_mode("dark")        # light ou dark

ctk.set_default_color_theme("blue")    # blue, green, etc## 🐛 Resolução de Problemas

```

### Erro ao abrir câmera

### Alterar Tamanho da Janela- Verifique se a câmera está conectada

- Verifique permissões do sistema

Em `main.py`, na função `main()`:- No Linux, pode ser necessário adicionar seu usuário ao grupo `video`



```python### Erro ao ler QR Code de imagem

root.geometry("800x600")  # largura x altura- Certifique-se de que a imagem contém um QR Code válido

```- Tente com uma imagem de melhor qualidade

- Verifique se o zbar está instalado corretamente

### Adicionar/Remover Produtos

### Banco de dados não inicializa

Edite `database.sql`:- Verifique se o arquivo `database.sql` está no mesmo diretório

- Verifique permissões de escrita na pasta

```sql

INSERT INTO produtos (nome, preco) VALUES## 🔄 Melhorias Futuras

('Novo Produto', 19.99),

('Outro Produto', 29.99);- [ ] Categorias de produtos

```- [ ] Imagens de produtos

- [ ] Histórico de carrinhos

Depois delete `shareproducts.db` para recriar.- [ ] Exportar/Importar lista em PDF

- [ ] Sincronização em nuvem

---- [ ] Multi-idioma

- [ ] Temas personalizáveis

## 🐛 Solução de Problemas- [ ] Favoritos/Listas salvas

- [ ] Busca avançada com filtros

### Erro: "pyzbar não encontrado"- [ ] Estatísticas de uso



Windows:## 📝 Licença

```bash

pip install pipwinEste projeto é de código aberto e está disponível para uso livre.

pipwin install zbar

```## 👨‍💻 Autor



macOS:Desenvolvido com ❤️ usando Python e CustomTkinter

```bash

brew install zbar## 🤝 Contribuições

```

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

Linux:

```bash---

sudo apt-get install libzbar0

```**Versão:** 1.0.0  

**Data:** 2025

### Erro: "Câmera não disponível"

- Verifique se a câmera está conectada
- Conceda permissão ao programa (Windows)
- Use arquivo ou código ao invés

### Banco corrompido

```bash
# Remova e deixe recriar:
del shareproducts.db
python main.py
```

### "main.py não encontrado"

```bash
# Certifique-se de estar no diretório correto:
cd "Projeto Compartilhar Listas"
python main.py
```

---

## 📚 Estrutura do Código

### database.py

```python
init_db()                    # Cria/inicializa banco
get_produtos(filtro="")      # Lista com filtro
get_produto(id)              # Busca por ID
gerar_codigo()               # Código único (12 chars)
salvar_carrinho(itens)       # Salva em JSON
carregar_carrinho(codigo)    # Carrega de JSON
```

### main.py

```python
atualizar_tela()             # Função principal de UI
  ├─ tela_produtos()         # Tela 1: Lista
  ├─ tela_carrinho()         # Tela 2: Carrinho
  ├─ tela_qr()               # Tela 3: QR Code
  └─ tela_qr_reader()        # Tela 4: Leitura

main()                       # Entry point
```

---

## 💡 Princípios de Design

✅ **Simplicidade** - Menos linhas = menos bugs  
✅ **Funcionalidade** - Tudo que precisa, nada mais  
✅ **Legibilidade** - Código fácil de entender  
✅ **Aprendizado** - Bom para iniciantes em Python  
✅ **Manutenibilidade** - Sem classe = sem OOP overhead  

---

## 🎓 O Que Você Aprende

- ✓ SQLite com Python
- ✓ Interface gráfica com customtkinter
- ✓ Geração de QR Codes
- ✓ Leitura de câmera com OpenCV
- ✓ Manipulação de JSON
- ✓ Programação funcional
- ✓ Boas práticas de simplicidade

---

## 📞 Suporte

Encontrou um bug? Abra uma issue ou entre em contato.

---

## 📝 Licença

Projeto educacional - Use e modifique livremente!

---

## 🎉 Desenvolvido com ❤️

Simplificado para máxima legibilidade e aprendizado.

**Versão**: 1.0 Simplificada | **Data**: 2026-03-24
