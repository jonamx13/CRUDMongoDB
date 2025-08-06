"""
Utilidades para operaciones específicas con MongoDB
Incluye funciones para datos de prueba y mantenimiento
"""

from db.mongo_config import get_collection
import logging

logger = logging.getLogger(__name__)

def datos_ya_existen():
    """
    Verifica si existen empleados en la colección
    - Devuelve True si hay datos
    - Devuelve False si está vacío
    - Devuelve None si hay error de conexión
    """
    try:
        collection = get_collection()
        if collection is None:
            logger.error("No se pudo conectar a la colección")
            return None
        
        return collection.count_documents({"empno": {"$exists": True}}) > 0

    except Exception as e:
        logger.error(f"Error al verificar datos existentes: {e}")
        return None

def insertar_datos_prueba():
    """
    Inserta datos de prueba del esquema SCOTT adaptado a MongoDB
    Maneja la posibilidad de que ya existan los empleados
    
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    try:
        collection = get_collection()
        if collection is None:
            logger.error("No se pudo conectar a la colección")
            print("❌ No se pudo conectar a la colección")
            return False
        
        # IDs de empleados de prueba
        empno_prueba = [7369, 7499, 7521, 7566, 7654, 7698, 
                        7782, 7788, 7839, 7844, 7876, 7900, 7902, 7934]
        
        # Verificar cuáles ya existen
        empno_existentes = set()
        for empno in empno_prueba:
            if collection.find_one({"empno": empno}):
                empno_existentes.add(empno)
        
        # Manejar empleados existentes
        if empno_existentes:
            print(f"⚠️ Algunos empleados ya existen (IDs: {', '.join(map(str, empno_existentes))})")
            sobrescribir = input("¿Deseas eliminarlos e insertar todos? (S/N): ").strip().upper()
            if sobrescribir != "S":
                print("Operación cancelada.")
                return False
            
            # Eliminar solo los existentes
            collection.delete_many({"empno": {"$in": list(empno_existentes)}})

        # Insertar datos de prueba
        empleados = _generar_datos_prueba()
        result = collection.insert_many(empleados)
        print(f"✅ Se insertaron {len(result.inserted_ids)} empleados correctamente")
        return True

    except Exception as e:
        logger.error(f"Error al insertar datos de prueba: {e}")
        print("❌ Error al insertar datos de prueba:", e)
        return False

def _generar_datos_prueba():
    """
    Genera la lista de empleados de prueba
    
    Returns:
        list: Lista de diccionarios con datos de empleados
    """
    return [
        {
            "empno": 7369, "ename": "SMITH", "job": "CLERK", "sal": 800,
            "departamento": {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"}
        },
        {
            "empno": 7499, "ename": "ALLEN", "job": "SALESMAN", "sal": 1600,
            "departamento": {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        },
        {
            "empno": 7521, "ename": "WARD", "job": "SALESMAN", "sal": 1250,
            "departamento": {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        },
        {
            "empno": 7566, "ename": "JONES", "job": "MANAGER", "sal": 2975,
            "departamento": {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"}
        },
        {
            "empno": 7654, "ename": "MARTIN", "job": "SALESMAN", "sal": 1250,
            "departamento": {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        },
        {
            "empno": 7698, "ename": "BLAKE", "job": "MANAGER", "sal": 2850,
            "departamento": {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        },
        {
            "empno": 7782, "ename": "CLARK", "job": "MANAGER", "sal": 2450,
            "departamento": {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"}
        },
        {
            "empno": 7788, "ename": "SCOTT", "job": "ANALYST", "sal": 3000,
            "departamento": {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"}
        },
        {
            "empno": 7839, "ename": "KING", "job": "PRESIDENT", "sal": 5000,
            "departamento": {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"}
        },
        {
            "empno": 7844, "ename": "TURNER", "job": "SALESMAN", "sal": 1500,
            "departamento": {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        },
        {
            "empno": 7876, "ename": "ADAMS", "job": "CLERK", "sal": 1100,
            "departamento": {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"}
        },
        {
            "empno": 7900, "ename": "JAMES", "job": "CLERK", "sal": 950,
            "departamento": {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        },
        {
            "empno": 7902, "ename": "FORD", "job": "ANALYST", "sal": 3000,
            "departamento": {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"}
        },
        {
            "empno": 7934, "ename": "MILLER", "job": "CLERK", "sal": 1300,
            "departamento": {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"}
        }
    ]

def limpiar_coleccion():
    """
    Elimina todos los documentos de la colección
    
    Returns:
        bool: True si se eliminaron documentos, False en caso de error
    """
    try:
        collection = get_collection()
        if collection is not None:
            result = collection.delete_many({})
            print(f"✅ Se eliminaron {result.deleted_count} documentos")
            return True
        return False
    except Exception as e:
        logger.error(f"Error al limpiar la colección: {e}")
        print("❌ Error al limpiar la colección:", e)
        return False