# 📚 CRUD MongoDB - Bases de Datos II

Aplicación CRUD (Create, Read, Update, Delete) para gestión de empleados utilizando MongoDB como base de datos. La aplicación ofrece una interfaz de consola interactiva con menús y validación robusta de datos.

<div align="center" style="background:white; padding:20px; display:inline-block">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg" width="400">
</div>

## 🧾 Créditos
- **Materia:** Bases de Datos II
- **Asesor:** José Saul De Lira Miramontes
- **Alumno:** Jonathan Eduardo Olivas Meixueiro
- **Matricula:** 240694
- **Fecha de entrega:** 07/Agosto/2025

## 💡 Características Principales
- **✅ Multiplataforma:** Funciona en ⊞ Windows, 🐧Linux y 🍎macOS
- ✅ **Dos modos de conexión:** 🍃MongoDB local o con 🐋Docker
- ✅ **Interfaz intuitiva:** Menús interactivos con navegación paso a paso
- ✅ **Validación robusta:** Control de errores y reintentos en todas las operaciones
- ✅ **MongoDB Express:** Acceso a interfaz web para administración de la base de datos
- ✅ **Datos de prueba:** Inserción automática de datos de ejemplo (esquema SCOTT)
- ✅ **Persistencia:** Guarda información de sesión entre ejecuciones
- ✅ **Configuración automática:** Script de setup para preparar el entorno

---

## ⚙️ Pre-requisitos mínimos

### ⊞ Windows
- 📟PowerShell 5.1+
- 🐍Python 3.10.x
- 🍃MongoDB (última versión)
- 🐋(Opcional) Docker Desktop 4.12+

### 🍎macOS/ 🐧Linux:
- 📟Terminal
- 🐍Python 3.10.x
- 🍃MongoDB (última versión)
- 🐋(Opcional) Docker Engine 20.10+
---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
   ```bash
   git clone https://github.com/tu-usuario/CRUDMongoDB.git
cd CRUDMongoDB
   ```
### 2. Configuración inicial
Correremos el script de configuración según nuestro sistema operativo

- ⊞ Windows
   ```bash
    # Ejecutar como administrador para mejores permisos
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

    # Script de configuración
    .\start_app.ps1
    ```

- 🍎macOS/ 🐧Linux:
    ```bash
    # Dar permisos de ejecución
    chmod +x *.sh

    # Script de configuración
    ./start_app.sh
    ```

Seguiremos la configuración guiada dando `Enter` en nuestra terminal por cada paso.

---


## 🐋 Uso con Docker
Si optaste por usar Docker, la aplicación incluye:
- Contenedor de MongoDB
- Contenedor de MongoDB Express (interfaz web)

