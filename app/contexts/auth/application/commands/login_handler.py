from app.shared.application.command_bus import CommandHandler
from app.contexts.auth.application.commands.login_command import LoginCommand
from app.contexts.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.contexts.auth.infrastructure.repositories.sqlalchemy_session_repository import (
    SQLAlchemySessionRepository,
)
from app.contexts.users.domain.services.password_service import PasswordService
from app.contexts.auth.infrastructure.services.jwt_service import JWTService
from app.contexts.users.domain.value_objects.email import Email
from app.contexts.auth.domain.entities.session import Session
from app.contexts.auth.domain.services.auth_service import AuthService
from app.shared.domain.exceptions import ValidationError, NotFoundError


class LoginHandler(CommandHandler):
    def __init__(
        self,
        user_repository: SQLAlchemyUserRepository,
        session_repository: SQLAlchemySessionRepository,
        password_service: PasswordService,
        jwt_service: JWTService,
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._auth_service = AuthService(password_service)
        self._jwt_service = jwt_service

    async def handle(self, command: LoginCommand) -> dict:
        # Sin async with - los repositorios manejan sus propias transacciones
        try:
            # Find user by email
            email = Email(command.email)
            user = await self._user_repository.find_by_email(email)

            if user is None:
                raise NotFoundError("Invalid email or password")

            # Authenticate user
            if not self._auth_service.authenticate_user(user, command.password):
                raise ValidationError("Invalid email or password")

            # Invalidate existing sessions
            await self._session_repository.invalidate_user_sessions(
                user.user_id
            )  # ← CORREGIR ESTO

            # Create new session
            new_session = Session.create(user.user_id)
            await self._session_repository.save(new_session)  # ← CORREGIR ESTO

            # Generate JWT token
            token = self._jwt_service.create_token(
                user_id=user.user_id.value, session_id=new_session.session_id.value
            )

            return {
                "access_token": token,
                "token_type": "bearer",
                "user_id": user.user_id.value,
                "expires_at": new_session.expires_at.isoformat(),
            }

        except Exception:
            raise
