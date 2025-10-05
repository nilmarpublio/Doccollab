#!/usr/bin/env python3
"""
Script para criar usuário admin no banco local
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from werkzeug.security import generate_password_hash

def create_admin_user():
    app, socketio = create_app()
    
    with app.app_context():
        from app import db
        from models.user import User
        
        # Verificar se já existe um usuário admin
        admin_user = User.query.filter_by(email='admin@doccollab.com').first()
        
        if not admin_user:
            print("🔧 Criando usuário admin...")
            
            # Criar usuário admin com todos os campos obrigatórios
            admin_user = User(
                name='Administrador',
                email='admin@doccollab.com',
                password_hash=generate_password_hash('admin123'),
                is_active=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("📧 Email: admin@doccollab.com")
            print("🔑 Senha: admin123")
        else:
            print("ℹ️ Usuário admin já existe!")
            print(f"📧 Email: {admin_user.email}")
            print(f"👤 Nome: {admin_user.name}")
            print(f"✅ Ativo: {admin_user.is_active}")
            
            # Atualizar senha para garantir que está correta
            admin_user.password_hash = generate_password_hash('admin123')
            db.session.commit()
            print("🔑 Senha atualizada para: admin123")
            
        # Listar todos os usuários
        users = User.query.all()
        print(f"\n📊 Total de usuários no banco: {len(users)}")
        for user in users:
            print(f"  - {user.name} ({user.email}) - Ativo: {user.is_active}")

if __name__ == '__main__':
    create_admin_user()
