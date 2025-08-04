import os

def limpiar_pantalla():
    """
    Limpia la pantalla de la consola multiplataforma
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033c", end="")

def mostrar_menu():
    """
    Muestra el menú principal de la aplicación
    """
    print("\n--- MENÚ CRUD EMPLEADOS MONGODB ---")
    print("1. Ver empleados")
    print("2. Crear empleado")
    print("3. Actualizar empleado")
    print("4. Eliminar empleado")
    print("5. Buscar empleado por ID")
    print("6. Listar empleados por departamento")
    print("7. Insertar datos de prueba")
    print("8. Limpiar base de datos")
    print("0. Salir")

def mostrar_banner():
    """
    Muestra el banner de bienvenida
    """
    print("=" * 60)
    print("🍃 CRUD EMPLEADOS - MONGODB")
    print("   Aplicación Python con detección de SO")
    print("=" * 60)