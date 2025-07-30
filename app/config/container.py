from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import settings
from app.contexts.users.application.commands.update_user_handler import (
    UpdateUserHandler,
)
from app.shared.infrastructure.database import Database
from app.shared.infrastructure.messaging.rabbitmq_connection import RabbitMQConnection
from app.shared.application.command_bus import CommandBus
from app.shared.application.query_bus import QueryBus

# Users context
from app.contexts.users.domain.repositories.user_repository import UserRepository
from app.contexts.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.contexts.users.application.commands.create_user_handler import (
    CreateUserHandler,
)
from app.contexts.users.application.queries.get_user_handler import GetUserHandler
from app.contexts.users.domain.services.password_service import (
    PasswordService,
)  # ← AGREGAR ESTE IMPORT

# Auth context
from app.contexts.auth.domain.repositories.session_repository import SessionRepository
from app.contexts.auth.infrastructure.repositories.sqlalchemy_session_repository import (
    SQLAlchemySessionRepository,
)
from app.contexts.auth.application.commands.login_handler import LoginHandler
from app.contexts.auth.infrastructure.services.jwt_service import JWTService
from app.contexts.auth.application.queries.validate_token_handler import (
    ValidateTokenHandler,
)


class Container(containers.DeclarativeContainer):
    # Configuration
    config = providers.Configuration()

    # Database
    database = providers.Singleton(Database, database_url=settings.DATABASE_URL)

    # Session factory - usar este
    session_factory = providers.Factory(lambda db: db.get_session(), db=database)

    # Message Broker
    rabbitmq = providers.Singleton(RabbitMQConnection, url=settings.RABBITMQ_URL)

    # Buses
    command_bus = providers.Singleton(CommandBus)
    query_bus = providers.Singleton(QueryBus)

    # Users Context
    password_service = providers.Singleton(PasswordService)

    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session=session_factory,
    )

    create_user_handler = providers.Factory(
        CreateUserHandler,
        user_repository=user_repository,
        password_service=password_service,
    )

    get_user_handler = providers.Factory(
        GetUserHandler, user_repository=user_repository
    )

    update_user_handler = providers.Factory(
        UpdateUserHandler,
        user_repository=user_repository,
    )

    # Auth Context
    jwt_service = providers.Singleton(
        JWTService,
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        expiration_minutes=settings.JWT_EXPIRATION_MINUTES,
    )

    session_repository = providers.Factory(
        SQLAlchemySessionRepository,
        session_factory=session_factory,
    )

    login_handler = providers.Factory(
        LoginHandler,
        user_repository=user_repository,
        session_repository=session_repository,
        password_service=password_service,
        jwt_service=jwt_service,
    )

    validate_token_handler = providers.Factory(
        ValidateTokenHandler,
        jwt_service=jwt_service,
        session_repository=session_repository,
    )
