import os
import grpc
from concurrent import futures
import externalscaler_pb2
import externalscaler_pb2_grpc
from custom_scaler import CustomScaler
from grpc_reflection.v1alpha import reflection

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    externalscaler_pb2_grpc.add_ExternalScalerServicer_to_server(CustomScaler(), server)

    # Enable gRPC Reflection
    service_names = (
        externalscaler_pb2.DESCRIPTOR.services_by_name['ExternalScaler'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    # Fetch port from environment variable or use default
    port = os.getenv('GRPC_PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    print(f'Server listening on port {port}')

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
