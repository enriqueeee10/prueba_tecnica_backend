from typing import Dict, Type, Any
from abc import ABC, abstractmethod


class Query(ABC):
    """Base class for Queries"""

    pass


class QueryHandler(ABC):
    """Base class for Query Handlers"""

    @abstractmethod
    async def handle(self, query: Query) -> Any:
        pass


class QueryBus:
    """Query Bus implementation"""

    def __init__(self):
        self._handlers: Dict[Type[Query], QueryHandler] = {}

    def register(self, query_type: Type[Query], handler: QueryHandler):
        """Register a query handler"""
        self._handlers[query_type] = handler

    async def execute(self, query: Query) -> Any:
        """Execute a query"""
        query_type = type(query)

        if query_type not in self._handlers:
            raise ValueError(f"No handler registered for query {query_type.__name__}")

        handler = self._handlers[query_type]
        return await handler.handle(query)
