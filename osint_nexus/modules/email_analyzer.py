"""
Módulo de investigación de correo electrónico
"""

import requests
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from urllib.parse import quote

class EmailAnalyzer:
    """Analizador de direcciones de correo electrónico"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Inicializa el analizador de email
        
        Args:
            api_keys: Diccionario con claves de API
        """
        self.api_keys = api_keys or {}
        self.results = {}
    
    def analyze_email(self, email: str) -> Dict[str, Any]:
        """
        Realiza un análisis completo de una dirección de email
        
        Args:
            email: Dirección de email a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        results = {
            'email': email,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'basic_info': self._get_basic_info(email),
            'domain_info': self._analyze_domain(email),
            'validation': self._validate_email(email),
            'breaches': self._check_breaches(email),
            'social_profiles': self._find_social_profiles(email),
            'hunter_info': self._get_hunter_info(email),
            'disposable_check': self._check_disposable_email(email),
            'reputation': self._check_reputation(email)
        }
        
        self.results = results
        return results
    
    def _get_basic_info(self, email: str) -> Dict[str, Any]:
        """Extrae información básica del email"""
        try:
            local_part, domain = email.split('@')
            
            return {
                'local_part': local_part,
                'domain': domain,
                'length': len(email),
                'has_numbers': bool(re.search(r'\d', local_part)),
                'has_dots': '.' in local_part,
                'has_plus': '+' in local_part,
                'has_underscore': '_' in local_part,
                'has_hyphen': '-' in local_part,
                'possible_patterns': self._detect_email_patterns(local_part)
            }
        except ValueError:
            return {'error': 'Invalid email format'}
    
    def _detect_email_patterns(self, local_part: str) -> List[str]:
        """Detecta patrones comunes en la parte local del email"""
        patterns = []
        
        # Patrones comunes
        if re.match(r'^[a-zA-Z]+\.[a-zA-Z]+$', local_part):
            patterns.append('firstname.lastname')
        elif re.match(r'^[a-zA-Z]+[a-zA-Z]+\d+$', local_part):
            patterns.append('name_with_numbers')
        elif re.match(r'^[a-zA-Z]+_[a-zA-Z]+$', local_part):
            patterns.append('firstname_lastname')
        elif re.match(r'^[a-zA-Z]+\d{2,4}$', local_part):
            patterns.append('name_birth_year')
        elif '+' in local_part:
            patterns.append('gmail_plus_trick')
        elif re.match(r'^[a-zA-Z]+[a-zA-Z]+$', local_part):
            patterns.append('concatenated_name')
        
        return patterns
    
    def _analyze_domain(self, email: str) -> Dict[str, Any]:
        """Analiza el dominio del email"""
        try:
            domain = email.split('@')[1]
            
            # Verificar si es un dominio popular
            popular_domains = [
                'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
                'aol.com', 'icloud.com', 'protonmail.com', 'mail.com'
            ]
            
            is_popular = domain.lower() in popular_domains
            
            # Información básica del dominio
            domain_info = {
                'domain': domain,
                'is_popular_provider': is_popular,
                'provider_type': self._get_provider_type(domain),
                'mx_records': self._get_mx_records(domain),
                'domain_age': self._estimate_domain_age(domain)
            }
            
            return domain_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_provider_type(self, domain: str) -> str:
        """Determina el tipo de proveedor de email"""
        domain_lower = domain.lower()
        
        # Proveedores gratuitos
        free_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'mail.com', 'gmx.com'
        ]
        
        # Proveedores empresariales
        business_providers = [
            'office365.com', 'google.com', 'microsoft.com'
        ]
        
        # Proveedores de privacidad
        privacy_providers = [
            'protonmail.com', 'tutanota.com', 'guerrillamail.com'
        ]
        
        if domain_lower in free_providers:
            return 'free'
        elif domain_lower in business_providers:
            return 'business'
        elif domain_lower in privacy_providers:
            return 'privacy'
        else:
            return 'custom'
    
    def _get_mx_records(self, domain: str) -> List[str]:
        """Obtiene registros MX del dominio"""
        try:
            import dns.resolver
            
            mx_records = []
            answers = dns.resolver.resolve(domain, 'MX')
            
            for rdata in answers:
                mx_records.append(str(rdata))
            
            return mx_records
            
        except Exception:
            return []
    
    def _estimate_domain_age(self, domain: str) -> Dict[str, Any]:
        """Estima la edad del dominio"""
        try:
            import whois
            
            w = whois.whois(domain)
            
            if w.creation_date:
                creation_date = w.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                
                age_days = (datetime.now() - creation_date).days
                
                return {
                    'creation_date': str(creation_date),
                    'age_days': age_days,
                    'age_years': round(age_days / 365.25, 1)
                }
            
            return {'error': 'Creation date not available'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _validate_email(self, email: str) -> Dict[str, Any]:
        """Valida la dirección de email"""
        validation_results = {
            'format_valid': self._validate_format(email),
            'domain_exists': self._check_domain_exists(email),
            'deliverable': None,  # Requiere API externa
            'role_account': self._is_role_account(email)
        }
        
        return validation_results
    
    def _validate_format(self, email: str) -> bool:
        """Valida el formato del email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _check_domain_exists(self, email: str) -> bool:
        """Verifica si el dominio existe"""
        try:
            import socket
            domain = email.split('@')[1]
            socket.gethostbyname(domain)
            return True
        except socket.gaierror:
            return False
    
    def _is_role_account(self, email: str) -> bool:
        """Verifica si es una cuenta de rol"""
        role_prefixes = [
            'admin', 'administrator', 'support', 'help', 'info',
            'contact', 'sales', 'marketing', 'noreply', 'no-reply',
            'webmaster', 'postmaster', 'abuse', 'security'
        ]
        
        local_part = email.split('@')[0].lower()
        return any(local_part.startswith(prefix) for prefix in role_prefixes)
    
    def _check_breaches(self, email: str) -> Dict[str, Any]:
        """Verifica brechas de datos usando Have I Been Pwned"""
        try:
            if not self.api_keys.get('HIBP_API_KEY'):
                return {'error': 'HIBP API key not provided'}
            
            headers = {
                'hibp-api-key': self.api_keys['HIBP_API_KEY'],
                'User-Agent': 'OSINT-Nexus'
            }
            
            # Verificar brechas
            breach_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote(email)}"
            response = requests.get(breach_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                
                breach_summary = {
                    'found_in_breaches': True,
                    'breach_count': len(breaches),
                    'breaches': []
                }
                
                for breach in breaches:
                    breach_summary['breaches'].append({
                        'name': breach.get('Name'),
                        'domain': breach.get('Domain'),
                        'breach_date': breach.get('BreachDate'),
                        'pwn_count': breach.get('PwnCount'),
                        'description': breach.get('Description'),
                        'compromised_data': breach.get('DataClasses', [])
                    })
                
                return breach_summary
                
            elif response.status_code == 404:
                return {
                    'found_in_breaches': False,
                    'breach_count': 0,
                    'message': 'No breaches found'
                }
            else:
                return {'error': f'HIBP API error: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _find_social_profiles(self, email: str) -> Dict[str, Any]:
        """Busca perfiles sociales asociados al email"""
        # Esta es una implementación básica que busca en patrones comunes
        # En producción, se integraría con APIs especializadas
        
        profiles = {
            'potential_usernames': self._generate_potential_usernames(email),
            'gravatar': self._check_gravatar(email),
            'google_profile': self._check_google_profile(email),
            'social_search_suggestions': self._get_social_search_suggestions(email)
        }
        
        return profiles
    
    def _generate_potential_usernames(self, email: str) -> List[str]:
        """Genera posibles nombres de usuario basados en el email"""
        local_part = email.split('@')[0]
        
        usernames = [local_part]
        
        # Variaciones comunes
        if '.' in local_part:
            usernames.append(local_part.replace('.', ''))
            usernames.append(local_part.replace('.', '_'))
        
        if '_' in local_part:
            usernames.append(local_part.replace('_', ''))
            usernames.append(local_part.replace('_', '.'))
        
        if any(char.isdigit() for char in local_part):
            usernames.append(re.sub(r'\d+', '', local_part))
        
        return list(set(usernames))
    
    def _check_gravatar(self, email: str) -> Dict[str, Any]:
        """Verifica si el email tiene un perfil de Gravatar"""
        try:
            import hashlib
            
            # Generar hash MD5 del email
            email_hash = hashlib.md5(email.lower().encode()).hexdigest()
            
            # Verificar si existe el perfil
            gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
            response = requests.head(gravatar_url, timeout=10)
            
            if response.status_code == 200:
                return {
                    'has_gravatar': True,
                    'profile_url': f"https://www.gravatar.com/{email_hash}",
                    'avatar_url': f"https://www.gravatar.com/avatar/{email_hash}"
                }
            else:
                return {'has_gravatar': False}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _check_google_profile(self, email: str) -> Dict[str, Any]:
        """Verifica información pública de Google"""
        try:
            # Buscar en Google usando el email
            search_url = f"https://www.google.com/search?q=\"{email}\""
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return {
                    'google_indexed': 'No results found' not in response.text,
                    'search_url': search_url
                }
            else:
                return {'error': 'Google search failed'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _get_social_search_suggestions(self, email: str) -> List[str]:
        """Genera sugerencias de búsqueda en redes sociales"""
        local_part = email.split('@')[0]
        
        suggestions = [
            f"Search '{local_part}' on Facebook",
            f"Search '{local_part}' on Twitter",
            f"Search '{local_part}' on LinkedIn",
            f"Search '{local_part}' on Instagram",
            f"Search '{email}' on Google",
            f"Search '{email}' on social media platforms"
        ]
        
        return suggestions
    
    def _get_hunter_info(self, email: str) -> Dict[str, Any]:
        """Obtiene información usando Hunter.io"""
        try:
            if not self.api_keys.get('HUNTER_API_KEY'):
                return {'error': 'Hunter.io API key not provided'}
            
            api_key = self.api_keys['HUNTER_API_KEY']
            
            # Verificar email
            verify_url = f"https://api.hunter.io/v2/email-verifier"
            params = {
                'email': email,
                'api_key': api_key
            }
            
            response = requests.get(verify_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data:
                    verification_data = data['data']
                    
                    return {
                        'email': verification_data.get('email'),
                        'result': verification_data.get('result'),
                        'score': verification_data.get('score'),
                        'regexp': verification_data.get('regexp'),
                        'gibberish': verification_data.get('gibberish'),
                        'disposable': verification_data.get('disposable'),
                        'webmail': verification_data.get('webmail'),
                        'mx_records': verification_data.get('mx_records'),
                        'smtp_server': verification_data.get('smtp_server'),
                        'smtp_check': verification_data.get('smtp_check'),
                        'accept_all': verification_data.get('accept_all'),
                        'block': verification_data.get('block')
                    }
                else:
                    return {'error': 'No verification data available'}
            else:
                return {'error': f'Hunter.io API error: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _check_disposable_email(self, email: str) -> Dict[str, Any]:
        """Verifica si es un email desechable"""
        try:
            domain = email.split('@')[1].lower()
            
            # Lista de dominios desechables conocidos
            disposable_domains = [
                '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
                'tempmail.org', 'yopmail.com', 'throwaway.email',
                'temp-mail.org', 'getnada.com', 'maildrop.cc'
            ]
            
            is_disposable = domain in disposable_domains
            
            # Verificar también con servicio externo si está disponible
            try:
                response = requests.get(
                    f"https://open.kickbox.com/v1/disposable/{domain}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    is_disposable = data.get('disposable', is_disposable)
                    
            except Exception:
                pass
            
            return {
                'is_disposable': is_disposable,
                'domain': domain,
                'confidence': 'high' if domain in disposable_domains else 'medium'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_reputation(self, email: str) -> Dict[str, Any]:
        """Verifica la reputación del email"""
        try:
            domain = email.split('@')[1]
            
            reputation = {
                'spam_score': self._calculate_spam_score(email),
                'domain_reputation': self._check_domain_reputation(domain),
                'blacklist_check': self._check_blacklists(domain),
                'trust_score': 0
            }
            
            # Calcular puntuación de confianza
            spam_score = reputation['spam_score']
            domain_rep = reputation['domain_reputation']
            
            trust_score = 100 - spam_score
            if domain_rep.get('is_trusted', False):
                trust_score += 10
            
            reputation['trust_score'] = max(0, min(100, trust_score))
            
            return reputation
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_spam_score(self, email: str) -> int:
        """Calcula una puntuación de spam basada en características"""
        score = 0
        local_part = email.split('@')[0]
        
        # Factores que aumentan la puntuación de spam
        if len(local_part) < 3:
            score += 20
        
        if len(local_part) > 20:
            score += 10
        
        if re.search(r'\d{4,}', local_part):  # Muchos números
            score += 15
        
        if local_part.count('.') > 2:
            score += 10
        
        if any(word in local_part.lower() for word in ['noreply', 'no-reply', 'donotreply']):
            score += 5
        
        return min(100, score)
    
    def _check_domain_reputation(self, domain: str) -> Dict[str, Any]:
        """Verifica la reputación del dominio"""
        # Dominios confiables
        trusted_domains = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
            'apple.com', 'microsoft.com', 'google.com'
        ]
        
        return {
            'is_trusted': domain.lower() in trusted_domains,
            'domain_age': self._estimate_domain_age(domain),
            'mx_valid': len(self._get_mx_records(domain)) > 0
        }
    
    def _check_blacklists(self, domain: str) -> Dict[str, Any]:
        """Verifica si el dominio está en listas negras"""
        # Implementación básica - en producción se integraría con APIs de blacklists
        
        suspicious_patterns = [
            r'^\d+\w+\d+$',  # Muchos números
            r'^[a-z]{1,3}\d+[a-z]{1,3}$',  # Patrón sospechoso
            r'temp|fake|spam|trash'  # Palabras sospechosas
        ]
        
        is_suspicious = any(re.search(pattern, domain.lower()) for pattern in suspicious_patterns)
        
        return {
            'is_blacklisted': is_suspicious,
            'blacklist_sources': ['pattern_detection'] if is_suspicious else [],
            'confidence': 'medium' if is_suspicious else 'low'
        }
    
    def generate_summary(self) -> Dict[str, Any]:
        """Genera un resumen del análisis"""
        if not self.results:
            return {'error': 'No analysis results available'}
        
        summary = {
            'email': self.results.get('email'),
            'validation': {
                'format_valid': self.results.get('validation', {}).get('format_valid', False),
                'domain_exists': self.results.get('validation', {}).get('domain_exists', False),
                'deliverable': self.results.get('hunter_info', {}).get('result', 'Unknown')
            },
            'security': {
                'found_in_breaches': self.results.get('breaches', {}).get('found_in_breaches', False),
                'breach_count': self.results.get('breaches', {}).get('breach_count', 0),
                'is_disposable': self.results.get('disposable_check', {}).get('is_disposable', False),
                'trust_score': self.results.get('reputation', {}).get('trust_score', 0)
            },
            'provider': {
                'domain': self.results.get('basic_info', {}).get('domain'),
                'provider_type': self.results.get('domain_info', {}).get('provider_type'),
                'is_popular': self.results.get('domain_info', {}).get('is_popular_provider', False)
            },
            'social': {
                'has_gravatar': self.results.get('social_profiles', {}).get('gravatar', {}).get('has_gravatar', False),
                'potential_usernames': self.results.get('social_profiles', {}).get('potential_usernames', [])
            }
        }
        
        return summary