import socket

def servidor_b_persistente():
    host = '127.0.0.1'
    puerto = 12345
    
    # Creamos y configuramos el socket principal
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reutilizar la dirección si el puerto quedó en TIME_WAIT
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    servidor.bind((host, puerto))
    servidor.listen(5)
    
    print(f"[*] Servidor B listo en {host}:{puerto}. Esperando conexiones...")

    try:
        while True:
            print("\n[i] Esperando nueva conexión...")
            conexion, direccion = servidor.accept()
            print(f"[+] Conexión establecida desde {direccion}")

            try:
                # Intentamos recibir el saludo
                datos = conexion.recv(1024)
                
                if not datos:
                    # Si recv devuelve vacío, el cliente cerró la conexión limpiamente
                    print("[-] El cliente cerró la conexión sin enviar datos.")
                else:
                    mensaje = datos.decode('utf-8')
                    print(f"[>] Mensaje de A: {mensaje}")
                    
                    # Respondemos
                    respuesta = "Hola A, mensaje recibido. B sigue en línea."
                    conexion.sendall(respuesta.encode('utf-8'))
                    print("[<] Respuesta enviada con éxito.")

            except (ConnectionResetError, BrokenPipeError):
                print("[!] El cliente A se desconectó abruptamente (proceso terminado).")
            
            except Exception as e:
                print(f"[!] Error inesperado con el cliente: {e}")
            
            finally:
                # Cerramos la conexión específica con este cliente, 
                # pero el socket 'servidor' sigue vivo.
                conexion.close()
                print(f"[-] Conexión con {direccion} finalizada. Volviendo a modo escucha.")

    except KeyboardInterrupt:
        print("\n[*] Apagando el servidor B manualmente.")
    finally:
        servidor.close()

if __name__ == "__main__":
    servidor_b_persistente()