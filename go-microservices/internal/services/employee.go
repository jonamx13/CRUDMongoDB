package services

import (
	"context"
	"errors"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"go-microservices/internal/models"
)

// EmployeeService maneja la lógica de negocio de empleados
type EmployeeService struct {
	collection *mongo.Collection
}

// NewEmployeeService crea una nueva instancia del servicio
func NewEmployeeService(collection *mongo.Collection) *EmployeeService {
	return &EmployeeService{
		collection: collection,
	}
}

// GetAll obtiene todos los empleados
func (s *EmployeeService) GetAll(ctx context.Context) ([]models.Employee, error) {
	opts := options.Find().SetSort(bson.D{{Key: "empno", Value: 1}})
	cursor, err := s.collection.Find(ctx, bson.M{}, opts)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var employees []models.Employee
	if err = cursor.All(ctx, &employees); err != nil {
		return nil, err
	}

	return employees, nil
}

// GetByID obtiene un empleado por su ID
func (s *EmployeeService) GetByID(ctx context.Context, empno int) (*models.Employee, error) {
	var employee models.Employee
	err := s.collection.FindOne(ctx, bson.M{"empno": empno}).Decode(&employee)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, errors.New("empleado no encontrado")
		}
		return nil, err
	}

	return &employee, nil
}

// Create crea un nuevo empleado
func (s *EmployeeService) Create(ctx context.Context, req models.CreateEmployeeRequest) (*models.Employee, error) {
	// Verificar si el empleado ya existe
	count, err := s.collection.CountDocuments(ctx, bson.M{"empno": req.EmpNo})
	if err != nil {
		return nil, err
	}
	if count > 0 {
		return nil, errors.New("ya existe un empleado con ese número")
	}

	employee := models.Employee{
		EmpNo:        req.EmpNo,
		EName:        req.EName,
		Job:          req.Job,
		Sal:          req.Sal,
		Departamento: req.Departamento,
	}

	result, err := s.collection.InsertOne(ctx, employee)
	if err != nil {
		return nil, err
	}

	employee.ID = result.InsertedID.(primitive.ObjectID)
	return &employee, nil
}

// Update actualiza un empleado existente
func (s *EmployeeService) Update(ctx context.Context, empno int, req models.UpdateEmployeeRequest) (*models.Employee, error) {
	// Verificar si el empleado existe
	_, err := s.GetByID(ctx, empno)
	if err != nil {
		return nil, err
	}

	// Construir el documento de actualización
	updateDoc := bson.M{}
	if req.EName != nil {
		updateDoc["ename"] = *req.EName
	}
	if req.Job != nil {
		updateDoc["job"] = *req.Job
	}
	if req.Sal != nil {
		updateDoc["sal"] = *req.Sal
	}
	if req.Departamento != nil {
		updateDoc["departamento"] = *req.Departamento
	}

	if len(updateDoc) == 0 {
		return nil, errors.New("no hay campos para actualizar")
	}

	// Actualizar el documento
	_, err = s.collection.UpdateOne(
		ctx,
		bson.M{"empno": empno},
		bson.M{"$set": updateDoc},
	)
	if err != nil {
		return nil, err
	}

	// Obtener el empleado actualizado
	return s.GetByID(ctx, empno)
}

// Delete elimina un empleado
func (s *EmployeeService) Delete(ctx context.Context, empno int) error {
	// Verificar si el empleado existe
	_, err := s.GetByID(ctx, empno)
	if err != nil {
		return err
	}

	result, err := s.collection.DeleteOne(ctx, bson.M{"empno": empno})
	if err != nil {
		return err
	}

	if result.DeletedCount == 0 {
		return errors.New("no se pudo eliminar el empleado")
	}

	return nil
}

// GetByDepartment obtiene empleados por departamento
func (s *EmployeeService) GetByDepartment(ctx context.Context, deptno int) ([]models.Employee, error) {
	opts := options.Find().SetSort(bson.D{{Key: "empno", Value: 1}})
	cursor, err := s.collection.Find(ctx, bson.M{"departamento.deptno": deptno}, opts)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var employees []models.Employee
	if err = cursor.All(ctx, &employees); err != nil {
		return nil, err
	}

	return employees, nil
}

// GetStats obtiene estadísticas de empleados
func (s *EmployeeService) GetStats(ctx context.Context) (map[string]interface{}, error) {
	pipeline := []bson.M{
		{
			"$group": bson.M{
				"_id": "$departamento.dname",
				"count": bson.M{"$sum": 1},
				"avgSalary": bson.M{"$avg": "$sal"},
				"totalSalary": bson.M{"$sum": "$sal"},
			},
		},
		{
			"$sort": bson.M{"_id": 1},
		},
	}

	cursor, err := s.collection.Aggregate(ctx, pipeline)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var results []bson.M
	if err = cursor.All(ctx, &results); err != nil {
		return nil, err
	}

	// Contar total de empleados
	total, err := s.collection.CountDocuments(ctx, bson.M{})
	if err != nil {
		return nil, err
	}

	stats := map[string]interface{}{
		"totalEmployees": total,
		"byDepartment":   results,
		"timestamp":      time.Now().Format(time.RFC3339),
	}

	return stats, nil
}