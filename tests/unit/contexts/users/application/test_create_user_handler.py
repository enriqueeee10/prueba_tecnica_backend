import pytest
from unittest.mock import AsyncMock, Mock

from app.contexts.users.application.commands.create_user_command import (
    CreateUserCommand,
)
from app.contexts.users.application.commands.create_user_handler import (
    CreateUserHandler,
)
from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.value_objects.email import Email
from app.shared.domain.exceptions import DuplicateError


class TestCreateUserHandler:
    def setup_method(self):
        self.user_repository = AsyncMock()
        self.password_service = Mock()
        self.handler = CreateUserHandler(
            user_repository=self.user_repository, password_service=self.password_service
        )

    @pytest.mark.asyncio
    async def test_create_user_success(self):
        """Test successful user creation"""
        # Arrange
        command = CreateUserCommand(
            name="John Doe", email="john@example.com", password="password123"
        )

        self.user_repository.exists_by_email.return_value = False
        self.password_service.hash_password.return_value = "hashed_password"

        # Act
        user_id = await self.handler.handle(command)

        # Assert
        assert user_id is not None
        self.user_repository.exists_by_email.assert_called_once()
        self.password_service.hash_password.assert_called_once_with("password123")
        self.user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        # Arrange
        command = CreateUserCommand(
            name="John Doe", email="john@example.com", password="password123"
        )

        self.user_repository.exists_by_email.return_value = True

        # Act & Assert
        with pytest.raises(DuplicateError):
            await self.handler.handle(command)
