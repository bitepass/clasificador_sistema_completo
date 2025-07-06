#!/bin/bash

# Script para migrar ramas de Excel/CSV a repositorio independiente
# Autor: Asistente IA
# Fecha: 2025-07-06

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== 🚀 Migración de Proyecto Excel/CSV ===${NC}\n"

# Ramas a migrar
EXCEL_BRANCHES=(
    "cursor/bc-b2fec4da-d0d6-42f2-a257-456226942d45-5b25"
    "cursor/bc-7b2c1c9b-bcde-49f0-ae20-a5ae47f4266d-39c1"
    "cursor/bc-586f43a9-e5f5-4727-bcfb-1d53b417d9c7-cb90"
)

echo -e "${YELLOW}Este script te ayudará a migrar las ramas de Excel/CSV a un nuevo repositorio.${NC}"
echo -e "${YELLOW}Asegúrate de haber creado el repositorio 'buscador-excel-csv' en GitHub primero.${NC}\n"

echo "Ramas a migrar:"
for branch in "${EXCEL_BRANCHES[@]}"; do
    echo "  - $branch"
done

echo -e "\n${YELLOW}¿Continuar con la migración? (s/n)${NC}"
read -r response

if [[ "$response" != "s" ]]; then
    echo "Migración cancelada."
    exit 0
fi

# Solicitar URL del nuevo repositorio
echo -e "\n${BLUE}Ingresa la URL del nuevo repositorio (ej: https://github.com/usuario/buscador-excel-csv.git):${NC}"
read -r NEW_REPO_URL

# Crear directorio temporal
TEMP_DIR="/tmp/excel-csv-migration-$(date +%s)"
mkdir -p "$TEMP_DIR"

echo -e "\n${GREEN}1. Clonando repositorio actual...${NC}"
git clone . "$TEMP_DIR/original" --no-hardlinks

cd "$TEMP_DIR/original"

echo -e "\n${GREEN}2. Configurando nuevo repositorio...${NC}"
# Crear nuevo repositorio vacío
mkdir -p "$TEMP_DIR/nuevo"
cd "$TEMP_DIR/nuevo"
git init
git remote add origin "$NEW_REPO_URL"

# Crear estructura inicial
cat > README.md << 'EOF'
# 🔍 Buscador de Texto en Excel/CSV

Aplicación web para buscar texto en archivos Excel y CSV con interfaz moderna.

## 🚀 Características

- **Búsqueda en Excel**: Soporta archivos .xlsx y .xls
- **Búsqueda en CSV**: Procesamiento rápido de archivos CSV
- **Interfaz Web**: Aplicación Flask con diseño moderno
- **Búsqueda Dinámica**: Resultados en tiempo real
- **Exportación**: Descarga de resultados

## 📋 Requisitos

- Python 3.8+
- Flask
- pandas
- openpyxl

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone [URL_DEL_REPO]
cd buscador-excel-csv

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🎯 Uso

```bash
# Ejecutar aplicación
python app.py

# La aplicación estará disponible en http://localhost:5000
```

## 📁 Estructura del Proyecto

```
buscador-excel-csv/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias
├── static/            # Archivos estáticos (CSS, JS)
├── templates/         # Plantillas HTML
└── uploads/           # Archivos subidos (temporal)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
EOF

# Crear requirements.txt básico
cat > requirements.txt << 'EOF'
Flask==2.3.2
pandas==2.0.3
openpyxl==3.1.2
werkzeug==2.3.6
EOF

git add .
git commit -m "Initial commit: Excel/CSV search project structure"

echo -e "\n${GREEN}3. Migrando ramas...${NC}"
cd "$TEMP_DIR/original"

for branch in "${EXCEL_BRANCHES[@]}"; do
    echo -e "\n${BLUE}Procesando rama: $branch${NC}"
    
    # Checkout de la rama
    git checkout -b "temp-$branch" "origin/$branch" 2>/dev/null || git checkout "origin/$branch"
    
    # Obtener solo los archivos relevantes para Excel/CSV
    # (Aquí podrías filtrar archivos específicos si es necesario)
    
    # Crear parche de los commits de esta rama
    git format-patch --stdout $(git merge-base origin/main HEAD)..HEAD > "$TEMP_DIR/patches-$branch.patch"
    
    # Aplicar en el nuevo repositorio
    cd "$TEMP_DIR/nuevo"
    
    # Crear nueva rama
    branch_name=$(echo "$branch" | sed 's/cursor\///')
    git checkout -b "$branch_name"
    
    # Intentar aplicar el parche
    if [ -s "$TEMP_DIR/patches-$branch.patch" ]; then
        git am --3way "$TEMP_DIR/patches-$branch.patch" 2>/dev/null || {
            echo -e "${YELLOW}Advertencia: No se pudieron aplicar todos los commits de $branch${NC}"
            git am --abort 2>/dev/null
        }
    fi
    
    cd "$TEMP_DIR/original"
done

cd "$TEMP_DIR/nuevo"

echo -e "\n${GREEN}4. Configurando rama principal...${NC}"
# Volver a main y configurar
git checkout -b main 2>/dev/null || git checkout main

echo -e "\n${GREEN}5. Preparando para push...${NC}"
echo -e "${YELLOW}El nuevo repositorio está listo en: $TEMP_DIR/nuevo${NC}"
echo -e "\n${BLUE}Para completar la migración:${NC}"
echo "1. cd $TEMP_DIR/nuevo"
echo "2. git push -u origin main"
echo "3. git push --all origin"
echo -e "\n${YELLOW}⚠️  Revisa los archivos antes de hacer push${NC}"

# Crear script de limpieza
cat > "$TEMP_DIR/nuevo/limpiar_repo_original.sh" << 'EOF'
#!/bin/bash
# Script para eliminar las ramas de Excel/CSV del repositorio original

echo "Este script eliminará las ramas de Excel/CSV del repositorio original."
echo "¿Estás seguro? (s/n)"
read -r response

if [[ "$response" == "s" ]]; then
    git push origin --delete cursor/bc-b2fec4da-d0d6-42f2-a257-456226942d45-5b25
    git push origin --delete cursor/bc-7b2c1c9b-bcde-49f0-ae20-a5ae47f4266d-39c1
    git push origin --delete cursor/bc-586f43a9-e5f5-4727-bcfb-1d53b417d9c7-cb90
    echo "Ramas eliminadas del repositorio remoto."
fi
EOF

chmod +x "$TEMP_DIR/nuevo/limpiar_repo_original.sh"

echo -e "\n${GREEN}✅ Migración preparada exitosamente${NC}"
echo -e "${BLUE}Encontrarás un script 'limpiar_repo_original.sh' en el nuevo repositorio${NC}"
echo -e "${BLUE}para eliminar las ramas del repositorio original después de verificar la migración.${NC}"