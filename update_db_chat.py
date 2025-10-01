#!/usr/bin/env python3
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
        print("\n🎉 Funcionalidade de chat colaborativo disponível!")
        print("📋 Funcionalidades adicionadas:")
        print("   - Chat em tempo real via WebSocket")
        print("   - Salas por projeto")
        print("   - Indicadores de usuários online")
        print("   - Histórico persistente de mensagens")
        print("   - Indicador de digitação")
    else:
        print("\n❌ Falha na atualização do banco de dados")
        sys.exit(1)