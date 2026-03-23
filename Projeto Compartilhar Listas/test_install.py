"""
Script de teste para verificar instalação do Share Products
"""
import sys

def test_imports():
    """Testa se todos os módulos necessários estão instalados"""
    
    print("🔍 Verificando instalação do Share Products...\n")
    
    modules = {
        "customtkinter": "Interface gráfica",
        "qrcode": "Geração de QR Code",
        "PIL": "Processamento de imagens",
        "cv2": "OpenCV - Leitura de QR Code",
        "pyzbar": "Decodificador de QR Code",
        "pyperclip": "Copiar para clipboard",
        "numpy": "Processamento numérico",
        "sqlite3": "Banco de dados"
    }
    
    errors = []
    success_count = 0
    
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"✅ {module:20} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module:20} - {description} - ERRO: {e}")
            errors.append(module)
    
    print(f"\n{'='*60}")
    print(f"Resultado: {success_count}/{len(modules)} módulos instalados")
    
    if errors:
        print(f"\n❌ Módulos faltando: {', '.join(errors)}")
        print("\n💡 Para instalar os módulos faltantes:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Todas as dependências estão instaladas!")
        return True

def test_database():
    """Testa se o banco de dados pode ser inicializado"""
    
    print(f"\n{'='*60}")
    print("🔍 Testando banco de dados...\n")
    
    try:
        from database import Database
        
        # Criar banco de teste
        db = Database("test.db")
        
        # Testar operações básicas
        produtos = db.get_produtos()
        print(f"✅ Banco de dados inicializado: {len(produtos)} produtos cadastrados")
        
        # Limpar banco de teste
        import os
        if os.path.exists("test.db"):
            os.remove("test.db")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar banco de dados: {e}")
        return False

def test_qrcode():
    """Testa geração de QR Code"""
    
    print(f"\n{'='*60}")
    print("🔍 Testando geração de QR Code...\n")
    
    try:
        import qrcode
        from PIL import Image
        
        # Gerar QR Code de teste
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data("TEST123")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        print("✅ QR Code gerado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar QR Code: {e}")
        return False

def test_camera():
    """Testa acesso à câmera"""
    
    print(f"\n{'='*60}")
    print("🔍 Testando acesso à câmera...\n")
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✅ Câmera acessível!")
            cap.release()
            return True
        else:
            print("⚠️  Câmera não detectada (opcional)")
            return True  # Não é erro crítico
    except Exception as e:
        print(f"⚠️  Erro ao acessar câmera (opcional): {e}")
        return True  # Não é erro crítico

def main():
    """Função principal de teste"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         SHARE PRODUCTS - VERIFICAÇÃO DE INSTALAÇÃO        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"Python version: {sys.version}\n")
    
    # Executar testes
    test1 = test_imports()
    test2 = test_database() if test1 else False
    test3 = test_qrcode() if test1 else False
    test4 = test_camera() if test1 else False
    
    # Resultado final
    print(f"\n{'='*60}")
    print("📊 RESULTADO FINAL\n")
    
    if test1 and test2 and test3:
        print("✅ TUDO OK! O Share Products está pronto para uso!")
        print("\n🚀 Para iniciar a aplicação, execute:")
        print("   python main.py")
    else:
        print("❌ Alguns problemas foram encontrados.")
        print("\n💡 Soluções:")
        print("   1. Execute: pip install -r requirements.txt")
        print("   2. Consulte o arquivo INSTALACAO.md")
        print("   3. Verifique o README.md para mais detalhes")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
