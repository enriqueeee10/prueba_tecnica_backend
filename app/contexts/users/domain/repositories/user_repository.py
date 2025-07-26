from abc import ABC, abstractmethod
from typing import Optional
from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.users.domain.value_objects.email import Email


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        pass
