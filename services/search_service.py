"""
Servicios para buscar empleados - Versión corregida
"""
import logging
from db.mongo_config import get_collection
from ui.menus import limpiar_pantalla

logger = logging.getLogger(__name__)

def buscar_empleado():
    """
    Busca empleados con múltiples criterios y validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        while True:  # Bucle principal para permitir múltiples búsquedas
            limpiar_pantalla()
            print("🔍 Buscar empleados")
            print("💡 Puedes escribir 'cancelar' en cualquier momento para salir\n")
            
            # Mostrar opciones de búsqueda
            print("Opciones de búsqueda:")
            print("1. Buscar por ID")
            print("2. Buscar por nombre")
            print("3. Buscar por puesto")
            print("4. Buscar por departamento")
            
            opcion = input("\nElige una opción (1-4 o 'cancelar'): ").strip()
            
            if opcion.lower() == 'cancelar':
                print("❌ Búsqueda cancelada por el usuario.")
                return
            elif opcion == '1':
                resultado = buscar_por_id(collection)
            elif opcion == '2':
                resultado = buscar_por_nombre(collection)
            elif opcion == '3':
                resultado = buscar_por_puesto(collection)
            elif opcion == '4':
                resultado = buscar_por_departamento(collection)
            else:
                print("❌ Opción no válida. Elige una opción del 1 al 4.")
                input("\nPresiona ENTER para continuar...")
                continue
                
            # Manejar resultado de la búsqueda
            if resultado == 'continuar':
                continue  # Realizar otra búsqueda
            elif resultado == 'salir':
                return
            
    except Exception as e:
        logger.error(f"Error inesperado en búsqueda: {e}")
        print(f"❌ Error inesperado en búsqueda: {str(e)}")

def buscar_por_id(collection):
    """Busca un empleado por su ID"""
    print("\n🆔 Búsqueda por ID")
    
    while True:
        empno = obtener_id_empleado("ID del empleado a buscar: ")
        if empno is None:  # Usuario canceló
            return 'salir'
            
        empleado = collection.find_one({"empno": empno})
        
        if not empleado:
            print(f"❌ No se encontró un empleado con ID: {empno}")
            opcion = obtener_opcion_reintento("empleado no encontrado")
            if opcion == 'cancelar':
                return 'salir'
            elif opcion == 'reintentar':
                continue
        else:
            # Empleado encontrado
            print("\n✅ Empleado encontrado:")
            mostrar_detalles_empleado(empleado)
            return manejar_despues_resultado()

def buscar_por_nombre(collection):
    """Busca empleados por nombre (búsqueda parcial)"""
    print("\n👤 Búsqueda por nombre")
    print("💡 Puedes buscar por nombre completo o parcial")
    
    while True:
        nombre = obtener_dato_texto("Nombre a buscar: ")
        if nombre is None:  # Usuario canceló
            return 'salir'
            
        # Búsqueda case-insensitive y parcial
        empleados = list(collection.find({
            "ename": {"$regex": nombre, "$options": "i"}
        }))
        
        if not empleados:
            print(f"❌ No se encontraron empleados con nombre que contenga: '{nombre}'")
            opcion = obtener_opcion_reintento("no se encontraron empleados")
            if opcion == 'cancelar':
                return 'salir'
            elif opcion == 'reintentar':
                continue
        else:
            # Empleados encontrados
            print(f"\n✅ Se encontraron {len(empleados)} empleado(s):")
            mostrar_lista_empleados(empleados)
            return manejar_despues_resultado()

def buscar_por_puesto(collection):
    """Busca empleados por puesto"""
    print("\n💼 Búsqueda por puesto")
    
    # Mostrar puestos disponibles
    puestos_disponibles = collection.distinct("job")
    if puestos_disponibles:
        print("Puestos disponibles:", ', '.join(sorted(puestos_disponibles)))
    
    while True:
        puesto = obtener_dato_texto("Puesto a buscar: ")
        if puesto is None:  # Usuario canceló
            return 'salir'
            
        empleados = list(collection.find({"job": puesto}))
        
        if not empleados:
            print(f"❌ No se encontraron empleados con puesto: '{puesto}'")
            opcion = obtener_opcion_reintento("no se encontraron empleados")
            if opcion == 'cancelar':
                return 'salir'
            elif opcion == 'reintentar':
                continue
        else:
            # Empleados encontrados
            print(f"\n✅ Se encontraron {len(empleados)} empleado(s) con puesto '{puesto}':")
            mostrar_lista_empleados(empleados)
            return manejar_despues_resultado()

def buscar_por_departamento(collection):
    """Busca empleados por departamento"""
    print("\n🏢 Búsqueda por departamento")
    
    # Mostrar departamentos disponibles
    departamentos = collection.distinct("departamento.dname")
    if departamentos:
        print("Departamentos disponibles:", ', '.join(sorted(departamentos)))
    
    while True:
        dept_nombre = obtener_dato_texto("Nombre del departamento a buscar: ")
        if dept_nombre is None:  # Usuario canceló
            return 'salir'
            
        empleados = list(collection.find({
            "departamento.dname": {"$regex": dept_nombre, "$options": "i"}
        }))
        
        if not empleados:
            print(f"❌ No se encontraron empleados en departamento: '{dept_nombre}'")
            opcion = obtener_opcion_reintento("no se encontraron empleados")
            if opcion == 'cancelar':
                return 'salir'
            elif opcion == 'reintentar':
                continue
        else:
            # Empleados encontrados
            print(f"\n✅ Se encontraron {len(empleados)} empleado(s) en el departamento '{dept_nombre}':")
            mostrar_lista_empleados(empleados)
            return manejar_despues_resultado()



def mostrar_detalles_empleado(empleado: dict):
    """Muestra los detalles completos de un empleado"""
    print("\n📋 Información del empleado:")
    print("-" * 60)
    print(f"ID: {empleado['empno']}")
    print(f"Nombre: {empleado['ename']}")
    print(f"Puesto: {empleado['job']}")
    print(f"Salario: ${empleado['sal']:,.2f}")
    
    dept = empleado.get('departamento', {})
    if dept:
        print(f"Departamento: {dept.get('dname', 'N/A')} (#{dept.get('deptno', 'N/A')})")
        print(f"Ubicación: {dept.get('loc', 'N/A')}")
    else:
        print("Departamento: Sin asignar")
    print("-" * 60)

def mostrar_lista_empleados(empleados: list):
    """Muestra una lista resumida de empleados"""
    print("\n" + "="*90)
    print(f"{'ID':<6} {'NOMBRE':<12} {'PUESTO':<12} {'SALARIO':<12} {'DEPARTAMENTO':<20} {'UBICACIÓN'}")
    print("="*90)
    
    for emp in empleados:
        dept = emp.get('departamento', {})
        dept_name = dept.get('dname', 'N/A')[:19]  # Truncar si es muy largo
        dept_loc = dept.get('loc', 'N/A')
        
        print(f"{emp['empno']:<6} {emp['ename']:<12} {emp['job']:<12} ${emp['sal']:<11,.2f} {dept_name:<20} {dept_loc}")
    
    print("="*90)
    
    # Si hay muchos resultados, ofrecer ver detalles
    if len(empleados) <= 10:
        print(f"\n💡 ¿Deseas ver los detalles de algún empleado específico?")
        ver_detalles = input("Escribe el ID del empleado o presiona ENTER para continuar: ").strip()
        
        if ver_detalles:
            try:
                empno = int(ver_detalles)
                empleado_detalle = next((emp for emp in empleados if emp['empno'] == empno), None)
                if empleado_detalle:
                    mostrar_detalles_empleado(empleado_detalle)
                else:
                    print(f"❌ ID {empno} no está en los resultados mostrados.")
            except ValueError:
                print("❌ ID inválido.")

def manejar_despues_resultado():
    """Maneja las opciones después de mostrar resultados"""
    print("\n¿Qué deseas hacer ahora?")
    print("1. Realizar otra búsqueda")
    print("2. Salir al menú principal")
    
    while True:
        opcion = input("\nElige una opción (1-2): ").strip()
        
        if opcion == '1':
            return 'continuar'
        elif opcion == '2':
            return 'salir'
        elif opcion.lower() == 'cancelar':
            return 'salir'
        else:
            print("❌ Opción no válida. Elige 1 o 2")

def manejar_sin_resultados():
    """Maneja el caso cuando no hay resultados"""
    print("\n¿Qué deseas hacer ahora?")
    print("1. Volver al menú de búsqueda")
    print("2. Salir al menú principal")
    
    while True:
        opcion = input("\nElige una opción (1-2): ").strip()
        
        if opcion == '1':
            return 'continuar'
        elif opcion == '2':
            return 'salir'
        else:
            print("❌ Opción no válida. Elige 1 o 2")

# Funciones auxiliares de validación
def obtener_id_empleado(prompt, reintentos=3):
    """Obtiene el ID del empleado con validación"""
    for intento in range(reintentos):
        try:
            entrada = input(prompt).strip()
            
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
    return None

def obtener_dato_texto(prompt, reintentos=3):
    """Obtiene un dato de texto con validación"""
    for intento in range(reintentos):
        valor = input(prompt).strip()
        if valor.lower() == 'cancelar':
            return None
            
        if not valor:
            print("❌ Este campo no puede estar vacío")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
            continue
            
        return valor.upper()
    
    print("❌ Demasiados intentos fallidos.")
    return None

def obtener_dato_texto_opcional(prompt):
    """Obtiene un dato de texto opcional"""
    valor = input(prompt).strip()
    if valor.lower() == 'cancelar':
        return None
    elif valor.lower() == 'atras':
        return 'atras'
    elif valor == '':
        return ''
    else:
        return valor.upper()

def obtener_dato_numerico_opcional(prompt, tipo=int):
    """Obtiene un dato numérico opcional"""
    valor = input(prompt).strip()
    if valor.lower() == 'cancelar':
        return None
    elif valor.lower() == 'atras':
        return 'atras'
    elif valor == '':
        return None  # Sin criterio numérico
    else:
        try:
            return tipo(valor)
        except ValueError:
            print("❌ Debe ser un número válido")
            return obtener_dato_numerico_opcional(prompt, tipo)

def obtener_opcion_reintento(razon):
    """Pregunta al usuario qué hacer después de un error"""
    print(f"\n⚠️ No se pudo proceder debido a: {razon}")
    print("¿Qué deseas hacer?")
    print("1. Intentar de nuevo")
    print("2. Cancelar búsqueda")
    
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