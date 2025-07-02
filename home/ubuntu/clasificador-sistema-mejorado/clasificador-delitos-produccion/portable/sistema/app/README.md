# 🚔 Clasificador de Delitos - Sistema Mejorado

Sistema inteligente para clasificación automática de delitos a partir de planillas Excel, con análisis por IA y generación de reportes situacionales.

## 🔧 **REPARACIONES REALIZADAS**

### ✅ **Problemas Solucionados:**
- ✅ **Clasificación Real**: Activada la versión completa con IA (Gemini + OpenAI)
- ✅ **APIs Configurables**: Sistema de cascada de clasificación inteligente
- ✅ **Procesamiento Real**: Reemplazada simulación por procesamiento real
- ✅ **Base de Datos**: Guardado real de datos clasificados
- ✅ **Exportación**: Excel con datos reales clasificados
- ✅ **Logs**: Sistema completo de auditoría y seguimiento

## 🚀 **Instalación y Configuración**

### **1. Instalar Dependencias**
```bash
cd /workspace/home/ubuntu/clasificador-sistema-mejorado
pip install -r requirements.txt
```

### **2. Configurar APIs (Recomendado)**
```bash
python setup_api_keys.py
```

**O manualmente editando `.env`:**
```env
# Para obtener gratis: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=tu_clave_gemini_aqui

# Para OpenAI (opcional, pago)
OPENAI_API_KEY=tu_clave_openai_aqui
```

### **3. Iniciar el Sistema**
```bash
python src/main.py
```

El servidor estará disponible en: `http://localhost:5000`

## 📊 **Características del Sistema**

### **🤖 Clasificación Inteligente por Cascada**
1. **Gemini AI** (Principal) - Gratis y potente
2. **OpenAI GPT** (Backup) - Opcional
3. **Reglas Básicas** (Fallback) - Siempre disponible
4. **Clasificación por Defecto** - Garantiza funcionamiento

### **📋 Categorías de Clasificación**
- **Jurisdicción**: URBANA, RURAL, MIXTA, OTROS
- **Calificación**: 40+ tipos de delitos específicos
- **Modalidad**: Detalles específicos del tipo de delito
- **Víctimas**: FEMENINO, MASCULINO, AMBOS, OTROS
- **Armas**: FUEGO, BLANCA, IMPROPIA, NINGUNA, OTROS
- **Lugar**: FINCA, VIA_PUBLICA, COMERCIO, EDUCATIVO, OTROS
- **Y más...**

### **📈 Funcionalidades**
- ✅ **Carga de Excel**: Soporte .xlsx y .xls
- ✅ **Procesamiento en Tiempo Real**: Con barra de progreso
- ✅ **Clasificación Automática**: IA + Reglas + Fallback
- ✅ **Exportación Excel**: Resultados formateados
- ✅ **Reportes Situacionales**: Análisis estadístico
- ✅ **Mapas de Calor**: Visualización geográfica
- ✅ **Logs Detallados**: Auditoría completa
- ✅ **API REST**: Integración con otros sistemas

## 🔗 **Endpoints Principales**

### **📤 Subir Archivo**
```http
POST /api/clasificador/upload
Content-Type: multipart/form-data
```

### **⚙️ Procesar Planilla**
```http
POST /api/clasificador/process/{planilla_id}
```

### **📊 Estado del Procesamiento**
```http
GET /api/clasificador/status/{planilla_id}
```

### **📥 Descargar Resultados**
```http
GET /api/clasificador/generate-excel/{planilla_id}
```

### **🧪 Probar Sistema**
```http
GET /api/clasificador/test
```

## 📁 **Formato de Excel Esperado**

### **Columnas Importantes:**
- `relato` / `descripcion` / `detalle` - **Texto principal para clasificar**
- `id_hecho` - Identificador único
- `nro_registro` - Número de registro
- `ipp` - Investigación penal preparatoria
- `fecha_hecho` - Fecha del hecho
- `comisaria` - Comisaría actuante
- `localidad` - Ubicación
- `direccion` - Dirección específica

> **Nota**: El sistema es flexible y detecta automáticamente las columnas disponibles.

## 🎯 **Ejemplo de Uso**

### **1. Subir Archivo**
```bash
curl -X POST -F "file=@planilla_delitos.xlsx" \
     http://localhost:5000/api/clasificador/upload
```

### **2. Procesar**
```bash
curl -X POST http://localhost:5000/api/clasificador/process/1
```

### **3. Ver Progreso**
```bash
curl http://localhost:5000/api/clasificador/status/1
```

### **4. Descargar Resultados**
```bash
curl -O http://localhost:5000/api/clasificador/generate-excel/1
```

## 📊 **Resultados de Clasificación**

Cada delito procesado incluye:
- **Clasificación completa** en todas las categorías
- **Método usado**: GEMINI / OPENAI / REGLAS / DEFECTO
- **Nivel de confianza**: 0.0 a 1.0
- **Tiempo de procesamiento**: en milisegundos
- **Observaciones**: detalles adicionales

## 🗄️ **Estructura de Base de Datos**

### **Modelos Principales:**
- **User**: Usuarios del sistema
- **Planilla**: Archivos subidos
- **HechoDelictivo**: Delitos clasificados
- **PersonaInvolucrada**: Víctimas e imputados
- **LogProcesamiento**: Auditoría de operaciones

## 🛠️ **Solución de Problemas**

### **❌ Error: APIs no configuradas**
```bash
python setup_api_keys.py
```

### **❌ Error: Dependencias faltantes**
```bash
pip install -r requirements.txt
```

### **❌ Error: Base de datos**
```bash
# La base de datos se crea automáticamente
rm src/database/app.db  # Si hay problemas, borrar y reiniciar
python src/main.py
```

### **❌ Error: Puerto ocupado**
```bash
# Cambiar puerto en main.py línea 58:
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📈 **Mejoras Implementadas**

1. **Sistema de Cascada**: Múltiples métodos de clasificación
2. **Validación de Datos**: Limpieza automática de resultados
3. **Logs Detallados**: Seguimiento completo del proceso
4. **Configuración Flexible**: APIs opcionales
5. **Exportación Mejorada**: Excel formateado con todos los datos
6. **Threading Seguro**: Procesamiento asíncrono estable
7. **Manejo de Errores**: Recuperación automática

## 🔮 **Próximas Mejoras Sugeridas**

- [ ] **Frontend React**: Interfaz moderna y responsiva
- [ ] **Autenticación**: Sistema de usuarios completo
- [ ] **Cache Redis**: Acelerar consultas repetitivas
- [ ] **Websockets**: Updates en tiempo real
- [ ] **Docker**: Contenedorización completa
- [ ] **Tests Unitarios**: Cobertura completa
- [ ] **CI/CD**: Pipeline automatizado

## 📞 **Soporte**

### **🧪 Probar el Sistema**
```bash
curl http://localhost:5000/api/clasificador/test
```

### **📋 Ver Planillas**
```bash
curl http://localhost:5000/api/clasificador/planillas
```

### **🔍 Logs del Sistema**
Los logs se muestran en la consola donde ejecutas `python src/main.py`

---

## 🎉 **¡Tu Sistema está Reparado y Funcionando!**

**✅ Clasificación real con IA activada**  
**✅ Procesamiento completo de Excel**  
**✅ Base de datos funcionando**  
**✅ Exportación de resultados**  
**✅ APIs configurables**  

¡Tu clasificador de delitos está listo para producción! 🚀