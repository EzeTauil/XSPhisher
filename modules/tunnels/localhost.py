# modules/tunnels/localhost.py

from utils.colors import Colors
from utils.helpers import get_ip

class LocalhostTunnel:
    def __init__(self):
        self.url = None
        self.port = None

    def connect(self, port):
        self.port = port
        self.url = f"http://localhost:{port}"
        Colors.print_success(f"Localhost conectado: {self.url}")
        return True

    def get_url(self):
        return self.url

    def disconnect(self):
        pass
