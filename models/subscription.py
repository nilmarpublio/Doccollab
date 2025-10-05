from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from enum import Enum

db = SQLAlchemy()

class PlanType(Enum):
    FREE = "free"
    PAID = "paid"

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    plan_type = db.Column(db.Enum(PlanType), default=PlanType.FREE, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # None for free plan
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship removed temporarily to avoid circular import issues
    # Will be added back after both models are fully loaded
    
    def __repr__(self):
        return f'<Subscription {self.plan_type.value} for user {self.user_id}>'
    
    @property
    def is_paid(self):
        """Check if user has paid plan"""
        return self.plan_type == PlanType.PAID and self.is_active
    
    @property
    def is_expired(self):
        """Check if subscription is expired"""
        if self.plan_type == PlanType.FREE:
            return False
        return self.expires_at and self.expires_at < datetime.utcnow()
    
    def can_create_project(self, current_project_count):
        """Check if user can create a new project"""
        if self.plan_type == PlanType.FREE:
            return current_project_count < 1
        return True  # Paid users can create unlimited projects
    
    def can_create_file(self, current_file_count):
        """Check if user can create a new file"""
        if self.plan_type == PlanType.FREE:
            return current_file_count < 1  # Only main.tex
        return True  # Paid users can create unlimited files
    
    def can_upload_file(self):
        """Check if user can upload files"""
        return self.plan_type == PlanType.PAID
    
    def can_collaborate(self):
        """Check if user can use collaboration features"""
        return self.plan_type == PlanType.PAID
    
    def get_plan_limits(self):
        """Get plan limits for display"""
        if self.plan_type == PlanType.FREE:
            return {
                'max_projects': 1,
                'max_files': 1,
                'can_upload': False,
                'can_collaborate': False,
                'can_rename_files': False,
                'can_delete_files': False
            }
        else:
            return {
                'max_projects': -1,  # Unlimited
                'max_files': -1,     # Unlimited
                'can_upload': True,
                'can_collaborate': True,
                'can_rename_files': True,
                'can_delete_files': True
            }
