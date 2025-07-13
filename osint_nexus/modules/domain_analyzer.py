"""
Módulo de análisis de dominio e infraestructura IP
"""

import socket
import ssl
import whois
import dns.resolver
import requests
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from urllib.parse import urlparse
import subprocess
import re

class DomainAnalyzer:
    """Analizador de dominios e infraestructura IP"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Inicializa el analizador de dominios
        
        Args:
            api_keys: Diccionario con claves de API
        """
        self.api_keys = api_keys or {}
        self.results = {}
    
    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """
        Realiza un análisis completo de un dominio
        
        Args:
            domain: Dominio a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        results = {
            'domain': domain,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'basic_info': self._get_basic_info(domain),
            'whois_info': self._get_whois_info(domain),
            'dns_records': self._get_dns_records(domain),
            'subdomains': self._find_subdomains(domain),
            'ssl_info': self._get_ssl_info(domain),
            'technology_stack': self._detect_technology(domain),
            'security_headers': self._check_security_headers(domain),
            'ports_scan': self._basic_port_scan(domain),
            'geolocation': self._get_geolocation(domain)
        }
        
        # Análisis adicional con APIs externas si están disponibles
        if self.api_keys.get('SHODAN_API_KEY'):
            results['shodan_info'] = self._get_shodan_info(domain)
        
        if self.api_keys.get('VIRUSTOTAL_API_KEY'):
            results['virustotal_info'] = self._get_virustotal_info(domain)
        
        if self.api_keys.get('URLSCAN_API_KEY'):
            results['urlscan_info'] = self._get_urlscan_info(domain)
        
        self.results = results
        return results
    
    def _get_basic_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información básica del dominio"""
        try:
            ip_address = socket.gethostbyname(domain)
            return {
                'ip_address': ip_address,
                'is_active': True,
                'resolved_at': datetime.now(timezone.utc).isoformat()
            }
        except socket.gaierror:
            return {
                'ip_address': None,
                'is_active': False,
                'error': 'Domain not found'
            }
    
    def _get_whois_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información WHOIS del dominio"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'updated_date': str(w.updated_date) if w.updated_date else None,
                'name_servers': w.name_servers if w.name_servers else [],
                'status': w.status if w.status else [],
                'emails': w.emails if w.emails else [],
                'registrant_country': w.country if hasattr(w, 'country') else None,
                'registrant_org': w.org if hasattr(w, 'org') else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_dns_records(self, domain: str) -> Dict[str, List[str]]:
        """Obtiene registros DNS del dominio"""
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
                records[record_type] = []
        
        return records
    
    def _find_subdomains(self, domain: str) -> List[str]:
        """Busca subdominios comunes"""
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test', 'staging',
            'api', 'app', 'shop', 'support', 'forum', 'news', 'portal'
        ]
        
        found_subdomains = []
        
        for subdomain in common_subdomains:
            full_domain = f"{subdomain}.{domain}"
            try:
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
            except socket.gaierror:
                pass
        
        return found_subdomains
    
    def _get_ssl_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información del certificado SSL"""
        try:
            context = ssl.create_default_context()
            
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'serial_number': cert['serialNumber'],
                        'version': cert['version'],
                        'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown'),
                        'san': cert.get('subjectAltName', [])
                    }
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_technology(self, domain: str) -> Dict[str, Any]:
        """Detecta tecnologías utilizadas en el sitio web"""
        try:
            url = f"https://{domain}"
            response = requests.get(url, timeout=10, verify=False)
            
            headers = response.headers
            content = response.text
            
            technologies = {
                'server': headers.get('Server', 'Unknown'),
                'powered_by': headers.get('X-Powered-By', 'Unknown'),
                'framework': self._detect_framework(content, headers),
                'cms': self._detect_cms(content, headers),
                'javascript_libraries': self._detect_js_libraries(content),
                'status_code': response.status_code,
                'content_type': headers.get('Content-Type', 'Unknown')
            }
            
            return technologies
            
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_framework(self, content: str, headers: Dict[str, str]) -> str:
        """Detecta el framework web utilizado"""
        frameworks = {
            'django': ['csrfmiddlewaretoken', 'django'],
            'flask': ['flask', 'werkzeug'],
            'rails': ['ruby on rails', 'rails'],
            'laravel': ['laravel', 'laravel_session'],
            'spring': ['spring', 'jsessionid'],
            'asp.net': ['asp.net', 'aspnet'],
            'express': ['express', 'x-powered-by: express']
        }
        
        content_lower = content.lower()
        headers_str = str(headers).lower()
        
        for framework, indicators in frameworks.items():
            for indicator in indicators:
                if indicator in content_lower or indicator in headers_str:
                    return framework
        
        return 'Unknown'
    
    def _detect_cms(self, content: str, headers: Dict[str, str]) -> str:
        """Detecta el CMS utilizado"""
        cms_patterns = {
            'wordpress': ['/wp-content/', '/wp-includes/', 'wp-json'],
            'drupal': ['/sites/default/', 'drupal', '/modules/'],
            'joomla': ['/media/jui/', '/templates/', 'joomla'],
            'magento': ['/skin/frontend/', 'magento', '/js/mage/'],
            'shopify': ['shopify', 'cdn.shopify.com']
        }
        
        content_lower = content.lower()
        
        for cms, patterns in cms_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    return cms
        
        return 'Unknown'
    
    def _detect_js_libraries(self, content: str) -> List[str]:
        """Detecta librerías JavaScript utilizadas"""
        libraries = {
            'jquery': ['jquery', '$.'],
            'react': ['react', 'ReactDOM'],
            'angular': ['angular', 'ng-'],
            'vue': ['vue.js', 'vue'],
            'bootstrap': ['bootstrap', 'btn-'],
            'fontawesome': ['font-awesome', 'fa-']
        }
        
        found_libraries = []
        content_lower = content.lower()
        
        for library, indicators in libraries.items():
            for indicator in indicators:
                if indicator in content_lower:
                    found_libraries.append(library)
                    break
        
        return found_libraries
    
    def _check_security_headers(self, domain: str) -> Dict[str, Any]:
        """Verifica headers de seguridad"""
        try:
            url = f"https://{domain}"
            response = requests.get(url, timeout=10, verify=False)
            
            security_headers = {
                'strict-transport-security': response.headers.get('Strict-Transport-Security'),
                'content-security-policy': response.headers.get('Content-Security-Policy'),
                'x-frame-options': response.headers.get('X-Frame-Options'),
                'x-content-type-options': response.headers.get('X-Content-Type-Options'),
                'x-xss-protection': response.headers.get('X-XSS-Protection'),
                'referrer-policy': response.headers.get('Referrer-Policy')
            }
            
            # Evaluar nivel de seguridad
            security_score = sum(1 for header in security_headers.values() if header)
            
            return {
                'headers': security_headers,
                'security_score': security_score,
                'max_score': len(security_headers),
                'rating': self._get_security_rating(security_score, len(security_headers))
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_security_rating(self, score: int, max_score: int) -> str:
        """Calcula el rating de seguridad"""
        percentage = (score / max_score) * 100
        
        if percentage >= 80:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 40:
            return 'C'
        elif percentage >= 20:
            return 'D'
        else:
            return 'F'
    
    def _basic_port_scan(self, domain: str) -> Dict[str, Any]:
        """Realiza un escaneo básico de puertos"""
        try:
            ip = socket.gethostbyname(domain)
            common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 3389, 5432, 3306]
            
            open_ports = []
            closed_ports = []
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((ip, port))
                
                if result == 0:
                    open_ports.append(port)
                else:
                    closed_ports.append(port)
                
                sock.close()
            
            return {
                'open_ports': open_ports,
                'closed_ports': closed_ports,
                'total_scanned': len(common_ports)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_geolocation(self, domain: str) -> Dict[str, Any]:
        """Obtiene la geolocalización del dominio"""
        try:
            ip = socket.gethostbyname(domain)
            
            # Usar servicio gratuito de geolocalización
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'ip': ip,
                    'country': data.get('country'),
                    'country_code': data.get('countryCode'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'isp': data.get('isp'),
                    'timezone': data.get('timezone')
                }
            else:
                return {'error': 'Geolocation failed'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _get_shodan_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información de Shodan"""
        try:
            import shodan
            
            api = shodan.Shodan(self.api_keys['SHODAN_API_KEY'])
            ip = socket.gethostbyname(domain)
            
            host = api.host(ip)
            
            return {
                'ip': ip,
                'organization': host.get('org', 'Unknown'),
                'operating_system': host.get('os', 'Unknown'),
                'ports': host.get('ports', []),
                'vulnerabilities': host.get('vulns', []),
                'last_update': host.get('last_update', 'Unknown'),
                'country': host.get('country_name', 'Unknown'),
                'city': host.get('city', 'Unknown'),
                'isp': host.get('isp', 'Unknown')
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_virustotal_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información de VirusTotal"""
        try:
            url = f"https://www.virustotal.com/vtapi/v2/domain/report"
            params = {
                'apikey': self.api_keys['VIRUSTOTAL_API_KEY'],
                'domain': domain
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('response_code') == 1:
                return {
                    'detected_urls': data.get('detected_urls', []),
                    'detected_downloaded_samples': data.get('detected_downloaded_samples', []),
                    'undetected_urls': data.get('undetected_urls', []),
                    'resolutions': data.get('resolutions', []),
                    'subdomains': data.get('subdomains', [])
                }
            else:
                return {'error': 'No data available'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _get_urlscan_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información de urlscan.io"""
        try:
            # Iniciar escaneo
            scan_url = "https://urlscan.io/api/v1/scan/"
            headers = {
                'API-Key': self.api_keys['URLSCAN_API_KEY'],
                'Content-Type': 'application/json'
            }
            data = {
                'url': f"https://{domain}",
                'visibility': 'public'
            }
            
            response = requests.post(scan_url, json=data, headers=headers, timeout=10)
            scan_result = response.json()
            
            if 'uuid' in scan_result:
                # Esperar un poco para que el escaneo se complete
                import time
                time.sleep(10)
                
                # Obtener resultados
                result_url = f"https://urlscan.io/api/v1/result/{scan_result['uuid']}/"
                result_response = requests.get(result_url, timeout=10)
                result_data = result_response.json()
                
                return {
                    'scan_id': scan_result['uuid'],
                    'url': result_data.get('task', {}).get('url'),
                    'screenshot': result_data.get('task', {}).get('screenshotURL'),
                    'domains': result_data.get('lists', {}).get('domains', []),
                    'ips': result_data.get('lists', {}).get('ips', []),
                    'countries': result_data.get('lists', {}).get('countries', []),
                    'technologies': result_data.get('meta', {}).get('processors', {}).get('wappa', {}).get('data', [])
                }
            else:
                return {'error': 'Scan failed'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def generate_summary(self) -> Dict[str, Any]:
        """Genera un resumen del análisis"""
        if not self.results:
            return {'error': 'No analysis results available'}
        
        summary = {
            'domain': self.results.get('domain'),
            'is_active': self.results.get('basic_info', {}).get('is_active', False),
            'ip_address': self.results.get('basic_info', {}).get('ip_address'),
            'registrar': self.results.get('whois_info', {}).get('registrar'),
            'creation_date': self.results.get('whois_info', {}).get('creation_date'),
            'expiration_date': self.results.get('whois_info', {}).get('expiration_date'),
            'subdomains_found': len(self.results.get('subdomains', [])),
            'open_ports': len(self.results.get('ports_scan', {}).get('open_ports', [])),
            'security_rating': self.results.get('security_headers', {}).get('rating', 'Unknown'),
            'technologies': {
                'server': self.results.get('technology_stack', {}).get('server'),
                'cms': self.results.get('technology_stack', {}).get('cms'),
                'framework': self.results.get('technology_stack', {}).get('framework')
            },
            'location': {
                'country': self.results.get('geolocation', {}).get('country'),
                'city': self.results.get('geolocation', {}).get('city'),
                'isp': self.results.get('geolocation', {}).get('isp')
            }
        }
        
        return summary