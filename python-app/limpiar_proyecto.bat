@echo off
REM limpiar_proyecto.bat
echo 🧹 Limpiando proyecto en Windows...

echo 🗑️ Eliminando entorno virtual...
if exist venv rmdir /s /q venv 2>nul

echo 🧼 Limpiando caché de Python...
for /r %%i in (__pycache__) do (
    if exist "%%i" rmdir /s /q "%%i"
)
del /s /q *.pyc 2>nul

echo 📁 Eliminando archivos temporales...
if exist .env del /f /q .env 2>nul
if exist last_session.json del /f /q last_session.json 2>nul

echo.
echo ✅ Proyecto limpio en Windows.
echo.
echo Para reconstruir:
echo 1. python -m venv venv
echo 2. venv\Scripts\activate
echo 3. pip install -r requirements.txt
echo.
pause