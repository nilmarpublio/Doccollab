#!/usr/bin/python3
"""
Script para configurar o banco de dados no PythonAnywhere
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
        from models.subscription import Subscription, PlanType
        admin_email = os.getenv('SEED_EMAIL', 'admin@test.com')
        admin_password = os.getenv('SEED_PASSWORD', 'admin123')
        
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(name='Admin', email=admin_email)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.flush()  # Get the ID
            
            # Create paid subscription for admin
            admin_subscription = Subscription(
                user_id=admin.id,
                plan_type=PlanType.PAID
            )
            db.session.add(admin_subscription)
            db.session.commit()
            print(f"✅ Usuário admin criado: {admin_email} (Paid Plan)")
        else:
            print(f"ℹ️  Usuário admin já existe: {admin_email}")
            
            # Ensure admin has a subscription
            if not hasattr(existing_admin, 'subscription') or not existing_admin.subscription:
                admin_subscription = Subscription(
                    user_id=existing_admin.id,
                    plan_type=PlanType.PAID
                )
                db.session.add(admin_subscription)
                db.session.commit()
                print(f"✅ Subscription criada para admin: {admin_email}")

if __name__ == "__main__":
    setup_database()


