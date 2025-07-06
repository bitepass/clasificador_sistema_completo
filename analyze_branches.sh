#!/bin/bash

# Script para analizar y organizar ramas de GitHub
# Fecha: $(date)

echo "🔍 ANÁLISIS DE REPOSITORIOS Y RAMAS - GITHUB"
echo "=============================================="
echo ""

# Obtener información del repositorio actual
REPO_URL=$(git remote get-url origin)
REPO_NAME=$(basename "$REPO_URL" .git)
echo "📁 Repositorio: $REPO_NAME"
echo "🔗 URL: $REPO_URL"
echo ""

# Obtener rama por defecto
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
echo "🌟 Rama predeterminada: $DEFAULT_BRANCH"
echo ""

# Fecha actual para cálculo de obsolescencia
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_TIMESTAMP=$(date +%s)
FIFTEEN_DAYS_AGO=$((CURRENT_TIMESTAMP - 15*24*60*60))

echo "📊 ANÁLISIS DE RAMAS"
echo "===================="
echo ""

# Crear archivo temporal para datos
TEMP_FILE=$(mktemp)

# Obtener información de todas las ramas
git for-each-ref --sort=-committerdate --format='%(refname:short)|%(committerdate:iso)|%(authorname)|%(subject)|%(committerdate:unix)' refs/heads/ refs/remotes/origin/ > "$TEMP_FILE"

# Contadores
TOTAL_BRANCHES=0
OBSOLETE_BRANCHES=0
EXCEL_BRANCHES=0

echo "| Rama | Fecha Último Commit | Autor | Mensaje Commit | Estado |"
echo "|------|-------------------|--------|---------------|---------|"

while IFS='|' read -r branch_name commit_date author subject unix_timestamp; do
    # Limpiar nombres de ramas remotas
    clean_branch=$(echo "$branch_name" | sed 's|origin/||')
    
    # Verificar si es rama por defecto
    if [[ "$clean_branch" == "$DEFAULT_BRANCH" ]]; then
        default_marker="⭐"
    else
        default_marker=""
    fi
    
    # Verificar obsolescencia
    if [[ $unix_timestamp -lt $FIFTEEN_DAYS_AGO ]]; then
        obsolete_marker="🚨 OBSOLETA"
        ((OBSOLETE_BRANCHES++))
    else
        obsolete_marker="✅ ACTIVA"
    fi
    
    # Verificar si es rama relacionada con Excel/CSV
    if [[ "$subject" == *"Excel"* ]] || [[ "$subject" == *"CSV"* ]] || [[ "$subject" == *"search"* ]]; then
        excel_marker="🔍 EXCEL/CSV"
        ((EXCEL_BRANCHES++))
    else
        excel_marker=""
    fi
    
    # Formatear fecha
    formatted_date=$(date -d "$commit_date" +"%Y-%m-%d %H:%M" 2>/dev/null || echo "$commit_date")
    
    # Truncar mensaje si es muy largo
    truncated_subject=$(echo "$subject" | cut -c1-50)
    if [[ ${#subject} -gt 50 ]]; then
        truncated_subject="${truncated_subject}..."
    fi
    
    echo "| $clean_branch $default_marker | $formatted_date | $author | $truncated_subject | $obsolete_marker $excel_marker |"
    
    ((TOTAL_BRANCHES++))
done < "$TEMP_FILE"

echo ""
echo "📈 RESUMEN ESTADÍSTICO"
echo "====================="
echo "🔢 Total de ramas: $TOTAL_BRANCHES"
echo "🚨 Ramas obsoletas (>15 días): $OBSOLETE_BRANCHES"
echo "🔍 Ramas Excel/CSV identificadas: $EXCEL_BRANCHES"
echo ""

echo "🎯 RECOMENDACIONES"
echo "=================="
echo ""

if [[ $OBSOLETE_BRANCHES -gt 0 ]]; then
    echo "⚠️  RAMAS OBSOLETAS DETECTADAS:"
    echo "   - Revisar las $OBSOLETE_BRANCHES ramas marcadas como OBSOLETAS"
    echo "   - Considerar fusionar o eliminar ramas no utilizadas"
    echo ""
fi

if [[ $EXCEL_BRANCHES -gt 0 ]]; then
    echo "🔍 PROYECTO EXCEL/CSV DETECTADO:"
    echo "   - Se encontraron $EXCEL_BRANCHES ramas relacionadas con búsqueda Excel/CSV"
    echo "   - RECOMENDACIÓN: Crear repositorio independiente para este proyecto"
    echo ""
    
    echo "📋 Ramas del proyecto Excel/CSV:"
    while IFS='|' read -r branch_name commit_date author subject unix_timestamp; do
        if [[ "$subject" == *"Excel"* ]] || [[ "$subject" == *"CSV"* ]] || [[ "$subject" == *"search"* ]]; then
            clean_branch=$(echo "$branch_name" | sed 's|origin/||')
            echo "   - $clean_branch: $subject"
        fi
    done < "$TEMP_FILE"
    echo ""
fi

echo "🛠️  ACCIONES SUGERIDAS:"
echo "   1. Crear nuevo repositorio: 'excel-csv-search-tool'"
echo "   2. Migrar ramas Excel/CSV al nuevo repositorio"
echo "   3. Limpiar ramas obsoletas del repositorio actual"
echo "   4. Establecer convención de nombres para ramas futuras"
echo ""

# Limpiar archivo temporal
rm "$TEMP_FILE"

echo "✅ Análisis completado - $(date)"