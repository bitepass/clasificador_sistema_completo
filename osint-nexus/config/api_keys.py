"""
Configuración de claves API para OSINT-Nexus
Las claves deben ser almacenadas en un archivo .env para mayor seguridad
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class APIConfig:
    """Gestión centralizada de claves API"""
    
    # Shodan API
    SHODAN_API_KEY = os.getenv('SHODAN_API_KEY', '')
    
    # Hunter.io API
    HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', '')
    
    # Have I Been Pwned API
    HIBP_API_KEY = os.getenv('HIBP_API_KEY', '')
    
    # Criminal IP API
    CRIMINAL_IP_API_KEY = os.getenv('CRIMINAL_IP_API_KEY', '')
    
    # Social Links API
    SOCIAL_LINKS_API_KEY = os.getenv('SOCIAL_LINKS_API_KEY', '')
    
    # URLScan.io API
    URLSCAN_API_KEY = os.getenv('URLSCAN_API_KEY', '')
    
    # VirusTotal API
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')
    
    # Proxy Configuration (opcional)
    USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
    PROXY_URL = os.getenv('PROXY_URL', '')
    
    @classmethod
    def get_proxies(cls):
        """Retorna configuración de proxy si está habilitada"""
        if cls.USE_PROXY and cls.PROXY_URL:
            return {
                'http': cls.PROXY_URL,
                'https': cls.PROXY_URL
            }
        return None
    
    @classmethod
    def is_api_configured(cls, api_name):
        """Verifica si una API específica está configurada"""
        api_map = {
            'shodan': cls.SHODAN_API_KEY,
            'hunter': cls.HUNTER_API_KEY,
            'hibp': cls.HIBP_API_KEY,
            'criminal_ip': cls.CRIMINAL_IP_API_KEY,
            'social_links': cls.SOCIAL_LINKS_API_KEY,
            'urlscan': cls.URLSCAN_API_KEY,
            'virustotal': cls.VIRUSTOTAL_API_KEY
        }
        return bool(api_map.get(api_name.lower(), ''))