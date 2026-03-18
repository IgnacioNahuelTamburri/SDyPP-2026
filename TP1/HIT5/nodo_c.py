import socket
import threading
import sys
import time
import json  # Importamos la librería para manejar JSON

def modo_servidor(mi_ip, mi_puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((mi_ip, mi_puerto))
        servidor.listen(5)
        print(f"[*] Servidor P2P listo en {mi_ip}:{mi_puerto}")
        
        while True:
            conexion, direccion = servidor.accept()
            try:
                # Recibimos los bytes y los decodificamos a string
                datos_raw = conexion.recv(1024).decode('utf-8')
                if datos_raw:
                    # DESERIALIZACIÓN: De String JSON a Diccionario Python
                    mensaje_dicc = json.loads(datos_raw)
                    
                    print(f"\n[MENSAJE RECIBIDO]")
                    print(f"Desde: {mensaje_dicc.get('emisor')}")
                    print(f"Contenido: {mensaje_dicc.get('contenido')}")
                    print(f"Timestamp: {mensaje_dicc.get('timestamp')}")

                    # Preparamos respuesta en formato JSON
                    respuesta_dicc = {
                        "emisor": f"Nodo_{mi_puerto}",
                        "contenido": "Confirmación: JSON recibido correctamente.",
                        "status": "OK"
                    }
                    # SERIALIZACIÓN: De Diccionario a String JSON
                    conexion.sendall(json.dumps(respuesta_dicc).encode('utf-8'))
            except json.JSONDecodeError:
                print("[-] Error: Se recibió algo que no es un JSON válido.")
            except Exception as e:
                print(f"[-] Error en el servidor: {e}")
            finally:
                conexion.close()
    finally:
        servidor.close()

def modo_cliente(remoto_ip, remoto_puerto, mi_puerto):
    while True:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cliente.connect((remoto_ip, remoto_puerto))
            
            # Creamos la estructura del mensaje
            mensaje_a_enviar = {
                "emisor": f"Nodo_{mi_puerto}",
                "contenido": "¡Hola! Este es un saludo estructurado en JSON.",
                "timestamp": time.strftime("%H:%M:%S"),
                "puerto_origen": mi_puerto
            }

            # SERIALIZACIÓN: Convertimos el diccionario a una cadena JSON y luego a bytes
            payload = json.dumps(mensaje_a_enviar)
            cliente.sendall(payload.encode('utf-8'))
            
            # Recibimos y deserializamos la respuesta
            respuesta_raw = cliente.recv(1024).decode('utf-8')
            if respuesta_raw:
                respuesta_json = json.loads(respuesta_raw)
                print(f"\n[RESPUESTA DE {remoto_puerto}]: {respuesta_json['contenido']}")
            
            time.sleep(10) # Espera entre saludos
            
        except (ConnectionRefusedError, ConnectionResetError):
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

    m_ip, m_port = sys.argv[1], int(sys.argv[2])
    r_ip, r_port = sys.argv[3], int(sys.argv[4])

    # Hilo para el servidor
    threading.Thread(target=modo_servidor, args=(m_ip, m_port), daemon=True).start()

    try:
        modo_cliente(r_ip, r_port, m_port)
    except KeyboardInterrupt:
        print("\n[-] Saliendo...")