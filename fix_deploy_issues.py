#!/usr/bin/env python3
"""
Script para corrigir problemas comuns de deploy
DocCollab - Deploy Final
"""

import os
import sys
import shutil
import subprocess

def run_command(command, cwd=None):
    """Executar comando e retornar resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_env_file():
    """Criar arquivo .env para produção"""
    env_content = """# Configuração de Produção - DocCollab
SECRET_KEY=doccollab-super-secret-key-2024-production-change-this
DEBUG=False
TESTING=False

# Banco de dados
DATABASE_URL=sqlite:///doccollab.db

# Compilação LaTeX
PDFLATEX=/usr/bin/pdflatex

# Usuário administrador
SEED_EMAIL=admin@doccollab.com
SEED_PASSWORD=admin123456

# SocketIO Configuration
SOCKETIO_ASYNC_MODE=eventlet

# Configurações de produção
FLASK_ENV=production
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600

# Configurações de upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads

# Configurações de sessão
PERMANENT_SESSION_LIFETIME=86400

# Configurações de segurança
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Configurações de CORS
CORS_ORIGINS=*
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=Content-Type,Authorization

# Configurações específicas do DocCollab
PROJECTS_ROOT=projects
TRASH_ROOT=trash
VERSIONS_ROOT=versions

# Configurações de planos
FREE_PLAN_MAX_PROJECTS=1
FREE_PLAN_MAX_FILES=1
PAID_PLAN_MAX_PROJECTS=999999
PAID_PLAN_MAX_FILES=999999

# Configurações de chat
CHAT_MESSAGE_LIMIT=500
CHAT_HISTORY_LIMIT=1000
CHAT_TYPING_TIMEOUT=3000

# Configurações de versões
VERSION_SNAPSHOT_ON_COMPILE=True
VERSION_MAX_HISTORY=50
VERSION_AUTO_CLEANUP=True

# Configurações de compilação LaTeX
LATEX_MAX_RUNS=2
LATEX_TIMEOUT=30
LATEX_OUTPUT_DIR=output

# Configurações de internacionalização
BABEL_DEFAULT_LOCALE=pt
BABEL_SUPPORTED_LOCALES=pt,en,es
BABEL_TRANSLATION_DIRECTORIES=translations
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ Arquivo .env criado")

def fix_wsgi_file():
    """Corrigir arquivo WSGI"""
    wsgi_content = '''#!/usr/bin/python3
import sys
import os

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Cria a aplicação Flask e SocketIO
app, socketio = create_app()

# Para produção, usamos apenas o app Flask
# O SocketIO será configurado via static files
application = app

if __name__ == "__main__":
    # Para desenvolvimento local
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
'''
    
    with open('wsgi.py', 'w', encoding='utf-8') as f:
        f.write(wsgi_content)
    print("✅ Arquivo wsgi.py corrigido")

def create_directories():
    """Criar diretórios necessários"""
    dirs = ['projects', 'trash', 'versions', 'logs', 'static/uploads']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✅ Diretórios criados")

def check_dependencies():
    """Verificar e instalar dependências"""
    print("📦 Verificando dependências...")
    
    # Verificar se requirements.txt existe
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt não encontrado")
        return False
    
    # Instalar dependências
    success, stdout, stderr = run_command("pip install -r requirements.txt")
    if success:
        print("✅ Dependências instaladas")
        return True
    else:
        print(f"❌ Erro ao instalar dependências: {stderr}")
        return False

def test_application():
    """Testar se a aplicação pode ser importada"""
    print("🧪 Testando aplicação...")
    try:
        from app import create_app
        app, socketio = create_app()
        print("✅ Aplicação pode ser importada")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        return False

def create_deploy_script():
    """Criar script de deploy"""
    deploy_script = '''#!/bin/bash
# Script de Deploy DocCollab

echo "🚀 Iniciando deploy do DocCollab..."

# Ativar ambiente virtual (se existir)
if [ -d "venv" ]; then
    echo "📦 Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Executar scripts de atualização do banco
echo "🗄️ Atualizando banco de dados..."
python update_db_versions.py
python update_db_chat.py

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p projects trash versions logs static/uploads

# Configurar permissões
echo "🔐 Configurando permissões..."
chmod 755 wsgi.py
chmod -R 755 static/
chmod -R 755 templates/

echo "✅ Deploy concluído!"
echo "🌐 Acesse sua aplicação no navegador"
'''
    
    with open('deploy.sh', 'w', encoding='utf-8') as f:
        f.write(deploy_script)
    
    # Tornar executável no Linux/Mac
    if os.name != 'nt':
        os.chmod('deploy.sh', 0o755)
    
    print("✅ Script de deploy criado")

def main():
    print("🔧 Iniciando correção de problemas de deploy...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('app.py'):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    # 1. Criar arquivo .env
    print("\n📋 1. Configurando variáveis de ambiente...")
    create_env_file()
    
    # 2. Corrigir WSGI
    print("\n📋 2. Corrigindo arquivo WSGI...")
    fix_wsgi_file()
    
    # 3. Criar diretórios
    print("\n📋 3. Criando diretórios necessários...")
    create_directories()
    
    # 4. Verificar dependências
    print("\n📋 4. Verificando dependências...")
    if not check_dependencies():
        print("⚠️  Dependências não foram instaladas. Execute manualmente: pip install -r requirements.txt")
    
    # 5. Testar aplicação
    print("\n📋 5. Testando aplicação...")
    if not test_application():
        print("⚠️  Aplicação não pode ser importada. Verifique os erros acima.")
    
    # 6. Criar script de deploy
    print("\n📋 6. Criando script de deploy...")
    create_deploy_script()
    
    print("\n🎉 Correções aplicadas!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python update_db_versions.py")
    print("2. Execute: python update_db_chat.py")
    print("3. Configure o WSGI no seu provedor de hospedagem")
    print("4. Reinicie a aplicação")
    print("\n🚀 DocCollab estará pronto para produção!")

if __name__ == "__main__":
    main()

