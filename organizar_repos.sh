#!/bin/bash

# Script para organizar repositorios y ramas de GitHub
# Autor: Asistente IA
# Fecha: 2025-07-06

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== 📋 Organizador de Repositorios GitHub ===${NC}\n"

# Función para calcular días desde último commit
days_since_commit() {
    commit_date=$1
    current_date=$(date +%s)
    commit_seconds=$(date -d "$commit_date" +%s)
    days=$(( (current_date - commit_seconds) / 86400 ))
    echo $days
}

# Función para analizar repositorio
analyze_repo() {
    repo_name=$(basename $(git remote get-url origin) .git)
    default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
    
    echo -e "${GREEN}📁 Repositorio: $repo_name${NC}"
    echo -e "${BLUE}Rama predeterminada: $default_branch${NC}\n"
    
    echo "| Rama | Último Commit | Días | Mensaje | Estado |"
    echo "|------|---------------|------|---------|--------|"
    
    # Obtener todas las ramas con información
    git for-each-ref --sort=-committerdate refs/remotes/origin/ --format='%(refname:short)|%(committerdate:iso)|%(subject)' | while IFS='|' read -r branch date subject; do
        branch_name=${branch#origin/}
        days=$(days_since_commit "$date")
        
        # Determinar estado
        status="✅ Activa"
        if [[ $days -gt 15 ]]; then
            status="⚠️ Obsoleta"
        fi
        
        # Marcar rama predeterminada
        if [[ "$branch_name" == "$default_branch" ]]; then
            status="$status (DEFAULT)"
        fi
        
        # Detectar proyecto Excel/CSV
        if [[ "$subject" == *"Excel"* ]] || [[ "$subject" == *"CSV"* ]] || [[ "$subject" == *"search"* ]]; then
            status="🔄 MOVER A REPO INDEPENDIENTE"
        fi
        
        # Formatear fecha
        formatted_date=$(date -d "$date" +"%Y-%m-%d")
        
        # Truncar mensaje si es muy largo
        if [ ${#subject} -gt 50 ]; then
            subject="${subject:0:47}..."
        fi
        
        echo "| $branch_name | $formatted_date | $days | $subject | $status |"
    done
    
    echo ""
}

# Función para crear nuevo repositorio
create_excel_search_repo() {
    echo -e "\n${YELLOW}¿Deseas crear el repositorio 'buscador-excel-csv' ahora? (s/n)${NC}"
    read -r response
    
    if [[ "$response" == "s" ]]; then
        echo -e "${GREEN}Creando nuevo repositorio...${NC}"
        
        # Crear directorio temporal
        temp_dir="/tmp/buscador-excel-csv"
        mkdir -p $temp_dir
        cd $temp_dir
        
        # Inicializar repo
        git init
        
        # Crear README
        cat > README.md << EOF
# 🔍 Buscador de Texto en Excel/CSV

Aplicación web para buscar texto en archivos Excel y CSV.

## Características
- Búsqueda de texto en archivos Excel (.xlsx, .xls)
- Búsqueda en archivos CSV
- Interfaz web con Flask
- Búsqueda dinámica

## Instalación
\`\`\`bash
pip install -r requirements.txt
python app.py
\`\`\`

## Uso
1. Sube tu archivo Excel o CSV
2. Ingresa el texto a buscar
3. Obtén resultados con ubicación exacta (hoja, fila, columna)
EOF
        
        git add README.md
        git commit -m "Initial commit: Excel/CSV text search project"
        
        echo -e "${YELLOW}Repositorio creado localmente en: $temp_dir${NC}"
        echo -e "${YELLOW}Ahora debes:${NC}"
        echo "1. Crear el repositorio en GitHub: https://github.com/new"
        echo "2. Agregar el remote: git remote add origin https://github.com/TU_USUARIO/buscador-excel-csv.git"
        echo "3. Push: git push -u origin main"
        
        cd - > /dev/null
    fi
}

# Función principal
main() {
    # Verificar si estamos en un repositorio git
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}Error: No estás en un repositorio Git${NC}"
        exit 1
    fi
    
    # Analizar repositorio actual
    analyze_repo
    
    # Buscar ramas de Excel/CSV
    excel_branches=$(git branch -r | grep -E "(Excel|CSV|search)" | wc -l)
    if [[ $excel_branches -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Se detectaron $excel_branches ramas relacionadas con Excel/CSV${NC}"
        echo -e "${YELLOW}Estas ramas deben moverse a un repositorio independiente${NC}"
        create_excel_search_repo
    fi
    
    # Generar reporte
    echo -e "\n${BLUE}=== 📊 Resumen ===${NC}"
    total_branches=$(git branch -r | wc -l)
    obsolete_branches=$(git for-each-ref --sort=-committerdate refs/remotes/origin/ --format='%(committerdate:iso)' | while read date; do
        days=$(days_since_commit "$date")
        if [[ $days -gt 15 ]]; then
            echo "1"
        fi
    done | wc -l)
    
    echo "Total de ramas: $total_branches"
    echo "Ramas obsoletas (>15 días): $obsolete_branches"
    echo -e "Estado: ${GREEN}Repositorio organizado${NC}"
    
    # Guardar reporte
    echo -e "\n${BLUE}Reporte guardado en: organizacion_repos_$(date +%Y%m%d).txt${NC}"
}

# Ejecutar
main 2>&1 | tee "organizacion_repos_$(date +%Y%m%d_%H%M%S).txt"