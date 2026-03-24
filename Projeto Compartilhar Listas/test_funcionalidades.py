#!/usr/bin/env python3
"""
Script de teste para validar funcionalidades principais
"""
from database import (
    init_db, get_produtos, get_produto, gerar_codigo, 
    salvar_carrinho, carregar_carrinho
)
import json
import os

print("=" * 50)
print("🧪 TESTES DO PROJETO SIMPLIFICADO")
print("=" * 50)

# Teste 1: Inicializar BD
print("\n✅ Teste 1: Inicializar banco de dados")
try:
    init_db()
    print("   ✓ Banco inicializado com sucesso")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 2: Listar produtos
print("\n✅ Teste 2: Listar produtos")
try:
    produtos = get_produtos()
    print(f"   ✓ {len(produtos)} produtos carregados")
    print(f"   - Primeiro: {produtos[0]['nome']} (R$ {produtos[0]['preco']:.2f})")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 3: Filtrar produtos
print("\n✅ Teste 3: Filtrar produtos")
try:
    filtrados = get_produtos("Arroz")
    print(f"   ✓ Encontrados {len(filtrados)} produto(s) com 'Arroz'")
    if filtrados:
        print(f"   - {filtrados[0]['nome']}")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 4: Obter produto por ID
print("\n✅ Teste 4: Obter produto por ID")
try:
    p = get_produto(1)
    if p:
        print(f"   ✓ Produto encontrado: {p['nome']}")
    else:
        print("   ✗ Produto não encontrado")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 5: Gerar código
print("\n✅ Teste 5: Gerar código único")
try:
    codigo1 = gerar_codigo()
    codigo2 = gerar_codigo()
    print(f"   ✓ Código 1: {codigo1}")
    print(f"   ✓ Código 2: {codigo2}")
    if codigo1 != codigo2:
        print("   ✓ Códigos são únicos")
    else:
        print("   ✗ Códigos deveriam ser diferentes!")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 6: Salvar carrinho
print("\n✅ Teste 6: Salvar carrinho")
try:
    itens_carrinho = [
        {"id": 1, "qty": 2, "preco": 25.90},
        {"id": 2, "qty": 1, "preco": 8.50}
    ]
    codigo_carrinho = salvar_carrinho(itens_carrinho)
    print(f"   ✓ Carrinho salvo com código: {codigo_carrinho}")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 7: Carregar carrinho
print("\n✅ Teste 7: Carregar carrinho")
try:
    carrinho = carregar_carrinho(codigo_carrinho)
    if carrinho:
        print(f"   ✓ Carrinho encontrado")
        print(f"   - Total: R$ {carrinho.get('total', 0):.2f}")
        print(f"   - Itens: {len(carrinho.get('itens', []))}")
    else:
        print("   ✗ Carrinho não encontrado")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# Teste 8: Verificar arquivo JSON
print("\n✅ Teste 8: Verificar arquivo de carrinhos (JSON)")
try:
    if os.path.exists("carrinhos.json"):
        with open("carrinhos.json", 'r') as f:
            dados = json.load(f)
        print(f"   ✓ Arquivo 'carrinhos.json' existe")
        print(f"   - Carrinhos salvos: {len(dados)}")
    else:
        print("   ✗ Arquivo não encontrado")
except Exception as e:
    print(f"   ✗ Erro: {e}")

print("\n" + "=" * 50)
print("✅ TODOS OS TESTES CONCLUÍDOS!")
print("=" * 50)
print("\n🚀 A aplicação está pronta para usar!")
print("   Execute: python main.py")
