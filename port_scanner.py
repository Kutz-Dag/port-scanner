import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    def valid_ip_checker(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def resolve_hostname(hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    ip_address = None
    
    if valid_ip_checker(target):
        ip_address = target
    else:
        ip_address = resolve_hostname(target)
        if ip_address is None:
            return "Error: Invalid hostname"

    if not valid_ip_checker(ip_address):
        return "Error: Invalid IP address"

    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                open_ports.append(port)

    if not verbose:
        return open_ports

    hostname_display = target if not valid_ip_checker(target) else ip_address
    output = f"Open ports for {hostname_display} ({ip_address})\nPORT     SERVICE\n"
    for port in open_ports:
        service = ports_and_services.get(port, "unknown")
        output += f"{port:<9}{service}\n"

    return output.strip()