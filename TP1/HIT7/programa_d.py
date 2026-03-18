import socket
import threading
import json
import time
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
ARCHIVO_LOG = "inscripciones.json"
ventana_actual = []   # Nodos participando AHORA
ventana_siguiente = [] # Nodos inscribiéndose para el próximo minuto

def guardar_log(evento, data):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": evento,
        "detalles": data
    }
    with open(ARCHIVO_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def orquestador_temporal():
    """Hilo que rota las ventanas cada minuto exacto"""
    global ventana_actual, ventana_siguiente
    while True:
        # Calcular cuánto falta para el próximo minuto exacto (segundo 00)
        ahora = datetime.now()
        espera = 60 - ahora.second
        time.sleep(espera)
        
        # Rotación de ventanas
        ventana_actual = list(ventana_siguiente)
        ventana_siguiente = []
        
        info = {
            "nueva_ventana_activa": ventana_actual,
            "minuto_inicio": datetime.now().strftime("%H:%M")
        }
        print(f"\n[TEMPORIZADOR] Ciclo completado. Nodos activos para este minuto: {len(ventana_actual)}")
        guardar_log("ROTACION_VENTANA", info)

def iniciar_registro_tcp(ip_d, puerto_d):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_d, puerto_d))
    server.listen(10)
    
    while True:
        conn, addr = server.accept()
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                solicitud = json.loads(data) # C envía {"ip":..., "puerto":...}
                
                # 1. El nodo C se anota para la SIGUIENTE ventana
                nuevo_nodo = {"ip": solicitud['ip'], "puerto": solicitud['puerto']}
                if nuevo_nodo not in ventana_siguiente:
                    ventana_siguiente.append(nuevo_nodo)
                    guardar_log("INSCRIPCION_RECIBIDA", {"nodo": nuevo_nodo, "para_minuto": (datetime.now() + timedelta(minutes=1)).minute})
                
                # 2. Le respondemos con la lista de la ventana ACTUAL (los que ya están activos)
                conn.sendall(json.dumps(ventana_actual).encode('utf-8'))
        finally:
            conn.close()

if __name__ == "__main__":
    # Iniciar el hilo que cambia las ventanas cada minuto
    threading.Thread(target=orquestador_temporal, daemon=True).start()
    print("[*] Nodo D: Orquestador de Ventanas iniciado (127.0.0.1:8000)")
    iniciar_registro_tcp('127.0.0.1', 8000)