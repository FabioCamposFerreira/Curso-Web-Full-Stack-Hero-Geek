"""
Script para gerar executável do Share Products
"""
import os
import subprocess
import shutil

def build_executable():
    """Gera o executável usando PyInstaller"""
    
    print("🔨 Iniciando build do Share Products...")
    
    # Limpar builds anteriores
    if os.path.exists("build"):
        print("🗑️  Removendo pasta build anterior...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("🗑️  Removendo pasta dist anterior...")
        shutil.rmtree("dist")
    
    if os.path.exists("ShareProducts.spec"):
        print("🗑️  Removendo spec anterior...")
        os.remove("ShareProducts.spec")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",              # Um único arquivo
        "--windowed",             # Sem console (Windows)
        "--name=ShareProducts",   # Nome do executável
        "--add-data=database.sql:.",  # Incluir arquivo SQL
        "main.py"
    ]
    
    print("📦 Executando PyInstaller...")
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build concluído com sucesso!")
        print(f"📁 Executável disponível em: dist/ShareProducts")
        
        # Copiar database.sql para dist
        if os.path.exists("database.sql"):
            shutil.copy("database.sql", "dist/database.sql")
            print("✅ Arquivo database.sql copiado para dist/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante o build: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    build_executable()
