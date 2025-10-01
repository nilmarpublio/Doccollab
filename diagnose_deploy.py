#!/usr/bin/env python3
"""
Script de diagnóstico para deploy no PythonAnywhere
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

def check_file_exists(file_path):
    """Verificar se arquivo existe"""
    return os.path.exists(file_path)

def main():
    print("🔍 Iniciando diagnóstico do deploy DocCollab...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    print("\n📋 1. Verificando estrutura do projeto...")
    required_files = [
        "app.py",
        "models/version.py",
        "models/chat_message.py",
        "routes/chat.py",
        "templates/editor.html",
        "templates/pdf_viewer.html",
        "templates/version_history.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not check_file_exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos ausentes: {', '.join(missing_files)}")
        print("💡 Solução: Execute 'git pull origin main' para atualizar")
    else:
        print("✅ Estrutura do projeto OK")
    
    print("\n📋 2. Verificando Git...")
    success, stdout, stderr = run_command("git status")
    if success:
        print("✅ Git funcionando")
        print(f"📊 Status: {stdout.strip()}")
    else:
        print(f"❌ Erro no Git: {stderr}")
    
    print("\n📋 3. Verificando ambiente virtual...")
    success, stdout, stderr = run_command("which python")
    if "venv" in stdout:
        print("✅ Ambiente virtual ativo")
    else:
        print("⚠️  Ambiente virtual não ativo")
        print("💡 Solução: Execute 'source venv/bin/activate'")
    
    print("\n📋 4. Verificando dependências...")
    success, stdout, stderr = run_command("pip3.10 list | grep -i flask")
    if success and "Flask" in stdout:
        print("✅ Flask instalado")
    else:
        print("❌ Flask não encontrado")
        print("💡 Solução: Execute 'pip3.10 install --user -r requirements.txt'")
    
    success, stdout, stderr = run_command("pip3.10 list | grep -i socketio")
    if success and "Flask-SocketIO" in stdout:
        print("✅ Flask-SocketIO instalado")
    else:
        print("❌ Flask-SocketIO não encontrado")
        print("💡 Solução: Execute 'pip3.10 install --user -r requirements.txt'")
    
    print("\n📋 5. Verificando banco de dados...")
    if check_file_exists("update_db_versions.py"):
        print("✅ Script de versões encontrado")
    else:
        print("❌ Script de versões não encontrado")
        print("💡 Solução: Execute 'git pull origin main'")
    
    if check_file_exists("update_db_chat.py"):
        print("✅ Script de chat encontrado")
    else:
        print("❌ Script de chat não encontrado")
        print("💡 Solução: Execute 'git pull origin main'")
    
    print("\n📋 6. Verificando arquivo .env...")
    if check_file_exists(".env"):
        print("✅ Arquivo .env encontrado")
    else:
        print("❌ Arquivo .env não encontrado")
        print("💡 Solução: Execute 'cp env_pythonanywhere_production.txt .env'")
    
    print("\n📋 7. Testando importação da aplicação...")
    try:
        from app import create_app
        app, socketio = create_app()
        print("✅ Aplicação pode ser importada")
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        print("💡 Solução: Verifique se todas as dependências estão instaladas")
    
    print("\n🎯 DIAGNÓSTICO CONCLUÍDO!")
    print("\n📋 Próximos passos recomendados:")
    print("1. Execute 'git pull origin main' para atualizar o código")
    print("2. Execute 'source venv/bin/activate' para ativar o ambiente virtual")
    print("3. Execute 'pip3.10 install --user -r requirements.txt' para instalar dependências")
    print("4. Execute 'python3.10 update_db_versions.py' para atualizar banco")
    print("5. Execute 'python3.10 update_db_chat.py' para atualizar banco")
    print("6. Configure o WSGI no PythonAnywhere")
    print("7. Reinicie a aplicação")
    print("\n🚀 DocCollab estará pronto para produção!")

if __name__ == "__main__":
    main()