Acceder a MongoDB Express:
*    Abre tu navegador en [http://localhost:8081](http://localhost:8081)
*   Usuario: `admin`
*   Contraseña: admin123

---
## 📊 Funcionalidades
El menú de la aplicación nos mostrará las siguientes características.

```
=======================================================
🌟 CRUD EMPLEADOS - MONGODB
   Sistema: # nombre completo del sistema que estemos utilizando (SO / Python)
=======================================================

💻Sistema operativo: # nombre corto de nuestro sistema operativo
🐍Python: # versión de Python que estamos usando
🏗Arquitectura: # La arquitectura de nuestro CPU
💾Plataforma: # nombre completo de nuestro sistema operativo
📅Fecha actual: # fecha y hora en que iniciamos la aplicación


👋Bienvenido por primera vez a la aplicación MongoDB CRUD.
ℹ️Usa la opción 6 para insertar datos de prueba.

📋 MENÚ CRUD EMPLEADOS - MONGODB
========================================
1. 👀 Ver todos los empleados
2. ➕ Crear nuevo empleado
3. ✏️ Actualizar empleado
4. ❌ Eliminar empleado
5. 🔍 Buscar empleado por ID
6. 🧪 Insertar datos de prueba
7. 🧹 Limpiar base de datos
0. 🚪 Salir
========================================

Seleccione una opción:
```

**Nota:** para volver a abrir nuestra aplicación después de salir, ejecutaremos los siguientes comandos:

- ⊞ Windows
    ```bash
    python .\main.py
    ```

-   🍎macOS/ 🐧Linux:
    ```bash
    python3 ./main.py
    ```

---
## 🧼 Limpieza de Proyecto:
Cúando hayamos finalizado y queramos volver al estado inicial de nuestra aplicación, haremos el proceso de limpieza.

### 1. Limpiar archivos temporales

- ⊞ Windows
    ```bash
    .\limpiar_proyecto.bat
    ```

-   🍎macOS/ 🐧Linux:
    ```bash
    ./limpiar_proyecto.sh
    ```
Esto eliminará los siguiente archivos:


    # Archivos de caché que
    aceleran la importación
    de módulos de Python.
    📁__pycache__

    # Entorno virtual de Python
    el cuál importa y aisla las
    librerías necesarias para
    ejecutar nuestra aplicación.
    📁venv

    # Archivo de variables
    de entorno para establecer
    la conexión con nuestra
    base de datos.
    💾.env
    ```

Así mismo, nos dará instrucciones para reinstalar nuestra aplicación utilizando la misma base de datos que ya habíamos creado.
```
Para reconstruir:
1. `python -m venv venv`
2. `venv\Scripts\activate ` o `venv/bin/activate`
3. `pip install -r requirements.txt`
```

### 2. Eliminar y desactivar contenedores o servicios

- Solo restará eliminar por completo nuestros contenedores de Docker:

```
# Este comando funciona con todas las terminales
docker compose down -v
```

- Si corrimos la aplicación con MongoDB instalado localmente, detendremos nuestro servicio:

```
# Detener mongoDB en Windows
net stop MongoDB

# Detener mondoDB en Unix-like (Linux, macOS, WSL)
sudo systemctl stop mongod

# Detener en macOS si usamos brew
brew services stop mongodb-community	
```

## 📁 Estructura completa de archivos:

Aquí mostramos la estructura de archivos que conforman la funcionalidad CRUD abordados de forma modular como “servicio”.
### 🥇 Principal

```
CRUDMongoDB/                     # Directorio raíz del proyecto
│
├── db/                          # Directorio con lo relacionado a la base de datos
│   ├── mongo_config.py          # Configura nuestra conexión a MongoDB
│   └── mongo_utils.py           # Herramientas para trabajar con la DB
│
├── models/                      # Define cómo se construyen y son nuestros documentos/datos
│   └── employee.py              # Modelo de Empleado y Departamento
│
├── services/                    # La lógica CRUD modularizada en paquetes
│   ├── create/                  # Lógica para crear nuevos empleados
│   ├── read/                    # Lógica para leer/ver empleados
│   ├── update/                  # Lógica para actualizar empleados
│   ├── delete/                  # Lógica para eliminar empleados
│   ├── search/                  # Lógica para buscar empleados
│   ├── shared/                  # Código y funciones que comparten todos los servicios
│   └── __init__.py              # Exporta todos los servicios CRUD para accederlos en la aplicación
│
├── ui/                          # Definición de la interfaz de usuario en CLI
│   └── menus.py                 # Menús y pantallas de la aplicación
│
├── .gitignore                   # Archivos que usamos en entorno local y no deben llegar a git
├── activate_env.sh              # Script para activar el entorno virtual (venv) de Python en Linux/macOS
├── docker-compose.yml           # Configuración para usar MongoDB en contenedores
├── init-mongo.js                # Datos iniciales proveidos por el maestro
├── limpiar_proyecto.bat         # Limpiar proyecto en Windows (caché, entorno virtual, .env, etc.)
├── limpiar_proyecto.sh          # Limpiar proyecto en Linux/macOS (caché, entorno virtual, .env, etc.)
├── main.py                      # Punto de entrada de la aplicación
├── README.md                    # Documentación del proyecto en Markdown para Github
├── requirements.txt             # Lista de dependencias de Python necesarias para el proyecto
├── session.py                   # Guarda información entre usos de la aplicación
├── setup.py                     # Configuración del proyecto Python (venv, .env, conexión a MongoDB)
├── start_app.ps1                # Inicia y configura toda la app Powershell - Windows (Python/MongoDB/Docker)
└── start_app.sh                 # Inicia y configura toda la app Terminal - Linux/macOS (Python/MongoDB/Docker)
```

### 🛠️ Directorio de servicios (Lógica CRUD)

- **CREATE**
```
CRUDMongoDB/
└── services/
    └── create/
        ├── __init__.py        # Vacío solo para indicar que se trata de un paquete
        ├── input_handlers.py  # Maneja lo que el usuario escribe
        └── service.py         # Lógica para guardar en la DB
```

- **READ**
```
CRUDMongoDB/
└── services/
    └── read/
        ├── __init__.py        # Vacío solo para indicar que se trata de un paquete
        └── service.py         # Lógica para mostrar empleados
```

- **UPDATE**
```
CRUDMongoDB/
└── services/
    └── update/
        ├── __init__.py        # Vacío solo para indicar que se trata de un paquete
        ├── display.py         # Muestra los cambios
        ├── input_handlers.py  # Maneja las modificaciones
        └── service.py         # Lógica para actualizar
```

- **DELETE**
```
CRUDMongoDB/
└── services/
    └── update/
        ├── __init__.py        # Vacío solo para indicar que se trata de un paquete
        ├── flow_control.py    # Controla el proceso de eliminación
        └── service.py         # Lógica para borrar
```
---

Al igual añadimos funcionalides extra para mantener orden de nuestros archivos, así como la accesibilidad de nuestras funcionalidades a través de una declaración de paquetes que nos permiten acceder a ellas desde el directorio raíz.


- **SEARCH**
```
CRUDMongoDB/
└── services/
    └── search/
        ├── __init__.py        # Vacío solo para indicar que se trata de un paquete
        ├── by_field.py        # Búsqueda por diferentes criterios
        ├── display.py         # Menú principal y limpieza de consola
        └── service.py         # Lógica de búsqueda
```

- **SHARED**
```
CRUDMongoDB/
└── services/
    └── shared/
        ├── __init__.py        # Exporta funciones para exponerlas a todos los servicios
        ├── constants.py       # Datos fijos (como los puestos válidos)
        ├── input_utils.py     # Funciones para leer lo que escribe el usuario
        └── validation.py      # Validación de datos
```
---

## 🧾 Créditos
- **Materia:** Bases de Datos II
- **Asesor:** José Saul De Lira Miramontes
- **Alumno:** Jonathan Eduardo Olivas Meixueiro
- **Matricula:** 240694
- **Fecha de entrega:** 07/Agosto/2025

