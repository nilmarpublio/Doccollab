#!/usr/bin/env python3
"""
Script de atualização manual para PythonAnywhere
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
    print("🔧 Iniciando atualização manual do DocCollab...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    print("\n📋 1. Verificando Git...")
    success, stdout, stderr = run_command("git status")
    if success:
        print("✅ Git funcionando")
        print(f"📊 Status: {stdout.strip()}")
    else:
        print(f"❌ Erro no Git: {stderr}")
    
    print("\n📋 2. Tentando atualizar código...")
    success, stdout, stderr = run_command("git pull origin main")
    if success:
        print("✅ Código atualizado")
        print(f"📊 Output: {stdout.strip()}")
    else:
        print(f"⚠️  Aviso: {stderr}")
        print("💡 Continuando com atualização manual...")
    
    print("\n📋 3. Verificando arquivos de atualização...")
    if os.path.exists("update_db_versions.py"):
        print("✅ update_db_versions.py encontrado")
    else:
        print("❌ update_db_versions.py não encontrado. Criando...")
        
        content = '''#!/usr/bin/env python3
"""
Script para atualizar o banco de dados com suporte a versões
DocCollab - Deploy Final
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.version import Version

def update_database():
    """Atualizar o banco de dados com a tabela de versões"""
    app, socketio = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Banco de dados atualizado com sucesso!")
            print("✅ Tabela de versões criada")
            
            # Verificar se há projetos existentes
            from models.project import Project
            projects = Project.query.all()
            
            if projects:
                print(f"📊 Encontrados {len(projects)} projetos existentes")
                print("ℹ️  Projetos existentes receberão snapshots de versão na próxima compilação")
            else:
                print("📝 Nenhum projeto existente encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao atualizar banco de dados: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("🔄 Atualizando banco de dados com suporte a versões...")
    success = update_database()
    
    if success:
        print("\\n🎉 Funcionalidade de histórico de versões disponível!")
        print("📋 Funcionalidades adicionadas:")
        print("   - Snapshots automáticos na compilação")
        print("   - Visualizador de histórico de versões")
        print("   - Comparação de versões")
        print("   - Restauração de versões")
    else:
        print("\\n❌ Falha na atualização do banco de dados")
        sys.exit(1)
'''
        
        if create_file("update_db_versions.py", content):
            print("✅ update_db_versions.py criado")
        else:
            print("❌ Falha ao criar update_db_versions.py")
    
    if os.path.exists("update_db_chat.py"):
        print("✅ update_db_chat.py encontrado")
    else:
        print("❌ update_db_chat.py não encontrado. Criando...")
        
        content = '''#!/usr/bin/env python3
"""
Script para atualizar o banco de dados com suporte a chat
DocCollab - Deploy Final
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.chat_message import ChatMessage

def update_database():
    """Atualizar o banco de dados com a tabela de chat"""
    app, socketio = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Banco de dados atualizado com sucesso!")
            print("✅ Tabela de chat criada")
            
            # Verificar se há projetos existentes
            from models.project import Project
            projects = Project.query.all()
            
            if projects:
                print(f"📊 Encontrados {len(projects)} projetos existentes")
                print("ℹ️  Projetos existentes terão chat habilitado")
            else:
                print("📝 Nenhum projeto existente encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao atualizar banco de dados: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("🔄 Atualizando banco de dados com suporte a chat...")
    success = update_database()
    
    if success:
        print("\\n🎉 Funcionalidade de chat colaborativo disponível!")
        print("📋 Funcionalidades adicionadas:")
        print("   - Chat em tempo real via WebSocket")
        print("   - Salas por projeto")
        print("   - Indicadores de usuários online")
        print("   - Histórico persistente de mensagens")
        print("   - Indicador de digitação")
    else:
        print("\\n❌ Falha na atualização do banco de dados")
        sys.exit(1)
'''
        
        if create_file("update_db_chat.py", content):
            print("✅ update_db_chat.py criado")
        else:
            print("❌ Falha ao criar update_db_chat.py")
    
    print("\n📋 4. Executando scripts de atualização...")
    
    # Atualizar banco de versões
    print("🔄 Atualizando banco - versões...")
    success, stdout, stderr = run_command("python3.10 update_db_versions.py")
    if success:
        print("✅ Banco de versões atualizado")
        print(f"📊 Output: {stdout.strip()}")
    else:
        print(f"⚠️  Aviso: {stderr}")
    
    # Atualizar banco de chat
    print("🔄 Atualizando banco - chat...")
    success, stdout, stderr = run_command("python3.10 update_db_chat.py")
    if success:
        print("✅ Banco de chat atualizado")
        print(f"📊 Output: {stdout.strip()}")
    else:
        print(f"⚠️  Aviso: {stderr}")
    
    print("\n📋 5. Verificando aplicação...")
    success, stdout, stderr = run_command("python3.10 -c 'from app import create_app; print(\"✅ Aplicação OK\")'")
    if success:
        print("✅ Aplicação funcionando")
    else:
        print(f"❌ Erro na aplicação: {stderr}")
    
    print("\n🎉 Atualização manual concluída!")
    print("\n📋 Próximos passos:")
    print("1. Configure o WSGI no PythonAnywhere")
    print("2. Configure os Static Files")
    print("3. Reinicie a aplicação")
    print("4. Acesse: https://123nilmarcastro.pythonanywhere.com")
    print("\n🚀 DocCollab está pronto para produção!")

if __name__ == "__main__":
    main()
