import socket

def servidor_b():
    # Creamos el socket: AF_INET para IPv4, SOCK_STREAM para TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configuramos el host y el puerto
    host = '127.0.0.1' # Localhost
    puerto = 12345
    
    servidor.bind((host, puerto))
    servidor.listen(1) # El servidor se pone en modo escucha
    print(f"Servidor B iniciado en {host}:{puerto}. Esperando a A...")

    # Aceptamos la conexión
    conexion, direccion = servidor.accept()
    print(f"Conectado con éxito por: {direccion}")

    try:
        # Esperamos el saludo de A (máximo 1024 bytes)
        mensaje_recibido = conexion.recv(1024).decode('utf-8')
        print(f"A dice: {mensaje_recibido}")

        # Respondemos el saludo
        respuesta = "¡Hola A! Recibí tu saludo. Aquí B, fuerte y claro."
        conexion.sendall(respuesta.encode('utf-8'))
    
    finally:
        conexion.close()
        servidor.close()

if __name__ == "__main__":
    servidor_b()