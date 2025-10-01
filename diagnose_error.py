#!/usr/bin/env python3
"""
Script de diagnóstico de erro para PythonAnywhere
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
    print("🔍 Iniciando diagnóstico de erro do DocCollab...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    print("\n📋 1. Verificando estrutura do projeto...")
    required_files = [
        "app.py",
        "models/__init__.py",
        "models/user.py",
        "models/project.py",
        "models/subscription.py",
        "models/version.py",
        "models/chat_message.py",
        "routes/__init__.py",
        "routes/main.py",
        "routes/auth.py",
        "routes/chat.py",
        "services/latex_compiler.py",
        "utils/file_ops.py",
        "utils/permissions.py"
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
    
    print("\n📋 2. Verificando dependências...")
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
        print("💡 Solução: Execute 'pip3.10 install --user flask-socketio'")
    
    success, stdout, stderr = run_command("pip3.10 list | grep -i sqlalchemy")
    if success and "Flask-SQLAlchemy" in stdout:
        print("✅ Flask-SQLAlchemy instalado")
    else:
        print("❌ Flask-SQLAlchemy não encontrado")
        print("💡 Solução: Execute 'pip3.10 install --user flask-sqlalchemy'")
    
    print("\n📋 3. Verificando arquivo .env...")
    if check_file_exists(".env"):
        print("✅ Arquivo .env encontrado")
    else:
        print("❌ Arquivo .env não encontrado")
        print("💡 Solução: Execute 'cp env_pythonanywhere_production.txt .env'")
    
    print("\n📋 4. Testando importação da aplicação...")
    try:
        from app import create_app
        print("✅ Importação da aplicação OK")
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Solução: Verifique se todas as dependências estão instaladas")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        print("💡 Solução: Verifique se todos os arquivos existem")
        return False
    
    print("\n📋 5. Testando criação da aplicação...")
    try:
        from app import create_app
        app, socketio = create_app()
        print("✅ Criação da aplicação OK")
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        print("💡 Solução: Verifique se o banco de dados está configurado")
        return False
    
    print("\n📋 6. Verificando banco de dados...")
    try:
        from app import create_app
        from models import db
        app, socketio = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Banco de dados OK")
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        print("💡 Solução: Execute 'python3.10 update_db_versions.py' e 'python3.10 update_db_chat.py'")
        return False
    
    print("\n📋 7. Verificando configuração WSGI...")
    wsgi_file = "/var/www/123nilmarcastro_pythonanywhere_com_wsgi.py"
    if check_file_exists(wsgi_file):
        print("✅ Arquivo WSGI encontrado")
    else:
        print("❌ Arquivo WSGI não encontrado")
        print("💡 Solução: Configure o WSGI no PythonAnywhere")
    
    print("\n🎯 DIAGNÓSTICO CONCLUÍDO!")
    print("\n📋 Próximos passos recomendados:")
    print("1. Execute 'pip3.10 install --user -r requirements.txt' para instalar dependências")
    print("2. Execute 'python3.10 update_db_versions.py' para atualizar banco")
    print("3. Execute 'python3.10 update_db_chat.py' para atualizar banco")
    print("4. Configure o WSGI no PythonAnywhere")
    print("5. Configure os Static Files no PythonAnywhere")
    print("6. Reinicie a aplicação")
    print("\n🚀 DocCollab estará pronto para produção!")

if __name__ == "__main__":
    main()
