"""
Manejadores de entrada para creación de empleados
"""
from shared import constants, input_utils
from db.mongo_config import get_collection
from pymongo.errors import DuplicateKeyError

def obtener_empno():
    """Obtiene el número de empleado con validación"""
    while True:
        empno = input_utils.obtener_dato_numerico(
            "Número de empleado (ej. 8000): ",
            validacion=lambda x: x > 0,
            mensaje_error="❌ El número de empleado debe ser positivo"
        )
        if empno is None:  # Usuario canceló
            return None
        elif empno == 'atras':
            return 'atras'
        
        # Verificar existencia previa
        collection = get_collection()
        if collection.find_one({"empno": empno}):
            print(f"❌ Ya existe un empleado con el número {empno}.")
            continue
        
        return empno

def obtener_nombre():
    """Obtiene el nombre del empleado con validación"""
    return input_utils.obtener_dato_texto(
        "Nombre (máx 10 caracteres): ",
        max_longitud=10,
        mensaje_error="❌ El nombre no puede estar vacío y debe tener máximo 10 caracteres"
    )

def obtener_puesto():
    """Obtiene el puesto del empleado con validación"""
    while True:
        print("\nPuestos disponibles:", ', '.join(sorted(constants.PUESTOS_VALIDOS)))
        job = input("Puesto (o escribe 'nuevo' para crear uno): ").strip().upper()
        
        if job.lower() == 'cancelar':
            return None
        elif job.lower() == 'atras':
            return 'atras'
        elif job == 'NUEVO' or (job and job not in constants.PUESTOS_VALIDOS):
            print("\n⚠️ Puesto no reconocido. Puedes:")
            print("1. Crear un nuevo puesto")
            print("2. Elegir uno de los disponibles")
            print("3. Escribir 'atras' para volver")
            print("4. Escribir 'cancelar' para salir")
            
            opcion = input("\nElige una opción (1-4): ").strip()
            
            if opcion == '1':
                nuevo_puesto = input_utils.obtener_dato_texto(
                    "Nombre del nuevo puesto: ",
                    mensaje_error="❌ El puesto no puede estar vacío"
                )
                if nuevo_puesto is None:
                    return None
                elif nuevo_puesto == 'atras':
                    continue
                constants.PUESTOS_VALIDOS.add(nuevo_puesto)
                return nuevo_puesto
            elif opcion == '2':
                continue  # Volver a mostrar puestos disponibles
            elif opcion == '3':
                return 'atras'
            elif opcion == '4':
                return None
            else:
                print("❌ Opción no válida")
        elif job in constants.PUESTOS_VALIDOS:
            return job
        elif job == '':
            print("❌ Debes seleccionar un puesto")
        else:
            print("❌ Puesto no válido")

def obtener_salario():
    """Obtiene el salario con validación"""
    return input_utils.obtener_dato_numerico(
        "Salario: ",
        tipo=float,
        validacion=lambda x: x >= 0,
        mensaje_error="❌ El salario no puede ser negativo"
    )

def obtener_departamento():
    """Obtiene el departamento con validación"""
    while True:
        print("\nDatos del departamento:")
        deptno = input_utils.obtener_dato_numerico(
            "Número de departamento (10=ACCOUNTING, 20=RESEARCH, 30=SALES): ",
            mensaje_error="❌ Número de departamento inválido"
        )
        if deptno is None:  # Usuario canceló
            return None
        elif deptno == 'atras':
            return 'atras'
        
        # Mapeo de departamentos predefinidos
        departamentos = {
            10: {"deptno": 10, "dname": "ACCOUNTING", "loc": "NEW YORK"},
            20: {"deptno": 20, "dname": "RESEARCH", "loc": "DALLAS"},
            30: {"deptno": 30, "dname": "SALES", "loc": "CHICAGO"}
        }
        
        if deptno in departamentos:
            return departamentos[deptno]
            
        print("\n⚠️ Departamento no reconocido. Puedes:")
        print("1. Crear un nuevo departamento")
        print("2. Volver a elegir número de departamento")
        print("3. Cancelar la operación")
        
        opcion = input("\nElige una opción (1-3): ").strip()
        
        if opcion == '1':
            print("\nIntroduce los datos del nuevo departamento:")
            dname = input_utils.obtener_dato_texto(
                "Nombre del departamento: ",
                mensaje_error="❌ El nombre no puede estar vacío"
            )
            if dname is None: 
                return None
            elif dname == 'atras': 
                continue
            
            loc = input_utils.obtener_dato_texto(
                "Ubicación: ",
                mensaje_error="❌ La ubicación no puede estar vacía"
            )
            if loc is None: 
                return None
            elif loc == 'atras': 
                continue

            return {"deptno": deptno, "dname": dname, "loc": loc}
            
        elif opcion == '2':
            continue  # Volver a pedir número de departamento
            
        elif opcion == '3':
            return None
            
        else:
            print("❌ Opción no válida")