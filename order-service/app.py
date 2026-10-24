from flask import Flask, request, jsonify
import pika
import json
import os
import time

app = Flask(__name__)

def connect():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials(
                        os.environ['RABBITMQ_USER'],
                        os.environ['RABBITMQ_PASSWORD']
                    )
                )
            )
            return connection
        except Exception as e:
            print(f"RabbitMQ connection failed: {e!r}")
            time.sleep(5)

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json

    connection = connect()
    channel = connection.channel()

    channel.queue_declare(queue='orders')

    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=json.dumps(data)
    )
    
    connection.close()
    print("Sending message:", data)
    return jsonify({"status": "Order sent", "data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)