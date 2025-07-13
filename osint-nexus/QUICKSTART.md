# 🚀 OSINT-NEXUS - Guía de Inicio Rápido

## Instalación en 3 minutos

### 1️⃣ Instalación Automática (Recomendada)

```bash
cd osint-nexus
python3 setup.py
```

El script de instalación:
- ✅ Verificará Python 3.8+
- ✅ Creará un entorno virtual
- ✅ Instalará todas las dependencias
- ✅ Configurará los archivos necesarios

### 2️⃣ Configurar APIs (Importante)

Edita el archivo `.env` con tus claves API:

```bash
nano .env
```

Agrega al menos una clave API para comenzar:
```env
SHODAN_API_KEY=tu_clave_aqui
```

### 3️⃣ Ejecutar OSINT-NEXUS

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Ejecutar aplicación
streamlit run app.py
```

## 🎯 Primera Investigación

1. **Abre tu navegador** en: http://localhost:8501

2. **Prueba con un dominio**:
   - Selecciona "🌐 Dominio"
   - Ingresa: `example.com`
   - Click en "🔍 Iniciar Investigación"

3. **Explora los resultados**:
   - 📋 Detalles: Información completa
   - 📊 Visualizaciones: Gráficos interactivos
   - 📄 Datos Raw: JSON completo

## 🔑 APIs Gratuitas Recomendadas

### Para empezar gratis:

1. **Shodan** (Free tier)
   - Registro: https://account.shodan.io/register
   - 100 resultados/mes gratis

2. **URLScan.io** (Gratis)
   - Registro: https://urlscan.io/user/signup
   - Sin límites estrictos

3. **Hunter.io** (Free tier)
   - Registro: https://hunter.io/users/sign_up
   - 25 búsquedas/mes gratis

## 💡 Tips Rápidos

- **Sin APIs?** La herramienta funciona con capacidades limitadas
- **Más profundidad?** Agrega más APIs en el archivo `.env`
- **Errores?** Revisa los logs en la terminal
- **Ayuda?** Consulta el README.md completo

## ⚡ Comandos Útiles

```bash
# Ver logs en tiempo real
streamlit run app.py --logger.level debug

# Cambiar puerto
streamlit run app.py --server.port 8502

# Ejecutar en segundo plano
nohup streamlit run app.py &
```

## 🛡️ Recordatorio de Seguridad

- ✅ Usa VPN cuando sea apropiado
- ✅ Respeta los límites de las APIs
- ✅ No investigues sin permiso
- ✅ Cumple las leyes locales

---

¡Listo para investigar! 🔍✨