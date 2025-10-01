from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure they are registered
from .user import User
from .project import Project
from .subscription import Subscription, PlanType
