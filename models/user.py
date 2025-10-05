from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects = db.relationship('Project', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    # Subscription relationship removed to avoid circular import issues

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_subscription(self):
        """Get user's subscription, create free one if doesn't exist"""
        from .subscription import Subscription, PlanType
        # Check if subscription already exists
        subscription = Subscription.query.filter_by(user_id=self.id).first()
        if not subscription:
            # Create free subscription if doesn't exist
            subscription = Subscription(
                user_id=self.id,
                plan_type=PlanType.FREE
            )
            db.session.add(subscription)
            db.session.commit()
        return subscription

    def can_create_project(self) -> bool:
        """Check if user can create a new project"""
        subscription = self.get_subscription()
        current_count = len([p for p in self.projects if p.is_active])
        return subscription.can_create_project(current_count)

    def can_create_file(self, project_id=None) -> bool:
        """Check if user can create a new file"""
        subscription = self.get_subscription()
        if project_id:
            # Check files in specific project
            from .project import Project
            project = Project.query.get(project_id)
            if project and project.user_id == self.id:
                # Count files in project directory
                import os
                from flask import current_app
                project_path = os.path.join(current_app.config['PROJECTS_ROOT'], str(self.id), project.name)
                if os.path.exists(project_path):
                    file_count = len([f for f in os.listdir(project_path) if os.path.isfile(os.path.join(project_path, f))])
                    return subscription.can_create_file(file_count)
        return subscription.can_create_file(0)

    def can_upload_file(self) -> bool:
        """Check if user can upload files"""
        subscription = self.get_subscription()
        return subscription.can_upload_file()

    def can_collaborate(self) -> bool:
        """Check if user can use collaboration features"""
        subscription = self.get_subscription()
        return subscription.can_collaborate()

    def get_plan_limits(self):
        """Get plan limits for display"""
        subscription = self.get_subscription()
        return subscription.get_plan_limits()
