"""
Servicios para eliminar empleados
"""
import logging
from db.mongo_config import get_collection
from services.read.service import leer_empleados
from ui.menus import limpiar_pantalla
from .flow_control import (
    confirmar_eliminacion, 
    obtener_id_empleado, 
    obtener_opcion_reintento,
    preguntar_continuar
)

logger = logging.getLogger(__name__)

def eliminar_empleado():
    """
    Elimina un empleado de la base de datos con validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        while True:  # Bucle principal para permitir eliminar múltiples empleados
            # Limpiar pantalla y mostrar lista actual de empleados
            limpiar_pantalla()
            leer_empleados()
            
            print("\n🗑️ Eliminar empleado")
            print("💡 Puedes escribir 'cancelar' en cualquier momento para salir\n")
            
            # Obtener ID del empleado
            empno = obtener_id_empleado()
            if empno is None:  # Usuario canceló
                print("❌ Operación cancelada por el usuario.")
                return
                
            # Buscar empleado
            empleado = collection.find_one({"empno": empno})
            if not empleado:
                print(f"❌ No se encontró un empleado con ID: {empno}")
                opcion = obtener_opcion_reintento("empleado no encontrado")
                if opcion == 'cancelar':
                    print("❌ Operación cancelada por el usuario.")
                    return
                elif opcion == 'reintentar':
                    continue  # Volver al inicio del bucle principal
                    
            else:
                # Empleado encontrado, proceder con confirmación
                resultado_confirmacion = confirmar_eliminacion(empleado, collection)
                
                if resultado_confirmacion == 'eliminado':
                    # Empleado eliminado exitosamente, preguntar si quiere eliminar otro
                    limpiar_pantalla()
                    leer_empleados()  # Mostrar lista actualizada
                    print(f"✅ Empleado {empleado['ename']} (ID: {empno}) eliminado exitosamente.\n")
                    
                    if preguntar_continuar():
                        continue  # Volver al inicio para eliminar otro empleado
                    else:
                        return  # Salir de la función
                        
                elif resultado_confirmacion == 'cancelado_continuar':
                    # Usuario canceló pero quiere eliminar otro empleado
                    continue  # Volver al inicio del bucle principal
                    
                elif resultado_confirmacion == 'cancelado_salir':
                    # Usuario canceló y quiere salir
                    print("❌ Operación cancelada por el usuario.")
                    return
                    
    except Exception as e:
        logger.error(f"Error inesperado al eliminar empleado: {e}")
        print(f"❌ Error inesperado al eliminar empleado: {str(e)}")