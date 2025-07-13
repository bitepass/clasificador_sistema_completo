"""
Procesador de Datos para OSINT-Nexus
Consolida, correlaciona y enriquece los datos recolectados
"""

import json
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import hashlib
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

class DataProcessor:
    """Procesador central de datos OSINT"""
    
    def __init__(self):
        self.entities = defaultdict(set)  # Almacenar entidades únicas
        self.relationships = []  # Almacenar relaciones entre entidades
        
    def process_investigation_results(self, investigation_type: str, 
                                    target: str, 
                                    results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar y enriquecer los resultados de una investigación
        
        Args:
            investigation_type: Tipo de investigación (domain, email, username)
            target: Objetivo de la investigación
            results: Resultados crudos de la investigación
            
        Returns:
            Diccionario con resultados procesados y enriquecidos
        """
        logger.info(f"Procesando resultados de {investigation_type} para {target}")
        
        # Procesar según el tipo de investigación
        if investigation_type == 'domain':
            processed = self._process_domain_results(target, results)
        elif investigation_type == 'email':
            processed = self._process_email_results(target, results)
        elif investigation_type == 'username':
            processed = self._process_username_results(target, results)
        else:
            processed = results
        
        # Extraer entidades y relaciones
        self._extract_entities_and_relationships(investigation_type, target, processed)
        
        # Agregar metadatos de procesamiento
        processed['_metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'investigation_type': investigation_type,
            'target': target,
            'entity_count': len(self.entities),
            'relationship_count': len(self.relationships)
        }
        
        return processed
    
    def _process_domain_results(self, domain: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar resultados específicos de dominio"""
        processed = results.copy()
        
        # Consolidar emails encontrados
        all_emails = set()
        if 'emails' in results:
            all_emails.update(results['emails'])
        
        # Extraer emails de WHOIS
        if results.get('whois') and results['whois'].get('emails'):
            all_emails.update(results['whois']['emails'])
        
        processed['consolidated_emails'] = list(all_emails)
        
        # Consolidar subdominios
        all_subdomains = set()
        if 'subdomains' in results:
            all_subdomains.update(results['subdomains'])
        
        processed['total_subdomains'] = len(all_subdomains)
        
        # Análisis de seguridad
        security_score = 100
        security_issues = []
        
        # Verificar SSL
        if results.get('ssl_info') is None:
            security_score -= 20
            security_issues.append('Sin certificado SSL detectado')
        
        # Verificar vulnerabilidades de Shodan
        if results.get('shodan') and results['shodan'].get('vulnerabilities'):
            vuln_count = len(results['shodan']['vulnerabilities'])
            security_score -= min(vuln_count * 10, 50)
            security_issues.append(f'{vuln_count} vulnerabilidades detectadas')
        
        processed['security_analysis'] = {
            'score': max(0, security_score),
            'issues': security_issues
        }
        
        return processed
    
    def _process_email_results(self, email: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar resultados específicos de email"""
        processed = results.copy()
        
        # Análisis de credibilidad
        credibility_score = 100
        credibility_factors = []
        
        if results.get('verification'):
            ver = results['verification']
            if not ver.get('domain_exists'):
                credibility_score -= 40
                credibility_factors.append('Dominio no existe')
            if ver.get('disposable'):
                credibility_score -= 30
                credibility_factors.append('Email desechable')
            if ver.get('role_based'):
                credibility_score -= 10
                credibility_factors.append('Email genérico/rol')
        
        processed['credibility_analysis'] = {
            'score': max(0, credibility_score),
            'factors': credibility_factors
        }
        
        # Resumen de exposición
        exposure_level = 'BAJO'
        if results.get('breaches'):
            breach_count = len(results['breaches'])
            if breach_count >= 5:
                exposure_level = 'CRÍTICO'
            elif breach_count >= 3:
                exposure_level = 'ALTO'
            elif breach_count >= 1:
                exposure_level = 'MEDIO'
        
        processed['exposure_summary'] = {
            'level': exposure_level,
            'breach_count': len(results.get('breaches', [])),
            'social_profiles': len(results.get('social_profiles', []))
        }
        
        return processed
    
    def _process_username_results(self, username: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar resultados específicos de username"""
        processed = results.copy()
        
        # Crear perfil digital consolidado
        digital_profile = {
            'username': username,
            'presence_score': 0,
            'activity_indicators': [],
            'primary_platforms': [],
            'interests': []
        }
        
        if 'analysis' in results:
            analysis = results['analysis']
            digital_profile['presence_score'] = analysis.get('digital_footprint_score', 0)
            
            # Determinar plataformas principales
            if 'found' in results:
                platform_counts = defaultdict(int)
                for profile in results['found']:
                    platform = profile.get('platform')
                    if platform:
                        platform_counts[platform] += 1
                
                # Top 5 plataformas
                top_platforms = sorted(platform_counts.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:5]
                digital_profile['primary_platforms'] = [p[0] for p in top_platforms]
            
            # Inferir intereses basados en categorías
            if 'platforms_by_category' in analysis:
                for category, count in analysis['platforms_by_category'].items():
                    if count >= 2:
                        digital_profile['interests'].append(category)
        
        processed['digital_profile'] = digital_profile
        
        return processed
    
    def _extract_entities_and_relationships(self, investigation_type: str, 
                                          target: str, 
                                          results: Dict[str, Any]):
        """Extraer entidades y relaciones de los resultados"""
        
        # Agregar entidad principal
        self.entities[investigation_type].add(target)
        
        if investigation_type == 'domain':
            # Extraer IPs
            if results.get('ip_info') and results['ip_info'].get('ip'):
                ip = results['ip_info']['ip']
                self.entities['ip'].add(ip)
                self.relationships.append({
                    'source': target,
                    'target': ip,
                    'type': 'resolves_to'
                })
            
            # Extraer emails
            if results.get('consolidated_emails'):
                for email in results['consolidated_emails']:
                    self.entities['email'].add(email)
                    self.relationships.append({
                        'source': target,
                        'target': email,
                        'type': 'email_found_on'
                    })
            
            # Extraer subdominios
            if results.get('subdomains'):
                for subdomain in results['subdomains']:
                    self.entities['subdomain'].add(subdomain)
                    self.relationships.append({
                        'source': target,
                        'target': subdomain,
                        'type': 'has_subdomain'
                    })
        
        elif investigation_type == 'email':
            # Extraer dominio del email
            domain = target.split('@')[1]
            self.entities['domain'].add(domain)
            self.relationships.append({
                'source': target,
                'target': domain,
                'type': 'email_domain'
            })
            
            # Extraer perfiles sociales
            if results.get('social_profiles'):
                for profile in results['social_profiles']:
                    if profile.get('url'):
                        self.entities['social_profile'].add(profile['url'])
                        self.relationships.append({
                            'source': target,
                            'target': profile['url'],
                            'type': 'has_profile'
                        })
        
        elif investigation_type == 'username':
            # Extraer URLs de perfiles encontrados
            if results.get('found'):
                for profile in results['found']:
                    if profile.get('url'):
                        self.entities['social_profile'].add(profile['url'])
                        self.relationships.append({
                            'source': target,
                            'target': profile['url'],
                            'type': 'username_found_at'
                        })
    
    def correlate_investigations(self, investigations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Correlacionar múltiples investigaciones para encontrar conexiones
        
        Args:
            investigations: Lista de resultados de investigaciones
            
        Returns:
            Diccionario con correlaciones encontradas
        """
        correlations = {
            'common_entities': defaultdict(list),
            'entity_graph': {
                'nodes': [],
                'edges': []
            },
            'insights': []
        }
        
        # Buscar entidades comunes
        entity_investigations = defaultdict(list)
        
        for inv in investigations:
            inv_type = inv.get('_metadata', {}).get('investigation_type')
            target = inv.get('_metadata', {}).get('target')
            
            if inv_type and target:
                # Registrar todas las entidades encontradas
                for entity_type, entities in self.entities.items():
                    for entity in entities:
                        entity_investigations[entity].append({
                            'type': inv_type,
                            'target': target
                        })
        
        # Identificar entidades que aparecen en múltiples investigaciones
        for entity, appearances in entity_investigations.items():
            if len(appearances) > 1:
                correlations['common_entities'][entity] = appearances
        
        # Construir grafo de entidades
        # Nodos
        for entity_type, entities in self.entities.items():
            for entity in entities:
                correlations['entity_graph']['nodes'].append({
                    'id': entity,
                    'type': entity_type,
                    'label': entity
                })
        
        # Aristas (relaciones)
        for rel in self.relationships:
            correlations['entity_graph']['edges'].append({
                'source': rel['source'],
                'target': rel['target'],
                'type': rel['type']
            })
        
        # Generar insights
        if correlations['common_entities']:
            correlations['insights'].append(
                f"Se encontraron {len(correlations['common_entities'])} entidades comunes entre investigaciones"
            )
        
        # Detectar patrones específicos
        email_domains = [e.split('@')[1] for e in self.entities.get('email', []) if '@' in e]
        unique_domains = set(email_domains)
        if len(unique_domains) == 1 and len(email_domains) > 1:
            correlations['insights'].append(
                f"Todos los emails encontrados pertenecen al mismo dominio: {list(unique_domains)[0]}"
            )
        
        return correlations
    
    def generate_summary_report(self, investigations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generar un reporte resumen de todas las investigaciones
        
        Args:
            investigations: Lista de investigaciones realizadas
            
        Returns:
            Diccionario con el resumen ejecutivo
        """
        summary = {
            'total_investigations': len(investigations),
            'investigation_types': defaultdict(int),
            'total_entities_discovered': sum(len(entities) for entities in self.entities.values()),
            'entity_breakdown': {},
            'risk_summary': {
                'high_risk_findings': [],
                'medium_risk_findings': [],
                'low_risk_findings': []
            },
            'key_findings': [],
            'recommendations': []
        }
        
        # Contar tipos de investigación
        for inv in investigations:
            inv_type = inv.get('_metadata', {}).get('investigation_type')
            if inv_type:
                summary['investigation_types'][inv_type] += 1
        
        # Desglose de entidades
        for entity_type, entities in self.entities.items():
            summary['entity_breakdown'][entity_type] = len(entities)
        
        # Analizar riesgos y hallazgos clave
        for inv in investigations:
            # Buscar indicadores de riesgo alto
            if inv.get('risk_assessment'):
                risk = inv['risk_assessment']
                if risk.get('level') == 'ALTO':
                    summary['risk_summary']['high_risk_findings'].append({
                        'target': inv.get('_metadata', {}).get('target'),
                        'factors': risk.get('factors', [])
                    })
            
            # Buscar brechas de datos
            if inv.get('breaches'):
                breach_count = len(inv['breaches'])
                if breach_count > 0:
                    summary['key_findings'].append(
                        f"Email {inv.get('email')} encontrado en {breach_count} brechas de datos"
                    )
            
            # Buscar vulnerabilidades
            if inv.get('shodan', {}).get('vulnerabilities'):
                vuln_count = len(inv['shodan']['vulnerabilities'])
                summary['key_findings'].append(
                    f"Dominio {inv.get('domain')} tiene {vuln_count} vulnerabilidades conocidas"
                )
        
        # Generar recomendaciones
        if summary['risk_summary']['high_risk_findings']:
            summary['recommendations'].append(
                "Se detectaron hallazgos de alto riesgo. Se recomienda acción inmediata."
            )
        
        if 'email' in summary['entity_breakdown'] and summary['entity_breakdown']['email'] > 0:
            summary['recommendations'].append(
                "Verificar y actualizar las políticas de privacidad de emails expuestos."
            )
        
        if 'vulnerabilities' in str(investigations):
            summary['recommendations'].append(
                "Realizar parcheo de vulnerabilidades identificadas en la infraestructura."
            )
        
        return summary