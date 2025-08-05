#!/bin/bash

# Limpiar pantalla
clear

# Mostrar banner
echo "==========================================================="
echo "🚀 INICIANDO APLICACIÓN MONGODB CRUD"
echo "==========================================================="

# Verificar Docker
if docker ps | grep -q "empresa_mongodb"; then
    echo "✅ MongoDB en Docker está corriendo"
else
    echo "⚠️ MongoDB en Docker NO está corriendo"
    read -p "¿Deseas iniciarlo ahora? (s/n): " iniciar_docker
    if [[ "$iniciar_docker" == "s" ]]; then
        docker-compose up -d
        echo "Esperando 5 segundos para que MongoDB inicie..."
        sleep 5
    fi
fi

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "⚠️ No se encontró entorno virtual"
    read -p "¿Deseas crearlo y instalar dependencias? (s/n): " crear_venv
    if [[ "$crear_venv" == "s" ]]; then
        python -m venv venv
        source venv/Scripts/activate
        pip install -r requirements.txt
    fi
else
    source venv/Scripts/activate
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️ No se encontró archivo .env"
    read -p "¿Deseas ejecutar el script de configuración? (s/n): " ejecutar_setup
    if [[ "$ejecutar_setup" == "s" ]]; then
        python setup.py
    fi
fi

# Iniciar aplicación
echo "▶️ Iniciando la aplicación..."
python main.py