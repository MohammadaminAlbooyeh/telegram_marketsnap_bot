# User model - stores user data and preferences
from datetime import datetime

class User:
    """User model for storing user data"""
    
    def __init__(self, user_id: int, first_name: str, 
                 last_name: str = None, username: str = None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language = "en"
        self.notifications_enabled = True
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "language": self.language,
            "notifications_enabled": self.notifications_enabled
        }