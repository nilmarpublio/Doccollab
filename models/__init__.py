# Import db from app_fixed instead of creating new instance
from app_fixed import db

# Import all models to ensure they are registered
# Import User first to avoid circular dependency
from .user import User
from .project import Project
from .version import Version
from .chat_message import ChatMessage
# Import Subscription last since it references User
from .subscription import Subscription, PlanType
# Import Group models
from .group import Group
from .group_member import GroupMember
from .group_document import GroupDocument
from .group_message import GroupMessage
