import grpc
import comunicacion_pb2
import comunicacion_pb2_grpc
import sys

def ejecutar_c(ip_d, puerto_d):
    # Crear el canal gRPC
    with grpc.insecure_channel(f'{ip_d}:{puerto_d}') as channel:
        stub = comunicacion_pb2_grpc.RegistroServiceStub(channel)
        
        # Puerto aleatorio simulado (en producción usaríamos sockets para obtenerlo)
        mi_puerto = 5555 
        
        # Llamada RPC
        print("[*] Intentando registro vía gRPC...")
        solicitud = comunicacion_pb2.SolicitudRegistro(ip="127.0.0.1", puerto=mi_puerto)
        
        try:
            respuesta = stub.RegistrarNodo(solicitud)
            print(f"[*] Registrado. Nodos activos en esta ventana: {len(respuesta.nodos)}")
            for nodo in respuesta.nodos:
                print(f"  -> Par activo encontrado: {nodo.ip}:{nodo.puerto}")
        except grpc.RpcError as e:
            print(f"[-] Error gRPC: {e.details()}")

if __name__ == "__main__":
    ejecutar_c('127.0.0.1', 50051)