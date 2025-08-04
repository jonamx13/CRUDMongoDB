#!/bin/bash

echo "🐍 Activando entorno virtual..."

# Detectar el sistema operativo
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "💻 Sistema detectado: Windows (Git Bash)"
    winpty venv/Scripts/activate.bat
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "💻 Sistema detectado: Linux"
    source venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "💻 Sistema detectado: macOS"
    source venv/bin/activate
else
    echo "⚠️ Sistema operativo no soportado automáticamente."
    echo "Activa manualmente el entorno virtual:"
    echo "  Windows: venv\\Scripts\\activate"
    echo "  Linux/macOS: source venv/bin/activate"
fi

echo "✅ Entorno virtual activado"
echo "📦 Para instalar dependencias: pip install -r requirements.txt"