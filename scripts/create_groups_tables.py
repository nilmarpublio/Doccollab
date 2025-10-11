"""
Script para criar tabelas de grupos no banco de dados
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.group import Group
from models.group_member import GroupMember
from models.group_document import GroupDocument
from models.group_message import GroupMessage

def create_tables():
    """Criar tabelas de grupos"""
    with app.app_context():
        print("Criando tabelas de grupos...")
        
        # Criar todas as tabelas
        db.create_all()
        
        print("✅ Tabelas criadas com sucesso!")
        print("\nTabelas criadas:")
        print("  - groups")
        print("  - group_members")
        print("  - group_documents")
        print("  - group_messages")

if __name__ == '__main__':
    create_tables()

