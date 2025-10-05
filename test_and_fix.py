#!/usr/bin/env python3
"""
Script para testar e corrigir a aplicação
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app():
    print("🔧 Testando aplicação...")
    
    try:
        from app import create_app
        app, socketio = create_app()
        
        with app.app_context():
            from app import db
            from models.user import User
            from models.subscription import Subscription, PlanType
            
            print("✅ Aplicação carregada com sucesso!")
            
            # Verificar se há usuários
            users = User.query.all()
            print(f"📊 Usuários encontrados: {len(users)}")
            
            # Criar usuário admin se não existir
            admin_user = User.query.filter_by(email='admin@doccollab.com').first()
            
            if not admin_user:
                print("🔧 Criando usuário admin...")
                
                from werkzeug.security import generate_password_hash
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
            else:
                print("ℹ️ Usuário admin já existe!")
                # Atualizar senha
                from werkzeug.security import generate_password_hash
                admin_user.password_hash = generate_password_hash('admin123')
                db.session.commit()
                print("🔑 Senha atualizada!")
            
            print("\n📧 Email: admin@doccollab.com")
            print("🔑 Senha: admin123")
            print("\n🚀 Aplicação pronta! Execute: python app.py")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_app()
