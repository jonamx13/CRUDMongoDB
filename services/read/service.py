"""
Servicios relacionados con la lectura de datos de empleados
"""
import logging
from db.mongo_config import get_collection

logger = logging.getLogger(__name__)

def leer_empleados():
    """
    Lista todos los empleados ordenados por empno
    
    Returns:
        None: Imprime resultados directamente en consola
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        empleados = list(collection.find({}).sort("empno", 1))
        
        if not empleados:
            print("⚠️ No hay empleados registrados.")
            return
            
        print("\n📋 Lista de empleados:")
        print("-" * 80)
        print(f"{'ID':<6} {'NOMBRE':<10} {'PUESTO':<12} {'SALARIO':<10} {'DEPARTAMENTO':<15} {'UBICACIÓN'}")
        print("-" * 80)
        
        for emp in empleados:
            dept = emp.get("departamento", {})
            print(
                f"{emp['empno']:<6} {emp['ename']:<10} "
                f"{emp['job']:<12} ${emp['sal']:<9.2f} "
                f"{dept.get('dname', 'N/A'):<15} {dept.get('loc', 'N/A')}"
            )
            
        print("-" * 80)
        
    except Exception as e:
        logger.error(f"Error al leer empleados: {e}")
        print("❌ Error al leer empleados:", e)