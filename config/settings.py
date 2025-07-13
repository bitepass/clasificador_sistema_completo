"""
Configuración principal de OSINT-Nexus
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
APP_NAME = "OSINT-Nexus"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Plataforma de Inteligencia Automatizada"

# Configuración de Streamlit
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🕵️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        "Get help": "https://github.com/osint-nexus",
        "Report a bug": "https://github.com/osint-nexus/issues",
        "About": f"{APP_NAME} v{APP_VERSION}"
    }
}

# Configuración de APIs
API_CONFIG = {
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 1,
    "user_agent": "OSINT-Nexus/1.0.0"
}

# Configuración de claves API
API_KEYS = {
    "shodan": os.getenv("SHODAN_API_KEY", ""),
    "hunter": os.getenv("HUNTER_API_KEY", ""),
    "hibp": os.getenv("HIBP_API_KEY", ""),
    "criminal_ip": os.getenv("CRIMINAL_IP_API_KEY", ""),
    "urlscan": os.getenv("URLSCAN_API_KEY", ""),
    "social_links": os.getenv("SOCIAL_LINKS_API_KEY", "")
}

# Configuración de límites
LIMITS = {
    "max_concurrent_requests": 10,
    "max_results_per_module": 100,
    "max_report_size_mb": 50
}

# Configuración de reportes
REPORT_CONFIG = {
    "format": "pdf",
    "include_graphs": True,
    "include_raw_data": False,
    "template": "default"
}

# Configuración de seguridad
SECURITY_CONFIG = {
    "enable_proxy": False,
    "proxy_url": os.getenv("PROXY_URL", ""),
    "enable_tor": False,
    "data_retention_hours": 24,
    "log_requests": True
}

# Configuración de visualización
VISUALIZATION_CONFIG = {
    "graph_layout": "spring",
    "max_nodes": 50,
    "max_edges": 100,
    "node_size": 20,
    "edge_width": 1
}

# Configuración de módulos
MODULES_CONFIG = {
    "domain": {
        "enabled": True,
        "tools": ["theharvester", "shodan", "criminal_ip", "whois", "urlscan"],
        "timeout": 60
    },
    "email": {
        "enabled": True,
        "tools": ["hunter", "hibp", "epieos"],
        "timeout": 45
    },
    "username": {
        "enabled": True,
        "tools": ["sherlock", "blackbird", "namechk"],
        "timeout": 90
    },
    "social": {
        "enabled": True,
        "tools": ["social_links", "osintgram"],
        "timeout": 60
    }
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "osint_nexus.log"
}

# Mensajes de advertencia ética
ETHICAL_WARNINGS = [
    "Esta herramienta debe usarse únicamente para investigaciones legítimas y éticas.",
    "Respetar siempre la privacidad y los derechos de terceros.",
    "Verificar la legalidad de cada investigación antes de proceder.",
    "No usar para acoso, espionaje o actividades maliciosas.",
    "Mantener la confidencialidad de la información obtenida."
]

# Colores del tema
THEME_COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "warning": "#d62728",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}