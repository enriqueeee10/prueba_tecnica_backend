import bcrypt


class PasswordService:
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# app/contexts/users/domain/events/user_created.py
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
