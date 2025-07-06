# 🔍 Buscador de Palabras en Excel/CSV

Una aplicación web moderna con diseño glassmorphism para buscar texto en archivos Excel y CSV con selector de columnas interactivo.

## ✨ Características

- **Carga de archivos**: Soporta archivos Excel (.xlsx, .xls) y CSV
- **Búsqueda inteligente**: Busca texto en columnas específicas o en todas
- **Selector de columnas estilo Google**: Interfaz intuitiva para seleccionar columnas
- **Resultados detallados**: Muestra fila, columna y contexto de cada coincidencia
- **Diseño glassmorphism**: Interfaz moderna con efectos de vidrio esmerilado
- **Búsqueda sensible a mayúsculas**: Opción para distinguir mayúsculas/minúsculas

## 🎨 Diseño Visual

La aplicación cuenta con un diseño glassmorphism moderno:
- Fondo degradado azul-púrpura
- Efectos de vidrio esmerilado con transparencias
- Botones oscuros con contraste
- Animaciones suaves y transiciones fluidas
- Chips de columnas interactivos

## 🚀 Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 📖 Uso

1. Ejecuta la aplicación:

```bash
python app.py
```

2. Abre tu navegador en: `http://localhost:5000`

3. **Cargar archivo**:
   - Haz clic en "Seleccione su archivo"
   - Elige un archivo Excel o CSV
   - Haz clic en "Cargar Archivo"

4. **Buscar texto**:
   - Selecciona las columnas donde buscar (por defecto todas)
   - Escribe el texto a buscar
   - Opcionalmente activa "Distinguir mayúsculas"
   - Haz clic en "Buscar" o presiona Enter

5. **Ver resultados**:
   - Cada resultado muestra:
     - Número de fila (compatible con Excel)
     - Nombre y número de columna
     - Texto completo de la celda
     - Contexto con otras columnas de la misma fila

## 🎯 Características del Selector de Columnas

- **Chips clickeables**: Haz clic para activar/desactivar columnas
- **Vista compacta**: Muestra las primeras 8 columnas, el resto se oculta
- **Botón "+ X más"**: Expande para ver todas las columnas
- **Controles rápidos**:
  - "Seleccionar Todas": Activa todas las columnas
  - "Deseleccionar Todas": Desactiva todas las columnas
- **Contador dinámico**: Muestra cuántas columnas están seleccionadas

## 🛠️ Requisitos

- Python 3.x
- Flask 2.3.3
- pandas 2.0.3
- openpyxl 3.1.2
- numpy 1.24.3

## 📁 Estructura del Proyecto

```
excel-word-finder/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias Python
├── README.md          # Este archivo
├── templates/         # Templates HTML
│   ├── index.html    # Página de carga de archivos
│   └── search.html   # Página de búsqueda
└── uploads/          # Carpeta temporal para archivos (se crea automáticamente)
```

## 🔧 Configuración

- **Puerto**: 5000 (modificable en app.py)
- **Host**: 0.0.0.0 (accesible desde red local)
- **Modo debug**: Activado por defecto

## 📝 Notas

- Los archivos se procesan en memoria y se eliminan después de cargar
- Soporta múltiples codificaciones para archivos CSV
- Compatible con archivos Excel de diferentes versiones
- La numeración de filas es compatible con Excel (empieza en 1)