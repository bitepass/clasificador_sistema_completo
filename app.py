"""
OSINT-Nexus: Plataforma de Inteligencia Automatizada
Aplicación principal de Streamlit
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Importar módulos
from config.settings import APP_NAME, APP_VERSION, ETHICAL_WARNINGS, THEME_COLORS
from config.api_keys import api_key_manager
from modules.domain_analyzer import DomainAnalyzer
from modules.email_analyzer import EmailAnalyzer
from modules.username_analyzer import UsernameAnalyzer
from modules.social_analyzer import SocialAnalyzer
from utils.network_graph import NetworkGraphGenerator
from utils.report_generator import ReportGenerator
from utils.data_processor import DataProcessor

# Configuración de la página
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Variables de sesión
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

class OSINTNexusApp:
    """Aplicación principal de OSINT-Nexus"""
    
    def __init__(self):
        self.domain_analyzer = DomainAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        self.username_analyzer = UsernameAnalyzer()
        self.social_analyzer = SocialAnalyzer()
        self.network_generator = NetworkGraphGenerator()
        self.report_generator = ReportGenerator()
        self.data_processor = DataProcessor()
    
    def run(self):
        """Ejecuta la aplicación principal"""
        self._render_header()
        self._render_sidebar()
        self._render_main_content()
        self._render_footer()
    
    def _render_header(self):
        """Renderiza el encabezado de la aplicación"""
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, {THEME_COLORS['primary']}, {THEME_COLORS['secondary']}); color: white; border-radius: 10px; margin-bottom: 2rem;">
                <h1>🕵️ {APP_NAME}</h1>
                <p>Plataforma de Inteligencia Automatizada v{APP_VERSION}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Advertencia ética
        with st.expander("⚠️ Advertencia Ética y Legal", expanded=False):
            for warning in ETHICAL_WARNINGS:
                st.warning(warning)
    
    def _render_sidebar(self):
        """Renderiza la barra lateral"""
        st.sidebar.title("🔧 Configuración")
        
        # Selector de tipo de análisis
        analysis_type = st.sidebar.selectbox(
            "Tipo de Análisis",
            ["Dominio", "Email", "Nombre de Usuario", "Red Social"],
            help="Selecciona el tipo de objetivo a analizar"
        )
        
        # Campo de entrada según el tipo
        if analysis_type == "Dominio":
            target = st.sidebar.text_input(
                "Dominio",
                placeholder="ejemplo.com",
                help="Introduce el dominio a analizar"
            )
        elif analysis_type == "Email":
            target = st.sidebar.text_input(
                "Email",
                placeholder="usuario@ejemplo.com",
                help="Introduce la dirección de email a analizar"
            )
        elif analysis_type == "Nombre de Usuario":
            target = st.sidebar.text_input(
                "Nombre de Usuario",
                placeholder="usuario123",
                help="Introduce el nombre de usuario a buscar"
            )
        else:  # Red Social
            target = st.sidebar.text_input(
                "URL del Perfil",
                placeholder="https://twitter.com/usuario",
                help="Introduce la URL del perfil social a analizar"
            )
        
        # Botón de análisis
        if st.sidebar.button("🚀 Iniciar Análisis", type="primary"):
            if target and target.strip():
                self._run_analysis(analysis_type.lower(), target.strip())
            else:
                st.error("Por favor, introduce un objetivo válido.")
        
        # Estado de APIs
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Estado de APIs")
        self._render_api_status()
        
        # Configuración de reportes
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Reportes")
        if st.session_state.current_analysis:
            if st.sidebar.button("📄 Generar Reporte PDF"):
                self._generate_pdf_report()
    
    def _render_main_content(self):
        """Renderiza el contenido principal"""
        if st.session_state.current_analysis:
            self._render_analysis_results()
        else:
            self._render_welcome()
    
    def _render_welcome(self):
        """Renderiza la página de bienvenida"""
        st.markdown("""
        ## 🎯 Bienvenido a OSINT-Nexus
        
        OSINT-Nexus es una plataforma avanzada de Inteligencia de Fuentes Abiertas que te permite:
        
        ### 🔍 **Análisis de Dominios**
        - Descubre subdominios y infraestructura
        - Identifica tecnologías y vulnerabilidades
        - Analiza certificados SSL y registros DNS
        
        ### 📧 **Análisis de Emails**
        - Verifica existencia y validez
        - Detecta exposiciones en brechas de datos
        - Encuentra perfiles sociales asociados
        
        ### 👤 **Búsqueda de Usuarios**
        - Busca presencia en redes sociales
        - Identifica perfiles en múltiples plataformas
        - Analiza patrones de actividad
        
        ### 🌐 **Análisis de Redes Sociales**
        - Analiza perfiles y conexiones
        - Extrae información de actividad
        - Identifica patrones de comportamiento
        
        ---
        
        ### 🚀 **Para comenzar:**
        1. Selecciona el tipo de análisis en la barra lateral
        2. Introduce el objetivo a investigar
        3. Haz clic en "Iniciar Análisis"
        4. Explora los resultados en las diferentes pestañas
        
        ### 📈 **Características Avanzadas:**
        - **Visualización de Grafos**: Relaciones entre entidades
        - **Reportes PDF**: Informes detallados y profesionales
        - **Correlación de Datos**: Análisis multi-fuente
        - **Exportación**: Múltiples formatos de salida
        """)
    
    def _render_analysis_results(self):
        """Renderiza los resultados del análisis"""
        analysis = st.session_state.current_analysis
        
        # Pestañas de resultados
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Resumen", 
            "🔍 Detalles", 
            "🕸️ Grafo de Relaciones", 
            "📈 Estadísticas",
            "📄 Datos Crudos"
        ])
        
        with tab1:
            self._render_summary_tab(analysis)
        
        with tab2:
            self._render_details_tab(analysis)
        
        with tab3:
            self._render_graph_tab(analysis)
        
        with tab4:
            self._render_statistics_tab(analysis)
        
        with tab5:
            self._render_raw_data_tab(analysis)
    
    def _render_summary_tab(self, analysis):
        """Renderiza la pestaña de resumen"""
        st.header("📊 Resumen del Análisis")
        
        # Información básica
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tipo de Análisis", analysis.get("analysis_type", "N/A"))
        
        with col2:
            st.metric("Objetivo", analysis.get("target", "N/A"))
        
        with col3:
            duration = analysis.get("metadata", {}).get("scan_time", 0)
            st.metric("Duración", f"{duration:.2f}s")
        
        # Estadísticas principales
        stats = analysis.get("statistics", {})
        if stats:
            st.subheader("📈 Estadísticas Principales")
            
            # Crear métricas dinámicas según el tipo de análisis
            if analysis.get("analysis_type") == "domain":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Subdominios", stats.get("total_subdomains", 0))
                with col2:
                    st.metric("IPs", stats.get("total_ips", 0))
                with col3:
                    st.metric("Tecnologías", stats.get("total_technologies", 0))
                with col4:
                    st.metric("Vulnerabilidades", stats.get("total_vulnerabilities", 0))
            
            elif analysis.get("analysis_type") == "email":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Brechas", stats.get("total_breaches", 0))
                with col2:
                    st.metric("Emails Relacionados", stats.get("total_related_emails", 0))
                with col3:
                    st.metric("Perfiles Sociales", stats.get("total_social_profiles", 0))
                with col4:
                    st.metric("Registros Expuestos", stats.get("total_records_exposed", 0))
            
            elif analysis.get("analysis_type") == "username":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Plataformas Verificadas", stats.get("total_platforms_checked", 0))
                with col2:
                    st.metric("Perfiles Encontrados", stats.get("profiles_found", 0))
                with col3:
                    success_rate = stats.get("success_rate", 0) * 100
                    st.metric("Tasa de Éxito", f"{success_rate:.1f}%")
                with col4:
                    platforms = len(stats.get("platforms_with_profiles", []))
                    st.metric("Plataformas con Perfiles", platforms)
        
        # Herramientas utilizadas
        tools_used = analysis.get("metadata", {}).get("tools_used", [])
        if tools_used:
            st.subheader("🛠️ Herramientas Utilizadas")
            for tool in tools_used:
                st.success(f"✅ {tool.title()}")
    
    def _render_details_tab(self, analysis):
        """Renderiza la pestaña de detalles"""
        st.header("🔍 Detalles del Análisis")
        
        analysis_type = analysis.get("analysis_type")
        
        if analysis_type == "domain":
            self._render_domain_details(analysis)
        elif analysis_type == "email":
            self._render_email_details(analysis)
        elif analysis_type == "username":
            self._render_username_details(analysis)
        elif analysis_type == "social":
            self._render_social_details(analysis)
    
    def _render_domain_details(self, analysis):
        """Renderiza detalles de análisis de dominio"""
        # Información del dominio
        domain_info = analysis.get("domain_info", {})
        if domain_info:
            st.subheader("🌐 Información del Dominio")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dominio:**", domain_info.get("domain", "N/A"))
                st.write("**Registrar:**", domain_info.get("registrar", "N/A"))
            
            with col2:
                st.write("**Fecha de Creación:**", domain_info.get("creation_date", "N/A"))
                st.write("**Fecha de Expiración:**", domain_info.get("expiration_date", "N/A"))
        
        # Subdominios
        subdomains = analysis.get("subdomains", [])
        if subdomains:
            st.subheader("🔗 Subdominios Encontrados")
            subdomain_df = pd.DataFrame(subdomains)
            st.dataframe(subdomain_df, use_container_width=True)
        
        # Tecnologías
        technologies = analysis.get("technologies", [])
        if technologies:
            st.subheader("⚙️ Tecnologías Detectadas")
            tech_df = pd.DataFrame(technologies)
            st.dataframe(tech_df, use_container_width=True)
        
        # Vulnerabilidades
        vulnerabilities = analysis.get("vulnerabilities", [])
        if vulnerabilities:
            st.subheader("⚠️ Vulnerabilidades Encontradas")
            vuln_df = pd.DataFrame(vulnerabilities)
            st.dataframe(vuln_df, use_container_width=True)
    
    def _render_email_details(self, analysis):
        """Renderiza detalles de análisis de email"""
        # Información del email
        email_info = analysis.get("email_info", {})
        if email_info:
            st.subheader("📧 Información del Email")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Email:**", email_info.get("email", "N/A"))
                st.write("**Usuario:**", email_info.get("username", "N/A"))
                st.write("**Dominio:**", email_info.get("domain", "N/A"))
            
            with col2:
                st.write("**Existe:**", "✅ Sí" if email_info.get("exists") else "❌ No")
                st.write("**Descartable:**", "✅ Sí" if email_info.get("disposable") else "❌ No")
                st.write("**Webmail:**", "✅ Sí" if email_info.get("webmail") else "❌ No")
        
        # Brechas de datos
        breaches = analysis.get("breaches", [])
        if breaches:
            st.subheader("🔓 Brechas de Datos")
            breach_df = pd.DataFrame(breaches)
            st.dataframe(breach_df, use_container_width=True)
        
        # Emails relacionados
        related_emails = analysis.get("related_emails", [])
        if related_emails:
            st.subheader("👥 Emails Relacionados")
            related_df = pd.DataFrame(related_emails)
            st.dataframe(related_df, use_container_width=True)
    
    def _render_username_details(self, analysis):
        """Renderiza detalles de análisis de username"""
        username = analysis.get("username", "N/A")
        st.subheader(f"👤 Análisis de Usuario: {username}")
        
        # Perfiles encontrados
        profiles = analysis.get("profiles", [])
        if profiles:
            found_profiles = [p for p in profiles if p.get("exists")]
            
            st.write(f"**Perfiles Encontrados:** {len(found_profiles)} de {len(profiles)}")
            
            # Crear DataFrame con perfiles encontrados
            if found_profiles:
                profile_df = pd.DataFrame(found_profiles)
                st.dataframe(profile_df, use_container_width=True)
            
            # Gráfico de plataformas
            platform_counts = {}
            for profile in profiles:
                platform = profile.get("platform", "unknown")
                status = "Encontrado" if profile.get("exists") else "No Encontrado"
                key = f"{platform}_{status}"
                platform_counts[key] = platform_counts.get(key, 0) + 1
            
            if platform_counts:
                fig = px.bar(
                    x=list(platform_counts.keys()),
                    y=list(platform_counts.values()),
                    title="Distribución por Plataforma",
                    labels={"x": "Plataforma", "y": "Cantidad"}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_social_details(self, analysis):
        """Renderiza detalles de análisis social"""
        # Información del perfil
        profile_info = analysis.get("profile_info", {})
        if profile_info:
            st.subheader("👤 Información del Perfil")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Plataforma:**", profile_info.get("platform", "N/A").title())
                st.write("**Usuario:**", profile_info.get("username", "N/A"))
                st.write("**Nombre:**", profile_info.get("display_name", "N/A"))
            
            with col2:
                st.write("**Seguidores:**", profile_info.get("followers_count", "N/A"))
                st.write("**Verificado:**", "✅ Sí" if profile_info.get("verified") else "❌ No")
        
        # Posts
        posts = analysis.get("posts", [])
        if posts:
            st.subheader("📝 Posts Recientes")
            post_df = pd.DataFrame(posts)
            st.dataframe(post_df, use_container_width=True)
        
        # Conexiones
        connections = analysis.get("connections", [])
        if connections:
            st.subheader("🔗 Conexiones")
            connection_df = pd.DataFrame(connections)
            st.dataframe(connection_df, use_container_width=True)
    
    def _render_graph_tab(self, analysis):
        """Renderiza la pestaña de grafo de relaciones"""
        st.header("🕸️ Grafo de Relaciones")
        
        # Generar grafo
        self.network_generator.clear_graph()
        
        # Añadir datos según el tipo de análisis
        analysis_type = analysis.get("analysis_type")
        if analysis_type == "domain":
            self.network_generator.add_domain_data(analysis)
        elif analysis_type == "email":
            self.network_generator.add_email_data(analysis)
        elif analysis_type == "username":
            self.network_generator.add_username_data(analysis)
        elif analysis_type == "social":
            self.network_generator.add_social_data(analysis)
        
        # Generar visualización
        fig = self.network_generator.generate_plotly_graph()
        st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas del grafo
        stats = self.network_generator.generate_statistics()
        if stats:
            st.subheader("📊 Estadísticas del Grafo")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Nodos", stats.get("total_nodes", 0))
            with col2:
                st.metric("Conexiones", stats.get("total_edges", 0))
            with col3:
                st.metric("Densidad", f"{stats.get('density', 0):.3f}")
            with col4:
                st.metric("Componentes", stats.get("connected_components", 0))
    
    def _render_statistics_tab(self, analysis):
        """Renderiza la pestaña de estadísticas"""
        st.header("📈 Estadísticas Detalladas")
        
        # Estadísticas generales
        stats = analysis.get("statistics", {})
        if stats:
            st.subheader("📊 Métricas Principales")
            
            # Crear gráficos según el tipo de análisis
            analysis_type = analysis.get("analysis_type")
            
            if analysis_type == "domain":
                self._render_domain_statistics(stats)
            elif analysis_type == "email":
                self._render_email_statistics(stats)
            elif analysis_type == "username":
                self._render_username_statistics(stats)
            elif analysis_type == "social":
                self._render_social_statistics(stats)
    
    def _render_domain_statistics(self, stats):
        """Renderiza estadísticas de dominio"""
        # Gráfico de tecnologías
        technologies = st.session_state.current_analysis.get("technologies", [])
        if technologies:
            tech_counts = {}
            for tech in technologies:
                name = tech.get("name", "Unknown")
                tech_counts[name] = tech_counts.get(name, 0) + 1
            
            if tech_counts:
                fig = px.pie(
                    values=list(tech_counts.values()),
                    names=list(tech_counts.keys()),
                    title="Distribución de Tecnologías"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_email_statistics(self, stats):
        """Renderiza estadísticas de email"""
        # Gráfico de brechas
        breaches = st.session_state.current_analysis.get("breaches", [])
        if breaches:
            breach_data = []
            for breach in breaches:
                breach_data.append({
                    "Brecha": breach.get("name", "Unknown"),
                    "Registros": breach.get("pwn_count", 0)
                })
            
            if breach_data:
                df = pd.DataFrame(breach_data)
                fig = px.bar(
                    df,
                    x="Brecha",
                    y="Registros",
                    title="Registros Expuestos por Brecha"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_username_statistics(self, stats):
        """Renderiza estadísticas de username"""
        # Gráfico de plataformas
        profiles = st.session_state.current_analysis.get("profiles", [])
        if profiles:
            platform_data = {}
            for profile in profiles:
                platform = profile.get("platform", "Unknown")
                status = "Encontrado" if profile.get("exists") else "No Encontrado"
                key = f"{platform}_{status}"
                platform_data[key] = platform_data.get(key, 0) + 1
            
            if platform_data:
                fig = px.bar(
                    x=list(platform_data.keys()),
                    y=list(platform_data.values()),
                    title="Resultados por Plataforma"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_social_statistics(self, stats):
        """Renderiza estadísticas sociales"""
        # Gráfico de actividad
        posts = st.session_state.current_analysis.get("posts", [])
        if posts:
            engagement_data = []
            for post in posts:
                engagement_data.append({
                    "Post": f"Post {post.get('id', 'Unknown')}",
                    "Likes": post.get("likes", 0),
                    "Retweets": post.get("retweets", 0),
                    "Replies": post.get("replies", 0)
                })
            
            if engagement_data:
                df = pd.DataFrame(engagement_data)
                fig = px.bar(
                    df,
                    x="Post",
                    y=["Likes", "Retweets", "Replies"],
                    title="Engagement por Post",
                    barmode="group"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_raw_data_tab(self, analysis):
        """Renderiza la pestaña de datos crudos"""
        st.header("📄 Datos Crudos")
        
        # Mostrar JSON completo
        st.json(analysis)
        
        # Botones de exportación
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Exportar JSON"):
                self._export_json(analysis)
        
        with col2:
            if st.button("📊 Exportar CSV"):
                self._export_csv(analysis)
        
        with col3:
            if st.button("🕸️ Exportar Grafo"):
                self._export_graph(analysis)
    
    def _render_api_status(self):
        """Renderiza el estado de las APIs"""
        status = api_key_manager.get_service_status()
        
        for service, info in status.items():
            if info["configured"]:
                if info["valid"]:
                    st.success(f"✅ {service.title()}")
                else:
                    st.error(f"❌ {service.title()}")
            else:
                st.info(f"ℹ️ {service.title()} (No configurado)")
    
    def _run_analysis(self, analysis_type: str, target: str):
        """Ejecuta el análisis según el tipo"""
        with st.spinner(f"🔍 Analizando {target}..."):
            try:
                if analysis_type == "dominio":
                    results = self.domain_analyzer.analyze_domain(target)
                elif analysis_type == "email":
                    results = self.email_analyzer.analyze_email(target)
                elif analysis_type == "nombre de usuario":
                    results = self.username_analyzer.analyze_username(target)
                elif analysis_type == "red social":
                    results = self.social_analyzer.analyze_social_profile(target)
                else:
                    st.error("Tipo de análisis no soportado")
                    return
                
                # Procesar datos
                if analysis_type == "dominio":
                    processed_results = self.data_processor.process_domain_data(results)
                elif analysis_type == "email":
                    processed_results = self.data_processor.process_email_data(results)
                elif analysis_type == "nombre de usuario":
                    processed_results = self.data_processor.process_username_data(results)
                elif analysis_type == "red social":
                    processed_results = self.data_processor.process_social_data(results)
                
                # Añadir metadatos
                processed_results["analysis_type"] = analysis_type
                processed_results["target"] = target
                processed_results["timestamp"] = datetime.now().isoformat()
                
                # Guardar en sesión
                st.session_state.current_analysis = processed_results
                st.session_state.analysis_results[target] = processed_results
                
                st.success(f"✅ Análisis completado para {target}")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error durante el análisis: {str(e)}")
    
    def _generate_pdf_report(self):
        """Genera reporte PDF"""
        if st.session_state.current_analysis:
            with st.spinner("📄 Generando reporte PDF..."):
                try:
                    report_path = self.report_generator.generate_report(
                        st.session_state.current_analysis
                    )
                    if report_path:
                        st.success(f"✅ Reporte generado: {report_path}")
                        
                        # Descargar archivo
                        with open(report_path, "rb") as file:
                            st.download_button(
                                label="📥 Descargar Reporte PDF",
                                data=file.read(),
                                file_name=f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error("❌ Error generando el reporte")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    def _export_json(self, data):
        """Exporta datos como JSON"""
        json_str = json.dumps(data, indent=2, default=str)
        st.download_button(
            label="📥 Descargar JSON",
            data=json_str,
            file_name=f"osint_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def _export_csv(self, data):
        """Exporta datos como CSV"""
        # Convertir datos a formato tabular
        if data.get("analysis_type") == "username":
            profiles = data.get("profiles", [])
            if profiles:
                df = pd.DataFrame(profiles)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv,
                    file_name=f"osint_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    def _export_graph(self, data):
        """Exporta grafo de relaciones"""
        try:
            # Generar grafo
            self.network_generator.clear_graph()
            analysis_type = data.get("analysis_type")
            
            if analysis_type == "domain":
                self.network_generator.add_domain_data(data)
            elif analysis_type == "email":
                self.network_generator.add_email_data(data)
            elif analysis_type == "username":
                self.network_generator.add_username_data(data)
            elif analysis_type == "social":
                self.network_generator.add_social_data(data)
            
            # Exportar
            graph_json = self.network_generator.export_graph("json")
            if graph_json:
                st.download_button(
                    label="📥 Descargar Grafo JSON",
                    data=graph_json,
                    file_name=f"osint_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"❌ Error exportando grafo: {str(e)}")
    
    def _render_footer(self):
        """Renderiza el pie de página"""
        st.markdown("---")
        st.markdown(
            f"""
            <div style="text-align: center; color: gray; padding: 1rem;">
                <p>{APP_NAME} v{APP_VERSION} - Desarrollado con ❤️ para la comunidad OSINT</p>
                <p>⚠️ Usar únicamente para investigaciones legítimas y éticas</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Ejecutar aplicación
if __name__ == "__main__":
    app = OSINTNexusApp()
    app.run()