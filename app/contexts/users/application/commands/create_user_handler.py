from app.shared.application.command_bus import CommandHandler
from app.contexts.users.application.commands.create_user_command import (
    CreateUserCommand,
)
from app.contexts.users.domain.repositories.user_repository import UserRepository
from app.contexts.users.domain.services.password_service import PasswordService
from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.value_objects.email import Email
from app.contexts.users.domain.events.user_created import UserCreated
from app.shared.domain.exceptions import DuplicateError


class CreateUserHandler(CommandHandler):
    def __init__(
        self, user_repository: UserRepository, password_service: PasswordService
    ):
        self._user_repository = user_repository
        self._password_service = password_service

    async def handle(self, command: CreateUserCommand) -> str:
        email = Email(command.email)

        # Check if user already exists
        if await self._user_repository.exists_by_email(email):
            raise DuplicateError(f"User with email {command.email} already exists")

        # Hash password
        hashed_password = self._password_service.hash_password(command.password)

        # Create user
        user = User.create(
            name=command.name, email=email, hashed_password=hashed_password
        )

        # Save user
        await self._user_repository.save(user)

        # Publish domain event
        event = UserCreated(
            user_id=user.user_id.value, name=user.name, email=user.email.value
        )

        return user.user_id.value
