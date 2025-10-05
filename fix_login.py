#!/usr/bin/env python3
"""
Script para parar a aplicação e criar usuário admin
"""
import os
import sys
import subprocess

# Parar processos Python
try:
    subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True)
    print("✅ Processos Python parados")
except:
    print("ℹ️ Nenhum processo Python encontrado")

# Aguardar um pouco
import time
time.sleep(2)

# Criar usuário admin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from werkzeug.security import generate_password_hash

def create_admin_user():
    app, socketio = create_app()
    
    with app.app_context():
        from app import db
        from models.user import User
        from models.subscription import Subscription, PlanType
        
        try:
            # Verificar se já existe um usuário admin
            admin_user = User.query.filter_by(email='admin@doccollab.com').first()
            
            if not admin_user:
                print("🔧 Criando usuário admin...")
                
                # Criar usuário admin
                admin_user = User(
                    name='Administrador',
                    email='admin@doccollab.com',
                    password_hash=generate_password_hash('admin123'),
                    is_active=True
                )
                
                db.session.add(admin_user)
                db.session.flush()  # Para obter o ID
                
                # Criar subscription gratuita
                subscription = Subscription(
                    user_id=admin_user.id,
                    plan_type=PlanType.FREE
                )
                db.session.add(subscription)
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
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_admin_user()
    print("\n🚀 Agora você pode executar: python app.py")
