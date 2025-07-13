"""
Procesador de Datos para OSINT-Nexus
Limpia, correlaciona y analiza datos de múltiples fuentes OSINT
"""
import re
import json
import hashlib
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from collections import Counter, defaultdict

class DataProcessor:
    """Procesador de datos para análisis y correlación OSINT"""
    
    def __init__(self):
        self.processed_data = {}
        self.correlations = {}
        self.entities = {}
        
    def process_domain_data(self, domain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa y limpia datos de análisis de dominio"""
        try:
            processed = {
                "domain_info": self._clean_domain_info(domain_data.get("domain_info", {})),
                "subdomains": self._clean_subdomains(domain_data.get("subdomains", [])),
                "ip_addresses": self._clean_ip_addresses(domain_data.get("ip_addresses", [])),
                "technologies": self._clean_technologies(domain_data.get("technologies", [])),
                "vulnerabilities": self._clean_vulnerabilities(domain_data.get("vulnerabilities", [])),
                "whois_data": self._clean_whois_data(domain_data.get("whois_data", {})),
                "dns_records": self._clean_dns_records(domain_data.get("dns_records", {})),
                "ssl_certificate": self._clean_ssl_data(domain_data.get("ssl_certificate", {})),
                "metadata": domain_data.get("metadata", {})
            }
            
            # Generar estadísticas
            processed["statistics"] = self._generate_domain_statistics(processed)
            
            return processed
            
        except Exception as e:
            print(f"Error procesando datos de dominio: {str(e)}")
            return domain_data
    
    def process_email_data(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa y limpia datos de análisis de email"""
        try:
            processed = {
                "email_info": self._clean_email_info(email_data.get("email_info", {})),
                "breaches": self._clean_breaches(email_data.get("breaches", [])),
                "social_profiles": self._clean_social_profiles(email_data.get("social_profiles", [])),
                "domain_info": self._clean_domain_info(email_data.get("domain_info", {})),
                "related_emails": self._clean_related_emails(email_data.get("related_emails", [])),
                "metadata": email_data.get("metadata", {})
            }
            
            # Generar estadísticas
            processed["statistics"] = self._generate_email_statistics(processed)
            
            return processed
            
        except Exception as e:
            print(f"Error procesando datos de email: {str(e)}")
            return email_data
    
    def process_username_data(self, username_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa y limpia datos de análisis de username"""
        try:
            processed = {
                "username": self._clean_username(username_data.get("username", "")),
                "profiles": self._clean_profiles(username_data.get("profiles", [])),
                "statistics": self._clean_statistics(username_data.get("statistics", {})),
                "metadata": username_data.get("metadata", {})
            }
            
            # Generar estadísticas adicionales
            processed["statistics"] = self._generate_username_statistics(processed)
            
            return processed
            
        except Exception as e:
            print(f"Error procesando datos de username: {str(e)}")
            return username_data
    
    def process_social_data(self, social_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa y limpia datos de análisis social"""
        try:
            processed = {
                "profile_info": self._clean_profile_info(social_data.get("profile_info", {})),
                "posts": self._clean_posts(social_data.get("posts", [])),
                "connections": self._clean_connections(social_data.get("connections", [])),
                "activity_analysis": self._clean_activity_analysis(social_data.get("activity_analysis", {})),
                "geolocation": self._clean_geolocation(social_data.get("geolocation", [])),
                "metadata": social_data.get("metadata", {})
            }
            
            # Generar estadísticas
            processed["statistics"] = self._generate_social_statistics(processed)
            
            return processed
            
        except Exception as e:
            print(f"Error procesando datos sociales: {str(e)}")
            return social_data
    
    def correlate_data(self, data_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Correlaciona datos de múltiples fuentes"""
        try:
            correlations = {
                "entities": {},
                "relationships": [],
                "patterns": {},
                "insights": []
            }
            
            # Extraer entidades únicas
            entities = self._extract_entities(data_sources)
            correlations["entities"] = entities
            
            # Encontrar relaciones
            relationships = self._find_relationships(data_sources, entities)
            correlations["relationships"] = relationships
            
            # Identificar patrones
            patterns = self._identify_patterns(data_sources)
            correlations["patterns"] = patterns
            
            # Generar insights
            insights = self._generate_insights(correlations)
            correlations["insights"] = insights
            
            return correlations
            
        except Exception as e:
            print(f"Error correlacionando datos: {str(e)}")
            return {}
    
    def _clean_domain_info(self, domain_info: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia información de dominio"""
        cleaned = {}
        
        if domain_info.get("domain"):
            cleaned["domain"] = domain_info["domain"].lower().strip()
        
        # Limpiar otros campos
        for key, value in domain_info.items():
            if value is not None and value != "":
                if isinstance(value, str):
                    cleaned[key] = value.strip()
                else:
                    cleaned[key] = value
        
        return cleaned
    
    def _clean_subdomains(self, subdomains: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia lista de subdominios"""
        cleaned = []
        seen = set()
        
        for subdomain in subdomains:
            name = subdomain.get("name", "").lower().strip()
            if name and name not in seen:
                seen.add(name)
                cleaned.append({
                    "name": name,
                    "ip": subdomain.get("ip", ""),
                    "source": subdomain.get("source", ""),
                    "first_seen": datetime.now().isoformat()
                })
        
        return cleaned
    
    def _clean_ip_addresses(self, ip_addresses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia lista de direcciones IP"""
        cleaned = []
        seen = set()
        
        for ip_info in ip_addresses:
            ip = ip_info.get("value", "").strip()
            if ip and self._is_valid_ip(ip) and ip not in seen:
                seen.add(ip)
                cleaned.append({
                    "ip": ip,
                    "type": ip_info.get("type", "unknown"),
                    "source": ip_info.get("source", ""),
                    "first_seen": datetime.now().isoformat()
                })
        
        return cleaned
    
    def _clean_technologies(self, technologies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia lista de tecnologías"""
        cleaned = []
        seen = set()
        
        for tech in technologies:
            name = tech.get("name", "").strip()
            if name and name not in seen:
                seen.add(name)
                cleaned.append({
                    "name": name,
                    "version": tech.get("version", ""),
                    "port": tech.get("port", ""),
                    "source": tech.get("source", ""),
                    "first_seen": datetime.now().isoformat()
                })
        
        return cleaned
    
    def _clean_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia lista de vulnerabilidades"""
        cleaned = []
        seen = set()
        
        for vuln in vulnerabilities:
            cve = vuln.get("cve", "").strip()
            if cve and cve not in seen:
                seen.add(cve)
                cleaned.append({
                    "cve": cve,
                    "port": vuln.get("port", ""),
                    "source": vuln.get("source", ""),
                    "severity": self._assess_vulnerability_severity(cve),
                    "first_seen": datetime.now().isoformat()
                })
        
        return cleaned
    
    def _clean_whois_data(self, whois_data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia datos WHOIS"""
        cleaned = {}
        
        for key, value in whois_data.items():
            if value is not None and value != "":
                if isinstance(value, list):
                    cleaned[key] = [str(v).strip() for v in value if v]
                elif isinstance(value, str):
                    cleaned[key] = value.strip()
                else:
                    cleaned[key] = value
        
        return cleaned
    
    def _clean_dns_records(self, dns_records: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia registros DNS"""
        cleaned = {}
        
        for record_type, records in dns_records.items():
            if records:
                cleaned[record_type] = [str(record).strip() for record in records if record]
        
        return cleaned
    
    def _clean_ssl_data(self, ssl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia datos SSL"""
        cleaned = {}
        
        for key, value in ssl_data.items():
            if value is not None and value != "":
                cleaned[key] = value
        
        return cleaned
    
    def _clean_email_info(self, email_info: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia información de email"""
        cleaned = {}
        
        if email_info.get("email"):
            cleaned["email"] = email_info["email"].lower().strip()
        
        if email_info.get("username"):
            cleaned["username"] = email_info["username"].lower().strip()
        
        if email_info.get("domain"):
            cleaned["domain"] = email_info["domain"].lower().strip()
        
        # Otros campos
        for key, value in email_info.items():
            if value is not None and value != "" and key not in ["email", "username", "domain"]:
                cleaned[key] = value
        
        return cleaned
    
    def _clean_breaches(self, breaches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia datos de brechas"""
        cleaned = []
        seen = set()
        
        for breach in breaches:
            name = breach.get("name", "").strip()
            if name and name not in seen:
                seen.add(name)
                cleaned.append({
                    "name": name,
                    "title": breach.get("title", ""),
                    "breach_date": breach.get("breach_date", ""),
                    "pwn_count": breach.get("pwn_count", 0),
                    "data_classes": breach.get("data_classes", []),
                    "is_verified": breach.get("is_verified", False),
                    "first_seen": datetime.now().isoformat()
                })
        
        return cleaned
    
    def _clean_social_profiles(self, profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia perfiles sociales"""
        cleaned = []
        
        for profile in profiles:
            cleaned.append({
                "platform": profile.get("platform", "").lower(),
                "username": profile.get("username", ""),
                "url": profile.get("url", ""),
                "exists": profile.get("exists", False),
                "last_checked": profile.get("last_checked", datetime.now().isoformat())
            })
        
        return cleaned
    
    def _clean_related_emails(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia emails relacionados"""
        cleaned = []
        seen = set()
        
        for email in emails:
            email_addr = email.get("email", "").lower().strip()
            if email_addr and email_addr not in seen:
                seen.add(email_addr)
                cleaned.append({
                    "email": email_addr,
                    "first_name": email.get("first_name", ""),
                    "last_name": email.get("last_name", ""),
                    "position": email.get("position", ""),
                    "department": email.get("department", ""),
                    "confidence": email.get("confidence", 0)
                })
        
        return cleaned
    
    def _clean_username(self, username: str) -> str:
        """Limpia nombre de usuario"""
        return username.lower().strip()
    
    def _clean_profiles(self, profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia perfiles de usuario"""
        cleaned = []
        
        for profile in profiles:
            cleaned.append({
                "platform": profile.get("platform", "").lower(),
                "url": profile.get("url", ""),
                "exists": profile.get("exists", False),
                "status_code": profile.get("status_code", ""),
                "title": profile.get("title", ""),
                "last_checked": profile.get("last_checked", datetime.now().isoformat())
            })
        
        return cleaned
    
    def _clean_statistics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia estadísticas"""
        cleaned = {}
        
        for key, value in stats.items():
            if value is not None:
                cleaned[key] = value
        
        return cleaned
    
    def _clean_profile_info(self, profile_info: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia información de perfil social"""
        cleaned = {}
        
        for key, value in profile_info.items():
            if value is not None and value != "":
                if isinstance(value, str):
                    cleaned[key] = value.strip()
                else:
                    cleaned[key] = value
        
        return cleaned
    
    def _clean_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia posts sociales"""
        cleaned = []
        
        for post in posts:
            cleaned.append({
                "id": post.get("id", ""),
                "text": post.get("text", ""),
                "created_at": post.get("created_at", ""),
                "likes": post.get("likes", 0),
                "retweets": post.get("retweets", 0),
                "replies": post.get("replies", 0),
                "hashtags": post.get("hashtags", []),
                "mentions": post.get("mentions", []),
                "urls": post.get("urls", [])
            })
        
        return cleaned
    
    def _clean_connections(self, connections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia conexiones sociales"""
        cleaned = []
        
        for connection in connections:
            cleaned.append({
                "name": connection.get("name", ""),
                "type": connection.get("type", ""),
                "url": connection.get("url", ""),
                "first_seen": datetime.now().isoformat()
            })
        
        return cleaned
    
    def _clean_activity_analysis(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia análisis de actividad"""
        cleaned = {}
        
        for key, value in activity.items():
            if value is not None and value != "":
                cleaned[key] = value
        
        return cleaned
    
    def _clean_geolocation(self, locations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia datos de geolocalización"""
        cleaned = []
        
        for location in locations:
            cleaned.append({
                "post_id": location.get("post_id", ""),
                "location": location.get("location", ""),
                "timestamp": location.get("timestamp", ""),
                "coordinates": location.get("coordinates", {})
            })
        
        return cleaned
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Valida formato de IP"""
        import re
        pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, ip))
    
    def _assess_vulnerability_severity(self, cve: str) -> str:
        """Evalúa la severidad de una vulnerabilidad basándose en el CVE"""
        # Simulación básica - en una implementación real usarías una base de datos de CVEs
        if "critical" in cve.lower() or "high" in cve.lower():
            return "high"
        elif "medium" in cve.lower():
            return "medium"
        else:
            return "low"
    
    def _generate_domain_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera estadísticas para datos de dominio"""
        stats = {
            "total_subdomains": len(data.get("subdomains", [])),
            "total_ips": len(data.get("ip_addresses", [])),
            "total_technologies": len(data.get("technologies", [])),
            "total_vulnerabilities": len(data.get("vulnerabilities", [])),
            "high_severity_vulns": len([v for v in data.get("vulnerabilities", []) if v.get("severity") == "high"]),
            "unique_sources": len(set([s.get("source") for s in data.get("subdomains", []) if s.get("source")]))
        }
        
        return stats
    
    def _generate_email_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera estadísticas para datos de email"""
        stats = {
            "total_breaches": len(data.get("breaches", [])),
            "total_related_emails": len(data.get("related_emails", [])),
            "total_social_profiles": len(data.get("social_profiles", [])),
            "total_records_exposed": sum([b.get("pwn_count", 0) for b in data.get("breaches", [])]),
            "verified_breaches": len([b for b in data.get("breaches", []) if b.get("is_verified")])
        }
        
        return stats
    
    def _generate_username_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera estadísticas para datos de username"""
        profiles = data.get("profiles", [])
        found_profiles = [p for p in profiles if p.get("exists")]
        
        stats = {
            "total_profiles_checked": len(profiles),
            "profiles_found": len(found_profiles),
            "success_rate": len(found_profiles) / len(profiles) if profiles else 0,
            "platforms_with_profiles": list(set([p.get("platform") for p in found_profiles]))
        }
        
        return stats
    
    def _generate_social_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera estadísticas para datos sociales"""
        stats = {
            "total_posts": len(data.get("posts", [])),
            "total_connections": len(data.get("connections", [])),
            "total_locations": len(data.get("geolocation", [])),
            "platform": data.get("profile_info", {}).get("platform", ""),
            "verified": data.get("profile_info", {}).get("verified", False)
        }
        
        return stats
    
    def _extract_entities(self, data_sources: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Extrae entidades únicas de múltiples fuentes"""
        entities = {
            "domains": set(),
            "emails": set(),
            "usernames": set(),
            "ips": set(),
            "organizations": set(),
            "locations": set()
        }
        
        for source in data_sources:
            # Extraer dominios
            if "domain_info" in source and source["domain_info"].get("domain"):
                entities["domains"].add(source["domain_info"]["domain"])
            
            # Extraer emails
            if "email_info" in source and source["email_info"].get("email"):
                entities["emails"].add(source["email_info"]["email"])
            
            # Extraer usernames
            if "username" in source:
                entities["usernames"].add(source["username"])
            
            # Extraer IPs
            for ip_info in source.get("ip_addresses", []):
                if ip_info.get("ip"):
                    entities["ips"].add(ip_info["ip"])
        
        return entities
    
    def _find_relationships(self, data_sources: List[Dict[str, Any]], entities: Dict[str, Set[str]]) -> List[Dict[str, Any]]:
        """Encuentra relaciones entre entidades"""
        relationships = []
        
        # Relaciones dominio-IP
        for source in data_sources:
            if "domain_info" in source and "ip_addresses" in source:
                domain = source["domain_info"].get("domain")
                for ip_info in source["ip_addresses"]:
                    if domain and ip_info.get("ip"):
                        relationships.append({
                            "source": domain,
                            "target": ip_info["ip"],
                            "type": "uses",
                            "source_type": "domain",
                            "target_type": "ip"
                        })
        
        # Relaciones email-dominio
        for source in data_sources:
            if "email_info" in source:
                email = source["email_info"].get("email")
                domain = source["email_info"].get("domain")
                if email and domain:
                    relationships.append({
                        "source": email,
                        "target": domain,
                        "type": "uses",
                        "source_type": "email",
                        "target_type": "domain"
                    })
        
        return relationships
    
    def _identify_patterns(self, data_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identifica patrones en los datos"""
        patterns = {
            "common_technologies": [],
            "common_breaches": [],
            "activity_patterns": [],
            "geographic_patterns": []
        }
        
        # Tecnologías más comunes
        tech_counter = Counter()
        for source in data_sources:
            for tech in source.get("technologies", []):
                tech_counter[tech.get("name", "")] += 1
        
        patterns["common_technologies"] = tech_counter.most_common(10)
        
        # Brechas más comunes
        breach_counter = Counter()
        for source in data_sources:
            for breach in source.get("breaches", []):
                breach_counter[breach.get("name", "")] += 1
        
        patterns["common_breaches"] = breach_counter.most_common(10)
        
        return patterns
    
    def _generate_insights(self, correlations: Dict[str, Any]) -> List[str]:
        """Genera insights basados en las correlaciones"""
        insights = []
        
        entities = correlations.get("entities", {})
        relationships = correlations.get("relationships", [])
        patterns = correlations.get("patterns", {})
        
        # Insight sobre número de entidades
        total_entities = sum(len(entities.get(key, set())) for key in entities)
        insights.append(f"Total unique entities discovered: {total_entities}")
        
        # Insight sobre relaciones
        if relationships:
            insights.append(f"Found {len(relationships)} relationships between entities")
        
        # Insight sobre tecnologías comunes
        common_techs = patterns.get("common_technologies", [])
        if common_techs:
            insights.append(f"Most common technology: {common_techs[0][0]} ({common_techs[0][1]} occurrences)")
        
        # Insight sobre brechas
        common_breaches = patterns.get("common_breaches", [])
        if common_breaches:
            insights.append(f"Most common breach: {common_breaches[0][0]} ({common_breaches[0][1]} occurrences)")
        
        return insights