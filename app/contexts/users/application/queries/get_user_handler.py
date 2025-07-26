from app.shared.application.query_bus import QueryHandler
from app.contexts.users.application.queries.get_user_query import GetUserQuery
from app.contexts.users.domain.repositories.user_repository import UserRepository
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.users.domain.entities.user import User
from app.shared.domain.exceptions import NotFoundError
from typing import Optional


class GetUserHandler(QueryHandler):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def handle(self, query: GetUserQuery) -> User:
        user_id = UserId(query.user_id)
        user = await self._user_repository.find_by_id(user_id)

        if user is None:
            raise NotFoundError(f"User with id {query.user_id} not found")

        return user
