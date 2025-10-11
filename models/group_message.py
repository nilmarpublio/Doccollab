"""
Modelo de Mensagem de Grupo
"""
from datetime import datetime
from . import db


class GroupMessage(db.Model):
    """Modelo de Mensagem de Chat em Grupo"""
    
    __tablename__ = 'group_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    message_type = db.Column(db.String(20), default='text')  # 'text', 'file', 'system'
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Relacionamentos
    user = db.relationship('User', backref='group_messages')
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'content': self.content if not self.is_deleted else '[Mensagem deletada]',
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'message_type': self.message_type,
            'is_deleted': self.is_deleted
        }
    
    def __repr__(self):
        return f'<GroupMessage group={self.group_id} user={self.user_id}>'

