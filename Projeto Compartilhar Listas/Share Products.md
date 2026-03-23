# 📋 CHECKLIST - Share Products

##  Telas 

1. **Listagem** - Veja todos os produtos
2. **Carrinho** - Gerencie sua lista
3. **QR Code** - Compartilhe
4. **Ler QR** - Importe listas


## Como Usar

**1. Adicionar produtos**
- Abra a aplicação
- Clique em "🛒 Adicionar" em 3-4 produtos
- Veja o contador aumentar

**2. Ver carrinho**
- Clique em "🛒 Carrinho (X)"
- Ajuste quantidades se quiser
- Veja o total calculado

**3. Compartilhar**
- Clique em "📤 Compartilhar"
- Copie o código gerado
- Pronto para compartilhar!

**4. Importar (teste)**
- Volte à tela inicial
- Clique em "📷 Ler QR Code"
- Cole o código que você copiou
- Clique em "📥 Carregar"
- Sua lista foi importada! ✅
  

##  TAREFAS (Tasks)

### 1. Criar banco de dados (.sql)
- ✓ Esquema completo de tabelas
- ✓ Tabela `produtos` com 20 produtos de exemplo
- ✓ Tabela `carrinhos` para compartilhamento
- ✓ Tabela `carrinho_itens` para itens
- ✓ Índices para performance
- ✓ Relacionamentos configurados

### 2. Criar Tela 1 (Principal)
- ✓ Listagem de todos os produtos
- ✓ Cards com nome, descrição e preço
- ✓ Botão para adicionar ao carrinho
- ✓ Indicador visual de itens já adicionados
- ✓ Contador de itens no carrinho
- ✓ Botão para acessar carrinho
- ✓ Botão para ler QR Code
- ✓ Layout responsivo em grid (2 colunas)

### 3. Criar Tela 2 (Carrinho)
- ✓ Lista de produtos selecionados
- ✓ Exibição de preço unitário
- ✓ Controles de quantidade (+ / -)
- ✓ Campo editável de quantidade
- ✓ Cálculo de valor total por produto
- ✓ Cálculo de valor geral do carrinho
- ✓ Botão para remover itens individuais
- ✓ Botão para limpar todo o carrinho
- ✓ Botão para compartilhar (gerar QR Code)
- ✓ Botão de voltar

### 4. Criar Tela 3 (QR Code)
- ✓ Geração de código único
- ✓ Exibição do código alfanumérico
- ✓ Geração e exibição do QR Code visual
- ✓ Botão para copiar código
- ✓ Botão para criar novo carrinho
- ✓ Mensagens de sucesso
- ✓ Botão de voltar ao carrinho

### 5. Criar Tela 4 (Ler QR Code)
- ✓ Input para digitar código manualmente
- ✓ Botão para carregar por código
- ✓ Botão para abrir imagem do QR Code
- ✓ Leitura de QR Code de arquivo de imagem
- ✓ Botão para usar câmera
- ✓ Leitura de QR Code via webcam
- ✓ Detecção automática do QR Code
- ✓ Carregamento automático do carrinho
- ✓ Botão de voltar

### 6. Adicionar filtro na Tela 1
- ✓ Campo de busca por nome
- ✓ Atualização em tempo real
- ✓ Botão para limpar filtro
- ✓ Busca case-insensitive

### 7. Funcionalidades Extras Implementadas
- ✓ Sistema completo de banco de dados
- ✓ Gerenciamento de carrinho em memória
- ✓ Cálculos automáticos de valores
- ✓ Validações de quantidade
- ✓ Mensagens de feedback
- ✓ Navegação entre telas
- ✓ Persistência de dados
- ✓ Códigos únicos de compartilhamento
- ✓ Suporte a múltiplos formatos de imagem
- ✓ Detecção automática de QR Code
- ✓ Copiar para clipboard
- ✓ Interface moderna com CustomTkinter
- ✓ Tema escuro
- ✓ Layout responsivo
- ✓ Tratamento de erros

## 📦 Estrutura do Projeto

### `main.py`
- ✅ `main.py` - Aplicação principal (4 telas completas)
  
### `database.py`
- ✅ `database.py` - Gerenciamento do banco de dados

### `database.sql`
- ✅ `database.sql` - Schema do banco + dados de exemplo

### `requirements.txt`
- ✅ `requirements.txt` - Dependências do projeto

### `ReadMe.md`
 Documentação completa do projeto





## 🎯 PRÓXIMOS PASSOS

### Para Começar a Usar:

1. **Instalar Dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar Aplicação**
   ```bash
   python main.py
   ```

### Para Gerar Executável:

1. **Executar Build**
   ```bash
   python build.py
   ```
   
2. **Executável Gerado em**
   ```
   dist/ShareProducts.exe  (Windows)
   dist/ShareProducts      (Linux/Mac)
   ```
