import asyncio
from app.shared.infrastructure.messaging.rabbitmq_connection import RabbitMQConnection
from app.shared.infrastructure.messaging.message_publisher import MessagePublisher


async def main():
    rabbitmq = RabbitMQConnection("amqp://guest:guest@localhost:5672/")
    publisher = MessagePublisher(rabbitmq)

    await publisher.publish_event(
        queue="my_test_queue",
        event_type="UserRegistered",
        data={"id": "123", "email": "usuario@demo.com"},
    )


if __name__ == "__main__":
    asyncio.run(main())
