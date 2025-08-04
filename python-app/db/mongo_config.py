import os
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class MongoDBConnection:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """
        Obtiene conexión singleton a MongoDB
        """
        if self._client is None:
            try:
                mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
                self._client = MongoClient(
                    mongo_uri,
                    serverSelectionTimeoutMS=5000,  # Timeout de 5 segundos
                    connectTimeoutMS=10000,         # Timeout de conexión
                    socketTimeoutMS=20000           # Timeout de socket
                )
                
                # Verificar conexión
                self._client.admin.command('ping')
                logger.info("✅ Conexión a MongoDB exitosa")
                
            except Exception as e:
                logger.error(f"❌ Error al conectar a MongoDB: {e}")
                self._client = None
                
        return self._client
    
    def close_connection(self):
        """
        Cierra la conexión a MongoDB
        """
        if self._client:
            self._client.close()
            self._client = None
            logger.info("🔌 Conexión a MongoDB cerrada")

# Instancia global
db_connection = MongoDBConnection()

def get_connection():
    return db_connection.get_connection()

def get_database():
    try:
        client = get_connection()
        if client is not None:  # Usar "is not None"
            db_name = os.getenv("MONGO_DB", "empresa_db")
            return client[db_name]
        return None
    except Exception as e:
        logger.error(f"❌ Error al obtener la base de datos: {e}")
        return None

def get_collection():
    try:
        db = get_database()
        if db is not None:  # Usar "is not None"
            collection_name = os.getenv("MONGO_COLLECTION", "rh")
            return db[collection_name]
        return None
    except Exception as e:
        logger.error(f"❌ Error al obtener la colección: {e}")
        return None

def close_connection():
    """
    Función pública para cerrar conexión
    """
    db_connection.close_connection()