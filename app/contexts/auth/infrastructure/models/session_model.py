from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from app.contexts.users.infrastructure.models.user_model import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
