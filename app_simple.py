from flask import Flask, request, session, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///doccollab.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['LANGUAGES'] = {
        'en': 'English',
        'pt': 'Português',
        'es': 'Español'
    }
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)