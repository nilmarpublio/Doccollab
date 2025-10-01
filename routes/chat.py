from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room, rooms
from models import db
from models.chat_message import ChatMessage
from models.project import Project
from datetime import datetime
import json

chat_bp = Blueprint('chat', __name__)

# Store online users per project
online_users = {}

@chat_bp.route('/project/<int:project_id>/messages')
@login_required
def get_messages(project_id):
    """Get chat messages for a project"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    # Get last 50 messages
    messages = ChatMessage.query.filter_by(project_id=project_id).order_by(ChatMessage.created_at.desc()).limit(50).all()
    messages.reverse()  # Show oldest first
    
    return jsonify({
        'success': True,
        'messages': [msg.to_dict() for msg in messages]
    })

@chat_bp.route('/project/<int:project_id>/online-users')
@login_required
def get_online_users(project_id):
    """Get online users for a project"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    online_in_project = online_users.get(str(project_id), [])
    return jsonify({
        'success': True,
        'online_users': online_in_project
    })

def socketio_events(socketio):
    """Define SocketIO event handlers"""
    
    @socketio.on('connect')
    def on_connect():
        print(f"User {current_user.id if current_user.is_authenticated else 'anonymous'} connected")
    
    @socketio.on('disconnect')
    def on_disconnect():
        print(f"User {current_user.id if current_user.is_authenticated else 'anonymous'} disconnected")
        # Remove user from all project rooms
        if current_user.is_authenticated:
            for project_id in list(online_users.keys()):
                if current_user.id in online_users[project_id]:
                    online_users[project_id].remove(current_user.id)
                    if not online_users[project_id]:
                        del online_users[project_id]
                    emit('user_left', {
                        'user_id': current_user.id,
                        'user_name': current_user.name
                    }, room=f'project_{project_id}')
    
    @socketio.on('join_project')
    def on_join_project(data):
        """Join a project room for chat"""
        if not current_user.is_authenticated:
            return
        
        project_id = data.get('project_id')
        if not project_id:
            return
        
        # Verify user has access to project
        project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
        if not project:
            return
        
        # Join the room
        room = f'project_{project_id}'
        join_room(room)
        
        # Add user to online users list
        if str(project_id) not in online_users:
            online_users[str(project_id)] = []
        
        if current_user.id not in online_users[str(project_id)]:
            online_users[str(project_id)].append(current_user.id)
            
            # Notify others that user joined
            emit('user_joined', {
                'user_id': current_user.id,
                'user_name': current_user.name
            }, room=room, include_self=False)
        
        # Send current online users to the joining user
        emit('online_users_update', {
            'online_users': online_users[str(project_id)]
        })
    
    @socketio.on('leave_project')
    def on_leave_project(data):
        """Leave a project room"""
        if not current_user.is_authenticated:
            return
        
        project_id = data.get('project_id')
        if not project_id:
            return
        
        room = f'project_{project_id}'
        leave_room(room)
        
        # Remove user from online users list
        if str(project_id) in online_users and current_user.id in online_users[str(project_id)]:
            online_users[str(project_id)].remove(current_user.id)
            if not online_users[str(project_id)]:
                del online_users[str(project_id)]
            
            # Notify others that user left
            emit('user_left', {
                'user_id': current_user.id,
                'user_name': current_user.name
            }, room=room)
    
    @socketio.on('send_message')
    def on_send_message(data):
        """Handle new chat message"""
        if not current_user.is_authenticated:
            return
        
        project_id = data.get('project_id')
        message_text = data.get('message', '').strip()
        
        if not project_id or not message_text:
            return
        
        # Verify user has access to project
        project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
        if not project:
            return
        
        # Create and save message
        try:
            message = ChatMessage(
                project_id=project_id,
                user_id=current_user.id,
                message=message_text,
                message_type='text'
            )
            db.session.add(message)
            db.session.commit()
            
            # Broadcast message to all users in the project room
            room = f'project_{project_id}'
            emit('new_message', message.to_dict(), room=room)
            
        except Exception as e:
            print(f"Error saving message: {e}")
            emit('error', {'message': 'Failed to send message'})
    
    @socketio.on('typing')
    def on_typing(data):
        """Handle typing indicator"""
        if not current_user.is_authenticated:
            return
        
        project_id = data.get('project_id')
        is_typing = data.get('is_typing', False)
        
        if not project_id:
            return
        
        # Verify user has access to project
        project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
        if not project:
            return
        
        # Broadcast typing status to other users in the room
        room = f'project_{project_id}'
        emit('user_typing', {
            'user_id': current_user.id,
            'user_name': current_user.name,
            'is_typing': is_typing
        }, room=room, include_self=False)
