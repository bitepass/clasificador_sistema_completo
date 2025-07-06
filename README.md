# 🔍 Buscador de Texto en Excel/CSV

Un programa web completo en Python que permite subir archivos Excel (.xlsx, .xls) o CSV, leer todas las columnas automáticamente y buscar texto con un selector de columnas avanzado.

## ✨ Características

- **Carga de archivos**: Soporta Excel (.xlsx, .xls) y CSV
- **Detección automática**: Codificación automática para archivos CSV
- **Selector de columnas**: Interfaz estilo Google con chips clickeables
- **Búsqueda avanzada**: Sensible a mayúsculas/minúsculas opcional
- **Resultados detallados**: Muestra fila, columna, texto completo y contexto
- **Interfaz moderna**: Diseño glassmorphism con efectos visuales

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone [url-del-repositorio]
cd buscador-excel-csv
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el programa

```bash
python app.py
```

### 4. Abrir en el navegador

Abre tu navegador web en: `http://localhost:5000`

## 📋 Uso

### Paso 1: Cargar archivo
- Haz clic en "Seleccionar archivo" y elige tu archivo Excel o CSV
- El programa detectará automáticamente el formato y codificación
- Verás información sobre el archivo cargado

### Paso 2: Seleccionar columnas
- Todas las columnas están seleccionadas por defecto
- Haz clic en los chips de columnas para seleccionar/deseleccionar
- Usa "Seleccionar Todas" o "Deseleccionar Todas" para control rápido
- Si hay más de 8 columnas, usa "+ X más" para ver todas

### Paso 3: Buscar texto
- Ingresa la palabra o texto que deseas buscar
- Opcional: Marca "Distinguir mayúsculas" para búsqueda sensible a mayúsculas
- Haz clic en "Buscar" o presiona Enter

### Paso 4: Ver resultados
- Los resultados muestran:
  - Número de fila (compatible con Excel)
  - Nombre y número de columna
  - Texto completo de la celda
  - Contexto de la fila completa

## 🎯 Casos de uso

- **Búsqueda de nombres**: Solo en columnas de nombres/apellidos
- **Búsqueda de fechas**: Solo en columnas de fechas
- **Búsqueda de códigos**: Solo en columnas de IDs/códigos
- **Análisis de datos**: Excluir columnas irrelevantes
- **Auditoría**: Encontrar información específica con contexto

## 🔧 Dependencias

- **Flask**: Framework web
- **pandas**: Manejo de datos
- **openpyxl**: Archivos Excel nuevos (.xlsx)
- **xlrd**: Archivos Excel antiguos (.xls)
- **Werkzeug**: Utilidades web
- **numpy**: Cálculos numéricos

## 🌟 Características técnicas

- **Detección automática de encoding**: UTF-8, Latin1, CP1252, ISO-8859-1
- **Validación de archivos**: Solo permite formatos soportados
- **Búsqueda en memoria**: Rápida y eficiente
- **Interfaz responsive**: Funciona en móviles y escritorio
- **Búsqueda asíncrona**: No bloquea la interfaz

## 🎨 Interfaz

- **Diseño glassmorphism**: Efectos de vidrio esmerilado
- **Colores**: Gradientes azules con transparencias
- **Animaciones**: Hover effects y transiciones suaves
- **Tipografía**: Segoe UI moderna

## 📱 Compatibilidad

- **Python**: 3.7+
- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Sistemas**: Windows, macOS, Linux
- **Archivos**: Excel 2007+, CSV con cualquier encoding

## 🔒 Seguridad

- Validación de tipos de archivo
- Nombres de archivo seguros
- Eliminación automática de archivos temporales
- Sin almacenamiento permanente de datos

## 🚨 Solución de problemas

### Error "No se pudo leer el archivo CSV"
- Verifica que el archivo no esté corrupto
- Intenta guardar el CSV con codificación UTF-8

### Error "Tipo de archivo no permitido"
- Solo se aceptan archivos .csv, .xlsx, .xls
- Verifica la extensión del archivo

### El servidor no inicia
- Verifica que tengas instaladas todas las dependencias
- Ejecuta: `pip install -r requirements.txt`

## 📞 Soporte

Para problemas o sugerencias:
1. Verifica que todas las dependencias estén instaladas
2. Comprueba la consola para errores
3. Reinicia el servidor con `python app.py`

## 🔄 Actualizaciones

El programa se actualiza automáticamente al reiniciar el servidor. Para obtener nuevas funciones, actualiza los archivos y reinicia.

---

**¡Disfruta buscando en tus archivos Excel y CSV! 🎉**