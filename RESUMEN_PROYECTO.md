# 🔍 BUSCADOR DE PALABRAS EN EXCEL/CSV - PROYECTO COMPLETO

## 🎯 ¿QUÉ ES?
Un programa web completo en Python que permite subir archivos Excel (.xlsx, .xls) o CSV, leer automáticamente todas las columnas, y buscar cualquier palabra con un selector de columnas avanzado estilo Google.

## ✨ CARACTERÍSTICAS PRINCIPALES

### 📂 Carga de Archivos
- ✅ Soporta Excel (.xlsx, .xls) y CSV
- ✅ Detección automática de codificación (UTF-8, Latin1, CP1252, ISO-8859-1)
- ✅ Validación de tipos de archivo
- ✅ Manejo de errores robusto

### 🔍 Búsqueda Avanzada
- ✅ Búsqueda en columnas específicas (selector tipo Google)
- ✅ Búsqueda sensible a mayúsculas/minúsculas
- ✅ Resultados detallados con contexto completo
- ✅ Numeración compatible con Excel

### 🎛️ Selector de Columnas
- ✅ Chips clickeables estilo Google
- ✅ Mostrar/ocultar columnas dinámicamente
- ✅ Seleccionar/deseleccionar todas
- ✅ Contador de columnas seleccionadas

### 🎨 Interfaz Moderna
- ✅ Diseño glassmorphism (vidrio esmerilado)
- ✅ Gradientes azules con transparencias
- ✅ Efectos hover y animaciones
- ✅ Responsive para móvil y escritorio

## 📁 ESTRUCTURA DEL PROYECTO

```
buscador-excel-csv/
├── app.py                    # Aplicación principal Flask
├── requirements.txt          # Dependencias
├── README.md                # Documentación completa
├── INICIO_RAPIDO.md         # Guía de inicio rápido
├── config.py                # Configuración del sistema
├── instalar.py              # Script de instalación automática
├── ejecutar.py              # Script de ejecución automática
├── ejemplo_datos.csv        # Datos de ejemplo para pruebas
├── templates/               # Templates HTML
│   ├── index.html          # Página principal
│   └── search.html         # Página de búsqueda
└── uploads/                # Directorio temporal (auto-creado)
```

## 🚀 INSTALACIÓN Y USO

### Instalación Rápida
```bash
# 1. Instalar dependencias
python instalar.py

# 2. Ejecutar programa
python app.py

# 3. Abrir navegador
# Ve a: http://localhost:5000
```

### Instalación Manual
```bash
# 1. Instalar dependencias
pip install --break-system-packages Flask pandas openpyxl xlrd Werkzeug numpy

# 2. Ejecutar
python app.py
```

## 🔧 DEPENDENCIAS TÉCNICAS

- **Flask 3.1.1**: Framework web
- **pandas 2.3.0**: Manejo de datos
- **openpyxl 3.1.5**: Archivos Excel nuevos
- **xlrd 2.0.2**: Archivos Excel antiguos
- **Werkzeug 3.1.3**: Utilidades web
- **numpy 2.3.1**: Cálculos numéricos

## 📋 FUNCIONALIDADES DETALLADAS

### 1. Carga de Archivos
- Interfaz drag & drop visual
- Validación automática de formatos
- Detección de encoding para CSV
- Información detallada del archivo cargado

### 2. Selector de Columnas
- Chips visuales clickeables
- Primeras 8 columnas siempre visibles
- Botón "mostrar más" para archivos grandes
- Controles "seleccionar todas" / "deseleccionar todas"
- Contador dinámico de columnas seleccionadas

### 3. Búsqueda
- Campo de búsqueda prominente
- Búsqueda por Enter o botón
- Checkbox para sensibilidad a mayúsculas
- Validación de entrada

### 4. Resultados
- Número de fila exacto (compatible con Excel)
- Nombre y número de columna
- Texto completo de la celda
- Contexto completo de la fila
- Contador de resultados encontrados

