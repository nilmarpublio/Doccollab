from datetime import datetime
from . import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='text')  # text, system, notification
    
    # Relacionamentos
    project = db.relationship('Project', backref=db.backref('chat_messages', lazy=True, order_by='ChatMessage.created_at.asc()'))
    user = db.relationship('User', backref=db.backref('chat_messages', lazy=True))
    
    def __repr__(self):
        return f'<ChatMessage {self.id} from User {self.user_id} in Project {self.project_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'message': self.message,
            'created_at': self.created_at.isoformat(),
            'message_type': self.message_type,
            'timestamp': self.created_at.strftime('%H:%M'),
            'date': self.created_at.strftime('%d/%m/%Y')
        }
