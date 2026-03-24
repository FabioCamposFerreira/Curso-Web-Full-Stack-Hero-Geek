from database import get_produtos

produtos = get_produtos()
print(f"✅ {len(produtos)} produtos carregados\n")
for p in produtos[:5]:
    print(f"  - {p['nome']}: R$ {p['preco']:.2f}")
print(f"  ... e mais {len(produtos)-5} produtos")
