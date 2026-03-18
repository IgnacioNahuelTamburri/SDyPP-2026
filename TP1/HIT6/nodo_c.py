import socket
import threading
import sys
import json
import time

def modo_servidor_c(sock_escucha):
    """Escucha saludos de otros nodos C"""
    sock_escucha.listen(5)
    while True:
        conn, addr = sock_escucha.accept()
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                msg = json.loads(data)
                print(f"\n[C-SERVER] Saludo de {msg['emisor']}: {msg['contenido']}")
        finally:
            conn.close()

def enviar_saludo(ip, puerto, mi_puerto):
    """Función auxiliar para saludar a un par específico"""
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.settimeout(2)
        c.connect((ip, puerto))
        payload = {
            "emisor": f"Nodo_{mi_puerto}",
            "contenido": "¡Hola par! Nodo D me dio tu contacto.",
            "timestamp": time.strftime("%H:%M:%S")
        }
        c.sendall(json.dumps(payload).encode('utf-8'))
        c.close()
    except:
        pass # El par podría haberse desconectado

def modo_cliente_c(ip_d, puerto_d, mi_ip, mi_puerto):
    """Se registra en D y saluda a los pares obtenidos"""
    try:
        # 1. Conectar a D para registrarse y obtener pares
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_d, puerto_d))
        
        registro = {"ip": mi_ip, "puerto": mi_puerto}
        s.sendall(json.dumps(registro).encode('utf-8'))
        
        # Recibir lista de pares
        respuesta = s.recv(4096).decode('utf-8')
        pares = json.loads(respuesta)
        s.close()
        
        print(f"[*] Registrado en D. Recibidos {len(pares)} pares conocidos.")

        # 2. Saludar a cada par recibido
        for par in pares:
            print(f"[*] Saludando a par en {par['ip']}:{par['puerto']}...")
            enviar_saludo(par['ip'], par['puerto'], mi_puerto)

    except Exception as e:
        print(f"[-] Error contactando al Registro D: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python nodo_c.py <IP_D> <PUERTO_D>")
        sys.exit(1)

    ip_d, puerto_d = sys.argv[1], int(sys.argv[2])

    # Crear socket con puerto aleatorio asignado por el OS (port=0)
    mi_ip = '127.0.0.1'
    sock_escucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_escucha.bind((mi_ip, 0))
    mi_puerto = sock_escucha.getsockname()[1]
    
    print(f"=== NODO C INICIADO EN PUERTO: {mi_puerto} ===")

    # Iniciar hilo de escucha (Servidor)
    threading.Thread(target=modo_servidor_c, args=(sock_escucha,), daemon=True).start()

    # Ejecutar lógica de registro y saludo (Cliente)
    modo_cliente_c(ip_d, puerto_d, mi_ip, mi_puerto)

    # Mantener el programa vivo
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("Saliendo...")