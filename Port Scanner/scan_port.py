import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_PORTS = [20, 21, 22, 23, 25, 42, 43, 53, 67, 69, 80, 110, 115, 123, 137, 138, 139, 143, 161, 179, 443, 445, 514, 515, 993, 995, 1080, 1194, 1433, 1702, 1723, 3128, 3268, 3306, 3389, 5432, 5060, 5900, 5938, 8080, 10000, 20000]

def check_single_port(host: str, port: int, timeout: float = 1.0) -> tuple:
    """Attempt to connect to a single port and return (port, is_active)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            res = s.connect_ex((host, port))
            if res == 0:
                return (port, True)
        except (socket.error, Exception):
            pass
    return (port, False)

def scan_ports(host: str, ports_list: list = None, max_threads: int = 20) -> list:
    """Scan ports concurrently using ThreadPoolExecutor."""
    if ports_list is None:
        ports_list = DEFAULT_PORTS

    host = host.strip()
    if not host:
        print("Error: Invalid host provided.")
        return []

    print(f"Starting port scan for host: '{host}' across {len(ports_list)} ports...")
    active_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_map = {executor.submit(check_single_port, host, port): port for port in ports_list}
        for future in as_completed(future_map):
            port, is_active = future.result()
            if is_active:
                print(f"-> {host}:{port} port is ACTIVE")
                active_ports.append(port)

    print(f"Scan complete! Found {len(active_ports)} active port(s).")
    return sorted(active_ports)

def main():
    if len(sys.argv) > 1:
        target_host = sys.argv[1]
    else:
        target_host = input('Enter hostname/IP address to scan (e.g. 127.0.0.1 or example.com): ').strip()

    if target_host:
        scan_ports(target_host)

if __name__ == '__main__':
    main()

