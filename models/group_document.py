"""
Modelo de Documento Compartilhado em Grupo
"""
from datetime import datetime
from . import db


class GroupDocument(db.Model):
    """Modelo de Documento Compartilhado em Grupo"""
    
    __tablename__ = 'group_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    shared_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.Column(db.String(20), default='read')  # 'read', 'write', 'admin'
    
    # Relacionamentos
    project = db.relationship('Project', backref='group_shares')
    sharer = db.relationship('User', backref='shared_documents', foreign_keys=[shared_by])
    
    # Constraint: um documento só pode ser compartilhado uma vez por grupo
    __table_args__ = (
        db.UniqueConstraint('group_id', 'project_id', name='unique_group_document'),
    )
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'group_id': self.group_id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'shared_by': self.shared_by,
            'sharer_name': self.sharer.name if self.sharer else None,
            'shared_at': self.shared_at.isoformat() if self.shared_at else None,
            'permissions': self.permissions
        }
    
    def __repr__(self):
        return f'<GroupDocument group={self.group_id} project={self.project_id}>'

