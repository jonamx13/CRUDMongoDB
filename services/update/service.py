"""
Servicios para actualizar empleados existentes - Versión corregida
"""
import logging
from db.mongo_config import get_collection
from services.read.service import leer_empleados
from ui.menus import limpiar_pantalla
from .input_handlers import obtener_nuevo_nombre, obtener_nuevo_puesto, obtener_nuevo_salario, obtener_nuevo_departamento_completo
from .display import mostrar_comparacion
from services.shared import constants
from services.shared.input_utils import obtener_dato_numerico, obtener_dato_texto, obtener_opcion_reintento

logger = logging.getLogger(__name__)

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