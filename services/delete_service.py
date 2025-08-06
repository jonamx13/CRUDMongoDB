"""
Servicios para eliminar empleados
"""
import logging
from db.mongo_config import get_collection
from services.read_service import leer_empleados

logger = logging.getLogger(__name__)

def eliminar_empleado():
    """
    Elimina un empleado de la base de datos
    
    Returns:
        None: Interacción por consola
    """
    leer_empleados()
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        empno = int(input("\nID del empleado a eliminar: "))
        
        empleado = collection.find_one({"empno": empno})
        if not empleado:
            print("❌ Empleado no encontrado.")
            return

        print(f"\n⚠️ Vas a eliminar al empleado: {empleado['ename']} ({empleado['job']})")
        confirmar = input("¿Estás seguro? (S/N): ").upper()
        
        if confirmar != 'S':
            print("Operación cancelada.")
            return
            
        result = collection.delete_one({"empno": empno})
        if result.deleted_count > 0:
            print("✅ Empleado eliminado exitosamente.")
        else:
            print("❌ No se pudo eliminar el empleado.")
            
    except ValueError:
        print("❌ Error: Ingresa un número válido.")
    except Exception as e:
        logger.error(f"Error al eliminar empleado: {e}")
        print("❌ Error al eliminar empleado:", e)