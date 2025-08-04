package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"go-microservices/internal/config"
	"go-microservices/internal/database"
	"go-microservices/internal/handlers"
	"go-microservices/internal/services"
)

func main() {
	// Cargar configuración
	cfg := config.Load()

	// Conectar a MongoDB
	mongoClient, err := database.Connect(cfg.MongoURI)
	if err != nil {
		log.Fatal("Error conectando a MongoDB:", err)
	}
	defer mongoClient.Disconnect(context.Background())

	// Obtener colección
	collection := mongoClient.Database(cfg.MongoDB).Collection(cfg.MongoCollection)

	// Inicializar servicios
	employeeService := services.NewEmployeeService(collection)

	// Inicializar handlers
	employeeHandler := handlers.NewEmployeeHandler(employeeService)

	// Configurar Gin
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()

	// Middleware de logging
	router.Use(gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		return fmt.Sprintf("🐳 [DOCKER] %s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
			param.ClientIP,
			param.TimeStamp.Format(time.RFC1123),
			param.Method,
			param.Path,
			param.Request.Proto,
			param.StatusCode,
			param.Latency,
			param.Request.UserAgent(),
			param.ErrorMessage,
		)
	}))

	// Middleware de recuperación
	router.Use(gin.Recovery())

	// Middleware CORS
	router.Use(func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")
		
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		
		c.Next()
	})

	// Rutas de salud
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":      "OK",
			"service":     "Go Microservice CRUD MongoDB",
			"environment": "Docker Container",
			"timestamp":   time.Now().Format(time.RFC3339),
		})
	})

	// Rutas de empleados
	v1 := router.Group("/api/v1")
	{
		employees := v1.Group("/employees")
		{
			employees.GET("", employeeHandler.GetAll)
			employees.GET("/:id", employeeHandler.GetByID)
			employees.POST("", employeeHandler.Create)
			employees.PUT("/:id", employeeHandler.Update)
			employees.DELETE("/:id", employeeHandler.Delete)
			employees.GET("/department/:deptno", employeeHandler.GetByDepartment)
		}
	}

	// Rutas legacy para compatibilidad
	router.GET("/employees", employeeHandler.GetAll)
	router.GET("/employees/:id", employeeHandler.GetByID)
	router.POST("/employees", employeeHandler.Create)
	router.PUT("/employees/:id", employeeHandler.Update)
	router.DELETE("/employees/:id", employeeHandler.Delete)
	router.GET("/employees/department/:deptno", employeeHandler.GetByDepartment)

	// Servidor HTTP
	srv := &http.Server{
		Addr:    ":" + cfg.Port,
		Handler: router,
	}

	// Goroutine para iniciar el servidor
	go func() {
		log.Printf("🐳 [DOCKER] Microservicio Go iniciado en puerto %s", cfg.Port)
		log.Printf("🍃 [DOCKER] Conectado a MongoDB: %s/%s", cfg.MongoDB, cfg.MongoCollection)
		log.Printf("🌐 [DOCKER] API disponible en: http://localhost:%s", cfg.Port)
		log.Printf("🔍 [DOCKER] Health check: http://localhost:%s/health", cfg.Port)
		
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Error iniciando servidor: %v", err)
		}
	}()

	// Esperar señal de interrupción
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("🐳 [DOCKER] Cerrando servidor...")

	// Graceful shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Error cerrando servidor:", err)
	}

	log.Println("🐳 [DOCKER] Servidor cerrado correctamente")
}