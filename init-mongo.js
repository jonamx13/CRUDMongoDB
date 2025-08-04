// Script de inicialización para MongoDB
// Se ejecuta automáticamente al crear el contenedor

// Conectar a la base de datos empresa_db
db = db.getSiblingDB('empresa_db');

// Crear la colección rh si no existe
db.createCollection('rh');

// Insertar datos de empleados con departamentos embebidos
print('🍃 Insertando datos iniciales en la colección rh...');

db.rh.insertMany([
  {
    "empno": 7369,
    "ename": "SMITH",
    "job": "CLERK",
    "sal": 800,
    "departamento": {
      "deptno": 20,
      "dname": "RESEARCH",
      "loc": "DALLAS"
    }
  },
  {
    "empno": 7499,
    "ename": "ALLEN",
    "job": "SALESMAN",
    "sal": 1600,
    "departamento": {
      "deptno": 30,
      "dname": "SALES",
      "loc": "CHICAGO"
    }
  },
  {
    "empno": 7521,
    "ename": "WARD",
    "job": "SALESMAN",
    "sal": 1250,
    "departamento": {
      "deptno": 30,
      "dname": "SALES",
      "loc": "CHICAGO"
    }
  },
  {
    "empno": 7566,
    "ename": "JONES",
    "job": "MANAGER",
    "sal": 2975,
    "departamento": {
      "deptno": 20,
      "dname": "RESEARCH",
      "loc": "DALLAS"
    }
  },
  {
    "empno": 7654,
    "ename": "MARTIN",
    "job": "SALESMAN",
    "sal": 1250,
    "departamento": {
      "deptno": 30,
      "dname": "SALES",
      "loc": "CHICAGO"
    }
  },
  {
    "empno": 7698,
    "ename": "BLAKE",
    "job": "MANAGER",
    "sal": 2850,
    "departamento": {
      "deptno": 30,
      "dname": "SALES",
      "loc": "CHICAGO"
    }
  },
  {
    "empno": 7782,
    "ename": "CLARK",
    "job": "MANAGER",
    "sal": 2450,
    "departamento": {
      "deptno": 10,
      "dname": "ACCOUNTING",
      "loc": "NEW YORK"
    }
  },
  {
    "empno": 7788,
    "ename": "SCOTT",
    "job": "ANALYST",
    "sal": 3000,
    "departamento": {
      "deptno": 20,
      "dname": "RESEARCH",
      "loc": "DALLAS"
    }
  },
  {
    "empno": 7839,
    "ename": "KING",
    "job": "PRESIDENT",
    "sal": 5000,
    "departamento": {
      "deptno": 10,
      "dname": "ACCOUNTING",
      "loc": "NEW YORK"
    }
  },
  {
    "empno": 7844,
    "ename": "TURNER",
    "job": "SALESMAN",
    "sal": 1500,
    "departamento": {
      "deptno": 30,
      "dname": "SALES",
      "loc": "CHICAGO"
    }
  },
  {
    "empno": 7876,
    "ename": "ADAMS",
    "job": "CLERK",
    "sal": 1100,
    "departamento": {
      "deptno": 20,
      "dname": "RESEARCH",
      "loc": "DALLAS"
    }
  },
  {
    "empno": 7900,
    "ename": "JAMES",
    "job": "CLERK",
    "sal": 950,
    "departamento": {
      "deptno": 30,
      "dname": "SALES",
      "loc": "CHICAGO"
    }
  },
  {
    "empno": 7902,
    "ename": "FORD",
    "job": "ANALYST",
    "sal": 3000,
    "departamento": {
      "deptno": 20,
      "dname": "RESEARCH",
      "loc": "DALLAS"
    }
  },
  {
    "empno": 7934,
    "ename": "MILLER",
    "job": "CLERK",
    "sal": 1300,
    "departamento": {
      "deptno": 10,
      "dname": "ACCOUNTING",
      "loc": "NEW YORK"
    }
  }
]);

// Crear índices para optimizar consultas
print('📊 Creando índices...');
db.rh.createIndex({ "empno": 1 }, { unique: true });
db.rh.createIndex({ "departamento.deptno": 1 });
db.rh.createIndex({ "ename": 1 });
db.rh.createIndex({ "job": 1 });

// Verificar inserción
const count = db.rh.countDocuments();
print(`✅ Datos insertados correctamente. Total de empleados: ${count}`);

print('🎉 Inicialización de MongoDB completada exitosamente!');