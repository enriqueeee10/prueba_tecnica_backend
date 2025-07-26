import pika
import json
from typing import Dict, Any


class RabbitMQConnection:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
            self.channel = self.connection.channel()

    def publish_message(self, queue: str, message: Dict[str, Any]):
        """Publish a message to a queue"""
        self.connect()

        self.channel.queue_declare(queue=queue, durable=True)

        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
        )

    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
