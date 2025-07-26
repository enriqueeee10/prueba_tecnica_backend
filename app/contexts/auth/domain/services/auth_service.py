from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.services.password_service import PasswordService
from app.shared.domain.exceptions import ValidationError


class AuthService:
    def __init__(self, password_service: PasswordService):
        self._password_service = password_service

    def authenticate_user(self, user: User, password: str) -> bool:
        """Authenticate user with password"""
        if not user.is_active:
            raise ValidationError("User account is deactivated")

        return self._password_service.verify_password(password, user.hashed_password)
