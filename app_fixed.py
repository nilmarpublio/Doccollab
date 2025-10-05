from flask import Flask, request, session, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_babel import Babel, gettext as _
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Criar instância única do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///doccollab.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Projects filesystem roots
    app.config['PROJECTS_ROOT'] = os.path.join(app.root_path, 'projects')
    app.config['TRASH_ROOT'] = os.path.join(app.root_path, 'trash')
    # External tools
    app.config['PDFLATEX'] = os.getenv('PDFLATEX')

    # i18n
    app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'pt', 'es']
    # Ensure Flask-Babel can locate compiled translations
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(app.root_path, 'translations')

    # Inicializar SQLAlchemy com a app
    db.init_app(app)

    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    babel = Babel()

    def get_locale():
        # Primeiro verifica se há idioma na URL (para forçar mudança)
        if request.args.get('lang') and request.args.get('lang') in app.config['BABEL_SUPPORTED_LOCALES']:
            # Atualiza a sessão com o idioma da URL
            session['lang'] = request.args.get('lang')
            # Force refresh of translations
            from flask_babel import refresh
            refresh()
            return request.args.get('lang')
        
        # Depois verifica se há idioma na sessão
        if 'lang' in session and session['lang'] in app.config['BABEL_SUPPORTED_LOCALES']:
            return session['lang']
        
        # Por último, usa o idioma preferido do navegador
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or app.config['BABEL_DEFAULT_LOCALE']

    babel.init_app(app, locale_selector=get_locale)

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.chat import chat_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # SocketIO events
    @socketio.on('connect')
    def handle_connect():
        print(f'Client connected: {request.sid}')

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f'Client disconnected: {request.sid}')

    @socketio.on('join_project')
    def handle_join_project(data):
        project_id = data.get('project_id')
        if project_id:
            join_room(f'project_{project_id}')
            emit('status', {'msg': f'Joined project {project_id}'}, room=f'project_{project_id}')

    @socketio.on('leave_project')
    def handle_leave_project(data):
        project_id = data.get('project_id')
        if project_id:
            leave_room(f'project_{project_id}')

    @socketio.on('send_message')
    def handle_send_message(data):
        project_id = data.get('project_id')
        message = data.get('message')
        if project_id and message:
            # Save message to database
            from models.chat_message import ChatMessage
            from flask_login import current_user
            
            if current_user.is_authenticated:
                chat_message = ChatMessage(
                    project_id=project_id,
                    user_id=current_user.id,
                    message=message
                )
                db.session.add(chat_message)
                db.session.commit()
                
                # Emit to all users in the project room
                emit('new_message', {
                    'id': chat_message.id,
                    'user_id': current_user.id,
                    'user_name': current_user.name,
                    'message': message,
                    'created_at': chat_message.created_at.isoformat()
                }, room=f'project_{project_id}')

    @socketio.on('typing')
    def handle_typing(data):
        project_id = data.get('project_id')
        is_typing = data.get('is_typing', False)
        if project_id:
            from flask_login import current_user
            if current_user.is_authenticated:
                emit('user_typing', {
                    'user_name': current_user.name,
                    'is_typing': is_typing
                }, room=f'project_{project_id}', include_self=False)

    # Create database tables
    with app.app_context():
        # Import all models to ensure they are registered
        from models.user import User
        from models.project import Project
        from models.subscription import Subscription, PlanType
        from models.version import Version
        from models.chat_message import ChatMessage
        
        db.create_all()
        
        # Create admin user if not exists
        admin_user = User.query.filter_by(email='admin@doccollab.com').first()
        if not admin_user:
            from werkzeug.security import generate_password_hash
            
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
                plan_type=PlanType.FREE
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