## 🎨 DISEÑO VISUAL

### Estilo Glassmorphism
- Fondo: Gradiente azul-púrpura
- Contenedores: Vidrio esmerilado con blur
- Transparencias: rgba(255, 255, 255, 0.15)
- Botones: Oscuros con efectos hover
- Animaciones: Suaves y elegantes

### Efectos Especiales
- Textura de fondo con patrones sutiles
- Hover effects con elevación
- Blur effects en diferentes niveles
- Transiciones fluidas de 0.3s

## 🎯 CASOS DE USO REALES

### Búsqueda de Personas
- Buscar nombres solo en columnas de nombres
- Encontrar personas por apellido
- Localizar contactos específicos

### Análisis de Datos
- Buscar fechas en columnas específicas
- Encontrar códigos en columnas de IDs
- Filtrar resultados por categorías

### Auditoría y Control
- Verificar información específica
- Encontrar inconsistencias
- Auditar datos con contexto completo

## 📊 DATOS DE EJEMPLO

El archivo `ejemplo_datos.csv` incluye:
- 15 registros de empleados
- 9 columnas: ID, Nombre, Apellido, Email, Teléfono, Ciudad, Empresa, Cargo, Salario
- Datos realistas para pruebas

### Búsquedas Sugeridas
- "Madrid" → Encuentra en columna Ciudad
- "Desarrollador" → Encuentra en columna Cargo
- "TechCorp" → Encuentra en columna Empresa
- "45000" → Encuentra en columna Salario

## 🔒 SEGURIDAD

- Validación de tipos de archivo
- Nombres de archivo seguros (secure_filename)
- Eliminación automática de archivos temporales
- Sin almacenamiento permanente de datos sensibles
- Configuración de límites de tamaño

## 📱 COMPATIBILIDAD

### Navegadores
- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅

### Sistemas Operativos
- Windows ✅
- macOS ✅
- Linux ✅

### Formatos de Archivo
- CSV (cualquier encoding) ✅
- Excel 2007+ (.xlsx) ✅
- Excel 97-2003 (.xls) ✅

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error de Dependencias
```bash
pip install --break-system-packages Flask pandas openpyxl xlrd Werkzeug numpy
```

### Puerto Ocupado
- Cerrar otros servidores en puerto 5000
- Editar puerto en `app.py`

### Archivo No Se Carga
- Verificar extensión (.csv, .xls, .xlsx)
- Probar con archivo de ejemplo
- Verificar que no esté corrupto

## 📈 RENDIMIENTO

- Carga en memoria para búsquedas rápidas
- Búsqueda asíncrona sin bloqueo
- Interfaz responsive
- Optimizado para archivos grandes

## 🔄 FUTURAS MEJORAS

Posibles mejoras profesionales:
- Base de datos para múltiples archivos
- Exportar resultados de búsqueda
- Búsqueda con expresiones regulares
- Filtros avanzados por tipo de dato
- Historial de búsquedas
- Modo batch para múltiples archivos

## 👥 CONTRIBUCIÓN

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear rama feature
3. Hacer commits descriptivos
4. Crear pull request

## 📞 SOPORTE

Para problemas o dudas:
1. Revisar documentación completa
2. Verificar instalación de dependencias
3. Comprobar compatibilidad del archivo
4. Reiniciar servidor si es necesario

---

## 🎉 CONCLUSIÓN

Este proyecto implementa completamente todas las funcionalidades solicitadas:

✅ **Subida de archivos Excel/CSV**  
✅ **Lectura automática de columnas**  
✅ **Búsqueda avanzada de palabras**  
✅ **Selector de columnas estilo Google**  
✅ **Resultados detallados con contexto**  
✅ **Interfaz web moderna glassmorphism**  
✅ **Manejo robusto de errores**  
✅ **Documentación completa**  
✅ **Scripts de instalación automática**  
✅ **Datos de ejemplo para pruebas**  

**¡El buscador está listo para usar! 🚀**