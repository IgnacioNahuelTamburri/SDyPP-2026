import grpc
from concurrent import futures
import comunicacion_pb2
import comunicacion_pb2_grpc
import threading
import time

ventana_actual = []
ventana_siguiente = []

class RegistroServicer(comunicacion_pb2_grpc.RegistroServiceServicer):
    def RegistrarNodo(self, request, context):
        global ventana_siguiente
        
        # Registrar para la siguiente ventana
        nuevo = {"ip": request.ip, "puerto": request.puerto}
        if nuevo not in ventana_siguiente:
            ventana_siguiente.append(nuevo)
            print(f"[+] Inscrito vía gRPC: {nuevo['ip']}:{nuevo['puerto']}")

        # Responder con la lista ACTUAL usando objetos Protobuf
        lista_pb = comunicacion_pb2.ListaNodos()
        for n in ventana_actual:
            lista_pb.nodos.add(ip=n['ip'], puerto=n['puerto'])
        
        return lista_pb

def orquestador_temporal():
    global ventana_actual, ventana_siguiente
    while True:
        time.sleep(60 - (time.time() % 60))
        ventana_actual = list(ventana_siguiente)
        ventana_siguiente = []
        print(f"[*] Ventana rotada. Activos: {len(ventana_actual)}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comunicacion_pb2_grpc.add_RegistroServiceServicer_to_server(RegistroServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("[*] Servidor D (gRPC) escuchando en el puerto 50051...")
    
    threading.Thread(target=orquestador_temporal, daemon=True).start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()