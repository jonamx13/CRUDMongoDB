"""
Servicios para actualizar empleados existentes - Versión corregida
"""
import logging
from db.mongo_config import get_collection
from services.read_service import leer_empleados
from ui.menus import limpiar_pantalla
from .validation import validar_empleado_data

logger = logging.getLogger(__name__)

# Puestos predefinidos
PUESTOS_VALIDOS = {
    'CLERK', 'SALESMAN', 'MANAGER', 'ANALYST', 'PRESIDENT'
}

def actualizar_empleado():
    """
    Actualiza un empleado existente con validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        while True:  # Bucle principal para permitir actualizar múltiples empleados
            # Limpiar pantalla y mostrar lista actual de empleados
            limpiar_pantalla()
            leer_empleados()
            
            print("\n✏️ Actualizar empleado")
            print("💡 Puedes escribir 'cancelar' en cualquier momento para salir\n")
            
            # Obtener ID del empleado
            empno = obtener_id_empleado()
            if empno is None:  # Usuario canceló
                print("❌ Operación cancelada por el usuario.")
                return
                
            # Buscar empleado
            empleado = collection.find_one({"empno": empno})
            if not empleado:
                print(f"❌ No se encontró un empleado con ID: {empno}")
                opcion = obtener_opcion_reintento("empleado no encontrado")
                if opcion == 'cancelar':
                    print("❌ Operación cancelada por el usuario.")
                    return
                elif opcion == 'reintentar':
                    continue  # Volver al inicio del bucle principal
                    
            else:
                # Empleado encontrado, proceder con actualización
                resultado_actualizacion = procesar_actualizacion(empleado, collection)
                
                if resultado_actualizacion == 'actualizado':
                    # Empleado actualizado exitosamente, preguntar si quiere actualizar otro
                    limpiar_pantalla()
                    leer_empleados()  # Mostrar lista actualizada
                    print(f"✅ Empleado {empleado['ename']} (ID: {empno}) actualizado exitosamente.\n")
                    
                    if preguntar_continuar():
                        continue  # Volver al inicio para actualizar otro empleado
                    else:
                        return  # Salir de la función
                        
                elif resultado_actualizacion == 'cancelado_continuar':
                    # Usuario canceló pero quiere actualizar otro empleado
                    continue  # Volver al inicio del bucle principal
                    
                elif resultado_actualizacion == 'cancelado_salir':
                    # Usuario canceló y quiere salir
                    print("❌ Operación cancelada por el usuario.")
                    return
                    
    except Exception as e:
        logger.error(f"Error inesperado al actualizar empleado: {e}")
        print(f"❌ Error inesperado al actualizar empleado: {str(e)}")

def procesar_actualizacion(empleado, collection):
    """
    Maneja todo el proceso de actualización de un empleado
    
    Args:
        empleado: Documento del empleado a actualizar
        collection: Colección de MongoDB
        
    Returns:
        str: 'actualizado', 'cancelado_continuar' o 'cancelado_salir'
    """
    print(f"\nActualizando empleado: {empleado['ename']} (ID: {empleado['empno']})")
    print("💡 Deja vacío para conservar el valor actual")
    print("💡 Escribe 'cancelar' para salir o 'atras' para volver al paso anterior\n")
    
    # Variables para almacenar los nuevos datos
    nuevo_nombre = None
    nuevo_job = None
    nuevo_sal = None
    nuevo_departamento = None
    
    # Control de flujo por pasos
    paso_actual = 0  # 0=nombre, 1=puesto, 2=salario, 3=departamento, 4=confirmación
    
    while True:
        if paso_actual == 0:  # Nombre
            resultado = obtener_nuevo_nombre(empleado['ename'])
            if resultado is None:
                return 'cancelado_salir'
            elif resultado == 'atras':
                print("ℹ️ No hay pasos anteriores. Estás en el primer campo.")
                continue
            else:
                nuevo_nombre = resultado
                paso_actual = 1
                
        elif paso_actual == 1:  # Puesto
            resultado = obtener_nuevo_puesto(empleado['job'])
            if resultado is None:
                return 'cancelado_salir'
            elif resultado == 'atras':
                paso_actual = 0
                continue
            else:
                nuevo_job = resultado
                paso_actual = 2
                
        elif paso_actual == 2:  # Salario
            resultado = obtener_nuevo_salario(empleado['sal'])
            if resultado is None:
                return 'cancelado_salir'
            elif resultado == 'atras':
                paso_actual = 1
                continue
            else:
                nuevo_sal = resultado
                paso_actual = 3
                
        elif paso_actual == 3:  # Departamento
            resultado = obtener_nuevo_departamento_completo(empleado.get('departamento', {}))
            if resultado is None:
                return 'cancelado_salir'
            elif resultado == 'atras':
                paso_actual = 2
                continue
            else:
                nuevo_departamento = resultado
                paso_actual = 4
                
        elif paso_actual == 4:  # Confirmación
            # Mostrar resumen de cambios
            print("\n📝 Resumen de cambios:")
            mostrar_comparacion(empleado, nuevo_nombre, nuevo_job, nuevo_sal, nuevo_departamento)
            
            confirmacion = input("\n¿Confirmar actualización? (S/N/atras): ").strip().upper()
            if confirmacion == 'ATRAS':
                paso_actual = 3  # Volver a departamento
                continue
            elif confirmacion == 'S':
                # Ejecutar actualización
                update_data = {
                    "$set": {
                        "ename": nuevo_nombre,
                        "job": nuevo_job,
                        "sal": nuevo_sal,
                        "departamento": nuevo_departamento
                    }
                }
                
                result = collection.update_one({"empno": empleado['empno']}, update_data)
                
                if result.modified_count > 0:
                    return 'actualizado'
                else:
                    print("⚠️ No se realizaron cambios (los datos son idénticos).")
                    return 'actualizado'  # Tratarlo como éxito
                    
            elif confirmacion == 'N':
                print("❌ Actualización cancelada por el usuario.")
                opcion = obtener_opcion_despues_cancelar()
                if opcion == 'salir':
                    return 'cancelado_salir'
                elif opcion == 'otro_empleado':
                    return 'cancelado_continuar'
                elif opcion == 'confirmar_de_nuevo':
                    continue  # Vuelve a mostrar la confirmación
                    
            elif confirmacion.lower() == 'cancelar':
                return 'cancelado_salir'
                
            else:
                print("❌ Opción no válida. Escribe S (Sí), N (No) o 'atras'")
                continue

def obtener_nuevo_nombre(nombre_actual):
    """Obtiene el nuevo nombre del empleado"""
    return obtener_dato_texto_opcional(
        f"Nuevo nombre [{nombre_actual}]: ",
        valor_actual=nombre_actual,
        max_longitud=10,
        mensaje_error="❌ El nombre debe tener máximo 10 caracteres"
    )

def obtener_nuevo_puesto(puesto_actual):
    """Obtiene el nuevo puesto del empleado"""
    while True:
        print(f"\nPuesto actual: {puesto_actual}")
        print("Puestos disponibles:", ', '.join(sorted(PUESTOS_VALIDOS)))
        entrada = input(f"Nuevo puesto [{puesto_actual}] (o 'nuevo' para crear uno): ").strip()
        
        if entrada.lower() == 'cancelar':
            return None
        elif entrada.lower() == 'atras':
            return 'atras'
        elif entrada == '':
            return puesto_actual  # Conservar valor actual
            
        job = entrada.upper()
        
        if job == 'NUEVO' or (job and job not in PUESTOS_VALIDOS):
            print("\n⚠️ Puesto no reconocido. Puedes:")
            print("1. Crear un nuevo puesto")
            print("2. Elegir uno de los disponibles")
            print("3. Conservar el puesto actual")
            print("4. Escribir 'atras' para volver")
            print("5. Escribir 'cancelar' para salir")
            
            opcion = input("\nElige una opción (1-5): ").strip()
            
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
                return puesto_actual
            elif opcion == '4':
                return 'atras'
            elif opcion == '5':
                return None
            else:
                print("❌ Opción no válida")
        elif job in PUESTOS_VALIDOS:
            return job
        else:
            print("❌ Puesto no válido")

def obtener_nuevo_salario(salario_actual):
    """Obtiene el nuevo salario del empleado"""
    return obtener_dato_numerico_opcional(
        f"Nuevo salario [{salario_actual}]: ",
        valor_actual=salario_actual,
        tipo=float,
        validacion=lambda x: x >= 0,
        mensaje_error="❌ El salario no puede ser negativo"
    )

def obtener_nuevo_departamento_completo(dept_actual):
    """Obtiene los datos del nuevo departamento"""
    print(f"\n📍 Departamento actual:")
    if dept_actual:
        print(f"   Número: {dept_actual.get('deptno', 'N/A')}")
        print(f"   Nombre: {dept_actual.get('dname', 'N/A')}")
        print(f"   Ubicación: {dept_actual.get('loc', 'N/A')}")
    else:
        print("   Sin departamento asignado")
    
    cambiar = input("\n¿Cambiar departamento? (S/N/atras): ").strip().upper()
    
    if cambiar.lower() == 'cancelar':
        return None
    elif cambiar.lower() == 'atras':
        return 'atras'
    elif cambiar == 'N' or cambiar == '':
        return dept_actual or {}
    elif cambiar == 'S':
        return obtener_departamento_nuevo()
    else:
        print("❌ Opción no válida. Escribe S (Sí) o N (No)")
        return obtener_nuevo_departamento_completo(dept_actual)

def obtener_departamento_nuevo():
    """Obtiene un nuevo departamento"""
    while True:
        deptno = obtener_dato_numerico(
            "Número de departamento (10=ACCOUNTING, 20=RESEARCH, 30=SALES): ",
            mensaje_error="❌ Número de departamento inválido"
        )
        if deptno is None:
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
            
        print("\n⚠️ Departamento no reconocido.")
        print("1. Crear un nuevo departamento")
        print("2. Volver a elegir número")
        print("3. Cancelar")
        
        opcion = input("\nElige una opción (1-3): ").strip()
        
        if opcion == '1':
            dname = obtener_dato_texto(
                "Nombre del departamento: ",
                mensaje_error="❌ El nombre no puede estar vacío"
            )
            if dname is None: return None
            elif dname == 'atras': continue
            
            loc = obtener_dato_texto(
                "Ubicación: ",
                mensaje_error="❌ La ubicación no puede estar vacía"
            )
            if loc is None: return None
            elif loc == 'atras': continue

            return {"deptno": deptno, "dname": dname, "loc": loc}
            
        elif opcion == '2':
            continue
        elif opcion == '3':
            return None
        else:
            print("❌ Opción no válida")

def mostrar_comparacion(empleado, nuevo_nombre, nuevo_job, nuevo_sal, nuevo_departamento):
    """Muestra una comparación entre valores actuales y nuevos"""
    print(f"Nombre: {empleado['ename']} → {nuevo_nombre}")
    print(f"Puesto: {empleado['job']} → {nuevo_job}")
    print(f"Salario: ${empleado['sal']:,.2f} → ${nuevo_sal:,.2f}")
    
    dept_actual = empleado.get('departamento', {})
    dept_actual_str = f"{dept_actual.get('dname', 'N/A')} ({dept_actual.get('loc', 'N/A')})"
    dept_nuevo_str = f"{nuevo_departamento.get('dname', 'N/A')} ({nuevo_departamento.get('loc', 'N/A')})"
    print(f"Departamento: {dept_actual_str} → {dept_nuevo_str}")

# Funciones auxiliares (reutilizadas del create_service)
def obtener_id_empleado(reintentos=3):
    """Obtiene el ID del empleado con validación"""
    for intento in range(reintentos):
        try:
            entrada = input("ID del empleado a actualizar: ").strip()
            
            if entrada.lower() == 'cancelar':
                return None
                
            if not entrada:
                print("❌ Debes ingresar un ID de empleado")
                if intento < reintentos - 1:
                    print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                continue
                
            empno = int(entrada)
            
            if empno <= 0:
                print("❌ El ID del empleado debe ser un número positivo")
                if intento < reintentos - 1:
                    print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                continue
                
            return empno
            
        except ValueError:
            print("❌ Error: Debes ingresar un número válido")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
            
    print("❌ Demasiados intentos fallidos.")
    opcion = obtener_opcion_reintento("demasiados intentos fallidos")
    if opcion == 'reintentar':
        return obtener_id_empleado(reintentos)
    else:
        return None

def obtener_opcion_reintento(razon):
    """Pregunta al usuario qué hacer después de un error"""
    print(f"\n⚠️ No se pudo proceder debido a: {razon}")
    print("¿Qué deseas hacer?")
    print("1. Intentar con otro ID")
    print("2. Cancelar operación")
    
    while True:
        opcion = input("\nElige una opción (1-2): ").strip()
        
        if opcion == '1':
            return 'reintentar'
        elif opcion == '2':
            return 'cancelar'
        else:
            print("❌ Opción no válida. Elige 1 o 2")

def obtener_opcion_despues_cancelar():
    """Pregunta al usuario qué hacer después de cancelar"""
    print("\n¿Qué deseas hacer ahora?")
    print("1. Actualizar otro empleado")
    print("2. Volver a confirmar este mismo empleado")
    print("3. Salir de la operación")
    
    while True:
        opcion = input("\nElige una opción (1-3): ").strip()
        
        if opcion == '1':
            return 'otro_empleado'
        elif opcion == '2':
            return 'confirmar_de_nuevo'
        elif opcion == '3':
            return 'salir'
        else:
            print("❌ Opción no válida. Elige 1, 2 o 3")

def preguntar_continuar():
    """Pregunta si el usuario quiere actualizar otro empleado"""
    print("¿Deseas actualizar otro empleado?")
    print("1. Sí, actualizar otro empleado")
    print("2. No, regresar al menú principal")
    
    while True:
        opcion = input("\nElige una opción (1-2): ").strip()
        
        if opcion == '1':
            return True
        elif opcion == '2':
            return False
        else:
            print("❌ Opción no válida. Elige 1 o 2")

def obtener_dato_numerico(prompt, tipo=int, validacion=None, mensaje_error="❌ Valor inválido", reintentos=3):
    """Obtiene un dato numérico con validación"""
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
    
    print("❌ Demasiados intentos fallidos.")
    return None

def obtener_dato_numerico_opcional(prompt, valor_actual, tipo=int, validacion=None, mensaje_error="❌ Valor inválido", reintentos=3):
    """Obtiene un dato numérico opcional (puede conservar el actual)"""
    for intento in range(reintentos):
        try:
            valor = input(prompt).strip()
            if valor.lower() == 'cancelar':
                return None
            elif valor.lower() == 'atras':
                return 'atras'
            elif valor == '':
                return valor_actual  # Conservar valor actual
                
            numero = tipo(valor)
            
            if validacion and not validacion(numero):
                print(mensaje_error)
                continue
                
            return numero
            
        except ValueError:
            print(mensaje_error)
            
        if intento < reintentos - 1:
            print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
    
    print("❌ Demasiados intentos fallidos.")
    return None

def obtener_dato_texto(prompt, max_longitud=None, mensaje_error="❌ Texto inválido", reintentos=3):
    """Obtiene un dato de texto con validación"""
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
            continue
            
        if max_longitud and len(valor) > max_longitud:
            print(f"❌ El texto no puede exceder {max_longitud} caracteres")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
            continue
            
        return valor.upper()
    
    print("❌ Demasiados intentos fallidos.")
    return None

def obtener_dato_texto_opcional(prompt, valor_actual, max_longitud=None, mensaje_error="❌ Texto inválido", reintentos=3):
    """Obtiene un dato de texto opcional (puede conservar el actual)"""
    for intento in range(reintentos):
        valor = input(prompt).strip()
        if valor.lower() == 'cancelar':
            return None
        elif valor.lower() == 'atras':
            return 'atras'
        elif valor == '':
            return valor_actual  # Conservar valor actual
            
        if max_longitud and len(valor) > max_longitud:
            print(f"❌ El texto no puede exceder {max_longitud} caracteres")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
            continue
            
        return valor.upper()
    
    print("❌ Demasiados intentos fallidos.")
    return None