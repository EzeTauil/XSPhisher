# modules/tunnels/ngrok.py

import subprocess
import time
import requests
import os
from utils.colors import Colors
from utils.helpers import show_loading

class NgrokTunnel:
    def __init__(self):
        self.url = None
        self.process = None
        self.token = None
        self._load_token()

    def _load_token(self):
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            self.token = os.getenv('NGROK_TOKEN')
            if self.token:
                Colors.print_info("Token de Ngrok cargado desde .env")
        except:
            pass

        if not self.token:
            try:
                env_file = '.env'
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        for line in f:
                            if line.startswith('NGROK_TOKEN='):
                                self.token = line.split('=')[1].strip()
                                Colors.print_info("Token de Ngrok cargado desde .env")
                                break
            except:
                pass


    def connect(self, port):

        Colors.print_info("Iniciando Ngrok...")

        if not self._check_installed():
            Colors.print_warning("Ngrok no está instalado")
            Colors.print_info("Descarga Ngrok desde: https://ngrok.com/download")
            return False

        if not self.token:
            Colors.print_warning("No se encontró token de Ngrok")
            token = input(Colors.colorize("└─> Ingresa tu token de Ngrok: ", Colors.BLUE))
            if token:
                self.token = token
                self._save_token(token)
                subprocess.run(['ngrok', 'config', 'add-authtoken', token],
                            capture_output=True)
            else:
                Colors.print_error("Token requerido para Ngrok")
                return False

        try:
            cmd = ['ngrok', 'http', str(port), '--log=stdout']

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self._get_url()

            if self.url:
                Colors.print_success(f"Ngrok conectado: {self.url}")
                return True
            else:
                Colors.print_error("No se pudo obtener URL de Ngrok")
                return False

        except Exception as e:
            Colors.print_error(f"Error en Ngrok: {e}")
            return False

    def _save_token(self, token):
        env_file = '.env'

        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                content = f.read()
        else:
            content = ''

        if 'NGROK_TOKEN=' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('NGROK_TOKEN='):
                    lines[i] = f'NGROK_TOKEN={token}'
            content = '\n'.join(lines)
        else:
            if content and not content.endswith('\n'):
                content += '\n'
            content += f'NGROK_TOKEN={token}\n'

        with open(env_file, 'w') as f:
            f.write(content)

        Colors.print_success("Token guardado en .env")

    def _get_url(self):

        show_loading("Conectando con Ngrok", 4)

        time.sleep(3)

        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('tunnels'):
                    self.url = data['tunnels'][0]['public_url']
                    return
        except:
            pass

        time.sleep(2)
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('tunnels'):
                    self.url = data['tunnels'][0]['public_url']
                    return
        except:
            pass

    def _check_installed(self):
        try:
            subprocess.run(['ngrok', '--version'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def get_url(self):
        return self.url

    def disconnect(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
