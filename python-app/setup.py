#!/usr/bin/env python3
"""
Script de configuración automática para el proyecto Python MongoDB CRUD
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, shell=False):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(command, shell=shell, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def create_venv():
    """Crea el entorno virtual"""
    print("🐍 Creando entorno virtual...")
    success, output = run_command([sys.executable, "-m", "venv", "venv"])
    if success:
        print("✅ Entorno virtual creado")
        return True
    else:
        print(f"❌ Error creando entorno virtual: {output}")
        return False

def get_pip_command():
    """Obtiene el comando pip según el SO"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip"
    else:
        return "venv/bin/pip"

def install_requirements():
    """Instala las dependencias"""
    print("📦 Instalando dependencias...")
    pip_cmd = get_pip_command()
    success, output = run_command([pip_cmd, "install", "-r", "requirements.txt"])
    if success:
        print("✅ Dependencias instaladas")
        return True
    else:
        print(f"❌ Error instalando dependencias: {output}")
        return False

def create_env_file():
    """Crea el archivo .env si no existe"""
    if not os.path.exists('.env'):
        print("⚙️ Creando archivo .env...")
        env_content = """# Configuración MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=empresa_db
MONGO_COLLECTION=rh
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
    else:
        print("ℹ️ Archivo .env ya existe")

def check_mongodb():
    """Verifica si MongoDB está corriendo"""
    print("🍃 Verificando conexión a MongoDB...")
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017", 
                                   serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB está disponible")
        return True
    except Exception as e:
        print(f"⚠️ MongoDB no disponible: {e}")
        print("💡 Asegúrate de que MongoDB esté corriendo o usa Docker:")
        print("   docker-compose up -d")
        return False

def main():
    """Función principal de configuración"""
    print("🚀 Configurando proyecto Python MongoDB CRUD")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('requirements.txt'):
        print("❌ No se encuentra requirements.txt")
        print("Ejecuta este script desde el directorio python-app/")
        return False
    
    # Crear entorno virtual
    if not os.path.exists('venv'):
        if not create_venv():
            return False
    else:
        print("ℹ️ Entorno virtual ya existe")
    
    # Instalar dependencias
    if not install_requirements():
        return False
    
    # Crear archivo .env
    create_env_file()
    
    # Verificar MongoDB
    check_mongodb()
    
    print("\n🎉 Configuración completada!")
    print("\nPasos siguientes:")
    
    if platform.system() == "Windows":
        print("1. Activar entorno: venv\\Scripts\\activate")
    else:
        print("1. Activar entorno: source venv/bin/activate")
    
    print("2. Ejecutar aplicación: python main.py")
    print("3. Si MongoDB no está disponible: docker-compose up -d")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)