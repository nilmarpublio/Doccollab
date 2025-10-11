"""
Modelo de Membro de Grupo
"""
from datetime import datetime
from . import db


class GroupMember(db.Model):
    """Modelo de Membro de Grupo"""
    
    __tablename__ = 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # 'admin', 'member', 'viewer'
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='group_memberships')
    
    # Constraint: um usuário só pode estar uma vez em cada grupo
    __table_args__ = (
        db.UniqueConstraint('group_id', 'user_id', name='unique_group_member'),
    )
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'user_email': self.user.email if self.user else None,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }
    
    def __repr__(self):
        return f'<GroupMember user={self.user_id} group={self.group_id} role={self.role}>'

