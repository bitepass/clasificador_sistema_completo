# 📚 Instrucciones para Organizar tus Repositorios GitHub

## 🎯 Resumen de la Situación Actual

### Repositorio: `clasificador_sistema_completo`
- **Rama predeterminada**: `cursor/check-in-with-the-user-acb6`
- **Total de ramas**: 8
- **Estado**: ✅ Todas las ramas están activas (ninguna > 15 días sin actualización)
- **⚠️ PROBLEMA DETECTADO**: El proyecto "Buscador de texto en Excel/CSV" está mezclado con el clasificador

## 🔧 Pasos para Organizar tus Repositorios

### Paso 1: Ejecutar el Análisis Inicial
```bash
# Ejecuta el script de organización para ver el estado actual
./organizar_repos.sh
```

### Paso 2: Crear Nuevo Repositorio para Excel/CSV

1. **Ve a GitHub** y crea un nuevo repositorio:
   - Nombre: `buscador-excel-csv`
   - Descripción: "Aplicación web para buscar texto en archivos Excel y CSV"
   - Privacidad: según tu preferencia
   - NO inicialices con README (lo crearemos nosotros)

2. **Copia la URL del nuevo repositorio** (ejemplo: `https://github.com/TU_USUARIO/buscador-excel-csv.git`)

### Paso 3: Migrar las Ramas de Excel/CSV

```bash
# Ejecuta el script de migración
./migrar_excel_csv.sh

# El script te pedirá:
# 1. Confirmación para proceder
# 2. La URL del nuevo repositorio que creaste
```

### Paso 4: Verificar y Completar la Migración

```bash
# El script creará el nuevo repositorio en un directorio temporal
# Ve al directorio indicado por el script
cd /tmp/excel-csv-migration-[TIMESTAMP]/nuevo

# Revisa que todo esté correcto
git log --oneline --graph --all

# Si todo está bien, sube al repositorio remoto
git push -u origin main
git push --all origin
```

### Paso 5: Limpiar el Repositorio Original

**⚠️ IMPORTANTE**: Solo haz esto después de verificar que la migración fue exitosa

```bash
# En el nuevo repositorio hay un script de limpieza
./limpiar_repo_original.sh

# O manualmente desde el repositorio original:
git push origin --delete cursor/bc-b2fec4da-d0d6-42f2-a257-456226942d45-5b25
git push origin --delete cursor/bc-7b2c1c9b-bcde-49f0-ae20-a5ae47f4266d-39c1
git push origin --delete cursor/bc-586f43a9-e5f5-4727-bcfb-1d53b417d9c7-cb90
```

### Paso 6: Fusionar Ramas Pendientes (Opcional)

Para el repositorio `clasificador_sistema_completo`, considera fusionar:

```bash
# Cambiar a la rama predeterminada
git checkout cursor/check-in-with-the-user-acb6

# Fusionar actualizaciones pendientes
git merge origin/cursor/actualizar-clasificador-ai-seg-n-nuevos-requisitos-3006
git merge origin/cursor/update-frontend-to-fix-fetch-error-df2e

# Subir cambios
git push origin cursor/check-in-with-the-user-acb6
```

## 🤖 Automatización Futura

### Configurar Alias de Git
Agrega estos alias a tu `~/.gitconfig`:

```bash
[alias]
    # Ver ramas ordenadas por fecha
    branch-by-date = for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:short) %(refname:short) %(subject)'
    
    # Limpiar ramas locales ya fusionadas
    cleanup = "!git branch --merged | grep -v '\\*' | xargs -n 1 git branch -d"
    
    # Ver resumen de repositorio
    repo-summary = "!f() { echo 'Repositorio:' $(basename $(git remote get-url origin) .git); echo 'Rama actual:' $(git branch --show-current); echo 'Total ramas:' $(git branch -r | wc -l); echo 'Último commit:' $(git log -1 --pretty=format:'%h - %s (%cr)'); }; f"
```

### Programar Revisiones Periódicas
Crea un recordatorio mensual para ejecutar:
```bash
./organizar_repos.sh
```

## 📊 Resultado Esperado

Después de completar estos pasos tendrás:

1. **Repositorio `clasificador_sistema_completo`**:
   - Solo código relacionado con el clasificador DDIC-SM
   - Ramas organizadas y fusionadas
   - Sin código de Excel/CSV

2. **Repositorio `buscador-excel-csv`** (nuevo):
   - Aplicación independiente para búsqueda en Excel/CSV
   - Historial de commits preservado
   - Listo para desarrollo independiente

## 🆘 Solución de Problemas

- **Error al ejecutar scripts**: Asegúrate de que tienen permisos: `chmod +x *.sh`
- **Conflictos al fusionar**: Resuelve manualmente o usa `git merge --abort` para cancelar
- **No puedo crear el repositorio en GitHub**: Verifica tu autenticación y permisos

## 📝 Notas Finales

- Los scripts crean backups automáticos antes de cambios importantes
- Todos los reportes se guardan con timestamp para referencia futura
- Puedes ejecutar `organizar_repos.sh` en cualquier momento para ver el estado actual

¡Tu organización de repositorios está lista! 🎉