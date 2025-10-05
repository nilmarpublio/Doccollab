#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar e configurar
from app import create_app
from werkzeug.security import generate_password_hash

app, socketio = create_app()

with app.app_context():
    from app import db
    from models.user import User
    from models.subscription import Subscription, PlanType
    
    # Deletar usuário admin existente se houver
    admin_user = User.query.filter_by(email='admin@doccollab.com').first()
    if admin_user:
        db.session.delete(admin_user)
        db.session.commit()
        print("🗑️ Usuário admin antigo removido")
    
    # Criar novo usuário admin
    print("🔧 Criando usuário admin...")
    admin_user = User(
        name='Administrador',
        email='admin@doccollab.com',
        password_hash=generate_password_hash('admin123'),
        is_active=True
    )
    
    db.session.add(admin_user)
    db.session.flush()
    
    # Criar subscription
    subscription = Subscription(
        user_id=admin_user.id,
        plan_type=PlanType.FREE
    )
    db.session.add(subscription)
    db.session.commit()
    
    print("✅ Usuário admin criado!")
    print("📧 Email: admin@doccollab.com")
    print("🔑 Senha: admin123")
    print("\n🚀 Agora execute: python app.py")
