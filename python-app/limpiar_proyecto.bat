@echo off
echo 🧼 Limpiando entorno del proyecto en Windows...

echo Eliminando entorno virtual...
rmdir /s /q venv 2>nul

echo Eliminando archivos de configuración...
del /f /q .env 2>nul
del /f /q last_session.json 2>nul

echo Eliminando caché de Python...
for /r %%i in (__pycache__) do (
    if exist "%%i" rmdir /s /q "%%i"
)

echo Eliminando archivos .pyc...
del /s /q *.pyc 2>nul

echo.
echo ✅ Proyecto limpio en Windows.
echo.
echo Para configurar de nuevo:
echo 1. python -m venv venv
echo 2. venv\Scripts\activate
echo 3. pip install -r requirements.txt
echo 4. Configurar archivo .env
echo.
pause