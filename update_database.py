import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configurar Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doccollab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar instância única do SQLAlchemy
db = SQLAlchemy(app)

# Definir modelos
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

with app.app_context():
    print("🔄 Atualizando banco de dados...")
    
    # Dropar e recriar todas as tabelas
    db.drop_all()
    db.create_all()
    
    print("✅ Banco de dados atualizado com sucesso!")
    print("📊 Tabelas criadas:")
    print("   - users")
    print("   - projects (com campo updated_at)")
    
    # Criar usuário admin
    from werkzeug.security import generate_password_hash
    
    admin_email = 'admin@doccollab.com'
    admin_password = 'admin123'
    
    admin_user = User(
        name='Administrador',
        email=admin_email,
        password_hash=generate_password_hash(admin_password),
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.session.add(admin_user)
    db.session.commit()
    
    print(f"👤 Usuário admin criado: {admin_email}")
    print("🔑 Senha: admin123")
    print("\n🚀 Agora você pode executar 'python app.py'")
