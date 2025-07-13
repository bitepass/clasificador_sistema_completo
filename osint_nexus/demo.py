#!/usr/bin/env python3
"""
Script de demostración para OSINT-Nexus
Muestra las capacidades básicas del sistema sin interfaz web
"""

import sys
import os
from datetime import datetime
import json

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos del proyecto
from modules.domain_analyzer import DomainAnalyzer
from modules.email_analyzer import EmailAnalyzer
from modules.username_analyzer import UsernameAnalyzer
from modules.social_analyzer import SocialAnalyzer
from utils.validators import validate_domain, validate_email, validate_username, detect_input_type
from utils.report_generator import ReportGenerator

def print_banner():
    """Muestra el banner de demostración"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         🔍 OSINT-NEXUS DEMO 🔍                              ║
║                                                                              ║
║                   Demostración de Capacidades del Sistema                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def demo_domain_analysis():
    """Demuestra el análisis de dominios"""
    print("\n" + "="*80)
    print("🌐 DEMO: ANÁLISIS DE DOMINIO")
    print("="*80)
    
    # Ejemplo con un dominio público
    domain = "example.com"
    print(f"Analizando dominio: {domain}")
    
    try:
        analyzer = DomainAnalyzer()
        results = analyzer.analyze_domain(domain)
        
        print("\n📊 Resultados del análisis:")
        print(f"  • Dominio: {results.get('domain', 'N/A')}")
        print(f"  • Estado: {'✅ Activo' if results.get('basic_info', {}).get('is_active') else '❌ Inactivo'}")
        print(f"  • IP: {results.get('basic_info', {}).get('ip_address', 'N/A')}")
        print(f"  • Subdominios encontrados: {len(results.get('subdomains', []))}")
        
        # Información WHOIS
        whois_info = results.get('whois_info', {})
        if 'error' not in whois_info:
            print(f"  • Registrador: {whois_info.get('registrar', 'N/A')}")
            print(f"  • Fecha de creación: {whois_info.get('creation_date', 'N/A')}")
        
        # Información de geolocalización
        geo_info = results.get('geolocation', {})
        if 'error' not in geo_info:
            print(f"  • País: {geo_info.get('country', 'N/A')}")
            print(f"  • ISP: {geo_info.get('isp', 'N/A')}")
        
        # Análisis de seguridad
        security_info = results.get('security_headers', {})
        if 'error' not in security_info:
            print(f"  • Rating de seguridad: {security_info.get('rating', 'N/A')}")
            print(f"  • Puntuación: {security_info.get('security_score', 0)}/{security_info.get('max_score', 6)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error en análisis de dominio: {e}")
        return None

def demo_email_analysis():
    """Demuestra el análisis de emails"""
    print("\n" + "="*80)
    print("📧 DEMO: ANÁLISIS DE EMAIL")
    print("="*80)
    
    # Ejemplo con un email público
    email = "test@example.com"
    print(f"Analizando email: {email}")
    
    try:
        analyzer = EmailAnalyzer()
        results = analyzer.analyze_email(email)
        
        print("\n📊 Resultados del análisis:")
        print(f"  • Email: {results.get('email', 'N/A')}")
        
        # Validación
        validation = results.get('validation', {})
        print(f"  • Formato válido: {'✅ Sí' if validation.get('format_valid') else '❌ No'}")
        print(f"  • Dominio existe: {'✅ Sí' if validation.get('domain_exists') else '❌ No'}")
        print(f"  • Cuenta de rol: {'✅ Sí' if validation.get('role_account') else '❌ No'}")
        
        # Información del proveedor
        domain_info = results.get('domain_info', {})
        if 'error' not in domain_info:
            print(f"  • Dominio: {domain_info.get('domain', 'N/A')}")
            print(f"  • Tipo de proveedor: {domain_info.get('provider_type', 'N/A')}")
            print(f"  • Proveedor popular: {'✅ Sí' if domain_info.get('is_popular_provider') else '❌ No'}")
        
        # Análisis de brechas (sin API real)
        breaches = results.get('breaches', {})
        if 'error' not in breaches:
            print(f"  • Brechas encontradas: {breaches.get('breach_count', 0)}")
        else:
            print(f"  • Brechas: {breaches.get('error', 'No se pudo verificar')}")
        
        # Análisis de reputación
        reputation = results.get('reputation', {})
        if 'error' not in reputation:
            print(f"  • Puntuación de confianza: {reputation.get('trust_score', 0)}/100")
            print(f"  • Puntuación de spam: {reputation.get('spam_score', 0)}/100")
        
        return results
        
    except Exception as e:
        print(f"❌ Error en análisis de email: {e}")
        return None

def demo_username_analysis():
    """Demuestra el análisis de usernames"""
    print("\n" + "="*80)
    print("👤 DEMO: ANÁLISIS DE USERNAME")
    print("="*80)
    
    # Ejemplo con un username común
    username = "johndoe"
    print(f"Analizando username: {username}")
    
    try:
        analyzer = UsernameAnalyzer()
        results = analyzer.analyze_username(username)
        
        print("\n📊 Resultados del análisis:")
        print(f"  • Username: {results.get('username', 'N/A')}")
        
        # Estadísticas
        stats = results.get('statistics', {})
        print(f"  • Plataformas verificadas: {stats.get('total_platforms_checked', 0)}")
        print(f"  • Encontrado en: {stats.get('platforms_found', 0)}")
        print(f"  • Disponible en: {stats.get('platforms_not_found', 0)}")
        print(f"  • Porcentaje de presencia: {stats.get('presence_percentage', 0):.1f}%")
        
        # Análisis de patrones
        patterns = results.get('patterns', {})
        print(f"  • Longitud: {patterns.get('length', 0)} caracteres")
        print(f"  • Tipo de patrón: {patterns.get('pattern_type', 'N/A')}")
        print(f"  • Contiene números: {'✅ Sí' if patterns.get('has_numbers') else '❌ No'}")
        print(f"  • Contiene símbolos: {'✅ Sí' if patterns.get('has_special_chars') else '❌ No'}")
        
        # Análisis de seguridad
        security = results.get('security_analysis', {})
        print(f"  • Puntuación de seguridad: {security.get('security_score', 0)}/100")
        print(f"  • Es seguro: {'✅ Sí' if security.get('is_secure') else '❌ No'}")
        
        # Plataformas encontradas
        platform_results = results.get('platform_results', [])
        found_platforms = [r for r in platform_results if r.get('exists')]
        
        if found_platforms:
            print(f"\n  📱 Plataformas donde se encontró (primeras 5):")
            for platform in found_platforms[:5]:
                print(f"    • {platform.get('platform', 'N/A')}: {platform.get('url', 'N/A')}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error en análisis de username: {e}")
        return None

def demo_social_analysis():
    """Demuestra el análisis de redes sociales"""
    print("\n" + "="*80)
    print("📱 DEMO: ANÁLISIS DE REDES SOCIALES")
    print("="*80)
    
    # Ejemplo con una URL pública
    url = "https://github.com/octocat"
    print(f"Analizando perfil: {url}")
    
    try:
        analyzer = SocialAnalyzer()
        results = analyzer.analyze_profile(url)
        
        print("\n📊 Resultados del análisis:")
        print(f"  • URL: {results.get('profile_url', 'N/A')}")
        print(f"  • Plataforma: {results.get('platform', 'N/A')}")
        
        # Información básica
        basic_info = results.get('basic_info', {})
        print(f"  • Accesible: {'✅ Sí' if basic_info.get('accessible') else '❌ No'}")
        print(f"  • Código de estado: {basic_info.get('status_code', 'N/A')}")
        
        # Análisis de la plataforma
        platform_analysis = results.get('platform_analysis', {})
        if 'error' not in platform_analysis:
            print(f"  • Nombre: {platform_analysis.get('name', 'N/A')}")
            print(f"  • Username: {platform_analysis.get('username', 'N/A')}")
            print(f"  • Verificado: {'✅ Sí' if platform_analysis.get('verified') else '❌ No'}")
            print(f"  • Ubicación: {platform_analysis.get('location', 'N/A')}")
        
        # Análisis de contenido
        content_analysis = results.get('content_analysis', {})
        if 'error' not in content_analysis:
            hashtags = content_analysis.get('hashtags', [])
            mentions = content_analysis.get('mentions', [])
            links = content_analysis.get('links', [])
            
            print(f"  • Hashtags encontrados: {len(hashtags)}")
            print(f"  • Menciones encontradas: {len(mentions)}")
            print(f"  • Enlaces encontrados: {len(links)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error en análisis de redes sociales: {e}")
        return None

def demo_input_validation():
    """Demuestra la validación de entrada"""
    print("\n" + "="*80)
    print("🔍 DEMO: VALIDACIÓN DE ENTRADA")
    print("="*80)
    
    test_inputs = [
        "example.com",
        "user@example.com",
        "johndoe",
        "https://github.com/octocat",
        "192.168.1.1",
        "+1234567890",
        "invalid_input_123"
    ]
    
    print("Detectando tipos de entrada automáticamente:")
    for test_input in test_inputs:
        detected_type = detect_input_type(test_input)
        print(f"  • '{test_input}' -> Tipo: {detected_type}")
        
        # Validación específica
        if detected_type == 'domain':
            valid = validate_domain(test_input)
            print(f"    Validación: {'✅ Válido' if valid else '❌ Inválido'}")
        elif detected_type == 'email':
            valid = validate_email(test_input)
            print(f"    Validación: {'✅ Válido' if valid else '❌ Inválido'}")
        elif detected_type == 'username':
            valid = validate_username(test_input)
            print(f"    Validación: {'✅ Válido' if valid else '❌ Inválido'}")

def demo_report_generation(results_dict):
    """Demuestra la generación de reportes"""
    print("\n" + "="*80)
    print("📄 DEMO: GENERACIÓN DE REPORTES")
    print("="*80)
    
    if not results_dict:
        print("❌ No hay resultados para generar reportes")
        return
    
    # Usar el primer resultado disponible
    investigation_type = list(results_dict.keys())[0]
    results = results_dict[investigation_type]
    
    print(f"Generando reportes para: {investigation_type}")
    
    try:
        generator = ReportGenerator(results, investigation_type)
        
        # Generar reportes en diferentes formatos
        print("\n📊 Generando reportes:")
        
        # JSON
        json_report = generator.generate_json_report()
        print(f"  • JSON: {len(json_report)} caracteres")
        
        # CSV
        csv_report = generator.generate_csv_report()
        print(f"  • CSV: {len(csv_report.splitlines())} líneas")
        
        # HTML
        html_report = generator.generate_html_report()
        print(f"  • HTML: {len(html_report)} caracteres")
        
        # XML
        xml_report = generator.generate_xml_report()
        print(f"  • XML: {len(xml_report)} caracteres")
        
        # Guardar ejemplo de reporte JSON
        try:
            json_path = generator.save_report('json')
            print(f"  • Reporte JSON guardado en: {json_path}")
        except Exception as e:
            print(f"  ❌ Error guardando reporte JSON: {e}")
        
        print("\n✅ Reportes generados exitosamente")
        
    except Exception as e:
        print(f"❌ Error generando reportes: {e}")

def main():
    """Función principal del demo"""
    print_banner()
    
    print("\n🚀 Iniciando demostración de OSINT-Nexus...")
    print("Este demo muestra las capacidades básicas del sistema sin APIs externas.")
    
    # Almacenar resultados para el demo de reportes
    results_dict = {}
    
    # 1. Demostrar validación de entrada
    demo_input_validation()
    
    # 2. Demostrar análisis de dominio
    domain_results = demo_domain_analysis()
    if domain_results:
        results_dict['domain'] = domain_results
    
    # 3. Demostrar análisis de email
    email_results = demo_email_analysis()
    if email_results:
        results_dict['email'] = email_results
    
    # 4. Demostrar análisis de username
    username_results = demo_username_analysis()
    if username_results:
        results_dict['username'] = username_results
    
    # 5. Demostrar análisis de redes sociales
    social_results = demo_social_analysis()
    if social_results:
        results_dict['url'] = social_results
    
    # 6. Demostrar generación de reportes
    demo_report_generation(results_dict)
    
    # Resumen final
    print("\n" + "="*80)
    print("🎉 DEMO COMPLETADO")
    print("="*80)
    print("La demostración ha finalizado exitosamente.")
    print("\nPara usar la interfaz web completa:")
    print("  1. Configure sus claves de API en el archivo .env")
    print("  2. Ejecute: streamlit run app.py")
    print("  3. Abra su navegador en: http://localhost:8501")
    print("\nPara más información, consulte README.md")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Demo cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el demo: {e}")
        import traceback
        traceback.print_exc()