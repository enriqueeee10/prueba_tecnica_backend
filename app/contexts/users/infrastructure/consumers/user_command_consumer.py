import asyncio
import json
import pika
from typing import Dict, Any

from app.config.container import Container
from app.contexts.users.application.commands.create_user_command import (
    CreateUserCommand,
)
from app.contexts.users.application.commands.create_user_handler import (
    CreateUserHandler,
)


class UserCommandConsumer:
    def __init__(self):
        self.container = Container()
        self.container.wire(modules=[__name__])

        # Setup RabbitMQ connection
        self.connection = pika.BlockingConnection(
            pika.URLParameters("amqp://guest:guest@rabbitmq:5672/")
        )
        self.channel = self.connection.channel()

        # Declare queues
        self.channel.queue_declare(queue="user_commands", durable=True)

    def start_consuming(self):
        """Start consuming messages from RabbitMQ"""
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="user_commands", on_message_callback=self.process_message
        )

        print("Starting to consume user commands...")
        self.channel.start_consuming()

    def process_message(self, ch, method, properties, body):
        """Process incoming command messages"""
        try:
            message = json.loads(body.decode("utf-8"))
            command_type = message.get("command_type")
            data = message.get("data", {})

            if command_type == "CreateUserCommand":
                asyncio.run(self._handle_create_user(data))

            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"Error processing message: {e}")
            # Reject message and don't requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    async def _handle_create_user(self, data: Dict[str, Any]):
        """Handle CreateUserCommand"""
        handler = self.container.create_user_handler()

        command = CreateUserCommand(
            name=data["name"], email=data["email"], password=data["password"]
        )

        await handler.handle(command)
        print(f"User created: {data['email']}")


if __name__ == "__main__":
    consumer = UserCommandConsumer()
    consumer.start_consuming()
