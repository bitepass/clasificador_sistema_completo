#!/bin/bash

# Script para migrar el proyecto Excel/CSV a un repositorio independiente
# Autor: Organizador de Repositorios GitHub

echo "🔄 MIGRACIÓN DEL PROYECTO EXCEL/CSV A REPOSITORIO INDEPENDIENTE"
echo "=============================================================="
echo ""

# Variables de configuración
NEW_REPO_NAME="excel-csv-search-tool"
EXCEL_BRANCHES=(
    "cursor/bc-b2fec4da-d0d6-42f2-a257-456226942d45-5b25"
    "cursor/bc-7b2c1c9b-bcde-49f0-ae20-a5ae47f4266d-39c1"
    "cursor/bc-586f43a9-e5f5-4727-bcfb-1d53b417d9c7-cb90"
)

echo "📋 Configuración de migración:"
echo "   - Repositorio destino: $NEW_REPO_NAME"
echo "   - Ramas a migrar: ${#EXCEL_BRANCHES[@]}"
for branch in "${EXCEL_BRANCHES[@]}"; do
    echo "     * $branch"
done
echo ""

# Función para mostrar ayuda
show_help() {
    echo "🛠️  PASOS PARA COMPLETAR LA MIGRACIÓN:"
    echo ""
    echo "1. CREAR NUEVO REPOSITORIO EN GITHUB:"
    echo "   - Ve a https://github.com/new"
    echo "   - Nombre: $NEW_REPO_NAME"
    echo "   - Descripción: 'Herramienta web para búsqueda de texto en archivos Excel/CSV'"
    echo "   - Público/Privado: según tu preferencia"
    echo "   - NO inicializar con README (lo haremos nosotros)"
    echo ""
    echo "2. EJECUTAR MIGRACIÓN AUTOMÁTICA:"
    echo "   ./migrate_excel_project.sh --migrate https://github.com/tu-usuario/$NEW_REPO_NAME.git"
    echo ""
    echo "3. LIMPIAR RAMAS ORIGINALES:"
    echo "   ./migrate_excel_project.sh --cleanup"
    echo ""
}

# Función para realizar la migración
perform_migration() {
    local new_repo_url=$1
    
    echo "🚀 Iniciando migración a: $new_repo_url"
    echo ""
    
    # Crear directorio temporal para el nuevo repositorio
    TEMP_DIR=$(mktemp -d)
    echo "📁 Creando repositorio temporal en: $TEMP_DIR"
    
    cd "$TEMP_DIR"
    git init
    git remote add origin "$new_repo_url"
    
    # Obtener la rama principal del proyecto Excel/CSV
    echo "📥 Obteniendo rama principal del proyecto..."
    git fetch origin "${EXCEL_BRANCHES[0]}"
    git checkout -b main FETCH_HEAD
    
    # Crear README específico para el proyecto
    cat > README.md << 'EOF'
# 🔍 Excel/CSV Search Tool

Herramienta web para búsqueda de texto en archivos Excel y CSV con interfaz intuitiva.

## 🚀 Características

- **Múltiples formatos**: Soporte para CSV, XLS, XLSX
- **Búsqueda flexible**: Buscar en columnas específicas o en todo el archivo
- **Interfaz web**: Fácil de usar desde el navegador
- **Búsqueda sensible a mayúsculas**: Opción configurable
- **Resultados con contexto**: Muestra información relevante de cada coincidencia

## 📋 Instalación Rápida

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

## 🌐 Uso

1. Abrir navegador en `http://localhost:5000`
2. Subir archivo CSV/Excel
3. Especificar término de búsqueda
4. Seleccionar columnas (opcional)
5. Ver resultados con contexto

## 🛠️ Tecnologías

- **Backend**: Flask, Pandas
- **Frontend**: HTML, CSS, JavaScript
- **Procesamiento**: NumPy, Werkzeug

## 📁 Estructura

```
excel-csv-search-tool/
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración
├── requirements.txt    # Dependencias
├── templates/          # Plantillas HTML
├── ejemplo_datos.csv   # Archivo de ejemplo
└── README.md          # Documentación
```

## 🔧 Desarrollo

Este proyecto fue migrado desde el repositorio `clasificador_sistema_completo` para mantener mejor organización y enfoque específico.

EOF
    
    # Commit inicial
    git add .
    git commit -m "feat: Migrate Excel/CSV search tool to independent repository

- Complete Flask web application for text search in Excel/CSV files
- Support for multiple file formats (CSV, XLS, XLSX)
- Flexible search with column selection
- Context-aware results display
- Clean and intuitive web interface"
    
    # Push a GitHub
    echo "⬆️  Subiendo código a GitHub..."
    git push -u origin main
    
    # Crear ramas adicionales si es necesario
    echo "🌿 Creando ramas adicionales..."
    for branch in "${EXCEL_BRANCHES[@]:1}"; do
        echo "   Procesando rama: $branch"
        git fetch origin "$branch"
        branch_name=$(echo "$branch" | sed 's/cursor\///' | sed 's/bc-[a-f0-9-]*-/feature-/')
        git checkout -b "$branch_name" FETCH_HEAD
        git push -u origin "$branch_name"
    done
    
    # Volver al directorio original
    cd - > /dev/null
    
    # Limpiar directorio temporal
    rm -rf "$TEMP_DIR"
    
    echo "✅ Migración completada exitosamente!"
    echo "🌐 Repositorio disponible en: $new_repo_url"
    echo ""
}

# Función para limpiar ramas originales
cleanup_branches() {
    echo "🧹 LIMPIEZA DE RAMAS ORIGINALES"
    echo "==============================="
    echo ""
    
    echo "⚠️  Las siguientes ramas serán eliminadas del repositorio original:"
    for branch in "${EXCEL_BRANCHES[@]}"; do
        echo "   - $branch"
    done
    echo ""
    
    read -p "¿Confirmas la eliminación? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for branch in "${EXCEL_BRANCHES[@]}"; do
            echo "🗑️  Eliminando rama: $branch"
            git push origin --delete "$branch" 2>/dev/null || echo "   (Ya eliminada o no existe)"
        done
        echo "✅ Limpieza completada"
    else
        echo "❌ Limpieza cancelada"
    fi
}

# Procesar argumentos
case "${1:-}" in
    --migrate)
        if [[ -z "$2" ]]; then
            echo "❌ Error: Debe especificar la URL del nuevo repositorio"
            echo "Uso: $0 --migrate https://github.com/usuario/repo.git"
            exit 1
        fi
        perform_migration "$2"
        ;;
    --cleanup)
        cleanup_branches
        ;;
    --help|-h)
        show_help
        ;;
    *)
        show_help
        ;;
esac