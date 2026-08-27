import os
import sys
import socket
from pathlib import Path

HOST = "0.0.0.0"
PORT = 1997

def get_content(base_folder: str, req_path: str):
    """Retrieve content safely preventing directory traversal."""
    root = Path(base_folder).resolve()

    if req_path == "/":
        target = root / "index.html"
        if not target.exists():
            return 200, b"The Server is working! but there is no index.html file to render", "text/plain; charset=utf-8"
    else:
        # Strip leading slash to resolve relative to root
        rel_path = req_path.lstrip("/")
        target = (root / rel_path).resolve()

    # Directory Traversal Security Guard
    try:
        if not target.is_relative_to(root):
            return 403, b"403 Forbidden: Directory Traversal Denied", "text/plain; charset=utf-8"
    except AttributeError:
        # Fallback for Python versions before 3.9
        if not str(target).startswith(str(root)):
            return 403, b"403 Forbidden: Directory Traversal Denied", "text/plain; charset=utf-8"

    if not target.exists() or not target.is_file():
        return 404, b"404 File Not Found", "text/plain; charset=utf-8"

    suffix = target.suffix.lower()
    content_type = "text/html; charset=utf-8" if suffix == ".html" else \
                   "text/plain; charset=utf-8" if suffix in (".txt", ".py", ".md") else \
                   "image/png" if suffix == ".png" else \
                   "image/jpeg" if suffix in (".jpg", ".jpeg") else \
                   "application/octet-stream"

    try:
        with open(target, "rb") as f:
            data = f.read()
        return 200, data, content_type
    except Exception as e:
        return 500, f"500 Internal Server Error: {e}".encode(), "text/plain; charset=utf-8"

def run_server(folder=".", host=HOST, port=PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()

        print("mHTTP: The Micro-HTTP Server")
        print(f"Server Started running at {host}:{port}\n")
        print("mhttp: waiting for connections...")

        try:
            while True:
                clnt, caddr = s.accept()
                with clnt:
                    req_raw = clnt.recv(1024)
                    if not req_raw:
                        continue

                    req = req_raw.decode('utf-8', errors='replace').split("\r\n")
                    if not req or len(req[0].split(" ")) < 2:
                        continue

                    path = req[0].split(" ")[1]
                    sts_cd, body, ctype = get_content(folder, path)

                    header = f"HTTP/1.1 {sts_cd}\r\nContent-Type: {ctype}\r\nContent-Length: {len(body)}\r\n\r\n"
                    clnt.sendall(header.encode() + body)
                    print(f"mhttp: sent response({sts_cd}) to {caddr[0]}:{caddr[1]} for {path}")
        except KeyboardInterrupt:
            print("\nmhttp: Got Keyboard Interrupt. Closing Server.", file=sys.stderr)

def main():
    folder = '.' if len(sys.argv) < 2 else sys.argv[1]
    run_server(folder)

if __name__ == '__main__':
    main()

            

