"""
Servicios para crear nuevos empleados - Versión final corregida
"""
import logging
from db.mongo_config import get_collection
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

# Puestos predefinidos
PUESTOS_VALIDOS = {
    'CLERK', 'SALESMAN', 'MANAGER', 'ANALYST', 'PRESIDENT'
}

def crear_empleado():
    """
    Crea un nuevo empleado en la base de datos con validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        print("\n🆕 Crear nuevo empleado")
        print("💡 Puedes escribir 'cancelar' en cualquier momento para salir")
        print("💡 Para volver al paso anterior escribe 'atras'\n")
        
        # Variables para almacenar los datos
        empno = None
        ename = None
        job = None
        sal = None
        departamento = None
        
        # Paso actual (0=empno, 1=ename, 2=job, 3=sal, 4=departamento)
        paso_actual = 0
        
        while True:
            if paso_actual == 0:  # Número de empleado
                resultado = obtener_empno()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # No hay pasos anteriores
                    print("ℹ️ No hay pasos anteriores. Estás en el primer campo.")
                    continue
                else:
                    empno = resultado
                    paso_actual = 1
                    
            elif paso_actual == 1:  # Nombre
                resultado = obtener_nombre()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a empno
                    paso_actual = 0
                    continue
                else:
                    ename = resultado
                    paso_actual = 2
                    
            elif paso_actual == 2:  # Puesto
                resultado = obtener_puesto()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a nombre
                    paso_actual = 1
                    continue
                else:
                    job = resultado
                    paso_actual = 3
                    
            elif paso_actual == 3:  # Salario
                resultado = obtener_salario()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a puesto
                    paso_actual = 2
                    continue
                else:
                    sal = resultado
                    paso_actual = 4
                    
            elif paso_actual == 4:  # Departamento
                resultado = obtener_departamento()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a salario
                    paso_actual = 3
                    continue
                else:
                    departamento = resultado
                    paso_actual = 5  # Ir a confirmación
                    
            elif paso_actual == 5:  # Confirmación
                # Mostrar resumen
                print("\n📝 Resumen del nuevo empleado:")
                print(f"ID: {empno}")
                print(f"Nombre: {ename}")
                print(f"Puesto: {job}")
                print(f"Salario: ${sal:,.2f}")
                print(f"Departamento: {departamento['dname']} ({departamento['loc']})")
                
                confirmacion = input("\n¿Confirmar creación? (S/N/atras): ").strip().upper()
                if confirmacion == 'ATRAS':
                    paso_actual = 4  # Volver a departamento
                    continue
                elif confirmacion == 'S':
                    # Crear documento e insertar
                    nuevo_empleado = {
                        "empno": empno,
                        "ename": ename,
                        "job": job,
                        "sal": sal,
                        "departamento": departamento
                    }
                    
                    result = collection.insert_one(nuevo_empleado)
                    print(f"\n✅ Empleado creado exitosamente con ID: {result.inserted_id}")
                    return
                elif confirmacion == 'N':
                    print("❌ Creación cancelada por el usuario")
                    return
                elif confirmacion.lower() == 'cancelar':
                    print("❌ Creación cancelada por el usuario")
                    return
                else:
                    print("❌ Opción no válida. Elige S (Sí), N (No) o 'atras'")
                    continue
        
    except DuplicateKeyError:
        print("❌ Error: Número de empleado duplicado (aunque se validó previamente).")
    except Exception as e:
        logger.error(f"Error inesperado al crear empleado: {e}")
        print("❌ Error inesperado al crear empleado:", str(e))

def obtener_empno():
    """Obtiene el número de empleado con validación"""
    while True:
        empno = obtener_dato_numerico(
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
    return obtener_dato_texto(
        "Nombre (máx 10 caracteres): ",
        max_longitud=10,
        mensaje_error="❌ El nombre no puede estar vacío y debe tener máximo 10 caracteres"
    )

def obtener_puesto():
    """Obtiene el puesto del empleado con validación"""
    while True:
        print("\nPuestos disponibles:", ', '.join(sorted(PUESTOS_VALIDOS)))
        job = input("Puesto (o escribe 'nuevo' para crear uno): ").strip().upper()
        
        if job.lower() == 'cancelar':
            return None
        elif job.lower() == 'atras':
            return 'atras'
        elif job == 'NUEVO' or (job and job not in PUESTOS_VALIDOS):
            print("\n⚠️ Puesto no reconocido. Puedes:")
            print("1. Crear un nuevo puesto")
            print("2. Elegir uno de los disponibles")
            print("3. Escribir 'atras' para volver")
            print("4. Escribir 'cancelar' para salir")
            
            opcion = input("\nElige una opción (1-4): ").strip()
            
            if opcion == '1':
                nuevo_puesto = obtener_dato_texto(
                    "Nombre del nuevo puesto: ",
                    mensaje_error="❌ El puesto no puede estar vacío"
                )
                if nuevo_puesto is None:
                    return None
                elif nuevo_puesto == 'atras':
                    continue
                PUESTOS_VALIDOS.add(nuevo_puesto)
                return nuevo_puesto
            elif opcion == '2':
                continue  # Volver a mostrar puestos disponibles
            elif opcion == '3':
                return 'atras'
            elif opcion == '4':
                return None
            else:
                print("❌ Opción no válida")
        elif job in PUESTOS_VALIDOS:
            return job
        elif job == '':
            print("❌ Debes seleccionar un puesto")
        else:
            print("❌ Puesto no válido")

def obtener_salario():
    """Obtiene el salario con validación"""
    return obtener_dato_numerico(
        "Salario: ",
        tipo=float,
        validacion=lambda x: x >= 0,
        mensaje_error="❌ El salario no puede ser negativo"
    )

def obtener_departamento():
    """Obtiene el departamento con validación"""
    while True:
        print("\nDatos del departamento:")
        deptno = obtener_dato_numerico(
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
            dname = obtener_dato_texto(
                "Nombre del departamento: ",
                mensaje_error="❌ El nombre no puede estar vacío"
            )
            if dname is None: 
                return None
            elif dname == 'atras': 
                continue
            
            loc = obtener_dato_texto(
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

def obtener_dato_numerico(
    prompt: str,
    tipo=int,
    validacion=None,
    mensaje_error: str = "❌ Valor inválido",
    reintentos: int = 3
):
    """
    Obtiene un dato numérico del usuario con validación y reintentos
    
    Args:
        prompt: Mensaje para mostrar al usuario
        tipo: Tipo numérico (int o float)
        validacion: Función de validación adicional
        mensaje_error: Mensaje a mostrar cuando falla la validación
        reintentos: Número máximo de reintentos
        
    Returns:
        Número válido, 'atras' o None si se cancela
    """
    for intento in range(reintentos):
        try:
            valor = input(prompt).strip()
            if valor.lower() == 'cancelar':
                return None
            elif valor.lower() == 'atras':
                return 'atras'
                
            numero = tipo(valor)
            
            if validacion and not validacion(numero):
                print(mensaje_error)
                continue
                
            return numero
            
        except ValueError:
            print(mensaje_error)
            
        if intento < reintentos - 1:
            print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
            print("💡 Escribe 'atras' para volver o 'cancelar' para salir")
    
    print("❌ Demasiados intentos fallidos. Operación cancelada.")
    return None

def obtener_dato_texto(
    prompt: str,
    max_longitud: int = None,
    mensaje_error: str = "❌ Texto inválido",
    reintentos: int = 3
):
    """
    Obtiene un dato de texto del usuario con validación
    
    Args:
        prompt: Mensaje para mostrar al usuario
        max_longitud: Longitud máxima permitida (opcional)
        mensaje_error: Mensaje a mostrar cuando falla la validación
        reintentos: Número máximo de reintentos
        
    Returns:
        Texto válido (en mayúsculas), 'atras' o None si se cancela
    """
    for intento in range(reintentos):
        valor = input(prompt).strip()
        if valor.lower() == 'cancelar':
            return None
        elif valor.lower() == 'atras':
            return 'atras'
            
        if not valor:
            print(mensaje_error)
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                print("💡 Escribe 'atras' para volver o 'cancelar' para salir")
            continue
            
        if max_longitud and len(valor) > max_longitud:
            print(f"❌ El texto no puede exceder {max_longitud} caracteres")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                print("💡 Escribe 'atras' para volver o 'cancelar' para salir")
            continue
            
        return valor.upper()
    
    print("❌ Demasiados intentos fallidos. Operación cancelada.")
    return None