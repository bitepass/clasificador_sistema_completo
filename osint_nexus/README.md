# 🔍 OSINT-Nexus

**Plataforma de Inteligencia Automatizada para Investigación de Fuentes Abiertas**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/osint-nexus/osint-nexus)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29+-orange.svg)](https://streamlit.io)

## 🎯 Descripción

OSINT-Nexus es una plataforma web moderna y potente diseñada para automatizar la recolección, correlación y visualización de inteligencia de fuentes abiertas (OSINT). Permite a investigadores, analistas de seguridad y profesionales de ciberseguridad realizar investigaciones completas mediante la integración de múltiples APIs y herramientas especializadas.

### ✨ Características Principales

- **🌐 Análisis de Dominios**: Infraestructura, DNS, SSL, tecnologías y seguridad
- **📧 Investigación de Emails**: Validación, brechas de datos, perfiles sociales
- **👤 Búsqueda de Usernames**: Presencia en múltiples plataformas sociales
- **📱 Análisis de Redes Sociales**: Perfiles, contenido, metadatos y conexiones
- **🔄 Procesamiento Concurrente**: Múltiples consultas en paralelo
- **📊 Reportes Avanzados**: JSON, CSV, HTML, PDF
- **🛡️ Enfoque Ético**: Cumplimiento legal y mejores prácticas
- **⚡ Interfaz Intuitiva**: Dashboard moderno con Streamlit

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación Automática

```bash
# Clonar el repositorio
git clone https://github.com/osint-nexus/osint-nexus.git
cd osint_nexus

# Ejecutar instalador automático
python install.py
```

### Instalación Manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir logs reports data temp

# Configurar variables de entorno
cp .env.example .env
# Editar .env con sus claves de API
```

## 📋 Configuración

### Variables de Entorno

Copie el archivo `.env.example` como `.env` y configure sus claves de API:

```env
# APIs de servicios OSINT
SHODAN_API_KEY=tu_clave_shodan
HUNTER_API_KEY=tu_clave_hunter
HIBP_API_KEY=tu_clave_hibp
VIRUSTOTAL_API_KEY=tu_clave_virustotal
URLSCAN_API_KEY=tu_clave_urlscan

# Configuración de proxy (opcional)
HTTP_PROXY=http://proxy:8080
HTTPS_PROXY=https://proxy:8080
```

### APIs Soportadas

| Servicio | Funcionalidad | Clave Requerida |
|----------|---------------|-----------------|
| **Shodan** | Análisis de infraestructura | ✅ |
| **Hunter.io** | Verificación de emails | ✅ |
| **Have I Been Pwned** | Brechas de datos | ✅ |
| **VirusTotal** | Análisis de malware | ✅ |
| **URLScan.io** | Análisis de sitios web | ✅ |
| **Whois** | Información de dominios | ❌ |
| **DNS** | Registros DNS | ❌ |

## 🎮 Uso

### Ejecución

```bash
# Iniciar la aplicación
streamlit run app.py

# Opciones adicionales
streamlit run app.py --server.port 8080
streamlit run app.py --server.headless true
```

### Tipos de Investigación

#### 1. **Análisis de Dominios**
```
Entrada: ejemplo.com
Funcionalidades:
- Información WHOIS
- Registros DNS (A, AAAA, MX, NS, TXT)
- Análisis de SSL/TLS
- Detección de tecnologías
- Headers de seguridad
- Escaneo de puertos
- Geolocalización
- Subdominios
```

#### 2. **Investigación de Emails**
```
Entrada: usuario@ejemplo.com
Funcionalidades:
- Validación de formato
- Verificación de dominio
- Búsqueda en brechas de datos
- Análisis de reputación
- Detección de emails desechables
- Perfiles sociales asociados
- Gravatar
```

#### 3. **Búsqueda de Usernames**
```
Entrada: nombreusuario
Funcionalidades:
- Verificación en 15+ plataformas sociales
- Análisis de patrones
- Variantes de usernames
- Evaluación de seguridad
- Estadísticas de presencia
- Información adicional de perfiles
```

#### 4. **Análisis de Redes Sociales**
```
Entrada: https://twitter.com/usuario
Funcionalidades:
- Información del perfil
- Análisis de contenido
- Metadatos
- Sentimientos
- Hashtags y menciones
- Conexiones
```

### Flujo de Trabajo

1. **Ingreso de Objetivo**: Introducir dominio, email, username o URL
2. **Detección Automática**: El sistema identifica el tipo de objetivo
3. **Selección de Módulo**: Automática o manual
4. **Análisis Concurrente**: Múltiples APIs en paralelo
5. **Procesamiento**: Correlación y enriquecimiento de datos
6. **Visualización**: Dashboard interactivo con resultados
7. **Exportación**: Reportes en múltiples formatos

## 🏗️ Arquitectura

### Estructura del Proyecto

```
osint_nexus/
├── app.py                 # Interfaz principal Streamlit
├── config.py              # Configuración global
├── install.py             # Instalador automático
├── requirements.txt       # Dependencias Python
├── .env.example          # Plantilla de variables de entorno
├── README.md             # Documentación
├── modules/              # Módulos de investigación
│   ├── domain_analyzer.py
│   ├── email_analyzer.py
│   ├── username_analyzer.py
│   └── social_analyzer.py
├── utils/                # Utilidades del sistema
│   ├── logger.py
│   ├── validators.py
│   ├── api_client.py
│   └── report_generator.py
├── static/               # Archivos estáticos
├── reports/              # Reportes generados
├── logs/                 # Archivos de log
└── data/                 # Datos temporales
```

### Arquitectura Técnica

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
├─────────────────────────────────────────────────────────────┤
│                  Núcleo de Aplicación                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Validadores│  │   Logger    │  │API Cliente  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    Módulos OSINT                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Dominio   │  │    Email    │  │  Username   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Social    │  │   Reportes  │  │   Datos     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                   APIs Externas                            │
│  Shodan | Hunter.io | HIBP | VirusTotal | URLScan | etc.  │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis de Dominio

```python
# Investigar example.com
target = "example.com"
results = domain_analyzer.analyze_domain(target)

# Resultados incluyen:
# - IP: 93.184.216.34
# - Registrador: IANA
# - Tecnologías: Apache, HTML5
# - Seguridad: Rating B
# - Subdominios: www.example.com
```

### Ejemplo 2: Investigación de Email

```python
# Verificar email
target = "test@example.com"
results = email_analyzer.analyze_email(target)

# Resultados incluyen:
# - Formato: Válido
# - Dominio: Existe
# - Brechas: 0 encontradas
# - Reputación: 85/100
```

### Ejemplo 3: Búsqueda de Username

```python
# Buscar username en redes sociales
target = "johndoe"
results = username_analyzer.analyze_username(target)

# Resultados incluyen:
# - Plataformas: 15 verificadas
# - Encontrado: 8 plataformas
# - Disponible: 7 plataformas
# - Presencia: 53.3%
```

## 🔒 Consideraciones Éticas y Legales

### Principios Fundamentales

1. **Fuentes Públicas**: Solo información de acceso público
2. **Uso Legítimo**: Investigación, seguridad, análisis de riesgos
3. **Privacidad**: Respeto a la privacidad individual
4. **Cumplimiento Legal**: Adherencia a leyes locales e internacionales
5. **Transparencia**: Documentación clara de metodologías

### Aviso Legal

⚠️ **IMPORTANTE**: Este software está diseñado para investigación de inteligencia en fuentes abiertas con fines legítimos y éticos. El usuario es responsable de:

- Cumplir con todas las leyes aplicables
- Respetar términos de servicio de APIs
- Usar la información de manera responsable
- No realizar actividades ilegales o no éticas

### Mejores Prácticas

- ✅ Investigación de seguridad autorizada
- ✅ Análisis de amenazas cibernéticas
- ✅ Due diligence empresarial
- ✅ Investigación periodística
- ❌ Acoso o intimidación
- ❌ Violación de privacidad
- ❌ Actividades ilegales

## 🛠️ Desarrollo

### Contribuir al Proyecto

1. Fork del repositorio
2. Crear rama de feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Estructura de Módulos

Para crear un nuevo módulo de investigación:

```python
class NuevoAnalyzer:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.results = {}
    
    def analyze_target(self, target: str) -> Dict[str, Any]:
        # Implementar lógica de análisis
        return results
    
    def generate_summary(self) -> Dict[str, Any]:
        # Generar resumen de resultados
        return summary
```

### Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Coverage
python -m pytest --cov=osint_nexus tests/
```

## 📈 Roadmap

### Versión 1.1.0
- [ ] Integración con más APIs (Maltego, Spyse, etc.)
- [ ] Análisis de números de teléfono
- [ ] Búsqueda en darkweb
- [ ] Dashboard de administración

### Versión 1.2.0
- [ ] Machine Learning para correlación
- [ ] API REST para integraciones
- [ ] Alertas y monitoreo
- [ ] Colaboración en equipo

### Versión 2.0.0
- [ ] Arquitectura distribuida
- [ ] Análisis de imágenes
- [ ] Inteligencia artificial
- [ ] Automatización avanzada

## 🤝 Soporte y Comunidad

### Obtener Ayuda

- 📖 **Documentación**: [Wiki del proyecto](https://github.com/osint-nexus/osint-nexus/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/osint-nexus/osint-nexus/discussions)
- 🐛 **Issues**: [Reportar problemas](https://github.com/osint-nexus/osint-nexus/issues)
- 📧 **Email**: support@osint-nexus.com

### Comunidad

- 🌐 **Website**: [https://osint-nexus.com](https://osint-nexus.com)
- 🐦 **Twitter**: [@OSINTNexus](https://twitter.com/OSINTNexus)
- 💼 **LinkedIn**: [OSINT-Nexus](https://linkedin.com/company/osint-nexus)

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Shodan**: Por proporcionar datos de infraestructura
- **Hunter.io**: Por servicios de verificación de email
- **Have I Been Pwned**: Por datos de brechas de seguridad
- **VirusTotal**: Por análisis de malware
- **Streamlit**: Por el framework de interfaz web
- **Comunidad OSINT**: Por herramientas y metodologías

---

<div align="center">

**🔍 OSINT-Nexus - Inteligencia Automatizada para el Mundo Digital**

[![Stars](https://img.shields.io/github/stars/osint-nexus/osint-nexus?style=social)](https://github.com/osint-nexus/osint-nexus)
[![Forks](https://img.shields.io/github/forks/osint-nexus/osint-nexus?style=social)](https://github.com/osint-nexus/osint-nexus)
[![Issues](https://img.shields.io/github/issues/osint-nexus/osint-nexus)](https://github.com/osint-nexus/osint-nexus/issues)

</div>