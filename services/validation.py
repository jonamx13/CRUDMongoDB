"""
Funciones de validación para datos de empleados
"""

def validar_empleado_data(empno: int, ename: str, job: str, sal: float) -> bool:
    """
    Valida los datos básicos de un empleado
    
    Args:
        empno: Número de empleado
        ename: Nombre del empleado
        job: Puesto del empleado
        sal: Salario del empleado
        
    Returns:
        bool: True si los datos son válidos, False de lo contrario
    """
    if empno <= 0:
        print("❌ El número de empleado debe ser positivo")
        return False
    
    if not ename or len(ename.strip()) == 0:
        print("❌ El nombre no puede estar vacío")
        return False
    
    if not job or len(job.strip()) == 0:
        print("❌ El puesto no puede estar vacío")
        return False
    
    if sal < 0:
        print("❌ El salario no puede ser negativo")
        return False
    
    return True