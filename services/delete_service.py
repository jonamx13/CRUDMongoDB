"""
Servicios para eliminar empleados
"""
import logging
from db.mongo_config import get_collection
from services.read_service import leer_empleados
from ui.menus import limpiar_pantalla

logger = logging.getLogger(__name__)

def eliminar_empleado():
    """
    Elimina un empleado de la base de datos con validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        while True:  # Bucle principal para permitir eliminar múltiples empleados
            # Limpiar pantalla y mostrar lista actual de empleados
            limpiar_pantalla()
            leer_empleados()
            
            print("\n🗑️ Eliminar empleado")
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
                # Empleado encontrado, proceder con confirmación
                resultado_confirmacion = confirmar_eliminacion(empleado, collection)
                
                if resultado_confirmacion == 'eliminado':
                    # Empleado eliminado exitosamente, preguntar si quiere eliminar otro
                    limpiar_pantalla()
                    leer_empleados()  # Mostrar lista actualizada
                    print(f"✅ Empleado {empleado['ename']} (ID: {empno}) eliminado exitosamente.\n")
                    
                    if preguntar_continuar():
                        continue  # Volver al inicio para eliminar otro empleado
                    else:
                        return  # Salir de la función
                        
                elif resultado_confirmacion == 'cancelado_continuar':
                    # Usuario canceló pero quiere eliminar otro empleado
                    continue  # Volver al inicio del bucle principal
                    
                elif resultado_confirmacion == 'cancelado_salir':
                    # Usuario canceló y quiere salir
                    print("❌ Operación cancelada por el usuario.")
                    return
                    
    except Exception as e:
        logger.error(f"Error inesperado al eliminar empleado: {e}")
        print(f"❌ Error inesperado al eliminar empleado: {str(e)}")

def confirmar_eliminacion(empleado, collection):
    """
    Maneja la confirmación de eliminación de un empleado
    
    Args:
        empleado: Documento del empleado a eliminar
        collection: Colección de MongoDB
        
    Returns:
        str: 'eliminado', 'cancelado_continuar' o 'cancelado_salir'
    """
    while True:
        print(f"\n⚠️ Vas a eliminar al empleado:")
        print(f"   ID: {empleado['empno']}")
        print(f"   Nombre: {empleado['ename']}")
        print(f"   Puesto: {empleado['job']}")
        print(f"   Salario: ${empleado['sal']:,.2f}")
        if 'departamento' in empleado:
            print(f"   Departamento: {empleado['departamento']['dname']} ({empleado['departamento']['loc']})")
        
        print("\n⚠️ Esta acción NO se puede deshacer.")
        confirmar = input("¿Estás seguro de que quieres eliminar este empleado? (S/N/cancelar): ").strip().upper()
        
        if confirmar == 'S':
            # Proceder con eliminación
            result = collection.delete_one({"empno": empleado['empno']})
            if result.deleted_count > 0:
                return 'eliminado'
            else:
                print("❌ No se pudo eliminar el empleado. Error interno.")
                return 'cancelado_salir'
                
        elif confirmar == 'N':
            print("❌ Eliminación cancelada por el usuario.")
            opcion = obtener_opcion_despues_cancelar()
            if opcion == 'salir':
                return 'cancelado_salir'
            elif opcion == 'otro_empleado':
                return 'cancelado_continuar'
            elif opcion == 'confirmar_de_nuevo':
                continue  # Vuelve a mostrar la confirmación del mismo empleado
                
        elif confirmar.lower() == 'cancelar':
            return 'cancelado_salir'
            
        else:
            print("❌ Opción no válida. Escribe S (Sí), N (No) o 'cancelar'")
            continue

def obtener_id_empleado(reintentos=3):
    """
    Obtiene el ID del empleado con validación y reintentos
    
    Args:
        reintentos: Número máximo de reintentos para entrada inválida
        
    Returns:
        int: ID del empleado válido o None si se cancela
    """
    for intento in range(reintentos):
        try:
            entrada = input("ID del empleado a eliminar: ").strip()
            
            if entrada.lower() == 'cancelar':
                return None
                
            if not entrada:
                print("❌ Debes ingresar un ID de empleado")
                if intento < reintentos - 1:
                    print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                    print("💡 Escribe 'cancelar' para salir")
                continue
                
            empno = int(entrada)
            
            if empno <= 0:
                print("❌ El ID del empleado debe ser un número positivo")
                if intento < reintentos - 1:
                    print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                    print("💡 Escribe 'cancelar' para salir")
                continue
                
            return empno
            
        except ValueError:
            print("❌ Error: Debes ingresar un número válido")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                print("💡 Escribe 'cancelar' para salir")
            
    print("❌ Demasiados intentos fallidos.")
    opcion = obtener_opcion_reintento("demasiados intentos fallidos")
    if opcion == 'reintentar':
        return obtener_id_empleado(reintentos)  # Recursión para reiniciar
    else:
        return None

def obtener_opcion_reintento(razon):
    """
    Pregunta al usuario qué hacer después de un error
    
    Args:
        razon: Razón del error para mostrar en el mensaje
        
    Returns:
        str: 'reintentar' o 'cancelar'
    """
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
        elif opcion.lower() == 'cancelar':
            return 'cancelar'
        else:
            print("❌ Opción no válida. Elige 1 o 2")

def obtener_opcion_despues_cancelar():
    """
    Pregunta al usuario qué hacer después de cancelar la confirmación
    
    Returns:
        str: 'salir', 'otro_empleado' o 'confirmar_de_nuevo'
    """
    print("\n¿Qué deseas hacer ahora?")
    print("1. Eliminar otro empleado")
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
        elif opcion.lower() == 'cancelar':
            return 'salir'
        else:
            print("❌ Opción no válida. Elige 1, 2 o 3")

def preguntar_continuar():
    """
    Pregunta si el usuario quiere eliminar otro empleado después de una eliminación exitosa
    
    Returns:
        bool: True si quiere continuar, False si quiere salir
    """
    print("¿Deseas eliminar otro empleado?")
    print("1. Sí, eliminar otro empleado")
    print("2. No, regresar al menú principal")
    
    while True:
        opcion = input("\nElige una opción (1-2): ").strip()
        
        if opcion == '1':
            return True
        elif opcion == '2':
            return False
        elif opcion.lower() == 'cancelar':
            return False
        else:
            print("❌ Opción no válida. Elige 1 o 2")