#!/bin/bash

# XSPhisher - Script de instalación
# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}     XSPhisher - Script de Instalación                     ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# 1. Instalar dependencias de Python
echo -e "${YELLOW}[1/4] Instalando dependencias de Python...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencias de Python instaladas${NC}"
    else
        echo -e "${RED}✗ Error al instalar dependencias${NC}"
    fi
else
    echo -e "${RED}✗ No se encontró requirements.txt${NC}"
fi
echo ""

# 2. Instalar PHP
echo -e "${YELLOW}[2/4] Instalando PHP...${NC}"
if command -v php &> /dev/null; then
    echo -e "${GREEN}✓ PHP ya está instalado${NC}"
else
    if command -v pacman &> /dev/null; then
        sudo pacman -S php --noconfirm
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install php -y
    elif command -v dnf &> /dev/null; then
        sudo dnf install php -y
    else
        echo -e "${RED}✗ No se pudo instalar PHP. Instalalo manualmente.${NC}"
    fi
fi
echo ""

# 3. Instalar Ngrok
echo -e "${YELLOW}[3/4] Instalando Ngrok...${NC}"
if command -v ngrok &> /dev/null; then
    echo -e "${GREEN}✓ Ngrok ya está instalado${NC}"
else
    if [[ "$(uname -s)" == "Linux" ]]; then
        wget -q https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -O ngrok.zip
        unzip -q ngrok.zip
        sudo mv ngrok /usr/local/bin/
        rm ngrok.zip
        echo -e "${GREEN}✓ Ngrok instalado${NC}"
    else
        echo -e "${YELLOW}⚠ Instala Ngrok manualmente desde https://ngrok.com/download${NC}"
    fi
fi
echo ""

# 4. Crear archivo .env
echo -e "${YELLOW}[4/4] Configurando .env...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# XSPhisher - Tokens de servicios
NGROK_TOKEN=tu_token_aqui
LOCALXPOSE_TOKEN=tu_token_aqui
EOF
    echo -e "${GREEN}✓ Archivo .env creado${NC}"
    echo -e "${YELLOW}⚠ Editá .env y agregá tus tokens${NC}"
else
    echo -e "${GREEN}✓ .env ya existe${NC}"
fi
echo ""

# Verificar instalación
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}¡Instalación completada!${NC}"
echo ""
echo -e "${GREEN}Para ejecutar la herramienta:${NC}"
echo -e "  ${BLUE}python3 xsphisher.py${NC}"
echo ""
echo -e "${YELLOW}⚠ Recordá configurar tus tokens en .env${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
