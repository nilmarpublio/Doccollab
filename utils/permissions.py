from functools import wraps
from flask import jsonify, request, current_app
from flask_login import current_user
from models.subscription import PlanType

def require_paid_plan(f):
    """Decorator to require paid plan for a function"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        subscription = current_user.get_subscription()
        if not subscription.is_paid:
            return jsonify({
                'success': False, 
                'error': 'This feature requires a paid plan',
                'upgrade_required': True,
                'message': 'Upgrade to a paid plan to access this feature'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def require_project_limit(f):
    """Decorator to check project creation limits"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        if not current_user.can_create_project():
            limits = current_user.get_plan_limits()
            return jsonify({
                'success': False,
                'error': f'Project limit reached. Free plan allows {limits["max_projects"]} project(s)',
                'upgrade_required': True,
                'message': 'Upgrade to a paid plan for unlimited projects'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def require_file_limit(project_id_param='project_id'):
    """Decorator factory to check file creation limits"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
            project_id = kwargs.get(project_id_param)
            if not current_user.can_create_file(project_id):
                limits = current_user.get_plan_limits()
                return jsonify({
                    'success': False,
                    'error': f'File limit reached. Free plan allows {limits["max_files"]} file(s)',
                    'upgrade_required': True,
                    'message': 'Upgrade to a paid plan for unlimited files'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def check_plan_limits():
    """Helper function to get current user's plan limits"""
    if not current_user.is_authenticated:
        return None
    return current_user.get_plan_limits()
