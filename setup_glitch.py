#!/usr/bin/python3
"""
Script para configurar o banco de dados no Glitch
Execute este script após fazer o upload dos arquivos
"""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db

def setup_database():
    """Configura o banco de dados"""
    app = create_app()
    
    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        print("✅ Banco de dados configurado com sucesso!")
        
        # Cria usuário admin se não existir
        from models.user import User
        admin_email = os.getenv('SEED_EMAIL', 'admin@glitch.com')
        admin_password = os.getenv('SEED_PASSWORD', 'admin123')
        
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(name='Admin', email=admin_email, plan='paid')
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Usuário admin criado: {admin_email}")
        else:
            print(f"ℹ️  Usuário admin já existe: {admin_email}")

if __name__ == "__main__":
    setup_database()









