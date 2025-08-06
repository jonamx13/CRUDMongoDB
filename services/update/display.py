"""
Funciones de visualización para actualización de empleados
"""

def mostrar_comparacion(empleado, nuevo_nombre, nuevo_job, nuevo_sal, nuevo_departamento):
    """Muestra una comparación entre valores actuales y nuevos"""
    print(f"Nombre: {empleado['ename']} → {nuevo_nombre}")
    print(f"Puesto: {empleado['job']} → {nuevo_job}")
    print(f"Salario: ${empleado['sal']:,.2f} → ${nuevo_sal:,.2f}")
    
    dept_actual = empleado.get('departamento', {})
    dept_actual_str = f"{dept_actual.get('dname', 'N/A')} ({dept_actual.get('loc', 'N/A')})"
    dept_nuevo_str = f"{nuevo_departamento.get('dname', 'N/A')} ({nuevo_departamento.get('loc', 'N/A')})"
    print(f"Departamento: {dept_actual_str} → {dept_nuevo_str}")