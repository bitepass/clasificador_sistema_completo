"""
Módulo de Búsqueda de Nombres de Usuario
Busca un alias en múltiples plataformas sociales
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from fake_useragent import UserAgent

from utils.api_manager import APIManager
from config.api_keys import APIConfig

logger = logging.getLogger(__name__)

class UsernameSearcher:
    """Buscador de nombres de usuario en múltiples plataformas"""
    
    def __init__(self):
        self.api_manager = APIManager()
        self.ua = UserAgent()
        
        # Diccionario de plataformas y sus URLs de perfil
        self.platforms = {
            'Twitter': 'https://twitter.com/{}',
            'Instagram': 'https://www.instagram.com/{}/',
            'Facebook': 'https://www.facebook.com/{}',
            'GitHub': 'https://github.com/{}',
            'LinkedIn': 'https://www.linkedin.com/in/{}',
            'YouTube': 'https://www.youtube.com/@{}',
            'TikTok': 'https://www.tiktok.com/@{}',
            'Pinterest': 'https://www.pinterest.com/{}/',
            'Reddit': 'https://www.reddit.com/user/{}',
            'Twitch': 'https://www.twitch.tv/{}',
            'Steam': 'https://steamcommunity.com/id/{}',
            'Spotify': 'https://open.spotify.com/user/{}',
            'Medium': 'https://medium.com/@{}',
            'Dev.to': 'https://dev.to/{}',
            'Dribbble': 'https://dribbble.com/{}',
            'Behance': 'https://www.behance.net/{}',
            'GitLab': 'https://gitlab.com/{}',
            'Bitbucket': 'https://bitbucket.org/{}/',
            'CodePen': 'https://codepen.io/{}',
            'Replit': 'https://replit.com/@{}',
            'Telegram': 'https://t.me/{}',
            'WhatsApp': 'https://wa.me/{}',
            'Snapchat': 'https://www.snapchat.com/add/{}',
            'Flickr': 'https://www.flickr.com/people/{}',
            'Tumblr': 'https://{}.tumblr.com/',
            'SoundCloud': 'https://soundcloud.com/{}',
            'Vimeo': 'https://vimeo.com/{}',
            'VK': 'https://vk.com/{}',
            'Discord': 'https://discord.com/users/{}',
            'Slack': 'https://{}.slack.com',
            'Keybase': 'https://keybase.io/{}',
            'Patreon': 'https://www.patreon.com/{}',
            'PayPal': 'https://www.paypal.me/{}',
            'CashApp': 'https://cash.app/${}',
            'Venmo': 'https://venmo.com/{}',
            'About.me': 'https://about.me/{}',
            'Linktree': 'https://linktr.ee/{}',
            'Xbox': 'https://account.xbox.com/profile?gamertag={}',
            'PlayStation': 'https://psnprofiles.com/{}',
            'Roblox': 'https://www.roblox.com/users/profile?username={}',
            'Minecraft': 'https://namemc.com/profile/{}',
            'Fortnite': 'https://fortnitetracker.com/profile/all/{}',
            'Chess.com': 'https://www.chess.com/member/{}',
            'HackerNews': 'https://news.ycombinator.com/user?id={}',
            'HackerRank': 'https://www.hackerrank.com/{}',
            'LeetCode': 'https://leetcode.com/{}',
            'Kaggle': 'https://www.kaggle.com/{}',
            'NPM': 'https://www.npmjs.com/~{}',
            'PyPI': 'https://pypi.org/user/{}/',
            'DockerHub': 'https://hub.docker.com/u/{}',
            'ProductHunt': 'https://www.producthunt.com/@{}'
        }
        
    async def search_username(self, username: str) -> Dict[str, Any]:
        """
        Buscar un nombre de usuario en múltiples plataformas
        
        Args:
            username: Nombre de usuario a buscar
            
        Returns:
            Diccionario con los resultados de la búsqueda
        """
        logger.info(f"Iniciando búsqueda de username: {username}")
        
        # Validar username
        if not username or len(username) < 2:
            return {'error': 'Nombre de usuario inválido'}
        
        # Ejecutar búsquedas en paralelo
        tasks = []
        for platform, url_template in self.platforms.items():
            url = url_template.format(username)
            task = self._check_platform(platform, url, username)
            tasks.append(task)
        
        # Limitar concurrencia para evitar bloqueos
        results = []
        for i in range(0, len(tasks), 10):  # Procesar de 10 en 10
            batch = tasks[i:i+10]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_results)
            await asyncio.sleep(0.5)  # Pequeña pausa entre batches
        
        # Procesar resultados
        found_profiles = []
        possible_profiles = []
        not_found = []
        
        for result in results:
            if isinstance(result, Exception):
                logger.debug(f"Error en búsqueda: {result}")
                continue
                
            if result['status'] == 'found':
                found_profiles.append(result)
            elif result['status'] == 'possible':
                possible_profiles.append(result)
            else:
                not_found.append(result['platform'])
        
        # Análisis adicional
        profile_analysis = self._analyze_profiles(found_profiles, username)
        
        return {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'total_platforms_checked': len(self.platforms),
            'profiles_found': len(found_profiles),
            'profiles_possible': len(possible_profiles),
            'found': found_profiles,
            'possible': possible_profiles,
            'not_found': not_found,
            'analysis': profile_analysis
        }
    
    async def _check_platform(self, platform: str, url: str, username: str) -> Dict[str, Any]:
        """Verificar si un username existe en una plataforma específica"""
        try:
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers, allow_redirects=True) as response:
                    status_code = response.status
                    
                    # Analizar respuesta según el código de estado
                    if status_code == 200:
                        # Verificar contenido para confirmar que es un perfil válido
                        content = await response.text()
                        
                        # Patrones de no existencia comunes
                        not_found_patterns = [
                            'page not found', 'user not found', 'does not exist',
                            '404', 'sorry', 'couldn\'t find', 'no existe',
                            'profile unavailable', 'suspended', 'deleted'
                        ]
                        
                        content_lower = content.lower()
                        
                        # Si contiene patrones de no encontrado
                        if any(pattern in content_lower for pattern in not_found_patterns):
                            return {
                                'platform': platform,
                                'url': url,
                                'status': 'not_found'
                            }
                        
                        # Si contiene el username en el contenido (buena señal)
                        if username.lower() in content_lower:
                            # Extraer metadatos si es posible
                            metadata = self._extract_metadata(content, platform)
                            
                            return {
                                'platform': platform,
                                'url': url,
                                'status': 'found',
                                'metadata': metadata
                            }
                        else:
                            # Posible perfil pero no confirmado
                            return {
                                'platform': platform,
                                'url': url,
                                'status': 'possible'
                            }
                    
                    elif status_code == 404:
                        return {
                            'platform': platform,
                            'url': url,
                            'status': 'not_found'
                        }
                    
                    elif status_code in [301, 302]:
                        # Redirección podría indicar que existe
                        return {
                            'platform': platform,
                            'url': url,
                            'status': 'possible',
                            'note': 'Redirección detectada'
                        }
                    
                    else:
                        return {
                            'platform': platform,
                            'url': url,
                            'status': 'unknown',
                            'status_code': status_code
                        }
                        
        except asyncio.TimeoutError:
            return {
                'platform': platform,
                'url': url,
                'status': 'timeout'
            }
        except Exception as e:
            logger.debug(f"Error verificando {platform}: {e}")
            return {
                'platform': platform,
                'url': url,
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_metadata(self, content: str, platform: str) -> Dict[str, Any]:
        """Extraer metadatos básicos del perfil"""
        metadata = {}
        
        try:
            # Buscar título de la página
            import re
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            # Buscar meta descripción
            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
            if desc_match:
                metadata['description'] = desc_match.group(1).strip()
            
            # Buscar imagen de perfil (patrones comunes)
            img_patterns = [
                r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']',
                r'<img[^>]+class=["\'][^"\']*avatar[^"\']*["\']\s+src=["\'](.*?)["\']',
                r'<img[^>]+class=["\'][^"\']*profile[^"\']*["\']\s+src=["\'](.*?)["\']'
            ]
            
            for pattern in img_patterns:
                img_match = re.search(pattern, content, re.IGNORECASE)
                if img_match:
                    metadata['profile_image'] = img_match.group(1)
                    break
            
            # Extraer información específica por plataforma
            if platform == 'Twitter':
                # Buscar conteo de seguidores
                followers_match = re.search(r'([0-9,]+)\s*Followers', content, re.IGNORECASE)
                if followers_match:
                    metadata['followers'] = followers_match.group(1)
                    
            elif platform == 'GitHub':
                # Buscar repositorios
                repos_match = re.search(r'([0-9]+)\s*repositories', content, re.IGNORECASE)
                if repos_match:
                    metadata['repositories'] = repos_match.group(1)
                    
        except Exception as e:
            logger.debug(f"Error extrayendo metadata de {platform}: {e}")
            
        return metadata
    
    def _analyze_profiles(self, profiles: List[Dict], username: str) -> Dict[str, Any]:
        """Analizar los perfiles encontrados para obtener insights"""
        analysis = {
            'total_profiles': len(profiles),
            'platforms_by_category': {},
            'profile_completeness': 0,
            'digital_footprint_score': 0
        }
        
        # Categorizar plataformas
        categories = {
            'social_media': ['Twitter', 'Instagram', 'Facebook', 'TikTok', 'LinkedIn', 'Snapchat', 'Tumblr'],
            'professional': ['LinkedIn', 'GitHub', 'GitLab', 'Bitbucket', 'Medium', 'Dev.to', 'Behance'],
            'gaming': ['Steam', 'Xbox', 'PlayStation', 'Roblox', 'Minecraft', 'Fortnite', 'Twitch'],
            'financial': ['PayPal', 'CashApp', 'Venmo', 'Patreon'],
            'messaging': ['Telegram', 'WhatsApp', 'Discord', 'Slack'],
            'content': ['YouTube', 'Vimeo', 'SoundCloud', 'Spotify', 'Flickr'],
            'coding': ['GitHub', 'GitLab', 'Bitbucket', 'CodePen', 'Replit', 'HackerRank', 'LeetCode']
        }
        
        for category, platforms in categories.items():
            count = sum(1 for p in profiles if p['platform'] in platforms)
            if count > 0:
                analysis['platforms_by_category'][category] = count
        
        # Calcular completitud del perfil
        important_platforms = ['GitHub', 'LinkedIn', 'Twitter', 'Instagram', 'Facebook']
        found_important = sum(1 for p in profiles if p['platform'] in important_platforms)
        analysis['profile_completeness'] = (found_important / len(important_platforms)) * 100
        
        # Calcular score de huella digital
        analysis['digital_footprint_score'] = min(100, len(profiles) * 4)
        
        # Detectar patrones
        patterns = []
        
        if analysis['platforms_by_category'].get('professional', 0) >= 3:
            patterns.append('Fuerte presencia profesional')
            
        if analysis['platforms_by_category'].get('gaming', 0) >= 3:
            patterns.append('Gamer activo')
            
        if analysis['platforms_by_category'].get('coding', 0) >= 2:
            patterns.append('Desarrollador/Programador')
            
        if analysis['platforms_by_category'].get('content', 0) >= 2:
            patterns.append('Creador de contenido')
            
        analysis['patterns'] = patterns
        
        return analysis