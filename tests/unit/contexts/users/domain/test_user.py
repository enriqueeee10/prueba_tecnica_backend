import pytest
from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.users.domain.value_objects.email import Email
from app.contexts.users.domain.value_objects.password import Password
from app.shared.domain.exceptions import ValidationError


class TestUser:
    def test_create_user_success(self):
        """Test successful user creation"""
        user = User.create(
            name="John Doe",
            email=Email("john@example.com"),
            hashed_password="hashed_password_123",
        )

        assert user.name == "John Doe"
        assert user.email.value == "john@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.is_active is True
        assert isinstance(user.user_id, UserId)

    def test_user_change_name(self):
        """Test changing user name"""
        user = User.create(
            name="John Doe",
            email=Email("john@example.com"),
            hashed_password="hashed_password_123",
        )

        user.change_name("Jane Doe")
        assert user.name == "Jane Doe"

    def test_user_deactivate(self):
        """Test user deactivation"""
        user = User.create(
            name="John Doe",
            email=Email("john@example.com"),
            hashed_password="hashed_password_123",
        )

        user.deactivate()
        assert user.is_active is False

    def test_user_activate(self):
        """Test user activation"""
        user = User.create(
            name="John Doe",
            email=Email("john@example.com"),
            hashed_password="hashed_password_123",
        )

        user.deactivate()
        user.activate()
        assert user.is_active is True


class TestEmail:
    def test_valid_email(self):
        """Test valid email creation"""
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_email_case_insensitive(self):
        """Test email is stored in lowercase"""
        email = Email("TEST@EXAMPLE.COM")
        assert email.value == "test@example.com"

    def test_invalid_email_format(self):
        """Test invalid email format raises ValidationError"""
        with pytest.raises(ValidationError):
            Email("invalid-email")

        with pytest.raises(ValidationError):
            Email("@example.com")

        with pytest.raises(ValidationError):
            Email("test@")


class TestPassword:
    def test_valid_password(self):
        """Test valid password creation"""
        password = Password("password123")
        assert password.value == "password123"

    def test_password_too_short(self):
        """Test password too short raises ValidationError"""
        with pytest.raises(ValidationError):
            Password("short")

    def test_password_string_representation(self):
        """Test password string representation is masked"""
        password = Password("password123")
        assert str(password) == "*" * len("password123")
