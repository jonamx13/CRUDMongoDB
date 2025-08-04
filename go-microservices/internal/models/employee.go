package models

import "go.mongodb.org/mongo-driver/bson/primitive"

// Department representa la información del departamento embebida
type Department struct {
	DeptNo int    `json:"deptno" bson:"deptno"`
	DName  string `json:"dname" bson:"dname"`
	Loc    string `json:"loc" bson:"loc"`
}

// Employee representa un empleado con departamento embebido
type Employee struct {
	ID           primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	EmpNo        int                `json:"empno" bson:"empno"`
	EName        string             `json:"ename" bson:"ename"`
	Job          string             `json:"job" bson:"job"`
	Sal          float64            `json:"sal" bson:"sal"`
	Departamento Department         `json:"departamento" bson:"departamento"`
}

// CreateEmployeeRequest estructura para crear empleado
type CreateEmployeeRequest struct {
	EmpNo        int        `json:"empno" binding:"required"`
	EName        string     `json:"ename" binding:"required"`
	Job          string     `json:"job" binding:"required"`
	Sal          float64    `json:"sal" binding:"required"`
	Departamento Department `json:"departamento" binding:"required"`
}

// UpdateEmployeeRequest estructura para actualizar empleado
type UpdateEmployeeRequest struct {
	EName        *string     `json:"ename,omitempty"`
	Job          *string     `json:"job,omitempty"`
	Sal          *float64    `json:"sal,omitempty"`
	Departamento *Department `json:"departamento,omitempty"`
}

// EmployeeResponse estructura de respuesta API
type EmployeeResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
	Count   *int        `json:"count,omitempty"`
}

// ErrorResponse estructura de respuesta de error
type ErrorResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	Error   string `json:"error,omitempty"`
}