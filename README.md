# 🕵️ OSINT-Nexus: Plataforma de Inteligencia Automatizada

## 📋 Descripción

OSINT-Nexus es una plataforma web modular e intuitiva que automatiza la recolección, correlación y visualización de Inteligencia de Fuentes Abiertas (OSINT). Permite a investigadores introducir un único dato (dominio, email, nombre de usuario, etc.) y recibir un informe de inteligencia consolidado y enriquecido.

## 🎯 Características Principales

- **Interfaz Web Intuitiva**: Desarrollada con Streamlit para una experiencia de usuario fluida
- **Módulos Especializados**: Análisis de dominios, emails, nombres de usuario y redes sociales
- **Integración Multi-API**: Conecta con múltiples herramientas OSINT especializadas
- **Visualización de Datos**: Grafos de relaciones y dashboards interactivos
- **Reportes Automatizados**: Generación de informes en PDF
- **Arquitectura Modular**: Fácil extensión y personalización

## 🏗️ Arquitectura

```
osint-nexus/
├── app.py                 # Aplicación principal Streamlit
├── config/
│   ├── __init__.py
│   ├── settings.py        # Configuración general
│   └── api_keys.py        # Gestión de claves API
├── modules/
│   ├── __init__.py
│   ├── domain_analyzer.py # Módulo de análisis de dominios
│   ├── email_analyzer.py  # Módulo de análisis de emails
│   ├── username_analyzer.py # Módulo de análisis de usuarios
│   └── social_analyzer.py # Módulo de análisis social
├── utils/
│   ├── __init__.py
│   ├── network_graph.py   # Generación de grafos
│   ├── report_generator.py # Generación de reportes
│   └── data_processor.py  # Procesamiento de datos
├── static/
│   ├── css/
│   └── images/
└── requirements.txt
```

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd osint-nexus
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus claves API
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

## 🔧 Configuración

### Claves API Requeridas

Para obtener el máximo rendimiento, configura las siguientes claves API:

- **Shodan**: [https://account.shodan.io/register](https://account.shodan.io/register)
- **Hunter.io**: [https://hunter.io/api-keys](https://hunter.io/api-keys)
- **Have I Been Pwned**: [https://haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key)

### Archivo .env
```env
SHODAN_API_KEY=tu_clave_shodan
HUNTER_API_KEY=tu_clave_hunter
HIBP_API_KEY=tu_clave_hibp
CRIMINAL_IP_API_KEY=tu_clave_criminal_ip
```

## 📖 Uso

### 1. Análisis de Dominio
- Selecciona "Dominio" en el menú desplegable
- Introduce el dominio (ej: ejemplo.com)
- Obtén información sobre infraestructura, subdominios, tecnologías

### 2. Análisis de Email
- Selecciona "Email" en el menú desplegable
- Introduce la dirección de email
- Descubre exposiciones en brechas, perfiles sociales asociados

### 3. Búsqueda de Usuario
- Selecciona "Nombre de Usuario" en el menú desplegable
- Introduce el alias
- Encuentra presencia en redes sociales

### 4. Análisis Social
- Selecciona "Red Social" en el menú desplegable
- Introduce la URL del perfil
- Analiza conexiones y actividad

## 🛡️ Consideraciones Éticas y Legales

### Principios Fundamentales
- **Solo fuentes públicas**: El sistema únicamente consulta información de acceso público
- **Respeto a la privacidad**: Cumple con normativas de protección de datos
- **Uso ético**: La herramienta debe usarse para investigaciones legítimas
- **No almacenamiento**: Los datos sensibles no se almacenan permanentemente

### Responsabilidad del Usuario
- Verificar la legalidad de cada investigación
- Respetar términos de servicio de las plataformas
- No usar para acoso o actividades maliciosas
- Mantener confidencialidad de la información obtenida

## 🔄 Módulos Disponibles

### Módulo 1: Análisis de Dominio
- **Herramientas**: TheHarvester, Shodan, Criminal IP, Whois, urlscan.io
- **Output**: Infraestructura digital, vectores de ataque, tecnologías

### Módulo 2: Análisis de Email
- **Herramientas**: Hunter.io, Have I Been Pwned, Epieos
- **Output**: Exposiciones, perfiles sociales, huella digital

### Módulo 3: Búsqueda de Usuario
- **Herramientas**: Sherlock, Blackbird, Namechk
- **Output**: Presencia en redes sociales, perfil de intereses

### Módulo 4: Análisis Social
- **Herramientas**: Social Links API, OSINTgram
- **Output**: Red de contactos, actividad, geolocalización

## 🎨 Características de la Interfaz

- **Dashboard Interactivo**: Visualización en tiempo real de resultados
- **Pestañas Organizadas**: Información categorizada por tipo
- **Grafos de Relaciones**: Visualización de conexiones entre entidades
- **Exportación de Datos**: Reportes en PDF con análisis detallado
- **Modo Oscuro/Claro**: Personalización de la interfaz

## 🔮 Roadmap

### Versión 1.1
- [ ] Integración con más APIs OSINT
- [ ] Análisis de imágenes y metadatos
- [ ] Sistema de alertas automáticas

### Versión 1.2
- [ ] Integración con LLM para análisis de texto
- [ ] Módulos personalizados por usuario
- [ ] API REST para integración externa

### Versión 2.0
- [ ] Análisis de blockchain y criptomonedas
- [ ] Integración con herramientas de threat intelligence
- [ ] Dashboard colaborativo para equipos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Esta herramienta está diseñada únicamente para investigaciones legítimas y éticas. Los desarrolladores no se hacen responsables del uso indebido de esta herramienta. Es responsabilidad del usuario asegurar que su uso cumple con todas las leyes y regulaciones aplicables.

## 📞 Soporte

Para soporte técnico o preguntas:
- Abre un issue en GitHub
- Consulta la documentación en `/docs`
- Revisa los ejemplos en `/examples`

---

**Desarrollado con ❤️ para la comunidad OSINT**