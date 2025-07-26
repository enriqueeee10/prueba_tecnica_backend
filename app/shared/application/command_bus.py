from typing import Dict, Type, Any
from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for Commands"""

    pass


class CommandHandler(ABC):
    """Base class for Command Handlers"""

    @abstractmethod
    async def handle(self, command: Command) -> Any:
        pass


class CommandBus:
    """Command Bus implementation"""

    def __init__(self):
        self._handlers: Dict[Type[Command], CommandHandler] = {}

    def register(self, command_type: Type[Command], handler: CommandHandler):
        """Register a command handler"""
        self._handlers[command_type] = handler

    async def execute(self, command: Command) -> Any:
        """Execute a command"""
        command_type = type(command)

        if command_type not in self._handlers:
            raise ValueError(
                f"No handler registered for command {command_type.__name__}"
            )

        handler = self._handlers[command_type]
        return await handler.handle(command)
