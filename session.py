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
    Guarda información de sesión en UTF-8
    """
    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sistema": sistema_legible(),
        "aplicacion": "Python MongoDB CRUD"
    }
    try:
        # Especificar codificación UTF-8 explícitamente
        with open(SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Sesión guardada correctamente (UTF-8)")
    except Exception as e:
        logger.error(f"No se pudo guardar la sesión: {e}")

def leer_sesion():
    """
    Lee la última sesión con UTF-8
    """
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        # Intentar leer con UTF-8
        with open(SESSION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        try:
            # Si falla, intentar con Latin-1
            logger.warning("⚠️ Problema con UTF-8, intentando Latin-1")
            with open(SESSION_FILE, 'r', encoding='latin-1') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"No se pudo leer la sesión: {e}")
            return None
    except Exception as e:
        logger.error(f"No se pudo leer la sesión: {e}")
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