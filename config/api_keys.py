"""
Gestión de claves API para OSINT-Nexus
"""
import os
import requests
from typing import Dict, Optional, List
from config.settings import API_KEYS, API_CONFIG

class APIKeyManager:
    """Gestor de claves API para las diferentes herramientas OSINT"""
    
    def __init__(self):
        self.api_keys = API_KEYS.copy()
        self.api_config = API_CONFIG.copy()
        self.validated_keys = {}
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Obtiene la clave API para un servicio específico"""
        return self.api_keys.get(service, "")
    
    def set_api_key(self, service: str, key: str) -> None:
        """Establece una nueva clave API para un servicio"""
        self.api_keys[service] = key
        # Actualizar variable de entorno
        os.environ[f"{service.upper()}_API_KEY"] = key
    
    def validate_api_key(self, service: str) -> bool:
        """Valida una clave API haciendo una petición de prueba"""
        if service in self.validated_keys:
            return self.validated_keys[service]
        
        key = self.get_api_key(service)
        if not key:
            self.validated_keys[service] = False
            return False
        
        try:
            if service == "shodan":
                response = requests.get(
                    "https://api.shodan.io/api-info",
                    params={"key": key},
                    timeout=self.api_config["timeout"]
                )
                is_valid = response.status_code == 200
            
            elif service == "hunter":
                response = requests.get(
                    "https://api.hunter.io/v2/domain-search",
                    params={"domain": "example.com", "api_key": key},
                    timeout=self.api_config["timeout"]
                )
                is_valid = response.status_code == 200
            
            elif service == "hibp":
                response = requests.get(
                    "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com",
                    headers={"hibp-api-key": key, "user-agent": self.api_config["user_agent"]},
                    timeout=self.api_config["timeout"]
                )
                # HIBP devuelve 404 para emails que no existen, lo cual es válido
                is_valid = response.status_code in [200, 404]
            
            else:
                # Para servicios sin endpoint de validación, asumimos que es válido si existe
                is_valid = bool(key)
            
            self.validated_keys[service] = is_valid
            return is_valid
            
        except Exception:
            self.validated_keys[service] = False
            return False
    
    def get_available_services(self) -> List[str]:
        """Retorna la lista de servicios con claves API configuradas"""
        return [service for service, key in self.api_keys.items() if key]
    
    def get_validated_services(self) -> List[str]:
        """Retorna la lista de servicios con claves API válidas"""
        return [service for service in self.api_keys.keys() if self.validate_api_key(service)]
    
    def get_service_status(self) -> Dict[str, Dict]:
        """Retorna el estado de todos los servicios"""
        status = {}
        for service in self.api_keys.keys():
            has_key = bool(self.get_api_key(service))
            is_valid = self.validate_api_key(service) if has_key else False
            
            status[service] = {
                "configured": has_key,
                "valid": is_valid,
                "status": "valid" if is_valid else "invalid" if has_key else "not_configured"
            }
        
        return status
    
    def export_keys_to_env(self, filepath: str = ".env") -> None:
        """Exporta las claves API a un archivo .env"""
        with open(filepath, "w") as f:
            for service, key in self.api_keys.items():
                if key:
                    f.write(f"{service.upper()}_API_KEY={key}\n")
    
    def import_keys_from_env(self, filepath: str = ".env") -> None:
        """Importa las claves API desde un archivo .env"""
        if not os.path.exists(filepath):
            return
        
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    service = key.lower().replace("_api_key", "")
                    self.set_api_key(service, value)

# Instancia global del gestor de claves API
api_key_manager = APIKeyManager()