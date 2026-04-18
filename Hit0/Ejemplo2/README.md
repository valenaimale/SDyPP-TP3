# SDyPP-TP3

## Ejemplo 2 - Fanout Exchange (broadcast)

Este ejemplo demuestra el uso de RabbitMQ con un patrón de broadcast mediante un exchange tipo fanout: un productor envía mensajes a un exchange, y todos los consumidores conectados reciben **una copia** de cada mensaje. Cada consumidor tiene su propia cola exclusiva.

### Arquitectura

```
┌─────────────────┐
│   Producer      │ Envía 10 mensajes
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Fanout Exchange                      │ (broadcast a todas las colas)
│ mi_exchange_fanout                   │
└──┬──────────────┬──────────────┬─────┘
   │              │              │
   ▼              ▼              ▼
┌─────┐   ┌─────┐    ┌─────┐
│Q: 1 │   │Q: 2 │    │Q: 3 │  Colas exclusivas
└──┬──┘   └──┬──┘    └──┬──┘
   │         │         │
   ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Consum. │ │Consum. │ │Consum. │  Cada uno recibe
│  1     │ │  2     │ │  3     │  TODOS los mensajes
└────────┘ └────────┘ └────────┘  (copia idéntica)
```

### Archivos
- `producer.py`: Envía 10 mensajes al exchange `mi_exchange_fanout`.
- `consumer.py`: Consumidor que crea una cola exclusiva, la vincula al exchange y recibe e imprime todos los mensajes.

### Comparación de comportamientos

#### Con 1 consumidor
- El productor envía 10 mensajes al exchange fanout.
- El único consumidor recibe todos los 10 mensajes (Mensaje 1, 2, ..., 10).
- Cada mensaje se recibe exactamente una vez por el consumidor.

#### Con 3 consumidores
- El productor envía 10 mensajes al exchange fanout.
- **Cada consumidor recibe todos los 10 mensajes** (copia idéntica).
- No hay distribución round-robin como en point-to-point; es un broadcast.
- Cada consumidor procesa de forma independiente los mismos mensajes.
- Ejemplo observado: 
  - Consumidor 1 recibe: Mensaje 1, 2, 3, ..., 10
  - Consumidor 2 recibe: Mensaje 1, 2, 3, ..., 10
  - Consumidor 3 recibe: Mensaje 1, 2, 3, ..., 10

### Explicación de Fanout Exchange en RabbitMQ

El fanout exchange es un patrón de broadcast puro. Funciona así:

- **Cómo funciona**: El exchange recibe un mensaje y lo replica a todas las colas vinculadas a él, sin considerar routing_key.
- **Colas exclusivas**: Cada consumidor crea su propia cola exclusiva (`exclusive=True`) al conectarse, garantizando que sea única y privada.
- **Binding**: Cada cola se vincula al exchange, y cuando el exchange recibe un mensaje, lo copia a todas las colas vinculadas.
- **Uso**: Ideal para notificaciones, eventos que deben procesarse por múltiples servicios, o streaming de datos a varios listeners.
- **Ventaja**: Simplicidad; todos reciben el mismo mensaje sin necesidad de routing_key.

### Diferencia con Ejemplo 1 (Point-to-Point vs Broadcast)

| Aspecto | Ejemplo 1 (Direct) | Ejemplo 2 (Fanout) |
|--------|-------------------|-------------------|
| **Patrón** | Point-to-point | Broadcast |
| **Cola** | Una cola compartida | Colas exclusivas por consumer |
| **Distribución** | Round-robin (cada mensaje a un consumer) | Replicación (todos reciben copia) |
| **Duplicados** | No | Sí (duplicado en cada consumer) |
| **Uso** | Tareas distribuidas | Notificaciones, eventos |

### Cómo ejecutar

1. Asegúrate de que RabbitMQ esté corriendo en `localhost:5672` (usuario/contraseña: guest/guest).
2. En una terminal, ejecuta el primer consumidor:
   ```bash
   python Hit0/Ejemplo2/consumer.py
   ```
3. En una segunda terminal, ejecuta el segundo consumidor:
   ```bash
   python Hit0/Ejemplo2/consumer.py
   ```
4. En una tercera terminal, ejecuta el tercer consumidor:
   ```bash
   python Hit0/Ejemplo2/consumer.py
   ```
   (Esto crea tres consumidores independientes, cada uno con su cola exclusiva vinculada al exchange.)
5. En una cuarta terminal, ejecuta el productor:
   ```bash
   python Hit0/Ejemplo2/producer.py
   ```

### Observación
- Con 1 consumidor, ese consumidor recibe los 10 mensajes.
- Con 3 consumidores, **todos reciben los mismos 10 mensajes** (copia idéntica).
- Mira las tres terminales de los consumidores mientras ejecutas el productor; verás que todos reciben exactamente el mismo contenido, al mismo tiempo.
- Si detiene un consumidor antes de que el productor envíe, ese consumidor pierde esos mensajes (las colas exclusivas se eliminan al desconectarse).

### Importante
- No necesitas Docker para este ejemplo.
- Las colas son **exclusivas** y **temporales**: se eliminan cuando el consumidor se desconecta.
- El prefetch_count se configura en 1 para evitar sobrecargar la red, pero con fanout todos reciben de todas formas.
- Este patrón es ideal cuando múltiples servicios necesitan reaccionar a los mismos eventos.
