"""
Manejadores de entrada para actualización de empleados
"""
from shared import constants, input_utils
from services.shared.input_utils import obtener_dato_texto, obtener_dato_numerico

def obtener_nuevo_nombre(nombre_actual):
    """Obtiene el nuevo nombre del empleado"""
    return input_utils.obtener_dato_texto(
        f"Nuevo nombre [{nombre_actual}]: ",
        max_longitud=10,
        mensaje_error="❌ El nombre debe tener máximo 10 caracteres"
    )

def obtener_nuevo_puesto(puesto_actual):
    """Obtiene el nuevo puesto del empleado"""
    while True:
        print(f"\nPuesto actual: {puesto_actual}")
        print("Puestos disponibles:", ', '.join(sorted(constants.PUESTOS_VALIDOS)))
        entrada = input(f"Nuevo puesto [{puesto_actual}] (o 'nuevo' para crear uno): ").strip()
        
        if entrada.lower() == 'cancelar':
            return None
        elif entrada.lower() == 'atras':
            return 'atras'
        elif entrada == '':
            return puesto_actual  # Conservar valor actual
            
        job = entrada.upper()
        
        if job == 'NUEVO' or (job and job not in constants.PUESTOS_VALIDOS):
            print("\n⚠️ Puesto no reconocido. Puedes:")
            print("1. Crear un nuevo puesto")
            print("2. Elegir uno de los disponibles")
            print("3. Conservar el puesto actual")
            print("4. Escribir 'atras' para volver")
            print("5. Escribir 'cancelar' para salir")
            
            opcion = input("\nElige una opción (1-5): ").strip()
            
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
                return puesto_actual
            elif opcion == '4':
                return 'atras'
            elif opcion == '5':
                return None
            else:
                print("❌ Opción no válida")
        elif job in constants.PUESTOS_VALIDOS:
            return job
        else:
            print("❌ Puesto no válido")

def obtener_nuevo_salario(salario_actual):
    """Obtiene el nuevo salario del empleado"""
    return input_utils.obtener_dato_numerico(
        f"Nuevo salario [{salario_actual}]: ",
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
        deptno = input_utils.obtener_dato_numerico(
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
            dname = input_utils.obtener_dato_texto(
                "Nombre del departamento: ",
                mensaje_error="❌ El nombre no puede estar vacío"
            )
            if dname is None: return None
            elif dname == 'atras': continue
            
            loc = input_utils.obtener_dato_texto(
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