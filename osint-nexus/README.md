# OSINT-NEXUS 🔍

**Plataforma de Inteligencia de Fuentes Abiertas Automatizada**

OSINT-NEXUS es una herramienta profesional de investigación que automatiza la recolección, correlación y visualización de inteligencia de fuentes abiertas (OSINT). Diseñada para investigadores de seguridad, analistas de inteligencia y profesionales de ciberseguridad.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Características Principales

### Módulos de Investigación

- **🌐 Análisis de Dominios**
  - Información WHOIS completa
  - Descubrimiento de subdominios
  - Análisis de infraestructura IP
  - Detección de tecnologías web
  - Verificación de certificados SSL
  - Integración con Shodan para análisis de seguridad

- **📧 Investigación de Emails**
  - Verificación de validez y existencia
  - Búsqueda en brechas de datos (HIBP)
  - Identificación de perfiles sociales asociados
  - Análisis de reputación del dominio
  - Evaluación de riesgo automatizada

- **👤 Búsqueda de Nombres de Usuario**
  - Búsqueda en más de 50 plataformas sociales
  - Detección de perfiles activos
  - Análisis de huella digital
  - Categorización por tipo de plataforma

### Características Avanzadas

- 📊 **Visualizaciones Interactivas**: Gráficos y métricas en tiempo real
- 🔗 **Análisis de Correlaciones**: Encuentra conexiones entre investigaciones
- 📄 **Generación de Reportes PDF**: Reportes profesionales automatizados
- 🎨 **Interfaz Moderna**: UI intuitiva con tema oscuro profesional
- 🔒 **Seguridad**: Soporte para proxies y manejo seguro de APIs

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/osint-nexus.git
cd osint-nexus
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar claves API**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus claves API
nano .env  # o usar tu editor preferido
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🔑 Configuración de APIs

OSINT-NEXUS integra múltiples APIs para maximizar la recolección de datos. Crea un archivo `.env` en la raíz del proyecto con las siguientes claves:

```env
# Shodan - https://shodan.io
SHODAN_API_KEY=tu_clave_aqui

# Hunter.io - https://hunter.io
HUNTER_API_KEY=tu_clave_aqui

# Have I Been Pwned - https://haveibeenpwned.com/API/v3
HIBP_API_KEY=tu_clave_aqui

# Criminal IP - https://www.criminalip.io
CRIMINAL_IP_API_KEY=tu_clave_aqui

# URLScan.io - https://urlscan.io
URLSCAN_API_KEY=tu_clave_aqui

# Configuración de Proxy (opcional)
USE_PROXY=false
PROXY_URL=http://tu-proxy:puerto
```

### Obtención de Claves API

1. **Shodan**: Regístrate en [shodan.io](https://shodan.io) y obtén tu API key en la sección de cuenta
2. **Hunter.io**: Crea una cuenta en [hunter.io](https://hunter.io) (plan gratuito disponible)
3. **HIBP**: Dona en [haveibeenpwned.com](https://haveibeenpwned.com/API/v3) para obtener acceso a la API
4. **URLScan.io**: Regístrate gratis en [urlscan.io](https://urlscan.io)

## 📖 Guía de Uso

### 1. Investigación de Dominio

```
1. Selecciona "🌐 Dominio" en el tipo de investigación
2. Ingresa el dominio (ej: ejemplo.com)
3. Haz clic en "🔍 Iniciar Investigación"
```

**Resultados obtenidos:**
- Información WHOIS del dominio
- Subdominios descubiertos
- Tecnologías detectadas
- Análisis de seguridad
- Emails asociados

### 2. Investigación de Email

```
1. Selecciona "📧 Email" en el tipo de investigación
2. Ingresa el email completo
3. Inicia la investigación
```

**Resultados obtenidos:**
- Verificación de validez
- Brechas de datos donde aparece
- Perfiles sociales vinculados
- Evaluación de riesgo

### 3. Búsqueda de Username

```
1. Selecciona "👤 Nombre de Usuario"
2. Ingresa el username/alias
3. Ejecuta la búsqueda
```

**Resultados obtenidos:**
- Perfiles encontrados en múltiples plataformas
- Análisis de presencia digital
- Categorización por tipo de plataforma

## 🛡️ Consideraciones Éticas y Legales

### Uso Responsable

- ✅ **HACER**: Usar para investigaciones legítimas de seguridad
- ✅ **HACER**: Respetar la privacidad de las personas
- ✅ **HACER**: Cumplir con las leyes locales de protección de datos
- ❌ **NO HACER**: Usar para acosar o dañar a personas
- ❌ **NO HACER**: Violar términos de servicio de las plataformas
- ❌ **NO HACER**: Realizar actividades ilegales

### Disclaimer

Esta herramienta está diseñada para uso profesional en investigaciones de seguridad y OSINT éticas. Los usuarios son responsables de cumplir con todas las leyes y regulaciones aplicables en su jurisdicción.

## 🔧 Solución de Problemas

### Error: "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Error: "API key not configured"
Asegúrate de haber creado el archivo `.env` con las claves API correctas

### La aplicación no se abre en el navegador
```bash
streamlit run app.py --server.port 8502
```

### Error de conexión con APIs
- Verifica tu conexión a internet
- Confirma que las claves API sean válidas
- Revisa si necesitas configurar un proxy

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Comunidad OSINT por las mejores prácticas
- Desarrolladores de las APIs integradas
- Contribuidores del proyecto

## 📞 Contacto y Soporte

- 📧 Email: soporte@osint-nexus.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/osint-nexus/issues)
- 💬 Discusiones: [GitHub Discussions](https://github.com/tu-usuario/osint-nexus/discussions)

---

**⚠️ Advertencia**: Esta herramienta debe usarse solo para fines éticos y legales. El mal uso de esta herramienta puede tener consecuencias legales.