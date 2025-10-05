from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Criar app Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurações
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doccollab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar instância única do SQLAlchemy
db = SQLAlchemy(app)

# Definir modelos
class User(db.Model, LoginManager.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Configurar LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('auth/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        if not email or not password:
            flash('Preencha email e senha.', 'warning')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Email ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

        if not user.is_active:
            flash('Conta desativada.', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        flash(f'Bem-vindo, {user.name}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)

@app.route('/create-project', methods=['POST'])
@login_required
def create_project():
    # Verificar limite de projetos (1 para usuários gratuitos)
    project_count = Project.query.filter_by(user_id=current_user.id).count()
    if project_count >= 1:
        flash('Limite de projetos atingido. Faça upgrade do plano.', 'warning')
        return redirect(url_for('dashboard'))
    
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Nome do projeto é obrigatório.', 'warning')
        return redirect(url_for('dashboard'))
    
    project = Project(
        name=name,
        description=description,
        user_id=current_user.id
    )
    
    db.session.add(project)
    db.session.commit()
    
    flash('Projeto criado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('index'))

# Criar banco de dados e usuário admin
with app.app_context():
    db.create_all()
    
    # Criar usuário admin se não existir
    admin_user = User.query.filter_by(email='admin@doccollab.com').first()
    if not admin_user:
        admin_user = User(
            name='Administrador',
            email='admin@doccollab.com',
            password_hash=generate_password_hash('admin123'),
            is_active=True
        )
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Usuário admin criado!")
        print("📧 Email: admin@doccollab.com")
        print("🔑 Senha: admin123")

if __name__ == '__main__':
    print("🚀 Iniciando aplicação...")
    print("📧 Email: admin@doccollab.com")
    print("🔑 Senha: admin123")
    print("🌐 Acesse: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
