package config

import (
	"os"
)

// Config estructura de configuración de la aplicación
type Config struct {
	MongoURI        string
	MongoDB         string
	MongoCollection string
	Port            string
}

// Load carga la configuración desde variables de entorno
func Load() *Config {
	return &Config{
		MongoURI:        getEnv("MONGO_URI", "mongodb://mongodb:27017"),
		MongoDB:         getEnv("MONGO_DB", "empresa_db"),
		MongoCollection: getEnv("MONGO_COLLECTION", "rh"),
		Port:            getEnv("PORT", "8080"),
	}
}

// getEnv obtiene una variable de entorno con valor por defecto
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}