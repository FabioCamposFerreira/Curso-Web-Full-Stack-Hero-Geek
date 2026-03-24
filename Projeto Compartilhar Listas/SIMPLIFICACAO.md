# 📝 Simplificação do Projeto Share Products

## ✅ Mudanças Realizadas

### 1. **database.sql** (Reduzido de 60 linhas para 18 linhas)
- ❌ Removidas tabelas: `carrinhos` e `carrinho_itens`
- ✅ Mantida apenas: Tabela `produtos` com colunas essenciais (`id`, `nome`, `preco`)
- ✅ Carrinhos agora são salvos em **JSON** (`carrinhos.json`)

### 2. **database.py** (Reduzido de 163 linhas para 68 linhas)
- ❌ Removida classe `Database`
- ✅ Convertidas para **funções simples**:
  - `init_db()` - Inicializa banco de dados
  - `get_produtos(filtro)` - Lista produtos
  - `get_produto(id)` - Busca um produto
  - `gerar_codigo()` - Cria código único
  - `salvar_carrinho(itens)` - Salva carrinho em JSON
  - `carregar_carrinho(codigo)` - Carrega carrinho do JSON

### 3. **main.py** (Reduzido de 865 linhas para ~250 linhas)
- ❌ Removida classe `ShareProductsApp`
- ✅ Refatorado para **funções aninhadas** com estado global
- ✅ Mantidas todas as funcionalidades:
  - ✅ Listagem de produtos com filtro
  - ✅ Carrinho com adicionar/remover/alterar quantidade
  - ✅ Geração de QR Code
  - ✅ Compartilhamento via código
  - ✅ Leitura de QR Code (digitando código, arquivo ou câmera)

## 📊 Comparação

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Linhas de código | ~1.088 | ~336 |
| **Redução** | - | **69%** ✨ |
| Classes | 1 | 0 |
| Funções | 30+ | 15 |
| Armazenamento | SQLite (3 tabelas) | SQLite (1 tabela) + JSON |
| Complexidade | Alta | Baixa ✓ |

## 🚀 Como Usar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

## 📦 Estrutura Simplificada

```
├── main.py              # Interface gráfica (funções aninhadas)
├── database.py          # Funções de BD (sem classes)
├── database.sql         # Schema simples (1 tabela)
├── carrinhos.json       # Carrinhos compartilhados (criado automaticamente)
├── shareproducts.db     # Banco de dados SQLite (criado automaticamente)
└── requirements.txt     # Dependências
```

## ⚡ Benefícios da Simplificação

✅ **Código mais legível** - Fácil de entender e manter
✅ **Menos linhas** - 69% de redução
✅ **Menos complexidade** - Sem classes abstratas
✅ **Mantém funcionalidades** - Tudo ainda funciona
✅ **Mais rápido** - Menos overhead de orientação a objetos
✅ **Mais acessível** - Melhor para aprendizado

## 🔄 Fluxo da Aplicação

1. **Tela Principal** → Lista produtos com filtro
2. **Adicionar ao Carrinho** → Estado salvo em memória
3. **Visualizar Carrinho** → Editar quantidades
4. **Compartilhar** → Gera código e QR Code (salva em JSON)
5. **Ler QR Code** → Carrega carrinho de outro usuário
   - Via código digitado
   - Via imagem (arquivo)
   - Via câmera em tempo real

## 💾 Armazenamento

- **Produtos**: SQLite (`shareproducts.db`)
- **Carrinhos Compartilhados**: JSON (`carrinhos.json`)
- **Carrinho Atual**: Memória do programa

## 🎯 Próximos Passos (Opcional)

Se quiser simplificar ainda mais:
- Remover leitura de câmera (deixar apenas código/imagem)
- Usar arquivo CSV ao invés de SQLite para produtos
- Remover filtro de produtos
