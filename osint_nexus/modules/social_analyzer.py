"""
Módulo de análisis de redes sociales (SOCMINT)
"""

import requests
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs
import time

class SocialAnalyzer:
    """Analizador de perfiles de redes sociales"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Inicializa el analizador social
        
        Args:
            api_keys: Diccionario con claves de API
        """
        self.api_keys = api_keys or {}
        self.results = {}
        self.supported_platforms = {
            'facebook': self._analyze_facebook,
            'twitter': self._analyze_twitter,
            'instagram': self._analyze_instagram,
            'linkedin': self._analyze_linkedin,
            'github': self._analyze_github,
            'youtube': self._analyze_youtube,
            'tiktok': self._analyze_tiktok,
            'reddit': self._analyze_reddit
        }
    
    def analyze_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Analiza un perfil de red social
        
        Args:
            profile_url: URL del perfil a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        platform = self._identify_platform(profile_url)
        
        if not platform:
            return {'error': 'Platform not supported or URL invalid'}
        
        results = {
            'profile_url': profile_url,
            'platform': platform,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'basic_info': self._get_basic_info(profile_url),
            'platform_analysis': self._analyze_platform_specific(profile_url, platform),
            'content_analysis': self._analyze_content(profile_url, platform),
            'network_analysis': self._analyze_network(profile_url, platform),
            'activity_analysis': self._analyze_activity(profile_url, platform),
            'security_analysis': self._analyze_security(profile_url, platform),
            'metadata': self._extract_metadata(profile_url)
        }
        
        self.results = results
        return results
    
    def _identify_platform(self, url: str) -> Optional[str]:
        """Identifica la plataforma de red social desde la URL"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        platform_domains = {
            'facebook.com': 'facebook',
            'www.facebook.com': 'facebook',
            'twitter.com': 'twitter',
            'www.twitter.com': 'twitter',
            'instagram.com': 'instagram',
            'www.instagram.com': 'instagram',
            'linkedin.com': 'linkedin',
            'www.linkedin.com': 'linkedin',
            'github.com': 'github',
            'www.github.com': 'github',
            'youtube.com': 'youtube',
            'www.youtube.com': 'youtube',
            'tiktok.com': 'tiktok',
            'www.tiktok.com': 'tiktok',
            'reddit.com': 'reddit',
            'www.reddit.com': 'reddit'
        }
        
        return platform_domains.get(domain)
    
    def _get_basic_info(self, url: str) -> Dict[str, Any]:
        """Obtiene información básica del perfil"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return {
                    'status_code': response.status_code,
                    'content_length': len(response.content),
                    'content_type': response.headers.get('content-type', ''),
                    'server': response.headers.get('server', ''),
                    'last_modified': response.headers.get('last-modified', ''),
                    'accessible': True
                }
            else:
                return {
                    'status_code': response.status_code,
                    'accessible': False,
                    'error': 'Profile not accessible'
                }
                
        except Exception as e:
            return {
                'accessible': False,
                'error': str(e)
            }
    
    def _analyze_platform_specific(self, url: str, platform: str) -> Dict[str, Any]:
        """Análisis específico según la plataforma"""
        if platform in self.supported_platforms:
            return self.supported_platforms[platform](url)
        else:
            return {'error': f'Platform {platform} not supported'}
    
    def _analyze_facebook(self, url: str) -> Dict[str, Any]:
        """Análisis específico de Facebook"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            # Extraer información usando regex
            profile_info = {
                'name': self._extract_facebook_name(content),
                'profile_id': self._extract_facebook_id(content),
                'profile_type': self._detect_facebook_type(content),
                'verified': self._check_facebook_verification(content),
                'location': self._extract_facebook_location(content),
                'work': self._extract_facebook_work(content),
                'education': self._extract_facebook_education(content),
                'relationship': self._extract_facebook_relationship(content),
                'friends_count': self._extract_facebook_friends(content),
                'photos_count': self._extract_facebook_photos(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_twitter(self, url: str) -> Dict[str, Any]:
        """Análisis específico de Twitter"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'username': self._extract_twitter_username(url),
                'display_name': self._extract_twitter_display_name(content),
                'bio': self._extract_twitter_bio(content),
                'location': self._extract_twitter_location(content),
                'website': self._extract_twitter_website(content),
                'joined_date': self._extract_twitter_joined_date(content),
                'verified': self._check_twitter_verification(content),
                'followers_count': self._extract_twitter_followers(content),
                'following_count': self._extract_twitter_following(content),
                'tweets_count': self._extract_twitter_tweets(content),
                'profile_image': self._extract_twitter_profile_image(content),
                'banner_image': self._extract_twitter_banner(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_instagram(self, url: str) -> Dict[str, Any]:
        """Análisis específico de Instagram"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'username': self._extract_instagram_username(url),
                'display_name': self._extract_instagram_display_name(content),
                'bio': self._extract_instagram_bio(content),
                'website': self._extract_instagram_website(content),
                'category': self._extract_instagram_category(content),
                'verified': self._check_instagram_verification(content),
                'private': self._check_instagram_privacy(content),
                'followers_count': self._extract_instagram_followers(content),
                'following_count': self._extract_instagram_following(content),
                'posts_count': self._extract_instagram_posts(content),
                'profile_image': self._extract_instagram_profile_image(content),
                'business_account': self._check_instagram_business(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_linkedin(self, url: str) -> Dict[str, Any]:
        """Análisis específico de LinkedIn"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'name': self._extract_linkedin_name(content),
                'headline': self._extract_linkedin_headline(content),
                'location': self._extract_linkedin_location(content),
                'industry': self._extract_linkedin_industry(content),
                'current_company': self._extract_linkedin_current_company(content),
                'education': self._extract_linkedin_education(content),
                'connections': self._extract_linkedin_connections(content),
                'skills': self._extract_linkedin_skills(content),
                'languages': self._extract_linkedin_languages(content),
                'profile_image': self._extract_linkedin_profile_image(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_github(self, url: str) -> Dict[str, Any]:
        """Análisis específico de GitHub"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'username': self._extract_github_username(url),
                'name': self._extract_github_name(content),
                'bio': self._extract_github_bio(content),
                'location': self._extract_github_location(content),
                'website': self._extract_github_website(content),
                'company': self._extract_github_company(content),
                'email': self._extract_github_email(content),
                'repositories': self._extract_github_repositories(content),
                'followers': self._extract_github_followers(content),
                'following': self._extract_github_following(content),
                'contributions': self._extract_github_contributions(content),
                'languages': self._extract_github_languages(content),
                'profile_image': self._extract_github_profile_image(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_youtube(self, url: str) -> Dict[str, Any]:
        """Análisis específico de YouTube"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'channel_name': self._extract_youtube_channel_name(content),
                'subscribers': self._extract_youtube_subscribers(content),
                'videos_count': self._extract_youtube_videos(content),
                'views_count': self._extract_youtube_views(content),
                'description': self._extract_youtube_description(content),
                'country': self._extract_youtube_country(content),
                'joined_date': self._extract_youtube_joined_date(content),
                'verified': self._check_youtube_verification(content),
                'channel_image': self._extract_youtube_channel_image(content),
                'banner_image': self._extract_youtube_banner(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_tiktok(self, url: str) -> Dict[str, Any]:
        """Análisis específico de TikTok"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'username': self._extract_tiktok_username(url),
                'display_name': self._extract_tiktok_display_name(content),
                'bio': self._extract_tiktok_bio(content),
                'followers': self._extract_tiktok_followers(content),
                'following': self._extract_tiktok_following(content),
                'likes': self._extract_tiktok_likes(content),
                'videos_count': self._extract_tiktok_videos(content),
                'verified': self._check_tiktok_verification(content),
                'profile_image': self._extract_tiktok_profile_image(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_reddit(self, url: str) -> Dict[str, Any]:
        """Análisis específico de Reddit"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            profile_info = {
                'username': self._extract_reddit_username(url),
                'karma': self._extract_reddit_karma(content),
                'cake_day': self._extract_reddit_cake_day(content),
                'posts': self._extract_reddit_posts(content),
                'comments': self._extract_reddit_comments(content),
                'trophies': self._extract_reddit_trophies(content),
                'subreddits': self._extract_reddit_subreddits(content)
            }
            
            return profile_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_content(self, url: str, platform: str) -> Dict[str, Any]:
        """Análisis de contenido del perfil"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            # Análisis de contenido general
            content_analysis = {
                'languages_detected': self._detect_languages(content),
                'sentiment_analysis': self._analyze_sentiment(content),
                'topics': self._extract_topics(content),
                'hashtags': self._extract_hashtags(content),
                'mentions': self._extract_mentions(content),
                'links': self._extract_links(content),
                'images': self._extract_images(content),
                'videos': self._extract_videos(content)
            }
            
            return content_analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_network(self, url: str, platform: str) -> Dict[str, Any]:
        """Análisis de red de conexiones"""
        try:
            # Análisis básico de red
            network_analysis = {
                'connection_type': self._determine_connection_type(platform),
                'network_size': self._estimate_network_size(url, platform),
                'interaction_patterns': self._analyze_interactions(url, platform),
                'influence_score': self._calculate_influence_score(url, platform),
                'community_detection': self._detect_communities(url, platform)
            }
            
            return network_analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_activity(self, url: str, platform: str) -> Dict[str, Any]:
        """Análisis de actividad del perfil"""
        try:
            activity_analysis = {
                'posting_frequency': self._estimate_posting_frequency(url, platform),
                'activity_patterns': self._analyze_activity_patterns(url, platform),
                'engagement_rate': self._calculate_engagement_rate(url, platform),
                'peak_hours': self._identify_peak_hours(url, platform),
                'content_types': self._analyze_content_types(url, platform)
            }
            
            return activity_analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_security(self, url: str, platform: str) -> Dict[str, Any]:
        """Análisis de seguridad del perfil"""
        try:
            security_analysis = {
                'privacy_level': self._assess_privacy_level(url, platform),
                'exposed_information': self._identify_exposed_info(url, platform),
                'security_score': self._calculate_security_score(url, platform),
                'recommendations': self._generate_security_recommendations(url, platform)
            }
            
            return security_analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_metadata(self, url: str) -> Dict[str, Any]:
        """Extrae metadatos del perfil"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            content = response.text
            
            metadata = {
                'og_tags': self._extract_og_tags(content),
                'twitter_cards': self._extract_twitter_cards(content),
                'json_ld': self._extract_json_ld(content),
                'meta_tags': self._extract_meta_tags(content)
            }
            
            return metadata
            
        except Exception as e:
            return {'error': str(e)}
    
    # Métodos auxiliares de extracción de datos específicos por plataforma
    
    def _extract_facebook_name(self, content: str) -> str:
        """Extrae el nombre de Facebook"""
        patterns = [
            r'<title>(.*?) \| Facebook</title>',
            r'"name":"([^"]+)"'
        ]
        return self._extract_with_patterns(content, patterns)
    
    def _extract_twitter_username(self, url: str) -> str:
        """Extrae el username de Twitter de la URL"""
        match = re.search(r'twitter\.com/([^/]+)', url)
        return match.group(1) if match else ''
    
    def _extract_instagram_username(self, url: str) -> str:
        """Extrae el username de Instagram de la URL"""
        match = re.search(r'instagram\.com/([^/]+)', url)
        return match.group(1) if match else ''
    
    def _extract_github_username(self, url: str) -> str:
        """Extrae el username de GitHub de la URL"""
        match = re.search(r'github\.com/([^/]+)', url)
        return match.group(1) if match else ''
    
    def _extract_with_patterns(self, content: str, patterns: List[str]) -> str:
        """Extrae información usando múltiples patrones"""
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ''
    
    def _extract_numbers_with_patterns(self, content: str, patterns: List[str]) -> int:
        """Extrae números usando múltiples patrones"""
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                number_str = match.group(1).replace(',', '').replace('.', '')
                try:
                    return int(re.sub(r'[^\d]', '', number_str))
                except ValueError:
                    continue
        return 0
    
    # Implementaciones básicas de métodos de extracción
    # (En una implementación completa, estos métodos tendrían patrones más específicos)
    
    def _extract_facebook_id(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"userID":"([^"]+)"'])
    
    def _detect_facebook_type(self, content: str) -> str:
        if 'Page' in content:
            return 'page'
        elif 'Profile' in content:
            return 'profile'
        return 'unknown'
    
    def _check_facebook_verification(self, content: str) -> bool:
        return 'verified' in content.lower()
    
    def _extract_facebook_location(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"location":"([^"]+)"'])
    
    def _extract_facebook_work(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"work":"([^"]+)"'])
    
    def _extract_facebook_education(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"education":"([^"]+)"'])
    
    def _extract_facebook_relationship(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"relationship":"([^"]+)"'])
    
    def _extract_facebook_friends(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'(\d+)\s+friends'])
    
    def _extract_facebook_photos(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'(\d+)\s+photos'])
    
    # Métodos similares para otras plataformas...
    # (Implementaciones básicas para demostrar la estructura)
    
    def _extract_twitter_display_name(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"name":"([^"]+)"'])
    
    def _extract_twitter_bio(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"description":"([^"]+)"'])
    
    def _extract_twitter_location(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"location":"([^"]+)"'])
    
    def _extract_twitter_website(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"url":"([^"]+)"'])
    
    def _extract_twitter_joined_date(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"created_at":"([^"]+)"'])
    
    def _check_twitter_verification(self, content: str) -> bool:
        return 'verified' in content.lower()
    
    def _extract_twitter_followers(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'(\d+)\s+followers'])
    
    def _extract_twitter_following(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'(\d+)\s+following'])
    
    def _extract_twitter_tweets(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'(\d+)\s+tweets'])
    
    def _extract_twitter_profile_image(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"profile_image_url":"([^"]+)"'])
    
    def _extract_twitter_banner(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"profile_banner_url":"([^"]+)"'])
    
    # Métodos de análisis avanzado
    
    def _detect_languages(self, content: str) -> List[str]:
        """Detecta idiomas en el contenido"""
        # Implementación básica - en producción se usaría una librería como langdetect
        return ['en']  # Placeholder
    
    def _analyze_sentiment(self, content: str) -> Dict[str, float]:
        """Analiza el sentimiento del contenido"""
        # Implementación básica - en producción se usaría VADER o similar
        return {'positive': 0.5, 'negative': 0.3, 'neutral': 0.2}
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extrae temas principales"""
        # Implementación básica usando palabras clave
        return []
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extrae hashtags"""
        return re.findall(r'#\w+', content)
    
    def _extract_mentions(self, content: str) -> List[str]:
        """Extrae menciones"""
        return re.findall(r'@\w+', content)
    
    def _extract_links(self, content: str) -> List[str]:
        """Extrae links"""
        return re.findall(r'https?://[^\s]+', content)
    
    def _extract_images(self, content: str) -> List[str]:
        """Extrae URLs de imágenes"""
        return re.findall(r'<img[^>]+src="([^"]+)"', content)
    
    def _extract_videos(self, content: str) -> List[str]:
        """Extrae URLs de videos"""
        return re.findall(r'<video[^>]+src="([^"]+)"', content)
    
    def _extract_og_tags(self, content: str) -> Dict[str, str]:
        """Extrae OpenGraph tags"""
        og_tags = {}
        pattern = r'<meta\s+property="og:([^"]+)"\s+content="([^"]+)"'
        matches = re.findall(pattern, content)
        for key, value in matches:
            og_tags[key] = value
        return og_tags
    
    def _extract_twitter_cards(self, content: str) -> Dict[str, str]:
        """Extrae Twitter Card metadata"""
        twitter_cards = {}
        pattern = r'<meta\s+name="twitter:([^"]+)"\s+content="([^"]+)"'
        matches = re.findall(pattern, content)
        for key, value in matches:
            twitter_cards[key] = value
        return twitter_cards
    
    def _extract_json_ld(self, content: str) -> Dict[str, Any]:
        """Extrae JSON-LD estructurado"""
        json_ld = {}
        pattern = r'<script type="application/ld\+json">(.*?)</script>'
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            try:
                json_ld.update(json.loads(match))
            except json.JSONDecodeError:
                continue
        return json_ld
    
    def _extract_meta_tags(self, content: str) -> Dict[str, str]:
        """Extrae meta tags generales"""
        meta_tags = {}
        pattern = r'<meta\s+name="([^"]+)"\s+content="([^"]+)"'
        matches = re.findall(pattern, content)
        for key, value in matches:
            meta_tags[key] = value
        return meta_tags
    
    # Métodos de análisis avanzado (implementaciones básicas)
    
    def _determine_connection_type(self, platform: str) -> str:
        """Determina el tipo de conexión de la plataforma"""
        connection_types = {
            'facebook': 'friends',
            'twitter': 'followers',
            'instagram': 'followers',
            'linkedin': 'connections',
            'github': 'followers',
            'youtube': 'subscribers'
        }
        return connection_types.get(platform, 'unknown')
    
    def _estimate_network_size(self, url: str, platform: str) -> int:
        """Estima el tamaño de la red"""
        # Implementación básica
        return 0
    
    def _analyze_interactions(self, url: str, platform: str) -> Dict[str, Any]:
        """Analiza patrones de interacción"""
        return {'likes': 0, 'comments': 0, 'shares': 0}
    
    def _calculate_influence_score(self, url: str, platform: str) -> float:
        """Calcula puntuación de influencia"""
        return 0.0
    
    def _detect_communities(self, url: str, platform: str) -> List[str]:
        """Detecta comunidades relacionadas"""
        return []
    
    def _estimate_posting_frequency(self, url: str, platform: str) -> str:
        """Estima frecuencia de publicación"""
        return 'unknown'
    
    def _analyze_activity_patterns(self, url: str, platform: str) -> Dict[str, Any]:
        """Analiza patrones de actividad"""
        return {'peak_days': [], 'activity_score': 0}
    
    def _calculate_engagement_rate(self, url: str, platform: str) -> float:
        """Calcula tasa de engagement"""
        return 0.0
    
    def _identify_peak_hours(self, url: str, platform: str) -> List[str]:
        """Identifica horas pico de actividad"""
        return []
    
    def _analyze_content_types(self, url: str, platform: str) -> Dict[str, int]:
        """Analiza tipos de contenido"""
        return {'text': 0, 'image': 0, 'video': 0, 'link': 0}
    
    def _assess_privacy_level(self, url: str, platform: str) -> str:
        """Evalúa nivel de privacidad"""
        return 'unknown'
    
    def _identify_exposed_info(self, url: str, platform: str) -> List[str]:
        """Identifica información expuesta"""
        return []
    
    def _calculate_security_score(self, url: str, platform: str) -> int:
        """Calcula puntuación de seguridad"""
        return 50  # Neutral
    
    def _generate_security_recommendations(self, url: str, platform: str) -> List[str]:
        """Genera recomendaciones de seguridad"""
        return ['Review privacy settings', 'Limit personal information exposure']
    
    # Métodos de extracción para otras plataformas (implementaciones básicas)
    
    def _extract_instagram_display_name(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"full_name":"([^"]+)"'])
    
    def _extract_instagram_bio(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"biography":"([^"]+)"'])
    
    def _extract_instagram_website(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"external_url":"([^"]+)"'])
    
    def _extract_instagram_category(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"category":"([^"]+)"'])
    
    def _check_instagram_verification(self, content: str) -> bool:
        return 'is_verified":true' in content
    
    def _check_instagram_privacy(self, content: str) -> bool:
        return 'is_private":true' in content
    
    def _extract_instagram_followers(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'"edge_followed_by":{"count":(\d+)'])
    
    def _extract_instagram_following(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'"edge_follow":{"count":(\d+)'])
    
    def _extract_instagram_posts(self, content: str) -> int:
        return self._extract_numbers_with_patterns(content, [r'"edge_owner_to_timeline_media":{"count":(\d+)'])
    
    def _extract_instagram_profile_image(self, content: str) -> str:
        return self._extract_with_patterns(content, [r'"profile_pic_url":"([^"]+)"'])
    
    def _check_instagram_business(self, content: str) -> bool:
        return 'is_business_account":true' in content
    
    def generate_summary(self) -> Dict[str, Any]:
        """Genera un resumen del análisis"""
        if not self.results:
            return {'error': 'No analysis results available'}
        
        basic_info = self.results.get('basic_info', {})
        platform_analysis = self.results.get('platform_analysis', {})
        content_analysis = self.results.get('content_analysis', {})
        
        summary = {
            'profile_url': self.results.get('profile_url'),
            'platform': self.results.get('platform'),
            'analysis_date': self.results.get('timestamp'),
            'accessibility': {
                'accessible': basic_info.get('accessible', False),
                'status_code': basic_info.get('status_code', 0)
            },
            'profile_info': {
                'name': platform_analysis.get('name', ''),
                'username': platform_analysis.get('username', ''),
                'bio': platform_analysis.get('bio', ''),
                'location': platform_analysis.get('location', ''),
                'verified': platform_analysis.get('verified', False)
            },
            'metrics': {
                'followers': platform_analysis.get('followers', 0),
                'following': platform_analysis.get('following', 0),
                'posts': platform_analysis.get('posts', 0)
            },
            'content': {
                'languages': content_analysis.get('languages_detected', []),
                'topics': content_analysis.get('topics', []),
                'hashtags_count': len(content_analysis.get('hashtags', [])),
                'links_count': len(content_analysis.get('links', []))
            }
        }
        
        return summary