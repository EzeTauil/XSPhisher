<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     _  ____                           ____  __    _      __               ║
║    | |/ / /_________  ____ ___  ___  / __ \/ /_  (_)____/ /_  ___  _____  ║
║    |   / __/ ___/ _ \/ __ `__ \/ _ \/ /_/ / __ \/ / ___/ __ \/ _ \/ ___/  ║
║   /   / /_/ /  /  __/ / / / / /  __/ ____/ / / / (__  ) / / /  __/ /      ║
║  /_/|_\__/_/   \___/_/ /_/ /_/\___/_/   /_/ /_/_/____/_/ /_/\___/_/       ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                           PHISHING   TOOL                                 ║
║                            Version 2.0.0                                  ║
║                                                          By:Dexlor        ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

# XSPhisher — Educational Phishing Framework
### Advanced phishing simulation tool with 47+ templates

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-orange?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Version](https://img.shields.io/badge/Version-2.0.0-red?style=flat-square)

</div>

---

## What is this?

**XSPhisher** is a command-line phishing simulation tool that automates the creation of realistic phishing pages for educational and security awareness purposes. Built as an enhanced version of Zphisher, it features **47+ updated templates**, **real-time credential capture**, **device fingerprinting**, and **multiple tunneling options**.

Built for **security researchers, penetration testers, and CTF players** who need a reliable, up-to-date phishing simulation tool for authorized security training.

---

## Features

- 🎯 **47+ Phishing Templates** — Facebook, Instagram, Google, WhatsApp, Telegram, TikTok, Discord, and more
- 🔐 **Real-time Credential Capture** — Username, password, IP, device, OS, browser, and timestamp
- 🌐 **Multiple Tunneling Options** — Cloudflare, Ngrok, Localhost (more coming)
- 🖥 **Device Fingerprinting** — Detects OS, browser, device type (PC/Mobile/Tablet)
- 📍 **Geolocation** — Country and city from IP address
- 🎨 **Beautiful CLI Interface** — Colored output with ASCII banners and structured tables
- 📁 **Export Capabilities** — Save captures to JSON or CSV
- 🔄 **Modular Architecture** — Easy to add new templates and tunnels
- 🐍 **Pure Python** — No PHP dependency except for serving templates

---

## Installation

```bash
# Clone the repository
git clone https://github.com/EzeTauil/XSPhisher.git
cd XSPhisher

# Install all

# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar
./install.sh

# Install PHP (required for serving templates)
# On Arch Linux:
sudo pacman -S php
# On Debian/Ubuntu:
sudo apt install php

# Run
python xsphisher.py
```

> Requirements: Python 3.10+, PHP 7.4+, Linux or Termux

---

## Quick Start

```bash
# Launch the tool
python xsphisher.py

# Select a template (e.g., Facebook)
# Choose tunneling method (Localhost, Cloudflare, Ngrok)
# Share the generated URL
# Watch credentials appear in real-time!
```

---

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🔐  CREDENCIALES CAPTURADAS                                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Sitio      ▸  facebook                                      ║
║  IP         ▸  186.123.217.76                                ║
╠══════════════════════════════════════════════════════════════╣
║  Usuario    ▸  johndoe@outlook.com                           ║
║  Contraseña ▸  securepassword123                             ║
╠══════════════════════════════════════════════════════════════╣
║  Hora       ▸  23:45:12                                      ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Usage

### Main Menu Options

| Option | Description |
|--------|-------------|
| `[1]`  | Select phishing template |
| `[2]`  | Select tunneling method |
| `[3]`  | Start server |
| `[4]`  | View captured credentials |
| `[5]`  | Update templates |
| `[6]`  | Manage templates |
| `[7]`  | Export captures |
| `[0]`  | Exit |

### Available Tunnels

| Tunnel | Description |
|--------|-------------|
| Cloudflare | Generates `.trycloudflare.com` URL (requires internet) |
| Ngrok | Generates `.ngrok.io` URL (requires token) |
| Localhost | Local network only (no internet required) |

### Available Templates (47+)

| # | Template | # | Template | # | Template |
|---|----------|---|----------|---|----------|
| 1 | Adobe | 17 | Protonmail | 33 | Snapchat |
| 2 | Badoo | 18 | Spotify | 34 | Stackoverflow |
| 3 | DeviantArt | 19 | Reddit | 35 | Steam |
| 4 | Discord | 20 | Tiktok | 36 | Telegram |
| 5 | Dropbox | 21 | Twitch | 37 | Twitter |
| 6 | Ebay | 22 | Vk | 38 | Vk Poll |
| 7 | Facebook | 23 | Vk Poll | 39 | Whatsapp |
| 8 | Fb Advanced | 24 | Whatsapp | 40 | Wordpress |
| 9 | Fb Messenger | 25 | Wordpress | 41 | Xbox |
| 10 | Fb Security | 26 | Xbox | 42 | Yahoo |
| 11 | Github | 27 | Yahoo | 43 | Yandex |
| 12 | Gitlab | 28 | Yandex | 44 | ... |
| 13 | Google | 29 | Instagram | 45 | ... |
| 14 | Google New | 30 | Ig Followers | 46 | ... |
| 15 | Google Poll | 31 | Ig Verify | 47 | ... |
| 16 | Linkedin | 32 | Mediafire | | |

---

## Architecture

```
XSPhisher/
├── core/
│   ├── engine.py         # Main orchestrator
│   └── server.py         # PHP server + file watcher
├── modules/
│   ├── tunnels/
│   │   ├── cloudflared.py
│   │   ├── ngrok.py
│   │   └── localhost.py
│   └── templates/
│       └── manager.py
├── templates/             # 47+ phishing templates
├── utils/
│   ├── colors.py          # ANSI color system
│   ├── banner.py          # ASCII banners
│   └── helpers.py         # Helper functions
├── xsphisher.py           # Entry point
└── requirements.txt       # Python dependencies
```

---

## Security & Disclaimer

> ⚠️ This tool is for **EDUCATIONAL PURPOSES ONLY**.

- ✅ Use only on systems you own or have explicit permission to test
- ✅ Use for security awareness training and CTF competitions
- ❌ **NEVER** use against unauthorized targets
- ❌ **NEVER** use for illegal activities

The author is not responsible for any misuse of this toolkit. By using this software, you agree to use it responsibly and within the bounds of the law.

---

## Roadmap

- [ ] Serveo tunnel support
- [ ] LocalXpose tunnel support
- [ ] Telegram/Discord notifications for captures
- [ ] Web dashboard with live feed
- [ ] Auto-update templates from internet
- [ ] QR code generation for mobile access
- [ ] Session persistence
- [ ] Multi-language support

---

## Why XSPhisher?

| Feature | Zphisher | XSPhisher |
|---------|----------|-----------|
| Templates | 30+ | 47+ |
| Device fingerprint | ❌ | ✅ |
| Geolocation | ❌ | ✅ |
| Live credential display | Basic | Enhanced with colors |
| Export formats | TXT only | JSON, CSV |
| Modular codebase | Bash + PHP | Python (modular) |
| Active development | Abandoned | Active |

---

## Credits

This tool is based on [Zphisher](https://github.com/htr-tech/zphisher) by [htr-tech](https://github.com/htr-tech).

**Improvements over Zphisher:**
- Python-based (instead of Bash)
- Modular architecture
- Better UI with colors
- Geolocation and device fingerprinting
- 47+ updated templates

---

## Author

**EzeTauil** / [GitHub](https://github.com/EzeTauil)

> *"Security awareness through education, not exploitation."*

---

## License

MIT License — feel free to use, modify, and distribute for educational purposes.
