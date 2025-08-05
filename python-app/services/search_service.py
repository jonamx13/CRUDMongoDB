"""
Servicios para buscar empleados
"""
import logging
from db.mongo_config import get_collection

logger = logging.getLogger(__name__)

def buscar_empleado():
    """
    Busca un empleado por su ID
    
    Returns:
        None: Imprime resultados en consola
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        empno = int(input("ID del empleado a buscar: "))
        
        empleado = collection.find_one({"empno": empno})
        
        if not empleado:
            print("❌ Empleado no encontrado.")
            return
            
        mostrar_detalles_empleado(empleado)
            
    except ValueError:
        print("❌ Error: Ingresa un número válido.")
    except Exception as e:
        logger.error(f"Error al buscar empleado: {e}")
        print("❌ Error al buscar empleado:", e)

def mostrar_detalles_empleado(empleado: dict):
    """
    Muestra los detalles de un empleado
    
    Args:
        empleado: Diccionario con datos del empleado
    """
    print("\n📋 Información del empleado:")
    print("-" * 50)
    print(f"ID: {empleado['empno']}")
    print(f"Nombre: {empleado['ename']}")
    print(f"Puesto: {empleado['job']}")
    print(f"Salario: ${empleado['sal']:,.2f}")
    
    dept = empleado.get('departamento', {})
    print(f"Departamento: {dept.get('dname', 'N/A')} ({dept.get('deptno', 'N/A')})")
    print(f"Ubicación: {dept.get('loc', 'N/A')}")
    print("-" * 50)