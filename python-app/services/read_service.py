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

def listar_por_departamento():
    """
    Lista empleados filtrados por departamento
    
    Returns:
        None: Imprime resultados directamente en consola
    """
    try:
        collection = get_collection()
        if not collection:
            print("❌ No se pudo conectar a la base de datos")
            return

        print("Departamentos disponibles:")
        print("10 - ACCOUNTING")
        print("20 - RESEARCH") 
        print("30 - SALES")
        
        deptno = int(input("\nIngresa el número del departamento: "))
        
        empleados = list(collection.find(
            {"departamento.deptno": deptno}
        ).sort("empno", 1))
        
        if not empleados:
            print(f"⚠️ No hay empleados en el departamento {deptno}.")
            return
            
        dept_info = empleados[0].get('departamento', {})
        print(
            f"\n📋 Empleados del departamento {dept_info.get('dname', 'N/A')} "
            f"({dept_info.get('loc', 'N/A')}):"
        )
        print("-" * 60)
        print(f"{'ID':<6} {'NOMBRE':<10} {'PUESTO':<12} {'SALARIO'}")
        print("-" * 60)
        
        for emp in empleados:
            print(f"{emp['empno']:<6} {emp['ename']:<10} {emp['job']:<12} ${emp['sal']:,.2f}")
            
        print("-" * 60)
        print(f"Total de empleados: {len(empleados)}")
            
    except ValueError:
        print("❌ Error: Ingresa un número válido.")
    except Exception as e:
        logger.error(f"Error al listar por departamento: {e}")
        print("❌ Error al listar empleados por departamento:", e)