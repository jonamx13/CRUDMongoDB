package handlers

import (
	"context"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"go-microservices/internal/models"
	"go-microservices/internal/services"
)

// EmployeeHandler maneja las peticiones HTTP de empleados
type EmployeeHandler struct {
	service *services.EmployeeService
}

// NewEmployeeHandler crea una nueva instancia del handler
func NewEmployeeHandler(service *services.EmployeeService) *EmployeeHandler {
	return &EmployeeHandler{
		service: service,
	}
}

// GetAll maneja GET /employees
func (h *EmployeeHandler) GetAll(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	employees, err := h.service.GetAll(ctx)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error obteniendo empleados",
			Error:   err.Error(),
		})
		return
	}

	count := len(employees)
	c.JSON(http.StatusOK, models.EmployeeResponse{
		Success: true,
		Message: "Empleados obtenidos correctamente",
		Data:    employees,
		Count:   &count,
	})
}

// GetByID maneja GET /employees/:id
func (h *EmployeeHandler) GetByID(c *gin.Context) {
	empnoStr := c.Param("id")
	empno, err := strconv.Atoi(empnoStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{
			Success: false,
			Message: "ID de empleado inválido",
			Error:   "El ID debe ser un número entero",
		})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	employee, err := h.service.GetByID(ctx, empno)
	if err != nil {
		if err.Error() == "empleado no encontrado" {
			c.JSON(http.StatusNotFound, models.ErrorResponse{
				Success: false,
				Message: "Empleado no encontrado",
				Error:   err.Error(),
			})
			return
		}
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error obteniendo empleado",
			Error:   err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.EmployeeResponse{
		Success: true,
		Message: "Empleado obtenido correctamente",
		Data:    employee,
	})
}

// Create maneja POST /employees
func (h *EmployeeHandler) Create(c *gin.Context) {
	var req models.CreateEmployeeRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{
			Success: false,
			Message: "Datos inválidos",
			Error:   err.Error(),
		})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	employee, err := h.service.Create(ctx, req)
	if err != nil {
		if err.Error() == "ya existe un empleado con ese número" {
			c.JSON(http.StatusConflict, models.ErrorResponse{
				Success: false,
				Message: "Empleado ya existe",
				Error:   err.Error(),
			})
			return
		}
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error creando empleado",
			Error:   err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, models.EmployeeResponse{
		Success: true,
		Message: "Empleado creado correctamente",
		Data:    employee,
	})
}

// Update maneja PUT /employees/:id
func (h *EmployeeHandler) Update(c *gin.Context) {
	empnoStr := c.Param("id")
	empno, err := strconv.Atoi(empnoStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{
			Success: false,
			Message: "ID de empleado inválido",
			Error:   "El ID debe ser un número entero",
		})
		return
	}

	var req models.UpdateEmployeeRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{
			Success: false,
			Message: "Datos inválidos",
			Error:   err.Error(),
		})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	employee, err := h.service.Update(ctx, empno, req)
	if err != nil {
		if err.Error() == "empleado no encontrado" {
			c.JSON(http.StatusNotFound, models.ErrorResponse{
				Success: false,
				Message: "Empleado no encontrado",
				Error:   err.Error(),
			})
			return
		}
		if err.Error() == "no hay campos para actualizar" {
			c.JSON(http.StatusBadRequest, models.ErrorResponse{
				Success: false,
				Message: "No hay campos para actualizar",
				Error:   err.Error(),
			})
			return
		}
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error actualizando empleado",
			Error:   err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.EmployeeResponse{
		Success: true,
		Message: "Empleado actualizado correctamente",
		Data:    employee,
	})
}

// Delete maneja DELETE /employees/:id
func (h *EmployeeHandler) Delete(c *gin.Context) {
	empnoStr := c.Param("id")
	empno, err := strconv.Atoi(empnoStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{
			Success: false,
			Message: "ID de empleado inválido",
			Error:   "El ID debe ser un número entero",
		})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	err = h.service.Delete(ctx, empno)
	if err != nil {
		if err.Error() == "empleado no encontrado" {
			c.JSON(http.StatusNotFound, models.ErrorResponse{
				Success: false,
				Message: "Empleado no encontrado",
				Error:   err.Error(),
			})
			return
		}
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error eliminando empleado",
			Error:   err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.EmployeeResponse{
		Success: true,
		Message: "Empleado eliminado correctamente",
	})
}

// GetByDepartment maneja GET /employees/department/:deptno
func (h *EmployeeHandler) GetByDepartment(c *gin.Context) {
	deptnoStr := c.Param("deptno")
	deptno, err := strconv.Atoi(deptnoStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{
			Success: false,
			Message: "Número de departamento inválido",
			Error:   "El número de departamento debe ser un entero",
		})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	employees, err := h.service.GetByDepartment(ctx, deptno)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error obteniendo empleados por departamento",
			Error:   err.Error(),
		})
		return
	}

	count := len(employees)
	c.JSON(http.StatusOK, models.EmployeeResponse{
		Success: true,
		Message: "Empleados del departamento obtenidos correctamente",
		Data:    employees,
		Count:   &count,
	})
}

// GetStats maneja GET /employees/stats (ruta adicional)
func (h *EmployeeHandler) GetStats(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	stats, err := h.service.GetStats(ctx)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{
			Success: false,
			Message: "Error obteniendo estadísticas",
			Error:   err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.EmployeeResponse{
		Success: true,
		Message: "Estadísticas obtenidas correctamente",
		Data:    stats,
	})
}