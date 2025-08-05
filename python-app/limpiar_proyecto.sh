#!/bin/bash

echo "🧹 Limpiando proyecto..."

# Eliminar entorno virtual
if [ -d "venv" ]; then
    echo "🗑️ Eliminando entorno virtual..."
    rm -rf venv
fi

# Eliminar caché de Python
echo "🧼 Limpiando caché de Python..."
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -exec rm -f {} +

# Eliminar archivos generados
echo "📁 Eliminando archivos temporales..."
[ -f ".env" ] && rm .env
[ -f "last_session.json" ] && rm last_session.json

echo "✅ Proyecto limpio"
echo
echo "Para reconstruir el proyecto:"
echo "1. python -m venv venv"
echo "2. source venv/bin/activate (o venv\Scripts\activate en Windows)"
echo "3. pip install -r requirements.txt"