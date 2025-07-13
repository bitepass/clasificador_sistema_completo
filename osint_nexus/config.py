"""
Configuración principal del proyecto OSINT-Nexus
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración general
APP_NAME = "OSINT-Nexus"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Plataforma de Inteligencia Automatizada - OSINT"

# Configuración de la interfaz
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🔍",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# APIs y claves de configuración
API_KEYS = {
    "SHODAN_API_KEY": os.getenv("SHODAN_API_KEY", ""),
    "HUNTER_API_KEY": os.getenv("HUNTER_API_KEY", ""),
    "HIBP_API_KEY": os.getenv("HIBP_API_KEY", ""),
    "VIRUSTOTAL_API_KEY": os.getenv("VIRUSTOTAL_API_KEY", ""),
    "URLSCAN_API_KEY": os.getenv("URLSCAN_API_KEY", "")
}

# Configuración de timeouts y límites
REQUEST_TIMEOUT = 30
MAX_CONCURRENT_REQUESTS = 10
MAX_RETRIES = 3

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de reportes
REPORT_FORMATS = ["PDF", "JSON", "HTML"]
REPORT_DIR = "reports"

# URLs de APIs
API_URLS = {
    "SHODAN": "https://api.shodan.io",
    "HUNTER": "https://api.hunter.io/v2",
    "HIBP": "https://haveibeenpwned.com/api/v3",
    "VIRUSTOTAL": "https://www.virustotal.com/vtapi/v2",
    "URLSCAN": "https://urlscan.io/api/v1",
    "WHOIS": "https://whois.whoisjson.com/whois"
}

# Configuración ética y legal
ETHICAL_NOTICE = """
⚠️ AVISO ÉTICO Y LEGAL ⚠️

Este software está diseñado para investigación de inteligencia en fuentes abiertas (OSINT) 
con fines legítimos y éticos. Al usar esta herramienta, usted acepta:

1. Utilizar únicamente fuentes de información públicas y legales
2. Respetar las leyes de privacidad y protección de datos aplicables
3. No realizar actividades de hacking, intrusión o acceso no autorizado
4. Usar la información obtenida de manera responsable y ética
5. No participar en actividades de acoso, desinformación o daño a terceros

El usuario es el único responsable del uso que haga de esta herramienta y 
de cumplir con todas las leyes y regulaciones aplicables.
"""

# Configuración de módulos
MODULES = {
    "domain": {
        "name": "Análisis de Dominio",
        "description": "Análisis de infraestructura de dominios e IPs",
        "icon": "🌐"
    },
    "email": {
        "name": "Investigación de Email",
        "description": "Análisis de direcciones de correo electrónico",
        "icon": "📧"
    },
    "username": {
        "name": "Búsqueda de Usuario",
        "description": "Búsqueda de nombres de usuario en redes sociales",
        "icon": "👤"
    },
    "social": {
        "name": "Análisis Social",
        "description": "Análisis de perfiles de redes sociales",
        "icon": "📱"
    }
}

# Configuración de proxies (para seguridad operacional)
PROXY_CONFIG = {
    "enabled": False,
    "http_proxy": "",
    "https_proxy": "",
    "socks_proxy": ""
}