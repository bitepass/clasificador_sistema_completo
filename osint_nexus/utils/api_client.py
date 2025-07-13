"""
Cliente base para interactuar con APIs de manera segura
"""

import requests
import asyncio
import aiohttp
import time
from typing import Dict, Any, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import REQUEST_TIMEOUT, MAX_RETRIES, PROXY_CONFIG
from utils.logger import setup_logger

logger = setup_logger("api_client")

class APIClient:
    """Cliente base para interactuar con APIs de OSINT"""
    
    def __init__(self, base_url: str, api_key: str = None, headers: Dict[str, str] = None):
        """
        Inicializa el cliente API
        
        Args:
            base_url: URL base de la API
            api_key: Clave de API (opcional)
            headers: Headers adicionales (opcional)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = self._create_session()
        self.headers = headers or {}
        
        # Configurar headers por defecto
        self.headers.update({
            'User-Agent': 'OSINT-Nexus/1.0.0 (Research Tool)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Agregar clave de API si está disponible
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def _create_session(self) -> requests.Session:
        """
        Crea una sesión con configuración de reintentos y proxies
        
        Returns:
            Sesión configurada
        """
        session = requests.Session()
        
        # Configurar estrategia de reintentos
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Configurar proxies si están habilitados
        if PROXY_CONFIG.get('enabled', False):
            proxies = {}
            if PROXY_CONFIG.get('http_proxy'):
                proxies['http'] = PROXY_CONFIG['http_proxy']
            if PROXY_CONFIG.get('https_proxy'):
                proxies['https'] = PROXY_CONFIG['https_proxy']
            if proxies:
                session.proxies.update(proxies)
        
        return session
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Realiza una petición GET
        
        Args:
            endpoint: Endpoint de la API
            params: Parámetros de la petición
            
        Returns:
            Respuesta de la API o None si hay error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.debug(f"GET request to: {url}")
            response = self.session.get(
                url,
                params=params,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición GET a {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return None
    
    def post(self, endpoint: str, data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Realiza una petición POST
        
        Args:
            endpoint: Endpoint de la API
            data: Datos a enviar
            
        Returns:
            Respuesta de la API o None si hay error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.debug(f"POST request to: {url}")
            response = self.session.post(
                url,
                json=data,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición POST a {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return None
    
    def close(self):
        """Cierra la sesión"""
        self.session.close()

class AsyncAPIClient:
    """Cliente asíncrono para peticiones concurrentes"""
    
    def __init__(self, base_url: str, api_key: str = None, headers: Dict[str, str] = None):
        """
        Inicializa el cliente asíncrono
        
        Args:
            base_url: URL base de la API
            api_key: Clave de API (opcional)
            headers: Headers adicionales (opcional)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = headers or {}
        
        # Configurar headers por defecto
        self.headers.update({
            'User-Agent': 'OSINT-Nexus/1.0.0 (Research Tool)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Agregar clave de API si está disponible
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    async def get(self, session: aiohttp.ClientSession, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Realiza una petición GET asíncrona
        
        Args:
            session: Sesión aiohttp
            endpoint: Endpoint de la API
            params: Parámetros de la petición
            
        Returns:
            Respuesta de la API o None si hay error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with session.get(
                url,
                params=params,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            logger.error(f"Error en petición async GET a {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return None
    
    async def post(self, session: aiohttp.ClientSession, endpoint: str, data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Realiza una petición POST asíncrona
        
        Args:
            session: Sesión aiohttp
            endpoint: Endpoint de la API
            data: Datos a enviar
            
        Returns:
            Respuesta de la API o None si hay error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with session.post(
                url,
                json=data,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            logger.error(f"Error en petición async POST a {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return None

async def make_concurrent_requests(requests_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Realiza múltiples peticiones de manera concurrente
    
    Args:
        requests_list: Lista de diccionarios con información de peticiones
        
    Returns:
        Lista de respuestas
    """
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for request_info in requests_list:
            client = AsyncAPIClient(
                request_info['base_url'],
                request_info.get('api_key'),
                request_info.get('headers')
            )
            
            if request_info.get('method', 'GET').upper() == 'GET':
                task = client.get(session, request_info['endpoint'], request_info.get('params'))
            else:
                task = client.post(session, request_info['endpoint'], request_info.get('data'))
            
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filtrar excepciones y devolver solo resultados válidos
    valid_results = []
    for result in results:
        if not isinstance(result, Exception) and result is not None:
            valid_results.append(result)
    
    return valid_results

def rate_limit_handler(func):
    """
    Decorador para manejar rate limiting
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada
    """
    last_call = {}
    
    def wrapper(*args, **kwargs):
        # Identificar la función por su nombre
        func_name = func.__name__
        current_time = time.time()
        
        # Verificar si necesitamos esperar
        if func_name in last_call:
            time_since_last = current_time - last_call[func_name]
            if time_since_last < 1.0:  # 1 segundo entre llamadas
                time.sleep(1.0 - time_since_last)
        
        # Actualizar tiempo de última llamada
        last_call[func_name] = time.time()
        
        # Ejecutar función
        return func(*args, **kwargs)
    
    return wrapper