import logging
from db.mongo_config import get_collection
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

def leer_empleados():
    """
    Lista todos los empleados ordenados por empno
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        empleados = list(collection.find({}).sort("empno", 1))
        
        if not empleados:
            print("⚠️ No hay empleados registrados.")
        else:
            print("\n📋 Lista de empleados:")
            print("-" * 80)
            print(f"{'ID':<6} {'NOMBRE':<10} {'PUESTO':<12} {'SALARIO':<10} {'DEPARTAMENTO':<15} {'UBICACIÓN'}")
            print("-" * 80)
            for emp in empleados:
                dept = emp.get("departamento", {})
                print(f"{emp['empno']:<6} {emp['ename']:<10} {emp['job']:<12} ${emp['sal']:<9.2f} {dept.get('dname', 'N/A'):<15} {dept.get('loc', 'N/A')}")
            print("-" * 80)
    except Exception as e:
        print("❌ Error al leer empleados:", e)

def crear_empleado():
    """
    Crea un nuevo empleado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        print("\n🆕 Crear nuevo empleado")
        
        # Solicitar datos del empleado
        empno = int(input("Número de empleado (ej. 8000): "))
        
        # Verificar si el empleado ya existe
        if collection.find_one({"empno": empno}):
            print("❌ Ya existe un empleado con ese número.")
            return
            
        ename = input("Nombre (máx 10 caracteres): ")[:10].upper()
        job = input("Puesto (ej. CLERK, MANAGER, ANALYST): ").upper()
        sal = float(input("Salario: "))
        
        print("\nDatos del departamento:")
        deptno = int(input("Número de departamento (10=ACCOUNTING, 20=RESEARCH, 30=SALES): "))
        
        # Mapeo de departamentos
        departamentos = {
            10: {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"},
            20: {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"},
            30: {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        }
        
        if deptno not in departamentos:
            print("⚠️ Departamento no reconocido. Usando datos personalizados...")
            dname = input("Nombre del departamento: ").upper()
            loc = input("Ubicación: ").upper()
            departamento = {"deptno": deptno, "dname": dname, "loc": loc}
        else:
            departamento = departamentos[deptno]

        # Crear documento del empleado
        nuevo_empleado = {
            "empno": empno,
            "ename": ename,
            "job": job,
            "sal": sal,
            "departamento": departamento
        }

        result = collection.insert_one(nuevo_empleado)
        print(f"✅ Empleado creado exitosamente con ID: {result.inserted_id}")
        
    except ValueError:
        print("❌ Error: Ingresa valores numéricos válidos.")
    except Exception as e:
        print("❌ Error al crear empleado:", e)

def actualizar_empleado():
    """
    Actualiza un empleado existente
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
        
        # Actualizar campos básicos
        nuevo_nombre = input(f"Nuevo nombre [{empleado['ename']}]: ").upper()
        if not nuevo_nombre:
            nuevo_nombre = empleado['ename']
            
        nuevo_job = input(f"Nuevo puesto [{empleado['job']}]: ").upper()
        if not nuevo_job:
            nuevo_job = empleado['job']
            
        nuevo_sal = input(f"Nuevo salario [{empleado['sal']}]: ")
        if nuevo_sal:
            nuevo_sal = float(nuevo_sal)
        else:
            nuevo_sal = empleado['sal']

        # Actualizar departamento
        dept_actual = empleado.get('departamento', {})
        print(f"\nDepartamento actual: {dept_actual.get('dname')} ({dept_actual.get('deptno')})")
        cambiar_dept = input("¿Cambiar departamento? (S/N): ").upper()
        
        if cambiar_dept == 'S':
            nuevo_deptno = int(input("Nuevo número de departamento: "))
            departamentos = {
                10: {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"},
                20: {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"},
                30: {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
            }
            
            if nuevo_deptno in departamentos:
                nuevo_departamento = departamentos[nuevo_deptno]
            else:
                dname = input("Nombre del departamento: ").upper()
                loc = input("Ubicación: ").upper()
                nuevo_departamento = {"deptno": nuevo_deptno, "dname": dname, "loc": loc}
        else:
            nuevo_departamento = dept_actual

        # Actualizar documento
        update_data = {
            "$set": {
                "ename": nuevo_nombre,
                "job": nuevo_job,
                "sal": nuevo_sal,
                "departamento": nuevo_departamento
            }
        }

        result = collection.update_one({"empno": empno}, update_data)
        
        if result.modified_count > 0:
            print("✅ Empleado actualizado exitosamente.")
        else:
            print("⚠️ No se realizaron cambios.")
            
    except ValueError:
        print("❌ Error: Ingresa valores numéricos válidos.")
    except Exception as e:
        print("❌ Error al actualizar empleado:", e)

def eliminar_empleado():
    """
    Elimina un empleado
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
        
        if confirmar == 'S':
            result = collection.delete_one({"empno": empno})
            if result.deleted_count > 0:
                print("✅ Empleado eliminado exitosamente.")
            else:
                print("❌ No se pudo eliminar el empleado.")
        else:
            print("Operación cancelada.")
            
    except ValueError:
        print("❌ Error: Ingresa un número válido.")
    except Exception as e:
        print("❌ Error al eliminar empleado:", e)

def buscar_empleado():
    """
    Busca un empleado por su ID
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
        else:
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
            
    except ValueError:
        print("❌ Error: Ingresa un número válido.")
    except Exception as e:
        print("❌ Error al buscar empleado:", e)

def listar_por_departamento():
    """
    Lista empleados por departamento
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        print("Departamentos disponibles:")
        print("10 - ACCOUNTING")
        print("20 - RESEARCH") 
        print("30 - SALES")
        
        deptno = int(input("\nIngresa el número del departamento: "))
        
        empleados = list(collection.find({"departamento.deptno": deptno}).sort("empno", 1))
        
        if not empleados:
            print(f"⚠️ No hay empleados en el departamento {deptno}.")
        else:
            dept_info = empleados[0].get('departamento', {})
            print(f"\n📋 Empleados del departamento {dept_info.get('dname', 'N/A')} ({dept_info.get('loc', 'N/A')}):")
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
        print("❌ Error al listar empleados por departamento:", e)

        # Agregar función de validación
def validar_empleado_data(empno: int, ename: str, job: str, sal: float) -> bool:
    """
    Valida los datos del empleado
    """
    if empno <= 0:
        print("❌ El número de empleado debe ser positivo")
        return False
    
    if not ename or len(ename.strip()) == 0:
        print("❌ El nombre no puede estar vacío")
        return False
    
    if not job or len(job.strip()) == 0:
        print("❌ El puesto no puede estar vacío")
        return False
    
    if sal < 0:
        print("❌ El salario no puede ser negativo")
        return False
    
    return True

# Agregar nueva función para estadísticas
def mostrar_estadisticas():
    """
    Muestra estadísticas de la base de datos
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        # Estadísticas generales
        total_empleados = collection.count_documents({})
        
        if total_empleados == 0:
            print("⚠️ No hay empleados registrados.")
            return

        # Estadísticas por departamento
        pipeline = [
            {
                "$group": {
                    "_id": "$departamento.dname",
                    "total": {"$sum": 1},
                    "salario_promedio": {"$avg": "$sal"},
                    "salario_total": {"$sum": "$sal"}
                }
            },
            {
                "$sort": {"total": -1}
            }
        ]
        
        stats = list(collection.aggregate(pipeline))
        
        print("\n📊 Estadísticas de Empleados")
        print("=" * 60)
        print(f"Total de empleados: {total_empleados}")
        print("\nPor departamento:")
        print("-" * 60)
        print(f"{'DEPARTAMENTO':<15} {'EMPLEADOS':<10} {'SALARIO PROM.':<15} {'TOTAL SAL.'}")
        print("-" * 60)
        
        for stat in stats:
            dept = stat['_id'] or 'Sin Depto'
            total = stat['total']
            promedio = stat['salario_promedio']
            total_sal = stat['salario_total']
            print(f"{dept:<15} {total:<10} ${promedio:<14,.2f} ${total_sal:,.2f}")
        
        print("-" * 60)
        
    except Exception as e:
        logger.error(f"Error al generar estadísticas: {e}")
        print("❌ Error al generar estadísticas:", e)