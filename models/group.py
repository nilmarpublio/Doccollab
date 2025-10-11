"""
Modelo de Grupo para colaboração
"""
from datetime import datetime
from . import db


class Group(db.Model):
    """Modelo de Grupo de Colaboração"""
    
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    creator = db.relationship('User', backref='created_groups', foreign_keys=[created_by])
    members = db.relationship('GroupMember', backref='group', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('GroupDocument', backref='group', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('GroupMessage', backref='group', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'is_active': self.is_active,
            'member_count': len(self.members),
            'document_count': len(self.documents)
        }
    
    def __repr__(self):
        return f'<Group {self.name}>'

