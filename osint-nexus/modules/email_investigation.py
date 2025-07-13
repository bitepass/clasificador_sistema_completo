"""
Módulo de Investigación de Correo Electrónico
Integra múltiples herramientas para análisis de emails
"""

import re
import logging
import asyncio
import socket
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import dns.resolver

from utils.api_manager import APIManager
from config.api_keys import APIConfig

logger = logging.getLogger(__name__)

class EmailInvestigator:
    """Investigador completo de correos electrónicos"""
    
    def __init__(self):
        self.api_manager = APIManager()
        
    async def investigate_email(self, email: str) -> Dict[str, Any]:
        """
        Investigación completa de un correo electrónico
        
        Args:
            email: Dirección de correo a investigar
            
        Returns:
            Diccionario con todos los resultados de la investigación
        """
        # Validar formato de email
        if not self._validate_email(email):
            return {'error': 'Formato de email inválido'}
            
        logger.info(f"Iniciando investigación de email: {email}")
        
        # Extraer dominio del email
        domain = email.split('@')[1]
        
        # Ejecutar investigaciones en paralelo
        tasks = [
            self._verify_email(email),
            self._check_breaches(email),
            self._search_social_profiles(email),
            self._check_domain_reputation(domain),
            self._search_paste_sites(email),
            self._generate_email_variations(email)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Consolidar resultados
        investigation_results = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'verification': results[0] if not isinstance(results[0], Exception) else None,
            'breaches': results[1] if not isinstance(results[1], Exception) else [],
            'social_profiles': results[2] if not isinstance(results[2], Exception) else [],
            'domain_reputation': results[3] if not isinstance(results[3], Exception) else None,
            'paste_sites': results[4] if not isinstance(results[4], Exception) else [],
            'email_variations': results[5] if not isinstance(results[5], Exception) else []
        }
        
        # Agregar análisis de riesgo
        investigation_results['risk_assessment'] = self._assess_risk(investigation_results)
        
        return investigation_results
    
    def _validate_email(self, email: str) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    async def _verify_email(self, email: str) -> Dict[str, Any]:
        """Verificar la existencia y validez del email"""
        verification = {
            'format_valid': True,
            'domain_exists': False,
            'mx_records': False,
            'smtp_valid': None,
            'disposable': False,
            'role_based': False
        }
        
        try:
            domain = email.split('@')[1]
            
            # Verificar existencia del dominio
            try:
                socket.gethostbyname(domain)
                verification['domain_exists'] = True
            except:
                pass
            
            # Verificar registros MX
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                if mx_records:
                    verification['mx_records'] = True
            except:
                pass
            
            # Verificar si es email desechable
            disposable_domains = [
                'tempmail.com', '10minutemail.com', 'guerrillamail.com',
                'mailinator.com', 'throwaway.email', 'yopmail.com'
            ]
            if any(d in domain for d in disposable_domains):
                verification['disposable'] = True
            
            # Verificar si es email basado en rol
            role_prefixes = [
                'admin', 'info', 'contact', 'support', 'sales',
                'webmaster', 'postmaster', 'noreply', 'no-reply'
            ]
            local_part = email.split('@')[0].lower()
            if any(prefix in local_part for prefix in role_prefixes):
                verification['role_based'] = True
            
            # Usar Hunter.io si está disponible
            if APIConfig.is_api_configured('hunter'):
                hunter_result = self.api_manager.hunter_email_verify(email)
                if hunter_result and 'data' in hunter_result:
                    data = hunter_result['data']
                    verification['smtp_valid'] = data.get('result') == 'deliverable'
                    verification['score'] = data.get('score', 0)
                    
        except Exception as e:
            logger.error(f"Error en verificación de email: {e}")
            
        return verification
    
    async def _check_breaches(self, email: str) -> List[Dict[str, Any]]:
        """Verificar si el email ha sido comprometido en brechas de datos"""
        breaches = []
        
        try:
            # Usar Have I Been Pwned
            if APIConfig.is_api_configured('hibp'):
                hibp_result = self.api_manager.hibp_check(email)
                
                if hibp_result and isinstance(hibp_result, list):
                    for breach in hibp_result:
                        breach_info = {
                            'name': breach.get('Name'),
                            'domain': breach.get('Domain'),
                            'date': breach.get('BreachDate'),
                            'pwn_count': breach.get('PwnCount'),
                            'data_classes': breach.get('DataClasses', []),
                            'is_verified': breach.get('IsVerified'),
                            'is_sensitive': breach.get('IsSensitive')
                        }
                        breaches.append(breach_info)
            
            # Agregar información adicional sin usar APIs pagadas
            # Hash del email para búsquedas anónimas
            email_hash = hashlib.sha1(email.encode()).hexdigest()
            
            # Nota: Aquí se podrían agregar más fuentes gratuitas de brechas
            
        except Exception as e:
            logger.error(f"Error verificando brechas: {e}")
            
        return breaches
    
    async def _search_social_profiles(self, email: str) -> List[Dict[str, Any]]:
        """Buscar perfiles sociales asociados al email"""
        profiles = []
        
        try:
            # Generar gravatar URL
            email_hash = hashlib.md5(email.lower().encode()).hexdigest()
            gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
            
            profiles.append({
                'platform': 'Gravatar',
                'url': gravatar_url,
                'confidence': 'medium'
            })
            
            # Patrones de URLs de perfiles sociales comunes
            # Nota: En producción, esto se haría con APIs específicas
            social_patterns = {
                'GitHub': f"https://github.com/search?q={email}",
                'LinkedIn': f"https://www.linkedin.com/search/results/all/?keywords={email}",
                'Twitter': f"https://twitter.com/search?q={email}"
            }
            
            for platform, search_url in social_patterns.items():
                profiles.append({
                    'platform': platform,
                    'search_url': search_url,
                    'confidence': 'low',
                    'note': 'Requiere búsqueda manual'
                })
                
        except Exception as e:
            logger.error(f"Error buscando perfiles sociales: {e}")
            
        return profiles
    
    async def _check_domain_reputation(self, domain: str) -> Dict[str, Any]:
        """Verificar la reputación del dominio del email"""
        reputation = {
            'domain': domain,
            'age': None,
            'is_suspicious': False,
            'spam_lists': [],
            'security_issues': []
        }
        
        try:
            # Lista de dominios sospechosos conocidos
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf']
            suspicious_patterns = ['temp', 'throw', 'fake', 'spam']
            
            # Verificar TLD sospechoso
            for tld in suspicious_tlds:
                if domain.endswith(tld):
                    reputation['is_suspicious'] = True
                    reputation['security_issues'].append(f'TLD sospechoso: {tld}')
            
            # Verificar patrones sospechosos
            for pattern in suspicious_patterns:
                if pattern in domain.lower():
                    reputation['is_suspicious'] = True
                    reputation['security_issues'].append(f'Patrón sospechoso: {pattern}')
            
            # Verificar longitud del dominio (dominios muy largos son sospechosos)
            if len(domain) > 30:
                reputation['security_issues'].append('Dominio inusualmente largo')
                
        except Exception as e:
            logger.error(f"Error verificando reputación del dominio: {e}")
            
        return reputation
    
    async def _search_paste_sites(self, email: str) -> List[Dict[str, Any]]:
        """Buscar el email en sitios de paste (pastebin, etc)"""
        pastes = []
        
        try:
            # Nota: En producción se usarían APIs específicas
            # Por ahora, solo generamos URLs de búsqueda
            paste_sites = {
                'Pastebin': f"https://www.google.com/search?q=site:pastebin.com+{email}",
                'GitHub Gists': f"https://gist.github.com/search?q={email}",
                'Paste.ee': f"https://www.google.com/search?q=site:paste.ee+{email}"
            }
            
            for site, search_url in paste_sites.items():
                pastes.append({
                    'site': site,
                    'search_url': search_url,
                    'note': 'Requiere búsqueda manual'
                })
                
        except Exception as e:
            logger.error(f"Error buscando en paste sites: {e}")
            
        return pastes
    
    async def _generate_email_variations(self, email: str) -> List[str]:
        """Generar variaciones comunes del email"""
        variations = []
        
        try:
            local_part, domain = email.split('@')
            
            # Patrones comunes de variación
            patterns = [
                f"{local_part}@gmail.com",
                f"{local_part}@yahoo.com",
                f"{local_part}@hotmail.com",
                f"{local_part}@outlook.com",
                f"{local_part}@protonmail.com"
            ]
            
            # Si tiene puntos, probar sin ellos (común en Gmail)
            if '.' in local_part and domain == 'gmail.com':
                no_dots = local_part.replace('.', '')
                patterns.append(f"{no_dots}@gmail.com")
            
            # Agregar números comunes
            for i in range(1, 4):
                patterns.append(f"{local_part}{i}@{domain}")
                patterns.append(f"{local_part}_{i}@{domain}")
            
            # Filtrar variaciones diferentes al email original
            variations = [v for v in patterns if v != email and '@' in v]
            
        except Exception as e:
            logger.error(f"Error generando variaciones: {e}")
            
        return variations
    
    def _assess_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluar el nivel de riesgo basado en los resultados"""
        risk_score = 0
        risk_factors = []
        
        # Verificación del email
        if results.get('verification'):
            if not results['verification'].get('domain_exists'):
                risk_score += 30
                risk_factors.append('Dominio no existe')
            if not results['verification'].get('mx_records'):
                risk_score += 20
                risk_factors.append('Sin registros MX')
            if results['verification'].get('disposable'):
                risk_score += 40
                risk_factors.append('Email desechable')
            if results['verification'].get('role_based'):
                risk_score += 10
                risk_factors.append('Email basado en rol')
        
        # Brechas de datos
        if results.get('breaches'):
            breach_count = len(results['breaches'])
            if breach_count > 0:
                risk_score += min(breach_count * 15, 50)
                risk_factors.append(f'{breach_count} brechas de datos')
        
        # Reputación del dominio
        if results.get('domain_reputation'):
            if results['domain_reputation'].get('is_suspicious'):
                risk_score += 25
                risk_factors.append('Dominio sospechoso')
        
        # Determinar nivel de riesgo
        if risk_score >= 70:
            risk_level = 'ALTO'
        elif risk_score >= 40:
            risk_level = 'MEDIO'
        else:
            risk_level = 'BAJO'
        
        return {
            'score': min(risk_score, 100),
            'level': risk_level,
            'factors': risk_factors
        }