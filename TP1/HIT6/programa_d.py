import socket
import threading
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- CONFIGURACIÓN Y BASE DE DATOS EN RAM ---
NODOS_REGISTRADOS = [] # Lista de diccionarios {"ip": ..., "puerto": ...}
START_TIME = time.time()

# --- SERVIDOR HTTP PARA HEALTH CHECK ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                "nodos_registrados_count": len(NODOS_REGISTRADOS),
                "uptime_seconds": int(time.time() - START_TIME),
                "estado_general": "OPERACIONAL",
                "nodos": NODOS_REGISTRADOS
            }
            self.wfile.write(json.dumps(status).encode('utf-8'))
        else:
            self.send_error(404)

    def log_message(self, format, *args): return # Silenciar logs de consola HTTP

def iniciar_http(puerto_http):
    web_server = HTTPServer(('0.0.0.0', puerto_http), HealthCheckHandler)
    print(f"[*] Endpoint HTTP Health Check en http://localhost:{puerto_http}/health")
    web_server.serve_forever()

# --- SERVIDOR TCP DE REGISTRO ---
def iniciar_registro_tcp(ip_d, puerto_d):
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp.bind((ip_d, puerto_d))
    server_tcp.listen(10)
    print(f"[*] Nodo D (Registro) escuchando en {ip_d}:{puerto_d}")

    while True:
        conn, addr = server_tcp.accept()
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                solicitud = json.loads(data) # C envía {"ip":..., "puerto":...}
                
                # 1. Enviar la lista actual de pares a C (antes de agregarlo a él mismo)
                pares_actuales = list(NODOS_REGISTRADOS)
                conn.sendall(json.dumps(pares_actuales).encode('utf-8'))
                
                # 2. Registrar el nuevo nodo si no existe
                nuevo_nodo = {"ip": solicitud['ip'], "puerto": solicitud['puerto']}
                if nuevo_nodo not in NODOS_REGISTRADOS:
                    NODOS_REGISTRADOS.append(nuevo_nodo)
                    print(f"[+] Nuevo nodo registrado: {nuevo_nodo}")

        except Exception as e:
            print(f"[-] Error en registro TCP: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    # D corre en el puerto 8000 (TCP) y 8080 (HTTP)
    threading.Thread(target=iniciar_http, args=(8080,), daemon=True).start()
    iniciar_registro_tcp('127.0.0.1', 8000)