import socket
import threading
import sys
import json
import time

def servidor_escucha_c(sock):
    sock.listen(10)
    while True:
        conn, addr = sock.accept()
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                msg = json.loads(data)
                print(f"\n[RECIBIDO] Saludo de {msg['emisor']} en la ventana actual.")
        finally:
            conn.close()

def inscribirse_y_saludar(ip_d, puerto_d, mi_ip, mi_puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_d, puerto_d))
        
        # Enviamos datos para la inscripción futura
        registro = {"ip": mi_ip, "puerto": mi_puerto}
        s.sendall(json.dumps(registro).encode('utf-8'))
        
        # D nos responde con los nodos que YA están activos ahora
        respuesta = s.recv(4096).decode('utf-8')
        pares_activos = json.loads(respuesta)
        s.close()

        if not pares_activos:
            print("[*] Inscrito para el próximo minuto. No hay nodos activos en esta ventana.")
        else:
            print(f"[*] Inscrito. Saludando a {len(pares_activos)} nodos activos ahora...")
            for par in pares_activos:
                try:
                    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    c.settimeout(1)
                    c.connect((par['ip'], par['puerto']))
                    c.sendall(json.dumps({"emisor": mi_puerto, "contenido": "¡Hola par activo!"}).encode('utf-8'))
                    c.close()
                except: pass
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python nodo_c.py <IP_D> <PUERTO_D>")
        sys.exit(1)

    ip_d, puerto_d = sys.argv[1], int(sys.argv[2])
    
    # Preparar servidor en puerto aleatorio
    sock_escucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_escucha.bind(('127.0.0.1', 0))
    mi_puerto = sock_escucha.getsockname()[1]
    
    print(f"=== NODO C INICIADO (Puerto: {mi_puerto}) ===")
    threading.Thread(target=servidor_escucha_c, args=(sock_escucha,), daemon=True).start()

    # Ejecutar la lógica de inscripción
    inscribirse_y_saludar(ip_d, puerto_d, '127.0.0.1', mi_puerto)

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: pass