# User service - manage user data, preferences, and operations
from app.core.database import db
from app.core.logger import logger


class UserService:
    """Service for user-related operations"""

    @staticmethod
    def create_or_get_user(user_id: int, first_name: str,
                           last_name: str = None, username: str = None) -> dict:
        """Create new user or get existing user"""
        try:
            result = db.execute_query(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            )
            if result:
                logger.info(f"User {user_id} accessed")
                return dict(result[0])

            db.execute_update(
                "INSERT INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                (user_id, first_name, last_name, username)
            )
            logger.info(f"New user created: {user_id}")
            return UserService.get_user(user_id)
        except Exception as e:
            logger.error(f"Error creating/getting user {user_id}: {e}")
            return None

    @staticmethod
    def get_user(user_id: int) -> dict:
        """Get user by user_id"""
        try:
            result = db.execute_query(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            )
            return dict(result[0]) if result else None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    @staticmethod
    def toggle_notifications(user_id: int, enabled: bool) -> bool:
        """Toggle user notifications"""
        try:
            db.execute_update(
                "UPDATE users SET notifications_enabled = ? WHERE user_id = ?",
                (1 if enabled else 0, user_id)
            )
            return True
        except Exception as e:
            logger.error(f"Error toggling notifications for {user_id}: {e}")
            return False

    @staticmethod
    def set_language(user_id: int, language: str) -> bool:
        """Set user language preference"""
        try:
            db.execute_update(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id)
            )
            return True
        except Exception as e:
            logger.error(f"Error setting language for {user_id}: {e}")
            return False