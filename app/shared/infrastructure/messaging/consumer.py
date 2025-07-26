import pika
import json


def callback(ch, method, properties, body):
    try:
        print(f"📦 Raw message: {body}")
        message = json.loads(body.decode("utf-8"))
        print(f"📩 Mensaje recibido: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar JSON: {e}")
        # Puedes enviar un nack para rechazar el mensaje
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def consume(queue_name: str):
    connection = pika.BlockingConnection(
        pika.URLParameters("amqp://guest:guest@localhost:5672/")
    )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(f"👂 Escuchando en la cola '{queue_name}'...")
    channel.start_consuming()


if __name__ == "__main__":
    consume("my_test_queue")
