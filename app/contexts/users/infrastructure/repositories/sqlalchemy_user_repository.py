from typing import Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.contexts.users.domain.repositories.user_repository import UserRepository
from app.contexts.users.domain.entities.user import User
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.users.domain.value_objects.email import Email
from app.contexts.users.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Callable[[], AsyncSession]):
        self._session_factory = session

    async def save(self, user: User) -> None:
        async with self._session_factory() as session:
            try:
                user_model = UserModel(
                    id=user.user_id.value,
                    name=user.name,
                    email=user.email.value,
                    hashed_password=user.hashed_password,
                    is_active=user.is_active,
                )
                session.add(user_model)
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        async with self._session_factory() as session:
            stmt = select(UserModel).where(UserModel.id == user_id.value)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()

            if user_model is None:
                return None

            return self._model_to_entity(user_model)

    async def find_by_email(self, email: Email) -> Optional[User]:
        async with self._session_factory() as session:
            stmt = select(UserModel).where(UserModel.email == email.value)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()

            if user_model is None:
                return None

            return self._model_to_entity(user_model)

    async def exists_by_email(self, email: Email) -> bool:
        async with self._session_factory() as session:
            stmt = select(UserModel.id).where(UserModel.email == email.value)
            result = await session.execute(stmt)
            return result.scalar_one_or_none() is not None

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            user_id=UserId(model.id),
            name=model.name,
            email=Email(model.email),
            hashed_password=model.hashed_password,
            is_active=model.is_active,
        )
