from datetime import datetime
from . import db

class Version(db.Model):
    __tablename__ = 'versions'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_name = db.Column(db.String(255), nullable=False, default='main.tex')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(500), nullable=True)
    
    # Relacionamento com projeto
    project = db.relationship('Project', backref=db.backref('versions', lazy=True, order_by='Version.created_at.desc()'))
    
    def __repr__(self):
        return f'<Version {self.version_number} of Project {self.project_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'version_number': self.version_number,
            'file_name': self.file_name,
            'created_at': self.created_at.isoformat(),
            'description': self.description,
            'content_preview': self.content[:200] + '...' if len(self.content) > 200 else self.content
        }
