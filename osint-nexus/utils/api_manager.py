"""
Gestor de APIs para OSINT-Nexus
Maneja las peticiones HTTP, límites de tasa y errores
"""

import requests
import time
import json
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.api_keys import APIConfig
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIManager:
    """Clase principal para gestionar todas las llamadas a APIs externas"""
    
    def __init__(self):
        self.session = self._create_session()
        self.rate_limits = {}  # Almacenar límites de tasa por API
        
    def _create_session(self) -> requests.Session:
        """Crea una sesión con reintentos automáticos"""
        session = requests.Session()
        
        # Configurar reintentos
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Configurar proxy si está habilitado
        proxies = APIConfig.get_proxies()
        if proxies:
            session.proxies.update(proxies)
            logger.info("Proxy configurado para las peticiones")
            
        return session
    
    def make_request(self, url: str, method: str = 'GET', 
                    headers: Optional[Dict] = None, 
                    params: Optional[Dict] = None,
                    data: Optional[Dict] = None,
                    api_name: str = 'generic') -> Optional[Dict[str, Any]]:
        """
        Realiza una petición HTTP con manejo de errores
        
        Args:
            url: URL de la API
            method: Método HTTP (GET, POST, etc.)
            headers: Headers adicionales
            params: Parámetros de query
            data: Datos para POST
            api_name: Nombre de la API para tracking
            
        Returns:
            Respuesta en formato JSON o None si hay error
        """
        try:
            # Verificar límites de tasa
            self._check_rate_limit(api_name)
            
            # Headers por defecto
            default_headers = {
                'User-Agent': 'OSINT-Nexus/1.0',
                'Accept': 'application/json'
            }
            
            if headers:
                default_headers.update(headers)
            
            # Realizar petición
            response = self.session.request(
                method=method,
                url=url,
                headers=default_headers,
                params=params,
                json=data if method == 'POST' else None,
                timeout=30
            )
            
            # Verificar respuesta
            response.raise_for_status()
            
            # Actualizar límites de tasa si están en headers
            self._update_rate_limits(api_name, response.headers)
            
            # Retornar JSON si es posible
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'raw_text': response.text}
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP en {api_name}: {e}")
            if e.response.status_code == 429:
                logger.warning(f"Límite de tasa alcanzado para {api_name}")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexión con {api_name}")
            return None
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout en petición a {api_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error inesperado en {api_name}: {e}")
            return None
    
    def _check_rate_limit(self, api_name: str):
        """Verifica y espera si es necesario por límites de tasa"""
        if api_name in self.rate_limits:
            limit_info = self.rate_limits[api_name]
            if 'reset_time' in limit_info:
                current_time = time.time()
                if current_time < limit_info['reset_time']:
                    wait_time = limit_info['reset_time'] - current_time
                    logger.info(f"Esperando {wait_time:.2f}s por límite de tasa en {api_name}")
                    time.sleep(wait_time)
    
    def _update_rate_limits(self, api_name: str, headers: Any):
        """Actualiza información de límites de tasa desde headers"""
        rate_limit_headers = {
            'X-RateLimit-Limit': 'limit',
            'X-RateLimit-Remaining': 'remaining',
            'X-RateLimit-Reset': 'reset_time'
        }
        
        limit_info = {}
        for header, key in rate_limit_headers.items():
            if header in headers:
                try:
                    value = int(headers[header])
                    limit_info[key] = value
                except ValueError:
                    pass
        
        if limit_info:
            self.rate_limits[api_name] = limit_info
            
    # Métodos específicos para cada API
    
    def shodan_search(self, query: str) -> Optional[Dict]:
        """Búsqueda en Shodan"""
        if not APIConfig.SHODAN_API_KEY:
            logger.warning("Shodan API key no configurada")
            return None
            
        url = "https://api.shodan.io/shodan/host/search"
        params = {
            'key': APIConfig.SHODAN_API_KEY,
            'query': query
        }
        
        return self.make_request(url, params=params, api_name='shodan')
    
    def hunter_email_verify(self, email: str) -> Optional[Dict]:
        """Verificación de email con Hunter.io"""
        if not APIConfig.HUNTER_API_KEY:
            logger.warning("Hunter.io API key no configurada")
            return None
            
        url = "https://api.hunter.io/v2/email-verifier"
        params = {
            'email': email,
            'api_key': APIConfig.HUNTER_API_KEY
        }
        
        return self.make_request(url, params=params, api_name='hunter')
    
    def hibp_check(self, email: str) -> Optional[Dict]:
        """Verificar brechas de datos en Have I Been Pwned"""
        if not APIConfig.HIBP_API_KEY:
            logger.warning("HIBP API key no configurada")
            return None
            
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {
            'hibp-api-key': APIConfig.HIBP_API_KEY
        }
        
        return self.make_request(url, headers=headers, api_name='hibp')
    
    def urlscan_submit(self, url: str) -> Optional[Dict]:
        """Enviar URL para análisis en URLScan.io"""
        if not APIConfig.URLSCAN_API_KEY:
            logger.warning("URLScan.io API key no configurada")
            return None
            
        api_url = "https://urlscan.io/api/v1/scan/"
        headers = {
            'API-Key': APIConfig.URLSCAN_API_KEY,
            'Content-Type': 'application/json'
        }
        data = {
            'url': url,
            'visibility': 'private'
        }
        
        return self.make_request(api_url, method='POST', 
                               headers=headers, data=data, 
                               api_name='urlscan')