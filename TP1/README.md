# Hit #1: El Saludo Básico (TCP)
### **Concepto: Comunicación unidireccional básica.**
Servidor (B): Escucha en un puerto fijo.

Cliente (A): Conecta, saluda y cierra.

Uso: Ejecutar servidor_b.py y luego cliente_a.py.

# Hit #2 y #3: Resiliencia y Reconexión
### **Concepto: Manejo de fallos y sockets persistentes.**

Cliente A: Implementa un bucle de reintento con backoff (espera) si B no está disponible.

Servidor B: Implementa try/except para no morir si A cierra la conexión abruptamente.

# Hit #4: El Nodo Híbrido (P2P)
### **Concepto: Simetría. El programa C es Cliente y Servidor simultáneamente usando threading.**

Uso: 

Terminal 1 (Nodo 1) ```python nodo_c.py 127.0.0.1 5001 127.0.0.1 5002```

Terminal 2 (Nodo 2) ```python nodo_c.py 127.0.0.1 5002 127.0.0.1 5001```

# Hit #5: Serialización de Datos (JSON)
### **Concepto: Estructuración de datos. Los mensajes dejan de ser texto plano para ser objetos JSON (dict en Python).**

Mejora: Se añade timestamp, emisor y contenido.

# Hit #6: Registro de Contactos (Nodo D)
### **Concepto: Service Discovery. Aparece el Nodo D como directorio central.**

Nodo D: Mantiene un array en RAM de los nodos C activos.

Nodo C: Ya no necesita IPs de pares. Pregunta a D: "¿Quién hay?" y saluda a la lista recibida.

Health Check: D expone un endpoint en http://localhost:8080/health.

# Hit #7: El Orquestador de Ventanas Temporales
### **Concepto: Sincronización por épocas (Epochs).**

Lógica: D gestiona dos listas: Actual (participantes ahora) y Siguiente (inscritos para el próximo minuto).

Persistencia: Cada movimiento se guarda en inscripciones.json.

Uso: Los nodos C que entran en el segundo 45 deben esperar al segundo 00 del siguiente minuto para ser "visibles".

# Hit #8: Refactorización a gRPC y Protobuf
### **Concepto: Optimización de protocolos y tipado estricto.**

Cambio: Se elimina el JSON manual por Protocol Buffers.

Compilación del contrato:

```python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. comunicacion.proto```
Ventaja: Mensajes mucho más ligeros (binarios) y menor latencia que el TCP crudo con strings.

Cómo ejecutar la versión final (P2P + gRPC + Ventanas)
Iniciar el Directorio (Nodo D):

```python programa_d.py```
D comenzará a contar los segundos para rotar las ventanas cada minuto.

Iniciar Nodos C (múltiples instancias):

# En distintas terminales
```python programa_c.py```
Cada nodo C se registrará para la ventana del minuto siguiente.

Verificación:

Revisa inscripciones.json para ver el historial de registros.

Accede a http://localhost:8080/health para ver el estado del sistema.
