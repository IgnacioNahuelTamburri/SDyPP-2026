import socket

def cliente_a():
    host = '127.0.0.1'
    puerto = 12345

    # Creamos el socket para el cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Intentamos conectar con el servidor B
        cliente.connect((host, puerto))
        
        # Enviamos el saludo
        saludo = "Hola Servidor B, soy el Cliente A. ¿Me escuchas?"
        cliente.sendall(saludo.encode('utf-8'))

        # Esperamos la respuesta de B
        respuesta_b = cliente.recv(1024).decode('utf-8')
        print(f"Respuesta de B: {respuesta_b}")

    except ConnectionRefusedError:
        print("Error: No se pudo conectar.")
    
    finally:
        cliente.close()

if __name__ == "__main__":
    cliente_a()