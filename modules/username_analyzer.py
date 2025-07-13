"""
Módulo de Análisis de Nombre de Usuario para OSINT-Nexus
Busca nombres de usuario en múltiples plataformas sociales
"""
import requests
import time
import json
from typing import Dict, List, Optional, Any
from config.settings import API_CONFIG, MODULES_CONFIG

class UsernameAnalyzer:
    """Analizador de nombres de usuario que busca en múltiples plataformas"""
    
    def __init__(self):
        self.api_config = API_CONFIG.copy()
        self.module_config = MODULES_CONFIG["username"]
        self.results = {
            "username": "",
            "profiles": [],
            "statistics": {},
            "metadata": {
                "scan_time": None,
                "platforms_checked": [],
                "errors": []
            }
        }
        
        # Lista de plataformas para buscar
        self.platforms = {
            "facebook": {
                "url": "https://www.facebook.com/{}",
                "check_method": "http_status"
            },
            "twitter": {
                "url": "https://twitter.com/{}",
                "check_method": "http_status"
            },
            "instagram": {
                "url": "https://www.instagram.com/{}",
                "check_method": "http_status"
            },
            "linkedin": {
                "url": "https://www.linkedin.com/in/{}",
                "check_method": "http_status"
            },
            "github": {
                "url": "https://github.com/{}",
                "check_method": "http_status"
            },
            "reddit": {
                "url": "https://www.reddit.com/user/{}",
                "check_method": "http_status"
            },
            "youtube": {
                "url": "https://www.youtube.com/{}",
                "check_method": "http_status"
            },
            "tiktok": {
                "url": "https://www.tiktok.com/@{}",
                "check_method": "http_status"
            },
            "discord": {
                "url": "https://discord.com/users/{}",
                "check_method": "http_status"
            },
            "telegram": {
                "url": "https://t.me/{}",
                "check_method": "http_status"
            },
            "snapchat": {
                "url": "https://www.snapchat.com/add/{}",
                "check_method": "http_status"
            },
            "pinterest": {
                "url": "https://www.pinterest.com/{}",
                "check_method": "http_status"
            },
            "tumblr": {
                "url": "https://{}.tumblr.com",
                "check_method": "http_status"
            },
            "medium": {
                "url": "https://medium.com/@{}",
                "check_method": "http_status"
            },
            "deviantart": {
                "url": "https://www.deviantart.com/{}",
                "check_method": "http_status"
            },
            "steam": {
                "url": "https://steamcommunity.com/id/{}",
                "check_method": "http_status"
            },
            "twitch": {
                "url": "https://www.twitch.tv/{}",
                "check_method": "http_status"
            },
            "spotify": {
                "url": "https://open.spotify.com/user/{}",
                "check_method": "http_status"
            },
            "soundcloud": {
                "url": "https://soundcloud.com/{}",
                "check_method": "http_status"
            },
            "behance": {
                "url": "https://www.behance.net/{}",
                "check_method": "http_status"
            },
            "dribbble": {
                "url": "https://dribbble.com/{}",
                "check_method": "http_status"
            },
            "flickr": {
                "url": "https://www.flickr.com/photos/{}",
                "check_method": "http_status"
            },
            "vimeo": {
                "url": "https://vimeo.com/{}",
                "check_method": "http_status"
            },
            "wordpress": {
                "url": "https://{}.wordpress.com",
                "check_method": "http_status"
            },
            "blogger": {
                "url": "https://{}.blogspot.com",
                "check_method": "http_status"
            }
        }
    
    def analyze_username(self, username: str) -> Dict[str, Any]:
        """Realiza un análisis completo del nombre de usuario"""
        start_time = time.time()
        
        # Limpiar y validar el username
        username = self._clean_username(username)
        if not self._validate_username(username):
            return {"error": "Nombre de usuario inválido"}
        
        self.results["username"] = username
        self.results["metadata"]["scan_time"] = start_time
        self.results["metadata"]["platforms_checked"] = []
        
        try:
            # Buscar en todas las plataformas
            for platform_name, platform_info in self.platforms.items():
                try:
                    profile = self._check_platform(username, platform_name, platform_info)
                    if profile:
                        self.results["profiles"].append(profile)
                        self.results["metadata"]["platforms_checked"].append(platform_name)
                    
                    # Pequeña pausa para no sobrecargar los servidores
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.results["metadata"]["errors"].append(f"Error en {platform_name}: {str(e)}")
            
            # Calcular estadísticas
            self._calculate_statistics()
            
        except Exception as e:
            self.results["metadata"]["errors"].append(str(e))
        
        self.results["metadata"]["scan_time"] = time.time() - start_time
        return self.results
    
    def _clean_username(self, username: str) -> str:
        """Limpia y normaliza el nombre de usuario"""
        return username.lower().strip()
    
    def _validate_username(self, username: str) -> bool:
        """Valida que el nombre de usuario tenga un formato correcto"""
        import re
        # Patrón básico para nombres de usuario
        pattern = r'^[a-zA-Z0-9._-]{3,30}$'
        return bool(re.match(pattern, username))
    
    def _check_platform(self, username: str, platform_name: str, platform_info: Dict) -> Optional[Dict]:
        """Verifica si el usuario existe en una plataforma específica"""
        try:
            url = platform_info["url"].format(username)
            method = platform_info["check_method"]
            
            headers = {
                "User-Agent": self.api_config["user_agent"]
            }
            
            if method == "http_status":
                return self._check_http_status(url, platform_name, headers)
            else:
                return None
                
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error verificando {platform_name}: {str(e)}")
            return None
    
    def _check_http_status(self, url: str, platform_name: str, headers: Dict) -> Optional[Dict]:
        """Verifica existencia basándose en el código de estado HTTP"""
        try:
            response = requests.get(url, headers=headers, timeout=self.api_config["timeout"])
            
            # Códigos de estado que indican que el perfil existe
            success_codes = [200, 201, 202]
            
            # Códigos de estado que indican que el perfil no existe
            not_found_codes = [404, 410]
            
            if response.status_code in success_codes:
                return {
                    "platform": platform_name,
                    "url": url,
                    "exists": True,
                    "status_code": response.status_code,
                    "title": self._extract_title(response.text),
                    "last_checked": time.time()
                }
            elif response.status_code in not_found_codes:
                return {
                    "platform": platform_name,
                    "url": url,
                    "exists": False,
                    "status_code": response.status_code,
                    "last_checked": time.time()
                }
            else:
                # Estado ambiguo, no podemos determinar si existe
                return {
                    "platform": platform_name,
                    "url": url,
                    "exists": None,
                    "status_code": response.status_code,
                    "last_checked": time.time()
                }
                
        except requests.exceptions.RequestException:
            # Error de conexión, no podemos determinar si existe
            return {
                "platform": platform_name,
                "url": url,
                "exists": None,
                "status_code": None,
                "error": "connection_error",
                "last_checked": time.time()
            }
    
    def _extract_title(self, html_content: str) -> Optional[str]:
        """Extrae el título de la página HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
            return None
        except Exception:
            return None
    
    def _calculate_statistics(self) -> None:
        """Calcula estadísticas del análisis"""
        total_platforms = len(self.platforms)
        found_profiles = [p for p in self.results["profiles"] if p.get("exists") is True]
        not_found_profiles = [p for p in self.results["profiles"] if p.get("exists") is False]
        ambiguous_profiles = [p for p in self.results["profiles"] if p.get("exists") is None]
        
        self.results["statistics"] = {
            "total_platforms": total_platforms,
            "platforms_checked": len(self.results["metadata"]["platforms_checked"]),
            "profiles_found": len(found_profiles),
            "profiles_not_found": len(not_found_profiles),
            "profiles_ambiguous": len(ambiguous_profiles),
            "success_rate": len(found_profiles) / total_platforms if total_platforms > 0 else 0,
            "platforms_with_profiles": [p["platform"] for p in found_profiles]
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del análisis"""
        return {
            "username": self.results["username"],
            "total_profiles_found": self.results["statistics"]["profiles_found"],
            "total_platforms_checked": self.results["statistics"]["platforms_checked"],
            "success_rate": self.results["statistics"]["success_rate"],
            "scan_duration": self.results["metadata"]["scan_time"],
            "errors": len(self.results["metadata"]["errors"])
        }
    
    def get_profiles_by_category(self) -> Dict[str, List]:
        """Agrupa los perfiles encontrados por categoría"""
        categories = {
            "social_media": ["facebook", "twitter", "instagram", "linkedin", "snapchat"],
            "professional": ["linkedin", "github", "behance", "dribbble"],
            "entertainment": ["youtube", "tiktok", "twitch", "spotify", "soundcloud"],
            "creative": ["deviantart", "behance", "dribbble", "flickr", "vimeo"],
            "gaming": ["steam", "twitch", "discord"],
            "blogging": ["medium", "tumblr", "wordpress", "blogger"],
            "other": []
        }
        
        categorized_profiles = {cat: [] for cat in categories.keys()}
        
        for profile in self.results["profiles"]:
            platform = profile["platform"]
            categorized = False
            
            for category, platforms in categories.items():
                if platform in platforms:
                    categorized_profiles[category].append(profile)
                    categorized = True
                    break
            
            if not categorized:
                categorized_profiles["other"].append(profile)
        
        return categorized_profiles
    
    def export_results(self, format: str = "json") -> str:
        """Exporta los resultados en diferentes formatos"""
        if format.lower() == "json":
            return json.dumps(self.results, indent=2, default=str)
        elif format.lower() == "csv":
            return self._export_to_csv()
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def _export_to_csv(self) -> str:
        """Exporta los resultados a formato CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        writer.writerow(["Platform", "URL", "Exists", "Status Code", "Title"])
        
        # Datos
        for profile in self.results["profiles"]:
            writer.writerow([
                profile.get("platform", ""),
                profile.get("url", ""),
                profile.get("exists", ""),
                profile.get("status_code", ""),
                profile.get("title", "")
            ])
        
        return output.getvalue()