# utils/helpers.py

import os
import time
import requests
import re
from utils.colors import Colors

def clear_screen():
    """Limpia la pantalla según el sistema operativo"""
    os.system('clear' if os.name == 'posix' else 'cls')

def press_enter():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input(Colors.colorize("\nPresiona Enter para continuar...", Colors.BLUE))

def show_loading(message, duration=3, steps=20):
    """Muestra una barra de carga con efecto visual"""
    print(Colors.colorize(f"  {message}...", Colors.BLUE))

    for i in range(steps + 1):
        time.sleep(duration / steps)
        progress = int((i / steps) * 100)
        filled = int(i * 50 / steps)
        bar = '█' * filled + '░' * (50 - filled)
        print(f"\r  [{bar}] {progress}%", end='')

    print()

def check_internet():
    """Verifica conexión a internet"""
    try:
        requests.get('https://google.com', timeout=3)
        return True
    except:
        return False

# utils/helpers.py

def get_ip():
    """Obtiene la IP pública de la máquina"""
    try:
        import requests
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return "No disponible"

def mask_url(url, mask_text=None):
    """Enmascara una URL con un texto personalizado"""
    result = {
        'original': url,
        'short': url,
        'masked': url,
        'success': False
    }

    if not url:
        return result

    if not mask_text:
        mask_text = "login-secure"

    mask_text = re.sub(r'[^a-zA-Z0-9-]', '', mask_text)

    # 1. is.gd
    try:
        response = requests.get(
            f'https://is.gd/create.php?format=simple&url={url}',
            timeout=5
        )
        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url and short_url.startswith('http'):
                result['short'] = short_url
                result['masked'] = f"https://{mask_text}@{short_url.replace('https://', '')}"
                result['success'] = True
                return result
    except:
        pass

    # 2. v.gd
    try:
        response = requests.get(
            f'https://v.gd/create.php?format=simple&url={url}',
            timeout=5
        )
        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url and short_url.startswith('http'):
                result['short'] = short_url
                result['masked'] = f"https://{mask_text}@{short_url.replace('https://', '')}"
                result['success'] = True
                return result
    except:
        pass

    # 3. tinyurl
    try:
        response = requests.get(
            f'https://tinyurl.com/api-create.php?url={url}',
            timeout=5
        )
        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url and short_url.startswith('http'):
                result['short'] = short_url
                result['masked'] = f"https://{mask_text}@{short_url.replace('https://', '')}"
                result['success'] = True
                return result
    except:
        pass

    result['success'] = False
    return result
