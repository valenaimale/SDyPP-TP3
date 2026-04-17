import pika

broker = pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=pika.PlainCredentials ('guest', 'guest'))

connection = pika.BlockingConnection(parameters=broker)

canal= connection.channel()##Devuelve un objeto de tipo Channel

for i in range(1, 11):
    canal.basic_publish(##funcion para publicar en la cola
        exchange='',##vacio porque el default es punto a punto (el que se requiere para este ejemplo)
        routing_key= 'cola_mensajes',##nombre de la cola donde se va a publicar el mensaje
        body= f"Mensaje {i}"
    )