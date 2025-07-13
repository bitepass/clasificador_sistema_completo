"""
Módulo de búsqueda de nombres de usuario en redes sociales
"""

import requests
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class UsernameAnalyzer:
    """Analizador de nombres de usuario en redes sociales"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Inicializa el analizador de usernames
        
        Args:
            api_keys: Diccionario con claves de API
        """
        self.api_keys = api_keys or {}
        self.results = {}
        self.platforms = self._get_platforms()
    
    def _get_platforms(self) -> List[Dict[str, str]]:
        """Define las plataformas de redes sociales a verificar"""
        return [
            {
                'name': 'Facebook',
                'url': 'https://www.facebook.com/{}',
                'check_url': 'https://www.facebook.com/{}',
                'method': 'GET',
                'success_indicators': ['og:title', 'fb:page_id'],
                'error_indicators': ['This content isn\'t available', 'Page Not Found']
            },
            {
                'name': 'Twitter',
                'url': 'https://twitter.com/{}',
                'check_url': 'https://twitter.com/{}',
                'method': 'GET',
                'success_indicators': ['twitter:title', 'ProfilePage'],
                'error_indicators': ['This account doesn\'t exist', 'suspended']
            },
            {
                'name': 'Instagram',
                'url': 'https://www.instagram.com/{}',
                'check_url': 'https://www.instagram.com/{}',
                'method': 'GET',
                'success_indicators': ['og:title', 'ProfilePage'],
                'error_indicators': ['Page Not Found', 'isn\'t available']
            },
            {
                'name': 'LinkedIn',
                'url': 'https://www.linkedin.com/in/{}',
                'check_url': 'https://www.linkedin.com/in/{}',
                'method': 'GET',
                'success_indicators': ['linkedin:owner', 'profile'],
                'error_indicators': ['Page not found', 'Profile not found']
            },
            {
                'name': 'GitHub',
                'url': 'https://github.com/{}',
                'check_url': 'https://github.com/{}',
                'method': 'GET',
                'success_indicators': ['github.com', 'user-profile'],
                'error_indicators': ['404', 'Not Found']
            },
            {
                'name': 'YouTube',
                'url': 'https://www.youtube.com/user/{}',
                'check_url': 'https://www.youtube.com/user/{}',
                'method': 'GET',
                'success_indicators': ['youtube.com', 'channel'],
                'error_indicators': ['404', 'This channel doesn\'t exist']
            },
            {
                'name': 'TikTok',
                'url': 'https://www.tiktok.com/@{}',
                'check_url': 'https://www.tiktok.com/@{}',
                'method': 'GET',
                'success_indicators': ['tiktok.com', 'user'],
                'error_indicators': ['404', 'Couldn\'t find this account']
            },
            {
                'name': 'Reddit',
                'url': 'https://www.reddit.com/user/{}',
                'check_url': 'https://www.reddit.com/user/{}',
                'method': 'GET',
                'success_indicators': ['reddit.com', 'user'],
                'error_indicators': ['404', 'page not found']
            },
            {
                'name': 'Pinterest',
                'url': 'https://www.pinterest.com/{}',
                'check_url': 'https://www.pinterest.com/{}',
                'method': 'GET',
                'success_indicators': ['pinterest.com', 'UserPage'],
                'error_indicators': ['404', 'Sorry, we couldn\'t find that page']
            },
            {
                'name': 'Snapchat',
                'url': 'https://www.snapchat.com/add/{}',
                'check_url': 'https://www.snapchat.com/add/{}',
                'method': 'GET',
                'success_indicators': ['snapchat.com', 'profile'],
                'error_indicators': ['404', 'User not found']
            },
            {
                'name': 'Telegram',
                'url': 'https://t.me/{}',
                'check_url': 'https://t.me/{}',
                'method': 'GET',
                'success_indicators': ['telegram.me', 'tgme_page'],
                'error_indicators': ['404', 'not found']
            },
            {
                'name': 'Steam',
                'url': 'https://steamcommunity.com/id/{}',
                'check_url': 'https://steamcommunity.com/id/{}',
                'method': 'GET',
                'success_indicators': ['steamcommunity.com', 'profile'],
                'error_indicators': ['404', 'not found']
            },
            {
                'name': 'Twitch',
                'url': 'https://www.twitch.tv/{}',
                'check_url': 'https://www.twitch.tv/{}',
                'method': 'GET',
                'success_indicators': ['twitch.tv', 'channel'],
                'error_indicators': ['404', 'channel not found']
            },
            {
                'name': 'Spotify',
                'url': 'https://open.spotify.com/user/{}',
                'check_url': 'https://open.spotify.com/user/{}',
                'method': 'GET',
                'success_indicators': ['spotify.com', 'user'],
                'error_indicators': ['404', 'not found']
            },
            {
                'name': 'Skype',
                'url': 'skype:{}?userinfo',
                'check_url': 'https://secure.skype.com/portal/overview',
                'method': 'SKIP',
                'success_indicators': [],
                'error_indicators': []
            }
        ]
    
    def analyze_username(self, username: str) -> Dict[str, Any]:
        """
        Realiza un análisis completo de un nombre de usuario
        
        Args:
            username: Nombre de usuario a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        results = {
            'username': username,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'username_variants': self._generate_username_variants(username),
            'platform_results': self._check_platforms(username),
            'statistics': self._calculate_statistics(username),
            'availability': self._check_availability(username),
            'patterns': self._analyze_patterns(username),
            'security_analysis': self._analyze_security(username)
        }
        
        self.results = results
        return results
    
    def _generate_username_variants(self, username: str) -> List[str]:
        """Genera variantes del nombre de usuario"""
        variants = [username]
        
        # Variantes comunes
        if '.' in username:
            variants.append(username.replace('.', ''))
            variants.append(username.replace('.', '_'))
            variants.append(username.replace('.', '-'))
        
        if '_' in username:
            variants.append(username.replace('_', ''))
            variants.append(username.replace('_', '.'))
            variants.append(username.replace('_', '-'))
        
        if '-' in username:
            variants.append(username.replace('-', ''))
            variants.append(username.replace('-', '_'))
            variants.append(username.replace('-', '.'))
        
        # Variantes con números
        if any(char.isdigit() for char in username):
            variants.append(re.sub(r'\d+', '', username))
        
        # Variantes de caso
        variants.append(username.lower())
        variants.append(username.upper())
        variants.append(username.title())
        
        # Variantes con sufijos comunes
        common_suffixes = ['_', '1', '2', '123', '_1', '_2', 'official', 'real']
        for suffix in common_suffixes:
            variants.append(username + suffix)
        
        return list(set(variants))
    
    def _check_platforms(self, username: str) -> List[Dict[str, Any]]:
        """Verifica la disponibilidad del username en todas las plataformas"""
        results = []
        
        # Usar ThreadPoolExecutor para verificaciones concurrentes
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            
            for platform in self.platforms:
                if platform['method'] != 'SKIP':
                    future = executor.submit(self._check_single_platform, username, platform)
                    futures[future] = platform
            
            for future in as_completed(futures):
                platform = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'platform': platform['name'],
                        'url': platform['url'].format(username),
                        'exists': False,
                        'status': 'error',
                        'error': str(e)
                    })
        
        return results
    
    def _check_single_platform(self, username: str, platform: Dict[str, str]) -> Dict[str, Any]:
        """Verifica un username en una plataforma específica"""
        url = platform['check_url'].format(username)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            
            # Análisis de la respuesta
            exists = False
            status_code = response.status_code
            content = response.text.lower()
            
            if status_code == 200:
                # Verificar indicadores de éxito
                for indicator in platform['success_indicators']:
                    if indicator.lower() in content:
                        exists = True
                        break
                
                # Verificar indicadores de error
                for indicator in platform['error_indicators']:
                    if indicator.lower() in content:
                        exists = False
                        break
                
                # Si no hay indicadores específicos, asumir que existe
                if not platform['success_indicators'] and not platform['error_indicators']:
                    exists = True
            
            # Extraer información adicional
            additional_info = self._extract_profile_info(content, platform['name'])
            
            return {
                'platform': platform['name'],
                'url': platform['url'].format(username),
                'exists': exists,
                'status': 'found' if exists else 'not_found',
                'status_code': status_code,
                'additional_info': additional_info,
                'last_checked': datetime.now(timezone.utc).isoformat()
            }
            
        except requests.RequestException as e:
            return {
                'platform': platform['name'],
                'url': platform['url'].format(username),
                'exists': False,
                'status': 'error',
                'error': str(e),
                'last_checked': datetime.now(timezone.utc).isoformat()
            }
    
    def _extract_profile_info(self, content: str, platform: str) -> Dict[str, Any]:
        """Extrae información adicional del perfil"""
        info = {}
        
        # Patrones comunes para extraer información
        patterns = {
            'title': [
                r'<title>(.*?)</title>',
                r'"title":"(.*?)"',
                r'og:title" content="(.*?)"'
            ],
            'description': [
                r'<meta name="description" content="(.*?)"',
                r'og:description" content="(.*?)"',
                r'"description":"(.*?)"'
            ],
            'image': [
                r'og:image" content="(.*?)"',
                r'"image":"(.*?)"',
                r'profile.*?src="(.*?)"'
            ]
        }
        
        content_lower = content.lower()
        
        for field, regex_patterns in patterns.items():
            for pattern in regex_patterns:
                match = re.search(pattern, content_lower)
                if match:
                    info[field] = match.group(1).strip()
                    break
        
        # Información específica por plataforma
        if platform.lower() == 'github':
            # Buscar repositorios, seguidores, etc.
            repo_match = re.search(r'(\d+)\s+repositories', content_lower)
            if repo_match:
                info['repositories'] = repo_match.group(1)
        
        elif platform.lower() == 'twitter':
            # Buscar seguidores, tweets, etc.
            followers_match = re.search(r'(\d+)\s+followers', content_lower)
            if followers_match:
                info['followers'] = followers_match.group(1)
        
        return info
    
    def _calculate_statistics(self, username: str) -> Dict[str, Any]:
        """Calcula estadísticas del análisis"""
        if not self.results or 'platform_results' not in self.results:
            return {}
        
        platform_results = self.results.get('platform_results', [])
        
        total_platforms = len(platform_results)
        found_platforms = sum(1 for result in platform_results if result.get('exists', False))
        error_platforms = sum(1 for result in platform_results if result.get('status') == 'error')
        
        return {
            'total_platforms_checked': total_platforms,
            'platforms_found': found_platforms,
            'platforms_not_found': total_platforms - found_platforms - error_platforms,
            'platforms_with_errors': error_platforms,
            'availability_percentage': ((total_platforms - found_platforms) / total_platforms * 100) if total_platforms > 0 else 0,
            'presence_percentage': (found_platforms / total_platforms * 100) if total_platforms > 0 else 0
        }
    
    def _check_availability(self, username: str) -> Dict[str, Any]:
        """Verifica la disponibilidad general del username"""
        if not self.results or 'platform_results' not in self.results:
            return {}
        
        platform_results = self.results.get('platform_results', [])
        
        available_platforms = []
        taken_platforms = []
        
        for result in platform_results:
            if result.get('status') == 'found':
                taken_platforms.append(result['platform'])
            elif result.get('status') == 'not_found':
                available_platforms.append(result['platform'])
        
        return {
            'available_on': available_platforms,
            'taken_on': taken_platforms,
            'availability_score': len(available_platforms) / (len(available_platforms) + len(taken_platforms)) * 100 if (len(available_platforms) + len(taken_platforms)) > 0 else 0
        }
    
    def _analyze_patterns(self, username: str) -> Dict[str, Any]:
        """Analiza patrones en el nombre de usuario"""
        patterns = {
            'length': len(username),
            'has_numbers': bool(re.search(r'\d', username)),
            'has_letters': bool(re.search(r'[a-zA-Z]', username)),
            'has_special_chars': bool(re.search(r'[._-]', username)),
            'is_alphanumeric': username.isalnum(),
            'starts_with_number': username[0].isdigit() if username else False,
            'ends_with_number': username[-1].isdigit() if username else False,
            'contains_birth_year': bool(re.search(r'19\d{2}|20\d{2}', username)),
            'contains_common_words': self._check_common_words(username),
            'pattern_type': self._classify_pattern(username)
        }
        
        return patterns
    
    def _check_common_words(self, username: str) -> List[str]:
        """Verifica si contiene palabras comunes"""
        common_words = [
            'admin', 'user', 'test', 'demo', 'official', 'real', 'original',
            'pro', 'master', 'king', 'queen', 'boss', 'lord', 'lady',
            'boy', 'girl', 'man', 'woman', 'guy', 'gal',
            'love', 'heart', 'soul', 'angel', 'devil', 'dark', 'light',
            'cool', 'hot', 'fire', 'ice', 'rock', 'star', 'moon', 'sun'
        ]
        
        found_words = []
        username_lower = username.lower()
        
        for word in common_words:
            if word in username_lower:
                found_words.append(word)
        
        return found_words
    
    def _classify_pattern(self, username: str) -> str:
        """Clasifica el tipo de patrón del username"""
        if re.match(r'^[a-zA-Z]+\d+$', username):
            return 'name_with_numbers'
        elif re.match(r'^[a-zA-Z]+\.[a-zA-Z]+$', username):
            return 'firstname_lastname'
        elif re.match(r'^[a-zA-Z]+_[a-zA-Z]+$', username):
            return 'firstname_lastname_underscore'
        elif re.match(r'^[a-zA-Z]+$', username):
            return 'letters_only'
        elif re.match(r'^\d+$', username):
            return 'numbers_only'
        elif re.match(r'^[a-zA-Z]+\d{4}$', username):
            return 'name_with_year'
        elif '_' in username:
            return 'underscore_separated'
        elif '.' in username:
            return 'dot_separated'
        elif '-' in username:
            return 'hyphen_separated'
        else:
            return 'mixed_pattern'
    
    def _analyze_security(self, username: str) -> Dict[str, Any]:
        """Analiza aspectos de seguridad del username"""
        security_issues = []
        recommendations = []
        
        # Verificar longitud
        if len(username) < 4:
            security_issues.append('Username too short')
            recommendations.append('Use at least 4 characters')
        
        # Verificar información personal
        if re.search(r'19\d{2}|20\d{2}', username):
            security_issues.append('Contains potential birth year')
            recommendations.append('Avoid using birth years in usernames')
        
        # Verificar palabras predictibles
        predictable_words = ['admin', 'user', 'test', '123', 'password']
        for word in predictable_words:
            if word in username.lower():
                security_issues.append(f'Contains predictable word: {word}')
                recommendations.append('Avoid using common/predictable words')
        
        # Verificar patrones secuenciales
        if re.search(r'123|abc|qwe', username.lower()):
            security_issues.append('Contains sequential characters')
            recommendations.append('Avoid sequential characters')
        
        # Calcular puntuación de seguridad
        base_score = 100
        score_deduction = len(security_issues) * 15
        security_score = max(0, base_score - score_deduction)
        
        return {
            'security_score': security_score,
            'security_issues': security_issues,
            'recommendations': recommendations,
            'is_secure': security_score >= 70
        }
    
    def search_variations(self, username: str) -> Dict[str, Any]:
        """Busca variaciones del username en las plataformas"""
        variations = self._generate_username_variants(username)
        results = {}
        
        for variation in variations[:5]:  # Limitar a 5 variaciones para evitar rate limiting
            if variation != username:
                results[variation] = self._check_platforms(variation)
                time.sleep(1)  # Pausa para evitar rate limiting
        
        return results
    
    def export_results(self, format: str = 'json') -> str:
        """Exporta los resultados en diferentes formatos"""
        if not self.results:
            return "No results to export"
        
        if format.lower() == 'json':
            return json.dumps(self.results, indent=2)
        
        elif format.lower() == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Headers
            writer.writerow(['Platform', 'URL', 'Exists', 'Status', 'Last Checked'])
            
            # Data
            for result in self.results.get('platform_results', []):
                writer.writerow([
                    result.get('platform', ''),
                    result.get('url', ''),
                    result.get('exists', False),
                    result.get('status', ''),
                    result.get('last_checked', '')
                ])
            
            return output.getvalue()
        
        elif format.lower() == 'html':
            html = f"""
            <html>
            <head><title>Username Analysis Report</title></head>
            <body>
            <h1>Username Analysis: {self.results.get('username', 'Unknown')}</h1>
            <h2>Statistics</h2>
            <ul>
            """
            
            stats = self.results.get('statistics', {})
            for key, value in stats.items():
                html += f"<li>{key}: {value}</li>"
            
            html += """
            </ul>
            <h2>Platform Results</h2>
            <table border="1">
            <tr><th>Platform</th><th>Status</th><th>URL</th></tr>
            """
            
            for result in self.results.get('platform_results', []):
                status = "✓ Found" if result.get('exists') else "✗ Not Found"
                html += f"""
                <tr>
                    <td>{result.get('platform', '')}</td>
                    <td>{status}</td>
                    <td><a href="{result.get('url', '')}">{result.get('url', '')}</a></td>
                </tr>
                """
            
            html += """
            </table>
            </body>
            </html>
            """
            
            return html
        
        else:
            return "Unsupported format"
    
    def generate_summary(self) -> Dict[str, Any]:
        """Genera un resumen del análisis"""
        if not self.results:
            return {'error': 'No analysis results available'}
        
        stats = self.results.get('statistics', {})
        availability = self.results.get('availability', {})
        patterns = self.results.get('patterns', {})
        security = self.results.get('security_analysis', {})
        
        summary = {
            'username': self.results.get('username'),
            'analysis_date': self.results.get('timestamp'),
            'availability': {
                'total_platforms': stats.get('total_platforms_checked', 0),
                'found_on': stats.get('platforms_found', 0),
                'available_on': len(availability.get('available_on', [])),
                'presence_score': round(stats.get('presence_percentage', 0), 2)
            },
            'patterns': {
                'length': patterns.get('length', 0),
                'type': patterns.get('pattern_type', 'unknown'),
                'has_numbers': patterns.get('has_numbers', False),
                'has_special_chars': patterns.get('has_special_chars', False)
            },
            'security': {
                'score': security.get('security_score', 0),
                'is_secure': security.get('is_secure', False),
                'issues_count': len(security.get('security_issues', []))
            },
            'top_platforms': [
                result['platform'] for result in self.results.get('platform_results', [])
                if result.get('exists', False)
            ][:5]
        }
        
        return summary