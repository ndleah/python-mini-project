# mHTTP - A simple HTTP server
# Written by M.V.Harish Kumar on 24/10/2023

import sys, socket
from pathlib import Path

HOST = "0.0.0.0"
PORT = 1997
FOLDER = '.' if len(sys.argv) < 2 else sys.argv[1]

def get_content(path):
    ext = "html"
    if path == "/":
        try:
            with open(FOLDER + "/index.html", "r") as f:
                content = f.read()
        except FileNotFoundError:
            content = "The Server is working! but there is no index.html file to render"
    else:
        try:
            with open(FOLDER + path, "r") as f:
                if Path(FOLDER + path).suffix != ".html":
                    ext = "plain"
                content = f.read()
        except FileNotFoundError:
            return 404, "File not found", ext
    return 200, content, ext

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
        s.listen()

        print("mHTTP: The Micro-HTTP Server")
        print(f"Server Started running at {HOST}:{PORT}\n")
        print("mhttp: waiting for connections...")

        while True:
            clnt, caddr = s.accept()
            with clnt:
                print(f"mhttp: got connection from {caddr[0]}:{caddr[1]}")
                req = clnt.recv(1024).decode()
                if not req:
                    print("mhttp: connection closed unexpectedly", file=sys.stderr)
                    break

                req = req.split("\r\n")
                print(f"mhttp: got request: {req[0]}")
                path = req[0].split(" ")[1]

                sts_cd, content, ftype = get_content(path)

                resp = f"HTTP/1.1 {sts_cd}\r\n" \
                       f"Content-Type: text/{ftype}\r\n" \
                       "\r\n" + content

                clnt.sendall(resp.encode())
                print(f"mhttp: sent response({sts_cd}) to {caddr[0]}:{caddr[1]}")
    except KeyboardInterrupt:
        print("mhttp: Got Keyboard Interrupt", file=sys.stderr)
        print("mhttp: Closing Connection.", file=sys.stderr)
            

