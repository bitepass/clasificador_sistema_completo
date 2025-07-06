#!/bin/bash

# Script maestro para reorganizar repositorios GitHub
# Autor: Organizador de Repositorios GitHub

echo "🎯 REORGANIZADOR MAESTRO DE REPOSITORIOS GITHUB"
echo "==============================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}🛠️  REORGANIZADOR MAESTRO DE GITHUB${NC}"
    echo ""
    echo "Este script coordina la reorganización completa de tus repositorios GitHub"
    echo ""
    echo -e "${YELLOW}Uso:${NC} $0 [OPCIÓN]"
    echo ""
    echo -e "${YELLOW}Opciones:${NC}"
    echo "  --analyze              Analizar estado actual"
    echo "  --migrate-excel        Migrar proyecto Excel/CSV"
    echo "  --full-reorganize      Reorganización completa"
    echo "  --maintenance          Mantenimiento continuo"
    echo "  --demo                 Demostración (solo reportes)"
    echo "  --help, -h             Mostrar esta ayuda"
    echo ""
    echo -e "${YELLOW}Flujo recomendado:${NC}"
    echo "1. $0 --analyze          # Analizar estado actual"
    echo "2. $0 --migrate-excel    # Migrar proyecto Excel/CSV"
    echo "3. $0 --maintenance      # Configurar mantenimiento"
    echo ""
}

# Función para mostrar progreso
show_progress() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Función para analizar estado actual
analyze_current_state() {
    echo -e "${BLUE}📊 ANÁLISIS DEL ESTADO ACTUAL${NC}"
    echo "================================="
    echo ""
    
    if [[ -f "analyze_branches.sh" ]]; then
        show_progress "Ejecutando análisis de ramas..."
        ./analyze_branches.sh
        echo ""
    else
        show_error "Script analyze_branches.sh no encontrado"
        return 1
    fi
    
    show_progress "Análisis completado"
}

# Función para migrar proyecto Excel/CSV
migrate_excel_project() {
    echo -e "${BLUE}🔄 MIGRACIÓN DEL PROYECTO EXCEL/CSV${NC}"
    echo "==================================="
    echo ""
    
    if [[ -f "migrate_excel_project.sh" ]]; then
        show_warning "ATENCIÓN: Este proceso migrará el proyecto Excel/CSV a un repositorio independiente"
        echo ""
        echo "Pasos a seguir:"
        echo "1. Crear nuevo repositorio en GitHub: excel-csv-search-tool"
        echo "2. Ejecutar migración automática"
        echo "3. Limpiar ramas originales"
        echo ""
        
        read -p "¿Deseas continuar con la migración? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            show_progress "Iniciando proceso de migración..."
            ./migrate_excel_project.sh
        else
            show_warning "Migración cancelada"
        fi
    else
        show_error "Script migrate_excel_project.sh no encontrado"
        return 1
    fi
}

# Función para reorganización completa
full_reorganize() {
    echo -e "${BLUE}🎯 REORGANIZACIÓN COMPLETA${NC}"
    echo "=========================="
    echo ""
    
    show_progress "Paso 1: Análisis del estado actual"
    analyze_current_state
    
    echo ""
    show_progress "Paso 2: Migración del proyecto Excel/CSV"
    read -p "¿Proceder con la migración del proyecto Excel/CSV? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        migrate_excel_project
    else
        show_warning "Migración del proyecto Excel/CSV omitida"
    fi
    
    echo ""
    show_progress "Paso 3: Configuración de mantenimiento"
    setup_maintenance
    
    echo ""
    show_progress "Reorganización completa finalizada"
}

