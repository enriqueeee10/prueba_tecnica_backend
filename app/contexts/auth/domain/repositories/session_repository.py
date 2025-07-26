from abc import ABC, abstractmethod
from typing import Optional
from app.contexts.auth.domain.entities.session import Session
from app.contexts.auth.domain.value_objects.session_id import SessionId
from app.contexts.users.domain.value_objects.user_id import UserId


class SessionRepository(ABC):
    @abstractmethod
    async def save(self, session: Session) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, session_id: SessionId) -> Optional[Session]:
        pass

    @abstractmethod
    async def find_active_by_user_id(self, user_id: UserId) -> Optional[Session]:
        pass

    @abstractmethod
    async def invalidate_user_sessions(self, user_id: UserId) -> None:
        pass
