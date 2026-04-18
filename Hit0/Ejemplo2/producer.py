import pika

broker = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
)

connection = pika.BlockingConnection(parameters=broker)
channel = connection.channel()

# Declarar el exchange de tipo 'fanout'
channel.exchange_declare(exchange='mi_exchange_fanout', exchange_type='fanout', durable=False)

print('[Producer] Exchange "mi_exchange_fanout" creado.')
print('[Producer] Enviando mensajes a todos los consumers...\n')

for i in range(1, 11):
    mensaje = f"Mensaje {i}"
    channel.basic_publish(
        exchange='mi_exchange_fanout',
        routing_key='',  # En fanout no se usa routing_key
        body=mensaje
    )
    print(f"[Producer] Enviado: {mensaje}")

print('\n[Producer] Todos los mensajes enviados.')
connection.close()
