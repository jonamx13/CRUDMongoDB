"""
Paquete que contiene todos los servicios CRUD
"""
from .create_service import crear_empleado
from .read_service import leer_empleados
from .update_service import actualizar_empleado
from .delete_service import eliminar_empleado
from .search_service import buscar_empleado

# Exportar servicios para fácil acceso
__all__ = [
    'crear_empleado',
    'leer_empleados',
    'actualizar_empleado',
    'eliminar_empleado',
    'buscar_empleado',
]