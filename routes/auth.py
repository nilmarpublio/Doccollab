from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    if not email or not password:
        flash('Preencha email e senha.', 'warning')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash('Email ou senha incorretos.', 'danger')
        return redirect(url_for('auth.login'))

    if not user.is_active:
        flash('Conta desativada.', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    flash(f'Bem-vindo, {user.name}!', 'success')
    return redirect(url_for('main.dashboard'))

@auth_bp.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([name, email, password, confirm_password]):
        flash('Preencha todos os campos.', 'warning')
        return redirect(url_for('auth.register'))

    if password != confirm_password:
        flash('As senhas não coincidem.', 'danger')
        return redirect(url_for('auth.register'))

    if User.query.filter_by(email=email).first():
        flash('Email já cadastrado.', 'warning')
        return redirect(url_for('auth.register'))

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # Get the ID
    
    # Create free subscription
    from models.subscription import Subscription, PlanType
    subscription = Subscription(
        user_id=user.id,
        plan_type=PlanType.FREE
    )
    db.session.add(subscription)
    db.session.commit()

    flash('Conta criada com sucesso! Faça login.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('main.index'))
