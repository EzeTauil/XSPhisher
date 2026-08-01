#!/usr/bin/env python3
# xsphisher.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.banner import show_banner
from utils.colors import Colors
from core.engine import PhishingEngine

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    show_banner()

    if sys.version_info < (3, 6):
        Colors.print_error("Se requiere Python 3.6 o superior")
        sys.exit(1)

    try:
        engine = PhishingEngine()
        engine.start()
    except KeyboardInterrupt:
        print()
        Colors.print_warning("Interrupción detectada. Saliendo...")
        sys.exit(0)
    except Exception as e:
        Colors.print_error(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
