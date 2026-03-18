import socket
import threading
import sys
import time

def modo_servidor(mi_ip, mi_puerto):
    """Función que actúa como el Servidor (B)"""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((mi_ip, mi_puerto))
        servidor.listen(5)
        print(f"[*] Servidor local listo en {mi_ip}:{mi_puerto}")
        
        while True:
            conexion, direccion = servidor.accept()
            try:
                datos = conexion.recv(1024).decode('utf-8')
                if datos:
                    print(f"\n[Recibido de {direccion}]: {datos}")
                    respuesta = f"¡Hola! Soy el nodo en el puerto {mi_puerto}, recibí tu saludo."
                    conexion.sendall(respuesta.encode('utf-8'))
            except Exception as e:
                print(f"[-] Error en recepción: {e}")
            finally:
                conexion.close()
    except Exception as e:
        print(f"[-] Error fatal en el servidor: {e}")
    finally:
        servidor.close()

def modo_cliente(remoto_ip, remoto_puerto, mi_puerto):
    """Función que actúa como el Cliente (A) con reconexión"""
    print(f"[*] Cliente intentando conectar a {remoto_ip}:{remoto_puerto}...")
    
    while True:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cliente.connect((remoto_ip, remoto_puerto))
            saludo = f"Saludos desde el nodo con puerto {mi_puerto}."
            cliente.sendall(saludo.encode('utf-8'))
            
            respuesta = cliente.recv(1024).decode('utf-8')
            if respuesta:
                print(f"\n[Respuesta del nodo remoto]: {respuesta}")
            
            # Esperamos un poco antes de volver a saludar para no saturar la consola
            time.sleep(10)
            
        except (ConnectionRefusedError, ConnectionResetError):
            # Si el otro nodo no ha subido su servidor, esperamos silenciosamente
            time.sleep(2)
        except Exception as e:
            print(f"[-] Error en el cliente: {e}")
            time.sleep(5)
        finally:
            cliente.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python nodo_c.py <MI_IP> <MI_PUERTO> <IP_REMOTO> <PUERTO_REMOTO>")
        sys.exit(1)

    mi_ip = sys.argv[1]
    mi_puerto = int(sys.argv[2])
    remoto_ip = sys.argv[3]
    remoto_puerto = int(sys.argv[4])

    # Lanzamos el Servidor en un hilo secundario (Background)
    hilo_servidor = threading.Thread(target=modo_servidor, args=(mi_ip, mi_puerto), daemon=True)
    hilo_servidor.start()

    # Ejecutamos el Cliente en el hilo principal
    try:
        modo_cliente(remoto_ip, remoto_puerto, mi_puerto)
    except KeyboardInterrupt:
        print("\n[-] Nodo finalizado por el usuario.")