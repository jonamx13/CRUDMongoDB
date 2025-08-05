"""
Manejo de la sesión de la aplicación
Guarda y recupera información entre ejecuciones
"""

import json
import platform
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

# Archivo para almacenar la última sesión
SESSION_FILE = "last_session.json"

def sistema_legible():
    """
    Devuelve el nombre del sistema operativo en formato legible
    
    Returns:
        str: Nombre del sistema operativo
    """
    sistemas = {
        "Windows": "Windows",
        "Linux": "Linux", 
        "Darwin": "macOS"
    }
    return sistemas.get(platform.system(), platform.system())

def guardar_sesion():
    """
    Guarda información de la sesión actual en un archivo JSON
    Incluye fecha/hora y sistema operativo
    """
    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sistema": sistema_legible(),
        "aplicacion": "Python MongoDB CRUD"
    }
    try:
        with open(SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Sesión guardada correctamente")
    except Exception as e:
        logger.error(f"No se pudo guardar la sesión: {e}")

def leer_sesion():
    """
    Lee la última sesión guardada
    
    Returns:
        dict: Datos de la última sesión o None si no existe
    """
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"No se pudo leer la sesión anterior: {e}")
        return None

def mostrar_info_sistema():
    """
    Muestra información detallada del sistema
    """
    print(f"\n💻 Sistema operativo: {sistema_legible()}")
    print(f"🐍 Python: {platform.python_version()}")
    print(f"🏗️ Arquitectura: {platform.machine()}")
    print(f"💾 Plataforma: {platform.platform()}")
    print(f"📅 Fecha actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")