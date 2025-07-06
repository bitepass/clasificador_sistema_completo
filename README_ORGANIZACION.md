# 🎯 Organizador de Repositorios GitHub

Sistema completo para organizar, analizar y mantener repositorios GitHub de forma eficiente.

## 📋 Archivos Incluidos

### 📊 Documentación
- **`ORGANIZACION_REPOSITORIOS_GITHUB.md`** - Análisis completo y recomendaciones
- **`README_ORGANIZACION.md`** - Esta guía de uso
- **`.github/BRANCH_NAMING.md`** - Convenciones de nomenclatura (generado automáticamente)

### 🛠️ Scripts Principales
- **`reorganize_github.sh`** - Script maestro coordinador
- **`analyze_branches.sh`** - Análisis detallado de ramas
- **`migrate_excel_project.sh`** - Migración del proyecto Excel/CSV
- **`github_maintenance.sh`** - Mantenimiento continuo

### 📈 Reportes (Generados)
- **`repository_status_*.md`** - Reportes de estado con timestamp
- **`maintenance_log.txt`** - Log de actividades

## 🚀 Inicio Rápido

### 1. Análisis Inicial
```bash
# Opción 1: Usando el script maestro
./reorganize_github.sh --analyze

# Opción 2: Directamente
./analyze_branches.sh
```

### 2. Migración del Proyecto Excel/CSV
```bash
# Paso 1: Crear repositorio en GitHub
# Ve a: https://github.com/new
# Nombre: excel-csv-search-tool

# Paso 2: Ejecutar migración
./migrate_excel_project.sh --migrate https://github.com/tu-usuario/excel-csv-search-tool.git

# Paso 3: Limpiar ramas originales
./migrate_excel_project.sh --cleanup
```

### 3. Configurar Mantenimiento
```bash
./github_maintenance.sh --setup-conventions
./github_maintenance.sh --report
```

## 🎮 Modo Interactivo

Simplemente ejecuta el script maestro sin argumentos:

```bash
./reorganize_github.sh
```

Esto te mostrará un menú interactivo con todas las opciones disponibles.

## 📚 Guía Detallada de Scripts

### 🎯 `reorganize_github.sh` - Script Maestro

**Propósito:** Coordina todos los procesos de reorganización

**Opciones:**
- `--analyze` - Analizar estado actual
- `--migrate-excel` - Migrar proyecto Excel/CSV
- `--full-reorganize` - Reorganización completa
- `--maintenance` - Configurar mantenimiento
- `--demo` - Demostración (solo reportes)
- `--help` - Mostrar ayuda

**Ejemplo:**
```bash
./reorganize_github.sh --full-reorganize
```

### 📊 `analyze_branches.sh` - Análisis de Ramas

**Propósito:** Analiza todas las ramas del repositorio y genera reportes

**Características:**
- Ordena ramas por fecha de actualización
- Identifica ramas obsoletas (>15 días)
- Detecta proyectos separables (Excel/CSV)
- Genera estadísticas completas

**Ejemplo:**
```bash
./analyze_branches.sh
```

### 🔄 `migrate_excel_project.sh` - Migración Excel/CSV

**Propósito:** Migra el proyecto Excel/CSV a un repositorio independiente

**Opciones:**
- `--migrate <url>` - Migrar a repositorio específico
- `--cleanup` - Limpiar ramas originales
- `--help` - Mostrar ayuda

**Ejemplo:**
```bash
./migrate_excel_project.sh --migrate https://github.com/usuario/excel-csv-search-tool.git
```

### 🔧 `github_maintenance.sh` - Mantenimiento Continuo

**Propósito:** Mantiene la organización a largo plazo

**Opciones:**
- `--analyze` - Analizar y limpiar ramas obsoletas
- `--report` - Generar reporte de estado
- `--setup-conventions` - Crear guía de convenciones
- `--full-maintenance` - Mantenimiento completo

