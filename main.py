from session import leer_sesion, guardar_sesion, mostrar_info_sistema
from db.mongo_utils import datos_ya_existen, insertar_datos_prueba, limpiar_coleccion
from ui.menus import mostrar_menu, limpiar_pantalla, mostrar_banner

from services import (
    leer_empleados,
    crear_empleado,
    actualizar_empleado,
    eliminar_empleado,
    buscar_empleado,
    listar_por_departamento
)

def menu():
    """
    Función principal del menú interactivo
    """
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip()

        match opcion:
            case "1":
                limpiar_pantalla()
                leer_empleados()
                input("\nPresiona ENTER para continuar...")
                
            case "2":
                limpiar_pantalla()
                crear_empleado()
                input("\nPresiona ENTER para continuar...")
                
            case "3":
                limpiar_pantalla()
                actualizar_empleado()
                input("\nPresiona ENTER para continuar...")
                
            case "4":
                limpiar_pantalla()
                eliminar_empleado()
                input("\nPresiona ENTER para continuar...")
                
            case "5":
                limpiar_pantalla()
                buscar_empleado()
                input("\nPresiona ENTER para continuar...")
                
            case "6":
                limpiar_pantalla()
                listar_por_departamento()
                input("\nPresiona ENTER para continuar...")
                
            case "7":
                limpiar_pantalla()
                if datos_ya_existen():
                    print("⚠️ La base de datos ya contiene empleados.")
                    print("\nOpciones disponibles:")
                    print("1. Resetear datos (eliminar todo e insertar datos de prueba)")
                    print("2. Conservar datos existentes y no hacer cambios")
                    
                    opcion = input("\nSelecciona una opción (1/2): ").strip()
                    
                    if opcion == "1":
                        print("\n⚠️ Esto eliminará todos los empleados existentes")
                        confirmar = input("¿Estás seguro? (S/N): ").strip().upper()
                        if confirmar == "S":
                            limpiar_coleccion()
                            insertar_datos_prueba()
                        else:
                            print("Operación cancelada.")
                    else:
                        print("No se realizaron cambios.")
                else:
                    confirmar = input("¿Deseas insertar los datos de prueba? (S/N): ").strip().upper()
                    if confirmar == "S":
                        insertar_datos_prueba()
                input("\nPresiona ENTER para continuar...")
                
            case "8":
                limpiar_pantalla()
                confirmar = input("⚠️ ¿Estás seguro que deseas ELIMINAR TODOS los empleados? (S/N): ").strip().upper()
                if confirmar == "S":
                    limpiar_coleccion()
                    insertar = input("¿Deseas insertar datos de prueba? (S/N): ").strip().upper()
                    if insertar == "S":
                        insertar_datos_prueba()
                input("\nPresiona ENTER para continuar...")
                
            case "0":
                print("\n👋 Guardando sesión y cerrando aplicación...")
                guardar_sesion()
                break
                
            case _:
                print("❌ Opción inválida. Intenta de nuevo.")
                input("\nPresiona ENTER para continuar...")
        
        limpiar_pantalla()

if __name__ == "__main__":
    # Limpiar consola al iniciar
    limpiar_pantalla()
    
    # Mostrar banner
    mostrar_banner()
    
    # Mostrar información del sistema
    mostrar_info_sistema()
    
    # Leer última sesión
    ultima = leer_sesion()

    # Verificar estado de la base de datos
    estado_db = datos_ya_existen()

    if ultima:
        print(f"\n👋 Bienvenido de nuevo.")
        print(f"📅 Tu última sesión fue el {ultima['fecha']}")
        print(f"💻 Desde {ultima['sistema']}")
        if datos_ya_existen():
            print("ℹ️ La base de datos contiene empleados.")
        else:
            print("ℹ️ La base de datos está vacía. Usa la opción 7 para insertar datos de prueba.")
    else:
        print("\n👋 Bienvenido por primera vez a la aplicación MongoDB CRUD.")
        print("ℹ️ Usa la opción 7 para insertar datos de prueba.")

    if estado_db is None:
        print("\n❌ No se pudo conectar a la base de datos")
        print("💡 Soluciones posibles:")
        print("1. Verifica que MongoDB esté corriendo")
        print("2. Ejecuta 'docker-compose up -d' si usas Docker")
        print("3. Revisa tu configuración en .env")
        print("4. Ejecuta 'python setup.py' para reconfigurar")
        input("\nPresiona ENTER para salir...")
        exit(1)
    elif estado_db:
        print("ℹ️ La base de datos contiene empleados")
    else:
        print("ℹ️ La base de datos está vacía")
        print("💡 Puedes insertar datos de prueba con la opción 7")

    # Iniciar menú principal
    menu()
    
    print("¡Hasta luego! 🍃")