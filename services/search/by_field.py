"""
Búsqueda de empleados por diferentes campos
"""
from services.shared.input_utils import obtener_dato_texto, obtener_dato_numerico
from db.mongo_config import get_collection
from .display import mostrar_detalles_empleado, mostrar_lista_empleados, manejar_despues_resultado

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