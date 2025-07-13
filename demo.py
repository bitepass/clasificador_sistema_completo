#!/usr/bin/env python3
"""
OSINT-Nexus Demo Script
Script de demostración para mostrar las capacidades de OSINT-Nexus
"""

import json
import time
from datetime import datetime
from modules.domain_analyzer import DomainAnalyzer
from modules.email_analyzer import EmailAnalyzer
from modules.username_analyzer import UsernameAnalyzer
from modules.social_analyzer import SocialAnalyzer
from utils.data_processor import DataProcessor
from utils.network_graph import NetworkGraphGenerator
from utils.report_generator import ReportGenerator

def print_banner():
    """Imprime el banner de la aplicación"""
    print("""
🕵️ OSINT-Nexus - Demo Script
============================
Plataforma de Inteligencia Automatizada v1.0.0
    """)

def demo_domain_analysis():
    """Demuestra el análisis de dominio"""
    print("\n🔍 DEMO: Análisis de Dominio")
    print("=" * 40)
    
    # Crear analizador
    analyzer = DomainAnalyzer()
    
    # Dominio de ejemplo (usar un dominio real para pruebas)
    domain = "example.com"
    print(f"Analizando dominio: {domain}")
    
    # Ejecutar análisis
    start_time = time.time()
    results = analyzer.analyze_domain(domain)
    duration = time.time() - start_time
    
    # Procesar resultados
    processor = DataProcessor()
    processed_results = processor.process_domain_data(results)
    
    # Mostrar resumen
    summary = analyzer.get_summary()
    print(f"\n📊 Resumen del Análisis:")
    print(f"   • Subdominios encontrados: {summary['total_subdomains']}")
    print(f"   • IPs descubiertas: {summary['total_ips']}")
    print(f"   • Tecnologías detectadas: {summary['total_technologies']}")
    print(f"   • Vulnerabilidades: {summary['total_vulnerabilities']}")
    print(f"   • Duración: {duration:.2f} segundos")
    print(f"   • Herramientas utilizadas: {', '.join(summary['tools_used'])}")
    
    return processed_results

def demo_email_analysis():
    """Demuestra el análisis de email"""
    print("\n📧 DEMO: Análisis de Email")
    print("=" * 40)
    
    # Crear analizador
    analyzer = EmailAnalyzer()
    
    # Email de ejemplo
    email = "test@example.com"
    print(f"Analizando email: {email}")
    
    # Ejecutar análisis
    start_time = time.time()
    results = analyzer.analyze_email(email)
    duration = time.time() - start_time
    
    # Procesar resultados
    processor = DataProcessor()
    processed_results = processor.process_email_data(results)
    
    # Mostrar resumen
    summary = analyzer.get_summary()
    print(f"\n📊 Resumen del Análisis:")
    print(f"   • Email existe: {summary.get('exists', 'N/A')}")
    print(f"   • Brechas encontradas: {summary['total_breaches']}")
    print(f"   • Emails relacionados: {summary['total_related_emails']}")
    print(f"   • Perfiles sociales: {summary['total_social_profiles']}")
    print(f"   • Duración: {duration:.2f} segundos")
    print(f"   • Herramientas utilizadas: {', '.join(summary['tools_used'])}")
    
    return processed_results

def demo_username_analysis():
    """Demuestra el análisis de username"""
    print("\n👤 DEMO: Búsqueda de Usuario")
    print("=" * 40)
    
    # Crear analizador
    analyzer = UsernameAnalyzer()
    
    # Username de ejemplo
    username = "testuser123"
    print(f"Buscando usuario: {username}")
    
    # Ejecutar análisis
    start_time = time.time()
    results = analyzer.analyze_username(username)
    duration = time.time() - start_time
    
    # Procesar resultados
    processor = DataProcessor()
    processed_results = processor.process_username_data(results)
    
    # Mostrar resumen
    summary = analyzer.get_summary()
    print(f"\n📊 Resumen del Análisis:")
    print(f"   • Plataformas verificadas: {summary['total_platforms_checked']}")
    print(f"   • Perfiles encontrados: {summary['total_profiles_found']}")
    print(f"   • Tasa de éxito: {summary['success_rate']*100:.1f}%")
    print(f"   • Duración: {duration:.2f} segundos")
    print(f"   • Plataformas con perfiles: {len(summary['platforms_with_profiles'])}")
    
    return processed_results

def demo_social_analysis():
    """Demuestra el análisis social"""
    print("\n🌐 DEMO: Análisis de Red Social")
    print("=" * 40)
    
    # Crear analizador
    analyzer = SocialAnalyzer()
    
    # URL de perfil de ejemplo
    profile_url = "https://twitter.com/testuser"
    print(f"Analizando perfil: {profile_url}")
    
    # Ejecutar análisis
    start_time = time.time()
    results = analyzer.analyze_social_profile(profile_url)
    duration = time.time() - start_time
    
    # Procesar resultados
    processor = DataProcessor()
    processed_results = processor.process_social_data(results)
    
    # Mostrar resumen
    summary = analyzer.get_summary()
    print(f"\n📊 Resumen del Análisis:")
    print(f"   • Plataforma: {summary.get('platform', 'N/A')}")
    print(f"   • Usuario: {summary.get('username', 'N/A')}")
    print(f"   • Posts analizados: {summary['total_posts']}")
    print(f"   • Conexiones: {summary['total_connections']}")
    print(f"   • Duración: {duration:.2f} segundos")
    print(f"   • Herramientas utilizadas: {', '.join(summary['tools_used'])}")
    
    return processed_results

