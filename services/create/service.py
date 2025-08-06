"""
Servicios para crear nuevos empleados
"""
import logging
from db.mongo_config import get_collection
from pymongo.errors import DuplicateKeyError
from .input_handlers import (
    obtener_empno,
    obtener_nombre,
    obtener_puesto,
    obtener_salario,
    obtener_departamento
)

logger = logging.getLogger(__name__)

def crear_empleado():
    """
    Crea un nuevo empleado en la base de datos con validación robusta
    
    Returns:
        None: Interacción por consola con manejo de errores mejorado
    """
    try:
        collection = get_collection()
        if collection is None:
            print("❌ No se pudo conectar a la base de datos")
            return

        print("\n🆕 Crear nuevo empleado")
        print("💡 Puedes escribir 'cancelar' en cualquier momento para salir")
        print("💡 Para volver al paso anterior escribe 'atras'\n")
        
        # Variables para almacenar los datos
        empno = None
        ename = None
        job = None
        sal = None
        departamento = None
        
        # Paso actual (0=empno, 1=ename, 2=job, 3=sal, 4=departamento)
        paso_actual = 0
        
        while True:
            if paso_actual == 0:  # Número de empleado
                resultado = obtener_empno()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # No hay pasos anteriores
                    print("ℹ️ No hay pasos anteriores. Estás en el primer campo.")
                    continue
                else:
                    empno = resultado
                    paso_actual = 1
                    
            elif paso_actual == 1:  # Nombre
                resultado = obtener_nombre()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a empno
                    paso_actual = 0
                    continue
                else:
                    ename = resultado
                    paso_actual = 2
                    
            elif paso_actual == 2:  # Puesto
                resultado = obtener_puesto()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a nombre
                    paso_actual = 1
                    continue
                else:
                    job = resultado
                    paso_actual = 3
                    
            elif paso_actual == 3:  # Salario
                resultado = obtener_salario()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a puesto
                    paso_actual = 2
                    continue
                else:
                    sal = resultado
                    paso_actual = 4
                    
            elif paso_actual == 4:  # Departamento
                resultado = obtener_departamento()
                if resultado is None:  # Cancelar
                    return
                elif resultado == 'atras':  # Volver a salario
                    paso_actual = 3
                    continue
                else:
                    departamento = resultado
                    paso_actual = 5  # Ir a confirmación
                    
            elif paso_actual == 5:  # Confirmación
                # Mostrar resumen
                print("\n📝 Resumen del nuevo empleado:")
                print(f"ID: {empno}")
                print(f"Nombre: {ename}")
                print(f"Puesto: {job}")
                print(f"Salario: ${sal:,.2f}")
                print(f"Departamento: {departamento['dname']} ({departamento['loc']})")
                
                confirmacion = input("\n¿Confirmar creación? (S/N/atras): ").strip().upper()
                if confirmacion == 'ATRAS':
                    paso_actual = 4  # Volver a departamento
                    continue
                elif confirmacion == 'S':
                    # Crear documento e insertar
                    nuevo_empleado = {
                        "empno": empno,
                        "ename": ename,
                        "job": job,
                        "sal": sal,
                        "departamento": departamento
                    }
                    
                    result = collection.insert_one(nuevo_empleado)
                    print(f"\n✅ Empleado creado exitosamente con ID: {result.inserted_id}")
                    return
                elif confirmacion == 'N':
                    print("❌ Creación cancelada por el usuario")
                    return
                elif confirmacion.lower() == 'cancelar':
                    print("❌ Creación cancelada por el usuario")
                    return
                else:
                    print("❌ Opción no válida. Elige S (Sí), N (No) o 'atras'")
                    continue
        
    except DuplicateKeyError:
        print("❌ Error: Número de empleado duplicado (aunque se validó previamente).")
    except Exception as e:
        logger.error(f"Error inesperado al crear empleado: {e}")
        print("❌ Error inesperado al crear empleado:", str(e))