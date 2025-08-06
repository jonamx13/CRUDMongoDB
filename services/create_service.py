"""
Servicios para crear nuevos empleados
"""
import logging
from db.mongo_config import get_collection
from pymongo.errors import DuplicateKeyError
from .validation import validar_empleado_data

logger = logging.getLogger(__name__)

def crear_empleado():
    """
    Crea un nuevo empleado en la base de datos
    
    Returns:
        None: Interacción por consola
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        print("\n🆕 Crear nuevo empleado")
        
        # Obtener datos del usuario
        empno = int(input("Número de empleado (ej. 8000): "))
        ename = input("Nombre (máx 10 caracteres): ")[:10].upper()
        job = input("Puesto (ej. CLERK, MANAGER, ANALYST): ").upper()
        sal = float(input("Salario: "))
        
        # Validar datos antes de continuar
        if not validar_empleado_data(empno, ename, job, sal):
            return
            
        # Verificar existencia previa
        if collection.find_one({"empno": empno}):
            print("❌ Ya existe un empleado con ese número.")
            return
        
        # Obtener datos de departamento
        print("\nDatos del departamento:")
        deptno = int(input("Número de departamento (10=ACCOUNTING, 20=RESEARCH, 30=SALES): "))
        
        departamento = obtener_datos_departamento(deptno)
        if not departamento:
            return

        # Crear documento
        nuevo_empleado = {
            "empno": empno,
            "ename": ename,
            "job": job,
            "sal": sal,
            "departamento": departamento
        }

        # Insertar en la base de datos
        result = collection.insert_one(nuevo_empleado)
        print(f"✅ Empleado creado exitosamente con ID: {result.inserted_id}")
        
    except ValueError:
        print("❌ Error: Ingresa valores numéricos válidos.")
    except DuplicateKeyError:
        print("❌ Error: Número de empleado duplicado.")
    except Exception as e:
        logger.error(f"Error al crear empleado: {e}")
        print("❌ Error al crear empleado:", e)

def obtener_datos_departamento(deptno: int) -> dict:
    """
    Obtiene los datos de departamento basado en el número
    
    Args:
        deptno: Número de departamento
        
    Returns:
        dict: Datos del departamento
    """
    # Mapeo de departamentos predefinidos
    departamentos = {
        10: {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"},
        20: {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"},
        30: {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
    }
    
    if deptno in departamentos:
        return departamentos[deptno]
        
    print("⚠️ Departamento no reconocido. Usando datos personalizados...")
    dname = input("Nombre del departamento: ").upper()
    loc = input("Ubicación: ").upper()
    return {"deptno": deptno, "dname": dname, "loc": loc}