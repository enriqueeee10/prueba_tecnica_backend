from app.contexts.users.domain.events.user_update import UserUpdate
from app.shared.domain.events import DomainEvent
from typing import Dict, Any
from app.shared.application.command_bus import Command


class UpdateUserCommand(Command):
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def to_event(self) -> DomainEvent:
        return UserUpdate(user_id=self.user_id, name=self.name, email=self.email)
