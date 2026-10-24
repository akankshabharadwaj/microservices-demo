import pika
import os
import time

def callback(ch, method, properties, body):
    print("Received order:", body.decode(), flush=True)

def connect():
    while True:
        try:
            print("Connecting to RabbitMQ...", flush=True)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials(
                        os.environ['RABBITMQ_USER'],
                        os.environ['RABBITMQ_PASSWORD']
                    )
                )
            )
            print("Connected to RabbitMQ", flush=True)
            return connection
        except Exception as e:
            print("Connection failed:", e, flush=True)
            time.sleep(5)

while True:
    try:
        connection = connect()
        channel = connection.channel()

        channel.queue_declare(queue='orders', durable=False)

        print("Waiting for messages...", flush=True)

        channel.basic_consume(
            queue='orders',
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()

    except Exception as e:
        print("Error occurred:", e, flush=True)
        time.sleep(5)