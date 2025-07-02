# 🎨 Frontend Sistema Clasificador de Delitos

Frontend moderno con diseño **glassmorphism** para el sistema de clasificación automática de delitos.

## ✨ Características

### 🎯 **Funcionalidades Principales**
- **Subida de archivos Excel** con drag & drop
- **Procesamiento en tiempo real** con barra de progreso animada
- **Temporizador dinámico** que estima tiempo restante
- **Descarga de resultados** en formato Excel clasificado
- **Generación de informes** situacionales y estadísticos
- **Navegación fluida** entre módulos

### 🎨 **Diseño Glassmorphism Avanzado**
- Tarjetas translúcidas con efecto de vidrio esmerilado
- Partículas animadas de fondo
- Sombras interiores y exteriores tipo neón
- Botones con efectos hover y animaciones pulsantes
- Barras de progreso con efecto shimmer
- Responsive design para móviles y tablets

### 🔧 **Tecnologías**
- **HTML5** + **CSS3** puro (sin frameworks)
- **JavaScript ES6+** vanilla
- **Font Awesome** para iconografía
- **Fetch API** para comunicación con backend
- **CSS Grid** y **Flexbox** para layouts responsivos

## 📁 Estructura de Archivos

```
src/static/
├── index.html          # Página principal - Clasificador
├── reports.html        # Generador de informes
└── assets/            # (opcional para recursos adicionales)
```

## 🚀 Instalación y Configuración

### 1. **Configurar Backend**
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar variables de entorno
nano .env
```

### 2. **Configurar APIs (Obligatorio)**
Edita el archivo `.env` con tus claves:
```env
GEMINI_API_KEY=tu_clave_gemini_aqui
OPENAI_API_KEY=tu_clave_openai_aqui
SECRET_KEY=tu_clave_secreta_aqui
```

### 3. **Ejecutar el Sistema**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python src/main.py
```

### 4. **Acceder al Frontend**
- **Clasificador:** `http://localhost:5000`
- **Informes:** `http://localhost:5000/reports.html`

## 🎯 Guía de Uso

### 📊 **Módulo Clasificador** (`index.html`)

#### **Paso 1: Subir Archivo**
1. Arrastra un archivo Excel (.xlsx/.xls) a la zona de carga
2. O haz clic para seleccionar archivo
3. Verifica la información del archivo mostrada

#### **Paso 2: Procesar**
1. Clic en "**Procesar Archivo**"
2. Observa la barra de progreso en tiempo real
3. El temporizador muestra tiempo estimado restante
4. Puedes cancelar en cualquier momento

#### **Paso 3: Descargar Resultados**
1. Al completarse, aparece el botón "**Descargar Excel Clasificado**"
2. El archivo incluye todas las clasificaciones automáticas
3. Opción de procesar nuevo archivo o generar informes

### 📈 **Módulo Informes** (`reports.html`)

#### **Paso 1: Seleccionar Tipo**
- **Situacional:** Análisis completo de delitos
- **Estadístico:** Datos numéricos y tendencias  
- **Comparativo:** Comparación entre períodos
- **Ejecutivo:** Síntesis para autoridades

#### **Paso 2: Configurar Parámetros**
- **Partido:** Seleccionar jurisdicción
- **Fechas:** Período de análisis
- **Formato:** PDF, Word o Excel

#### **Paso 3: Vista Previa y Generación**
- Clic en "**Vista Previa**" para ver resumen
- Clic en "**Generar Informe**" para descargar

## 🔧 Configuración Avanzada

### **Variables de Entorno Frontend**
El frontend detecta automáticamente la URL base del servidor. Para entornos de producción:

```javascript
// En index.html y reports.html, línea ~680
const API_BASE = window.location.origin; // Detecta automáticamente

// Para URL personalizada:
const API_BASE = 'https://tu-servidor.com';
```

### **CORS Configuration**
En `src/main.py`, línea 20:
```python
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000', 'https://tu-dominio.com'])
```

### **Límites de Archivo**
En `.env`:
```env
MAX_CONTENT_LENGTH=52428800  # 50MB máximo
```

## 🎨 Personalización Visual

### **Colores del Tema**
```css
/* Variables principales en ambos archivos HTML */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--success-color: #4CAF50;
--danger-color: #f44336;
--warning-color: #FF9800;
```

### **Efectos Glassmorphism**
```css
.glass-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
}
```

### **Partículas de Fondo**
Modifica la cantidad en JavaScript:
```javascript
const particleCount = 50; // Cambiar número de partículas
```

## 📱 Responsive Design

### **Breakpoints**
- **Desktop:** > 768px (layout completo)
- **Tablet:** 768px - 480px (grid adaptativo)
- **Mobile:** < 480px (columna única)

### **Características Móviles**
- Navegación vertical en móviles
- Botones táctiles optimizados
- Texto y elementos escalables
- Gestos drag & drop funcionales

## 🔒 Seguridad

### **Validaciones Frontend**
- Tipos de archivo permitidos: `.xlsx`, `.xls`
- Tamaño máximo: 50MB
- Validación de fechas en informes
- Sanitización de inputs

### **Comunicación Segura**
- Requests HTTPS en producción
- Headers de seguridad configurados
- Manejo de errores sin exposición de datos

## 🐛 Solución de Problemas

### **Error: "Failed to fetch"**
```javascript
// Verificar configuración de API_BASE
const API_BASE = window.location.origin;

// O configurar manualmente:
const API_BASE = 'http://localhost:5000';
```

### **CORS Errors**
Agregar tu dominio en `src/main.py`:
```python
CORS(app, origins=['tu-dominio.com'])
```

### **Archivos no se procesan**
1. Verificar que las APIs estén configuradas
2. Revisar logs del servidor: `tail -f logs/app.log`
3. Verificar formato del Excel

### **Informes no se generan**
1. Verificar que existan datos procesados
2. Comprobar configuración de fechas
3. Revisar permisos de escritura

## 🚀 Despliegue en Producción

### **Opción 1: Servidor Tradicional**
```bash
# Copiar archivos estáticos
cp -r src/static/* /var/www/html/

# Configurar servidor web (nginx/apache)
# Proxy reverso a Flask en puerto 5000
```

### **Opción 2: Docker**
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "src/main.py"]
```

### **Variables de Producción**
```env
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
```

## 📞 Soporte

### **Logs y Debugging**
- Logs del servidor: `logs/app.log`
- Console del navegador: F12 → Console
- Network tab para requests fallidos

### **Contacto**
Para soporte técnico o consultas sobre el frontend, revisar:
1. Logs del navegador (F12)
2. Logs del servidor Flask
3. Configuración de variables de entorno
4. Estados de la base de datos

---

## 🎉 **¡Listo para usar!**

El frontend está completamente integrado con tu backend Flask. Solo necesitas:
1. ✅ Configurar las API keys
2. ✅ Ejecutar `python src/main.py`
3. ✅ Abrir `http://localhost:5000`

**¡Tu sistema clasificador con diseño glassmorphism está funcionando!** 🚀