#!/usr/bin/env python3
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
        print("\n🎉 Funcionalidade de histórico de versões disponível!")
        print("📋 Funcionalidades adicionadas:")
        print("   - Snapshots automáticos na compilação")
        print("   - Visualizador de histórico de versões")
        print("   - Comparação de versões")
        print("   - Restauração de versões")
    else:
        print("\n❌ Falha na atualização do banco de dados")
        sys.exit(1)