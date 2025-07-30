from app.shared.domain.events import DomainEvent
from typing import Dict, Any
from app.shared.application.command_bus import Command


class UserUpdate(DomainEvent):
    def __init__(self, user_id: str, name: str, email: str):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.email = email

    def _get_event_data(self) -> Dict[str, Any]:
        return {"user_id": self.user_id, "name": self.name, "email": self.email}


class UpdateUserCommand(Command):
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def to_event(self) -> UserUpdate:
        return UserUpdate(user_id=self.user_id, name=self.name, email=self.email)
