from app.shared.domain.events import DomainEvent
from typing import Dict, Any


class UserCreated(DomainEvent):
    def __init__(self, user_id: str, name: str, email: str):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.email = email

    def _get_event_data(self) -> Dict[str, Any]:
        return {"user_id": self.user_id, "name": self.name, "email": self.email}


# app/contexts/users/application/commands/create_user_command.py
from app.shared.application.command_bus import Command


class CreateUserCommand(Command):
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password
