#!/bin/bash

echo "🐍 Activando entorno virtual..."

# Detectar sistema operativo
case "$OSTYPE" in
  msys*|win32) 
    echo "💻 Sistema: Windows (Git Bash)"
    winpty venv/Scripts/activate.bat
    ;;
  linux-gnu*)
    echo "💻 Sistema: Linux"
    source venv/bin/activate
    ;;
  darwin*)
    echo "💻 Sistema: macOS"
    source venv/bin/activate
    ;;
  *)
    echo "⚠️ Sistema no soportado: $OSTYPE"
    echo "Activa manualmente el entorno virtual:"
    echo "  Windows: venv\\Scripts\\activate"
    echo "  Linux/macOS: source venv/bin/activate"
    ;;
esac

echo "✅ Entorno virtual activado"
echo "📦 Para instalar dependencias: pip install -r requirements.txt"