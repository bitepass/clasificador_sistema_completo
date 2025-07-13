"""
Módulo de Análisis de Redes Sociales para OSINT-Nexus
Análisis profundo de perfiles sociales y conexiones
"""
import requests
import re
import time
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs
from config.api_keys import api_key_manager
from config.settings import API_CONFIG, MODULES_CONFIG

class SocialAnalyzer:
    """Analizador de redes sociales que realiza análisis profundo de perfiles"""
    
    def __init__(self):
        self.api_config = API_CONFIG.copy()
        self.module_config = MODULES_CONFIG["social"]
        self.results = {
            "profile_info": {},
            "posts": [],
            "connections": [],
            "activity_analysis": {},
            "geolocation": [],
            "metadata": {
                "scan_time": None,
                "tools_used": [],
                "errors": []
            }
        }
        
        # Plataformas soportadas
        self.supported_platforms = {
            "twitter": {
                "domain": "twitter.com",
                "analyzer": self._analyze_twitter
            },
            "instagram": {
                "domain": "instagram.com",
                "analyzer": self._analyze_instagram
            },
            "linkedin": {
                "domain": "linkedin.com",
                "analyzer": self._analyze_linkedin
            },
            "facebook": {
                "domain": "facebook.com",
                "analyzer": self._analyze_facebook
            },
            "youtube": {
                "domain": "youtube.com",
                "analyzer": self._analyze_youtube
            },
            "tiktok": {
                "domain": "tiktok.com",
                "analyzer": self._analyze_tiktok
            }
        }
    
    def analyze_social_profile(self, profile_url: str) -> Dict[str, Any]:
        """Realiza un análisis completo del perfil social"""
        start_time = time.time()
        
        # Limpiar y validar la URL
        profile_url = self._clean_url(profile_url)
        if not self._validate_url(profile_url):
            return {"error": "URL de perfil inválida"}
        
        # Identificar la plataforma
        platform = self._identify_platform(profile_url)
        if not platform:
            return {"error": "Plataforma no soportada"}
        
        self.results["metadata"]["scan_time"] = start_time
        self.results["metadata"]["tools_used"] = []
        
        try:
            # Análisis específico de la plataforma
            analyzer_func = self.supported_platforms[platform]["analyzer"]
            platform_results = analyzer_func(profile_url)
            
            if platform_results:
                self.results.update(platform_results)
                self.results["metadata"]["tools_used"].append(platform)
            
            # Análisis adicionales
            self._analyze_activity_patterns()
            self._analyze_geolocation_data()
            
        except Exception as e:
            self.results["metadata"]["errors"].append(str(e))
        
        self.results["metadata"]["scan_time"] = time.time() - start_time
        return self.results
    
    def _clean_url(self, url: str) -> str:
        """Limpia y normaliza la URL"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def _validate_url(self, url: str) -> bool:
        """Valida que la URL tenga un formato correcto"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _identify_platform(self, url: str) -> Optional[str]:
        """Identifica la plataforma social basándose en la URL"""
        domain = urlparse(url).netloc.lower()
        
        for platform, info in self.supported_platforms.items():
            if info["domain"] in domain:
                return platform
        
        return None
    
    def _analyze_twitter(self, profile_url: str) -> Dict[str, Any]:
        """Analiza un perfil de Twitter"""
        try:
            # Extraer username de la URL
            username = self._extract_twitter_username(profile_url)
            if not username:
                return {}
            
            # Simulación de análisis de Twitter
            # En una implementación real, usarías la API oficial de Twitter
            
            profile_info = {
                "platform": "twitter",
                "username": username,
                "profile_url": profile_url,
                "display_name": f"@{username}",
                "bio": "Análisis de bio no disponible sin API",
                "location": "Ubicación no disponible",
                "website": None,
                "followers_count": "No disponible sin API",
                "following_count": "No disponible sin API",
                "tweets_count": "No disponible sin API",
                "verified": False,
                "created_at": None,
                "profile_image": None
            }
            
            # Simular algunos posts recientes
            posts = [
                {
                    "id": "sample_1",
                    "text": "Este es un tweet de ejemplo",
                    "created_at": "2024-01-01T12:00:00Z",
                    "likes": 10,
                    "retweets": 5,
                    "replies": 2,
                    "hashtags": ["#ejemplo"],
                    "mentions": [],
                    "urls": []
                }
            ]
            
            return {
                "profile_info": profile_info,
                "posts": posts,
                "connections": [],
                "activity_analysis": {
                    "posting_frequency": "No disponible",
                    "peak_activity_hours": [],
                    "most_used_hashtags": [],
                    "engagement_rate": "No disponible"
                }
            }
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error Twitter: {str(e)}")
            return {}
    
    def _extract_twitter_username(self, url: str) -> Optional[str]:
        """Extrae el username de una URL de Twitter"""
        try:
            # Patrones comunes de URLs de Twitter
            patterns = [
                r'twitter\.com/([^/]+)',
                r'x\.com/([^/]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    username = match.group(1)
                    # Remover parámetros de consulta
                    username = username.split('?')[0]
                    return username
            
            return None
        except Exception:
            return None
    
    def _analyze_instagram(self, profile_url: str) -> Dict[str, Any]:
        """Analiza un perfil de Instagram"""
        try:
            username = self._extract_instagram_username(profile_url)
            if not username:
                return {}
            
            # Simulación de análisis de Instagram
            profile_info = {
                "platform": "instagram",
                "username": username,
                "profile_url": profile_url,
                "display_name": username,
                "bio": "Análisis de bio no disponible sin API",
                "website": None,
                "followers_count": "No disponible sin API",
                "following_count": "No disponible sin API",
                "posts_count": "No disponible sin API",
                "verified": False,
                "private": False,
                "profile_image": None
            }
            
            return {
                "profile_info": profile_info,
                "posts": [],
                "connections": [],
                "activity_analysis": {
                    "posting_frequency": "No disponible",
                    "most_liked_posts": [],
                    "engagement_rate": "No disponible"
                }
            }
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error Instagram: {str(e)}")
            return {}
    
    def _extract_instagram_username(self, url: str) -> Optional[str]:
        """Extrae el username de una URL de Instagram"""
        try:
            pattern = r'instagram\.com/([^/]+)'
            match = re.search(pattern, url)
            if match:
                username = match.group(1)
                username = username.split('?')[0]
                return username
            return None
        except Exception:
            return None
    
    def _analyze_linkedin(self, profile_url: str) -> Dict[str, Any]:
        """Analiza un perfil de LinkedIn"""
        try:
            profile_id = self._extract_linkedin_profile_id(profile_url)
            if not profile_id:
                return {}
            
            # Simulación de análisis de LinkedIn
            profile_info = {
                "platform": "linkedin",
                "profile_id": profile_id,
                "profile_url": profile_url,
                "name": "Nombre no disponible sin API",
                "headline": "Título profesional no disponible",
                "company": "Empresa no disponible",
                "location": "Ubicación no disponible",
                "connections_count": "No disponible sin API",
                "verified": False,
                "profile_image": None
            }
            
            return {
                "profile_info": profile_info,
                "posts": [],
                "connections": [],
                "activity_analysis": {
                    "posting_frequency": "No disponible",
                    "engagement_rate": "No disponible"
                }
            }
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error LinkedIn: {str(e)}")
            return {}
    
    def _extract_linkedin_profile_id(self, url: str) -> Optional[str]:
        """Extrae el ID del perfil de LinkedIn"""
        try:
            pattern = r'linkedin\.com/in/([^/]+)'
            match = re.search(pattern, url)
            if match:
                profile_id = match.group(1)
                profile_id = profile_id.split('?')[0]
                return profile_id
            return None
        except Exception:
            return None
    
    def _analyze_facebook(self, profile_url: str) -> Dict[str, Any]:
        """Analiza un perfil de Facebook"""
        try:
            profile_id = self._extract_facebook_profile_id(profile_url)
            if not profile_id:
                return {}
            
            # Simulación de análisis de Facebook
            profile_info = {
                "platform": "facebook",
                "profile_id": profile_id,
                "profile_url": profile_url,
                "name": "Nombre no disponible sin API",
                "friends_count": "No disponible sin API",
                "verified": False,
                "profile_image": None
            }
            
            return {
                "profile_info": profile_info,
                "posts": [],
                "connections": [],
                "activity_analysis": {
                    "posting_frequency": "No disponible",
                    "engagement_rate": "No disponible"
                }
            }
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error Facebook: {str(e)}")
            return {}
    
    def _extract_facebook_profile_id(self, url: str) -> Optional[str]:
        """Extrae el ID del perfil de Facebook"""
        try:
            # Facebook tiene múltiples formatos de URL
            patterns = [
                r'facebook\.com/([^/?]+)',
                r'facebook\.com/profile\.php\?id=(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    profile_id = match.group(1)
                    return profile_id
            
            return None
        except Exception:
            return None
    
    def _analyze_youtube(self, profile_url: str) -> Dict[str, Any]:
        """Analiza un canal de YouTube"""
        try:
            channel_id = self._extract_youtube_channel_id(profile_url)
            if not channel_id:
                return {}
            
            # Simulación de análisis de YouTube
            profile_info = {
                "platform": "youtube",
                "channel_id": channel_id,
                "profile_url": profile_url,
                "name": "Nombre del canal no disponible sin API",
                "subscribers_count": "No disponible sin API",
                "videos_count": "No disponible sin API",
                "description": "Descripción no disponible sin API",
                "verified": False,
                "profile_image": None
            }
            
            return {
                "profile_info": profile_info,
                "posts": [],
                "connections": [],
                "activity_analysis": {
                    "upload_frequency": "No disponible",
                    "most_popular_videos": [],
                    "engagement_rate": "No disponible"
                }
            }
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error YouTube: {str(e)}")
            return {}
    
    def _extract_youtube_channel_id(self, url: str) -> Optional[str]:
        """Extrae el ID del canal de YouTube"""
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            # Buscar channel_id en parámetros de consulta
            if 'channel' in query_params:
                return query_params['channel'][0]
            
            # Buscar en el path
            path_parts = parsed_url.path.split('/')
            for part in path_parts:
                if part.startswith('UC'):
                    return part
            
            return None
        except Exception:
            return None
    
    def _analyze_tiktok(self, profile_url: str) -> Dict[str, Any]:
        """Analiza un perfil de TikTok"""
        try:
            username = self._extract_tiktok_username(profile_url)
            if not username:
                return {}
            
            # Simulación de análisis de TikTok
            profile_info = {
                "platform": "tiktok",
                "username": username,
                "profile_url": profile_url,
                "display_name": username,
                "followers_count": "No disponible sin API",
                "following_count": "No disponible sin API",
                "likes_count": "No disponible sin API",
                "verified": False,
                "profile_image": None
            }
            
            return {
                "profile_info": profile_info,
                "posts": [],
                "connections": [],
                "activity_analysis": {
                    "posting_frequency": "No disponible",
                    "most_popular_videos": [],
                    "engagement_rate": "No disponible"
                }
            }
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error TikTok: {str(e)}")
            return {}
    
    def _extract_tiktok_username(self, url: str) -> Optional[str]:
        """Extrae el username de una URL de TikTok"""
        try:
            pattern = r'tiktok\.com/@([^/?]+)'
            match = re.search(pattern, url)
            if match:
                username = match.group(1)
                return username
            return None
        except Exception:
            return None
    
    def _analyze_activity_patterns(self) -> None:
        """Analiza patrones de actividad del perfil"""
        try:
            # Análisis básico de patrones de actividad
            if self.results.get("posts"):
                posts = self.results["posts"]
                
                # Análisis de frecuencia de posts
                if len(posts) > 1:
                    # Calcular frecuencia promedio
                    self.results["activity_analysis"]["posting_frequency"] = "Análisis disponible"
                
                # Análisis de hashtags más usados
                hashtags = []
                for post in posts:
                    if "hashtags" in post:
                        hashtags.extend(post["hashtags"])
                
                if hashtags:
                    from collections import Counter
                    hashtag_counts = Counter(hashtags)
                    self.results["activity_analysis"]["most_used_hashtags"] = [
                        {"hashtag": tag, "count": count}
                        for tag, count in hashtag_counts.most_common(10)
                    ]
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error análisis de actividad: {str(e)}")
    
    def _analyze_geolocation_data(self) -> None:
        """Analiza datos de geolocalización"""
        try:
            # Extraer información de geolocalización de posts
            if self.results.get("posts"):
                for post in self.results["posts"]:
                    if "location" in post and post["location"]:
                        self.results["geolocation"].append({
                            "post_id": post.get("id"),
                            "location": post["location"],
                            "timestamp": post.get("created_at")
                        })
            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error geolocalización: {str(e)}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del análisis"""
        return {
            "platform": self.results.get("profile_info", {}).get("platform"),
            "username": self.results.get("profile_info", {}).get("username"),
            "total_posts": len(self.results["posts"]),
            "total_connections": len(self.results["connections"]),
            "total_locations": len(self.results["geolocation"]),
            "scan_duration": self.results["metadata"]["scan_time"],
            "tools_used": self.results["metadata"]["tools_used"],
            "errors": len(self.results["metadata"]["errors"])
        }