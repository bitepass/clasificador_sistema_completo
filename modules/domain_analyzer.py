"""
Módulo de Análisis de Dominio para OSINT-Nexus
Integra múltiples herramientas para análisis completo de dominios e infraestructura
"""
import requests
import whois
import dns.resolver
import socket
import json
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
from config.api_keys import api_key_manager
from config.settings import API_CONFIG, MODULES_CONFIG

class DomainAnalyzer:
    """Analizador de dominios que integra múltiples herramientas OSINT"""
    
    def __init__(self):
        self.api_config = API_CONFIG.copy()
        self.module_config = MODULES_CONFIG["domain"]
        self.results = {
            "domain_info": {},
            "subdomains": [],
            "ip_addresses": [],
            "ports_services": [],
            "technologies": [],
            "vulnerabilities": [],
            "whois_data": {},
            "dns_records": {},
            "ssl_certificate": {},
            "related_domains": [],
            "metadata": {
                "scan_time": None,
                "tools_used": [],
                "errors": []
            }
        }
    
    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Realiza un análisis completo del dominio"""
        start_time = time.time()
        
        # Limpiar y validar el dominio
        domain = self._clean_domain(domain)
        if not self._validate_domain(domain):
            return {"error": "Dominio inválido"}
        
        self.results["metadata"]["scan_time"] = start_time
        self.results["metadata"]["tools_used"] = []
        
        try:
            # Análisis básico de DNS y WHOIS
            self._analyze_dns(domain)
            self._analyze_whois(domain)
            
            # Análisis con herramientas externas
            if api_key_manager.validate_api_key("shodan"):
                self._analyze_shodan(domain)
                self.results["metadata"]["tools_used"].append("shodan")
            
            if api_key_manager.validate_api_key("criminal_ip"):
                self._analyze_criminal_ip(domain)
                self.results["metadata"]["tools_used"].append("criminal_ip")
            
            # Análisis de subdominios (simulado)
            self._analyze_subdomains(domain)
            
            # Análisis de tecnologías web
            self._analyze_web_technologies(domain)
            
            # Análisis de SSL
            self._analyze_ssl_certificate(domain)
            
        except Exception as e:
            self.results["metadata"]["errors"].append(str(e))
        
        self.results["metadata"]["scan_time"] = time.time() - start_time
        return self.results
    
    def _clean_domain(self, domain: str) -> str:
        """Limpia y normaliza el dominio"""
        domain = domain.lower().strip()
        if domain.startswith(("http://", "https://")):
            domain = urlparse(domain).netloc
        return domain
    
    def _validate_domain(self, domain: str) -> bool:
        """Valida que el dominio tenga un formato correcto"""
        import re
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        return bool(re.match(pattern, domain))
    
    def _analyze_dns(self, domain: str) -> None:
        """Analiza registros DNS del dominio"""
        try:
            # Resolución de IP
            try:
                ip = socket.gethostbyname(domain)
                self.results["ip_addresses"].append({
                    "type": "A",
                    "value": ip,
                    "source": "DNS"
                })
            except socket.gaierror:
                pass
            
            # Registros DNS específicos
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    self.results["dns_records"][record_type] = [
                        str(answer) for answer in answers
                    ]
                except Exception:
                    continue
                    
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error DNS: {str(e)}")
    
    def _analyze_whois(self, domain: str) -> None:
        """Analiza información WHOIS del dominio"""
        try:
            w = whois.whois(domain)
            self.results["whois_data"] = {
                "registrar": w.registrar,
                "creation_date": w.creation_date,
                "expiration_date": w.expiration_date,
                "updated_date": w.updated_date,
                "status": w.status,
                "name_servers": w.name_servers,
                "emails": w.emails
            }
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error WHOIS: {str(e)}")
    
    def _analyze_shodan(self, domain: str) -> None:
        """Analiza el dominio usando Shodan"""
        try:
            api_key = api_key_manager.get_api_key("shodan")
            if not api_key:
                return
            
            # Buscar información del dominio
            url = "https://api.shodan.io/shodan/host/search"
            params = {
                "key": api_key,
                "query": f"hostname:{domain}",
                "facets": "port,product"
            }
            
            response = requests.get(url, params=params, timeout=self.api_config["timeout"])
            if response.status_code == 200:
                data = response.json()
                
                for result in data.get("matches", []):
                    # Información de puertos y servicios
                    port_info = {
                        "port": result.get("port"),
                        "product": result.get("product"),
                        "version": result.get("version"),
                        "transport": result.get("transport"),
                        "data": result.get("data", "")[:500]  # Limitar datos
                    }
                    self.results["ports_services"].append(port_info)
                    
                    # Tecnologías detectadas
                    if result.get("product"):
                        tech = {
                            "name": result.get("product"),
                            "version": result.get("version"),
                            "port": result.get("port"),
                            "source": "shodan"
                        }
                        self.results["technologies"].append(tech)
                
                # Vulnerabilidades conocidas
                for result in data.get("matches", []):
                    if result.get("vulns"):
                        for vuln in result["vulns"]:
                            vuln_info = {
                                "cve": vuln,
                                "port": result.get("port"),
                                "source": "shodan"
                            }
                            self.results["vulnerabilities"].append(vuln_info)
                            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error Shodan: {str(e)}")
    
    def _analyze_criminal_ip(self, domain: str) -> None:
        """Analiza el dominio usando Criminal IP"""
        try:
            api_key = api_key_manager.get_api_key("criminal_ip")
            if not api_key:
                return
            
            # Simulación de análisis con Criminal IP
            # En una implementación real, usarías la API oficial
            url = "https://api.criminalip.io/v1/domain/overview"
            headers = {"x-api-key": api_key}
            params = {"query": domain}
            
            response = requests.get(url, headers=headers, params=params, timeout=self.api_config["timeout"])
            if response.status_code == 200:
                data = response.json()
                
                # Procesar resultados (estructura específica de Criminal IP)
                if "data" in data:
                    domain_data = data["data"]
                    
                    # Subdominios
                    if "subdomains" in domain_data:
                        for subdomain in domain_data["subdomains"]:
                            self.results["subdomains"].append({
                                "name": subdomain,
                                "source": "criminal_ip"
                            })
                    
                    # IPs relacionadas
                    if "ips" in domain_data:
                        for ip in domain_data["ips"]:
                            self.results["ip_addresses"].append({
                                "type": "related",
                                "value": ip,
                                "source": "criminal_ip"
                            })
                            
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error Criminal IP: {str(e)}")
    
    def _analyze_subdomains(self, domain: str) -> None:
        """Analiza subdominios del dominio"""
        try:
            # Lista de subdominios comunes para probar
            common_subdomains = [
                "www", "mail", "ftp", "admin", "blog", "dev", "test",
                "api", "cdn", "static", "img", "images", "media",
                "support", "help", "docs", "forum", "shop", "store"
            ]
            
            for subdomain in common_subdomains:
                full_domain = f"{subdomain}.{domain}"
                try:
                    ip = socket.gethostbyname(full_domain)
                    self.results["subdomains"].append({
                        "name": full_domain,
                        "ip": ip,
                        "source": "dns_enumeration"
                    })
                except socket.gaierror:
                    continue
                    
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error subdominios: {str(e)}")
    
    def _analyze_web_technologies(self, domain: str) -> None:
        """Analiza tecnologías web del sitio"""
        try:
            url = f"https://{domain}"
            headers = {
                "User-Agent": self.api_config["user_agent"]
            }
            
            response = requests.get(url, headers=headers, timeout=self.api_config["timeout"])
            
            # Detectar tecnologías basadas en headers
            server = response.headers.get("Server")
            if server:
                self.results["technologies"].append({
                    "name": "Web Server",
                    "version": server,
                    "source": "http_headers"
                })
            
            powered_by = response.headers.get("X-Powered-By")
            if powered_by:
                self.results["technologies"].append({
                    "name": "Framework",
                    "version": powered_by,
                    "source": "http_headers"
                })
            
            # Detectar tecnologías en el contenido HTML
            content = response.text.lower()
            
            # Detectar frameworks populares
            frameworks = {
                "WordPress": ["wp-content", "wp-includes"],
                "Drupal": ["drupal", "sites/default"],
                "Joomla": ["joomla", "components/com_"],
                "Laravel": ["laravel", "csrf-token"],
                "Django": ["csrfmiddlewaretoken", "django"],
                "React": ["react", "reactjs"],
                "Angular": ["ng-", "angular"],
                "Vue.js": ["vue", "v-"],
                "Bootstrap": ["bootstrap", "bootstrap.min.css"]
            }
            
            for framework, indicators in frameworks.items():
                if any(indicator in content for indicator in indicators):
                    self.results["technologies"].append({
                        "name": framework,
                        "version": "detected",
                        "source": "html_analysis"
                    })
                    
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error tecnologías web: {str(e)}")
    
    def _analyze_ssl_certificate(self, domain: str) -> None:
        """Analiza el certificado SSL del dominio"""
        try:
            import ssl
            import socket
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=self.api_config["timeout"]) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    self.results["ssl_certificate"] = {
                        "subject": dict(x[0] for x in cert["subject"]),
                        "issuer": dict(x[0] for x in cert["issuer"]),
                        "version": cert["version"],
                        "serial_number": cert["serialNumber"],
                        "not_before": cert["notBefore"],
                        "not_after": cert["notAfter"],
                        "san": cert.get("subjectAltName", [])
                    }
                    
        except Exception as e:
            self.results["metadata"]["errors"].append(f"Error SSL: {str(e)}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del análisis"""
        return {
            "domain": self.results.get("domain_info", {}),
            "total_subdomains": len(self.results["subdomains"]),
            "total_ips": len(self.results["ip_addresses"]),
            "total_ports": len(self.results["ports_services"]),
            "total_technologies": len(self.results["technologies"]),
            "total_vulnerabilities": len(self.results["vulnerabilities"]),
            "scan_duration": self.results["metadata"]["scan_time"],
            "tools_used": self.results["metadata"]["tools_used"],
            "errors": len(self.results["metadata"]["errors"])
        }