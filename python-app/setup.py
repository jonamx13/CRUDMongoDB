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
    
def configurar_mongodb():
    """Configura la conexión a MongoDB de forma interactiva"""
    print("\n🔧 Configuración de MongoDB")
    print("=" * 50)
    
    opciones = [
        "Usar Docker (recomendado)",
        "Usar MongoDB local",
    ]
    
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    
    eleccion = input("\nSelecciona una opción (1-2): ").strip()
    
    config = {
        "MONGO_HOST": "localhost",
        "MONGO_PORT": "27017",
        "MONGO_DB": "empresa_db",
        "MONGO_COLLECTION": "rh"
    }
    
    if eleccion == "1":
        # Docker usa un puerto diferente por defecto
        config["MONGO_PORT"] = "27018"
        print("\n✅ Configurado para usar MongoDB en Docker (puerto 27018)")
        print("💡 Asegúrate de tener Docker Desktop instalado y ejecutar:")
        print("   docker-compose up -d")
    elif eleccion == "2":
        print("\n✅ Configurado para usar MongoDB local (puerto 27017)")
        print("⚠️ Verifica que no tengas otro MongoDB ejecutándose en este puerto")
    else:
        print("Opción inválida, usando configuración por defecto")
    
    return config

def crear_archivo_env(config):
    """Crea el archivo .env con codificación UTF-8"""
    if not os.path.exists('.env'):
        print("\n⚙️ Creando archivo .env...")
    contenido = f"""# Configuración MongoDB
MONGO_URI=mongodb://{config['MONGO_HOST']}:{config['MONGO_PORT']}
MONGO_DB={config['MONGO_DB']}
MONGO_COLLECTION={config['MONGO_COLLECTION']}
"""
    try:
        # Guardar explícitamente como UTF-8
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Archivo .env creado (UTF-8)")
    except Exception as e:
        print(f"❌ Error al crear .env: {e}")
    else:
        print("\nℹ️ Archivo .env ya existe")
        # Verificar si podemos leer como UTF-8
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            print("⚠️ El .env tiene problemas de codificación, creando nuevo...")
            os.rename('.env', '.env.backup')
            crear_archivo_env()

        return config

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
    
    # Paso 1: Configurar MongoDB
    config = configurar_mongodb()
    
    # Paso 2: Crear entorno virtual si no existe
    if not os.path.exists('venv'):
        crear_entorno_virtual()

    else:
        print("\nℹ️ Entorno virtual ya existe, omitiendo creación")
    
    # Paso 3: Instalar dependencias
    instalar_dependencias()
    
    # Paso 4: Crear archivo .env
    crear_archivo_env(config)
    
    # Paso 5: Verificar conexión a MongoDB
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