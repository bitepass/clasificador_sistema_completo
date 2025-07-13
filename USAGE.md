# 📖 Guía de Uso - OSINT-Nexus

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd osint-nexus

# Ejecutar script de instalación
./install.sh

# O instalación manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configuración
Edita el archivo `.env` con tus claves API:
```env
SHODAN_API_KEY=tu_clave_shodan
HUNTER_API_KEY=tu_clave_hunter
HIBP_API_KEY=tu_clave_hibp
```

### 3. Ejecutar
```bash
streamlit run app.py
```

## 🔍 Tipos de Análisis

### Análisis de Dominio
**Objetivo:** Analizar infraestructura digital de un dominio

**Entrada:** `ejemplo.com`

**Herramientas utilizadas:**
- TheHarvester (subdominios)
- Shodan (puertos, servicios, vulnerabilidades)
- Criminal IP (inteligencia de amenazas)
- WHOIS (información de registro)
- DNS (registros DNS)
- SSL (certificados)

**Resultados:**
- Subdominios descubiertos
- Direcciones IP asociadas
- Tecnologías detectadas
- Vulnerabilidades conocidas
- Información de registro
- Certificados SSL

### Análisis de Email
**Objetivo:** Investigar una dirección de email

**Entrada:** `usuario@ejemplo.com`

**Herramientas utilizadas:**
- Hunter.io (verificación, emails relacionados)
- Have I Been Pwned (brechas de datos)
- Epieos (búsqueda inversa)

**Resultados:**
- Verificación de existencia
- Emails relacionados del mismo dominio
- Exposiciones en brechas de datos
- Perfiles sociales asociados
- Información del dominio

### Búsqueda de Usuario
**Objetivo:** Encontrar perfiles en redes sociales

**Entrada:** `usuario123`

**Plataformas verificadas:**
- Redes sociales: Facebook, Twitter, Instagram, LinkedIn
- Plataformas profesionales: GitHub, Behance, Dribbble
- Entretenimiento: YouTube, TikTok, Twitch, Spotify
- Gaming: Steam, Discord
- Blogging: Medium, Tumblr, WordPress

**Resultados:**
- Lista de perfiles encontrados
- URLs de perfiles
- Estadísticas de presencia
- Categorización por tipo de plataforma

### Análisis de Redes Sociales
**Objetivo:** Análisis profundo de un perfil social

**Entrada:** `https://twitter.com/usuario`

**Plataformas soportadas:**
- Twitter/X
- Instagram
- LinkedIn
- Facebook
- YouTube
- TikTok

**Resultados:**
- Información del perfil
- Posts recientes
- Conexiones y seguidores
- Análisis de actividad
- Datos de geolocalización

## 📊 Interpretación de Resultados

### Pestaña de Resumen
- **Métricas principales:** Estadísticas clave del análisis
- **Herramientas utilizadas:** APIs y servicios consultados
- **Duración del análisis:** Tiempo de procesamiento

### Pestaña de Detalles
- **Información específica:** Datos detallados según el tipo de análisis
- **Tablas organizadas:** Resultados en formato tabular
- **Enlaces directos:** URLs para verificación manual

### Pestaña de Grafo de Relaciones
- **Visualización interactiva:** Grafo de conexiones entre entidades
- **Tipos de nodos:** Dominios, emails, usuarios, IPs, etc.
- **Tipos de relaciones:** Conexiones entre entidades
- **Estadísticas del grafo:** Métricas de red

### Pestaña de Estadísticas
- **Gráficos dinámicos:** Visualizaciones según el tipo de análisis
- **Distribuciones:** Análisis de frecuencias y patrones
- **Métricas avanzadas:** Estadísticas detalladas

### Pestaña de Datos Crudos
- **JSON completo:** Datos sin procesar
- **Exportación:** Múltiples formatos de salida
- **Análisis técnico:** Para usuarios avanzados

## 📄 Generación de Reportes

### Reporte PDF
1. Ejecuta un análisis
2. En la barra lateral, haz clic en "📄 Generar Reporte PDF"
3. Descarga el archivo generado

**Contenido del reporte:**
- Página de título con información del análisis
- Resumen ejecutivo
- Detalles técnicos
- Conclusiones y recomendaciones
- Apéndices con metadatos

### Exportación de Datos
- **JSON:** Datos completos en formato JSON
- **CSV:** Datos tabulares para análisis en Excel
- **Grafo:** Estructura de relaciones en formato JSON

## ⚙️ Configuración Avanzada

### Gestión de APIs
```python
# Verificar estado de APIs
from config.api_keys import api_key_manager
status = api_key_manager.get_service_status()
```

### Personalización de Módulos
```python
# Añadir nuevo módulo de análisis
from modules.custom_analyzer import CustomAnalyzer
analyzer = CustomAnalyzer()
results = analyzer.analyze(target)
```

### Configuración de Seguridad
```env
# Habilitar proxy
PROXY_URL=http://proxy:port

# Configurar retención de datos
DATA_RETENTION_HOURS=24

# Habilitar Tor (experimental)
ENABLE_TOR=true
```

## 🔧 Solución de Problemas

### Error: "API Key inválida"
1. Verifica que la clave API esté correctamente configurada en `.env`
2. Confirma que la clave tenga permisos suficientes
3. Revisa los límites de uso de la API

### Error: "Timeout en la conexión"
1. Verifica tu conexión a internet
2. Considera usar un proxy si es necesario
3. Aumenta el timeout en la configuración

### Error: "Módulo no encontrado"
1. Verifica que todas las dependencias estén instaladas
2. Ejecuta `pip install -r requirements.txt`
3. Reinicia el entorno virtual

### Rendimiento lento
1. Verifica la velocidad de tu conexión
2. Considera usar menos APIs simultáneamente
3. Ajusta los timeouts en la configuración

## 📈 Mejores Prácticas

### Ética y Legalidad
- ✅ Usar únicamente para investigaciones legítimas
- ✅ Respetar términos de servicio de las plataformas
- ✅ No realizar actividades de acoso o espionaje
- ✅ Mantener confidencialidad de la información

### Seguridad Operacional
- 🔒 Usar VPN o proxy cuando sea necesario
- 🔒 No almacenar datos sensibles permanentemente
- 🔒 Rotar claves API regularmente
- 🔒 Monitorear el uso de APIs

### Optimización
- ⚡ Configurar solo las APIs necesarias
- ⚡ Usar timeouts apropiados
- ⚡ Implementar rate limiting
- ⚡ Cachear resultados cuando sea posible

## 🆘 Soporte

### Recursos Adicionales
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [API de Shodan](https://developer.shodan.io/)
- [API de Hunter.io](https://hunter.io/api-keys)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)

### Comunidad
- GitHub Issues para reportar bugs
- Discord para soporte comunitario
- Wiki para documentación adicional

### Contribuciones
1. Fork el proyecto
2. Crea una rama para tu feature
3. Implementa los cambios
4. Añade tests si es necesario
5. Envía un Pull Request

---

**⚠️ Disclaimer:** Esta herramienta está diseñada únicamente para investigaciones legítimas y éticas. Es responsabilidad del usuario asegurar que su uso cumple con todas las leyes y regulaciones aplicables.