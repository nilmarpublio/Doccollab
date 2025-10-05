from flask import Flask, request, session, redirect, url_for, send_from_directory, render_template, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_babel import Babel, gettext as _
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Criar instância única do SQLAlchemy
db = SQLAlchemy()

# Definir modelos diretamente aqui para evitar conflitos
class User(db.Model, LoginManager.UserMixin):
    __tablename__ = 'users'
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

    def get_subscription(self):
        """Get user's subscription, create free one if doesn't exist"""
        subscription = Subscription.query.filter_by(user_id=self.id).first()
        if not subscription:
            subscription = Subscription(
                user_id=self.id,
                plan_type='free'
            )
            db.session.add(subscription)
            db.session.commit()
        return subscription

    def can_create_project(self) -> bool:
        """Check if user can create a new project"""
        subscription = self.get_subscription()
        if subscription.plan_type == 'free':
            project_count = Project.query.filter_by(user_id=self.id).count()
            return project_count < 1
        return True

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    plan_type = db.Column(db.String(20), default='free', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///doccollab.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROJECTS_ROOT'] = os.path.join(app.root_path, 'projects')
    app.config['TRASH_ROOT'] = os.path.join(app.root_path, 'trash')

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Rotas principais
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
        if not current_user.can_create_project():
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

    # SocketIO events
    @socketio.on('connect')
    def handle_connect():
        print(f'Client connected: {request.sid}')

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f'Client disconnected: {request.sid}')

    # Create database tables and admin user
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin_user = User.query.filter_by(email='admin@doccollab.com').first()
        if not admin_user:
            admin_user = User(
                name='Administrador',
                email='admin@doccollab.com',
                password_hash=generate_password_hash('admin123'),
                is_active=True
            )
            db.session.add(admin_user)
            db.session.flush()
            
            # Create free subscription
            subscription = Subscription(
                user_id=admin_user.id,
                plan_type='free'
            )
            db.session.add(subscription)
            db.session.commit()
            
            print("✅ Usuário admin criado!")
            print("📧 Email: admin@doccollab.com")
            print("🔑 Senha: admin123")

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
