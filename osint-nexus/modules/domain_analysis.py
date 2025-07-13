"""
Módulo de Análisis de Dominio e Infraestructura IP
Integra múltiples herramientas para análisis completo de dominios
"""

import socket
import whois
import dns.resolver
import ipwhois
import validators
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import re

from utils.api_manager import APIManager
from config.api_keys import APIConfig

logger = logging.getLogger(__name__)

class DomainAnalyzer:
    """Analizador completo de dominios e infraestructura"""
    
    def __init__(self):
        self.api_manager = APIManager()
        self.results = {}
        
    async def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """
        Análisis completo de un dominio
        
        Args:
            domain: Dominio a analizar (ej: ejemplo.com)
            
        Returns:
            Diccionario con todos los resultados del análisis
        """
        # Validar dominio
        if not validators.domain(domain):
            return {'error': 'Dominio inválido'}
            
        logger.info(f"Iniciando análisis de dominio: {domain}")
        
        # Ejecutar análisis en paralelo
        tasks = [
            self._get_whois_info(domain),
            self._get_dns_records(domain),
            self._get_subdomains(domain),
            self._get_ip_info(domain),
            self._shodan_analysis(domain),
            self._check_web_technologies(domain),
            self._get_ssl_info(domain)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Consolidar resultados
        analysis_results = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'whois': results[0] if not isinstance(results[0], Exception) else None,
            'dns_records': results[1] if not isinstance(results[1], Exception) else None,
            'subdomains': results[2] if not isinstance(results[2], Exception) else [],
            'ip_info': results[3] if not isinstance(results[3], Exception) else None,
            'shodan': results[4] if not isinstance(results[4], Exception) else None,
            'technologies': results[5] if not isinstance(results[5], Exception) else None,
            'ssl_info': results[6] if not isinstance(results[6], Exception) else None
        }
        
        # Extraer emails encontrados
        analysis_results['emails'] = self._extract_emails(analysis_results)
        
        return analysis_results
    
    async def _get_whois_info(self, domain: str) -> Optional[Dict]:
        """Obtener información WHOIS del dominio"""
        try:
            w = whois.whois(domain)
            
            # Convertir a diccionario serializable
            whois_data = {
                'registrar': getattr(w, 'registrar', None),
                'creation_date': str(getattr(w, 'creation_date', None)),
                'expiration_date': str(getattr(w, 'expiration_date', None)),
                'name_servers': getattr(w, 'name_servers', []),
                'status': getattr(w, 'status', None),
                'emails': getattr(w, 'emails', []),
                'org': getattr(w, 'org', None),
                'country': getattr(w, 'country', None)
            }
            
            return whois_data
            
        except Exception as e:
            logger.error(f"Error en WHOIS: {e}")
            return None
    
    async def _get_dns_records(self, domain: str) -> Dict[str, List[str]]:
        """Obtener registros DNS del dominio"""
        records = {
            'A': [],
            'AAAA': [],
            'MX': [],
            'NS': [],
            'TXT': [],
            'CNAME': [],
            'SOA': []
        }
        
        for record_type in records.keys():
            try:
                answers = dns.resolver.resolve(domain, record_type)
                for rdata in answers:
                    records[record_type].append(str(rdata))
            except dns.resolver.NXDOMAIN:
                logger.warning(f"Dominio {domain} no encontrado")
                break
            except dns.resolver.NoAnswer:
                pass
            except Exception as e:
                logger.debug(f"Error obteniendo {record_type} para {domain}: {e}")
                
        return records
    
    async def _get_subdomains(self, domain: str) -> List[str]:
        """Buscar subdominios usando múltiples técnicas"""
        subdomains = set()
        
        # Lista común de subdominios para probar
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'vpn', 'api', 'dev', 'staging', 'test', 'portal', 'secure', 'app',
            'mobile', 'static', 'cdn', 'assets', 'img', 'images', 'css', 'js'
        ]
        
        # Probar subdominios comunes
        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            try:
                socket.gethostbyname(subdomain)
                subdomains.add(subdomain)
            except socket.gaierror:
                pass
        
        # Usar Certificate Transparency logs si está disponible
        try:
            ct_subdomains = await self._get_ct_subdomains(domain)
            subdomains.update(ct_subdomains)
        except Exception as e:
            logger.debug(f"Error obteniendo subdominios de CT: {e}")
        
        return list(subdomains)
    
    async def _get_ct_subdomains(self, domain: str) -> List[str]:
        """Obtener subdominios desde Certificate Transparency logs"""
        subdomains = set()
        
        try:
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for entry in data:
                            name_value = entry.get('name_value', '')
                            # Extraer todos los dominios del certificado
                            names = name_value.replace('*.', '').split('\n')
                            for name in names:
                                if name and domain in name:
                                    subdomains.add(name.strip())
                                    
        except Exception as e:
            logger.debug(f"Error en crt.sh: {e}")
            
        return list(subdomains)
    
    async def _get_ip_info(self, domain: str) -> Optional[Dict]:
        """Obtener información de la IP del dominio"""
        try:
            # Resolver IP
            ip = socket.gethostbyname(domain)
            
            # Obtener información de la IP
            obj = ipwhois.IPWhois(ip)
            results = obj.lookup_rdap()
            
            ip_info = {
                'ip': ip,
                'asn': results.get('asn', None),
                'asn_description': results.get('asn_description', None),
                'asn_country': results.get('asn_country_code', None),
                'network': {
                    'cidr': results.get('network', {}).get('cidr', None),
                    'name': results.get('network', {}).get('name', None),
                    'country': results.get('network', {}).get('country', None)
                }
            }
            
            return ip_info
            
        except Exception as e:
            logger.error(f"Error obteniendo info IP: {e}")
            return None
    
    async def _shodan_analysis(self, domain: str) -> Optional[Dict]:
        """Análisis usando Shodan"""
        if not APIConfig.is_api_configured('shodan'):
            return None
            
        try:
            # Obtener IP del dominio
            ip = socket.gethostbyname(domain)
            
            # Buscar en Shodan
            result = self.api_manager.shodan_search(f"ip:{ip}")
            
            if result and 'matches' in result:
                # Procesar resultados de Shodan
                services = []
                vulnerabilities = []
                
                for match in result['matches']:
                    service = {
                        'port': match.get('port'),
                        'service': match.get('product', 'Unknown'),
                        'version': match.get('version', ''),
                        'transport': match.get('transport', '')
                    }
                    services.append(service)
                    
                    # Extraer vulnerabilidades si existen
                    if 'vulns' in match:
                        vulnerabilities.extend(match['vulns'])
                
                return {
                    'ip': ip,
                    'services': services,
                    'vulnerabilities': list(set(vulnerabilities)),
                    'total_services': len(services)
                }
                
        except Exception as e:
            logger.error(f"Error en análisis Shodan: {e}")
            
        return None
    
    async def _check_web_technologies(self, domain: str) -> Optional[Dict]:
        """Detectar tecnologías web utilizadas"""
        try:
            url = f"http://{domain}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10, allow_redirects=True) as response:
                    if response.status == 200:
                        html = await response.text()
                        headers = dict(response.headers)
                        
                        # Detectar tecnologías
                        technologies = {
                            'server': headers.get('Server', 'Unknown'),
                            'powered_by': headers.get('X-Powered-By', None),
                            'cms': self._detect_cms(html, headers),
                            'frameworks': self._detect_frameworks(html),
                            'analytics': self._detect_analytics(html)
                        }
                        
                        return technologies
                        
        except Exception as e:
            logger.debug(f"Error detectando tecnologías: {e}")
            
        return None
    
    def _detect_cms(self, html: str, headers: Dict) -> Optional[str]:
        """Detectar CMS utilizado"""
        cms_signatures = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Joomla': ['joomla', 'com_content', 'Joomla!'],
            'Drupal': ['drupal', 'sites/all', 'node/add'],
            'Magento': ['magento', 'Mage.Cookies', 'varien'],
            'Shopify': ['shopify', 'cdn.shopify'],
            'Wix': ['wix.com', 'X-Wix-'],
            'SquareSpace': ['squarespace', 'sqsp']
        }
        
        for cms, signatures in cms_signatures.items():
            for signature in signatures:
                if signature.lower() in html.lower() or signature in str(headers):
                    return cms
                    
        return None
    
    def _detect_frameworks(self, html: str) -> List[str]:
        """Detectar frameworks JavaScript"""
        frameworks = []
        
        framework_signatures = {
            'React': ['react', 'react.js', 'ReactDOM'],
            'Angular': ['ng-app', 'angular', 'ng-'],
            'Vue.js': ['vue', 'v-for', 'v-if'],
            'jQuery': ['jquery', '$(', 'jQuery('],
            'Bootstrap': ['bootstrap', 'btn btn-'],
            'Express': ['X-Powered-By: Express']
        }
        
        for framework, signatures in framework_signatures.items():
            for signature in signatures:
                if signature in html:
                    frameworks.append(framework)
                    break
                    
        return frameworks
    
    def _detect_analytics(self, html: str) -> List[str]:
        """Detectar herramientas de analytics"""
        analytics = []
        
        analytics_patterns = {
            'Google Analytics': [r'google-analytics\.com', r'ga\(', r'gtag\('],
            'Google Tag Manager': [r'googletagmanager\.com'],
            'Facebook Pixel': [r'facebook\.com/tr', r'fbq\('],
            'Hotjar': [r'hotjar\.com'],
            'Matomo': [r'matomo', r'piwik']
        }
        
        for tool, patterns in analytics_patterns.items():
            for pattern in patterns:
                if re.search(pattern, html, re.IGNORECASE):
                    analytics.append(tool)
                    break
                    
        return analytics
    
    async def _get_ssl_info(self, domain: str) -> Optional[Dict]:
        """Obtener información del certificado SSL"""
        try:
            import ssl
            import certifi
            
            context = ssl.create_default_context(cafile=certifi.where())
            
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        ssl_info = {
                            'issuer': cert.get('issuer', ''),
                            'subject': cert.get('subject', ''),
                            'version': cert.get('version', ''),
                            'serial_number': cert.get('serialNumber', ''),
                            'not_before': cert.get('notBefore', ''),
                            'not_after': cert.get('notAfter', ''),
                            'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown'),
                            'san': cert.get('subjectAltName', [])
                        }
                        
                        return ssl_info
                    else:
                        return None
                    
        except Exception as e:
            logger.debug(f"Error obteniendo info SSL: {e}")
            
        return None
    
    def _extract_emails(self, results: Dict) -> List[str]:
        """Extraer todos los emails encontrados en los resultados"""
        emails = set()
        
        # Desde WHOIS
        if results.get('whois') and results['whois'].get('emails'):
            emails.update(results['whois']['emails'])
        
        # Patrón para buscar emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Buscar en todos los resultados
        def find_emails(obj):
            if isinstance(obj, str):
                found = re.findall(email_pattern, obj)
                emails.update(found)
            elif isinstance(obj, dict):
                for value in obj.values():
                    find_emails(value)
            elif isinstance(obj, list):
                for item in obj:
                    find_emails(item)
        
        find_emails(results)
        
        return list(emails)