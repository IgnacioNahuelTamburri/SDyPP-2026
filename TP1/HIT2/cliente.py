import socket
import time

def cliente_a_robusto():
    host = '127.0.0.1'
    puerto = 12345
    reintentos = 0

    print("--- Iniciando Cliente A (Modo Persistente) ---")

    while True:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Intentamos conectar
            cliente.connect((host, puerto))
            print(f"\n[+] Conectado a B tras {reintentos} reintentos fallidos.")
            reintentos = 0 # Reiniciamos el contador al conectar con éxito

            # Enviamos el saludo
            saludo = "Hola B, aquí A intentando mantener el contacto."
            cliente.sendall(saludo.encode('utf-8'))

            # Esperamos respuesta
            # Si B se cierra aquí, recv() devolverá 0 bytes o lanzará ConnectionResetError
            respuesta = cliente.recv(1024).decode('utf-8')
            
            if not respuesta:
                # Si recibimos un mensaje vacío, es que el socket se cerró ordenadamente
                raise ConnectionResetError
                
            print(f"B respondió: {respuesta}")
            
            # Mantenemos la conexión viva o la cerramos según lógica de negocio
            # Para este ejemplo, cerramos y volvemos a empezar tras una pausa
            time.sleep(5) 

        except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError):
            reintentos += 1
            print(f"[!] B no disponible. Reintentando en 3 segundos... (Intento #{reintentos})", end='\r')
            time.sleep(3)
        
        except KeyboardInterrupt:
            print("\n[-] Deteniendo el cliente A por el usuario.")
            break
            
        finally:
            cliente.close()

if __name__ == "__main__":
    cliente_a_robusto()