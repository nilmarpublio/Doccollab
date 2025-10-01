#!/usr/bin/env python3
"""
Script de correção de erro de importação para PythonAnywhere
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

def create_file(file_path, content):
    """Criar arquivo com conteúdo"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Erro ao criar arquivo {file_path}: {e}")
        return False

def main():
    print("🔧 Iniciando correção de erro de importação...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    print("\n📋 1. Verificando dependências...")
    dependencies = [
        "flask",
        "flask-socketio",
        "flask-sqlalchemy",
        "flask-babel",
        "flask-login",
        "python-dotenv"
    ]
    
    for dep in dependencies:
        success, stdout, stderr = run_command(f"pip3.10 list | grep -i {dep}")
        if success and dep in stdout.lower():
            print(f"✅ {dep} instalado")
        else:
            print(f"❌ {dep} não encontrado")
            print(f"💡 Instalando {dep}...")
            success, stdout, stderr = run_command(f"pip3.10 install --user {dep}")
            if success:
                print(f"✅ {dep} instalado com sucesso")
            else:
                print(f"❌ Falha ao instalar {dep}: {stderr}")
    
    print("\n📋 2. Verificando arquivos críticos...")
    critical_files = [
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
    for file_path in critical_files:
        if not check_file_exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos ausentes: {', '.join(missing_files)}")
        print("💡 Criando arquivos ausentes...")
        
        # Criar models/version.py se ausente
        if "models/version.py" in missing_files:
            content = '''from datetime import datetime
from models import db

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(500), nullable=True)

    project = db.relationship('Project', backref=db.backref('versions', lazy=True))

    def __repr__(self):
        return f'<Version {self.version_number} for Project {self.project_id}>'
'''
            if create_file("models/version.py", content):
                print("✅ models/version.py criado")
        
        # Criar models/chat_message.py se ausente
        if "models/chat_message.py" in missing_files:
            content = '''from datetime import datetime
from models import db

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project = db.relationship('Project', backref=db.backref('chat_messages', lazy=True))
    user = db.relationship('User', backref=db.backref('chat_messages', lazy=True))

    def __repr__(self):
        return f'<ChatMessage {self.id} from User {self.user_id}>'
'''
            if create_file("models/chat_message.py", content):
                print("✅ models/chat_message.py criado")
    else:
        print("✅ Todos os arquivos críticos existem")
    
    print("\n📋 3. Testando importações...")
    
    # Testar importações básicas
    test_imports = [
        ("flask", "Flask"),
        ("flask_socketio", "SocketIO"),
        ("flask_sqlalchemy", "SQLAlchemy"),
        ("flask_babel", "Babel"),
        ("flask_login", "LoginManager"),
        ("dotenv", "load_dotenv")
    ]
    
    for module, class_name in test_imports:
        try:
            exec(f"import {module}")
            print(f"✅ {module} OK")
        except ImportError as e:
            print(f"❌ {module} não encontrado: {e}")
        except Exception as e:
            print(f"⚠️  {module} erro: {e}")
    
    print("\n📋 4. Testando importação da aplicação...")
    try:
        from app import create_app
        print("✅ Importação da aplicação OK")
        
        # Testar criação da aplicação
        app, socketio = create_app()
        print("✅ Criação da aplicação OK")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se todos os arquivos existem")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")
        return False
    
    print("\n📋 5. Verificando banco de dados...")
    try:
        from app import create_app
        from models import db
        app, socketio = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Banco de dados OK")
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        print("💡 Execute 'python3.10 update_db_versions.py' e 'python3.10 update_db_chat.py'")
        return False
    
    print("\n🎉 Correção de erro de importação concluída!")
    print("\n📋 Próximos passos:")
    print("1. Configure o WSGI no PythonAnywhere")
    print("2. Configure os Static Files")
    print("3. Reinicie a aplicação")
    print("4. Acesse: https://123nilmarcastro.pythonanywhere.com")
    print("\n🚀 DocCollab está pronto para produção!")

if __name__ == "__main__":
    main()
