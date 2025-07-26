from typing import Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.contexts.auth.domain.repositories.session_repository import SessionRepository
from app.contexts.auth.domain.entities.session import Session
from app.contexts.auth.domain.value_objects.session_id import SessionId
from app.contexts.auth.infrastructure.models.session_model import SessionModel


class SQLAlchemySessionRepository(SessionRepository):
    def __init__(self, session: Callable[[], AsyncSession]):
        self._session_factory = session

    async def save(self, session_entity: Session) -> None:
        async with self._session_factory() as session:
            try:
                session_model = SessionModel(
                    id=session_entity.session_id.value,
                    user_id=session_entity.user_id,
                    is_active=session_entity.is_active,
                    created_at=session_entity.created_at,
                    expires_at=session_entity.expires_at,
                )
                session.add(session_model)
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def find_by_id(self, session_id: SessionId) -> Optional[Session]:
        async with self._session_factory() as session:
            stmt = select(SessionModel).where(SessionModel.id == session_id.value)
            result = await session.execute(stmt)
            session_model = result.scalar_one_or_none()

            if session_model is None:
                return None

            return self._model_to_entity(session_model)

    async def find_by_user_id(self, user_id: str) -> list[Session]:
        async with self._session_factory() as session:
            stmt = select(SessionModel).where(SessionModel.user_id == user_id)
            result = await session.execute(stmt)
            session_models = result.scalars().all()

            return [self._model_to_entity(model) for model in session_models]

    async def update(self, session_entity: Session) -> None:
        async with self._session_factory() as session:
            try:
                stmt = select(SessionModel).where(
                    SessionModel.id == session_entity.session_id.value
                )
                result = await session.execute(stmt)
                session_model = result.scalar_one_or_none()

                if session_model:
                    session_model.is_active = session_entity.is_active
                    session_model.expires_at = session_entity.expires_at
                    await session.commit()
            except Exception:
                await session.rollback()
                raise

    def _model_to_entity(self, model: SessionModel) -> Session:
        return Session(
            session_id=SessionId(model.id),
            user_id=model.user_id,
            is_active=model.is_active,
            created_at=model.created_at,
            expires_at=model.expires_at,
        )