**Ejemplo:**
```bash
./github_maintenance.sh --full-maintenance
```

## 🎨 Flujo de Trabajo Recomendado

### Primera Vez (Reorganización Inicial)
```bash
# 1. Análisis completo
./reorganize_github.sh --analyze

# 2. Revisar recomendaciones
cat ORGANIZACION_REPOSITORIOS_GITHUB.md

# 3. Crear repositorio excel-csv-search-tool en GitHub

# 4. Migrar proyecto Excel/CSV
./reorganize_github.sh --migrate-excel

# 5. Configurar mantenimiento
./reorganize_github.sh --maintenance
```

### Mantenimiento Periódico
```bash
# Semanal
./github_maintenance.sh --report

# Mensual
./github_maintenance.sh --analyze

# Trimestral
./github_maintenance.sh --full-maintenance
```

## 🛡️ Seguridad y Backups

### Backups Automáticos
Los scripts crean backups automáticamente antes de realizar cambios:
- Ubicación: `$HOME/git_backups/`
- Formato: `{repo}_backup_{timestamp}/`
- Contenido: Bundle completo + información de ramas

### Confirmaciones
Todos los scripts requieren confirmación antes de:
- Eliminar ramas
- Migrar código
- Realizar cambios destructivos

## 📋 Resultado de la Organización

### Estado Actual Identificado:
- ✅ **10 ramas analizadas**
- ✅ **0 ramas obsoletas**
- 🔍 **3 ramas del proyecto Excel/CSV identificadas**
- ⭐ **Rama predeterminada:** `cursor/check-in-with-the-user-acb6`

### Proyecto Excel/CSV Detectado:
- **Ramas:** 3 ramas relacionadas con búsqueda Excel/CSV
- **Funcionalidad:** Aplicación web Flask completa
- **Características:** Soporte CSV/XLS/XLSX, búsqueda por columnas
- **Recomendación:** Migrar a repositorio independiente

## 🎯 Beneficios de la Organización

### ✅ Inmediatos
- **Claridad:** Proyectos separados por funcionalidad
- **Mantenibilidad:** Código más fácil de mantener
- **Navegación:** Estructura clara y lógica

### ✅ A Largo Plazo
- **Escalabilidad:** Crecimiento independiente por proyecto
- **Colaboración:** Mejor para trabajo en equipo
- **Documentación:** Específica por proyecto

## 🔧 Personalización

### Configurar Días de Obsolescencia
Edita la variable `DAYS_OBSOLETE` en `github_maintenance.sh`:
```bash
DAYS_OBSOLETE=15  # Cambiar según necesidades
```

### Modificar Criterios de Detección
Edita las condiciones en `analyze_branches.sh`:
```bash
# Detectar proyectos específicos
if [[ "$subject" == *"Excel"* ]] || [[ "$subject" == *"CSV"* ]]; then
    # Lógica personalizada
fi
```

## 🚨 Solución de Problemas

### Script No Ejecutable
```bash
chmod +x *.sh
```

### Directorio No es Repositorio Git
```bash
cd /path/to/your/git/repository
```

### Permisos de GitHub
Verifica que tengas permisos para crear repositorios y eliminar ramas.

## 📞 Soporte

### Logs
Revisa `maintenance_log.txt` para troubleshooting.

### Ayuda
Cada script tiene ayuda integrada:
```bash
./reorganize_github.sh --help
./analyze_branches.sh --help
./migrate_excel_project.sh --help
./github_maintenance.sh --help
```

## 🎉 Conclusión

Este sistema de organización te permite:
1. **Analizar** el estado actual de tus repositorios
2. **Separar** proyectos en repositorios independientes
3. **Mantener** la organización a largo plazo
4. **Automatizar** tareas repetitivas

**¡Repositorios organizados = Desarrollo más eficiente!**

---

*Sistema desarrollado para la organización eficiente de repositorios GitHub*  
*Fecha: 6 de Julio, 2025*