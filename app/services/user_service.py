# User service - manage user data, preferences, and operations
from app.core.database import db
from app.models.user import User
from app.core.logger import logger
from datetime import datetime

class UserService:
    """Service for user-related operations"""
    
    @staticmethod
    def create_or_get_user(user_id: int, first_name: str,
                          last_name: str = None, username: str = None) -> dict:
        """Create new user or get existing user"""
        # Check if user exists
        result = db.execute_query(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        
        if result:
            logger.info(f"User {user_id} accessed")
            return dict(result[0])
        
        # Create new user
        db.execute_update(
            """INSERT INTO users (user_id, first_name, last_name, username)
               VALUES (?, ?, ?, ?)""",
            (user_id, first_name, last_name, username)
        )
        
        logger.info(f"New user created: {user_id}")
        return UserService.get_user(user_id)
    
    @staticmethod
    def get_user(user_id: int) -> dict:
        """Get user by user_id"""
        result = db.execute_query(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return dict(result[0]) if result else None
    
    @staticmethod
    def toggle_notifications(user_id: int, enabled: bool) -> bool:
        """Toggle user notifications"""
        db.execute_update(
            "UPDATE users SET notifications_enabled = ? WHERE user_id = ?",
            (1 if enabled else 0, user_id)
        )
        return True
    
    @staticmethod
    def set_language(user_id: int, language: str) -> bool:
        """Set user language preference"""
        db.execute_update(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (language, user_id)
        )
        return True