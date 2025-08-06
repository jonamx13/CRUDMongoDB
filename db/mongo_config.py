"""
Configuración y conexión a MongoDB usando el patrón Singleton
Maneja conexiones persistentes con timeouts configurados
"""

import os
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import logging
import sys



# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path, encoding='utf-8')

# Intentar cargar .env con diferentes codificaciones
try:
    # Primero intentar con UTF-8
    load_dotenv(find_dotenv(), encoding='utf-8')
except UnicodeDecodeError:
    try:
        # Si falla, intentar con Latin-1 (compatible con español)
        logger.warning("⚠️ Error con UTF-8, intentando Latin-1")
        load_dotenv(find_dotenv(), encoding='latin-1')
    except Exception as e:
        logger.error(f"❌ Error fatal al cargar .env: {e}")
        sys.exit(1)
except Exception as e:
    logger.error(f"❌ Error al cargar .env: {e}")
    sys.exit(1)

class MongoDBConnection:
    """
    Clase Singleton para gestionar la conexión a MongoDB
    Garantiza una única instancia de conexión en toda la aplicación
    """
    _instance = None
    _client = None
    
    def __new__(cls):
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """
        Obtiene la conexión a MongoDB (la crea si no existe)
        
        Returns:
            MongoClient: Instancia del cliente de MongoDB
        """
        if self._client is None:
            try:
                # Obtener URI de conexión desde variables de entorno
                mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
                
                # Crear conexión con timeouts configurados
                self._client = MongoClient(
                    mongo_uri,
                    serverSelectionTimeoutMS=5000,  # Timeout para selección de servidor
                    connectTimeoutMS=10000,         # Timeout para conexión inicial
                    socketTimeoutMS=20000           # Timeout para operaciones
                )
                
                # Verificar conexión con un comando simple
                self._client.admin.command('ping')
                logger.info("✅ Conexión a MongoDB exitosa: {mongo_uri}")
                
            except Exception as e:
                logger.error(f"❌ Error al conectar a MongoDB: {e}")
                logger.info("💡 Soluciones posibles:")
                logger.info("1. Verifica que MongoDB esté corriendo")
                logger.info("2. Ejecuta 'docker-compose up -d' si usas Docker")
                logger.info("3. Revisa tu configuración en .env")
                self._client = None
                
        return self._client
    
    def close_connection(self):
        """Cierra la conexión activa a MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("🔌 Conexión a MongoDB cerrada")

# Instancia global de la conexión
db_connection = MongoDBConnection()

def get_connection():
    """
    Obtiene la conexión a MongoDB
    
    Returns:
        MongoClient: Instancia del cliente de MongoDB
    """
    return db_connection.get_connection()

def get_database():
    """
    Obtiene la base de datos configurada
    
    Returns:
        Database: Objeto de base de datos de MongoDB
    """
    try:
        client = get_connection()
        if client is not None:
            # Obtener nombre de BD desde variables de entorno
            db_name = os.getenv("MONGO_DB", "empresa_db")
            return client[db_name]
        return None
    except Exception as e:
        logger.error(f"❌ Error al obtener la base de datos: {e}")
        return None

def get_collection():
    """
    Obtiene la colección configurada
    
    Returns:
        Collection: Objeto de colección de MongoDB
    """
    try:
        db = get_database()
        if db is not None:
            # Obtener nombre de colección desde variables de entorno
            collection_name = os.getenv("MONGO_COLLECTION", "rh")
            return db[collection_name]
        return None
    except Exception as e:
        logger.error(f"❌ Error al obtener la colección: {e}")
        return None

def close_connection():
    """Función pública para cerrar la conexión a MongoDB"""
    db_connection.close_connection()