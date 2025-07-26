import pytest
from unittest.mock import AsyncMock

from app.contexts.users.application.queries.get_user_query import GetUserQuery
from app.contexts.users.application.queries.get_user_handler import GetUserHandler
from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.users.domain.value_objects.email import Email
from app.shared.domain.exceptions import NotFoundError


class TestGetUserHandler:
    def setup_method(self):
        self.user_repository = AsyncMock()
        self.handler = GetUserHandler(user_repository=self.user_repository)

    @pytest.mark.asyncio
    async def test_get_user_success(self):
        """Test successful user retrieval"""
        # Arrange
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        query = GetUserQuery(user_id=user_id)

        expected_user = User.create(
            name="John Doe",
            email=Email("john@example.com"),
            hashed_password="hashed_password",
        )
        expected_user._user_id = UserId(user_id)

        self.user_repository.find_by_id.return_value = expected_user

        # Act
        result = await self.handler.handle(query)

        # Assert
        assert result == expected_user
        self.user_repository.find_by_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_not_found(self):
        """Test user not found"""
        # Arrange
        user_id = "non-existent-id"
        query = GetUserQuery(user_id=user_id)

        self.user_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundError):
            await self.handler.handle(query)
