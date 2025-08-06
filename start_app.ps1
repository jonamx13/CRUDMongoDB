# start_app.ps1
# Script de inicio para aplicación MongoDB CRUD - Compatible con PowerShell

# Configurar codificación para caracteres especiales
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [Console]::OutputEncoding

# Limpiar pantalla
Clear-Host

# Mostrar banner
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "🚀 INICIANDO APLICACIÓN MONGODB CRUD" -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Cyan

# Verificar Docker
Write-Host "Verificando estado de MongoDB en Docker..." -ForegroundColor Yellow

$dockerStatus = docker ps --format "table {{.Names}}" 2>$null | Select-String "empresa_mongodb"

if ($dockerStatus) {
    Write-Host "✅ MongoDB en Docker está corriendo" -ForegroundColor Green
}
else {
    Write-Host "⚠️ MongoDB en Docker NO está corriendo" -ForegroundColor Red
    $iniciarDocker = Read-Host "¿Deseas iniciarlo ahora? (s/n)"
    
    if ($iniciarDocker -eq "s" -or $iniciarDocker -eq "S") {
        Write-Host "Iniciando Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d
        Write-Host "Esperando 5 segundos para que MongoDB inicie..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

# Verificar entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "⚠️ No se encontró entorno virtual" -ForegroundColor Red
    $crearVenv = Read-Host "¿Deseas crearlo y instalar dependencias? (s/n)"
    
    if ($crearVenv -eq "s" -or $crearVenv -eq "S") {
        Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
        python -m venv venv
        
        Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
        & ".\venv\Scripts\Activate.ps1"
        
        Write-Host "Instalando dependencias..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
}
else {
    Write-Host "✅ Entorno virtual encontrado. Activando..." -ForegroundColor Green
    & ".\venv\Scripts\Activate.ps1"
}

# Verificar archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️ No se encontró archivo .env" -ForegroundColor Red
    $ejecutarSetup = Read-Host "¿Deseas ejecutar el script de configuración? (s/n)"
    
    if ($ejecutarSetup -eq "s" -or $ejecutarSetup -eq "S") {
        Write-Host "Ejecutando script de configuración..." -ForegroundColor Yellow
        python setup.py
    }
}
else {
    Write-Host "✅ Archivo .env encontrado" -ForegroundColor Green
}

# Iniciar aplicación
Write-Host ""
Write-Host "▶️ Iniciando la aplicación..." -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Cyan

try {
    python main.py
}
catch {
    Write-Host "❌ Error al iniciar la aplicación: $($_.Exception.Message)" -ForegroundColor Red
}

# Pausa al final para ver mensajes
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Yellow
Read-Host