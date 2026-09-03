import socket
import sys

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 3000

def send_message(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, message: str = "Hello from client") -> bytes:
    """Connect to socket server and exchange messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Server Response: {response.decode('utf-8', errors='replace')}")
        return response
    except Exception as e:
        print(f"Client connection error ({host}:{port}): {e}")
        return b""
    finally:
        client_socket.close()

def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello from client"
    send_message(DEFAULT_HOST, DEFAULT_PORT, msg)

if __name__ == '__main__':
    main()

