"""
Paquete que contiene todos los servicios CRUD
"""
from .create.service import crear_empleado
from .read.service import leer_empleados
from .update.service import actualizar_empleado
from .delete.service import eliminar_empleado
from .search.service import buscar_empleado

# Exportar servicios para fácil acceso
__all__ = [
    'crear_empleado',
    'leer_empleados',
    'actualizar_empleado',
    'eliminar_empleado',
    'buscar_empleado',
]