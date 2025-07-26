from datetime import datetime, timedelta
from typing import Optional
from app.contexts.auth.domain.value_objects.session_id import SessionId
from app.contexts.users.domain.value_objects.user_id import UserId


class Session:
    def __init__(
        self,
        session_id: SessionId,
        user_id: UserId,
        expires_at: datetime,
        created_at: Optional[datetime] = None,
        is_active: bool = True,
    ):
        self._session_id = session_id
        self._user_id = user_id
        self._expires_at = expires_at
        self._created_at = created_at or datetime.utcnow()
        self._is_active = is_active

    @property
    def session_id(self) -> SessionId:
        return self._session_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_active(self) -> bool:
        return self._is_active

    def is_expired(self) -> bool:
        return datetime.utcnow() > self._expires_at

    def invalidate(self):
        self._is_active = False

    @classmethod
    def create(cls, user_id: UserId, expiration_minutes: int = 30) -> "Session":
        return cls(
            session_id=SessionId(),
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(minutes=expiration_minutes),
        )
