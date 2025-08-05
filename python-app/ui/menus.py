"""
Funciones para la interfaz de usuario
Maneja la visualización de menús y limpieza de pantalla
"""

import os
import platform

def limpiar_pantalla():
    """
    Limpia la pantalla de manera multiplataforma
    Detecta automáticamente el sistema operativo
    """
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Unix/Linux/MacOS
    else:
        os.system('clear')
    # Secuencia de escape ANSI para limpiar pantalla
    print("\033c", end="")

def mostrar_menu():
    """
    Muestra el menú principal con las opciones disponibles
    """
    print("\n" + "=" * 40)
    print("📋 MENÚ CRUD EMPLEADOS - MONGODB")
    print("=" * 40)
    print("1. 👀 Ver todos los empleados")
    print("2. ➕ Crear nuevo empleado")
    print("3. ✏️ Actualizar empleado")
    print("4. ❌ Eliminar empleado")
    print("5. 🔍 Buscar empleado por ID")
    print("6. 🏢 Listar por departamento")
    print("7. 🧪 Insertar datos de prueba")
    print("8. 🧹 Limpiar base de datos")
    print("9. 📊 Mostrar estadísticas")
    print("0. 🚪 Salir")
    print("=" * 40)

def mostrar_banner():
    """
    Muestra el banner de bienvenida de la aplicación
    Incluye información sobre el sistema operativo
    """
    sistema = platform.system()
    version = platform.release()
    
    print("\n" + "=" * 60)
    print(f"🌟 CRUD EMPLEADOS - MONGODB")
    print(f"   Sistema: {sistema} {version} | Python {platform.python_version()}")
    print("=" * 60)

def mostrar_subtitulo(texto: str):
    """
    Muestra un subtítulo formateado
    
    Args:
        texto: Texto a mostrar como subtítulo
    """
    print("\n" + "-" * 60)
    print(f" {texto}")
    print("-" * 60)