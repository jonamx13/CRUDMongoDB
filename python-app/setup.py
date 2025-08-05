#!/usr/bin/env python3
"""
Script de configuración automática para el proyecto
Crea entorno virtual, instala dependencias y verifica MongoDB
"""

import os
import sys
import subprocess
import platform
import time
import logging

logger = logging.getLogger(__name__)

def run_command(command, shell=False):
    """
    Ejecuta un comando en la terminal
    
    Args:
        command: Comando a ejecutar (lista o string)
        shell: Ejecutar a través de shell del sistema
    
    Returns:
        tuple: (success, output) Éxito y salida del comando
    """
    try:
        result = subprocess.run(command, shell=shell, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def crear_entorno_virtual():
    """Crea un entorno virtual para el proyecto"""
    print("\n🐍 Creando entorno virtual...")
    success, output = run_command([sys.executable, "-m", "venv", "venv"])
    if success:
        print("✅ Entorno virtual creado exitosamente")
        return True
    else:
        print(f"❌ Error creando entorno virtual: {output}")
        return False

def instalar_dependencias():
    """Instala las dependencias desde requirements.txt"""
    print("\n📦 Instalando dependencias...")
    
    # Determinar comando pip según SO
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    success, output = run_command([pip_cmd, "install", "-r", "requirements.txt"])
    
    if success:
        print("✅ Dependencias instaladas correctamente")
        return True
    else:
        print(f"❌ Error instalando dependencias: {output}")
        return False

def crear_archivo_env():
    """Crea el archivo .env con configuraciones predeterminadas"""
    if not os.path.exists('.env'):
        print("\n⚙️ Creando archivo .env...")
        contenido = """# Configuración MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=empresa_db
MONGO_COLLECTION=rh
"""
        with open('.env', 'w') as f:
            f.write(contenido)
        print("✅ Archivo .env creado")
    else:
        print("\nℹ️ Archivo .env ya existe, no se modificará")

def verificar_mongodb():
    """Verifica si MongoDB está disponible"""
    print("\n🍃 Verificando conexión a MongoDB...")
    try:
        # Importar solo cuando sea necesario
        from pymongo import MongoClient
        
        intentos = 0
        max_intentos = 3
        while intentos < max_intentos:
            try:
                client = MongoClient(
                    "mongodb://localhost:27017", 
                    serverSelectionTimeoutMS=2000
                )
                client.admin.command('ping')
                print("✅ MongoDB está disponible")
                return True
            except Exception:
                intentos += 1
                if intentos < max_intentos:
                    print(f"⚠️ Intento {intentos}/{max_intentos} - Reintentando en 2 segundos...")
                    time.sleep(2)
        
        print(f"❌ No se pudo conectar a MongoDB después de {max_intentos} intentos")
        return False
        
    except ImportError:
        print("❌ PyMongo no está instalado. Instala dependencias primero.")
        return False

def mostrar_pasos_siguientes():
    """Muestra instrucciones para continuar después de la instalación"""
    print("\n🎉 ¡Configuración completada con éxito!")
    print("\nPasos siguientes:")
    
    if platform.system() == "Windows":
        print("1. Activar entorno virtual: venv\\Scripts\\activate")
        print("2. Ejecutar la aplicación: python main.py")
    else:
        print("1. Activar entorno virtual: source venv/bin/activate")
        print("2. Ejecutar la aplicación: python3 main.py")
    
    print("\n💡 Si MongoDB no está instalado localmente, puedes usar Docker:")
    print("   docker-compose up -d")

def main():
    """Función principal de configuración"""
    print("\n" + "=" * 50)
    print("🚀 CONFIGURADOR DE PROYECTO MONGODB CRUD")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('requirements.txt'):
        print("❌ Error: No se encuentra requirements.txt")
        print("   Ejecuta este script desde el directorio python-app/")
        return False
    
    # 1. Crear entorno virtual
    if not os.path.exists('venv'):
        if not crear_entorno_virtual():
            return False
    else:
        print("\nℹ️ Entorno virtual ya existe, omitiendo creación")
    
    # 2. Instalar dependencias
    if not instalar_dependencias():
        return False
    
    # 3. Crear archivo .env
    crear_archivo_env()
    
    # 4. Verificar MongoDB
    verificar_mongodb()
    
    # Mostrar pasos siguientes
    mostrar_pasos_siguientes()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Configuración cancelada por el usuario")
        sys.exit(1)