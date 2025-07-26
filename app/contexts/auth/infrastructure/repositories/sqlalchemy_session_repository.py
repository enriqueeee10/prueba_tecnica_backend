from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime

from app.contexts.auth.domain.repositories.session_repository import SessionRepository
from app.contexts.auth.domain.entities.session import Session as DomainSession
from app.contexts.auth.domain.value_objects.session_id import SessionId
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.auth.infrastructure.models.session_model import SessionModel


class SQLAlchemySessionRepository(SessionRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def save(self, session: DomainSession) -> None:
        async with self._session_factory() as db_session:  # ← Cambiar nombre de variable
            try:
                session_model = SessionModel(
                    id=session.session_id.value,
                    user_id=session.user_id.value,
                    expires_at=session.expires_at,
                    is_active=session.is_active,
                    created_at=session.created_at,
                )
                db_session.add(session_model)  # ← Usar db_session
                await db_session.commit()  # ← Agregar commit
            except Exception:
                await db_session.rollback()
                raise

    async def find_by_id(self, session_id: SessionId) -> Optional[DomainSession]:
        async with self._session_factory() as db_session:  # ← Agregar async with
            stmt = select(SessionModel).where(SessionModel.id == session_id.value)
            result = await db_session.execute(stmt)  # ← Usar db_session
            session_model = result.scalar_one_or_none()

            if session_model is None:
                return None

            return self._model_to_entity(session_model)

    async def find_active_by_user_id(self, user_id: UserId) -> Optional[DomainSession]:
        async with self._session_factory() as db_session:  # ← Agregar async with
            stmt = select(SessionModel).where(
                SessionModel.user_id == user_id.value,
                SessionModel.is_active == True,
                SessionModel.expires_at > datetime.utcnow(),
            )
            result = await db_session.execute(stmt)  # ← Usar db_session
            session_model = result.scalar_one_or_none()

            if session_model is None:
                return None

            return self._model_to_entity(session_model)

    async def invalidate_user_sessions(self, user_id: UserId) -> None:
        async with self._session_factory() as db_session:  # ← Agregar async with
            try:
                stmt = (
                    update(SessionModel)
                    .where(SessionModel.user_id == user_id.value)
                    .values(is_active=False)
                )
                await db_session.execute(stmt)  # ← Usar db_session
                await db_session.commit()  # ← Agregar commit
            except Exception:
                await db_session.rollback()
                raise

    def _model_to_entity(self, model: SessionModel) -> DomainSession:
        return DomainSession(
            session_id=SessionId(model.id),
            user_id=UserId(model.user_id),
            expires_at=model.expires_at,
            created_at=model.created_at,
            is_active=model.is_active,
        )
