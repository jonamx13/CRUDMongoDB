"""
Visualización de resultados de búsqueda
"""

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