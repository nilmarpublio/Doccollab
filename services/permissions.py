"""
Sistema de permissões e controle de acesso
"""

from enum import Enum
from typing import Optional
from flask_login import current_user

class Permission(Enum):
    """Permissões disponíveis"""
    # Edição
    EDIT_DOCUMENT = "edit_document"
    DELETE_DOCUMENT = "delete_document"
    CREATE_DOCUMENT = "create_document"
    
    # Assistente
    USE_ASSISTANT = "use_assistant"
    INSERT_SNIPPET = "insert_snippet"
    APPLY_PATCH = "apply_patch"
    COMPILE = "compile"
    GENERATE_BIBTEX = "generate_bibtex"
    
    # Admin
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    MANAGE_PERMISSIONS = "manage_permissions"

class Role(Enum):
    """Roles do sistema"""
    GUEST = "guest"       # Apenas leitura
    USER = "user"         # Usuário padrão
    EDITOR = "editor"     # Pode editar todos os documentos
    ADMIN = "admin"       # Admin completo

# Mapeamento de roles para permissões
ROLE_PERMISSIONS = {
    Role.GUEST: [
        # Apenas visualização, sem edição
    ],
    
    Role.USER: [
        Permission.EDIT_DOCUMENT,
        Permission.CREATE_DOCUMENT,
        Permission.USE_ASSISTANT,
        Permission.INSERT_SNIPPET,
        Permission.COMPILE,
        Permission.GENERATE_BIBTEX
    ],
    
    Role.EDITOR: [
        Permission.EDIT_DOCUMENT,
        Permission.DELETE_DOCUMENT,
        Permission.CREATE_DOCUMENT,
        Permission.USE_ASSISTANT,
        Permission.INSERT_SNIPPET,
        Permission.APPLY_PATCH,
        Permission.COMPILE,
        Permission.GENERATE_BIBTEX
    ],
    
    Role.ADMIN: [
        # Admin tem todas as permissões
        Permission.EDIT_DOCUMENT,
        Permission.DELETE_DOCUMENT,
        Permission.CREATE_DOCUMENT,
        Permission.USE_ASSISTANT,
        Permission.INSERT_SNIPPET,
        Permission.APPLY_PATCH,
        Permission.COMPILE,
        Permission.GENERATE_BIBTEX,
        Permission.MANAGE_USERS,
        Permission.VIEW_AUDIT_LOGS,
        Permission.MANAGE_PERMISSIONS
    ]
}

def get_user_role(user=None) -> Role:
    """
    Obtém role do usuário
    
    Args:
        user: Usuário (usa current_user se None)
    
    Returns:
        Role do usuário
    """
    if user is None:
        if not current_user.is_authenticated:
            return Role.GUEST
        user = current_user
    
    # Por padrão, verificar se tem atributo 'role'
    if hasattr(user, 'role'):
        try:
            return Role(user.role)
        except ValueError:
            return Role.USER
    
    # Verificar se é admin pelo email (temporário)
    if hasattr(user, 'email') and user.email == 'admin@doccollab.com':
        return Role.ADMIN
    
    # Usuário padrão
    return Role.USER if user and hasattr(user, 'id') else Role.GUEST

def has_permission(permission: Permission, user=None) -> bool:
    """
    Verifica se usuário tem permissão
    
    Args:
        permission: Permissão a verificar
        user: Usuário (usa current_user se None)
    
    Returns:
        True se tem permissão
    """
    role = get_user_role(user)
    return permission in ROLE_PERMISSIONS.get(role, [])

def user_can_edit(user=None, document_id: Optional[int] = None) -> bool:
    """
    Verifica se usuário pode editar documento
    
    Args:
        user: Usuário (usa current_user se None)
        document_id: ID do documento (verifica ownership se fornecido)
    
    Returns:
        True se pode editar
    """
    if user is None:
        if not current_user.is_authenticated:
            return False
        user = current_user
    
    # Verificar permissão básica
    if not has_permission(Permission.EDIT_DOCUMENT, user):
        return False
    
    # Se é editor ou admin, pode editar qualquer documento
    role = get_user_role(user)
    if role in [Role.EDITOR, Role.ADMIN]:
        return True
    
    # Se forneceu document_id, verificar ownership
    if document_id:
        # TODO: Implementar verificação de ownership no banco
        # Por enquanto, assumir que pode editar se é USER e está autenticado
        return role == Role.USER
    
    return True

def user_can_use_assistant(user=None, action_type: Optional[str] = None) -> bool:
    """
    Verifica se usuário pode usar assistente
    
    Args:
        user: Usuário (usa current_user se None)
        action_type: Tipo de ação específica (opcional)
    
    Returns:
        True se pode usar
    """
    if user is None:
        if not current_user.is_authenticated:
            return False
        user = current_user
    
    # Verificar permissão básica de usar assistente
    if not has_permission(Permission.USE_ASSISTANT, user):
        return False
    
    # Verificar permissão específica por tipo de ação
    if action_type:
        action_permission_map = {
            'insert_snippet': Permission.INSERT_SNIPPET,
            'apply_patch': Permission.APPLY_PATCH,
            'compile': Permission.COMPILE,
            'generate_bibtex': Permission.GENERATE_BIBTEX
        }
        
        required_permission = action_permission_map.get(action_type)
        if required_permission and not has_permission(required_permission, user):
            return False
    
    return True

def user_can_view_audit_logs(user=None) -> bool:
    """
    Verifica se usuário pode ver logs de auditoria
    
    Args:
        user: Usuário (usa current_user se None)
    
    Returns:
        True se pode ver
    """
    if user is None:
        if not current_user.is_authenticated:
            return False
        user = current_user
    
    return has_permission(Permission.VIEW_AUDIT_LOGS, user)

def require_permission(permission: Permission):
    """
    Decorator para exigir permissão em views
    
    Usage:
        @require_permission(Permission.EDIT_DOCUMENT)
        def my_view():
            ...
    """
    def decorator(f):
        from functools import wraps
        from flask import abort
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not has_permission(permission):
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator







