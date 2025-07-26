from typing import Dict, Any
from app.shared.infrastructure.messaging.rabbitmq_connection import RabbitMQConnection


class MessagePublisher:
    def __init__(self, rabbitmq_connection: RabbitMQConnection):
        self.rabbitmq = rabbitmq_connection

    async def publish_command(
        self, queue: str, command_type: str, data: Dict[str, Any]
    ):
        """Publish a command message"""
        message = {"command_type": command_type, "data": data}

        self.rabbitmq.publish_message(queue, message)

    async def publish_event(self, queue: str, event_type: str, data: Dict[str, Any]):
        """Publish an event message"""
        message = {"event_type": event_type, "data": data}

        self.rabbitmq.publish_message(queue, message)
