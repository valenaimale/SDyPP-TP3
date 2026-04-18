# SDyPP-TP3

## Ejemplo 1 - Message Queue (punto a punto)

Este ejemplo demuestra el uso de RabbitMQ en un patrón punto a punto: un productor envía mensajes a una cola, y los consumidores los procesan. Cada mensaje es procesado exactamente por un consumidor.

### Archivos
- `producer.py`: Envía 10 tareas numeradas a la cola `cola_mensajes`.
- `consumer.py`: Consumidor que recibe e imprime mensajes de la cola.

### Comparación de comportamientos

#### Con 1 consumidor
- El productor envía 10 mensajes.
- El único consumidor recibe y procesa todos los mensajes en secuencia (Mensaje 1, 2, ..., 10).
- Los mensajes se eliminan de la cola solo después del ack (confirmación de procesamiento).

#### Con 2 consumidores (round-robin)
- El productor envía 10 mensajes.
- RabbitMQ distribuye los mensajes alternadamente entre los dos consumidores conectados.
- Ejemplo observado: Mensaje 1 → Consumidor 1, Mensaje 2 → Consumidor 2, Mensaje 3 → Consumidor 1, etc.
- Cada consumidor procesa aproximadamente la mitad de los mensajes (5 cada uno, si son 10).
- No hay duplicados; cada mensaje se procesa exactamente una vez.

### Cómo ejecutar

1. Asegúrate de que RabbitMQ esté corriendo en `localhost:5672` (usuario/contraseña: guest/guest).
2. Ejecuta el productor:
   ```
   python Hit0/Ejemplo1/producer.py
   ```
3. Para 1 consumidor:
   ```
   python Hit0/Ejemplo1/consumer.py
   ```
4. Para 2 consumidores (en terminales separadas):
   ```
   python Hit0/Ejemplo1/consumer.py
   ```
   (Ejecuta el comando dos veces en terminales distintas).

### Explicación de round-robin en RabbitMQ

En RabbitMQ, el round-robin es un mecanismo de distribución de mensajes entre consumidores conectados a la misma cola. A diferencia del round-robin en scheduling de CPU (que asigna tiempo fijo o "quantum" a procesos), aquí no hay quantum de tiempo.

- **Cómo funciona**: Los mensajes se entregan uno por uno a consumidores en secuencia circular. Si hay N consumidores, el primer mensaje va al consumidor 1, el segundo al 2, ..., el N+1 al 1, y así sucesivamente.
- **Prefetch**: Con `prefetch_count=1` (como en el código), cada consumidor recibe solo un mensaje a la vez hasta confirmar el anterior. Esto asegura distribución justa, incluso si un consumidor es más lento.
- **Sin prefetch**: Si no hay límite, un consumidor rápido podría recibir muchos mensajes antes de que otros procesen, rompiendo el balance.
- **Ventaja**: Es eficiente y automático; el broker empuja mensajes sin polling.

Para observar, ejecuta el código y mira los logs en consola.

### Cómo ejecutar

1. Asegúrate de que RabbitMQ esté corriendo en `localhost:5672` (usuario/contraseña: guest/guest).
2. En una terminal, ejecuta el primer consumidor:
   ```bash
   python Hit0/Ejemplo1/consumer.py
   ```
3. En otra terminal, ejecuta el segundo consumidor:
   ```bash
   python Hit0/Ejemplo1/consumer.py
   ```
   (Esto crea dos consumidores independientes conectados a la misma cola.)
4. En una tercera terminal, ejecuta el productor:
   ```bash
   python Hit0/Ejemplo1/producer.py
   ```

### Observación
- Con 1 consumidor, ese consumidor procesa los 10 mensajes.
- Con 2 consumidores, RabbitMQ reparte los mensajes entre ambos en forma aproximada round-robin.
- Si quieres ver cómo se reparten, mira las dos terminales de los consumidores mientras ejecutas el productor.

### Importante
- No necesitas Docker para este ejemplo.
- Si el puerto `5672` ya está ocupado, detén la instancia de RabbitMQ anterior o cambia tu configuración local.
- El ejercicio funciona con RabbitMQ instalado localmente y los scripts `producer.py`/`consumer.py` ejecutados desde Python.
