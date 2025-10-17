"""
Módulo de autenticação e controle de sessão
"""
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from utils.db import execute_query, dict_from_row
from datetime import datetime

def login_required(f):
    """Decorator para proteger rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator para rotas que requerem admin do grupo"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(email, password):
    """
    Autentica um usuário
    
    Returns:
        dict: Dados do usuário ou None se falhar
    """
    user_row = execute_query(
        'SELECT * FROM users WHERE email = ?',
        (email,),
        fetch_one=True
    )
    
    if user_row and check_password_hash(user_row['password_hash'], password):
        user = dict_from_row(user_row)
        
        # Atualizar último login
        execute_query(
            'UPDATE users SET last_login = ? WHERE id = ?',
            (datetime.now(), user['id']),
            commit=True
        )
        
        # Registrar atividade
        log_activity(user['id'], 'login', f'Login realizado de {email}')
        
        return user
    
    return None

def create_user(name, email, password, is_admin=0):
    """
    Cria um novo usuário
    
    Returns:
        int: ID do usuário criado ou None se falhar
    """
    # Verificar se email já existe
    existing = execute_query(
        'SELECT id FROM users WHERE email = ?',
        (email,),
        fetch_one=True
    )
    
    if existing:
        return None
    
    password_hash = generate_password_hash(password)
    
    user_id = execute_query(
        'INSERT INTO users (name, email, password_hash, is_admin) VALUES (?, ?, ?, ?)',
        (name, email, password_hash, is_admin),
        commit=True
    )
    
    return user_id

def get_current_user():
    """Retorna os dados do usuário logado"""
    if 'user_id' not in session:
        return None
    
    user_row = execute_query(
        'SELECT id, name, email, is_admin, created_at FROM users WHERE id = ?',
        (session['user_id'],),
        fetch_one=True
    )
    
    return dict_from_row(user_row) if user_row else None

def log_activity(user_id, action, details=''):
    """Registra uma atividade no log"""
    execute_query(
        'INSERT INTO activity_log (user_id, action, details) VALUES (?, ?, ?)',
        (user_id, action, details),
        commit=True
    )

def is_group_admin(user_id, group_id):
    """Verifica se o usuário é admin de um grupo"""
    row = execute_query(
        'SELECT role FROM group_members WHERE user_id = ? AND group_id = ?',
        (user_id, group_id),
        fetch_one=True
    )
    
    return row and row['role'] == 'admin'

def is_group_member(user_id, group_id):
    """Verifica se o usuário é membro de um grupo"""
    row = execute_query(
        'SELECT id FROM group_members WHERE user_id = ? AND group_id = ?',
        (user_id, group_id),
        fetch_one=True
    )
    
    return row is not None

