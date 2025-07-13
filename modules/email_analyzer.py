"""
Módulo de Análisis de Email para OSINT-Nexus
Integra múltiples herramientas para análisis completo de direcciones de email
"""
import requests
import re
import time
from typing import Dict, List, Optional, Any
from config.api_keys import api_key_manager
from config.settings import API_CONFIG, MODULES_CONFIG

class EmailAnalyzer:
    """Analizador de emails que integra múltiples herramientas OSINT"""
    
    def __init__(self):
        self.api_config = API_CONFIG.copy()
        self.module_config = MODULES_CONFIG["email"]
        self.results = {
            "email_info": {},
            "breaches": [],
            "social_profiles": [],
            "domain_info": {},
            "related_emails": [],
            "password_exposures": [],
            "metadata": {
                "scan_time": None,
                "tools_used": [],
                "errors": []
            }
        }
    
    def analyze_email(self, email: str) -> Dict[str, Any]:
        """Realiza un análisis completo del email"""
        start_time = time.time()
        
        # Limpiar y validar el email
        email = self._clean_email(email)
        if not self._validate_email(email):
            return {"error": "Email inválido"}
        
        self.results["metadata"]["scan_time"] = start_time
        self.results["metadata"]["tools_used"] = []
        
        try:
            # Información básica del email
            self._analyze_email_structure(email)
            
            # Análisis con herramientas externas
            if api_key_manager.validate_api_key("hunter"):
                self._analyze_hunter(email)
                self.results["metadata"]["tools_used"].append("hunter")
            
            if api_key_manager.validate_api_key("hibp"):
                self._analyze_hibp(email)
                self.results["metadata"]["tools_used"].append("hibp")
            
            # Análisis de dominio del email
            self._analyze_email_domain(email)
            
            # Búsqueda de perfiles sociales
            self._analyze_social_profiles(email)
            
        except Exception as e:
            self.results["metadata"]["errors"].append(str(e))
        
        self.results["metadata"]["scan_time"] = time.time() - start_time
        return self.results
    
    def _clean_email(self, email: str) -> str:
        """Limpia y normaliza el email"""
        return email.lower().strip()
    
    def _validate_email(self, email: str) -> bool:
        """Valida que el email tenga un formato correcto"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _analyze_email_structure(self, email: str) -> None:
        """Analiza la estructura básica del email"""
        username, domain = email.split('@')
        
        self.results["email_info"] = {
            "email": email,
            "username": username,
            "domain": domain,
            "length": len(email),
            "username_length": len(username),
            "domain_length": len(domain),
            "has_numbers": any(c.isdigit() for c in username),
            "has_special_chars": any(c in "._%+-" for c in username)
        }
    
    def _analyze_hunter(self, email: str) -> None:
        """Analiza el email usando Hunter.io"""
        try:
            api_key = api_key_manager.get_api_key("hunter")
            if not api_key:
                return
            
            # Verificar existencia del email
            url = "https://api.hunter.io/v2/email-verifier"
            params = {
                "email": email,
                "api_key": api_key
            }
            
            response = requests.get(url, params=params, timeout=self.api_config["timeout"])
            if response.status_code == 200:
                data = response.json()
                
                if "data" in data:
                    email_data = data["data"]
                    
                    # Información de verificación
                    self.results["email_info"].update({
                        "exists": email_data.get("status") == "valid",
                        "score": email_data.get("score"),
                        "regexp": email_data.get("regexp"),
                        "gibberish": email_data.get("gibberish"),
                        "disposable": email_data.get("disposable"),
                        "webmail": email_data.get("webmail"),
                        "mx_records": email_data.get("mx_records"),
                        "smtp_server": email_data.get("smtp_server"),
                        "smtp_check": email_data.get("smtp_check")
                    })
            
            # Buscar otros emails del mismo dominio
            domain = email.split('@')[1]
            url = "https://api.hunter.io/v2/domain-search"
            params = {
                "domain": domain,
                "api_key": api_key,
                "limit": 10
            }
            
            response = requests.get(url, params=params, timeout=self.api_config["timeout"])
            if response.status_code == 200:
                data = response.json()
                
                if "data" in data and "emails" in data["data"]:
                    for email_info in data["data"]["emails"]:
                        if email_info.get("value") != email:
                            self.results["related_emails"].append({
                                "email": email_info.get("value"),
                                "first_name": email_info.get("first_name"),
                                "last_name": email_info.get("last_name"),
                                "position": email_info.get("position"),
                                "department": email_info.get("department"),
                                "linkedin": email_info.get("linkedin"),
                                "twitter": email_info.get("twitter"),
                                "confidence": email_info.get("confidence")
                            })
                            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error Hunter: {str(e)}")
    
    def _analyze_hibp(self, email: str) -> None:
        """Analiza el email usando Have I Been Pwned"""
        try:
            api_key = api_key_manager.get_api_key("hibp")
            if not api_key:
                return
            
            # Buscar en brechas de datos
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {
                "hibp-api-key": api_key,
                "user-agent": self.api_config["user_agent"]
            }
            
            response = requests.get(url, headers=headers, timeout=self.api_config["timeout"])
            if response.status_code == 200:
                breaches = response.json()
                
                for breach in breaches:
                    breach_info = {
                        "name": breach.get("Name"),
                        "title": breach.get("Title"),
                        "domain": breach.get("Domain"),
                        "breach_date": breach.get("BreachDate"),
                        "added_date": breach.get("AddedDate"),
                        "modified_date": breach.get("ModifiedDate"),
                        "pwn_count": breach.get("PwnCount"),
                        "description": breach.get("Description"),
                        "logo_path": breach.get("LogoPath"),
                        "data_classes": breach.get("DataClasses", []),
                        "is_verified": breach.get("IsVerified"),
                        "is_fabricated": breach.get("IsFabricated"),
                        "is_sensitive": breach.get("IsSensitive"),
                        "is_retired": breach.get("IsRetired"),
                        "is_spam_list": breach.get("IsSpamList")
                    }
                    self.results["breaches"].append(breach_info)
            
            # Buscar en pastebin
            url = f"https://haveibeenpwned.com/api/v3/pasteaccount/{email}"
            response = requests.get(url, headers=headers, timeout=self.api_config["timeout"])
            if response.status_code == 200:
                pastes = response.json()
                
                for paste in pastes:
                    paste_info = {
                        "source": paste.get("Source"),
                        "id": paste.get("Id"),
                        "title": paste.get("Title"),
                        "date": paste.get("Date"),
                        "email_count": paste.get("EmailCount")
                    }
                    self.results["breaches"].append({
                        "name": f"Pastebin - {paste.get('Source')}",
                        "title": paste.get("Title"),
                        "breach_date": paste.get("Date"),
                        "data_classes": ["pastebin"],
                        "is_paste": True,
                        "paste_info": paste_info
                    })
                    
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error HIBP: {str(e)}")
    
    def _analyze_email_domain(self, email: str) -> None:
        """Analiza el dominio del email"""
        try:
            domain = email.split('@')[1]
            
            # Información básica del dominio
            self.results["domain_info"] = {
                "domain": domain,
                "is_common_provider": self._is_common_provider(domain),
                "provider_type": self._get_provider_type(domain)
            }
            
            # Verificar si es un dominio corporativo
            if not self._is_common_provider(domain):
                # Aquí se podría integrar con herramientas de análisis de dominios
                self.results["domain_info"]["is_corporate"] = True
                
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error dominio: {str(e)}")
    
    def _is_common_provider(self, domain: str) -> bool:
        """Verifica si es un proveedor de email común"""
        common_providers = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
            "aol.com", "icloud.com", "protonmail.com", "tutanota.com",
            "yandex.com", "mail.ru", "qq.com", "163.com"
        ]
        return domain.lower() in common_providers
    
    def _get_provider_type(self, domain: str) -> str:
        """Determina el tipo de proveedor de email"""
        if self._is_common_provider(domain):
            return "personal"
        elif domain.endswith((".edu", ".ac.uk", ".edu.au")):
            return "educational"
        elif domain.endswith((".gov", ".gov.uk", ".gov.au")):
            return "government"
        else:
            return "corporate"
    
    def _analyze_social_profiles(self, email: str) -> None:
        """Busca perfiles sociales asociados al email"""
        try:
            # Simulación de búsqueda en redes sociales
            # En una implementación real, usarías APIs específicas
            
            social_platforms = [
                "facebook", "twitter", "linkedin", "instagram",
                "github", "reddit", "discord", "telegram"
            ]
            
            for platform in social_platforms:
                # Simular búsqueda (en realidad usarías APIs específicas)
                profile_info = {
                    "platform": platform,
                    "username": None,
                    "url": None,
                    "exists": False,
                    "last_checked": time.time()
                }
                
                # Aquí se integraría con APIs específicas de cada plataforma
                # Por ahora es una simulación
                
                self.results["social_profiles"].append(profile_info)
                
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error perfiles sociales: {str(e)}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del análisis"""
        return {
            "email": self.results["email_info"].get("email"),
            "exists": self.results["email_info"].get("exists"),
            "total_breaches": len(self.results["breaches"]),
            "total_related_emails": len(self.results["related_emails"]),
            "total_social_profiles": len(self.results["social_profiles"]),
            "domain_type": self.results["domain_info"].get("provider_type"),
            "scan_duration": self.results["metadata"]["scan_time"],
            "tools_used": self.results["metadata"]["tools_used"],
            "errors": len(self.results["metadata"]["errors"])
        }
    
    def get_breach_summary(self) -> Dict[str, Any]:
        """Retorna un resumen de las brechas encontradas"""
        if not self.results["breaches"]:
            return {"total_breaches": 0, "breaches": []}
        
        total_records = sum(breach.get("pwn_count", 0) for breach in self.results["breaches"])
        
        return {
            "total_breaches": len(self.results["breaches"]),
            "total_records_exposed": total_records,
            "breaches": [
                {
                    "name": breach.get("name"),
                    "date": breach.get("breach_date"),
                    "records": breach.get("pwn_count"),
                    "data_types": breach.get("data_classes", [])
                }
                for breach in self.results["breaches"]
            ]
        }