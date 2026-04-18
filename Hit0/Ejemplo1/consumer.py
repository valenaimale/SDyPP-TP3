import pika

broker = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
)

connection = pika.BlockingConnection(parameters=broker)
channel = connection.channel()

channel.queue_declare(queue='cola_mensajes', durable=False)
channel.basic_qos(prefetch_count=1)

print('[Consumer] Esperando mensajes. Presiona CTRL+C para salir.')


def callback(ch, method, properties, body):
    mensaje = body.decode()
    print(f"[Consumer] Recibido: {mensaje}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='cola_mensajes', on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('\n[Consumer] Detenido por el usuario.')
    channel.stop_consuming()
finally:
    connection.close()