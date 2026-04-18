import pika
import sys

broker = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
)

connection = pika.BlockingConnection(parameters=broker)
channel = connection.channel()

# Declarar el exchange de tipo 'fanout'
channel.exchange_declare(exchange='mi_exchange_fanout', exchange_type='fanout', durable=False)

# Crear una cola única para este consumer (aleatoria y exclusiva)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Vincular la cola al exchange
channel.queue_bind(exchange='mi_exchange_fanout', queue=queue_name)

channel.basic_qos(prefetch_count=1)

print(f'[Consumer] Cola creada: {queue_name}')
print('[Consumer] Esperando mensajes. Presiona CTRL+C para salir.\n')


def callback(ch, method, properties, body):
    mensaje = body.decode()
    print(f"[Consumer] Recibido: {mensaje}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('\n[Consumer] Detenido por el usuario.')
    channel.stop_consuming()
finally:
    connection.close()
