# modules/tunnels/cloudflared.py

import subprocess
import time
import re
import os
from utils.colors import Colors
from utils.helpers import show_loading

class CloudflaredTunnel:
    def __init__(self):
        self.url = None
        self.process = None
        self.log_file = "cloudflared.log"

    def connect(self, port):
        Colors.print_info("Iniciando Cloudflared...")

        if not self._check_installed():
            Colors.print_warning("Cloudflared no está instalado")
            Colors.print_info("Instalando Cloudflared...")
            if not self._install():
                Colors.print_error("No se pudo instalar Cloudflared")
                return False
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

        try:

            cmd = [
                'cloudflared', 'tunnel',
                '--url', f'http://localhost:{port}',
                '--logfile', self.log_file
            ]

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )


            self._find_url()

            if self.url:
                Colors.print_success(f"Cloudflared conectado: {self.url}")
                return True
            else:
                Colors.print_error("No se pudo obtener URL de Cloudflared")
                return False

        except Exception as e:
            Colors.print_error(f"Error en Cloudflared: {e}")
            return False

    def _find_url(self):

        show_loading("Conectando con Cloudflared", 5)

        time.sleep(5)

        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    content = f.read()
                    match = re.search(r'https://[-0-9a-z]*\.trycloudflare\.com', content)
                    if match:
                        self.url = match.group(0)
                        return
        except:
            pass

        time.sleep(5)
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    content = f.read()
                    match = re.search(r'https://[-0-9a-z]*\.trycloudflare\.com', content)
                    if match:
                        self.url = match.group(0)
                        return
        except:
            pass

    def _check_installed(self):
        try:
            subprocess.run(['cloudflared', '--version'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def _install(self):

        try:
            import platform
            arch = platform.machine()
            if 'x86_64' in arch:
                url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
            elif 'aarch64' in arch:
                url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
            else:
                url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386'

            subprocess.run(['wget', '-q', url, '-O', 'cloudflared'], check=True)
            subprocess.run(['chmod', '+x', 'cloudflared'], check=True)
            subprocess.run(['sudo', 'mv', 'cloudflared', '/usr/local/bin/'], check=True)
            return True
        except:
            return False

    def get_url(self):
        return self.url

    def disconnect(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
