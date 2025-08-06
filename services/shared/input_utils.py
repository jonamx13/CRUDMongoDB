"""
Utilidades para entrada de datos
"""
import logging

logger = logging.getLogger(__name__)

def obtener_dato_numerico(
    prompt: str,
    tipo=int,
    validacion=None,
    mensaje_error: str = "❌ Valor inválido",
    reintentos: int = 3
):
    """
    Obtiene un dato numérico del usuario con validación y reintentos
    
    Args:
        prompt: Mensaje para mostrar al usuario
        tipo: Tipo numérico (int o float)
        validacion: Función de validación adicional
        mensaje_error: Mensaje a mostrar cuando falla la validación
        reintentos: Número máximo de reintentos
        
    Returns:
        Número válido, 'atras' o None si se cancela
    """
    for intento in range(reintentos):
        try:
            valor = input(prompt).strip()
            if valor.lower() == 'cancelar':
                return None
            elif valor.lower() == 'atras':
                return 'atras'
                
            numero = tipo(valor)
            
            if validacion and not validacion(numero):
                print(mensaje_error)
                continue
                
            return numero
            
        except ValueError:
            print(mensaje_error)
            
        if intento < reintentos - 1:
            print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
            print("💡 Escribe 'atras' para volver o 'cancelar' para salir")
    
    print("❌ Demasiados intentos fallidos. Operación cancelada.")
    return None

def obtener_dato_texto(
    prompt: str,
    max_longitud: int = None,
    mensaje_error: str = "❌ Texto inválido",
    reintentos: int = 3
):
    """
    Obtiene un dato de texto del usuario con validación
    
    Args:
        prompt: Mensaje para mostrar al usuario
        max_longitud: Longitud máxima permitida (opcional)
        mensaje_error: Mensaje a mostrar cuando falla la validación
        reintentos: Número máximo de reintentos
        
    Returns:
        Texto válido (en mayúsculas), 'atras' o None si se cancela
    """
    for intento in range(reintentos):
        valor = input(prompt).strip()
        if valor.lower() == 'cancelar':
            return None
        elif valor.lower() == 'atras':
            return 'atras'
            
        if not valor:
            print(mensaje_error)
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                print("💡 Escribe 'atras' para volver o 'cancelar' para salir")
            continue
            
        if max_longitud and len(valor) > max_longitud:
            print(f"❌ El texto no puede exceder {max_longitud} caracteres")
            if intento < reintentos - 1:
                print(f"🔄 Inténtalo de nuevo ({intento + 1}/{reintentos})")
                print("💡 Escribe 'atras' para volver o 'cancelar' para salir")
            continue
            
        return valor.upper()
    
    print("❌ Demasiados intentos fallidos. Operación cancelada.")
    return None