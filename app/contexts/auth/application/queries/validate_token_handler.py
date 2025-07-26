from app.shared.application.query_bus import QueryHandler
from app.contexts.auth.application.queries.validate_token_query import (
    ValidateTokenQuery,
)
from app.contexts.auth.infrastructure.services.jwt_service import JWTService
from app.contexts.auth.domain.repositories.session_repository import SessionRepository
from app.contexts.auth.domain.value_objects.session_id import SessionId
from app.shared.domain.exceptions import ValidationError


class ValidateTokenHandler(QueryHandler):
    def __init__(self, jwt_service: JWTService, session_repository: SessionRepository):
        self._jwt_service = jwt_service
        self._session_repository = session_repository

    async def handle(self, query: ValidateTokenQuery) -> dict:
        # Decode token
        try:
            payload = self._jwt_service.decode_token(query.token)
        except Exception:
            raise ValidationError("Invalid token")

        # Get session
        session_id = SessionId(payload["session_id"])
        session = await self._session_repository.find_by_id(session_id)

        if session is None or not session.is_active or session.is_expired():
            raise ValidationError("Invalid or expired session")

        return {
            "user_id": payload["user_id"],
            "session_id": payload["session_id"],
            "is_valid": True,
        }
