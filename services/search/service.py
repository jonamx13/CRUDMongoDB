"""
Servicios para buscar empleados - Versión corregida
"""
import logging
from db.mongo_config import get_collection
from ui.menus import limpiar_pantalla
from .by_field import buscar_por_id, buscar_por_nombre, buscar_por_puesto, buscar_por_departamento
from .display import manejar_despues_resultado, manejar_sin_resultados

logger = logging.getLogger(__name__)

def buscar_empleado():
    """
    Busca empleados con múltiples criterios y validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        while True:  # Bucle principal para permitir múltiples búsquedas
            limpiar_pantalla()
            print("🔍 Buscar empleados")
            print("💡 Puedes escribir 'cancelar' en cualquier momento para salir\n")
            
            # Mostrar opciones de búsqueda
            print("Opciones de búsqueda:")
            print("1. Buscar por ID")
            print("2. Buscar por nombre")
            print("3. Buscar por puesto")
            print("4. Buscar por departamento")
            
            opcion = input("\nElige una opción (1-4 o 'cancelar'): ").strip()
            
            if opcion.lower() == 'cancelar':
                print("❌ Búsqueda cancelada por el usuario.")
                return
            elif opcion == '1':
                resultado = buscar_por_id(collection)
            elif opcion == '2':
                resultado = buscar_por_nombre(collection)
            elif opcion == '3':
                resultado = buscar_por_puesto(collection)
            elif opcion == '4':
                resultado = buscar_por_departamento(collection)
            else:
                print("❌ Opción no válida. Elige una opción del 1 al 4.")
                input("\nPresiona ENTER para continuar...")
                continue
                
            # Manejar resultado de la búsqueda
            if resultado == 'continuar':
                continue  # Realizar otra búsqueda
            elif resultado == 'salir':
                return
            
    except Exception as e:
        logger.error(f"Error inesperado en búsqueda: {e}")
        print(f"❌ Error inesperado en búsqueda: {str(e)}")