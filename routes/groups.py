"""
Rotas para gerenciamento de grupos
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from models import db
from models.group import Group
from models.group_member import GroupMember
from models.group_document import GroupDocument
from models.project import Project


# ===== GRUPOS =====

@login_required
def list_groups():
    """Listar grupos do usuário"""
    try:
        # Buscar grupos onde o usuário é membro
        memberships = GroupMember.query.filter_by(user_id=current_user.id).all()
        groups = [membership.group for membership in memberships if membership.group.is_active]
        
        return jsonify({
            'success': True,
            'groups': [group.to_dict() for group in groups]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def create_group():
    """Criar novo grupo"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'Nome do grupo é obrigatório'
            }), 400
        
        # Criar grupo
        group = Group(
            name=name,
            description=description,
            created_by=current_user.id
        )
        db.session.add(group)
        db.session.flush()  # Para obter o ID
        
        # Adicionar criador como admin
        member = GroupMember(
            group_id=group.id,
            user_id=current_user.id,
            role='admin'
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'group': group.to_dict(),
            'message': 'Grupo criado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def get_group(group_id):
    """Obter detalhes do grupo"""
    try:
        # Verificar se usuário é membro
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Você não é membro deste grupo'
            }), 403
        
        group = Group.query.get(group_id)
        if not group or not group.is_active:
            return jsonify({
                'success': False,
                'error': 'Grupo não encontrado'
            }), 404
        
        # Incluir membros e documentos
        group_dict = group.to_dict()
        group_dict['members'] = [m.to_dict() for m in group.members]
        group_dict['documents'] = [d.to_dict() for d in group.documents]
        group_dict['user_role'] = member.role
        
        return jsonify({
            'success': True,
            'group': group_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def update_group(group_id):
    """Atualizar grupo (admin only)"""
    try:
        # Verificar se usuário é admin
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id,
            role='admin'
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Apenas administradores podem editar o grupo'
            }), 403
        
        group = Group.query.get(group_id)
        if not group:
            return jsonify({
                'success': False,
                'error': 'Grupo não encontrado'
            }), 404
        
        data = request.get_json()
        if 'name' in data:
            group.name = data['name']
        if 'description' in data:
            group.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'group': group.to_dict(),
            'message': 'Grupo atualizado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def delete_group(group_id):
    """Deletar grupo (admin only)"""
    try:
        # Verificar se usuário é admin
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id,
            role='admin'
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Apenas administradores podem deletar o grupo'
            }), 403
        
        group = Group.query.get(group_id)
        if not group:
            return jsonify({
                'success': False,
                'error': 'Grupo não encontrado'
            }), 404
        
        # Soft delete
        group.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo deletado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ===== MEMBROS =====

@login_required
def list_members(group_id):
    """Listar membros do grupo"""
    try:
        # Verificar se usuário é membro
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Você não é membro deste grupo'
            }), 403
        
        members = GroupMember.query.filter_by(group_id=group_id).all()
        
        return jsonify({
            'success': True,
            'members': [m.to_dict() for m in members]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def add_member(group_id):
    """Adicionar membro (admin only)"""
    try:
        # Verificar se usuário é admin
        admin_member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id,
            role='admin'
        ).first()
        
        if not admin_member:
            return jsonify({
                'success': False,
                'error': 'Apenas administradores podem adicionar membros'
            }), 403
        
        data = request.get_json()
        user_id = data.get('user_id')
        role = data.get('role', 'member')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'ID do usuário é obrigatório'
            }), 400
        
        # Verificar se já é membro
        existing = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Usuário já é membro do grupo'
            }), 400
        
        # Adicionar membro
        member = GroupMember(
            group_id=group_id,
            user_id=user_id,
            role=role
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'member': member.to_dict(),
            'message': 'Membro adicionado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def remove_member(group_id, user_id):
    """Remover membro (admin only)"""
    try:
        # Verificar se usuário é admin
        admin_member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id,
            role='admin'
        ).first()
        
        if not admin_member:
            return jsonify({
                'success': False,
                'error': 'Apenas administradores podem remover membros'
            }), 403
        
        # Não permitir remover a si mesmo se for o único admin
        if user_id == current_user.id:
            admin_count = GroupMember.query.filter_by(
                group_id=group_id,
                role='admin'
            ).count()
            
            if admin_count == 1:
                return jsonify({
                    'success': False,
                    'error': 'Não é possível remover o único administrador'
                }), 400
        
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Membro não encontrado'
            }), 404
        
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Membro removido com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def update_member_role(group_id, user_id):
    """Atualizar role do membro (admin only)"""
    try:
        # Verificar se usuário é admin
        admin_member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id,
            role='admin'
        ).first()
        
        if not admin_member:
            return jsonify({
                'success': False,
                'error': 'Apenas administradores podem alterar roles'
            }), 403
        
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['admin', 'member', 'viewer']:
            return jsonify({
                'success': False,
                'error': 'Role inválido'
            }), 400
        
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Membro não encontrado'
            }), 404
        
        # Não permitir remover admin de si mesmo se for o único
        if user_id == current_user.id and new_role != 'admin':
            admin_count = GroupMember.query.filter_by(
                group_id=group_id,
                role='admin'
            ).count()
            
            if admin_count == 1:
                return jsonify({
                    'success': False,
                    'error': 'Não é possível remover o único administrador'
                }), 400
        
        member.role = new_role
        db.session.commit()
        
        return jsonify({
            'success': True,
            'member': member.to_dict(),
            'message': 'Role atualizado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ===== DOCUMENTOS =====

@login_required
def list_group_documents(group_id):
    """Listar documentos do grupo"""
    try:
        # Verificar se usuário é membro
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Você não é membro deste grupo'
            }), 403
        
        documents = GroupDocument.query.filter_by(group_id=group_id).all()
        
        return jsonify({
            'success': True,
            'documents': [d.to_dict() for d in documents]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def share_document(group_id):
    """Compartilhar documento no grupo"""
    try:
        # Verificar se usuário é membro
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Você não é membro deste grupo'
            }), 403
        
        data = request.get_json()
        project_id = data.get('project_id')
        permissions = data.get('permissions', 'read')
        
        if not project_id:
            return jsonify({
                'success': False,
                'error': 'ID do projeto é obrigatório'
            }), 400
        
        # Verificar se projeto existe e pertence ao usuário
        project = Project.query.get(project_id)
        if not project or project.user_id != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Projeto não encontrado ou você não tem permissão'
            }), 403
        
        # Verificar se já está compartilhado
        existing = GroupDocument.query.filter_by(
            group_id=group_id,
            project_id=project_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Documento já está compartilhado neste grupo'
            }), 400
        
        # Compartilhar documento
        doc = GroupDocument(
            group_id=group_id,
            project_id=project_id,
            shared_by=current_user.id,
            permissions=permissions
        )
        db.session.add(doc)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'document': doc.to_dict(),
            'message': 'Documento compartilhado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@login_required
def unshare_document(group_id, doc_id):
    """Remover documento do grupo"""
    try:
        # Verificar se usuário é admin ou quem compartilhou
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=current_user.id
        ).first()
        
        if not member:
            return jsonify({
                'success': False,
                'error': 'Você não é membro deste grupo'
            }), 403
        
        doc = GroupDocument.query.get(doc_id)
        if not doc or doc.group_id != group_id:
            return jsonify({
                'success': False,
                'error': 'Documento não encontrado'
            }), 404
        
        # Apenas admin ou quem compartilhou pode remover
        if member.role != 'admin' and doc.shared_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Você não tem permissão para remover este documento'
            }), 403
        
        db.session.delete(doc)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Documento removido do grupo'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

