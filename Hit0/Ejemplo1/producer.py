import pika

broker = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
)

connection = pika.BlockingConnection(parameters=broker)
channel = connection.channel()

# Asegurarse de que la cola exista antes de publicar.
channel.queue_declare(queue='cola_mensajes', durable=False)

for i in range(1, 11):
    channel.basic_publish(
        exchange='',
        routing_key='cola_mensajes',
        body=f"Mensaje {i}"
    )
    print(f"[Producer] Mensaje {i} enviado")

connection.close()    