# Función para configurar mantenimiento
setup_maintenance() {
    echo -e "${BLUE}🔧 CONFIGURACIÓN DE MANTENIMIENTO${NC}"
    echo "=================================="
    echo ""
    
    if [[ -f "github_maintenance.sh" ]]; then
        show_progress "Configurando convenciones de nomenclatura..."
        ./github_maintenance.sh --setup-conventions
        
        show_progress "Generando reporte de estado..."
        ./github_maintenance.sh --report
        
        echo ""
        show_progress "Configuración de mantenimiento completada"
        echo ""
        echo -e "${YELLOW}💡 RECOMENDACIONES DE MANTENIMIENTO:${NC}"
        echo "• Ejecutar análisis semanal: ./github_maintenance.sh --report"
        echo "• Limpiar ramas obsoletas mensualmente: ./github_maintenance.sh --clean"
        echo "• Mantenimiento completo trimestral: ./github_maintenance.sh --full-maintenance"
        
    else
        show_error "Script github_maintenance.sh no encontrado"
        return 1
    fi
}

# Función para demostración (solo reportes)
run_demo() {
    echo -e "${BLUE}🎬 DEMOSTRACIÓN DEL ORGANIZADOR${NC}"
    echo "==============================="
    echo ""
    
    show_progress "Ejecutando análisis de demostración..."
    analyze_current_state
    
    echo ""
    show_progress "Generando reporte de estado..."
    if [[ -f "github_maintenance.sh" ]]; then
        ./github_maintenance.sh --report
    fi
    
    echo ""
    show_progress "Demostración completada"
    echo ""
    echo -e "${YELLOW}📋 RESUMEN DE LA DEMOSTRACIÓN:${NC}"
    echo "• Se analizaron todas las ramas del repositorio"
    echo "• Se identificaron proyectos separables (Excel/CSV)"
    echo "• Se generaron reportes detallados"
    echo "• Se proporcionaron recomendaciones de organización"
}

# Verificar que estamos en un repositorio Git
if [[ ! -d ".git" ]]; then
    show_error "No estás en un repositorio Git"
    exit 1
fi

# Verificar que los scripts existen
REQUIRED_SCRIPTS=("analyze_branches.sh" "migrate_excel_project.sh" "github_maintenance.sh")
for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [[ ! -f "$script" ]]; then
        show_error "Script requerido no encontrado: $script"
        exit 1
    fi
done

# Hacer scripts ejecutables
chmod +x analyze_branches.sh migrate_excel_project.sh github_maintenance.sh

# Procesar argumentos
case "${1:-}" in
    --analyze)
        analyze_current_state
        ;;
    --migrate-excel)
        migrate_excel_project
        ;;
    --full-reorganize)
        full_reorganize
        ;;
    --maintenance)
        setup_maintenance
        ;;
    --demo)
        run_demo
        ;;
    --help|-h)
        show_help
        ;;
    *)
        echo -e "${BLUE}🎯 REORGANIZADOR MAESTRO DE REPOSITORIOS GITHUB${NC}"
        echo ""
        echo "Selecciona una opción:"
        echo ""
        echo "1. Análisis del estado actual"
        echo "2. Migración del proyecto Excel/CSV"
        echo "3. Reorganización completa"
        echo "4. Configuración de mantenimiento"
        echo "5. Demostración (solo reportes)"
        echo "6. Ayuda"
        echo ""
        read -p "Opción (1-6): " -n 1 -r
        echo ""
        
        case $REPLY in
            1) analyze_current_state ;;
            2) migrate_excel_project ;;
            3) full_reorganize ;;
            4) setup_maintenance ;;
            5) run_demo ;;
            6) show_help ;;
            *) show_error "Opción no válida" ;;
        esac
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Proceso completado exitosamente${NC}"
echo ""
echo -e "${YELLOW}📚 DOCUMENTACIÓN DISPONIBLE:${NC}"
echo "• ORGANIZACION_REPOSITORIOS_GITHUB.md - Guía completa"
echo "• .github/BRANCH_NAMING.md - Convenciones de nomenclatura"
echo "• maintenance_log.txt - Log de actividades"
echo ""
echo -e "${YELLOW}🔗 PRÓXIMOS PASOS:${NC}"
echo "1. Revisar la documentación generada"
echo "2. Crear repositorio excel-csv-search-tool en GitHub"
echo "3. Ejecutar migración con la URL del nuevo repositorio"
echo "4. Configurar mantenimiento periódico"