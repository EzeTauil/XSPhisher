# utils/colors.py

class Colors:
    # Colores base
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    WHITE = '\033[97m'

    # Estilos
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    # Alias
    INFO = BLUE
    SUCCESS = GREEN
    ERROR = RED
    WARNING = YELLOW
    HIGHLIGHT = PURPLE

    @staticmethod
    def colorize(text, color, bold=False):
        """Aplica color a un texto"""
        style = Colors.BOLD if bold else ''
        return f"{style}{color}{text}{Colors.RESET}"

    @staticmethod
    def print_banner(text):
        """Imprime en rojo y negrita (para el banner)"""
        print(f"{Colors.RED}{Colors.BOLD}{text}{Colors.RESET}")

    @staticmethod
    def print_success(text):
        """Imprime en verde (éxito)"""
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

    @staticmethod
    def print_error(text):
        """Imprime en rojo (error)"""
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")

    @staticmethod
    def print_info(text):
        """Imprime en azul (información)"""
        print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

    @staticmethod
    def print_warning(text):
        """Imprime en amarillo (advertencia)"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")
