"""
Servicios para actualizar empleados existentes
"""
import logging
from db.mongo_config import get_collection
from services.read_service import leer_empleados
from .validation import validar_empleado_data

logger = logging.getLogger(__name__)

def actualizar_empleado():
    """
    Actualiza un empleado existente
    
    Returns:
        None: Interacción por consola
    """
    leer_empleados()
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        empno = int(input("\nID del empleado a actualizar: "))
        
        empleado = collection.find_one({"empno": empno})
        if not empleado:
            print("❌ Empleado no encontrado.")
            return

        print(f"\nActualizando empleado: {empleado['ename']}")
        print("Deja vacío para conservar el valor actual:")
        
        # Obtener nuevos valores
        nuevo_nombre = input(f"Nuevo nombre [{empleado['ename']}]: ").strip().upper() or empleado['ename']
        nuevo_job = input(f"Nuevo puesto [{empleado['job']}]: ").strip().upper() or empleado['job']
        
        nuevo_sal_input = input(f"Nuevo salario [{empleado['sal']}]: ").strip()
        nuevo_sal = float(nuevo_sal_input) if nuevo_sal_input else empleado['sal']
        
        # Validar nuevos datos
        if not validar_empleado_data(empno, nuevo_nombre, nuevo_job, nuevo_sal):
            return

        # Manejar departamento
        dept_actual = empleado.get('departamento', {})
        print(f"\nDepartamento actual: {dept_actual.get('dname')} ({dept_actual.get('deptno')})")
        
        cambiar_dept = input("¿Cambiar departamento? (S/N): ").upper()
        nuevo_departamento = obtener_nuevo_departamento(cambiar_dept, dept_actual)

        # Preparar actualización
        update_data = {
            "$set": {
                "ename": nuevo_nombre,
                "job": nuevo_job,
                "sal": nuevo_sal,
                "departamento": nuevo_departamento
            }
        }

        # Ejecutar actualización
        result = collection.update_one({"empno": empno}, update_data)
        
        if result.modified_count > 0:
            print("✅ Empleado actualizado exitosamente.")
        else:
            print("⚠️ No se realizaron cambios.")
            
    except ValueError:
        print("❌ Error: Ingresa valores numéricos válidos.")
    except Exception as e:
        logger.error(f"Error al actualizar empleado: {e}")
        print("❌ Error al actualizar empleado:", e)

def obtener_nuevo_departamento(cambiar_dept: str, dept_actual: dict) -> dict:
    """
    Obtiene los datos del nuevo departamento
    
    Args:
        cambiar_dept: Confirmación del usuario
        dept_actual: Datos actuales del departamento
        
    Returns:
        dict: Datos del departamento (actualizados o no)
    """
    if cambiar_dept != 'S':
        return dept_actual
        
    nuevo_deptno = int(input("Nuevo número de departamento: "))
    
    departamentos = {
        10: {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"},
        20: {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"},
        30: {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
    }
    
    return departamentos.get(nuevo_deptno) or {
        "deptno": nuevo_deptno,
        "dname": input("Nombre del departamento: ").upper(),
        "loc": input("Ubicación: ").upper()
    }