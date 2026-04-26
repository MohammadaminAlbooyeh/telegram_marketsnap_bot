import pytest
import os
import tempfile

# Set test environment variables before importing app modules
os.environ["BOT_TOKEN"] = "test_token"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture
def temp_db():
    """Provide a temporary in-memory database."""
    from app.core.database import Database
    db = Database("sqlite:///:memory:")
    yield db
    db.close()


@pytest.fixture
def sample_user():
    """Provide a sample user."""
    from app.models.user import User
    return User(user_id=123456, first_name="Test", last_name="User", username="testuser")


@pytest.fixture
def sample_alert():
    """Provide a sample alert."""
    from app.models.user_alert import UserAlert
    return UserAlert(
        user_id=123456,
        asset_type="crypto",
        asset_name="bitcoin",
        target_price=3000000,
        condition="above"
    )
