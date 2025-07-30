from app.contexts.users.domain.events.user_update import UserUpdate
from app.contexts.users.domain.value_objects.email import Email
from app.contexts.users.domain.value_objects.user_id import UserId
from app.shared.domain.events import DomainEvent
from typing import Dict, Any
from app.contexts.users.domain.repositories.user_repository import UserRepository
from app.shared.application.command_bus import Command
from app.shared.application.command_bus import CommandHandler


class UpdateUserCommand(Command):
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def to_event(self) -> DomainEvent:
        return UserUpdate(user_id=self.user_id, name=self.name, email=self.email)


class UpdateUserHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: UpdateUserCommand) -> None:
        user = await self.user_repository.find_by_id(UserId(command.user_id))
        if not user:
            raise Exception("User not found")
        # Solo verifica si el email es diferente al actual
        if user.email != Email(command.email):
            if await self.user_repository.exists_by_email(Email(command.email)):
                raise Exception("Email already in use")
            user.change_email(Email(command.email))
        user.change_name(command.name)
        await self.user_repository.update(user)
