from flask import Flask, request, session, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_babel import Babel, gettext as _
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from models import db
from models.user import User

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

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    babel = Babel()

    def get_locale():
        lang = session.get('lang')
        if lang in app.config['BABEL_SUPPORTED_LOCALES']:
            return lang
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or app.config['BABEL_DEFAULT_LOCALE']

    babel.init_app(app, locale_selector=get_locale)

    @app.context_processor
    def inject_lang():
        return {'current_locale': get_locale(), 'get_locale': get_locale}

    @app.route('/set-language/<lang_code>')
    def set_language(lang_code):
        if lang_code in app.config['BABEL_SUPPORTED_LOCALES']:
            session['lang'] = lang_code
        return redirect(request.referrer or url_for('main.index'))

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.svg', mimetype='image/svg+xml')
    
    @app.route('/test-lang')
    def test_lang():
        from flask_babel import gettext
        return f"Current locale: {get_locale()}, Test: {gettext('Home')}"

    from routes.main import main_bp
    from routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        # Ensure project directories exist
        os.makedirs(app.config['PROJECTS_ROOT'], exist_ok=True)
        os.makedirs(app.config['TRASH_ROOT'], exist_ok=True)
        db.create_all()
        seed_email = os.getenv('SEED_EMAIL', 'admin@test.com')
        seed_pass = os.getenv('SEED_PASSWORD', 'admin123')
        existing = User.query.filter_by(email=seed_email).first()
        if not existing:
            u = User(name='Admin Test', email=seed_email, plan='paid')
            u.set_password(seed_pass)
            db.session.add(u)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)
