#!/bin/bash

# OSINT-Nexus Installation Script
# Este script instala y configura OSINT-Nexus

set -e

echo "🕵️ OSINT-Nexus - Script de Instalación"
echo "======================================"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor, instala Python 3.8 o superior."
    exit 1
fi

# Verificar versión de Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Se requiere Python 3.8 o superior. Versión actual: $python_version"
    exit 1
fi

echo "✅ Python $python_version detectado"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "✅ Archivo .env creado. Por favor, edítalo con tus claves API."
else
    echo "✅ Archivo .env ya existe."
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p static/css static/images logs

# Verificar instalación
echo "🔍 Verificando instalación..."
python3 -c "
import sys
sys.path.append('.')
try:
    from config.settings import APP_NAME, APP_VERSION
    print(f'✅ {APP_NAME} v{APP_VERSION} instalado correctamente')
except ImportError as e:
    print(f'❌ Error de importación: {e}')
    sys.exit(1)
"

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita el archivo .env con tus claves API"
echo "2. Activa el entorno virtual: source venv/bin/activate"
echo "3. Ejecuta la aplicación: streamlit run app.py"
echo ""
echo "🌐 La aplicación estará disponible en: http://localhost:8501"
echo ""
echo "⚠️ Recuerda usar esta herramienta únicamente para investigaciones legítimas y éticas."