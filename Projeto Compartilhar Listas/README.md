# 📦 Share Products

Sistema de compartilhamento de produtos via QR Code desenvolvido em Python com CustomTkinter.

## 🎯 Funcionalidades

### ✅ Implementado

1. **Tela Principal (Listagem de Produtos)**
   - ✓ Exibição de todos os produtos cadastrados
   - ✓ Filtro de pesquisa por nome
   - ✓ Botão para adicionar produtos ao carrinho
   - ✓ Indicador visual de produtos já adicionados
   - ✓ Contador de itens no carrinho

2. **Tela do Carrinho**
   - ✓ Lista de produtos selecionados
   - ✓ Controles de quantidade (+ / - / edição manual)
   - ✓ Cálculo automático de valores (unitário, total por produto, total geral)
   - ✓ Botão para remover itens
   - ✓ Botão para limpar carrinho
   - ✓ Botão para compartilhar via QR Code

3. **Tela de QR Code**
   - ✓ Geração de código único de compartilhamento
   - ✓ Exibição do QR Code visual
   - ✓ Botão para copiar código
   - ✓ Opção de criar novo carrinho

4. **Tela de Leitura de QR Code**
   - ✓ Input para digitar código manualmente
   - ✓ Leitura de QR Code de imagem
   - ✓ Leitura de QR Code via câmera
   - ✓ Carregamento automático do carrinho compartilhado

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** - Linguagem de programação
- **CustomTkinter** - Interface gráfica moderna
- **SQLite** - Banco de dados
- **qrcode** - Geração de QR Codes
- **OpenCV + pyzbar** - Leitura de QR Codes
- **PyInstaller** - Conversão para executável

## 📋 Pré-requisitos

### Windows
```bash
# Python 3.10 ou superior
# Git (opcional)
```

### Linux/Mac
```bash
# Python 3.10 ou superior
# zbar (para leitura de QR Code)
sudo apt-get install libzbar0  # Ubuntu/Debian
brew install zbar  # macOS
```

## 🚀 Instalação

### 1. Clone o repositório (ou baixe os arquivos)
```bash
git clone <url-do-repositorio>
cd share-products
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Inicialize o banco de dados
O banco de dados será criado automaticamente na primeira execução.

## ▶️ Como Executar

### Modo Desenvolvimento
```bash
python main.py
```

### Gerar Executável
```bash
# Windows
pyinstaller --onefile --windowed --name="ShareProducts" --icon=icon.ico main.py

# Linux/Mac
pyinstaller --onefile --windowed --name="ShareProducts" main.py
```

O executável será gerado na pasta `dist/`.

## 📖 Como Usar

### 1. Adicionar Produtos ao Carrinho
1. Na tela principal, navegue pelos produtos
2. Use o filtro para buscar produtos específicos
3. Clique em "🛒 Adicionar" para adicionar ao carrinho
4. Clique em "🛒 Carrinho (X)" para ver seu carrinho

### 2. Gerenciar Carrinho
1. No carrinho, ajuste as quantidades usando +/- ou editando diretamente
2. Veja os valores individuais e o total geral
3. Remova itens com o botão 🗑️
4. Limpe todo o carrinho com "🗑️ Limpar Carrinho"

### 3. Compartilhar Carrinho
1. No carrinho, clique em "📤 Compartilhar"
2. Um código único será gerado
3. Compartilhe o código ou o QR Code com outros usuários

### 4. Importar Carrinho Compartilhado
1. Na tela principal, clique em "📷 Ler QR Code"
2. Escolha uma das opções:
   - **Digite o código**: Cole ou digite o código manualmente
   - **Abrir Imagem**: Selecione uma imagem do QR Code
   - **Usar Câmera**: Use a webcam para escanear o QR Code

## 🗂️ Estrutura do Projeto

```
share-products/
│
├── main.py              # Aplicação principal com interface
├── database.py          # Gerenciamento do banco de dados
├── database.sql         # Schema do banco de dados
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
│
└── shareproducts.db    # Banco de dados (criado automaticamente)
```

## 💾 Banco de Dados

### Tabelas

#### produtos
- `id`: ID único do produto
- `nome`: Nome do produto
- `descricao`: Descrição do produto
- `preco_unitario`: Preço unitário
- `imagem`: Caminho da imagem (futuro)
- `ativo`: Status do produto (1 = ativo)
- `data_criacao`: Data de criação

#### carrinhos
- `id`: ID único do carrinho
- `codigo_compartilhamento`: Código único para compartilhamento
- `nome_carrinho`: Nome do carrinho
- `valor_total`: Valor total do carrinho
- `data_criacao`: Data de criação

#### carrinho_itens
- `id`: ID único do item
- `carrinho_id`: Referência ao carrinho
- `produto_id`: Referência ao produto
- `quantidade`: Quantidade do produto
- `preco_unitario`: Preço unitário no momento da compra
- `valor_total`: Valor total do item

## 🎨 Capturas de Tela

### Tela Principal
- Lista de produtos com filtro
- Cards com nome, descrição e preço
- Botão de adicionar ao carrinho

### Tela do Carrinho
- Lista de itens selecionados
- Controles de quantidade
- Valores calculados automaticamente
- Total geral destacado

### Tela de QR Code
- Código de compartilhamento
- QR Code visual
- Botão de copiar

### Tela de Leitura
- Input manual de código
- Upload de imagem
- Scanner via câmera

## 🔧 Configurações

### Tema
O aplicativo usa tema escuro por padrão. Para alterar, modifique em `main.py`:
```python
ctk.set_appearance_mode("light")  # ou "dark" ou "system"
```

### Cores
As cores podem ser personalizadas modificando os parâmetros `fg_color` e `hover_color` nos botões.

## 🐛 Resolução de Problemas

### Erro ao abrir câmera
- Verifique se a câmera está conectada
- Verifique permissões do sistema
- No Linux, pode ser necessário adicionar seu usuário ao grupo `video`

### Erro ao ler QR Code de imagem
- Certifique-se de que a imagem contém um QR Code válido
- Tente com uma imagem de melhor qualidade
- Verifique se o zbar está instalado corretamente

### Banco de dados não inicializa
- Verifique se o arquivo `database.sql` está no mesmo diretório
- Verifique permissões de escrita na pasta

## 🔄 Melhorias Futuras

- [ ] Categorias de produtos
- [ ] Imagens de produtos
- [ ] Histórico de carrinhos
- [ ] Exportar/Importar lista em PDF
- [ ] Sincronização em nuvem
- [ ] Multi-idioma
- [ ] Temas personalizáveis
- [ ] Favoritos/Listas salvas
- [ ] Busca avançada com filtros
- [ ] Estatísticas de uso

## 📝 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 👨‍💻 Autor

Desenvolvido com ❤️ usando Python e CustomTkinter

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Versão:** 1.0.0  
**Data:** 2025
