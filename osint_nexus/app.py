"""
Interfaz principal de OSINT-Nexus
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import time
import asyncio
import sys
import os

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos del proyecto
from config import *
from utils.validators import *
from utils.logger import setup_logger
from modules.domain_analyzer import DomainAnalyzer
from modules.email_analyzer import EmailAnalyzer
from modules.username_analyzer import UsernameAnalyzer
from modules.social_analyzer import SocialAnalyzer

# Configurar logging
logger = setup_logger("osint_nexus_app")

# Configuración de la página
st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    page_icon=STREAMLIT_CONFIG["page_icon"],
    layout=STREAMLIT_CONFIG["layout"],
    initial_sidebar_state=STREAMLIT_CONFIG["initial_sidebar_state"]
)

class OSINTNexusApp:
    """Aplicación principal de OSINT-Nexus"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.setup_session_state()
        self.setup_api_keys()
        self.analyzer_instances = {}
    
    def setup_session_state(self):
        """Configura el estado de la sesión"""
        if 'investigation_history' not in st.session_state:
            st.session_state.investigation_history = []
        
        if 'current_results' not in st.session_state:
            st.session_state.current_results = {}
        
        if 'api_keys_configured' not in st.session_state:
            st.session_state.api_keys_configured = False
        
        if 'ethical_agreement' not in st.session_state:
            st.session_state.ethical_agreement = False
    
    def setup_api_keys(self):
        """Configura las claves de API desde variables de entorno o entrada del usuario"""
        if not st.session_state.api_keys_configured:
            self.api_keys = {}
            
            # Intentar cargar desde variables de entorno
            for key, value in API_KEYS.items():
                if value:
                    self.api_keys[key] = value
                else:
                    self.api_keys[key] = ""
            
            st.session_state.api_keys_configured = True
        else:
            self.api_keys = getattr(st.session_state, 'api_keys', {})
    
    def show_ethical_notice(self):
        """Muestra el aviso ético y legal"""
        if not st.session_state.ethical_agreement:
            st.error("⚠️ AVISO ÉTICO Y LEGAL REQUERIDO")
            
            with st.expander("📋 Leer y Aceptar Términos de Uso", expanded=True):
                st.markdown(ETHICAL_NOTICE)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Acepto los términos", type="primary"):
                        st.session_state.ethical_agreement = True
                        st.rerun()
                
                with col2:
                    if st.button("❌ No acepto"):
                        st.error("Debe aceptar los términos para continuar")
                        st.stop()
            
            st.stop()
    
    def show_sidebar(self):
        """Muestra la barra lateral con configuración"""
        st.sidebar.markdown("## 🔧 Configuración")
        
        # Configuración de APIs
        with st.sidebar.expander("🔑 Claves de API"):
            st.markdown("**Configure sus claves de API para análisis avanzado:**")
            
            self.api_keys['SHODAN_API_KEY'] = st.text_input(
                "Shodan API Key", 
                value=self.api_keys.get('SHODAN_API_KEY', ''),
                type="password"
            )
            
            self.api_keys['HUNTER_API_KEY'] = st.text_input(
                "Hunter.io API Key", 
                value=self.api_keys.get('HUNTER_API_KEY', ''),
                type="password"
            )
            
            self.api_keys['HIBP_API_KEY'] = st.text_input(
                "Have I Been Pwned API Key", 
                value=self.api_keys.get('HIBP_API_KEY', ''),
                type="password"
            )
            
            self.api_keys['VIRUSTOTAL_API_KEY'] = st.text_input(
                "VirusTotal API Key", 
                value=self.api_keys.get('VIRUSTOTAL_API_KEY', ''),
                type="password"
            )
            
            self.api_keys['URLSCAN_API_KEY'] = st.text_input(
                "URLScan.io API Key", 
                value=self.api_keys.get('URLSCAN_API_KEY', ''),
                type="password"
            )
            
            st.session_state.api_keys = self.api_keys
        
        # Configuración de proxy
        with st.sidebar.expander("🌐 Configuración de Proxy"):
            use_proxy = st.checkbox("Usar Proxy", value=PROXY_CONFIG.get('enabled', False))
            
            if use_proxy:
                proxy_http = st.text_input("HTTP Proxy", value=PROXY_CONFIG.get('http_proxy', ''))
                proxy_https = st.text_input("HTTPS Proxy", value=PROXY_CONFIG.get('https_proxy', ''))
                
                PROXY_CONFIG['enabled'] = use_proxy
                PROXY_CONFIG['http_proxy'] = proxy_http
                PROXY_CONFIG['https_proxy'] = proxy_https
        
        # Historial de investigaciones
        st.sidebar.markdown("## 📊 Historial")
        
        if st.session_state.investigation_history:
            st.sidebar.markdown(f"**Investigaciones realizadas:** {len(st.session_state.investigation_history)}")
            
            if st.sidebar.button("🗑️ Limpiar historial"):
                st.session_state.investigation_history = []
                st.rerun()
        else:
            st.sidebar.markdown("*No hay investigaciones previas*")
    
    def show_main_interface(self):
        """Muestra la interfaz principal"""
        # Header
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1>🔍 OSINT-Nexus</h1>
            <h3>Plataforma de Inteligencia Automatizada</h3>
            <p><i>Versión {}</i></p>
        </div>
        """.format(APP_VERSION), unsafe_allow_html=True)
        
        # Barra de búsqueda principal
        st.markdown("### 🎯 Iniciar Investigación")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            target_input = st.text_input(
                "Ingrese el objetivo de la investigación:",
                placeholder="ejemplo.com, usuario@email.com, nombreusuario, https://twitter.com/usuario",
                help="Ingrese un dominio, email, nombre de usuario o URL de perfil social"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🔍 Investigar", type="primary", disabled=not target_input):
                self.perform_investigation(target_input)
        
        # Detector automático de tipo
        if target_input:
            detected_type = detect_input_type(target_input)
            
            if detected_type != 'unknown':
                st.success(f"✅ Tipo detectado: **{detected_type.upper()}**")
                
                # Mostrar información sobre el tipo de análisis
                type_info = {
                    'domain': "Se realizará análisis de infraestructura, DNS, SSL, tecnologías y seguridad",
                    'email': "Se verificará la validez, brechas de datos, perfiles sociales y reputación",
                    'username': "Se buscará en múltiples plataformas de redes sociales",
                    'url': "Se analizará el perfil de la red social especificada",
                    'ip': "Se realizará análisis de infraestructura y geolocalización",
                    'phone': "Se verificará la validez y se buscará información asociada"
                }
                
                if detected_type in type_info:
                    st.info(f"📋 {type_info[detected_type]}")
            else:
                st.warning("⚠️ No se pudo detectar el tipo de objetivo. Verifique el formato.")
        
        # Selector manual de módulo
        st.markdown("### 🎛️ Selección Manual de Módulo")
        
        selected_module = st.selectbox(
            "Seleccione el módulo a utilizar:",
            options=["Auto-detectar"] + list(MODULES.keys()),
            format_func=lambda x: "🤖 Auto-detectar" if x == "Auto-detectar" else f"{MODULES[x]['icon']} {MODULES[x]['name']}",
            help="Seleccione manualmente el módulo si la detección automática no es correcta"
        )
        
        if selected_module != "Auto-detectar":
            st.info(f"📝 {MODULES[selected_module]['description']}")
        
        # Opciones avanzadas
        with st.expander("⚙️ Opciones Avanzadas"):
            col1, col2 = st.columns(2)
            
            with col1:
                deep_analysis = st.checkbox("Análisis profundo", value=True, help="Realizar análisis más detallado (puede tomar más tiempo)")
                concurrent_requests = st.checkbox("Solicitudes concurrentes", value=True, help="Realizar múltiples solicitudes en paralelo")
            
            with col2:
                include_variants = st.checkbox("Incluir variantes", value=True, help="Buscar variantes del objetivo (usernames, subdominios, etc.)")
                save_results = st.checkbox("Guardar resultados", value=True, help="Guardar resultados en el historial")
    
    def perform_investigation(self, target: str):
        """Realiza la investigación del objetivo"""
        if not target:
            return
        
        # Sanitizar entrada
        target = sanitize_input(target)
        
        # Detectar tipo
        input_type = detect_input_type(target)
        
        if input_type == 'unknown':
            st.error("❌ No se pudo determinar el tipo de objetivo")
            return
        
        # Mostrar progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Inicializar el analizador apropiado
            analyzer = self.get_analyzer(input_type)
            
            if not analyzer:
                st.error(f"❌ No hay analizador disponible para el tipo: {input_type}")
                return
            
            # Realizar análisis
            status_text.text("🔍 Iniciando análisis...")
            progress_bar.progress(10)
            
            results = self.run_analysis(analyzer, target, input_type, progress_bar, status_text)
            
            if results:
                # Guardar resultados
                st.session_state.current_results = results
                
                # Agregar al historial
                if st.session_state.get('save_results', True):
                    self.add_to_history(target, input_type, results)
                
                # Mostrar resultados
                self.display_results(results, input_type)
                
                progress_bar.progress(100)
                status_text.text("✅ Análisis completado")
            else:
                st.error("❌ No se pudieron obtener resultados")
                
        except Exception as e:
            st.error(f"❌ Error durante el análisis: {str(e)}")
            logger.error(f"Error en investigación: {e}")
        
        finally:
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
    
    def get_analyzer(self, input_type: str):
        """Obtiene el analizador apropiado para el tipo de entrada"""
        if input_type not in self.analyzer_instances:
            if input_type == 'domain' or input_type == 'ip':
                self.analyzer_instances[input_type] = DomainAnalyzer(self.api_keys)
            elif input_type == 'email':
                self.analyzer_instances[input_type] = EmailAnalyzer(self.api_keys)
            elif input_type == 'username':
                self.analyzer_instances[input_type] = UsernameAnalyzer(self.api_keys)
            elif input_type == 'url':
                self.analyzer_instances[input_type] = SocialAnalyzer(self.api_keys)
            else:
                return None
        
        return self.analyzer_instances.get(input_type)
    
    def run_analysis(self, analyzer, target, input_type, progress_bar, status_text):
        """Ejecuta el análisis específico"""
        try:
            if input_type == 'domain' or input_type == 'ip':
                status_text.text("🌐 Analizando dominio/IP...")
                progress_bar.progress(30)
                results = analyzer.analyze_domain(target)
                
            elif input_type == 'email':
                status_text.text("📧 Analizando email...")
                progress_bar.progress(30)
                results = analyzer.analyze_email(target)
                
            elif input_type == 'username':
                status_text.text("👤 Buscando username...")
                progress_bar.progress(30)
                results = analyzer.analyze_username(target)
                
            elif input_type == 'url':
                status_text.text("📱 Analizando perfil social...")
                progress_bar.progress(30)
                results = analyzer.analyze_profile(target)
            
            else:
                return None
            
            progress_bar.progress(70)
            status_text.text("📊 Procesando resultados...")
            
            return results
            
        except Exception as e:
            logger.error(f"Error en análisis {input_type}: {e}")
            return None
    
    def add_to_history(self, target, input_type, results):
        """Agrega la investigación al historial"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'target': target,
            'type': input_type,
            'results': results,
            'summary': self.generate_summary(results, input_type)
        }
        
        st.session_state.investigation_history.append(history_entry)
        
        # Mantener solo las últimas 50 investigaciones
        if len(st.session_state.investigation_history) > 50:
            st.session_state.investigation_history = st.session_state.investigation_history[-50:]
    
    def generate_summary(self, results, input_type):
        """Genera un resumen de los resultados"""
        if input_type == 'domain':
            return {
                'domain': results.get('domain', ''),
                'is_active': results.get('basic_info', {}).get('is_active', False),
                'ip_address': results.get('basic_info', {}).get('ip_address', ''),
                'subdomains_found': len(results.get('subdomains', [])),
                'security_rating': results.get('security_headers', {}).get('rating', 'Unknown')
            }
        
        elif input_type == 'email':
            return {
                'email': results.get('email', ''),
                'format_valid': results.get('validation', {}).get('format_valid', False),
                'found_in_breaches': results.get('breaches', {}).get('found_in_breaches', False),
                'breach_count': results.get('breaches', {}).get('breach_count', 0)
            }
        
        elif input_type == 'username':
            return {
                'username': results.get('username', ''),
                'platforms_found': results.get('statistics', {}).get('platforms_found', 0),
                'total_platforms': results.get('statistics', {}).get('total_platforms_checked', 0),
                'availability_score': results.get('availability', {}).get('availability_score', 0)
            }
        
        elif input_type == 'url':
            return {
                'profile_url': results.get('profile_url', ''),
                'platform': results.get('platform', ''),
                'accessible': results.get('basic_info', {}).get('accessible', False),
                'verified': results.get('platform_analysis', {}).get('verified', False)
            }
        
        return {}
    
    def display_results(self, results, input_type):
        """Muestra los resultados del análisis"""
        st.markdown("## 📊 Resultados del Análisis")
        
        if input_type == 'domain':
            self.display_domain_results(results)
        elif input_type == 'email':
            self.display_email_results(results)
        elif input_type == 'username':
            self.display_username_results(results)
        elif input_type == 'url':
            self.display_social_results(results)
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Descargar JSON"):
                self.download_json(results)
        
        with col2:
            if st.button("📄 Generar PDF"):
                self.generate_pdf_report(results, input_type)
        
        with col3:
            if st.button("🔄 Nueva Investigación"):
                st.rerun()
    
    def display_domain_results(self, results):
        """Muestra resultados del análisis de dominio"""
        # Información básica
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Estado", "✅ Activo" if results.get('basic_info', {}).get('is_active') else "❌ Inactivo")
        
        with col2:
            st.metric("IP Address", results.get('basic_info', {}).get('ip_address', 'N/A'))
        
        with col3:
            st.metric("Subdominios", len(results.get('subdomains', [])))
        
        # Información WHOIS
        if 'whois_info' in results:
            with st.expander("📋 Información WHOIS"):
                whois_info = results['whois_info']
                if 'error' not in whois_info:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Registrador:**", whois_info.get('registrar', 'N/A'))
                        st.write("**Fecha de creación:**", whois_info.get('creation_date', 'N/A'))
                    with col2:
                        st.write("**Fecha de expiración:**", whois_info.get('expiration_date', 'N/A'))
                        st.write("**País:**", whois_info.get('registrant_country', 'N/A'))
                else:
                    st.error(f"Error obteniendo WHOIS: {whois_info['error']}")
        
        # Registros DNS
        if 'dns_records' in results:
            with st.expander("🌐 Registros DNS"):
                dns_records = results['dns_records']
                for record_type, records in dns_records.items():
                    if records:
                        st.write(f"**{record_type}:**")
                        for record in records:
                            st.write(f"  • {record}")
        
        # Análisis de seguridad
        if 'security_headers' in results:
            with st.expander("🔒 Análisis de Seguridad"):
                security = results['security_headers']
                if 'error' not in security:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Rating de Seguridad", security.get('rating', 'N/A'))
                    with col2:
                        st.metric("Score", f"{security.get('security_score', 0)}/{security.get('max_score', 6)}")
                    
                    # Headers de seguridad
                    headers = security.get('headers', {})
                    for header, value in headers.items():
                        status = "✅" if value else "❌"
                        st.write(f"{status} **{header}:** {value or 'No configurado'}")
        
        # Tecnologías detectadas
        if 'technology_stack' in results:
            with st.expander("💻 Stack Tecnológico"):
                tech = results['technology_stack']
                if 'error' not in tech:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Servidor:**", tech.get('server', 'N/A'))
                        st.write("**Framework:**", tech.get('framework', 'N/A'))
                    with col2:
                        st.write("**CMS:**", tech.get('cms', 'N/A'))
                        st.write("**Estado HTTP:**", tech.get('status_code', 'N/A'))
                    
                    js_libs = tech.get('javascript_libraries', [])
                    if js_libs:
                        st.write("**Librerías JavaScript:**")
                        for lib in js_libs:
                            st.write(f"  • {lib}")
        
        # Geolocalización
        if 'geolocation' in results:
            with st.expander("📍 Geolocalización"):
                geo = results['geolocation']
                if 'error' not in geo:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**País:**", geo.get('country', 'N/A'))
                        st.write("**Ciudad:**", geo.get('city', 'N/A'))
                    with col2:
                        st.write("**ISP:**", geo.get('isp', 'N/A'))
                        st.write("**Zona horaria:**", geo.get('timezone', 'N/A'))
                    
                    # Mapa si hay coordenadas
                    if geo.get('latitude') and geo.get('longitude'):
                        try:
                            df = pd.DataFrame({
                                'lat': [geo['latitude']],
                                'lon': [geo['longitude']]
                            })
                            st.map(df)
                        except Exception:
                            pass
        
        # Puertos abiertos
        if 'ports_scan' in results:
            with st.expander("🚪 Puertos Abiertos"):
                ports = results['ports_scan']
                if 'error' not in ports:
                    open_ports = ports.get('open_ports', [])
                    if open_ports:
                        st.write("**Puertos abiertos encontrados:**")
                        for port in open_ports:
                            st.write(f"  • Puerto {port}")
                    else:
                        st.write("No se encontraron puertos abiertos en el escaneo básico")
    
    def display_email_results(self, results):
        """Muestra resultados del análisis de email"""
        # Información básica
        col1, col2, col3 = st.columns(3)
        
        with col1:
            validation = results.get('validation', {})
            st.metric("Formato", "✅ Válido" if validation.get('format_valid') else "❌ Inválido")
        
        with col2:
            st.metric("Dominio", "✅ Existe" if validation.get('domain_exists') else "❌ No existe")
        
        with col3:
            breaches = results.get('breaches', {})
            breach_count = breaches.get('breach_count', 0)
            st.metric("Brechas", breach_count, delta=f"{'🔴 Comprometido' if breach_count > 0 else '🟢 Seguro'}")
        
        # Información del proveedor
        if 'domain_info' in results:
            with st.expander("📧 Información del Proveedor"):
                domain_info = results['domain_info']
                if 'error' not in domain_info:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Dominio:**", domain_info.get('domain', 'N/A'))
                        st.write("**Tipo:**", domain_info.get('provider_type', 'N/A'))
                    with col2:
                        st.write("**Popular:**", "Sí" if domain_info.get('is_popular_provider') else "No")
                        
                        mx_records = domain_info.get('mx_records', [])
                        if mx_records:
                            st.write("**Registros MX:**")
                            for mx in mx_records:
                                st.write(f"  • {mx}")
        
        # Análisis de brechas
        if 'breaches' in results:
            with st.expander("🔓 Análisis de Brechas de Datos"):
                breaches = results['breaches']
                if 'error' not in breaches:
                    if breaches.get('found_in_breaches', False):
                        st.error(f"❌ Este email fue encontrado en {breaches.get('breach_count', 0)} brechas de datos")
                        
                        breach_list = breaches.get('breaches', [])
                        if breach_list:
                            for breach in breach_list:
                                with st.container():
                                    st.write(f"**{breach.get('name', 'N/A')}**")
                                    st.write(f"Fecha: {breach.get('breach_date', 'N/A')}")
                                    st.write(f"Afectados: {breach.get('pwn_count', 'N/A'):,}")
                                    st.write(f"Datos comprometidos: {', '.join(breach.get('compromised_data', []))}")
                                    st.write("---")
                    else:
                        st.success("✅ No se encontraron brechas de datos para este email")
                else:
                    st.warning(f"⚠️ No se pudo verificar brechas: {breaches['error']}")
        
        # Perfiles sociales
        if 'social_profiles' in results:
            with st.expander("📱 Perfiles Sociales"):
                social = results['social_profiles']
                
                # Gravatar
                gravatar = social.get('gravatar', {})
                if gravatar.get('has_gravatar'):
                    st.success("✅ Perfil de Gravatar encontrado")
                    st.write(f"**URL:** {gravatar.get('profile_url', 'N/A')}")
                else:
                    st.info("ℹ️ No se encontró perfil de Gravatar")
                
                # Nombres de usuario potenciales
                usernames = social.get('potential_usernames', [])
                if usernames:
                    st.write("**Nombres de usuario potenciales:**")
                    for username in usernames:
                        st.write(f"  • {username}")
        
        # Análisis de reputación
        if 'reputation' in results:
            with st.expander("🏆 Análisis de Reputación"):
                reputation = results['reputation']
                if 'error' not in reputation:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        trust_score = reputation.get('trust_score', 0)
                        st.metric("Puntuación de Confianza", f"{trust_score}/100")
                    
                    with col2:
                        spam_score = reputation.get('spam_score', 0)
                        st.metric("Puntuación de Spam", f"{spam_score}/100")
                    
                    # Verificación de email desechable
                    disposable = results.get('disposable_check', {})
                    if disposable.get('is_disposable'):
                        st.warning("⚠️ Este email utiliza un servicio de email desechable")
                    else:
                        st.success("✅ No es un email desechable")
    
    def display_username_results(self, results):
        """Muestra resultados del análisis de username"""
        # Estadísticas principales
        stats = results.get('statistics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Plataformas", stats.get('total_platforms_checked', 0))
        
        with col2:
            st.metric("Encontrado en", stats.get('platforms_found', 0))
        
        with col3:
            st.metric("Disponible en", stats.get('platforms_not_found', 0))
        
        with col4:
            presence = stats.get('presence_percentage', 0)
            st.metric("Presencia", f"{presence:.1f}%")
        
        # Resultados por plataforma
        platform_results = results.get('platform_results', [])
        
        if platform_results:
            # Crear DataFrame para visualización
            df_data = []
            for result in platform_results:
                df_data.append({
                    'Plataforma': result.get('platform', 'N/A'),
                    'Estado': 'Encontrado' if result.get('exists') else 'No encontrado',
                    'URL': result.get('url', 'N/A'),
                    'Última verificación': result.get('last_checked', 'N/A')
                })
            
            df = pd.DataFrame(df_data)
            
            # Mostrar tabla
            st.markdown("### 📋 Resultados por Plataforma")
            st.dataframe(df, use_container_width=True)
            
            # Gráfico de presencia
            found_count = len([r for r in platform_results if r.get('exists')])
            not_found_count = len([r for r in platform_results if not r.get('exists') and r.get('status') != 'error'])
            error_count = len([r for r in platform_results if r.get('status') == 'error'])
            
            fig = px.pie(
                values=[found_count, not_found_count, error_count],
                names=['Encontrado', 'No encontrado', 'Error'],
                title="Distribución de Resultados"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Plataformas donde se encontró
            found_platforms = [r for r in platform_results if r.get('exists')]
            if found_platforms:
                st.markdown("### ✅ Plataformas donde se encontró el usuario")
                
                for platform in found_platforms:
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**{platform.get('platform', 'N/A')}**")
                        st.write(f"URL: {platform.get('url', 'N/A')}")
                        
                        # Información adicional si está disponible
                        additional_info = platform.get('additional_info', {})
                        if additional_info:
                            for key, value in additional_info.items():
                                if value:
                                    st.write(f"{key}: {value}")
                    
                    with col2:
                        st.link_button("Ver perfil", platform.get('url', ''))
                    
                    st.write("---")
        
        # Análisis de patrones
        if 'patterns' in results:
            with st.expander("🔍 Análisis de Patrones"):
                patterns = results['patterns']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Características:**")
                    st.write(f"• Longitud: {patterns.get('length', 0)} caracteres")
                    st.write(f"• Tipo: {patterns.get('pattern_type', 'N/A')}")
                    st.write(f"• Contiene números: {'Sí' if patterns.get('has_numbers') else 'No'}")
                    st.write(f"• Contiene símbolos: {'Sí' if patterns.get('has_special_chars') else 'No'}")
                
                with col2:
                    st.write("**Análisis adicional:**")
                    st.write(f"• Alfanumérico: {'Sí' if patterns.get('is_alphanumeric') else 'No'}")
                    st.write(f"• Empieza con número: {'Sí' if patterns.get('starts_with_number') else 'No'}")
                    st.write(f"• Termina con número: {'Sí' if patterns.get('ends_with_number') else 'No'}")
                    
                    if patterns.get('contains_birth_year'):
                        st.warning("⚠️ Posible año de nacimiento detectado")
                
                # Palabras comunes encontradas
                common_words = patterns.get('contains_common_words', [])
                if common_words:
                    st.write("**Palabras comunes encontradas:**")
                    for word in common_words:
                        st.write(f"  • {word}")
        
        # Análisis de seguridad
        if 'security_analysis' in results:
            with st.expander("🔒 Análisis de Seguridad"):
                security = results['security_analysis']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    security_score = security.get('security_score', 0)
                    st.metric("Puntuación de Seguridad", f"{security_score}/100")
                    
                    is_secure = security.get('is_secure', False)
                    st.write(f"**Estado:** {'🟢 Seguro' if is_secure else '🔴 Inseguro'}")
                
                with col2:
                    issues = security.get('security_issues', [])
                    if issues:
                        st.write("**Problemas de seguridad:**")
                        for issue in issues:
                            st.write(f"  • {issue}")
                    else:
                        st.write("**No se encontraron problemas de seguridad**")
                
                # Recomendaciones
                recommendations = security.get('recommendations', [])
                if recommendations:
                    st.write("**Recomendaciones:**")
                    for rec in recommendations:
                        st.write(f"  • {rec}")
    
    def display_social_results(self, results):
        """Muestra resultados del análisis de redes sociales"""
        # Información básica
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Plataforma", results.get('platform', 'N/A'))
        
        with col2:
            basic_info = results.get('basic_info', {})
            st.metric("Accesible", "✅ Sí" if basic_info.get('accessible') else "❌ No")
        
        with col3:
            st.metric("Código de Estado", basic_info.get('status_code', 'N/A'))
        
        # Análisis de la plataforma
        if 'platform_analysis' in results:
            with st.expander("📱 Información del Perfil"):
                platform_analysis = results['platform_analysis']
                
                if 'error' not in platform_analysis:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Información básica:**")
                        st.write(f"• Nombre: {platform_analysis.get('name', 'N/A')}")
                        st.write(f"• Username: {platform_analysis.get('username', 'N/A')}")
                        st.write(f"• Verificado: {'✅ Sí' if platform_analysis.get('verified') else '❌ No'}")
                        st.write(f"• Ubicación: {platform_analysis.get('location', 'N/A')}")
                    
                    with col2:
                        st.write("**Métricas:**")
                        st.write(f"• Seguidores: {platform_analysis.get('followers_count', 'N/A')}")
                        st.write(f"• Siguiendo: {platform_analysis.get('following_count', 'N/A')}")
                        st.write(f"• Posts: {platform_analysis.get('posts_count', 'N/A')}")
                        st.write(f"• Tweets: {platform_analysis.get('tweets_count', 'N/A')}")
                    
                    # Biografía
                    bio = platform_analysis.get('bio', '')
                    if bio:
                        st.write("**Biografía:**")
                        st.write(bio)
                    
                    # Sitio web
                    website = platform_analysis.get('website', '')
                    if website:
                        st.write(f"**Sitio web:** {website}")
                else:
                    st.error(f"Error en análisis: {platform_analysis['error']}")
        
        # Análisis de contenido
        if 'content_analysis' in results:
            with st.expander("📄 Análisis de Contenido"):
                content = results['content_analysis']
                
                if 'error' not in content:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Hashtags
                        hashtags = content.get('hashtags', [])
                        if hashtags:
                            st.write("**Hashtags encontrados:**")
                            for hashtag in hashtags[:10]:  # Mostrar solo los primeros 10
                                st.write(f"  • {hashtag}")
                    
                    with col2:
                        # Menciones
                        mentions = content.get('mentions', [])
                        if mentions:
                            st.write("**Menciones encontradas:**")
                            for mention in mentions[:10]:  # Mostrar solo las primeras 10
                                st.write(f"  • {mention}")
                    
                    # Enlaces
                    links = content.get('links', [])
                    if links:
                        st.write("**Enlaces encontrados:**")
                        for link in links[:5]:  # Mostrar solo los primeros 5
                            st.write(f"  • {link}")
                    
                    # Análisis de sentimiento
                    sentiment = content.get('sentiment_analysis', {})
                    if sentiment:
                        st.write("**Análisis de sentimiento:**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Positivo", f"{sentiment.get('positive', 0):.1%}")
                        with col2:
                            st.metric("Neutral", f"{sentiment.get('neutral', 0):.1%}")
                        with col3:
                            st.metric("Negativo", f"{sentiment.get('negative', 0):.1%}")
                else:
                    st.error(f"Error en análisis de contenido: {content['error']}")
        
        # Metadatos
        if 'metadata' in results:
            with st.expander("🔍 Metadatos"):
                metadata = results['metadata']
                
                if 'error' not in metadata:
                    # OpenGraph tags
                    og_tags = metadata.get('og_tags', {})
                    if og_tags:
                        st.write("**OpenGraph Tags:**")
                        for key, value in og_tags.items():
                            st.write(f"  • {key}: {value}")
                    
                    # Twitter Cards
                    twitter_cards = metadata.get('twitter_cards', {})
                    if twitter_cards:
                        st.write("**Twitter Cards:**")
                        for key, value in twitter_cards.items():
                            st.write(f"  • {key}: {value}")
                    
                    # Meta tags
                    meta_tags = metadata.get('meta_tags', {})
                    if meta_tags:
                        st.write("**Meta Tags:**")
                        for key, value in list(meta_tags.items())[:10]:  # Mostrar solo los primeros 10
                            st.write(f"  • {key}: {value}")
                else:
                    st.error(f"Error en metadatos: {metadata['error']}")
    
    def download_json(self, results):
        """Permite descargar los resultados en formato JSON"""
        json_str = json.dumps(results, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="💾 Descargar JSON",
            data=json_str,
            file_name=f"osint_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def generate_pdf_report(self, results, input_type):
        """Genera un reporte PDF"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            import io
            
            # Crear buffer para PDF
            buffer = io.BytesIO()
            
            # Crear documento
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Crear contenido
            story = []
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.darkblue
            )
            story.append(Paragraph("OSINT-Nexus - Reporte de Investigación", title_style))
            story.append(Spacer(1, 12))
            
            # Información básica
            info_data = [
                ["Objetivo:", results.get('domain') or results.get('email') or results.get('username') or results.get('profile_url', 'N/A')],
                ["Tipo:", input_type.upper()],
                ["Fecha:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ["Generado por:", "OSINT-Nexus v" + APP_VERSION]
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # Resumen de resultados
            story.append(Paragraph("Resumen de Resultados", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Agregar contenido específico por tipo
            if input_type == 'domain':
                self.add_domain_pdf_content(story, results, styles)
            elif input_type == 'email':
                self.add_email_pdf_content(story, results, styles)
            elif input_type == 'username':
                self.add_username_pdf_content(story, results, styles)
            elif input_type == 'url':
                self.add_social_pdf_content(story, results, styles)
            
            # Construir PDF
            doc.build(story)
            
            # Preparar descarga
            buffer.seek(0)
            
            st.download_button(
                label="📄 Descargar PDF",
                data=buffer.getvalue(),
                file_name=f"osint_report_{input_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            
        except ImportError:
            st.error("❌ La librería ReportLab no está instalada. No se puede generar el PDF.")
        except Exception as e:
            st.error(f"❌ Error generando PDF: {str(e)}")
    
    def add_domain_pdf_content(self, story, results, styles):
        """Agrega contenido específico de dominio al PDF"""
        basic_info = results.get('basic_info', {})
        story.append(Paragraph(f"Dominio: {results.get('domain', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"Estado: {'Activo' if basic_info.get('is_active') else 'Inactivo'}", styles['Normal']))
        story.append(Paragraph(f"IP: {basic_info.get('ip_address', 'N/A')}", styles['Normal']))
        
        # Información WHOIS
        whois_info = results.get('whois_info', {})
        if 'error' not in whois_info:
            story.append(Paragraph("Información WHOIS:", styles['Heading3']))
            story.append(Paragraph(f"Registrador: {whois_info.get('registrar', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"Fecha de creación: {whois_info.get('creation_date', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"Fecha de expiración: {whois_info.get('expiration_date', 'N/A')}", styles['Normal']))
    
    def add_email_pdf_content(self, story, results, styles):
        """Agrega contenido específico de email al PDF"""
        story.append(Paragraph(f"Email: {results.get('email', 'N/A')}", styles['Normal']))
        
        validation = results.get('validation', {})
        story.append(Paragraph(f"Formato válido: {'Sí' if validation.get('format_valid') else 'No'}", styles['Normal']))
        story.append(Paragraph(f"Dominio existe: {'Sí' if validation.get('domain_exists') else 'No'}", styles['Normal']))
        
        breaches = results.get('breaches', {})
        if 'error' not in breaches:
            breach_count = breaches.get('breach_count', 0)
            story.append(Paragraph(f"Brechas encontradas: {breach_count}", styles['Normal']))
    
    def add_username_pdf_content(self, story, results, styles):
        """Agrega contenido específico de username al PDF"""
        story.append(Paragraph(f"Username: {results.get('username', 'N/A')}", styles['Normal']))
        
        stats = results.get('statistics', {})
        story.append(Paragraph(f"Plataformas verificadas: {stats.get('total_platforms_checked', 0)}", styles['Normal']))
        story.append(Paragraph(f"Encontrado en: {stats.get('platforms_found', 0)}", styles['Normal']))
        story.append(Paragraph(f"Disponible en: {stats.get('platforms_not_found', 0)}", styles['Normal']))
    
    def add_social_pdf_content(self, story, results, styles):
        """Agrega contenido específico de redes sociales al PDF"""
        story.append(Paragraph(f"Perfil: {results.get('profile_url', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"Plataforma: {results.get('platform', 'N/A')}", styles['Normal']))
        
        basic_info = results.get('basic_info', {})
        story.append(Paragraph(f"Accesible: {'Sí' if basic_info.get('accessible') else 'No'}", styles['Normal']))
    
    def run(self):
        """Ejecuta la aplicación principal"""
        try:
            # Mostrar aviso ético
            self.show_ethical_notice()
            
            # Mostrar sidebar
            self.show_sidebar()
            
            # Mostrar interfaz principal
            self.show_main_interface()
            
        except Exception as e:
            st.error(f"❌ Error en la aplicación: {str(e)}")
            logger.error(f"Error en aplicación: {e}")

def main():
    """Función principal"""
    try:
        app = OSINTNexusApp()
        app.run()
    except Exception as e:
        st.error(f"❌ Error crítico: {str(e)}")
        logger.error(f"Error crítico: {e}")

if __name__ == "__main__":
    main()