def demo_network_graph():
    """Demuestra la generación de grafos de red"""
    print("\n🕸️ DEMO: Generación de Grafo de Red")
    print("=" * 40)
    
    # Crear generador de grafos
    graph_generator = NetworkGraphGenerator()
    
    # Añadir datos de ejemplo
    sample_domain_data = {
        "domain_info": {"domain": "example.com"},
        "subdomains": [
            {"name": "www.example.com", "ip": "192.168.1.1"},
            {"name": "mail.example.com", "ip": "192.168.1.2"}
        ],
        "ip_addresses": [
            {"value": "192.168.1.1", "type": "A"},
            {"value": "192.168.1.2", "type": "A"}
        ],
        "technologies": [
            {"name": "Apache", "version": "2.4"},
            {"name": "PHP", "version": "7.4"}
        ]
    }
    
    graph_generator.add_domain_data(sample_domain_data)
    
    # Generar estadísticas
    stats = graph_generator.generate_statistics()
    print(f"\n📊 Estadísticas del Grafo:")
    print(f"   • Nodos totales: {stats['total_nodes']}")
    print(f"   • Conexiones: {stats['total_edges']}")
    print(f"   • Densidad: {stats['density']:.3f}")
    print(f"   • Componentes conectados: {stats['connected_components']}")
    
    # Mostrar nodos centrales
    central_nodes = graph_generator.get_central_nodes(5)
    if central_nodes:
        print(f"\n🎯 Nodos más centrales:")
        for node, centrality in central_nodes:
            print(f"   • {node}: {centrality:.3f}")
    
    return graph_generator

def demo_report_generation():
    """Demuestra la generación de reportes"""
    print("\n📄 DEMO: Generación de Reporte PDF")
    print("=" * 40)
    
    # Crear generador de reportes
    report_generator = ReportGenerator()
    
    # Datos de ejemplo para el reporte
    sample_data = {
        "analysis_type": "domain",
        "target": "example.com",
        "statistics": {
            "total_subdomains": 5,
            "total_ips": 3,
            "total_technologies": 8,
            "total_vulnerabilities": 2
        },
        "metadata": {
            "scan_time": 15.5,
            "tools_used": ["shodan", "whois", "dns"],
            "errors": []
        }
    }
    
    # Generar reporte
    print("Generando reporte PDF...")
    report_path = report_generator.generate_report(sample_data, "demo_report.pdf")
    
    if report_path:
        print(f"✅ Reporte generado: {report_path}")
    else:
        print("❌ Error generando el reporte")
    
    return report_path

def demo_data_correlation():
    """Demuestra la correlación de datos"""
    print("\n🔗 DEMO: Correlación de Datos")
    print("=" * 40)
    
    # Crear procesador de datos
    processor = DataProcessor()
    
    # Datos de ejemplo de múltiples fuentes
    sample_data_sources = [
        {
            "domain_info": {"domain": "example.com"},
            "ip_addresses": [{"ip": "192.168.1.1"}],
            "technologies": [{"name": "Apache"}]
        },
        {
            "email_info": {"email": "admin@example.com", "domain": "example.com"},
            "breaches": [{"name": "Test Breach", "pwn_count": 1000}]
        }
    ]
    
    # Correlacionar datos
    correlations = processor.correlate_data(sample_data_sources)
    
    print(f"\n📊 Resultados de Correlación:")
    print(f"   • Entidades únicas: {sum(len(entities) for entities in correlations['entities'].values())}")
    print(f"   • Relaciones encontradas: {len(correlations['relationships'])}")
    print(f"   • Patrones identificados: {len(correlations['patterns'])}")
    print(f"   • Insights generados: {len(correlations['insights'])}")
    
    # Mostrar insights
    if correlations['insights']:
        print(f"\n💡 Insights:")
        for insight in correlations['insights']:
            print(f"   • {insight}")
    
    return correlations

def main():
    """Función principal del demo"""
    print_banner()
    
    print("Este script demuestra las capacidades principales de OSINT-Nexus.")
    print("⚠️ Nota: Este es un demo con datos de ejemplo. Para análisis reales,")
    print("   configura las claves API en el archivo .env")
    print()
    
    try:
        # Ejecutar demos
        domain_results = demo_domain_analysis()
        email_results = demo_email_analysis()
        username_results = demo_username_analysis()
        social_results = demo_social_analysis()
        
        # Demos avanzados
        graph_generator = demo_network_graph()
        report_path = demo_report_generation()
        correlations = demo_data_correlation()
        
        print("\n🎉 ¡Demo completado exitosamente!")
        print("\n📋 Resumen de funcionalidades demostradas:")
        print("   ✅ Análisis de dominios")
        print("   ✅ Análisis de emails")
        print("   ✅ Búsqueda de usuarios")
        print("   ✅ Análisis de redes sociales")
        print("   ✅ Generación de grafos de red")
        print("   ✅ Generación de reportes PDF")
        print("   ✅ Correlación de datos")
        
        print(f"\n📁 Archivos generados:")
        if report_path:
            print(f"   • Reporte PDF: {report_path}")
        
        print("\n🚀 Para usar OSINT-Nexus con datos reales:")
        print("   1. Configura las claves API en .env")
        print("   2. Ejecuta: streamlit run app.py")
        print("   3. Accede a la interfaz web en http://localhost:8501")
        
    except Exception as e:
        print(f"\n❌ Error durante el demo: {str(e)}")
        print("Esto puede deberse a dependencias faltantes o configuración incorrecta.")
        print("Verifica que todas las dependencias estén instaladas.")

if __name__ == "__main__":
    main()