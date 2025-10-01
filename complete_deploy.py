#!/usr/bin/env python3
"""
Script completo de deploy para PythonAnywhere
DocCollab - Deploy Final
"""

import sys
import os
import subprocess

def run_command(command):
    """Executar comando e retornar resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Iniciando deploy completo do DocCollab...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    print("\n📋 Passo 1: Ativando ambiente virtual...")
    success, stdout, stderr = run_command("source venv/bin/activate && echo 'Virtual environment activated'")
    if success:
        print("✅ Ambiente virtual ativado")
    else:
        print("⚠️  Aviso: Não foi possível ativar o ambiente virtual")
    
    print("\n📋 Passo 2: Instalando dependências...")
    success, stdout, stderr = run_command("pip3.10 install --user -r requirements.txt")
    if success:
        print("✅ Dependências instaladas")
    else:
        print(f"❌ Erro ao instalar dependências: {stderr}")
        return False
    
    print("\n📋 Passo 3: Atualizando banco de dados - Versões...")
    success, stdout, stderr = run_command("python3.10 update_db_versions.py")
    if success:
        print("✅ Tabela de versões criada")
    else:
        print(f"⚠️  Aviso: {stderr}")
    
    print("\n📋 Passo 4: Atualizando banco de dados - Chat...")
    success, stdout, stderr = run_command("python3.10 update_db_chat.py")
    if success:
        print("✅ Tabela de chat criada")
    else:
        print(f"⚠️  Aviso: {stderr}")
    
    print("\n📋 Passo 5: Verificando arquivo .env...")
    if os.path.exists(".env"):
        print("✅ Arquivo .env encontrado")
    else:
        print("⚠️  Arquivo .env não encontrado. Copiando exemplo...")
        success, stdout, stderr = run_command("cp env_pythonanywhere_production.txt .env")
        if success:
            print("✅ Arquivo .env criado a partir do exemplo")
        else:
            print("❌ Erro ao criar arquivo .env")
    
    print("\n📋 Passo 6: Verificando estrutura do projeto...")
    required_files = ["app.py", "models", "routes", "templates", "static"]
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos/diretórios ausentes: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Estrutura do projeto OK")
    
    print("\n🎉 Deploy concluído com sucesso!")
    print("\n📋 Próximos passos manuais:")
    print("1. Configure o WSGI no PythonAnywhere:")
    print("   - Vá para Web → WSGI configuration file")
    print("   - Use o conteúdo do arquivo wsgi_pythonanywhere.py")
    print("\n2. Configure os Static Files:")
    print("   - URL: /static/ → /home/123nilmarcastro/DocCollab/static")
    print("   - URL: /socket.io/ → /home/123nilmarcastro/DocCollab/static")
    print("\n3. Reinicie a aplicação:")
    print("   - Vá para Web → Reload")
    print("   - Acesse: https://123nilmarcastro.pythonanywhere.com")
    print("\n🚀 DocCollab está pronto para produção!")

if __name__ == "__main__":
    main()
