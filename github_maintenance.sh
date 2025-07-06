#!/bin/bash

# Script de mantenimiento continuo para repositorios GitHub
# Automatiza la limpieza y organización de ramas

echo "🔧 MANTENIMIENTO CONTINUO DE REPOSITORIOS GITHUB"
echo "================================================"
echo ""

# Configuración
DAYS_OBSOLETE=15
BACKUP_DIR="$HOME/git_backups"
LOG_FILE="maintenance_log.txt"

# Función para logging
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Función para crear backup antes de limpiar
create_backup() {
    local repo_name=$1
    local backup_path="$BACKUP_DIR/${repo_name}_backup_$(date +%Y%m%d_%H%M%S)"
    
    log_message "Creating backup in: $backup_path"
    mkdir -p "$backup_path"
    
    # Crear bundle con todas las ramas
    git bundle create "$backup_path/complete_repo.bundle" --all
    
    # Exportar información de ramas
    git for-each-ref --format='%(refname:short)|%(committerdate:iso)|%(subject)' > "$backup_path/branches_info.txt"
    
    echo "✅ Backup creado: $backup_path"
}

# Función para analizar y limpiar ramas obsoletas
analyze_and_clean() {
    local current_timestamp=$(date +%s)
    local cutoff_timestamp=$((current_timestamp - DAYS_OBSOLETE*24*60*60))
    
    echo "🔍 Analizando ramas obsoletas (>$DAYS_OBSOLETE días)..."
    
    # Obtener ramas obsoletas
    local obsolete_branches=()
    while IFS='|' read -r branch_name commit_date unix_timestamp; do
        if [[ $unix_timestamp -lt $cutoff_timestamp ]]; then
            # Excluir ramas principales
            if [[ "$branch_name" != "main" ]] && [[ "$branch_name" != "master" ]] && [[ "$branch_name" != *"main"* ]]; then
                obsolete_branches+=("$branch_name")
            fi
        fi
    done < <(git for-each-ref --format='%(refname:short)|%(committerdate:iso)|%(committerdate:unix)' refs/heads/ refs/remotes/origin/)
    
    if [[ ${#obsolete_branches[@]} -gt 0 ]]; then
        echo "🚨 Ramas obsoletas encontradas: ${#obsolete_branches[@]}"
        
        for branch in "${obsolete_branches[@]}"; do
            echo "   - $branch"
        done
        
        echo ""
        read -p "¿Deseas crear un backup antes de limpiar? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
            create_backup "$(basename $(git rev-parse --show-toplevel))"
        fi
        
        echo ""
        read -p "¿Proceder con la limpieza de ramas obsoletas? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            for branch in "${obsolete_branches[@]}"; do
                echo "🗑️  Eliminando rama: $branch"
                git branch -D "$branch" 2>/dev/null || echo "   (Local no existe)"
                git push origin --delete "$branch" 2>/dev/null || echo "   (Remota no existe)"
                log_message "Deleted obsolete branch: $branch"
            done
            echo "✅ Limpieza completada"
        else
            echo "❌ Limpieza cancelada"
        fi
    else
        echo "✅ No se encontraron ramas obsoletas"
    fi
}

# Función para generar reporte de estado
generate_status_report() {
    local report_file="repository_status_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# 📊 Reporte de Estado del Repositorio

**Fecha:** $(date)
**Repositorio:** $(basename $(git rev-parse --show-toplevel))

## 🌿 Estado de Ramas

| Rama | Última Actualización | Autor | Mensaje | Estado |
|------|---------------------|-------|---------|--------|
EOF
    
    # Agregar información de ramas
    git for-each-ref --sort=-committerdate --format='%(refname:short)|%(committerdate:short)|%(authorname)|%(subject)|%(committerdate:unix)' refs/heads/ refs/remotes/origin/ | while IFS='|' read -r branch_name commit_date author subject unix_timestamp; do
        local current_timestamp=$(date +%s)
        local days_ago=$(((current_timestamp - unix_timestamp) / 86400))
        
        if [[ $days_ago -gt $DAYS_OBSOLETE ]]; then
            local status="🚨 OBSOLETA ($days_ago días)"
        else
            local status="✅ ACTIVA"
        fi
        
        # Limpiar nombres de ramas
        local clean_branch=$(echo "$branch_name" | sed 's|origin/||')
        local truncated_subject=$(echo "$subject" | cut -c1-40)
        
        echo "| $clean_branch | $commit_date | $author | $truncated_subject | $status |" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

## 📈 Estadísticas

- **Total de ramas:** $(git branch -a | wc -l)
- **Ramas locales:** $(git branch | wc -l)
- **Ramas remotas:** $(git branch -r | wc -l)
- **Últimos commits:** $(git log --oneline -5 | wc -l)

## 🎯 Recomendaciones

### Ramas Obsoletas
$(git for-each-ref --format='%(refname:short)|%(committerdate:unix)' refs/heads/ refs/remotes/origin/ | awk -F'|' -v cutoff=$(($(date +%s) - DAYS_OBSOLETE*24*60*60)) '$2 < cutoff {print "- " $1}' | head -10)

### Acciones Sugeridas
1. **Revisar ramas obsoletas** - Fusionar o eliminar ramas sin actividad
2. **Consolidar branches** - Unificar ramas relacionadas
3. **Documentar decisiones** - Mantener registro de cambios importantes
4. **Automatizar limpieza** - Configurar este script como tarea periódica

## 🔧 Próximos Pasos

- [ ] Revisar ramas marcadas como obsoletas
- [ ] Crear backups si es necesario
- [ ] Ejecutar limpieza de ramas
- [ ] Actualizar documentación del proyecto

---
*Generado automáticamente por el script de mantenimiento GitHub*
EOF
    
    log_message "Status report generated: $report_file"
    echo "📄 Reporte generado: $report_file"
}

# Función para establecer convenciones de naming
setup_branch_conventions() {
    cat > ".github/BRANCH_NAMING.md" << 'EOF'
# 🌿 Convenciones de Nombres para Ramas

## Estructura Recomendada

```
<tipo>/<descripción-corta>
```

## Tipos de Ramas

- **feature/**: Nuevas funcionalidades
- **bugfix/**: Corrección de errores
- **hotfix/**: Correcciones urgentes
- **docs/**: Documentación
- **refactor/**: Refactorización de código
- **test/**: Pruebas
- **chore/**: Tareas de mantenimiento

## Ejemplos

```bash
feature/excel-search-improvements
bugfix/csv-encoding-issue
hotfix/security-patch-2024
docs/api-documentation
refactor/database-optimization
test/unit-tests-coverage
chore/dependency-updates
```

## Comandos Útiles

```bash
# Crear rama con convención
git checkout -b feature/nueva-funcionalidad

# Listar ramas con patrón
git branch | grep "feature/"

# Limpiar ramas fusionadas
git branch --merged | grep -E "feature/|bugfix/" | xargs git branch -d
```

## Automatización

Considera usar este script para mantener la organización:

```bash
./github_maintenance.sh --analyze
./github_maintenance.sh --clean
./github_maintenance.sh --report
```
EOF
    
    mkdir -p ".github"
    echo "📋 Convenciones de naming creadas en .github/BRANCH_NAMING.md"
}

# Procesador de argumentos
case "${1:-}" in
    --analyze)
        analyze_and_clean
        ;;
    --clean)
        analyze_and_clean
        ;;
    --report)
        generate_status_report
        ;;
    --setup-conventions)
        setup_branch_conventions
        ;;
    --full-maintenance)
        echo "🔄 Ejecutando mantenimiento completo..."
        generate_status_report
        analyze_and_clean
        setup_branch_conventions
        echo "✅ Mantenimiento completo finalizado"
        ;;
    --help|-h)
        echo "🛠️  SCRIPT DE MANTENIMIENTO GITHUB"
        echo ""
        echo "Uso: $0 [OPCIÓN]"
        echo ""
        echo "Opciones:"
        echo "  --analyze              Analizar y limpiar ramas obsoletas"
        echo "  --clean                Limpiar ramas obsoletas (alias de --analyze)"
        echo "  --report               Generar reporte de estado"
        echo "  --setup-conventions    Crear guía de convenciones"
        echo "  --full-maintenance     Ejecutar mantenimiento completo"
        echo "  --help, -h             Mostrar esta ayuda"
        echo ""
        echo "Ejemplos:"
        echo "  $0 --report            # Generar reporte de estado"
        echo "  $0 --analyze           # Analizar y limpiar ramas"
        echo "  $0 --full-maintenance  # Mantenimiento completo"
        ;;
    *)
        echo "🎯 MANTENIMIENTO REPOSITORIOS GITHUB"
        echo ""
        echo "Ejecuta --help para ver opciones disponibles"
        echo ""
        echo "🔍 Análisis rápido:"
        generate_status_report
        ;;
esac

log_message "Maintenance script completed"