import socket
import sys

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 3000

def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, single_shot: bool = False):
    """Run socket server supporting multiple or single-shot client requests."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server running on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            print(f"New connection from {addr}")

            data = conn.recv(1024)
            if data:
                print(f"Received from client: {data.decode('utf-8', errors='replace')}")

            conn.sendall(b"Hello from server!")
            conn.close()

            if single_shot:
                break
    except Exception as e:
        print(f"Server error on {host}:{port}: {e}")
    finally:
        server_socket.close()

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(DEFAULT_HOST, port)

if __name__ == '__main__':
    main()

